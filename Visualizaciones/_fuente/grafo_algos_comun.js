const ALGOS = {};
function L(k, sub, occ = 0) {
  let c = -1; const ls = CODES[k].lines;
  for (let i = 0; i < ls.length; i++) if (ls[i].includes(sub)) { c++; if (c === occ) return i + 1; }
  throw new Error('ancla no encontrada en ' + k + ': ' + sub);
}
const ek = (v, w) => DIR ? v + '>' + w : Math.min(v, w) + '>' + Math.max(v, w);
function ctx() {
  const f = [], st = { node: {}, edge: {}, tag: {} };
  return { f, st, snap(msg, lines, vecs, extra) { f.push({ msg, lines, node: { ...st.node }, edge: { ...st.edge }, tag: { ...st.tag }, vecs: vecs || [], ...(extra || {}) }); } };
}
const vecOf = (name, arr, hot, okFn) => ({ kind: 'vec', name, vals: arr.map(x => x === null ? '·' : x), hot: hot == null ? -1 : hot, ok: okFn ? arr.map((x, i) => okFn(x) ? i : -1).filter(i => i >= 0) : [] });
const listOf = (name, arr, hot) => ({ kind: 'list', name, vals: arr.slice(), hot: hot == null ? -1 : hot });
const cl = a => a.map(x => x.slice());

/* ---- BFS (CaminosBFS): dist, cola, camino mínimo al final ---- */
ALGOS.bfs = (s, t) => {
  const n = G.n, dist = Array(n).fill(-1), par = Array(n).fill(-1), q = [], C = ctx(), S = C.st;
  const V = hot => [vecOf('dist', dist, hot, x => x >= 0), listOf('cola q (frente a la izquierda)', q, 0)];
  C.snap(`<code>CaminosBFS(g, ${s})</code>: <code>dist</code> empieza con todo a <b>-1</b> («sin visitar»).`, [L('bfs', 'dist(g.V(), -1)')], V(-1));
  dist[s] = 0; q.push(s); S.node[s] = 's-q'; S.tag[s] = 0;
  C.snap(`El origen ${s} tiene <b>dist = 0</b> y entra en la cola.`, [L('bfs', 'dist[origen] = 0;'), L('bfs', 'q.push(origen);')], V(s));
  while (q.length) {
    const v = q.shift(); S.node[v] = 's-cur';
    C.snap(`Saco el frente de la cola: <b>${v}</b> (dist = ${dist[v]}). Miro ${DIR ? 'sus sucesores' : 'sus vecinos'}: [${G.ady[v].join(', ') || 'ninguno'}].`, [L('bfs', 'while (!q.empty())'), L('bfs', 'int v = q.front(); q.pop();')], V(v));
    for (const w of G.ady[v]) {
      const k = ek(v, w), prev = S.edge[k];
      S.edge[k] = 'cur';
      if (dist[w] === -1) {
        dist[w] = dist[v] + 1; par[w] = v; q.push(w); S.node[w] = 's-q'; S.tag[w] = dist[w];
        C.snap(`${w} no estaba visitado → <code>dist[${w}] = dist[${v}] + 1 = ${dist[w]}</code> y entra en la cola.`, [L('bfs', 'for (int w : g.ady(v))'), L('bfs', 'if (dist[w] == -1)'), L('bfs', 'dist[w] = dist[v] + 1;'), L('bfs', 'q.push(w);')], V(w));
        S.edge[k] = 'tree';
      } else {
        C.snap(`${w} ya tiene distancia (${dist[w]}): lo ignoro. ${dist[w] <= dist[v] ? 'Llegar otra vez no mejora nada: BFS ya lo alcanzó por un camino igual o más corto.' : ''}`, [L('bfs', 'for (int w : g.ady(v))'), L('bfs', 'if (dist[w] == -1)')], V(w));
        S.edge[k] = prev || '';
      }
    }
    S.node[v] = 's-done';
  }
  // resultado
  const fin = [];
  if (dist[t] >= 0) {
    let x = t; const path = [t];
    while (par[x] >= 0) { x = par[x]; path.push(x); }
    path.reverse();
    for (let i = 0; i + 1 < path.length; i++) S.edge[ek(path[i], path[i + 1])] = 'new';
    path.forEach(x => { S.node[x] = 's-cur'; });
    C.snap(`<b>Fin del BFS.</b> Distancia de ${s} a ${t}: <b>${dist[t]}</b> aristas. Camino mínimo: ${path.join(' ' + (DIR ? '→' : '–') + ' ')}. Los vértices con <code>dist = -1</code> (${dist.map((d, i) => d < 0 ? i : -1).filter(i => i >= 0).join(', ') || 'ninguno'}) ${DIR ? 'no son alcanzables desde ' + s : 'están en otra componente'}.`, [L('bfs', 'int distancia(int v) const')], V(t));
  } else {
    C.snap(`<b>Fin del BFS.</b> ${t} <b>no se alcanza</b> desde ${s} (<code>dist[${t}] = -1</code>).`, [L('bfs', 'int distancia(int v) const')], V(t));
  }
  return C.f;
};
