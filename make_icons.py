# -*- coding: utf-8 -*-
"""Генерация иконок приложения «Полиглот»: глобус на индиго-фоне."""
from PIL import Image, ImageDraw

INDIGO = (79, 70, 229, 255)
WHITE = (255, 255, 255, 255)


def globe(draw, size, scale=1.0):
    """Рисует глобус: круг, меридианы, экватор."""
    cx = cy = size // 2
    r = int(size * 0.30 * scale)
    w = max(3, int(size * 0.045))
    thin = max(2, int(w * 0.6))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=w)
    # экватор и ось
    draw.line([cx - r, cy, cx + r, cy], fill=WHITE, width=thin)
    draw.line([cx, cy - r, cx, cy + r], fill=WHITE, width=thin)
    # два меридиана (узкие эллипсы)
    rx = int(r * 0.5)
    draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=WHITE, width=thin)
    ry = int(r * 0.5)
    draw.ellipse([cx - r, cy - ry, cx + r, cy + ry], outline=WHITE, width=thin)


def make(size, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        # сплошной фон до краёв, глобус в безопасной зоне (~70%)
        d.rectangle([0, 0, size, size], fill=INDIGO)
        globe(d, size, scale=0.7)
    else:
        rad = int(size * 0.22)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=INDIGO)
        globe(d, size)
    img.save(path)
    print(path, img.size)


if __name__ == "__main__":
    make(192, "icon-192.png")
    make(512, "icon-512.png")
    make(512, "icon-maskable-512.png", maskable=True)
