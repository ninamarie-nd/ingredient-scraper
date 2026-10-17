"""Generic grader + report builder for the Puberty Scanner brand audit pipeline.

Usage: python3 grader.py <brand_slug> <brand_display_name> <brand_url>

Reads <brand_slug>_ingredients.json (dict of product_name -> {verbatim, url, type, category})
Produces: <brand_slug>_audit.xlsx, <brand_slug>_content_mining.md, <brand_slug>_audit_log.md
"""
import json, re, os, sys
from datetime import datetime
import openpyxl
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(HERE, 'ref_compact.json')

ref_data = json.load(open(REF_PATH))
REF = ref_data.get('ref', ref_data)
ALIASES = ref_data.get('aliases', {})
if not ALIASES:
    # fallback: load aliases.json
    aliases_path = os.path.join(HERE, 'ingredient_aliases.json')
    if os.path.exists(aliases_path):
        ALIASES = json.load(open(aliases_path))

NAT_FRAG = {'linalool','limonene','citral','citronellal','geraniol','eugenol','isoeugenol','coumarin','farnesol','hydroxycitronellal','bisabolol'}
EO_HINTS = ['oil','essential oil','extract','butter','juice','wax','absolute']
FORMALDEHYDE = {'dmdm hydantoin','diazolidinyl urea','diazolidinylurea','imidazolidinyl urea','imidazolidinylurea','quaternium-15','methenamine','paraformaldehyde','benzylhemiformal','5-bromo-5-nitro-1,3-dioxane','sodium hydroxymethylglycinate','glyoxal','polyoxymethylene urea','2-bromo-2-nitropropane-1,3-diol'}
FATTY_ALC_SUBSTR = ['cetearyl alcohol','cetyl alcohol','stearyl alcohol','behenyl alcohol','brassica alcohol','myristyl alcohol','lauryl alcohol','coconut alcohol','hexadecanol']

LOW_TOX = set([
'water','aqua','eau','aqua / water / eau','aqua/water/eau','water/aqua/eau','water/aqua','aqua/eau','glycerin','sodium chloride','citric acid','sodium citrate','sodium hyaluronate','niacinamide','hydrolyzed hyaluronic acid','phytosphingosine','xanthan gum','cholesterol','carbomer','potassium phosphate','dipotassium phosphate','sodium lauroyl lactylate','panthenol','allantoin','sodium hydroxide','potassium hydroxide','potassium sorbate','sodium benzoate','tocopherol','tocopheryl acetate','caprylic/capric triglyceride','caprylyl glycol','sodium pca','arginine pca','lactic acid','salicylic acid','ascorbic acid','retinol','kaolin','squalane','hydroxyethylcellulose','jojoba esters','sorbitol','urea','maltodextrin','dextran','biosaccharide gum-1','palmitic acid','stearic acid','myristic acid','lauric acid','glycine','threonine','arginine','serine','valine','proline','isoleucine','alanine','phenylalanine','histidine','aspartic acid','sodium lactate','glyceryl stearate','glyceryl stearate se','glyceryl oleate','glyceryl laurate','sorbitan isostearate','sorbitan tristearate','sorbitan oleate','sorbitan stearate','sorbitan palmitate','trisodium ethylenediamine disuccinate','tetrasodium glutamate diacetate','benzoic acid','hydroxyacetophenone','sodium polyacrylate','polyglyceryl-3 diisostearate','acrylates/c10-30 alkyl acrylate crosspolymer','octyldodecanol','isohexadecane','isopropyl myristate','isopropyl palmitate','ethylhexyl palmitate','cetyl palmitate','polysorbate 20','polysorbate 60','polysorbate 80','cetearyl isononanoate','cetearyl ethylhexanoate','isononyl isononanoate','isostearyl neopentanoate','dicaprylyl ether','hydrogenated vegetable oil','hydrogenated olive oil','hydrogenated castor oil','hydrogenated palm glycerides','ozokerite','pantolactone','pca','zinc citrate','zinc pca','copper pca','calcium gluconate','gluconolactone','gluconic acid','sodium carbonate','sodium phytate','phytic acid','disodium cocoyl glutamate','sodium cocoyl glutamate','potassium lactate','sodium methyl cocoyl taurate','coco-betaine','sodium cocoyl isethionate','sodium isethionate','sodium lauroyl sarcosinate','disodium cocoamphodiacetate','sodium borate','hectorite','chitosan','carrageenan','beta-glucan','lecithin','hydrogenated lecithin','polyacrylate crosspolymer-6','ammonium lactate','chlorhexidine digluconate','piroctone olamine','pramoxine hydrochloride','hydrocortisone','benzoyl peroxide','colloidal oatmeal','glycolic acid','acrylamide/sodium acryloyldimethyltaurate copolymer','ammonium polyacryloyldimethyl taurate','sodium acryloyldimethyltaurate/vp crosspolymer','hydrogenated jojoba oil','copernicia cerifera (carnauba) wax','dipotassium glycyrrhizate','palmitoyl tripeptide-1','palmitoyl tetrapeptide-7','caprooyl tetrapeptide-3','tripeptide-1','copper tripeptide-34','caprooyl phytosphingosine','caprooyl sphingosine','ascorbyl palmitate','sucrose','sucrose laurate','sucrose stearate','sucrose palmitate','behenic acid','sodium hyaluronate crosspolymer','potassium cetyl phosphate','methyl glucose sesquistearate','methylpropanediol','cholecalciferol','saccharide isomerate','jojoba beads','caprooyl glycine','caproyl glycine','capryloyl glycine','cellulose','rice bran wax','tetrahexyldecyl ascorbate','trideceth-6','glyceryl isostearate','polyhydroxystearic acid','potassium cocoate','hydroxypropyl guar','trisodium citrate','betaine','polyglyceryl-4 isostearate','polyglyceryl-3 beeswax','polyglyceryl-3 stearate','polyglyceryl-4 caprate','pentaerythrityl distearate','sodium gluconate','sorbic acid','sodium cumenesulfonate','trisodium dicarboxymethyl alaninate','copper','polyepsilon-lysine','sodium cocoyl alaninate','disodium laurimidodiproprionate','sodium acrylates/beheneth-25 methacrylate crosspolymer','triethyl citrate','ethoxydiglycol','c12-13 alkyl lactate','c15-19 alkane','hexyl laurate','c12-15 alkyl benzoate','c12-20 alkyl glucoside','octyl/decyl glucoside','polyurethane-62','polyglyceryl-6 esters','sodium cocoate','sodium palmate','sodium olivoyl glutamate','capryloyl glycerin/sebacic acid copolymer','sodium iminodisuccinate','pentylene glycol','caprylhydroxamic acid','malic acid','dicaprylyl carbonate','panthenyl hydroxypropyl steardimonium chloride','polyglyceryl-6 stearate','polyglyceryl-6 behenate','polyglyceryl-6 caprylate','polyglyceryl-6 ricinoleate','polyglyceryl-6 oleate','polyglyceryl-3 cocoate','polyglyceryl-3 polyricinoleate','sodium lauryl sulfoacetate','sodium methyl oleoyl taurate','xylitylglucoside','anhydroxylitol','xylitol','menthyl lactate','charcoal powder','microcrystalline cellulose','lithium magnesium sodium silicate','hydroxypropyl starch phosphate','adenosine','ubiquinone','sandalore','hydroxyapatite','sodium metabisulfite','zinc chloride','pyridoxine hcl','folic acid','calcium pantothenate','sodium ascorbyl phosphate','hydroxypropyl guar hydroxypropyltrimonium chloride','polyglutamic acid','hyaluronic acid','ethyl macadamiate','sodium starch octenylsuccinate','pullulan','sodium polyitaconate','euphorbia cerifera (candelilla) wax','stearyl behenate','sodium formate','sodium glycolate','sodium levulinate','levulinic acid','fumaric acid','isopropyl alcohol','benzotriazolyl dodecyl p-cresol','sodium cocoyl methyl isethionate','capryloyl/caproyl methyl glucamide','lauroyl/myristoyl methyl glucamide','distarch phosphate','polyquaternium-37','polyquaternium-10','polyquaternium-7','polyquaternium-71','fructose','2,3-butanediol','trimethylbenzenepropanol','polyglyceryl-4 laurate','titanium dioxide (ci 77891)','algin','mineral salts','volcanic ash','curcumin','methyl diisopropyl propionamide','sclerotium gum','beta-carotene ci 40800','caprylic acid','sodium lauroyl methyl isethionate','cetyl esters','cetyl hydroxyethylcellulose','decyl glucoside','caprylyl/capryl glucoside','sodium bicarbonate','acacia senegal gum','camellia sinensis leaf extract','simmondsia chinensis seed oil','butyrospermum parkii (shea) butter','cocos nucifera (coconut) oil','ricinus communis (castor) seed oil','persea gratissima (avocado) oil','olea europaea (olive) fruit oil','argania spinosa kernel oil','prunus amygdalus dulcis (sweet almond) oil','aloe barbadensis leaf juice','avena sativa (oat) kernel flour','p-anisic acid','propanediol','ethyl macadamiate','mica','zinc stearate','magnesium stearate','pyrus malus (apple) fruit extract'
])
# Removed from LOW_TOX (now graded via reference database):
#   'pentylene glycol' — reference database lists it as cat-1 (carcinogen /
#   developmental concern) and cat-2 (endocrine disruptor). Previously it
#   was being skipped as "low-tox", which overrode the reference flag.
LOW_TOX.discard('pentylene glycol')

PATTERN_WATCH = [
    # Catches: PEG-X, PPG-X, PEG-X-Y, PEG X, PEG/PPG-X/Y (combined ethoxylate form).
    # Previously only matched "peg-" or "ppg-" + digit, so combined "PEG/PPG-8/3 LAURATE"
    # (and all siblings) fell through unflagged.
    (re.compile(r'^(peg|ppg)[-\s/]', re.I), [1,2,4,5], 'PEG/PPG ethoxylate'),
    # Titanium Dioxide: inhalation risk only — handled via product-type gating in grade().
    # Phenoxyethanol: fixed to drop cat-8 (does NOT release formaldehyde — chemical error).
    (re.compile(r'\bphenoxyethanol\b', re.I), [1,2,4,5], 'phenoxyethanol'),
    (re.compile(r'(?:^|\s|-)(laureth|ceteth|oleth|steareth|trideceth|ceteareth|buteth|pareth|isoceteth)(?:-?\d|$)', re.I), [1,4,5], '-eth ethoxylate'),
    (re.compile(r'siloxane$|cyclopentasiloxane|cyclohexasiloxane|cyclotetrasiloxane|cyclomethicone', re.I), [1,2,6], 'siloxane'),
    # Dimethicone: silicone polymer. Flagged for environmental persistence ONLY.
    # Dropped the endocrine [2] flag (no evidence) and the "silicone" label (which
    # was triggering the PFAS escalation incorrectly — dimethicone is not PFAS).
    (re.compile(r'(^|\s)dimethicone\b', re.I), [6], 'dimethicone persistence'),
    (re.compile(r'dimethiconol', re.I), [6], 'dimethicone persistence'),
    (re.compile(r'\bparaben\b', re.I), [2,4], 'paraben'),
    (re.compile(r'sulfate$', re.I), [1,4,5], 'sulfate'),
    (re.compile(r'^sodium c14-16 olefin sulfonate$', re.I), [4], 'sodium C14-16 olefin sulfonate'),
    (re.compile(r'phthalate', re.I), [2], 'phthalate'),
    (re.compile(r'\bbenzophenone\b', re.I), [3], 'benzophenone'),
    (re.compile(r'^propylene glycol$|^butylene glycol$|^hexylene glycol$|^ethylene glycol$|^dipropylene glycol$', re.I), [1,2], '-glycol'),
    (re.compile(r'monium chloride$|^behenalkonium|^stearalkonium|^cetrimonium|^cetyl pyridinium|^guar hydroxypropyltrimonium|hydroxypropyltrimonium chloride$|dicetyldimonium chloride$|^behentrimonium chloride', re.I), [2], '-nium quat'),
    # (Phenoxyethanol pattern moved up and corrected — dropped cat-8 formaldehyde-releaser flag.)
    (re.compile(r'\bbht\b|butylated hydroxytoluene', re.I), [1,2], 'BHT'),
    (re.compile(r'\bbha\b|butylated hydroxyanisole', re.I), [1,2], 'BHA'),
    (re.compile(r'^tetrasodium edta$', re.I), [1], 'tetrasodium EDTA'),
    (re.compile(r'^disodium edta$', re.I), [4], 'disodium EDTA'),
    (re.compile(r'^ethylhexylglycerin$', re.I), [4,5], 'ethylhexylglycerin'),
    (re.compile(r'^chlorphenesin$', re.I), [4], 'chlorphenesin'),
    (re.compile(r'^methylparaben$|^propylparaben$|^butylparaben$|^ethylparaben$|^isobutylparaben$', re.I), [2,4], 'paraben'),
    (re.compile(r'^triethanolamine', re.I), [1,4], 'TEA'),
    (re.compile(r'^ethanolamine$', re.I), [4], 'ethanolamine'),
    (re.compile(r'^mineral oil$|paraffinum liquidum|^petrolatum$|^petroleum$|^paraffin$', re.I), [1], 'petroleum'),
    (re.compile(r'^cocamidopropyl', re.I), [1,4], 'cocamidopropyl'),
    (re.compile(r'^lauramidopropyl', re.I), [1,4], 'lauramidopropyl'),
    (re.compile(r'^silica$', re.I), [1,2], 'silica'),
    (re.compile(r'^polyethylene$', re.I), [6], 'polyethylene'),
    (re.compile(r'^alcohol\s*denat', re.I), [4], 'alcohol denat'),
    (re.compile(r'^alcohol$', re.I), [4], 'alcohol'),
    (re.compile(r'^aluminum|^aluminium', re.I), [3], 'aluminum'),
    (re.compile(r'^iron oxides?\b', re.I), [1,2,3], 'iron oxides CI#'),
    (re.compile(r'^ci 77', re.I), [1,2,3], 'colorant CI#'),
    (re.compile(r'^isododecane', re.I), [1,2], 'isododecane'),
    (re.compile(r'^vp/va copolymer', re.I), [1,4,6], 'VP/VA copolymer'),
    (re.compile(r'^glycol distearate', re.I), [4], '-glycol'),
    (re.compile(r'^sulfosuccinate$', re.I), [5], 'sulfosuccinate'),
    (re.compile(r'^polysilicone-', re.I), [2,6], 'silicone'),
    (re.compile(r'^trisiloxane$|silsesquioxane', re.I), [2,6], 'siloxane'),
    (re.compile(r'^talc\b', re.I), [1,3], 'talc'),
    (re.compile(r'^oxybenzone|^octinoxate|^octocrylene|^homosalate|^avobenzone', re.I), [2], 'chemical sunscreen'),
    (re.compile(r'^retinyl palmitate|^retinyl acetate', re.I), [1,2], 'retinyl ester'),
    (re.compile(r'^resorcinol', re.I), [1,2,4], 'resorcinol'),
    (re.compile(r'^toluene', re.I), [1,2,4,7], 'toluene'),
    (re.compile(r'^formaldehyde', re.I), [1,4,8], 'formaldehyde'),
    (re.compile(r'^coal tar|^fd&c|^d&c', re.I), [1,2,3], 'synthetic dye'),
    (re.compile(r'^diethanolamine|^dea\b|^cocamide dea|^lauramide dea', re.I), [1,2,4], 'DEA'),
    (re.compile(r'^monoethanolamine|^mea\b|^cocamide mea|^lauramide mea', re.I), [4], 'MEA'),
    (re.compile(r'^trisodium nitrilotriacetate', re.I), [1], 'nitrilo-'),
    (re.compile(r'^poly c10-30', re.I), [6], 'acrylate microplastic'),
    (re.compile(r'^ethylene/acrylic acid copolymer', re.I), [6], 'acrylate microplastic'),
    (re.compile(r'^sodium dodecylbenzenesulfonate', re.I), [1], 'alkylbenzenesulfonate'),
    (re.compile(r'^diethylhexyl syringylidenemalonate', re.I), [2], 'sunscreen booster'),
    (re.compile(r'^1,2-hexanediol$', re.I), [1,2], '-glycol'),
    (re.compile(r'^1,3-butylene glycol$', re.I), [1,2], '-glycol'),
    (re.compile(r'^hexylene glycol$', re.I), [1,2], '-glycol'),
    (re.compile(r'^lauryl pyrrolidone$', re.I), [4], 'lauryl pyrrolidone'),
    (re.compile(r'^sodium benzotriazolyl butylphenol sulfonate$', re.I), [1,2], 'polymeric UV absorber'),
    (re.compile(r'^dmdm hydantoin|^diazolidinyl urea|^imidazolidinyl urea|^quaternium-15', re.I), [1,2,4,5], 'formaldehyde releaser'),
    (re.compile(r'^methylisothiazolinone|^methylchloroisothiazolinone', re.I), [4,7], 'isothiazolinone'),
]

def norm(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.replace('*','').strip()
    return s.strip(' .,;:')

def is_fatty_alc(low):
    return any(fa in low for fa in FATTY_ALC_SUBSTR)

def is_natural_frag(low, verbatim_lower):
    if low in NAT_FRAG:
        if any(h in verbatim_lower for h in EO_HINTS):
            return low
    return None

def split_ingredients(text):
    t = text
    t = re.sub(r'(?i)active ingredient[s]?\s*:\s*', '', t)
    t = re.sub(r'(?i)inactive ingredient[s]?\s*:\s*', ',', t)
    t = re.sub(r'(?i)^ingredients:\s*', '', t.strip())
    t = re.sub(r'(?i)^ingredients?\b\s*', '', t.strip())
    t = re.sub(r'\b[A-Z][a-zA-Z0-9+\- ]+:\s*', ', ', t)
    t = re.sub(r'\(code [^)]+\)', '', t, flags=re.I)
    # Protect commas that live INSIDE a chemical name like "1,2-hexanediol"
    # or "1,3-butylene glycol" — splitting on them would turn one
    # ingredient into two unidentifiable fragments ("1" + "2-hexanediol").
    # Temporarily swap digit-digit commas for a sentinel, split, then restore.
    SENTINEL = '\x00'
    t = re.sub(r'(?<=\d),(?=\d)', SENTINEL, t)
    parts = re.split(r'[,;]|\.\s+', t)
    parts = [p.replace(SENTINEL, ',') for p in parts]
    out = []
    for p in parts:
        p = p.strip(' .;,:')
        p = re.sub(r'\s*\d+(\.\d+)?\s*%\s*$', '', p)
        p = re.sub(r'^\s*\d+(\.\d+)?\s*%\s*', '', p)
        p = re.sub(r'\([^)]*\d+(\.\d+)?\s*%[^)]*\)', '', p)
        if not p: continue
        low = p.lower()
        if low in ('ingredients','inactive ingredients','active ingredient','active ingredients','inactive','active'): continue
        if 'may contain' in low: continue
        out.append(p)
    return out

def is_inhalation_risk(name, product_type):
    """True when a product is likely to be inhaled or lofted: loose powders,
    sprays, mists, aerosols. Silica/talc/mica/titanium dioxide/iron oxides
    are only flagged in these — in a cream, balm, or lotion they don't
    reach the lungs and are considered safe for topical use."""
    n = (name or '').lower()
    pt = (product_type or '').lower()
    if 'powder' in pt or 'spray' in pt or 'aerosol' in pt or 'mist' in pt:
        return True
    if any(w in n for w in [' spray', ' mist', ' aerosol', 'dry shampoo',
                              'loose powder', 'setting powder', 'bronzer powder',
                              'blush powder', 'foundation powder', 'baby powder',
                              'talcum powder', 'body powder', 'face powder']):
        return True
    return False

def infer_product_type(name, hint=None):
    if hint: return hint
    n = name.lower()
    if 'shampoo' in n or 'cleanser' in n or 'cleansing bar' in n or 'body wash' in n or 'wash' in n or 'bubble bath' in n:
        return 'body wash/shampoo/conditioner'
    if 'conditioner' in n or 'mask' in n:
        if 'leave-in' in n or 'leave in' in n:
            return 'hair styling'
        return 'body wash/shampoo/conditioner'
    if 'lotion' in n or 'cream' in n or 'moisturizer' in n or 'moisturiser' in n or 'balm' in n:
        return 'leave-on skincare'
    if 'serum' in n or 'oil' in n or 'treatment' in n or 'spray' in n or 'leave-in' in n or 'leave in' in n or 'gel' in n or 'foam' in n or 'stick' in n or 'mist' in n:
        return 'hair styling'
    if 'deodorant' in n or 'antiperspirant' in n:
        return 'leave-on skincare'
    if 'toothpaste' in n or 'mouthwash' in n:
        return 'oral care'
    if 'sunscreen' in n or 'spf' in n:
        return 'leave-on skincare'
    if 'powder' in n:
        return 'powder'
    return 'leave-on skincare'

def grade(product_name, product_type, verbatim):
    ingredients = split_ingredients(verbatim)
    verbatim_lower = verbatim.lower()
    flagged = []; natural = []; unknown = []; escalations = set()
    seen = set()
    for ing in ingredients:
        low = norm(ing)
        if not low or low in seen: continue
        seen.add(low)
        if 'behentrimonium methosulfate' in low: continue
        if is_fatty_alc(low): continue
        nf = is_natural_frag(low, verbatim_lower)
        if nf:
            natural.append((ing, [4,8]))
            continue
        if low in LOW_TOX: continue
        if low.startswith('ceramide '): continue
        if ' leaf extract' in low or ' flower extract' in low or ' fruit extract' in low or ' root extract' in low or ' seed extract' in low or ' bark extract' in low or ' peel extract' in low or ' stem extract' in low:
            continue
        if 'ferment' in low or 'extract' in low or low.endswith(' oil') or 'butter' in low or 'juice' in low or low.endswith(' wax') or low.endswith(' bran') or ' seed oil' in low or ' root oil' in low or ' peel oil' in low or low.endswith(' water'):
            continue
        if low.endswith(' acid') and not any(b in low for b in ['acrylic acid','sulfonic acid']):
            continue
        key = ALIASES.get(low, low)
        if key in REF:
            d = REF[key]
            if d.get('l'):
                continue
            # Conditional flags: honored only when the product type matches
            # the condition. "inhalation_risk" means powder/spray/aerosol —
            # silica/talc/mica/TiO2/iron-oxides are safe in creams and balms.
            cond = d.get('cond', '')
            if cond == 'inhalation_risk' and not is_inhalation_risk(product_name, product_type):
                continue
            cats = d.get('c', [])
            if cats:
                flagged.append((ing, cats))
                if key in FORMALDEHYDE or low in FORMALDEHYDE:
                    escalations.add('formaldehyde-releaser')
                if 3 in cats:
                    escalations.add('heavy metals')
                note = (d.get('n') or '').lower()
                # PFAS escalation: only fire when the ingredient's note
                # EXPLICITLY calls out PFAS treatment AND the product is
                # one where PFAS treatment is a real concern (leave-on,
                # powders, waterproof formulas). Was previously firing on
                # any ingredient with "PFAS" in the note (e.g., dimethicone),
                # which was over-flagging because the note was "PFAS treated
                # [sometimes]" rather than "contains PFAS".
                if 'pfas' in note and (
                    key in ('silica silylate', 'trimethylsiloxysilicate',
                            'perfluorooctyl triethoxysilane')
                    or 'perfluoro' in low):
                    escalations.add('PFAS')
                if 1 in cats and product_type == 'leave-on skincare':
                    escalations.add('carcinogen in leave-on')
            continue
        matched = False
        for pat, cats, label in PATTERN_WATCH:
            if pat.search(low):
                if cats:
                    flagged.append((ing + f' [inferred: {label}]', cats))
                    if 3 in cats:
                        escalations.add('heavy metals')
                    # Narrowed: only cyclic siloxanes (D4/D5/D6 EU-restricted
                    # for bioaccumulation) trigger PFAS. Dimethicone label
                    # changed to "dimethicone persistence" so it won't match.
                    if 'siloxane' in label.lower() and 'dimethicone' not in label.lower():
                        escalations.add('PFAS')
                    if 'formaldehyde' in label.lower():
                        escalations.add('formaldehyde-releaser')
                    if 1 in cats and product_type == 'leave-on skincare':
                        escalations.add('carcinogen in leave-on')
                matched = True
                break
        if matched: continue
        # Fragrance: catch any ingredient containing the word fragrance/parfum/perfume
        # (as a whole word) — matches "Natural Fragrance", "Fragrance Oil(s)",
        # "Synthetic Fragrance", "Parfum/Fragrance", "Fragrance (Parfum)*",
        # "Natural Fragrance Oils", "Fragrance Blend", etc.
        # Also catches EU-labeled "Aroma" (same meaning as fragrance in INCI).
        # Specific disclosed aromatic compounds (linalool, limonene, geraniol,
        # citral, named plant oils) don't contain these words so they don't match.
        if re.search(r'\b(fragrance|parfum|perfume|aroma)\b', low):
            flagged.append((ing, [1,2,4,8])); continue
        if low in FORMALDEHYDE:
            flagged.append((ing, [1,2,4,5])); escalations.add('formaldehyde-releaser'); continue
        unknown.append(ing)
    uq = []; sn = set()
    for n,c in flagged:
        k = n.lower()
        if k in sn: continue
        sn.add(k); uq.append((n,c))
    flagged = uq
    flag_count = len(flagged)
    has_paraben = any('paraben' in n.lower() for n,_ in flagged)
    # Match any fragrance variant: trailing *, **, dagger, parentheticals, "Fragrance (Parfum)*", etc.
    # Strip common footnote markers and trailing punctuation before matching.
    def _is_fragrance_name(n):
        low = n.lower().strip()
        # Strip trailing footnote markers and punctuation
        low = re.sub(r'[\*†‡¤\.\s]+$', '', low).strip()
        # Match any ingredient containing fragrance/parfum/perfume/aroma as a word.
        # Mirrors the detection logic above so the tier escalation stays consistent.
        return bool(re.search(r'\b(fragrance|parfum|perfume|aroma)\b', low))
    has_fragrance = any(_is_fragrance_name(n) for n,_ in flagged)
    has_heavy = 'heavy metals' in escalations or any(3 in c for _,c in flagged)
    has_carc_lo = 'carcinogen in leave-on' in escalations
    has_pfas = 'PFAS' in escalations
    has_form = 'formaldehyde-releaser' in escalations
    has_cat2 = any(2 in c for _,c in flagged)
    max_cats = max([len(c) for _,c in flagged], default=0)
    tier = 'Puberty Safe'
    if flag_count == 0:
        tier = 'Puberty Safe'
    elif flag_count <= 2 and not has_paraben and not has_fragrance and not has_heavy and not has_form:
        tier = 'Use Caution'
    elif flag_count >= 3 or max_cats >= 3 or has_paraben:
        tier = 'Avoid (Mild)'
    order = ['Puberty Safe','Use Caution','Avoid (Mild)','Avoid (Moderate)','Avoid (High Priority Swap)']
    if has_heavy or has_form or has_fragrance or flag_count >= 5:
        if order.index(tier) < order.index('Avoid (Moderate)'):
            tier = 'Avoid (Moderate)'
    # Endocrine disruption escalation. Triggered when either:
    #   (a) A high-priority endocrine disruptor is present by name
    #       (parabens, phthalates, triclosan/triclocarban, oxybenzone / BP-3,
    #        octinoxate / OMC, octocrylene, resorcinol, BHA, aluminum salts), OR
    #   (b) >=3 distinct ingredients carry a cat-2 (endocrine) flag.
    # Fragrance alone is not enough — it is already a Moderate-tier trigger on its own.
    HIGH_ENDOCRINE_HINTS = [
        'paraben','phthalate','triclosan','triclocarban',
        'oxybenzone','benzophenone-3','bp-3','bp3',
        'octinoxate','ethylhexyl methoxycinnamate','octyl methoxycinnamate',
        'octocrylene','homosalate','resorcinol','bha ',' bha,',' bha.',
        'butylated hydroxyanisole',
        'aluminum chloro','aluminum zirconium','aluminum chlorohydrate',
        'aluminum sesquichlorohydrate','aluminium chloro','aluminium zirconium',
    ]
    def _has_high_endocrine(name):
        low = name.lower()
        for h in HIGH_ENDOCRINE_HINTS:
            if h in low:
                return True
        return False
    high_endo_hits = [n for n,_ in flagged if _has_high_endocrine(n)]
    cat2_hits = [n for n,c in flagged if 2 in c and not _is_fragrance_name(n)]
    has_endocrine = bool(high_endo_hits) or len(cat2_hits) >= 3

    if has_pfas or flag_count >= 8 or has_carc_lo or (has_heavy and has_cat2 and has_fragrance):
        tier = 'Avoid (High Priority Swap)'
    # Multi-marker endocrine disruption on its own is enough to escalate to HPS
    if has_endocrine and (len(cat2_hits) >= 3 or len(high_endo_hits) >= 2):
        tier = 'Avoid (High Priority Swap)'

    esc = []
    if has_pfas: esc.append('PFAS')
    if has_heavy: esc.append('heavy metals')
    if has_form: esc.append('formaldehyde-releaser')
    if has_carc_lo: esc.append('carcinogen in leave-on')
    if has_endocrine: esc.append('endocrine disruption')
    return tier, flag_count, flagged, natural, unknown, esc


def build_outputs(brand_slug, brand_name, brand_url, ingredients, out_dir, scrape_notes=None):
    """ingredients: dict product_name -> {verbatim, url, type?, category?, status?}"""
    os.makedirs(out_dir, exist_ok=True)
    xlsx_path = os.path.join(out_dir, f'{brand_slug}_audit.xlsx')
    cm_path = os.path.join(out_dir, f'{brand_slug}_content_mining.md')
    log_path = os.path.join(out_dir, f'{brand_slug}_audit_log.md')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'{brand_name[:28]} Audit'
    headers = ["product_name","product_url","brand_category","product_type","ingredients_verbatim","tier","flag_count","flagged_ingredients","naturally_occurring_allergens","unknown_ingredients","automatic_escalation","one_line_summary","audit_notes","audit_status"]
    ws.append(headers)

    tier_count = Counter()
    flag_counter = Counter()
    cat_counter = Counter()
    product_rows = []
    graded_count = 0
    skipped_count = 0
    unknown_queue = Counter()

    for name, data in ingredients.items():
        verbatim = data.get('verbatim') or ''
        url = data.get('url') or ''
        bcat = data.get('category') or 'General'
        ptype = infer_product_type(name, data.get('type'))
        notes = data.get('notes') or ''
        status_hint = data.get('status') or ''

        if not verbatim or status_hint == 'ingredients not found':
            row = [name, url, bcat, ptype, verbatim, '', 0, '', '', '', '', '', notes or 'No INCI list published on product page.', 'ingredients not found']
            ws.append(row); product_rows.append({'name': name, 'tier': None, 'flag_count': 0, 'flagged': [], 'category': bcat, 'url': url})
            skipped_count += 1
            continue

        tier, flag_count, flagged, natural, unknown, esc = grade(name, ptype, verbatim)
        tier_count[tier] += 1
        graded_count += 1

        for n, c in flagged:
            fkey = re.sub(r'\s*\[inferred:[^\]]+\]', '', n).strip().lower()
            flag_counter[fkey] += 1
            for cat in c:
                cat_counter[cat] += 1
        for u in unknown:
            unknown_queue[u.lower()] += 1

        flag_str = ' / '.join(f"{n} [{','.join(str(x) for x in c)}]" for n,c in flagged)
        nat_str = ' / '.join(f"{n} [{','.join(str(x) for x in c)}]" for n,c in natural)
        unk_str = ', '.join(unknown)
        esc_str = ', '.join(esc)
        if flag_count == 0:
            summary = "No flagged ingredients present per reference."
        else:
            top = [n.split(' [inferred')[0] for n,_ in flagged[:3]]
            summary = f"{flag_count} flagged ingredient(s) incl. {', '.join(top)}."
            if esc: summary += f" Escalation: {esc_str}."
        row = [name, url, bcat, ptype, verbatim, tier, flag_count, flag_str, nat_str, unk_str, esc_str, summary, notes, 'complete']
        ws.append(row)
        product_rows.append({'name': name, 'tier': tier, 'flag_count': flag_count, 'flagged': flagged, 'escalations': esc, 'category': bcat, 'url': url})

    wb.save(xlsx_path)

    # Content mining markdown
    total = len(ingredients)
    def pct(n):
        return f"{(n*100)/graded_count:.0f}%" if graded_count else "0%"

    cat_name = {1:'Carcinogen',2:'Endocrine Disruption',3:'Heavy Metals',4:'Allergies/Irritation',5:'Microbiome-Busting',6:'Microplastics',7:'Acutely Toxic',8:'Respiratory Irritant'}

    graded_rows = [r for r in product_rows if r['tier'] is not None]
    graded_rows_sorted = sorted(graded_rows, key=lambda r: -r['flag_count'])
    most_flagged = graded_rows_sorted[0] if graded_rows_sorted else None
    cleanest = None
    for r in sorted(graded_rows, key=lambda x: x['flag_count']):
        if r['tier'] == 'Puberty Safe':
            cleanest = r; break
    if not cleanest and graded_rows_sorted:
        cleanest = graded_rows_sorted[-1]

    top_flag = flag_counter.most_common(1)
    top_cat = cat_counter.most_common(1)

    # Groupings for comparison section
    by_cat = {}
    for r in graded_rows:
        by_cat.setdefault(r['category'], []).append(r)

    today = datetime.utcnow().strftime('%Y-%m-%d')
    cm_lines = []
    cm_lines.append(f"# {brand_name} Audit — Content Mining Report")
    cm_lines.append('')
    cm_lines.append(f"**Date audited:** {today}")
    cm_lines.append(f"**Products audited:** {total} enumerated; {graded_count} graded ({skipped_count} without published INCI)")
    cm_lines.append(f"**Source:** {brand_url}")
    cm_lines.append('')
    cm_lines.append('---')
    cm_lines.append('')
    cm_lines.append('## Section A — Brand-level callout')
    cm_lines.append('')

    if graded_count:
        safe = tier_count.get('Puberty Safe', 0)
        cm_lines.append(f"**Headline finding:** Of {graded_count} {brand_name} products graded, {safe} are Puberty Safe ({pct(safe)}); " + \
            (f"the single largest tier is {tier_count.most_common(1)[0][0]} ({tier_count.most_common(1)[0][1]} products, {pct(tier_count.most_common(1)[0][1])})." if tier_count else "no graded tier distribution available."))
    else:
        cm_lines.append(f"**Headline finding:** Of {total} {brand_name} products enumerated, 0 could be graded because INCI lists are not published on the brand site.")
    cm_lines.append('')
    cm_lines.append('**Tier distribution:**')
    for t in ['Puberty Safe','Use Caution','Avoid (Mild)','Avoid (Moderate)','Avoid (High Priority Swap)']:
        n = tier_count.get(t, 0)
        cm_lines.append(f"- {t}: {n} ({pct(n)})")
    if skipped_count:
        cm_lines.append(f"- **Not gradable (no INCI published): {skipped_count} ({(skipped_count*100)/total:.0f}% of catalog)**")
    cm_lines.append('')

    if most_flagged and most_flagged['flag_count'] > 0:
        top_names = [n.split(' [inferred')[0] for n,_ in most_flagged['flagged'][:5]]
        cm_lines.append(f"**Single most-flagged product:** {most_flagged['name']} — {most_flagged['flag_count']} flags. Stacks {', '.join(top_names)}" + (f" plus {most_flagged['flag_count']-5} more." if most_flagged['flag_count']>5 else "."))
    else:
        cm_lines.append("**Single most-flagged product:** N/A — no graded products carried flags.")
    cm_lines.append('')
    if cleanest and cleanest['tier'] == 'Puberty Safe':
        cm_lines.append(f"**Cleanest product (if any):** {cleanest['name']} — Puberty Safe (0 flags).")
    elif cleanest:
        cm_lines.append(f"**Cleanest product (if any):** {cleanest['name']} — {cleanest['tier']}, {cleanest['flag_count']} flag(s).")
    else:
        cm_lines.append("**Cleanest product (if any):** N/A.")
    cm_lines.append('')
    cm_lines.append('**Content angle for Section A:**')
    if graded_count:
        safe_pct = f"{(safe*100)/graded_count:.0f}%"
        cm_lines.append(f"\"I scanned every {brand_name} product on their site — {safe} out of {graded_count} are Puberty Safe\" is the one-line hook. The brand positions itself around its marketing promise; the data shows the gap between that promise and the formulations.")
    else:
        cm_lines.append(f"{brand_name}'s on-site transparency is the story: with 0 of {total} products publishing a full INCI list on the brand's own website, the consumer can't check the formula from the product page.")
    cm_lines.append('')
    cm_lines.append('---')
    cm_lines.append('')

    cm_lines.append('## Section B — Pattern callouts')
    cm_lines.append('')
    if top_flag and graded_count:
        n, c = top_flag[0]
        cm_lines.append(f"**Most common flagged ingredient:** {n.title()} — appears in {c} of {graded_count} graded products ({(c*100)/graded_count:.0f}%).")
    else:
        cm_lines.append("**Most common flagged ingredient:** N/A.")
    cm_lines.append('')
    if top_cat and graded_count:
        c_id, c_n = top_cat[0]
        cm_lines.append(f"**Most common risk category:** Category {c_id} ({cat_name.get(c_id,'')}) — flagged {c_n} times across the audit.")
    else:
        cm_lines.append("**Most common risk category:** N/A.")
    cm_lines.append('')
    cm_lines.append('**"Clean marketing, dirty formula" finds:**')
    marketing_cues = ['natural', 'gentle', 'baby', 'sensitive', 'pure', 'clean', 'free', 'organic', 'plant', 'botanical', 'mild']
    cm_calls = []
    for r in graded_rows_sorted[:10]:
        n = r['name'].lower()
        if r['flag_count'] >= 3 and any(cue in n for cue in marketing_cues):
            tops = [x.split(' [inferred')[0] for x,_ in r['flagged'][:3]]
            cm_calls.append(f"- {r['name']} ({r['tier']}, {r['flag_count']} flags) — marketed as 'clean/gentle/natural'; still carries {', '.join(tops)}.")
    if not cm_calls:
        cm_calls.append("- No standout 'clean marketing, dirty formula' examples surfaced from the graded set. See `_audit.xlsx` for per-product detail.")
    cm_lines.extend(cm_calls[:5])
    cm_lines.append('')
    cm_lines.append('**Repeated flagged ingredients (top 8):**')
    for fname, fc in flag_counter.most_common(8):
        cm_lines.append(f"- {fname.title()} — {fc} of {graded_count} products ({(fc*100)/graded_count:.0f}%)" if graded_count else f"- {fname.title()} — {fc}")
    cm_lines.append('')
    cm_lines.append('**Content angles for Section B:**')
    if top_flag and graded_count:
        n, c = top_flag[0]
        pct_n = f"{(c*100)/graded_count:.0f}%"
        cm_lines.append(f"- \"{brand_name} uses {n.title()} in {c} of {graded_count} products I scanned — that's {pct_n} of the graded catalog.\"")
    cm_lines.append(f"- \"The tier distribution across {brand_name} is {tier_count.get('Puberty Safe',0)} Puberty Safe / {tier_count.get('Use Caution',0)} Use Caution / {tier_count.get('Avoid (Mild)',0)} Avoid Mild / {tier_count.get('Avoid (Moderate)',0)} Avoid Moderate / {tier_count.get('Avoid (High Priority Swap)',0)} Avoid HPS. The shape of that distribution is the story.\"")
    cm_lines.append('')
    cm_lines.append('---')
    cm_lines.append('')
    cm_lines.append('## Section C — Comparison angles')
    cm_lines.append('')
    cm_lines.append('**Best vs worst within categories:**')
    for cat_name_g, rs in sorted(by_cat.items()):
        if len(rs) < 2: continue
        srs = sorted(rs, key=lambda r: r['flag_count'])
        best = srs[0]; worst = srs[-1]
        cm_lines.append(f"- {cat_name_g}: Best = {best['name']} ({best['tier']}, {best['flag_count']} flags). Worst = {worst['name']} ({worst['tier']}, {worst['flag_count']} flags).")
    cm_lines.append('')
    cm_lines.append('**Cleanest in each category:**')
    for cat_name_g, rs in sorted(by_cat.items()):
        srs = sorted(rs, key=lambda r: r['flag_count'])
        best = srs[0]
        cm_lines.append(f"- {cat_name_g}: {best['name']} ({best['tier']}, {best['flag_count']} flags)")
    cm_lines.append('')
    cm_lines.append('**Content angles for Section C:**')
    cm_lines.append(f"- \"Same brand, same shelf, different story on the back.\" Within {brand_name}, categories vary widely in flag count — see per-category best/worst above for one-to-one comparisons.")
    cm_lines.append('')
    cm_lines.append('---')
    cm_lines.append('')
    cm_lines.append('## Raw data summary')
    cm_lines.append('')
    cm_lines.append('**Unknown ingredients (manual review queue):**')
    if unknown_queue:
        for u, _c in unknown_queue.most_common(15):
            cm_lines.append(f"- {u} (×{_c})")
    else:
        cm_lines.append('- None — all ingredients resolved against the reference.')
    cm_lines.append('')
    with open(cm_path, 'w') as f:
        f.write('\n'.join(cm_lines) + '\n')

    # Audit log
    log_lines = []
    log_lines.append(f"# {brand_name} Audit Log")
    log_lines.append('')
    log_lines.append(f"**Brand URL:** {brand_url}")
    log_lines.append(f"**Audit date:** {today}")
    log_lines.append(f"**Products enumerated:** {total}")
    log_lines.append(f"**Products graded:** {graded_count}")
    log_lines.append(f"**Products without published INCI:** {skipped_count}")
    log_lines.append('')
    log_lines.append('## Status')
    log_lines.append('')
    if graded_count == 0:
        log_lines.append('Complete. All enumerated SKUs retrieved. 0 of {} graded — brand site does not publish full INCI lists on product pages (same pattern as Carol\'s Daughter).'.format(total))
    else:
        log_lines.append(f'Complete. {graded_count} of {total} products successfully graded against the reference.')
    log_lines.append('')
    log_lines.append('## Scraping method')
    log_lines.append('')
    if scrape_notes:
        log_lines.append(scrape_notes)
    else:
        log_lines.append('See per-product URLs in the spreadsheet. Enumeration + ingredient extraction via built-in browser pane.')
    log_lines.append('')
    log_lines.append('## Tier roll-up')
    log_lines.append('')
    for t in ['Puberty Safe','Use Caution','Avoid (Mild)','Avoid (Moderate)','Avoid (High Priority Swap)']:
        log_lines.append(f"- {t}: {tier_count.get(t, 0)}")
    if skipped_count:
        log_lines.append(f"- Ingredients not published: {skipped_count}")
    log_lines.append(f"- **Total:** {total}")
    log_lines.append('')
    log_lines.append('## Per-product status')
    log_lines.append('')
    for r in product_rows:
        if r['tier'] is None:
            log_lines.append(f"- {r['name']}: ingredients not found on page")
        else:
            log_lines.append(f"- {r['name']}: {r['tier']}, {r['flag_count']} flag(s)")
    log_lines.append('')
    log_lines.append('## Manual review queue')
    log_lines.append('')
    if unknown_queue:
        for u, _c in unknown_queue.most_common(25):
            log_lines.append(f"- {u} (×{_c})")
    else:
        log_lines.append('Empty — all ingredients resolved cleanly.')
    log_lines.append('')
    log_lines.append('## Anomalies / Notes')
    log_lines.append('')
    log_lines.append('- Browser choice: unattended scheduled run; the Claude in Chrome connector requires per-session browser selection, so the built-in Claude Browser pane was used instead (same as the SheaMoisture 2026-10-12 and Carol\'s Daughter 2026-10-14 audits).')
    if unknown_queue:
        log_lines.append(f'- {len(unknown_queue)} ingredient(s) landed in the manual review queue — see list above. Pattern matcher caught most of the obvious cases; everything else is a candidate for the next reference addendum.')
    with open(log_path, 'w') as f:
        f.write('\n'.join(log_lines) + '\n')

    return {
        'xlsx': xlsx_path,
        'content_mining': cm_path,
        'audit_log': log_path,
        'tier_count': dict(tier_count),
        'graded': graded_count,
        'skipped': skipped_count,
        'top_flag': top_flag[0] if top_flag else None,
        'most_flagged': most_flagged,
        'cleanest': cleanest,
    }


if __name__ == '__main__':
    brand_slug = sys.argv[1]
    brand_name = sys.argv[2]
    brand_url = sys.argv[3]
    ing_json_path = sys.argv[4]
    out_dir = sys.argv[5]
    scrape_notes_path = sys.argv[6] if len(sys.argv) > 6 else None
    scrape_notes = None
    if scrape_notes_path and os.path.exists(scrape_notes_path):
        scrape_notes = open(scrape_notes_path).read()
    ingredients = json.load(open(ing_json_path))
    res = build_outputs(brand_slug, brand_name, brand_url, ingredients, out_dir, scrape_notes)
    print(json.dumps({'xlsx': res['xlsx'], 'tier_count': res['tier_count'], 'graded': res['graded'], 'skipped': res['skipped'], 'top_flag': res['top_flag']}, indent=2))
