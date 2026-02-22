from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List, Optional
import traceback
from app import config
from PIL import Image
import os, io
import zipfile
import asyncio
from app.core.pipeline import MangaTranslationPipeline


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


pipelines = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        pipeline = MangaTranslationPipeline()
        pipelines['pipeline'] = pipeline
        print("Startup Completed")
    except Exception as e:
        print("Start up failed")
        raise e
    
    yield

    print("Shutting down server")
    pipelines.clear()
    
app = FastAPI(lifespan=lifespan)

origins = [
    'http://localhost:5173'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/translated", StaticFiles(directory="output"), name="static")

@app.get("/health")
async def check_health(request: Request):
    print(f"Checked Health")
    return {"status": "ok"}


@app.post("/translate-images/")
async def translate_images_in_batch(
    request: Request,
    files: List[UploadFile] = File(...),
    translator: Optional[str] = Form("gemini")
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    if 'pipeline' not in pipelines:
        raise HTTPException(status_code=500, detail="Server is still initializing")

    print(f"Received {len(files)} image(s) with translator: {translator}")
    
    pipeline = pipelines['pipeline']

    image_list = []
    original_filename = []
    original_file_extensions = []

    for file in files:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        filename, extension = os.path.splitext(file.filename)
        image_list.append(image)
        original_filename.append(filename)
        original_file_extensions.append(extension.lstrip('.'))

    loop = asyncio.get_running_loop()

    try:
        all_text_and_coord_data = await loop.run_in_executor(
            None,
            pipeline.detect_and_extract_text,
            image_list
        )

        all_translated_data = await pipeline.translate_all_texts(
            all_text_and_coord_data,
            translator
        )

        processed_images = await loop.run_in_executor(
            None,
            pipeline.inpaint_and_render, 
            all_translated_data,
            image_list
        )

        #processed_images = await pipeline.process_images(image_list)

    except Exception as e:
        print(f"Error during image processing: {e}")
        raise HTTPException(status_code=500, detail=f"Something went wrong and inpaint process failed")
    
    translated_file_names = save_images(processed_images, original_filename, original_file_extensions)
    
    json_res = {}
    for index, name in enumerate(translated_file_names):
        json_res[f'image_{index}'] ={
            'imageUrl': f'{request.base_url}translated/{name}',
            'name': name,
        }
    
    print(json_res)

    return JSONResponse(content=json_res, status_code=201, media_type='application/json')



def save_images(processed_images, original_filename, original_file_extensions):
    translated_file_names = []
    for img, orig_name, orig_ext in zip(processed_images, original_filename, original_file_extensions):
        final_file_name = f'{orig_name}_translated.{orig_ext}'
        output_path = os.path.join(config.OUTPUT_DIR, final_file_name)
        
        img.save(output_path)

        translated_file_names.append(final_file_name)
    return translated_file_names

def create_zip(processed_images, original_filename, original_file_extensions):

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:

        # Creating a buffer for each individual image
        for image_index, image in enumerate(processed_images):

            img_buffer = io.BytesIO()

            save_format = original_file_extensions[image_index].upper()
            if save_format == 'JPG':
                save_format = 'JPEG'           

            image.save(img_buffer, format=save_format) # This should be changed later to match the user's image extension
            img_buffer.seek(0)

            # Write the image bytes to the zip file
            zip_file.writestr(f'translated_{original_filename[image_index]}.{original_file_extensions[image_index]}', img_buffer.read())



        # Go back to the beginning of the Zip buffer stream before sending
        zip_buffer.seek(0)

    return zip_buffer

    """
    # Returning the ZIP file as a streaming response
    headers = {"Content-Disposition": "attachment; filename=translated_images.zip"}
    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)
    """