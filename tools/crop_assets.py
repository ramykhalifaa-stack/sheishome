"""Cut the photographs out of the enlarged mockup plates (see tools/prep_sources.py) into
web assets. Boxes are in the coordinate space of the original page-map slides; plates that were
exported at a different size carry a scale factor. Every asset is rendered from the four-times
plate and then resampled down to its display size, which is what keeps it looking crisp.

Run: python tools/prep_sources.py && python tools/crop_assets.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
PLATES = Path("/private/tmp/claude-501/-Users-ramy-Projects-reviews-and-response-system/a9e28590-5df1-44f4-bb62-ffbbdc476520/scratchpad/she/x4")
OUT = Path(__file__).resolve().parent.parent / "src/static/img"
OUT.mkdir(parents=True, exist_ok=True)

# Plates exported at a different size from the page-map slides the boxes were measured on.
SCALE: dict[str, float] = {"gather": 1024 / 922, "retreats": 1225 / 735}

# How wide the finished file should be. Full-bleed photographs need the most, small
# thumbnails the least. Anything not listed uses DEFAULT.
DEFAULT = 1500
WIDTHS: dict[str, int] = {
    "home-hero": 2600, "home-join": 2400, "about-hero": 2400, "about-strip": 2400,
    "about-bottom": 2200, "join-bottom": 2200, "chapters-bottom": 2200, "gather-hero": 2600,
    "explore-bottom": 1900, "tools-bottom": 2200, "scottish-bowls": 2200, "scottish-loch": 2400,
    "coffee-bottom": 2200, "cync-bottom": 2200, "question-hero": 1900, "story-main": 1900,
    "becoming-product-hero": 1900, "glowing-hero": 1900, "tools-hero": 1900, "chapters-hero": 1900,
}
PREFIX_WIDTHS: tuple[tuple[str, int], ...] = (
    ("tile-", 760), ("conv-", 760), ("q-", 760), ("related-", 760), ("qrelated-", 760),
    ("way-", 900), ("event-", 1000), ("prod-", 900), ("becoming-inside-", 900),
    ("story-side", 900), ("swatch", 400),
)


def width_for(name: str, native: int) -> int:
    if name in WIDTHS:
        want = WIDTHS[name]
    else:
        want = DEFAULT
        for prefix, value in PREFIX_WIDTHS:
            if name.startswith(prefix):
                want = value
                break
    return max(320, min(native, want))


CROPS: dict[str, tuple[str, tuple[int, int, int, int]]] = {
    # Home
    "home-hero": ("home", (0, 50, 959, 400)),
    "home-hero-left": ("home", (0, 50, 330, 400)),
    "home-hero-right": ("home", (640, 50, 959, 400)),
    "tile-becoming": ("home", (37, 520, 160, 665)),
    "tile-resetting": ("home", (183, 520, 313, 665)),
    "tile-blooming": ("home", (337, 520, 467, 665)),
    "tile-rising": ("home", (492, 520, 621, 665)),
    "tile-letting-go": ("home", (646, 520, 777, 665)),
    "tile-beginning-again": ("home", (800, 520, 930, 665)),
    "home-gather": ("home", (0, 740, 545, 985)),
    "home-explore": ("home", (450, 985, 959, 1200)),
    "home-tools": ("home", (0, 1205, 512, 1385)),
    "home-join": ("home", (300, 1390, 959, 1595)),
    # About
    "about-hero": ("about", (0, 265, 1024, 565)),
    "about-strip": ("about", (0, 785, 1024, 930)),
    "about-bottom": ("about", (0, 1400, 1024, 1536)),
    # Join
    "join-hero": ("join", (430, 50, 1024, 440)),
    "join-whatsapp": ("join", (0, 965, 545, 1225)),
    "join-bottom": ("join", (0, 1225, 790, 1450)),
    # Chapters landing
    "chapters-hero": ("chapters", (470, 70, 1024, 480)),
    "chapters-bottom": ("chapters", (0, 1400, 1024, 1536)),
    # Becoming
    "becoming-hero": ("becoming", (252, 42, 436, 278)),
    "becoming-1": ("becoming", (218, 285, 436, 415)),
    "becoming-2": ("becoming", (0, 420, 218, 585)),
    "becoming-3": ("becoming", (218, 595, 436, 705)),
    "becoming-4": ("becoming", (0, 715, 218, 825)),
    "becoming-explore": ("becoming", (25, 880, 140, 945)),
    "becoming-gather": ("becoming", (158, 880, 275, 945)),
    "becoming-tools": ("becoming", (295, 880, 412, 945)),
    # Resetting
    "resetting-hero": ("resetting", (190, 42, 428, 280)),
    "resetting-1": ("resetting", (0, 290, 214, 420)),
    "resetting-2": ("resetting", (218, 420, 428, 575)),
    "resetting-3": ("resetting", (0, 585, 214, 700)),
    "resetting-4": ("resetting", (218, 705, 428, 825)),
    "resetting-explore": ("resetting", (18, 880, 135, 945)),
    "resetting-gather": ("resetting", (153, 880, 270, 945)),
    "resetting-tools": ("resetting", (290, 880, 410, 945)),
    # Blooming
    "blooming-hero": ("blooming", (200, 42, 429, 280)),
    "blooming-1": ("blooming", (214, 283, 429, 415)),
    "blooming-2": ("blooming", (0, 420, 214, 580)),
    "blooming-3": ("blooming", (214, 585, 429, 695)),
    "blooming-4": ("blooming", (0, 700, 214, 830)),
    "blooming-explore": ("blooming", (18, 880, 135, 945)),
    "blooming-gather": ("blooming", (153, 880, 270, 945)),
    "blooming-tools": ("blooming", (290, 880, 410, 945)),
    # Rising
    "rising-hero": ("rising", (330, 55, 734, 360)),
    "rising-1": ("rising", (0, 390, 367, 660)),
    "rising-2": ("rising", (367, 675, 734, 905)),
    "rising-3": ("rising", (0, 925, 367, 1150)),
    "rising-4": ("rising", (380, 1105, 734, 1255)),
    "rising-5": ("rising", (0, 1420, 734, 1500)),
    "rising-explore": ("rising", (55, 1660, 247, 1760)),
    "rising-gather": ("rising", (272, 1660, 462, 1760)),
    "rising-tools": ("rising", (487, 1660, 680, 1760)),
    # Letting Go
    "letting-go-hero": ("lettinggo", (315, 50, 501, 300)),
    "letting-go-1": ("lettinggo", (255, 305, 501, 455)),
    "letting-go-2": ("lettinggo", (0, 460, 255, 655)),
    "letting-go-3": ("lettinggo", (255, 660, 501, 800)),
    "letting-go-4": ("lettinggo", (0, 805, 255, 955)),
    "letting-go-5": ("lettinggo", (255, 960, 501, 1105)),
    "letting-go-explore": ("lettinggo", (30, 1140, 165, 1225)),
    "letting-go-gather": ("lettinggo", (185, 1140, 320, 1225)),
    "letting-go-tools": ("lettinggo", (340, 1140, 475, 1225)),
    # Beginning Again
    "beginning-again-hero": ("beginning", (245, 50, 508, 300)),
    "beginning-again-1": ("beginning", (255, 305, 508, 455)),
    "beginning-again-2": ("beginning", (0, 460, 255, 650)),
    "beginning-again-3": ("beginning", (255, 660, 508, 800)),
    "beginning-again-4": ("beginning", (0, 805, 255, 955)),
    "beginning-again-5": ("beginning", (255, 960, 508, 1100)),
    "beginning-again-explore": ("beginning", (30, 1140, 165, 1225)),
    "beginning-again-gather": ("beginning", (185, 1140, 320, 1225)),
    "beginning-again-tools": ("beginning", (340, 1140, 475, 1225)),
    # Explore
    "explore-hero": ("explore", (475, 60, 971, 490)),
    "conv-1": ("explore", (400, 545, 565, 715)),
    "conv-2": ("explore", (580, 545, 745, 715)),
    "conv-3": ("explore", (760, 545, 925, 715)),
    "q-1": ("explore", (400, 910, 565, 1080)),
    "q-2": ("explore", (580, 910, 745, 1080)),
    "q-3": ("explore", (760, 910, 925, 1080)),
    "explore-bottom": ("explore", (0, 1265, 565, 1619)),
    # Conversation
    "story-side": ("conv", (705, 95, 978, 375)),
    "story-main": ("conv", (55, 380, 672, 715)),
    "story-mid": ("conv", (55, 1150, 672, 1360)),
    "related-1": ("conv", (705, 685, 818, 800)),
    "related-2": ("conv", (705, 820, 818, 940)),
    "related-3": ("conv", (705, 960, 818, 1075)),
    # Question
    "question-hero": ("question", (520, 140, 1024, 695)),
    "qrelated-1": ("question", (640, 1060, 770, 1150)),
    "qrelated-2": ("question", (640, 1180, 770, 1275)),
    "qrelated-3": ("question", (640, 1305, 770, 1400)),
    # Gather
    "gather-hero": ("gather", (405, 60, 922, 585)),
    "way-coffee": ("gather", (47, 705, 167, 840)),
    "way-circles": ("gather", (187, 705, 310, 840)),
    "way-workshops": ("gather", (328, 705, 455, 840)),
    "way-retreats": ("gather", (470, 705, 598, 840)),
    "way-special": ("gather", (613, 705, 740, 840)),
    "way-cities": ("gather", (755, 705, 878, 840)),
    "event-coffee": ("gather", (283, 1015, 468, 1160)),
    "event-retreat": ("gather", (488, 1015, 673, 1160)),
    "event-dinner": ("gather", (693, 1015, 878, 1160)),
    # Event: Create Your Next Chapter
    "cync-hero": ("cync", (430, 55, 1024, 545)),
    "cync-about": ("cync", (405, 560, 710, 865)),
    "cync-expect": ("cync", (432, 885, 708, 1200)),
    "cync-bottom": ("cync", (0, 1215, 620, 1440)),
    # Event: London Coffee Morning
    "coffee-hero": ("coffee", (425, 55, 1024, 515)),
    "coffee-about": ("coffee", (393, 525, 720, 840)),
    "coffee-left": ("coffee", (0, 850, 360, 1180)),
    "coffee-right": ("coffee", (708, 850, 1024, 1180)),
    "coffee-bottom": ("coffee", (320, 1185, 1024, 1440)),
    # Retreats landing (right-hand version of the two-up mockup)
    # The Scottish Hills
    "scottish-hero": ("scottish", (413, 55, 1024, 490)),
    "scottish-about": ("scottish", (390, 500, 745, 815)),
    "scottish-loch": ("scottish", (0, 825, 345, 1105)),
    "scottish-cup": ("scottish", (720, 825, 1024, 1105)),
    "scottish-bowls": ("scottish", (0, 1120, 345, 1320)),
    "scottish-journal": ("scottish", (690, 1120, 1024, 1320)),
    # Tools
    "tools-hero": ("tools", (300, 50, 1024, 400)),
    "tools-story": ("tools", (0, 405, 512, 730)),
    "tools-becoming": ("tools", (0, 735, 255, 965)),
    "tools-glowing": ("tools", (515, 735, 755, 965)),
    "prod-becoming-physical": ("tools", (60, 1060, 265, 1200)),
    "prod-becoming-digital": ("tools", (320, 1060, 455, 1200)),
    "prod-glowing-physical": ("tools", (545, 1060, 700, 1200)),
    "prod-glowing-digital": ("tools", (795, 1060, 930, 1200)),
    "tools-bottom": ("tools", (0, 1330, 660, 1490)),
    # The Becoming
    "becoming-product-hero": ("becomingj", (345, 45, 835, 370)),
    "becoming-why": ("becomingj", (430, 380, 835, 595)),
    "becoming-page": ("becomingj", (0, 605, 430, 875)),
    "becoming-inside-1": ("becomingj", (45, 985, 225, 1180)),
    "becoming-inside-2": ("becomingj", (235, 985, 415, 1180)),
    "becoming-inside-3": ("becomingj", (425, 985, 605, 1180)),
    "becoming-inside-4": ("becomingj", (615, 985, 795, 1180)),
    "becoming-physical": ("becomingj", (60, 1520, 205, 1700)),
    "becoming-digital": ("becomingj", (480, 1520, 590, 1700)),
    # She's Glowing
    "glowing-hero": ("glowing", (335, 50, 800, 395)),
    "glowing-belly": ("glowing", (380, 395, 800, 640)),
    "glowing-page": ("glowing", (0, 645, 415, 935)),
    "glowing-inside": ("glowing", (335, 1150, 800, 1400)),
    "glowing-cup": ("glowing", (0, 1410, 265, 1660)),
    "glowing-physical": ("glowing", (30, 1755, 155, 1920)),
    "glowing-digital": ("glowing", (430, 1755, 530, 1920)),
}


def main() -> None:
    only = set(sys.argv[1:])
    cache: dict[str, Image.Image] = {}
    made = []
    missing = set()
    for name, (src, box) in CROPS.items():
        if only and name not in only:
            continue
        plate = PLATES / f"{src}.png"
        if not plate.exists():
            missing.add(src)
            continue
        img = cache.get(src)
        if img is None:
            img = Image.open(plate).convert("RGB")
            cache = {src: img}          # one plate in memory at a time, they are large
        factor = SCALE.get(src, 1.0) * 4
        left, top, right, bottom = (int(round(v * factor)) for v in box)
        right, bottom = min(right, img.width), min(bottom, img.height)
        crop = img.crop((left, top, right, bottom))
        want = width_for(name, crop.width)
        if crop.width != want:
            height = max(1, round(crop.height * want / crop.width))
            crop = crop.resize((want, height), Image.LANCZOS)
        # Two-stage sharpening: a wide pass for depth, a fine pass for edge definition.
        crop = crop.filter(ImageFilter.UnsharpMask(radius=6, percent=22, threshold=3))
        crop = crop.filter(ImageFilter.UnsharpMask(radius=0.8, percent=55, threshold=2))
        crop.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)
        made.append((name, crop.size))
    for name, size in made:
        print(f"{name:26s} {size[0]}x{size[1]}")
    if missing:
        print("no plate yet for: " + ", ".join(sorted(missing)))
    print(f"{len(made)} assets written to {OUT}")


if __name__ == "__main__":
    main()
