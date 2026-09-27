import os, glob, subprocess, json
import numpy as np
from audio_scan import load, SR

# memo -> list of (key, start, end) in the recorded list order
MAP = {
    "fight":            [("fight", .28, 1.54)],
    "fight 2":          [("fight", .98, 1.40)],
    "fight 3":          [("fight", .24, .70)],
    "fanfare winner":   [("win", .62, 3.06), ("win", 4.32, 6.52), ("win", 7.96, 9.70), ("win", 11.06, 17.12)],
    "player joined":    [("join", .60, 1.42), ("join", 3.06, 3.80), ("join", 4.94, 5.36), ("join", 6.24, 6.70), ("join", 8.50, 9.14), ("join", 9.98, 10.86)],
    "items":            [("pick", 1.04, 1.58), ("ammo", 2.18, 2.82)],
    "items 2":          [("pick", .62, 1.18), ("ammo", 1.66, 2.16)],
    "items 3":          [("pick", .64, 1.36), ("ammo", 1.98, 3.68)],
    "moving":           [("jump", .50, .72), ("jump2", 1.68, 2.04), ("land", 3.00, 3.20)],
    "moving 2":         [("jump", .78, 1.54), ("jump2", 2.38, 3.04), ("land", 4.00, 4.22)],
    "moving 3":         [("jump", .44, .70), ("jump2", 1.74, 1.98), ("land", 2.98, 3.28)],
    "explosions":       [("boom_r", 1.04, 2.92), ("boom_b", 5.12, 6.68)],
    "explosions 2":     [("boom_r", .90, 1.58), ("boom_b", 3.10, 4.78)],
    "explosjons 3":     [("boom_r", .48, 1.98), ("boom_b", 3.00, 3.92)],
    "getting bit bonk oof":       [("hit", 1.64, 1.96), ("hit", 2.68, 2.98), ("hit", 3.74, 5.26)],
    "getting hit bonk oof 2":     [("hit", .68, 1.12), ("hit", 1.48, 2.36), ("hit", 3.30, 3.80)],
    "getting hit bonk oof 3":     [("hit", .76, 1.16), ("hit", 1.66, 1.92), ("hit", 2.54, 3.50)],
    "death screams":    [("die", a, b) for a, b in [(1.72, 3.34), (3.8, 4.92), (5.4, 5.88), (6.66, 7.44), (8.02, 8.98), (9.48, 10.54), (10.96, 11.74), (12.4, 13.12), (13.84, 14.76), (15.42, 16.94)]],
    "death screams 2":  [("die", a, b) for a, b in [(.86, 1.4), (2.24, 2.88), (3.82, 4.86), (5.28, 9.24), (9.7, 10.8), (11.78, 13.14)]],
    "falling":          [("fall", .58, 3.96)],
    "falling 2":        [("fall", a, b) for a, b in [(.46, 3.54), (5.74, 8.22), (10.16, 12.82), (13.2, 16.28), (17.06, 23.82)]],
    "tauntz":           [("taunt", a, b) for a, b in [(1.28, 2.8), (3.46, 4.52), (5.76, 6.86), (8.04, 10.0), (10.62, 12.46), (13.48, 15.16), (16.22, 17.26), (18.86, 19.88), (20.9, 22.88), (24.28, 25.16), (26.82, 28.58), (30.26, 31.94), (34.06, 35.62)]],
    "taunts 2":         [("taunt", a, b) for a, b in [(1.44, 2.52), (4.7, 6.76), (8.74, 10.48), (11.78, 13.64), (14.16, 15.72), (17.04, 17.9), (19.02, 20.12), (21.12, 23.02), (24.48, 25.94), (27.38, 30.0)]],
    "taunts 3":         [("taunt", a, b) for a, b in [(1.78, 2.86), (4.98, 6.06), (8.0, 9.92), (11.06, 12.12), (13.72, 14.96), (16.62, 17.96), (19.54, 21.64), (23.36, 25.66)]],
}
W = ["pew", "shot", "brrt", "ar", "sniper", "rocket", "toss"]
for memo, segs in {
    "weapons 1": [(1.52, 1.66), (2.92, 3.24), (4.38, 5.38), (7.74, 7.96), (9.68, 9.98), (11.36, 12.22), (13.08, 13.22)],
    "weapons 2": [(1.08, 1.78), (2.16, 2.48), (3.58, 4.54), (5.4, 5.78), (8.32, 9.0), (9.9, 10.26), (11.82, 12.12)],
    "weapons 3": [(1.04, 1.56), (2.26, 2.62), (4.0, 5.08), (6.18, 7.32), (8.44, 8.84), (10.22, 10.64), (11.58, 13.14)],
}.items():
    MAP[memo] = [(k, a, b) for k, (a, b) in zip(W, segs)]

MAXLEN = {"fall": 4.0}
PRE, POST = .04, .12

def main():
    out = "audio"
    for f in glob.glob(f"{out}/*.mp3"):
        os.remove(f)
    counts, manifest = {}, {}
    for memo, segs in MAP.items():
        src = f"raw/zip/{memo}.m4a"
        x = load(src)
        dur = len(x) / SR
        for i, (k, a, b) in enumerate(segs):
            nxt = segs[i+1][1] if i + 1 < len(segs) else dur
            a0 = max(0, a - PRE)
            b0 = min(nxt - .02, b + POST, dur)
            if k in MAXLEN:
                b0 = min(b0, a0 + MAXLEN[k])
            peak = np.abs(x[int(a0*SR):int(b0*SR)]).max()
            gain = 20*np.log10(0.89 / max(peak, 1e-4))
            counts[k] = counts.get(k, 0) + 1
            name = f"{k}_{counts[k]}"
            fo = max(.03, min(.25, (b0 - a0) * .2))
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                            "-af", f"atrim=start={a0:.3f}:end={b0:.3f},asetpts=PTS-STARTPTS,volume={gain:.2f}dB,afade=t=in:d=0.01,afade=t=out:st={b0-a0-fo:.3f}:d={fo:.3f}",
                            "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-q:a", "4", f"{out}/{name}.mp3"], check=True)
            manifest.setdefault(k, []).append(name)
    json.dump(manifest, open("blobs/audio_manifest.json", "w"), indent=0)
    print({k: len(v) for k, v in manifest.items()}, "total", sum(counts.values()))

if __name__ == "__main__":
    main()
