/* Puberty-Safe grader, browser port of scraper/grader.py.
   Keep this file in step with grader.py: the parity test (scraper/browser/parity_test.js)
   compares every dashboard record against it.
   Built into puberty_scanner_embed.html by scraper/browser/build_embed.py, which replaces
   the __CONSTANTS__ token with scraper/browser/constants.json and passes the reference
   table in as refData. */
(function (root) {
  'use strict';

  var C = __CONSTANTS__;

  function makeGrader(refData) {
    var refRaw = refData.ref || refData;
    var REF = refRaw;
    var ALIASES = Object.assign({}, refData.aliases || {});
    ALIASES['white petrolatum'] = 'petrolatum';
    ALIASES['white petrolatum usp'] = 'petrolatum';
    ALIASES['petrolatum 100%'] = 'petrolatum';

    function has(obj, k) { return Object.prototype.hasOwnProperty.call(obj, k); }
    function aget(k, dflt) { return has(ALIASES, k) ? ALIASES[k] : dflt; }

    // Reference keys with a parenthetical also match the bare name.
    Object.keys(REF).forEach(function (k) {
      var bare = k.replace(/\s*\([^)]*\)/g, '').trim();
      if (bare && bare !== k && !has(REF, bare) && !has(ALIASES, bare)) ALIASES[bare] = k;
    });

    var NAT_FRAG = new Set(C.NAT_FRAG);
    var EO_HINTS = C.EO_HINTS;
    var FORMALDEHYDE = new Set(C.FORMALDEHYDE);
    var FATTY_ALC_SUBSTR = C.FATTY;
    var LOW_TOX = new Set(C.LOW_TOX);

    var EXEMPT_FRAG = new Set(
      'hexyl cinnamal|citronellol|benzyl salicylate|benzyl benzoate|menthol|camphor|pinene|alpha-pinene|beta-pinene|terpineol|beta-caryophyllene|linalyl acetate|linalool|limonene|geraniol|citral|alpha-isomethyl ionone|tetramethyl acetyloctahydronaphthalenes|gamma-decalactone|maltol|isoamyl acetate|eugenol|cinnamyl alcohol|coumarin|farnesol|benzyl alcohol|hydroxycitronellal|amyl cinnamal|butylphenyl methylpropional|rosemary verbenone|msm'.split('|')
    );

    var PATTERN_WATCH = [
      [/\bpolyquaternium[-\s]?\d+\b|\bquaternium-(?!15\b)\d+\b|\b(trimonium|dimonium|nium) (chloride|methosulfate|sulfate)\b/i, [2], 'quaternary ammonium (quat)'],
      [/^(peg|ppg)[-\s\/]/i, [1, 2, 4, 5], 'PEG/PPG ethoxylate'],
      [/\bphenoxyethanol\b/i, [1, 2, 4, 5], 'phenoxyethanol'],
      [/(?:^|\s|-)(laureth|ceteth|oleth|steareth|trideceth|ceteareth|buteth|pareth|isoceteth)(?:-?\d|$)/i, [1, 4, 5], '-eth ethoxylate'],
      [/siloxane$|cyclopentasiloxane|cyclohexasiloxane|cyclotetrasiloxane|cyclomethicone/i, [1, 2, 6], 'siloxane'],
      [/(^|\s)dimethicone\b/i, [6], 'dimethicone persistence'],
      [/dimethiconol/i, [6], 'dimethicone persistence'],
      [/\bparaben\b/i, [2, 4], 'paraben'],
      [/sulfate$/i, [1, 4, 5], 'sulfate'],
      [/^sodium c14-16 olefin sulfonate$/i, [4], 'sodium C14-16 olefin sulfonate'],
      [/phthalate/i, [2], 'phthalate'],
      [/\bbenzophenone\b/i, [2], 'benzophenone'],
      [/^propylene glycol$|^butylene glycol$|^hexylene glycol$|^ethylene glycol$|^dipropylene glycol$/i, [1, 2], '-glycol'],
      [/monium chloride$|^behenalkonium|^stearalkonium|^cetrimonium|^cetyl pyridinium|^guar hydroxypropyltrimonium|hydroxypropyltrimonium chloride$|dicetyldimonium chloride$|^behentrimonium chloride/i, [2], '-nium quat'],
      [/\bbht\b|butylated hydroxytoluene/i, [1, 2], 'BHT'],
      [/\bbha\b|butylated hydroxyanisole/i, [1, 2], 'BHA'],
      [/^tetrasodium edta$/i, [1], 'tetrasodium EDTA'],
      [/^disodium edta$/i, [4], 'disodium EDTA'],
      [/^ethylhexylglycerin$/i, [4, 5], 'ethylhexylglycerin'],
      [/^chlorphenesin$/i, [4], 'chlorphenesin'],
      [/^methylparaben$|^propylparaben$|^butylparaben$|^ethylparaben$|^isobutylparaben$/i, [2, 4], 'paraben'],
      [/^triethanolamine/i, [1, 4], 'TEA'],
      [/^ethanolamine$/i, [4], 'ethanolamine'],
      [/^mineral oil$|paraffinum liquidum|^petrolatum$|^petroleum$|^paraffin$/i, [1], 'petroleum'],
      [/^cocamidopropyl/i, [1, 4], 'cocamidopropyl'],
      [/^lauramidopropyl/i, [1, 4], 'lauramidopropyl'],
      [/^silica$/i, [1, 2], 'silica'],
      [/^polyethylene$/i, [6], 'polyethylene'],
      [/^alcohol\s*denat/i, [4], 'alcohol denat'],
      [/^alcohol$/i, [4], 'alcohol'],
      [/alumin/i, [3], 'aluminum'],
      [/^iron oxides?\b/i, [1, 2, 3], 'iron oxides CI#'],
      [/^ci 77/i, [1, 2, 3], 'colorant CI#'],
      [/^isododecane/i, [1, 2], 'isododecane'],
      [/^vp\/va copolymer/i, [1, 4, 6], 'VP/VA copolymer'],
      [/^glycol distearate/i, [4], '-glycol'],
      [/^sulfosuccinate$/i, [5], 'sulfosuccinate'],
      [/^polysilicone-/i, [2, 6], 'silicone'],
      [/^trisiloxane$|silsesquioxane/i, [2, 6], 'siloxane'],
      [/^talc\b/i, [1, 3], 'talc'],
      [/^oxybenzone|^octinoxate|^octocrylene|^homosalate|^avobenzone/i, [2], 'chemical sunscreen'],
      [/^retinyl palmitate|^retinyl acetate/i, [1, 2], 'retinyl ester'],
      [/^resorcinol/i, [1, 2, 4], 'resorcinol'],
      [/^toluene/i, [1, 2, 4, 7], 'toluene'],
      [/^formaldehyde/i, [1, 4, 8], 'formaldehyde'],
      [/^coal tar|^fd&c|^d&c/i, [1, 2, 3], 'synthetic dye'],
      [/^diethanolamine|^dea\b|^cocamide dea|^lauramide dea/i, [1, 2, 4], 'DEA'],
      [/^monoethanolamine|^mea\b|^cocamide mea|^lauramide mea/i, [4], 'MEA'],
      [/^trisodium nitrilotriacetate/i, [1], 'nitrilo-'],
      [/^poly c10-30/i, [6], 'acrylate microplastic'],
      [/^ethylene\/acrylic acid copolymer/i, [6], 'acrylate microplastic'],
      [/^sodium dodecylbenzenesulfonate/i, [1], 'alkylbenzenesulfonate'],
      [/^diethylhexyl syringylidenemalonate/i, [2], 'sunscreen booster'],
      [/^1,2-hexanediol$/i, [1, 2], '-glycol'],
      [/^1,3-butylene glycol$/i, [1, 2], '-glycol'],
      [/^hexylene glycol$/i, [1, 2], '-glycol'],
      [/^lauryl pyrrolidone$/i, [4], 'lauryl pyrrolidone'],
      [/^sodium benzotriazolyl butylphenol sulfonate$/i, [1, 2], 'polymeric UV absorber'],
      [/^dmdm hydantoin|^diazolidinyl urea|^imidazolidinyl urea|^quaternium-15/i, [1, 2, 4, 5], 'formaldehyde releaser'],
      [/^methylisothiazolinone|^methylchloroisothiazolinone/i, [4, 7], 'isothiazolinone'],
      [/monium|quaternium|alkonium/i, [2], 'nium quat (inferred from naming pattern)'],
      [/\w*eth\b/i, [1, 4, 5], 'eth ethoxylate (inferred from naming pattern)'],
      [/^[a-z\- ]*glycol$/i, [1, 2], 'glycol (inferred from naming pattern)']
    ];

    var HIGH_ENDOCRINE_HINTS = [
      'paraben', 'phthalate', 'triclosan', 'triclocarban', 'pyrithione', 'polyquaternium-9',
      'oxybenzone', 'benzophenone-3', 'bp-3', 'bp3',
      'octinoxate', 'ethylhexyl methoxycinnamate', 'octyl methoxycinnamate',
      'octocrylene', 'homosalate', 'resorcinol', 'bha ', ' bha,', ' bha.',
      'butylated hydroxyanisole',
      'aluminum chloro', 'aluminum zirconium', 'aluminum chlorohydrate',
      'aluminum sesquichlorohydrate', 'aluminium chloro', 'aluminium zirconium'
    ];

    var INHAL_ONLY_WORDS = ['mica', 'silica', 'iron oxide', 'titanium dioxide', 'talc'];

    var DYE_RE = new RegExp(
      '\\bfd&c\\b|\\bd&c\\b|\\b(red|yellow|blue|green|violet|orange|black)\\s?\\d{1,2}\\b' +
      '|\\bci\\s?(?!75130\\b)(?:1[0-9]{4}|[4-6][0-9]{4}|7[0-4][0-9]{3}|75[0-9]{3})\\b', 'i');

    var ORDER = ['Puberty Safe', 'Use Caution', 'Avoid (Mild)', 'Avoid (Moderate)', 'Avoid (High)'];

    var CERT_RE = new RegExp('^(?:(?:usda |certified |cosmos |ecocert |eco[- ]?cert |made with |contains )*' +
      '(?:organic|natural|vegan|halal|kosher|fair[- ]?trade|fair for life|non[- ]?gmo(?: project)?(?: verified)?|gmo[- ]free|' +
      'b[- ]?corp(?:oration)?|leaping bunny|cruelty[- ]free|gluten[- ]free|' +
      'rainforest alliance|marine stewardship(?: council)?|carbon neutral|climate neutral|sustainably sourced|ethically sourced)' +
      '(?: certified| verified| sourced| ingredients?)*)\\)?$');
    var CLAIM_RE = /^(not an? .*|plant[- ]based.*|made (with|in) .*|certified (?:cotton|organic)|.*\bsummary\b.*)\)?$/;

    // ---------- helpers ----------
    function stripChars(s, chars) {
      var a = 0, b = s.length;
      while (a < b && chars.indexOf(s[a]) >= 0) a++;
      while (b > a && chars.indexOf(s[b - 1]) >= 0) b--;
      return s.slice(a, b);
    }

    function norm(s) {
      s = String(s).toLowerCase().trim();
      s = s.replace(/\s+/g, ' ');
      s = s.replace(/\*/g, '').replace(/®/g, '').replace(/™/g, '').trim();
      s = s.replace(/[\+†±ϝᵻ\^·​]+$/, '').trim();
      s = s.replace(/[^\x00-\x7f]+$/, '').trim();
      s = s.replace(/[\s+\/]+$/, '').trim();
      s = s.replace(/([a-z])\d$/, '$1').trim();
      return stripChars(s, ' .,;:-–');
    }

    function isFattyAlc(low) {
      return FATTY_ALC_SUBSTR.some(function (f) { return low.indexOf(f) >= 0; });
    }

    function isNaturalFrag(low, verbatimLower) {
      if (NAT_FRAG.has(low)) {
        if (EO_HINTS.some(function (h) { return verbatimLower.indexOf(h) >= 0; })) return low;
      }
      return null;
    }

    function splitIngredients(text) {
      var SENT = '\u0000';
      var t = String(text);
      t = t.replace(/active ingredient[s]?\s*:\s*/gi, '');
      t = t.replace(/inactive ingredient[s]?\s*:\s*/gi, ',');
      t = t.trim().replace(/^ingredients:\s*/i, '');
      t = t.trim().replace(/^ingredients?\b\s*/i, '');
      t = t.replace(/\b[A-Z][a-zA-Z0-9+\- ]+:\s*/g, ', ');
      t = t.replace(/\(code [^)]+\)/gi, '');
      t = t.replace(/\bSt\. /g, 'St ');
      t = t.replace(/(\d),(?=\d)/g, '$1' + SENT);
      t = t.replace(/\([^()]*\)/g, function (m) { return m.replace(/,/g, SENT); });
      t = t.replace(/\[[^\]]*\]?/g, '');
      // Keep ' and ' / ' with ' inside parentheses together; split phrases like 'pulp and polymer' outside them (user ruling 2026-11-10).
      t = t.replace(/\([^()]*\)/g, function (m) { return m.replace(/\s+(and|with)\s+/gi, ' \u0002$1\u0002 '); });
      var parts = t.split(/[,;]|\.\s+/).reduce(function (a, p) { return a.concat(p.replace(/^\s*(made|formulated|enriched|infused|fortified|contains|features?)\s+with\s+/i, '').split(/\s+(?:and|with)\s+/i)); }, []);
      parts = parts.map(function (p) { return p.split(SENT).join(',').replace(/\u0002/g, ''); });
      var out = [];
      parts.forEach(function (raw) {
        var p = stripChars(raw, ' .;,:');
        p = stripChars(p, '*† ').trim();
        var lp = p.toLowerCase();
        if (/^(no )?(parabens?|sunscreens?)\W*$/.test(lp)) return;
        if (/natural component of|\*?certified organic\s*$/.test(lp)) return;
        p = p.replace(/\s*\(\d{1,2}\)\s*$/, '');
        p = p.replace(/\s*\d+(\.\d+)?\s*%\s*$/, '');
        p = p.replace(/^\s*\d+(\.\d+)?\s*%\s*/, '');
        p = p.replace(/\([^)]*\d+(\.\d+)?\s*%[^)]*\)/g, '');
        // Footnote text printed after an ingredient, e.g. 'Plant Glycerin* * Organic Ingredients'.
        p = p.replace(/[\s*]*(certified\s+)?organic ingredients?\s*$/i, '').trim();
        if (!p) return;
        var low = p.toLowerCase();
        if (['ingredients', 'inactive ingredients', 'active ingredient', 'active ingredients', 'inactive', 'active'].indexOf(low) >= 0) return;
        if (low.indexOf('may contain') >= 0) return;
        if (CERT_RE.test(low)) return;
        if (CLAIM_RE.test(low)) return;
        // Claims and product descriptions, not ingredients (user ruling 2026-11-10).
        if (/^chlorine[- ]free$|^ph[- ]balanced$|^softer$|^heating patches$|^period stickers$|^non[- ]toxic\b(?!.*adhesive)|^no oil-based\b|^sustainably[- ]sourced\b/.test(low)) return;
        if (/^extra-long\b|^more flexible version\b|^bundle of\b|^sample pack\b|^\d+\s+(pads?|ultra|liners?|regular|tampons?|cups?)\b/.test(low)) return;
        if (low.endsWith(')') && low.indexOf('(') < 0) return;
        if (/\b(wrappers?|applicators?|packaging|recyclable|compostable|pouch|bottle|pump)\b/.test(low) && low.indexOf('plastic') < 0) return;
        if (/chlorine-free|natural component|†/.test(low)) return;
        if (p.indexOf(' – ') >= 0 || low.indexOf(' helps ') >= 0 || low.indexOf('botanical that') >= 0 || low.indexOf('stronger-looking') >= 0) return;
        if (low === 'inwater') return;
        out.push(p);
      });
      if (!out.length && String(text || '').trim()) out.push('ingredient list not published');
      return out;
    }

    var FLUORIDE_RE = /fluorid|monofluorophosphate/i;
    function isOralCare(productType) { return /toothpaste|oral|mouthwash|tooth/i.test(String(productType || '')); }
    function isLeaveOn(productType) {
      var pt = String(productType || '').toLowerCase();
      var rinse = ['shampoo', 'wash', 'conditioner', 'bar soap', 'hand soap', 'bath', 'shaving', 'scrub', 'exfoliant', 'cleansing', 'toothpaste', 'mouthwash'];
      return !rinse.some(function (k) { return pt.indexOf(k) >= 0; });
    }

    function isInhalationRisk(name, productType) {
      var n = String(name || '').toLowerCase();
      var pt = String(productType || '').toLowerCase();
      if (pt.indexOf('powder') >= 0 || pt.indexOf('spray') >= 0 || pt.indexOf('aerosol') >= 0 || pt.indexOf('mist') >= 0) return true;
      var words = [' spray', ' mist', ' aerosol', 'dry shampoo', 'loose powder', 'setting powder', 'bronzer powder',
        'blush powder', 'foundation powder', 'baby powder', 'talcum powder', 'body powder', 'face powder'];
      return words.some(function (w) { return n.indexOf(w) >= 0; });
    }

    function inferProductType(name, hint) {
      if (hint) return hint;
      var n = String(name).toLowerCase();
      if (n.indexOf('shampoo') >= 0 || n.indexOf('cleanser') >= 0 || n.indexOf('cleansing bar') >= 0 || n.indexOf('body wash') >= 0 || n.indexOf('wash') >= 0 || n.indexOf('bubble bath') >= 0) return 'body wash/shampoo/conditioner';
      if (n.indexOf('conditioner') >= 0 || n.indexOf('mask') >= 0) {
        if (n.indexOf('leave-in') >= 0 || n.indexOf('leave in') >= 0) return 'hair styling';
        return 'body wash/shampoo/conditioner';
      }
      if (/lotion|cream|moisturi[sz]er|balm/.test(n)) return 'leave-on skincare';
      if (/serum|oil|treatment|spray|leave-in|leave in|gel|foam|stick|mist/.test(n)) return 'hair styling';
      if (n.indexOf('deodorant') >= 0 || n.indexOf('antiperspirant') >= 0) return 'leave-on skincare';
      if (n.indexOf('toothpaste') >= 0 || n.indexOf('mouthwash') >= 0) return 'oral care';
      if (n.indexOf('sunscreen') >= 0 || n.indexOf('spf') >= 0) return 'leave-on skincare';
      if (n.indexOf('powder') >= 0) return 'powder';
      return 'leave-on skincare';
    }

    function isExemptUnknown(name) {
      var low = norm(name);
      low = low.replace(/[+^†‡]+/g, '');
      low = low.replace(/\s*\(\d{1,2}\)\s*$/, '').trim();
      low = low.replace(/([a-z])\d{1,2}$/, '$1').trim();
      low = stripChars(low, ' –-');
      if (EXEMPT_FRAG.has(low)) return true;
      if (low.indexOf('essential oil') >= 0) return true;
      // User ruling 2026-11-05: sea kelp (Organic, Acadian, Ascophyllum) is fine.
      if (low.indexOf('kelp') >= 0) return true;
      if (low.indexOf('organic ') === 0 || /\b(extract|powder|flour|seed|leaf|stem|bark|root|peel|flower|fruit|sucrose)\b/.test(low)) return true;
      if (/\b(olea|pisum|zea|cocos|bambusa|chenopodium|mentha|lavandula|vanilla|lavender|peppermint|tansy|ylang|hypericum|kale|lemon|carrot|rice|coconut|citrus|daucus|brassica)\b/.test(low)) return true;
      if (low.indexOf('silicon dioxide') >= 0) return true;
      if (String(name).trim().endsWith('*')) return true;
      if (/\b(carbonate|hydroxide|oxide|silica|bentonite|clay|sea salt|salt|ascorbate|starch)\b/.test(low)) return true;
      return false;
    }

    function inhalOnly(name) {
      var low = String(name || '').toLowerCase();
      if (low.indexOf('silylate') >= 0 || low.indexOf('silicone') >= 0) return false;
      if (/\bsilica\b/.test(low) && low.indexOf('hydrated') < 0) return true;
      return INHAL_ONLY_WORDS.some(function (w) { return w !== 'silica' && low.indexOf(w) >= 0; });
    }

    function rulingExempt(low) {
      if (has(REF, low) || (aget(low, '') !== '' && has(REF, aget(low, '')))) return false;
      if (/\b(water|aqua|eau)\b/.test(low)) return true;
      if (/\bwax\b|\bcera\b|\bvitamin\b/.test(low)) return true;
      if (/cobalamin|ascorbic|ascorbyl|niacin|niacinamide|riboflavin|thiamine|pyridoxine|folic|pantothenic|biotin|calciferol|cholecalciferol|\bb[1-9]\b|\bb1[0-2]\b/.test(low)) return true;
      if (/\b(sodium|potassium|magnesium|calcium|zinc)\s?(chloride|carbonate|phosphate|sulfate|silicate|hydroxide|citrate)\b/.test(low)) return true;
      if (/\b(hydrated silica|silica|kaolin|bentonite|clay|sea salt|dead sea salt)\b/.test(low)) return true;
      if (/\bextract\b/.test(low)) return true;
      if (/\bamino acids?\b|\barginine\b|\bcarnitine\b|\bcarnosine\b|\bkeratin amino\b/.test(low)) return true;
      if (/\barrowroot\b|\bbioflavonoid|\binositol\b|\bpapain\b|\bglycine soja\b|\bsoy|\bsoybean\b|\bessential oil blend\b|\baromatherapy blend\b|\bherbal blend\b/.test(low)) return true;
      if (/\bstarch\b/.test(low) || (/\bhydrolyzed\b/.test(low) && /\b(protein|peptide|amino|starch|quinoa|rice|wheat|oat|soy|corn)\b/.test(low))) return true;
      if (/^[a-z]+ [a-z]+ \(/.test(low) && /\b(oil|butter|extract|leaf|flower|root|seed|fruit|juice|peel|kernel|bark|powder)\b/.test(low)) return true;
      return false;
    }

    function isFragranceName(n) {
      var low = String(n).toLowerCase().trim().replace(/[\*†‡¤\.\s]+$/, '').trim();
      return /\b(fragrance|parfum|perfume|aroma|flavou?r|flavoring)\b/.test(low);
    }

    var BLEND_RE = /\bessential oil blend\b|\baromatherapy blend\b|\bherbal blend\b/;
    var FRAG_RE = /\b(fragrance|parfum|perfume|aroma|flavou?r|flavoring)\b/;

    // ---------- main ----------
    function grade(productName, productType, verbatim, disclosedFragrance) {
      var ingredients = splitIngredients(verbatim);
      var inhalProduct = isInhalationRisk(productName, productType);
      var vl = String(verbatim).toLowerCase();
      var flagged = [], natural = [], unknown = [];
      var escalations = new Set();
      var seen = new Set();
      var minTiers = [];

      for (var di = 0; di < ingredients.length; di++) {
        if (DYE_RE.test(ingredients[di])) { minTiers.push('Avoid (High)'); break; }
      }

      for (var i = 0; i < ingredients.length; i++) {
        var pos = i + 1;
        var ing = ingredients[i];
        var low = norm(ing);
        if (!low || seen.has(low)) continue;
        // Silver is not yet classified in the reference: always treat as unknown (manual review).
        if (/silver/i.test(low)) { unknown.push(ing); continue; }
        if (low === 'ext' || low === 'ext.') continue;
        if (isOralCare(productType) && FLUORIDE_RE.test(ing)) { flagged.push([ing, [9]]); minTiers.push('Avoid (High)'); seen.add(low); continue; }
        if (/^[^\p{L}\p{M}]*$/u.test(low)) continue;
        if (/^(aqua|water|eau)\)?(\s*[\/(]\s*(aqua|water|eau)\s*\)?)*$/.test(low)) continue;

        if (FRAG_RE.test(low) && BLEND_RE.test(low)) { natural.push([ing, [4, 8]]); continue; }
        var fragWord = /\b(fragrance|parfum|perfume|aroma|flavou?r|flavoring)\b(?![\s-]*free)/.test(low) && !BLEND_RE.test(low);
        if (rulingExempt(low) && !fragWord) continue;
        if (/^(vegetable |organic |plant )?glycerin\b\s*(\(.*\))?$/.test(low)) continue;
        seen.add(low);
        if (disclosedFragrance && /^(fragrance|parfum)(\s*\((fragrance|parfum)\))?$/.test(low)) continue;
        if (low.indexOf('behentrimonium methosulfate') >= 0) continue;
        // Any organic cotton is treated as low-tox (user ruling 2026-11-10).
        if (/\borganic cotton\b/.test(low)) continue;
        if (isFattyAlc(low)) continue;
        var nf = isNaturalFrag(low, vl);
        if (nf) { natural.push([ing, [4, 8]]); continue; }
        if (NAT_FRAG.has(low)) { flagged.push([ing, [1, 2, 4, 8]]); continue; }
        var lk = aget(low, low);
        if (LOW_TOX.has(low) && has(REF, lk) && !(REF[lk].c && REF[lk].c.length)) continue;
        if (low.indexOf('ceramide ') === 0) continue;
        var sc = !/^(peg|ppg)[-\s\/]/.test(low) && low.indexOf('arnica') < 0;
        if (sc && !fragWord && [' leaf extract', ' flower extract', ' fruit extract', ' root extract', ' seed extract', ' bark extract', ' peel extract', ' stem extract'].some(function (s) { return low.indexOf(s) >= 0; })) continue;
        if (sc && !fragWord && (low.indexOf('ferment') >= 0 || low.indexOf('extract') >= 0 || low.endsWith(' oil') || low.indexOf('butter') >= 0 || low.indexOf('juice') >= 0 || low.endsWith(' wax') || low.endsWith(' bran') || low.indexOf(' seed oil') >= 0 || low.indexOf(' root oil') >= 0 || low.indexOf(' peel oil') >= 0 || low.endsWith(' water'))) continue;
        if (low.endsWith(' acid') && !['acrylic acid', 'sulfonic acid'].some(function (b) { return low.indexOf(b) >= 0; })) continue;
        if (low.indexOf('mica') >= 0 && !inhalProduct && pos > 3) continue;
        if (inhalOnly(low) && !inhalProduct && low.indexOf('mica') < 0) continue;

        var key = aget(low, low);
        if (!has(REF, key)) {
          var base = key.replace(/\s*\([^)]*\)\s*$/, '').trim();
          var inner = key.match(/\(([^)]*)\)\s*$/);
          if (has(REF, base)) key = base;
          else if (inner && has(REF, inner[1].trim())) key = inner[1].trim();
        }
        if (has(REF, key)) {
          var d = REF[key];
          if (d.min) minTiers.push(d.min);
          if (d.l) continue;
          var cond = d.cond || '';
          if (cond === 'inhalation_risk' && !isInhalationRisk(productName, productType)) continue;
          var cats = d.c || [];
          if (cats.length) {
            flagged.push([ing, cats.concat(d.cnt4 ? [104] : [])]);
            if (FORMALDEHYDE.has(key) || FORMALDEHYDE.has(low)) escalations.add('formaldehyde-releaser');
            if (cats.indexOf(3) >= 0) escalations.add('heavy metals');
            var note = String(d.n || '').toLowerCase();
            if (note.indexOf('pfas treated') >= 0 && note.indexOf('may be pfas treated') < 0) escalations.add('PFAS');
            else if (note.indexOf('pfas') >= 0 && (low.indexOf('perfluoro') >= 0 || low.indexOf('pfas') >= 0)) escalations.add('PFAS');
            if (cats.indexOf(1) >= 0 && isLeaveOn(productType)) escalations.add('carcinogen in leave-on');
          }
          continue;
        }

        var matched = false;
        for (var pi = 0; pi < PATTERN_WATCH.length; pi++) {
          var pw = PATTERN_WATCH[pi];
          var pat = pw[0], pcats = pw[1], label = pw[2];
          if (pat.test(low)) {
            if (inhalOnly(label) && !inhalProduct) { matched = true; break; }
            if (pcats.length) {
              flagged.push([ing + ' [inferred: ' + label + ']', pcats]);
              if (pcats.indexOf(3) >= 0) escalations.add('heavy metals');
              var ll = label.toLowerCase();
              if (ll.indexOf('siloxane') >= 0 && ll.indexOf('dimethicone') < 0) escalations.add('PFAS');
              if (ll.indexOf('formaldehyde') >= 0) escalations.add('formaldehyde-releaser');
              if (pcats.indexOf(1) >= 0 && isLeaveOn(productType)) escalations.add('carcinogen in leave-on');
            }
            matched = true; break;
          }
        }
        if (matched) continue;

        if (FRAG_RE.test(low)) { flagged.push([ing, [1, 2, 4, 8]]); continue; }
        if (FORMALDEHYDE.has(low)) { flagged.push([ing, [1, 2, 4, 5]]); escalations.add('formaldehyde-releaser'); continue; }
        unknown.push(ing);
      }

      // Unique by lowercase name (first occurrence wins), as in grade().
      var sn = new Set(), flaggedAll = [];
      flagged.forEach(function (f) {
        var k = f[0].toLowerCase();
        if (sn.has(k)) return;
        sn.add(k); flaggedAll.push(f);
      });

      // Categories 4 and 5 alone never count toward the tier.
      var counted = flaggedAll.filter(function (f) {
        return !f[1].every(function (c) { return c === 4 || c === 5; });
      });
      var flagCount = counted.length;
      var hasParaben = counted.some(function (f) { return f[0].toLowerCase().indexOf('paraben') >= 0; });
      var hasFragrance = counted.some(function (f) { return isFragranceName(f[0]); });
      var hasHeavy = escalations.has('heavy metals') || counted.some(function (f) { return f[1].indexOf(3) >= 0; });
      var hasCarcLo = escalations.has('carcinogen in leave-on');
      var hasPfas = escalations.has('PFAS');
      var hasForm = escalations.has('formaldehyde-releaser');
      var hasCat2 = counted.some(function (f) { return f[1].indexOf(2) >= 0; });
      var maxCats = 0;
      counted.forEach(function (f) { if (f[1].length > maxCats) maxCats = f[1].length; });
      var catSet = new Set();
      counted.forEach(function (f) {
        f[1].forEach(function (k) {
          if (k !== 4 && k !== 5) catSet.add(k);
          else if (k === 104) catSet.add(4);
        });
      });
      var nCats = catSet.size;

      var tier = 'Puberty Safe';
      if (flagCount === 0) tier = 'Puberty Safe';
      else if (nCats <= 2 && !hasParaben && !hasFragrance && !hasHeavy && !hasForm) tier = 'Use Caution';
      else if (nCats >= 3 || maxCats >= 3 || hasParaben) tier = 'Avoid (Mild)';
      if (hasHeavy || hasForm || hasFragrance || nCats >= 5) {
        if (ORDER.indexOf(tier) < ORDER.indexOf('Avoid (Moderate)')) tier = 'Avoid (Moderate)';
      }

      var highEndoHits = counted.filter(function (f) {
        var l = f[0].toLowerCase();
        return HIGH_ENDOCRINE_HINTS.some(function (h) { return l.indexOf(h) >= 0; });
      }).map(function (f) { return f[0]; });
      var cat2Hits = counted.filter(function (f) {
        return f[1].indexOf(2) >= 0 && !isFragranceName(f[0]);
      }).map(function (f) { return f[0]; });
      var hasEndocrine = highEndoHits.length > 0 || cat2Hits.length >= 3;
      var hasCat1 = counted.some(function (f) { return f[1].indexOf(1) >= 0; });

      if (hasPfas || nCats >= 8 || hasCarcLo || (hasHeavy && (hasCat1 || hasCat2))) tier = 'Avoid (High)';
      // User ruling 2026-11-07: in a rinse-off product, 3+ carcinogen (category 1) ingredients is Avoid (Moderate); 6+ is Avoid (High).
      var nCarc = counted.filter(function (f) { return f[1].indexOf(1) >= 0; }).length;
      var carcRinse = !isLeaveOn(productType) && nCarc >= 3;
      if (carcRinse && nCarc >= 6) tier = 'Avoid (High)';
      else if (carcRinse && ORDER.indexOf(tier) < ORDER.indexOf('Avoid (Moderate)')) tier = 'Avoid (Moderate)';
      if (hasEndocrine && (cat2Hits.length >= 3 || highEndoHits.length >= 2)) tier = 'Avoid (High)';

      minTiers.forEach(function (mt) {
        if (ORDER.indexOf(tier) < ORDER.indexOf(mt)) tier = mt;
      });

      var esc = [];
      if (hasPfas) esc.push('PFAS');
      if (hasHeavy) esc.push('heavy metals');
      if (hasForm) esc.push('formaldehyde-releaser');
      if (carcRinse) esc.push('carcinogens in rinse-off');
      if (hasCarcLo) esc.push('carcinogen in leave-on');
      if (hasEndocrine) esc.push('endocrine disruption');

      if (tier === 'Puberty Safe' && unknown.some(function (u) { return !isExemptUnknown(u); })) tier = 'Use Caution';

      return {
        tier: tier,
        flagCount: flagCount,
        flagged: flaggedAll,      // [name, cats][]
        natural: natural,         // [name, cats][]
        unknown: unknown,         // names[]
        esc: esc,                 // names[]
        ingredients: ingredients  // parsed list, in order
      };
    }

    return {
      grade: grade,
      splitIngredients: splitIngredients,
      norm: norm,
      inferProductType: inferProductType,
      isInhalationRisk: isInhalationRisk
    };
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = makeGrader;
  else root.makeGrader = makeGrader;
})(typeof window !== 'undefined' ? window : this);
