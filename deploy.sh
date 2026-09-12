#!/usr/bin/env bash
# Build www.sheishome.co.uk and publish it.
# The built site is committed in the docs folder, which is what GitHub Pages,
# Cloudflare Pages and Vercel can all serve from.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-/Users/ramy/Projects/reviews-and-response-system/.venv/bin/python}"

"$PY" build.py
rm -rf docs
cp -R dist docs
touch docs/.nojekyll          # keep GitHub Pages from reprocessing the pages

git add -A
if git diff --cached --quiet; then
  echo "nothing changed"
  exit 0
fi
git commit -q -m "${1:-Update the site}"
if git remote get-url origin >/dev/null 2>&1; then
  git push -q origin main
  echo "pushed. The host will publish the new version within a minute or two."
else
  echo "committed. No remote set yet, so nothing was published."
fi
