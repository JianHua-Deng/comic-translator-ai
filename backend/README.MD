## How It Works: The Translation Pipeline

The core logic is managed by the `MangaTranslationPipeline` class. When an image is processed, it goes through the following steps in sequence:

1.  **Image Loading**: The pipeline loads images from the `/input` directory (At least for now)
2.  **Speech Bubble Detection** (`bubble_detection.py`): A computer vision model scans the image to identify the coordinates of all speech bubbles.
3.  **Text Recognition (OCR)** (`ocr.py`): For each detected bubble, an Optical Character Recognition (OCR) model extracts the original text (e.g., Japanese).
4.  **Inpainting** (`inpainting.py`): The original text within each bubble is "erased" or "painted over," creating a clean slate for the translation. This is done using the bubble coordinates and a mask. (Currently using a Lama model, which is very slow, might switch it to something else)
5.  **Translation** (`translation.py`): The extracted text is sent to a translation service or model to be translated into the target language (we are only focusing on English for now).
6.  **Text Rendering** (`render_box.py`): The translated text is drawn back onto the inpainted speech bubbles on the image. The font size and placement are calculated to fit the text neatly.
7.  **Saving Output**: The final translated image is saved to the `/output` directory.

## Folder Structure

```
backend/
├── app/
│   ├── core/
│   │   └── pipeline.py       # Main pipeline orchestrator
│   ├── processing/
│   │   ├── bubble_detection.py # Step 2
│   │   ├── ocr.py              # Step 3
│   │   ├── inpainting.py       # Step 4
│   │   └── translation.py      # Step 5
│   ├── utils/
│   │   └── render_box.py       # Step 6
│   └── app.py                # FastAPI server and local run script
├── input/                    # Place images to be translated here
├── output/                   # Translated images will be saved here
└── requirements.txt          # Project dependencies
```

## Setup and Installation

### Prerequisites
*   Python 3.9+

### Installation

1.  **Go in to the Backend diretory and create a Virtual Environment:**

    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    # Create the virtual environment
    python -m venv .venv

    # Activate it (on Windows)
    .\.venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    Install all the required Python packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## How to Run (On Window)

There are two ways to run this application: as a local script to process a folder of images, or as a web server with an API endpoint (Currently the endpoint are commented out, I haven't tested it yet).

### 1. Local Folder Processing

This method is ideal for testing or batch processing a folder of comics.

1.  Place all the comic pages you want to translate into the `/input` directory.
2.  From the `backend` directory, run the following command in your terminal:
    ```bash
    python -m app.app
    ```
3.  The script will process each image in the `/input` folder and save the translated versions in the `/output` folder.

### 2. As a Web Server (FastAPI)

This method runs a web server, allowing you to send images for translation via an API.

1.  To start the server, run the following command from the `backend` directory:
    ```bash
    uvicorn app.app:app --reload
    ```
2.  The server will be running at `http://127.0.0.1:8000`.
3.  You can then send a `POST` request with image files to the `/translate-images/` endpoint to get back a `.zip` file containing the translated images.

## Achknowledgement

