# Vaseline Audit — Content Mining Report

**Date audited:** 2026-10-16 (regraded with the unified grader under practitioner decisions D1 to D7)
**Products audited:** 52 listed: 0 graded, 36 ungradable (unresolved ingredients), 16 ungradable (no ingredient text)
**Source:** https://www.vaseline.com/us/en/products.html (US site)

**Read this first:** "Ungradable" is not a grade. It means at least one printed ingredient is not in the reference (D4), so no tier is assigned (D7). Partial flags are for ranking only. Sixteen product pages show no ingredient text at all, so they cannot be checked from the data.

---

## Section A — Brand-level callout

**Headline finding:** None of the 52 Vaseline products can be graded: 36 contain at least one ingredient the reference does not cover, and 16 have no ingredient text on the product page. Petrolatum is among the partial flags for 30 products.

**Tier distribution (52 products):**
- Puberty Safe: 0 (0%)
- Use Caution: 0 (0%)
- Avoid (Mild): 0 (0%)
- Avoid (Moderate): 0 (0%)
- Avoid (High Priority Swap): 0 (0%)
- Ungradable, counted separately: 52 (100%), of which 36 have unresolved ingredients and 16 have no ingredient text

**Single most-flagged product:** Vaseline Intensive Care Cocoa Body Butter — 15 partial flags, including Petrolatum, Paraffin, Parfum (no disclosure), Methylparaben, BHT, and several silicones.

**Cleanest product with text (if any):** Vaseline Healing Jelly Original — 0 partial flags, 1 unknown ("White Petrolatum USP"). The printed ingredient is petrolatum under another name, so the zero is a naming gap, not a clean result. The same is true of Lip Therapy Advanced Healing Tube.

**Content angle for Section A:**
"I checked 52 Vaseline products. None can be graded yet: most contain base ingredients the reference does not cover, and 16 pages show no ingredient list at all." Do not describe the no-text products as clean or unclean.

---

## Section B — Pattern callouts

**Most common flagged ingredient:** Petrolatum — in the partial flags of 30 of 52 products. Next: Fragrance (Parfum) (20), Dimethicone (18), Phenoxyethanol (18), Linalool (18, a natural component flagged in full because no source essential oil is listed), Methylparaben (13).

**Most common risk category:** Category 1 (Carcinogen) — in the partial flags of 34 of 52 products. Category 2 and Category 4 each appear in 27 products, and Category 8 in 27.

**"Clean marketing, dirty formula" finds:**
- Vaseline Men Cooling Hydration Lotion: 11 partial flags, including Fragrance (Parfum), Methylparaben, Propylparaben, Carbomer, and Eugenol.
- Vaseline Intensive Care Cocoa Body Butter: 15 partial flags. It is the highest count in the brand, and most of the flags come from silicones, parabens, and fragrance.
- Vaseline Lip Therapy Rosy Lips Stick: 5 partial flags as printed, but one of them (cranberry extract, flagged as a quat) is a false positive from the naming pattern. Correct the count to 4 before using it.

**Repeated naming patterns:**
- Stearic Acid is the most common unknown in this brand (16 products). It is not in the reference.
- White Petrolatum USP appears in 2 products (Healing Jelly Original and Lip Therapy Advanced Healing Tube). The reference lists Petrolatum as category 1. Under D4 these stay unknown.
- Mica (CI 77019) is flagged in three shimmer products. The rubric says mica is not a concern unless it is the first or main ingredient. That conditional is not implemented, so these flags are overstated.

**Content angles for Section B:**
1. "Petrolatum is in the partial flags of 30 of the 52 Vaseline products I could read." Say "partial flags" and "reference category 1."
2. "Two Vaseline products list petrolatum under another name, White Petrolatum USP. The reference's Petrolatum entry does not match the name, so they show zero flags. That is a data gap, not a clean product." Use this to show the method, not to call the products clean.
3. "Vaseline Lip Therapy minis have one partial flag each. The Aloe Vera and Cocoa Butter sticks have four each, and Rosy Lips Stick has four after the false positive is removed." Check the lists before posting.

---

## Section C — Comparison angles

**Best vs worst within categories (with text):**
- Lip Therapy: Best = Original Mini (1 partial flag, 1 unknown). Worst = Rosy Lips Stick (5 partial flags as printed, 4 after the false positive; 14 unknowns).
- Intensive Care lotions and creams: Best = Cocoa Radiant Gel Oil (2 partial flags, 2 unknowns). Worst = Cocoa Body Butter (15 partial flags, 24 unknowns).
- Men: Men Fast Absorbing Lotion (10 partial flags, 10 unknowns) vs Men Cooling Hydration Lotion (11 partial flags, 13 unknowns) and Men Extra Strength Lotion (11 partial flags, 8 unknowns).
- Radiant X: Replenishing Hydrating Body Oil (5 partial flags, 6 unknowns) vs Even Tone Nourishing Body Lotion (9 partial flags, 17 unknowns).
- Shimmer and body oils: Sunlit Glow Body Shimmer Gel Oil (7 partial flags, 8 unknowns) vs Golden Hour Glow Bronze Body Shimmer Gel Oil (8 partial flags, 9 unknowns).

**Similar marketing, different grades:**
- Vaseline Intensive Care Cocoa Radiant Gel Oil (2 partial flags) and Vaseline Intensive Care Cocoa Body Butter (15 partial flags) share the "Cocoa Radiant" and "Intensive Care" names. The gel oil is the lower-flag version.
- Vaseline Lip Therapy Original Stick (1 partial flag, 9 unknowns) and Vaseline Lip Therapy Rosy Lips Stick (4 to 5 partial flags) both sit in the same line.

**Cleanest in each category (with text):**
- Lip Therapy: Original Mini (1 partial flag, 1 unknown).
- Intensive Care: Cocoa Radiant Gel Oil (2 partial flags, 2 unknowns).
- Radiant X: Replenishing Hydrating Body Oil (5 partial flags, 6 unknowns).

**Content angles for Section C:**
1. "The Cocoa Radiant gel oil has 2 partial flags. The Cocoa Body Butter has 15. Same brand, same names." Use the counts and the reference categories.
2. "Men Cooling versus Men Fast Absorbing: 11 versus 10 partial flags. Neither can be graded yet."

---

## Raw data summary

**Unknown ingredients (manual review queue):** 119 distinct names. Most frequent: Stearic Acid (16 products), Theobroma Cacao (Cocoa) Seed Butter (10), Glyceryl Stearate (8), Tocopheryl Acetate (8), Helianthus Annuus (Sunflower) Seed Oil (8), Glycol Stearate (7), Acrylates/C10-30 Alkyl Acrylate Crosspolymer (7), Hexyl Cinnamal (7). The full deduplicated list is in the Regrade section of `vaseline_audit_log.md`.

**Name variants to decide (D4):**
- White Petrolatum USP (2 products): the reference's Petrolatum entry is category 1. If you decide it is an alias, each product gains a Petrolatum flag and a "carcinogen in leave-on" escalation.
- Silica Dimethyl Silylate (Cocoa Shimmer Jelly Stick): see the Eucerin note.

**Known limits:** The Vaccinium false positive (Rosy Lips Stick) and the unimplemented mica conditional (three shimmer products) are listed in the audit log. Neither changes a tier here, since every product is ungradable, but both change the partial flags shown above.
