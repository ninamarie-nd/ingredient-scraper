/* Label scanner: photo -> text (in the browser) -> grade straight away.
   Name, brand and type are only asked for when the user saves the product.
   Depends on makeGrader (grader.js) and the reference data in #scanner-ref. */
(function () {
  'use strict';

  var TESS_URL = 'https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js';
  var SCANS_KEY = 'pss_my_scans_v1';
  var DEFAULT_TYPE = 'leave-on skincare';
  var CAT_NAME = { 1: 'Carcinogen', 2: 'Endocrine Disruption', 3: 'Heavy Metals', 4: 'Allergies/Irritation',
                   5: 'Microbiome-Busting', 6: 'Microplastics', 7: 'Acutely Toxic', 8: 'Respiratory Irritant', 104: 'Allergies/Irritation' };
  var TIER_WRAP = { 'Puberty Safe': 't-safe', 'Use Caution': 't-caution', 'Avoid (Mild)': 't-mild', 'Avoid (Moderate)': 't-moderate', 'Avoid (High)': 't-hps' };

  var productData = JSON.parse(document.getElementById('product-data').textContent);
  var G = window.makeGrader(JSON.parse(document.getElementById('scanner-ref').textContent));

  var $ = function (id) { return document.getElementById(id); };
  var modal = $('scan-modal'), fileEl = $('scan-file'), preview = $('scan-preview'), statusEl = $('scan-status');
  var resultEl = $('scan-result'), tierEl = $('scan-tier'), detailsEl = $('scan-details'), textEl = $('scan-text');
  var nameEl = $('scan-name'), brandEl = $('scan-brand'), typeEl = $('scan-type'), saveBtn = $('scan-save'), saveStatus = $('scan-save-status');

  var previewUrl = null, current = null, typeTouched = false, tessPromise = null, busy = false;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function tidy(s) { return String(s || '').replace(/\s*\n\s*/g, ' ').replace(/ {2,}/g, ' ').trim(); }

  // OCR returns the whole page. Keep the text after the "Ingredients" label, up to the next section heading.
  function extractIngredients(s) {
    var m = /\bingredients?\b\s*[:\-–]?\s*/i.exec(s);
    if (!m) return s;
    var rest = s.slice(m.index + m[0].length);
    var stop = /\b(description|directions|how to use|scent profile|warnings?|caution|net wt|made in|distributed by|questions|reviews?|about this|key benefits)\b/i.exec(rest);
    if (stop) rest = rest.slice(0, stop.index);
    rest = rest.trim().replace(/[,\s]+$/, '');
    return rest.indexOf(',') >= 0 ? rest : s;
  }

  function setStatus(msg) { statusEl.textContent = msg || ''; }
  function setSaveStatus(msg) { saveStatus.textContent = msg || ''; }

  function loadScans() {
    try {
      var a = JSON.parse(localStorage.getItem(SCANS_KEY) || '[]');
      return Array.isArray(a) ? a : [];
    } catch (e) { return []; }
  }

  // ----- type dropdown -----
  (function fillTypes() {
    var seen = {};
    productData.types.forEach(function (t) {
      if (!t || seen[t]) return;
      seen[t] = true;
      var o = document.createElement('option');
      o.value = t; o.textContent = t;
      typeEl.appendChild(o);
    });
    typeEl.value = DEFAULT_TYPE;
  })();

  function ensureType(value) {
    var has = Array.prototype.some.call(typeEl.options, function (o) { return o.value === value; });
    if (!has) {
      var o = document.createElement('option');
      o.value = value; o.textContent = value;
      typeEl.appendChild(o);
    }
    typeEl.value = value;
  }

  nameEl.addEventListener('input', function () {
    if (!typeTouched && nameEl.value.trim()) ensureType(G.inferProductType(nameEl.value.trim(), null));
  });
  typeEl.addEventListener('change', function () { typeTouched = true; });

  // ----- open / close -----
  function open() {
    modal.hidden = false;
    setStatus('');
    fileEl.focus();
  }
  function close() { modal.hidden = true; }
  function reset() {
    current = null;
    resultEl.hidden = true;
    tierEl.innerHTML = '';
    detailsEl.innerHTML = '';
    textEl.value = '';
    nameEl.value = '';
    brandEl.value = '';
    typeTouched = false;
    typeEl.value = DEFAULT_TYPE;
    setSaveStatus('');
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save to my scans';
    fileEl.value = '';
    if (previewUrl) { URL.revokeObjectURL(previewUrl); previewUrl = null; }
    preview.removeAttribute('src');
    preview.hidden = true;
    setStatus('');
  }
  $('scan-open').addEventListener('click', open);
  $('scan-close').addEventListener('click', close);
  $('scan-another').addEventListener('click', function () { reset(); fileEl.click(); });
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });

  // ----- photo -> text -> grade -----
  // Light clean-up before OCR: grayscale and stretch the contrast. Falls back to the original photo.
  function prepare(file) {
    return new Promise(function (resolve) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () {
        try {
          var s = Math.min(1, 2000 / Math.max(img.naturalWidth, img.naturalHeight));
          var c = document.createElement('canvas');
          c.width = Math.round(img.naturalWidth * s);
          c.height = Math.round(img.naturalHeight * s);
          var ctx = c.getContext('2d');
          ctx.drawImage(img, 0, 0, c.width, c.height);
          var d = ctx.getImageData(0, 0, c.width, c.height), px = d.data, i, g, lo = 255, hi = 0;
          for (i = 0; i < px.length; i += 4) {
            g = 0.299 * px[i] + 0.587 * px[i + 1] + 0.114 * px[i + 2];
            px[i] = px[i + 1] = px[i + 2] = g;
            if (g < lo) lo = g;
            if (g > hi) hi = g;
          }
          var span = Math.max(1, hi - lo);
          for (i = 0; i < px.length; i += 4) {
            g = (px[i] - lo) * 255 / span;
            px[i] = px[i + 1] = px[i + 2] = g;
          }
          ctx.putImageData(d, 0, 0);
          URL.revokeObjectURL(url);
          c.toBlob(function (b) { resolve(b || file); }, 'image/png');
        } catch (e) { URL.revokeObjectURL(url); resolve(file); }
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
      img.src = url;
    });
  }

  function loadTesseract() {
    if (window.Tesseract) return Promise.resolve(window.Tesseract);
    if (!tessPromise) {
      tessPromise = new Promise(function (resolve, reject) {
        var s = document.createElement('script');
        s.src = TESS_URL;
        s.onload = function () { resolve(window.Tesseract); };
        s.onerror = function () { tessPromise = null; reject(new Error('load failed')); };
        document.head.appendChild(s);
      });
    }
    return tessPromise;
  }

  function readPhoto(file) {
    return loadTesseract().then(function (T) {
      return prepare(file).then(function (blob) {
        return T.createWorker('eng', 1, {
          logger: function (m) {
            if (m && m.status === 'recognizing text' && typeof m.progress === 'number') {
              setStatus('Reading the label... ' + Math.round(m.progress * 100) + '%');
            }
          }
        }).then(function (worker) {
          return worker.recognize(blob).then(function (res) {
            return worker.terminate().then(function () { return res; });
          });
        });
      });
    }).then(function (res) {
      return extractIngredients(tidy(res && res.data && res.data.text));
    });
  }

  fileEl.addEventListener('change', function () {
    var f = fileEl.files && fileEl.files[0];
    if (!f || busy) return;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(f);
    preview.src = previewUrl;
    preview.hidden = false;
    resultEl.hidden = true;
    busy = true;
    setStatus('Reading the label...');
    readPhoto(f).then(function (text) {
      busy = false;
      if (!text || text.split(',').length < 2) {
        setStatus("We couldn't read an ingredient list from this photo. Try again with the list close, flat and in focus.");
        return;
      }
      textEl.value = text;
      setStatus('');
      gradeFromBox(true);
    }).catch(function () {
      busy = false;
      setStatus('The text reader could not load. Check your internet connection and try the photo again.');
    });
  });

  // ----- grade -----
  function summaryOf(r) {
    var names = r.flagged.map(function (f) { return f[0].replace(/ \[inferred: .*\]$/, ''); });
    if (!r.flagCount) return 'No flagged ingredients.';
    return r.flagCount + ' flagged ingredient' + (r.flagCount === 1 ? '' : 's') + (names.length ? ' incl. ' + names[0] : '') + '.';
  }

  function catText(cats) {
    var out = [];
    cats.forEach(function (c) {
      var n = CAT_NAME[c];
      if (n && out.indexOf(n) < 0) out.push(n);
    });
    return out.join(', ');
  }

  function renderResult(c) {
    var r = c.r;
    // If many words could not be matched, the photo was probably unclear or showed more than the ingredient list.
    var unreliable = r.ingredients.length >= 3 && (r.unknown.length / r.ingredients.length) > 0.3;
    if (unreliable) {
      tierEl.className = '';
      tierEl.innerHTML = '<span class="tier-pill">Read unclear</span>';
    } else {
      tierEl.className = TIER_WRAP[r.tier] || '';
      tierEl.innerHTML = '<span class="tier-pill">' + esc(r.tier) + '</span>';
    }
    var html = '';
    if (unreliable) {
      html += '<p class="scan-note"><b>Many words could not be matched to an ingredient, so this grade may be wrong.</b> Retake the photo with only the ingredient list in frame, close, flat and in focus, then scan again.</p>';
    }
    html += '<p class="scan-note">' + esc(summaryOf(r)) + ' Read ' + r.ingredients.length + ' ingredient' + (r.ingredients.length === 1 ? '' : 's') + '.</p>';
    if (c.dup) {
      html += '<p class="scan-note">This name is already in the database (' + esc(c.dup.b) + ', ' + esc(c.dup.t) + ').</p>';
    }
    if (r.flagged.length) {
      html += '<h3>Flagged</h3><ul>' + r.flagged.map(function (f) {
        return '<li>' + esc(f[0].replace(/ \[inferred: .*\]$/, '')) + (catText(f[1]) ? ' <span class="scan-note">(' + esc(catText(f[1])) + ')</span>' : '') + '</li>';
      }).join('') + '</ul>';
    }
    if (r.natural.length) {
      html += '<h3>Naturally occurring allergens (soft flag)</h3><ul>' + r.natural.map(function (f) {
        return '<li>' + esc(f[0]) + '</li>';
      }).join('') + '</ul>';
    }
    if (r.unknown.length) {
      html += '<h3>Not in the reference, needs manual review</h3><ul>' + r.unknown.map(function (u) {
        return '<li>' + esc(u) + '</li>';
      }).join('') + '</ul>';
    }
    if (r.esc.length) html += '<p class="scan-note">Escalations: ' + esc(r.esc.join(', ')) + '.</p>';
    html += '<p class="scan-note">If a word in the list looks wrong, fix it in the box below and tap Regrade.</p>';
    detailsEl.innerHTML = html;
    resultEl.hidden = false;
  }

  // Grades the ingredient box. Used after a photo is read and again after any correction.
  function gradeFromBox(scrollIntoView) {
    var raw = textEl.value.trim();
    if (!raw) { setStatus('The ingredient list is empty. Fix it, then tap Regrade.'); return; }
    var name = nameEl.value.trim() || 'Scanned product';
    var type = typeEl.value || DEFAULT_TYPE;
    var text = tidy(raw);
    var r = G.grade(name, type, text);
    var key = name.toLowerCase();
    var dup = null;
    if (nameEl.value.trim()) {
      productData.products.some(function (p) {
        if (String(p.n || '').toLowerCase() === key) { dup = p; return true; }
        return false;
      });
    }
    current = { name: name, brand: brandEl.value.trim(), type: type, raw: raw, r: r, dup: dup, saved: false };
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save to my scans';
    setSaveStatus('');
    renderResult(current);
    if (scrollIntoView) resultEl.scrollIntoView({ block: 'start' });
    if (r.ingredients.length < 2) setStatus('Only ' + r.ingredients.length + ' ingredient found. Check the list, then tap Regrade.');
    else setStatus('');
  }

  $('scan-regrade').addEventListener('click', function () { gradeFromBox(false); });

  // ----- save / export -----
  function buildRecord(c) {
    var r = c.r;
    var summary = summaryOf(r);
    return {
      n: c.name,
      b: c.brand || 'Scanned by user',
      bs: 'scanned',
      cat: 'Scanned label',
      pt: c.type,
      t: r.tier,
      f: r.flagCount,
      fl: r.flagged.map(function (f) { return f[0].replace(/ \[inferred: .*\]$/, ''); }),
      esc: r.esc.join(', '),
      u: '',
      note: summary,
      ing: c.raw,
      sum: summary,
      pts: [c.type],
      tags: [],
      ez: r.tier === 'Puberty Safe' && !r.flagged.some(function (f) { return f[1].indexOf(4) >= 0 || f[1].indexOf(104) >= 0; }) && !r.natural.length,
      source: 'scan',
      scanned_at: new Date().toISOString()
    };
  }

  saveBtn.addEventListener('click', function () {
    if (!current) return;
    if (current.saved) return;
    // Save what the user sees now: regrade with the name, brand, type and text as they are.
    gradeFromBox(false);
    var rec = buildRecord(current);
    var list = loadScans().filter(function (s) { return !(s.n === rec.n && s.b === rec.b && s.ing === rec.ing); });
    list.push(rec);
    var stored = true;
    try { localStorage.setItem(SCANS_KEY, JSON.stringify(list)); } catch (e) { stored = false; }
    document.dispatchEvent(new CustomEvent('pss-scan-saved', { detail: rec }));
    current.saved = true;
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saved';
    setSaveStatus(stored
      ? 'Saved on this device. It now shows up in search.'
      : 'Shown in search for this visit only. This browser would not keep it, so export it now if you want to keep it.');
  });

  $('scan-export').addEventListener('click', function () {
    var list = loadScans();
    if (!list.length) { setSaveStatus('No saved scans yet. Save a product first.'); return; }
    var payload = { exported_at: new Date().toISOString(), count: list.length, products: list };
    var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'scanned_products_' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  });
})();
