import json
import numpy as np
from PIL import Image
from font import glyphs, to_img
from crops import sheet

ROT = 270
CAP, BASE, CELL_H = 64, 68, 84

L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
P07 = [32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 37, 14, 36, 35, 34, 33, 46, 45]
P11 = {"0": 28, "1": 31, "2": 26, "3": 25, "4": 19, "5": 24, "6": 23, "7": 22, "8": 21, "9": 20}

def trim(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im

def fit_h(im, h):
    return im.resize((max(1, round(im.size[0] * h / im.size[1])), h), Image.LANCZOS)

def fit_w(im, w):
    return im.resize((w, max(1, round(im.size[1] * w / im.size[0]))), Image.LANCZOS)

def cell(parts, w):
    c = Image.new("RGBA", (w, CELL_H), (0, 0, 0, 0))
    for im, x, y in parts:
        c.alpha_composite(im, (x, y))
    return c

g7 = glyphs("p07")
g11 = glyphs("p11_digits")
G = lambda gs, i: trim(to_img(gs[i], ROT))

chars = {}
for ch, i in zip(L, P07):
    im = fit_h(G(g7, i), CAP)
    chars[ch] = cell([(im, 2, BASE - CAP)], im.size[0] + 4)
for ch, i in P11.items():
    im = fit_h(G(g11, i), CAP)
    chars[ch] = cell([(im, 2, BASE - CAP)], im.size[0] + 4)

dot = fit_h(G(g7, 40), 11)
dw = dot.size[0]
chars["."] = cell([(dot, 3, BASE - 11)], dw + 6)
chars[":"] = cell([(dot, 3, BASE - 11), (dot, 3, BASE - 40)], dw + 6)
bang = fit_h(G(g7, 44), 44)
chars["!"] = cell([(bang, 3, BASE - CAP), (dot, 3 + (bang.size[0] - dw) // 2, BASE - 11)], max(bang.size[0], dw) + 6)
q = fit_h(G(g7, 43), 44)
chars["?"] = cell([(q, 2, BASE - CAP), (dot, 2 + (q.size[0] - dw) // 2, BASE - 11)], max(q.size[0], dw) + 4)
comma = fit_h(G(g7, 48), 20)
chars[","] = cell([(comma, 2, BASE - 8)], comma.size[0] + 4)
apos = fit_h(G(g7, 42), 20)
chars["'"] = cell([(apos, 3, BASE - CAP)], apos.size[0] + 6)
dash = fit_w(G(g7, 41), 26)
chars["-"] = cell([(dash, 3, BASE - 32 - dash.size[1] // 2)], dash.size[0] + 6)
for ch, i in (("(", 39), (")", 38)):
    im = fit_h(G(g7, i), 78)
    chars[ch] = cell([(im, 3, BASE - CAP - 6)], im.size[0] + 6)

maxw, x, y, rowh = 1024, 0, 0, CELL_H
meta, placed = {}, []
for ch, im in chars.items():
    if x + im.size[0] > maxw:
        x, y = 0, y + rowh
    placed.append((im, x, y))
    meta[ch] = [x, y, im.size[0]]
    x += im.size[0] + 2
atlas = Image.new("RGBA", (maxw, y + rowh), (0, 0, 0, 0))
for im, px, py in placed:
    atlas.alpha_composite(im, (px, py))
atlas.save("img/font.png")
json.dump({"cellH": CELL_H, "base": BASE, "cap": CAP, "g": meta}, open("img/font.json", "w"), separators=(",", ":"))

prev = Image.new("RGBA", (maxw, CELL_H * 2 + 20), "white")
xx = 10
for s, row in (("THE QUICK BROWN FOX JUMPS", 0), ("OVER 0123456789 (DOG)! OK? A:B, IT'S - .", 1)):
    xx = 10
    for ch in s:
        if ch == " ":
            xx += 20; continue
        im = chars[ch]
        prev.alpha_composite(im, (xx, row * CELL_H + 10))
        xx += im.size[0] - 2
prev.convert("RGB").save("blobs/font_preview.png")
print("glyphs", len(meta), "atlas", atlas.size)
