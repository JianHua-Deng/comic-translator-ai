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
              <h1 className='text-5xl md:text-6xl font-bold bg-gradient-to-r from-red-500 via-pink-500 to-red-500 bg-clip-text text-transparent'>
                Manga Translator AI
              </h1>
              <p className='text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto'>
                Upload your manga pages and let AI translate them to English instantly
              </p>
              <div className='flex items-center justify-center gap-6 mt-2 text-sm text-gray-500 dark:text-gray-400'>
                <div className='flex items-center gap-2'>
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>OCR Detection</span>
                </div>
                <div className='flex items-center gap-2'>
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>AI Translation</span>
                </div>
                <div className='flex items-center gap-2'>
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Smart Rendering</span>
                </div>
              </div>
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