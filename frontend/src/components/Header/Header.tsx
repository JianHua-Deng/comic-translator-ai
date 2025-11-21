import { useTheme } from "../../contexts/ThemeContext"
import { MoonFilledIcon as MoonIcon } from "../ui/icons/ant-design-moon-filled"
import { SunFilledIcon as SunIcon } from "../ui/icons/ant-design-sun-filled"


export default function Header() {

const {theme, setTheme} = useTheme();

const switchTheme = () => {
  if (theme === 'light') {
    setTheme('dark');
  } else {
    setTheme('light');
  }
}


  return (
    <header className="w-full h-20 bg-red-400 dark:bg-red-500/80">
      <div className="max-w-7xl mx-auto h-full px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-white dark:bg-gray-900 rounded-lg p-2 shadow-md">
            <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Manga Translator</h1>
          </div>
        </div>

        <button
          onClick={switchTheme}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm p-2.5 rounded-lg transition-all duration-200 hover:scale-105"
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ?
            <SunIcon className="text-white w-6 h-6" /> :
            <MoonIcon className="text-white w-6 h-6" />
          }
        </button>
      </div>
    </header>
  )
}