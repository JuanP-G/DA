/* Utilidades comunes: reproductor paso a paso y panel de código. */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const SVGNS = 'http://www.w3.org/2000/svg';
function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function esc(s) { return String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }

/* Panel de código C++ con coloreado sencillo y líneas resaltables (numeradas desde 1). */
function mountCode(host, fname, lines) {
  const kws = /^(for|if|else|while|return|const|class|struct|public|private|protected|void|bool|int|auto|true|false|template|typename|using|throw|new|delete|break|continue|static|nullptr)$/;
  const tys = /^(Link|Set|Grafo|Digrafo|IndexPQ|Par|vector|queue|stack|string|T|std|Adys|Comparator|TreeNode|size_t)$/;
  const tok = /(\/\/.*$)|("[^"]*")|(\b\d+\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)/g;
  host.classList.add('codebox');
  host.innerHTML = '<div class="fname">' + esc(fname) + '</div>';
  const rows = lines.map((src, i) => {
    let html = '', m; tok.lastIndex = 0;
    while ((m = tok.exec(src))) {
      const t = m[0];
      if (m[1]) html += '<span class="c">' + esc(t) + '</span>';
      else if (m[2]) html += '<span class="s">' + esc(t) + '</span>';
      else if (m[3]) html += '<span class="n">' + t + '</span>';
      else if (m[4] && kws.test(t)) html += '<span class="k">' + t + '</span>';
      else if (m[4] && tys.test(t)) html += '<span class="t">' + t + '</span>';
      else html += esc(t);
    }
    const d = document.createElement('div');
    d.className = 'ln'; d.innerHTML = '<i>' + (i + 1) + '</i><span>' + html + '</span>';
    host.appendChild(d);
    return d;
  });
  return function mark(active) {
    const set = new Set(active || []);
    rows.forEach((r, i) => r.classList.toggle('on', set.has(i + 1)));
    const first = rows.find((r, i) => set.has(i + 1));
    if (first) {
      const top = first.offsetTop, h = host.clientHeight;
      if (top < host.scrollTop + 20 || top > host.scrollTop + h - 40) host.scrollTop = Math.max(0, top - h / 3);
    }
  };
}

/* Reproductor: frames = [{ msg: 'html', lines: [nº de línea de código], ... }]
   render(frame, prevFrame) lo implementa cada página. */
class Player {
  constructor({ render, mark }) {
    this.render = render; this.mark = mark; this.frames = []; this.i = 0; this.timer = null;
    this.$prev = $('#pPrev'); this.$next = $('#pNext'); this.$play = $('#pPlay'); this.$first = $('#pFirst'); this.$last = $('#pLast');
    this.$speed = $('#pSpeed'); this.$count = $('#pCount'); this.$msg = $('#msg'); this.$seek = $('#pSeek');
    this.$prev.onclick = () => { this.pause(); this.go(this.i - 1); };
    this.$next.onclick = () => { this.pause(); this.go(this.i + 1); };
    this.$first.onclick = () => { this.pause(); this.go(0); };
    this.$last.onclick = () => { this.pause(); this.go(this.frames.length - 1); };
    this.$play.onclick = () => this.toggle();
    this.$seek.oninput = () => { this.pause(); this.go(+this.$seek.value); };
    document.addEventListener('keydown', e => {
      if (/INPUT|SELECT|TEXTAREA/.test((e.target.tagName || ''))) return;
      if (e.key === 'ArrowRight') { this.pause(); this.go(this.i + 1); }
      else if (e.key === 'ArrowLeft') { this.pause(); this.go(this.i - 1); }
      else if (e.key === ' ') { e.preventDefault(); this.toggle(); }
    });
  }
  delay() { return [1900, 1300, 900, 550, 280][(+this.$speed.value || 3) - 1]; }
  /* Carga una secuencia nueva. start = frame inicial; play = arrancar solo. */
  load(frames, { play = true, start = 0 } = {}) {
    this.pause(); this.frames = frames; this.$seek.max = Math.max(0, frames.length - 1);
    this.prevFrame = null; this.go(start, true);
    if (play && frames.length > 1) this.play();
  }
  go(i, instant) {
    if (!this.frames.length) return;
    i = Math.max(0, Math.min(this.frames.length - 1, i));
    const f = this.frames[i], prev = this.frames[this.i] || null;
    this.i = i;
    this.render(f, prev, !!instant);
    this.$msg.innerHTML = f.msg || '';
    if (this.mark) this.mark(f.lines || []);
    this.$count.textContent = 'paso ' + (i + 1) + ' de ' + this.frames.length;
    this.$seek.value = i;
    this.$first.disabled = this.$prev.disabled = i === 0;
    this.$last.disabled = this.$next.disabled = i === this.frames.length - 1;
    if (i === this.frames.length - 1) this.pause();
  }
  play() {
    if (this.i >= this.frames.length - 1) this.go(0, true);
    this.$play.textContent = '⏸ Pausa'; this.$play.classList.add('on');
    const tick = () => {
      if (this.i >= this.frames.length - 1) { this.pause(); return; }
      this.go(this.i + 1);
      if (this.timer !== null) this.timer = setTimeout(tick, this.delay());
    };
    this.timer = setTimeout(tick, this.delay());
  }
  pause() { if (this.timer) clearTimeout(this.timer); this.timer = null; this.$play.textContent = '▶ Reproducir'; this.$play.classList.remove('on'); }
  toggle() { this.timer ? this.pause() : this.play(); }
}
const PLAYER_HTML = `
<div class="player">
  <div class="msg" id="msg" role="status" aria-live="polite"></div>
  <div class="row">
    <button class="btn" id="pFirst" title="Primer paso" aria-label="Primer paso">⏮</button>
    <button class="btn" id="pPrev" title="Paso anterior (←)" aria-label="Paso anterior">◀</button>
    <button class="btn primary" id="pPlay">▶ Reproducir</button>
    <button class="btn" id="pNext" title="Paso siguiente (→)" aria-label="Paso siguiente">▶|</button>
    <button class="btn" id="pLast" title="Último paso" aria-label="Último paso">⏭</button>
    <label>velocidad <input type="range" id="pSpeed" min="1" max="5" value="3"></label>
    <span class="count" id="pCount"></span>
  </div>
  <input type="range" id="pSeek" min="0" max="0" value="0" aria-label="Posición en la secuencia" style="width:100%">
</div>`;
