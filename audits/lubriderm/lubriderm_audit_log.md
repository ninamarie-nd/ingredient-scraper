# Lubriderm Audit Log

> **Regrade 2026-10-16:** the per-product status and tier sections written before this regrade are superseded. The current grades are in the spreadsheet and in the Regrade section at the end of this log.

**Brand URL:** https://www.lubriderm.com/
**Audit start:** 2026-10-16T23:22:38Z
**Audit end:** 2026-10-16T23:27:18Z
**Total elapsed:** 4 min

## Master product list

Enumerated from https://www.lubriderm.com/products (single listing, 7 items; sidebar filter counts agree: Fragrance Free 4 + Lightly Scented 3 = 7). Category query parameter (?category=bundle-packs) did not change the listing. Homepage category links (Body Lotion, Body & Face Wash, Bundle Packs) are covered by these 7.

1. Daily Moisture Lotion Fragrance-Free | https://lubriderm.com/products/daily-moisture-lotion-fragrance-free | leave-on skincare
2. Daily Moisture Lotion | https://lubriderm.com/products/daily-moisture-lotion | leave-on skincare
3. Advanced Therapy Lotion Fragrance-Free | https://lubriderm.com/products/advanced-therapy-lotion-fragrance-free | leave-on skincare
4. Advanced Therapy Body Wash Fragrance-Free | https://lubriderm.com/products/advanced-therapy-body-wash-fragrancy-free | rinse-off skincare
5. Intense Skin Repair Lotion | https://lubriderm.com/products/intense-skin-repair-lotion | leave-on skincare
6. Daily Moisture Body Wash Lightly Scented | https://lubriderm.com/products/daily-moisture-body-wash-lightly-scented | rinse-off skincare
7. Daily Moisture Lotion Fragrance-Free 24 fl oz, 2-count + 6 fl oz Travel Size | https://lubriderm.com/products/daily-moisture-lotion-fragrance-free-24-fl-oz-2-count-6-fl-oz-travel-size | leave-on skincare

## Per-product status

1. Daily Moisture Lotion Fragrance-Free: complete. Tier Avoid (High Priority Swap), 5 flags. Printed list includes "Fragrance" despite the fragrance-free copy.
2. Daily Moisture Lotion: complete. Tier Avoid (High Priority Swap), 5 flags. Printed list identical to #1 (possible page error, flagged).
3. Advanced Therapy Lotion Fragrance-Free: complete. Tier Avoid (High Priority Swap), 6 flags (PFAS, carcinogen in leave-on escalations).
4. Advanced Therapy Body Wash Fragrance-Free: complete. Tier Avoid (Mild), 3 flags.
5. Intense Skin Repair Lotion: complete. Tier Avoid (High Priority Swap), 8 flags (PFAS, carcinogen in leave-on escalations).
6. Daily Moisture Body Wash Lightly Scented: complete. Tier Avoid (Moderate), 5 flags (fragrance).
7. Daily Moisture Lotion FF 24 fl oz + 6 fl oz Travel Size: ingredients not found on page. The printed INCI list is absent from the page text. The CMS holds a function-grouped explanation, not a verbatim list, so it was not used for grading.

## Failures

- Product 7 (travel bundle): ingredients not found on page. Not graded.

## Grading notes

- Lookup order: reference (ref_compact.json, with ingredient_aliases.json) first, then the pattern rules, then the team LOW TOX shortcut list, then the botanical rule. Carbomer and Sodium Cocoyl Isethionate are flagged by the reference, and the template's shortcut list would have exempted them, so the order was corrected.
- Polysorbate 60 is in Ingredient_Safety_Reference.pdf (categories 1, 2, 4, 5) but absent from ref_compact.json. Applied from the PDF (pdftotext check, 2026-10-16).
- Titanium dioxide: conditional rule applied (not a concern in cream/lotion skincare). Not flagged in any product.
- Pattern rules used: PEG-80 Sorbitan Laurate (PEG-), Ceteareth-20 (-eth), Disodium EDTA (-EDTA, category 4), Cocamidopropyl Betaine (reference). Glycol Distearate (reference, category 4).
- Shortcut-list items not in the reference (classed as no flag, per team list): Water, Glycerin, Potassium Cetyl Phosphate, Sodium Polyacrylate, Hydrogenated Palm Glycerides, Sorbitol, Palmitic Acid, Stearic Acid, Sodium Hydroxide, Lecithin, Caprylic/Capric Triglyceride, Panthenol, Tocopheryl Acetate, Sodium Benzoate, Potassium Sorbate, Sodium Citrate, Citric Acid, Caprylyl Glycol, Ceramide NP. The PDF confirms most of these as LOW TOX or lists them as cat 1-8 flags. The rest are not in the PDF.
- Hand checks on products 3, 4 and 6 matched the grader output before the Polysorbate 60 fix. Recheck is recommended after merging addendum entries.

## Manual review queue

Unique unknown ingredients (deduplicated, across all graded products):
- Acrylates/C10-30 Alkyl Acrylate Crosspolymer (Advanced Therapy Body Wash FF; Daily Moisture Body Wash Lightly Scented). Addendum analog Poly C10-30 Alkyl Acrylate is category 6. Tiers unchanged if applied.
- Avena Sativa (Oat) Kernel Flour (Advanced Therapy Body Wash FF; Daily Moisture Body Wash Lightly Scented)
- Copper Gluconate (Daily Moisture Lotion FF; Daily Moisture Lotion; Intense Skin Repair Lotion)
- Magnesium Aspartate (Daily Moisture Lotion FF; Daily Moisture Lotion; Intense Skin Repair Lotion)
- Zinc Gluconate (Daily Moisture Lotion FF; Daily Moisture Lotion; Intense Skin Repair Lotion)

## Anomalies

- Product 2 (Daily Moisture Lotion) printed ingredient list is character-identical to product 1 (Fragrance-Free) and includes "Fragrance." Verify against the package.
- Product 1 claims "Free of ... fragrance" but its printed list includes "Fragrance."
- Product 7 (travel bundle) has no printed INCI list in its visible text.
- Category filter query parameters on /products do not filter. Only 7 products exist on the page.
- No parabens, no formaldehyde-releasers, and no heavy metals (category 3) were flagged in any graded product.
- Reference gap: Polysorbate 60 is in the PDF but missing from ref_compact.json. Also missing from ref_compact.json (not verified in PDF): Copper Gluconate, Zinc Gluconate, Magnesium Aspartate, Avena Oat Kernel Flour.

## Regrade 2026-10-16: unified grader, practitioner decisions D1 to D7

**Provenance:** Every product was regraded from the verbatim text in `lubriderm_ingredients.json` (unchanged). The grader is `_grader.py`, the same file in all five brand folders, and it writes `lubriderm_audit.xlsx` and `_grade_summary.json`. The pre-regrade workbook is the git HEAD copy and was used only for the change table below.

### Practitioner decisions as applied

- **D1 Silica (plain "Silica" only).** Reference categories [1, 2] still count as a flag. The PFAS-treated escalation does not apply. A product that would otherwise grade Puberty Safe grades Use Caution. "Silica (hydrated)" is LOW TOX and is unchanged. "Silica Silylate" and "Trimethylsiloxysilicate" keep their PFAS tags. "Silica Dimethyl Silylate" is not in the reference and stays unknown under D4.
- **D2 Iron oxides (CI 77491, CI 77492, CI 77499, plain "iron oxides").** Categories [1, 2, 3] per the reference. Category 3 triggers the heavy-metal escalation (minimum Avoid (Moderate)). The PFAS tag is kept. The plain "iron oxides" entry carries the PFAS tag because its reference note aliases it to the three CI entries.
- **D3 Bisabolol.** Category 4 full flag. It is soft only when chamomile oil or extract is listed in the same product. No product in these five brands lists chamomile, so every bisabolol here is a full flag.
- **D4 Not in reference = unknown.** Ceramide (including the NP, AP, NG and 3 variants) and coconut oil are LOW TOX and are not flagged. Lanolin alcohol and botanical oils not in the reference are unknown. No reference entries were edited or added.
- **D5 Water** (Water, Aqua, Eau, and parenthetical forms such as "Water (Aqua)"). Clear: no flag, no unknown. Recorded in the explicit exception table in `_grader.py`.
- **D6 Glycerin.** Caution ingredient: no flag, no unknown. A product that would otherwise grade Puberty Safe grades Use Caution; otherwise the other flags decide. Recorded in the same exception table. Glycerin is not in the reference.
- **D7 Ungradable.** A product that still carries an unknown after D1 to D6 has tier `ungradable`, audit_status `needs review`, and its unknowns listed in audit_notes. A product with no ingredient text has tier `ungradable` and audit_status `ingredients not found`. flag_count and flagged_ingredients are still recorded. Ungradable is counted apart from the five tiers.

### Grader changes (minimal)

- One `_grader.py` in every brand folder. Its loader reads all three JSON layouts used by these brands: a `products` list, a `products` mapping, and a top-level mapping.
- Product URL falls back to a `url` key (Lubriderm).
- Added: the D5 and D6 exception table, the Use Caution floor for silica and glycerin, the `ungradable` tier with its status rules, and a separate ungradable count.
- No other grading rule was changed. The reference was not edited.

### Result

- Products: 7. Puberty Safe 0, Use Caution 0, Avoid (Mild) 0, Avoid (Moderate) 0, Avoid (High Priority Swap) 0.
- **Ungradable: 7 (counted separately from the five tiers).** 6 with unresolved ingredients under D4, 1 with no ingredient text.
- Moved from a graded tier to ungradable: 6. Moved from no tier to ungradable (no ingredient text): 1.
- Pre-regrade distribution (git HEAD): Avoid (High Priority Swap) 4, Avoid (Mild) 1, Avoid (Moderate) 1, (none) 1.
- Unique unknown ingredients remaining: 19.

### Products that changed tier

Pre-regrade tier from git HEAD, current tier from this regrade. "Unknowns left" is the number of distinct unknown ingredients still unresolved for that product.

| Product | Before | Now | Unknowns left | Reason |
|---|---|---|---|---|
| Daily Moisture Lotion Fragrance-Free | Avoid (High Priority Swap) | ungradable | 10 | D7: 10 unknown(s) remain |
| Daily Moisture Lotion | Avoid (High Priority Swap) | ungradable | 10 | D7: 10 unknown(s) remain |
| Advanced Therapy Lotion Fragrance-Free | Avoid (High Priority Swap) | ungradable | 9 | D7: 9 unknown(s) remain |
| Advanced Therapy Body Wash Fragrance-Free | Avoid (Mild) | ungradable | 6 | D7: 6 unknown(s) remain |
| Intense Skin Repair Lotion | Avoid (High Priority Swap) | ungradable | 14 | D7: 14 unknown(s) remain |
| Daily Moisture Body Wash Lightly Scented | Avoid (Moderate) | ungradable | 6 | D7: 6 unknown(s) remain |
| Daily Moisture Lotion Fragrance-Free 24 fl oz, 2-count + 6 fl oz Travel Size | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |

Products whose tier did not change: 0.

### Hand-check (two products)

- **Daily Moisture Lotion Fragrance-Free (glycerin D6).** Glycerin adds no flag and no unknown. Flags: Mineral Oil [1], Carbomer [1, 4, 6], Phenoxyethanol [1, 2, 4, 5, 8], and Fragrance [1, 2, 4, 8] with no disclosure. The printed list does include "Fragrance". Water is clear (D5). Stays ungradable with 10 unknowns.
- **Intense Skin Repair Lotion (unknowns, titanium dioxide conditional).** Titanium dioxide in a lotion is not a concern, so no flag. Flags: Mineral Oil, Dimethicone [2, 6], Carbomer, Ceteareth-20 (-eth pattern), Phenoxyethanol, Fragrance (6 total). The unknown list includes a Polysorbate entry. REF.txt marks Polysorbate 20, 60 and 80 as [1, 2, 4, 5], but ref_compact.json does not have them. Stays ungradable with 14 unknowns.

### Unique unknown ingredients remaining (manual review queue)

Each unknown is listed once, with the number of products it appears in. Counts are over all products, including ungradable ones.

- Avena Sativa (Oat) Kernel Oil (6)
- Sodium Hydroxide (6)
- Butyrospermum Parkii (Shea) Butter (4)
- Caprylic/Capric Triglyceride (4)
- Copper Gluconate (3)
- Disodium EDTA (3)
- Magnesium Aspartate (3)
- Tocopheryl Acetate (3)
- Zinc Gluconate (3)
- Acrylates/C10-30 Alkyl Acrylate Crosspolymer (2)
- Avena Sativa (Oat) Kernel Flour (2)
- Hydrogenated Palm Glycerides (2)
- Lecithin (2)
- Palmitic Acid (2)
- Polysorbate 60 (2)
- Potassium Cetyl Phosphate (2)
- Sodium Polyacrylate (2)
- Sorbitol (2)
- Stearic Acid (2)

### Known limits found during the regrade (not changed; outside D1 to D7)

- **Mica conditional not implemented.** The rubric says mica is not a concern unless it is the first or main ingredient. The grader flags Mica [1, 4] wherever it appears. Mica appears in no product in this brand.
- **`-nium` pattern false positive.** "Vaccinium" (the cranberry genus) matches the quat pattern. Flagged as [2] in Vaseline Lip Therapy Rosy Lips Stick. Partial flags only.
- **Reference gap.** REF.txt has Polysorbate 20, 60, 80 and Nylon-12, which ref_compact.json does not. Those ingredients stay unknown. Resolving them would change partial flags on 10 products across the five brands and would make no product gradable.

### Anomalies

- **Fragrance in a Fragrance-Free product.** The printed list for Daily Moisture Lotion Fragrance-Free includes "Fragrance", which is flagged [1, 2, 4, 8] with no disclosure. The same list, character for character, appears in the standard Daily Moisture Lotion, which the product copy describes as free of parabens, phthalates and dyes. Verify against the package before publishing.
- **Advanced Therapy Lotion Fragrance-Free** does not list "Fragrance" in its printed text.
- **Daily Moisture Lotion Fragrance-Free 24 fl oz, 2-count + 6 fl oz Travel Size** has no ingredient text. It is ungradable with no tier.
- **Polysorbate entries** are unknown in this grader (reference gap above). Under REF.txt they would add [1, 2, 4, 5] flags to the two lotions that carry them (Advanced Therapy Lotion Fragrance-Free and Intense Skin Repair Lotion).

## Regrade 2026-10-16, D8: one unknown ingredient gets a Use Caution floor

This section supersedes the tier counts and ungradable counts in the regrade sections above. Flags, escalations and unknown lists are unchanged by D8 (checked for every product row).

### Decision as applied

- D8 (practitioner, 2026-10-16): a product with exactly one unknown ingredient gets the Use Caution floor, the same way D1 and D6 work. A Puberty Safe product becomes Use Caution. A higher tier from the other flags is kept.
- The one unknown stays in unknown_ingredients and audit_notes. Status stays "complete" with the note "one unknown ingredient, Use Caution floor applied", except where the source JSON already carries a needs-review flag (see Open items).
- Two or more unknowns: still ungradable under D7. Products with no ingredient text: still "ingredients not found" with no tier.

### Grader change

- One grader for all five brands (`_grader.py`), copied into each brand folder with identical contents and pointed at its own folder. The D8 block sits directly before the D7 check. D7 now applies at two or more unknowns. The ungradable summary text now reads "two or more". No other rule changed.

### Tier counts, before and after D8

- Before D8 (D1 to D7): graded 0, ungradable 7 (no ingredient text: 1).
- After D8: Puberty Safe 0, Use Caution 0, Avoid (Mild) 0, Avoid (Moderate) 0, Avoid (High Priority Swap) 0; ungradable 7 (6 with two or more unknowns, 1 with no ingredient text). Total 7.

### Products that left ungradable under D8

None. No product in this brand has exactly one unknown ingredient.

### Hand checks (two products)

- **No product moved under D8.** The brand has no product with exactly one unknown.
- **Advanced Therapy Body Wash Fragrance-Free (stays ungradable, six unknowns).** Sodium Hydroxide and Tocopheryl Acetate are both absent from REF.txt. D7 applies correctly.
- **Intense Skin Repair Lotion (stays ungradable).** REF.txt lists Polysorbate 20 and Polysorbate 60 as categories 1, 2, 4 and 5. ref_compact.json has a malformed key for Polysorbate 20 and no usable entry for Polysorbate 60 or 80, so the grader treats them as unknown. This is a reference-compilation defect, not a grading decision, and it was not changed (the reference is not to be edited).

### Unique unknown ingredients remaining (manual review queue)

19 unique names in this brand (ignoring case), each still in the manual review queue. D8 does not remove any of them. Across all five brands: 308 unique names ignoring case, 354 distinct spellings as printed.

### Open items for the practitioner

- Polysorbate 20, 60 and 80 are missing or malformed in the compiled reference (see the hand check above). Intense Skin Repair Lotion is ungradable partly for this reason. Fixing the reference is the practitioner's decision; it was not changed here.

### Files written this pass

- `lubriderm/_grader.py` (D8 added), `lubriderm/lubriderm_audit.xlsx` (regenerated, 14 template columns), `lubriderm/_grade_summary.json` (regenerated), `lubriderm/lubriderm_content_mining.md`, and this log. The verbatim `lubriderm_ingredients.json` is unchanged.
