/* Label scanner: photo -> text (in the browser) -> grade straight away.
   Only the product type is asked for, because it changes the grade.
   Depends on makeGrader (grader.js) and the reference data in #scanner-ref. */
(function () {
  'use strict';

  var TESS_URL = 'https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js';
  var DEFAULT_TYPE = 'leave-on skincare';
  var CAT_NAME = { 1: 'Carcinogen', 2: 'Endocrine Disruption', 3: 'Heavy Metals', 4: 'Allergies/Irritation',
                   5: 'Microbiome-Busting', 6: 'Microplastics', 7: 'Acutely Toxic', 8: 'Respiratory Irritant', 104: 'Allergies/Irritation' , 9: 'Fluoride (oral care)'};
  var TIER_WRAP = { 'Puberty Safe': 't-safe', 'Use Caution': 't-caution', 'Avoid (Mild)': 't-mild', 'Avoid (Moderate)': 't-moderate', 'Avoid (High)': 't-hps' };

  var productData = JSON.parse(document.getElementById('product-data').textContent);
  var G = window.makeGrader(JSON.parse(document.getElementById('scanner-ref').textContent));

  var $ = function (id) { return document.getElementById(id); };
  var modal = $('scan-modal'), fileEl = $('scan-file'), camEl = $('scan-camera'), preview = $('scan-preview'), statusEl = $('scan-status');
  var cropBox = $('scan-crop'), cropCanvas = $('scan-crop-canvas'), cropSrc = null, cropFile = null, cropUrl = null;
  var resultEl = $('scan-result'), tierEl = $('scan-tier'), detailsEl = $('scan-details'), textEl = $('scan-text');
  var typeEl = $('scan-type');

  var previewUrl = null, current = null, typeTouched = false, tessPromise = null, busy = false, lastFixes = [];

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Labels often print one ingredient per line with no commas. Treat line breaks as separators in that case.
  function tidy(s) {
    var raw = String(s || '');
    if (raw.indexOf(',') < 0) raw = raw.replace(/\s*\n\s*/g, ', ');
    return raw.replace(/\s*\n\s*/g, ' ').replace(/ {2,}/g, ' ').replace(/,\s*,/g, ',').trim();
  }

  // OCR returns the whole page. Keep the text after the "Ingredients" label, up to the next section heading.
  function extractIngredients(s) {
    var m = /\bin\w{0,2}gr?\w{0,3}ents?\b\s*[:;\-–]?\s*/i.exec(s);
    if (!m) return s;
    var rest = s.slice(m.index + m[0].length);
    var stop = /\b(description|directions|how to use|scent profile|warnings?|caution|net wt|made in|distributed by|questions|reviews?|about this|key benefits)\b/i.exec(rest);
    if (stop) rest = rest.slice(0, stop.index);
    rest = rest.replace(/^[,\s]+/, '').trim().replace(/[,\s]+$/, '');
    return rest.indexOf(',') >= 0 ? rest : s;
  }

  // Number of pieces that match a reference name. Real ingredient lists match several; junk matches none.
  function knownCount(text) {
    if (!text) return 0;
    var fixed = fixIngredients(text).text;
    return fixed.split(',').filter(function (p) {
      return knownNames().indexOf(p.trim().toLowerCase()) >= 0;
    }).length;
  }

  // ----- fix OCR misreads by matching each ingredient to the reference names -----
  var KNOWN = null;
  function knownNames() {
    if (KNOWN) return KNOWN;
    KNOWN = [];
    var seen = {};
    function add(k) { var n = String(k).toLowerCase().replace(/\s+/g, ' ').trim(); if (n && !seen[n]) { seen[n] = 1; KNOWN.push(n); } }
    var ref = JSON.parse(document.getElementById('scanner-ref').textContent);
    Object.keys(ref.ref || {}).forEach(add);
    Object.keys(ref.aliases || {}).forEach(add);
    return KNOWN;
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
    var lower = raw.toLowerCase().replace(/\s+/g, ' ').trim();
    if (!lower || lower.length < 4) return null;
    var names = knownNames(), best = null, bestSim = 0, i;
    for (i = 0; i < names.length; i++) {
      var n = names[i];
      if (n === lower) return n; // exact match: nothing to fix, but it still counts as a known name
      if (Math.abs(n.length - lower.length) > (Math.max(n.length, lower.length) > 20 ? 9 : 6)) continue;
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
        var known = knownNames().indexOf(pc.text.toLowerCase()) >= 0;
        if (!known) { out.push(pc.text); return; }
        var shown = titleCase(pc.text);
        if (pc.orig.toLowerCase() !== pc.text.toLowerCase()) fixes.push([pc.orig, shown]);
        out.push(shown);
      });
    });
    return { text: out.join(', '), fixes: fixes };
  }

  function setStatus(msg) { statusEl.textContent = msg || ''; }


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
    typeTouched = false;
    lastFixes = [];
    typeEl.value = DEFAULT_TYPE;
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
          var s = Math.min(1, 2000 / longSide);
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

  // Try the on-device reader first; fall back to Tesseract if it can't load or read.
  // readLog records what each reader did, for the ?debug=1 readout (no effect on normal use).
  var readLog = {};
  // Cloud Vision reader (Google Cloud Function). Empty = off: the on-device
  // reader below is used. Set this to the deployed function URL only after
  // the privacy wording has been approved, because photos leave the phone.
  var VISION_ENDPOINT = '';

  function readWithVision(file) {
    return prepare(file).then(function (blob) {
      return new Promise(function (resolve, reject) {
        var fr = new FileReader();
        fr.onload = function () { resolve(String(fr.result)); };
        fr.onerror = function () { reject(fr.error); };
        fr.readAsDataURL(blob);
      });
    }).then(function (dataUrl) {
      return fetch(VISION_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
      });
    }).then(function (r) {
      if (!r.ok) throw new Error('vision ' + r.status);
      return r.json();
    }).then(function (j) {
      return j && j.text ? j.text : '';
    });
  }

  function readPhoto(file) {
    readLog = {};
    if (VISION_ENDPOINT) {
      return readWithVision(file).then(function (t) {
        readLog.visionChars = (t || '').length;
        var a = extractIngredients(tidy(t));
        readLog.visionKnown = knownCount(a);
        if (knownCount(a) >= 3) return a;
        return readPhotoOnDevice(file);
      }, function (e) {
        readLog.visionError = String((e && e.message) || e).slice(0, 160);
        return readPhotoOnDevice(file);
      });
    }
    return readPhotoOnDevice(file);
  }

  function readPhotoOnDevice(file) {
    return readWithOnnx(file).then(function (t) {
      readLog.onnxChars = (t || '').length;
      readLog.onnxKnown = knownCount(extractIngredients(tidy(t)));
      return extractIngredients(tidy(t));
    }, function (e) {
      readLog.onnxError = String((e && e.message) || e).slice(0, 160);
      return null;
    }).then(function (a) {
      if (a && knownCount(a) >= 3) return a;
      return readWithTesseract(file).then(function (t) {
        var b = extractIngredients(tidy(t));
        readLog.tessKnown = knownCount(b);
        if (!a) return b;
        return knownCount(b) > knownCount(a) ? b : a;
      }, function (e) {
        readLog.tessError = String((e && e.message) || e).slice(0, 160);
        return a;
      });
    });
  }
  var DEBUG_READ = /[?&]debug=1/.test(location.search);

  function readWithTesseract(file) {
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
      return res && res.data && res.data.text;
    });
  }

  // ----- on-device reader: PP-OCRv5 (Apache 2.0, ONNX). Finds text lines, then reads each line. -----
  var OCR_BASE = 'https://ninamarie-nd.github.io/ingredient-scraper/scraper/browser/ocr/';
  var ORT_URL = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.2/dist/ort.min.js';
  var ORT_DIR = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.2/dist/';
  var ocrPromise = null;

  function loadScriptOnce(src) {
    return new Promise(function (resolve, reject) {
      if (window.ort) return resolve(window.ort);
      var s = document.createElement('script');
      s.src = src;
      s.onload = function () { resolve(window.ort); };
      s.onerror = function () { reject(new Error('load failed')); };
      document.head.appendChild(s);
    });
  }

  function loadOcr() {
    if (!ocrPromise) {
      ocrPromise = loadScriptOnce(ORT_URL).then(function (ort) {
        ort.env.wasm.wasmPaths = ORT_DIR;
        return Promise.all([
          fetch(OCR_BASE + 'PP-OCRv5_mobile_det.onnx').then(function (r) { return r.arrayBuffer(); }),
          fetch(OCR_BASE + 'latin_PP-OCRv5_mobile_rec.onnx').then(function (r) { return r.arrayBuffer(); }),
          fetch(OCR_BASE + 'latin_PP-OCRv5_mobile_rec.dict.json').then(function (r) { return r.json(); })
        ]).then(function (parts) {
          return Promise.all([
            ort.InferenceSession.create(parts[0], { executionProviders: ['wasm'] }),
            ort.InferenceSession.create(parts[1], { executionProviders: ['wasm'] })
          ]).then(function (sess) {
            return { ort: ort, det: sess[0], rec: sess[1], dict: parts[2] };
          });
        });
      }).catch(function (e) { ocrPromise = null; throw e; });
    }
    return ocrPromise;
  }

  // Original colors, shrunk only if very large. (The Tesseract path still uses prepare().)
  // Uses an <img> element (works on every phone browser), not createImageBitmap (not always available).
  function colorCanvasFromFile(file) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () {
        try {
          var s = Math.min(1, 2000 / Math.max(img.naturalWidth, img.naturalHeight));
          var c = document.createElement('canvas');
          c.width = Math.round(img.naturalWidth * s); c.height = Math.round(img.naturalHeight * s);
          c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
          URL.revokeObjectURL(url);
          resolve(c);
        } catch (e) { URL.revokeObjectURL(url); reject(e); }
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('photo load failed')); };
      img.src = url;
    });
  }

  function canvasFromBlob(blob) {
    return createImageBitmap(blob).then(function (bmp) {
      var c = document.createElement('canvas');
      c.width = bmp.width; c.height = bmp.height;
      c.getContext('2d').drawImage(bmp, 0, 0);
      return c;
    });
  }

  // Light sharpening helps with slightly blurred phone photos.
  function sharpenCanvas(src) {
    var w = src.width, h = src.height, sctx = src.getContext('2d');
    var s = sctx.getImageData(0, 0, w, h), d = s.data, out = new Uint8ClampedArray(d.length), x, y, c, i, v;
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) for (c = 0; c < 3; c++) {
      i = (y * w + x) * 4 + c;
      if (x === 0 || y === 0 || x === w - 1 || y === h - 1) { out[i] = d[i]; continue; }
      v = 5 * d[i] - d[i - 4] - d[i + 4] - d[i - w * 4] - d[i + w * 4];
      out[i] = v < 0 ? 0 : v > 255 ? 255 : v;
    }
    for (i = 3; i < out.length; i += 4) out[i] = 255;
    var o = document.createElement('canvas');
    o.width = w; o.height = h;
    o.getContext('2d').putImageData(new ImageData(out, w, h), 0, 0);
    return o;
  }

  // Text-line detection (DB). Returns rotated rectangles in the source canvas's coordinates.
  function detectLines(ocr, src) {
    var W = src.width, H = src.height;
    var r = Math.min(1, 960 / Math.max(W, H));
    var nw = Math.max(32, Math.round(W * r / 32) * 32), nh = Math.max(32, Math.round(H * r / 32) * 32);
    var c = document.createElement('canvas');
    c.width = nw; c.height = nh;
    var cx = c.getContext('2d');
    cx.drawImage(src, 0, 0, nw, nh);
    var px = cx.getImageData(0, 0, nw, nh).data, n = nw * nh, t = new Float32Array(3 * n), i, p;
    var mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225];
    for (p = 0; p < n; p++) {
      // The model expects channels in BGR order with these means and deviations.
      t[p] = (px[p * 4 + 2] / 255 - mean[0]) / std[0];
      t[n + p] = (px[p * 4 + 1] / 255 - mean[1]) / std[1];
      t[2 * n + p] = (px[p * 4] / 255 - mean[2]) / std[2];
    }
    var input = new ocr.ort.Tensor('float32', t, [1, 3, nh, nw]);
    return ocr.det.run((function(o){ var m = {}; m[ocr.det.inputNames[0]] = o; return m; })(input)).then(function (res) {
      var key = Object.keys(res)[0], prob = res[key].data;
      var bm = new Uint8Array(n), seen = new Uint8Array(n), k;
      for (k = 0; k < n; k++) bm[k] = prob[k] > 0.3 ? 1 : 0;
      var rects = [], stack = [], q, xx, yy, pts, sum, mx, my;
      for (k = 0; k < n; k++) {
        if (!bm[k] || seen[k]) continue;
        pts = []; sum = 0; stack = [k]; seen[k] = 1;
        while (stack.length) {
          q = stack.pop(); pts.push(q); sum += prob[q];
          xx = q % nw; yy = (q - xx) / nw;
          var nb = [q - 1, q + 1, q - nw, q + nw];
          for (var j = 0; j < 4; j++) {
            var nq = nb[j];
            if (nq < 0 || nq >= n) continue;
            if ((j === 0 && xx === 0) || (j === 1 && xx === nw - 1)) continue;
            if (bm[nq] && !seen[nq]) { seen[nq] = 1; stack.push(nq); }
          }
        }
        if (pts.length < 6 || sum / pts.length < 0.6) continue;
        // Orientation from the pixel spread (principal axis), then the rectangle in that frame.
        mx = 0; my = 0;
        pts.forEach(function (q) { mx += q % nw; my += Math.floor(q / nw); });
        mx /= pts.length; my /= pts.length;
        var sxx = 0, syy = 0, sxy = 0, dx, dy;
        pts.forEach(function (q) { dx = (q % nw) - mx; dy = Math.floor(q / nw) - my; sxx += dx * dx; syy += dy * dy; sxy += dx * dy; });
        var th = 0.5 * Math.atan2(2 * sxy, sxx - syy), ct = Math.cos(th), st = Math.sin(th);
        var umin = Infinity, umax = -Infinity, vmin = Infinity, vmax = -Infinity, u, v;
        pts.forEach(function (q) {
          dx = (q % nw) - mx; dy = Math.floor(q / nw) - my;
          u = dx * ct + dy * st; v = -dx * st + dy * ct;
          if (u < umin) umin = u; if (u > umax) umax = u;
          if (v < vmin) vmin = v; if (v > vmax) vmax = v;
        });
        var rw = umax - umin + 1, rh = vmax - vmin + 1;
        var d = rw * rh * 1.5 / (2 * (rw + rh));          // unclip, as in DB post-processing
        rw += 2 * d; rh += 2 * d;
        var cu = (umin + umax) / 2, cv = (vmin + vmax) / 2;
        var cxNew = mx + cu * ct - cv * st, cyNew = my + cu * st + cv * ct;
        // Back to the source canvas coordinates.
        var sx = W / nw, sy = H / nh;
        rects.push({ cx: cxNew * sx, cy: cyNew * sy, w: rw * sx, h: rh * sy, th: th });
      }
      return rects;
    });
  }

  function cropRect(src, rc) {
    // A little extra room on each end keeps edge characters (like a final "0") from being clipped.
    var pad = 0.3 * rc.h;
    var w = Math.max(2, Math.round(rc.w + 2 * pad)), h = Math.max(2, Math.round(rc.h));
    var c = document.createElement('canvas');
    c.width = w; c.height = h;
    var cx = c.getContext('2d');
    cx.translate(w / 2, h / 2);
    cx.rotate(-rc.th);
    cx.translate(-rc.cx, -rc.cy);
    cx.drawImage(src, 0, 0);
    return c;
  }

  // Read one line image (CTC greedy decoding).
  function readLine(ocr, line) {
    var h = line.height, w = line.width;
    var nw = Math.max(8, Math.min(3200, Math.ceil(w * 48 / h)));
    var c = document.createElement('canvas');
    c.width = nw; c.height = 48;
    c.getContext('2d').drawImage(line, 0, 0, nw, 48);
    var px = c.getContext('2d').getImageData(0, 0, nw, 48).data, n = nw * 48, t = new Float32Array(3 * n), p;
    for (p = 0; p < n; p++) {
      t[p] = (px[p * 4] / 255 - 0.5) / 0.5;
      t[n + p] = (px[p * 4 + 1] / 255 - 0.5) / 0.5;
      t[2 * n + p] = (px[p * 4 + 2] / 255 - 0.5) / 0.5;
    }
    return ocr.rec.run((function(o){ var m = {}; m[ocr.rec.inputNames[0]] = o; return m; })(new ocr.ort.Tensor('float32', t, [1, 3, 48, nw]))).then(function (res) {
      var key = Object.keys(res)[0], out = res[key].data, dims = res[key].dims;
      var T = dims[1], C = dims[2], text = '', prev = -1, k, best, bi, v;
      for (var ti = 0; ti < T; ti++) {
        best = -Infinity; bi = 0;
        for (k = 0; k < C; k++) { v = out[ti * C + k]; if (v > best) { best = v; bi = k; } }
        if (bi !== prev && bi !== 0) {
          if (bi >= 1 && bi <= ocr.dict.length) text += ocr.dict[bi - 1];
          else if (bi === ocr.dict.length + 1) text += ' ';
        }
        prev = bi;
      }
      return text.trim();
    });
  }

  // Full pipeline: detect lines, group pieces on the same line, read each line, return text with one line per row.
  function readWithOnnx(file) {
    return loadOcr().then(function (ocr) {
      return colorCanvasFromFile(file).then(function (src) {
        var sharp = sharpenCanvas(src);
        return detectLines(ocr, sharp).then(function (rects) {
          return groupRows(rects).reduce(function (chain, row) {
            return chain.then(function (acc) {
              var parts = row.items.map(function (it) { return cropRect(sharp, it); });
              return parts.reduce(function (c2, piece) {
                return c2.then(function (list) {
                  return readLine(ocr, piece).then(function (t) { if (t) list.push(t); return list; });
                });
              }, Promise.resolve([])).then(function (list) {
                if (list.length) acc.push(list.join(' '));
                return acc;
              });
            });
          }, Promise.resolve([])).then(function (lines) { return lines.join('\n'); });
        });
      });
    });
  }

  // Group rotated rectangles that sit side by side on one line; each row keeps its pieces left to right.
  function groupRows(rects) {
    var items = rects.map(function (r) { return { r: r, h: Math.min(r.w, r.h), x0: r.cx - r.w / 2, x1: r.cx + r.w / 2, cy: r.cy }; });
    items.sort(function (a, b) { return a.cy - b.cy; });
    var rows = [];
    items.forEach(function (it) {
      var placed = false;
      rows.forEach(function (row) {
        if (placed) return;
        var near = row.items.some(function (o) { return Math.abs(it.cy - o.cy) < 0.2 * Math.min(it.h, o.h); });
        var gap = Math.min.apply(null, row.items.map(function (o) { return Math.max(0, Math.max(it.x0, o.x0) - Math.min(it.x1, o.x1)); }).concat([1e9]));
        if (near && gap < Math.min(it.h, row.h)) { row.items.push(it); row.cy = (row.cy + it.cy) / 2; row.h = (row.h + it.h) / 2; placed = true; }
      });
      if (!placed) rows.push({ cy: it.cy, h: it.h, items: [it] });
    });
    rows.sort(function (a, b) { return a.cy - b.cy; });
    rows.forEach(function (row) { row.items.sort(function (a, b) { return a.x0 - b.x0; }); row.items = row.items.map(function (i) { return i.r; }); });
    return rows;
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
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(f);
    preview.src = previewUrl;
    preview.hidden = false;
    resultEl.hidden = true;
    busy = true;
    setStatus('Reading the label...');
    readPhoto(f).then(function (text) {
      busy = false;
      // A real ingredient list matches several reference names. Junk like "See, bee" matches none.
      if (!text || knownCount(text) < 3) {
        // Never a dead end: show the box so the shopper can type or paste the list and regrade.
        lastFixes = [];
        // Clear the previous product's grade so an old result never sits under a failed read.
        current = null; tierEl.innerHTML = ''; detailsEl.innerHTML = '';
        textEl.value = text || '';
        resultEl.hidden = false;
        setStatus("We couldn't read the full list from this photo. Type or paste the ingredients in the box below and tap Regrade, or retake the photo close, flat and in focus.");
        if (DEBUG_READ) setStatus(statusEl.textContent + '\n[debug] ' + JSON.stringify(readLog));
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
    if (!r.flagCount) return r.tier === 'Use Caution' ? 'No flagged ingredients. This product is rated Use Caution because one or more ingredients on its list aren\'t in our reference yet, or their exact identity isn\'t verified, so we can\'t clear them. This is a gap in our data, not a known concern.' : 'No flagged ingredients.';
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
    // Always show the grade, labelled provisional when words could not be read.
    tierEl.className = TIER_WRAP[r.tier] || '';
    tierEl.innerHTML = '<span class="tier-pill">' + (unreliable ? 'Provisional: ' : '') + esc(r.tier) + '</span>';
    var html = '';
    if (unreliable) {
      html += '<p class="scan-note"><b>Provisional.</b> Some words could not be read. This grade is based on the words that were read. The words we could not match are listed below. Fix them in the box, or retake the photo closer, then tap Regrade.</p>';
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
      html += '<h3>' + (unreliable ? 'Words we could not read' : 'Not in the reference, needs manual review') + '</h3><ul>' + r.unknown.map(function (u) {
        return '<li>' + esc(u) + '</li>';
      }).join('') + '</ul>';
    }
    if (r.esc.length) html += '<p class="scan-note">Escalations: ' + esc(r.esc.join(', ')) + '.</p>';
    // Card copy: why it matters for puberty and what to look for instead (shared with the library cards).
    if (window.PSCard) {
      var cpKeys = [];
      var rinseType = /shampoo|wash|conditioner|cleanser|scrub|soap|toothpaste|mouthwash|bath|shaving|exfoliant/i.test(c.type || '');
      r.flagged.forEach(function (f) {
        f[1].forEach(function (cn) {
          if (cn === 2) cpKeys.push('endocrine');
          else if (cn === 4) cpKeys.push('irritation');
          else if (cn === 3) cpKeys.push('heavy');
          else if (cn === 1 && !rinseType) cpKeys.push('carc');
        });
      });
      r.esc.forEach(function (e) {
        var low = String(e).toLowerCase();
        if (/pfas/.test(low)) cpKeys.push('pfas');
        if (/heavy/.test(low)) cpKeys.push('heavy');
        if (/endocrine/.test(low)) cpKeys.push('endocrine');
        if (/carcinogen in leave-on/.test(low) && !rinseType) cpKeys.push('carc');
      });
      var cpSec = window.PSCard.sections({
        pt: c.type,
        tier: r.tier,
        names: r.flagged.map(function (f) { return f[0].replace(/ \[inferred: .*\]$/, ''); }),
        keys: cpKeys,
        ing: (r.ingredients || []).join(', ')
      });
      if (cpSec.why) html += '<h3>Why this matters for kids in puberty</h3><p class="scan-note">' + esc(cpSec.why) + '</p>';
      if (cpSec.swap) html += '<h3>What to look for instead</h3><p class="scan-note">' + esc(cpSec.swap) + '</p>';
    }
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
    var name = 'Scanned product';
    var type = typeEl.value || DEFAULT_TYPE;
    var text = tidy(raw);
    var r = G.grade(name, type, text);
    current = { name: name, type: type, raw: raw, r: r, dup: null };
    renderResult(current);
    if (scrollIntoView) resultEl.scrollIntoView({ block: 'start' });
    if (r.ingredients.length < 2) setStatus('Only ' + r.ingredients.length + ' ingredient found. Check the list, then tap Regrade.');
    else setStatus('');
  }

  $('scan-regrade').addEventListener('click', function () { gradeFromBox(false); });

})();
