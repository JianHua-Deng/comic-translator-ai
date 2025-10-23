import { useState } from 'react'
import './App.css'
import Header from './components/Header/Header'
import ImageDropZone from './components/ImageDropZone/ImageDropZone'

function App() {


  return (

    <div className='h-screen w-screen flex flex-col'>
      <Header/>
      <div className='h-screen flex flex-col justify-center items-center gap-10'>
        <div className='w-4xl h-36 flex flex-col justify-around'>
          <h1 className='text-5xl'>Manga Translator</h1>
          <p className=' text-gray-400 dark:text-gray-200'>Upload your Manga pages for translations</p>
        </div>
        <ImageDropZone/>
      </div>
    </div>

  )
}

export default App
