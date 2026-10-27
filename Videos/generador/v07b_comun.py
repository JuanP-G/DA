"""Piezas comunes de los vídeos 07-4 a 07-7: Dijkstra con traza (varios orígenes, prioridad compuesta, corte)."""
from vidlib import Slide, C, font
from v07_comun import etiquetas

INF = 10 ** 9


def traza(n, arcs, srcs, und=False, add=lambda d, c: d + c, zero=0, inf=INF, corta_si=None):
    """
    Dijkstra tal como en el .cpp (sale el de menor dist; a igualdad, el de menor número).
    arcs: [(a, b, coste)]; und=True: cada arista vale en los dos sentidos. srcs: varios orígenes.
    corta_si(d): tras sacar un vértice con esa dist se corta (07-7).
    """
    adj = [[] for _ in range(n)]
    for k, (a, b, c) in enumerate(arcs):
        adj[a].append((b, c, k))
        if und:
            adj[b].append((a, c, k))
    dist, ulti, done = [inf] * n, [None] * n, [False] * n
    for s in srcs:
        dist[s] = zero
    pq = set(srcs)
    pasos = []

    def snap(tipo, **kw):
        pasos.append(dict(tipo=tipo, dist=dist[:], ulti=ulti[:], done=done[:],
                          cola=sorted(pq, key=lambda v: (dist[v], v)), **kw))

    snap("ini")
    while pq:
        v = min(pq, key=lambda u: (dist[u], u))
        pq.discard(v)
        done[v] = True
        snap("saca", v=v)
        if corta_si and corta_si(dist[v]):
            snap("corta", v=v)
            break
        for (w, c, k) in adj[v]:
            nuevo = add(dist[v], c)
            if nuevo < dist[w]:
                ant = dist[w]
                dist[w], ulti[w] = nuevo, v
                pq.add(w)
                snap("mejora", v=v, w=w, k=k, nuevo=nuevo, ant=ant, c=c)
            else:
                snap("peor", v=v, w=w, k=k, nuevo=nuevo, c=c)
    return pasos


def dibuja(s, pos, arcs, paso, dirigido, fmt, inf=INF, first=1, base=None, flip=False, r=22, extra_es=None):
    """Grafo con el estado de un paso. base: {v: relleno} (p.ej. bandos) que no cambia con done/cola.
    flip: dibuja las flechas al revés (grafo inverso)."""
    n = len(pos)
    base = base or {}
    ns = {}
    for v in range(n):
        if v in base:
            ns[v] = (base[v], "node_t", None)
        elif paso["done"][v]:
            ns[v] = ("green", "node_t", None)
        elif v in paso["cola"]:
            ns[v] = ("purple", "node_t", None)
    es, hl = {}, {}
    tree = {(u, w) for w, u in enumerate(paso["ulti"]) if u is not None}
    dib = [(b, a) if flip else (a, b) for a, b, c in arcs]
    for k, (a, b, c) in enumerate(arcs):
        key = (b, a) if flip else (a, b)
        enarbol = (b, a) in tree if flip else (a, b) in tree
        if enarbol or (not dirigido and (b, a) in tree):
            es[key] = ("blue", 5)
            hl[k] = "blue"
    if extra_es:
        es.update(extra_es)
    t, v, w, k = paso["tipo"], paso.get("v"), paso.get("w"), paso.get("k")
    if k is not None:
        a, b, c = arcs[k]
        es[(b, a) if flip else (a, b)] = ("gold", 7)
        hl[k] = "gold"
    if t in ("saca", "corta") and v is not None:
        ns[v] = (ns.get(v, ("green",))[0], "node_t", "gold")
    if t in ("mejora", "peor"):
        ns[v] = (ns.get(v, ("green",))[0], "node_t", "gold")
        ns[w] = (ns.get(w, ("node",))[0], "node_t", "text")
    under = {u: fmt(d) for u, d in enumerate(paso["dist"]) if (d[0] if isinstance(d, tuple) else d) < inf}
    labels = [str(u + first) for u in range(n)]
    if dirigido:
        el = {((b, a) if flip else (a, b)): (str(c), hl.get(k, "text") if hl.get(k) else "muted") for k, (a, b, c) in enumerate(arcs)}
        s.dgraph(pos, dib, ns=ns, es=es, r=r, under=under, labels=labels, elabels=el)
    else:
        s.graph(pos, [(a, b) for a, b, c in arcs], ns=ns, es=es, r=r, under=under, labels=labels)
        etiquetas(s, pos, arcs, hl)


def vectores(s, x, y, paso, n, fmt, first=1, cw=44, con_cola=True, dy=62, etq="dist"):
    d = [fmt(v) for v in paso["dist"]]
    hot = {paso["w"]} if paso.get("w") is not None else set()
    col = {v: "green_d" for v in range(n) if paso["done"][v]}
    s.cells(x, y, etq, d, first=first, cw=cw, hl=hot, colors=col)
    s.cells(x, y + dy, "ulti", ["–" if u is None else u + first for u in paso["ulti"]], first=first, cw=cw, hl=hot)
    if con_cola:
        cola = [f"{v + first}({fmt(paso['dist'][v])})" for v in paso["cola"]]
        s.queue_row(x, y + 2 * dy, "cola", cola, size=17)


def slide_paso(titulo, corner, code, ctitle, hl, pos, arcs, paso, dirigido, cap, fmt, n, k, N, **kw):
    s = Slide(titulo, f"{corner} · paso {k} de {N}")
    s.code(24, 84, 640, 520, code, hl=hl, title=ctitle)
    s.box(684, 84, 572, 310, kw.pop("gtitle", "el grafo"))
    cw = kw.pop("cw", 44)
    etq = kw.pop("etq", "dist")
    dibuja(s, pos, arcs, paso, dirigido, fmt, **kw)
    s.box(684, 410, 572, 194, "estado")
    vectores(s, 704, 434, paso, n, fmt, cw=cw, etq=etq)
    s.caption(cap, y=628)
    return s
