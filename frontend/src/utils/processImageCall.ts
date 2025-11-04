import { useState } from "react";
import { type ImageItem } from "../types/types";

export async function uploadImages(images: ImageItem[]) {
  try {
    const formData = new FormData();
    images.forEach((image, index) => {
      formData.append('files', image.file);
    });

    const response = await fetch('http://127.0.0.1:8000/translate-images/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed, response was not ok");
    }

  } catch (error) {
    console.error('Error uploading images:', error);
    throw error;
  }
}