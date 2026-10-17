# Aquaphor Audit — Content Mining Report

**Date audited:** 2026-10-16 (regraded with the unified grader under practitioner decisions D1 to D8)
**Products audited:** 41 listed: 2 graded, 36 ungradable (two or more unknown ingredients), 3 ungradable (no ingredient text)
**Source:** https://www.aquaphorus.com/ (product names and retailer-printed ingredient lists; sources per row in the audit log). aquaphor.com is an unrelated company and was not used.

**Read this first:** "Ungradable" is not a grade. Under D4, D7 and D8, a product with two or more ingredients the reference does not cover gets no tier, and a product with exactly one gets a Use Caution floor or keeps a higher tier from its other flags. Most Aquaphor products contain at least one common base ingredient the reference does not list, such as Caprylic/Capric Triglyceride, Shea Butter, Castor Seed Oil, or Lanolin Alcohol. Partial flags are shown for ranking only.

---

## Section A — Brand-level callout

**Headline finding:** Of 41 Aquaphor products, 2 can be graded, both Avoid (Moderate): the two Baby Wash & Shampoo listings, each with five flags and one unknown (Sea Salt). The other 39 are ungradable: 36 carry two or more unknown ingredients and 3 have no ingredient text. No product moved to Use Caution under D8. Bisabolol, a category 4 flag, appears in the partial flags of 27 of 41 products.

**Tier distribution (41 products):**
- Puberty Safe: 0 (0%)
- Use Caution: 0 (0%)
- Avoid (Mild): 0 (0%)
- Avoid (Moderate): 2 (5%)
- Avoid (High Priority Swap): 0 (0%)
- Ungradable, counted separately: 39 (95%), of which 36 carry two or more unknown ingredients (D7) and 3 have no ingredient text

**Single most-flagged product:** Aquaphor Lip Protectant + SPF 30 and Aquaphor Lip Protectant + SPF (Dual Pack) — 7 partial flags each: Petrolatum (category 1), Avobenzone, Octinoxate, Octisalate, Octocrylene, Oxybenzone (category 2), and BHT.

**Cleanest product (if any):** Aquaphor Lip Repair Stick Naturally Inspired, Aloe Vera and Coconut single packs — 0 partial flags each, with 11 and 9 unknowns. Zero flags here does not mean cleared.

**Content angle for Section A:**
"I tried to grade all 41 Aquaphor products. Two Baby Wash & Shampoo listings can be graded, and both come out Avoid (Moderate). The rest can't be graded yet, because the reference does not cover the base ingredients most of them share." Frame it as a coverage gap.

---

## Section B — Pattern callouts

**Most common flagged ingredient:** Bisabolol — in 27 of 41 products. It is a full category 4 flag under D3, because no chamomile oil or extract is printed beside it in any of these lists. Next: Petrolatum (18), Mineral Oil (14), Phenoxyethanol (9), Sodium Cetearyl Sulfate (8).

**Most common risk category:** Category 4 (Allergies, Irritation, Corrosion) and Category 1 (Carcinogen), each flagged in 29 of 41 products (partial flags).

**"Clean marketing, dirty formula" finds:**
- The two "Naturally Inspired" lip sticks are the only products with zero partial flags. Each still has 9 to 11 ingredients the reference does not cover, so neither can be graded.
- The Lip Protectant + SPF products carry seven partial flags, including sunscreen filters. A lip product with SPF is marketed differently from a plain lip balm, and the flags reflect that.

**Repeated naming patterns:**
- Bisabolol appears in 27 products, every time as a full flag under D3.
- Ceramide AP, NP and NG appear in 6 to 7 products each. Under D4 they are LOW TOX and are not flagged.
- Lanolin Alcohol appears in 14 products. The reference does not list it, so it is unknown under D4.

**Content angles for Section B:**
1. "Bisabolol is in 27 of the 41 Aquaphor products I checked. None of the printed lists names chamomile beside it, so the reference's category 4 flag applies in full." Use the caveat.
2. "The two Naturally Inspired lip sticks have zero flags and still have 9 to 11 ingredients the reference does not cover. Zero flags is not the same as cleared." Keep the framing.
3. "Lanolin Alcohol is in 14 of the 41 products. The reference does not list it, so I log it as unknown rather than assume it is low tox."

---

## Section C — Comparison angles

**Best vs worst within categories:**
- Chapped lips: Best = Naturally Inspired Aloe Vera Single Pack (0 partial flags, 11 unknowns). Worst = Lip Protectant + SPF (Dual Pack) (7 partial flags, 9 unknowns).
- Baby care: Best = Baby Healing Ointment (7oz) (3 partial flags, 2 unknowns). Worst = Baby Wash & Shampoo (25.4oz) (5 partial flags, 1 unknown; graded Avoid (Moderate) under D8).
- Cracked skin: Best = Healing Ointment (7oz) (3 partial flags, 2 unknowns). Worst = Foot Mask (5 partial flags, 11 unknowns).
- Diaper rash: Diaper Rash Paste (3.5oz) (0 partial flags, 5 unknowns). Diaper Rash Cream (3oz) has no ingredient text.

**Similar marketing, different grades:**
- Lip Repair Stick (plain) has 1 partial flag (Dimethicone). Lip Repair Stick + Sunscreen has 5 (four sunscreen filters and Dimethicone). The sunscreen version is the one with the extra flags.

**Cleanest in each category (with text):**
- Lip products: the Naturally Inspired Aloe Vera single pack (0 partial flags, 11 unknowns).
- Baby care: Baby Healing Ointment (7oz) (3 partial flags, 2 unknowns).
- Diaper rash: Diaper Rash Paste (0 partial flags, 5 unknowns).

**Content angles for Section C:**
1. "Same Aquaphor family, different lip products: 0 partial flags versus 7, and the difference is the sunscreen."
2. "Baby Healing Ointment (7oz) versus Baby Wash & Shampoo: 3 partial flags versus 5." Keep it to the printed lists.

---

## Raw data summary

**Unknown ingredients (manual review queue):** 48 distinct names. Most frequent: Caprylic/Capric Triglyceride (16 products), Butyrospermum Parkii (Shea) Butter (16), Ricinus Communis (Castor) Seed Oil (16), Ceresin (14), Lanolin Alcohol (13), Hydrogenated Castor Oil (12), Octyldodecanol (11), Tocopheryl Acetate (9). The full deduplicated list is in the Regrade section of `aquaphor_audit_log.md`.

**Ingredient text not captured:** Aquaphor Diaper Rash Cream (3oz.), Aquaphor Hand Mask, and Aquaphor Healing Ointment (2x.3.5oz).

**Naming decisions:** Lanolin Alcohol (D4) is the largest single decision for this brand. Under the reference it is not listed, so it stays unknown until you decide otherwise.

**D8 (2026-10-16, one unknown ingredient):** Two Baby Wash & Shampoo listings (25.4 oz and 16.9 fl oz) moved from ungradable to Avoid (Moderate) on one unknown, Sea Salt, with five flags. No product moved to Use Caution.
