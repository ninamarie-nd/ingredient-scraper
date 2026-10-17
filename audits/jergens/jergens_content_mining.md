# Jergens Audit — Content Mining Report

**Date audited:** 2026-10-16 (regraded with the unified grader under practitioner decisions D1 to D8)
**Products audited:** 38 catalog items: 0 graded, 31 ungradable (two or more unknown ingredients), 7 ungradable (no ingredient text)
**Source:** https://us.jergens.com/ (Shop All and the category collections)

**Read this first:** "Ungradable" is not a grade. It means two or more printed ingredients are not in the reference (D4 and D7), so no tier is assigned. A product with exactly one such ingredient gets a Use Caution floor, or keeps a higher tier from its other flags (D8). Bundles and multi-shade pages merge several ingredient lists into one block, so their partial flags are not product counts. Do not publish bundle figures until each bundle's single-product lists are captured.

---

## Section A — Brand-level callout

**Headline finding:** None of the 38 Jergens products can be graded: 31 carry two or more ingredients the reference does not cover, and 7 have no ingredient text. No Jergens product has exactly one unknown, so the D8 floor changes nothing for this brand. Fragrance is in the partial flags of 29 products.

**Tier distribution (38 products):**
- Puberty Safe: 0 (0%)
- Use Caution: 0 (0%)
- Avoid (Mild): 0 (0%)
- Avoid (Moderate): 0 (0%)
- Avoid (High Priority Swap): 0 (0%)
- Ungradable, counted separately: 38 (100%), of which 31 carry two or more unknown ingredients (D7) and 7 have no ingredient text

**Single most-flagged product:** Natural Glow Wet Skin Moisturizer — 15 partial flags, including Fragrance (no disclosure) and Dimethicone. The highest overall count is the Gotta Glow Bundle at 22, but it merges several product lists, so it is not a product count.

**Cleanest product with text (if any):** Sparkling Berry Shea Fusion — 4 partial flags (Fragrance, Dimethicone, Ceteareth-20, Phenoxyethanol), 10 unknowns.

**Content angle for Section A:**
"I checked every Jergens product on the US site for a readable ingredient list. None can be graded yet, and seven pages show no ingredient list at all." Keep it about coverage and missing data.

---

## Section B — Pattern callouts

**Most common flagged ingredient:** Fragrance (no disclosure) — in the partial flags of 29 of 38 products. Next: Dimethicone (26), Ceteareth-20 (21), Phenoxyethanol (21), Mineral Oil (16), Methylparaben (15).

**Most common risk category:** Categories 1 (Carcinogen), 2 (Endocrine Disruption), 4 (Allergies, Irritation, Corrosion) and 5 (Microbiome-Busting) — each in the partial flags of 31 of 38 products.

**"Clean marketing, dirty formula" finds:**
- Natural Glow Wet Skin Moisturizer: the "Natural Glow" name, 15 partial flags, including Fragrance (no disclosure).
- Natural Glow Instant Sun Moisturizer + Bronzer: 14 partial flags, including Fragrance, Geraniol, and Limonene (natural components flagged in full because no source essential oil is listed).
- Ultra Healing Fragrance Free Moisturizer: the label says fragrance-free, but no ingredient text was captured, so the label cannot be checked from the data. Re-scrape it before any post.

**Repeated naming patterns:**
- Parabens are common. Methylparaben is in the partial flags of 15 products, and Ethylparaben is in others. Both are flagged under the paraben pattern (categories 2 and 4).
- Sodium Hydroxide (20 products) and Tocopheryl Acetate (20) are the most common unknowns. Neither is in the reference.

**Content angles for Section B:**
1. "Fragrance is in the printed list of 29 of the 38 Jergens products I checked." Note that bundle lists are merged, and that the count is partial.
2. "A product named 'Natural Glow' listed 15 partial flags. The name is marketing; the list is the part to read." Keep the wording neutral.
3. "The fragrance-free moisturizer has no ingredient list in my data. I can't check that label yet." Honest framing.

---

## Section C — Comparison angles

**Best vs worst within categories (with text):**
- Shea Fusions: Best = Sparkling Berry Shea Fusion (4 partial flags, 10 unknowns). Worst = Lavender Dreams Shea Fusion (8 partial flags, 11 unknowns).
- Everyday Lotions: Best = Original Scent Moisturizer (6 partial flags, 7 unknowns). Worst = Nourishing Honey Moisturizer (11 partial flags, 11 unknowns).
- Buildable Glow: Best = Natural Glow Hydra Gel (6 partial flags, 10 unknowns). Worst = Natural Glow + Firming Daily Moisturizer (12 partial flags, 18 unknowns).
- Vacation Skin (sun-related): Best = Natural Glow Instant Sun Drops (6 partial flags, 10 unknowns). Worst = Natural Glow Instant Sun Moisturizer + Bronzer (14 partial flags, 25 unknowns).
- In-shower: Best = Wet Skin Moisturizer Coconut Oil (6 partial flags, 6 unknowns). Worst = Natural Glow Wet Skin Moisturizer (15 partial flags, 14 unknowns).
- Bundles are excluded from this comparison because their lists are merged.

**Similar marketing, different grades:**
- Natural Glow Instant Sun Drops (6 partial flags) and Natural Glow Instant Sun Moisturizer + Bronzer (14 partial flags) share the "Natural Glow Instant Sun" name. The moisturizer-plus-bronzer adds a shade-specific bronzing list.
- Wet Skin Moisturizer Coconut Oil (6) and Wet Skin Moisturizer Shea Oil (7) share the same format. The coconut-oil version lists coconut oil, which the reference marks LOW TOX under D4 and does not flag.

**Cleanest in each category (with text):**
- Shea Fusions: Sparkling Berry Shea Fusion (4 partial flags).
- Everyday Lotions: Original Scent Moisturizer (6 partial flags).
- Buildable Glow: Natural Glow Hydra Gel (6 partial flags).
- Vacation Skin: Natural Glow Instant Sun Drops (6 partial flags).
- In-shower: Wet Skin Moisturizer Coconut Oil (6 partial flags).

**Content angles for Section C:**
1. "Two Natural Glow Instant Sun products, 6 partial flags and 14. The name is the same; the bronzer makes the difference."
2. "The Coconut Oil wet-skin moisturizer lists coconut oil, which the reference marks low tox. Its partial flags still come from fragrance and parabens." Keep it factual.

---

## Raw data summary

**Unknown ingredients (manual review queue):** 143 distinct names. Most frequent: Sodium Hydroxide (20 products), Tocopheryl Acetate (20), Stearic Acid (19), Arginine (14), Acrylates/C10-30 Alkyl Acrylate Crosspolymer (14), Butyrospermum Parkii (Shea) Butter (11), Ethylhexyl Isononanoate (10), Hydroxyacetophenone (10). The full deduplicated list is in the Regrade section of `jergens_audit_log.md`.

**Parser artifacts (not ingredients):** Bundle lists contain "||" separators, bracketed shade names (for example "[Glow Daily Moisturizer] Water"), repeated "FRAGRANCE INGREDIENTS:" blocks, and fragments such as "Caramel FRAGRANCE", "Ext. Violet 2", and "Ethylparaben With an illuminating HYDRALUCENCE blend". These stay unknown under D4, which is why the bundles are ungradable. Recapture the single-product pages.

**Botanicals not in the reference:** Cocos Nucifera (Coconut) Water and Cocos Nucifera (Coconut) Fruit Extract are unknown under D4. The coconut oil entry is LOW TOX and is not flagged.

**Old files in this folder:** `_grader_jergens.py`, `_master.py`, `_save.py`, and `_master_list.json` predate the unified grader. `_grader_jergens.py` is superseded by `_grader.py` and was not run.

**D8 (2026-10-16):** No product in this brand has exactly one unknown ingredient, so the Use Caution floor changes nothing here.
