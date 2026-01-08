#!/usr/bin/env python3
import sys, pathlib

def ts(seconds: float) -> str:
    ms = int(round((seconds - int(seconds)) * 1000))
    base = int(seconds)
    h = base // 3600
    m = (base % 3600) // 60
    s = base % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def build(lines, duration):
    n = max(1, len(lines))
    slice_ = duration / n
    out = []
    for i, line in enumerate(lines, 1):
        start = (i-1)*slice_
        end = i*slice_
        out += [str(i), f"{ts(start)} --> {ts(end)}", line, ""]
    return '\n'.join(out)

if __name__ == '__main__':
    duration = float(sys.argv[1])
    out_path = sys.argv[2]
    lines = sys.argv[3:]
    pathlib.Path(out_path).write_text(build(lines, duration), encoding='utf-8')
