# Grading Master Document

Single place for how products are graded. Rules are here; the data and code must match this document. Last updated 2026-10-27.

---

## 1. Every source the grader uses today

The grader currently reads from several places. This is the full list, so nothing is hidden.

| # | Source | Entries | Used for | Status |
|---|---|---|---|---|
| 1 | `Ingredient_Safety_Reference.pdf` | 425 listed; 424 parsed | Master reference (categories, low-tox) | Authority. Not yet fully reflected in the grader. |
| 2 | `scraper/ref_compact.json` (`ref`) | 444 | The file the grader actually loads | Contains some entries not in the PDF, some wrong categories, and 3 corrupted keys. |
| 3 | `ref_compact.json` (repo root) | 442 | Not read by the grader | Older copy; retire it. |
| 4 | `ingredient_reference.json` (repo root) | 403 | Not read by the grader | Older copy; retire it. |
| 5 | `scraper/ref_compact.json` (`aliases`) and `ingredient_aliases.json` | 28 and 35 | Name variants | Two alias lists; merge into one. |
| 6 | `LOW_TOX` set inside `grader.py` | about 400 names | Neutral ingredients | Hard-coded. About 215 of these are not in any reference file, so they are treated as unknown. |
| 7 | `PATTERN_WATCH` rules inside `grader.py` | about 70 patterns | Flags for names not in the reference | Partly disagrees with the PDF (see section 6). |
| 8 | `Ingredient_Safety_Reference_Addendum_2026-10-09.md` | proposed | Proposed additions | Not sourced. Not in the grader except where copied into #2. |

Target: one reference file (PDF-derived), one alias list, and LOW_TOX and PATTERN_WATCH moved into the reference data. Until then, check all of these before trusting a grade.

---

## 2. Risk categories

1. Carcinogen
2. Endocrine disruption
3. Heavy metals (bio-accumulation)
4. Allergies, irritation, corrosion
5. Microbiome-busting (skin barrier)
6. Microplastics (non-biodegradable)
7. Acutely toxic
8. Respiratory irritant, asthmagen

---

## 3. Tiers

Dashboard names: **Puberty Safe / Use Caution / Avoid (Mild) / Avoid (Moderate) / Avoid (High)**. The rubric calls the last one "Avoid (High Priority Swap)".

| Tier | Rule (as you set it, and the rubric) |
|---|---|
| Puberty Safe | No flagged ingredients. Only low-tox and naturally occurring fragrance components. Irritation-only flags (category 4 alone) do not count. |
| Use Caution | 1 or 2 flagged ingredients, no paraben, fragrance, heavy metal, or formaldehyde-releaser. Also: a Puberty Safe product with any unknown ingredient drops to Use Caution. |
| Avoid (Mild) | 3 or more flagged ingredients, OR one ingredient with 3 or more categories, OR any paraben. |
| Avoid (Moderate) | Heavy metal (category 3), formaldehyde-releaser, or fragrance without disclosure, OR 5 or more flagged ingredients. |
| Avoid (High) | PFAS-treated ingredient, OR 8 or more flagged ingredients, OR carcinogen (category 1) in a leave-on, OR heavy metal + endocrine + fragrance, OR two or more high-priority endocrine disruptors, OR three or more endocrine (category 2) ingredients. |

Unknown ingredients: for any grade other than Puberty Safe, they don't change the tier. They are listed in the summary as "also N unknown ingredient(s): …".

Open: the rubric says "5+ flagged categories" for Avoid (Moderate) and "multiple flags" for Avoid (Mild). The code counts ingredients, not categories. See section 6.

---

## 4. Scoring procedure

1. Take the verbatim INCI list exactly as printed.
2. Split on commas and semicolons. Remove "Ingredients:" headers, percentages, and "(code …)" text. Keep 1,2-hexanediol and similar digit-comma names whole.
3. Normalize: lowercase, collapse spaces, remove asterisks and trailing punctuation.
4. Neutral: water (aqua, eau and combinations) and glycerin.
5. Look up the name in the reference, then the alias list, then the name without a parenthetical, then the text inside it.
6. Low-tox: no flag.
7. Fragrance: any name containing fragrance, parfum, perfume, aroma, flavor, flavour or flavoring is a full flag (categories 1, 2, 4, 8). "Natural Fragrance" is the same as "Fragrance (Parfum)".
8. Pattern families for names not in the reference (section 5).
9. Anything still unmatched: unknown, for manual review.
10. Naturally occurring allergens (section 5d) go to their own list, not the flag count.
11. Apply conditional rules (5a), then escalations (section 7).
12. Tally and assign a tier per section 3.

---

## 5. Rules

### 5a. Conditional rules (from the reference)
- Titanium dioxide (CI 77891): flagged in sprays, aerosols, powders, oral care; not a concern in cream skincare or makeup. Reference category: 1, 2, 3 (the PDF). The grader currently uses 1, 2 only and gates it by product type. Needs correcting.
- Mica: not a concern unless first or main ingredient.
- Zeolite: avoid in powdered form only.
- Zinc oxide (non-nano): low tox in creams and lotions; avoid in sprays and aerosols.
- Acetic acid (vinegar): flag only for inhalation exposure.
- Enzymes (amylase, cellulase, subtilisin): flag in powders; lower concern in liquids.

### 5b. Hair products
- Quaternary ammonium (-nium) compounds are flagged. Note in reports that quat-free conditioners are rare. This is context, not a softer grade.
- Behentrimonium methosulfate: low tox. Not flagged.
- Fatty alcohols (cetearyl, cetyl, stearyl, behenyl, brassica): low tox. Not flagged.
- Curl creams, gels, stylers: graded as leave-on.
- Shampoos: rinse-off but daily. Sulfate flags still trigger Avoid.

### 5c. Fragrance
- "Fragrance" or "Parfum" with no breakdown: full flag (1, 2, 4, 8).
- "Natural Fragrance" with no disclosure: full flag. "Natural" is not protective.
- "Fragrance (proprietary blend of essential oils)" with the oils disclosed elsewhere: soft flag.
- Individual essential oils named without a fragrance wrapper: no fragrance flag; check for naturally occurring allergens.

### 5d. Naturally occurring allergens (soft)
Linalool, limonene, citral, citronellal, geraniol, eugenol, isoeugenol, coumarin, farnesol, hydroxycitronellal, benzyl alcohol (from essential oil), bisabolol. Soft only when the source essential oil is also listed; standalone means full fragrance flags.

### 5e. Your decisions
- Water: exempt.
- Glycerin: left alone (not flagged, not unknown).
- Irritation-only flags (category 4 alone): shown, do not lower the tier. Affect Eczema Safe only.
- Eczema Safe: Puberty Safe AND no category 4 flag (including naturally occurring allergens in category 4).
- Polysorbates (20, 21, 40, 60, 61, 65, 80, 81, 85): flagged, categories 1, 2, 4, 5. Confirmed in the PDF.
- C14-16 Olefin Sulfonate: alias for Sodium C14-16 Olefin Sulfonate (category 4). Note: this entry is NOT in the PDF.
- PEG/PPG family: counts by name (PEG/PPG) AND by chemistry (any -eth, -pareth, or polysorbate ethoxylate).
- Unknown ingredients: see section 3.
- Spiral Spritz (Kinky-Curly): Puberty Safe as is, with two unknowns (Aloe Vera Gel, Vitamin B-5). Specific exception, not a general rule.
- Stellar Strands: Biotin, Silk Amino Acids, Collagen Amino Acids reviewed as fine.
- Attitude products: fragrance-disclosure rule (section 8).

---

## 6. Nasty 9 (final, not ranked)

These are the finalized nine ingredient families. Do not rank them.
1. Fragrance / Parfum
2. Phenoxyethanol
3. Quats (quaternary ammonium compounds)
4. PEG and PPG compounds
5. Sodium Laureth Sulfate and Sodium Lauryl Sulfate
6. UV filters (homosalate, octinoxate, octocrylene)
7. Parabens and phthalates
8. Aluminum (in antiperspirants)
9. Formaldehyde releasers (DMDM hydantoin, Quaternium-15)

---

## 7. Automatic escalations

- Heavy metals (category 3): minimum Avoid (Moderate). With a category 1 or 2 flag: Avoid (High).
- PFAS-treated ingredient: minimum Avoid (High).
- Formaldehyde releasers: minimum Avoid (Moderate). Names: DMDM hydantoin, diazolidinyl urea, imidazolidinyl urea, Quaternium-15, methenamine, paraformaldehyde, benzylhemiformal, 5-bromo-5-nitro-1,3-dioxane, sodium hydroxymethylglycinate, glyoxal, polyoxymethylene urea, 2-bromo-2-nitropropane-1,3-diol.

---

## 8. Attitude products (exception)

- Tier comes from the fragrance-disclosure rule: each asterisked component is graded on its own; the umbrella "Fragrance (Parfum)" is not counted.
- Attitude fragrances are not described as essential oils only.
- Unknown components: the Puberty Safe to Use Caution rule applies.
- Only the irritation-only case moves an Attitude product to Puberty Safe.

---

## 9. Grader audit (2026-10-27) — findings

Results of the line-by-line check against the PDF and a review of `grader.py`.

**Reference data**
1. Three corrupted keys in `scraper/ref_compact.json` (Capryleth-4, Laureth-23, Octylisothiazolinone). Octylisothiazolinone (categories 4, 5, 8) is silently ignored by the grader.
2. Benzophenone entry has the wrong category (3; PDF says 2).
3. Dimethicone: PDF categories 2 and 6; grader has 6 only. The skill also says 6 only.
4. Ethylhexylglycerin: PDF categories 4 and 5; grader has 4 only.
5. Phenoxyethanol: PDF categories 1, 2, 4, 5, 8; grader has 1, 2, 4, 5 (drops 8).
6. Titanium dioxide: PDF categories 1, 2, 3; grader has 1, 2.
7. In the PDF but missing from the grader's reference: Quaternium-15 (a formaldehyde releaser, but caught by a pattern), Nylon-12, Polyquaternium-9, C10-16 Pareth, Cocamidopropylamine Oxide, Alkyl C12-14 Dimethylethylbenzyl Ammonium Chloride, Dihydrogenated Tallow Benzylmonium Chloride, Polyethylene glycol (nonylphenol and octylphenol ethoxylates, four entries), Ammonium Acryloyldimethyltaurate/VP Copolymer (name differs).
8. In the grader's reference but not in the PDF (40 entries): for example 1,2-hexanediol (flagged 1 and 2 from the unsourced 2026-10-09 addendum), 2,3-butanediol, sodium C14-16 olefin sulfonate, disodium EDTA, alumina, iron oxides (PDF lists CI 77491, 77492, 77499 at 1, 2, 3), and about 20 low-tox entries.
9. About 215 low-tox names appear only in the hard-coded `LOW_TOX` set in `grader.py`. They include sodium hydroxide, caprylic/capric triglyceride, tocopheryl acetate, and glyceryl stearate. Separately, fragrance components such as hexyl cinnamal, citronellol, and benzyl salicylate are not in the reference, so they are unknown rather than flagged. Every one of them is currently treated as unknown.

**Grader logic**
10. `LOW_TOX` is checked only when the name is also in the reference, so names in `LOW_TOX` but not in the reference are treated as unknown. This is the cause of most unknowns.
11. Reference entries with no categories and not low-tox are skipped silently (three corrupted entries; see item 1).
12. Pattern rules apply only when a name is missing from the reference. So a wrong reference entry overrides a correct pattern.
13. Tier rules differ from the rubric in three places (section 3): Use Caution threshold (ingredients vs single-flag ingredients), Avoid (Mild) threshold ("multiple flags"), and Avoid (Moderate) "5+ categories" (code counts ingredients).
14. The unknown rule (Puberty Safe with an unknown becomes Use Caution) is implemented in `grader.py` but not yet applied to the dashboard. Applying it now would move 457 products, almost all because of item 9.

**Decisions needed before a regrade**
- A. Add the low-tox names from `LOW_TOX` to the reference (as low-tox), or keep them as unknown?
- B. Keep or remove the 40 entries not in the PDF?
- C. Use the PDF categories for the seven corrected entries in items 2–6?
- D. Tier threshold wording: ingredients or categories for Use Caution, Avoid (Mild), and Avoid (Moderate)?

---

## 10. Dashboard

- Tier counts and Eczema Safe count are recomputed on every regrade.
- Summaries drop the "[inferred: …]" tags.
- Attitude rows are kept unless approved otherwise.
- The dashboard does not yet show unknown-ingredient notes for non-Puberty-Safe grades. That display change is pending.

---

## 11. Changing this document

- A rule change updates this file and, if it changes grades, triggers a regrade with a before-and-after count of tier changes.
- Reference data changes go only in the one reference file, once it is consolidated.
- Dashboard pushes happen only after approval of the count.
