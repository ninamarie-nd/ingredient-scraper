# Lubriderm Audit Log

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
