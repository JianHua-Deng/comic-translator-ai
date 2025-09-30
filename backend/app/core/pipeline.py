print("[Pipeline] start import", flush=True)
from PIL import Image, ImageDraw
from app import config
import os, glob, math
print("[Pipeline Imports] Starting...")

from app.processing.bubble_detection import BubbleDetector
print("[Pipeline Imports] <-- BubbleDetector Imported.")

from app.processing.ocr import OcrProcessor
print("[Pipeline Imports] <-- OcrProcessor Imported.")

from app.processing.inpainting import InPainter
print("[Pipeline Imports] <-- InPainter Imported.")

from app.processing.translation import TextTranslator
print("[Pipeline Imports] <-- TextTranslator Imported.")

from app.utils.box_calculations import group_by_iou, shrink_box
from app.utils.render_box import draw_text_in_box

print("[Pipeline Imports] All imports successful.")
print("[Pipeline] finished top-level imports, next: bubble_detector import (should appear next)", flush=True)


class MangaTranslationPipeline:
    def __init__(self):
        print("Initializing MangaTranslationPipeline...")
        self.detector = BubbleDetector()
        print("BubbleDetector loaded.")
        self.ocr = OcrProcessor()
        print("OcrProcessor loaded.")
        self.translator = TextTranslator()
        print("extTranslator loaded.")
        self.inpainter = InPainter()
        print("InPainter loaded.")
        self.bubble_map = {0: "bubble", 1: "text_bubble", 2: "text_free"}
        print("Finished Initializing Pipeline.")
    
    async def process_images(self, image_list):
        
        # Detect all the text bubbles and corresponding coordinates from the images
        all_raw_results = self.detector.detect(image_list)
        # Structure, group and get the original text from the images
        all_text_and_coord_data = self.get_text_data_from_detections(all_raw_results, image_list)
        # Translated all the text from all the images in one batch
        all_translated_data = await self.translate_all_texts(all_text_and_coord_data)
        # Inpaint the original text area
        cleaned_images = self.inpaint_images(all_translated_data, image_list)
        # Render the final translated text onto the cleaned images
        final_images = self.render_text(all_translated_data, cleaned_images)
        
        # self.debug_draw_boxes_raw(final_images, all_translated_data, save_prefix="debug_simple") # Debugging function, use it if there's something gouing wrong


        return final_images

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

        return text_and_coords
    

    async def translate_from_folder(self):
        image_extensions = ('*.jpg', '*.jpeg', '*.png')
        image_paths = []

        for ext in image_extensions:
            image_paths.extend(glob.glob(os.path.join(config.INPUT_DIR, ext)))

        if not image_paths:
            return []
        
        image_list = [Image.open(path).convert('RGB') for path in image_paths]

        # Run the pipeline
        final_images = await self.process_images(image_list)

        # Saving the final results
        for i, final_image in enumerate(final_images):
            original_filename = os.path.basename(image_paths[i])
            filename, extension = os.path.splitext(original_filename)

            output_filename = f'{filename}_translated{extension}'
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)

            final_image.save(output_path)
            print(f'saved translated image to: {output_path}')
    
    
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
    

    def inpaint_images(self, all_translated_data, image_list, max_dim: int = 812):
        """
        Rescale -> inpaint -> rescale back -> composite.
        Put this method INSIDE the MangaTranslationPipeline class.
        max_dim: max size of long edge during inpainting (512/768/1024)
        """
        inpainted_images = []

        for image_index, image in enumerate(image_list):
            width, height = image.size

            # Build binary mask 'L' with white=mask (255)
            mask = Image.new('L', (width, height), 0)
            draw = ImageDraw.Draw(mask)

            if image_index in all_translated_data:
                for bubble in all_translated_data[image_index].values():
                    coords_to_inpaint = bubble.get('text_bubble_coordinates') or bubble.get('bubble_coordinates')
                    if coords_to_inpaint:
                        # coords are expected as [x1, y1, x2, y2]
                        draw.rectangle(coords_to_inpaint, fill=255)

            # Decide whether to downscale
            long_side = max(width, height)
            if long_side > max_dim:
                scale = max_dim / float(long_side)
                new_w = max(1, int(round(width * scale)))
                new_h = max(1, int(round(height * scale)))

                img_small = image.resize((new_w, new_h), Image.LANCZOS)
                mask_small = mask.resize((new_w, new_h), Image.NEAREST)
            else:
                scale = 1.0
                img_small = image
                mask_small = mask

            # Run inpainting on smaller image
            inpainted_small = self.inpainter.inpaint(img_small, mask_small)

            # If the inpaint returns numpy array convert to PIL
            if not isinstance(inpainted_small, Image.Image):
                try:
                    inpainted_small = Image.fromarray(inpainted_small)
                except Exception:
                    # fallback: keep original image if conversion fails
                    inpainted_images.append(image)
                    continue

            # Upscale back if we downscaled
            if scale != 1.0:
                inpainted_up = inpainted_small.resize((width, height), Image.BILINEAR)
            else:
                inpainted_up = inpainted_small

            # Composite: where mask==255 use inpainted_up, else keep original
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
