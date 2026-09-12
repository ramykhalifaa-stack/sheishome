# www.sheishome.co.uk

The SHE website: a static site built from the approved page map
(`SHE_Website_Page_Map_Canva_Ready_FIXED`). Twenty one pages, no database, no server to keep
alive, nothing to pay for.

For the non technical steps to publish it and point the domain at it, read `GO-LIVE.md`.

## The stack, and why

| Piece | Choice | Reason |
| --- | --- | --- |
| Pages | Jinja2 templates rendered to plain HTML by `build.py` | Nothing to run in production, so hosting is free and the site cannot go down |
| Words | One Python file, `src/content/__init__.py` | Every sentence on the site is in one place and can be edited without touching markup |
| Styling | One stylesheet, `src/static/css/site.css` | Design tokens at the top, no build step, no framework |
| Motion | One script, `src/static/js/site.js` | Reveal on scroll, gentle parallax, a warm cursor light, a soft 3D tilt on the journals |
| Three dimensional touch | A shader sphere on the home and Join pages | Slow, warm and out of focus, so it reads as light rather than technology |
| Type | Playfair Display and DM Sans | Matches the lettering in the approved mockups |
| Photography | Cut from the mockups, enlarged four times with EDSR, then resampled to display size | Keeps the approved imagery and makes it sharp on large screens |

Motion is disabled for anyone whose device asks for reduced motion.

## Layout

```
build.py                 renders src/content + src/templates into dist/
deploy.sh                builds, copies dist to docs/, commits and pushes
src/content/__init__.py  every word on the site
src/templates/           base layout, macros and one template per page type
src/static/              stylesheet, script, images, brand marks
src/CNAME                the custom domain for GitHub Pages
tools/prep_sources.py    pulls the mockup plates out of the PDFs, paints out baked in
                         headline text and enlarges them four times (needs OpenCV)
tools/crop_assets.py     cuts the finished photographs from those plates
tools/social_card.py     the picture shown when a page is shared, and the touch icon
```

## Working on it

```bash
PY=/Users/ramy/Projects/reviews-and-response-system/.venv/bin/python

$PY build.py --serve     # http://localhost:8020, rebuilds when a file changes
$PY build.py             # one off build into dist/
./deploy.sh "message"    # build, commit, push
```

Re cutting the photography is only needed if a crop changes:

```bash
$PY tools/prep_sources.py     # about fifty minutes, writes the enlarged plates to the scratchpad
$PY tools/crop_assets.py      # seconds, writes src/static/img/*.webp
```

## Pages

Home, About, Join, The Chapters and its six chapter pages, Explore with one conversation and one
question, Gather with two events, Retreats and The Scottish Hills, Tools with The Becoming and
She's Glowing.

## House rules kept throughout

British English. No em dashes anywhere. Nothing on the site mentions automation or how anything
is built. No invented numbers: every date, price and quotation comes from the page map.

## The one connected piece

The Join form posts to `POST /she/join` on the ROSE platform, which stores the name and email
and shows them under Community in that dashboard, with a CSV download. Everything else on the
site is static.
