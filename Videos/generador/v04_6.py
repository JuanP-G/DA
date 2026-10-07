"""Vídeo EJ 04-6 · Un nodo muy muy lejano"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line

CPP = "../../EJ_04-6/EJ_04-6.cpp"
NOMBRE = "Un nodo muy muy lejano"

# red 1 del ejemplo; nodos 1..7 -> vértices 0..6
ENTRADA = [(1, 2), (2, 3), (1, 4), (4, 5), (5, 6), (4, 6), (6, 7)]
N = 7
E = [(a - 1, b - 1) for a, b in ENTRADA]
LAB = {v: str(v + 1) for v in range(N)}
P = {0: (760, 150), 1: (760, 255), 2: (760, 360), 3: (900, 150), 4: (1050, 150), 5: (975, 280), 6: (1140, 330)}

L_BFS = find_line(CPP, "void bfs(")
L_INI = [find_line(CPP, "dist[origen] = 0;"), find_line(CPP, "++alcanzados;", L_BFS), find_line(CPP, "q.push(origen);")]
L_POP = find_line(CPP, "int v = q.front(); q.pop();")
L_CUT = find_line(CPP, "if (dist[v] == ttl) continue;")
L_NEW = find_line(CPP, "if (dist[w] == -1)")
L_SET = [find_line(CPP, "dist[w] = dist[v] + 1;"), find_line(CPP, "++alcanzados;", L_NEW), find_line(CPP, "q.push(w);")]
CODE = code_lines(CPP, find_line(CPP, "class NodosAlcanzables"), find_line(CPP, "};", L_BFS),
                  skip=[(find_line(CPP, "int inalcanzables()") - 1, find_line(CPP, "int alcanzados;") + 1)])


def ady():
    a = [[] for _ in range(N)]
    for v, w in E:
        a[v].append(w)
        a[w].append(v)
    return a


def traza(origen, ttl):
    a = ady()
    dist = [-1] * N
    q = deque()
    pasos = []
    dist[origen] = 0
    alc = 1
    q.append(origen)
    pasos.append(("ini", origen, None, dist[:], list(q), alc))
    while q:
        v = q.popleft()
        if dist[v] == ttl:
            pasos.append(("corta", v, None, dist[:], list(q), alc))
            continue
        pasos.append(("saca", v, None, dist[:], list(q), alc))
        for w in a[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                alc += 1
                q.append(w)
                pasos.append(("descubre", v, w, dist[:], list(q), alc))
    return pasos


def estilo(dist, actual):
    ns = {}
    for u, d in enumerate(dist):
        if d >= 0:
            ns[u] = (["gold", "blue", "purple", "green"][min(d, 3)], "node_t", None)
    if actual is not None:
        ns[actual] = (ns.get(actual, ("node",))[0], "node_t", "text")
    return ns


def slide_paso(k, n, tipo, v, w, dist, q, alc, ttl, hl, cap):
    s = Slide(f"Ejecución · origen 4, TTL {ttl}", f"paso {k} de {n}")
    s.code(24, 84, 610, 520, CODE, hl=hl, title="class NodosAlcanzables")
    s.box(652, 84, 604, 330, "red (nodos 1..7)")
    es = {(v, w): ("gold", 6)} if w is not None else None
    s.graph(P, E, ns=estilo(dist, v), es=es, labels=LAB,
            under={u: f"d={d}" for u, d in enumerate(dist) if d >= 0})
    s.box(652, 430, 604, 174, "estado")
    s.cells(672, 455, "dist", [d if d >= 0 else "·" for d in dist], first=1,
            colors={u: "blue_d" for u, d in enumerate(dist) if d >= 0}, hl={w} if w is not None else None)
    s.queue_row(672, 520, "cola", [u + 1 for u in q])
    s.text((1080, 528), "alcanzados", size=17, color="muted", bold=True)
    s.pill(1200, 520, str(alc), fill="gold")
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-6"),
             "Un nodo muy muy lejano. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    segs.append((ideas("El problema", [
        "Cada mensaje lleva un TTL: cuántos saltos le quedan.",
        "Cada nodo que lo recibe resta 1. Si llega a 0, ya no lo reenvía.",
        "Si no, lo reenvía a todos sus vecinos.",
        "Para cada consulta (origen, TTL): ¿cuántos nodos NO reciben el mensaje?",
    ]), "Cada mensaje lleva un campo T T L, que dice cuántos saltos le quedan. Cada nodo que lo recibe le resta uno: "
        "si llega a cero ya no lo reenvía, y si no, lo reenvía a todos sus vecinos. "
        "Para cada consulta, con un nodo origen y un T T L, nos piden cuántos nodos no reciben el mensaje.", 0))

    s = Slide("La clave: traducirlo a grafos")
    s.box(60, 90, 560, 380, "red del ejemplo")
    s.graph({v: (x - 640, y + 30) for v, (x, y) in P.items()}, E, labels=LAB,
            ns=estilo([1, 2, 3, 0, 1, 1, 2], 3), under={0: "1", 1: "2", 2: "3", 3: "0", 4: "1", 5: "1", 6: "2"})
    s.bullets(660, 110, 560, [
        "Cada salto a un vecino gasta 1 de TTL.",
        ("w recibe el mensaje  ⇔  distancia(origen, w) ≤ TTL", "gold"),
        "distancia = mínimo número de aristas.",
        "Desde 4 con TTL 2: llegan todos menos el 3 (está a distancia 3).",
        "Respuesta = N − alcanzados.",
    ], size=22)
    segs.append((s, "La clave es traducir la historia a grafos. Cada salto de un nodo a un vecino gasta uno de T T L. "
                    "Por tanto, un nodo recibe el mensaje si y solo si su distancia al origen, contada en aristas, es menor o igual que el T T L.", 0))
    segs.append((s, "Aquí, desde el nodo cuatro, los números de debajo son las distancias. Con T T L dos llegan todos menos el tres, que está a distancia tres. "
                    "La respuesta es el número de nodos menos los alcanzados.", 0))

    segs.append((ideas("¿Cómo se calculan distancias? BFS", [
        "Grafo SIN pesos + distancia mínima en aristas  ⇒  recorrido en ANCHURA (BFS).",
        "El BFS visita los vértices por orden de distancia: primero los de distancia 1, luego los de 2...",
        "La PRIMERA vez que llega a un vértice, lo hace por el camino más corto.",
        "Además se puede cortar: un nodo con dist == TTL no reenvía.",
    ]), "Distancias mínimas en un grafo sin pesos: eso es un recorrido en anchura, un B F S. "
        "El B F S usa una cola y visita los vértices por orden de distancia: primero los que están a uno, luego los que están a dos, y así. "
        "Por eso la primera vez que llega a un vértice lo hace por el camino más corto.", 0))

    # por qué no DFS
    s = Slide("¿Y por qué no un DFS?")
    dfs_d = {3: 0, 0: 1, 1: 2, 2: 3, 4: 1, 5: 2, 6: 3}
    s.box(60, 90, 560, 380, "DFS desde 4 (profundidad de llegada)")
    s.graph({v: (x - 640, y + 30) for v, (x, y) in P.items()}, E, labels=LAB,
            ns={6: ("red", "node_t", None), 3: ("gold", "node_t", None)},
            es={(3, 0): ("gold", 4), (0, 1): ("gold", 4), (1, 2): ("gold", 4), (3, 4): ("gold", 4), (4, 5): ("gold", 4), (5, 6): ("gold", 4)},
            under={v: str(d) for v, d in dfs_d.items()})
    s.box(660, 90, 560, 380, "BFS desde 4 (distancia real)")
    s.graph({v: (x - 40, y + 30) for v, (x, y) in P.items()}, E, labels=LAB,
            ns={6: ("green", "node_t", None), 3: ("gold", "node_t", None)},
            es={(3, 0): ("gold", 4), (0, 1): ("gold", 4), (3, 4): ("gold", 4), (3, 5): ("gold", 4), (5, 6): ("gold", 4), (1, 2): ("gold", 4)},
            under={0: "1", 1: "2", 2: "3", 3: "0", 4: "1", 5: "1", 6: "2"})
    s.caption("El DFS llega al 7 por 4-5-6-7 (3 saltos) y lo daría por perdido con TTL 2.", y=500)
    s.caption("El BFS lo encuentra por 4-6-7 (2 saltos): sí recibe el mensaje.", y=540)
    segs.append((s, "¿Y por qué no vale un D F S? Porque puede llegar primero a un nodo por un camino largo. "
                    "Desde el cuatro, el D F S llega al siete pasando por el cinco y el seis: tres saltos, y con T T L dos lo daría por inalcanzable.", 0))
    segs.append((s, "Pero hay un atajo, cuatro, seis, siete, de solo dos saltos. El B F S lo encuentra porque va por capas de distancia.", 0))

    s = Slide("El código", "EJ_04-6.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_CUT, L_NEW} | set(L_SET), title="class NodosAlcanzables")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, [
        "dist[v] = -1 significa: aún no alcanzado.",
        "Se saca v de la cola; si dist[v] == TTL no se reenvía.",
        "Cada vecino nuevo: dist + 1, alcanzados + 1 y a la cola.",
        "Un BFS por consulta (como mucho 10).",
    ], size=20, gap=16)
    segs.append((s, "En el código, dist vale menos uno para los nodos no alcanzados. Sacamos un nodo de la cola; si su distancia ya es igual al T T L, "
                    "no reenvía y pasamos al siguiente. Si no, cada vecino nuevo recibe la distancia más uno, se cuenta como alcanzado y entra en la cola.", 0))

    pasos = traza(3, 2)
    n = len(pasos)
    for k, (tipo, v, w, dist, q, alc) in enumerate(pasos, 1):
        if tipo == "ini":
            hl, cap = set(L_INI), "dist[4] = 0, alcanzados = 1, el 4 entra en la cola"
            nar = "Empezamos en el nodo cuatro: distancia cero, alcanzados uno, y lo metemos en la cola."
        elif tipo == "saca":
            hl, cap = {L_POP}, f"Sacamos el {v + 1} (dist {dist[v]} < TTL): reenvía a sus vecinos"
            nar = f"Sacamos el {v + 1}. Su distancia es {dist[v]}, menor que el T T L, así que reenvía."
        elif tipo == "descubre":
            hl, cap = set(L_SET) | {L_NEW}, f"{w + 1} es nuevo: dist[{w + 1}] = {dist[w]}, alcanzados = {alc}"
            nar = f"El {w + 1} es nuevo: distancia {dist[w]}. Ya van {alc}."
        else:
            hl, cap = {L_POP, L_CUT}, f"Sacamos el {v + 1}: dist = TTL = 2, el mensaje no sigue"
            nar = f"Sacamos el {v + 1}. Está a distancia dos, igual que el T T L: aquí el mensaje no sigue."
        segs.append((slide_paso(k, n, tipo, v, w, dist, q, alc, 2, hl, cap), nar, 0))

    segs.append((ideas("Resultado y resto de consultas", [
        "origen 4, TTL 2: alcanzados 6 de 7  ⇒  1",
        "origen 4, TTL 3: llega también al 3  ⇒  0",
        "origen 7, TTL 3: el 7 está lejos del 2 y del 3  ⇒  2",
        "origen 1, TTL 0: solo el propio 1  ⇒  6",
        ("Después de las consultas de cada red se escribe ---", "muted"),
    ]), "La cola se ha vaciado con seis nodos alcanzados de siete: la respuesta es uno. "
        "Con T T L tres llegaría también al tres y la respuesta sería cero. Y con T T L cero solo se alcanza el propio origen.", 0))

    segs.append((cierre(NOMBRE, [
        "Recibe el mensaje  ⇔  distancia(origen, w) ≤ TTL.",
        "Distancias en un grafo sin pesos  ⇒  BFS (un DFS puede llegar por un camino largo).",
        "Se corta el BFS cuando dist[v] == TTL.",
        "Respuesta = N − alcanzados.   Coste: O(N + C) por consulta.",
    ]), "Resumiendo: un nodo recibe el mensaje si su distancia al origen no supera el T T L. "
        "Las distancias se calculan con un B F S, que se puede cortar al llegar al T T L, y la respuesta es el número de nodos menos los alcanzados.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-6_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-6_nodo_muy_lejano.mp4")
        print(f"04-6: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
