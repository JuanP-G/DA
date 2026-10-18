"""Piezas comunes de los vídeos del tema 7 (Dijkstra): simulación con traza y dibujo del estado."""
from vidlib import Slide, C, font

INF = 10 ** 9
FINITO = lambda d: d < INF


def traza(n, edges, s, und=False, carga=None, parar=None, contar=False):
    """
    Simula Dijkstra tal como lo hace el .cpp (vértice de menor dist primero; a igualdad, el de menor número).
    edges: [(a, b, coste)]. und=True: cada arista se recorre en los dos sentidos.
    carga: coste de llegar a cada vértice (07-1). contar: cuenta caminos mínimos (07-2).
    Devuelve una lista de pasos (diccionarios) con una copia del estado en cada uno.
    """
    adj = [[] for _ in range(n)]
    for k, (a, b, c) in enumerate(edges):
        adj[a].append((b, c, k))
        if und:
            adj[b].append((a, c, k))
    dist, ulti, formas, done = [INF] * n, [None] * n, [0] * n, [False] * n
    dist[s] = carga[s] if carga else 0
    formas[s] = 1
    pq = {s}
    pasos = []

    def snap(tipo, **kw):
        pasos.append(dict(tipo=tipo, dist=dist[:], ulti=ulti[:], formas=formas[:], done=done[:],
                          cola=sorted(pq, key=lambda v: (dist[v], v)), **kw))

    snap("ini")
    while pq:
        v = min(pq, key=lambda u: (dist[u], u))
        pq.discard(v)
        done[v] = True
        snap("saca", v=v)
        if parar is not None and v == parar:
            snap("fin", v=v)
            break
        for (w, c, k) in adj[v]:
            coste = c + (carga[w] if carga else 0)
            nuevo = dist[v] + coste
            if nuevo < dist[w]:
                ant = dist[w]
                dist[w], ulti[w], formas[w] = nuevo, v, formas[v]
                pq.add(w)
                snap("mejora", v=v, w=w, k=k, nuevo=nuevo, ant=ant, coste=coste, c=c)
            elif contar and nuevo == dist[w]:
                formas[w] += formas[v]
                snap("empata", v=v, w=w, k=k, nuevo=nuevo, coste=coste, c=c)
            else:
                snap("peor", v=v, w=w, k=k, nuevo=nuevo, coste=coste, c=c)
    return pasos


def etiquetas(s, pos, edges, hl=None, textos=None, dirigido=True):
    """Pone el valor de cada arista en su centro. hl: {k: color}. textos: {k: texto} para sustituir el valor."""
    hl = hl or {}
    textos = textos or {}
    for k, (a, b, c) in enumerate(edges):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        t = str(textos.get(k, c))
        f = font(16, True)
        w = s.d.textlength(t, font=f) + 12
        col = hl.get(k)
        s.d.rounded_rectangle((mx - w / 2, my - 12, mx + w / 2, my + 12), 6, fill=C["panel"],
                              outline=C[col] if col else C["border"], width=2)
        s.d.text((mx, my), t, font=f, fill=C[col] if col else C["text"], anchor="mm")


def dibuja_grafo(s, pos, edges, paso, dirigido=True, r=22, carga=None, hl_edge=None, extra_ns=None, caminos=None,
                 etiq=None, first=0, es_extra=None, hl_extra=None):
    """Grafo con el estado de un paso: hechos en verde, en cola en morado, aristas de ulti[] en azul."""
    n = len(pos)
    ns = {}
    for v in range(n):
        if paso["done"][v]:
            ns[v] = ("green", "node_t", None)
        elif v in paso["cola"]:
            ns[v] = ("purple", "node_t", None)
    es, hl = {}, {}
    arbol = {}
    for w in range(n):
        u = paso["ulti"][w]
        if u is not None:
            arbol[(u, w)] = 1
    for k, (a, b, c) in enumerate(edges):
        if (a, b) in arbol or (b, a) in arbol and not dirigido:
            es[(a, b)] = ("blue", 5)
            hl[k] = "blue"
    if hl_edge is not None:
        k = hl_edge
        a, b, c = edges[k]
        es[(a, b)] = ("gold", 7)
        hl[k] = "gold"
    if paso["tipo"] in ("saca", "fin") and paso.get("v") is not None:
        ns[paso["v"]] = ("green", "node_t", "gold")
    if paso["tipo"] in ("mejora", "empata", "peor"):
        ns[paso["v"]] = ("green", "node_t", "gold")
        w = paso["w"]
        ns[w] = (ns.get(w, ("node",))[0], "node_t", "text")
    if es_extra:
        es.update(es_extra)
    if hl_extra:
        hl.update(hl_extra)
    if extra_ns:
        ns.update(extra_ns)
    under = {v: str(d) for v, d in enumerate(paso["dist"]) if FINITO(d)}
    if paso.get("_formas"):
        under = {v: f"{d}×{paso['formas'][v]}" for v, d in enumerate(paso["dist"]) if FINITO(d)}
    labels = [str(v + first) for v in range(n)]
    over = {v: f"c={carga[v]}" for v in range(n)} if carga else None
    if dirigido:
        s.dgraph(pos, [(a, b) for a, b, c in edges], ns=ns, es=es, r=r, under=under, labels=labels)
    else:
        s.graph(pos, [(a, b) for a, b, c in edges], ns=ns, es=es, r=r, under=under, over=over, labels=labels)
    if dirigido and over:
        for v, t in over.items():
            s.d.text((pos[v][0], pos[v][1] - r - 10), t, font=font(16), fill=C["muted"], anchor="md")
    etiquetas(s, pos, edges, hl, etiq, dirigido)


def estado(s, x, y, paso, n, contar=False, w=572, first=0, dy=62, con_cola=True):
    """Vectores dist, ulti (padre), formas y la cola de prioridad."""
    d = [("∞" if not FINITO(v) else v) for v in paso["dist"]]
    cw = 44 if n <= 8 else 36
    hot = set()
    if paso.get("w") is not None:
        hot = {paso["w"]}
    col = {v: "green_d" for v in range(n) if paso["done"][v]}
    s.cells(x, y, "dist", d, first=first, cw=cw, hl=hot, colors=col)
    s.cells(x, y + dy, "ulti", ["–" if u is None else u + first for u in paso["ulti"]], first=first, cw=cw, hl=hot)
    yy = y + 2 * dy
    if contar:
        s.cells(x, yy, "formas", [paso["formas"][v] if FINITO(paso["dist"][v]) else 0 for v in range(n)], first=first, cw=cw, hl=hot)
        yy += dy
    if not con_cola:
        return
    cola = [f"{v + first}({paso['dist'][v]})" for v in paso["cola"]]
    s.queue_row(x, yy, "cola", cola)
