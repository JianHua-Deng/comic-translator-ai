import { type FileWithPath } from "react-dropzone";

export interface ImageItem {
  objectURL: string;
  file?: FileWithPath;
  fileName: string;
}