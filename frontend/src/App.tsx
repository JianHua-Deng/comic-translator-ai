import { useState } from 'react'
import './App.css'
import Header from './components/Header/Header'
import ImageDropZone from './components/ImageDropZone/ImageDropZone'

function App() {


  return (

  <div className='bg-gray-100 dark:bg-gray-800 dark:text-gray-100 h-screen w-screen grid grid-cols-3 grid-rows-[1fr_6fr]'>
      <div className='row-start-1 col-span-4'>
        <Header/>
      </div>

      <div className='min-h-3/4 h-fit grid-rows-1 col-span-4 flex flex-col justify-center items-center'>
        <div className='flex flex-col justify-center items-center gap-10'>
          <div className='w-4xl h-36 flex flex-col gap-5 justify-around'>
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
