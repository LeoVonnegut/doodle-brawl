import sys, os
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

def main(path, outdir, prefix, min_area=300, dilate_r=7, pad=12, thresh=150, max_dim=1600):
    im = ImageOps.exif_transpose(Image.open(path)).convert("L")
    im.thumbnail((max_dim, max_dim), Image.LANCZOS)
    arr = np.array(im)
    mask = arr < thresh
    struct = np.ones((dilate_r, dilate_r), dtype=bool)
    merged = ndimage.binary_dilation(mask, structure=struct)
    labels, n = ndimage.label(merged, structure=np.ones((3,3)))
    h, w = mask.shape
    os.makedirs(outdir, exist_ok=True)
    objs = ndimage.find_objects(labels)
    results = []
    idx = 0
    for lid, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        ys, xs = sl
        region_mask = mask[ys, xs] & (labels[ys, xs] == lid)
        area = region_mask.sum()
        if area < min_area:
            continue
        bh = ys.stop - ys.start
        bw = xs.stop - xs.start
        if bh < 10 or bw < 10:
            continue
        idx += 1
        y0 = max(0, ys.start - pad); y1 = min(h, ys.stop + pad)
        x0 = max(0, xs.start - pad); x1 = min(w, xs.stop + pad)
        crop_gray = arr[y0:y1, x0:x1]
        crop_ink = crop_gray < thresh
        ch, cw = crop_ink.shape
        rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        rgba[..., 0] = 35; rgba[..., 1] = 45; rgba[..., 2] = 65
        alpha = np.clip((thresh - crop_gray.astype(np.int32)) * 4, 0, 255).astype(np.uint8)
        alpha[~crop_ink] = 0
        rgba[..., 3] = alpha
        out_img = Image.fromarray(rgba, mode="RGBA")
        fname = f"{prefix}_{idx:02d}_{cw}x{ch}.png"
        out_img.save(os.path.join(outdir, fname))
        results.append((fname, x0, y0, cw, ch, int(area)))
    results.sort(key=lambda r: (r[2]//120, r[1]))
    print(f"{prefix}: {len(results)} blobs from {path} (image {w}x{h})")
    for r in results:
        print("  ", r)
    return results

if __name__ == "__main__":
    path, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
    kwargs = {}
    if len(sys.argv) > 4: kwargs['min_area'] = int(sys.argv[4])
    if len(sys.argv) > 5: kwargs['dilate_r'] = int(sys.argv[5])
    main(path, outdir, prefix, **kwargs)
