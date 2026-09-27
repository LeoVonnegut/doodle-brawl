import os
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from scipy import ndimage

RAW = "raw"
OUT = "img"
DISP_W = 1500

# name, page, x0, y0, x1, y1 (display coords, 1500 wide), rotate (deg CCW), flip, keep
ITEMS = [
    ("head",        "p01",  960,  275, 1100,  420,   0, False, "main"),
    ("face_normal", "p01",  770,  825,  945,  950,   0, False, "all"),
    ("face_dead",   "p01",  250,  530,  455,  700,   0, False, "all"),
    ("face_hurt",   "p01",  265,  800,  490,  970,   0, False, "all"),
    ("face_taunt",  "p02", 1220,  900, 1400, 1115,   0, False, "all"),
    ("skull",       "p01", 1070,  675, 1305,  975,   0, False, "main"),
    ("hat_party",   "p01",  430,   60,  590,  335,   0, False, "all"),
    ("hat_top",     "p01",  215,   75,  400,  300,   0, False, "main"),
    ("hat_crown",   "p01",  620,  165,  800,  300,   0, False, "main"),
    ("hat_cap",     "p02",  440,  285,  595,  420,   0, False, "main+fill"),
    ("hat_beanie",  "p02", 1190,  195, 1400,  350,   0, False, "main"),
    ("arm_l",       "p02",  830, 1040,  980, 1445,   0, False, "main"),
    ("arm_r",       "p02", 1080, 1040, 1190, 1445,   0, False, "main"),
    ("torso",       "p02",  970, 1330, 1040, 1585,   0, False, "main"),
    ("leg_l",       "p02",  820, 1505,  950, 1755,   0, False, "main"),
    ("leg_r",       "p02",  990, 1570, 1090, 1735,   0, False, "main"),
    ("gun_rocket",  "p09",  560,  240,  695,  445,  90, False, "main"),
    ("gun_sniper",  "p09",  545,  650,  655,  905,  90, False, "all"),
    ("gun_minigun", "p09",  550, 1010,  665, 1270,  90, False, "all"),
    ("gun_shotgun", "p09",  560, 1395,  645, 1595,  90, False, "main"),
    ("gun_pea",     "p09",  565, 1650,  655, 1755,  90, False, "main"),
    ("gun_banana",  "p05",  870,  210, 1065,  385,   0, False, "all"),
    ("proj_rocket", "p09",  750,  370,  890,  505,  90, False, "all"),
    ("proj_bullet", "p09",  715, 1710,  760, 1785,  90, False, "main"),
    ("proj_pea",    "p09",  850, 1510,  935, 1600,   0, False, "main"),
    ("proj_pellets","p09",  675, 1155,  835, 1265,  90, False, "all"),
    ("proj_banana", "p05", 1190,  240, 1320,  350,   0, False, "main"),
    ("logo",        "p09",  490,   60, 1215,  190, 180, False, "all"),
    ("crosshair",   "p05",  495,  275,  650,  425,   0, False, "all"),
    ("plat_thin",   "p05",  140,  540,  640,  630,   0, False, "main"),
    ("plat_oval",   "p05",  750,  455, 1155,  595,   0, False, "main"),
    ("plat_floor",  "p05",  750,  650, 1340,  830,   0, False, "main"),
    ("crate",       "p05",  130,  780,  320,  970,   0, False, "all"),
    ("boom_1",      "p05",  395, 1120,  515, 1260,   0, False, "all"),
    ("boom_2",      "p05",  525, 1055,  750, 1290,   0, False, "all"),
    ("boom_3",      "p05",  745,  930, 1105, 1345,   0, False, "all"),
    ("boom_4",      "p05",  595, 1330, 1170, 1835,   0, False, "all"),
    ("confetti",    "p04",  500,   85,  870,  490,   0, False, "all"),
    ("txt_bonk",    "p04", 1055,  175, 1450,  335,   0, False, "all"),
    ("txt_kaboom",  "p04",  140,  390,  380,  885,  90, False, "all"),
    ("txt_wins",    "p04",  215, 1040,  390, 1425,  90, False, "all"),
    ("muzzle_1",    "p04",  665, 1165,  765, 1255,   0, True,  "all"),
    ("muzzle_2",    "p04",  770, 1115,  950, 1285,   0, True,  "all+fill"),
    ("poof_1",      "p04",  515, 1435,  595, 1535,   0, False, "all"),
    ("poof_2",      "p04",  600, 1365,  740, 1565,   0, False, "all"),
    ("poof_3",      "p04",  740, 1315,  890, 1535,   0, False, "all"),
    ("splat_1",     "p04", 1035, 1370, 1090, 1425,   0, False, "all"),
    ("splat_2",     "p04", 1100, 1350, 1180, 1445,   0, False, "all"),
    ("splat_3",     "p04", 1180, 1320, 1285, 1465,   0, False, "all"),
    ("dust_1",      "p04",  500, 1635,  640, 1725,   0, False, "all"),
    ("dust_2",      "p04",  660, 1595,  840, 1720,   0, False, "all"),
    ("dust_3",      "p04",  830, 1555, 1070, 1725,   0, False, "all"),
]

_pages = {}
def page(name):
    if name not in _pages:
        im = ImageOps.exif_transpose(Image.open(f"{RAW}/{name}.jpg")).convert("L")
        g = np.asarray(im).astype(np.float32)
        bg = ndimage.gaussian_filter(g, sigma=35)
        ratio = g / np.maximum(bg, 1)
        _pages[name] = (ratio, im.size[0] / DISP_W)
    return _pages[name]

def cut(name, pg, x0, y0, x1, y1, rot, flip, keep):
    ratio, s = page(pg)
    r = ratio[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]
    a = np.clip((0.82 - r) / (0.82 - 0.6), 0, 1)
    ink = a > 0.35
    if "fill" in keep:
        solid = ndimage.binary_fill_holes(ndimage.binary_closing(a > 0.15, iterations=6))
        a[solid] = 1; ink = a > 0.35
    lab, n = ndimage.label(ndimage.binary_dilation(ink, iterations=2))
    if n:
        sizes = ndimage.sum(ink, lab, range(1, n+1))
        big = sizes.max()
        minsz = big * 0.15 if keep.startswith("main") else max(12, big * 0.01)
        good = np.isin(lab, [i+1 for i, sz in enumerate(sizes) if sz >= minsz])
        a = a * good
    ys, xs = np.where(a > 0.2)
    if len(ys) == 0:
        print("EMPTY", name); return None
    pad = 4
    a = a[max(0, ys.min()-pad):ys.max()+pad+1, max(0, xs.min()-pad):xs.max()+pad+1]
    rgba = np.zeros((*a.shape, 4), np.uint8)
    rgba[..., :3] = (35, 50, 74)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    img = Image.fromarray(rgba)
    if rot: img = img.rotate(rot, expand=True)
    if flip: img = ImageOps.mirror(img)
    maxd = 256
    if max(img.size) > maxd:
        k = maxd / max(img.size)
        img = img.resize((max(1, round(img.size[0]*k)), max(1, round(img.size[1]*k))), Image.LANCZOS)
    img.save(f"{OUT}/{name}.png")
    return img

def sheet(imgs, path):
    cell, cols = 200, 8
    rows = (len(imgs) + cols - 1) // cols
    sh = Image.new("RGB", (cols*cell, rows*cell), "white")
    d = ImageDraw.Draw(sh)
    f = ImageFont.load_default(size=16)
    for i, (n, im) in enumerate(imgs):
        cx, cy = (i % cols) * cell, (i // cols) * cell
        d.rectangle([cx, cy, cx+cell-1, cy+cell-1], outline=(220, 220, 220))
        if im is not None:
            t = im.copy(); t.thumbnail((cell-16, cell-36))
            sh.paste(t, (cx + (cell - t.size[0])//2, cy + 4 + (cell-36 - t.size[1])//2), t)
        d.text((cx+6, cy+cell-24), n, fill=(200, 30, 30), font=f)
    sh.save(path)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in ("skull", "tophat", "partyhat", "crown"):
        p = f"{OUT}/{f}.png"
        if os.path.exists(p): os.remove(p)
    res = [(it[0], cut(*it)) for it in ITEMS]
    sheet(res, "blobs/sheet.png")
    print("done", len(res))
