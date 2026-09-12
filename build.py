"""Build sheishome.co.uk: Jinja2 templates + content dictionaries -> dist/ (plain static files).

  python build.py          # build once
  python build.py --serve  # build and serve on http://localhost:8020 with rebuild on change
"""
from __future__ import annotations

import http.server
import importlib
import shutil
import sys
import threading
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
SRC, DIST = ROOT / "src", ROOT / "dist"
sys.path.insert(0, str(SRC))

SITE = {
    "name": "SHE",
    "tagline": "Sacred Human Experience",
    "domain": "https://www.sheishome.co.uk",
    "description": "SHE is home. A space for every chapter of becoming: chapters, conversations, gatherings, retreats and journals for women, on their terms.",
    "nav": [("Home", "/"), ("About", "/about/"), ("The Chapters", "/chapters/"), ("Explore", "/explore/"), ("Gather", "/gather/"), ("Tools", "/tools/")],
    "footer_nav": [("Home", "/"), ("About", "/about/"), ("The Chapters", "/chapters/"), ("Explore", "/explore/"), ("Gather", "/gather/"), ("Tools", "/tools/"), ("Contact", "/join/#contact")],
    "join_url": "/join/",
    # Set when the community exists. Leave blank and the WhatsApp button says "coming soon".
    "whatsapp_url": "",
    # The Join form posts here (a small endpoint on the ROSE by SHE app). Blank disables the form.
    "signup_endpoint": "https://reviews-and-response-system-production.up.railway.app/she/join",
    "social": {"instagram": "https://instagram.com/", "pinterest": "https://pinterest.com/", "youtube": "https://youtube.com/"},
}


def build() -> int:
    import content  # src/content/__init__.py
    importlib.reload(content)
    env = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    # Build into a temporary folder, then swap it in, so the served site is never half-built.
    TMP = DIST.with_name(DIST.name + ".building")
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir()
    shutil.copytree(SRC / "static", TMP / "static")
    for extra in ("CNAME", "robots.txt"):
        if (SRC / extra).exists():
            shutil.copy(SRC / extra, TMP / extra)
    pages = content.pages()
    for page in pages:
        out = TMP / page["path"].strip("/") / "index.html" if page["path"] != "/" else TMP / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        html = env.get_template(page["template"]).render(site=SITE, page=page, pages=pages, **page.get("data", {}))
        out.write_text(html, encoding="utf-8")
    (TMP / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE['domain']}{p['path']}</loc></url>\n" for p in pages) + "</urlset>\n")
    (TMP / "404.html").write_text(env.get_template("404.html").render(site=SITE, page={"title": "Not found", "path": "/404"}))
    OLD = DIST.with_name(DIST.name + ".old")
    shutil.rmtree(OLD, ignore_errors=True)
    if DIST.exists():
        DIST.rename(OLD)
    TMP.rename(DIST)
    shutil.rmtree(OLD, ignore_errors=True)
    return len(pages)


def serve() -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(DIST), **k)

        def log_message(self, *a):
            pass

    def watch():
        stamp = 0.0
        while True:
            latest = max(p.stat().st_mtime for p in SRC.rglob("*") if p.is_file())
            if latest > stamp:
                stamp = latest
                try:
                    print(f"built {build()} pages")
                except Exception as exc:
                    print("build failed:", exc)
            time.sleep(1)

    threading.Thread(target=watch, daemon=True).start()
    print("serving http://localhost:8020")
    http.server.ThreadingHTTPServer(("127.0.0.1", 8020), Handler).serve_forever()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        serve()
    else:
        print(f"built {build()} pages into {DIST}")
