import sys
import numpy as np
from PIL import Image, ImageOps

def crop(src, out, x0, y0, x1, y1, thresh=165, disp_w=None, disp_h=None):
    im = ImageOps.exif_transpose(Image.open(src))
    W, H = im.size
    if disp_w and disp_h:
        sx, sy = W/disp_w, H/disp_h
        x0, x1 = x0*sx, x1*sx
        y0, y1 = y0*sy, y1*sy
    box = (int(x0), int(y0), int(x1), int(y1))
    region = im.convert("L").crop(box)
    arr = np.array(region).astype(np.int32)
    hard = thresh - 25
    alpha = np.clip((thresh - arr) * (255.0 / (thresh - hard)), 0, 255).astype(np.uint8)
    alpha[arr < hard] = 255
    rgba = np.zeros((*arr.shape, 4), dtype=np.uint8)
    rgba[..., 0] = 30; rgba[..., 1] = 40; rgba[..., 2] = 60
    rgba[..., 3] = alpha
    Image.fromarray(rgba, "RGBA").save(out)
    print(out, region.size)

if __name__ == "__main__":
    a = sys.argv
    crop(a[1], a[2], float(a[3]), float(a[4]), float(a[5]), float(a[6]),
         thresh=int(a[7]) if len(a) > 7 else 165,
         disp_w=float(a[8]) if len(a) > 8 else None,
         disp_h=float(a[9]) if len(a) > 9 else None)
