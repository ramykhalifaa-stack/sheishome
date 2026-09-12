"""Build a copy of the site that works from any base path, for sharing a preview link.

The published site uses absolute paths (/static/..., /about/). A preview host serves the
site from a subdirectory, so every link and image here is rewritten to a relative path,
and the home page is written as page content only, without the outer document tags.

Run: python build.py && python tools/build_artifact.py
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = Path("/private/tmp/claude-501/-Users-ramy-Projects-reviews-and-response-system/a9e28590-5df1-44f4-bb62-ffbbdc476520/scratchpad/she/artifact")

ATTR = re.compile(r'(href|src)="/([^"]*)"')


def relative(html: str, depth: int) -> str:
    """Turn every site absolute path into one relative to a page at this depth."""
    up = "../" * depth

    def swap(m: re.Match) -> str:
        attr, path = m.group(1), m.group(2)
        if path.startswith("/"):          # protocol relative, leave alone
            return m.group(0)
        if path == "":
            target = "index.html"
        elif path.endswith("/"):
            target = path + "index.html"
        elif "#" in path and path.split("#")[0].endswith("/"):
            page, _, frag = path.partition("#")
            target = page + "index.html#" + frag
        else:
            target = path
        return f'{attr}="{up}{target}"'

    return ATTR.sub(swap, html)


def main() -> None:
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    shutil.copytree(DIST / "static", OUT / "static")

    pages = sorted(DIST.rglob("index.html")) + [DIST / "404.html"]
    for page in pages:
        rel = page.relative_to(DIST)
        depth = len(rel.parts) - 1
        html = relative(page.read_text(encoding="utf-8"), depth)
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if rel.as_posix() == "index.html":
            # The host wraps the entry page in its own document, so hand it page content only.
            title = re.search(r"<title>(.*?)</title>", html, re.S)
            head = re.findall(r'<link [^>]*>', html)
            body = re.search(r"<body>(.*)</body>", html, re.S)
            parts = [f"<title>{title.group(1)}</title>" if title else ""]
            parts += [tag for tag in head if "icon" not in tag]
            parts.append(body.group(1) if body else html)
            dest.write_text("\n".join(parts), encoding="utf-8")
        else:
            dest.write_text(html, encoding="utf-8")

    files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file())
    (OUT.parent / "artifact_files.txt").write_text("\n".join(files))
    print(f"{len(files)} files in {OUT}")


if __name__ == "__main__":
    main()
