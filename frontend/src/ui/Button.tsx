interface ButtonProps {
  onClick: () => void;
  text: string;

}

export default function Button({onClick, text}: ButtonProps) {
  return (
    <button onClick={onClick} className="h-8 w-25 text-sm text-gray-50 bg-red-400 hover:bg-red-300">
      {text}
    </button>
  )
}