print("[InPainter] importing transformers/torch - this can take a while", flush=True)
import os
import torch
import numpy as np
from PIL import Image
from app import config
from app.utils.utils import download_models
print("[InPainter] transformers/torch imported", flush=True)


class InPainter:
    def __init__(self):
        self.model = self.load_model()

    
    def load_model(self):
        if not os.path.exists(config.CACHED_INPAINTER_MODEL_PATH):
            download_models(config.INPAINTER_MODEL, config.CACHED_INPAINTER_MODEL_PATH)
        
        print("Trying to load the Inpainter Model")
        try:
            model = torch.jit.load(config.CACHED_INPAINTER_MODEL_PATH, map_location=config.DEVICE)
            model.eval()
            model.to(config.DEVICE)
            return model

        except Exception as e:
            print("Something went wrong while trying to load the InPainter Model")
            raise e
        
    
    def inpaint(self, image: Image.Image, mask: Image.Image) -> Image.Image:

        # Convert PIL to Numpy and Normalize it to 0.0 - 1.0 values
        img_np = np.array(image).astype('float32') / 255.0
        mask_np = np.array(mask).astype('float') / 255.0

        # Binarize mask
        mask_np = (mask_np > 0.5).astype('float32')

        # Prepare tensors
        # Image: HWC -> CHW -> Add Batch Dimensions(size) -> move to device
        img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0).to(config.DEVICE)

        # Mask: HW -> Add Batch and Channel Dimensions (1, 1, H, W) -> Move to device
        if len(mask_np.shape) == 2:
            mask_tensor = torch.from_numpy(mask_np).unsqueeze(0).unsqueeze(0).to(config.DEVICE)
        else:
            mask_tensor = torch.from_numpy(mask_np).permute(2, 0, 1).unsqueeze(0).to(config.DEVICE)


        # Inference
        with torch.no_grad():
            output = self.model(img_tensor, mask_tensor)

        # Post process: Tensor -> Numpy -> PIL
        # Removing batch dimensions -> CHW ->HWC
        res_img = output[0].permute(1, 2, 0).detach().cpu().numpy()

        # Clip to 0-255 and converts to uint8
        res_img = np.clip(res_img * 255, 0, 255).astype("uint8")

        return Image.fromarray(res_img)
            
            