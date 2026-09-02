# -*- coding: utf-8 -*-
"""Иконки приложения «Нихао!»: иероглиф 你 на индиго-фоне."""
from PIL import Image, ImageDraw, ImageFont

INDIGO = (79, 70, 229, 255)
WHITE = (255, 255, 255, 255)
FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",    # Microsoft YaHei
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",  # SimHei
]


def load_font(px):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, px)
        except Exception:
            continue
    raise SystemExit("Не найден китайский шрифт (msyh/simhei)")


def make(size, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        # сплошной фон до краёв, знак в безопасной зоне
        d.rectangle([0, 0, size, size], fill=INDIGO)
        fpx = int(size * 0.42)
    else:
        rad = int(size * 0.22)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=INDIGO)
        fpx = int(size * 0.52)
    font = load_font(fpx)
    ch = "你"
    b = d.textbbox((0, 0), ch, font=font)
    w, h = b[2] - b[0], b[3] - b[1]
    d.text(((size - w) / 2 - b[0], (size - h) / 2 - b[1]), ch, font=font, fill=WHITE)
    img.save(path)
    print(path, img.size)


if __name__ == "__main__":
    make(192, "icon-192.png")
    make(512, "icon-512.png")
    make(512, "icon-maskable-512.png", maskable=True)
