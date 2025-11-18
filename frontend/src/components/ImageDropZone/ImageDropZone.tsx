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
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
          role="status"
          aria-live="polite"
        >
          <div className="bg-white dark:bg-gray-800 rounded-xl p-8 flex flex-col items-center gap-5 shadow-2xl w-full max-w-md border border-gray-100 dark:border-gray-700 animate-in fade-in zoom-in duration-300">
            <div className="relative">
              <svg
                className="animate-spin h-14 w-14 text-red-500"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle className="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-8 h-8 bg-red-500 rounded-full animate-pulse" />
              </div>
            </div>

            <div className="text-center space-y-2">
              <div className="font-semibold text-lg text-gray-900 dark:text-gray-100">Processing Your Manga</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                Translating {images.length} image{images.length !== 1 ? 's' : ''}...
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500 pt-1">
                This may take a minute depending on image complexity
              </div>
            </div>

            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 overflow-hidden">
              <div className="h-full bg-gradient-to-r from-red-500 to-pink-500 rounded-full animate-pulse" style={{width: '70%'}} />
            </div>
          </div>
        </div>
      )}

      <div className={`w-full h-full flex flex-col gap-6 ${isProcessing ? "pointer-events-none select-none" : ""}`}>
        <div
          {...getRootProps({
            className:
              "group relative flex min-h-72 max-h-full justify-center items-center p-12 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-2xl cursor-pointer bg-white dark:bg-gray-800/50 hover:bg-gradient-to-br hover:from-red-50 hover:to-pink-50 dark:hover:from-gray-800 dark:hover:to-gray-700 hover:border-red-400 dark:hover:border-red-400 transition-all duration-300 hover:shadow-lg backdrop-blur-sm",
          })}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center gap-4 text-center">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 rounded-full blur-xl opacity-20 group-hover:opacity-40 transition-opacity" />
              <div className="relative bg-gradient-to-br from-red-500 to-pink-500 p-4 rounded-2xl shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
            </div>
            <div className="space-y-2">
              <p className="text-lg font-semibold text-gray-700 dark:text-gray-200">Drop your manga pages here</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">or click to browse files</p>
            </div>
            <div className="flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500 pt-2">
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                </svg>
                JPG, PNG
              </span>
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                Max 5MB
              </span>
            </div>
          </div>
        </div>

        {images.length !== 0 && (
          <aside className="max-h-96 overflow-y-auto bg-white dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between mb-3 p-4 border-b border-gray-200 dark:border-gray-700 sticky top-0 bg-white dark:bg-gray-800 z-10">
              <h4 className="text-base font-semibold flex items-center gap-2">
                <span className="bg-gradient-to-r from-red-500 to-pink-500 text-white px-2.5 py-0.5 rounded-full text-sm">
                  {images.length}
                </span>
                Uploaded Images
              </h4>
              <button
                type="button"
                onClick={handleClearAll}
                className="text-sm px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
              >
                Clear All
              </button>
            </div>

            <div className="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {images.map((image, idx) => (
                <div key={image.objectURL ?? idx} className="group relative rounded-xl overflow-hidden border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-md hover:shadow-xl hover:scale-105 transition-all duration-300">
                  <div className="w-full aspect-[3/4] bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center">
                    <PreviewImage image={image.objectURL} styles="w-full h-full object-contain" />
                  </div>

                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent p-3 pt-8">
                    <div className="flex items-center justify-between text-white">
                      <div className="truncate text-xs font-medium mr-2">{image.fileName ?? `Image ${idx + 1}`}</div>
                      <button
                        onClick={() => handleDelete(image)}
                        className="flex-shrink-0 inline-flex items-center justify-center p-1.5 rounded-lg bg-red-500/80 hover:bg-red-500 transition-colors"
                        type="button"
                        aria-label="Delete image"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div className="absolute top-2 left-2 bg-gradient-to-br from-red-500 to-pink-500 text-white text-xs font-bold px-2 py-1 rounded-lg shadow-lg">
                    #{idx + 1}
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