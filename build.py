"""Build sheishome.co.uk: Jinja2 templates + content dictionaries -> dist/ (plain static files).

  python build.py               # build once
  python build.py --serve       # build and serve on http://localhost:8020, rebuilding on change
  python build.py --serve --port 8043

The build also makes the site fast on a phone:
  * resized copies of every photograph (tools/responsive_images.py), so a phone fetches a
    phone-sized picture instead of the desktop one;
  * srcset, sizes, width and height on every <img> (tools/markup.py), and a preload for the
    picture at the top of the page;
  * the two typefaces served from our own site (tools/webfonts.py) instead of Google's;
  * a _headers file so the host caches the pictures, styles and fonts for a long time.
"""
from __future__ import annotations

import hashlib
import http.server
import os
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
sys.path.insert(0, str(ROOT))

from tools.markup import responsive_images  # noqa: E402
from tools.responsive_images import build_images  # noqa: E402
from tools.webfonts import build_fonts  # noqa: E402

# How the host should cache each kind of file. Copied into dist as _headers (Cloudflare
# Pages and Netlify read it) and used by the local --serve preview so it behaves the same.
CACHE_RULES = [
    ("/static/css/*", "public, max-age=31536000, immutable"),
    ("/static/js/*", "public, max-age=31536000, immutable"),
    ("/static/fonts/*", "public, max-age=31536000, immutable"),
    ("/static/img/*", "public, max-age=2592000"),
    ("/static/*", "public, max-age=2592000"),
    ("/*", "public, max-age=300, must-revalidate"),
]

SITE = {
    "name": "SHE",
    "tagline": "Sacred Human Experience",
    "domain": "https://www.sheishome.co.uk",
    "description": "SHE is home. A space for every chapter of becoming: chapters, conversations, gatherings, retreats and journals for women, on their terms.",
    "nav": [("Home", "/"), ("About", "/about/"), ("The Chapters", "/chapters/"), ("Explore", "/explore/"), ("Gather", "/gather/"), ("Tools", "/tools/")],
    "footer_nav": [("Home", "/"), ("About", "/about/"), ("The Chapters", "/chapters/"), ("Explore", "/explore/"), ("Gather", "/gather/"), ("Tools", "/tools/"), ("Contact", "/join/#contact")],
    "join_url": "/join/",
    # Set when the community exists. Leave blank and the WhatsApp button says "coming soon".
    "whatsapp_url": "https://wa.me/447904582443",
    "beacons_url": "https://beacons.ai/sacredhumanexperience",
    # The Join form posts here (a small endpoint on the ROSE by SHE app). Blank disables the form.
    "signup_endpoint": "https://reviews-and-response-system-production.up.railway.app/she/join",
    "social": {"instagram": "https://instagram.com/", "pinterest": "https://pinterest.com/", "youtube": "https://youtube.com/"},
}


def _stamp(path: Path) -> str:
    """A short fingerprint of a file, so styles and scripts can be cached for a year."""
    try:
        return hashlib.sha1(path.read_bytes()).hexdigest()[:8]
    except OSError:
        return "0"


def build() -> int:
    import content  # src/content/__init__.py
    importlib.reload(content)
    env = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    # Build into a temporary folder, then swap it in, so the served site is never half-built.
    TMP = DIST.with_name(f"{DIST.name}.building-{os.getpid()}")
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SRC / "static", TMP / "static")
    for extra in ("CNAME", "robots.txt", "_headers"):
        if (SRC / extra).exists():
            shutil.copy(SRC / extra, TMP / extra)
    if not (TMP / "_headers").exists():
        (TMP / "_headers").write_text("".join(f"{p}\n  Cache-Control: {v}\n" for p, v in CACHE_RULES))

    pictures = build_images(SRC / "static" / "img", TMP / "static" / "img", ROOT / ".imgcache")
    fonts = build_fonts(ROOT / "tools" / "fonts", TMP / "static" / "fonts", ROOT / ".fontcache")
    assets = {"css": _stamp(SRC / "static" / "css" / "site.css"), "js": _stamp(SRC / "static" / "js" / "site.js")}

    def render(template: str, **context) -> str:
        html = env.get_template(template).render(site=SITE, fonts=fonts, assets=assets, **context)
        html, preload = responsive_images(html, pictures)
        return html.replace("<!--first-picture-preload-->", preload)

    pages = content.pages()
    for page in pages:
        out = TMP / page["path"].strip("/") / "index.html" if page["path"] != "/" else TMP / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page["template"], page=page, pages=pages, **page.get("data", {})), encoding="utf-8")
    (TMP / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE['domain']}{p['path']}</loc></url>\n"
                   for p in pages if not p.get("unlisted")) + "</urlset>\n")
    (TMP / "404.html").write_text(render("404.html", page={"title": "Not found", "path": "/404"}, pages=pages))
    OLD = DIST.with_name(f"{DIST.name}.old-{os.getpid()}")
    shutil.rmtree(OLD, ignore_errors=True)
    if DIST.exists():
        DIST.rename(OLD)
    TMP.rename(DIST)
    shutil.rmtree(OLD, ignore_errors=True)
    return len(pages)


def serve(port: int = 8020) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.1"  # keep the connection open, the way a real host does

        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(DIST), **k)

        def end_headers(self):
            path = self.path.split("?")[0]
            for pattern, value in CACHE_RULES:
                if path.startswith(pattern.rstrip("*")):
                    self.send_header("Cache-Control", value)
                    break
            super().end_headers()

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
    print(f"serving http://localhost:{port}")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    port = 8020
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    if "--serve" in sys.argv:
        serve(port)
    else:
        print(f"built {build()} pages into {DIST}")
