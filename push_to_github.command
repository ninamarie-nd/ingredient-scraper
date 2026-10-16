#!/bin/bash
# Double-click to push the Ingredient Scraper repo to GitHub.
cd "$(dirname "$0")"
clear
echo "=================================================="
echo "  Pushing Ingredient Scraper → GitHub"
echo "=================================================="
echo
echo "Repo: github.com/ninamarie-nd/ingredient-scraper"
echo "Branch: main"
echo
git push --force -u origin main
EXIT=$?
echo
if [ $EXIT -eq 0 ]; then
    echo "=================================================="
    echo "  ✓ Push complete."
    echo "=================================================="
    echo
    echo "Next step: open this URL to turn on GitHub Pages"
    echo "https://github.com/ninamarie-nd/ingredient-scraper/settings/pages"
    echo
    echo "Full instructions: see HOW_TO_PUSH.md in this folder."
else
    echo "=================================================="
    echo "  ✗ Push failed (exit $EXIT)"
    echo "=================================================="
    echo
    echo "See HOW_TO_PUSH.md for help, or tell Claude what you see."
fi
echo
echo "Press any key to close this window."
read -n 1 -s
