import json, sys, os, datetime
P = '/home/claude/ingredient-scraper/audits/jergens/jergens_ingredients.json'
M = json.load(open('/home/claude/ingredient-scraper/audits/jergens/_master_list.json'))
bys = {m['slug']: m for m in M}
data = json.load(open(P)) if os.path.exists(P) else {"brand":"JERGENS","brand_url":"https://us.jergens.com/","products":{}, "progress":{}}
new = json.load(sys.stdin)  # {slug: {"status":..., "ingredients_verbatim":..., "page_title":..., "note":...}}
for slug, rec in new.items():
    assert slug in bys, slug
    m = bys[slug]
    data['products'][slug] = {"product_name": m['product_name'], "product_url": m['product_url'], "brand_category": m['brand_category'], "product_type": m['product_type'], **rec}
data['progress']['last_saved_utc'] = datetime.datetime.utcnow().isoformat()+'Z'
data['progress']['scraped'] = sum(1 for v in data['products'].values() if v.get('status')=='scraped')
data['progress']['failed'] = sum(1 for v in data['products'].values() if v.get('status')!='scraped')
json.dump(data, open(P,'w'), indent=1, ensure_ascii=False)
print('saved', len(data['products']), 'of', len(M), '| scraped', data['progress']['scraped'])
