
/* ---- Componentes conexas con DFS (MaximaCompConexa) ---- */
ALGOS.comp = () => {
  const n = G.n, visit = Array(n).fill(false), comp = Array(n).fill(null), C = ctx(), S = C.st;
  let maxim = 0, nc = 0; const tams = [];
  const V = hot => [vecOf('visit', visit.map(x => x ? 'T' : 'F'), hot, x => x === 'T'), vecOf('componente', comp, -1, x => x !== null)];
  C.snap(`<code>MaximaCompConexa(g)</code>: <code>visit</code> todo a <code>false</code>, <code>maxim = 0</code>. Recorro los vértices en orden y, cada vez que encuentro uno sin visitar, <b>empieza una componente nueva</b>.`, [L('comp', 'visit(g.V(), false)')], V(-1));
  function dfs(v, c) {
    visit[v] = true; comp[v] = 'C' + c; S.node[v] = 's-cur'; S.tag[v] = 'C' + c;
    C.snap(`<code>dfs(${v})</code>: marco ${v} como visitado y empiezo a contar (<code>tam = 1</code>).`, [L('comp', 'visit[v] = true;'), L('comp', 'int tam = 1;')], V(v));
    let tam = 1;
    for (const w of G.ady[v]) {
      const k = ek(v, w), prev = S.edge[k]; S.edge[k] = 'cur';
      if (!visit[w]) {
        C.snap(`Vecino ${w} de ${v}: <b>sin visitar</b> → llamo a <code>dfs(${w})</code> y sumo lo que devuelva.`, [L('comp', 'for (int w : g.ady(v))'), L('comp', 'if (!visit[w]) tam += dfs(g, w);')], V(w));
        S.edge[k] = 'tree'; S.node[v] = 's-vis';
        tam += dfs(w, c);
        S.node[v] = 's-cur';
      } else {
        C.snap(`Vecino ${w} de ${v}: <b>ya visitado</b> (${w === v ? 'es un bucle' : 'seguramente por donde vine, o un ciclo'}): lo salto.`, [L('comp', 'for (int w : g.ady(v))'), L('comp', 'if (!visit[w]) tam += dfs(g, w);')], V(w));
        S.edge[k] = prev || '';
      }
    }
    S.node[v] = 's-done';
    C.snap(`<code>dfs(${v})</code> termina y devuelve <b>tam = ${tam}</b>.`, [L('comp', 'return tam;')], V(v));
    return tam;
  }
  for (let v = 0; v < n; v++) {
    if (!visit[v]) {
      C.snap(`<b>visit[${v}] = false</b> → ${v} empieza la componente nº ${nc + 1}.`, [L('comp', 'if (!visit[v])')], V(v));
      const tam = dfs(v, nc + 1); tams.push(tam); nc++;
      maxim = Math.max(maxim, tam);
      C.snap(`La componente ${nc} tiene <b>${tam}</b> vértices. <code>maxim = max(maxim, ${tam}) = ${maxim}</code>.`, [L('comp', 'maxim = max(maxim, tam);')], V(v));
    }
  }
  C.snap(`<b>Fin.</b> ${nc} componente${nc === 1 ? '' : 's'} conexa${nc === 1 ? '' : 's'} de tamaños [${tams.join(', ')}]; la mayor tiene <b>${maxim}</b>. ${nc === 1 ? 'El grafo es <b>conexo</b>.' : ''} ${nc === 1 && G.A === n - 1 ? 'Además A = V − 1 = ' + (n - 1) + ': es un <b>árbol libre</b> (04-1).' : ''}`, [L('comp', 'int maximo() const')], V(-1));
  return C.f;
};

/* ---- Bipartito: DFS coloreando (Bipartito) ---- */
ALGOS.bip = () => {
  const n = G.n, visit = Array(n).fill(false), color = Array(n).fill(null), C = ctx(), S = C.st;
  let bipar = true;
  const V = hot => [vecOf('visit', visit.map(x => x ? 'T' : 'F'), hot, x => x === 'T'), vecOf('color', color.map(c => c === null ? null : (c ? 'true' : 'false')), -1, x => x !== null)];
  const paint = (v) => { S.node[v] = color[v] ? 's-q' : 's-vis'; S.tag[v] = color[v] ? 'true' : 'false'; };
  C.snap(`<code>Bipartito(g)</code>: nadie visitado y <code>bipar = true</code>. Colores: <b style="color:var(--blue)">false</b> (azul) y <b style="color:var(--purple)">true</b> (morado).`, [L('bip', 'visit(g.V(), false), color(g.V(), false), bipar(true)')], V(-1));
  function dfs(v) {
    visit[v] = true; S.node[v] = 's-cur';
    C.snap(`<code>dfs(${v})</code>: ${v} ya tiene color (${color[v]}), lo marco como visitado.`, [L('bip', 'visit[v] = true;')], V(v));
    for (const w of G.ady[v]) {
      if (!bipar) return;
      const k = ek(v, w), prev = S.edge[k]; S.edge[k] = 'cur';
      if (!visit[w]) {
        color[w] = !color[v]; paint(w);
        C.snap(`Vecino ${w} sin visitar: le doy el color contrario al de ${v}: <code>color[${w}] = !color[${v}] = ${color[w]}</code>, y bajo a él.`, [L('bip', 'if (!visit[w])'), L('bip', 'color[w] = !color[v];'), L('bip', 'dfs(g, w);')], V(w));
        S.edge[k] = 'tree';
        dfs(w);
        if (bipar) S.node[v] = 's-cur';
      } else if (color[w] === color[v]) {
        bipar = false; S.node[v] = 's-red'; S.node[w] = 's-red'; S.edge[k] = 'back';
        C.snap(`Vecino ${w}: ya visitado y con <b>el mismo color</b> que ${v} (${color[v]}). Una arista entre iguales ⇒ ciclo de longitud impar ⇒ <b>NO es bipartito</b>. <code>bipar = false</code> y todo el DFS corta.`, [L('bip', 'else if (color[w] == color[v]) bipar = false;')], V(w));
        return;
      } else {
        C.snap(`Vecino ${w}: ya visitado, con color distinto a ${v}. La arista es compatible.`, [L('bip', 'else if (color[w] == color[v]) bipar = false;')], V(w));
        S.edge[k] = prev || '';
      }
    }
    if (bipar) { paint(v); }
  }
  for (let v = 0; v < n && bipar; v++) {
    if (!visit[v]) {
      color[v] = false; paint(v);
      C.snap(`${v} sin visitar: nueva componente. Su primer vértice puede ir de cualquier color: <code>color[${v}] = false</code>.`, [L('bip', 'if (!visit[v])'), L('bip', 'color[v] = false;')], V(v));
      dfs(v);
    }
  }
  if (bipar) C.snap(`<b>Fin: SÍ es bipartito.</b> Los vértices azules y los morados forman las dos mitades; toda arista une un azul con un morado.`, [L('bip', 'bool esBipartito() const')], V(-1));
  else C.snap(`<b>Fin: NO es bipartito.</b> Los dos vértices rojos están unidos y tienen el mismo color.`, [L('bip', 'bool esBipartito() const')], V(-1));
  return C.f;
};
