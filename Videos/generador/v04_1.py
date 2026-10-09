"""Vídeo EJ 04-1 · Árboles libres"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../4-Grafos no dirigidos/EJ_04-1/EJ_04-1.cpp"
NOMBRE = "Árboles libres"

# caso 1 y 2 del enunciado (mismas posiciones que el dibujo del PDF)
P1 = {0: (950, 150), 5: (830, 215), 4: (1070, 215), 2: (950, 265), 1: (850, 345), 3: (1050, 345)}
E1 = [(0, 5), (0, 2), (2, 1), (2, 3), (4, 3)]
P2 = {1: (790, 160), 2: (950, 160), 5: (1110, 160), 0: (790, 320), 3: (950, 320), 4: (1110, 320)}
E2 = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5)]


def ady(V, edges):
    """Mismo orden de adyacentes que Grafo::ponArista."""
    a = [[] for _ in range(V)]
    for v, w in edges:
        a[v].append(w)
        a[w].append(v)
    return a


def traza_dfs(V, edges):
    """Simula ArbolLibre::dfs y devuelve los pasos (tipo, v, w, visit, alcanzados, pila)."""
    a = ady(V, edges)
    visit = [False] * V
    pasos, pila = [], []
    cnt = [0]

    def dfs(v):
        visit[v] = True
        cnt[0] += 1
        pila.append(v)
        pasos.append(("entra", v, None, visit[:], cnt[0], pila[:]))
        for w in a[v]:
            if not visit[w]:
                dfs(w)
            else:
                pasos.append(("visto", v, w, visit[:], cnt[0], pila[:]))
        pila.pop()
        pasos.append(("sale", v, None, visit[:], cnt[0], pila[:]))

    dfs(0)
    return pasos


L_DFS = find_line(CPP, "void dfs(")
L_VIS = find_line(CPP, "visit[v] = true;")
L_ALC = find_line(CPP, "++alcanzados;")
L_FOR = find_line(CPP, "for (int w : g.ady(v))")
L_IF = find_line(CPP, "if (!visit[w]) dfs(g, w);")
L_CALL = find_line(CPP, "dfs(g, 0);")
L_CON = find_line(CPP, "bool conexo")
L_ARB = find_line(CPP, "arbol = conexo")
CODE = code_lines(CPP, find_line(CPP, "class ArbolLibre"), find_line(CPP, "};", L_DFS))


def estilo(visit, actual, pila):
    ns = {}
    for v, vis in enumerate(visit):
        if vis:
            ns[v] = ("blue", "node_t", None)
    for v in pila:
        ns[v] = ("gold", "node_t", None)
    if actual is not None:
        ns[actual] = ("gold", "node_t", "text")
    return ns


def paso_slide(caso, pos, edges, k, n, visit, cnt, pila, actual, hl, caption, es=None):
    s = Slide(f"Ejecución · Caso {caso}", f"paso {k} de {n}")
    s.code(24, 84, 610, 520, CODE, hl=hl, title="class ArbolLibre")
    s.box(652, 84, 604, 330, "grafo")
    s.graph(pos, edges, ns=estilo(visit, actual, pila), es=es)
    s.box(652, 430, 604, 174, "estado")
    s.cells(672, 470, "visit", ["T" if x else "·" for x in visit],
            colors={i: "blue_d" for i, x in enumerate(visit) if x}, hl={actual} if actual is not None else None)
    s.text((672, 540), "alcanzados", size=17, color="muted", bold=True)
    s.pill(790, 532, f"{cnt}", fill="gold")
    s.text((870, 540), "pila de llamadas", size=17, color="muted", bold=True)
    s.text((1045, 540), " → ".join(map(str, pila)) if pila else "vacía", size=18, bold=True)
    s.caption(caption, y=628)
    return s


def ejecucion(caso, pos, edges, V):
    pasos = traza_dfs(V, edges)
    segs = []
    vistos = pasos
    n = len(vistos)
    for k, (tipo, v, w, visit, cnt, pila) in enumerate(vistos, 1):
        if tipo == "entra":
            hl = {L_VIS, L_ALC}
            cap = f"dfs({v}): marcamos {v} como visitado. alcanzados = {cnt}"
            nar = (f"Entramos en el {v}. Lo marcamos y ya llevamos {cnt}." if k > 1 else
                   f"Llamamos a dfs desde el cero. Lo marcamos: alcanzados vale uno.")
            es = None
            if len(pila) > 1:
                es = {(pila[-2], v): ("gold", 5)}
        elif tipo == "visto":
            hl = {L_FOR, L_IF}
            cap = f"El vecino {w} de {v} ya está visitado: no se vuelve a entrar"
            nar = f"Desde el {v} vemos al {w}, pero ya está visitado, así que no entramos."
            es = {(v, w): ("muted", 3)}
        else:
            hl = {L_FOR}
            cap = f"{v} no tiene más vecinos nuevos: volvemos" + (f" al {pila[-1]}" if pila else "")
            nar = (f"El {v} ya no tiene vecinos sin visitar, volvemos." if pila else
                   "El cero no tiene más vecinos: el recorrido ha terminado.")
            es = None
        actual = v if tipo != "sale" else (pila[-1] if pila else None)
        segs.append((paso_slide(caso, pos, edges, k, n, visit, cnt, pila, actual, hl, cap, es), nar, 0))
    return segs, pasos[-1]


def main(preview=False):
    segs = []
    segs.append((portada(NOMBRE, "EJ 04-1"),
                 "Árboles libres. En este vídeo vemos cómo se plantea, por qué funciona la idea y cómo se ejecuta paso a paso.", 0))

    s = Slide("¿Qué es un árbol libre?")
    s.box(60, 100, 560, 360, "Caso 1: árbol libre")
    s.box(660, 100, 560, 360, "Caso 2: NO lo es")
    s.graph({v: (x - 610, y + 30) for v, (x, y) in P1.items()}, E1)
    s.graph({v: (x - 10, y + 30) for v, (x, y) in P2.items()}, E2,
            es={(0, 1): ("red", 4), (1, 2): ("red", 4), (2, 3): ("red", 4), (3, 0): ("red", 4)})
    s.caption("Árbol libre = grafo no dirigido, ACÍCLICO y CONEXO", y=500)
    s.caption("El caso 2 tiene un ciclo 0-1-2-3 y además {4,5} va por separado", y=545)
    segs.append((s, "Un árbol libre es un grafo no dirigido que no tiene ciclos y que es conexo: "
                    "entre cada par de vértices hay exactamente un camino.", 0))
    segs.append((s, "El de la izquierda lo es. El de la derecha no: tiene un ciclo, cero uno dos tres, "
                    "y además los vértices cuatro y cinco quedan separados del resto.", 0))

    segs.append((ideas("La idea clave", [
        "Habría que comprobar dos cosas: que no hay ciclos y que es conexo.",
        "Pero en un grafo con V vértices, dos cualesquiera de estas tres implican la tercera:",
        ("  conexo   ·   acíclico   ·   exactamente V − 1 aristas", "gold"),
        "Así que: árbol libre  ⇔  conexo  y  A = V − 1",
    ], note="Contar aristas es gratis (g.A()). Solo hay que mirar si es conexo: un DFS desde el 0 que visite los V vértices."),
        "Habría que comprobar dos cosas, que no hay ciclos y que es conexo. Pero los árboles tienen una propiedad muy útil: "
        "en un grafo con uve vértices, si se cumplen dos de estas tres condiciones, conexo, acíclico, y tener uve menos una aristas, "
        "entonces se cumple también la tercera.", 0))
    segs.append((segs[-1][0],
                 "Por tanto, ser árbol libre equivale a ser conexo y tener exactamente uve menos una aristas. "
                 "El número de aristas nos lo da el grafo directamente, así que solo hay que comprobar que es conexo: "
                 "un recorrido en profundidad desde el cero tiene que llegar a todos los vértices.", 0))

    segs.append((ideas("¿Por qué así y no de otra forma?", [
        "Buscar ciclos directamente también funciona: un vecino ya visitado que no es tu padre indica un ciclo.",
        "Pero hay que llevar el padre de cada vértice, y además seguir comprobando la conexión.",
        "Contar aristas + un recorrido es más simple y más difícil de equivocar.",
        "¿DFS o BFS? Para saber A QUÉ vértices se llega da igual el orden: DFS es lo más corto de escribir.",
    ]), "También podríamos buscar ciclos directamente, pero hay que llevar el padre de cada vértice y además seguir comprobando "
        "la conexión. Contar aristas y hacer un recorrido es más sencillo. Y como solo queremos saber a qué vértices se llega, "
        "da igual usar profundidad o anchura: el D F S es lo más corto de escribir.", 0))

    s = Slide("El código", "EJ_04-1.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_CALL, L_CON, L_ARB}, title="class ArbolLibre")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, [
        "El constructor lanza dfs desde el 0 (V ≥ 1, siempre existe).",
        "dfs marca el vértice, suma 1 a alcanzados y sigue por los vecinos no visitados.",
        "conexo ⇔ alcanzados == V",
        "árbol ⇔ conexo y A == V − 1",
    ], size=20, gap=16)
    segs.append((s, "En el código, el constructor lanza el D F S desde el vértice cero, que siempre existe porque hay al menos un vértice. "
                    "Cada vez que el recorrido entra en un vértice lo marca y suma uno a alcanzados. "
                    "Al terminar, el grafo es conexo si alcanzados vale uve, y es árbol si además hay uve menos una aristas.", 0))

    # ejecución caso 1 (sin los pasos de "ya visitado" para no alargar)
    segs.append((ideas("Ejecución · Caso 1", ["V = 6, A = 5  →  A = V − 1 se cumple.",
                                             "Ahora el DFS desde el 0 tiene que llegar a los 6 vértices."]),
                 "Vamos con el primer caso. Tiene seis vértices y cinco aristas, así que la condición de las aristas se cumple. "
                 "Veamos si el recorrido llega a todos.", 0))
    e1, fin1 = ejecucion(1, P1, E1, 6)
    segs += [x for x in e1]
    s = Slide("Caso 1 · resultado")
    s.graph({v: (x - 310, y + 40) for v, (x, y) in P1.items()}, E1, ns={v: ("blue", "node_t", None) for v in P1})
    s.caption("alcanzados = 6 = V   y   A = 5 = V − 1   ⇒   SI", y=480)
    segs.append((s, "El recorrido ha llegado a los seis vértices y hay cinco aristas: la respuesta es sí.", 0))

    e2, fin2 = ejecucion(2, P2, E2, 6)
    segs.append((ideas("Ejecución · Caso 2", ["V = 6, A = 5  →  A = V − 1 también se cumple.",
                                             "¿Llega el DFS a todos?"]),
                 "El segundo caso también tiene seis vértices y cinco aristas. Aquí está la trampa: con contar aristas no basta.", 0))
    segs += e2
    s = Slide("Caso 2 · resultado")
    s.graph({v: (x - 310, y + 40) for v, (x, y) in P2.items()}, E2,
            ns={v: ("blue", "node_t", None) for v in range(4)},
            es={(0, 1): ("red", 4), (1, 2): ("red", 4), (2, 3): ("red", 4), (3, 0): ("red", 4)})
    s.caption("alcanzados = 4 ≠ 6   ⇒   no es conexo   ⇒   NO", y=480)
    s.caption("Las aristas 'que sobran' en el ciclo son las que faltan para unir {4,5}", y=525)
    segs.append((s, "Solo se alcanzan cuatro vértices: no es conexo y la respuesta es no. "
                    "La arista que sobra cerrando el ciclo es justo la que falta para conectar el cuatro y el cinco.", 0))

    segs.append((cierre(NOMBRE, [
        "Árbol libre ⇔ conexo y A = V − 1 (no hace falta buscar ciclos).",
        "Conexo ⇔ un DFS desde el 0 visita los V vértices.",
        "Coste: O(V + A) por caso; cada vértice y arista se mira una vez.",
        ("Ojo: el DFS recursivo puede bajar V niveles; en Visual Studio con 1 MB de pila un caso enorme podría desbordarla.", "muted"),
    ]), "Resumiendo: un grafo es árbol libre si es conexo y tiene uve menos una aristas. La conexión se comprueba con un D F S "
        "desde el cero. El coste es lineal, del orden de uve más a, porque cada vértice y cada arista se miran una sola vez.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-1_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-1_arboles_libres.mp4")
        print(f"04-1: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
