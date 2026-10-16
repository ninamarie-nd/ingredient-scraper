#!/bin/bash
# Double-click this file in Finder to push the Ingredient Scraper repo to GitHub.
# Alternatively, open Terminal and run:  bash ~/Desktop/Ingredient\ Scraper/push_to_github.command
cd "$(dirname "$0")"
echo "=== Pushing to github.com/ninamarie-nd/ingredient-scraper ==="
echo
git push --force -u origin main
echo
echo "Done. Press any key to close."
read -n 1 -s
