"""Draw media/icon.png: an operating-guide page with a check mark.

Original artwork for this repository (MIT, see LICENSE), drawn only from
geometric shapes; no font, photo or third-party image is used. It shares the
colour family of the extension icon but is a separate drawing.
Run: python3 media/make_icon.py   (needs Pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw

SIZE, SCALE = 256, 4
S = SIZE * SCALE
TOP, BOTTOM = (28, 58, 77), (29, 106, 97)   # dark blue-teal -> teal-green
PAGE, LINE, CHECK = (240, 246, 244), (120, 150, 156), (32, 168, 120)


def draw():
    gradient = Image.new("RGB", (S, S))
    pixels = gradient.load()
    for y in range(S):
        t = y / (S - 1)
        row = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM))
        for x in range(S):
            pixels[x, y] = row
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, S - 1, S - 1), radius=56 * SCALE, fill=255)
    icon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    icon.paste(gradient, (0, 0), mask)

    d = ImageDraw.Draw(icon)
    u = SCALE
    # Page with a folded top-right corner
    left, top, right, bottom, fold = 64 * u, 40 * u, 192 * u, 216 * u, 36 * u
    d.polygon([(left, top), (right - fold, top), (right, top + fold), (right, bottom), (left, bottom)], fill=PAGE)
    d.polygon([(right - fold, top), (right - fold, top + fold), (right, top + fold)], fill=(196, 214, 212))
    # Three text lines
    for i, width in enumerate((92, 76, 84)):
        y = (88 + i * 26) * u
        d.rounded_rectangle((84 * u, y, (84 + width) * u, y + 10 * u), radius=5 * u, fill=LINE)
    # Check mark in a circle, lower right
    cx, cy, r = 168 * u, 184 * u, 40 * u
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CHECK, outline=PAGE, width=6 * u)
    d.line([(cx - 20 * u, cy + 1 * u), (cx - 5 * u, cy + 16 * u), (cx + 21 * u, cy - 14 * u)],
           fill=PAGE, width=10 * u, joint="curve")
    return icon.resize((SIZE, SIZE), Image.LANCZOS)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "icon.png"
    draw().save(out, optimize=True)
    print(out)
