# Lubriderm Audit — Content Mining Report

**Date audited:** 2026-10-16 (regraded with the unified grader under practitioner decisions D1 to D7)
**Products audited:** 7 listed: 0 graded, 6 ungradable (unresolved ingredients), 1 ungradable (no ingredient text)
**Source:** https://www.lubriderm.com/

**Read this first:** "Ungradable" is not a grade. It means at least one printed ingredient is not in the reference (D4), so no tier is assigned (D7). Partial flags are for ranking only.

---

## Section A — Brand-level callout

**Headline finding:** None of the 7 Lubriderm products can be graded. Six contain at least one ingredient the reference does not cover, and the travel bundle has no ingredient text. Fragrance is printed in the ingredient list of Daily Moisture Lotion Fragrance-Free.

**Tier distribution (7 products):**
- Puberty Safe: 0 (0%)
- Use Caution: 0 (0%)
- Avoid (Mild): 0 (0%)
- Avoid (Moderate): 0 (0%)
- Avoid (High Priority Swap): 0 (0%)
- Ungradable, counted separately: 7 (100%), of which 6 have unresolved ingredients and 1 has no ingredient text

**Single most-flagged product:** Intense Skin Repair Lotion — 6 partial flags (Mineral Oil, Dimethicone, Carbomer, Ceteareth-20, Phenoxyethanol, Fragrance). Its list also includes a Polysorbate entry that the reference (REF.txt) marks as a flag but the grader's compiled reference does not, so the partial count is likely to rise.

**Cleanest product with text (if any):** Advanced Therapy Body Wash Fragrance-Free — 3 partial flags (Cocamidopropyl Betaine, PEG-80 Sorbitan Laurate, Sodium Cocoyl Isethionate), 6 unknowns. This is the lowest partial count with text, not a clean grade.

**Content angle for Section A:**
"I checked all seven Lubriderm products on the brand site. The one that says Fragrance-Free lists 'Fragrance' in its ingredient text. Check the package before posting." Keep the claim to the printed list.

---

## Section B — Pattern callouts

**Most common flagged ingredient:** Mineral Oil, Carbomer, Phenoxyethanol and Fragrance — each in the partial flags of 4 of 7 products.

**Most common risk category:** Categories 1 (Carcinogen), 2 (Endocrine Disruption), 4 (Allergies, Irritation, Corrosion) and 5 (Microbiome-Busting) — each in the partial flags of 6 of 7 products.

**"Clean marketing, dirty formula" finds:**
- Daily Moisture Lotion Fragrance-Free: the name says fragrance-free, but the printed list includes "Fragrance" (category 1, 2, 4 and 8, with no disclosure). Partial flags: 4.
- Daily Moisture Lotion (the standard version) prints an ingredient list identical to the Fragrance-Free version. The two lists match character for character, so one of the two pages may be showing the wrong list. Verify against the packages.
- Daily Moisture Body Wash Lightly Scented: 5 partial flags, including Fragrance. "Lightly Scented" is accurate for that flag.

**Repeated naming patterns:**
- Mineral Oil, Carbomer, Phenoxyethanol and Fragrance each appear in 4 of the 7 products.
- Fragrance appears in the partial flags of the Lightly Scented body wash and of the Fragrance-Free lotion. The Advanced Therapy Body Wash Fragrance-Free does not list it.

**Content angles for Section B:**
1. "The Fragrance-Free label and the printed list don't match. The list includes 'Fragrance.'" Use the printed text and recommend checking the package first.
2. "Two Lubriderm lotions print the same ingredient list. Their front-of-bottle claims differ." Verify first.
3. "Titanium dioxide in a Lubriderm lotion is not flagged, because the reference marks it as a concern only in sprays, powders and oral care." Explains a conditional rule without an alarm.

---

## Section C — Comparison angles

**Best vs worst within categories:**
- Lotions: Best (partial) = Daily Moisture Lotion Fragrance-Free (4 partial flags, 10 unknowns). Worst (partial) = Intense Skin Repair Lotion (6 partial flags, 14 unknowns). Advanced Therapy Lotion Fragrance-Free sits between them (5 partial flags, 9 unknowns).
- Body washes: Best (partial) = Advanced Therapy Body Wash Fragrance-Free (3 partial flags, 6 unknowns). Worst (partial) = Daily Moisture Body Wash Lightly Scented (5 partial flags, 6 unknowns).
- Bundle: no ingredient text, so not compared.

**Similar marketing, different grades:**
- Advanced Therapy Body Wash Fragrance-Free (3 partial flags) and Daily Moisture Body Wash Lightly Scented (5 partial flags) are both body washes. The Lightly Scented wash adds two entries to the shared surfactant flags: Fragrance and Glycol Distearate. Neither is graded.

**Cleanest in each category (partial, with text):**
- Lotions: Daily Moisture Lotion Fragrance-Free (4 partial flags).
- Body washes: Advanced Therapy Body Wash Fragrance-Free (3 partial flags).

**Content angles for Section C:**
1. "Advanced Therapy Body Wash Fragrance-Free versus Daily Moisture Body Wash Lightly Scented: 3 partial flags versus 5. The difference is the fragrance." Keep it to the printed lists.
2. "Intense Skin Repair Lotion has the most partial flags in the line, at 6." Note the Polysorbate gap first.

---

## Raw data summary

**Unknown ingredients (manual review queue):** 19 distinct names. Most frequent: Sodium Hydroxide (6 products), Avena Sativa (Oat) Kernel Oil (6), Butyrospermum Parkii (Shea) Butter (4), Caprylic/Capric Triglyceride (4), Disodium EDTA (3), Magnesium Aspartate (3), Zinc Gluconate (3), Copper Gluconate (3). The full deduplicated list is in the Regrade section of `lubriderm_audit_log.md`.

**Reference gap:** Polysorbate 20, 60 and 80 are in REF.txt (categories 1, 2, 4 and 5) but missing from the compiled reference. Under this grader they are unknown, which makes Intense Skin Repair Lotion and Advanced Therapy Lotion Fragrance-Free ungradable. Merging them into the compiled reference would add partial flags and would not make any Lubriderm product gradable.

**Ingredient text not captured:** Daily Moisture Lotion Fragrance-Free (24 fl oz, 2-count + 6 fl oz Travel Size) has no printed ingredient list in the data.
