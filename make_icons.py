#!/usr/bin/env python3
# 仅用标准库生成 PWA 图标（与主视觉一致的双轨方块 logo）。
import struct, zlib, os

def png_bytes(size, px):
    raw = bytearray()
    for row in px:
        raw.append(0)
        for (r, g, b, a) in row:
            raw += bytes((r, g, b, a))
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")

def inside(x, y, cx, cy, half, rad):
    dx = abs(x - cx); dy = abs(y - cy)
    if dx <= half - rad and dy <= half: return True
    if dx <= half and dy <= half - rad: return True
    if dx > half - rad and dy > half - rad:
        ex = dx - (half - rad); ey = dy - (half - rad)
        return ex * ex + ey * ey <= rad * rad
    return True

def make(size):
    top = (37, 99, 235); bot = (234, 88, 12)
    pad = 0.20 * size
    gap = 0.07 * size
    grid = size - 2 * pad
    cell = (grid - gap) / 2
    half = cell / 2
    rad = cell * 0.20
    step = cell + gap
    rows = []
    for y in range(size):
        t = y / (size - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        row = []
        for x in range(size):
            white = False
            for j in range(2):
                cx0 = pad + j * step
                for i in range(2):
                    cy0 = pad + i * step
                    cx = cx0 + half; cy = cy0 + half
                    if inside(x + 0.5, y + 0.5, cx, cy, half, rad):
                        white = True
            row.append((255, 255, 255, 255) if white else (r, g, b, 255))
        rows.append(row)
    return png_bytes(size, rows)

here = os.path.dirname(os.path.abspath(__file__))
for s, name in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")]:
    out = os.path.join(here, "icons", name)
    with open(out, "wb") as f:
        f.write(make(s))
    print("wrote", out, s, "px")
