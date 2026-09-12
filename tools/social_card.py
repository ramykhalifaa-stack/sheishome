"""Make the picture that appears when a SHE page is shared, plus the touch icon.

Run: python tools/social_card.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "src/static/img"
FONTS = Path(__file__).resolve().parent / "fonts"
CREAM = (247, 244, 239)
INK = (30, 30, 28)


def fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = size
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def width_of(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) + tracking for c in text) - tracking


def main() -> None:
    card = fit(Image.open(OUT / "home-hero.webp").convert("RGB"), (1200, 630))
    veil = Image.new("RGB", card.size, CREAM)
    card = Image.blend(card, veil, 0.42)
    d = ImageDraw.Draw(card)
    serif = ImageFont.truetype(str(FONTS / "PlayfairDisplay.ttf"), 150)
    sans = ImageFont.truetype(str(FONTS / "DMSans.ttf"), 26)
    w = width_of(d, "SHE", serif, 44)
    tracked(d, ((1200 - w) / 2, 210), "SHE", serif, INK, 44)
    line = "FOR EVERY CHAPTER OF BECOMING."
    w2 = width_of(d, line, sans, 6)
    tracked(d, ((1200 - w2) / 2, 400), line, sans, INK, 6)
    card.save(OUT / "og-she.jpg", "JPEG", quality=88, optimize=True)

    # Touch icon: the wordmark on cream, so a saved shortcut looks like the brand.
    icon = Image.new("RGB", (512, 512), CREAM)
    di = ImageDraw.Draw(icon)
    f = ImageFont.truetype(str(FONTS / "PlayfairDisplay.ttf"), 170)
    wi = width_of(di, "SHE", f, 26)
    tracked(di, ((512 - wi) / 2, 160), "SHE", f, INK, 26)
    icon.save(OUT / "apple-touch-icon.png", "PNG")
    print("og-she.jpg and apple-touch-icon.png written")


if __name__ == "__main__":
    main()
