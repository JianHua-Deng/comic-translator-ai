import { useCallback, useEffect, useState } from "react";
import Dropzone, { useDropzone, type FileWithPath } from "react-dropzone";
import PreviewImage from "../../ui/PreviewImage";
import Button from "../../ui/Button";


interface ImageItem {
  objectURL: string;
  file: FileWithPath;
}

export default function ImageDropZone() {

  const [images, setImages] = useState<ImageItem[]>([]);

  const onDrop = useCallback( (acceptedFiles: FileWithPath[]) => {
    const newImages = acceptedFiles.map((imageFile) => ({
      objectURL: URL.createObjectURL(imageFile),
      file: imageFile
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
    <section className="max-w-full max-h-full w-4xl rounded-lg flex flex-col gap-10">
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
        <Button text={'Submit'} onClick={() => {}}/>
      </div>}  
    </section>
  );
}