# Grading Master Document

Single place for how products are graded. The rules here must match `scraper/grader.py` and `scraper/ref_compact.json`. Last updated 2026-11-02.

When a ruling changes a grade, update this file in the same commit, and regrade with a before-and-after count of tier changes before publishing.

---

## 1. Sources

| Source | Used for | Status |
|---|---|---|
| `Ingredient_Safety_Reference.pdf` (425 ingredients) | Authority for categories | Not every entry is reflected in the grader yet (see section 9). |
| `scraper/ref_compact.json` (`ref`) | The file the grader loads: ingredient → categories, low-tox flag, minimum tier, eczema flag | Source of truth for grading. Includes user rulings dated in section 10. |
| `scraper/ref_compact.json` (`aliases`) | Name variants → reference key | Source of truth for name matching. |
| `LOW_TOX` set in `grader.py` | Legacy neutral names | Still present; reference entries should take precedence. Review in section 9. |
| `PATTERN_WATCH` rules in `grader.py` | Name patterns for names not in the reference (quats, ethoxylates, glycols, etc.) | Applies only when a name is not in the reference. |
| `Ingredient_Safety_Reference_Addendum_2026-10-09.md` | Proposed additions | Not authoritative. Items are used only where copied into the reference with a dated ruling. |

---

## 2. Risk categories

1. Carcinogen
2. Endocrine disruption
3. Heavy metals (bio-accumulation)
4. Allergies, irritation, corrosion (does not count toward tier)
5. Microbiome-busting, skin barrier (does not count toward tier)
6. Microplastics (non-biodegradable polymers and silicones)
7. Acutely toxic
8. Respiratory irritant, asthmagen

Dashboard and copy use "associated with" or "flagged for." Never "causes."

---

## 3. Tiers (as coded)

Dashboard names: **Puberty Safe / Use Caution / Avoid (Mild) / Avoid (Moderate) / Avoid (High)**. Do not add tiers.

"Categories" below means distinct risk categories counted across all flagged ingredients, using categories 1, 2, 3, 6, 8, plus category 4 only for the surfactant exception in section 5e. Categories 4 and 5 otherwise do not count.

| Tier | Rule |
|---|---|
| Puberty Safe | No flagged ingredients. Irritation-only flags (category 4 alone) do not lower the tier. |
| Use Caution | 1 or 2 categories, and no paraben, fragrance, heavy metal, or formaldehyde releaser. Also: any Puberty Safe product with an unmapped ingredient drops to Use Caution. |
| Avoid (Mild) | 3 or more categories, OR any single ingredient with 3 or more categories, OR any paraben. |
| Avoid (Moderate) | Heavy metal (category 3), formaldehyde releaser, fragrance, OR 5 or more categories. |
| Avoid (High) | PFAS-treated ingredient, OR 8 or more categories, OR carcinogen (category 1) in a leave-on product, OR heavy metal together with a category 1 or 2 flag, OR endocrine disruption (3 or more category-2 ingredients, or 2 or more high-priority endocrine disruptors by name). |
| Minimum tiers | Any ingredient with a `min` tier in the reference sets at least that tier. Dyes are Avoid (High) (section 5f). |

Unknown ingredients: for any grade other than Puberty Safe, they don't change the tier. They are listed in the summary as "also N unknown ingredient(s)."

---

## 4. Scoring procedure

1. Take the verbatim INCI list exactly as printed. Keep it in the audit record.
2. Split on commas and semicolons. Drop "Ingredients:" headers, percentages, "(code …)" text, claim words, and non-ingredient footnotes. Keep digit-comma names like 1,2-hexanediol whole. "St. John's Wort" stays whole.
3. Normalize: lowercase, collapse spaces, remove asterisks, ® and ™, trailing footnote symbols (+, †, ±, ϝ, ᵻ, ϯ, ώ, and other trailing non-ASCII marks), trailing "+/", and trailing footnote digits.
4. Neutral: water (aqua, eau, and combinations) and glycerin.
5. Look up the name in the reference, then the aliases, then the name without its parenthetical, then the text inside it.
6. Low-tox entries: no flag.
7. Fragrance: any name containing fragrance, parfum, perfume, aroma, flavor, or flavour is a full flag (categories 1, 2, 4, 8).
8. Pattern rules for names not in the reference (section 1).
9. Anything still unmatched: unknown, for manual review.
10. Naturally occurring fragrance allergens (section 5d) are listed separately and do not add to the tier count.
11. Apply conditional rules (section 5a), minimum tiers, and escalations (section 7).
12. Assign the tier from section 3.

---

## 5. Rules

### 5a. Conditional rules
- Titanium dioxide: flagged in sprays, aerosols, powders, and oral care. Not a concern in creams or makeup.
- Mica: not a concern unless it is the first or main ingredient.
- Zeolite: avoid in powdered form only.
- Zinc oxide (non-nano): Puberty Safe in creams and lotions (user ruling 2026-11-02). Avoid in sprays and aerosols.
- Acetic acid (vinegar): flagged only for inhalation exposure.
- Enzymes (amylase, cellulase, subtilisin): flagged in powders. Lower concern in liquids.

### 5b. Hair products
- Quaternary ammonium (-nium) compounds are flagged.
- Behentrimonium methosulfate and fatty alcohols (cetearyl, cetyl, stearyl, behenyl, brassica): low tox, not flagged.
- Curl creams, gels, and stylers are graded as leave-on.
- Shampoos are rinse-off but used daily. Sulfate flags still trigger Avoid.

### 5c. Fragrance
- "Fragrance" or "Parfum" with no breakdown: full flag (categories 1, 2, 4, 8).
- "Natural fragrance" with no disclosure: full flag. "Natural" is not protective.
- "Fragrance (proprietary blend of essential oils)" with the oils disclosed elsewhere: soft flag.
- Individual essential oils named without a fragrance wrapper: no fragrance flag. Check for naturally occurring allergens.
- Fragrance chemicals named individually (hexyl cinnamal, citronellol, benzyl salicylate, benzyl benzoate, linalyl acetate, alpha-isomethyl ionone, menthol, pinene, terpineol, and others) are full flags (user ruling 2026-11-01).

### 5d. Naturally occurring allergens (soft)
Linalool, limonene, citral, citronellal, geraniol, eugenol, isoeugenol, coumarin, farnesol, hydroxycitronellal, benzyl alcohol from an essential oil, bisabolol. Soft only when the source essential oil is also listed. Standalone, they are full fragrance flags.

### 5e. Surfactant and betaine allergy flags (user ruling 2026-11-02)
Allergy (category 4) flags on surfactants and betaines count toward the tier. This is an exception to the general rule that category 4 does not count. Applies to the 30 surfactant and betaine names flagged in the Perplexity screen, marked `cnt4` in the reference. Other category 4 flags do not count.

### 5f. Colorants (user rulings 2026-11-01 and 2026-11-02)
- Any dye (FD&C, D&C, named dyes like Red 33, and CI codes in the dye ranges) is Avoid (High).
- Carmine (CI 75470) and annatto (CI 75120) are Avoid (High) because they carry CI numbers.
- CI 75130 (beta-carotene colorant) is Avoid (Mild) and is excluded from the dye rule.
- Plain "beta carotene" is a vitamin (low tox).
- Caramel is rated carcinogenic (category 1). Under section 3, a category 1 flag in a leave-on product makes it Avoid (High).
- Spirulina is Puberty Safe (user ruling 2026-11-02).
- Pigments: chromium oxide greens, chromium hydroxide green, ultramarines, bismuth oxychloride, and iron titanium oxide are category 3 (user ruling 2026-11-02). Ferric ferrocyanide and other pigments are pending research.

### 5g. Eczema-safe flag (separate from tier)
Eczema Safe = Puberty Safe AND no category 4 flag, AND no eczema-trigger ingredient. Trigger ingredients: wheat (including wheat amino acids), corn (zea mays), soy (including soy sterols and glycine soja), grape seed, rapeseed, and base alcohols (cetearyl, cetyl, stearyl, behenyl, lauryl, myristyl, oleyl, isostearyl, ethyl, isopropyl, SD alcohol, alcohol denat, ethanol). Benzyl alcohol is not a trigger. Corn, soy, rapeseed, and grape seed keep the Puberty Safe grade (user ruling 2026-11-01). They only affect the Eczema Safe flag.

### 5h. Essential oil blends and herbal blends
Essential oil blend and EO organic herbal blend are Puberty Safe (user ruling 2026-11-01).

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
- Formaldehyde releasers: minimum Avoid (Moderate). Names include DMDM hydantoin, diazolidinyl urea, imidazolidinyl urea, Quaternium-15, methenamine, paraformaldehyde, benzylhemiformal, 5-bromo-5-nitro-1,3-dioxane, sodium hydroxymethylglycinate, glyoxal, polyoxymethylene urea, and 2-bromo-2-nitropropane-1,3-diol.
- Carcinogen (category 1) in a leave-on product: Avoid (High).
- Endocrine disruption: see section 3.

---

## 8. Attitude products (exception)

- Tier comes from the fragrance-disclosure rule: each asterisked component is graded on its own. The umbrella "Fragrance (Parfum)" is not counted.
- Attitude fragrances are not described as essential oils only.
- Unknown components: the Puberty Safe to Use Caution rule applies.
- Only the irritation-only case moves an Attitude product to Puberty Safe.

---

## 9. Open items

1. Reference coverage: ~40 entries in `ref_compact.json` are not in the PDF, and some PDF categories are not yet reflected (for example titanium dioxide categories 1, 2, 3, and phenoxyethanol category 8). Reconcile against the PDF.
2. `LOW_TOX` in `grader.py` still holds names that are not in the reference. Move them into the reference or confirm they stay unknown.
3. Pigments pending: ferric ferrocyanide, bismuth oxychloride (beyond the category 3 ruling), CI 77491, zinc oxide CI 77947 (mapped to non-nano).
4. Fragments awaiting label check: "oils," "acid," "acetate," "sodium," "carbon." Source pages could not be fetched.
5. Calcium disodium EDTA: EDTA entries conflict.
6. Silicones and UV filters: classification pending for names not in the screen.
7. Tier wording: confirm whether section 3 thresholds count ingredients or categories everywhere. The code counts categories for the Use Caution, Avoid (Mild), and Avoid (Moderate) thresholds.

---

## 10. Dated rulings

| Date | Ruling |
|---|---|
| 2026-10-27 | Polysorbates flagged (categories 1, 2, 4, 5). PEG/PPG counts by name and by chemistry. |
| 2026-10-27 | Grader audit findings recorded (section 9 above). |
| 2026-11-01 | Any dye colorant is Avoid (High). |
| 2026-11-01 | Lavender-containing products stay Puberty Safe with a note that lavender may behave estrogenically. |
| 2026-11-01 | Corn, soy, rapeseed, and grape seed stay Puberty Safe. Wheat is not eczema safe. Base alcohols are not eczema safe. |
| 2026-11-01 | Fragrance chemicals listed by name are full flags. Beta-carotene is a vitamin. |
| 2026-11-01 | Propylene-based ingredients are marked petroleum-based. |
| 2026-11-02 | Caramel: category 1. Carmine and annatto: Avoid (High). CI 75130: Avoid (Mild). Spirulina and zinc oxide: Puberty Safe. |
| 2026-11-02 | Genistein: category 2 (endocrine). Microplastic candidates: category 6. Pigments (chromium, bismuth, ultramarine, iron titanium oxide): category 3. |
| 2026-11-02 | Surfactant and betaine allergy flags count toward the tier (section 5e). |
| 2026-11-02 | Royal jelly stays low tox. Spirulina stays Puberty Safe. |
