from PIL import Image, ImageDraw, ImageFilter
from app import config
import os, glob, math
import cv2
import numpy as np

from app.processing.bubble_detection import BubbleDetector
from app.processing.ocr import OcrProcessor
from app.processing.inpainting import InPainter
from app.processing.translation import TextTranslator
from app.utils.box_calculations import group_by_iou, shrink_box, enlarge_box
from app.utils.render_box import draw_text_in_box

print("[Pipeline Imports] All imports successful.")



class MangaTranslationPipeline:
    def __init__(self, translator_option='google'):

        self.detector = BubbleDetector()
        self.ocr = OcrProcessor()
        self.translator = TextTranslator()
        self.inpainter = InPainter()
        self.bubble_map = {0: "bubble", 1: "text_bubble", 2: "text_free"}
    
    # This runs detection and OCR
    def detect_and_extract_text(self, image_list):
        """
        Runs the CPU-bound detection and OCR steps.
        This is a synchronous, blocking function.
        """
        # Detect all the text bubbles and corresponding coordinates from the images
        all_raw_results = self.detector.detect(image_list)
        # Structure, group and get the original text from the images
        all_text_and_coord_data = self.get_text_data_from_detections(all_raw_results, image_list)

        return all_text_and_coord_data
    
    # This runs inpainting and rendering
    def inpaint_and_render(self, all_translated_data, image_list):

        # Inpaint the original text area
        cleaned_images = self.inpaint_images(all_translated_data, image_list)
        # Render the final translated text onto the cleaned images
        final_images = self.render_text(all_translated_data, cleaned_images)
        
        self.debug_draw_boxes_raw(final_images, all_translated_data, save_prefix="debug_simple")
        return final_images
    

    async def translate_from_folder(self):
        image_extensions = ('*.jpg', '*.jpeg', '*.png')
        image_paths = []

        for ext in image_extensions:
            image_paths.extend(glob.glob(os.path.join(config.INPUT_DIR, ext)))

        if not image_paths:
            return []

        image_list = [Image.open(path).convert('RGB') for path in image_paths]

        all_text_data = self.detect_and_extract_text(image_list)

        all_translated_data = await self.translate_all_texts(all_text_data)

        final_images = self.inpaint_and_render(all_translated_data, image_list)

        # Saving the final results
        for i, final_image in enumerate(final_images):
            original_filename = os.path.basename(image_paths[i])
            filename, extension = os.path.splitext(original_filename)

            output_filename = f'{filename}_translated{extension}'
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)

            final_image.save(output_path)
            print(f'saved translated image to: {output_path}')


    def get_text_data_from_detections(self, all_raw_results, image_list):
        text_and_coords = {}
        # First structure the raw result we got
        for image_index, (image, single_image_results) in enumerate(zip(image_list, all_raw_results)):
            detections = {}
            max_width, max_height = image.size
            for box_index, (score, label, coord) in enumerate(zip(single_image_results['scores'], single_image_results['labels'], single_image_results['boxes'])):
                label_value = int(label.item())
                detections[box_index] = {
                    'label': self.bubble_map.get(label_value),
                    'coordinates': [float(c) for c in coord],
                    'confidance_score': float(score),
                }

            # Group the bubbles
            grouped_bubbles = group_by_iou(detections, iou_threshold=0.3)

            # Crop all the bubbles in this image and run OCR
            image_text_data = {}
            for bubble_index, data in grouped_bubbles.items():
                if 'bubble' not in data:
                    continue
            
                bubble_coords = data['bubble']
                text_bubble_coords = data.get('text_bubble', shrink_box(bubble_coords, max_width=max_width, max_height=max_height)) # Either get the text bubble coords, or if doesn't exist, use the shrink version of bubble coords
                #text_bubble_coords = adjust_box_height(text_bubble_coords, bubble_coords) # Adjust and increase the height of the box if it is too small (For example, a single Jap word translating to english will make it appear small after rerender)

                if bubble_coords and len(bubble_coords) == 4:
                    crop = image.crop(bubble_coords)
                else:
                    crop = image.crop(text_bubble_coords)

                text = self.ocr.extract_text(crop)

                image_text_data[bubble_index] = {
                    "bubble_coordinates": bubble_coords,
                    "text_bubble_coordinates": text_bubble_coords,
                    "original_text": text,
                }

            text_and_coords[image_index] = image_text_data
            print(text_and_coords)

        return text_and_coords
    
    
    async def translate_all_texts(self, all_text_data, translator_option: str):
        # Collect all text into a single list for batch translation
        original_texts = []
        for img_data in all_text_data.values():
            for bubble in img_data.values():
                original_texts.append(bubble['original_text'])

        translated_texts = await self.translator.translate_batch(original_texts, translator_option=translator_option)

        translated_iter = iter(translated_texts)

        for img_data in all_text_data.values():
            for bubble in img_data.values():
                bubble['translated_text'] = next(translated_iter, bubble['original_text']) # bubble['original_text'] serve as a fall back here in case translation failed

        return all_text_data
    
    # Erase the original text by filling it with white color
    def erase_by_filling(self, text_and_coords, image_list):
        erased_images = []
        for image_index, image in enumerate(image_list):
            orig_img = image.copy()
            draw = ImageDraw.Draw(orig_img)

            if image_index in text_and_coords:
                for bubble in text_and_coords[image_index]:
                    box_to_fill = bubble.get('text_bubble_coordinates')
                    if box_to_fill:
                        draw.rectangle(box_to_fill, fill='white')

            erased_images.append(orig_img)
        
        return erased_images
    

    def inpaint_images(self, text_and_coords, image_list):

        stride = 8

        inpainted_images = []
        for image_index, image in enumerate(image_list):
            width, height = image.size
            mask = Image.new('L', (width, height), 0) # L for grayscale
            draw = ImageDraw.Draw(mask)

            if image_index in text_and_coords:
                for bubble in text_and_coords[image_index].values():
                    coords_to_inpaint = bubble.get('text_bubble_coordinates')
                    if coords_to_inpaint:
                        #coords_to_inpaint = enlarge_box(coords_to_inpaint, width, height) # Enlarge the mask by a bit so that it has higher probability of not leaving any marks
                        draw.rectangle(coords_to_inpaint, fill='white')

            # Pad to Stride required for LaMa model since the dimension needs to be divisible by 8
            new_w = math.ceil(width/stride) * stride
            new_h = math.ceil(height/stride) * stride

            pad_w = new_w - width
            pad_h = new_h - height

            if pad_w > 0 or pad_h > 0:

                # Pad image with gray
                img_padded = Image.new(image.mode, (new_w, new_h), (128, 128, 128))
                img_padded.paste(image, (0, 0))

                # Pad mask with black
                mask_padded = Image.new(mask.mode, (new_w, new_h), 0)
                mask_padded.paste(mask, (0, 0))

            else:
                img_padded = image
                mask_padded = mask
            
            cleaned_image = self.inpainter.inpaint(img_padded, mask_padded)

            if pad_w > 0 or pad_h > 0:
                final_image = cleaned_image.crop((0, 0, width, height))
            else:
                final_image = cleaned_image

            final_image.save(os.path.join(config.OUTPUT_DIR, f'{image_index}_debug_inpainted.png'))
            inpainted_images.append(final_image)
        
        return inpainted_images



    def render_text(self, all_translated_data, inpainted_images):
        final_images = []

        for image_index, image in enumerate(inpainted_images):
            draw = ImageDraw.Draw(image)
            if image_index in all_translated_data:
                for bubble in all_translated_data[image_index].values():
                    if bubble['text_bubble_coordinates']:
                        translated_text = bubble.get('translated_text', "")

                        bubble['translated_text'] = translated_text
                        draw_text_in_box(draw, bubble['text_bubble_coordinates'], bubble['translated_text'], config.FONT_PATH)
            
            final_images.append(image)
        
        return final_images
    


    # AI generated function to draw boxes around detected boxes for me to debug, didn't proofread the codes or anything 
    def debug_draw_boxes_raw(self, images, all_translated_data, save_prefix="debug"):
        """
        - images: list of PIL.Image objects (inpainted_images or final_images)
        - all_translated_data: mapping image_index -> {bubble_index: {...}}
        - saves images to config.OUTPUT_DIR named {save_prefix}_img_{i}.png
        """

        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        for img_idx, img in enumerate(images):
            out_img = img.copy()
            draw = ImageDraw.Draw(out_img)

            if img_idx not in all_translated_data:
                print(f"[debug_simple] img={img_idx} - no detections", flush=True)
            else:
                for bubble_idx, bubble in all_translated_data[img_idx].items():
                    bubble_coords = bubble.get("bubble_coordinates")
                    text_coords = bubble.get("text_bubble_coordinates")
                    translated = bubble.get("translated_text", "")
                    original = bubble.get("original_text", "")

                    # Draw bubble box (blue) exactly as provided
                    if bubble_coords:
                        try:
                            draw.rectangle(bubble_coords, outline="blue", width=2)
                        except Exception as e:
                            print(f"[debug_simple] img={img_idx} bubble={bubble_idx} draw bubble_rect failed: {e}", flush=True)

                    # Draw text_bubble box (green) exactly as provided
                    if text_coords:
                        try:
                            draw.rectangle(text_coords, outline="green", width=2)
                        except Exception as e:
                            print(f"[debug_simple] img={img_idx} bubble={bubble_idx} draw text_rect failed: {e}", flush=True)

                    # Try to render translated text inside the text_coords if present,
                    # otherwise try bubble_coords. This uses your current draw_text_in_box.
                    target_box = text_coords or bubble_coords
                    if target_box:
                        try:
                            # NOTE: this will behave exactly as your current draw_text_in_box does
                            draw_text_in_box(draw, target_box, translated or original, config.FONT_PATH)
                        except Exception as e:
                            print(f"[debug_simple] img={img_idx} bubble={bubble_idx} draw_text_in_box failed: {e}", flush=True)

                    # Terminal summary (raw values shown)
                    preview = (translated or original)[:140].replace("\n", " ")
                    print(f"[debug_simple] img={img_idx} bubble={bubble_idx} bubble_coords={bubble_coords} text_coords={text_coords} preview='{preview}'", flush=True)

            out_path = os.path.join(config.OUTPUT_DIR, f"{save_prefix}_img_{img_idx}.png")
            try:
                out_img.save(out_path)
                print(f"[debug_simple] saved {out_path}", flush=True)
            except Exception as e:
                print(f"[debug_simple] failed to save img {img_idx}: {e}", flush=True)
