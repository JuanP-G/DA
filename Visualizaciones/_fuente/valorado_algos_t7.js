/* ---- Dijkstra y sus variantes: Dijkstra (IndexPQ), DijkstraVector, 07-1 (carga en vértices), 07-2 (contar caminos), 07-3 (ruta) ---- */
const fd = x => (x === Infinity ? '∞' : x);
function cargasDe(txt, n) {
  const v = String(txt || '').split(/[\s,;]+/).filter(x => x !== '').map(Number).map(x => (isNaN(x) || x < 0 ? 0 : Math.floor(x)));
  while (v.length < n) v.push(0);
  return v.slice(0, n);
}
/* coste del ARM del grafo sin sentidos (para compararlo con el árbol de caminos mínimos) */
function costeARMsinSentidos() {
  const p = [...Array(G.n).keys()], f = a => (p[a] === a ? a : (p[a] = f(p[a])));
  let tot = 0, k = 0;
  for (const e of G.edges.slice().sort((a, b) => a.c - b.c)) { const a = f(e.v), b = f(e.w); if (a !== b) { p[a] = b; tot += e.c; k++; } }
  return k === G.n - 1 ? tot : null;
}

function dijkstra(mode, s, t, txt) {
  const n = G.n, C = ctx(), S = C.st;
  const und = mode === 'e72' || mode === 'e73';
  const code = { pq: 'dijkstra', vec: 'dijkstra_vec', e71: 'e71', e72: 'e72', e73: 'e73' }[mode];
  const carga = mode === 'e71' ? cargasDe(txt, n) : null;
  const nb = v => (und ? G.edges.filter(e => e.v === v || e.w === v).map(e => ({ e, to: otro(e, v) })) : G.ady[v].map(e => ({ e, to: e.w })));
  const peso = (e, to) => e.c + (carga ? carga[to] : 0);
  const dist = Array(n).fill(Infinity), par = Array(n).fill(null).map(() => []), done = Array(n).fill(false), inq = Array(n).fill(false);
  const formas = Array(n).fill(0);
  const origDist = carga ? carga[s] : 0;
  const ln = k => L(code, k);
  const tagOf = v => (dist[v] === Infinity ? '' : (mode === 'e72' ? dist[v] + ' ×' + formas[v] : '' + dist[v]));
  const refrescaTags = () => { for (let v = 0; v < n; v++) S.tag[v] = tagOf(v); };
  const refrescaTree = () => {
    for (const e of G.edges) if (S.edge[e.id] === 'tree') S.edge[e.id] = '';
    par.forEach(l => l.forEach(id => { S.edge[id] = 'tree'; }));
  };
  const ultiTxt = v => (par[v].length ? par[v].map(id => { const e = G.edges[id]; return (und ? otro(e, v) : e.v) + '→' + v; }).join(' | ') : '–');
  let comps = 0;                         /* accesos al vector al buscar el mínimo (versión con vector) */
  const pqChips = hot => {
    const q = []; for (let v = 0; v < n; v++) if (inq[v]) q.push(v);
    q.sort((a, b) => dist[a] - dist[b] || a - b);
    return q.map(v => ({ t: v + ' (' + dist[v] + ')', cls: v === hot ? 'cur' : '' }));
  };
  const V = hot => {
    const out = [vecOf('dist', dist.map(fd), hot)];
    out[0].ok = done.map((d, i) => (d ? i : -1)).filter(i => i >= 0 && i !== hot);
    out.push(vecOf('ulti (arista que llega)', par.map((_, v) => ultiTxt(v)), -1));
    if (mode === 'e72') out.push(vecOf('formas', formas.map((x, v) => (dist[v] === Infinity ? 0 : x)), hot));
    if (mode === 'vec') out.push(vecOf('tratado', done.map(x => (x ? 'T' : 'F')), -1, x => x === 'T'), textOf('accesos al vector buscando el mínimo', comps + ''));
    else out.push(chipsOf('cola de prioridad pq (la menor va primero)', pqChips(hot)));
    return out;
  };
  const arista = (e, v, to) => (und ? v + '–' + to : v + '→' + to) + ' (' + e.c + ')';

  /* ----- inicio ----- */
  const intro = {
    pq: `<code>Dijkstra(g, ${s})</code>: <code>dist</code> empieza en ∞ para todos (<code>INF</code>), <code>dist[${s}] = 0</code> y el origen entra en la cola de prioridad con prioridad 0.`,
    vec: `<code>DijkstraVector(g, ${s})</code>: <code>dist</code> empieza en ∞, <code>dist[${s}] = 0</code> y no hay cola: en cada paso se recorrerá el vector buscando el mínimo.`,
    e71: `<b>07-1</b>: la página de partida (vértice ${s}, página ${s + 1} del enunciado) también hay que cargarla, así que <code>dist[0] = carga[0] = ${origDist}</code>. El coste de cada arista es <b>tiempo del enlace + carga de la página a la que llega</b> (<code>t + carga[w]</code>), con cargas <code>${carga ? carga.join(' ') : ''}</code>.`,
    e72: `<b>07-2</b>: las calles se recorren en los dos sentidos. <code>dist[0] = 0</code> y <code>formas[0] = 1</code>: hay una forma de estar en casa (no moverse). <code>formas[v]</code> contará los caminos mínimos hasta <code>v</code>.`,
    e73: `<b>07-3</b>: Dijkstra desde el origen del pedido (${s}). Además de <code>dist</code> se guarda <code>ulti[w]</code> = vértice anterior en el camino mínimo.`,
  }[mode];
  dist[s] = origDist; formas[s] = 1; inq[s] = mode !== 'vec';
  S.node[s] = mode === 'vec' ? 's-cur' : 's-q'; refrescaTags();
  C.snap(intro, mode === 'vec' ? [ln('dist[origen] = 0;')] : mode === 'e71' ? [ln('dist[0] = carga[0];'), ln('pq.push(0, dist[0]);')] : mode === 'e72' ? [ln('dist[0] = 0;'), ln('formas[0] = 1;'), ln('pq.push(0, 0);')] : [ln('dist[origen] = 0;'), ln('pq.push(origen, 0);')], V(-1));

  let paso = 0, parar = false;
  while (!parar) {
    let v = -1;
    if (mode === 'vec') {
      for (let u = 0; u < n; u++) if (!done[u] && dist[u] !== Infinity && (v === -1 || dist[u] < dist[v])) v = u;
      comps += n;
      if (v === -1) {
        C.snap(`Paso ${++paso}: se recorren los ${n} vértices (accesos acumulados: <b>${comps}</b>) y <b>ninguno</b> no tratado tiene <code>dist</code> finita: lo que queda no es alcanzable. <code>break</code>.`, [ln('for (int u = 0; u < g.V(); ++u)'), ln('if (v == -1) break;')], V(-1));
        break;
      }
      Object.keys(S.node).forEach(k => { if (S.node[k] === 's-cur') S.node[k] = 's-done'; });
      S.node[v] = 's-cur'; done[v] = true;
      C.snap(`Paso ${++paso}: se recorre el vector <code>dist</code> entero (${n} accesos; en total ${comps}) y el no tratado de menor distancia es <b>${v}</b> con <code>dist[${v}] = ${dist[v]}</code>. <code>tratado[${v}] = true</code>: su distancia ya es definitiva.`, [ln('for (int u = 0; u < g.V(); ++u)'), ln('tratado[v] = true;')], V(v));
    } else {
      let q = []; for (let u = 0; u < n; u++) if (inq[u]) q.push(u);
      if (!q.length) break;
      q.sort((a, b) => dist[a] - dist[b] || a - b); v = q[0];
      Object.keys(S.node).forEach(k => { if (S.node[k] === 's-cur') S.node[k] = 's-done'; });
      S.node[v] = 's-cur'; inq[v] = false; done[v] = true;
      C.snap(`Paso ${++paso}: <code>pq.top().elem</code> es <b>${v}</b> (la menor prioridad, <code>dist[${v}] = ${dist[v]}</code>); <code>pop()</code> lo saca. Su distancia ya es <b>definitiva</b>: ahora se relajan sus aristas.`, [ln('int v = pq.top().elem; pq.pop();'), ...(mode === 'e71' ? [ln('while (!pq.empty())')] : [])], V(v));
      if ((mode === 'e71' && v === t) || (mode === 'e73' && v === t)) {
        C.snap(`<code>v == ${mode === 'e71' ? 'N - 1' : 'destino'}</code>: la distancia al destino ya es definitiva y no hace falta seguir. <code>break</code>.`, [ln(mode === 'e71' ? 'if (v == N - 1) break;' : 'if (v == destino) break;')], V(v));
        parar = true; break;
      }
    }
    for (const { e, to: w } of nb(v)) {
      const w0 = S.edge[e.id], cst = peso(e, w), nuevo = dist[v] + cst;
      S.edge[e.id] = 'cur';
      const formula = carga ? `${dist[v]} + ${e.c} + carga[${w}] (${carga[w]}) = ${nuevo}` : `${dist[v]} + ${e.c} = ${nuevo}`;
      const lnFor = ln(mode === 'vec' ? 'for (auto a : g.ady(v)) {' : mode === 'pq' ? 'for (auto a : g.ady(v))' : 'for (auto a : g.ady(v)) {');
      const lnIf = mode === 'e72' ? ln('int d = dist[v] + a.valor();') : mode === 'pq' ? ln('if (dist[w] > dist[v] + a.valor())') : mode === 'vec' ? ln('if (dist[w] > dist[v] + a.valor())') : ln('if (dist[w] > dist[v] + a.valor()) {');
      C.snap(`Relajar <b>${arista(e, v, w)}</b>: <code>dist[${v}] + valor${carga ? ' + carga' : ''}</code> = ${formula}; <code>dist[${w}]</code> vale ${fd(dist[w])}.`, [lnFor, lnIf], V(w));
      if (nuevo < dist[w]) {
        const antes = dist[w];
        par[w].forEach(id => { if (S.edge[id] === 'tree') S.edge[id] = ''; });
        dist[w] = nuevo; par[w] = [e.id]; formas[w] = formas[v];
        if (mode !== 'vec') { inq[w] = true; if (!done[w]) S.node[w] = 's-q'; }
        S.edge[e.id] = 'tree'; refrescaTags();
        const lines = mode === 'e72' ? [ln('if (d < dist[w]) {'), ln('formas[w] = formas[v];'), ln('pq.update(w, d);')]
          : mode === 'e73' ? [ln('dist[w] = dist[v] + a.valor();'), ln('ulti[w] = v;'), ln('pq.update(w, dist[w]);')]
          : mode === 'e71' ? [ln('dist[w] = dist[v] + a.valor();'), ln('pq.update(w, dist[w]);')]
          : mode === 'vec' ? [ln('if (dist[w] > dist[v] + a.valor())')]
          : [ln('dist[w] = dist[v] + a.valor(); ulti[w] = a;'), ln('pq.update(w, dist[w]);')];
        C.snap(`${nuevo} &lt; ${fd(antes)}: <b>mejora</b>. <code>dist[${w}] = ${nuevo}</code>${mode === 'e72' ? `, <code>formas[${w}] = formas[${v}] = ${formas[v]}</code> (los caminos anteriores a ${w} ya no valen)` : ''}, <code>ulti[${w}]</code> pasa a ser ${arista(e, v, w)}${mode === 'vec' ? '' : `; <code>pq.update(${w}, ${nuevo})</code> ${antes === Infinity ? '(mete a ' + w + ' en la cola)' : '(le cambia la prioridad)'}`}.`, lines, V(w));
      } else if (mode === 'e72' && nuevo === dist[w] && dist[w] !== Infinity) {
        par[w].push(e.id); formas[w] += formas[v]; S.edge[e.id] = 'tree'; refrescaTags();
        C.snap(`${nuevo} = <code>dist[${w}]</code>: otra forma <b>igual de buena</b> de llegar a ${w}. <code>formas[${w}] += formas[${v}]</code> (${formas[v]}) → <b>${formas[w]}</b>.`, [ln('} else if (d == dist[w]) {'), ln('formas[w] += formas[v];')], V(w));
      } else {
        S.edge[e.id] = w0 === 'cur' ? '' : (w0 || '');
        if (par[w].includes(e.id)) S.edge[e.id] = 'tree';
        C.snap(`${nuevo} ${nuevo === dist[w] ? '=' : '≥'} ${fd(dist[w])}: <b>no mejora</b>${done[w] ? ` (además ${w} ya está tratado)` : ''}. No se cambia nada.`, [lnIf], V(w));
      }
    }
    if (mode === 'vec' && done.every(x => x)) break;
  }

  /* ----- resultado ----- */
  Object.keys(S.node).forEach(k => { S.node[k] = ''; });
  const alc = v => dist[v] !== Infinity;
  for (let v = 0; v < n; v++) S.node[v] = alc(v) ? 's-done' : '';
  refrescaTree(); refrescaTags();
  if (mode === 'e73') {
    if (!alc(t)) { S.node[t] = 's-red'; C.snap(`<b>Fin.</b> <code>dist[${t}]</code> es ∞: no hay camino del vértice ${s} al ${t} (puntos ${s + 1} y ${t + 1} del enunciado). Se escribe <b>NO LLEGA</b>.`, [ln('if (dist[destino] == INF) {')], V(-1)); C.f.res = { dist: null }; return C.f; }
    const camino = [t]; for (let v = t; v !== s;) { const e = G.edges[par[v][0]]; v = otro(e, v); camino.unshift(v); }
    for (const e of G.edges) S.edge[e.id] = '';
    C.snap(`Ya hay camino: <code>dist[${t}] = ${dist[t]}</code>. Para escribirlo se <b>retrocede</b> desde el destino con <code>ulti[]</code>, metiendo cada vértice por delante.`, [ln('if (dist[destino] == INF) {')], V(-1));
    const cur = [t]; S.node[t] = 's-done';
    C.snap(`<code>camino.push_front(${t})</code> (empezamos por el destino): camino = <code>${cur.join(' -> ')}</code>.`, [ln('for (int v = destino; v != origen; v = ulti[v]) camino.push_front(v);')], V(t));
    for (let v = t; v !== s;) {
      const eid = par[v][0], e = G.edges[eid], u = otro(e, v); S.edge[eid] = 'new'; S.node[u] = 's-done'; cur.unshift(u); v = u;
      C.snap(`<code>v = ulti[v]</code> → <b>${u}</b>: ${v === s ? 'es el origen, se acabó el retroceso' : 'se sigue hacia atrás'}. camino = <code>${cur.join(' -> ')}</code>.`, [ln('for (int v = destino; v != origen; v = ulti[v]) camino.push_front(v);')], V(-1));
    }
    C.snap(`<b>Fin.</b> Se escribe <b>${dist[t]}: ${cur.map(x => x + 1).join(' -> ')}</b> (en el enunciado los puntos se numeran desde 1: el vértice <code>v</code> se escribe como <code>v + 1</code>).`, [ln('cout << dist[destino] << ":";')], V(-1));
    C.f.res = { dist: dist[t], camino: cur }; return C.f;
  }
  if (mode === 'e71') {
    if (alc(t)) { for (let v = t; v !== s;) { const e = G.edges[par[v][0]]; S.edge[e.id] = 'new'; v = e.v; } }
    S.node[t] = alc(t) ? 's-done' : 's-red';
    C.snap(alc(t) ? `<b>Fin.</b> Tiempo mínimo para llegar al vértice ${t} (página ${t + 1} del enunciado): <b>${dist[t]}</b> ms (incluye la carga de la página de partida y de la de llegada).` : `<b>Fin.</b> <code>dist[${t}]</code> sigue en ∞: no hay ninguna cadena de enlaces hasta el vértice ${t}. Se escribe <b>IMPOSIBLE</b>.`, [ln('if (dist[N - 1] == INF)')], V(-1));
    C.f.res = { dist: alc(t) ? dist[t] : null }; return C.f;
  }
  if (mode === 'e72') {
    S.node[t] = alc(t) ? 's-done' : 's-red';
    C.snap(alc(t) ? `<b>Fin.</b> <code>formas[${t}] = ${formas[t]}</code>: Lucas puede ir de ${s} a ${t} de <b>${formas[t]}</b> ${formas[t] === 1 ? 'forma' : 'formas'} distintas recorriendo la distancia mínima (<b>${dist[t]}</b>). Las aristas azules son las que están en algún camino mínimo.` : `<b>Fin.</b> No se llega a ${t}: <code>formas[${t}]</code> sigue en 0 y se escribe <b>0</b>.`, [ln('cout << formas[N - 1]')], V(-1));
    C.f.res = { formas: alc(t) ? formas[t] : 0, dist: dist[t] }; return C.f;
  }
  /* pq y vec: árbol de caminos mínimos */
  let suma = 0, aristas = 0;
  par.forEach(l => l.forEach(id => { S.edge[id] = 'new'; suma += G.edges[id].c; aristas++; }));
  const todos = dist.every(x => x !== Infinity), arm = todos ? costeARMsinSentidos() : null;
  const extra = todos && arm !== null
    ? ` <b>¿Es un ARM?</b> El árbol suma <b>${suma}</b>; un árbol de recubrimiento de coste mínimo del mismo grafo (sin mirar los sentidos) sumaría <b>${arm}</b>${suma === arm ? ': aquí coinciden en coste' : ': <b>no es el mismo árbol</b>'} (los dos responden a preguntas distintas).` : '';
  const sinAlcanzar = dist.map((x, v) => (x === Infinity ? v : -1)).filter(v => v >= 0);
  C.snap(`<b>Fin.</b> ${mode === 'pq' ? 'La cola se vacía' : 'No quedan vértices con <code>dist</code> finita'}: <code>dist</code> tiene las distancias mínimas desde ${s} y las aristas verdes forman el <b>árbol de caminos mínimos</b> (<code>ulti[]</code>).${sinAlcanzar.length ? ` ${sinAlcanzar.join(', ')} no ${sinAlcanzar.length > 1 ? 'son alcanzables' : 'es alcanzable'} (<code>hayCamino</code> = false).` : ''}${mode === 'vec' ? ` Se han hecho <b>${comps}</b> accesos al vector: del orden de V² = ${n * n}.` : ''}${extra}`, [mode === 'vec' ? ln('if (v == -1) break;') : ln('bool hayCamino(int v) const')], V(-1));
  C.f.res = { dist: dist.map(fd), suma, arm, comps };
  return C.f;
}
ALGOS.dij_pq = s => dijkstra('pq', s);
ALGOS.dij_vec = s => dijkstra('vec', s);
ALGOS.e71 = (s, t, _p, txt) => dijkstra('e71', s, t, txt);
ALGOS.e72 = (s, t) => dijkstra('e72', s, t);
ALGOS.e73 = (s, t) => dijkstra('e73', s, t);
