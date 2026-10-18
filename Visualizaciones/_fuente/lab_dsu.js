
/* ================== Laboratorio de conjuntos disjuntos (4 implementaciones) ================== */
const LAB = { v: 'pc', n: 10, p: [], tam: [], id: [], ncj: 10, acc: 0, markFn: null, codeKey: null };
const labSvg = $('#labSvg');
function labReinit(n) {
  LAB.n = n; LAB.p = [...Array(n).keys()]; LAB.tam = Array(n).fill(1); LAB.id = [...Array(n).keys()]; LAB.ncj = n; LAB.acc = 0;
  for (const i of ['#labA', '#labB']) { $(i).max = n - 1; if (+$(i).value > n - 1) $(i).value = n - 1; }
}
const labSnap = () => ({ p: LAB.p.slice(), tam: LAB.tam.slice(), id: LAB.id.slice(), ncj: LAB.ncj, acc: LAB.acc });
const labHints = {
  qf: 'Un vector <code>id[]</code>: <code>buscar</code> es <b>un acceso</b>, pero <code>unir</code> recorre <b>todo</b> el vector (N accesos).',
  qu: 'Un árbol por conjunto con enlaces al padre <code>p[]</code>: <code>unir</code> solo cambia un enlace, pero <code>buscar</code> sube hasta la raíz, y un árbol puede degenerar en una <b>cadena</b> (prueba «Peor caso: cadena»).',
  sz: 'Igual que la unión rápida, pero cuelga la raíz del árbol <b>más pequeño</b> de la del más grande: la altura nunca pasa de log₂N. (En empate esta cabecera cuelga la raíz de <code>a</code> de la de <code>b</code>; las transparencias lo hacen al revés.)',
  pc: 'Lo mismo y además <b>compresión de caminos</b>: <code>buscar</code> deja todos los nodos del camino colgando directamente de la raíz. Es <code>ConjuntosDisjuntos.h</code>, el que usa el juez: coste casi constante (lg* N).',
};
const labCode = () => LAB_CODES[LAB.v];
function labShowCode() {
  const key = LAB.v; if (LAB.codeKey === key) return; LAB.codeKey = key;
  const c = LAB_CODES[key]; LAB.markFn = mountCode($('#labCodeHost'), c.f, c.lines);
}
const LL = (sub, occ = 0) => { let c = -1; const ls = LAB_CODES[LAB.v].lines; for (let i = 0; i < ls.length; i++) if (ls[i].includes(sub)) { c++; if (c === occ) return i + 1; } throw new Error('ancla lab: ' + sub); };
const LLopt = (sub, occ = 0) => { try { return [LL(sub, occ)]; } catch (e) { return []; } };

/* ---- dibujo ---- */
function labLayoutForest(p, tam) {
  const n = p.length, ch = Array.from({ length: n }, () => []);
  const roots = []; for (let i = 0; i < n; i++) { if (p[i] === i) roots.push(i); else ch[p[i]].push(i); }
  const w = {}, depth = {};
  const medir = (v, d) => { depth[v] = d; let s = 0; for (const c of ch[v]) s += medir(c, d + 1); return (w[v] = Math.max(1, s)); };
  let total = 0; for (const r of roots) total += medir(r, 0);
  const maxd = Math.max(...Object.values(depth)), unit = Math.min(64, 600 / Math.max(total, 1)), dy = Math.min(62, 210 / Math.max(maxd, 1));
  const pos = {}; let x0 = 20 + (600 - total * unit) / 2;
  const colocar = (v, x) => { pos[v] = [x + w[v] * unit / 2, 38 + depth[v] * dy]; let cx = x; for (const c of ch[v]) { colocar(c, cx); cx += w[c] * unit; } };
  for (const r of roots) { colocar(r, x0); x0 += w[r] * unit; }
  return { pos, maxd };
}
function labDraw(s, f) {
  labSvg.innerHTML = '';
  const node = (f && f.node) || {}, edge = (f && f.edge) || {};
  const eg = el('g', {}, labSvg), ng = el('g', {}, labSvg);
  const r = Math.min(17, 240 / Math.max(s.p.length, 8));
  if (LAB.v === 'qf') {
    /* grupos por identificador */
    const grupos = new Map(); s.id.forEach((g, i) => { if (!grupos.has(g)) grupos.set(g, []); grupos.get(g).push(i); });
    let x = 16, y = 18; const rowH = 78;
    for (const [g, els] of grupos) {
      const w = els.length * 38 + 14;
      if (x + w > 628) { x = 16; y += rowH; }
      el('rect', { x, y, width: w, height: 62, rx: 10, fill: 'var(--panel-2)', stroke: 'var(--line)' }, eg);
      const t = el('text', { x: x + 7, y: y + 13, 'font-size': 11 }, eg); t.setAttribute('class', 'muted'); t.textContent = 'id = ' + g;
      els.forEach((e, k) => {
        const gg = el('g', { class: 'node ' + (node[e] || ''), transform: `translate(${x + 7 + 17 + k * 38} ${y + 38})` }, ng);
        el('circle', { r: 15 }, gg); const tt = el('text', {}, gg); tt.textContent = e;
      });
      x += w + 10;
    }
  } else {
    const { pos } = labLayoutForest(s.p, s.tam);
    for (let v = 0; v < s.p.length; v++) {
      if (s.p[v] === v) continue;
      const [x1, y1] = pos[v], [x2, y2] = pos[s.p[v]];
      const L = Math.hypot(x2 - x1, y2 - y1) || 1, ux = (x2 - x1) / L, uy = (y2 - y1) / L;
      const g = el('g', { class: 'eg ' + (edge[v] || '') }, eg);
      el('path', { class: 'edge', d: `M${x1 + ux * r} ${y1 + uy * r} L${x2 - ux * r} ${y2 - uy * r}` }, g);
    }
    for (let v = 0; v < s.p.length; v++) {
      const gg = el('g', { class: 'node ' + (node[v] || ''), transform: `translate(${pos[v][0]} ${pos[v][1]})` }, ng);
      el('circle', { r }, gg); const tt = el('text', {}, gg); tt.textContent = v;
      if ((LAB.v === 'sz' || LAB.v === 'pc') && s.p[v] === v) { const k = el('text', { class: 'tg', x: 0, y: -r - 6, style: 'text-anchor:middle;font-size:11px;font-weight:600;fill:var(--accent)' }, gg); k.textContent = 'tam ' + s.tam[v]; }
    }
  }
  /* vectores */
  const host = $('#labVecs'); host.innerHTML = '';
  const blocks = LAB.v === 'qf' ? [vecOf('id', s.id, f && f.hot != null ? f.hot : -1)] : [vecOf('p', s.p, f && f.hot != null ? f.hot : -1)];
  if (LAB.v === 'sz' || LAB.v === 'pc') blocks.push(vecOf('tam (vale en las raíces)', s.tam, -1));
  for (const blk of blocks) {
    const d = document.createElement('div');
    d.innerHTML = '<div class="note" style="margin-bottom:3px"><code>' + esc(blk.name) + '</code></div>';
    const v = document.createElement('div'); v.className = 'vec';
    blk.vals.forEach((x, i) => { const c = document.createElement('div'); c.className = 'c' + (f && f.cells && f.cells.includes(i) ? ' hot' : ''); c.innerHTML = '<i>' + i + '</i><b>' + esc(x) + '</b>'; v.appendChild(c); });
    d.appendChild(v); host.appendChild(d);
  }
  $('#labK1').textContent = s.ncj; $('#labK2').textContent = s.acc;
}
window.labRender = f => labDraw(f.snap, f);
window.labMark = lines => { if (LAB.markFn) LAB.markFn(lines); };
window.labEnter = () => { labShowCode(); labDraw(labSnap(), null); $('#msg').innerHTML = 'Prueba <b>unir</b>, <b>unidos</b>, <b>buscar</b> o <b>cardinal</b>, o carga la <b>autoevaluación 6.1</b>.'; $('#labHint').innerHTML = labHints[LAB.v]; LAB.markFn && LAB.markFn([]); };

/* ---- operaciones: cada una devuelve frames y deja LAB en el estado final ---- */
function labFrames() {
  const f = [];
  return { f, push(msg, lines, extra) { f.push({ msg, lines, snap: labSnap(), ...(extra || {}) }); } };
}
/* sube desde a hasta la raíz; devuelve camino */
function camino(a) { const c = [a]; while (LAB.p[c[c.length - 1]] !== c[c.length - 1]) c.push(LAB.p[c[c.length - 1]]); return c; }
function nodesOf(path, root) { const o = {}; path.forEach(x => { o[x] = 's-vis'; }); o[path[0]] = 's-cur'; o[root] = 's-done'; return o; }
function edgesOf(path) { const o = {}; for (let i = 0; i + 1 < path.length; i++) o[path[i]] = 'tree'; return o; }

/* buscar(a) en las variantes con árboles; con compresión rehace los enlaces. Devuelve la raíz. */
function labBuscar(a, F, quien) {
  if (LAB.v === 'qf') {
    LAB.acc += 1;
    F.push(`<code>${quien}</code>: en búsqueda rápida es <b>un solo acceso</b>: <code>id[${a}] = ${LAB.id[a]}</code>.`, LLopt('int buscar(int a) const'), { node: { [a]: 's-cur' }, cells: [a], hot: a });
    return LAB.id[a];
  }
  const path = camino(a), root = path[path.length - 1], pasos = path.length - 1;
  LAB.acc += path.length;
  const pas = pasos === 0 ? `${a} ya es una raíz (<code>p[${a}] = ${a}</code>): 1 acceso.` : `se sube por los enlaces <code>p[]</code>: ${path.join(' → ')}; la raíz es <b>${root}</b> (${pasos} paso${pasos === 1 ? '' : 's'}).`;
  if (LAB.v === 'pc') {
    F.push(`<code>${quien}</code>: ${pas}`, [...LLopt('if (p.at(a) == a)'), ...(pasos ? LLopt('return p[a] = buscar(p[a]);') : LLopt('return a;'))], { node: nodesOf(path, root), edge: edgesOf(path), cells: path });
    const cambia = path.filter(x => x !== root && LAB.p[x] !== root);
    if (cambia.length) {
      cambia.forEach(x => { LAB.p[x] = root; });
      F.push(`<b>Compresión de caminos</b>: al volver de la recursión, <code>p[x] = buscar(p[x])</code> deja ${cambia.join(', ')} colgando <b>directamente de la raíz ${root}</b>. La próxima vez, buscar costará un paso.`, LLopt('return p[a] = buscar(p[a]);'), { node: nodesOf([path[0]], root), edge: Object.fromEntries(cambia.map(x => [x, 'new'])), cells: cambia });
    }
  } else {
    F.push(`<code>${quien}</code>: ${pas}`, LLopt('while (p.at(a) != a) a = p[a];'), { node: nodesOf(path, root), edge: edgesOf(path), cells: path });
  }
  return root;
}

function labUnir(a, b) {
  const F = labFrames(), v = LAB.v, N = LAB.n;
  F.push(`<code>unir(${a}, ${b})</code> con ${v === 'qf' ? 'búsqueda rápida' : v === 'qu' ? 'unión rápida' : v === 'sz' ? 'unión por tamaños' : 'unión por tamaños + compresión'}.`, [], { node: { [a]: 's-cur', [b]: 's-cur' } });
  if (v === 'qf') {
    const ia = labBuscar(a, F, `int ia = buscar(${a})`), ib = labBuscar(b, F, `int ib = buscar(${b})`);
    if (ia === ib) { F.push(`<code>ia == ib</code> (${ia}): ya estaban en el mismo conjunto, no hay nada que hacer.`, LL('if (ia == ib) return;') ? [LL('if (ia == ib) return;')] : [], { node: { [a]: 's-done', [b]: 's-done' } }); return F.f; }
    const cambian = []; LAB.id.forEach((x, k) => { if (x === ia) cambian.push(k); });
    LAB.acc += N;
    F.push(`Hay que <b>recorrer todo el vector</b> (${N} accesos) y cambiar cada <code>id[k] == ${ia}</code> por <code>${ib}</code>: cambian ${cambian.join(', ')}.`, [LL('for (int k = 0; k < (int)id.size(); ++k)'), LL('if (id[k] == ia) id[k] = ib;')], { node: Object.fromEntries(cambian.map(k => [k, 's-cur'])), cells: cambian });
    cambian.forEach(k => { LAB.id[k] = ib; }); LAB.ncj--;
    F.push(`Listo: ${LAB.id.filter(x => x === ib).length} elementos con <code>id = ${ib}</code>. <code>--ncjtos</code> → ${LAB.ncj} conjuntos. Coste de esta unión: O(N).`, [LL('--ncjtos;')], { node: Object.fromEntries(cambian.map(k => [k, 's-done'])), cells: cambian });
    return F.f;
  }
  const i = labBuscar(a, F, `int i = buscar(${a})`), j = labBuscar(b, F, `int j = buscar(${b})`);
  if (i === j) { F.push(`<code>i == j</code> (${i}): ${a} y ${b} <b>ya están en el mismo conjunto</b>; <code>unir</code> no hace nada.`, LLopt('if (i == j) return;'), { node: { [i]: 's-done' } }); return F.f; }
  if (v === 'qu') {
    LAB.p[i] = j; LAB.ncj--;
    F.push(`Raíces distintas (${i} y ${j}): <code>p[${i}] = ${j}</code>. <b>La raíz de a cuelga de la de b</b>, aunque su árbol sea mucho más grande. Un solo enlace cambia.`, [...LLopt('p[i] = j;'), ...LLopt('--ncjtos;')], { node: { [i]: 's-cur', [j]: 's-done' }, edge: { [i]: 'new' }, cells: [i] });
    return F.f;
  }
  const ti = LAB.tam[i], tj = LAB.tam[j];
  if (ti > tj) {
    LAB.tam[i] += tj; LAB.p[j] = i; LAB.ncj--;
    F.push(`<code>tam[${i}] = ${ti} &gt; tam[${j}] = ${tj}</code>: el árbol de ${i} es el mayor. <b>${j} cuelga de ${i}</b> y <code>tam[${i}] = ${LAB.tam[i]}</code>.`, [...LLopt('if (tam[i] > tam[j])'), ...LLopt('tam[i] += tam[j]; p[j] = i;'), ...LLopt('--ncjtos;')], { node: { [j]: 's-cur', [i]: 's-done' }, edge: { [j]: 'new' }, cells: [j, i] });
  } else {
    LAB.tam[j] += ti; LAB.p[i] = j; LAB.ncj--;
    F.push(`<code>tam[${i}] = ${ti} ${ti === tj ? '=' : '&lt;'} tam[${j}] = ${tj}</code>: ${ti === tj ? 'empate; esta cabecera hace el <code>else</code>' : 'el árbol de ' + j + ' es el mayor'}. <b>${i} cuelga de ${j}</b> y <code>tam[${j}] = ${LAB.tam[j]}</code>.`, [...LLopt('if (tam[i] > tam[j])'), ...LLopt('tam[j] += tam[i]; p[i] = j;'), ...LLopt('--ncjtos;')], { node: { [i]: 's-cur', [j]: 's-done' }, edge: { [i]: 'new' }, cells: [i, j] });
  }
  return F.f;
}
function labUnidos(a, b) {
  const F = labFrames();
  F.push(`<code>unidos(${a}, ${b})</code> = <code>buscar(${a}) == buscar(${b})</code>.`, LLopt('bool unidos(int a, int b) const'), { node: { [a]: 's-cur', [b]: 's-cur' } });
  const ra = labBuscar(a, F, `buscar(${a})`), rb = labBuscar(b, F, `buscar(${b})`);
  F.push(`${ra} ${ra === rb ? '=' : '≠'} ${rb}: <b>${ra === rb ? 'true, están en el mismo conjunto' : 'false, conjuntos distintos'}</b>.`, LLopt('bool unidos(int a, int b) const'), { node: { [a]: ra === rb ? 's-done' : 's-red', [b]: ra === rb ? 's-done' : 's-red' } });
  return F.f;
}
function labBusca(a) {
  const F = labFrames();
  const r = labBuscar(a, F, `buscar(${a})`);
  F.push(`<code>buscar(${a})</code> devuelve <b>${r}</b>: el representante del conjunto de ${a}.`, [], { node: { [a]: 's-cur', [r]: 's-done' } });
  return F.f;
}
function labCardinal(a) {
  const F = labFrames();
  if (LAB.v === 'qf' || LAB.v === 'qu') { F.push(`Esta implementación <b>no guarda tamaños</b>: no tiene <code>cardinal()</code>. Habría que contar todos los elementos del conjunto (O(N)). Por eso la versión por tamaños añade el vector <code>tam[]</code>.`, [], { node: { [a]: 's-cur' } }); return F.f; }
  F.push(`<code>cardinal(${a})</code> = <code>tam[buscar(${a})]</code>.`, LLopt('int cardinal(int a) const'), { node: { [a]: 's-cur' } });
  const r = labBuscar(a, F, `buscar(${a})`);
  F.push(`<code>tam[${r}]</code> = <b>${LAB.tam[r]}</b> elementos en el conjunto de ${a}.`, LLopt('int cardinal(int a) const'), { node: { [a]: 's-cur', [r]: 's-done' }, cells: [r] });
  return F.f;
}
function labRun(frames) { labShowCode(); player.load(frames, { play: true }); }
function labInt(id) { const n = +$(id).value; return Math.max(0, Math.min(LAB.n - 1, Number.isFinite(n) ? n : 0)); }
$('#labUnir').onclick = () => labRun(labUnir(labInt('#labA'), labInt('#labB')));
$('#labUnidos').onclick = () => labRun(labUnidos(labInt('#labA'), labInt('#labB')));
$('#labBuscar').onclick = () => labRun(labBusca(labInt('#labA')));
$('#labCard').onclick = () => labRun(labCardinal(labInt('#labA')));
function labSecuencia(pares) {
  const all = [];
  for (const [a, b] of pares) { const fr = labUnir(a, b); all.push(...fr); }
  return all;
}
$('#labSeqRun').onclick = () => {
  const pares = [...$('#labSeq').value.matchAll(/(\d+)\s*[-,–]\s*(\d+)/g)].map(m => [+m[1], +m[2]]).filter(([a, b]) => a < LAB.n && b < LAB.n);
  if (!pares.length) { $('#msg').innerHTML = 'Escribe pares como <code>0-1 2-3 0-2</code> (elementos entre 0 y ' + (LAB.n - 1) + ').'; return; }
  labRun(labSecuencia(pares));
};
function labReset() { labReinit(Math.max(3, Math.min(16, +$('#labN').value || 10))); LAB.codeKey = null; labShowCode(); labDraw(labSnap(), null); player.pause(); player.frames = []; $('#pCount').textContent = ''; $('#msg').innerHTML = 'Estructura reiniciada: ' + LAB.n + ' conjuntos de un elemento.'; $('#labHint').innerHTML = labHints[LAB.v]; LAB.markFn && LAB.markFn([]); }
$('#labReset').onclick = labReset; $('#labN').onchange = labReset;
$('#labVar').onchange = () => { LAB.v = $('#labVar').value; labReset(); };
$('#labAuto').onclick = () => { $('#labN').value = 10; labReinit(10); const pares = [[9, 0], [3, 4], [5, 8], [7, 2], [2, 1], [5, 7], [0, 3], [4, 2]]; $('#labSeq').value = pares.map(p => p.join('-')).join(' '); labRun(labSecuencia(pares)); };
$('#labChain').onclick = () => { const n = Math.max(3, Math.min(16, +$('#labN').value || 10)); labReinit(n); const pares = []; for (let i = 0; i + 1 < n; i++) pares.push([i, i + 1]); $('#labSeq').value = pares.map(p => p.join('-')).join(' '); labRun(labSecuencia(pares)); };
$('#labLegend').innerHTML = '<span><b style="border-color:var(--accent);background:var(--accent-soft)"></b>elemento de la operación</span><span><b style="border-color:var(--blue);background:var(--blue-soft)"></b>camino hacia la raíz</span><span><b style="border-color:var(--green);background:var(--green-soft)"></b>raíz / resultado</span><span><b style="border-color:var(--red);background:var(--red-soft)"></b>conjuntos distintos</span>';

/* ================== Aplicación: manchas de petróleo (06-1) ================== */
const GF = 8, GC = 8, CELL = 42;
const GPAL = ['#f5a623', '#58b2f2', '#4fd1a0', '#ff7468', '#a58cf2', '#ff9f5a', '#4fd1d1', '#f08cc8', '#aac85a', '#8a96ff'];
const Grid = { oil: [], dsu: null, out: [], log: [] };
function gridReset() { Grid.oil = Array(GF * GC).fill(false); Grid.dsu = new DSU(GF * GC); Grid.mayor = 0; Grid.out = [0]; Grid.log = []; }
function gridAdd(i, j, silent) {
  const c = i * GC + j; if (Grid.oil[c]) return;
  Grid.oil[c] = true; const unidos = [];
  for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
    if (!di && !dj) continue; const a = i + di, b = j + dj;
    if (a < 0 || a >= GF || b < 0 || b >= GC || !Grid.oil[a * GC + b]) continue;
    Grid.dsu.unir(c, a * GC + b); unidos.push(a * GC + b);
  }
  Grid.mayor = Math.max(Grid.mayor, Grid.dsu.cardinal(c));
  if (!silent) { Grid.out.push(Grid.mayor); Grid.log.unshift(`celda (${i + 1},${j + 1}) = nº ${c}: ${unidos.length ? 'unir con ' + unidos.join(', ') : 'sin vecinas negras'} → cardinal = ${Grid.dsu.cardinal(c)}, mayor = ${Grid.mayor}`); Grid.log = Grid.log.slice(0, 5); }
}
function gridDraw() {
  const g = $('#gridSvg'); g.innerHTML = '';
  const raiz = c => Grid.dsu.buscar(c), col = new Map();
  for (let i = 0; i < GF; i++) for (let j = 0; j < GC; j++) {
    const c = i * GC + j; const oil = Grid.oil[c];
    let fill = 'var(--panel-2)';
    if (oil) { const r = raiz(c); if (!col.has(r)) col.set(r, GPAL[col.size % GPAL.length]); fill = col.get(r); }
    const r = el('rect', { x: j * CELL, y: i * CELL, width: CELL - 2, height: CELL - 2, rx: 5, fill, stroke: 'var(--line)', 'data-c': c, style: 'cursor:pointer' }, g);
    if (oil && Grid.dsu.cardinal(c) === Grid.mayor) r.setAttribute('stroke', 'var(--ink)'), r.setAttribute('stroke-width', '2');
    if (oil) { const t = el('text', { x: j * CELL + CELL / 2 - 1, y: i * CELL + CELL / 2, 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 11, fill: '#111', 'pointer-events': 'none' }, g); t.textContent = c; }
  }
  const tams = [...col.keys()].map(r => Grid.dsu.tam[r]).sort((a, b) => b - a);
  $('#gridInfo').innerHTML = `Celdas de petróleo: <b>${Grid.oil.filter(Boolean).length}</b> · manchas: <b>${tams.length}</b> ${tams.length ? '(tamaños ' + tams.join(', ') + ')' : ''} · mancha más grande: <b>${Grid.mayor}</b> (borde oscuro).`;
  const o = $('#gridOut'); o.innerHTML = ''; Grid.out.forEach(x => { const c = document.createElement('span'); c.className = 'chip'; c.textContent = x; o.appendChild(c); });
  $('#gridLog').innerHTML = Grid.log.map(esc).join('<br>');
}
$('#gridSvg').addEventListener('click', e => { const r = e.target.closest('rect'); if (!r) return; const c = +r.dataset.c; gridAdd(Math.floor(c / GC), c % GC); gridDraw(); });
const GRID_EJ = ['-#-#---#', '-###--##', '-----###', '-#------', '-#-#----', '-###-##-', '###--##-', '--#-----'];
$('#gridEj').onclick = () => { gridReset(); GRID_EJ.forEach((row, i) => [...row].forEach((ch, j) => { if (ch === '#') gridAdd(i, j, true); })); Grid.out = [Grid.mayor]; Grid.log = ['imagen inicial: cada celda negra se une con sus vecinas negras']; gridDraw(); };
$('#gridEj3').onclick = () => { if (Grid.out.length === 1 && Grid.mayor === 0) $('#gridEj').onclick(); [[6, 8], [2, 5], [6, 5]].forEach(([f, c]) => gridAdd(f - 1, c - 1)); gridDraw(); };
$('#gridClear').onclick = () => { gridReset(); gridDraw(); };
gridReset(); gridDraw();
