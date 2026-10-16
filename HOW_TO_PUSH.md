# How to push to GitHub

## One-time setup (do this ONE TIME, when you get back from workout)

**Option A — Double-click (easiest):**

1. Open Finder → Desktop → Ingredient Scraper
2. Double-click `push_to_github.command`
3. Wait ~1 minute for the push to finish
4. The Terminal window will say "Done. Press any key to close."

If macOS blocks it with "cannot be opened because it is from an unidentified developer":
- Right-click `push_to_github.command` → Open → Open (confirm)
- OR: System Settings → Privacy & Security → scroll down → "Open Anyway"

**Option B — Terminal:**

```
cd ~/Desktop/Ingredient\ Scraper
git push --force -u origin main
```

## What this uploads

- 248 files, 11.4 MB total
- One commit for the project state as of today
- A README.md with the project overview
- The `.gitignore` file (so junk like `.DS_Store` and `__pycache__` don't get tracked)

## After the push

Tell Claude "pushed" and I'll:
1. Enable GitHub Pages on the repo (so the dashboard goes live)
2. Give you the one-line iframe code to paste into WordPress
3. Confirm the dashboard loads from GitHub Pages

## Keeping the repo in sync later

Whenever we update the dashboard, I'll make the change in this folder. You then run:

```
cd ~/Desktop/Ingredient\ Scraper
git add -A
git commit -m "describe what changed"
git push
```

(Or just double-click a `push_to_github.command` I'll keep updated for you.)

The dashboard on WordPress will update automatically within ~1 minute — no more manual HTML uploads.

## Security — revoke the PAT after setup

The remote URL in `.git/config` has a GitHub Personal Access Token embedded. After the first successful push:

1. Go to https://github.com/settings/tokens
2. Delete the token that starts with `ghp_aHnTF...`
3. Tell Claude "PAT revoked" and I'll switch the remote URL to use macOS keychain or `gh auth`
