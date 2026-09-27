import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
from crops import page, sheet

def glyphs(pg, min_px=60, max_frac=0.02):
    ratio, s = page(pg)
    a = np.clip((0.82 - ratio) / (0.82 - 0.6), 0, 1)
    ink = a > 0.35
    lab, n = ndimage.label(ndimage.binary_dilation(ink, iterations=3))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = (lab[sl] == i) & ink[sl]
        px = int(m.sum())
        h, w = m.shape
        if px < min_px or h * w > max_frac * ratio.size:
            continue
        out.append(dict(y=sl[0].start, x=sl[1].start, h=h, w=w, px=px, a=(a[sl] * m)))
    out.sort(key=lambda g: (g["x"] // 120, g["y"]))
    return out

def to_img(g, rot=0):
    al = g["a"]
    rgba = np.zeros((*al.shape, 4), np.uint8)
    rgba[..., :3] = (35, 50, 74)
    rgba[..., 3] = (al * 255).astype(np.uint8)
    im = Image.fromarray(rgba)
    return im.rotate(rot, expand=True) if rot else im

if __name__ == "__main__":
    pg, rot = sys.argv[1], int(sys.argv[2])
    gs = glyphs(pg)
    sheet([(f"{i}", to_img(g, rot)) for i, g in enumerate(gs)], f"blobs/font_{pg}.png")
    print(pg, len(gs))
