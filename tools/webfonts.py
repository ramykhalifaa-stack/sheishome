"""The two typefaces, served from our own site instead of Google's.

The site used to fetch Playfair Display and DM Sans from fonts.googleapis.com. On a phone
that means two new connections and two round trips before a single word can be drawn in the
right face. The same two typefaces are already in tools/fonts as variable TTF files, so this
cuts them down to the Latin letters the site uses, writes them as WOFF2 next to the pages,
and the browser gets them from the same connection as everything else.

Nothing is downloaded: the sources are the files already in the repository.

  build_fonts(Path("tools/fonts"), Path("dist/static/fonts"), Path(".fontcache"))
  -> {"ok": True, "css": "@font-face{...}", "preload": ["/static/fonts/dm-sans.woff2", ...]}

If fontTools or brotli are missing, it returns {"ok": False} and the build falls back to
Google Fonts, so the site still builds on a machine without them.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

# The Latin range Google Fonts serves, so the site keeps every character it can show today.
UNICODES = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
            "U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")

FACES = [
    # source file, published name, CSS family, the weights the site uses, and what to keep of
    # the file's built-in range. Keeping only the weights the site asks for halves the download.
    # DM Sans also carries an optical size axis; the site sets it nowhere, so it is fixed at the
    # text setting the typeface was drawn for.
    ("PlayfairDisplay.ttf", "playfair-display.woff2", "Playfair Display", "400 600",
     {"wght": (400, 400, 600)}),
    ("DMSans.ttf", "dm-sans.woff2", "DM Sans", "300 700",
     {"opsz": 14, "wght": (300, 400, 700)}),
]


def _subset(src: Path, out: Path, limits: dict) -> None:
    import tempfile

    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    trimmed_file = None
    if limits:
        trimmed = TTFont(str(src))
        instancer.instantiateVariableFont(trimmed, limits, inplace=True, updateFontNames=False)
        handle = tempfile.NamedTemporaryFile(suffix=".ttf", delete=False)
        handle.close()
        trimmed.save(handle.name)
        trimmed.close()
        src = trimmed_file = Path(handle.name)

    try:
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]      # keep kerning and ligatures
        options.name_IDs = ["*"]
        options.notdef_outline = True
        options.recalc_bounds = True
        font = subset.load_font(str(src), options)
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(unicodes=subset.parse_unicodes(UNICODES))
        subsetter.subset(font)
        subset.save_font(font, str(out), options)
        font.close()
    finally:
        if trimmed_file:
            trimmed_file.unlink(missing_ok=True)


def build_fonts(src_dir: Path, out_dir: Path, cache_dir: Path) -> dict:
    try:
        import fontTools  # noqa: F401
        import brotli  # noqa: F401
    except Exception:
        return {"ok": False}

    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    css, preload = [], []
    for source, name, family, weights, limits in FACES:
        src = src_dir / source
        if not src.exists():
            return {"ok": False}
        cached = cache_dir / name
        if not cached.exists() or cached.stat().st_mtime < src.stat().st_mtime:
            try:
                _subset(src, cached, limits)
            except Exception:
                return {"ok": False}
        dest = out_dir / name
        if not dest.exists():
            try:
                os.link(cached, dest)
            except OSError:
                shutil.copy2(cached, dest)
        url = f"/static/fonts/{name}"
        css.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
                   "src:url(%s) format('woff2')}" % (family, weights, url))
        preload.append(url)
    return {"ok": True, "css": "".join(css), "preload": preload}
