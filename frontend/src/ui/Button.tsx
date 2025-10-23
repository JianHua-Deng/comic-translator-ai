interface ButtonProps {
  onClick: () => void;
  text: string;

}

export default function Button({onClick, text}: ButtonProps) {
  return (
    <button onClick={onClick} className="h-10 w-30 text- bg-emerald-300 hover:bg-emerald-200">
      {text}
    </button>
  )
}