# Vaseline Audit Log

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
