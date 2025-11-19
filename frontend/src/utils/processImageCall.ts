
import { type ImageItem } from "../types/types";

export async function uploadImages(images: ImageItem[], translator: string = 'gemini') {
  try {
    const formData = new FormData();
    images.forEach((image, index) => {
      if (image.file){
        formData.append('files', image.file);
      }
    });

    // Add translator selection to form data
    formData.append('translator', translator);

    const response = await fetch('http://127.0.0.1:8000/translate-images/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed, response was not ok");
    }

    return response.json();

  } catch (error) {
    console.error('Error uploading images:', error);
    throw error;
  }
}