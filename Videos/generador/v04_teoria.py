"""Vídeo de teoría · Tema 4 · Grafos no dirigidos (animado)."""
from collections import deque
from vidlib import C, W, H, font
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

TEMA = "Tema 4 · Grafos no dirigidos"
POS = {0: (250, 200), 1: (430, 140), 2: (430, 320), 3: (610, 230), 4: (790, 230), 5: (900, 420), 6: (1060, 360), 7: (1060, 500)}
ARI = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (5, 6), (6, 7)]
ADY = {v: [] for v in POS}
for a, b in ARI:
    ADY[a].append(b)
    ADY[b].append(a)


def dfs_orden(s):
    vis, orden, arbol = set(), [], []

    def rec(v):
        vis.add(v)
        orden.append(v)
        for w in ADY[v]:
            if w not in vis:
                arbol.append((v, w))
                rec(w)
    rec(s)
    return orden, arbol


DFS, DFS_A = dfs_orden(0)


def bfs(s):
    dist, q, orden, arbol = {s: 0}, deque([s]), [], []
    while q:
        v = q.popleft()
        orden.append((v, list(q)))
        for w in ADY[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                arbol.append((v, w))
                q.append(w)
    return orden, dist, arbol


BFS, DIST, BFS_A = bfs(0)


def grafo(f, ns=None, es=None, under=None, pos=None, aristas=None, u=1.0):
    if u <= 0:
        return
    f.graph(pos or POS, aristas or ARI, ns=ns or {}, es=es or {}, r=28, under=under)


def e_portada(f):
    def dib(f):
        p = {0: (900, 260), 1: (1020, 230), 2: (960, 360), 3: (1080, 340)}
        if f.t >= 0.3:
            f.graph(p, [(0, 1), (0, 2), (1, 3), (2, 3)], r=22)
    portada(f, "Teoría", "Grafos no dirigidos", TEMA, dib)


def e_que(f):
    grafo(f, u=aparece(f, f.c(0)))
    texto(f, (640, 60), "grafo = vértices + aristas (sin dirección)", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        grafo(f, ns={3: ("gold", "node_t", None), 1: ("green", "node_t", None), 2: ("green", "node_t", None), 4: ("green", "node_t", None)},
              es={(1, 3): ("gold", 5), (2, 3): ("gold", 5), (3, 4): ("gold", 5)})
        etiqueta(f, (640, 590), "adyacentes del 3: 1, 2 y 4  ·  grado(3) = 3", 24, "text", u)
    if f.t >= f.c(2):
        etiqueta(f, (640, 655), "amigos, carreteras, píxeles de una imagen, actores de películas…", 22, "muted", aparece(f, f.c(2)))


def e_conceptos(f):
    texto(f, (640, 60), "caminos, ciclos y componentes conexas", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    ns, es = {}, {}
    if f.t < f.c(1):
        es = {(0, 1): ("gold", 5), (1, 3): ("gold", 5), (3, 4): ("gold", 5)}
        grafo(f, es=es)
        etiqueta(f, (640, 600), "camino de 0 a 4: 0 – 1 – 3 – 4", 24, "text", aparece(f, f.c(0)))
    elif f.t < f.c(2):
        es = {(0, 1): ("red", 5), (1, 3): ("red", 5), (2, 3): ("red", 5), (0, 2): ("red", 5)}
        grafo(f, es=es)
        etiqueta(f, (640, 600), "ciclo: 0 – 1 – 3 – 2 – 0", 24, "red", aparece(f, f.c(1)))
    else:
        ns = {v: ("blue" if v <= 4 else "purple", "node_t", None) for v in POS}
        grafo(f, ns=ns)
        etiqueta(f, (640, 600), "2 componentes conexas: {0,1,2,3,4} y {5,6,7}", 24, "text", aparece(f, f.c(2)))
        if f.t >= f.c(3):
            etiqueta(f, (640, 660), "conexo = una sola componente  ·  árbol libre = conexo y sin ciclos (A = V − 1)", 22, "green", aparece(f, f.c(3)))


def e_repr(f):
    texto(f, (640, 60), "¿cómo se guarda?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        caja(f, 330, 160, "matriz de adyacencia", c="red", u=u, w=360, h=60, tam=24)
        for i in range(5):
            for j in range(5):
                on = (i, j) in ARI or (j, i) in ARI
                caja(f, 210 + j * 60, 240 + i * 50, "1" if on else "0", c="red" if on else "dim", u=u, w=52, h=44, tam=18, borde=2)
        texto(f, (330, 520), "memoria V²", 24, "red", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        caja(f, 900, 160, "listas de adyacencia", c="green", u=u, w=360, h=60, tam=24)
        for v in range(5):
            texto(f, (720, 250 + v * 50), f"{v}:", 24, "muted", u, mono=True)
            for k, w in enumerate(ADY[v]):
                caja(f, 800 + k * 64, 262 + v * 50, w, c="green", u=u, w=52, h=40, tam=20, borde=2)
        texto(f, (900, 520), "memoria V + A  ·  la que usamos", 24, "green", u, anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 620), "Grafo g(V);   g.ponArista(v, w);   for (int w : g.ady(v))", 24, "gold", aparece(f, f.c(3)), mono=True)


def e_dfs(f):
    k, fr = paso_idx(f, f.c(1), f.c(3), len(DFS))
    vis = DFS[:max(0, min(k + 1, len(DFS)))]
    ns = {v: ("green", "node_t", None) for v in vis}
    if 0 <= k < len(DFS):
        ns[DFS[k]] = ("gold", "node_t", "gold")
    es = {e: ("green", 6) for e in DFS_A if e[1] in vis}
    under = {v: f"{q + 1}º" for q, v in enumerate(vis)}
    grafo(f, ns=ns, es=es, under=under)
    texto(f, (640, 60), "DFS: búsqueda en profundidad (recursiva)", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(0):
        etiqueta(f, (640, 590), "marca v; para cada adyacente w sin visitar: ant[w] = v, dfs(w)", 22, "text", aparece(f, f.c(0)), mono=True)
    if f.t >= f.c(3):
        etiqueta(f, (640, 655), "llega a todo lo alcanzable · las aristas verdes forman un árbol (ant)", 22, "green", aparece(f, f.c(3)))


def e_bfs(f):
    k, fr = paso_idx(f, f.c(1), f.c(3), len(BFS))
    hechos = [v for v, q in BFS[:max(0, min(k + 1, len(BFS)))]]
    vistos = set(hechos)
    for v in hechos:
        for w in ADY[v]:
            vistos.add(w)
    ns = {v: ("green", "node_t", None) for v in vistos}
    if 0 <= k < len(BFS):
        ns[BFS[k][0]] = ("gold", "node_t", "gold")
    es = {e: ("blue", 6) for e in BFS_A if e[1] in vistos}
    under = {v: f"d={DIST[v]}" for v in vistos}
    grafo(f, ns=ns, es=es, under=under)
    texto(f, (640, 60), "BFS: búsqueda en anchura (con una cola)", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if 0 <= k < len(BFS):
        cola = BFS[k + 1][1] if k + 1 < len(BFS) else []
        texto(f, (100, 580), "cola:", 22, "muted", 1)
        for q, v in enumerate(cola):
            caja(f, 200 + q * 64, 590, v, c="blue", w=52, h=44, tam=20)
    if f.t >= f.c(3):
        etiqueta(f, (640, 655), "dist[v] = mínimo número de aristas desde el origen", 24, "green", aparece(f, f.c(3)))


def e_aplicaciones(f):
    items = [("Componentes conexas", "un DFS desde cada vértice sin visitar", "04-1, 04-2, 04-3, 04-5", C["blue"]),
             ("Bipartito", "2 colores; falla si una arista une iguales", "04-7", C["purple"]),
             ("Ciclos", "arista a un visitado que no es el padre", "04-1: árbol = conexo con A = V − 1", C["red"]),
             ("Distancias mínimas", "BFS: en número de aristas", "04-4, 04-6, 04-L", C["green"])]
    texto(f, (640, 50), "Lo que sale de un recorrido", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (t, d, e, c) in enumerate(items):
        if f.t < f.c(k + 1):
            continue
        u = aparece(f, f.c(k + 1))
        x = 40 + (k % 2) * 610
        y = 110 + (k // 2) * 250
        f.d.rounded_rectangle((x, y, x + 590, y + 220), 16, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        f.d.text((x + 24, y + 44), t, font=font(28, True), fill=mix(C["bot"], c, u), anchor="lm")
        f.d.text((x + 24, y + 110), d, font=font(21), fill=mix(C["bot"], C["text"], u), anchor="lm")
        f.d.text((x + 24, y + 170), e, font=font(21, True), fill=mix(C["bot"], C["muted"], u), anchor="lm")


BITMAP = ["#..##", "#..#.", "..##.", "##..."]


def e_implicito(f):
    texto(f, (640, 60), "grafos implícitos: los vecinos se calculan, no se guardan", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(1))
    if f.t >= f.c(1):
        cols = {(i, j): (C["blue"] if (i, j) in [(0, 0), (1, 0)] else (C["green"] if j >= 2 and i <= 2 and BITMAP[i][j] == "#" else C["purple"]))
                for i, r in enumerate(BITMAP) for j, ch in enumerate(r) if ch == "#"}
        f.grid(330, 170, BITMAP, 70, fills=cols if f.t >= f.c(2) else None)
        texto(f, (505, 480), "cada píxel negro es un vértice", 22, "text", u, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (980, 260), "vecinos: arriba, abajo, izquierda, derecha", 22, "text", aparece(f, f.c(2)))
        etiqueta(f, (980, 330), "manchas = componentes conexas (04-3)", 22, "green", aparece(f, f.c(2) + 0.3))
    if f.t >= f.c(3):
        etiqueta(f, (640, 620), "vértice (i, j)  →  número i·columnas + j, y DFS como siempre", 22, "gold", aparece(f, f.c(3)), mono=True)


def e_coste(f):
    f.box(60, 120, 1160, 420)
    items = [("DFS y BFS visitan cada vértice y cada arista una vez:  O(V + A)", "gold"),
             ("para distancias en número de aristas: BFS (DFS no las da)", "text"),
             ("para componentes, ciclos o colorear: cualquiera de los dos", "text"),
             ("Grafo_algoritmos.h: DFS, BFS, componentes, bipartito y ciclos", "muted")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 23, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Grafos no dirigidos", [
        "vértices y aristas; listas de adyacencia (Grafo.h)",
        "DFS recursivo: componentes, ciclos, bipartito",
        "BFS con cola: distancias mínimas en aristas",
        "todo en O(V + A); también con grafos implícitos",
    ])


ESC = [
    Escena("Grafos no dirigidos: cómo representarlos y cómo recorrerlos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Un grafo es un conjunto de vértices unidos por aristas; en un grafo no dirigido, las aristas no tienen dirección. "
           "Dos vértices unidos por una arista son adyacentes, y el grado de un vértice es cuántos adyacentes tiene: el tres tiene grado tres. "
           "Con grafos se modelan amigos, carreteras, los píxeles de una imagen o los actores de las películas.",
           e_que, titulo="Qué es un grafo", extra=1.5),
    Escena("Un camino es una secuencia de vértices unidos por aristas, como cero, uno, tres, cuatro. "
           "Un ciclo es un camino que vuelve al principio. "
           "Y una componente conexa es un grupo de vértices conectados entre sí: aquí hay dos. "
           "Un grafo conexo tiene una sola, y un árbol libre es conexo y sin ciclos, con uve menos uno aristas.",
           e_conceptos, titulo="Caminos y componentes", extra=1.5),
    Escena("¿Cómo se guarda un grafo? "
           "Con una matriz de adyacencia, uve por uve, que gasta mucha memoria si hay pocas aristas. "
           "O con listas de adyacencia: para cada vértice, la lista de sus vecinos. Ocupa uve más a, y es la que usamos. "
           "En la clase Grafo: el constructor con uve vértices, ponArista para unir dos, y ady para recorrer los vecinos.",
           e_repr, titulo="Representación", extra=1.5),
    Escena("El recorrido en profundidad, DFS, es recursivo: marca el vértice y se llama sobre cada adyacente que no esté marcado, apuntando de dónde vino. "
           "Desde el cero: va al uno, del uno al tres, del tres al dos, y vuelve para ir al cuatro. "
           "Se mete todo lo que puede por un camino antes de volver atrás. "
           "Visita todo lo alcanzable, y las aristas que usa forman un árbol.",
           e_dfs, titulo="DFS", extra=1.5),
    Escena("El recorrido en anchura, BFS, usa una cola. "
           "Desde el cero, visita primero sus vecinos, el uno y el dos, a distancia uno; después el tres, a distancia dos; y luego el cuatro. "
           "Va por capas, de más cerca a más lejos. "
           "Por eso calcula la distancia mínima, en número de aristas, desde el origen a cada vértice.",
           e_bfs, titulo="BFS", extra=1.5),
    Escena("Con un recorrido se resuelven muchas cosas. "
           "Las componentes conexas: un DFS desde cada vértice sin visitar. "
           "Saber si es bipartito: colorear con dos colores, y fallar si una arista une dos iguales. "
           "Detectar ciclos: una arista hacia un visitado que no es el padre. "
           "Y las distancias mínimas, con BFS.",
           e_aplicaciones, titulo="Aplicaciones", extra=1.5),
    Escena("A veces el grafo no se construye: los vecinos se calculan sobre la marcha. "
           "En una imagen, cada píxel negro es un vértice. "
           "Sus vecinos son los de arriba, abajo, izquierda y derecha, y las manchas son las componentes conexas. "
           "Se numera cada casilla y se hace el DFS de siempre.",
           e_implicito, titulo="Grafos implícitos", extra=1.5),
    Escena("Los dos recorridos visitan cada vértice y cada arista una vez: uve más a. "
           "Para distancias en número de aristas hace falta BFS. "
           "Para componentes, ciclos o colorear, sirve cualquiera. "
           "Y todos estos algoritmos están juntos en el fichero de algoritmos de grafos.",
           e_coste, titulo="Coste y cuál usar", extra=1.5),
    Escena("Resumiendo: los grafos se guardan con listas de adyacencia; DFS sirve para componentes, ciclos y colorear, y BFS para distancias mínimas, todo en uve más a.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/04-0", "../04-0_grafos_no_dirigidos_teoria.mp4", "04-0")
