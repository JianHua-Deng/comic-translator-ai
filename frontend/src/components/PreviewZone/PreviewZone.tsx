import type { ImageItem } from "../../types/types";
import Button from "../../ui/Button";
import PreviewImage from "../../ui/PreviewImage";
import { download_zip } from "../../utils/downloadCall";
import ImageModal from "../ImageModal/ImageModal";
import { useState } from "react";

interface PreviewZoneProps {
  imageUrls: ImageItem[];
  clearFunction: () => void;
}

export default function PreviewZone({ imageUrls, clearFunction }: PreviewZoneProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  return (
    <div className="w-full h-full flex flex-col gap-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Translation Complete!</h3>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {imageUrls.length} image{imageUrls.length !== 1 ? "s" : ""} processed successfully
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={() => download_zip(imageUrls)}
              text="Download All"
              variant="secondary"
              size="sm"
              disabled={imageUrls.length === 0}
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              }
            />
            <Button
              onClick={clearFunction}
              text="New Translation"
              variant="primary"
              size="sm"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              }
            />
          </div>
        </div>
      </div>

      {imageUrls.length === 0 ? (
        <div className="w-full p-12 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-700 text-center bg-white dark:bg-gray-800">
          <div className="flex flex-col items-center gap-3">
            <div className="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400">No images yet — upload to see processed results</p>
          </div>
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
          <div className="max-h-[65vh] p-5 overflow-y-auto overflow-x-hidden pr-2">
            <div className="grid gap-5 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 auto-rows-fr">
              {imageUrls.map((image, idx) => (
                <button
                  key={image.objectURL ?? idx}
                  onClick={() => setSelectedImage(image.objectURL)}
                  className="group relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 p-0 hover:shadow-2xl hover:border-red-400 dark:hover:border-red-400 transform hover:-translate-y-1 hover:scale-105 transition-all duration-300"
                  type="button"
                  aria-label={`Open processed image ${idx + 1}`}
                >
                  <div className="w-full aspect-[3/4] bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center p-2">
                    <PreviewImage
                      image={image.objectURL}
                      styles="w-full h-full object-contain rounded-lg"
                    />
                  </div>

                  <div className="absolute inset-x-0 bottom-0 px-3 py-2 bg-gradient-to-t from-black/80 via-black/50 to-transparent">
                    <div className="text-xs font-medium text-white truncate">{image.fileName ?? `Image ${idx + 1}`}</div>
                  </div>

                  <div className="absolute top-2 left-2 bg-red-400 dark:bg-red-500/80 text-white text-xs font-bold px-2.5 py-1 rounded-lg shadow-lg">
                    #{idx + 1}
                  </div>

                  <div className="absolute inset-0 bg-gradient-to-t from-red-500/0 via-red-500/0 to-red-500/0 group-hover:from-red-500/5 group-hover:via-red-500/5 group-hover:to-red-500/10 transition-all duration-300 pointer-events-none" />
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {selectedImage && <ImageModal imageUrl={selectedImage} onClose={() => setSelectedImage(null)} />}
    </div>
  );
}