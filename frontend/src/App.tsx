import './App.css'
import { useState } from 'react';
import Header from './components/Header/Header'
import ImageDropZone from './components/ImageDropZone/ImageDropZone'
import { type ImageItem } from "./types/types";
import PreviewZone from './components/PreviewZone/PreviewZone';

function App() {

  const [images, setImages] = useState<ImageItem[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedImagesUrl, setProcessedImagesUrl] = useState<ImageItem[]>([]);

  return (
    <div className='bg-gradient-to-br from-gray-100 via-gray-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 dark:text-gray-100 min-h-screen w-screen flex flex-col'>
      <div className='flex-shrink-0'>
        <Header/>
      </div>

      {processedImagesUrl.length === 0 ? (
        <div className='flex-grow flex flex-col justify-center items-center p-6 md:p-10'>
          <div className='w-full flex flex-col justify-center items-center gap-12 animate-in fade-in duration-700'>
            <div className='w-full max-w-4xl flex flex-col gap-4 text-center'>
              <h1 className='text-5xl md:text-6xl font-bold bg-gradient-to-r text-red-400'>
                Manga Translator
              </h1>
              <p className='text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto'>
                Upload your Japanese manga pages and it will translate them to English
              </p>

            </div>

            <ImageDropZone
              images={images}
              processedImagesUrl={processedImagesUrl}
              isProcessing={isProcessing}
              setImages={setImages}
              setProcessedImagesUrl={setProcessedImagesUrl}
              setIsProcessing={setIsProcessing}
            />
          </div>
        </div>
      ) : (
        <div className='flex flex-grow justify-center items-center w-full p-6 md:p-10'>
          <div className='w-full max-w-6xl animate-in fade-in duration-500'>
            <PreviewZone imageUrls={processedImagesUrl} clearFunction={ () => {
              setProcessedImagesUrl([]);
              setImages([]);
            }} />
          </div>
        </div>
      )}
    </div>
  )
}

export default App