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
    <header className="w-full h-24 bg-red-400 p-4 grid grid-cols-3">
      <div className="items-center h-full w-full place-items-end place-content-center col-start-3 p-5">
          {theme === 'light' ? <SunIcon onClick={switchTheme} className="text-gray-800 w-10 h-10 cursor-pointer" /> : <MoonIcon onClick={switchTheme} className="text-gray-800 w-10 h-10 cursor-pointer" />}
      </div>
    </header>
  )
}