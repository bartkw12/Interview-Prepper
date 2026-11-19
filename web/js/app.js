// Interview Prepper: the study app.
// Data comes from data/cards.js (window.PREP_DATA), built by scripts/build_data.py.
// Marks are saved to progress.json through run.py's /api/progress when the app is served by run.py,
// and always mirrored to localStorage, so the page still works when index.html is opened from disk.
(async function () {
  'use strict';
  const DATA = window.PREP_DATA;
  const $ = id => document.getElementById(id);
  if (!DATA || !Array.isArray(DATA.cards)) {
    document.querySelector('main').innerHTML =
      '<div class="empty"><h2>No card data found</h2><p>web/data/cards.js is missing. Run <code>python scripts/build_data.py</code>, then reload.</p></div>';
    return;
  }
  const CARDS = DATA.cards;
  const SECS = DATA.sections || {};
  const CONFIG = DATA.config || {};
  const byId = new Map(CARDS.map(c => [c.id, c]));

  // ---------- saving ----------
  const KEY = 'interviewprepper.v1';
  const Store = {
    server: false,
    timer: null,
    readLocal() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } },
    writeLocal(obj) { try { localStorage.setItem(KEY, JSON.stringify(obj)); } catch (e) { /* private window or blocked storage */ } },
    async load() {
      const local = this.readLocal();
      if (location.protocol === 'http:' || location.protocol === 'https:') {
        try {
          const r = await fetch('api/progress', { cache: 'no-store' });
          if (r.ok) {
            this.server = true;
            const remote = await r.json();
            // Prefer the file on disk; fall back to this browser's copy if the file is still empty.
            return remote && Object.keys(remote).length ? remote : local;
          }
        } catch (e) { /* not served by run.py */ }
      }
      return local;
    },
    save(obj) {
      this.writeLocal(obj);
      if (!this.server) return;
      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        fetch('api/progress', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(obj) })
          .then(r => { if (!r.ok) throw new Error(r.status); setSaved('Marks saved to progress.json'); })
          .catch(() => setSaved('Could not reach run.py; marks are kept in this browser for now', true));
      }, 250);
    },
  };
  function setSaved(text, warn) {
    const el = $('saved');
    el.textContent = text;
    el.style.color = warn ? 'var(--hard)' : '';
  }

  const saved = await Store.load();
  const st = {
    marks: saved.marks || {},
    retired: new Set(Array.isArray(saved.retired) ? saved.retired : []),  // "Memorized": kept apart from marks so they survive a round trip
    deck: saved.deck || 'all',
    secs: new Set((saved.secs || []).filter(k => k in SECS)),
    shuffle: !!saved.shuffle,
    view: 'study',
    order: [], pos: 0, hint: 0, shown: false, editing: false,
    sheet: saved.sheet || 0,
  };
  const Timer = window.PrepTimer;
  const persist = () => Store.save({
    marks: st.marks, retired: [...st.retired], deck: st.deck, secs: [...st.secs], shuffle: st.shuffle, sheet: st.sheet,
    timer: Timer ? Timer.options() : saved.timer,
  });
  if (Timer) Timer.init(saved.timer, persist);
  setSaved(Store.server ? 'Marks saved to progress.json' : 'Marks saved in this browser');

  // ---------- header ----------
  if (CONFIG.title) document.title = CONFIG.title;
  if (CONFIG.brand) $('brand').textContent = CONFIG.brand;
  function countdown() {
    const iv = CONFIG.interview;
    const el = $('countdown');
    if (!iv || !iv.datetime) { el.textContent = ''; return; }
    const t = new Date(iv.datetime).getTime() - Date.now();
    const label = iv.label || new Date(iv.datetime).toLocaleString();
    if (isNaN(t)) { el.textContent = ''; return; }
    if (t <= 0) { el.textContent = 'Interview: ' + label; return; }
    const d = Math.floor(t / 864e5), h = Math.floor(t % 864e5 / 36e5), m = Math.floor(t % 36e5 / 6e4);
    el.textContent = 'Interview ' + label + ' · in ' + (d ? d + 'd ' + h + 'h' : h ? h + 'h ' + m + 'm' : m + 'm');
  }
  countdown(); setInterval(countdown, 60000);

  // ---------- decks and order ----------
  const live = c => !st.retired.has(c.id);
  const DECKS = [
    { id: 'all', label: 'All cards', test: c => live(c) },
    { id: 'star', label: '★ Must-know', test: c => live(c) && c.star },
    { id: 'hard', label: 'Struggling', test: c => live(c) && st.marks[c.id] === 'hard' },
    { id: 'todo', label: 'Not got yet', test: c => live(c) && st.marks[c.id] !== 'got' },
    { id: 'retired', label: 'Memorized', test: c => !live(c) },
  ];
  const fmtTime = t => {
    if (!t || !t.target) return '';
    const f = Timer ? Timer.fmt : (s => s + 's');
    return '⏱ ' + f(t.target) + (t.min != null && t.max != null ? ' <small>(' + f(t.min) + '–' + f(t.max) + ')</small>' : '');
  };
  const esc = s => String(s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));

  function pool() {
    const d = DECKS.find(x => x.id === st.deck) || DECKS[0];
    return CARDS.filter(c => d.test(c) && (st.secs.size === 0 || st.secs.has(c.sec)));
  }
  function rebuild(keepId) {
    const ids = pool().map(c => c.id);
    if (st.shuffle) {
      for (let i = ids.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [ids[i], ids[j]] = [ids[j], ids[i]]; }
    }
    st.order = ids;
    const k = keepId ? ids.indexOf(keepId) : -1;
    st.pos = k >= 0 ? k : 0;
    st.hint = 0; st.shown = false;
  }
  const cur = () => byId.get(st.order[st.pos]);

  // ---------- study view ----------
  function renderFilters() {
    const dr = $('deck-row');
    dr.querySelectorAll('.chip').forEach(n => n.remove());
    DECKS.forEach(d => {
      const b = document.createElement('button');
      b.className = 'chip'; b.id = 'deck-' + d.id;
      b.setAttribute('aria-pressed', String(st.deck === d.id));
      b.innerHTML = esc(d.label) + ' <span class="ct">' + CARDS.filter(c => d.test(c)).length + '</span>';
      b.onclick = () => { st.deck = d.id; persist(); rebuild(); renderAll(); };
      dr.appendChild(b);
    });
    const sr = $('sec-row');
    sr.querySelectorAll('.chip').forEach(n => n.remove());
    Object.keys(SECS).forEach(k => {
      const b = document.createElement('button');
      b.className = 'chip'; b.id = 'sec-' + k;
      b.setAttribute('aria-pressed', String(st.secs.has(k)));
      b.innerHTML = '<span class="dot" style="background:var(--s-' + k + ', var(--ink-3))"></span>' + esc(SECS[k]) +
        ' <span class="ct">' + CARDS.filter(c => c.sec === k).length + '</span>';
      b.onclick = () => { st.secs.has(k) ? st.secs.delete(k) : st.secs.add(k); persist(); rebuild(); renderAll(); };
      sr.appendChild(b);
    });
    $('order-btn').setAttribute('aria-pressed', String(st.shuffle));
    $('order-btn').textContent = st.shuffle ? 'Shuffled' : 'Shuffle';
  }

  function renderMeter() {
    const p = pool();
    const g = p.filter(c => st.marks[c.id] === 'got').length;
    const h = p.filter(c => st.marks[c.id] === 'hard').length;
    const n = p.length || 1;
    const r = CARDS.filter(c => !live(c)).length;
    $('meter').innerHTML =
      '<span>' + p.length + ' cards</span>' +
      '<span class="track" aria-hidden="true"><i class="g" style="width:' + (100 * g / n) + '%"></i><i class="h" style="width:' + (100 * h / n) + '%"></i></span>' +
      '<span class="leg"><span class="dot" style="background:var(--good)"></span>' + g + ' got it</span>' +
      '<span class="leg"><span class="dot" style="background:var(--hard)"></span>' + h + ' struggling</span>' +
      (r && st.deck !== 'retired' ? '<span class="leg"><span class="dot" style="background:var(--mem)"></span>' + r + ' memorized (hidden)</span>' : '');
  }

  function statusPill(id) {
    if (st.retired.has(id)) return '<span class="status mem">MEMORIZED</span>';
    const m = st.marks[id];
    if (m === 'got') return '<span class="status got">GOT IT</span>';
    if (m === 'hard') return '<span class="status hard">STRUGGLING</span>';
    return '';
  }

  let timerCard;
  function renderStage() {
    const stage = $('stage');
    const c = cur();
    if (Timer && (c ? c.id : null) !== timerCard) { timerCard = c ? c.id : null; Timer.setCard(c ? c.time : null); }
    $('view-study').classList.toggle('editing', st.editing && !!c);
    if (st.editing && c) {
      // Keep an open editor as it is when something else re-renders (e.g. coming back from another tab).
      if (stage.dataset.editing !== c.id) {
        stage.dataset.editing = c.id;
        window.PrepEditor.open(stage, c.id, { onSave: onEdited, onCancel: () => { st.editing = false; renderStage(); } });
      }
      return;
    }
    st.editing = false;
    delete stage.dataset.editing;
    if (!c) {
      const msg = st.deck === 'hard'
        ? ['No struggling cards here yet', 'Press Struggling on any card you are unsure of while studying. Those cards collect in this deck.']
        : st.deck === 'todo'
          ? ['Everything in this selection is marked Got it', 'Pick another deck or section, or clear your marks to start over.']
          : st.deck === 'retired'
            ? ['No memorized cards yet', 'Press Memorized (3) on a card you always get right. It leaves your other decks and waits here until you bring it back.']
            : ['No cards match', 'Turn off a section filter or pick another deck.'];
      stage.innerHTML = '<div class="empty"><h2>' + msg[0] + '</h2><p>' + msg[1] + '</p><button class="btn primary" id="go-all">Study all cards</button></div>';
      $('go-all').onclick = () => { st.deck = 'all'; st.secs.clear(); persist(); rebuild(); renderAll(); };
      return;
    }
    let slots = '';
    for (let i = 0; i < c.n; i++) {
      let inner = '<span class="blank">point ' + (i + 1) + '</span>';
      if (st.hint >= 2) {
        const kws = c.hint2[i] || [];
        inner = kws.length ? '<span class="kw">' + kws.map(k => '<span>' + k + '</span>').join('') + '</span>' : '<span class="lead">' + c.hint1[i] + '</span>';
      } else if (st.hint === 1) {
        inner = '<span class="lead">' + c.hint1[i] + '</span>';
      }
      slots += '<li class="slot"><span class="num">' + (i + 1) + '</span><span class="txt">' + inner + '</span></li>';
    }
    const hintLabel = st.hint === 1 ? 'More hint' : 'Hint';
    const retired = st.retired.has(c.id);
    stage.innerHTML =
      '<article class="card" aria-live="polite">' +
        '<div class="card-top"><span class="sec" style="color:var(--s-' + c.sec + ', var(--ink-2))"><span class="dot" style="background:var(--s-' + c.sec + ', var(--ink-3))"></span>' + esc(c.tag) + '</span>' +
        '<span class="cid">' + esc(c.id) + '</span>' + (c.star ? '<span class="must">★ MUST-KNOW</span>' : '') +
        (c.time ? '<span class="tchip" title="Recommended answer time (range)">' + fmtTime(c.time) + '</span>' : '') +
        '<span class="top-r">' + statusPill(c.id) +
          (Store.server && window.PrepEditor ? '<button class="ebtn" id="b-edit" title="Edit this card">Edit <kbd>E</kbd></button>' : '') + '</span></div>' +
        '<div class="front"><h1 class="prompt">' + c.prompt + '</h1>' +
          '<div class="pts">Hit <b>' + c.n + '</b> point' + (c.n === 1 ? '' : 's') + '</div>' +
          (st.shown ? '' : '<ol class="slots">' + slots + '</ol>') + '</div>' +
        (st.shown ? '<div class="answer">' + c.answer + '</div>' : '') +
        '<div class="ctrl">' +
          (st.shown
            ? '<button class="btn hard" id="b-hard">Struggling <kbd>1</kbd></button><button class="btn good" id="b-got">Got it <kbd>2</kbd></button>'
            : '<button class="btn" id="b-hint"' + (st.hint >= 2 ? ' disabled' : '') + '>' + hintLabel + ' <kbd>H</kbd></button><button class="btn primary" id="b-show">Reveal answer <kbd>Space</kbd></button>') +
          '<span class="spacer"></span><button class="btn mem" id="b-mem" title="' +
            (retired ? 'Put this card back in your decks' : 'You always get this one: hide it from your decks (you can bring it back)') + '">' +
            (retired ? 'Bring back' : 'Memorized') + ' <kbd>3</kbd></button>' +
        '</div>' +
      '</article>' +
      '<div class="nav"><button class="btn" id="b-prev"' + (st.pos === 0 ? ' disabled' : '') + '>← Previous</button>' +
      '<span class="pos">' + (st.pos + 1) + ' / ' + st.order.length + '</span>' +
      '<button class="btn" id="b-next"' + (st.pos >= st.order.length - 1 ? ' disabled' : '') + '>Next →</button></div>';
    const on = (id, f) => { const n = $(id); if (n) n.onclick = f; };
    on('b-hint', hint); on('b-show', reveal); on('b-hard', () => mark('hard')); on('b-got', () => mark('got'));
    on('b-mem', retire); on('b-edit', edit);
    on('b-prev', () => go(-1)); on('b-next', () => go(1));
    stage.querySelectorAll('img.fig').forEach(im => { im.onclick = () => zoom(im.src); });
  }

  function hint() { if (!cur() || st.shown) return; st.hint = Math.min(2, st.hint + 1); renderStage(); }
  function reveal() { if (!cur()) return; st.shown = true; if (Timer) Timer.pause(); renderStage(); }
  function go(d) {
    const np = st.pos + d;
    if (np < 0 || np >= st.order.length) return;
    st.pos = np; st.hint = 0; st.shown = false; renderStage();
    window.scrollTo({ top: 0, behavior: 'auto' });
  }
  function mark(m) {
    const c = cur(); if (!c) return;
    st.marks[c.id] = m; persist();
    moveOn(c);
  }
  // Memorized: move the card to (or back from) the Memorized deck, with an Undo.
  function retire() {
    const c = cur(); if (!c) return;
    const pos = st.pos, was = st.retired.has(c.id);
    was ? st.retired.delete(c.id) : st.retired.add(c.id);
    persist();
    moveOn(c);
    toast(was ? c.id + ' is back in your decks' : c.id + ' moved to Memorized', () => {
      was ? st.retired.add(c.id) : st.retired.delete(c.id);
      persist();
      if (pool().some(x => x.id === c.id) && !st.order.includes(c.id)) st.order.splice(Math.min(pos, st.order.length), 0, c.id);
      const k = st.order.indexOf(c.id);
      if (k >= 0) st.pos = k;
      st.hint = 0; st.shown = false;
      renderAll();
    });
  }
  function edit() { if (!cur() || !Store.server || !window.PrepEditor) return; hideToast(); st.editing = true; renderStage(); }
  function onEdited(card) {
    const i = CARDS.findIndex(x => x.id === card.id);
    if (i >= 0) CARDS[i] = card;
    byId.set(card.id, card);
    st.editing = false;
    timerCard = undefined;  // pick up a changed answer time
    renderAll();
    toast(card.id + ' saved to cue_cards.md');
  }
  let toastTimer = null;
  function toast(text, undo) {
    $('toast-msg').textContent = text;
    const b = $('toast-undo');
    b.hidden = !undo;
    b.onclick = () => { hideToast(); if (undo) undo(); };
    $('toast').hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(hideToast, 6000);
  }
  function hideToast() { clearTimeout(toastTimer); $('toast').hidden = true; }
  function moveOn(c) {
    const stays = pool().some(x => x.id === c.id);
    if (!stays) {
      // The card left this deck (e.g. marked Got it in "Not got yet"): drop it and stay at this position.
      st.order.splice(st.pos, 1);
      if (st.pos >= st.order.length) st.pos = Math.max(0, st.order.length - 1);
    } else if (st.pos < st.order.length - 1) {
      st.pos += 1;
    }
    st.hint = 0; st.shown = false;
    renderFilters(); renderMeter(); renderStage();
    window.scrollTo({ top: 0, behavior: 'auto' });
  }

  // ---------- all cards view ----------
  function renderList() {
    const g = CARDS.filter(c => live(c) && st.marks[c.id] === 'got').length;
    const h = CARDS.filter(c => live(c) && st.marks[c.id] === 'hard').length;
    const r = CARDS.filter(c => !live(c)).length;
    $('list-summary').textContent = CARDS.length + ' cards · ' + g + ' got it · ' + h + ' struggling · ' + r + ' memorized. Click a card to study it.';
    let out = '';
    Object.keys(SECS).forEach(k => {
      const cs = CARDS.filter(c => c.sec === k);
      out += '<h2><span class="dot" style="background:var(--s-' + k + ', var(--ink-3))"></span>' + esc(SECS[k]) + ' <span class="ct">' + cs.length + '</span></h2><div class="rows">';
      cs.forEach(c => {
        out += '<button class="row" data-id="' + esc(c.id) + '"><span class="rid">' + esc(c.id) + '</span><span class="rp">' + c.prompt +
          ' <span class="cid">(' + c.n + ')</span></span><span class="rs">' + (c.star ? '<span class="must">★</span>' : '') + statusPill(c.id) + '</span></button>';
      });
      out += '</div>';
    });
    $('list-body').innerHTML = out;
    $('list-body').querySelectorAll('.row').forEach(r => {
      r.onclick = () => {
        if (st.editing) return;
        st.deck = st.retired.has(r.dataset.id) ? 'retired' : 'all';
        st.secs.clear(); persist(); rebuild(r.dataset.id); setView('study');
      };
    });
  }

  // ---------- sheets view ----------
  function renderSheets() {
    const sheets = DATA.sheets || [];
    const tabs = $('sheet-tabs');
    const body = $('sheet-body');
    tabs.innerHTML = '';
    if (!sheets.length) { body.innerHTML = '<p>No sheets in this deck.</p>'; return; }
    if (st.sheet >= sheets.length) st.sheet = 0;
    sheets.forEach((s, i) => {
      const b = document.createElement('button');
      b.className = 'chip'; b.id = 'sheet-' + i;
      b.setAttribute('aria-pressed', String(i === st.sheet));
      b.textContent = s.title.replace(/^Sheet (\d+) · /, '$1 · ').split(':')[0];
      b.onclick = () => { st.sheet = i; persist(); renderSheets(); };
      tabs.appendChild(b);
    });
    const s = sheets[st.sheet];
    body.innerHTML = '<h1>' + esc(s.title) + '</h1>' + s.html;
    body.querySelectorAll('table').forEach(t => { const w = document.createElement('div'); w.className = 'tablewrap'; t.parentNode.insertBefore(w, t); w.appendChild(t); });
    body.querySelectorAll('img.fig').forEach(im => { im.onclick = () => zoom(im.src); });
  }

  // ---------- figure lightbox ----------
  function zoom(src) { $('lb-img').src = src; $('lb').hidden = false; }
  function unzoom() { $('lb').hidden = true; $('lb-img').removeAttribute('src'); }
  $('lb').onclick = unzoom;

  // ---------- views, buttons, keys ----------
  function setView(v) {
    st.view = v;
    ['study', 'list', 'sheets'].forEach(x => {
      $('view-' + x).hidden = x !== v;
      $('tab-' + x).setAttribute('aria-selected', String(x === v));
    });
    $('timer').hidden = v !== 'study';
    if (v === 'study') renderAll();
    if (v === 'list') renderList();
    if (v === 'sheets') renderSheets();
    window.scrollTo({ top: 0, behavior: 'auto' });
  }
  document.querySelectorAll('.tab').forEach(t => { t.onclick = () => setView(t.dataset.view); });

  $('order-btn').onclick = () => { st.shuffle = !st.shuffle; persist(); rebuild(); renderAll(); };
  let armed = false, armTimer = null;
  $('reset-btn').onclick = () => {
    const b = $('reset-btn');
    if (!armed) {
      armed = true; b.textContent = 'Click again to clear all marks'; b.setAttribute('aria-pressed', 'true');
      armTimer = setTimeout(() => { armed = false; b.textContent = 'Clear my marks'; b.setAttribute('aria-pressed', 'false'); }, 3500);
      return;
    }
    clearTimeout(armTimer);
    armed = false; st.marks = {}; persist(); rebuild(); renderAll();  // Memorized cards stay memorized
    b.textContent = 'Marks cleared'; b.setAttribute('aria-pressed', 'false');
  };

  document.addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input, textarea')) return;
    if (!$('lb').hidden) { if (e.key === 'Escape') unzoom(); return; }
    if (st.view !== 'study' || st.editing || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === ' ' || e.key === 'Enter') {
      if (e.target.tagName === 'BUTTON' && e.key === 'Enter') return;
      e.preventDefault(); if (!st.shown) reveal();
    } else if (e.key === 'h' || e.key === 'H') hint();
    else if (e.key === '1' && st.shown) mark('hard');
    else if (e.key === '2' && st.shown) mark('got');
    else if (e.key === '3') retire();
    else if ((e.key === 'e' || e.key === 'E') && $('b-edit')) { e.preventDefault(); edit(); }
    else if ((e.key === 't' || e.key === 'T') && Timer) Timer.toggle();
    else if ((e.key === 'r' || e.key === 'R') && Timer) Timer.reset();
    else if (e.key === 'ArrowRight') go(1);
    else if (e.key === 'ArrowLeft') go(-1);
  });

  function renderAll() { renderFilters(); renderMeter(); renderStage(); if (Timer) Timer.place(); }
  rebuild();
  renderAll();
})();
