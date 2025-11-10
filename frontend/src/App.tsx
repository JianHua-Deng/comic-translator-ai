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

    <div className='bg-gray-200 dark:bg-gray-800 dark:text-gray-100 min-h-screen w-screen flex flex-col'>
      

      <div className='flex-shrink-0'>
        <Header/>
      </div>
      {processedImagesUrl.length === 0 ? (
        <div className='flex-grow flex flex-col justify-center items-center p-4'>
          <div className='w-full flex flex-col justify-center items-center gap-10'>

            <div className='w-full max-w-4xl h-36 flex flex-col gap-5 justify-around'>
              <h1 className='text-5xl'>Manga Translator</h1>
              <p className=' text-gray-600 dark:text-gray-300'>Upload your Manga pages for translations to English</p>
            </div>
            
            <ImageDropZone 
              images={images} 
              processedImagesUrl={processedImagesUrl} 
              isProcessing={isProcessing} setImages={setImages} 
              setProcessedImagesUrl={setProcessedImagesUrl} 
              setIsProcessing={setIsProcessing}
            />
          </div>
        </div>
      ) : (
        <div className='flex flex-grow justify-center items-center w-full'>
          <div className='w-full max-w-5xl'>
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