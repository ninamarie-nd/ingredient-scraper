# ATTITUDE Kids Audit Log

**Brand URL:** https://attitudeliving.com (Baby + Kids → Kids)
**Audit start:** 2026-07-09 ~18:10 UTC
**Audit end:** 2026-07-09 ~19:40 UTC
**Total elapsed:** ~1 h 30 min
**Scope:** Full ATTITUDE Kids line — one row per scent variant (per Nina-Marie's instruction). Bundle kit and gift card excluded (no single INCI list).

## Master product list (11 products, 32 scent variants)

1. 2-in-1 Kids Shampoo & Body Wash — body wash/shampoo/conditioner — 4 scents (Vanilla & Pear, Blueberry, Watermelon & Coco, Mango) — /products/2-in-1-kids-shampoo-body-wash
2. Kids Conditioner — body wash/shampoo/conditioner — 4 scents — /products/kids-conditioner
3. Kids Bubble Bath — body wash/shampoo/conditioner — 4 scents — /products/kids-bubble-bath
4. Kids Hair Detangler — hair styling (leave-on) — 2 scents (Watermelon & Coco, Vanilla & Pear) — /products/kids-hair-detangler
5. Kids Body Lotion — leave-on skincare — 2 scents (Watermelon & Coco, Mango) — /products/kids-body-lotion
6. Kids Foaming Hand Soap — rinse-off skincare — 4 scents — /products/kids-foaming-hand-soap
7. Kids Hand Sanitizer — other (leave-on) — 3 scents (Vanilla & Pear, Watermelon & Coco, Mango) — /products/kids-hand-sanitizer
8. Kids Fluoride Toothpaste — oral care — 3 flavours (Watermelon, Blueberry, Mango) — /products/kids-fluoride-toothpaste
9. Kids Fluoride-Free Toothpaste — oral care — 2 flavours (Mango, Coconut Mint) — /products/kids-fluoride-free-toothpaste
10. Kids Mineral Face & Body Sunscreen SPF 50 (lotion) — sunscreen — 2 (Unscented, Watermelon & Coco) — /products/kids-face-body-sunscreen-spf-50
11. Kids Mineral Sunscreen Stick SPF 50 — sunscreen — 2 (Unscented, Watermelon & Coco) — /products/kids-face-body-sunscreen-stick-spf-50

## Per-product status

- **2-in-1 Kids Shampoo & Body Wash:** complete — all 4 scents — Avoid (Moderate) (4–5 flags)
- **Kids Conditioner:** complete — all 4 scents — Avoid (Moderate) (1–2 flags)
- **Kids Bubble Bath:** complete — all 4 scents — Avoid (Moderate) (4–5 flags)
- **Kids Hair Detangler:** complete — both scents — Avoid (Moderate) (1–2 flags)
- **Kids Body Lotion:** complete — both scents — Avoid (Moderate) (1–2 flags)
- **Kids Foaming Hand Soap:** complete — all 4 scents — Avoid (Moderate) (2–3 flags)
- **Kids Hand Sanitizer:** complete — all 3 scents — Avoid (Moderate) (1 flag)
- **Kids Fluoride Toothpaste:** complete — all 3 flavours — Avoid (Moderate) (2–3 flags)
- **Kids Fluoride-Free Toothpaste:** complete — both flavours — Avoid (Moderate) (2–3 flags)
- **Kids Mineral Face & Body Sunscreen SPF 50 (lotion):** complete — both — Avoid (High Priority Swap) (3–5 flags; PFAS-silica escalation)
- **Kids Mineral Sunscreen Stick SPF 50:** complete — Unscented = Puberty Safe (0 flags); Watermelon & Coco = Avoid (Moderate) (2 flags)

## Failures

- None. All 11 products and 32 in-catalog scent variants captured with verbatim INCI.
- Excluded by rule: Kids Hair & Body Wash Kit (bundle — no single INCI) and e-gift card.

## Method notes

- attitudeliving.com is a JavaScript (Hydrogen/React) storefront; the standard Shopify `products.json` / `.js` endpoints are disabled (404). Ingredient lists render from per-variant `key_ingredients_content` metafields embedded in the page's flight data.
- Verbatim INCI per scent was extracted by decoding those metafields directly (validated against the live on-page ingredient panel for the 2-in-1 Wash across all four scents). Each scent carries a distinct fragrance/flavour tail on an otherwise-shared base.
- Product-type mapping: bubble bath and foaming hand soap classified with the wash family for the sulfate conditional; hand sanitizer and detangler treated as leave-on; toothpastes as oral care; sunscreens as sunscreen.

## Grading interpretation decisions (for Nina-Marie's review)

1. **Fragrance/flavour catch-all → Avoid (Moderate) minimum.** ATTITUDE discloses individual synthetic fragrance/flavour components but still prints a "*Fragrance (Parfum)" / "*Flavour (Aroma)" wrapper (undisclosed remainder). Per the rubric's "fragrance/parfum without full disclosure = full flag," this is treated as a full fragrance flag [1,2,4,8] → min Avoid (Moderate). This single decision is why 29 of 32 variants land at Moderate. If you prefer to credit the partial disclosure as a soft flag, most scented cosmetics would fall to Use Caution / Avoid (Mild).
2. **Plain Silica → PFAS escalation.** The reference note on Silica reads "Hydrated silica is acceptable / PFAS treated." The two Mineral Sunscreen *lotions* contain plain **Silica** (not hydrated), triggering the PFAS auto-escalation → Avoid (High Priority Swap). Toothpastes use **Hydrated Silica** (treated as acceptable, no flag). Recommend confirming the PFAS-treatment status of the sunscreen silica before publishing a hard claim.
3. **Zinc oxide / Mica** handled per conditional rules — non-nano zinc oxide in cream/stick = no flag; mica present but not first/main = no flag.
4. **Behentrimonium Methosulfate** (Kids Conditioner) — LOW TOX per reference, not flagged despite the -nium spelling, per rubric.

## Manual review queue (27 unique — all disclosed synthetic fragrance/flavour components not in the reference DB)

1,2-Dihydrolinalool; 2,6-Dimethyl-7-Octen-2-Ol; 2-T-Butylcyclohexyl Acetate; 3-Hexenol; 3-Hexyl Hexanoate; Alpha-Ionone; Butyl Isovalerate; Dimethyl Heptenal; Ethyl 2-Methylbutyrate; Ethyl Butyrate; Ethyl Hexanoate; Gamma-Decalactone; Gamma-Nonalactone; Gamma-Octalactone; Gamma-Undecalactone; Hexahydro-Methanoindenyl Propionate; Hexenol; Hexenyl Acetate; Hexyl Acetate; Hexyl Hexanoate; Isoamyl Acetate; L-Alpha-Pinene; Linalyl Acetate; Maltol; Methyldihydrojasmonate; Raspberry Ketone; Terpineol.

## Anomalies

- Source-copy quirks preserved verbatim (do not affect grading): Mango 2-in-1 Wash lists "Vaccinium Mytillus" (typo for Myrtillus) and "Isethionate,Lauryl" (missing space); Watermelon Conditioner prints "*fragrance" lowercase.
- The store's page data intermixes recommended-product and cross-sell variants; the authoritative per-product fragrance sets were confirmed against each product's own options block and on-page dropdown before scraping.
