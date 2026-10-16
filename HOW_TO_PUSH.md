# How to push + go live on WordPress

## Step 1 — Push the repo to GitHub (2 min)

**Easiest: double-click `push_to_github.command`** in Finder.

Or in Terminal:

```
cd ~/Desktop/Ingredient\ Scraper
git push --force -u origin main
```

That's it — 248 files, 11.4 MB, ~1 minute.

If macOS blocks the `.command` file with "cannot be opened because it is from an unidentified developer":
right-click → Open → Open (confirm). You only have to do this once.

## Step 2 — Turn on GitHub Pages (1 click, 30 sec)

Open this URL:

**https://github.com/ninamarie-nd/ingredient-scraper/settings/pages**

Under "Build and deployment":
- Source: **Deploy from a branch**
- Branch: **main** / **/ (root)** → **Save**

GitHub will build and publish the site. Takes ~1 minute. When it's ready, the top of the page will show:

> Your site is live at `https://ninamarie-nd.github.io/ingredient-scraper/`

The dashboard URL will be:

**https://ninamarie-nd.github.io/ingredient-scraper/puberty_scanner_embed.html**

Open that in a new tab to confirm it loads.

## Step 3 — Update WordPress to use the GitHub Pages URL (3 min)

The current embed on doctorninamarie.com uses a one-off HTML file you uploaded manually. We're replacing that with an iframe that always loads the latest version from GitHub Pages — so from now on, when the dashboard updates, WordPress auto-updates with it.

1. In WordPress, open the Puberty Scanner page in **Elementor**.
2. Find the HTML widget (the one with the current dashboard code).
3. **Replace** everything in it with just this:

```html
<iframe
  src="https://ninamarie-nd.github.io/ingredient-scraper/puberty_scanner_embed.html"
  style="width:100%; height:100vh; border:none; display:block;"
  loading="lazy"
  allowfullscreen>
</iframe>
```

4. Save / Update the page.
5. View the live page — the dashboard should load inside the iframe.

That's it. From now on, every time the dashboard changes:
- I update the file in the Ingredient Scraper folder on your Mac
- You (or I, via a script) run `git push`
- GitHub Pages auto-rebuilds in ~1 min
- WordPress shows the new version automatically — no edits needed

## Step 4 — Revoke the GitHub token (30 sec, important)

The remote URL in `.git/config` has your GitHub Personal Access Token embedded. That token can push to this one repo. After the first successful push, revoke it:

1. Go to https://github.com/settings/tokens
2. Find the token (starts with `ghp_aHnTF…`) → **Delete**

Then tell me "PAT revoked" and I'll switch the remote URL to use the macOS keychain or `gh auth login` for future pushes.

(Even if you forget, the token auto-expires in 30 days.)

## Keeping the repo in sync later

Whenever we update anything in the folder (dashboard, grader, audits), you push with:

```
cd ~/Desktop/Ingredient\ Scraper
git add -A
git commit -m "describe what changed"
git push
```

Or just double-click a `push_to_github.command` I'll keep updated.

If you ever want to work on this project from a different laptop:

```
cd ~/Desktop
git clone https://github.com/ninamarie-nd/ingredient-scraper.git "Ingredient Scraper"
```

Everything will be there.
