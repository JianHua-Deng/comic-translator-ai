import { useCallback, useEffect, useState, type Dispatch, type SetStateAction } from "react";
import Dropzone, { useDropzone, type FileWithPath } from "react-dropzone";
import PreviewImage from "../../ui/PreviewImage";
import Button from "../../ui/Button";
import { type ImageItem } from "../../types/types";
import { uploadImages } from "../../utils/processImageCall";
import PreviewZone from "../PreviewZone/PreviewZone";

interface ImageDropZoneProp {
  images: ImageItem[];
  processedImagesUrl: ImageItem[];
  isProcessing: boolean;
  setImages: Dispatch<SetStateAction<ImageItem[]>>;
  setProcessedImagesUrl: Dispatch<SetStateAction<ImageItem[]>>;
  setIsProcessing: Dispatch<SetStateAction<boolean>>;
}

export default function ImageDropZone({ images, processedImagesUrl, isProcessing, setImages, setProcessedImagesUrl, setIsProcessing}: ImageDropZoneProp) {

  const onDrop = useCallback( (acceptedFiles: FileWithPath[]) => {
    const newImages = acceptedFiles.map((imageFile) => ({
      objectURL: URL.createObjectURL(imageFile),
      file: imageFile,
      fileName: imageFile.name,
    }));

    setImages(prevImages => [...prevImages, ...newImages]);
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/jpeg': ['.jpeg', '.jpg'],
      'image/png': ['.png'],
    },
    maxSize: 5 * 1024 * 1024, // file size limiting to 5mb
    onDrop,
  });


  function handleDelete(imageToDelete: ImageItem) {
    setImages( (prevImages) => prevImages.filter((img) => imageToDelete !== img) );
  }
  

  return (
    <section className="w-full max-w-4xl max-h-full rounded-lg flex flex-col">
      <div className="w-full h-full flex flex-col gap-10">
        <div {...getRootProps({
          className: 'flex min-h-86 max-h-full justify-center items-center p-10 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer bg-gray-200 hover:bg-gray-300 dark:bg-gray-900 dark:hover:bg-gray-600 dark:bg-transparent hover:border-blue-400 transition-colors'
          })}>
          <input {...getInputProps()}/>
          <p className="text-gray-500">Drag your RAW Japanese manga images here, or click to select files</p>
        </div>
        {
          images.length !== 0 && (
            <aside className="max-h-80 overflow-y-auto">
              <h4>Uploaded Images</h4>
              <div className="p-3 flex flex-wrap gap-2">
                {
                  images.map( (image) => (
                    <PreviewImage key={image.objectURL} image={image.objectURL} deleteFunction={() => handleDelete(image)} 
                    />
                  ))
                }
              </div>
  
            </aside>
          ) 
        }
  
        {images.length !== 0 && 
        <div className="flex justify-end">
          <Button text={'Submit'} onClick={async () => {
              try {
                setIsProcessing(true);
                const resp = await uploadImages(images);
                console.log('Response from uploadImages:', resp);
                const imageList = Object.values(resp).map((item: any) => ({
                  objectURL: item.imageUrl,
                  fileName: item.name,
                }));
                console.log(imageList);
                setProcessedImagesUrl(imageList);

              } catch (error) {
                console.error('Error uploading images:', error);
                throw error;
              } finally {
                setIsProcessing(false);
              }
            }
          }/>
        </div>}  
      </div>
    </section>
  );
}