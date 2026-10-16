import json, re, sys
import openpyxl

BASE = '/home/claude/ingredient-scraper'
REF_PATH = f'{BASE}/ref_compact.json'
ALIAS_PATH = f'{BASE}/ingredient_aliases.json'
ING_PATH = f'{BASE}/audits/eucerin/eucerin_ingredients.json'
OUT_XLSX = f'{BASE}/audits/eucerin/eucerin_audit.xlsx'

ref_data = json.load(open(REF_PATH))
REF = ref_data['ref']
ALIASES = dict(ref_data['aliases'])
ALIASES.update(json.load(open(ALIAS_PATH)))
# Addendum 2026-10-09: bare "Zinc Oxide" in a cream/lotion is treated as zinc oxide (non-nano)
ALIASES['zinc oxide'] = 'zinc oxide (non-nano)'

# LOW TOX list carried over from the briogeo grader (names the reference file does not list)
LOW_TOX = set([
'water','aqua','glycerin','sodium chloride','citric acid','sodium citrate','sodium hyaluronate','niacinamide',
'phytosphingosine','xanthan gum','cholesterol','carbomer','panthenol','allantoin','sodium hydroxide','potassium hydroxide',
'potassium sorbate','sodium benzoate','tocopherol','tocopheryl acetate','caprylic/capric triglyceride','caprylyl glycol',
'sodium pca','lactic acid','salicylic acid','ascorbic acid','retinol','kaolin','squalane','hydroxyethylcellulose',
'sorbitol','urea','maltodextrin','dextran','glycine','threonine','arginine','serine','valine','proline','isoleucine',
'alanine','phenylalanine','histidine','aspartic acid','sodium lactate','glyceryl stearate','glyceryl oleate',
'octyldodecanol','isohexadecane','isopropyl myristate','isopropyl palmitate','ethylhexyl palmitate','cetyl palmitate',
'polysorbate 20','polysorbate 60','polysorbate 80','cetearyl isononanoate','coco-betaine','sodium cocoyl isethionate',
'sodium isethionate','hydrogenated vegetable oil','hydrogenated castor oil','ozokerite','hyaluronic acid',
'cetyl hydroxyethylcellulose','decyl glucoside','beeswax','beeswax (cera alba)','dicaprylyl carbonate',
'triethylhexanoin','sorbitan stearate','benzoic acid','sodium polyacrylate','dipotassium phosphate','potassium phosphate',
'cetearyl alcohol','cetyl alcohol','stearyl alcohol','behenyl alcohol','brassica alcohol','c14-22 alcohols',
'caprylyl/capryl glucoside','coco-glucoside','coco glucoside','behentrimonium methosulfate',
])
FATTY_ALC = ['cetearyl alcohol','cetyl alcohol','stearyl alcohol','behenyl alcohol','brassica alcohol','c14-22 alcohols']
NAT_FRAG = {'linalool','limonene','citral','citronellal','geraniol','eugenol','isoeugenol','coumarin','farnesol',
            'hydroxycitronellal','bisabolol'}
EO_HINTS = ['oil','essential oil','extract','butter','juice','wax','absolute']
FORMALDEHYDE = {'dmdm hydantoin','diazolidinyl urea','imidazolidinyl urea','quaternium-15','methenamine',
                'paraformaldehyde','benzylhemiformal','5-bromo-5-nitro-1,3-dioxane','sodium hydroxymethylglycinate',
                'glyoxal','polyoxymethylene urea','2-bromo-2-nitropropane-1,3-diol'}
PATTERN_WATCH = [
    (re.compile(r'^peg[-\s]?\d', re.I), [1,2,4,5], 'PEG-'),
    (re.compile(r'^ppg[-\s]?\d', re.I), [1,2,4,5], 'PPG-'),
    (re.compile(r'(?:^|\s|-)(laureth|ceteth|oleth|steareth|trideceth|ceteareth|buteth|pareth|isoceteth)(?:-?\d|$)', re.I), [1,4,5], '-eth ethoxylate'),
    (re.compile(r'siloxane$|cyclopentasiloxane|cyclohexasiloxane|cyclotetrasiloxane|cyclomethicone', re.I), [1,2,6], 'siloxane'),
    (re.compile(r'(^|\s)dimethicone\b', re.I), [2,6], 'silicone'),
    (re.compile(r'\bparaben\b', re.I), [2,4], 'paraben'),
    (re.compile(r'sulfate$', re.I), [1,4,5], 'sulfate'),
    (re.compile(r'phthalate', re.I), [2], 'phthalate'),
    (re.compile(r'^propylene glycol$|^butylene glycol$|^hexylene glycol$|^ethylene glycol$|^dipropylene glycol$', re.I), [1,2], '-glycol'),
    (re.compile(r'monium chloride$|^behenalkonium|^stearalkonium|^cetrimonium|dicetyldimonium chloride$', re.I), [2], '-nium quat'),
    (re.compile(r'\bphenoxyethanol\b', re.I), [1,2,4,5,8], 'phenoxyethanol'),
    (re.compile(r'^alcohol\s*denat', re.I), [4], 'alcohol denat'),
    (re.compile(r'^alcohol$', re.I), [4], 'alcohol'),
    (re.compile(r'^aluminum|^aluminium', re.I), [3], 'aluminum'),
    (re.compile(r'^mineral oil$|^petrolatum$|^petroleum$|^paraffin$', re.I), [1], 'petroleum'),
    (re.compile(r'^cocamidopropyl', re.I), [1,4], 'cocamidopropyl'),
]
FRAG_NAMES = ('fragrance','parfum','natural fragrance','parfum/fragrance','perfume','fragrance (parfum)')

def norm(s):
    s = s.lower().strip()
    s = re.sub(r'\s*\([^)]*\)\s*$', '', s)     # drop trailing "(3%)" or "(3.5)" concentration notes
    s = re.sub(r'\s+', ' ', s).strip(' .,;:*')
    return s

def is_fatty_alc(low):
    return any(fa in low for fa in FATTY_ALC)

def split_ingredients(text):
    parts = re.split(r',', text)
    return [p.strip() for p in parts if p.strip()]

def lookup(ing):
    """Return (kind, cats, label). kind: 'flag' | 'nat' | 'ok' | 'unknown' """
    low = norm(ing)
    if low == 'behentrimonium methosulfate' or is_fatty_alc(low):
        return ('ok', [], 'rubric exemption')
    if low in NAT_FRAG:
        return ('nat', [4,8], low)
    key = ALIASES.get(low, low)
    if key in REF:
        d = REF[key]
        if d.get('l'):
            return ('ok', [], 'reference LOW TOX')
        cats = d.get('c', [])
        if cats:
            return ('flag', cats, 'reference')
        return ('ok', [], 'reference, no category')
    if low in LOW_TOX or key in LOW_TOX:
        return ('ok', [], 'LOW TOX list')
    if low in FRAG_NAMES:
        return ('flag', [1,2,4,8], 'fragrance without disclosure')
    if low in FORMALDEHYDE:
        return ('flag', [1,2,4,5], 'formaldehyde-releaser')
    for pat, cats, label in PATTERN_WATCH:
        if pat.search(low):
            return ('flag', cats, 'inferred: ' + label)
    return ('unknown', [], '')

def grade(product_type, verbatim):
    flagged, natural, unknown = [], [], []
    esc = set()
    seen = set()
    for ing in split_ingredients(verbatim):
        low = norm(ing)
        if low in seen: continue
        seen.add(low)
        kind, cats, label = lookup(ing)
        if kind == 'flag':
            flagged.append((ing, cats, label))
            if 3 in cats: esc.add('heavy metals')
            if norm(ing) in FORMALDEHYDE or ALIASES.get(low, low) in FORMALDEHYDE: esc.add('formaldehyde-releaser')
            if 1 in cats and product_type == 'leave-on skincare': esc.add('carcinogen in leave-on')
        elif kind == 'nat':
            natural.append((ing, cats, label))
        elif kind == 'unknown':
            unknown.append(ing)
    flag_count = len(flagged)
    has_paraben = any('paraben' in label or 'paraben' in n.lower() for n,_,label in flagged)
    has_frag = any(label.startswith('fragrance') for _,_,label in flagged)
    has_heavy = 'heavy metals' in esc
    has_form = 'formaldehyde-releaser' in esc
    has_carc_lo = 'carcinogen in leave-on' in esc
    max_cats = max([len(c) for _,c,_ in flagged], default=0)
    order = ['Puberty Safe','Use Caution','Avoid (Mild)','Avoid (Moderate)','Avoid (High Priority Swap)']
    tier = 'Puberty Safe'
    if flag_count == 0:
        tier = 'Puberty Safe'
    elif flag_count <= 2 and max_cats < 3 and not has_paraben and not has_frag and not has_heavy and not has_form:
        tier = 'Use Caution'
    else:
        tier = 'Avoid (Mild)'
    if has_heavy or has_form or has_frag or flag_count >= 5:
        if order.index(tier) < order.index('Avoid (Moderate)'):
            tier = 'Avoid (Moderate)'
    if has_carc_lo or flag_count >= 8 or (has_heavy and has_frag):
        tier = 'Avoid (High Priority Swap)'
    esc_list = []
    for x in ['heavy metals','formaldehyde-releaser','carcinogen in leave-on']:
        if x in esc: esc_list.append(x)
    return tier, flagged, natural, unknown, esc_list

def fmt_flags(items):
    return ' / '.join(f"{n} [{','.join(str(c) for c in cats)}]" + (f" (inferred: {l[10:]})" if l.startswith('inferred: ') else '') for n,cats,l in items)

def fmt_nat(items):
    return ' / '.join(f"{n} [{','.join(str(c) for c in cats)}]" for n,cats,l in items)

if __name__ == '__main__':
    data = json.load(open(ING_PATH))
    prods = data['products']
    # identical-text detection across products
    text_map = {}
    for p in prods:
        text_map.setdefault(p['ingredients_verbatim'], []).append(p['product_name'])
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'audit'
    headers = ["product_name","product_url","brand_category","product_type","ingredients_verbatim","tier","flag_count",
               "flagged_ingredients","naturally_occurring_allergens","unknown_ingredients","automatic_escalation",
               "one_line_summary","audit_notes","audit_status"]
    ws.append(headers)
    tiers = {}; results = []
    for p in prods:
        tier, flagged, natural, unknown, esc = grade(p['product_type'], p['ingredients_verbatim'])
        tiers[tier] = tiers.get(tier,0)+1
        fl = fmt_flags(flagged); nat = fmt_nat(natural); unk = ', '.join(unknown)
        esc_s = ', '.join(esc)
        if flagged:
            top = ', '.join(n for n,_,_ in flagged[:3])
            summary = f"{len(flagged)} flagged ingredient(s) in the printed list ({top}); tier applies to printed subset only."
        else:
            summary = "No flagged ingredients in the printed subset per reference."
        if unknown:
            summary += f" {len(unknown)} unknown ingredient(s) not in reference."
        notes = [f"Printed block: {p['listing_block']}.",
                 "Site publishes a partial list (key/active ingredients only, no full INCI); tier is provisional."]
        same = [x for x in text_map[p['ingredients_verbatim']] if x != p['product_name']]
        if same:
            notes.append(f"Identical printed text on {len(same)} other product(s): {'; '.join(same[:4])}.")
        if unknown:
            notes.append("Unknown ingredients left unscored; tier does not account for them.")
        if p['product_type'] == 'sunscreen' and 'zinc oxide' in p['ingredients_verbatim'].lower():
            notes.append("Zinc Oxide treated as zinc oxide (non-nano) per addendum 2026-10-09; LOW TOX in lotions.")
        row = [p['product_name'], p['product_url'], p['brand_category'], p['product_type'], p['ingredients_verbatim'],
               tier, len(flagged), fl, nat, unk, esc_s, summary, ' '.join(notes), 'needs review']
        ws.append(row); results.append(row)
    wb.save(OUT_XLSX)
    print('tiers:', tiers)
    print('rows:', len(results))
    json.dump({'tiers': tiers, 'rows': [dict(zip(headers, r)) for r in results]},
              open(f'{BASE}/audits/eucerin/_grade_summary.json','w'), indent=1, ensure_ascii=False)
