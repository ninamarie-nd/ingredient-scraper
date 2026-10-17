# Vaseline Audit Log

> **Regrade 2026-10-16:** the per-product status and tier sections written before this regrade are superseded. The current grades are in the spreadsheet and in the Regrade section at the end of this log.

**Brand URL:** https://www.vaseline.com/us/en/products.html
**Audit start:** 2026-10-16, approximately 23:12 UTC (estimated; no start time was logged at the outset)
**Audit end:** 2026-10-16, approximately 23:34 UTC (estimated)
**Total elapsed:** about 20 to 25 minutes (estimated)

## Method

- **Enumeration:** products.html loads 6 products, then a "Show More" control. Repeated clicks rendered 50 unique product links; further clicks stopped adding items while the control stayed on the page. Every category, range and skin-concern listing page (23 pages including products.html: 7 category pages, 8 range pages including clinical-care-lotions, which is empty, 7 skin-concern pages and 1 healing-jelly/tube page) was read from its server markup. The union gave 52 unique products. The two Pro VitaB3 lotions appear only on the Pro VitaB3 range page; they were not in the 50 rendered on the main listing. The sitemap lists no product detail URLs.
- **Ingredient capture:** Each product page's Ingredients section was read from the page (the same text get_page_text returns, trimmed to the Ingredients block) and copied into vaseline_ingredients.json as printed, including casing and typos. Deviation from the brief: product pages were read in batches from the browser page context, not with one get_page_text call per page. Three empty-block pages were confirmed with get_page_text on the rendered page (Vanilla Comfort Lotion, Cherry Aura Body Lotion, Original Healing Jelly Tube). Spot-check recommended on a sample of 5 products before publication, because the verbatim copy was transcribed from tool output.
- **Grading:** vaseline_grader.py, adapted from audits/briogeo/_grader.py. Paths repointed to /home/claude/ingredient-scraper. Logic changes from the template are listed under Anomalies.

## Master product list

Order is the scrape order. Status is the capture result.

1. Vaseline® Vanilla Comfort Trial & Travel Lotion | SKU 00305210049840 | Vanilla Comfort | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-vanilla-comfort-trial-and-travel-lotion.html/00305210049840
2. Vaseline Vanilla Comfort Lotion | SKU 00305210049864 | Vanilla Comfort | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-vanilla-comfort-lotion.html/00305210049864
3. Vaseline® Vanilla Comfort Gel Oil | SKU 00305210049963 | Vanilla Comfort | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-vanilla-comfort-gel-oil.html/00305210049963
4. Vaseline® Radiant X Firm & Restore Body Lotion | SKU 00305210047778 | Radiant X | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-radiant-x-firm-&-restore-body-lotion.html/00305210047778
5. Vaseline® Radiant X Even Tone Nourishing Body Lotion | SKU 00305210046788 | Radiant X | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-radiant-x-even-tone-body-lotion.html/00305210046788
6. Vaseline® Radiant X Replenishing Hydrating Body Oil | SKU 00305210046702 | Radiant X | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-radiant-x-replenishing-body-oil.html/00305210046702
7. Vaseline® Radiant X Deep Nourishment Body Cream | SKU 00305210046740 | Radiant X | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-radiant-x-deep-nourishment-body-cream.html/00305210046740
8. Vaseline® Radiant X Deep Nourishment Hand Butter | SKU 00305210046764 | Radiant X | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-radiant-x-deep-nourishment-hand-butter.html/00305210046764
9. Vaseline® Intensive Care™ Hydra Replenish Hand Crème | SKU 00305210045699 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-intensive-care-hydra-replenish-hand-creme.html/00305210045699
10. Vaseline® Healing Jelly Original | SKU 00305212352009 | Healing Jelly | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-healing-jelly-original.html/00305212352009
11. Vaseline® Healing Jelly Cocoa Butter | SKU 00305210069275 | Healing Jelly | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-healing-jelly-cocoa-butter.html/00305210069275
12. Vaseline® Lip Therapy® Advanced Healing Tube | SKU 00305212750003 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-advanced-healing-tube.html/00305212750003
13. Vaseline® Cocoa Shimmer Jelly Stick | SKU 00305210044876 | Healing Jelly | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-cocoa-shimmer-jelly-stick.html/00305210044876
14. Vaseline® All-Over Body Balm Jelly Stick | SKU 00305210043558 | Healing Jelly | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-all-over-body-balm-jelly-stick.html/00305210043558
15. Vaseline® Soothing Hydration Lotion | SKU 00305213093000 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-soothing-hydration-lotion.html/00305213093000
16. Vaseline® Cocoa Radiant® Lotion | SKU 00305210134423 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-cocoa-radiant-lotion.html/00305210134423
17. Vaseline® Nourishing Moisture Lotion | SKU 00305213079004 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-nourishing-moisture-lotion.html/00305213079004
18. Vaseline® Calm Healing Lotion | SKU 00305210043596 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-calm-healing-lotion.html/00305210043596
19. Vaseline® Advanced Repair Unscented Lotion | SKU 00305213087009 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-advanced-repair-unscented-lotion.html/00305213087009
20. Vaseline® Almond Smooth Lotion | SKU 00305210044647 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-almond-smooth-lotion.html/00305210044647
21. Vaseline® Men Cooling Hydration Lotion | SKU 00305210071148 | Men | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-men-cooling-lotion.html/00305210071148
22. Vaseline® Intensive Care™ Cocoa Body Butter | SKU 00305210312142 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-intensive-care-cocoa-body-butter.html/00305210312142
23. Vaseline® Men Fast Absorbing Lotion | SKU 00305210416383 | Men | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-men-fast-absorbing-lotion.html/00305210416383
24. Vaseline® Men Extra Strength Lotion | SKU 00305210416390 | Men | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-men-extra-strength-lotion.html/00305210416390
25. Vaseline® Lip Therapy® Original Mini | SKU 00305210206779 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-original-mini.html/00305210206779
26. Vaseline® Lip Therapy® Rosy Mini | SKU 00305210231597 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-rosy-mini.html/00305210231597
27. Vaseline® Lip Therapy® Cocoa Butter Mini | SKU 00305210232518 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-cocoa-butter-mini.html/00305210232518
28. Vaseline® Lip Therapy® Crème Brûlée Mini | SKU 00305210464728 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-creme-brulee-mini.html/00305210464728
29. Vaseline® Intensive Care™ Aloe Soothe Spray | SKU 00305210268494 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-intensive-care-aloe-soothe-spray.html/00305210268494
30. Vaseline® Intensive Care™ Cocoa Radiant Spray | SKU 00305210269637 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-intensive-care-cocoa-radiant-spray.html/00305210269637
31. Vaseline® Lip Therapy® Original Stick | SKU 00859581006846 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-original-stick.html/00859581006846
32. Vaseline® Lip Therapy® Rosy Lips Stick | SKU 00859581006853 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-rosy-lips-stick.html/00859581006853
33. Vaseline® Lip Therapy® Aloe Vera Stick | SKU 00859581006860 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-aloe-vera-stick.html/00859581006860
34. Vaseline® Lip Therapy® Cocoa Butter Stick | SKU 00859581006877 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-cocoa-butter-stick.html/00859581006877
35. Vaseline® Lip Therapy® Rosy Lips Tin | SKU 00305210536494 | Lip Therapy | lip product | captured | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-rosy-lips-tin.html/00305210536494
36. Vaseline® Baby Healing Jelly | SKU 00305210048034 | Baby | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-baby-healing-jelly.html/00305210048034
37. Sunlit Glow Body Shimmer Gel Oil | SKU 00305210049123 | Body Oils | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-sunlit-glow-shimmer-gel-oil.html/00305210049123
38. Golden Hour Glow Bronze Body Shimmer Gel Oil | SKU 00305210049130 | Body Oils | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-golden-hour-glow-shimmer-gel-oil.html/00305210049130
39. Vaseline® Baby Healing Jelly Tube | SKU 00305210049239 | Baby | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-baby-healing-jelly-tube.html/00305210049239
40. Vaseline® Original Healing Jelly™ Tube | SKU 00305210049246 | Healing Jelly | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-original-healing-jelly-tube.html/00305210049246
41. Vaseline® Baby Healing Jelly Stick | SKU 00305210049260 | Baby | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-baby-healing-jelly-stick.html/00305210049260
42. Vaseline® Lip Therapy Arctic Mint Mini | SKU 00305210049307 | Lip Therapy | lip product | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-arctic-mint-mini.html/00305210049307
43. Vaseline® Lip Therapy Vanilla Swirl Mini | SKU 00305210049314 | Lip Therapy | lip product | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-vanilla-swirl-mini.html/00305210049314
44. Vaseline® Lip Therapy Berry Crush Mini | SKU 00305210049390 | Lip Therapy | lip product | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-berry-crush-mini.html/00305210049390
45. Vaseline® Cherry Aura Hand Butter | SKU 00305210049857 | Cherry Aura | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-cherry-aura-hand-butter.html/00305210049857
46. Vaseline® Cherry Aura Body Lotion | SKU 00305210049871 | Cherry Aura | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-cherry-aura-body-lotion.html/00305210049871
47. Vaseline® Cherry Aura Whipped Body Cream | SKU 00305210050013 | Cherry Aura | leave-on skincare | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-cherry-aura-whipped-body-cream.html/00305210050013
48. Vaseline® Intensive Care™ Cocoa Radiant Gel Oil | SKU 00305210287303 | Intensive Care | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-intensive-care-cocoa-radiant-gel-oil.html/00305210287303
49. Vaseline Lip Therapy Pink Grapefruit Mini | SKU 00850068951918 | Lip Therapy | lip product | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-pink-grapefruit-mini.html/00850068951918
50. Vaseline Lip Therapy Pistachio Donut Mini | SKU 00850081897248 | Lip Therapy | lip product | ingredients not found | https://www.vaseline.com/us/en/p/vaseline-lip-therapy-pistachio-donut-mini.html/00850081897248
51. Vaseline® Pro VitaB3 Supple & Soft Serum Burst Lotion | SKU 00305210047600 | Pro-VitaB3 | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-pro-vitab3-supple-and-soft-serum-burst-lotion.html/00305210047600
52. Vaseline® Pro VitaB3 Luminous Glow Serum Burst Lotion | SKU 00305210047617 | Pro-VitaB3 | leave-on skincare | captured | https://www.vaseline.com/us/en/p/vaseline-pro-vitab3-luminous-glow-serum-burst-lotion.html/00305210047617

## Per-product status

Vaseline® Vanilla Comfort Trial & Travel Lotion: ingredients not found — Ingredients section empty on page; not graded.
Vaseline Vanilla Comfort Lotion: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Vanilla Comfort Gel Oil: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Radiant X Firm & Restore Body Lotion: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Radiant X Even Tone Nourishing Body Lotion: complete — Avoid (High Priority Swap); 10 flags; 6 unknown.
Vaseline® Radiant X Replenishing Hydrating Body Oil: complete — Avoid (High Priority Swap); 5 flags; 1 unknown.
Vaseline® Radiant X Deep Nourishment Body Cream: complete — Avoid (High Priority Swap); 10 flags; 6 unknown.
Vaseline® Radiant X Deep Nourishment Hand Butter: complete — Avoid (High Priority Swap); 10 flags; 6 unknown.
Vaseline® Intensive Care™ Hydra Replenish Hand Crème: complete — Avoid (High Priority Swap); 12 flags; 3 unknown.
Vaseline® Healing Jelly Original: complete — Avoid (High Priority Swap); 1 flags; 0 unknown.
Vaseline® Healing Jelly Cocoa Butter: complete — Avoid (High Priority Swap); 2 flags; 0 unknown.
Vaseline® Lip Therapy® Advanced Healing Tube: complete — Avoid (High Priority Swap); 1 flags; 0 unknown.
Vaseline® Cocoa Shimmer Jelly Stick: complete — Avoid (High Priority Swap); 8 flags; 4 unknown.
Vaseline® All-Over Body Balm Jelly Stick: complete — Avoid (High Priority Swap); 2 flags; 1 unknown.
Vaseline® Soothing Hydration Lotion: complete — Avoid (High Priority Swap); 10 flags; 4 unknown.
Vaseline® Cocoa Radiant® Lotion: complete — Avoid (High Priority Swap); 14 flags; 5 unknown.
Vaseline® Nourishing Moisture Lotion: complete — Avoid (High Priority Swap); 13 flags; 8 unknown.
Vaseline® Calm Healing Lotion: complete — Avoid (High Priority Swap); 12 flags; 5 unknown.
Vaseline® Advanced Repair Unscented Lotion: complete — Avoid (High Priority Swap); 7 flags; 2 unknown.
Vaseline® Almond Smooth Lotion: complete — Avoid (High Priority Swap); 11 flags; 5 unknown.
Vaseline® Men Cooling Hydration Lotion: complete — Avoid (High Priority Swap); 13 flags; 6 unknown.
Vaseline® Intensive Care™ Cocoa Body Butter: complete — Avoid (High Priority Swap); 18 flags; 15 unknown.
Vaseline® Men Fast Absorbing Lotion: complete — Avoid (High Priority Swap); 11 flags; 3 unknown.
Vaseline® Men Extra Strength Lotion: complete — Avoid (High Priority Swap); 12 flags; 2 unknown.
Vaseline® Lip Therapy® Original Mini: complete — Avoid (High Priority Swap); 1 flags; 1 unknown.
Vaseline® Lip Therapy® Rosy Mini: complete — Avoid (High Priority Swap); 1 flags; 3 unknown.
Vaseline® Lip Therapy® Cocoa Butter Mini: complete — Avoid (High Priority Swap); 1 flags; 2 unknown.
Vaseline® Lip Therapy® Crème Brûlée Mini: complete — Avoid (High Priority Swap); 1 flags; 2 unknown.
Vaseline® Intensive Care™ Aloe Soothe Spray: complete — Avoid (High Priority Swap); 8 flags; 2 unknown.
Vaseline® Intensive Care™ Cocoa Radiant Spray: complete — Avoid (High Priority Swap); 8 flags; 1 unknown.
Vaseline® Lip Therapy® Original Stick: complete — Avoid (High Priority Swap); 1 flags; 3 unknown.
Vaseline® Lip Therapy® Rosy Lips Stick: complete — Avoid (High Priority Swap); 4 flags; 7 unknown.
Vaseline® Lip Therapy® Aloe Vera Stick: complete — Avoid (High Priority Swap); 4 flags; 4 unknown.
Vaseline® Lip Therapy® Cocoa Butter Stick: complete — Avoid (High Priority Swap); 4 flags; 10 unknown.
Vaseline® Lip Therapy® Rosy Lips Tin: complete — Avoid (High Priority Swap); 2 flags; 2 unknown.
Vaseline® Baby Healing Jelly: ingredients not found — Ingredients section empty on page; not graded.
Sunlit Glow Body Shimmer Gel Oil: complete — Avoid (High Priority Swap); 7 flags; 5 unknown.
Golden Hour Glow Bronze Body Shimmer Gel Oil: complete — Avoid (High Priority Swap); 8 flags; 6 unknown.
Vaseline® Baby Healing Jelly Tube: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Original Healing Jelly™ Tube: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Baby Healing Jelly Stick: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Lip Therapy Arctic Mint Mini: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Lip Therapy Vanilla Swirl Mini: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Lip Therapy Berry Crush Mini: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Cherry Aura Hand Butter: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Cherry Aura Body Lotion: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Cherry Aura Whipped Body Cream: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Intensive Care™ Cocoa Radiant Gel Oil: complete — Avoid (High Priority Swap); 2 flags; 1 unknown.
Vaseline Lip Therapy Pink Grapefruit Mini: ingredients not found — Ingredients section empty on page; not graded.
Vaseline Lip Therapy Pistachio Donut Mini: ingredients not found — Ingredients section empty on page; not graded.
Vaseline® Pro VitaB3 Supple & Soft Serum Burst Lotion: complete — Avoid (High Priority Swap); 9 flags; 6 unknown.
Vaseline® Pro VitaB3 Luminous Glow Serum Burst Lotion: complete — Avoid (High Priority Swap); 8 flags; 4 unknown.

## Failures

16 of 52 products had no ingredient text on the product page (the Ingredients section is present but empty in both the page markup and the rendered view). They are logged as "ingredients not found" and not graded. No ingredient lists were inferred from sibling products.

- Vaseline® Vanilla Comfort Trial & Travel Lotion (SKU 00305210049840)
- Vaseline Vanilla Comfort Lotion (SKU 00305210049864)
- Vaseline® Vanilla Comfort Gel Oil (SKU 00305210049963)
- Vaseline® Radiant X Firm & Restore Body Lotion (SKU 00305210047778)
- Vaseline® Baby Healing Jelly (SKU 00305210048034)
- Vaseline® Baby Healing Jelly Tube (SKU 00305210049239)
- Vaseline® Original Healing Jelly™ Tube (SKU 00305210049246)
- Vaseline® Baby Healing Jelly Stick (SKU 00305210049260)
- Vaseline® Lip Therapy Arctic Mint Mini (SKU 00305210049307)
- Vaseline® Lip Therapy Vanilla Swirl Mini (SKU 00305210049314)
- Vaseline® Lip Therapy Berry Crush Mini (SKU 00305210049390)
- Vaseline® Cherry Aura Hand Butter (SKU 00305210049857)
- Vaseline® Cherry Aura Body Lotion (SKU 00305210049871)
- Vaseline® Cherry Aura Whipped Body Cream (SKU 00305210050013)
- Vaseline Lip Therapy Pink Grapefruit Mini (SKU 00850068951918)
- Vaseline Lip Therapy Pistachio Donut Mini (SKU 00850081897248)

No page errors or timeouts occurred.

## Manual review queue

Every ingredient not resolved to the reference, the project LOW_TOX list, or a rubric pattern, deduplicated across all graded products (60 unique names). These are not counted as flags. Each name shows the number of products it appears in.

- aloe barbadensis leaf extract — 1 product(s)
- aloe barbadensis leaf juice powder — 2 product(s)
- alpha-isomethyl ionone — 6 product(s)
- ammonium acryloyldimethyltaurate/vp copolymer — 3 product(s)
- avena sativa (oat) straw extract — 1 product(s)
- avocado fruit extract — 1 product(s)
- benzyl benzoate — 2 product(s)
- benzyl salicylate — 3 product(s)
- butyrospermum parkii butter — 1 product(s)
- c20-40 alkyl stearate — 4 product(s)
- calcium aluminum borosilicate — 1 product(s)
- calcium sodium borosilicate — 3 product(s)
- caprylic triglyceride — 1 product(s)
- carnauba wax — 1 product(s)
- ci 19140 — 1 product(s)
- cinnamyl alcohol — 1 product(s)
- citronellol — 4 product(s)
- cocoa seed butter — 1 product(s)
- copernicia cerifera (camauba) wax — 1 product(s)
- cystine — 2 product(s)
- diisostearate — 1 product(s)
- ethylhexyl cocoate — 1 product(s)
- flavor — 3 product(s)
- flavor (aroma) — 1 product(s)
- glyceryl hydroxystearate — 1 product(s)
- glycol stearate — 12 product(s)
- hexyl cinnamal — 10 product(s)
- hydrogenated didecene — 1 product(s)
- hydrogenated polydecene — 1 product(s)
- hydrogenated polyisobutene — 1 product(s)
- hydrogenated styrene/butadiene copolymer — 3 product(s)
- hydroxystearic acid — 4 product(s)
- isostearic acid — 1 product(s)
- jojoba seed oil — 1 product(s)
- lavandula angustifolia (lavender) flower extract — 1 product(s)
- macadamia integrifolia seed oil — 1 product(s)
- magnesium aluminum silicate — 5 product(s)
- menthol — 1 product(s)
- microcrystalline wax — 5 product(s)
- phaseolus lunatus (green bean) seed extract — 4 product(s)
- polyglyceryl-3 distearate — 4 product(s)
- potato starch modified — 1 product(s)
- propylp — 1 product(s)
- red 30 (ci 73360) — 1 product(s)
- red 30 lake — 1 product(s)
- red 7 lake (ci 15850) — 1 product(s)
- rubus idaeus (raspberry) fruit extract — 1 product(s)
- rutin — 4 product(s)
- shea butter — 1 product(s)
- silica dimethyl silylate — 1 product(s)
- sodium acrylate/sodium acryloyldimethyl taurate copolymer — 2 product(s)
- sodium hydroxypropyl starch phosphate — 1 product(s)
- sorbitan monooleate — 1 product(s)
- stearamide amp — 11 product(s)
- theobroma cacao seed butter — 1 product(s)
- tin oxide (ci 77861) — 3 product(s)
- vaccinium macrocarpon (cranberry) fruit extract — 1 product(s)
- yellow 5 (ci 19140) — 1 product(s)
- yellow 5 lake — 4 product(s)
- yellow 5 lake (ci 19140) — 2 product(s)

## Anomalies

- Dimethicone and other silicone entries carry a 'PFAS treated' note in the reference, which triggers the PFAS escalation in 25 graded products. Applied as the rubric states; the escalation depends on that note.
- Petrolatum, mineral oil and paraffin are category 1 in the reference, and are present in all 36 graded products. Under the rubric's leave-on carcinogen escalation, every graded product is therefore High Priority Swap. Sensitivity tiers without that escalation are in the spreadsheet audit_notes column. Confirm this classification before publishing tier claims.
- Advanced Repair Unscented Lotion (SKU 00305213087009): the printed ingredient list is cut off at 'PROPYLP' on the page and in the page's own data layer. The remainder is not captured. Status set to 'needs review'.
- 16 products have an empty Ingredients block on the page: Vanilla Comfort Trial & Travel Lotion, Vanilla Comfort Lotion, Vanilla Comfort Gel Oil, Radiant X Firm & Restore Body Lotion, Baby Healing Jelly (both tube and stick versions), Original Healing Jelly Tube, Lip Therapy Arctic Mint, Vanilla Swirl, Berry Crush, Pink Grapefruit and Pistachio Donut minis, and the three Cherry Aura products. No SmartLabel link was found on the pages checked (three of the 16 were checked directly).
- Product name casing: several product pages print the h1 without the 'Vaseline' brand prefix (Sunlit Glow, Golden Hour Glow, the Lip Therapy minis). Listing names were used as printed.
- Typos kept as printed: 'Camauba' in the Lip Therapy Rosy Lips Stick carnauba entry; 'Usp' in the Healing Jelly original.
- Rendering: several Ingredient lines were stored on the site with unusual capitalisation (all-caps for the Soothing Hydration, Cocoa Radiant, Nourishing Moisture, Calm Healing and Advanced Repair lotions). Captured as printed.
- Grader changes from the template: (1) substring heuristics that silently skipped ingredients ending in oil, butter, extract, wax, and similar were removed, because they would hide flags such as Mineral Oil; (2) the project LOW_TOX list is used, but nothing was added from memory; (3) the '^ci 77' colorant pattern was dropped because it is not in the rubric's watch list, so unlisted CI colorants stay unknown; (4) Iron Oxides without a CI number follow the addendum (categories 1, 2, 3; PFAS treated); (5) titanium dioxide is exempt only in lotion, cream and butter bases; (6) natural fragrance components are soft only when a source oil is listed (Calm Healing Lotion linalool, with lavender extract, is the only soft entry in this catalog).
- Spray products (Aloe Soothe, Cocoa Radiant): the page does not say whether they are aerosols. Graded as leave-on skincare; the spray and aerosol titanium dioxide rule was not triggered, because neither lists titanium dioxide.
- Lip products are graded with the leave-on escalation. The rubric does not name lip products explicitly; they were treated as leave-on because of ingestion exposure.
- Shimmer gel oils contain mica, which is exempt because it is never the first ingredient. Colorant lakes (Yellow 5, Red 30, Red 7, Blue 1) are flagged only where the reference has a CI entry; the lakes without a CI entry are in the unknown queue.
- The two Pro VitaB3 lotions appear only on the Pro VitaB3 range page, not in the main listing's first 50, which suggests the main listing's 'Show More' control does not reach every product.

## Regrade 2026-10-16: unified grader, practitioner decisions D1 to D7

**Provenance:** Every product was regraded from the verbatim text in `vaseline_ingredients.json` (unchanged). The grader is `_grader.py`, the same file in all five brand folders, and it writes `vaseline_audit.xlsx` and `_grade_summary.json`. The pre-regrade workbook is the git HEAD copy and was used only for the change table below.

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

- Products: 52. Puberty Safe 0, Use Caution 0, Avoid (Mild) 0, Avoid (Moderate) 0, Avoid (High Priority Swap) 0.
- **Ungradable: 52 (counted separately from the five tiers).** 36 with unresolved ingredients under D4, 16 with no ingredient text.
- Moved from a graded tier to ungradable: 36. Moved from no tier to ungradable (no ingredient text): 16.
- Pre-regrade distribution (git HEAD): Avoid (High Priority Swap) 36, (none) 16.
- Unique unknown ingredients remaining: 119.

### Products that changed tier

Pre-regrade tier from git HEAD, current tier from this regrade. "Unknowns left" is the number of distinct unknown ingredients still unresolved for that product.

| Product | Before | Now | Unknowns left | Reason |
|---|---|---|---|---|
| Vaseline® Vanilla Comfort Trial & Travel Lotion | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline Vanilla Comfort Lotion | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Vanilla Comfort Gel Oil | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Radiant X Firm & Restore Body Lotion | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Radiant X Even Tone Nourishing Body Lotion | Avoid (High Priority Swap) | ungradable | 17 | D7: 17 unknown(s) remain |
| Vaseline® Radiant X Replenishing Hydrating Body Oil | Avoid (High Priority Swap) | ungradable | 6 | D7: 6 unknown(s) remain |
| Vaseline® Radiant X Deep Nourishment Body Cream | Avoid (High Priority Swap) | ungradable | 17 | D7: 17 unknown(s) remain |
| Vaseline® Radiant X Deep Nourishment Hand Butter | Avoid (High Priority Swap) | ungradable | 14 | D7: 14 unknown(s) remain |
| Vaseline® Intensive Care™ Hydra Replenish Hand Crème | Avoid (High Priority Swap) | ungradable | 12 | D7: 12 unknown(s) remain |
| Vaseline® Healing Jelly Original | Avoid (High Priority Swap) | ungradable | 1 | D7: 1 unknown(s) remain |
| Vaseline® Healing Jelly Cocoa Butter | Avoid (High Priority Swap) | ungradable | 1 | D7: 1 unknown(s) remain |
| Vaseline® Lip Therapy® Advanced Healing Tube | Avoid (High Priority Swap) | ungradable | 1 | D7: 1 unknown(s) remain |
| Vaseline® Cocoa Shimmer Jelly Stick | Avoid (High Priority Swap) | ungradable | 6 | D7: 6 unknown(s) remain |
| Vaseline® All-Over Body Balm Jelly Stick | Avoid (High Priority Swap) | ungradable | 3 | D7: 3 unknown(s) remain |
| Vaseline® Soothing Hydration Lotion | Avoid (High Priority Swap) | ungradable | 10 | D7: 10 unknown(s) remain |
| Vaseline® Cocoa Radiant® Lotion | Avoid (High Priority Swap) | ungradable | 12 | D7: 12 unknown(s) remain |
| Vaseline® Nourishing Moisture Lotion | Avoid (High Priority Swap) | ungradable | 15 | D7: 15 unknown(s) remain |
| Vaseline® Calm Healing Lotion | Avoid (High Priority Swap) | ungradable | 12 | D7: 12 unknown(s) remain |
| Vaseline® Advanced Repair Unscented Lotion | Avoid (High Priority Swap) | ungradable | 7 | D7: 7 unknown(s) remain |
| Vaseline® Almond Smooth Lotion | Avoid (High Priority Swap) | ungradable | 15 | D7: 15 unknown(s) remain |
| Vaseline® Men Cooling Hydration Lotion | Avoid (High Priority Swap) | ungradable | 13 | D7: 13 unknown(s) remain |
| Vaseline® Intensive Care™ Cocoa Body Butter | Avoid (High Priority Swap) | ungradable | 24 | D7: 24 unknown(s) remain |
| Vaseline® Men Fast Absorbing Lotion | Avoid (High Priority Swap) | ungradable | 10 | D7: 10 unknown(s) remain |
| Vaseline® Men Extra Strength Lotion | Avoid (High Priority Swap) | ungradable | 8 | D7: 8 unknown(s) remain |
| Vaseline® Lip Therapy® Original Mini | Avoid (High Priority Swap) | ungradable | 1 | D7: 1 unknown(s) remain |
| Vaseline® Lip Therapy® Rosy Mini | Avoid (High Priority Swap) | ungradable | 3 | D7: 3 unknown(s) remain |
| Vaseline® Lip Therapy® Cocoa Butter Mini | Avoid (High Priority Swap) | ungradable | 3 | D7: 3 unknown(s) remain |
| Vaseline® Lip Therapy® Crème Brûlée Mini | Avoid (High Priority Swap) | ungradable | 3 | D7: 3 unknown(s) remain |
| Vaseline® Intensive Care™ Aloe Soothe Spray | Avoid (High Priority Swap) | ungradable | 7 | D7: 7 unknown(s) remain |
| Vaseline® Intensive Care™ Cocoa Radiant Spray | Avoid (High Priority Swap) | ungradable | 7 | D7: 7 unknown(s) remain |
| Vaseline® Lip Therapy® Original Stick | Avoid (High Priority Swap) | ungradable | 9 | D7: 9 unknown(s) remain |
| Vaseline® Lip Therapy® Rosy Lips Stick | Avoid (High Priority Swap) | ungradable | 14 | D7: 14 unknown(s) remain |
| Vaseline® Lip Therapy® Aloe Vera Stick | Avoid (High Priority Swap) | ungradable | 12 | D7: 12 unknown(s) remain |
| Vaseline® Lip Therapy® Cocoa Butter Stick | Avoid (High Priority Swap) | ungradable | 14 | D7: 14 unknown(s) remain |
| Vaseline® Lip Therapy® Rosy Lips Tin | Avoid (High Priority Swap) | ungradable | 2 | D7: 2 unknown(s) remain |
| Vaseline® Baby Healing Jelly | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Sunlit Glow Body Shimmer Gel Oil | Avoid (High Priority Swap) | ungradable | 8 | D7: 8 unknown(s) remain |
| Golden Hour Glow Bronze Body Shimmer Gel Oil | Avoid (High Priority Swap) | ungradable | 9 | D7: 9 unknown(s) remain |
| Vaseline® Baby Healing Jelly Tube | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Original Healing Jelly™ Tube | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Baby Healing Jelly Stick | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Lip Therapy Arctic Mint Mini | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Lip Therapy Vanilla Swirl Mini | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Lip Therapy Berry Crush Mini | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Cherry Aura Hand Butter | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Cherry Aura Body Lotion | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Cherry Aura Whipped Body Cream | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Intensive Care™ Cocoa Radiant Gel Oil | Avoid (High Priority Swap) | ungradable | 2 | D7: 2 unknown(s) remain |
| Vaseline Lip Therapy Pink Grapefruit Mini | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline Lip Therapy Pistachio Donut Mini | (no tier: no ingredient text) | ungradable | 0 | no ingredient text: no tier before or now |
| Vaseline® Pro VitaB3 Supple & Soft Serum Burst Lotion | Avoid (High Priority Swap) | ungradable | 15 | D7: 15 unknown(s) remain |
| Vaseline® Pro VitaB3 Luminous Glow Serum Burst Lotion | Avoid (High Priority Swap) | ungradable | 13 | D7: 13 unknown(s) remain |

Products whose tier did not change: 0.

### Hand-check (two products)

- **Golden Hour Glow Bronze Body Shimmer Gel Oil (silica D1, iron D2).** Silica [1, 2] is flagged with no PFAS escalation of its own. The PFAS and heavy-metal escalations come from Iron Oxides (CI 77491) and (CI 77499), which is correct. Mica (CI 77019) is also flagged here, which is the known mica gap above. Stays ungradable with 9 unknowns.
- **Vaseline Lip Therapy Cocoa Butter Stick (iron D2).** Iron Oxides [1, 2, 3] is flagged, with heavy-metal and PFAS escalations. Petrolatum [1], Butylene Glycol [1, 2] and Fragrance (no disclosure, [1, 2, 4, 8]) match the reference. Stays ungradable with 14 unknowns, including Octyldodecanol and Caprylic Triglyceride.

### Unique unknown ingredients remaining (manual review queue)

Each unknown is listed once, with the number of products it appears in. Counts are over all products, including ungradable ones.

- Stearic Acid (16)
- Theobroma Cacao (Cocoa) Seed Butter (10)
- Glyceryl Stearate (8)
- Helianthus Annuus (Sunflower) Seed Oil (8)
- Tocopheryl Acetate (8)
- Acrylates/C10-30 Alkyl Acrylate Crosspolymer (7)
- Glycol Stearate (7)
- Hexyl Cinnamal (7)
- Butyrospermum Parkii (Shea) Butter (6)
- Caprylic/Capric Triglyceride (6)
- Caramel (6)
- Disodium Edta (6)
- Disodium EDTA (6)
- Tapioca Starch (6)
- Alpha-Isomethyl Ionone (5)
- Copernicia Cerifera (Carnauba) Wax (5)
- GLYCERYL STEARATE (5)
- GLYCOL STEARATE (5)
- HELIANTHUS ANNUUS (SUNFLOWER) SEED OIL (5)
- Microcrystalline Wax (5)
- Stearamide AMP (5)
- STEARIC ACID (5)
- C20-40 Alkyl Stearate (4)
- DISODIUM EDTA (4)
- Hydroxystearic Acid (4)
- Isohexadecane (4)
- Isopropyl Myristate (4)
- Octyldodecanol (4)
- Palmitoyl Tetrapeptide-7 (4)
- Palmitoyl Tripeptide-1 (4)
- Phaseolus Lunatus (Green Bean) Seed Extract (4)
- Polyglyceryl-3 Distearate (4)
- Ricinus Communis (Castor) Seed Oil (4)
- Rutin (4)
- Sodium Ascorbyl Phosphate (4)
- STEARAMIDE AMP (4)
- Yellow 5 Lake (4)
- ACRYLATES/C10-30 ALKYL ACRYLATE CROSSPOLYMER (3)
- Benzyl Salicylate (3)
- Calcium Sodium Borosilicate (3)
- Flavor (3)
- HEXYL CINNAMAL (3)
- Hydrogenated Styrene/Butadiene Copolymer (3)
- ISOPROPYL MYRISTATE (3)
- Isopropyl Palmitate (3)
- MAGNESIUM ALUMINUM SILICATE (3)
- TAPIOCA STARCH (3)
- Ammonium Acryloyldimethyltaurate/Vp Copolymer (2)
- Benzyl Benzoate (2)
- Camellia Sinensis Leaf Extract (2)
- CITRONELLOL (2)
- Citronellol (2)
- Cystine (2)
- Glycine (2)
- ISOPROPYL PALMITATE (2)
- Magnesium Aluminum Silicate (2)
- Polysorbate 80 (2)
- Prunus Amygdalus Dulcis (Sweet Almond) Oil (2)
- Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer (2)
- Sodium Pca (2)
- Sorbitan Isostearate (2)
- Stearamide Amp (2)
- Tin Oxide (CI 77861) (2)
- Yellow 5 Lake (Ci 19140) (2)
- Aloe Barbadensis Leaf Extract (1)
- ALOE BARBADENSIS LEAF JUICE POWDER (1)
- Aloe Barbadensis Leaf Juice Powder (1)
- ALPHA-ISOMETHYL IONONE (1)
- Ammonium Acryloyldimethyltaurate/VP Copolymer (1)
- AVENA SATIVA (OAT) STRAW EXTRACT (1)
- Avocado Fruit Extract (1)
- Blue 1 (CI 42090) (1)
- Butyrospermum Parkii Butter (1)
- Calcium Aluminum Borosilicate (1)
- Caprylic Triglyceride (1)
- CARAMEL (1)
- Carnauba Wax (1)
- CI 19140 (1)
- CINNAMYL ALCOHOL (1)
- Cocoa Seed Butter (1)
- Copernicia Cerifera (Camauba) Wax (1)
- Dicaprylyl Ether (1)
- Diisostearate (1)
- Dimethiconol (1)
- Disteareth-75 IPDI (1)
- Ethylhexyl Cocoate (1)
- Flavor (Aroma) (1)
- Glyceryl Hydroxystearate (1)
- Hydrogenated Didecene (1)
- Hydrogenated Polydecene (1)
- Hydrogenated Polyisobutene (1)
- Isostearic Acid (1)
- Jojoba Seed Oil (1)
- LAVANDULA ANGUSTIFOLIA (LAVENDER) FLOWER EXTRACT (1)
- Macadamia Integrifolia Seed Oil (1)
- Maltodextrin (1)
- Menthol (1)
- Olea Europaea (Olive) Fruit Oil (1)
- Ozokerite (1)
- Persea Gratissima (Avocado) Oil (1)
- Potato Starch Modified (1)
- PROPYLP (1)
- Red 30 (Ci 73360) (1)
- Red 30 Lake (1)
- Red 7 Lake (Ci 15850) (1)
- Rose Flower Oil (1)
- Rubus Idaeus (Raspberry) Fruit Extract (1)
- Shea Butter (1)
- Silica Dimethyl Silylate (1)
- Simmondsia Chinensis (Jojoba) Seed Oil (1)
- SODIUM HYDROXYPROPYL STARCH PHOSPHATE (1)
- Sorbitan Monooleate (1)
- THEOBROMA CACAO (COCOA) SEED BUTTER (1)
- Theobroma Cacao Seed Butter (1)
- Tin Oxide (Ci 77861) (1)
- Vitis Vinifera (Grape) Seed Oil (1)
- White Petrolatum Usp (1)
- White Petrolatum USP (1)
- Yellow 5 (CI 19140) (1)

### Known limits found during the regrade (not changed; outside D1 to D7)

- **Mica conditional not implemented.** The rubric says mica is not a concern unless it is the first or main ingredient. The grader flags Mica [1, 4] wherever it appears. Mica appears in three shimmer products (Cocoa Shimmer Jelly Stick, Sunlit Glow, Golden Hour Glow Bronze).
- **`-nium` pattern false positive.** "Vaccinium" (the cranberry genus) matches the quat pattern. Flagged as [2] in Vaseline Lip Therapy Rosy Lips Stick. Partial flags only.
- **Reference gap.** REF.txt has Polysorbate 20, 60, 80 and Nylon-12, which ref_compact.json does not. Those ingredients stay unknown. Resolving them would change partial flags on 10 products across the five brands and would make no product gradable.

### Anomalies

- **16 products have no ingredient text**, including the three Vanilla Comfort products, Radiant X Firm and Restore, three Baby Healing Jelly products, Original Healing Jelly Tube, the Cherry Aura trio, and five Lip Therapy minis (Arctic Mint, Vanilla Swirl, Berry Crush, Pink Grapefruit, Pistachio Donut). These are ungradable with no tier.
- **"White Petrolatum USP" is unknown** in Vaseline Healing Jelly Original and Lip Therapy Advanced Healing Tube. The reference's Petrolatum entry is category 1. Under D4 these stay unknown, so each shows 0 partial flags and 1 unknown. If you decide this is an alias of Petrolatum, each product gains a Petrolatum [1] flag and a "carcinogen in leave-on" escalation. This is a decision for you.
- **Silica Dimethyl Silylate** (Cocoa Shimmer Jelly Stick) is unknown (see the Eucerin note).
- **Mica (CI 77019)** is flagged in three shimmer products. This is the known mica gap above.

## Regrade 2026-10-16, D8: one unknown ingredient gets a Use Caution floor

This section supersedes the tier counts and ungradable counts in the regrade sections above. Flags, escalations and unknown lists are unchanged by D8 (checked for every product row).

### Decision as applied

- D8 (practitioner, 2026-10-16): a product with exactly one unknown ingredient gets the Use Caution floor, the same way D1 and D6 work. A Puberty Safe product becomes Use Caution. A higher tier from the other flags is kept.
- The one unknown stays in unknown_ingredients and audit_notes. Status stays "complete" with the note "one unknown ingredient, Use Caution floor applied", except where the source JSON already carries a needs-review flag (see Open items).
- Two or more unknowns: still ungradable under D7. Products with no ingredient text: still "ingredients not found" with no tier.

### Grader change

- One grader for all five brands (`_grader.py`), copied into each brand folder with identical contents and pointed at its own folder. The D8 block sits directly before the D7 check. D7 now applies at two or more unknowns. The ungradable summary text now reads "two or more". No other rule changed.

### Tier counts, before and after D8

- Before D8 (D1 to D7): graded 0, ungradable 52 (no ingredient text: 16).
- After D8: Puberty Safe 0, Use Caution 2, Avoid (Mild) 0, Avoid (Moderate) 0, Avoid (High Priority Swap) 2; ungradable 48 (32 with two or more unknowns, 16 with no ingredient text). Total 52.

### Products that left ungradable under D8

Use Caution (floor applied):
- Vaseline® Healing Jelly Original: unknown "White Petrolatum Usp"; now Use Caution.
- Vaseline® Lip Therapy® Advanced Healing Tube: unknown "White Petrolatum USP"; now Use Caution.

Kept a higher tier from other flags:
- Vaseline® Healing Jelly Cocoa Butter: unknown "Theobroma Cacao (Cocoa) Seed Butter"; now Avoid (High Priority Swap).
- Vaseline® Lip Therapy® Original Mini: unknown "Yellow 5 Lake"; now Avoid (High Priority Swap).

### Hand checks (two products)

- **Vaseline® Healing Jelly Original (ungradable to Use Caution).** Printed text "White Petrolatum Usp (100%)". One unknown, White Petrolatum Usp, and no flags. REF.txt has no white petrolatum entry; its Petrolatum entry (category 1) is under the plain name. Result Use Caution, as the D8 rule requires.
- **Vaseline® Lip Therapy® Rosy Lips Tin (stays ungradable).** Printed text "Petrolatum, Flavor (Aroma), Titanium Dioxide (Ci 77891), Red 30 (Ci 73360)." Unknowns Flavor (Aroma) and Red 30 (Ci 73360) are both absent from REF.txt. Two unknowns, so D7 applies and no tier is assigned.

### Unique unknown ingredients remaining (manual review queue)

97 unique names in this brand (ignoring case), each still in the manual review queue. D8 does not remove any of them. Across all five brands: 308 unique names ignoring case, 354 distinct spellings as printed.

### Open items for the practitioner

- White Petrolatum USP (Healing Jelly Original and Lip Therapy Advanced Healing Tube) is the largest single driver of the D8 moves. The grader does not alias it (D4). If it is treated as petrolatum, both products move to Avoid (High Priority Swap) through the carcinogen-in-leave-on escalation.
- Yellow 5 Lake (Lip Therapy Original Mini) and Theobroma Cacao (Cocoa) Seed Butter (Healing Jelly Cocoa Butter) are single unknowns on products already held at High Priority by Petrolatum. Their D8 result does not depend on how those names are resolved.

### Files written this pass

- `vaseline/_grader.py` (D8 added), `vaseline/vaseline_audit.xlsx` (regenerated, 14 template columns), `vaseline/_grade_summary.json` (regenerated), `vaseline/vaseline_content_mining.md`, and this log. The verbatim `vaseline_ingredients.json` is unchanged.

## Regrade 2026-10-17: changes 1 to 3 (practitioner decisions)

Applied in this pass with the same `_grader.py` in every brand folder. The reference was edited only for change 2 (`ref_compact.json`). The reference PDF text was not edited.

**Change 1: White Petrolatum USP is petrolatum.** Alias recorded in the grader's alias table (`TYPO_FIXES` in `_grader.py`): "white petrolatum usp", "white petrolatum (usp)" and "white petrolatum", each mapped to the reference entry `petrolatum` (reference category 1). Source: REF.txt line 789 (Petrolatum, category 1). Basis: practitioner decision; White Petrolatum USP is a purified grade of petroleum jelly. `ingredient_aliases.json` was not edited, because this pass writes only inside the brand folders and `ref_compact.json`.

**Change 2: all polysorbates flagged.** `ref_compact.json`: added Polysorbate 20, 21, 40, 60, 61, 65, 80, 81 and 85, categories 1, 2, 4 and 5, note "Watch for: Polysorbate- (#)", transcribed from REF.txt lines 885 to 910. Removed one malformed key, `polysorbate 20 1 2 4 5 watch for: polysorbate- (#)`, a parser artifact with an empty category list that was the only prior polysorbate row. Reference entries: 434 before, 442 after. The grader also flags any other polysorbate number through a `^polysorbate` pattern, labeled "inferred". Nothing else in the reference changed.

**Change 3: explicit ungradable exceptions.** Not applicable to this brand. The exception list holds Eucerin products only, and none of this brand's products is on it.

**Tier changes in this brand:**
- Vaseline® Healing Jelly Original: Use Caution to Avoid (High Priority Swap). Reason: change 1: White Petrolatum USP read as petrolatum (category 1), carcinogen-in-leave-on escalation.
- Vaseline® Lip Therapy® Advanced Healing Tube: Use Caution to Avoid (High Priority Swap). Reason: change 1: White Petrolatum USP read as petrolatum (category 1), carcinogen-in-leave-on escalation.

**Flag and unknown changes from change 2 (tiers unchanged unless listed above):**
- Vaseline® Intensive Care™ Hydra Replenish Hand Crème: flags 11 to 12 (Polysorbate 80); unknowns 12 to 11 (Polysorbate 80 no longer unknown); tier ungradable.
- Vaseline® Healing Jelly Original: flags 0 to 1 (White Petrolatum Usp); unknowns 1 to 0 (White Petrolatum Usp no longer unknown); tier Avoid (High Priority Swap).
- Vaseline® Lip Therapy® Advanced Healing Tube: flags 0 to 1 (White Petrolatum USP); unknowns 1 to 0 (White Petrolatum USP no longer unknown); tier Avoid (High Priority Swap).
- Vaseline® Intensive Care™ Cocoa Body Butter: flags 15 to 16 (Polysorbate 80); unknowns 24 to 23 (Polysorbate 80 no longer unknown); tier ungradable.

**D7 and D8 counts, recomputed from the new flags:**
- D8 (exactly one unknown): 4 to 2.
- D7 (two or more unknowns, ungradable): 32 to 32.
- Unique unknown ingredient spellings in this brand: 119 to 116.

**Hand checks (2026-10-17):**
- Intensive Care Hydra Replenish Hand Crème: Polysorbate 80 is in the verbatim list and flags [1,2,4,5]. Flag count 11 to 12, unknowns 12 to 11. Still ungradable (D7). Agrees with the manual read.
- Healing Jelly Original: verbatim "White Petrolatum Usp (100%)" reads as petrolatum, category 1, one flag in a leave-on, so the carcinogen-in-leave-on escalation gives Avoid (High Priority Swap). Agrees.

**Tier counts after this pass:** ungradable: 48; Avoid (High Priority Swap): 4.
