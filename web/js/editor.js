// Interview Prepper: edit a card in place. Saves through run.py (PUT api/card/<ID>), which rewrites the card in
// content/cue_cards.md and rebuilds web/data/cards.js. Images go to web/figs/ through POST api/figure.
window.PrepEditor = (function () {
  'use strict';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));
  const POINT = /^(- |\d+\. )/;

  // Mirrors split_back / join_back in scripts/cardfile.py, for switching between the two views.
  function splitBack(back) {
    const lines = back.split('\n');
    const idx = lines.map((l, i) => POINT.test(l) ? i : -1).filter(i => i >= 0);
    if (!idx.length) return { before: back.trim(), points: [], after: '', ordered: false, ok: true };
    const first = idx[0], pts = [];
    let cur = null, last = first;
    for (let i = first; i < lines.length; i++) {
      const ln = lines[i];
      if (POINT.test(ln)) { if (cur !== null) pts.push(cur); cur = ln.replace(POINT, ''); last = i; }
      else if (cur !== null && ln.startsWith('  ') && ln.trim()) { cur += '\n' + ln.trim(); last = i; }
      else if (cur !== null && !ln.trim()) { pts.push(cur); cur = null; }
      else if (ln.trim()) { if (idx.some(j => j > i)) return { ok: false }; break; }
    }
    if (cur !== null) pts.push(cur);
    return { before: lines.slice(0, first).join('\n').trim(), points: pts, after: lines.slice(last + 1).join('\n').trim(), ordered: /^\d/.test(lines[first]), ok: true };
  }
  function joinBack(before, points, after, ordered) {
    const parts = [];
    if (before.trim()) parts.push(before.trim());
    const pts = points.map(p => p.split('\n').map(l => l.trim()).filter(Boolean)).filter(l => l.length)
      .map((l, i) => (ordered ? (i + 1) + '. ' : '- ') + l.join('\n  '));
    if (pts.length) parts.push(pts.join('\n'));
    if (after.trim()) parts.push(after.trim());
    return parts.join('\n\n');
  }
  const countPoints = back => back.split('\n').filter(l => POINT.test(l)).length;

  async function open(host, id, hooks) {
    host.innerHTML = '<div class="card editor"><div class="ed-body"><p class="ed-note">Loading ' + esc(id) + '…</p></div></div>';
    let res;
    try {
      const r = await fetch('api/card/' + encodeURIComponent(id), { cache: 'no-store' });
      res = await r.json();
      if (!r.ok) throw new Error(res.error || r.status);
    } catch (e) {
      host.innerHTML = '<div class="card editor"><div class="ed-body"><p class="ed-err">Could not load ' + esc(id) + ': ' + esc(e.message) +
        '</p></div><div class="ctrl"><button class="btn" id="ed-cancel">Back</button></div></div>';
      host.querySelector('#ed-cancel').onclick = hooks.onCancel;
      return;
    }
    const f = res.fields;
    const t = f.time || {};
    const s = {
      prompt: f.prompt, star: f.star, target: t.target || '', min: t.min == null ? '' : t.min, max: t.max == null ? '' : t.max,
      mode: f.structured ? 'pts' : 'md', before: f.before, points: f.points.slice(), after: f.after, ordered: f.ordered, back: f.back,
    };
    let lastBox = null, busy = false, msg = '', msgErr = false;

    function payload() {
      const out = { prompt: s.prompt.trim(), star: s.star };
      const tv = [s.target, s.min, s.max].map(v => String(v).trim());
      out.time = tv.every(v => !v) ? null : { target: tv[0], min: tv[1], max: tv[2] };
      if (s.mode === 'md') out.back = s.back;
      else Object.assign(out, { before: s.before, points: s.points.filter(p => p.trim()), after: s.after, ordered: s.ordered });
      return out;
    }
    const initial = JSON.stringify(payload());
    const dirty = () => JSON.stringify(payload()) !== initial;

    function check(p) {
      if (!p.prompt) return 'The question can\'t be empty.';
      const n = p.points ? p.points.length : countPoints(p.back);
      if (!n) return 'A card needs at least one point.';
      if (p.time) {
        const [a, lo, hi] = [p.time.target, p.time.min, p.time.max].map(v => v === '' ? null : Number(v));
        if (!(a > 0)) return 'Set a target time in seconds, or clear all three time boxes.';
        if ((lo === null) !== (hi === null)) return 'Give both a min and a max time, or neither.';
        if (lo !== null && !(lo > 0 && lo <= a && a <= hi)) return 'Times must be min ≤ target ≤ max.';
      }
      return '';
    }

    function render(focus) {
      const pts = s.points.map((p, i) =>
        '<li class="ed-pt"><span class="num">' + (s.ordered ? (i + 1) + '.' : (i + 1)) + '</span>' +
        '<textarea class="ed-box" data-pt="' + i + '" rows="2" aria-label="Point ' + (i + 1) + '">' + esc(p) + '</textarea>' +
        '<span class="ed-ptb"><button class="ib" data-up="' + i + '" title="Move up"' + (i === 0 ? ' disabled' : '') + '>↑</button>' +
        '<button class="ib" data-down="' + i + '" title="Move down"' + (i === s.points.length - 1 ? ' disabled' : '') + '>↓</button>' +
        '<button class="ib del" data-del="' + i + '" title="Remove this point">✕</button></span></li>').join('');
      const n = s.mode === 'md' ? countPoints(s.back) : s.points.filter(p => p.trim()).length;
      host.innerHTML =
        '<article class="card editor">' +
          '<div class="card-top"><span class="sec">Editing</span><span class="cid">' + esc(f.id) + ' · ' + esc(f.tag) + '</span>' +
            '<span class="top-r"><span class="ed-n">' + n + ' point' + (n === 1 ? '' : 's') + '</span>' +
            '<button class="chip" id="ed-mode" aria-pressed="' + (s.mode === 'md') + '">Markdown</button></span></div>' +
          '<div class="ed-body">' +
            '<label class="ed-l">Question<input class="ed-in" id="ed-prompt" value="' + esc(s.prompt) + '"></label>' +
            '<div class="ed-row"><label class="ed-chk"><input type="checkbox" id="ed-star"' + (s.star ? ' checked' : '') + '> ★ Must-know</label>' +
              '<span class="ed-time"><span class="ed-tl">Answer time (s)</span>' +
              '<label>target <input class="ed-in num" id="ed-target" inputmode="numeric" value="' + esc(s.target) + '"></label>' +
              '<label>min <input class="ed-in num" id="ed-min" inputmode="numeric" value="' + esc(s.min) + '"></label>' +
              '<label>max <input class="ed-in num" id="ed-max" inputmode="numeric" value="' + esc(s.max) + '"></label></span></div>' +
            (s.mode === 'md'
              ? '<label class="ed-l"><span>Back of the card <small>(markdown: each <code>- </code> or <code>1. </code> line is a point)</small></span>' +
                  '<textarea class="ed-box md" id="ed-back" rows="14">' + esc(s.back) + '</textarea></label>'
              : '<label class="ed-l"><span>Notes before the points <small>(optional, e.g. a mnemonic)</small></span>' +
                  '<textarea class="ed-box" id="ed-before" rows="1">' + esc(s.before) + '</textarea></label>' +
                '<div class="ed-l"><span>Points <small>(<b>**bold**</b> words become the hints)</small></span></div>' +
                '<ol class="ed-pts">' + pts + '</ol>' +
                '<button class="btn" id="ed-add">+ Add point</button>' +
                '<label class="ed-l"><span>Notes after the points <small>(optional, e.g. <i>*Simply:*</i> or a backup story)</small></span>' +
                  '<textarea class="ed-box" id="ed-after" rows="1">' + esc(s.after) + '</textarea></label>') +
            '<div class="ed-row"><button class="btn" id="ed-img">Add image</button><input type="file" id="ed-file" accept="image/png,image/jpeg,image/gif,image/webp" hidden>' +
              '<span class="ed-note">or paste a screenshot into any box. It goes in at the cursor.</span></div>' +
            '<p class="ed-msg' + (msgErr ? ' ed-err' : '') + '" id="ed-msg" role="status">' + esc(msg) + '</p>' +
          '</div>' +
          '<div class="ctrl"><button class="btn" id="ed-cancel">Cancel <kbd>Esc</kbd></button><span class="spacer"></span>' +
            '<button class="btn primary" id="ed-save"' + (busy ? ' disabled' : '') + '>' + (busy ? 'Saving…' : 'Save') + ' <kbd>Ctrl+S</kbd></button></div>' +
        '</article>';
      wire();
      host.querySelectorAll('textarea').forEach(grow);
      if (focus) { const el = host.querySelector(focus); if (el) { el.focus(); const L = el.value.length; el.setSelectionRange(L, L); } }
    }

    function grow(ta) { ta.style.height = 'auto'; ta.style.height = (ta.scrollHeight + 2) + 'px'; }
    function setMsg(text, err) {
      msg = text; msgErr = !!err;
      const el = host.querySelector('#ed-msg');
      if (el) { el.textContent = text; el.classList.toggle('ed-err', !!err); }
    }
    function updCount() {
      const n = s.mode === 'md' ? countPoints(s.back) : s.points.filter(p => p.trim()).length;
      const el = host.querySelector('.ed-n'); if (el) el.textContent = n + ' point' + (n === 1 ? '' : 's');
    }

    function wire() {
      const q = sel => host.querySelector(sel);
      const bind = (sel, key) => { const el = q(sel); if (el) el.oninput = () => { s[key] = el.value; if (el.tagName === 'TEXTAREA') grow(el); updCount(); }; };
      bind('#ed-prompt', 'prompt'); bind('#ed-target', 'target'); bind('#ed-min', 'min'); bind('#ed-max', 'max');
      bind('#ed-before', 'before'); bind('#ed-after', 'after'); bind('#ed-back', 'back');
      q('#ed-star').onchange = e => { s.star = e.target.checked; };
      host.querySelectorAll('[data-pt]').forEach(ta => { ta.oninput = () => { s.points[+ta.dataset.pt] = ta.value; grow(ta); updCount(); }; });
      host.querySelectorAll('textarea').forEach(ta => { ta.onfocus = () => { lastBox = ta; }; });
      host.querySelectorAll('[data-up]').forEach(b => { b.onclick = () => { const i = +b.dataset.up; [s.points[i - 1], s.points[i]] = [s.points[i], s.points[i - 1]]; render('[data-pt="' + (i - 1) + '"]'); }; });
      host.querySelectorAll('[data-down]').forEach(b => { b.onclick = () => { const i = +b.dataset.down; [s.points[i + 1], s.points[i]] = [s.points[i], s.points[i + 1]]; render('[data-pt="' + (i + 1) + '"]'); }; });
      host.querySelectorAll('[data-del]').forEach(b => {
        b.onclick = () => {
          const i = +b.dataset.del;
          if (s.points[i].trim() && !confirm('Remove point ' + (i + 1) + '?\n\n' + s.points[i])) return;
          s.points.splice(i, 1); render();
        };
      });
      const add = q('#ed-add');
      if (add) add.onclick = () => { s.points.push('**Key:** '); render('[data-pt="' + (s.points.length - 1) + '"]'); };
      q('#ed-mode').onclick = () => {
        if (s.mode === 'pts') { s.back = joinBack(s.before, s.points, s.after, s.ordered); s.mode = 'md'; render('#ed-back'); return; }
        const sp = splitBack(s.back);
        if (!sp.ok) { setMsg('Notes sit between points here, so this card can only be edited in the Markdown view.', true); return; }
        Object.assign(s, { before: sp.before, points: sp.points, after: sp.after, ordered: sp.ordered, mode: 'pts' });
        render();
      };
      q('#ed-img').onclick = () => q('#ed-file').click();
      q('#ed-file').onchange = e => { const file = e.target.files[0]; if (file) upload(file, file.name); e.target.value = ''; };
      q('#ed-cancel').onclick = cancel;
      q('#ed-save').onclick = save;
    }

    async function upload(file, name) {
      const box = lastBox && host.contains(lastBox) ? lastBox : host.querySelector(s.mode === 'md' ? '#ed-back' : '#ed-after');
      const at = box.selectionStart != null && box === lastBox ? box.selectionStart : box.value.length;
      setMsg('Uploading ' + (name || 'image') + '…');
      try {
        const r = await fetch('api/figure?name=' + encodeURIComponent(name || f.id + '-figure'),
          { method: 'POST', headers: { 'Content-Type': file.type || 'application/octet-stream' }, body: file });
        const j = await r.json();
        if (!r.ok) throw new Error(j.error || r.status);
        const before = box.value.slice(0, at), after = box.value.slice(at);
        const md = (before && !/\s$/.test(before) ? ' ' : '') + '![](' + j.src + ')';
        box.value = before + md + after;
        box.dispatchEvent(new Event('input'));
        box.focus(); box.setSelectionRange(at + md.length, at + md.length);
        setMsg('Added ' + j.src + '. It shows when you save.');
      } catch (e) { setMsg('Image not added: ' + e.message, true); }
    }

    function cancel() {
      if (busy) return;
      if (dirty() && !confirm('Discard your changes to ' + f.id + '?')) return;
      cleanup(); hooks.onCancel();
    }

    async function save() {
      if (busy) return;
      const p = payload();
      const problem = check(p);
      if (problem) { setMsg(problem, true); return; }
      if (!dirty()) { cleanup(); hooks.onCancel(); return; }
      busy = true; msg = ''; msgErr = false; render();
      try {
        const r = await fetch('api/card/' + encodeURIComponent(f.id), { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) });
        const j = await r.json();
        if (!r.ok) throw new Error(j.error || r.status);
        cleanup(); hooks.onSave(j.card);
      } catch (e) {
        busy = false; msg = (e.message === 'Failed to fetch' ? 'Could not reach run.py. Is it still running?' : e.message); msgErr = true; render();
      }
    }

    function onPaste(e) {
      const items = (e.clipboardData && e.clipboardData.items) || [];
      for (const it of items) {
        if (it.kind === 'file' && it.type.startsWith('image/')) {
          e.preventDefault();
          if (e.target.tagName === 'TEXTAREA') lastBox = e.target;
          upload(it.getAsFile(), f.id + '-screenshot');
          return;
        }
      }
    }
    function onKey(e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S' || e.key === 'Enter')) { e.preventDefault(); save(); }
      else if (e.key === 'Escape') { e.preventDefault(); cancel(); }
    }
    function cleanup() { document.removeEventListener('keydown', onKey, true); host.removeEventListener('paste', onPaste); }
    document.addEventListener('keydown', onKey, true);
    host.addEventListener('paste', onPaste);

    if (!res.editable) {
      host.innerHTML = '<div class="card editor"><div class="ed-body"><p class="ed-err">' + esc(res.reason) +
        '</p></div><div class="ctrl"><button class="btn" id="ed-cancel">Back</button></div></div>';
      host.querySelector('#ed-cancel').onclick = () => { cleanup(); hooks.onCancel(); };
      return;
    }
    render('#ed-prompt');
  }

  return { open };
})();
