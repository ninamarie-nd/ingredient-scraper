# Eucerin (US) Audit — Content Mining Report

**Date audited:** 2026-10-16 (regraded with the unified grader under practitioner decisions D1 to D7)
**Products audited:** 48 listed: 3 graded, 45 ungradable (unresolved ingredients), 0 without ingredient text
**Source:** https://www.eucerinus.com/ (product names and retailer-printed ingredient lists; sources per row in the audit log)

**Read this first:** "Ungradable" is not a grade. It means at least one ingredient in the printed list is not in the reference (D4), so no tier is assigned (D7). Partial flags on ungradable products are for ranking only. The three graded products are graded from partial ingredient text and are provisional.

---

## Section A — Brand-level callout

**Headline finding:** Of 48 Eucerin products, 3 can be graded (1 Use Caution, 2 Avoid (Mild)), none are Puberty Safe, and 45 are ungradable because the reference does not cover at least one ingredient in each printed list.

**Tier distribution (48 products):**
- Puberty Safe: 0 (0%)
- Use Caution: 1 (2%)
- Avoid (Mild): 2 (4%)
- Avoid (Moderate): 0 (0%)
- Avoid (High Priority Swap): 0 (0%)
- Ungradable, counted separately: 45 (94%)

**Single most-flagged product:** Tinted Age Defense SPF 50 Face Sunscreen — 13 partial flags, ungradable. The most-flagged graded product is Advanced Hydration SPF 30 Sunscreen Spray, Avoid (Mild), 4 flags (Avobenzone, Homosalate, Octisalate, Octocrylene), graded from the four listed actives only.

**Cleanest product (if any):** Daily Hydration Lotion with Broad Spectrum SPF 15 — Use Caution, 1 flag (Octisalate). Its only captured ingredient text is "Octisalate (3.5)", so treat this grade as provisional.

**Content angle for Section A:**
"I tried to grade all 48 Eucerin products against the reference. Only 3 had ingredient lists I could grade, because most contain common base ingredients the reference does not yet cover." Say it as a coverage gap, not a verdict on the products.

---

## Section B — Pattern callouts

**Most common flagged ingredient:** Phenoxyethanol — flagged in 26 of 48 products (reference categories 1, 2, 4, 5, 8). Next: Dimethicone (15 products), Alcohol Denat (14), Ethylhexylglycerin (12).

**Most common risk category:** Category 4 (Allergies, Irritation, Corrosion) — flagged in 38 of 48 products. Category 2 (Endocrine Disruption) appears in 37 and Category 1 (Carcinogen) in 36. These counts include partial flags on ungradable products.

**"Clean marketing, dirty formula" finds:**
- Sensitive Mineral SPF 50 Sunscreen and Baby Sensitive Mineral SPF 50 Sunscreen Lotion. The product names say "Mineral." Each has 7 partial flags (Dimethicone, Cyclopentasiloxane, PEG-12 Dimethicone Crosspolymer, Propylene Glycol, 1,2-Hexanediol, Butyloctyl Salicylate, Cetyl PEG/PPG-10/1 Dimethicone) and 8 unknowns.
- Eczema Relief Flare-Up Treatment has 7 partial flags (Mineral Oil, PEG-40 Stearate, Decylene Glycol, 1,2-Hexanediol, Phenoxyethanol, Ethylhexylglycerin, BHT). The Eucerin Eczema Relief Hydrogel in the same line has 1.
- Baby Wash and Shampoo grades Avoid (Mild) on one flag (Sodium Myreth Sulfate, sulfate pattern). Provisional, see Section A.

**Repeated naming patterns:**
- Phenoxyethanol appears in 26 of 48 products.
- Silica appears in 6 SPF products. Under D1 its PFAS-treated tag does not escalate; its reference categories [1, 2] still count.
- Iron oxides appear in 3 products. Under D2 they carry category 3 (heavy metals) and the PFAS tag, which escalates the grade whenever they are present.

**Content angles for Section B:**
1. "Phenoxyethanol is in 26 of the 48 Eucerin products I checked. Here is what the reference says it is associated with." Use "associated with" wording.
2. "Three Eucerin products list iron oxides. The reference marks them category 1, 2 and 3, with the PFAS tag." Ungradable products still show it.
3. "The 'Mineral' sunscreens still list silicones and glycols." Stick to the printed list.

---

## Section C — Comparison angles

**Best vs worst within categories:**
- Sun protection: Best graded = Advanced Hydration SPF 30 Sunscreen Spray (Avoid (Mild), 4 flags, provisional). Worst = Tinted Age Defense SPF 50 Face Sunscreen (13 partial flags, ungradable).
- Eczema Relief: Best = Eucerin Eczema Relief Hydrogel (1 partial flag, 7 unknowns). Worst = Eczema Relief Flare-Up Treatment (7 partial flags, 9 unknowns).
- Baby: Best = Baby Lotion (0 partial flags, 1 unknown). Worst = Baby Eczema Relief Cream & Body Wash (5 partial flags, 14 unknowns).
- Cleansers: Hydrating Cleansing Gel, both sizes (0 partial flags, 5 unknowns each) vs Eucerin Advanced Cleansing Body and Face Wash (5 partial flags, 5 unknowns).

**Similar marketing, different grades:**
- Hydrating Cleansing Gel in 13.5 fl oz and 6.8 fl oz share one list and one count. Both are ungradable with 0 partial flags, so the size is not the variable.
- Eczema Relief Hydrogel and Eczema Relief Flare-Up Treatment sit in the same line. The hydrogel has 1 partial flag and the Flare-Up Treatment has 7.

**Cleanest in each category:**
- Sun protection: Advanced Hydration SPF 30 Sunscreen Spray (provisional, Avoid (Mild)).
- Daily hydration: Daily Hydration Lotion with Broad Spectrum SPF 15 (provisional, Use Caution).
- Baby: Baby Lotion (0 partial flags, 1 unknown).

**Content angles for Section C:**
1. "Same Eczema Relief line, 1 flag versus 7." (Hydrogel vs Flare-Up Treatment.)
2. "Two sizes of the Hydrating Cleansing Gel: same list, same unknowns." Use for a format-versus-formula point.
3. "Baby Lotion has 0 partial flags but one unknown ingredient. It can't be graded yet." Honest framing.

---

## Raw data summary

**Unknown ingredients (manual review queue):** 133 distinct names. Most frequent: Glycyrrhiza Inflata Root Extract (17 products), Caprylic/Capric Triglyceride (15), Octyldodecanol (13), Glyceryl Stearate (13), Isopropyl Palmitate (12), C12-15 Alkyl Benzoate (12), Lactic Acid (10), Hydroxyacetophenone (10). The full deduplicated list is in the Regrade section of `eucerin_audit_log.md`.

**Naming variant to decide:** Silica Dimethyl Silylate (5 products) is unknown. It is not the reference's "Silica Silylate" entry (categories 1 and 2, PFAS treated). If you decide it is an alias, those five products gain a PFAS escalation and a flag.

**Provisional grades:** The three graded products are graded from partial text (see the Anomalies section of the audit log). Do not publish their tiers until the full INCI lists are captured.
