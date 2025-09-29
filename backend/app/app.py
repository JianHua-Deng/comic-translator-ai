from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
import traceback
from app import config
from PIL import Image
import os
import zipfile
import asyncio
from app.core.pipeline import MangaTranslationPipeline

# Entry point for our backend services with FastAPI
app = FastAPI()

async def main():
    try:
        pipeline = MangaTranslationPipeline()
        print("Pipeline created successfully.", flush=True)
        await pipeline.translate_from_folder()

    except Exception as e:
        print("Pipeline run failed:", flush=True)
        traceback.print_exc()

if __name__ == "__main__":
    # Run the async main; asyncio.run will create and close the loop cleanly.
    asyncio.run(main())


""""

@app.post("/translate-images/")

async def translate_images_in_batch(files: List[UploadFile] = File(...)):

    image_list = []
    original_filename = []
    original_file_extensions = []



    for file in files:

        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        filename, extension = os.path.splitext(file.filename)
        image_list.append(image)
        original_filename.append(filename)
        original_file_extensions.append(extension)



        processed_images = await pipeline.process_images(image_list)
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:

            # Creating a buffer for each individual image
            for image_index, image in enumerate(processed_images):

            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG") # This should be changed later to match the user's image extension
            img_buffer.seek(0)

            # Write the image bytes to the zip file
            zip_file.writestr(f'translated_{original_filename[image_index]}', img_buffer.read())



        # Go back to the beginning of the Zip buffer stream before sending
        zip_buffer.seek(0)

    # Returning the ZIP file as a streaming response
    return StreamingResponse(zip_buffer, media_type='application/zip', headers={'Content-Disposition': 'attachment; filename=translated_manga.zip'})

"""