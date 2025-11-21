from PIL import Image, ImageDraw, ImageFilter
from app import config
import os, glob, math
import cv2
import numpy as np

from app.processing.bubble_detection import BubbleDetector
from app.processing.ocr import OcrProcessor
from app.processing.inpainting import InPainter
from app.processing.translation import TextTranslator
from app.utils.box_calculations import group_by_iou, shrink_box
from app.utils.render_box import draw_text_in_box

print("[Pipeline Imports] All imports successful.")



class MangaTranslationPipeline:
    def __init__(self, translator_option='gemini'):

        self.detector = BubbleDetector()
        self.ocr = OcrProcessor()
        self.translator = TextTranslator(translator_option)
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
                text_bubble_coords = data.get('text_bubble', shrink_box(bubble_coords)) # Either get the text bubble coords, or if doesn't exist, use the shrink version of bubble coords
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
    
    
    async def translate_all_texts(self, all_text_data):
        # Collect all text into a single list for batch translation
        original_texts = []
        for img_data in all_text_data.values():
            for bubble in img_data.values():
                original_texts.append(bubble['original_text'])

        translated_texts = await self.translator.translate_batch(original_texts)

        translated_iter = iter(translated_texts)

        for img_data in all_text_data.values():
            for bubble in img_data.values():
                bubble['translated_text'] = next(translated_iter, bubble['original_text']) # bubble['original_text'] serve as a fall back here in case translation failed

        return all_text_data
    

    def inpaint_images(self, all_translated_data, image_list, max_dim: int = 896, pad_stride: int = 8):
        """
        Rescale: adding strade padding -> inpaint -> crop -> rescale. max_dim should be 768 or 1024 for best result, the higher the better the quality, but loses performance speed
        - dilate_px: expand mask by this many pixels (helps blending).
        - feather_radius: Gaussian blur radius for final soft mask (in pixels).
        - pad_stride: pad small image to multiples of this stride (many LaMa variants like powers of 8).
        """
        inpainted_images = []

        for image_index, image in enumerate(image_list):
            width, height = image.size

            # Build binary mask 'L' (white=mask)
            mask = Image.new('L', (width, height), 0)
            draw = ImageDraw.Draw(mask)
            if image_index in all_translated_data:
                for bubble in all_translated_data[image_index].values():
                    coords_to_inpaint = bubble.get('text_bubble_coordinates') or bubble.get('bubble_coordinates')
                    if coords_to_inpaint:
                        draw.rectangle(coords_to_inpaint, fill=255)


            # Downscale decision
            long_side = max(width, height)
            if long_side > max_dim:
                scale = max_dim / float(long_side)
                new_w = max(1, int(round(width * scale)))
                new_h = max(1, int(round(height * scale)))
                img_small = image.resize((new_w, new_h), Image.LANCZOS)
                # For inpaint we want hard mask (nearest)
                mask_small = mask.resize((new_w, new_h), Image.NEAREST)
            else:
                scale = 1.0
                img_small = image.copy()
                mask_small = mask.copy()

            # Adds extra pixels (padding) so the image dimensions become multiples of the variable "stride", such so the model avoids edge artifacts
            def pad_to_stride(pil_img, stride, fill=0):
                w, h = pil_img.size
                new_w = math.ceil(w / stride) * stride
                new_h = math.ceil(h / stride) * stride
                if new_w == w and new_h == h:
                    return pil_img, (0, 0)
                canvas = Image.new(pil_img.mode, (new_w, new_h), fill)
                canvas.paste(pil_img, (0, 0))
                return canvas, (new_w - w, new_h - h)

            img_padded, pad_amount = pad_to_stride(img_small, pad_stride, fill=(128,128,128) if img_small.mode=='RGB' else 0)
            mask_padded, _ = pad_to_stride(mask_small, pad_stride, fill=0)

            inpainted_padded = self.inpainter.inpaint(img_padded, mask_padded)

            # Convert numpy -> PIL if needed
            if not isinstance(inpainted_padded, Image.Image):
                inpainted_padded = Image.fromarray(inpainted_padded)

            # Remove padding if present (crop back to original small size)
            pad_right, pad_bottom = pad_amount
            if pad_right > 0 or pad_bottom > 0:
                wpad, hpad = img_padded.size
                crop_w = wpad - pad_right
                crop_h = hpad - pad_bottom
                inpainted_small = inpainted_padded.crop((0, 0, crop_w, crop_h))
            else:
                inpainted_small = inpainted_padded

            # Upscale back to original size
            if scale != 1.0:
                inpainted_up = inpainted_small.resize((width, height), Image.BICUBIC)
            else:
                inpainted_up = inpainted_small


            # Composite using soft mask (PIL composite uses mask values 0..255 to blend)
            final = Image.composite(inpainted_up, image, mask)

            inpainted_images.append(final)

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
        from PIL import ImageDraw
        import os
        # use your existing draw_text_in_box (must be importable)
        from app.utils.render_box import draw_text_in_box

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
