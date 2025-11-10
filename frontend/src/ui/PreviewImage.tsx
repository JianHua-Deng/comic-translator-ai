import Button from "./Button";

interface PreviewImageProps {
  image: string;
  deleteFunction?: () => void;
  styles?: string;
}

export default function PreviewImage({image, deleteFunction, styles} : PreviewImageProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <img className={`h-40 max-w-30 w-auto ${styles || ''}`} src={image}/>
      {deleteFunction && (<Button text="Remove" onClick={deleteFunction}/>)}
    </div>
  )
}