"""Merge scraped sticker prices into the dashboard's product-data JSON.

Reads scraper/prices/prices.json (written by scrape_prices.py) and adds three
fields to every product in puberty_scanner_embed.html:
  pr  - sticker price as a number (USD), or null when no price was found
  pb  - price bucket: "Under $10", "$10–15", "$15–20", "$20–25", "$25+", or "Unknown"
  pd  - date the price was captured (YYYY-MM-DD)
Also sets top-level "price_captured" and "price_counts" in the JSON.

Bucket edges: a price of exactly $10 is "$10–15"; exactly $15 is "$15–20";
exactly $20 is "$20–25"; exactly $25 is "$25+".

Products that share a URL (several sizes on one page) get the same price.
"""
import json, re, sys
from collections import Counter

HERE = __file__.rsplit('/', 1)[0]
REPO = HERE.rsplit('/scraper/', 1)[0]
EMBED = REPO + '/puberty_scanner_embed.html'
PRICES = HERE + '/prices.json'
PATTERN = re.compile(r'(<script id="product-data" type="application/json">)(.*?)(</script>)', re.S)

BUCKETS = ['Under $10', '$10–15', '$15–20', '$20–25', '$25+']


def bucket(price):
    if price is None:
        return 'Unknown'
    if price < 10:
        return 'Under $10'
    if price < 15:
        return '$10–15'
    if price < 20:
        return '$15–20'
    if price < 25:
        return '$20–25'
    return '$25+'


def main():
    prices = json.load(open(PRICES))
    captured = prices['captured']
    by_url = {r['url']: r for r in prices['records']}

    html = open(EMBED).read()
    m = PATTERN.search(html)
    if not m:
        sys.exit('product-data block not found')
    data = json.loads(m.group(2))

    counts = Counter()
    for p in data['products']:
        rec = by_url.get(p.get('u'))
        # Only positive USD prices are bucketed. Zero prices are placeholders;
        # non-USD prices (INR, CAD, GBP on a few sites) would land in the wrong bucket.
        usable = rec and rec.get('status') == 'ok' and rec.get('currency') == 'USD' and (rec.get('price') or 0) > 0
        price = rec['price'] if usable else None
        p['pr'] = price
        p['pb'] = bucket(price)
        p['pd'] = captured if price is not None else None
        counts[p['pb']] += 1

    data['price_captured'] = captured
    data['price_counts'] = {b: counts.get(b, 0) for b in BUCKETS + ['Unknown']}

    raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = html[:m.start(2)] + raw + html[m.end(2):]
    open(EMBED, 'w').write(html)
    print(json.dumps(data['price_counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
