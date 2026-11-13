// Parity check: browser grader vs the Python-graded dashboard records.
// Usage: node scraper/browser/parity_test.js [--show N]
const fs = require('fs');
const path = require('path');
const here = __dirname;
const C = JSON.parse(fs.readFileSync(path.join(here, 'constants.json'), 'utf8'));
const refData = JSON.parse(fs.readFileSync(path.join(here, '..', 'ref_compact.json'), 'utf8'));
const src = fs.readFileSync(path.join(here, 'grader.js'), 'utf8').replace('var C = __CONSTANTS__;', () => 'var C = ' + JSON.stringify(C) + ';');
const m = { exports: {} };
new Function('module', 'exports', src)(m, m.exports);
const makeGrader = m.exports;
const G = makeGrader(refData);

const html = fs.readFileSync(path.join(here, '..', '..', 'puberty_scanner_embed.html'), 'utf8');
const data = JSON.parse(html.match(/<script id="product-data"[^>]*>([\s\S]*?)<\/script>/)[1]);
const show = process.argv.includes('--show') ? +process.argv[process.argv.indexOf('--show') + 1] : 10;

let tierMismatch = 0, flagMismatch = 0, escMismatch = 0, total = 0;
const examples = [];
for (const p of data.products) {
  if (!p.ing) continue;
  total++;
  const r = G.grade(p.n, p.pt, p.ing, undefined, p.b);
  const escStr = r.esc.join(', ');
  const tierOk = r.tier === p.t;
  const flagOk = String(r.flagCount) === String(p.f);
  const escOk = (escStr || '') === (p.esc || '');
  if (!tierOk) tierMismatch++;
  if (!flagOk) flagMismatch++;
  if (!escOk) escMismatch++;
  if (!tierOk || !flagOk || !escOk) {
    if (examples.length < show) examples.push({ n: p.n, pt: p.pt, want: [p.t, p.f, p.esc], got: [r.tier, r.flagCount, escStr] });
  }
}
console.log(JSON.stringify({ total, tierMismatch, flagMismatch, escMismatch }));
examples.forEach(e => console.log(JSON.stringify(e)));
