
/* ---- Orden topológico con DFS y 3 estados (OrdenTopologico) ---- */
ALGOS.topo = () => {
  const n = G.n, estado = Array(n).fill(0), post = [], pila = [], C = ctx(), S = C.st;
  let hayCiclo = false;
  const V = hot => [vecOf('estado (0 sin visitar · 1 en pila · 2 terminado)', estado, hot, x => x === 2), listOf('pila de llamadas', pila, pila.length - 1), listOf('post (orden de terminación)', post, -1)];
  C.snap(`<code>OrdenTopologico(g)</code>: todos los estados a 0. Lanzo un DFS desde cada vértice sin visitar, <b>en orden</b>.`, [L('topo', 'estado(g.V(), 0)'), L('topo', 'if (estado[v] == 0) dfs(g, v);')], V(-1));
  function dfs(v) {
    estado[v] = 1; pila.push(v); S.node[v] = 's-cur';
    C.snap(`<code>dfs(${v})</code>: <b>estado[${v}] = 1</b> (en la pila: lo estoy explorando).`, [L('topo', 'estado[v] = 1;')], V(v));
    for (const w of G.ady[v]) {
      if (hayCiclo) return;
      const k = ek(v, w), prev = S.edge[k]; S.edge[k] = 'cur';
      if (estado[w] === 1) {
        hayCiclo = true; S.node[w] = 's-red'; S.node[v] = 's-red'; S.edge[k] = 'back';
        C.snap(`Sucesor ${w}: <b>estado 1</b>, sigue en la pila ⇒ ${w} es un antecesor de ${v} y la arista ${v}→${w} <b>cierra un ciclo</b>. <code>hayCiclo = true</code> ⇒ <b>Imposible</b>.`, [L('topo', 'if (estado[w] == 1) hayCiclo = true;')], V(w));
        return;
      } else if (estado[w] === 0) {
        C.snap(`Sucesor ${w}: estado 0 → <code>dfs(${w})</code>.`, [L('topo', 'for (int w : g.ady(v))'), L('topo', 'else if (estado[w] == 0) dfs(g, w);')], V(w));
        S.edge[k] = 'tree'; S.node[v] = 's-vis';
        dfs(w);
        if (hayCiclo) return;
        S.node[v] = 's-cur';
      } else {
        C.snap(`Sucesor ${w}: <b>estado 2</b> (ya terminado). Es normal, no hay ciclo: ${w} y todo lo que depende de él ya está en <code>post</code>.`, [L('topo', 'for (int w : g.ady(v))'), L('topo', 'if (estado[w] == 1) hayCiclo = true;')], V(w));
        S.edge[k] = prev || '';
      }
    }
    estado[v] = 2; pila.pop(); post.push(v); S.node[v] = 's-done';
    C.snap(`${v} no tiene más sucesores: <b>estado[${v}] = 2</b> y entra en <code>post</code> (terminan primero las tareas que dependen de él).`, [L('topo', 'estado[v] = 2;'), L('topo', 'post.push_back(v);')], V(v));
  }
  for (let v = 0; v < n && !hayCiclo; v++) if (estado[v] === 0) {
    C.snap(`${v} está sin visitar: nuevo DFS desde ${v}.`, [L('topo', 'if (estado[v] == 0) dfs(g, v);')], V(v));
    dfs(v);
  }
  if (hayCiclo) {
    C.snap(`<b>Imposible</b>: con un ciclo ninguna tarea del ciclo puede ir antes que las demás. El programa escribe <code>Imposible</code>.`, [L('topo', 'bool posible() const')], V(-1));
  } else {
    const orden = post.slice().reverse();
    Object.keys(S.node).forEach(k => { S.node[k] = 's-done'; });
    orden.forEach((x, i) => { S.tag[x] = i + 1; });
    C.snap(`<code>reverse(post)</code> ⇒ <b>orden topológico: ${orden.join(' ')}</b>. Los números sobre los vértices indican su posición. Toda arista va de un vértice a otro posterior en el orden (hay muchos órdenes válidos; el juez acepta cualquiera).`, [L('topo', 'reverse(post.begin(), post.end());')], [...V(-1).slice(0, 2), listOf('orden topológico (post invertido)', orden, -1)]);
  }
  return C.f;
};

/* ---- inverso(): copia con todas las aristas invertidas ---- */
ALGOS.inv = () => {
  const C = ctx(), S = C.st, n = G.n, inv = Array.from({ length: n }, () => []);
  const ex = (v, j) => ({ adys: cl(inv), adysName: 'inv._ady', hotList: v, newChip: v == null ? null : { v, j } });
  C.snap(`<code>Digrafo inv(_V)</code>: mismos ${n} vértices y ninguna arista. Voy a recorrer cada arista <code>v→w</code> de <i>este</i> grafo.`, [L('clase', 'Digrafo inv(_V);')], [], ex(null));
  for (let v = 0; v < n; v++) for (const w of G.ady[v]) {
    const k = v + '>' + w; S.edge[k] = 'cur'; S.node[v] = 's-cur'; S.node[w] = 's-vis';
    inv[w].push(v);
    C.snap(`Arista <b>${v}→${w}</b> ⇒ <code>inv.ponArista(${w}, ${v})</code>: ${v} entra en la lista de ${w} del inverso.`, [L('clase', 'for (int v = 0; v < _V; ++v) {'), L('clase', 'inv.ponArista(w, v);')], [], ex(w, inv[w].length - 1));
    S.edge[k] = ''; S.node[v] = ''; S.node[w] = '';
  }
  C.snap(`<code>return inv</code>: ahora <code>inv.ady(w)</code> son los <b>predecesores</b> de <code>w</code> en el grafo original. Pulsa <b>⇄ Invertir grafo</b> para quedarte con él y verlo dibujado.`, [L('clase', 'return inv;')], [], ex(null));
  return C.f;
};
document.getElementById('bInv').onclick = () => {
  const inv = gInv(); G.ady = inv.ady; afterEdit();
  $('#msg').innerHTML = 'El grafo es ahora <code>g.inverso()</code>: todas las flechas giradas. Si lo vuelves a invertir, recuperas el original (salvo el orden dentro de las listas).';
};
