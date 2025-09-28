from simple_lama_inpainting import SimpleLama
from app import config

class InPainter:
    def __init__(self, device='cpu'):
        self.lama = SimpleLama(device=device)

    def inpaint(self, image, mask):
        return self.lama(image, mask)