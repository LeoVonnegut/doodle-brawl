import subprocess, sys, glob, os, json
import numpy as np

SR = 16000
FR = 0.02

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def envelope(x):
    n = int(SR * FR)
    k = len(x) // n
    fr = x[:k*n].reshape(k, n)
    rms = np.sqrt((fr**2).mean(1) + 1e-12)
    return 20*np.log10(rms)

def segments(db, thr, min_gap, min_len):
    on = db > thr
    segs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            segs.append([i, j]); i = j
        else:
            i += 1
    merged = []
    for s in segs:
        if merged and (s[0] - merged[-1][1]) * FR < min_gap:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [(a*FR, b*FR) for a, b in merged if (b - a)*FR >= min_len]

def scan(path, min_gap=0.35, min_len=0.08):
    x = load(path)
    db = envelope(x)
    floor = np.percentile(db, 15)
    peak = db.max()
    thr = max(floor + 12, peak - 38)
    segs = segments(db, thr, min_gap, min_len)
    info = []
    for a, b in segs:
        seg = db[int(a/FR):int(b/FR)]
        info.append((round(a, 2), round(b, 2), round(b-a, 2), round(float(seg.max() - peak), 1)))
    return len(x)/SR, info

if __name__ == "__main__":
    gap = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
    for p in sorted(glob.glob("raw/zip/*.m4a")):
        dur, info = scan(p, gap)
        print(f"{os.path.basename(p):32s} {dur:5.1f}s  n={len(info)}")
        print("    " + "  ".join(f"[{a}-{b} {d}s {pk}dB]" for a, b, d, pk in info))
