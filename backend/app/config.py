# This is where all the necessary variable will be placed, such as env variables
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
INPUT_DIR = os.path.join(PROJECT_ROOT, 'input')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
FONT_PATH = os.path.join(APP_ROOT, 'assets', 'fonts', 'arial.ttf')

DETECTOR_MODEL_ID = "ogkalu/comic-text-and-bubble-detector"

DEVICE = "cpu"
DETECTION_CONFIDENCE = 0.80
IOU_THRESHOLD = 0.3