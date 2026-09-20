"""Resized copies of every photograph, made at build time.

src/static/img stays the single source of truth. This writes smaller copies of each
picture (420, 640, 900, 1280, 1800 pixels wide, never larger than the original) into a
cache folder, then links them into dist/static/img, so a phone downloads a picture that
fits a phone instead of the desktop one.

Rerunning is cheap: a copy is only made when it is missing or older than its source.

  from tools.responsive_images import build_images
  manifest = build_images(Path("src/static/img"), Path("dist/static/img"), Path(".imgcache"))
  manifest["home-hero.webp"] -> {"w": 3200, "h": 1800, "srcset": [(420, "/static/img/home-hero-420.webp"), ...]}
"""
from __future__ import annotations

import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WIDTHS = (420, 640, 900, 1280, 1800)
QUALITY = 80
URL_BASE = "/static/img/"


def _targets(width: int) -> list[int]:
    """The ladder widths worth making for a source this wide (the original covers the rest)."""
    return [w for w in WIDTHS if w < width * 0.9]


def _resize(src: Path, out: Path, width: int) -> None:
    from PIL import Image

    with Image.open(src) as im:
        im = im.convert("RGBA" if ("A" in im.getbands() or "transparency" in im.info) else "RGB")
        height = max(1, round(im.height * width / im.width))
        im.resize((width, height), Image.LANCZOS).save(
            out, "WEBP", quality=QUALITY, method=6)
    os.utime(out, None)


def build_images(src_dir: Path, out_dir: Path, cache_dir: Path, verbose: bool = False) -> dict:
    """Make the resized copies, put every size in out_dir, return the srcset manifest."""
    from PIL import Image

    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = cache_dir / "sizes.json"
    try:
        meta = json.loads(meta_path.read_text())
    except Exception:
        meta = {}

    jobs, manifest, made = [], {}, 0
    for src in sorted(src_dir.glob("*.webp")):
        stamp = src.stat().st_mtime
        entry = meta.get(src.name)
        if not entry or entry.get("mtime") != stamp:
            with Image.open(src) as im:
                entry = {"mtime": stamp, "w": im.width, "h": im.height}
            meta[src.name] = entry
        width, height = entry["w"], entry["h"]
        sizes = [(width, URL_BASE + src.name)]
        for target in _targets(width):
            copy = cache_dir / f"{src.stem}-{target}.webp"
            if not copy.exists() or copy.stat().st_mtime < stamp:
                jobs.append((src, copy, target))
            sizes.append((target, URL_BASE + copy.name))
        sizes.sort()
        manifest[src.name] = {"w": width, "h": height, "srcset": sizes}

    if jobs:
        with ThreadPoolExecutor(max_workers=min(8, (os.cpu_count() or 4))) as pool:
            list(pool.map(lambda j: _resize(*j), jobs))
        made = len(jobs)
    meta_path.write_text(json.dumps(meta))

    # Put every size next to the original in dist. Hard links cost nothing and keep dist a
    # plain folder of files that any host can serve.
    for entry in manifest.values():
        for _, url in entry["srcset"]:
            name = url.rsplit("/", 1)[-1]
            dest = out_dir / name
            source = (src_dir if (src_dir / name).exists() else cache_dir) / name
            if dest.exists():
                continue
            try:
                os.link(source, dest)
            except OSError:
                shutil.copy2(source, dest)
    if verbose and made:
        print(f"made {made} resized pictures")
    return manifest
