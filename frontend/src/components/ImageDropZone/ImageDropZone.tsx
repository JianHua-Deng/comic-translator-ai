import { useCallback, useEffect, useState } from "react";
import Dropzone, { useDropzone, type FileWithPath } from "react-dropzone";
import PreviewImage from "../../ui/PreviewImage";

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
      'image/jpeg': ['.jpeg', 'jpg'],
      'image/png': ['.png'],
    },
    maxSize: 5 * 1024 * 1024, // file size limiting to 5mb
    onDrop,
  });

  useEffect(() => {

  }, [images])

  function handleDelete(imageToDelete: ImageItem) {
    setImages( (prevImages) => prevImages.filter((img) => imageToDelete !== img) );
  }
  

  return (
    <section className="max-w-full w-4xl h-86 rounded-lg flex flex-col gap-10">
      <div {...getRootProps({
        className: 'flex h-full justify-center items-center p-10 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer bg-gray-200 hover:bg-gray-300 dark:bg-gray-900 dark:hover:bg-gray-600 dark:bg-transparent hover:border-blue-400 transition-colors'
        })}>
        <input {...getInputProps()}/>
        <p className="text-gray-500">Drag some images here, or click to select files</p>
      </div>
      <aside>
        <h4>Uploaded Images</h4>
        <div className="p-3 flex gap-2">
          {
            images.map( (image) => (
              <PreviewImage image={image.objectURL} deleteFunction={() => handleDelete(image)} 
              />
            ))
          }
        </div>
      </aside>
    </section>
  );
}