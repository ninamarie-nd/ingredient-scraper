"""JERGENS grader. Adapted from audits/briogeo/_grader.py (paths and reference handling changed).

Differences from the briogeo template, all deliberate:
- Reference lookup runs first (ref_compact.json + ingredient_aliases.json + the 2026-10-09 addendum).
  The template ran a hardcoded LOW_TOX list before the reference, which marks carbomer LOW even though
  the reference flags it [1,4,6]. Here the reference wins.
- The template LOW_TOX list and botanical-name heuristic are used only as a disclosed fallback for names
  that are not in the reference at all. Every fallback use is recorded in the summary for review.
- PFAS escalation applies only to reference entries whose note says "PFAS treated" (rubric wording),
  not to every pattern-matched silicone.
- Carcinogen-in-leave-on escalation applies only to direct reference/addendum category-1 hits, not
  pattern-inferred categories.
- Essential-oil source check: naturally occurring fragrance components are soft only if the product
  lists an essential oil (an ingredient containing 'oil' plus a plant name). Otherwise full flags.
"""
import json, re, os
import openpyxl

BASE = '/home/claude/ingredient-scraper'
OUTDIR = BASE + '/audits/jergens'
REF_PATH = BASE + '/ref_compact.json'
ALIAS_PATH = BASE + '/ingredient_aliases.json'
ADD_PATH = BASE + '/Ingredient_Safety_Reference_Addendum_2026-10-09.md'
TEMPLATE = BASE + '/audits/briogeo/_grader.py'
ING_PATH = OUTDIR + '/jergens_ingredients.json'
MASTER = OUTDIR + '/_master_list.json'
XLSX = OUTDIR + '/jergens_audit.xlsx'
SUMMARY = OUTDIR + '/_grade_summary.json'

TIERS = ['Puberty Safe', 'Use Caution', 'Avoid (Mild)', 'Avoid (Moderate)', 'Avoid (High Priority Swap)']

def ck(s):
    s = s.lower().replace('.', '')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'(\w)\s*-\s*(\d)', r'\1-\2', s)   # 'c13- 14' -> 'c13-14'
    return s.strip(' ,;:')

# ---------- reference ----------
ref_data = json.load(open(REF_PATH))
REF = {ck(k): dict(v, src='ref') for k, v in ref_data['ref'].items()}
ALIASES = {ck(k): ck(v) for k, v in ref_data['aliases'].items()}
ALIASES.update({ck(k): ck(v) for k, v in json.load(open(ALIAS_PATH)).items()})

ADD = {}
for line in open(ADD_PATH):
    if not line.startswith('| ') or line.startswith('| Ingredient') or line.startswith('|---'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 4:
        continue
    name, cats, lowtox, notes = cells[0], cells[1], cells[2], cells[3]
    c = [] if cats in ('—', '-', '') else [int(x) for x in re.findall(r'\d', cats)]
    entry = {'c': c, 'l': 'LOW TOX' in lowtox, 'n': notes, 'src': 'addendum'}
    for k in {ck(name), ck(re.sub(r'\s*\(.*?\)', '', name))}:
        ADD.setdefault(k, entry)

GREF = dict(REF)
for k, v in ADD.items():
    GREF.setdefault(k, v)

# ---------- rubric pattern rules (copied from template PATTERN_WATCH) ----------
PATTERN_WATCH = [
    (re.compile(r'^peg[-\s]?\d', re.I), [1,2,4,5], 'PEG-'),
    (re.compile(r'^ppg[-\s]?\d', re.I), [1,2,4,5], 'PPG-'),
    (re.compile(r'(?:^|\s|-)(laureth|ceteth|oleth|steareth|trideceth|ceteareth|buteth|pareth|isoceteth)(?:-?\d|$)', re.I), [1,4,5], '-eth ethoxylate'),
    (re.compile(r'^laureth-\d', re.I), [1,4,5], 'laureth-'),
    (re.compile(r'siloxane$|cyclopentasiloxane|cyclohexasiloxane|cyclotetrasiloxane|cyclomethicone', re.I), [1,2,6], 'siloxane'),
    (re.compile(r'(^|\s)dimethicone\b', re.I), [2,6], 'silicone'),
    (re.compile(r'dimethiconol', re.I), [2,6], 'silicone'),
    (re.compile(r'\bparaben\b', re.I), [2,4], 'paraben'),
    (re.compile(r'sulfate$', re.I), [1,4,5], 'sulfate'),
    (re.compile(r'phthalate', re.I), [2], 'phthalate'),
    (re.compile(r'\bbenzophenone\b', re.I), [3], 'benzophenone'),
    (re.compile(r'^propylene glycol$|^butylene glycol$|^hexylene glycol$|^ethylene glycol$|^dipropylene glycol$', re.I), [1,2], '-glycol'),
    (re.compile(r'monium chloride$|^behenalkonium|^stearalkonium|^cetrimonium|^cetyl pyridinium|^guar hydroxypropyltrimonium|hydroxypropyltrimonium chloride$|dicetyldimonium chloride$|^behentrimonium chloride', re.I), [2], '-nium quat'),
    (re.compile(r'\bphenoxyethanol\b', re.I), [1,2,4,5,8], 'phenoxyethanol'),
    (re.compile(r'\bbht\b|butylated hydroxytoluene', re.I), [1,2], 'BHT'),
    (re.compile(r'\bbha\b|butylated hydroxyanisole', re.I), [1,2], 'BHA'),
    (re.compile(r'^tetrasodium edta$', re.I), [1], 'tetrasodium EDTA'),
    (re.compile(r'^disodium edta$', re.I), [4], 'disodium EDTA'),
    (re.compile(r'^ethylhexylglycerin$', re.I), [4,5], 'ethylhexylglycerin'),
    (re.compile(r'^chlorphenesin$', re.I), [4], 'chlorphenesin'),
    (re.compile(r'^triethanolamine', re.I), [1,4], 'TEA'),
    (re.compile(r'^ethanolamine$', re.I), [4], 'ethanolamine'),
    (re.compile(r'^mineral oil$|paraffinum liquidum|^petrolatum$|^petroleum$|^paraffin$', re.I), [1], 'petroleum'),
    (re.compile(r'^cocamidopropyl', re.I), [1,4], 'cocamidopropyl'),
    (re.compile(r'^lauramidopropyl', re.I), [1,4], 'lauramidopropyl'),
    (re.compile(r'^polyethylene$', re.I), [6], 'polyethylene'),
    (re.compile(r'^alcohol\s*denat', re.I), [4], 'alcohol denat'),
    (re.compile(r'^alcohol$', re.I), [4], 'alcohol'),
    (re.compile(r'^aluminum|^aluminium', re.I), [3], 'aluminum'),
    (re.compile(r'^ci 77', re.I), [1,2,3], 'colorant CI#'),
    (re.compile(r'^isododecane', re.I), [1,2], 'isododecane'),
    (re.compile(r'^vp/va copolymer', re.I), [1,4,6], 'VP/VA copolymer'),
    (re.compile(r'^sulfosuccinate$', re.I), [5], 'sulfosuccinate'),
    (re.compile(r'^polyquaternium-\d+$', re.I), [2], 'polyquaternium'),
]

# ---------- formaldehyde releasers (rubric list) ----------
FORMALDEHYDE = {'dmdm hydantoin','diazolidinyl urea','diazolidinylurea','imidazolidinyl urea','imidazolidinylurea','quaternium-15','methenamine','paraformaldehyde','benzylhemiformal','5-bromo-5-nitro-1,3-dioxane','sodium hydroxymethylglycinate','glyoxal','polyoxymethylene urea','2-bromo-2-nitropropane-1,3-diol'}

NAT_FRAG = {'linalool','limonene','citral','citronellal','geraniol','eugenol','isoeugenol','coumarin','farnesol','hydroxycitronellal','bisabolol'}
FRAG_NAMES = {'fragrance','parfum','natural fragrance','fragrance/parfum','parfum/fragrance','perfume','fragrance (parfum)'}
FATTY_ALC = ['cetearyl alcohol','cetyl alcohol','stearyl alcohol','behenyl alcohol','brassica alcohol','myristyl alcohol','lauryl alcohol','c14-22 alcohols']

# ---------- fallback lists (template, used only if a name is not in the reference) ----------
_tsrc = open(TEMPLATE).read()
_m = re.search(r'LOW_TOX = set\(\[(.*?)\]\)', _tsrc, re.S)
LOW_FALLBACK = set(x.lower() for x in re.findall(r"'([^']*)'", _m.group(1)))

EO_KEYWORDS = ['lavender','lavandula','lemon','citrus limon','orange','citrus aurantium dulcis','bergamot','rosa','rose','eucalyptus','peppermint','mentha','tea tree','melaleuca','cinnamon','chamomile','ylang','geranium','sandalwood','patchouli','vetiver','clary','grapefruit','citrus grandis','lime','lemongrass','cymbopogon','basil','ocimum']

def has_eo_source(text):
    for part in re.split(r',|\|\|', text):
        p = part.lower()
        if ' oil' in p and any(k in p for k in EO_KEYWORDS):
            return True
    return False

def clean_item(s):
    s = re.sub(r'\(\s*\d+(\.\d+)?\s*%\s*\)', '', s)
    s = re.sub(r'\d+(\.\d+)?\s*%', '', s)
    s = re.sub(r'^\s*(and|And)\s+', '', s.strip())
    s = re.sub(r'^\s*(active ingredients?|inactive ingredients?)\s*:?\s*', '', s, flags=re.I)
    s = s.strip(' .;:')
    return s

def _split_top(text):
    """Split on , or ; but not inside () or []."""
    parts, buf, depth = [], [], 0
    for ch in text:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth = max(0, depth - 1)
        if ch in ',;' and depth == 0:
            parts.append(''.join(buf)); buf = []
        else:
            buf.append(ch)
    parts.append(''.join(buf))
    return parts

def split_list(text):
    protected = re.sub(r'(\d),(\d)', r'\1<C>\2', text)
    protected = protected.replace('Inactive Ingredients :', ',').replace('Inactive Ingredients:', ',')
    protected = re.sub(r'With an illuminating[^,]*?(?=FRAGRANCE|$)', '', protected)
    out = []
    for p in _split_top(protected):
        p = p.replace('<C>', ',')
        p = clean_item(p)
        if p and p.lower() not in ('ingredients', ''):
            out.append(p)
    return out

def segments(verbatim):
    """Return list of (label, [items], [fragrance_breakdown_items]) for each shade/component."""
    segs = []
    for raw in verbatim.split(' || '):
        label = ''
        m = re.match(r'^\[([^\]]+)\]\s*', raw)
        if m:
            label = m.group(1)
            raw = raw[m.end():]
        raw = raw.replace('Active Ingredients:', '').replace('Active Ingredients :', '')
        if 'FRAGRANCE INGREDIENTS:' in raw:
            main, frag = raw.split('FRAGRANCE INGREDIENTS:', 1)
            frag_items = split_list(frag)
        else:
            main, frag_items = raw, []
        # strip a shade header like 'Jergens Natural Glow ... Light Bronze:' if present
        main = re.sub(r'^[^:]*Bronze:\s*', '', main)
        items = split_list(main)
        segs.append((label, items, frag_items))
    return segs

def classify(item, eo_source):
    n = ck(item)
    canon = ALIASES.get(n, n)
    if 'behentrimonium methosulfate' in n:
        return ('LOW', 'rubric exemption (behentrimonium methosulfate)')
    if any(fa in n for fa in FATTY_ALC):
        return ('LOW', 'rubric exemption (fatty alcohol)')
    if canon in FRAG_NAMES or n in FRAG_NAMES:
        if canon in GREF and not GREF[canon]['l'] and GREF[canon]['c']:
            return ('FLAG', GREF[canon]['c'], 'ref', GREF[canon])
        return ('FLAG', [1, 2, 4, 8], 'fragrance', {'n': 'fragrance/parfum (full flag, rubric)'})
    if canon in GREF:
        e = GREF[canon]
        if e['l']:
            return ('LOW', e['src'] + ' LOW TOX')
        if e['c']:
            if canon in NAT_FRAG and eo_source:
                return ('NATURAL', e['c'], e['src'], e)
            return ('FLAG', e['c'], e['src'], e)
        return ('LOW', e['src'] + ' (no categories)')
    if n in NAT_FRAG and eo_source:
        return ('NATURAL', [4, 8], 'pattern-nat', {'n': ''})
    for pat, cats, label in PATTERN_WATCH:
        if pat.search(n):
            return ('FLAG', cats, 'pattern:' + label, {'n': ''})
    if n in FORMALDEHYDE or canon in FORMALDEHYDE:
        return ('FLAG', [1, 2, 4, 5], 'formaldehyde-releaser', {'n': ''})
    if n in LOW_FALLBACK or canon in LOW_FALLBACK:
        return ('LOW', 'fallback: template LOW list (not in reference)')
    if (('ferment' in n or 'extract' in n or n.endswith(' oil') or 'butter' in n or 'juice' in n
         or n.endswith(' wax') or n.endswith(' bran') or ' seed oil' in n or ' root oil' in n
         or ' peel oil' in n or n.endswith(' water'))):
        return ('LOW', 'fallback: botanical name heuristic (not in reference)')
    return ('UNKNOWN',)

def grade_segment(items, frag_items, eo_source):
    flagged, natural, unknown, fallback, esc = [], [], [], [], set()
    seen = set()
    for it in items + frag_items:
        key = ck(it)
        if not key or key in seen:
            continue
        seen.add(key)
        r = classify(it, eo_source)
        if r[0] == 'LOW':
            if 'fallback' in r[1]:
                fallback.append((it, r[1]))
            continue
        if r[0] == 'UNKNOWN':
            unknown.append(it)
            continue
        if r[0] == 'NATURAL':
            natural.append((it, r[1]))
            continue
        _, cats, src, entry = r
        note = (entry.get('n') or '').lower()
        flagged.append({'name': it, 'cats': cats, 'src': src, 'pattern': src.startswith('pattern')})
        if 3 in cats:
            esc.add('heavy metals')
        if src in ('ref', 'addendum') and 'pfas treated' in note:
            esc.add('PFAS')
        if key in FORMALDEHYDE or ALIASES.get(key, key) in FORMALDEHYDE or src == 'formaldehyde-releaser':
            esc.add('formaldehyde-releaser')
        if src in ('ref', 'addendum') and 1 in cats:
            esc.add('carcinogen in leave-on')
    return flagged, natural, unknown, fallback, esc

def tier_for(flagged, esc):
    fc = len(flagged)
    if fc == 0:
        return 'Puberty Safe', fc
    names = [f['name'].lower() for f in flagged]
    paraben = any('paraben' in n for n in names)
    frag = any(('fragrance' in n or 'parfum' in n or n.startswith('perfume')) for n in names)
    heavy = 'heavy metals' in esc
    form = 'formaldehyde-releaser' in esc
    pfas = 'PFAS' in esc
    cat1 = 'carcinogen in leave-on' in esc
    cat2 = any(2 in f['cats'] for f in flagged)
    max_cats = max(len(f['cats']) for f in flagged)
    high = pfas or fc >= 8 or cat1 or (heavy and cat2 and frag)
    mod = heavy or form or frag or fc >= 5
    mild = fc >= 3 or max_cats >= 3 or paraben
    if high:
        t = 'Avoid (High Priority Swap)'
    elif mod:
        t = 'Avoid (Moderate)'
    elif mild:
        t = 'Avoid (Mild)'
    elif fc in (1, 2):
        t = 'Use Caution'
    else:
        t = 'Puberty Safe'
    return t, fc

def fmt_cats(c):
    return '[' + ','.join(str(x) for x in c) + ']'

def grade_product(verbatim):
    eo = has_eo_source(verbatim)
    segs = segments(verbatim)
    all_flag, all_nat, all_unk, all_fb = {}, {}, [], []
    esc = set()
    for label, items, frag in segs:
        f, nat, unk, fb, e = grade_segment(items, frag, eo)
        for x in f:
            all_flag.setdefault(x['name'].lower(), x)
        for n, c in nat:
            all_nat.setdefault(n.lower(), (n, c))
        for u in unk:
            if u not in all_unk:
                all_unk.append(u)
        for x in fb:
            if x not in all_fb:
                all_fb.append(x)
        esc |= e
    flagged = list(all_flag.values())
    tier, fc = tier_for(flagged, esc)
    return {
        'tier': tier, 'flag_count': fc,
        'flagged': flagged, 'natural': list(all_nat.values()),
        'unknown': all_unk, 'fallback': all_fb, 'esc': esc,
        'eo_source': eo, 'segments': len(segs),
    }

def format_flagged(flagged):
    out = []
    for f in flagged:
        s = f"{f['name']} {fmt_cats(f['cats'])}"
        if f['pattern']:
            s += ' (inferred: ' + f['src'].split(':', 1)[1] + ')'
        out.append(s)
    return ' / '.join(out)

def format_natural(natural):
    return ' / '.join(f"{n} {fmt_cats(c)}" for n, c in natural)

def summary_line(res, name):
    if res['flag_count'] == 0:
        s = 'No flagged ingredients per reference (after rubric exemptions).'
    else:
        top = [f['name'] for f in res['flagged'][:3]]
        s = f"{res['flag_count']} flagged ingredient(s), including {', '.join(top)}."
    if res['esc']:
        s += ' Escalation: ' + ', '.join(sorted(res['esc'])) + '.'
    return s

def main():
    ing = json.load(open(ING_PATH))
    master = json.load(open(MASTER))
    headers = ["product_name","product_url","brand_category","product_type","ingredients_verbatim",
               "tier","flag_count","flagged_ingredients","naturally_occurring_allergens",
               "unknown_ingredients","automatic_escalation","one_line_summary","audit_notes","audit_status"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'audit'
    ws.append(headers)
    results = {}
    unknown_all, fallback_all = {}, {}
    for m in master:
        slug = m['slug']
        rec = ing['products'].get(slug, {})
        verbatim = rec.get('ingredients_verbatim', '') or ''
        status = rec.get('status', 'ingredients not found')
        notes = rec.get('note', '') or ''
        if rec.get('variants'):
            notes = (notes + ' ' if notes else '') + rec['variants']
        row = [m['product_name'], m['product_url'], m['brand_category'], m['product_type'], verbatim]
        if status != 'scraped' or not verbatim:
            row += ['', None, '', '', '', '', 'Not graded: no ingredient list on page.', notes, 'ingredients not found']
            ws.append(row)
            results[slug] = {'status': status, 'tier': None}
            continue
        res = grade_product(verbatim)
        results[slug] = {'status': 'complete', 'tier': res['tier'], 'fc': res['flag_count'],
                         'esc': sorted(res['esc']), 'flagged': [f['name'] for f in res['flagged']],
                         'unknown': res['unknown'], 'fallback': res['fallback'], 'eo_source': res['eo_source'],
                         'natural': [n for n, _ in res['natural']]}
        for u in res['unknown']:
            unknown_all.setdefault(ck(u), (u, []))[1].append(m['product_name'])
        for fb, why in res['fallback']:
            fallback_all.setdefault(ck(fb), (fb, why, []))[2].append(m['product_name'])
        extra = []
        if res['segments'] > 1:
            extra.append(f"Graded as one union across {res['segments']} shade/component lists.")
        if res['natural']:
            extra.append('Naturally occurring fragrance components listed standalone (no essential oil source on page), graded as full flags per rubric.')
        if any(f['name'].lower().startswith('fragrance') or f['name'].lower().startswith('parfum') for f in res['flagged']):
            extra.append('Fragrance listed; full flag applied.')
        if res['unknown']:
            extra.append(f"{len(res['unknown'])} unknown ingredient(s) not in reference, see unknown column.")
        if res['fallback']:
            extra.append(f"{len(res['fallback'])} name(s) classified by template fallback (not in reference): " + ', '.join(x for x, _ in res['fallback']) + '.')
        if notes:
            extra.insert(0, notes)
        row = [m['product_name'], m['product_url'], m['brand_category'], m['product_type'], verbatim,
               res['tier'], res['flag_count'], format_flagged(res['flagged']), format_natural(res['natural']),
               ('unknown — manual review needed: ' + ', '.join(res['unknown'])) if res['unknown'] else '',
               ', '.join(sorted(res['esc'])), summary_line(res, m['product_name']),
               ' '.join(extra), ('needs review' if res['unknown'] else 'complete')]
        ws.append(row)
    wb.save(XLSX)
    json.dump({'results': results,
               'unknown_dedup': [{'ingredient': v[0], 'products': sorted(set(v[1]))} for v in unknown_all.values()],
               'fallback_dedup': [{'ingredient': v[0], 'why': v[1], 'products': sorted(set(v[2]))} for v in fallback_all.values()]},
              open(SUMMARY, 'w'), indent=1, ensure_ascii=False)
    from collections import Counter
    print('tiers:', Counter(r['tier'] for r in results.values() if r.get('tier')))
    print('not graded:', [s for s, r in results.items() if r['status'] != 'complete' and r.get('tier') is None])
    print('unknown dedup count:', len(unknown_all))
    print('fallback dedup count:', len(fallback_all))

if __name__ == '__main__':
    main()
