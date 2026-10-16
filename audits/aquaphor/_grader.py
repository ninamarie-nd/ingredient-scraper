import json, re, openpyxl, shutil, os

REF_PATH = '/home/claude/ingredient-scraper/ref_compact.json'
ING_PATH = '/home/claude/ingredient-scraper/audits/aquaphor/aquaphor_ingredients.json'
OUT_XLSX = '/home/claude/ingredient-scraper/audits/aquaphor/aquaphor_audit.xlsx'

ref_data = json.load(open(REF_PATH))
REF = ref_data['ref']
ALIASES = ref_data['aliases']
ING = json.load(open(ING_PATH))

NAT_FRAG = {'linalool','limonene','citral','citronellal','geraniol','eugenol','isoeugenol','coumarin','farnesol','hydroxycitronellal','bisabolol'}
EO_HINTS = ['oil','essential oil','extract','butter','juice','wax','absolute']
FORMALDEHYDE = {'dmdm hydantoin','diazolidinyl urea','diazolidinylurea','imidazolidinyl urea','imidazolidinylurea','quaternium-15','methenamine','paraformaldehyde','benzylhemiformal','5-bromo-5-nitro-1,3-dioxane','sodium hydroxymethylglycinate','glyoxal','polyoxymethylene urea','2-bromo-2-nitropropane-1,3-diol'}
FATTY_ALC_SUBSTR = ['cetearyl alcohol','cetyl alcohol','stearyl alcohol','behenyl alcohol','brassica alcohol','myristyl alcohol','lauryl alcohol','coconut alcohol','hexadecanol']

LOW_TOX = set([
'water','aqua','eau','aqua / water / eau','aqua/water/eau','water/aqua/eau','water/aqua','aqua/eau','glycerin','sodium chloride','citric acid','sodium citrate','sodium hyaluronate','niacinamide','hydrolyzed hyaluronic acid','phytosphingosine','xanthan gum','cholesterol','ceramide np','ceramide ap','ceramide eop','ceramide ns','ceramide eos','ceramide ng','ceramide as','carbomer','potassium phosphate','dipotassium phosphate','sodium lauroyl lactylate','panthenol','allantoin','sodium hydroxide','potassium hydroxide','potassium sorbate','sodium benzoate','tocopherol','tocopheryl acetate','caprylic/capric triglyceride','caprylyl glycol','sodium pca','arginine pca','lactic acid','salicylic acid','ascorbic acid','retinol','kaolin','squalane','hydroxyethylcellulose','jojoba esters','sorbitol','urea','maltodextrin','dextran','biosaccharide gum-1','palmitic acid','stearic acid','myristic acid','lauric acid','glycine','threonine','arginine','serine','valine','proline','isoleucine','alanine','phenylalanine','histidine','aspartic acid','sodium lactate','glyceryl stearate','glyceryl stearate se','glyceryl oleate','glyceryl laurate','sorbitan isostearate','sorbitan tristearate','sorbitan oleate','trisodium ethylenediamine disuccinate','tetrasodium glutamate diacetate','benzoic acid','hydroxyacetophenone','sodium polyacrylate','polyglyceryl-3 diisostearate','acrylates/c10-30 alkyl acrylate crosspolymer','octyldodecanol','isohexadecane','isopropyl myristate','isopropyl palmitate','ethylhexyl palmitate','cetyl palmitate','polysorbate 20','polysorbate 60','polysorbate 80','cetearyl isononanoate','cetearyl ethylhexanoate','isononyl isononanoate','isostearyl neopentanoate','dicaprylyl ether','hydrogenated vegetable oil','hydrogenated olive oil','hydrogenated castor oil','hydrogenated palm glycerides','ozokerite','pantolactone','pca','zinc citrate','zinc pca','copper pca','calcium gluconate','gluconolactone','gluconic acid','sodium carbonate','sodium phytate','phytic acid','disodium cocoyl glutamate','sodium cocoyl glutamate','potassium lactate','sodium methyl cocoyl taurate','coco-betaine','sodium cocoyl isethionate','sodium isethionate','sodium lauroyl sarcosinate','disodium cocoamphodiacetate','sodium borate','hectorite','chitosan','carrageenan','beta-glucan','lecithin','hydrogenated lecithin','polyacrylate crosspolymer-6','ammonium lactate','chlorhexidine digluconate','piroctone olamine','pramoxine hydrochloride','hydrocortisone','benzoyl peroxide','colloidal oatmeal','glycolic acid','acrylamide/sodium acryloyldimethyltaurate copolymer','ammonium polyacryloyldimethyl taurate','sodium acryloyldimethyltaurate/vp crosspolymer','hydrogenated jojoba oil','copernicia cerifera (carnauba) wax','copernicia cerifera cera / carnauba wax / cire de carnauba','dipotassium glycyrrhizate','palmitoyl tripeptide-1','palmitoyl tetrapeptide-7','caprooyl tetrapeptide-3','tripeptide-1','copper tripeptide-34','caprooyl phytosphingosine','caprooyl sphingosine','ascorbyl palmitate','sucrose','sucrose laurate','sucrose stearate','sucrose palmitate','behenic acid','sodium hyaluronate crosspolymer','potassium cetyl phosphate','methyl glucose sesquistearate','methylpropanediol','cholecalciferol','saccharide isomerate','jojoba beads','caprooyl glycine','caproyl glycine','capryloyl glycine','cellulose','rice bran wax','tetrahexyldecyl ascorbate','trideceth-6','glyceryl isostearate','ethylhexyl methoxycrylene','triethoxycaprylylsilane','polyhydroxystearic acid','methyl methacrylate crosspolymer','potassium cocoate','hydroxypropyl guar','trisodium citrate','betaine','polyglyceryl-4 isostearate','polyglyceryl-3 beeswax','polyglyceryl-3 stearate','polyglyceryl-4 caprate','sorbitan palmitate','pentaerythrityl distearate','sodium gluconate','sorbic acid','sodium cumenesulfonate','trisodium dicarboxymethyl alaninate','copper','pentaerythrityl tetra-di-t-butyl hydroxyhydrocinnamate','polyepsilon-lysine','sodium cocoyl alaninate','disodium laurimidodiproprionate','sodium acrylates/beheneth-25 methacrylate crosspolymer','triethyl citrate','ethoxydiglycol','c12-13 alkyl lactate','c15-19 alkane','hexyl laurate','c12-15 alkyl benzoate','c12-20 alkyl glucoside','methyl di-t-butyl hydroxyhydrocinnamate','octyl/decyl glucoside','polyurethane-62','cera / carnauba wax / cire de carnauba','polyglyceryl-6 esters','sodium cocoate','sodium palmate','sodium olivoyl glutamate','capryloyl glycerin/sebacic acid copolymer','sodium iminodisuccinate','pentylene glycol','caprylhydroxamic acid','malic acid','dicaprylyl carbonate','panthenyl hydroxypropyl steardimonium chloride','polyglyceryl-6 stearate','polyglyceryl-6 behenate','polyglyceryl-6 caprylate','polyglyceryl-6 ricinoleate','polyglyceryl-6 oleate','polyglyceryl-3 cocoate','polyglyceryl-3 polyricinoleate','sodium lauryl sulfoacetate','sodium methyl oleoyl taurate','xylitylglucoside','anhydroxylitol','xylitol','menthyl lactate','charcoal powder','microcrystalline cellulose','lithium magnesium sodium silicate','hydroxypropyl starch phosphate','adenosine','ubiquinone','sandalore','hydroxyapatite','sodium metabisulfite','zinc chloride','pyridoxine hcl','folic acid','calcium pantothenate','sodium ascorbyl phosphate','hydroxypropyl guar hydroxypropyltrimonium chloride','polyglutamic acid','hyaluronic acid','ethyl macadamiate','rose flower oil','rose extract','sodium starch octenylsuccinate','pullulan','sodium polyitaconate','euphorbia cerifera (candelilla) wax','stearyl behenate','sodium formate','sodium glycolate','sodium levulinate','levulinic acid','fumaric acid','isopropyl alcohol','benzotriazolyl dodecyl p-cresol','sodium cocoyl methyl isethionate','capryloyl/caproyl methyl glucamide','lauroyl/myristoyl methyl glucamide','saccharomyces/rice ferment filtrate','hydrolyzed rice protein','rice bran oil/hydrogenated rice bran oil esters','selaginella lepidophylla extract','lactobacillus ferment','oryza sativa (rice) bran water','hydrogenated castor oil/sebacic acid copolymer','phospholipids','glycolipids','distarch phosphate','quercetin','polyquaternium-37','polyquaternium-10','polyquaternium-7','polyquaternium-71','hydrolyzed vegetable protein pg-propyl silanetriol','hydrogenated ethylhexyl olivate','hydrogenated olive oil unsaponifiables','fructose','2,3-butanediol','trimethylbenzenepropanol','polyglyceryl-4 laurate','titanium dioxide (ci 77891)','acyl coenzyme a desaturase','algin','mineral salts','volcanic ash','curcumin','spirulina maxima extract','methyl diisopropyl propionamide','sclerotium gum','sodium benzotriazolyl butylphenol sulfonate','beta-carotene ci 40800','chlorophyllin-copper complex (ci 75810)','caprylic acid','camellia oleifera seed oil','tribehenin','lauryl laurate','hydrolyzed jojoba esters','oleic/linoleic/linolenic polyglycerides','hydroxystearic/linolenic/oleic polyglycerides','orbignya speciosa kernel oil','astrocaryum murumuru seed butter','salvia hispanica seed oil','salvia hispanica seed extract','linum usitatissimum (linseed) seed extract','citrus junos peel extract','rhus verniciflua peel wax','shorea robusta resin','olea europaea (olive) oil unsaponifiables','hippophae rhamnoides fruit oil','hippophae rhamnoides oil','acacia senegal gum','lamium album extract','plantago psyllium seed extract','phyllanthus emblica fruit extract','larix europaea wood extract','lindera strychnifolia root extract','lithospermum erythrorhizon root extract','castor oil/ipdi copolymer','camellia sinensis leaf extract','panax ginseng root extract','simmondsia chinensis seed oil','glycine soja (soybean) oil','glycine soja (soybean) sterols','helianthus annuus hybrid oil','helianthus annuus (sunflower) seed oil','helianthus annuus (sunflower) seed oil/helianthus annuus seed oil','helianthus annuus (sunflower) extract','helianthus annuus (sunflower) seed wax','ricinus communis (castor) seed oil','rose canina fruit oil','rosa canina fruit oil','rosa canina (rosehip) fruit oil','rosa canina seed oil','argania spinosa kernel oil','cocos nucifera (coconut) oil','cocos nucifera (coconut) fruit extract','cocos nucifera (coconut) seed butter','butyrospermum parkii (shea) butter','persea gratissima (avocado) oil','prunus amygdalus dulcis (sweet almond) oil','vitis vinifera (grape) seed oil','olea europaea (olive) fruit oil','rosmarinus officinalis (rosemary) leaf oil','rosmarinus officinalis (rosemary) leaf extract','melaleuca alternifolia (tea tree) leaf oil','mentha piperita (peppermint) oil','mentha viridis (spearmint) leaf oil','zingiber officinale (ginger) root oil','zingiber officinale (ginger) root extract','santalum album (sandalwood) oil','amyris balsamifera bark oil','pogostemon cablin oil','elettaria cardamomum seed oil','ferula galbaniflua (galbanum) resin oil','adansonia digitata seed oil','abies sibirica oil','abies sibirica oi','citrus aurantium dulcis (orange) peel oil','citrus paradisi (grapefruit) peel oil','citrus limon (lemon) peel oil','citrus tangerina (tangerine) peel oil','citrus aurantium dulcis (orange) fruit extract','citrus grandis (grapefruit) fruit extract','citrus limon (lemon) fruit extract','hamamelis virginiana (witch hazel) water','hamamelis virginiana (witch hazel) leaf extract','daucus carota sativa (carrot) root extract','daucus carota sativa (carrot) seed oil','lycium barbarum fruit extract','mangifera indica (mango) juice','mangifera indica (mango) fruit extract','prunus cerasus (bitter cherry) fruit extract','papain','actinidia chinensis (kiwi) fruit extract','spinacia oleracea (spinach) leaf extract','brassica oleracea italica (broccoli) extract','brassica oleracea acephala leaf extract','pyrus malus (apple) fruit extract','cucumis sativus (cucumber) fruit extract','beta vulgaris (beet) root extract','cymbopogon schoenanthus extract','chlorella vulgaris extract','sambucus nigra flower extract','vaccinium angustifolium (blueberry) fruit extract','rubus villosus (blackberry) fruit extract','euterpe oleracea fruit extract','passiflora edulis fruit extract','passiflora edulis seed oil','ribes nigrum (black currant) seed oil','fragaria ananassa (strawberry) seed oil','prunus domestica seed oil','musa sapientum (banana) peel extract','ananas sativus (pineapple) fruit extract','carica papaya (papaya) fruit extract','curcuma longa (turmeric) root extract','ocimum basilicum (basil) flower/leaf extract','ocimum basilicum (basil) leaf extract','melia azadirachta flower extract','melia azadirachta leaf extract','ocimum sanctum leaf extract','aloe barbadensis leaf juice','aloe barbadensis flower extract','punica granatum bark extract','corallina officinalis extract','lactobacillus','averrhoa carambola fruit extract','glyceryl caprylate','polyglyceryl-6 oleate','sodium surfactin','avena sativa (oat) bran extract','avena sativa (oat) bran','avena sativa (oat) kernel flour','avena sativa (oat) kernel extract','simmondsia chinensis (jojoba) seed oil','plantago lanceolata leaf extract','laminaria saccharina extract','sargassum filipendula extract','sargassum filipendula (sargassum) extract','palmaria palmata extract','saccharina longicruris extract','trametes versicolor extract','algae extract','laurus nobilis leaf extract','calendula officinalis flower extract','hydrolyzed corn protein','hydrolyzed wheat protein','hydrolyzed soy protein','hydrolyzed keratin','keratin amino acids','biotin','hydrolyzed quinoa','rice amino acids','oryza sativa (rice) extract','oryza sativa (rice) bran extract','oryza sativa (rice) bran oil','oryza sativa (rice) starch','zea mays (corn) starch','tapioca starch','sodium bicarbonate','bambusa arundinacea stem extract','bambusa arundinacea leaf extract','bambusa vulgaris extract','chamomilla recutita (matricaria) flower extract','sorbitan oleate decylglucoside crosspolymer','hibiscus sabdariffa flower extract','acanthus mollis leaf extract','coccinia indica fruit extract','solanum melongena (eggplant) fruit extract','theobroma cacao (cocoa) seed butter','disodium laureth sulfosuccinate','propylene glycol dicaprylate/dicaprate','ppg-1 trideceth-6','1,2-hexanediol','potassium phosphate','montmorillonite','coffea arabica (coffee) seed oil','coffea arabica seed oil','coco-caprylate/caprate','polyporus umbellatus (mushroom) extract','moringa oleifera (moringa) seed oil','ethylhexyl olivate','aspergillus ferment','gluconolactone','heptyl glucoside','tilia tomentosa extract','laureth-2','laureth-9','undaria pinnatifida extract','macadamia ternifolia seed oil','melia azadirachta (neem) leaf extract','eclipta prostrata extract','sodium methyl isethionate','hydrolyzed gardenia florida extract','caprylyl/capryl glucoside','caramel','p-anisic acid','p anisic acid','pentylene glycol','propanediol'
])

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
    (re.compile(r'^sodium c14-16 olefin sulfonate$', re.I), [4], 'sodium C14-16 olefin sulfonate'),
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
    # Section labels like "Shampoo:", "Mask:", "Moisture Treatment:", "Protein Treatment:"
    t = re.sub(r'\b[A-Z][a-zA-Z0-9+\- ]+:\s*', ', ', t)
    t = re.sub(r'\(code [^)]+\)', '', t, flags=re.I)
    parts = re.split(r'[,;]|\.\s+', t)
    out = []
    for p in parts:
        p = p.strip(' .;,:')
        p = re.sub(r'\s*\d+(\.\d+)?\s*%\s*$', '', p)
        p = re.sub(r'^\s*\d+(\.\d+)?\s*%\s*', '', p)
        if not p: continue
        low = p.lower()
        if low in ('ingredients','inactive ingredients','active ingredient','active ingredients','inactive','active'): continue
        out.append(p)
    return out

def infer_product_type(name):
    n = name.lower()
    if 'shampoo' in n or 'cleanser' in n or 'cleansing bar' in n or 'body wash' in n or 'wash' in n:
        return 'body wash/shampoo/conditioner'
    if 'conditioner' in n or 'mask' in n or 'conditioning mask' in n:
        if 'leave-in' in n or 'leave in' in n:
            return 'hair styling'
        return 'body wash/shampoo/conditioner'
    if 'serum' in n or 'oil' in n or 'treatment' in n or 'spray' in n or 'leave-in' in n or 'leave in' in n:
        return 'hair styling'
    if 'gel' in n or 'cream' in n or 'foam' in n or 'stick' in n or 'puff' in n or 'mist' in n:
        return 'hair styling'
    return 'hair styling'

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
        if 'ferment' in low or 'extract' in low or low.endswith(' oil') or 'butter' in low or 'juice' in low or low.endswith(' wax') or low.endswith(' bran') or ' seed oil' in low or ' root oil' in low or ' peel oil' in low or low.endswith(' water'):
            continue
        if low.endswith(' acid') and not any(b in low for b in ['acrylic acid','sulfonic acid']):
            continue
        key = ALIASES.get(low, low)
        if key in REF:
            d = REF[key]
            if d.get('l'):
                continue
            cats = d.get('c', [])
            if cats:
                flagged.append((ing, cats))
                if key in FORMALDEHYDE or low in FORMALDEHYDE:
                    escalations.add('formaldehyde-releaser')
                if 3 in cats:
                    escalations.add('heavy metals')
                note = (d.get('n') or '').lower()
                if 'pfas' in note:
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
                    if 'silicone' in label.lower() or 'siloxane' in label.lower():
                        escalations.add('PFAS')
                matched = True
                break
        if matched: continue
        if low in ('fragrance','parfum','natural fragrance','parfum/fragrance','perfume','fragrance (parfum)'):
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
    has_fragrance = any(n.lower() in ('fragrance','parfum','natural fragrance','parfum/fragrance','perfume','fragrance (parfum)') for n,_ in flagged)
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
    if has_pfas or flag_count >= 8 or has_carc_lo or (has_heavy and has_cat2 and has_fragrance):
        tier = 'Avoid (High Priority Swap)'
    esc = []
    if has_pfas: esc.append('PFAS')
    if has_heavy: esc.append('heavy metals')
    if has_form: esc.append('formaldehyde-releaser')
    if has_carc_lo: esc.append('carcinogen in leave-on')
    return tier, flag_count, flagged, natural, unknown, esc

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'audit'
headers = ["product_name","product_url","brand_category","product_type","ingredients_verbatim","tier","flag_count","flagged_ingredients","naturally_occurring_allergens","unknown_ingredients","automatic_escalation","one_line_summary","audit_notes","audit_status"]
ws.append(headers)
tier_count = {}
rows_out = []

# Infer category from name
def infer_category(name):
    n = name.lower()
    if 'curl charisma' in n: return 'Curl Charisma'
    if "don't despair" in n or "don’t despair" in n: return "Don't Despair, Repair!"
    if 'scalp revival' in n: return 'Scalp Revival'
    if 'superfoods' in n: return 'Briogeo Superfoods'
    if 'farewell frizz' in n: return 'Farewell Frizz'
    if 'be gentle, be kind' in n: return 'Be Gentle, Be Kind'
    if 'destined for density' in n: return 'Destined For Density'
    if 'style + treat' in n or 'style+treat' in n: return 'Style + Treat'
    return 'Other'

for name, verbatim in ING.items():
    ptype = infer_product_type(name)
    bcat = infer_category(name)
    # Build URL from name (approximate)
    url = 'https://www.briogeohair.com/products/' + re.sub(r'[^a-z0-9]+','-', name.lower()).strip('-')
    if not verbatim:
        row = [name, url, bcat, ptype, '', '', 0, '', '', '', '', '', '', 'ingredients not found']
        ws.append(row); rows_out.append(row); continue
    tier, flag_count, flagged, natural, unknown, esc = grade(name, ptype, verbatim)
    tier_count[tier] = tier_count.get(tier, 0) + 1
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
    row = [name, url, bcat, ptype, verbatim, tier, flag_count, flag_str, nat_str, unk_str, esc_str, summary, '', 'complete']
    ws.append(row); rows_out.append(row)

wb.save(OUT_XLSX)
print('tiers:', tier_count)
print('rows:', len(rows_out))
json.dump({'tier_count': tier_count, 'rows': [dict(zip(headers, r)) for r in rows_out]}, open('/tmp/briogeo_summary.json','w'))
