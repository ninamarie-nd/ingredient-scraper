# Puberty Scanner — Ingredient Audit Database

Internal research tool for Dr. Nina-Marie Rueda, ND.

This repo contains:

- **`puberty_scanner_embed.html`** — the public-facing dashboard (deployed via GitHub Pages, embedded on doctorninamarie.com).
- **`products.json`** — master dataset: 4,327 products across 107 brands with ingredients, flags, tiers.
- **`audits/`** — per-brand audit spreadsheets, content-mining reports, and audit logs.
- **`scraper/`** — grader source (`grader.py`), compact reference database (`ref_compact.json`), and scraping scripts.
- **`Ingredient_Safety_Reference.pdf`** — 425-ingredient master database.
- **`GRADING_RUBRIC.pdf`**, **`AUDIT_WORKFLOW.pdf`**, **`OUTPUT_TEMPLATES.pdf`** — grading rubric and audit process documentation.

## Dashboard

Live at: https://ninamarie-nd.github.io/ingredient-scraper/puberty_scanner_embed.html

Embedded on doctorninamarie.com via iframe. Updates to `puberty_scanner_embed.html` on `main` auto-deploy to GitHub Pages within ~1 min, so no manual WordPress edits are needed to push changes.

## Grading rubric

Five tiers, in order of concern:
1. **Puberty Safe** — no flagged ingredients
2. **Use Caution** — 1–2 mild flags (e.g., naturally-occurring fragrance allergens)
3. **Avoid (Mild)** — 1–2 moderate flags
4. **Avoid (Moderate)** — 3+ flags, or 1 escalation (PFAS, formaldehyde-releaser, carcinogen in leave-on, endocrine disruption, heavy metals)
5. **Avoid (High Priority Swap)** — 2+ escalations

See `GRADING_RUBRIC.pdf` for the full rubric and `scraper/grader.py` for the implementation.
