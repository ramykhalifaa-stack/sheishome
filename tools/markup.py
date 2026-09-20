"""Finish the pictures in a rendered page.

Templates write a plain <img src="/static/img/name.webp" ...>. This adds, at build time:

  srcset          every resized copy, so a phone fetches a phone-sized file
  sizes           kept from the template, or 100vw when the template says nothing
  width, height   the real size of the picture, so the page does not jump while it loads
  loading         lazy for everything except the picture at the top of the page
  fetchpriority   high for the picture at the top of the page, which is what a visitor sees first

It also returns a <link rel="preload"> for that first picture, to be put in the head.
"""
from __future__ import annotations

import re

IMG = re.compile(r"<img\b([^>]*?)/?>", re.I | re.S)
ATTR = re.compile(r"""([:@a-zA-Z_][-:.\w]*)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?""")
SRC = re.compile(r"^/static/img/(.+\.webp)$")


def _attrs(blob: str) -> list[list[str | None]]:
    out = []
    for m in ATTR.finditer(blob):
        value = m.group(2) if m.group(2) is not None else (m.group(3) if m.group(3) is not None else m.group(4))
        out.append([m.group(1), value])
    return out


def _render(attrs) -> str:
    parts = []
    for name, value in attrs:
        parts.append(name if value is None else f'{name}="{value}"')
    return "<img " + " ".join(parts) + ">"


def responsive_images(html: str, manifest: dict) -> tuple[str, str]:
    """Return (html with finished <img> tags, preload link for the first picture)."""
    state = {"first": True, "preload": ""}

    def fix(match: re.Match) -> str:
        attrs = _attrs(match.group(1))
        by_name = {a[0].lower(): a for a in attrs}
        src = (by_name.get("src") or [None, ""])[1] or ""
        found = SRC.match(src)
        entry = manifest.get(found.group(1)) if found else None
        if not entry:
            return match.group(0)

        def put(name, value, overwrite=True):
            slot = by_name.get(name)
            if slot is None:
                slot = [name, value]
                attrs.append(slot)
                by_name[name] = slot
            elif overwrite:
                slot[1] = value

        def drop(name):
            if name in by_name:
                attrs.remove(by_name.pop(name))

        sizes = (by_name.get("sizes") or [None, None])[1] or "100vw"
        srcset = ", ".join(f"{url} {w}w" for w, url in entry["srcset"])
        if len(entry["srcset"]) > 1:
            put("srcset", srcset, overwrite=False)
            put("sizes", sizes)
        put("width", str(entry["w"]), overwrite=False)
        put("height", str(entry["h"]), overwrite=False)
        put("decoding", "async", overwrite=False)

        if state["first"]:
            state["first"] = False
            drop("loading")
            put("fetchpriority", "high")
            # With several sizes the preload names the same set as the tag, and no single
            # address: a browser that cannot read the set then skips the preload rather than
            # fetching the large original and the right size both.
            where = (f'imagesrcset="{srcset}" imagesizes="{sizes}"' if len(entry["srcset"]) > 1
                     else f'href="{src}"')
            # A hero inside a <picture> has a phone version of its own, so the preload must
            # follow the same rule. Otherwise a phone fetches the wide picture as well.
            before = html[:match.start()]
            cut = before.rfind("<picture")
            source = ""
            if cut != -1 and before.rfind("</picture>") < cut:
                head = before[cut:]
                media = re.search(r'<source[^>]*media="([^"]*)"[^>]*>', head)
                sset = re.search(r'<source[^>]*srcset="([^"]*)"[^>]*>', head)
                ssizes = re.search(r'<source[^>]*sizes="([^"]*)"[^>]*>', head)
                if media and sset:
                    source = (f'<link rel="preload" as="image" imagesrcset="{sset.group(1)}" '
                              f'imagesizes="{(ssizes.group(1) if ssizes else sizes)}" '
                              f'media="{media.group(1)}" fetchpriority="high">')
                    where += f' media="not all and ({media.group(1).strip("()")})"'
            state["preload"] = source + f'<link rel="preload" as="image" {where} fetchpriority="high">'
        else:
            put("loading", "lazy", overwrite=False)
        return _render(attrs)

    return IMG.sub(fix, html), state["preload"]
