"""Unified Puberty-Safe ingredient grader (one grader for every brand audit).

Copy this file into a brand folder (audits/<brand>/_grader.py) and run it there:

    python3 _grader.py

It reads <brand>_ingredients.json from its own folder (brand = folder name), looks up each
ingredient in ../../ref_compact.json and ../../ingredient_aliases.json, and writes
<brand>_audit.xlsx and _grade_summary.json into its own folder. Nothing else is written.

Grading rules come from /home/claude/GRADING_RUBRIC.txt and the practitioner decisions D1 to D6
(2026-10-16) recorded below. D7 and D8 (unknown-ingredient rules) were replaced 2026-10-17: unknown
ingredients add no flags and set no floor, except that Puberty Safe requires zero unknowns (such a product grades
Use Caution). Practitioner rule (2026-10-17): parabens and DMDM hydantoin grade Avoid (High Priority Swap), see
PARABEN_DMDM_RE and RETAILER_TEXT_OVERRIDES. The verbatim ingredient text in the JSON is never modified;
normalization is applied only in memory. The input JSON may use any of the three layouts the
brands were scraped into: {"products": [list]}, {"products": {name_or_slug: {...}}}, or a
top-level {name: {...}} mapping.
"""
import json
import os
import re

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.basename(HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
REF_PATH = os.path.join(ROOT, 'ref_compact.json')
ALIAS_PATH = os.path.join(ROOT, 'ingredient_aliases.json')
ING_PATH = os.path.join(HERE, f'{BRAND}_ingredients.json')
OUT_XLSX = os.path.join(HERE, f'{BRAND}_audit.xlsx')
OUT_SUMMARY = os.path.join(HERE, '_grade_summary.json')
CATALOG_PATH = os.path.join(HERE, f'{BRAND}_catalog.json')   # optional: brand product URL and brand category per product

TIERS = ['Puberty Safe', 'Use Caution', 'Avoid (Mild)', 'Avoid (Moderate)', 'Avoid (High Priority Swap)']
UNGRADABLE = 'ungradable'   # Not a tier. Used only for products with no ingredient text and the explicit exception list below.

HEADERS = ['product_name', 'product_url', 'brand_category', 'product_type', 'ingredients_verbatim', 'tier',
           'flag_count', 'flagged_ingredients', 'naturally_occurring_allergens', 'unknown_ingredients',
           'automatic_escalation', 'one_line_summary', 'audit_notes', 'audit_status']

# ------------------------------------------------------------------ reference
_ref = json.load(open(REF_PATH, encoding='utf-8'))
REF = _ref['ref']
ALIASES = dict(_ref.get('aliases', {}))
ALIASES.update(json.load(open(ALIAS_PATH, encoding='utf-8')))

# Scraper-side fixes only (addendum 2026-10-09 "parser artifacts" and typos seen in these two brands).
# These map a misspelled or variant name to the canonical name. They never add a reference entry.
TYPO_FIXES = {
    'aqua / water / eau': 'water', 'aqua/water/eau': 'water', 'water/aqua/eau': 'water',
    'water/aqua': 'water', 'aqua/eau': 'water',
    'phytosphyngosine': 'phytosphingosine', 'xantham gum': 'xanthan gum',
    '3-butanediol': '2,3-butanediol', 'beeswax (cera alba)': 'beeswax',
    'zinc oxide': 'zinc oxide (non-nano)',                 # addendum: bare zinc oxide in cream = non-nano
    'ceteary alcohol': 'cetearyl alcohol', 'soidum lactate': 'sodium lactate',
    '1,2-hexandiol': '1,2-hexanediol', '1-2-hexanediol': '1,2-hexanediol', '1,2 hexanediol': '1,2-hexanediol',
    'caprylic-capric-triglyceride': 'caprylic/capric triglyceride',
    'caprylic-capric triglyceride': 'caprylic/capric triglyceride',
    'pantalactone': 'pantolactone',
    'glyceryl glucosdie': 'glyceryl glucoside',
    'butyrospemum parkii (shea) butter': 'butyrospermum parkii (shea) butter',
    'helianthus annus (sunflower) seed oil': 'helianthus annuus (sunflower) seed oil',
    'sunflower seed oil': 'helianthus annuus (sunflower) seed oil',
    # D4 (practitioner, 2026-10-16): these name variants map to reference entries that are LOW TOX.
    'cocos nucifera (coconut) oil': 'coconut oil',
    'ceramide np': 'ceramide', 'ceramide ap': 'ceramide', 'ceramide ng': 'ceramide', 'ceramide 3': 'ceramide',
    # Change 1 (practitioner, 2026-10-17): White Petrolatum USP is a purified grade of petrolatum. It maps to the
    # reference entry 'petrolatum' (REF.txt line 789, category 1). Recorded here as a grader alias, not in the reference PDF text.
    'white petrolatum usp': 'petrolatum', 'white petrolatum (usp)': 'petrolatum', 'white petrolatum': 'petrolatum',
}
ALIASES.update(TYPO_FIXES)

# Reference index keyed by base name (parenthetical common names removed), e.g. "bht" -> "bht (butylated hydroxytoluene)".
BASE_INDEX = {}
for _k in REF:
    _b = re.sub(r'\s+', ' ', re.sub(r'\s*\([^)]*\)', '', _k)).strip()
    BASE_INDEX.setdefault(_b, _k)

# D4 (practitioner, 2026-10-16): no LOW TOX fallback list. An ingredient is LOW TOX only when the reference says so.
# Names not in the reference (botanical oils, lanolin alcohol, water, glycerin, etc.) log as unknown.

# Rubric exemptions: fatty alcohols are not drying alcohols (LOW TOX); behentrimonium methosulfate is LOW TOX.
FATTY_ALC = ['cetearyl alcohol', 'cetyl alcohol', 'stearyl alcohol', 'behenyl alcohol', 'brassica alcohol', 'c14-22 alcohols']

# D5 and D6 (practitioner, 2026-10-16): explicit exception table. These are grader rules, not reference edits.
#   'clear'   = D5: water is clear. No flag, no unknown, no tier effect.
#   'caution' = D6: glycerin is a caution ingredient. No flag, no unknown. If the product would otherwise grade
#               Puberty Safe it grades Use Caution; otherwise the other flags decide.
EXCEPTIONS = {'water': 'clear', 'aqua': 'clear', 'eau': 'clear', 'glycerin': 'caution'}
WATER_PARTS = {'water', 'aqua', 'eau'}

# Change 3 (practitioner, 2026-10-17): explicit exception list. These Eucerin products are Use Caution in the 2026-10-16
# grade and have audit_status "needs review" (source text unresolved). They move to ungradable. Flags, flagged
# ingredients and the unknown ingredient are kept as recorded; only the tier changes. Keyed by brand folder, then exact product name.
UNGRADABLE_EXCEPTIONS = {
    'eucerin': {
        'Q10 Revitalize Night Cream': 'source text unresolved',
        'Daily Hydration Lotion with Broad Spectrum SPF 15': 'source text unresolved',
        'Daily Hydration Lotion': 'source text unresolved',
        'Eucerin Baby Eczema Relief Hydrogel': 'source text unresolved',
        'Baby Lotion': 'source text unresolved',
    },
}

# Iron oxides (reference: categories 1, 2 and 3; PFAS treated). D2 (2026-10-16): heavy-metal escalation applies and the
# PFAS tag stands. The plain "iron oxides" entry is an alias of CI 77491/77492/77499 per its reference note, so it carries the same tag.
IRON_KEYS = {'ci 77491 (red iron oxide)', 'ci 77492 (yellow iron oxide)', 'ci 77499 (black iron oxide)', 'iron oxides'}
# D1 (practitioner, 2026-10-16): unspecified "silica" does not trigger the PFAS-treated escalation. The reference
# category flags [1, 2] still count; a product that would otherwise be Puberty Safe grades Use Caution.
SILICA_KEY = 'silica'
# D3 (practitioner, 2026-10-16): bisabolol is soft only when chamomile oil or chamomile extract is also listed.
CHAMOMILE = re.compile(r'chamomil|matricaria', re.I)

# Practitioner rule (2026-10-17), escalation like the PFAS and heavy-metal escalations: any paraben, or DMDM hydantoin,
# among the ingredients grades Avoid (High Priority Swap) whatever else the product contains. Matched on the cleaned
# ingredient names: any name containing "paraben", and DMDM hydantoin by name.
PARABEN_DMDM_RE = re.compile(r'paraben|dmdm\s*hydantoin', re.I)
PARABEN_ESC = 'paraben or DMDM hydantoin'
# Practitioner rule (2026-10-17), product-level source override. Keyed by brand folder, then exact product name, giving the
# json field whose ingredient text the paraben/DMDM rule also reads. Flags and the printed verbatim text are not changed by
# this; only the tier is set by the retailer listing, and the audit notes say so.
RETAILER_TEXT_OVERRIDES = {
    'eucerin': {'Q10 Revitalize Daily Cream': 'candidate_retailer_text'},
}

# Rubric: naturally occurring fragrance components (soft only when the source essential oil is also listed).
NAT_FRAG = {'linalool', 'limonene', 'citral', 'citronellal', 'geraniol', 'eugenol', 'isoeugenol', 'coumarin',
            'farnesol', 'hydroxycitronellal', 'benzyl alcohol', 'bisabolol'}

FRAG_NAMES = {'fragrance', 'parfum', 'natural fragrance', 'parfum/fragrance', 'perfume', 'fragrance (parfum)'}

FORMALDEHYDE = {'dmdm hydantoin', 'diazolidinyl urea', 'imidazolidinyl urea', 'quaternium-15', 'methenamine',
                'paraformaldehyde', 'benzylhemiformal', '5-bromo-5-nitro-1,3-dioxane', 'sodium hydroxymethylglycinate',
                'glyoxal', 'polyoxymethylene urea', '2-bromo-2-nitropropane-1,3-diol'}

# Watched naming patterns from the rubric (-nium, -eth, -paraben, -glycol, Fragrance/Parfum, -siloxane, -sulfate,
# formaldehyde-releaser names). Applied only after the reference lookup fails.
PATTERN_WATCH = [
    (re.compile(r'^peg[-\s]?\d', re.I), [1, 2, 4, 5], 'PEG-'),
    (re.compile(r'^ppg[-\s]?\d', re.I), [1, 2, 4, 5], 'PPG-'),
    (re.compile(r'(?:^|\s|-)(laureth|ceteth|oleth|steareth|trideceth|ceteareth|buteth|pareth|isoceteth)(?:-?\d|$)', re.I), [1, 4, 5], '-eth ethoxylate'),
    (re.compile(r'siloxane$|cyclopentasiloxane|cyclohexasiloxane|cyclotetrasiloxane|cyclomethicone', re.I), [1, 2, 6], 'siloxane'),
    (re.compile(r'(^|\s)dimethicone\b', re.I), [2, 6], 'silicone'),
    (re.compile(r'paraben$', re.I), [2, 4], 'paraben'),
    (re.compile(r'sulfate$', re.I), [1, 4, 5], 'sulfate'),
    (re.compile(r'phthalate', re.I), [2], 'phthalate'),
    (re.compile(r'glycol$', re.I), [1, 2], '-glycol'),
    (re.compile(r'^(?!.*ammonium).*nium\b|quaternium-\d', re.I), [2], '-nium quat'),
    (re.compile(r'\bphenoxyethanol\b', re.I), [1, 2, 4, 5, 8], 'phenoxyethanol'),
    (re.compile(r'^alcohol\s*denat', re.I), [4], 'alcohol denat'),
    (re.compile(r'^alcohol$', re.I), [4], 'alcohol'),
    (re.compile(r'^aluminum|^aluminium', re.I), [3], 'aluminum'),
    (re.compile(r'^mineral oil$|^petrolatum$|^petroleum$|^paraffin$', re.I), [1], 'petroleum'),
    (re.compile(r'^cocamidopropyl', re.I), [1, 4], 'cocamidopropyl'),
    # Change 2 (practitioner, 2026-10-17): any polysorbate is flagged. The nine numbers in REF.txt lines 885 to 910 resolve
    # through the reference entries first; this pattern catches any other polysorbate number.
    (re.compile(r'^polysorbate\b', re.I), [1, 2, 4, 5], 'polysorbate'),
]

# Ingredients whose flag depends on product form (rubric product-type conditionals).
CONDITIONAL_KEYS = {'ci 77891 (titanium dioxide)', 'zinc oxide (non-nano)', 'zeolite',
                    'acetic acid (vinegar)', 'amylase', 'cellulase'}

# Purpose labels the brand prints as part of the ingredient block.
PURPOSE_WORDS = {'sunscreen', 'skin protectant', 'skin protectant (ointment)', 'skin protectant ointment',
                 'anti-itch', 'anti-itch ointment', 'uv filter', 'treatment or prevention of diaper rash'}

# Brand-printed fragments that are not ingredients (seen in the Aquaphor Naturally Inspired block).
NOTE_FRAGMENTS = {'skin safe synthetic'}

# Two ingredients printed with a missing comma (the Aquaphor Healing Ointment .25oz audit note says so).
SPLIT_FIXES = {'panthenol glycerin': ['Panthenol', 'Glycerin']}

# A source essential oil (rubric: "lavender oil, citrus oil, rose oil"). Carrier oils do not count.
EO_SOURCE = re.compile(
    r'essential oil|\babsolute\b|\b(lavender|rose|citrus|orange|lemon|lime|peppermint|spearmint|mint|eucalyptus|tea tree|'
    r'melaleuca|chamomile|bergamot|sandalwood|ylang|jasmine|geranium|rosemary|cedar|cinnamon|clove|grapefruit|tangerine|'
    r'neroli|patchouli|vetiver|basil|lemongrass|cypress|pine|anise|cardamom|sage|marjoram|myrrh|frankincense|thyme)\b'
    r'.*\b(oil|absolute)\b', re.I)
FRAG_DISCLOSED = re.compile(r'essential oils?', re.I)

# ------------------------------------------------------------------ product type
RINSE_OFF_TYPES = {'rinse-off skincare', 'body wash/shampoo/conditioner'}


def is_leave_on(product_type):
    """Rubric: the leave-on tier thresholds apply. Only the rinse-off types are excluded; ambiguous types default to leave-on."""
    return product_type not in RINSE_OFF_TYPES


def is_spray(name, category):
    return bool(re.search(r'\bspray\b|aerosol|\bmist\b', f'{name} {category}', re.I))


def is_powder(name, category):
    return bool(re.search(r'\bpowder\b', f'{name} {category}', re.I))


def is_oral(name, category):
    return bool(re.search(r'toothpaste|mouthwash|oral care', f'{name} {category}', re.I))


# ------------------------------------------------------------------ normalization
def clean_segments(raw):
    """Split the verbatim text into ingredient names. Normalization is in memory only."""
    t = raw.replace('’', "'").replace(' ', ' ').replace('*', '')
    t = re.sub(r'\.{2,}', ', ', t)                                              # "41%...Purpose:" -> comma
    t = re.sub(r'\([^()]*purpose[^()]*\)', ', ', t, flags=re.I)                 # "(Purpose: Anti-Itch Ointment)"
    t = re.sub(r'(?i)\b(?:active|inactive|other)\s+ingredients?\s*:', ', ', t)  # section labels
    t = re.sub(r'(?i)\b(?:active|inactive)\s*:', ', ', t)
    t = re.sub(r'(?i)\bingredients?\s*:', ', ', t)
    t = re.sub(r'(?i)purpose\s*:[^,;]*?(?=\.\s|[,;]|$)', ', ', t)               # "Purpose: ..." fragments
    t = re.sub(r'\(\s*[^()]*%[^()]*\)', '', t)                                  # (41%), (3 %), (9%)
    t = re.sub(r'\(\s*[\d.\s]+\)', '', t)                                       # (3.5)
    t = re.sub(r'\s*\((?=[^()]*(?:skin protectant|analgesic|anti-itch|purpose|external))[^()]*\)', '', t, flags=re.I)
    t = re.sub(r'\s*\((?=[a-z])[^()]*\)', '', t)                                 # lowercase concentration/usage notes
    t = re.sub(r'\s*[\d.]+\s*%', '', t)                                         # 41%, 40.0%
    t = re.sub(r'\b(sodium|potassium|disodium|trisodium|ammonium|calcium|magnesium)(?=[a-z])', r'\1 ', t, flags=re.I)
    parts = re.split(r',(?!\d)|;(?!\d)|\.\s+|\n', t)                            # "1,2-Hexanediol" is not split
    out = []
    for p in parts:
        p = re.sub(r'\s+', ' ', p).strip(' .:,;-')
        p = re.sub(r'^[A-Za-z][A-Za-z ]{1,25}:\s*', '', p).strip(' .:,;-')      # "Synthetics: X" -> "X"
        if not p or p.lower() in PURPOSE_WORDS or p.lower() in NOTE_FRAGMENTS or re.fullmatch(r'[\d.\s-]+', p):
            continue
        out.extend(SPLIT_FIXES.get(p.lower(), [p]))
    return out


def norm_key(s):
    low = s.lower().strip()
    low = re.sub(r'\s*/\s*', '/', low)
    low = re.sub(r'\s+', ' ', low).strip(' .,;:-')
    return ALIASES.get(low, low) if low in TYPO_FIXES else low


def canonical_name(ing):
    """Display form of an unknown name: the scraper-side canonical spelling when one exists, otherwise the cleaned text."""
    low = ing.lower().strip()
    low = re.sub(r'\s*/\s*', '/', low)
    low = re.sub(r'\s+', ' ', low).strip(' .,;:-')
    return TYPO_FIXES.get(low, ing.strip(' .,;:-'))


def base_key(low):
    return re.sub(r'\s+', ' ', re.sub(r'\s*\([^)]*\)', '', low)).strip()


def resolve(low):
    """Reference key for a normalized name, or None. Tries the exact name, aliases, base-name index, and a salt-form fallback."""
    cands = [low, ALIASES.get(low, low)]
    b = base_key(low)
    cands += [b, ALIASES.get(b, b), BASE_INDEX.get(b, '')]
    salt = re.sub(r'\s+(hcl|hci)$', '', low)
    if salt != low:
        cands += [salt, base_key(salt), BASE_INDEX.get(base_key(salt), '')]
    for c in cands:
        if c and c in REF:
            return c
    return None


def has_eo_source(segments, exclude):
    return any(s != exclude and EO_SOURCE.search(s) for s in segments)


def exception_kind(low):
    """D5/D6 exception table lookup. Parentheticals are ignored: 'Water (Aqua)' and 'WATER (EAU)' are water."""
    base = re.sub(r'\s+', ' ', re.sub(r'\s*\([^)]*\)', '', low)).strip(' .,;:-')
    if base in EXCEPTIONS:
        return EXCEPTIONS[base]
    parts = [p.strip() for p in base.split('/')]
    if all(p in WATER_PARTS for p in parts):          # 'aqua/water/eau' and similar
        return 'clear'
    return None


# ------------------------------------------------------------------ lookup
def conditional_flag(key, name, category):
    """Rubric product-type conditionals. Returns (kind, cats, label) or None."""
    if key == 'ci 77891 (titanium dioxide)':
        if is_spray(name, category) or is_powder(name, category) or is_oral(name, category):
            return ('flag', [1, 2, 3], 'titanium dioxide in spray, powder or oral care')
        return ('ok', [], 'titanium dioxide in cream or lotion: not a concern (rubric)')
    if key == 'zinc oxide (non-nano)':
        if is_spray(name, category):
            return ('flag', [], 'zinc oxide in spray or aerosol: avoid (rubric; no category in reference)')
        return ('ok', [], 'zinc oxide in cream or lotion: low tox (rubric)')
    if key == 'zeolite':
        if is_powder(name, category):
            return ('flag', [], 'zeolite in powdered form (rubric)')
        return ('ok', [], 'zeolite not powdered: not a concern (rubric)')
    if key == 'acetic acid (vinegar)':
        if is_spray(name, category):
            return ('flag', [8], 'acetic acid with inhalation exposure (spray)')
        return ('ok', [], 'acetic acid without inhalation exposure (rubric)')
    if key in ('amylase', 'cellulase'):
        if is_powder(name, category):
            return ('flag', [8], 'enzyme in powdered product (rubric)')
        return ('ok', [], 'enzyme in liquid: lower concern (rubric)')
    return None


def lookup(ing, segments, name, category, product_type):
    """Classify one ingredient. kind: flag | soft | ok | unknown. Also returns pfas and formaldehyde markers."""
    low = norm_key(ing)
    out = {'pfas': False, 'formaldehyde': False}
    if not low:
        return dict(out, kind='ok', cats=[], label='empty')
    exc = exception_kind(low)
    if exc == 'clear':
        return dict(out, kind='ok', cats=[], label='D5: water is clear')
    if exc == 'caution':
        return dict(out, kind='caution', cats=[], label='D6: glycerin, caution ingredient')
    if low == 'behentrimonium methosulfate' or any(fa in low for fa in FATTY_ALC):
        return dict(out, kind='ok', cats=[], label='rubric exemption')

    # Fragrance / Parfum: a disclosed blend with the essential oils listed elsewhere is soft; otherwise full flag.
    if base_key(low) in FRAG_NAMES:
        if FRAG_DISCLOSED.search(ing) and has_eo_source(segments, ing):
            return dict(out, kind='soft', cats=[4, 8], label='fragrance blend, essential oils disclosed elsewhere')
        return dict(out, kind='flag', cats=[1, 2, 4, 8], label='fragrance without disclosure')

    # Naturally occurring fragrance components: soft only when the source essential oil is listed.
    if low in NAT_FRAG:
        key = resolve(low)
        cats = REF[key]['c'] if key and REF[key].get('c') else [4, 8]
        if low == 'bisabolol':   # D3: the source must be chamomile oil or chamomile extract
            source_listed = any(s != ing and CHAMOMILE.search(s) and re.search(r'\b(oil|extract)\b', s, re.I) for s in segments)
        else:
            source_listed = has_eo_source(segments, ing)
        if source_listed:
            return dict(out, kind='soft', cats=cats, label='natural component, source essential oil listed')
        if low == 'benzyl alcohol':
            return dict(out, kind='ok', cats=[], label='reference LOW TOX')
        return dict(out, kind='flag', cats=cats, label='natural component, no source essential oil listed: full flag')

    key = resolve(low)
    if key in CONDITIONAL_KEYS:
        c = conditional_flag(key, name, category)
        if c is not None:
            kind, cats, label = c
            pfas = kind == 'flag' and bool(re.search(r'PFAS treated', REF[key].get('n') or '', re.I))
            return dict(out, kind=kind, cats=cats, label=label, pfas=pfas)
    if key and REF[key].get('l') and not REF[key].get('c'):
        return dict(out, kind='ok', cats=[], label='reference LOW TOX')
    if key:
        d = REF[key]
        cats = d.get('c', [])
        if cats:
            pfas = bool(re.search(r'PFAS treated', d.get('n') or '', re.I))
            if key == SILICA_KEY:
                pfas = False        # D1: unspecified silica is not PFAS-escalated
            if key in IRON_KEYS:
                pfas = True         # iron oxides: PFAS tag applied as written in the reference
            form = key in FORMALDEHYDE
            return dict(out, kind='flag', cats=cats, label='reference', pfas=pfas, formaldehyde=form)
        return dict(out, kind='ok', cats=[], label='reference, no category')

    if low in FORMALDEHYDE:
        return dict(out, kind='flag', cats=[1, 2, 4, 5], label='formaldehyde-releaser (name)', formaldehyde=True)
    for pat, cats, label in PATTERN_WATCH:
        if pat.search(low):
            return dict(out, kind='flag', cats=cats, label='inferred: ' + label)
    return dict(out, kind='unknown', cats=[], label='')


# ------------------------------------------------------------------ grading
def paraben_dmdm_hits(segments):
    """Practitioner rule (2026-10-17): the ingredient names that trigger the paraben or DMDM hydantoin escalation."""
    return list(dict.fromkeys(s for s in segments if PARABEN_DMDM_RE.search(s)))


def grade(product_name, product_type, category, verbatim, retailer_text=None):
    segments = clean_segments(verbatim)
    flagged, natural, unknown = [], [], []
    esc = set()
    pfas_hit = False
    heavy_stack = False
    caution_hit = False      # D6: glycerin present (caution, not a flag)
    seen = set()
    for ing in segments:
        key = norm_key(ing)
        if key in seen:
            continue
        seen.add(key)
        r = lookup(ing, segments, product_name, category, product_type)
        if r['kind'] == 'flag':
            flagged.append({'name': ing, 'cats': r['cats'], 'label': r['label'], 'heavy_exempt': r.get('heavy_exempt', False)})
            pfas_hit = pfas_hit or r.get('pfas', False)
            if r.get('formaldehyde'):
                esc.add('formaldehyde-releaser')
        elif r['kind'] == 'soft':
            natural.append({'name': ing, 'cats': r['cats'], 'label': r['label']})
        elif r['kind'] == 'caution':
            caution_hit = True
        elif r['kind'] == 'unknown':
            unknown.append(canonical_name(ing))

    flag_count = len(flagged)
    max_cats = max([len(f['cats']) for f in flagged], default=0)
    has_paraben = any(re.search(r'paraben$', f['name'], re.I) for f in flagged)
    has_fragrance = any(f['label'].startswith('fragrance') for f in flagged)
    has_heavy = any(3 in f['cats'] and not f['heavy_exempt'] for f in flagged)   # D2: iron oxides (cat. 3) escalate
    has_form = 'formaldehyde-releaser' in esc
    has_sulfate = any(re.search(r'sulfate$', f['name'], re.I) for f in flagged)
    if has_heavy:
        esc.add('heavy metals')
    if pfas_hit:
        esc.add('PFAS')
    if is_leave_on(product_type) and any(1 in f['cats'] for f in flagged):
        esc.add('carcinogen in leave-on')

    # Heavy metal (cat. 3) stacked with a cat. 1 or cat. 2 flag from a different ingredient.
    for h in flagged:
        if 3 in h['cats'] and not h['heavy_exempt'] and any((o is not h) and (1 in o['cats'] or 2 in o['cats']) for o in flagged):
            heavy_stack = True

    order = TIERS
    if flag_count == 0:
        tier = 'Puberty Safe'
    elif flag_count <= 2 and max_cats < 3 and not has_paraben and not has_fragrance and not has_heavy and not has_form:
        tier = 'Use Caution'
    else:
        tier = 'Avoid (Mild)'
    if has_heavy or has_form or has_fragrance or flag_count >= 5:
        tier = max(tier, 'Avoid (Moderate)', key=order.index)
    notes = []
    if has_sulfate and product_type in RINSE_OFF_TYPES:
        tier = max(tier, 'Avoid (Mild)', key=order.index)
        notes.append('Sulfate-flagged ingredient in a daily rinse-off product: minimum Avoid (Mild) (rubric, shampoos).')
    if pfas_hit or flag_count >= 8 or 'carcinogen in leave-on' in esc or heavy_stack:
        tier = 'Avoid (High Priority Swap)'
    if heavy_stack:
        notes.append('Heavy metal stacked with a cat. 1 or cat. 2 flag: Avoid (High Priority Swap).')
    # Practitioner decisions D1 to D3, recorded per product.
    flagged_keys = {norm_key(f['name']) for f in flagged}
    silica_hit = bool(flagged_keys & {SILICA_KEY})
    if silica_hit:
        notes.append('D1: unspecified silica does not trigger the PFAS-treated escalation.')
    # D1 and D6: silica or glycerin means a Puberty Safe product grades Use Caution. Otherwise the other flags decide.
    if (silica_hit or caution_hit) and tier == 'Puberty Safe':
        tier = 'Use Caution'
    if caution_hit:
        notes.append('D6: glycerin is a caution ingredient (not a flag); it floors a Puberty Safe product at Use Caution.')
    # 2026-10-17 practitioner rule: unknown ingredients add no flags and set no floor and no ungradable tier. They stay
    # listed in unknown_ingredients. The one exception: Puberty Safe requires zero unknowns, so a product that would
    # otherwise grade Puberty Safe with any unknown grades Use Caution. No other tier is changed by unknowns.
    if unknown:
        notes.append(f'{len(unknown)} unknown ingredient(s) excluded from flags (2026-10-17).')
    if unknown and tier == 'Puberty Safe':
        tier = 'Use Caution'
        notes.append(f'Puberty Safe requires zero unknown ingredients: {len(unknown)} unknown ingredient(s) move this product to Use Caution (2026-10-17 practitioner rule).')
    if any(norm_key(f['name']) in IRON_KEYS for f in flagged):
        notes.append('Iron oxides (reference cat. 1, 2, 3): heavy-metal (cat. 3) escalation applies; PFAS-treated tag applied as written.')
    for f in flagged:
        if norm_key(f['name']) == 'bisabolol':
            notes.append('D3: bisabolol counted as a full flag (cat. 4); no chamomile oil or extract listed in this product.')
    for n in natural:
        if norm_key(n['name']) == 'bisabolol':
            notes.append('D3: bisabolol counted as a soft (naturally occurring) flag; chamomile oil or extract is listed.')

    # Practitioner rule (2026-10-17): paraben or DMDM hydantoin in the ingredient text forces Avoid (High Priority Swap).
    # The retailer text is read only for products named in RETAILER_TEXT_OVERRIDES.
    pd_printed = paraben_dmdm_hits(segments)
    pd_retail = paraben_dmdm_hits(clean_segments(retailer_text)) if retailer_text else []
    if pd_printed or pd_retail:
        esc.add(PARABEN_ESC)
        tier = 'Avoid (High Priority Swap)'
        if pd_printed:
            notes.append(f"Practitioner rule (2026-10-17): {', '.join(pd_printed)} in the printed ingredient text: Avoid (High Priority Swap).")
        if pd_retail:
            notes.append(f"Practitioner rule (2026-10-17): tier set from the retailer listing ({', '.join(pd_retail)}). The brand's printed text does not include them.")

    esc_list = [x for x in ['heavy metals', 'PFAS', 'formaldehyde-releaser', 'carcinogen in leave-on', PARABEN_ESC] if x in esc]
    return {'tier': tier, 'flagged': flagged, 'natural': natural, 'unknown': unknown, 'esc': esc_list,
            'segments': segments, 'rule_notes': notes}


def fmt_cats(cats):
    return ','.join(str(c) for c in cats)


def fmt_flags(items):
    out = []
    for f in items:
        s = f"{f['name']} [{fmt_cats(f['cats'])}]"
        if f['label'].startswith('inferred: '):
            s += f" (inferred: {f['label'][10:]})"
        elif f['label'] not in ('reference', 'reference, no category'):
            s += f" ({f['label']})"
        out.append(s)
    return ' / '.join(out)


def fmt_nat(items):
    return ' / '.join(f"{n['name']} [{fmt_cats(n['cats'])}]" for n in items)


# ------------------------------------------------------------------ input adapters
SITE_LIMITATION = ''


def load_products():
    global SITE_LIMITATION
    data = json.load(open(ING_PATH, encoding='utf-8'))
    if isinstance(data, list):
        rows = [dict(p) for p in data if isinstance(p, dict)]
    elif isinstance(data.get('products'), list):
        SITE_LIMITATION = data.get('site_limitation', '')
        rows = [dict(p) for p in data['products'] if isinstance(p, dict)]
    elif isinstance(data.get('products'), dict):
        SITE_LIMITATION = data.get('site_limitation', '')
        rows = [dict(p, product_name=p.get('product_name') or k)
                for k, p in data['products'].items() if isinstance(p, dict)]
    else:
        # Top-level {name: {...}} mapping. Skip the progress log and other non-product blocks.
        rows = [dict(p, product_name=p.get('product_name', k)) for k, p in data.items()
                if isinstance(p, dict) and 'ingredients_verbatim' in p]
    if os.path.exists(CATALOG_PATH):
        catalog = json.load(open(CATALOG_PATH, encoding='utf-8')).get('products', {})
        for row in rows:
            extra = catalog.get(row['product_name'], {})
            for field in ('product_url', 'brand_category'):
                if not row.get(field) and extra.get(field):
                    row[field] = extra[field]
    return rows


def product_url(p):
    if p.get('product_url'):
        return p['product_url']
    if p.get('url'):
        return p['url']
    m = re.search(r'https?://\S+', p.get('ingredient_source') or '')
    return m.group(0).rstrip(')') if m else ''


def brand_category(p):
    if p.get('brand_category'):
        return p['brand_category']
    n = re.sub(r'\(.*?\)', '', p.get('product_name', ''))
    return re.sub(r'^Aquaphor®?\s*', '', n).strip(' ,')


def main():
    products = load_products()
    text_map = {}
    for p in products:
        text_map.setdefault(p.get('ingredients_verbatim', ''), []).append(p.get('product_name', ''))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'audit'
    ws.append(HEADERS)
    tier_counts = {t: 0 for t in TIERS + [UNGRADABLE]}
    summary = []
    for p in products:
        name = p.get('product_name', '')
        ptype = p.get('product_type') or 'leave-on skincare'
        category = brand_category(p)
        verbatim = p.get('ingredients_verbatim', '') or ''
        url = product_url(p)
        status = 'needs review' if p.get('audit_status') == 'needs review' else 'complete'
        if not verbatim.strip():
            # No ingredient text means no tier. Partial flags are empty because there is nothing to flag.
            tier_counts[UNGRADABLE] += 1
            ws.append([name, url, category, ptype, '', UNGRADABLE, 0, '', '', '', '',
                       'Ungradable: no ingredient text on the source page, so no tier is assigned.',
                       ((p.get('audit_notes') or '') + ' No verbatim ingredient text in the json; not graded.').strip(),
                       'ingredients not found'])
            summary.append({'product_name': name, 'tier': UNGRADABLE, 'status': 'ingredients not found'})
            continue
        rt_field = RETAILER_TEXT_OVERRIDES.get(BRAND, {}).get(name)
        retailer_text = (p.get(rt_field) or '') if rt_field else ''
        g = grade(name, ptype, category, verbatim, retailer_text)
        tier = g['tier']
        rule_notes = g['rule_notes']
        exc_reason = UNGRADABLE_EXCEPTIONS.get(BRAND, {}).get(name)
        if exc_reason and tier != UNGRADABLE:
            # Change 3: explicit exception list (2026-10-17). Flags and unknowns are kept; only the tier changes.
            tier = UNGRADABLE
            note =f'Moved to ungradable: {exc_reason} (practitioner exception, 2026-10-17, change 3).'
            if g['unknown']:
                note += f" Unknown kept: {', '.join(g['unknown'])}."
            rule_notes.append(note)
        tier_counts[tier] += 1
        if tier == UNGRADABLE:
            status = 'needs review'
        flagged, natural, unknown = g['flagged'], g['natural'], g['unknown']
        esc_str = ', '.join(g['esc'])
        if tier == UNGRADABLE and exc_reason:
            summary_txt = (f"Ungradable: {exc_reason} (practitioner exception, 2026-10-17). "
                           f"Partial flags recorded: {len(flagged)}.")
        elif flagged:
            top = ', '.join(f['name'] for f in flagged[:3])
            summary_txt = f"{len(flagged)} flagged ingredient(s) in the printed list ({top}); tier applies to the printed subset only."
        else:
            summary_txt = 'No flagged ingredients in the printed list per reference and rubric conditionals.'
        if unknown and tier != UNGRADABLE:
            summary_txt += f" {len(unknown)} unknown ingredient(s) not in reference, excluded from grade."
        if esc_str:
            summary_txt += f" Escalation: {esc_str}."
        notes = []
        if p.get('listing_block'):
            notes.append(f"Printed block: {p['listing_block']}.")
        if SITE_LIMITATION:
            notes.append(f"Site limitation: {SITE_LIMITATION}")
        if p.get('audit_notes_retail'):
            notes.append(f"Retailer notes: {p['audit_notes_retail']}")
        if rt_field and retailer_text:
            notes.append(f"Paraben/DMDM rule source: {p.get('candidate_retailer_source') or 'retailer listing'} "
                         f"(practitioner directive 2026-10-17). The brand's own printed text is '{verbatim}' and does not "
                         f"include them; the variant match is not confirmed, so the tier rests on the retailer listing.")
        if p.get('audit_notes'):
            notes.append(f"Audit notes: {p['audit_notes']}")
        same = [x for x in text_map.get(verbatim, []) if x != name]
        if same:
            notes.append(f"Identical printed text on {len(same)} other product(s): {'; '.join(same[:4])}.")
        notes.extend(rule_notes)
        if p.get('ingredient_source'):
            notes.append(f"Ingredient source: {p['ingredient_source']}.")
        row = [name, url, category, ptype, verbatim, tier, len(flagged), fmt_flags(flagged), fmt_nat(natural),
               ('unknown — manual review needed: ' + ', '.join(unknown)) if unknown else '',
               esc_str, summary_txt, ' '.join(notes).strip(), status]
        ws.append(row)
        summary.append({'product_name': name, 'tier': tier, 'flag_count': len(flagged), 'product_type': ptype,
                        'flagged': [f['name'] for f in flagged], 'natural': [n['name'] for n in natural],
                        'unknown': unknown, 'esc': g['esc'], 'status': status})

    wb.save(OUT_XLSX)
    with open(OUT_SUMMARY, 'w', encoding='utf-8') as fh:
        json.dump({'brand': BRAND, 'tier_counts': tier_counts, 'rows': summary}, fh, indent=1, ensure_ascii=False)
    graded = sum(tier_counts[t] for t in TIERS)
    print(f'brand: {BRAND}  products: {len(products)}  graded: {graded}  ungradable: {tier_counts[UNGRADABLE]}')
    print('tiers:', tier_counts)


if __name__ == '__main__':
    main()
