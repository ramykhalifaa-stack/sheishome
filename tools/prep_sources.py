"""Prepare high resolution source plates from the approved mockups.

The mockups live inside two PDFs in ~/Downloads. Both were exported from the same Canva
design, so where a page exists in both we take the lossless PNG rather than the JPEG.
Baked-in headline text is painted out first (so our own live text can sit on the photograph),
then every plate is enlarged four times with the EDSR neural upscaler. Crops are taken from
these plates by tools/crop_assets.py, so photographs stay sharp at full screen width.

Run: python tools/prep_sources.py [key ...]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import cv2
import numpy as np

SCRATCH = Path("/private/tmp/claude-501/-Users-ramy-Projects-reviews-and-response-system/a9e28590-5df1-44f4-bb62-ffbbdc476520/scratchpad/she")
PAGEMAP = SCRATCH / "pagemap"
WEBSITE = SCRATCH / "website"
OUT = SCRATCH / "x4"
MODEL = SCRATCH / "models/EDSR_x4.pb"
OUT.mkdir(parents=True, exist_ok=True)

# key: (file, scale of this plate against the page-map coordinates used by crop_assets, is_jpeg)
SOURCES: dict[str, tuple[Path, float, bool]] = {
    "home":       (WEBSITE / "w10_46.png", 1.0, False),
    "about":      (WEBSITE / "w08_37.png", 1.0, False),
    "join":       (WEBSITE / "w06_29.png", 1.0, False),
    "chapters":   (WEBSITE / "w03_17.png", 1.0, False),
    "becoming":   (PAGEMAP / "p06_801.png", 1.0, True),
    "resetting":  (PAGEMAP / "p07_815.png", 1.0, True),
    "blooming":   (PAGEMAP / "p08_829.png", 1.0, True),
    "rising":     (WEBSITE / "w02_11.png", 1.0, False),
    "lettinggo":  (PAGEMAP / "p10_857.png", 1.0, True),
    "beginning":  (PAGEMAP / "p11_871.png", 1.0, True),
    "explore":    (WEBSITE / "w12_54.png", 1.0, False),
    "conv":       (WEBSITE / "w14_62.png", 1.0, False),
    "question":   (WEBSITE / "w13_58.png", 1.0, False),
    "gather":     (WEBSITE / "w11_50.png", 1024 / 922, False),
    "cync":       (WEBSITE / "w17_75.png", 1.0, False),
    "coffee":     (WEBSITE / "w05_25.png", 1.0, False),
    "retreats":   (WEBSITE / "w19_83.png", 1225 / 735, False),
    "scottish":   (WEBSITE / "w09_42.png", 1.0, False),
    "tools":      (WEBSITE / "w16_70.png", 1.0, False),
    "becomingj":  (WEBSITE / "w20_87.png", 1.0, False),
    "glowing":    (WEBSITE / "w07_33.png", 1.0, False),
}

# Headline text baked into a photograph we want to reuse: painted out before enlarging.
# Boxes are in the plate's own pixels.
INPAINT: dict[str, list[tuple[int, int, int, int]]] = {
    "home": [(398, 118, 558, 184), (330, 185, 634, 203), (385, 205, 575, 231),
             (384, 243, 574, 277), (843, 163, 922, 277)],
    "about": [(377, 806, 648, 851)],
    "join": [(846, 160, 950, 250), (838, 1285, 968, 1355)],
}


def load(key: str) -> np.ndarray:
    path, _, is_jpeg = SOURCES[key]
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"missing plate: {path}")
    if is_jpeg:  # soften JPEG blocking so the upscaler does not amplify it
        img = cv2.bilateralFilter(img, 5, 18, 5)
    boxes = INPAINT.get(key, [])
    if boxes:
        mask = np.zeros(img.shape[:2], np.uint8)
        for box in boxes:
            cv2.rectangle(mask, (box[0], box[1]), (box[2], box[3]), 255, -1)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
        # The filled area sits on smooth sky, so a feathered blur there removes
        # the last trace of the lettering without touching anything around it.
        soft = cv2.GaussianBlur(img, (0, 0), 7)
        feather = cv2.GaussianBlur(cv2.dilate(mask, np.ones((9, 9), np.uint8)), (0, 0), 9)
        alpha = (feather.astype(np.float32) / 255.0)[:, :, None]
        img = (soft * alpha + img * (1 - alpha)).astype(np.uint8)
    return img


def upscale(img: np.ndarray, sr, tile: int = 240, pad: int = 24) -> np.ndarray:
    """EDSR x4, tile by tile with an overlap so seams do not show."""
    h, w = img.shape[:2]
    out = np.zeros((h * 4, w * 4, 3), np.uint8)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1, y1 = min(w, x + tile + pad), min(h, y + tile + pad)
            piece = sr.upsample(img[y0:y1, x0:x1])
            cx, cy = (x - x0) * 4, (y - y0) * 4
            cw, ch = (min(w, x + tile) - x) * 4, (min(h, y + tile) - y) * 4
            out[y * 4:y * 4 + ch, x * 4:x * 4 + cw] = piece[cy:cy + ch, cx:cx + cw]
    return out


def main() -> None:
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(MODEL))
    sr.setModel("edsr", 4)
    keys = sys.argv[1:] or list(SOURCES)
    for key in keys:
        dest = OUT / f"{key}.png"
        if dest.exists():
            print(f"{key}: already done", flush=True)
            continue
        started = time.time()
        img = load(key)
        big = upscale(img, sr)
        cv2.imwrite(str(dest), big, [cv2.IMWRITE_PNG_COMPRESSION, 4])
        print(f"{key}: {img.shape[1]}x{img.shape[0]} -> {big.shape[1]}x{big.shape[0]} "
              f"in {time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    main()
