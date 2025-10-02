print("[BubbleDetector] importing transformers/torch - this can take a while", flush=True)
from transformers import RTDetrV2ForObjectDetection, RTDetrImageProcessor
import torch
from app import config
import os
print("[BubbleDetector] transformers/torch imported", flush=True)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)

class BubbleDetector:
    def __init__(self):
        
        self.processor = RTDetrImageProcessor.from_pretrained(config.DETECTOR_MODEL_ID)
        self.model = RTDetrV2ForObjectDetection.from_pretrained(config.DETECTOR_MODEL_ID).to(config.DEVICE)
        self.device = config.DEVICE


    def detect(self, image_list):
        # processing input
        input = self.processor(images=image_list, return_tensors='pt').to(self.device)

        # inference
        with torch.no_grad():
            outputs = self.model(**input)

        target_sizes = torch.tensor([img.size[::-1] for img in image_list], device=self.device)
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=config.DETECTION_CONFIDENCE)

        return results
