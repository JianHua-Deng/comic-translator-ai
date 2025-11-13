import { useCallback, type Dispatch, type SetStateAction } from "react";
import { useDropzone, type FileWithPath } from "react-dropzone";
import PreviewImage from "../../ui/PreviewImage";
import Button from "../../ui/Button";
import { type ImageItem } from "../../types/types";
import { uploadImages } from "../../utils/processImageCall";

interface ImageDropZoneProp {
  images: ImageItem[];
  processedImagesUrl: ImageItem[];
  isProcessing: boolean;
  setImages: Dispatch<SetStateAction<ImageItem[]>>;
  setProcessedImagesUrl: Dispatch<SetStateAction<ImageItem[]>>;
  setIsProcessing: Dispatch<SetStateAction<boolean>>;
}

export default function ImageDropZone({
  images,
  processedImagesUrl,
  isProcessing,
  setImages,
  setProcessedImagesUrl,
  setIsProcessing,
}: ImageDropZoneProp) {
  const onDrop = useCallback(
    (acceptedFiles: FileWithPath[]) => {
      const newImages = acceptedFiles.map((imageFile) => ({
        objectURL: URL.createObjectURL(imageFile),
        file: imageFile,
        fileName: imageFile.name,
        fileSize: imageFile.size,
      }));

      setImages((prevImages) => [...prevImages, ...newImages]);
    },
    [setImages]
  );

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "image/jpeg": [".jpeg", ".jpg"],
      "image/png": [".png"],
    },
    maxSize: 5 * 1024 * 1024,
    onDrop,
  });

  function handleDelete(imageToDelete: ImageItem) {
    try {
      URL.revokeObjectURL(imageToDelete.objectURL);
    } catch {}
    setImages((prevImages) => prevImages.filter((img) => imageToDelete !== img));
  }

  function handleClearAll() {
    images.forEach((img) => {
      try {
        URL.revokeObjectURL(img.objectURL);
      } catch {}
    });
    setImages([]);
  }

  return (
    <section className="w-full max-w-4xl max-h-full rounded-lg flex flex-col relative">

      {isProcessing && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          role="status"
          aria-live="polite"
        >
          <div className="bg-white dark:bg-gray-800 rounded-md p-6 flex flex-col items-center gap-4 shadow-lg w-full max-w-sm">
            <svg
              className="animate-spin h-10 w-10 text-red-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
            </svg>

            <div className="text-center">
              <div className="font-medium text-sm">Uploading and processing images</div>
              <div className="text-xs text-gray-500 mt-1">
                This may take a minute depending on image count ({images.length}) and backend load.
              </div>
            </div>
          </div>
        </div>
      )}

      <div className={`w-full h-full flex flex-col gap-6 ${isProcessing ? "pointer-events-none select-none" : ""}`}>
        <div
          {...getRootProps({
            className:
              "flex min-h-86 max-h-full justify-center items-center p-10 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer bg-gray-200 hover:bg-gray-300 dark:bg-gray-900 dark:hover:bg-gray-600 dark:bg-transparent hover:border-blue-400 transition-colors",
          })}
        >
          <input {...getInputProps()} />
          <p className="text-gray-500">Drag your RAW Japanese manga images here, or click to select files</p>
        </div>

        {images.length !== 0 && (
          <aside className="max-h-80 overflow-y-auto">
            <div className="flex items-center justify-between mb-2 p-3">
              <h4 className="text-sm font-medium">
                Uploaded Images <span className="text-xs text-gray-500">({images.length})</span>
              </h4>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleClearAll}
                  className="text-xs px-2 py-1 rounded-md border bg-white dark:bg-gray-500 gray-50 disabled:opacity-50"
                >
                  Clear All
                </button>
              </div>
            </div>

            <div className="p-2 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {images.map((image, idx) => (
                <div key={image.objectURL ?? idx} className="relative rounded-md overflow-hidden border bg-white shadow-sm">
                  <div className="w-full aspect-[3/4] bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                    <PreviewImage image={image.objectURL} styles="w-full h-full object-contain" />
                  </div>

                  <div className="absolute left-2 bottom-2 right-2 flex items-center justify-between bg-black/50 text-white text-xs px-2 py-1 rounded">
                    <div className="truncate mr-2">{image.fileName ?? `Image ${idx + 1}`}</div>

                    <button
                      onClick={() => handleDelete(image)}
                      className="ml-1 inline-flex items-center justify-center p-1 rounded hover:bg-white/20"
                      type="button"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                          fillRule="evenodd"
                          d="M6 6a1 1 0 011-1h6a1 1 0 011 1v1H6V6zm2 3a1 1 0 00-1 1v6a1 1 0 001 1h4a1 1 0 001-1v-6a1 1 0 00-1-1H8z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </aside>
        )}

        {images.length !== 0 && (
          <div className="flex justify-end">
            <Button
              text={"Submit"}
              onClick={async () => {
                try {
                  setIsProcessing(true);
                  const resp = await uploadImages(images);
                  const imageList = Object.values(resp).map((item: any) => ({
                    objectURL: item.imageUrl,
                    fileName: item.name,
                  }));
                  setProcessedImagesUrl(imageList);
                } catch (error) {
                  console.error("Error uploading images:", error);
                } finally {
                  setIsProcessing(false);
                }
              }}
              loading={isProcessing}
              disabled={isProcessing}
            />
          </div>
        )}
      </div>
    </section>
  );
}