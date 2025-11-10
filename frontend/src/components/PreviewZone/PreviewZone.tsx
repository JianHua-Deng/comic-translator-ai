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
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Processed Images</h3>
        <div className="flex items-center gap-2">
          <Button onClick={clearFunction} text="Return" />
        </div>
      </div>

      {imageUrls.length === 0 ? (
        <div className="w-full p-8 rounded-lg border border-dashed border-gray-300 text-center text-sm text-gray-500">
          No images yet — upload to see processed results
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {imageUrls.map((image, idx) => (
            <button
              key={image.objectURL ?? idx}
              onClick={() => setSelectedImage(image.objectURL)}
              className="group relative overflow-hidden rounded-lg shadow-sm bg-gray-50 dark:bg-gray-800 p-0 border hover:shadow-lg transform hover:scale-[1.02] transition"
              type="button"
            >
              <div className="w-full h-40 bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                <PreviewImage image={image.objectURL} styles="w-full h-full object-cover" />
              </div>

              <div className="absolute inset-x-0 bottom-0 px-2 py-1 bg-gradient-to-t from-black/60 to-transparent">
                <div className="text-xs text-white truncate">{image.fileName ?? `Image ${idx + 1}`}</div>
              </div>

              <div className="absolute top-2 left-2 text-xs bg-black/50 text-white px-2 py-0.5 rounded">{idx + 1}</div>
            </button>
          ))}
        </div>
      )}

      {selectedImage && (
        <ImageModal imageUrl={selectedImage} onClose={() => setSelectedImage(null)} />
      )}
    </div>
  );
}