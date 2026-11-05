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
  var modal = $('scan-modal'), fileEl = $('scan-file'), camEl = $('scan-camera'), preview = $('scan-preview'), statusEl = $('scan-status');
  var cropBox = $('scan-crop'), cropCanvas = $('scan-crop-canvas'), cropSrc = null, cropFile = null, cropUrl = null;
  var resultEl = $('scan-result'), tierEl = $('scan-tier'), detailsEl = $('scan-details'), textEl = $('scan-text');
  var nameEl = $('scan-name'), brandEl = $('scan-brand'), typeEl = $('scan-type'), saveBtn = $('scan-save'), saveStatus = $('scan-save-status');

  var previewUrl = null, current = null, typeTouched = false, tessPromise = null, busy = false, lastFixes = [];

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

  // ----- fix OCR misreads by matching each ingredient to the reference names -----
  var KNOWN = null, KNOWN_SET = null, KNOWN_BG = null;
  // Names to match against: the reference list, plus ingredient names that appear in at least two
  // products in the database. The database adds many common names the reference does not list.
  function knownNames() {
    if (KNOWN) return KNOWN;
    KNOWN = [];
    KNOWN_SET = {};
    function add(k) {
      var n = String(k).toLowerCase().replace(/\s+/g, ' ').trim();
      if (n && !KNOWN_SET[n]) { KNOWN_SET[n] = 1; KNOWN.push(n); }
    }
    var ref = JSON.parse(document.getElementById('scanner-ref').textContent);
    Object.keys(ref.ref || {}).forEach(add);
    Object.keys(ref.aliases || {}).forEach(add);
    try {
      var el = document.getElementById('product-data');
      var data = el ? JSON.parse(el.textContent) : { products: [] };
      var count = {};
      (data.products || []).forEach(function (pr) {
        var seenHere = {};
        String(pr.ing || '').split(',').forEach(function (seg) {
          var n = seg.toLowerCase().replace(/\s+/g, ' ').replace(/^[^a-z(]+/, '').replace(/[^a-z)]+$/, '').trim();
          if (n.length < 4 || n.length > 60 || /[:%\/]/.test(n) || seenHere[n]) return;
          seenHere[n] = 1;
          count[n] = (count[n] || 0) + 1;
        });
      });
      Object.keys(count).forEach(function (n) { if (count[n] >= 2) add(n); });
    } catch (e) { /* no database on this page: reference names only */ }
    KNOWN_BG = KNOWN.map(bigrams);
    return KNOWN;
  }
  function bigrams(str) {
    var set = {}, i;
    for (i = 0; i < str.length - 1; i++) set[str.substr(i, 2)] = 1;
    return set;
  }
  // Fraction of shared letter pairs (Dice coefficient). Cheap pre-check before the full edit distance.
  function diceScore(qb, nb) {
    var shared = 0, qn = 0, nn = 0, k;
    for (k in qb) { qn++; if (nb[k]) shared++; }
    for (k in nb) nn++;
    return qn + nn ? (2 * shared) / (qn + nn) : 0;
  }
  function editDistance(a, b) {
    var prev = [], cur, i, j, cost;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) {
        cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
      }
      prev = cur;
    }
    return prev[b.length];
  }
  // Best reference name for one OCR'd ingredient, or null when nothing is close enough.
  function bestName(raw, inner) {
    // Stray symbols from the photo ("|", "~", "»") are not words: drop them before matching.
    var lower = raw.toLowerCase().replace(/[^a-z() \-]+/g, ' ').replace(/\s+/g, ' ').trim();
    if (!lower || lower.length < 4) return null;
    var names = knownNames(), best = null, bestSim = 0, i;
    if (KNOWN_SET[lower]) return lower; // exact match: nothing to fix, but it still counts as a known name
    var qb = bigrams(lower);
    var qWords = lower.split(' ').length;
    for (i = 0; i < names.length; i++) {
      var n = names[i];
      if (Math.abs(n.length - lower.length) > (Math.max(n.length, lower.length) > 20 ? 9 : 6)) continue;
      // Word count must agree, so a short piece cannot be stretched into a longer name ("Flower" -> "Flower Oil").
      var nWords = n.split(' ').length;
      if (nWords !== qWords) continue;
      if (diceScore(qb, KNOWN_BG[i]) < 0.5) continue; // too different to be a misread of this name
      var d = editDistance(lower, n), sim = 1 - d / Math.max(lower.length, n.length);
      if (sim > bestSim) { bestSim = sim; best = n; }
    }
    // Require a high match; short names must be nearly exact.
    if (lower.length < 12) return bestSim >= 0.9 ? best : null;
    if (bestSim >= 0.82) return best;
    // A whole ingredient with garbled OCR can keep its start: accept a looser match only then.
    // Pieces found inside a merged line must match closely, so a stray word cannot rename them.
    if (inner) return null;
    return bestSim >= 0.65 && best && best.slice(0, 3) === lower.slice(0, 3) ? best : null;
  }
  // Split one OCR'd piece into reference names. Handles two ingredients that lost their comma.
  // Returns null when nothing in the piece matches a reference name.
  function splitFix(clean) {
    var words = clean.split(/\s+/), pieces = [], buf = [], i = 0, any = false;
    while (i < words.length) {
      var found = null, len, f;
      for (len = Math.min(4, words.length - i); len >= 1 && !found; len--) {
        f = bestName(words.slice(i, i + len).join(' '), true);
        if (f) found = { name: f, len: len };
      }
      if (found) {
        if (buf.length) { pieces.push({ text: buf.join(' '), orig: buf.join(' ') }); buf = []; }
        pieces.push({ text: found.name, orig: words.slice(i, i + found.len).join(' ') });
        i += found.len;
        any = true;
      } else {
        buf.push(words[i]);
        i++;
      }
    }
    if (buf.length) pieces.push({ text: buf.join(' '), orig: buf.join(' ') });
    return any ? pieces : null;
  }
  function titleCase(s) { return s.replace(/\b\w/g, function (c) { return c.toUpperCase(); }); }
  function fixIngredients(text) {
    var fixes = [];
    var out = [];
    // OCR can leave the label heading stuck to the front, e.g. "hgredients/Ingredientes: Water, ..."
    text = String(text).replace(/^[^,:]{0,40}:\s*/, '');
    String(text).split(',').forEach(function (p) {
      var orig = p.trim();
      var clean = orig.replace(/^[^A-Za-z(]+/, '').replace(/[^A-Za-z)]+$/, '');
      if (!clean) { out.push(orig); return; }
      var whole = bestName(clean);
      var pieces = whole ? [{ text: whole, orig: clean }] : splitFix(clean);
      if (!pieces) { out.push(orig); return; }
      pieces.forEach(function (pc) {
        var known = !!KNOWN_SET[pc.text.toLowerCase()];
        if (!known) { out.push(pc.text); return; }
        var shown = titleCase(pc.text);
        if (pc.orig.toLowerCase() !== pc.text.toLowerCase()) fixes.push([pc.orig, shown]);
        out.push(shown);
      });
    });
    return { text: out.join(', '), fixes: fixes };
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
  typeEl.addEventListener('change', function () {
    typeTouched = true;
    // Product type changes the grade (leave-on vs rinse-off), so re-grade if a result is showing.
    if (current) gradeFromBox(false);
  });

  // ----- open / close -----
  function open() {
    modal.hidden = false;
    setStatus('');
    showSources();
    $('scan-take').focus();
  }
  function showSources() {
    $('scan-sources').hidden = false;
    cropBox.hidden = true;
    if (cropUrl) { URL.revokeObjectURL(cropUrl); cropUrl = null; }
    cropSrc = null; cropFile = null;
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
    lastFixes = [];
    typeEl.value = DEFAULT_TYPE;
    setSaveStatus('');
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save to my scans';
    fileEl.value = '';
    camEl.value = '';
    showSources();
    if (previewUrl) { URL.revokeObjectURL(previewUrl); previewUrl = null; }
    preview.removeAttribute('src');
    preview.hidden = true;
    setStatus('');
  }
  $('scan-open').addEventListener('click', open);
  $('scan-close').addEventListener('click', close);
  $('scan-another').addEventListener('click', function () { reset(); });
  $('scan-take').addEventListener('click', function () { camEl.click(); });
  $('scan-library').addEventListener('click', function () { fileEl.click(); });
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
          var longSide = Math.max(img.naturalWidth, img.naturalHeight);
          // OCR reads large letters best: enlarge small crops, shrink very large photos.
          var s = Math.min(3000 / longSide, Math.max(1, 2400 / longSide));
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

  // ----- choose a photo -> optional crop -> read -----
  function pickedFile(input) {
    var f = input.files && input.files[0];
    if (!f || busy) return;
    input.value = '';
    showCrop(f);
  }
  fileEl.addEventListener('change', function () { pickedFile(fileEl); });
  camEl.addEventListener('change', function () { pickedFile(camEl); });

  var cropImg = null;
  function showCrop(f) {
    cropFile = f;
    setStatus('');
    resultEl.hidden = true;
    preview.hidden = true;
    $('scan-sources').hidden = true;
    cropBox.hidden = false;
    ['top', 'bottom', 'left', 'right'].forEach(function (k) { $('crop-' + k).value = 0; });
    var img = new Image();
    var url = URL.createObjectURL(f);
    img.onload = function () {
      cropImg = img;
      cropSrc = url;
      drawCrop();
    };
    img.onerror = function () {
      URL.revokeObjectURL(url);
      showSources();
      setStatus("We couldn't open that photo. Try another one.");
    };
    img.src = url;
  }
  function cropRect() {
    var t = +$('crop-top').value / 100, b = +$('crop-bottom').value / 100;
    var l = +$('crop-left').value / 100, r = +$('crop-right').value / 100;
    // Keep at least 10% of the photo in each direction, so the box cannot collapse.
    if (t + b > 0.9) { var kv = 0.9 / (t + b); t *= kv; b *= kv; }
    if (l + r > 0.9) { var kh = 0.9 / (l + r); l *= kh; r *= kh; }
    var W = cropImg.naturalWidth, H = cropImg.naturalHeight;
    return { x: Math.round(l * W), y: Math.round(t * H), w: Math.round(W * (1 - l - r)), h: Math.round(H * (1 - t - b)) };
  }
  function drawCrop() {
    if (!cropImg) return;
    var W = cropImg.naturalWidth, H = cropImg.naturalHeight;
    var scale = Math.min(1, 600 / W);
    cropCanvas.width = Math.round(W * scale);
    cropCanvas.height = Math.round(H * scale);
    var ctx = cropCanvas.getContext('2d');
    ctx.drawImage(cropImg, 0, 0, cropCanvas.width, cropCanvas.height);
    var r = cropRect();
    var sx = r.x * scale, sy = r.y * scale, sw = r.w * scale, sh = r.h * scale;
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.fillRect(0, 0, cropCanvas.width, sy);
    ctx.fillRect(0, sy + sh, cropCanvas.width, cropCanvas.height - sy - sh);
    ctx.fillRect(0, sy, sx, sh);
    ctx.fillRect(sx + sw, sy, cropCanvas.width - sx - sw, sh);
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#3aa0a4';
    ctx.strokeRect(sx, sy, sw, sh);
  }
  ['top', 'bottom', 'left', 'right'].forEach(function (k) {
    $('crop-' + k).addEventListener('input', drawCrop);
  });
  // Drag an edge of the blue box directly on the photo.
  var dragEdge = null;
  function canvasPoint(e) {
    var r = cropCanvas.getBoundingClientRect();
    return { x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height };
  }
  function edgeAt(p) {
    var t = +$('crop-top').value / 100, b = 1 - (+$('crop-bottom').value / 100);
    var l = +$('crop-left').value / 100, r = 1 - (+$('crop-right').value / 100);
    var tol = 0.07, best = null, bd = tol;
    var inX = p.x >= l - tol && p.x <= r + tol, inY = p.y >= t - tol && p.y <= b + tol;
    if (inX) {
      if (Math.abs(p.y - t) < bd) { bd = Math.abs(p.y - t); best = 'top'; }
      if (Math.abs(p.y - b) < bd) { bd = Math.abs(p.y - b); best = 'bottom'; }
    }
    if (inY) {
      if (Math.abs(p.x - l) < bd) { bd = Math.abs(p.x - l); best = 'left'; }
      if (Math.abs(p.x - r) < bd) { bd = Math.abs(p.x - r); best = 'right'; }
    }
    return best;
  }
  cropCanvas.addEventListener('pointerdown', function (e) {
    if (!cropImg) return;
    var edge = edgeAt(canvasPoint(e));
    if (!edge) return;
    dragEdge = edge;
    cropCanvas.setPointerCapture(e.pointerId);
    e.preventDefault();
  });
  cropCanvas.addEventListener('pointermove', function (e) {
    if (!dragEdge) return;
    var p = canvasPoint(e), v;
    if (dragEdge === 'top') v = p.y * 100;
    else if (dragEdge === 'bottom') v = (1 - p.y) * 100;
    else if (dragEdge === 'left') v = p.x * 100;
    else v = (1 - p.x) * 100;
    v = Math.max(0, Math.min(80, Math.round(v)));
    $('crop-' + dragEdge).value = v;
    drawCrop();
  });
  function endDrag() { dragEdge = null; }
  cropCanvas.addEventListener('pointerup', endDrag);
  cropCanvas.addEventListener('pointercancel', endDrag);
  $('crop-cancel').addEventListener('click', function () { showSources(); fileEl.value = ''; camEl.value = ''; });
  $('crop-full').addEventListener('click', function () { if (cropFile) startRead(cropFile); });
  $('crop-use').addEventListener('click', function () {
    if (!cropImg) return;
    var r = cropRect();
    var c = document.createElement('canvas');
    c.width = r.w; c.height = r.h;
    c.getContext('2d').drawImage(cropImg, r.x, r.y, r.w, r.h, 0, 0, r.w, r.h);
    c.toBlob(function (blob) { startRead(blob || cropFile); }, 'image/jpeg', 0.95);
  });

  function startRead(f) {
    if (busy) return;
    cropBox.hidden = true;
    $('scan-sources').hidden = true;
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
      var fixed = fixIngredients(text);
      lastFixes = fixed.fixes;
      textEl.value = fixed.text;
      setStatus('');
      gradeFromBox(true);
    }).catch(function () {
      busy = false;
      setStatus('The text reader could not load. Check your internet connection and try the photo again.');
    });
  }

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
    if (lastFixes && lastFixes.length) {
      html += '<p class="scan-note">We corrected ' + lastFixes.length + ' word' + (lastFixes.length === 1 ? '' : 's') + ' from the photo to the closest ingredient name. Check these: ' +
        lastFixes.slice(0, 8).map(function (f) { return esc(f[0]) + ' \u2192 ' + esc(f[1]); }).join('; ') + '.</p>';
    }
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
