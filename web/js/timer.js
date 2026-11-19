// Interview Prepper: the answer stopwatch on the side of the Study view.
// app.js drives it: setCard() when a new card opens (sets the target, resets if "Reset on new card" is on),
// pause() on reveal, toggle()/reset() from the T and R keys. Settings are saved with your marks.
window.PrepTimer = (function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const opts = { autoReset: true, chime: false, def: 90 };
  let running = false, startAt = 0, acc = 0, iv = null, card = null, chimed = false, hitShown = false;
  let onChange = () => {};
  let audio = null;

  const fmt = sec => { sec = Math.max(0, Math.floor(sec)); return Math.floor(sec / 60) + ':' + String(sec % 60).padStart(2, '0'); };
  const elapsed = () => (acc + (running ? performance.now() - startAt : 0)) / 1000;

  // The card's time, or the default target with a band of ±15% around it.
  function goal() {
    if (card && card.target) {
      const t = card.target;
      return { target: t, min: card.min != null ? card.min : Math.round(t * 0.85), max: card.max != null ? card.max : Math.round(t * 1.15), own: true };
    }
    const t = opts.def;
    return { target: t, min: Math.round(t * 0.85), max: Math.round(t * 1.15), own: false };
  }

  function chime() {
    try {
      const A = window.AudioContext || window.webkitAudioContext;
      audio = audio || new A();
      const o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime;
      o.frequency.value = 880;
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(0.25, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.6);
      o.connect(g); g.connect(audio.destination);
      o.start(t); o.stop(t + 0.65);
    } catch (e) { /* no audio available */ }
  }

  function draw() {
    const root = $('timer');
    if (!root) return;
    const s = elapsed(), g = goal();
    const scale = g.max * 1.2;
    $('t-read').textContent = fmt(s);
    $('t-fill').style.width = Math.min(100, 100 * s / scale) + '%';
    $('t-band').style.left = (100 * g.min / scale) + '%';
    $('t-band').style.width = (100 * (g.max - g.min) / scale) + '%';
    $('t-tick').style.left = (100 * g.target / scale) + '%';
    const phase = s >= g.max ? 'over' : s >= g.min ? 'ok' : 'early';
    root.dataset.phase = s > 0 ? phase : 'idle';
    root.dataset.running = String(running);
    $('t-target').textContent = (g.own ? 'Target ' : 'Default ') + fmt(g.target) + ' · ' + fmt(g.min) + '–' + fmt(g.max);
    $('t-go').firstChild.textContent = running ? 'Pause ' : (s > 0 ? 'Resume ' : 'Start ');
    if (s >= g.target && !hitShown) {
      hitShown = true;
      root.classList.remove('hit'); void root.offsetWidth; root.classList.add('hit');
    }
    if (s >= g.max && !chimed && running) { chimed = true; if (opts.chime) chime(); }
  }

  function start() { if (running) return; running = true; startAt = performance.now(); clearInterval(iv); iv = setInterval(draw, 100); draw(); }
  function pause() { if (!running) return; acc += performance.now() - startAt; running = false; clearInterval(iv); draw(); }
  function toggle() { running ? pause() : start(); }
  function reset() { running = false; acc = 0; chimed = false; hitShown = false; clearInterval(iv); $('timer').classList.remove('hit'); draw(); }

  function setCard(time) {
    card = time || null;
    if (opts.autoReset) reset(); else draw();
  }

  // Wide screens: the panel sits beside the card, level with its top, and sticks below the header on scroll.
  const wide = window.matchMedia('(min-width: 1280px)');
  function place() {
    const root = $('timer'), stage = $('stage'), bar = document.querySelector('.bar');
    if (!root) return;
    if (!wide.matches || !stage) { root.style.top = ''; return; }
    const minTop = (bar ? bar.getBoundingClientRect().bottom : 0) + 16;
    root.style.top = Math.max(minTop, stage.getBoundingClientRect().top) + 'px';
  }
  window.addEventListener('scroll', place, { passive: true });
  window.addEventListener('resize', place);

  function init(saved, changed) {
    if (saved && typeof saved === 'object') {
      if (typeof saved.autoReset === 'boolean') opts.autoReset = saved.autoReset;
      if (typeof saved.chime === 'boolean') opts.chime = saved.chime;
      if (saved.def > 0) opts.def = Math.round(saved.def);
    }
    onChange = changed || onChange;
    $('t-autoreset').checked = opts.autoReset;
    $('t-chime').checked = opts.chime;
    $('t-default').value = opts.def;
    $('t-go').onclick = toggle;
    $('t-reset').onclick = reset;
    $('t-autoreset').onchange = e => { opts.autoReset = e.target.checked; onChange(); };
    $('t-chime').onchange = e => { opts.chime = e.target.checked; if (opts.chime) chime(); onChange(); };
    $('t-default').onchange = e => {
      const v = Math.round(Number(e.target.value));
      if (v >= 5 && v <= 1800) { opts.def = v; onChange(); draw(); } else e.target.value = opts.def;
    };
    draw();
  }

  return { init, setCard, start, pause, toggle, reset, place, fmt, options: () => ({ ...opts }) };
})();
