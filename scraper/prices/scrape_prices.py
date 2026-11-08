"""Scrape sticker prices for every product URL in the Puberty Scanner database.

Reads product URLs from puberty_scanner_embed.html, fetches each unique URL once
(one request per domain at a time, with a pause between requests), and writes
scraper/prices/prices.json with one record per URL:
  {"url", "status", "price", "currency", "method", "captured"}

Price sources, in order: JSON-LD Product offers, then product:price meta tags.
"""
import json, re, sys, time, datetime, urllib.request, urllib.error, concurrent.futures
from collections import defaultdict
import urllib.parse
from urllib.parse import urlparse

HERE = __file__.rsplit('/', 1)[0]
REPO = HERE.rsplit('/scraper/', 1)[0]
OUT = HERE + '/prices.json'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
PAUSE = 1.0
TODAY = datetime.date.today().isoformat()


def load_urls():
    t = open(REPO + '/puberty_scanner_embed.html').read()
    raw = re.search(r'<script id="product-data" type="application/json">(.*?)</script>', t, re.S).group(1)
    products = json.loads(raw)['products']
    return sorted({p['u'] for p in products if p.get('u')})


def fetch(url):
    url = urllib.parse.quote(url, safe=":/?=&%#+,;@!$'()*~[]")
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read(1500000).decode('utf8', 'ignore')


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def price_from_html(html):
    for block in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            data = json.loads(block.strip())
        except Exception:
            continue
        for node in _walk(data):
            typ = node.get('@type')
            types = typ if isinstance(typ, list) else [typ]
            if 'Product' not in types:
                continue
            offers = node.get('offers')
            offers = offers if isinstance(offers, list) else [offers]
            for off in offers:
                if not isinstance(off, dict):
                    continue
                for key in ('price', 'lowPrice', 'lowestPrice'):
                    if off.get(key) not in (None, ''):
                        try:
                            return float(str(off[key]).replace(',', '')), off.get('priceCurrency', 'USD'), 'json-ld'
                        except ValueError:
                            pass
    m = re.search(r'<meta[^>]+property=["\'](?:product:price:amount|og:price:amount)["\'][^>]+content=["\']([\d.,]+)', html, re.I)
    if m:
        cur = re.search(r'<meta[^>]+property=["\'](?:product:price:currency|og:price:currency)["\'][^>]+content=["\']([A-Za-z]{3})', html, re.I)
        return float(m.group(1).replace(',', '')), (cur.group(1).upper() if cur else 'USD'), 'meta'
    # Visible price element: a class containing "price" (not wholesale/was/strike/compare) whose text is a dollar amount.
    m = re.search(r'class=["\'][^"\']*price[^"\']*["\'][^>]*>\s*\$\s?(\d{1,4}(?:,\d{3})*\.\d{2})\s*<', html, re.I)
    if m and not re.search(r'wholesale|strike|compare|was-|old', html[max(0, m.start()-60):m.start()], re.I):
        return float(m.group(1).replace(',', '')), 'USD', 'class-price'
    return None, None, None


def shopify_price(url):
    """Shopify stores expose /products/<handle>.js with prices in cents."""
    try:
        data = json.loads(fetch(url.split('?')[0].rstrip('/') + '.js'))
    except Exception:
        return None, None, None
    cents = data.get('price')
    if cents is None:
        return None, None, None
    return cents / 100.0, 'USD', 'shopify'


def scrape_one(url):
    rec = {'url': url, 'status': None, 'price': None, 'currency': None, 'method': None, 'captured': TODAY}
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        rec['status'] = 'blocked' if e.code in (401, 403, 307, 429) else f'http {e.code}'
        return rec
    except Exception as e:
        rec['status'] = f'error: {type(e).__name__}'
        return rec
    price, cur, method = price_from_html(html)
    if price is None and '/products/' in url:
        price, cur, method = shopify_price(url)
    if price is None:
        rec['status'] = 'no price found'
    else:
        rec.update(status='ok', price=price, currency=cur, method=method)
    return rec


def scrape_domain(urls):
    out = []
    for u in urls:
        out.append(scrape_one(u))
        time.sleep(PAUSE)
    return out


def retry_misses():
    """Re-fetch only URLs that did not produce a price on the last run."""
    prev = json.load(open(OUT))
    misses = [r['url'] for r in prev['records'] if r['status'] != 'ok']
    print(f'retrying {len(misses)} URLs without a price', flush=True)
    by_host = defaultdict(list)
    for u in misses:
        by_host[urlparse(u).netloc].append(u)
    fresh = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        for recs in ex.map(scrape_domain, by_host.values()):
            for r in recs:
                fresh[r['url']] = r
    keep = [fresh.get(r['url'], r) if r['status'] != 'ok' else r for r in prev['records']]
    keep.sort(key=lambda r: r['url'])
    json.dump({'captured': TODAY, 'records': keep}, open(OUT, 'w'), indent=1)
    ok = sum(1 for r in keep if r['status'] == 'ok')
    print(f'done: {ok} priced, {len(keep) - ok} without price -> {OUT}', flush=True)


def main(limit=None):
    urls = load_urls()
    if limit:
        urls = urls[:limit]
    by_host = defaultdict(list)
    for u in urls:
        by_host[urlparse(u).netloc].append(u)
    print(f'{len(urls)} unique URLs across {len(by_host)} hosts', flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        for recs in ex.map(scrape_domain, by_host.values()):
            results.extend(recs)
    results.sort(key=lambda r: r['url'])
    json.dump({'captured': TODAY, 'records': results}, open(OUT, 'w'), indent=1)
    ok = sum(1 for r in results if r['status'] == 'ok')
    print(f'done: {ok} priced, {len(results) - ok} without price -> {OUT}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--retry':
        retry_misses()
    else:
        main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
