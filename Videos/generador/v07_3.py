"""Vídeo EJ 07-3 · RapidEats con ruta"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07_comun import traza, dibuja_grafo, estado, FINITO

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-3/EJ_07-3.cpp"
NOMBRE = "RapidEats con ruta"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1: 4 puntos y 4 tramos (vértices 0..3 = puntos 1..4); pedidos 1→3 y 4→1
EDGES = [(0, 1, 15), (0, 2, 30), (1, 2, 20), (3, 2, 10)]
POS = {0: (760, 230), 1: (940, 140), 2: (960, 330), 3: (1160, 330)}

L_INI = [find_line(CPP, "dist[origen] = 0;"), find_line(CPP, "pq.push(origen, 0);")]
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_BRK = find_line(CPP, "if (v == destino) break;")
L_FOR = find_line(CPP, "for (auto a : g.ady(v))")
L_IF = find_line(CPP, "if (dist[w] > dist[v] + a.valor())")
L_SET = [find_line(CPP, "dist[w] = dist[v] + a.valor();"), find_line(CPP, "ulti[w] = v;"), find_line(CPP, "pq.update(w, dist[w]);")]
L_NO = find_line(CPP, 'cout << "NO LLEGA\\n";')
L_RET = find_line(CPP, "for (int v = destino; v != origen; v = ulti[v]) camino.push_front(v);")
L_PUSH0 = find_line(CPP, "camino.push_front(origen);")
L_OUT = [find_line(CPP, 'cout << dist[destino] << ":";'), find_line(CPP, "cout << (i == 0")]
INI = find_line(CPP, "// Dijkstra desde el origen del pedido")
CODE = [(n, t) for n, t in code_lines(CPP, INI, find_line(CPP, "cout << \"---\\n\";"), maxc=64) if t.strip()]
CODE = [(n, t) for n, t in CODE if not (find_line(CPP, "int K; cin >> K;") <= n <= INI)]
CODE_D = [(n, t) for n, t in CODE if n <= find_line(CPP, "if (dist[destino] == INF) {") - 1]
CODE_R = [(n, t) for n, t in code_lines(CPP, find_line(CPP, "if (dist[destino] == INF) {"), find_line(CPP, 'cout << "---\\n";'), maxc=70) if t.strip()]


def slide_paso(k, n, paso, hl, cap, titulo):
    s = Slide(titulo, f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE_D, hl=hl, title="Dijkstra desde el origen del pedido")
    s.box(684, 84, 572, 310, "la ciudad (valor = minutos del tramo)")
    dibuja_grafo(s, POS, EDGES, paso, dirigido=False, r=22, hl_edge=paso.get("k"), first=1)
    s.box(684, 410, 572, 194, "estado")
    estado(s, 704, 436, paso, 4, first=1)
    s.caption(cap, y=628)
    return s


def traza_pedido(titulo, origen, destino, segs, edges=EDGES, n=4):
    pasos = traza(n, edges, origen, und=True, parar=destino)
    N = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl, cap = set(L_INI), f"dist[{origen + 1}] = 0 y el punto {origen + 1} entra en la cola"
            nar = f"Empezamos en el punto {origen + 1}: distancia cero, y a la cola."
        elif t == "saca":
            hl, cap = {L_POP}, f"Sale el punto {v + 1}, dist = {p['dist'][v]}: definitiva"
            nar = f"Sacamos el punto {v + 1}, con distancia {p['dist'][v]}. Ya es definitiva."
        elif t == "fin":
            hl, cap = {L_POP, L_BRK}, f"Es el destino: dist = {p['dist'][v]}, paramos"
            nar = f"Es el destino, el {v + 1}, a distancia {p['dist'][v]}. Paramos."
        else:
            w = p["w"]
            if t == "mejora":
                hl = {L_FOR, L_IF} | set(L_SET)
                ant = "∞" if not FINITO(p["ant"]) else p["ant"]
                cap = f"{v + 1}–{w + 1}: {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: mejora, ulti[{w + 1}] = {v + 1}"
                nar = f"Tramo de {v + 1} a {w + 1}: {p['nuevo']}, " + ("antes infinito" if not FINITO(p["ant"]) else f"antes {p['ant']}") + f". Mejora, y ulti de {w + 1} pasa a ser {v + 1}."
            else:
                hl = {L_FOR, L_IF}
                cap = f"{v + 1}–{w + 1}: {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
                nar = f"Tramo de {v + 1} a {w + 1}: {p['nuevo']}, que no mejora {p['dist'][w]}."
        segs.append((slide_paso(k, N, p, hl, cap, titulo), nar, 0))
    return pasos[-1]


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-3", TEMA),
             "RapidEats con ruta. Dijkstra directo, y además tenemos que decir por dónde se va: lo hace el vector ulti.", 0)]

    segs.append((ideas("El problema", [
        "N puntos de la ciudad (hasta 20.000) y C tramos de calle con minutos (1 a 500).",
        "Los tramos se recorren en AMBOS sentidos; puede haber varios entre los mismos puntos.",
        "K ≤ 10 pedidos por caso: de un origen a un destino.",
        "Para cada pedido: el tiempo mínimo y la ruta   «40: 4 -> 3 -> 1»   o   NO LLEGA.",
        ("Después de cada caso, una línea  ---", "muted"),
    ]), "Tenemos una ciudad con puntos de recarga y tramos de calle, con su duración. Los tramos se recorren en los dos sentidos. "
        "Para cada pedido, de un origen a un destino, hay que escribir el tiempo mínimo y la ruta que lo consigue. "
        "Si no hay camino, escribimos no llega. Y después de cada caso, una línea de guiones.", 0))

    s = Slide("Cómo se plantea")
    s.bullets(70, 120, W_ := 1140, [
        "Es un camino de coste mínimo: Dijkstra directo, sin trucos.",
        ("Además hay que dar el CAMINO: ulti[w] guarda el vértice anterior en el camino mínimo.", "gold"),
        "Un Dijkstra por pedido: los orígenes pueden ser distintos (K ≤ 10).",
        "Cada tramo = dos aristas dirigidas; los tramos repetidos no molestan (gana el más rápido).",
        "Al sacar el destino de la cola, su distancia ya es definitiva: se puede parar.",
    ], size=25, gap=22)
    segs.append((s, "Es un camino de coste mínimo, así que usamos Dijkstra directamente. Además tenemos que dar la ruta, y para eso guardamos en ulti, para cada punto, el punto anterior en el camino mínimo. "
                    "Ejecutamos un Dijkstra por cada pedido, porque los orígenes pueden ser distintos. Cada tramo son dos aristas dirigidas, y si hay varios tramos entre los mismos puntos, gana el más rápido. "
                    "Y podemos parar al sacar el destino.", 0))

    s = Slide("El código: Dijkstra con ulti", "EJ_07-3.cpp")
    s.code(24, 84, 700, 520, CODE_D, hl={L_BRK, L_IF} | set(L_SET), title="un pedido")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["Mismo Dijkstra de siempre, desde el origen del pedido.",
                              "ulti[w] = v cada vez que se mejora dist[w].",
                              "ulti[origen] se queda en -1: no tiene anterior.",
                              "Si sale el destino, break."], size=20, gap=16)
    segs.append((s, "El código es el Dijkstra de siempre. La única novedad es que cada vez que mejoramos la distancia de w, apuntamos en ulti de w el vértice v de donde venimos. "
                    "El origen no tiene anterior, así que se queda en menos uno. Y si sale el destino, paramos.", 0))

    fin = traza_pedido("Pedido 4 → 1 del ejemplo 1", 3, 0, segs)

    # reconstrucción
    camino = [0]
    v = 0
    while v != 3:
        v = fin["ulti"][v]
        camino.append(v)
    camino.reverse()
    cam_edges = {}
    for a, b in zip(camino, camino[1:]):
        for k, (x, y, c) in enumerate(EDGES):
            if {x, y} == {a, b}:
                cam_edges[k] = (x, y)
    pf = dict(fin, tipo="fin", v=None, cola=[])

    def slide_ruta(k_pasos, cur, cap, hl, titulo="Reconstruir la ruta hacia atrás"):
        s = Slide(titulo, "ulti[]")
        s.code(24, 84, 640, 520, CODE_R, hl=hl, title="escribir el camino")
        s.box(684, 84, 572, 310, "ulti[] marca el camino hacia atrás")
        es, hlx = {}, {}
        for k in k_pasos:
            a, b = cam_edges[k]
            es[(a, b)] = ("gold", 7)
            hlx[k] = "gold"
        extra = {u: ("green", "node_t", "gold") for u in cur}
        dibuja_grafo(s, POS, EDGES, pf, dirigido=False, r=22, first=1, es_extra=es, hl_extra=hlx, extra_ns=extra)
        s.box(684, 410, 572, 194, "estado")
        estado(s, 704, 436, pf, 4, first=1, con_cola=False)
        s.queue_row(704, 560, "camino", [str(u + 1) for u in cur])
        s.caption(cap, y=628)
        return s

    segs.append((slide_ruta([], [0], "camino.push_front(1): empezamos por el destino", {L_RET}),
                 "Para escribir la ruta retrocedemos desde el destino. Metemos el punto uno por delante.", 0))
    cur = [0]
    ks = []
    v = 0
    while v != 3:
        u = fin["ulti"][v]
        for k, (x, y, c) in enumerate(EDGES):
            if {x, y} == {u, v}:
                ks.append(k)
        cur.insert(0, u)
        cap = f"ulti[{v + 1}] = {u + 1}: camino = {' → '.join(str(z + 1) for z in cur)}"
        segs.append((slide_ruta(list(ks), list(cur), cap, {L_RET} | ({L_PUSH0} if u == 3 else set())),
                     f"El anterior de {v + 1} es {u + 1}. Lo metemos por delante: " + ", ".join(str(z + 1) for z in cur) + ".", 0))
        v = u
    tiempo = fin["dist"][0]
    segs.append((slide_ruta(list(ks), list(cur), f"Salida:   {tiempo}: " + " -> ".join(str(z + 1) for z in cur), set(L_OUT)),
                 f"Ya tenemos la ruta. Escribimos el tiempo, {tiempo}, dos puntos, y los puntos separados por flechas, sumando uno porque en el enunciado se numeran desde uno.", 0))

    s = Slide("El segundo caso y los guiones")
    s.box(40, 90, 620, 440, "caso 2: tramos 1–3 (10) y 2–4 (20); pedidos 1→2 y 3→1")
    E2 = [(0, 2, 10), (1, 3, 20)]
    pl = {0: (130, 190), 1: (130, 400), 2: (560, 190), 3: (560, 400)}
    p2 = dict(traza(4, E2, 0, und=True)[-1], tipo="fin", v=None, cola=[])
    dibuja_grafo(s, pl, E2, p2, dirigido=False, r=24, first=1, extra_ns={1: ("red", "node_t", None), 3: ("red", "node_t", None)})
    s.text((690, 120), "Salida del ejemplo:", size=22, color="muted", bold=True)
    for i, ln in enumerate(["30: 1 -> 3", "40: 4 -> 3 -> 1", "---", "NO LLEGA", "10: 3 -> 1", "---"]):
        s.text((700, 165 + i * 40), ln, size=24, mono=True, color="gold" if ln == "---" else ("red" if ln == "NO LLEGA" else "text"))
    segs.append((s, "En el segundo caso, los puntos uno y tres están conectados entre sí, y el dos y el cuatro también, pero no hay camino entre los dos grupos. "
                    "Del uno al dos, escribimos no llega. Del tres al uno, son diez minutos. Y después de cada caso, la línea de guiones.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(K · C log N) por caso: un Dijkstra por pedido.",
        "El grafo se construye UNA vez por caso; los vectores, en cada pedido.",
        "Tramos de doble sentido: dos ponArista. Varios tramos iguales: gana el más rápido.",
        "Formato:  tiempo: a -> b -> c   (con espacios) y --- tras cada caso.",
        ("Si varias rutas empatan, vale cualquiera.", "muted"),
    ]), "El coste es K por C por logaritmo de N en cada caso. El grafo se construye una vez y los vectores se crean para cada pedido. "
        "Ojo con el formato: el tiempo, dos puntos, y los puntos con flechas y espacios. Y los guiones después de cada caso.", 0))

    segs.append((cierre(NOMBRE, [
        "Camino de coste mínimo  ⇒  Dijkstra con IndexPQ.",
        "ulti[w] = v al mejorar dist[w]: el anterior en el camino mínimo.",
        "La ruta: retroceder desde el destino y meter por delante (push_front).",
        "Sin camino: dist[destino] = INF  ⇒  NO LLEGA.   Un Dijkstra por pedido.",
    ]), "Resumiendo: Dijkstra, guardando para cada punto el anterior. Para la ruta, retrocedemos desde el destino. Si no hay camino, no llega.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-3_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-3_rapideats.mp4")
        print(f"07-3: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
