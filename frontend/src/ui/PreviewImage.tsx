import Button from "./Button";

interface PreviewImageProps {
  image: string;
  deleteFunction: () => void;
}

export default function PreviewImage({image, deleteFunction} : PreviewImageProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <img className="h-40 max-w-30 w-auto" src={image}/>
      <Button text="Remove" onClick={deleteFunction}/>
    </div>
  )
}