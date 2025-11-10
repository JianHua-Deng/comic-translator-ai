# This is where all the necessary variable will be placed, such as env variables
import os
import torch
SERVER_URL = 'http://127.0.0.1:8000'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
INPUT_DIR = os.path.join(PROJECT_ROOT, 'input')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
FONT_PATH = os.path.join(APP_ROOT, 'assets', 'fonts', 'NotoSans-Regular.ttf')

DETECTOR_MODEL_ID = "ogkalu/comic-text-and-bubble-detector"


if torch.cuda.is_available():
    DEVICE = 'cuda'
    print(f'running in cuda, cuda: {torch.cuda.is_available()}')
else:
    DEVICE = 'cpu'
    print(f'running in cpu, cuda: {torch.cuda.is_available()}')
DETECTION_CONFIDENCE = 0.80
IOU_THRESHOLD = 0.3