// Re-grade every product in the dashboard from the current grader and reference,
// and write the explanation sentences (p.x) that the dashboard appends to each summary.
// Usage: node scraper/browser/resync.js
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..', '..');
const here = path.join(root, 'scraper', 'browser');
const C = JSON.parse(fs.readFileSync(path.join(here, 'constants.json'), 'utf8'));
const ref = JSON.parse(fs.readFileSync(path.join(root, 'scraper', 'ref_compact.json'), 'utf8'));
const src = fs.readFileSync(path.join(here, 'grader.js'), 'utf8').replace('var C = __CONSTANTS__;', () => 'var C = ' + JSON.stringify(C) + ';');
const m = { exports: {} }; new Function('module', 'exports', src)(m, m.exports);
const G = m.exports(ref);
const HTML = path.join(root, 'puberty_scanner_embed.html');
let html = fs.readFileSync(HTML, 'utf8');
const re = /(<script id="product-data"[^>]*>)([\s\S]*?)(<\/script>)/;
const data = JSON.parse(html.match(re)[2]);
const MISSING = 'ingredient list not published';
const NOTE_MISSING = 'Ingredients missing: full list not published. Use Caution until sourced.';
const uniq = a => [...new Set(a)];
const list = (a, n) => a.length > n ? a.slice(0, n).join(', ') + ' and ' + (a.length - n) + ' more' : a.join(', ');

function explain(p, r) {
  const out = [];
  const frag = uniq(r.fragNames || []);
  if (frag.length) out.push('Fragrance is used in this product (' + list(frag, 4) + ').');
  if (p.cat === 'Period Care') {
    const floors = uniq((r.floors || []).map(f => f[0] + '|' + f[1])).map(s => s.split('|'));
    floors.forEach(f => out.push('Grade rule: ' + f[0] + ' sets a minimum of ' + f[1] + ' whatever else is on the list.'));
    const unk = uniq((r.unknown || []).filter(u => u !== MISSING).map(u => u.replace(/\s*\(.*$/, '').trim()));
    if (unk.length) out.push(unk.length + ' ingredient' + (unk.length === 1 ? '' : 's') + ' not yet identified (' + list(unk, 4) + '); they can\'t be cleared until the brand names them.');
    const nat = uniq((r.natural || []).map(n => n[0]));
    if (nat.length) out.push('Naturally occurring fragrance components (' + list(nat, 3) + ') count as a soft flag, not a full one.');
  }
  return out;
}

let t = 0, nt = 0; const ch = [];
for (const p of data.products) {
  if (!p.ing) continue;
  const r = G.grade(p.n, p.pt, p.ing);
  const fl = (r.flagged || []).map(x => x[0]);
  const esc = (r.esc || []).join(', ');
  const miss = (r.unknown || []).indexOf(MISSING) >= 0;
  if (String(r.tier) !== String(p.t)) { t++; ch.push([p.b, p.n, p.t, '->', r.tier]); }
  if (String(r.tier) !== String(p.t) || String(r.flagCount) !== String(p.f) || esc !== String(p.esc || '') || JSON.stringify(fl) !== JSON.stringify(p.fl || [])) {
    p.t = r.tier; p.f = r.flagCount; p.fl = fl; p.esc = esc; p.ez = !!(p.t === 'Puberty Safe' && p.f === 0);
    if (p.cat === 'Period Care' || miss) { p.note = miss ? NOTE_MISSING : (fl.length ? `${r.flagCount} flagged ingredient(s) incl. ${fl[0]}.` : 'No flagged ingredients.'); p.sum = p.note; nt++; }
  }
  if (miss && p.note !== NOTE_MISSING) { p.note = NOTE_MISSING; p.sum = NOTE_MISSING; nt++; }
  const x = explain(p, r);
  if (x.length) p.x = x; else delete p.x;
}
const counts = {}; for (const p of data.products) counts[p.t] = (counts[p.t] || 0) + 1;
data.tier_counts = Object.fromEntries(Object.keys(data.tier_counts).map(k => [k, counts[k] || 0]));
html = html.replace(re, (a, b, c, d) => b + JSON.stringify(data).replace(/<\//g, '<\\/') + d);
fs.writeFileSync(HTML, html);
console.log('tier changes', t, 'notes touched', nt, JSON.stringify(data.tier_counts));
console.log(JSON.stringify(ch));
