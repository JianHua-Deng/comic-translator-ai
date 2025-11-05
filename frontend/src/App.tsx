import './App.css'
import Header from './components/Header/Header'
import ImageDropZone from './components/ImageDropZone/ImageDropZone'

function App() {
  return (
    // 1. Use "flex flex-col" for a simple vertical stack
    // 2. Use "min-h-screen" instead of "h-screen" to allow content to grow
    <div className='bg-gray-100 dark:bg-gray-800 dark:text-gray-100 min-h-screen w-screen flex flex-col'>
      
      {/* 3. Removed "row-start-1 col-span-4" */}
      <div className='flex-shrink-0'>
        <Header/>
      </div>

      {/* 4. Removed grid classes, added "flex-grow" to fill remaining space */}
      {/* 5. Added "p-4" for padding on small screens */}
      <div className='flex-grow flex flex-col justify-center items-center p-4'>
        <div className='w-full flex flex-col justify-center items-center gap-10'>
          
          {/* 6. Changed "w-4xl" to "w-full max-w-4xl" */}
          <div className='w-full max-w-4xl h-36 flex flex-col gap-5 justify-around'>
            <h1 className='text-5xl'>Manga Translator</h1>
            <p className=' text-gray-400 dark:text-gray-300'>Upload your Manga pages for translations to English</p>
          </div>
          
          <ImageDropZone/>
        </div>
      </div>
    </div>
  )
}

export default App