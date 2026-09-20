"""Put the founder's original photographs into the site's picture slots.

The first set of site images was cut out of a PDF mockup and enlarged, so many were soft. The
originals live in a folder of the founder's (subfolders named after the sections). A mapping file
says which original belongs in which slot, and which part of it must survive the crop.

Each slot keeps the shape it has today, because the page's CSS crops to fill (object-fit: cover)
and those shapes were chosen for the layout. Each new file is cropped to that shape around the
focus, resized (never enlarged more than MAX_ENLARGE, so nothing turns soft), sharpened a little,
and saved as .webp beside the old one.

Run: python tools/replace_photos.py mapping.json [--dry-run] [--only prefix]
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "src/static/img"
BACKUP = ROOT / "tools/.photo_backup"          # the version before this run, so a change can be undone
MAX_ENLARGE = 2.0                              # never blow a picture up by more than twice
QUALITY = 90

# Where the focus sits inside the picture, as a fraction of the way across or down.
FOCUS = {"centre": (0.5, 0.5), "top": (0.5, 0.18), "upper-third": (0.5, 0.3),
         "bottom": (0.5, 0.82), "lower-third": (0.5, 0.7), "left": (0.2, 0.5), "right": (0.8, 0.5)}


def crop_to(im: Image.Image, ratio: float, focus: str) -> Image.Image:
    """The largest crop of this shape that fits, placed around the focus."""
    w, h = im.size
    if w / h > ratio:                          # too wide: take a full-height slice
        nw, nh = int(round(h * ratio)), h
    else:                                      # too tall: take a full-width slice
        nw, nh = w, int(round(w / ratio))
    fx, fy = FOCUS.get(focus, FOCUS["centre"])
    x = min(max(int(round(w * fx - nw / 2)), 0), w - nw)
    y = min(max(int(round(h * fy - nh / 2)), 0), h - nh)
    return im.crop((x, y, x + nw, y + nh))


def finish(im: Image.Image, width: int) -> tuple[Image.Image, int]:
    """Resize to the slot's width and sharpen gently. Returns the picture and the width used."""
    used = min(width, int(im.size[0] * MAX_ENLARGE))
    height = int(round(used * im.size[1] / im.size[0]))
    if used > im.size[0]:                      # enlarging: go in two steps, which holds detail better
        mid = (int(round(im.size[0] ** 0.5 * used ** 0.5)), int(round(im.size[1] ** 0.5 * height ** 0.5)))
        im = im.resize(mid, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=40, threshold=3))
    im = im.resize((used, height), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=3)), used


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    only = argv[argv.index("--only") + 1] if "--only" in argv else ""
    mapping = json.loads(Path(argv[1]).read_text())
    BACKUP.mkdir(parents=True, exist_ok=True)
    done, skipped = 0, []
    for row in mapping:
        slot, source = row["slot"], row.get("source")
        if row.get("picture") == "keep" or not source:
            skipped.append((slot, "kept the picture that is there")); continue
        if only and not slot.startswith(only):
            continue
        target = IMG / f"{slot}.webp"
        size = row.get("size")                     # a brand new slot says its own shape
        if not size and not target.exists():
            skipped.append((slot, "no such slot")); continue
        size = tuple(size) if size else Image.open(target).size
        ratio = size[0] / size[1]
        src = Image.open(source)
        if src.mode not in ("RGB", "RGBA"):
            src = src.convert("RGB")
        keep_alpha = row.get("contain") and src.mode == "RGBA"
        out, used = finish(crop_to(src.convert("RGBA" if keep_alpha else "RGB"), ratio, row.get("focus", "centre")), size[0])
        note = f"{slot:26} {src.size[0]}x{src.size[1]} -> {out.size[0]}x{out.size[1]}"
        if used < size[0]:
            note += f"  (slot wants {size[0]}px; kept to {MAX_ENLARGE:g}x rather than soften it)"
        print(note)
        if not dry:
            if target.exists() and not (BACKUP / target.name).exists():
                shutil.copy2(target, BACKUP / target.name)
            out.save(target, "WEBP", quality=QUALITY, method=6)
        done += 1
    for slot, why in skipped:
        print(f"{slot:26} {why}")
    print(f"\n{done} picture{'' if done == 1 else 's'} {'would be' if dry else ''} replaced, {len(skipped)} left alone")
    print(f"The versions from before this run are in {BACKUP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
