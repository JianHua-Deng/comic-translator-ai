import JSZip from "jszip";
import type { ImageItem } from "../types/types";

export async function download_zip(imageItem: ImageItem[]) {
  const zip = new JSZip();

  for (const item of imageItem) {
    try {
      const resp = await fetch(item.objectURL);
      const blob = resp.blob();
      const fileName = item.fileName;
      zip.file(fileName, blob);
    } catch (error) {
      console.error(`Error fetching image from ${item.objectURL}:`, error);
    }
  }

  try {
    const zipData = await zip.generateAsync({ type: 'blob' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(zipData);
    link.download = 'translated.zip';
    document.body.appendChild(link);
    link.click()
    document.body.removeChild(link);

  } catch (error) {
    console.error('Error generating or downloading zip file', error);
  }

}