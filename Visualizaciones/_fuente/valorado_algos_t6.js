
/* ---- Conjuntos disjuntos EXACTAMENTE como ConjuntosDisjuntos.h (unión por tamaño + compresión) ---- */
class DSU {
  constructor(n) { this.p = [...Array(n).keys()]; this.tam = Array(n).fill(1); this.ncj = n; }
  buscar(a) { if (this.p[a] === a) return a; return (this.p[a] = this.buscar(this.p[a])); }
  unir(a, b) {
    const i = this.buscar(a), j = this.buscar(b);
    if (i === j) return;
    if (this.tam[i] > this.tam[j]) { this.tam[i] += this.tam[j]; this.p[j] = i; }
    else { this.tam[j] += this.tam[i]; this.p[i] = j; }
    this.ncj--;
  }
  unidos(a, b) { return this.buscar(a) === this.buscar(b); }
  cardinal(a) { return this.tam[this.buscar(a)]; }
  conjuntos() {
    const m = new Map();
    for (let v = 0; v < this.p.length; v++) { const r = this.buscar(v); if (!m.has(r)) m.set(r, []); m.get(r).push(v); }
    return [...m.values()];
  }
}
const conjTxt = d => d.conjuntos().map(c => '{' + c.join(',') + '}').join(' ');

/* ---- Kruskal y sus tres usos: ARM_Kruskal, 06-3 (suma), 06-4 (última arista), 06-5 (minimax) ---- */
function kruskal(mode, s, t, par) {
  const n = G.n, C = ctx(), S = C.st, d = new DSU(n);
  const A = {
    clase: { code: 'kruskal', sort: 'std::sort(aristas.begin(), aristas.end());', cd: 'ConjuntosDisjuntos cjtos(g.V());', loop: 'for (auto const& a : aristas) {', uv: 'int v = a.uno(), w = a.otro(v);', test: 'if (!cjtos.unidos(v, w))', unir: 'cjtos.unir(v, w);', acum: ['_ARM.push_back(a);', 'coste += a.valor();'], brk: 'if (_ARM.size() == (size_t)g.V() - 1) break;', brkAfter: true, fin: 'bool conexo() const' },
    suma: { code: 'e63', sort: 'sort(puentes.begin(), puentes.end());', cd: 'ConjuntosDisjuntos cd(g.V());', loop: 'for (auto const& p : puentes) {', uv: 'int u = p.uno(), v = p.otro(u);', test: 'if (!cd.unidos(u, v)) {', unir: 'cd.unir(u, v);', acum: ['coste += p.valor();', '++elegidos;'], brk: 'if (elegidos == g.V() - 1) break;', fin: 'if (elegidos == g.V() - 1) cout << coste' },
    ultima: { code: 'e64', sort: 'sort(saltos.begin(), saltos.end());', cd: 'ConjuntosDisjuntos cd(g.V());', loop: 'for (auto const& s : saltos) {', uv: 'int u = s.uno(), v = s.otro(u);', test: 'if (!cd.unidos(u, v)) {', unir: 'cd.unir(u, v);', acum: ['ultima = s.valor();'], brk: 'if (cd.num_cjtos() == 1) break;', fin: 'if (cd.num_cjtos() == 1) cout << ultima' },
    aero: { code: 'e6L', sort: 'sort(carreteras.begin(), carreteras.end());', cd: 'ConjuntosDisjuntos cd(N);', loop: 'for (auto const& c : carreteras) {', uv: 'int u = c.uno(), v = c.otro(u);', test: 'if (!cd.unidos(u, v)) {', unir: 'cd.unir(u, v);', acum: ['coste += c.valor();'], brk: 'if (c.valor() >= A) break;', fin: 'coste += (long long)aeropuertos * A;' },
    minimax: { code: 'e65', sort: 'sort(galerias.begin(), galerias.end());', cd: 'ConjuntosDisjuntos cd(g.V());', loop: 'for (auto const& a : galerias) {', uv: 'int u = a.uno(), v = a.otro(u);', test: 'if (!cd.unidos(u, v)) {', unir: 'cd.unir(u, v);', acum: ['aguante = a.valor();'], brk: 'if (cd.unidos(origen, destino)) break;', fin: 'if (cd.unidos(origen, destino)) cout << aguante' },
  }[mode];
  const ln = k => L(A.code, A[k]);
  const edges = G.edges.slice().sort((a, b) => a.c - b.c || a.id - b.id);
  const est = {};            /* id -> '' | 'ok' | 'bad' | 'cur' | 'dead' */
  let total = 0, elegidos = 0, ultima = 0;
  const fin = () => mode === 'clase' ? elegidos === n - 1 : mode === 'suma' ? elegidos === n - 1 : mode === 'ultima' ? d.ncj === 1 : d.unidos(s, t);
  const estado = () => mode === 'aero' ? `carreteras construidas = ${total} · grupos (aeropuertos) = ${d.ncj} · A = ${par}` : mode === 'clase' || mode === 'suma' ? `elegidos = ${elegidos} de V − 1 = ${n - 1} · coste = ${total}` : mode === 'ultima' ? `conjuntos = ${d.ncj} · ultima = ${ultima}` : `¿unidos(${s}, ${t})? ${d.unidos(s, t) ? 'sí' : 'no'} · aguante = ${ultima}`;
  const V = hotP => [
    chipsOf('aristas ordenadas por valor', edges.map(e => ({ t: eTxt(e), cls: est[e.id] || '' }))),
    vecOf('p (padre)', d.p, hotP), vecOf('tam (solo en raíces)', d.tam, -1),
    textOf('conjuntos', conjTxt(d)), textOf('estado', estado())];
  const lineasAcum = A.acum.map(x => L(A.code, x));
  C.snap(`Primero se pide <code>g.aristas()</code> (cada arista <b>una sola vez</b>) y se ordena por valor creciente con <code>sort</code>. Las ${edges.length} aristas quedan así: <code>${edges.map(e => e.v + '–' + e.w + '(' + e.c + ')').join('  ')}</code>. ${edges.some((e, i) => i && edges[i - 1].c === e.c) ? 'Con valores repetidos el orden entre ellos puede variar según el <code>sort</code>; el coste no cambia.' : ''}`, [ln('sort')], V(-1));
  C.snap(`<code>ConjuntosDisjuntos</code> con los ${n} vértices: al principio cada uno está <b>solo</b> en su conjunto (${d.ncj} conjuntos).`, [ln('cd')], V(-1));
  let paro = false;
  const motivoParo = e => mode === 'aero' ? `<code>valor() ≥ A</code>: la carretera ${e.v}–${e.w} cuesta ${e.c} ≥ A = ${par} y, al ir ordenadas, las siguientes también; ya no compensa construir más` : mode === 'clase' || mode === 'suma' ? `ya hay V − 1 = ${n - 1} aristas: el árbol está completo` : mode === 'ultima' ? '<code>num_cjtos() == 1</code>: todo está conectado' : `<code>unidos(${s}, ${t})</code>: origen y destino ya están conectados`;
  for (let k = 0; k < edges.length && !paro; k++) {
    const e = edges[k], u = e.v, v = e.w;
    if (!A.brkAfter && (mode === 'aero' ? e.c >= par : fin())) { paro = true; edges.slice(k).forEach(x => { est[x.id] = 'dead'; S.edge[x.id] = 'dead'; }); C.snap(`Al empezar la vuelta ${k + 1} se cumple ${motivoParo(e)}: <code>break</code>. Las ${edges.length - k} aristas restantes no se miran.`, [ln('brk')], V(-1)); break; }
    est[e.id] = 'cur'; S.edge[e.id] = 'cur'; S.node[u] = 's-cur'; S.node[v] = 's-cur';
    const ru = d.buscar(u), rv = d.buscar(v);
    C.snap(`Arista <b>${u}–${v}</b> de valor <b>${e.c}</b>: <code>unidos(${u}, ${v})</code> compara <code>buscar(${u}) = ${ru}</code> con <code>buscar(${v}) = ${rv}</code>.`, [ln('loop'), ln('uv'), ln('test')], V(-1));
    if (ru === rv) {
      est[e.id] = 'bad'; S.edge[e.id] = 'back'; S.node[u] = ''; S.node[v] = '';
      C.snap(`Mismo conjunto (${ru}): ${u} y ${v} <b>ya estaban conectados</b>. Esta arista cerraría un <b>ciclo</b>: se descarta.`, [ln('test')], V(-1));
    } else {
      d.unir(u, v); total += e.c; elegidos++; ultima = e.c;
      est[e.id] = 'ok'; S.edge[e.id] = 'tree'; S.node[u] = 's-vis'; S.node[v] = 's-vis';
      C.snap(`Conjuntos distintos (${ru} y ${rv}): <code>unir(${u}, ${v})</code> los junta y la arista <b>se acepta</b>${mode === 'clase' || mode === 'suma' ? `: coste += ${e.c} → <b>${total}</b>` : mode === 'aero' ? `: carretera construida (${e.c} < A = ${par}), coste += ${e.c} → <b>${total}</b>` : mode === 'ultima' ? `: <code>ultima = ${e.c}</code>` : `: <code>aguante = ${e.c}</code>`}.`, [ln('unir'), ...lineasAcum], V(-1));
    }
    if (A.brkAfter && fin()) { paro = true; edges.slice(k + 1).forEach(x => { est[x.id] = 'dead'; S.edge[x.id] = 'dead'; }); if (k + 1 < edges.length) C.snap(`Se cumple ${motivoParo()}: <code>break</code>. Las ${edges.length - k - 1} aristas restantes no se miran.`, [ln('brk')], V(-1)); }
  }
  /* resultado */
  Object.keys(S.node).forEach(x => { S.node[x] = ''; });
  edges.forEach(e => { if (est[e.id] === 'ok') S.edge[e.id] = 'new'; });
  const conexo = d.ncj === 1;
  let res;
  if (mode === 'clase') res = conexo ? `<b>Fin.</b> <code>conexo()</code> es true: el ARM tiene ${elegidos} aristas y coste <b>${total}</b>. Las aristas verdes forman el árbol.` : `<b>Fin.</b> Quedan ${d.ncj} conjuntos: el grafo <b>no es conexo</b>, no existe ARM (<code>conexo()</code> es false).`;
  else if (mode === 'aero') res = `<b>Fin.</b> Quedan <b>${d.ncj}</b> grupos ⇒ ${d.ncj} aeropuerto(s): coste = ${total} + ${d.ncj} · ${par} = <b>${total + d.ncj * par}</b>. Se escribe «${total + d.ncj * par} ${d.ncj}». (Una carretera con C = A no se construye: se prefieren más aeropuertos.)`;
  else if (mode === 'suma') res = elegidos === n - 1 ? `<b>Fin.</b> Se escribe el coste mínimo: <b>${total}</b>${n === 1 ? ' (una sola isla: no hace falta ningún puente)' : ''}.` : `<b>Fin.</b> Solo ${elegidos} puentes elegidos < ${n - 1}: se escribe <b>No hay puentes suficientes</b>.`;
  else if (mode === 'ultima') res = conexo ? `<b>Fin.</b> Se escribe la última arista aceptada: <b>${ultima}</b>${n === 1 ? ' (un solo árbol: no se necesita cuerda)' : ' (la cuerda más corta que conecta toda la selva)'}.` : `<b>Fin.</b> Quedan ${d.ncj} conjuntos: se escribe <b>Imposible</b>.`;
  else res = d.unidos(s, t) ? `<b>Fin.</b> ${s} y ${t} quedan unidos: se escribe <b>${ultima}</b>${s === t ? ' (origen = destino: no hay que bucear)' : ' (la galería más larga del mejor camino)'}.` : `<b>Fin.</b> ${s} y ${t} nunca llegan a estar unidos: se escribe <b>IMPOSIBLE</b>.`;
  C.snap(res, [ln('fin')], V(-1));
  C.f.res = { total: mode === 'aero' ? total + d.ncj * par : total, elegidos, ncj: d.ncj, ultima, unidos: mode === 'minimax' ? d.unidos(s, t) : null };
  return C.f;
}
ALGOS.kr_clase = () => kruskal('clase');
ALGOS.kr_suma = () => kruskal('suma');
ALGOS.kr_ultima = () => kruskal('ultima');
ALGOS.kr_minimax = (s, t) => kruskal('minimax', s, t);
ALGOS.kr_aero = (s, t, par) => kruskal('aero', s, t, par);

/* ---- Prim: crece un árbol desde el vértice 0 con una cola de prioridad de aristas ---- */
ALGOS.prim = () => {
  const n = G.n, C = ctx(), S = C.st, visit = Array(n).fill(false), pq = [], arm = [];
  let coste = 0, orden = 0;
  const est = {};
  const pqChips = hot => pq.slice().sort((a, b) => a.e.c - b.e.c || a.o - b.o).map((x, i) => ({ t: eTxt(x.e), cls: i === hot ? 'cur' : (visit[x.e.v] && visit[x.e.w] ? 'dead' : '') }));
  const V = hot => [chipsOf('cola de prioridad pq (la menor va primero)', pqChips(hot)), vecOf('visit', visit.map(x => x ? 'T' : 'F'), -1, x => x === 'T'), listOf('ARM (aristas elegidas)', arm.map(eTxt), -1), textOf('estado', `coste = ${coste} · aristas = ${arm.length} de V − 1 = ${n - 1}`)];
  function visitar(v) {
    visit[v] = true; S.node[v] = 's-done';
    const nuevas = [];
    for (const e of G.ady[v]) if (!visit[otro(e, v)]) { pq.push({ e, o: orden++ }); nuevas.push(e); S.edge[e.id] = S.edge[e.id] === 'tree' ? 'tree' : 'cur'; }
    C.snap(`<code>visitar(${v})</code>: ${v} entra en el árbol y se meten en <code>pq</code> las aristas que salen de ${v} hacia vértices <b>fuera</b> del árbol: ${nuevas.length ? nuevas.map(eTxt).join(', ') : 'ninguna'}.`, [L('prim', 'visit[v] = true;'), L('prim', 'if (!visit[a.otro(v)]) pq.push(a);')], V(-1));
    nuevas.forEach(e => { if (S.edge[e.id] === 'cur') S.edge[e.id] = ''; });
  }
  C.snap(`<code>ARM_Prim(g)</code>: el árbol empieza vacío. Se parte del <b>vértice 0</b> y se mantiene una cola de prioridad con las aristas que salen del árbol.`, [L('prim', 'visitar(g, 0);')], V(-1));
  visitar(0);
  let cur = null;
  while (pq.length && arm.length < n - 1) {
    pq.sort((a, b) => a.e.c - b.e.c || a.o - b.o);
    const x = pq.shift(), e = x.e, v = e.v, w = e.w;
    S.edge[e.id] = 'cur';
    C.snap(`<code>pq.top()</code>: la arista más barata es <b>${eTxt(e)}</b>. Se saca con <code>pop()</code>.`, [L('prim', 'while (!pq.empty()'), L('prim', 'auto a = pq.top(); pq.pop();'), L('prim', 'int v = a.uno(), w = a.otro(v);')], V(-1));
    if (visit[v] && visit[w]) {
      S.edge[e.id] = 'back';
      C.snap(`Los dos extremos (${v} y ${w}) <b>ya están en el árbol</b>: la arista sobra (se metió en la cola cuando el otro extremo aún no estaba dentro). <code>continue</code>.`, [L('prim', 'if (visit[v] && visit[w]) continue;')], V(-1));
      continue;
    }
    arm.push(e); coste += e.c; S.edge[e.id] = 'tree'; est[e.id] = 'ok';
    C.snap(`Un extremo está fuera: la arista <b>se acepta</b>: <code>_ARM.push_back(a)</code>, coste += ${e.c} → <b>${coste}</b>.`, [L('prim', '_ARM.push_back(a);'), L('prim', 'coste += a.valor();')], V(-1));
    if (!visit[v]) visitar(v);
    if (!visit[w]) visitar(w);
  }
  Object.keys(S.node).forEach(k => { S.node[k] = 's-done'; });
  arm.forEach(e => { S.edge[e.id] = 'new'; });
  for (const e of G.edges) if (S.edge[e.id] !== 'new') S.edge[e.id] = 'dead';
  const conexo = arm.length === n - 1;
  C.snap(conexo ? `<b>Fin.</b> El árbol tiene ${arm.length} = V − 1 aristas y coste <b>${coste}</b> (es el mismo coste que da Kruskal; el árbol puede ser distinto si hay valores repetidos).` : `<b>Fin.</b> La cola se vació con ${arm.length} aristas < V − 1: desde el vértice 0 <b>no se llega a todos</b>. El grafo no es conexo y no existe ARM.`, [L('prim', 'bool conexo() const')], V(-1));
  C.f.res = { coste, conexo, n: arm.length };
  return C.f;
};

/* ---- DFS que solo cruza aristas con valor >= ancho (06-2 Camiones de reparto) ---- */
ALGOS.dfsancho = (s, t, ancho) => {
  const n = G.n, visit = Array(n).fill(false), C = ctx(), S = C.st;
  const V = hot => [vecOf('visitado', visit.map(x => x ? 'T' : 'F'), hot, x => x === 'T'), textOf('consulta', `origen = ${s} · destino = ${t} · ancho del camión = ${ancho}`)];
  C.snap(`<b>Consulta</b>: ¿puede un camión de ancho <b>${ancho}</b> ir de ${s} a ${t}? Se crea <code>Alcanzables(g, ${s}, ${ancho})</code>: un DFS desde ${s} que <b>ignora las calles con anchura máxima &lt; ${ancho}</b>. Las aristas que no valen se verán atenuadas.`, [L('e62', 'dfs(g, origen);')], V(-1));
  function dfs(v) {
    visit[v] = true; S.node[v] = 's-cur';
    C.snap(`<code>dfs(${v})</code>: ${v} queda visitado.`, [L('e62', 'void dfs('), L('e62', 'visitado[v] = true;')], V(v));
    for (const e of G.ady[v]) {
      const w = otro(e, v), prev = S.edge[e.id];
      if (e.c < ancho) {
        S.edge[e.id] = 'dead';
        C.snap(`Calle ${v}–${w} de anchura máxima <b>${e.c}</b> &lt; ${ancho}: el camión <b>no cabe</b>, no se usa.`, [L('e62', 'for (auto a : g.ady(v))'), L('e62', 'if (a.valor() >= ancho && !visitado[w]) dfs(g, w);')], V(w));
      } else if (visit[w]) {
        C.snap(`Calle ${v}–${w} (${e.c} ≥ ${ancho}) cabe, pero ${w} <b>ya está visitado</b>: se salta.`, [L('e62', 'for (auto a : g.ady(v))'), L('e62', 'if (a.valor() >= ancho && !visitado[w]) dfs(g, w);')], V(w));
        S.edge[e.id] = prev || '';
      } else {
        S.edge[e.id] = 'tree'; S.node[v] = 's-vis';
        C.snap(`Calle ${v}–${w} (${e.c} ≥ ${ancho}): <b>cabe</b> y ${w} no está visitado → <code>dfs(${w})</code>.`, [L('e62', 'int w = a.otro(v);'), L('e62', 'if (a.valor() >= ancho && !visitado[w]) dfs(g, w);')], V(w));
        dfs(w); S.node[v] = 's-cur';
      }
    }
    S.node[v] = 's-done';
  }
  dfs(s);
  const ok = visit[t];
  if (ok) S.node[t] = 's-cur'; else S.node[t] = 's-red';
  C.snap(`<b>Fin del DFS.</b> <code>alcanzable(${t})</code> es <b>${ok ? 'true → SI' : 'false → NO'}</b>: ${ok ? 'hay un camino por calles donde el camión de ancho ' + ancho + ' cabe' : 'todas las rutas hacia ' + t + ' pasan por alguna calle más estrecha que ' + ancho}.`, [L('e62', 'bool alcanzable(int v) const')], V(t));
  C.f.res = { ok };
  return C.f;
};
