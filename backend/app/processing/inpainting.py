from simple_lama_inpainting import SimpleLama
from app import config
import torch
import contextlib

_orig_jit_load = torch.jit.load

# This function is to avoid the error of not being able to run with CPU
def _jit_load_force_cpu(f, *args, **kwargs):
    # prefer explicit map_location to CPU; if caller already passed map_location, keep it
    if 'map_location' not in kwargs and len(args) == 0:
        return _orig_jit_load(f, map_location=torch.device('cpu'))
    # if they passed e.g. a map_location in args, let original handle it (rare)
    return _orig_jit_load(f, *args, **kwargs)

torch.jit.load = _jit_load_force_cpu

class InPainter:
    def __init__(self, device=config.DEVICE):
        self.lama = SimpleLama(device=device)

    def inpaint(self, image, mask):
        """
        Wrap the model call with both no_grad (disable autograd)
        and optimized_execution(False) to avoid JIT optimization overhead
        on first calls (fixes slow-first-inference issue).
        """
        # safe fallback if optimized_execution isn't available
        try:
            opt_ctx = torch.jit.optimized_execution(False)
        except Exception:
            opt_ctx = contextlib.nullcontext()

        with torch.no_grad():
            with opt_ctx:
                return self.lama(image, mask)