"""
Vídeo · Tema 5 · Grafos dirigidos: explicación general.

Material que cubre: 12_Grafos_dirigidos, 13_La_máquina_calculadora, 14_Ordenación_topológica,
15_Detección_de_ciclos, grafoEMT (autobuses de Madrid) y los ejercicios 05-1, 05-2 y 05-3.
Extras: representaciones comparadas, inverso(), grafo implícito vs explícito, componentes
fuertemente conexas (Kosaraju), pistas para reconocer el algoritmo en el juez.

Las trazas se simulan con el MISMO algoritmo y el mismo orden de aristas que
Estructuras de datos/Digrafo_algoritmos.h (comprobado contra Digrafo_demo.cpp).
El código en pantalla se lee de los .cpp/.h reales.
"""
import math
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C, W, H

ED = "../../Estructuras de datos/"
DIG = ED + "Digrafo.h"
GRA = ED + "Grafo.h"
ALG = ED + "Digrafo_algoritmos.h"
EMT = "material/emt_ejemplo.cpp"
NOMBRE = "Grafos dirigidos"
TEMA = "Tema 5 · explicación general"
CORNER = "Tema 5 · Grafos dirigidos"

# ---------------------------------------------------------------------------
# Grafos de las transparencias
# ---------------------------------------------------------------------------
# digrafo de 13 vértices (transparencias 12 y 15), aristas en este orden
E13 = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0), (11, 12), (12, 9), (9, 10), (9, 11), (7, 9),
       (10, 12), (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5), (6, 4), (6, 9), (7, 6)]
N13 = 13
REL13 = {0: (70, 60), 1: (150, 220), 2: (290, 180), 3: (290, 310), 4: (430, 390), 5: (90, 390),
         6: (430, 110), 7: (720, 70), 8: (570, 150), 9: (590, 270), 10: (720, 230),
         11: (590, 410), 12: (720, 380)}

# DAG de 7 vértices (transparencia 14)
E7 = [(0, 1), (0, 2), (0, 5), (6, 0), (6, 4), (5, 2), (3, 2), (3, 5), (3, 4), (3, 6), (1, 4)]
N7 = 7
REL7 = {0: (0, 0), 2: (90, 150), 5: (250, 150), 1: (408, 150), 3: (173, 278), 4: (317, 300), 6: (0, 400)}


def adys(n, edges):
    a = [[] for _ in range(n)]
    for v, w in edges:
        a[v].append(w)
    return a


A13 = adys(N13, E13)
A7 = adys(N7, E7)


def pos(rel, ox, oy, k=1.0):
    return {v: (ox + x * k, oy + y * k) for v, (x, y) in rel.items()}


def P13(ox=50, oy=130, k=1.0):
    return pos(REL13, ox, oy, k)


def P7(ox, oy, k=1.0):
    return pos(REL7, ox, oy, k)


# colores por estado
BASE = ("node", "node_t", None)
EST_VISIT = ("blue", "node_t", None)
EST_ACT = ("gold", "node_t", None)
EST_FIN = ("green", "node_t", None)
EST_RED = ("red", "node_t", None)
COMP_COL = [(112, 222, 152), (255, 206, 92), (92, 192, 255), (255, 118, 108), (196, 150, 255)]


def aristas(edges, base=("dim", 3), **marca):
    return {e: base for e in edges}


# ---------------------------------------------------------------------------
# utilidades de dibujo
# ---------------------------------------------------------------------------
def tabla(s, x, y, cols, filas, cab=None, size=19, rowh=44, hl=(), pad=14):
    """cols: anchos; filas: [[texto, ...]]; hl: índices de fila resaltados."""
    tw = sum(cols)
    yy = y
    if cab:
        s.d.rounded_rectangle((x, yy, x + tw, yy + rowh - 6), 8, fill=C["border"])
        xx = x
        for c, t in zip(cols, cab):
            s.text((xx + pad, yy + (rowh - 6) / 2), t, size=size - 2, color="gold", bold=True, anchor="lm")
            xx += c
        yy += rowh
    for i, fila in enumerate(filas):
        if i in hl:
            s.d.rectangle((x, yy, x + tw, yy + rowh - 4), fill=(60, 66, 40))
        s.d.line((x, yy + rowh - 4, x + tw, yy + rowh - 4), fill=C["border"], width=1)
        xx = x
        for c, t in zip(cols, fila):
            col = "text"
            if isinstance(t, tuple):
                t, col = t
            s.text((xx + pad, yy + (rowh - 4) / 2), t, size=size, color=col, anchor="lm")
            xx += c
        yy += rowh
    return yy


def arcos(s, orden, edges, y0, x0, dx, ns=None, color="gold", hs=0.28):
    """Vértices en fila (en el orden dado) y flechas como arcos por encima."""
    p = {v: (x0 + i * dx, y0) for i, v in enumerate(orden)}
    for a, b in edges:
        (x1, _), (x2, _) = p[a], p[b]
        h = 22 + abs(x2 - x1) * hs
        pts = [(x1 + (x2 - x1) * (t / 20), y0 - 26 - 4 * h * (t / 20) * (1 - t / 20)) for t in range(21)]
        s.d.line(pts, fill=C[color], width=3)
        (px, py), (qx, qy) = pts[-2], pts[-1]
        L = math.hypot(qx - px, qy - py)
        ux, uy = (qx - px) / L, (qy - py) / L
        s.d.polygon([(qx + ux * 4, qy + uy * 4), (qx - ux * 10 - uy * 6, qy - uy * 10 + ux * 6),
                     (qx - ux * 10 + uy * 6, qy - uy * 10 - ux * 6)], fill=C[color])
    ns = ns or {}
    for v in orden:
        x, y = p[v]
        fill, tc, ring = ns.get(v, BASE)
        if ring:
            s.d.ellipse((x - 31, y - 31, x + 31, y + 31), outline=C.get(ring, ring), width=4)
        s.d.ellipse((x - 25, y - 25, x + 25, y + 25), fill=C.get(fill, fill))
        s.text((x, y), str(v), size=22, color=tc, bold=True, anchor="mm")
    return p


def matriz(s, x, y, n, edges, cell=27, hl_row=None, hl_col=None):
    ar = set(edges)
    for j in range(n):
        s.text((x + 30 + j * cell + cell / 2, y + 10), str(j), size=13, color="muted", anchor="mm", bold=(j == hl_col))
    for i in range(n):
        yy = y + 24 + i * cell
        s.text((x + 14, yy + cell / 2), str(i), size=13, color="muted", anchor="mm", bold=(i == hl_row))
        for j in range(n):
            xx = x + 30 + j * cell
            uno = (i, j) in ar
            fill = (110, 88, 28) if uno else (18, 34, 66)
            if hl_row == i and uno:
                fill = (160, 120, 20)
            s.d.rectangle((xx + 1, yy + 1, xx + cell - 2, yy + cell - 2), fill=fill)
            s.text((xx + cell / 2, yy + cell / 2), "1" if uno else "0", size=14,
                   color="gold" if uno else "dim", bold=uno, anchor="mm")


def dgr(s, pos_, edges, ns=None, es=None, r=22, **kw):
    s.dgraph(pos_, edges, ns=ns, es=es, r=r, **kw)


def lista_q(vals):
    return [str(x) for x in vals]


def chips(s, x, y, vals, hecho=(), actual=None, w=30, h=28, size=13):
    """Fila compacta de vértices; los ya procesados se atenúan y el actual va en dorado."""
    for i, v in enumerate(vals):
        cx = x + i * (w + 3)
        if v == actual:
            fill, tc = C["gold"], C["node_t"]
        elif v in hecho:
            fill, tc = (30, 90, 60), C["muted"]
        else:
            fill, tc = C["blue_d"], C["text"]
        s.d.rounded_rectangle((cx, y, cx + w, y + h), 6, fill=fill, outline=C["blue"], width=1)
        s.text((cx + w / 2, y + h / 2), str(v), size=size, color=tc, bold=True, anchor="mm")


# ---------------------------------------------------------------------------
# simulaciones (mismo orden de aristas que Digrafo_algoritmos.h)
# ---------------------------------------------------------------------------
def sim_dfs(a, s0):
    visit = [False] * len(a)
    pila, ev = [], []

    def dfs(v, via):
        visit[v] = True
        pila.append(v)
        saltados = []
        ev.append(["entra", v, via, visit[:], pila[:], saltados])
        for w in a[v]:
            if not visit[w]:
                dfs(w, v)
            else:
                ev[-1][5].append((v, w))   # (se anota en el último "entra"; se reparte luego)
        pila.pop()

    dfs(s0, None)
    return ev


def sim_dfs_detallado(a, s0):
    """Eventos 'entra' y 'visto' (arista a un vértice ya visitado) en orden."""
    visit = [False] * len(a)
    pila, ev = [], []

    def dfs(v, via):
        visit[v] = True
        pila.append(v)
        ev.append(("entra", v, via, visit[:], pila[:]))
        for w in a[v]:
            if not visit[w]:
                dfs(w, v)
            else:
                ev.append(("visto", v, w, visit[:], pila[:]))
        pila.pop()
        ev.append(("sale", v, None, visit[:], pila[:]))

    dfs(s0, None)
    return ev


def sim_bfs(a, s0):
    n = len(a)
    visit, dist, ant = [False] * n, [None] * n, [None] * n
    visit[s0], dist[s0] = True, 0
    q, ev = [s0], []
    while q:
        v = q.pop(0)
        nuevos = []
        for w in a[v]:
            if not visit[w]:
                visit[w], dist[w], ant[w] = True, dist[v] + 1, v
                q.append(w)
                nuevos.append(w)
        ev.append((v, nuevos, visit[:], dist[:], ant[:], q[:]))
    return ev, dist, ant


def sim_topo(a):
    n = len(a)
    visit = [False] * n
    post, ev, pila = [], [], []

    def dfs(v):
        visit[v] = True
        pila.append(v)
        for w in a[v]:
            if not visit[w]:
                dfs(w)
        pila.pop()
        post.append(v)
        ev.append((v, post[:], visit[:], pila[:]))

    for v in range(n):
        if not visit[v]:
            dfs(v)
    return ev, post


def sim_ciclo(a, orden):
    n = len(a)
    visit, ap, ant = [False] * n, [False] * n, [None] * n
    pila, ev = [], []
    hay = [False]
    ciclo = []

    def dfs(v):
        ap[v] = True
        visit[v] = True
        pila.append(v)
        ev.append(("entra", v, None, visit[:], ap[:], pila[:], ant[:]))
        for w in a[v]:
            if hay[0]:
                return
            if not visit[w]:
                ant[w] = v
                dfs(w)
            elif ap[w]:
                hay[0] = True
                x = v
                while x != w:
                    ciclo.insert(0, x)
                    x = ant[x]
                ciclo.insert(0, w)
                ciclo.insert(0, v)
                ev.append(("ciclo", v, w, visit[:], ap[:], pila[:], ant[:]))
            else:
                ev.append(("visto", v, w, visit[:], ap[:], pila[:], ant[:]))
        ap[v] = False
        pila.pop()
        ev.append(("sale", v, None, visit[:], ap[:], pila[:], ant[:]))

    for v in orden:
        if not visit[v]:
            dfs(v)
        if hay[0]:
            break
    return ev, ciclo


def sim_cfc(a):
    """Kosaraju como en Digrafo_algoritmos.h: orden = postorden inverso de g^R; luego DFS en g."""
    n = len(a)
    inv = [[] for _ in range(n)]
    for v in range(n):
        for w in a[v]:
            inv[w].append(v)
    ev, post = sim_topo(inv)
    orden = list(reversed(post))
    comp = [-1] * n
    visit = [False] * n
    k = 0
    pasos = []

    def dfs(v):
        visit[v] = True
        comp[v] = k
        for w in a[v]:
            if not visit[w]:
                dfs(w)

    for v in orden:
        if not visit[v]:
            dfs(v)
            pasos.append((v, [u for u in range(n) if comp[u] == k], comp[:]))
            k += 1
    return inv, post, orden, pasos


# ---------------------------------------------------------------------------
# código de los .h reales
# ---------------------------------------------------------------------------
def bloque(path, ini, fin, maxc=62, skip=()):
    return code_lines(path, find_line(path, ini), find_line(path, fin, find_line(path, ini)), maxc=maxc, skip=skip)


def seg_texto(path, inicio, ref_ini, ref_fin):
    a = find_line(path, ref_ini, find_line(path, inicio))
    b = find_line(path, ref_fin, a)
    return a, b


# ---------------------------------------------------------------------------
# A · introducción y conceptos
# ---------------------------------------------------------------------------
LAB13 = {v: str(v) for v in range(N13)}
SCC13 = [[1], [0, 2, 3, 4, 5], [9, 10, 11, 12], [6, 8], [7]]


def g13(s, ns=None, es=None, ox=50, oy=130, r=22, **kw):
    s.box(40, 90, 780, 470, "digrafo de las transparencias: 13 vértices, 22 aristas")
    base = {e: ("muted", 3) for e in E13}
    base.update(es or {})
    dgr(s, P13(ox, oy), E13, ns=ns, es=base, labels=LAB13, r=r, **kw)


def sec_intro(segs):
    segs.append((portada(NOMBRE, "TEMA 5", TEMA),
                 "Grafos dirigidos. Un repaso general de todo el tema cinco: los conceptos, el T A D, los recorridos, "
                 "la máquina calculadora, el grafo de autobuses de la EMT, la ordenación topológica y la detección de ciclos.", 0))

    s = Slide("Qué vamos a ver", CORNER)
    filas = [
        ("12", "Grafos dirigidos", "conceptos, TAD Digrafo, DFS, BFS", "PDF 12"),
        ("13", "La máquina calculadora", "BFS en un grafo implícito", "PDF 13 · EJ 05-1, 05-2"),
        ("EMT", "Autobuses de Madrid", "BFS contra DFS en un grafo real", "grafoEMT.zip"),
        ("14", "Ordenación topológica", "postorden inverso de un DFS", "PDF 14 · EJ 05-3"),
        ("15", "Detección de ciclos", "DFS con vértices apilados", "PDF 15 · EJ 05-3"),
        ("+", "Extras", "representaciones, grafo inverso, componentes fuertemente conexas, pistas para el juez", "no vienen en las transparencias"),
    ]
    y = 105
    for i, (n, t, d, f) in enumerate(filas):
        col = "gold" if n != "+" else "purple"
        s.box(50, y, 1180, 80, fill=(14, 28, 60), border=col if n == "+" else "border")
        s.d.ellipse((72, y + 16, 120, y + 64), fill=C[col])
        s.text((96, y + 40), n, size=20 if len(n) < 3 else 15, color="node_t", bold=True, anchor="mm")
        s.text((145, y + 14), t, size=24, bold=True)
        s.wrap(145, y + 46, 760, d, size=17, color="muted", gap=2)
        s.text((1210, y + 40), f, size=16, color="muted", anchor="rm")
        y += 92
    segs.append((s, "Seguimos el orden de las transparencias. Primero los conceptos y el T A D de grafos dirigidos, con los dos recorridos. "
                    "Luego la máquina calculadora, que es un grafo implícito, y el ejemplo de los autobuses de la EMT. "
                    "Después, la ordenación topológica y la detección de ciclos. Y al final, unos extras que te pueden servir en el juez.", 0))

    # ---- definición
    s = Slide("Grafo dirigido (digrafo)", CORNER)
    g13(s)
    s.bullets(850, 110, 390, [
        "Un conjunto de VÉRTICES y un conjunto de ARISTAS DIRIGIDAS.",
        ("Una arista es un par ORDENADO (v, w): sale de v y llega a w.", "gold"),
        "v → w NO implica w → v.",
        "Aquí: V = 13 vértices y A = 22 aristas.",
    ], size=21, gap=16)
    segs.append((s, "Un grafo dirigido, o digrafo, es un conjunto de vértices y un conjunto de aristas dirigidas. "
                    "Cada arista es un par ordenado: sale de un vértice y llega a otro. Que haya una flecha de v a w no implica que haya otra de w a v. "
                    "Este es el digrafo de las transparencias: trece vértices y veintidós aristas.", 0))

    # ---- grados
    v = 6
    sal = [(v, w) for w in A13[v]]
    ent = [(u, v) for u, w in E13 if w == v]
    s = Slide("Grado de salida y grado de entrada", CORNER)
    es = {e: ("gold", 6) for e in sal}
    es.update({e: ("blue", 6) for e in ent})
    g13(s, ns={6: ("node", "node_t", "text")}, es=es)
    s.box(850, 110, 380, 200, "vértice 6")
    s.text((870, 150), "grado de salida = 4", size=24, color="gold", bold=True)
    s.text((870, 186), "6→0  6→8  6→4  6→9", size=19, color="muted", mono=True)
    s.text((870, 236), "grado de entrada = 2", size=24, color="blue", bold=True)
    s.text((870, 272), "7→6  8→6", size=19, color="muted", mono=True)
    s.wrap(850, 335, 380, "La suma de todos los grados de salida es A. Lo mismo con los de entrada.", size=20, color="muted")
    segs.append((s, "El grado de salida de un vértice es el número de aristas que salen de él, y el de entrada, las que llegan. "
                    "El vértice seis tiene grado de salida cuatro, hacia el cero, el ocho, el cuatro y el nueve, y grado de entrada dos, desde el siete y desde el ocho. "
                    "Si sumamos los grados de salida de todos los vértices, sale el número de aristas.", 0))

    # ---- camino y ciclo
    cam = [(7, 9), (9, 11), (11, 4)]
    cic = [(9, 10), (10, 12), (12, 9)]
    s = Slide("Camino dirigido y ciclo dirigido", CORNER)
    es = {e: ("green", 6) for e in cam}
    es.update({e: ("red", 6) for e in cic})
    ns = {v: EST_FIN for v in (7, 9, 11, 4)}
    ns.update({v: EST_RED for v in (10, 12)})
    ns[9] = EST_RED
    g13(s, ns=ns, es=es)
    s.bullets(850, 110, 390, [
        ("Camino dirigido: sucesión de aristas, cada una empieza donde acabó la anterior.", "green"),
        "7 → 9 → 11 → 4  tiene longitud 3.",
        ("Ciclo dirigido: camino que vuelve a su punto de partida.", "red"),
        "9 → 10 → 12 → 9",
    ], size=20, gap=16)
    segs.append((s, "Un camino dirigido es una sucesión de aristas, cada una empezando donde acaba la anterior, y siempre en el sentido de la flecha. "
                    "Por ejemplo, del siete al cuatro pasando por el nueve y el once: longitud tres. "
                    "Un ciclo dirigido es un camino que vuelve a su punto de partida, como el nueve, diez, doce, nueve.", 0))

    # ---- componentes fuertemente conexas
    ns = {}
    for k, comp in enumerate(SCC13):
        for u in comp:
            ns[u] = (COMP_COL[k], "node_t", None)
    es = {}
    for a, b in E13:
        ka = [k for k, c in enumerate(SCC13) if a in c][0]
        kb = [k for k, c in enumerate(SCC13) if b in c][0]
        es[(a, b)] = (COMP_COL[ka], 4) if ka == kb else ("muted", 3)
    s = Slide("Componentes fuertemente conexas", CORNER)
    g13(s, ns=ns, es=es)
    s.box(850, 110, 380, 170, "5 componentes")
    yy = 150
    for k, comp in enumerate(SCC13):
        s.d.ellipse((870, yy + 3, 886, yy + 19), fill=COMP_COL[k])
        s.text((900, yy), "{" + ", ".join(map(str, comp)) + "}", size=18, mono=True)
        yy += 22
    s.bullets(850, 305, 390, [
        "v y w están en la misma componente si hay camino de v a w Y de w a v.",
        "Fuertemente conexo: una sola componente.",
    ], size=19, gap=12)
    segs.append((s, "Esta es la idea de conexión en los grafos dirigidos. Dos vértices están en la misma componente fuertemente conexa si hay un camino de uno al otro y también al revés. "
                    "Nuestro digrafo tiene cinco componentes: el uno solo, el cero, dos, tres, cuatro y cinco, el nueve, diez, once y doce, el seis con el ocho, y el siete solo. "
                    "Un grafo es fuertemente conexo si tiene una sola.", 0))

    # ---- aplicaciones
    s = Slide("Aplicaciones de los grafos dirigidos", CORNER)
    filas = [("mapa", "intersección", "calle de sentido único"),
             ("planificación", "tarea", "precedencia"),
             ("web", "página", "enlace"),
             ("referencias", "artículo", "cita"),
             ("juego", "estado del tablero", "movimiento legal"),
             ("memoria dinámica", "objeto", "puntero"),
             ("orientación a objetos", "clase", "herencia")]
    tabla(s, 110, 110, [370, 360, 330], filas, cab=["aplicación", "vértice", "arista"], size=22, rowh=60, hl=(1, 4))
    s.caption("En amarillo, las dos que aparecen en los ejercicios: tareas con precedencia (05-3) y estados de un juego (05-1 y 05-2).", y=640)
    segs.append((s, "Los grafos dirigidos están por todas partes. Un mapa, con calles de sentido único. Una planificación, con tareas y precedencias. "
                    "La web, con páginas y enlaces. Las citas entre artículos. Un juego, con estados del tablero y movimientos legales. "
                    "La memoria dinámica, con objetos y punteros. Y la herencia entre clases. "
                    "En los ejercicios del tema aparecen dos: las tareas con precedencias y los estados de un juego.", 0))

    # ---- problemas
    s = Slide("Problemas sobre grafos dirigidos", CORNER)
    filas = [("camino s → t", "¿existe un camino dirigido de s a t?", "DFS o BFS"),
             ("camino más corto", "menos aristas de s a t", "BFS"),
             ("ciclo dirigido", "¿hay algún ciclo?", "DFS con pila"),
             ("fuertemente conexo", "¿hay camino entre todo par de vértices?", "DFS + DFS en el inverso"),
             ("orden topológico", "ordenar para que las aristas apunten hacia delante", "postorden inverso"),
             ("cierre transitivo", "¿para qué pares v, w hay camino?", "un DFS desde cada vértice"),
             ("PageRank", "¿qué importancia tiene una página web?", ("fuera del temario", "muted"))]
    tabla(s, 50, 105, [260, 560, 360], filas, cab=["problema", "pregunta", "cómo se resuelve"], size=20, rowh=60,
          hl=(0, 1, 2, 4))
    s.caption("Resaltados, los que resuelve el temario con código: alcanzabilidad, camino mínimo, ciclos y orden topológico.", y=640)
    segs.append((s, "Y estos son los problemas típicos. ¿Hay camino de s a t? Con un D F S o un B F S. ¿Cuál es el más corto? Con un B F S. "
                    "¿Hay un ciclo? Con un D F S que recuerda qué vértices están en la pila. "
                    "¿Se puede ordenar el grafo de forma que todas las aristas apunten hacia delante? Con el postorden inverso. "
                    "Las componentes fuertemente conexas y el cierre transitivo los veremos como extra, y el Page Rank queda fuera del temario.", 0))


# ---------------------------------------------------------------------------
# B · TAD Digrafo, representaciones, inverso
# ---------------------------------------------------------------------------
def sec_tad(segs):
    # ---- TAD
    L_PON = find_line(DIG, "void ponArista")
    L_ADY = find_line(DIG, "Adys const& ady")
    L_INV = find_line(DIG, "Digrafo inverso")
    code = code_lines(DIG, 15, 58, maxc=56, skip=[(26, 42), (49, 52)])
    s = Slide("El TAD Digrafo", "Digrafo.h")
    s.box(40, 90, 480, 500, "operaciones")
    ops = [("Digrafo(int V)", "crea un grafo con V vértices, sin aristas"),
           ("ponArista(v, w)", "añade la arista v → w"),
           ("ady(v)", "lista de los adyacentes (sucesores) de v"),
           ("V()  ·  A()", "número de vértices y de aristas"),
           ("inverso()", "el grafo con todas las flechas al revés")]
    y = 125
    for a, b in ops:
        s.text((62, y), a, size=21, color="gold", bold=True, mono=True)
        s.wrap(62, y + 30, 440, b, size=18, color="muted", gap=2)
        y += 88
    s.code(540, 90, 700, 500, code, hl={L_PON + 4, L_PON + 3}, title="Digrafo.h")
    segs.append((s, "El T A D de los grafos dirigidos tiene seis operaciones. Crear un grafo con uve vértices. Añadir una arista. "
                    "Consultar los adyacentes de un vértice, es decir, sus sucesores. Consultar el número de vértices y el de aristas. "
                    "Y calcular el grafo inverso. Está implementado con un vector de listas de adyacentes.", 0))

    # ---- diferencia con Grafo
    cg = code_lines(GRA, find_line(GRA, "void ponArista"), find_line(GRA, "void ponArista") + 7, maxc=46)
    cd = code_lines(DIG, find_line(DIG, "void ponArista"), find_line(DIG, "void ponArista") + 5, maxc=46)
    s = Slide("ponArista: Grafo contra Digrafo", CORNER)
    s.code(40, 100, 600, 250, cg, hl={find_line(GRA, "_ady[w].push_back(v)"), find_line(GRA, "_ady[v].push_back(w)")}, title="Grafo.h (no dirigido)")
    s.code(660, 100, 580, 250, cd, hl={find_line(DIG, "_ady[v].push_back(w)")}, title="Digrafo.h (dirigido)")
    s.box(40, 375, 600, 140, fill=(24, 40, 70))
    s.wrap(60, 392, 560, "No dirigido: la arista v-w se guarda dos veces, en la lista de v y en la de w.", size=21)
    s.box(660, 375, 580, 140, fill=(24, 40, 70), border="gold")
    s.wrap(680, 392, 540, "Dirigido: v → w se guarda una sola vez, solo en la lista de v. Por eso A es la suma de los grados de salida.", size=21)
    s.caption("Una consecuencia: en un Digrafo, w está en ady(v) pero v no tiene por qué estar en ady(w).", y=560)
    segs.append((s, "La diferencia con el grafo no dirigido está en poner arista. En un grafo no dirigido, la arista se guarda dos veces, en la lista de v y en la de w. "
                    "En un digrafo se guarda una sola vez, solo en la lista del vértice de origen. "
                    "Así que w puede estar en los adyacentes de v sin que v esté en los de w.", 0))

    # ---- matriz
    s = Slide("Representación 1: matriz de adyacencia", CORNER)
    s.box(40, 90, 440, 440, "V × V booleanos")
    matriz(s, 56, 125, N13, E13, cell=27)
    s.bullets(510, 110, 720, [
        "Matriz de V × V: la casilla (v, w) vale 1 si existe la arista v → w.",
        "Espacio V² aunque haya pocas aristas: aquí 22 unos entre 169 casillas.",
        ("Comprobar si v → w existe: O(1).", "green"),
        ("Recorrer los adyacentes de v: hay que mirar la fila entera, O(V).", "red"),
    ], size=22, gap=20)
    s.box(510, 400, 720, 130, fill=(24, 40, 70))
    s.wrap(530, 418, 680, "Con V = 100.000 vértices serían 10.000 millones de casillas: ni cabe en memoria.", size=22, color="gold")
    segs.append((s, "Primera representación: la matriz de adyacencia. Una matriz de uve por uve donde la casilla v w vale uno si existe la arista. "
                    "Comprobar si hay una arista es inmediato, pero recorrer los adyacentes de un vértice obliga a mirar una fila entera. "
                    "Y ocupa uve al cuadrado aunque haya pocas aristas: aquí, veintidós unos entre ciento sesenta y nueve casillas.", 0))

    # ---- listas
    s = Slide("Representación 2: listas de adyacentes", CORNER)
    s.box(40, 90, 520, 500, "una lista por vértice, una entrada por arista")
    for v in range(N13):
        y = 125 + v * 34
        s.d.rounded_rectangle((60, y, 112, y + 28), 6, fill=C["border"])
        s.text((86, y + 14), str(v), size=17, bold=True, anchor="mm")
        x = 124
        for w in A13[v]:
            s.d.rounded_rectangle((x, y, x + 44, y + 28), 6, fill=C["blue_d"], outline=C["blue"], width=2)
            s.text((x + 22, y + 14), str(w), size=17, bold=True, anchor="mm")
            x += 50
        if not A13[v]:
            s.text((x + 4, y + 14), "—", size=18, color="dim", anchor="lm")
    s.bullets(590, 110, 650, [
        "vector<Adys> _ady: _ady[v] guarda los sucesores de v, en orden de inserción.",
        "Espacio V + A: solo las aristas que existen.",
        ("Recorrer los adyacentes de v: O(grado de salida de v).", "green"),
        ("Comprobar si v → w existe: hay que mirar la lista de v, O(grado de salida).", "gold"),
        "Es lo que usan todos los algoritmos de recorrido.",
    ], size=21, gap=18)
    segs.append((s, "Segunda representación: listas de adyacentes. Un vector con una lista por vértice, y cada lista guarda los sucesores de ese vértice. "
                    "El espacio es uve más a, porque solo se guardan las aristas que existen. "
                    "Recorrer los adyacentes de un vértice cuesta su grado de salida, que es justo lo que hacen todos los recorridos.", 0))

    # ---- comparativa
    s = Slide("Qué representación elegir", CORNER)
    filas = [("matriz de adyacencia", "V²", "1", "1", "V"),
             ("listas de adyacentes", "V + A", "1", "grado-sal(v)", "grado-sal(v)"),
             ("lista de aristas", "A", "1", "A", "A")]
    tabla(s, 50, 110, [330, 130, 230, 230, 250], filas,
          cab=["representación", "espacio", "añadir v → w", "¿v → w existe?", "recorrer adyacentes"], size=20, rowh=62, hl=(1,))
    s.bullets(70, 360, 1140, [
        "Los algoritmos de este tema se basan en recorrer los adyacentes de un vértice.",
        "Los grafos dirigidos que aparecen en la práctica suelen ser DISPERSOS: A mucho menor que V².",
        ("Por eso la asignatura usa listas de adyacentes.", "gold"),
    ], size=23, gap=20)
    segs.append((s, "Comparando las tres: la matriz gasta uve al cuadrado y recorrer adyacentes cuesta uve. La lista de aristas gasta solo a, pero para todo hay que recorrerla entera. "
                    "Las listas de adyacentes gastan uve más a, y recorrer los adyacentes de un vértice cuesta solo su grado. "
                    "Como los algoritmos del tema se basan en recorrer adyacentes, y los grafos dirigidos reales suelen ser dispersos, usamos listas.", 0))

    # ---- inverso
    EI = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    EIR = [(b, a) for a, b in EI]
    PI = {0: (60, 150), 1: (180, 70), 2: (180, 230), 3: (310, 150), 4: (430, 150)}
    s = Slide("Grafo inverso: inverso()", "Digrafo.h")
    s.box(40, 90, 580, 290, "g")
    dgr(s, {v: (x + 80, y + 70) for v, (x, y) in PI.items()}, EI, es={e: ("gold", 4) for e in EI}, r=24)
    s.box(640, 90, 600, 290, "g.inverso()")
    dgr(s, {v: (x + 700, y + 70) for v, (x, y) in PI.items()}, EIR, es={e: ("blue", 4) for e in EIR}, r=24)
    s.code(40, 400, 700, 215, code_lines(DIG, L_INV := find_line(DIG, "Digrafo inverso"), L_INV + 8, maxc=60), hl={L_INV + 4},
           title="Digrafo.h")
    s.bullets(760, 410, 480, [
        "Cada arista v → w pasa a w → v.",
        "Cuesta O(V + A): recorre todas las listas una vez.",
        "ady(v) en el inverso = PREDECESORES de v en g.",
    ], size=19, gap=10)
    segs.append((s, "El grafo inverso tiene las mismas aristas pero con todas las flechas al revés. Se calcula recorriendo todas las listas una vez, "
                    "y para cada arista de v a w, se añade la de w a v. Cuesta uve más a. "
                    "Es útil porque los adyacentes de v en el inverso son los predecesores de v en el grafo original, es decir, los que llegan a él. "
                    "Más adelante lo usaremos para calcular las componentes fuertemente conexas.", 0))


# ---------------------------------------------------------------------------
# C · recorridos: DFS y BFS
# ---------------------------------------------------------------------------
def nombres(lst):
    return ", ".join(str(x) for x in lst)


def y_lista(lst):
    """Enumeración en castellano: 'el 2, el 3 y el 5'."""
    t = [f"el {x}" for x in lst]
    if len(t) <= 1:
        return "".join(t)
    return ", ".join(t[:-1]) + " y " + t[-1]


def sec_dfs(segs):
    L0 = find_line(ALG, "class DFSDirigido")
    CODE = code_lines(ALG, L0, find_line(ALG, "};", L0), maxc=52)
    L_VIS = find_line(ALG, "visit[v] = true;", L0)
    L_FOR = find_line(ALG, "for (int w : g.ady(v))", L0)
    L_REC = find_line(ALG, "if (!visit[w]) dfs(g, w);", L0)

    s = Slide("Recorrido en profundidad (DFS dirigido)", "Digrafo_algoritmos.h")
    s.code(40, 90, 640, 500, CODE, hl={L_VIS, L_REC}, title="class DFSDirigido")
    s.bullets(710, 110, 530, [
        "Marca v como visitado y baja recursivamente por cada adyacente NO visitado.",
        "visit[v] = ¿hay un camino dirigido de s a v?",
        ("En un digrafo solo se llega a lo que SALE de s: el sentido de las flechas manda.", "gold"),
        "Coste O(V + A): cada vértice y cada arista se miran una vez.",
    ], size=21, gap=16)
    segs.append((s, "El recorrido en profundidad es igual que en los grafos no dirigidos. Marcamos el vértice como visitado, y por cada adyacente que no esté visitado, bajamos recursivamente. "
                    "Al terminar, visit de v nos dice si hay un camino dirigido de s a v. Ojo: en un digrafo solo llegamos a lo que sale de s, el sentido de las flechas manda. "
                    "El coste es uve más a.", 0))

    ev = sim_dfs_detallado(A13, 2)
    entras = [e for e in ev if e[0] == "entra"]
    n = len(entras)
    LD = find_line(ALG, "void dfs(", L0)
    CODE_D = code_lines(ALG, LD, find_line(ALG, "}", LD + 3), maxc=44)
    prev = None
    for k, (tipo, v, via, visit, pila) in enumerate(entras, 1):
        s = Slide("DFS desde s = 2", f"paso {k} de {n}")
        s.code(24, 90, 480, 175, CODE_D, hl=({L_VIS} if via is None else {L_VIS, L_REC}), title="dfs(g, v)", size=15)
        s.box(24, 285, 480, 305, "estado")
        s.text((44, 322), f"vértice actual: {v}", size=22, color="gold", bold=True)
        s.queue_row(44, 365, "visitados", [u for u in range(N13) if visit[u]], size=16)
        s.queue_row(44, 420, "pila dfs", pila, size=16)
        s.wrap(44, 475, 440, "visit[v] = true antes de recorrer los vecinos; la pila es la cadena de llamadas recursivas.", size=16, color="muted")
        s.box(524, 90, 730, 500, "grafo (azul: visitado · amarillo: vértice actual)")
        ns = {u: EST_VISIT for u in range(N13) if visit[u]}
        ns[v] = ("gold", "node_t", "text")
        es = {e: ("muted", 3) for e in E13}
        for kk in range(k):
            vv, vi = entras[kk][1], entras[kk][2]
            if vi is not None:
                es[(vi, vv)] = ("blue", 5)
        if via is not None:
            es[(via, v)] = ("gold", 7)
        dgr(s, P13(560, 135, 0.9), E13, ns=ns, es=es, labels=LAB13, r=21)
        vec = A13[v]
        vis = [w for w in vec if visit[w]]
        nov = [w for w in vec if not visit[w]]
        if via is None:
            cap = f"Empezamos en s = {v}: visit[{v}] = true"
            nar = f"Empezamos en el vértice {v}: lo marcamos como visitado."
        else:
            cap = f"{via} → {v}: el {v} estaba sin visitar, entramos"
            if prev is not None and via != prev:
                nar = f"Volvemos atrás hasta el {via}, y desde ahí pasamos a {v}, que estaba sin visitar."
            else:
                nar = f"De {via} pasamos a {v}, que estaba sin visitar."
        if vec:
            partes = []
            if vis:
                partes.append(f"{y_lista(vis)} ya {'estaba' if len(vis) == 1 else 'estaban'} {'visitado' if len(vis) == 1 else 'visitados'}")
            if nov:
                partes.append(f"{y_lista(nov)} {'está' if len(nov) == 1 else 'están'} sin visitar")
            nar += f" Sus vecinos: {' y '.join(partes)}."
            cap += f"   ·   vecinos: {nombres(vec)}"
        else:
            nar += " No tiene vecinos: volvemos atrás."
            cap += "   ·   sin vecinos, volvemos atrás"
        prev = v
        s.caption(cap, y=618)
        segs.append((s, nar, 0))

    s = Slide("Alcanzables desde 2", CORNER)
    visit = ev[-1][3]
    ns = {u: (EST_VISIT if visit[u] else BASE) for u in range(N13)}
    s.box(40, 90, 780, 470, "visit[v] al terminar")
    dgr(s, P13(), E13, ns=ns, es={e: ("muted", 3) for e in E13}, labels=LAB13, r=22)
    s.bullets(850, 110, 390, [
        ("Alcanzables: 0, 1, 2, 3, 4, 5.", "blue"),
        "No alcanzables: 6, 7, 8, 9, 10, 11, 12. Las flechas que entran a la componente no sirven para salir.",
        "Aplicaciones: código muerto, recolector de basura, web crawler.",
    ], size=20, gap=16)
    segs.append((s, "Al terminar, desde el dos son alcanzables el cero, el uno, el dos, el tres, el cuatro y el cinco. Los demás no: hay flechas que entran en esa zona, pero ninguna que salga. "
                    "Esto sirve para detectar código muerto en un programa, para el recolector de basura, o para un web crawler.", 0))


def sec_bfs(segs):
    L0 = find_line(ALG, "class BFSDirigido")
    LB = find_line(ALG, "void bfs(", L0)
    CODE = code_lines(ALG, find_line(ALG, "std::vector<bool> visit;", L0), find_line(ALG, "};", LB) - 1, maxc=50)
    L_Q = find_line(ALG, "q.push(s);", L0)
    L_POP = find_line(ALG, "int v = q.front()", L0)
    L_FOR = find_line(ALG, "for (int w : g.ady(v))", LB)
    L_IF = find_line(ALG, "if (!visit[w]) {", LB)
    L_SET = find_line(ALG, "ant[w] = v; dist[w]", LB)
    L_PUSH = find_line(ALG, "q.push(w);", LB)

    s = Slide("Recorrido en anchura (BFS dirigido)", "Digrafo_algoritmos.h")
    s.code(40, 90, 680, 500, CODE, hl={L_Q, L_SET, L_PUSH}, title="class BFSDirigido (privado)", size=15)
    s.bullets(745, 110, 495, [
        "Usa una COLA: primero los vértices a distancia 1, luego a distancia 2…",
        "dist[v]: nº de aristas del camino más corto de s a v.",
        "ant[v]: el vértice desde el que se descubrió v.",
        ("Como explora por capas, el primer camino que encuentra es el más corto.", "gold"),
        "Coste O(V + A).",
    ], size=20, gap=14)
    segs.append((s, "El recorrido en anchura usa una cola. Primero salen los vértices a distancia uno de s, luego los de distancia dos, y así. "
                    "Guardamos dist de v, el número de aristas del camino más corto, y ant de v, el vértice desde el que descubrimos a v. "
                    "Como se explora por capas, el primer camino que encuentra a v es el más corto. El coste es uve más a.", 0))

    ev, dist_f, ant_f = sim_bfs(A13, 7)
    con = [e for e in ev if e[1]]          # desencolados que descubren algo
    n = len(con)
    orden_sacado = [e[0] for e in ev]
    LCODE = code_lines(ALG, L_POP, L_PUSH + 2, maxc=44)
    for k, (v, nuevos, visit, dist, ant, q) in enumerate(con, 1):
        s = Slide("BFS desde s = 7", f"paso {k} de {n}")
        s.box(40, 90, 780, 470, "grafo (verde: ya sacado · azul: en la cola · amarillo: se saca ahora)")
        sacados = set(orden_sacado[:orden_sacado.index(v)])
        ns = {u: EST_VISIT for u in range(N13) if visit[u]}
        for u in sacados:
            ns[u] = EST_FIN
        ns[v] = ("gold", "node_t", "text")
        es = {e: ("muted", 3) for e in E13}
        for u in range(N13):
            if ant[u] is not None and visit[u]:
                es[(ant[u], u)] = ("blue", 5)
        for w in nuevos:
            es[(v, w)] = ("gold", 7)
        under = {u: str(dist[u]) for u in range(N13) if visit[u]}
        dgr(s, P13(), E13, ns=ns, es=es, labels=LAB13, r=22, under=under)
        s.box(850, 90, 390, 235, "estado")
        s.text((870, 122), f"sacamos el {v}  (dist = {dist[v]})", size=21, color="gold", bold=True)
        s.queue_row(870, 165, "cola", q, size=17)
        s.text((870, 218), "nuevos:", size=18, color="muted")
        s.text((960, 218), nombres(nuevos) + f"  →  dist = {dist[v] + 1}", size=19, color="blue", bold=True)
        s.wrap(870, 262, 350, "El número dorado bajo cada vértice es su dist.", size=16, color="muted")
        s.code(850, 340, 390, 220, LCODE, hl={L_POP, L_SET, L_PUSH}, title="bfs(g)", size=14)
        s.caption(f"Sacamos {v}: sus sucesores sin visitar ({nombres(nuevos)}) reciben dist = {dist[v] + 1}, ant = {v}, y entran en la cola", y=600)
        plural = len(nuevos) > 1
        nar = (f"Sacamos el {v}, que está a distancia {dist[v]}. Descubrimos {y_lista(nuevos)}, "
               f"que {'quedan' if plural else 'queda'} a distancia {dist[v] + 1} y {'entran' if plural else 'entra'} en la cola.")
        if k == 1:
            nar = f"Empezamos en s igual a {v}, con distancia cero. Lo sacamos: descubrimos {y_lista(nuevos)}, a distancia uno, y entran en la cola."
        segs.append((s, nar, 0))

    s = Slide("BFS desde 7: resultado", CORNER)
    s.box(40, 90, 780, 470, "dist[v] = nº mínimo de aristas desde 7")
    ns = {u: ((COMP_COL[[0, 2, 1, 4, 3][min(dist_f[u], 3)] % 5]) if False else EST_VISIT) for u in range(N13)}
    capa_col = {0: ("gold", "node_t", None), 1: EST_FIN, 2: EST_VISIT, 3: ("purple", "node_t", None)}
    ns = {u: capa_col[dist_f[u]] for u in range(N13)}
    es = {e: ("muted", 3) for e in E13}
    for u in range(N13):
        if ant_f[u] is not None:
            es[(ant_f[u], u)] = ("blue", 5)
    dgr(s, P13(), E13, ns=ns, es=es, labels=LAB13, r=22, under={u: str(dist_f[u]) for u in range(N13)})
    s.box(850, 110, 390, 190, "capas")
    for i, (d, col) in enumerate([(0, "gold"), (1, "green"), (2, "blue"), (3, "purple")]):
        vs = [u for u in range(N13) if dist_f[u] == d]
        s.d.ellipse((870, 150 + i * 34, 888, 168 + i * 34), fill=C[col])
        s.text((902, 150 + i * 34), f"dist {d}:  {nombres(vs)}", size=19, mono=True)
    s.wrap(850, 325, 390, "Las aristas azules forman el árbol de caminos mínimos (las que guarda ant).", size=19, color="muted")
    segs.append((s, "Terminado el recorrido, cada vértice tiene su distancia. El siete a distancia cero; el seis y el nueve a uno; el cuatro, el ocho, el cero, el diez y el once a dos; "
                    "y el uno, el dos, el tres, el cinco y el doce a tres. Las aristas azules, las que guarda ant, forman el árbol de caminos mínimos.", 0))

    # camino
    LC = find_line(ALG, "Camino camino(int v) const", L0)
    CODEC = code_lines(ALG, LC, find_line(ALG, "return cam;", LC) + 1, maxc=50)
    s = Slide("Recuperar el camino con ant", "Digrafo_algoritmos.h")
    s.code(40, 90, 600, 270, CODEC, hl={find_line(ALG, "for (int x = v; x != s", LC), find_line(ALG, "cam.push_front(x);", LC)},
           title="BFSDirigido::camino(v)", size=16)
    s.box(660, 90, 580, 270, "camino de 7 a 3")
    xs = [820, 960, 1100, 1220]
    cadena = [3, 4, 6, 7]
    pts = [(700 + i * 150, 230) for i in range(4)]
    for i, u in enumerate(cadena):
        x, y = pts[i]
        s.d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=C["gold"] if u in (3,) else C["node"])
        s.text((x, y), str(u), size=24, color="node_t", bold=True, anchor="mm")
        if i < 3:
            s.d.line((x + 30, y, x + 118, y), fill=C["blue"], width=4)
            s.d.polygon([(x + 30, y), (x + 44, y - 7), (x + 44, y + 7)], fill=C["blue"])
            s.text((x + 74, y - 22), f"ant[{u}]", size=14, color="muted", anchor="mm")
    s.text((950, 150), "se sigue ant hacia atrás", size=18, color="muted", anchor="mm")
    s.text((950, 300), "push_front  ⇒  queda  7 → 6 → 4 → 3", size=20, color="gold", bold=True, anchor="mm")
    s.bullets(60, 395, 1160, [
        "Se parte de v y se sigue ant[x] hasta llegar a s; push_front deja el camino en el orden correcto, de s a v.",
        "Longitud = dist[v] = 3 aristas. Coste proporcional a la longitud del camino.",
        ("¡Ojo!  Si no hay camino de s a v, camino(v) lanza domain_error.", "red"),
    ], size=21, gap=14)
    segs.append((s, "Para recuperar el camino, partimos de v y vamos siguiendo ant hacia atrás hasta llegar a s. "
                    "Como insertamos por delante, el camino queda en el orden correcto, de s a v. Del siete al tres: siete, seis, cuatro, tres, con distancia tres. "
                    "Si no hay camino, la función lanza una excepción.", 0))


# ---------------------------------------------------------------------------
# D · la máquina calculadora: grafo implícito
# ---------------------------------------------------------------------------
IMP = ED + "Digrafo_implicito_calculadora.cpp"
MAXN = 10000


def ady_calc(v):
    return [(v + 1) % MAXN, (v * 2) % MAXN, v // 3]


def sim_calc(o, d):
    """BFS implícito (el mismo orden que Digrafo_implicito_calculadora.cpp)."""
    dist = {o: 0}
    ant = {}
    q = [o]
    ev = []
    while q:
        v = q.pop(0)
        nuevos, vistos = [], []
        for i, w in enumerate(ady_calc(v)):
            if w not in dist:
                dist[w] = dist[v] + 1
                ant[w] = (v, i)
                nuevos.append((w, i))
                if w == d:
                    ev.append((v, nuevos, vistos))
                    return ev, dist, ant
                q.append(w)
            else:
                vistos.append((w, i))
        ev.append((v, nuevos, vistos))
    return ev, dist, ant


OPS = ["+1", "×2", "÷3"]


def sec_calc(segs):
    # ---- problema
    s = Slide("La máquina calculadora", CORNER)
    s.box(40, 90, 560, 450, "la máquina de Luis")
    s.d.rounded_rectangle((90, 140, 550, 230), 10, fill=(14, 40, 30), outline=C["green"], width=3)
    s.text((520, 185), "9999", size=56, color="green", bold=True, anchor="rm", mono=True)
    for i, (t, d) in enumerate([("+1", "suma uno"), ("×2", "dobla"), ("÷3", "división entera")]):
        x = 90 + i * 160
        s.d.rounded_rectangle((x, 270, x + 140, 350), 12, fill=C["blue_d"], outline=C["blue"], width=3)
        s.text((x + 70, 310), t, size=34, bold=True, anchor="mm")
        s.text((x + 70, 372), d, size=16, color="muted", anchor="mm")
    s.wrap(90, 420, 460, "Marcador de 4 dígitos: todo se hace módulo 10.000.", size=20, color="muted")
    s.bullets(630, 110, 610, [
        "Javier pone un número en la máquina y reta a Luis: conseguir otro número pulsando botones.",
        ("El menor número de pulsaciones.", "gold"),
        "Ejemplo: de 9999 a 6666 se consigue en 2 pulsaciones: ÷3 (3333) y ×2 (6666).",
        "¿Cómo se modela?",
    ], size=21, gap=18)
    segs.append((s, "La máquina calculadora. Javier configura una máquina con un número, y reta a Luis a conseguir otro número pulsando los botones el menor número de veces. "
                    "Hay tres botones: sumar uno, doblar, y dividir entre tres con división entera, siempre con un marcador de cuatro dígitos, es decir, módulo diez mil. "
                    "Por ejemplo, de nueve mil novecientos noventa y nueve a seis mil seiscientos sesenta y seis se llega en dos pulsaciones: dividir entre tres, y doblar.", 0))

    # ---- modelo
    s = Slide("Modelado: un grafo dirigido de números", CORNER)
    s.box(40, 90, 700, 480, "los adyacentes de 9999")
    pc = {9999: (150, 330), 0: (560, 180), 9998: (560, 330), 3333: (560, 480)}
    es = {(9999, 0): ("gold", 4), (9999, 9998): ("gold", 4), (9999, 3333): ("gold", 4)}
    dgr(s, pc, list(es), es=es, r=44, labels={9999: "9999", 0: "0", 9998: "9998", 3333: "3333"}, lsize=22,
        elabels={(9999, 0): ("+1", "gold"), (9999, 9998): ("×2", "gold"), (9999, 3333): ("÷3", "gold")})
    s.wrap(70, 505, 660, "(9999+1) mod 10000 = 0 · (9999·2) mod 10000 = 9998 · 9999 ÷ 3 = 3333", size=15, color="muted", center=True)
    s.bullets(770, 110, 470, [
        ("Vértices: los números 0 … 9999.", "gold"),
        "Aristas: v → w si algún botón convierte v en w.",
        "Cada vértice tiene como mucho 3 aristas de salida.",
        "Es DIRIGIDO: 5000 → 0 con ×2, pero desde 0 no se llega a 5000 con un solo botón.",
        ("Menor nº de pulsaciones = camino más corto ⇒ BFS.", "green"),
    ], size=20, gap=14)
    segs.append((s, "Lo modelamos con un grafo dirigido. Los vértices son los números, de cero a nueve mil novecientos noventa y nueve, y hay una arista de v a w si algún botón convierte v en w. "
                    "Cada vértice tiene como mucho tres aristas de salida. Y es dirigido: con doblar se va de cinco mil a cero, pero desde cero no se llega a cinco mil con un solo botón. "
                    "El menor número de pulsaciones es el camino más corto, así que usamos un B F S.", 0))

    # ---- grafo implícito: código
    L_ADY = find_line(IMP, "int adyacente")
    CODE = code_lines(IMP, L_ADY, find_line(IMP, "}", L_ADY + 6), maxc=48)
    s = Slide("Grafo implícito", "Digrafo_implicito_calculadora.cpp")
    s.code(40, 90, 580, 300, CODE, hl={L_ADY + 2, L_ADY + 3, L_ADY + 4}, title="adyacente(v, i)", size=16)
    s.bullets(650, 105, 590, [
        ("El grafo NO se construye: tiene 10.000 vértices y 30.000 aristas, pero no hace falta guardarlas.", "gold"),
        "adyacente(v, i) calcula al vuelo el i-ésimo sucesor de v.",
        "El BFS lo llama donde antes hacía ady(v).",
        "Se puede parar en cuanto se llega al destino.",
    ], size=20, gap=14)
    s.box(40, 410, 1200, 150, fill=(24, 40, 70), border="gold")
    s.wrap(64, 430, 1150, "Un grafo es implícito cuando sus aristas se pueden deducir de las reglas del problema. "
                          "Es habitual en juegos y puzles: los vértices son estados y las aristas, movimientos.", size=23)
    segs.append((s, "Aquí el grafo es implícito: no lo construimos. Tiene diez mil vértices y treinta mil aristas, pero no hace falta guardarlas, "
                    "porque la función adyacente de v e i calcula al vuelo el i-ésimo sucesor de v. El B F S la llama justo donde antes consultaba los adyacentes, y puede parar en cuanto llega al destino. "
                    "Un grafo es implícito cuando sus aristas se deducen de las reglas del problema, algo muy habitual en juegos y puzles.", 0))

    # ---- traza
    ev, dist, ant = sim_calc(9999, 6666)
    L_B = find_line(IMP, "int bfs(")
    L_POP = find_line(IMP, "int v = cola.front()", L_B)
    L_W = find_line(IMP, "int w = adyacente", L_B)
    L_SET = find_line(IMP, "distancia[w] = distancia[v] + 1;", L_B)
    L_END = find_line(IMP, "if (w == destino)", L_B)
    CODEB = code_lines(IMP, L_B, find_line(IMP, "return -1;", L_B) + 1, maxc=46)
    # posiciones por capas
    PT = {9999: (110, 330), 0: (330, 200), 9998: (330, 300), 3333: (330, 455),
          1: (570, 165), 9996: (570, 255), 3332: (570, 335), 3334: (570, 415), 6666: (570, 500)}
    capa_vistos = []
    cur_edges, cur_labels, cur_nodes = [], {}, {9999: ("gold", "node_t", None)}
    descubiertos = {9999}
    n = len(ev)
    for k, (v, nuevos, vistos) in enumerate(ev, 1):
        s = Slide("BFS implícito: de 9999 a 6666", f"paso {k} de {n}")
        s.code(24, 90, 560, 420, CODEB, hl={L_POP, L_W, L_SET} | ({L_END} if any(w == 6666 for w, _ in nuevos) else set()),
               title="bfs(origen, destino)", size=14)
        s.box(604, 90, 650, 530, "vértices descubiertos (la etiqueta de cada flecha es el botón)")
        for w, i in nuevos:
            cur_edges.append((v, w))
            cur_labels[(v, w)] = (OPS[i], "gold")
            descubiertos.add(w)
        ns = {u: EST_VISIT for u in descubiertos}
        for e2 in ev[:k - 1]:
            ns[e2[0]] = EST_FIN
        ns[v] = ("gold", "node_t", "text")
        for w, i in nuevos:
            if w == 6666:
                ns[w] = ("green", "node_t", "text")
        es = {e: ("blue", 4) for e in cur_edges}
        for w, i in nuevos:
            es[(v, w)] = ("gold", 6)
        pp = {u: (x + 560, y) for u, (x, y) in PT.items() if u in descubiertos or u == v}
        dgr(s, pp, cur_edges, ns=ns, es=es, r=30, labels={u: str(u) for u in pp}, lsize=17, elabels=cur_labels,
            under={u: str(dist[u]) for u in pp if u in dist})
        s.box(24, 530, 560, 90, fill=(14, 28, 60))
        txt = []
        for w, i in nuevos:
            txt.append(f"{OPS[i]} → {w}")
        for w, i in vistos:
            txt.append(f"{OPS[i]} → {w} (visto)")
        s.wrap(40, 545, 530, "saca " + str(v) + ":  " + "   ".join(txt), size=18, color="text")
        # narración
        partes = []
        for w, i in nuevos:
            partes.append(f"{['sumar uno', 'doblar', 'dividir entre tres'][i]} da {w}")
        nar = f"Sacamos el {v}, a distancia {dist[v]}: " + ", ".join(partes) + "."
        if vistos:
            vv = list(dict.fromkeys(str(w) for w, i in vistos))
            nar += f" {'El' if len(vv) == 1 else 'Los'} {' y '.join(vv)} ya {'estaba' if len(vv) == 1 else 'estaban'} visto{'' if len(vv) == 1 else 's'}."
        if any(w == 6666 for w, _ in nuevos):
            nar += " Es el destino: paramos ya, sin terminar de recorrer nada más. Dos pulsaciones."
        if k == 1:
            nar = "Empezamos en nueve mil novecientos noventa y nueve, a distancia cero. " + nar.split(": ", 1)[1].capitalize()
        s.caption("El BFS se detiene al descubrir el destino" if any(w == 6666 for w, _ in nuevos) else "", y=632)
        segs.append((s, nar, 0))

    # ---- camino
    s = Slide("Resultado: 9999 → 6666 en 2 pulsaciones", CORNER)
    s.box(40, 100, 1200, 250)
    xs = [220, 640, 1060]
    cadena = [(9999, None), (3333, "÷3"), (6666, "×2")]
    for i, (u, op) in enumerate(cadena):
        x, y = xs[i], 225
        s.d.ellipse((x - 55, y - 55, x + 55, y + 55), fill=C["green"] if u == 6666 else C["node"])
        s.text((x, y), str(u), size=30, color="node_t", bold=True, anchor="mm")
        if i < 2:
            s.d.line((x + 62, y, xs[i + 1] - 66, y), fill=C["gold"], width=6)
            s.d.polygon([(xs[i + 1] - 62, y), (xs[i + 1] - 84, y - 12), (xs[i + 1] - 84, y + 12)], fill=C["gold"])
            s.text(((x + xs[i + 1]) / 2, y - 30), cadena[i + 1][1], size=30, color="gold", bold=True, anchor="mm")
    s.bullets(70, 385, 1140, [
        "Se visitan pocos vértices antes de llegar: el grafo de 10.000 nunca llega a recorrerse entero.",
        "Con +1 siempre se puede llegar a cualquier número, así que la respuesta siempre existe.",
        "origen == destino ⇒ 0 pulsaciones (se trata con distancia[origen] = 0).",
    ], size=21, gap=16)
    segs.append((s, "El resultado: dos pulsaciones, dividir entre tres y doblar. Antes de llegar solo hemos visitado unos pocos vértices, así que el grafo de diez mil nunca se recorre entero. "
                    "Como con sumar uno se llega a cualquier número, la respuesta siempre existe. Y si origen y destino coinciden, son cero pulsaciones.", 0))

    # ---- explícito vs implícito
    s = Slide("Grafo explícito o implícito", CORNER)
    filas = [("las aristas", "se guardan en ady(v)", "se calculan al vuelo"),
             ("memoria", "V + A", "solo dist: V"),
             ("conviene si", "el grafo se reutiliza en varios casos", "las reglas son sencillas o el grafo es enorme"),
             ("se puede parar al llegar", "sí, igual", "sí, igual"),
             ("en el temario", "EJ 05-2 (se construye una vez), EMT", "PDF 13; alternativa para EJ 05-1")]
    tabla(s, 50, 105, [260, 480, 440], filas, cab=["", "explícito: Digrafo", "implícito: adyacente(v, i)"], size=19, rowh=62)
    s.box(50, 495, 1180, 110, fill=(24, 40, 70), border="gold")
    s.wrap(74, 512, 1130, "Ejemplo del EJ 05-1: con M = 10.000 y N = 100 operaciones construir el Digrafo serían un millón de aristas por caso; "
                         "calcular los sucesores al vuelo evita esa construcción y es más rápido.", size=21)
    segs.append((s, "Entonces, ¿grafo explícito o implícito? En el explícito, las aristas se guardan en las listas de adyacentes, y conviene si el mismo grafo se reutiliza en muchos casos, "
                    "como en el ejercicio cero cinco guion dos. En el implícito, se calculan al vuelo, y conviene si las reglas son sencillas o el grafo es enorme. "
                    "En el ejercicio cero cinco guion uno, por ejemplo, construir un millón de aristas por caso es más lento que calcular los sucesores al vuelo.", 0))


# ---------------------------------------------------------------------------
# E · el grafo de autobuses de la EMT
# ---------------------------------------------------------------------------
BFS_EMT = [(3863, "Paraninfo - Informática"), (1696, "Paraninfo - Derecho"), (1694, "Paraninfo - Filosofía"),
           (1692, "Avenida Complutense - Jardín Botánico"), (1691, "Avenida Complutense - Jardín Botánico"),
           (1693, "Paraninfo - Matemáticas")]
DFS_EMT = [(3863, "Paraninfo - Informática"), (1696, "Paraninfo - Derecho"), (1694, "Paraninfo - Filosofía"),
           (1692, "Avenida Complutense - Jardín Botánico"), (1690, "Avenida Complutense - Ciencias Información"),
           (1688, "Metro Ciudad Universitaria"), (1685, "Cardenal Cisneros"), (1331, "Avenida De La Memoria"),
           (5575, "Moncloa")]
DFS_FIN = [(1686, "Agrónomos"), (1687, "Metro Ciudad Universitaria"), (1689, "Avenida Complutense - Ciencias Información"),
           (1691, "Avenida Complutense - Jardín Botánico"), (1693, "Paraninfo - Matemáticas")]
N_DFS = 2032   # paradas del camino que encuentra el DFS (resultado real de material/emt_ejemplo.cpp)


def parada(s, x, y, num, nombre, col="node", w=190, h=74, ring=None):
    s.d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), 12, fill=C.get(col, col), outline=C.get(ring, ring) if ring else None,
                          width=3 if ring else 0)
    s.text((x, y - 18), str(num), size=22, color="node_t", bold=True, anchor="mm")
    s.wrap(x - w / 2 + 6, y + 2, w - 12, nombre, size=13, color="node_t", gap=0, center=True)


def flecha(s, x1, y, x2, col="gold", wd=4):
    s.d.line((x1, y, x2 - 10, y), fill=C[col], width=wd)
    s.d.polygon([(x2, y), (x2 - 14, y - 8), (x2 - 14, y + 8)], fill=C[col])


def sec_emt(segs):
    LK = find_line(EMT, "for (int k = 1; k < numParadasLinea[i]; ++k)")
    CODE1 = code_lines(EMT, LK - 5, LK + 5, maxc=52)
    s = Slide("Un grafo real: los autobuses de la EMT", "grafoEMT.zip")
    s.code(40, 90, 640, 260, CODE1, hl={LK + 2}, title="leeGrafoEMT()", size=15)
    s.box(700, 90, 540, 260, "datos")
    s.text((720, 130), "paradas.txt", size=18, color="gold", bold=True, mono=True)
    s.text((720, 156), "3863 Paraninfo - Informática", size=15, color="muted", mono=True)
    s.text((720, 176), "1693 Paraninfo - Matemáticas", size=15, color="muted", mono=True)
    s.text((720, 216), "líneas.txt", size=18, color="gold", bold=True, mono=True)
    s.text((720, 242), "<línea> <paradas ida> <paradas vuelta>", size=15, color="muted", mono=True)
    s.text((720, 262), "<nº de parada> <metros desde el inicio>", size=15, color="muted", mono=True)
    s.text((720, 282), "… una fila por parada, ida y vuelta", size=15, color="muted", mono=True)
    s.bullets(60, 375, 1160, [
        ("Vértices: las paradas. Vértice = nº de parada − 1  (hay 50.022).", "gold"),
        "Aristas: de cada parada a la siguiente de su línea, en el sentido de la marcha: 10.956 aristas.",
        "Es dirigido porque cada sentido de una línea tiene paradas distintas: no se puede volver por donde se vino.",
    ], size=20, gap=14)
    segs.append((s, "Y ahora un grafo real: la red de autobuses de la E M T de Madrid. Los vértices son las paradas, el vértice es el número de parada menos uno, y hay cincuenta mil veintidós. "
                    "Por cada línea, y en cada sentido, añadimos una arista de cada parada a la siguiente. Salen diez mil novecientas cincuenta y seis aristas. "
                    "Es dirigido, porque cada sentido de una línea tiene sus propias paradas: no siempre se puede volver por donde se vino.", 0))

    # ---- gemelas
    LG = find_line(EMT, "if (it != paradas.end())")
    CODEG = code_lines(EMT, LG, LG + 6, maxc=46)
    s = Slide("Paradas gemelas", "grafoEMT.zip")
    s.box(40, 90, 620, 330, "paradas con el mismo nombre (una a cada lado de la calle)")
    parada(s, 190, 230, 1691, "Avenida Complutense - Jardín Botánico", "blue", w=210, h=90)
    parada(s, 510, 230, 1692, "Avenida Complutense - Jardín Botánico", "blue", w=210, h=90)
    s.d.line((302, 218, 398, 218), fill=C["purple"], width=5)
    s.d.polygon([(402, 218), (386, 210), (386, 226)], fill=C["purple"])
    s.d.line((398, 246, 302, 246), fill=C["purple"], width=5)
    s.d.polygon([(298, 246), (314, 238), (314, 254)], fill=C["purple"])
    s.text((350, 300), "ponGemelas: arista en los dos sentidos", size=17, color="purple", bold=True, anchor="mm")
    s.text((350, 340), "se puede cruzar la calle andando", size=17, color="muted", anchor="mm")
    s.code(680, 90, 560, 330, CODEG, hl={LG + 1, LG + 2}, title="ponGemelas(Digrafo& g)", size=15)
    s.bullets(60, 450, 1160, [
        "Dos paradas con idéntico nombre suelen estar enfrentadas: se añaden dos aristas, una por sentido.",
        ("Son 4.514 aristas más: 10.956 + 4.514 = 15.470 aristas.", "gold"),
        "Sin ellas no se podría hacer transbordo entre sentidos de una misma calle.",
    ], size=20, gap=12)
    segs.append((s, "Además, las paradas que tienen el mismo nombre suelen estar enfrentadas, una a cada lado de la calle, así que se puede pasar andando de una a otra. "
                    "La función poner gemelas añade una arista en cada sentido entre ellas. Son cuatro mil quinientas catorce aristas más, hasta quince mil cuatrocientas setenta. "
                    "Sin ellas no podríamos hacer transbordos entre sentidos de una misma calle.", 0))

    # ---- BFS
    s = Slide("De Informática a Matemáticas: BFS", "grafoEMT.zip")
    s.box(40, 90, 1200, 330, "origen 3863 → destino 1693 · BFS (CaminoMasCorto)")
    xs = [150 + i * 196 for i in range(6)]
    for i, (num, nom) in enumerate(BFS_EMT):
        col = "gold" if i in (0, 5) else "node"
        ring = None
        if i == 4:
            col = "node"
        parada(s, xs[i], 255, num, nom, col, w=172, h=100, ring="purple" if i in (3, 4) else None)
        if i < 5:
            flecha(s, xs[i] + 88, 255, xs[i + 1] - 86, "purple" if i == 3 else "blue", 4)
    s.text((xs[3] + 101, 325), "gemelas", size=16, color="purple", bold=True, anchor="mm")
    s.text((640, 380), "5 aristas  ·  6 paradas", size=26, color="green", bold=True, anchor="mm")
    s.bullets(60, 450, 1160, [
        "CaminoMasCorto es el BFS de las transparencias, con ant, dist y parada anticipada al llegar al destino.",
        "Sale: Informática → Derecho → Filosofía → Jardín Botánico (ida) → Jardín Botánico (enfrente) → Matemáticas.",
        ("El salto entre las dos paradas Jardín Botánico es una arista «gemela».", "purple"),
    ], size=19, gap=12)
    segs.append((s, "Buscamos el camino de la parada Paraninfo Informática, la tres mil ochocientos sesenta y tres, a la parada Paraninfo Matemáticas, la mil seiscientos noventa y tres. "
                    "El B F S nos da un camino de cinco aristas, seis paradas: Informática, Derecho, Filosofía, Jardín Botánico, la parada gemela de enfrente, y Matemáticas. "
                    "El salto entre las dos paradas de Jardín Botánico es una de las aristas gemelas.", 0))

    # ---- DFS
    s = Slide("El mismo trayecto con DFS", "grafoEMT.zip")
    s.box(40, 90, 1200, 330, "origen 3863 → destino 1693 · DFS (CaminosDFS)")
    for i, (num, nom) in enumerate(DFS_EMT[:5]):
        x = 150 + i * 196
        parada(s, x, 215, num, nom, "node", w=172, h=84)
        flecha(s, x + 88, 215, x + 110, "red", 4) if i < 4 else None
    s.text((1130, 215), "…", size=60, color="red", bold=True, anchor="mm")
    s.text((640, 300), "2.032 paradas", size=44, color="red", bold=True, anchor="mm")
    s.text((640, 355), "el primer camino que encuentra el DFS: Moncloa, Príncipe Pío, Illescas, Valmojado…", size=19, color="muted", anchor="mm")
    s.text((640, 390), "y por fin vuelve a Ciudad Universitaria para acabar en Matemáticas", size=19, color="muted", anchor="mm")
    s.bullets(60, 450, 1160, [
        "El DFS baja por la primera arista de cada lista: de Jardín Botánico no gira a la gemela, sigue por la línea.",
        ("Cuando por fin llega, el camino tiene 2.032 paradas en lugar de 6.", "red"),
    ], size=21, gap=14)
    segs.append((s, "Si lo hacemos con un D F S, el resultado es muy distinto. El recorrido baja por la primera arista de cada lista, y de Jardín Botánico no gira a la gemela, sigue por la línea. "
                    "Pasa por Moncloa, Príncipe Pío, y llega hasta Illescas y Valmojado, a decenas de kilómetros. Solo después vuelve a la Ciudad Universitaria y acaba en Matemáticas. "
                    "El camino tiene dos mil treinta y dos paradas, en lugar de seis.", 0))

    # ---- moraleja
    s = Slide("BFS contra DFS", CORNER)
    s.box(60, 100, 540, 330, fill=(14, 50, 40), border="green")
    s.text((330, 150), "BFS", size=40, color="green", bold=True, anchor="mm")
    s.text((330, 220), "6 paradas", size=44, bold=True, anchor="mm")
    s.text((330, 275), "camino MÁS CORTO", size=24, color="green", anchor="mm")
    s.wrap(90, 320, 480, "explora por capas, con una cola", size=20, color="muted", center=True)
    s.box(680, 100, 540, 330, fill=(60, 24, 24), border="red")
    s.text((950, 150), "DFS", size=40, color="red", bold=True, anchor="mm")
    s.text((950, 220), "2.032 paradas", size=44, bold=True, anchor="mm")
    s.text((950, 275), "UN camino cualquiera", size=24, color="red", anchor="mm")
    s.wrap(710, 320, 480, "se mete a fondo con una pila", size=20, color="muted", center=True)
    s.bullets(80, 460, 1120, [
        "Los dos responden bien a «¿hay camino de s a t?».",
        ("Si importa cuántas aristas, o el menor número de pasos: BFS.", "gold"),
    ], size=23, gap=16)
    segs.append((s, "La moraleja: los dos recorridos responden igual de bien a la pregunta de si hay un camino de s a t. "
                    "Pero el B F S encuentra el más corto, y el D F S encuentra uno cualquiera, que puede ser larguísimo. "
                    "Cuando importa el número de aristas, o el menor número de pasos, hay que usar B F S.", 0))


# ---------------------------------------------------------------------------
# F · ordenación topológica
# ---------------------------------------------------------------------------
LAB7 = {v: str(v) for v in range(N7)}
ORD7 = [3, 6, 0, 5, 2, 1, 4]


def g7(s, ox=90, oy=165, k=0.95, ns=None, es=None, title="DAG de las transparencias: 7 vértices, 11 aristas", box=(40, 90, 520, 500), r=24, under=None):
    s.box(*box, title)
    base = {e: ("muted", 3) for e in E7}
    base.update(es or {})
    dgr(s, P7(ox, oy, k), E7, ns=ns, es=base, labels=LAB7, r=r, under=under)


def sec_topo(segs):
    # ---- planificación
    s = Slide("Planificación de tareas con precedencia", CORNER)
    g7(s, title="tareas = vértices · «a antes que b» = arista a → b")
    s.bullets(590, 110, 650, [
        "Tenemos tareas con restricciones de precedencia.",
        ("¿En qué orden deberíamos planificarlas?", "gold"),
        "Un ORDEN TOPOLÓGICO ordena los vértices de forma que toda arista vaya de un vértice a otro POSTERIOR.",
        ("Imprescindible que no haya ciclos: el grafo debe ser un DAG (grafo dirigido acíclico).", "red"),
    ], size=21, gap=18)
    segs.append((s, "Pasamos a la ordenación topológica. Imaginemos tareas con restricciones de precedencia: una tarea tiene que hacerse antes que otra. "
                    "¿En qué orden las planificamos? Un orden topológico ordena los vértices de forma que toda arista vaya de un vértice a otro posterior. "
                    "Y es imprescindible que no haya ciclos: el grafo tiene que ser un D A G, un grafo dirigido acíclico.", 0))

    # ---- orden con arcos
    s = Slide("Un orden topológico: todas las flechas hacia la derecha", CORNER)
    s.box(40, 90, 1200, 290)
    arcos(s, ORD7, E7, 340, 160, 150, hs=0.14)
    s.wrap(60, 400, 1160, "Un orden válido:  3  6  0  5  2  1  4", size=26, center=True, bold=True)
    s.wrap(60, 450, 1160, "No es único: también valdría 3 6 0 1 5 2 4. Basta con respetar todas las flechas.", size=21, color="muted", center=True)
    s.wrap(60, 500, 1160, "Con un ciclo, ningún orden vale: cada vértice del ciclo tendría que ir antes que otro que, a su vez, va antes que él.", size=21, color="red", center=True)
    segs.append((s, "Este es el mismo grafo dibujado en línea, con el orden tres, seis, cero, cinco, dos, uno, cuatro. Todas las flechas van hacia la derecha. "
                    "El orden no es único: también valdría tres, seis, cero, uno, cinco, dos, cuatro. Y si hay un ciclo, ningún orden sirve, porque cada vértice del ciclo tendría que ir antes que otro que a su vez va antes que él.", 0))

    # ---- idea postorden
    segs.append((ideas("Cómo se calcula: postorden", [
        "Hacemos un DFS que recorre todos los vértices.",
        ("Añadimos cada vértice a la lista DESPUÉS de las llamadas recursivas (postorden).", "gold"),
        "Cuando v se añade, todos sus sucesores ya están en la lista: ya han terminado.",
        ("El orden topológico es el postorden al revés (postorden inverso).", "green"),
    ], CORNER), "El algoritmo es un D F S que recorre todos los vértices. Añadimos cada vértice a una lista después de las llamadas recursivas, es decir, en postorden. "
                "Cuando añadimos v, todos sus sucesores ya están en la lista, porque ya han terminado. Así que el orden topológico es el postorden al revés.", 0))

    # ---- traza
    ev, post_final = sim_topo(A7)
    L0 = find_line(ALG, "class OrdenTopologico")
    LD = find_line(ALG, "void dfs(", L0)
    L_PF = find_line(ALG, "_orden.push_front(v);", L0)
    CODE = code_lines(ALG, LD, find_line(ALG, "}", L_PF), maxc=44)
    n = len(ev)
    for k, (v, post, visit, pila) in enumerate(ev, 1):
        s = Slide("Postorden en el DAG", f"paso {k} de {n}")
        s.code(24, 90, 480, 215, CODE, hl={L_PF}, title="dfs(g, v)", size=15)
        s.box(24, 325, 480, 265, "estado")
        s.text((44, 362), f"termina el vértice {v}", size=22, color="gold", bold=True)
        s.queue_row(44, 405, "postorden", post, size=17)
        s.queue_row(44, 460, "pila dfs", pila, size=17)
        s.wrap(44, 515, 440, "se añade a postorden cuando acaba su dfs, no al entrar.", size=16, color="muted")
        ns = {u: EST_FIN for u in post}
        for u in pila:
            ns[u] = EST_ACT
        ns[v] = ("green", "node_t", "text")
        g7(s, ox=630, oy=165, k=0.95, ns=ns, title="verde: terminado · amarillo: en la pila (DFS en curso)", box=(524, 90, 730, 500))
        suc = A7[v]
        if suc:
            if len(suc) == 1:
                nar = f"Termina el {v}: su sucesor, {y_lista(suc)}, ya ha terminado. Entra en postorden."
            else:
                nar = f"Termina el {v}: sus sucesores, {y_lista(suc)}, ya han terminado. Entra en postorden."
            cap = f"{v} termina: sus sucesores ({nombres(suc)}) ya están en postorden"
        else:
            nar = f"El {v} no tiene sucesores: termina y entra en postorden."
            cap = f"{v} no tiene sucesores: termina y entra el primero en postorden"
        if k == 1:
            nar = "El D F S empieza en el cero, baja al uno y de ahí al cuatro. " + nar
        nar += f" Postorden: {' '.join(str(x) for x in post)}."
        s.caption(cap + f"   ·   postorden = {' '.join(str(x) for x in post)}", y=618)
        segs.append((s, nar, 0))

    # ---- inverso
    inv = list(reversed(post_final))
    s = Slide("Postorden inverso = orden topológico", CORNER)
    s.box(40, 90, 1200, 160)
    s.text((70, 118), "postorden:", size=22, color="muted", bold=True)
    s.queue_row(230, 112, "", post_final, size=22)
    s.text((70, 182), "al revés:", size=22, color="gold", bold=True)
    s.queue_row(230, 176, "", inv, size=22)
    s.box(40, 270, 1200, 300)
    arcos(s, inv, E7, 520, 160, 150, hs=0.14)
    s.caption("Todas las flechas van hacia la derecha: 3 6 0 5 2 1 4 es un orden topológico.", y=585)
    segs.append((s, "Al terminar, el postorden es cuatro, uno, dos, cinco, cero, seis, tres. Le damos la vuelta y sale tres, seis, cero, cinco, dos, uno, cuatro, "
                    "exactamente el orden de las transparencias. Y todas las flechas van hacia la derecha.", 0))

    # ---- código
    s = Slide("Implementación", "Digrafo_algoritmos.h")
    CODE = code_lines(ALG, L0, find_line(ALG, "};", LD), maxc=50)
    s.code(40, 90, 680, 500, CODE, hl={L_PF}, title="class OrdenTopologico", size=15)
    s.bullets(750, 110, 490, [
        "El constructor lanza el dfs desde cada vértice no visitado.",
        ("push_front(v) después de las llamadas recursivas: el postorden queda ya invertido.", "gold"),
        "orden() devuelve el deque con el orden topológico.",
        ("Precondición: g es un DAG. Con un ciclo no falla, pero el orden NO es válido.", "red"),
        "Coste O(V + A).",
    ], size=20, gap=14)
    segs.append((s, "En el código, el constructor lanza el D F S desde cada vértice no visitado. Y en lugar de guardar el postorden y darle la vuelta, "
                    "se usa push front después de las llamadas recursivas, así que el orden ya queda invertido. "
                    "Pero cuidado: el grafo tiene que ser un D A G. Con un ciclo el algoritmo no falla, pero el resultado no es un orden válido. El coste es uve más a.", 0))

    # ---- corrección: tres casos con líneas de tiempo
    s = Slide("Corrección: ¿por qué funciona?", CORNER)
    s.text((640, 92), "Para cualquier arista v → w, al hacer dfs(v):", size=22, color="muted", anchor="mm")
    casos = [
        ("Caso 1", "dfs(w) ya terminó", "green", (330, 440), (150, 250), "w termina antes de que v empiece"),
        ("Caso 2", "dfs(w) aún no empezó", "green", (150, 440), (230, 340), "v llama a w: w termina antes que v"),
        ("Caso 3", "dfs(w) empezó y no ha terminado", "red", (270, 340), (150, 440), "IMPOSIBLE en un DAG"),
    ]
    for i, (t, d, col, bv, bw, nota) in enumerate(casos):
        x0 = 40 + i * 405
        s.box(x0, 120, 385, 400, fill=(14, 28, 60), border=col)
        s.text((x0 + 20, 142), t, size=24, color=col, bold=True)
        s.wrap(x0 + 20, 178, 345, d, size=19, color="text")
        base = x0 - 150 + 20
        # barras de tiempo
        s.text((x0 + 20, 262), "tiempo →", size=14, color="dim")
        s.d.line((x0 + 20, 280, x0 + 360, 280), fill=C["dim"], width=2)
        for (lab, (a, b), yy, cc) in (("dfs(v)", bv, 305, "gold"), ("dfs(w)", bw, 365, "blue")):
            xa, xb = x0 + 20 + (a - 150) * 340 / 290, x0 + 20 + (b - 150) * 340 / 290
            s.d.rounded_rectangle((xa, yy, xb, yy + 36), 8, fill=C[cc])
            s.text(((xa + xb) / 2, yy + 18), lab, size=17, color="node_t", bold=True, anchor="mm")
        s.wrap(x0 + 20, 430, 345, nota, size=19, color=col, bold=True)
    s.wrap(40, 540, 1200, "En los casos 1 y 2, w termina antes que v ⇒ w queda DESPUÉS de v en el postorden inverso. "
                          "El caso 3 exigiría un camino de w a v: junto con v → w sería un ciclo.", size=21, color="text", center=True)
    segs.append((s, "¿Por qué funciona? Tomamos cualquier arista de v a w y miramos qué pasa al hacer D F S de v. "
                    "Caso uno: D F S de w ya se hizo y terminó. Entonces w terminó antes que v. "
                    "Caso dos: D F S de w aún no se ha hecho. La arista de v a w provoca esa llamada, y w terminará antes que v. "
                    "Caso tres: D F S de w ha empezado pero no ha terminado. Es imposible: la cadena de llamadas implica un camino de w a v, y con la arista de v a w sería un ciclo, que en un D A G no existe. "
                    "En los dos casos posibles, w termina antes que v, así que en el postorden inverso w va después de v.", 0))


# ---------------------------------------------------------------------------
# G · detección de ciclos
# ---------------------------------------------------------------------------
def sec_ciclo(segs):
    L0 = find_line(ALG, "class CicloDirigido")
    LD = find_line(ALG, "void dfs(", L0)
    CODE = code_lines(ALG, LD, find_line(ALG, "apilado[v] = false;", LD) + 1, maxc=54)
    L_AP = find_line(ALG, "apilado[v] = true;", LD)
    L_VIS = find_line(ALG, "visit[v] = true;", LD)
    L_NEW = find_line(ALG, "if (!visit[w])", LD)
    L_ANT = find_line(ALG, "ant[w] = v; dfs(g, w);", LD)
    L_CIC = find_line(ALG, "else if (apilado[w])", LD)
    L_HAY = find_line(ALG, "hayciclo = true;", LD)
    L_BACK = find_line(ALG, "for (int x = v; x != w", LD)
    L_PF1 = find_line(ALG, "_ciclo.push_front(x);", LD)
    L_PF2 = find_line(ALG, "_ciclo.push_front(w);", LD)
    L_OUT = find_line(ALG, "apilado[v] = false;", LD)

    segs.append((ideas("Detección de ciclos dirigidos", [
        "Un ciclo hace imposible un orden de tareas, y aparece en muchos problemas reales (dependencias circulares).",
        ("Se usa un DFS: la pila de la recursión contiene el camino actual.", "gold"),
        "Si desde v vemos un vértice w que SIGUE EN LA PILA, la arista v → w cierra un ciclo.",
        "Hacen falta dos marcas: visit (¿ya lo alcanzamos?) y apilado (¿está ahora en la pila?).",
    ], CORNER), "Pasamos a la detección de ciclos. Un ciclo hace imposible ordenar tareas, y aparece en muchos problemas reales, como las dependencias circulares. "
                "Usamos un D F S, porque la pila de la recursión contiene el camino actual. "
                "Si desde v vemos un vértice w que sigue en la pila, la arista de v a w cierra un ciclo. "
                "Para eso hacen falta dos marcas: visit, que dice si ya hemos alcanzado el vértice, y apilado, que dice si está ahora mismo en la pila.", 0))

    # ---- tres casos para un vecino
    s = Slide("Un vecino w de v: tres casos", CORNER)
    filas = [("w sin visitar", "visit[w] = false", "es un vértice nuevo: ant[w] = v y seguimos con dfs(w)", "green"),
             ("w visitado y APILADO", "apilado[w] = true", "w es un antecesor de v: la arista v → w cierra un CICLO", "red"),
             ("w visitado y NO apilado", "apilado[w] = false", "w ya terminó: lo que sale de w ya se exploró, sin ciclo por ahí", "blue")]
    y = 115
    for t, c, d, col in filas:
        s.box(60, y, 1160, 120, fill=(14, 28, 60), border=col)
        s.text((90, y + 28), t, size=26, color=col, bold=True)
        s.text((90, y + 74), c, size=20, color="muted", mono=True)
        s.wrap(560, y + 32, 630, d, size=22)
        y += 140
    s.caption("Ver un vértice ya visitado NO basta para decir que hay un ciclo: tiene que estar apilado.", y=545)
    segs.append((s, "Para cada vecino w de v hay tres casos. Si w está sin visitar, es un vértice nuevo: guardamos ant de w igual a v, y seguimos. "
                    "Si w está visitado y apilado, es un antecesor de v, y la arista de v a w cierra un ciclo. "
                    "Y si w está visitado pero ya no está apilado, es que terminó: lo que sale de w ya se exploró y no hay ciclo por ahí. "
                    "Ver un vértice visitado no basta; tiene que estar apilado.", 0))

    # ---- código
    s = Slide("Implementación", "Digrafo_algoritmos.h")
    s.code(40, 90, 740, 500, CODE, hl={L_AP, L_CIC}, title="CicloDirigido::dfs", size=15)
    s.bullets(805, 105, 435, [
        "apilado[v] = true al entrar y false al salir: es la pila.",
        "ant[w] = v permite luego reconstruir el ciclo.",
        "Al detectarlo, hayciclo = true y se corta todo el recorrido.",
        "Coste O(V + A).",
    ], size=19, gap=14)
    segs.append((s, "En el código, apilado de v se pone a verdadero al entrar en dfs y a falso al salir: es la pila de la recursión. "
                    "ant de w guarda el vértice anterior, y nos servirá para reconstruir el ciclo. Cuando se detecta un ciclo, se activa hayciclo y se corta todo el recorrido. "
                    "El coste es uve más a.", 0))

    # ---- traza sobre el digrafo de 13 vértices
    ev, ciclo = sim_ciclo(A13, range(N13))
    entras = [e for e in ev if e[0] in ("entra", "ciclo")]
    n = len(entras)
    prev = None
    for k, (tipo, v, w, visit, ap, pila, ant) in enumerate(entras, 1):
        s = Slide("Buscando un ciclo en el digrafo", f"paso {k} de {n}")
        hl = {L_AP, L_VIS}
        if tipo == "ciclo":
            hl = {L_CIC, L_HAY}
        elif ant[v] is not None:
            hl = {L_NEW, L_ANT}
        s.code(24, 90, 480, 360, CODE, hl=hl, title="CicloDirigido::dfs", size=13)
        s.box(24, 465, 480, 135, "estado")
        s.queue_row(40, 495, "apilado", [u for u in pila], size=16)
        s.queue_row(40, 545, "visit", [u for u in range(N13) if visit[u]], size=15)
        s.box(524, 90, 730, 510, "grafo (azul: visitado · amarillo: en la pila · rojo: ciclo)")
        ns = {u: EST_VISIT for u in range(N13) if visit[u]}
        for u in pila:
            ns[u] = EST_ACT
        es = {e: ("muted", 3) for e in E13}
        for u in range(N13):
            if ant[u] is not None and visit[u]:
                es[(ant[u], u)] = ("gold", 5)
        if tipo == "ciclo":
            for u in ciclo:
                ns[u] = EST_RED
            es[(v, w)] = ("red", 8)
            for a, b in zip(ciclo[1:], ciclo[2:]):
                es[(a, b)] = ("red", 8)
            es[(ciclo[-1], ciclo[0])] = ("red", 8) if False else es.get((ciclo[-1], ciclo[0]), ("muted", 3))
        else:
            ns[v] = ("gold", "node_t", "text")
        dgr(s, P13(550, 135, 0.92), E13, ns=ns, es=es, labels=LAB13, r=21)
        if tipo == "entra":
            if ant[v] is None:
                cap = f"Empezamos en {v}: visit y apilado a true"
                nar = f"Empezamos en el {v}: lo marcamos como visitado y lo apilamos."
            else:
                a = ant[v]
                cap = f"{a} → {v}: el {v} está sin visitar, ant[{v}] = {a}"
                if prev is not None and a != prev:
                    nar = f"Volvemos atrás hasta el {a}, y desde ahí el {v} está sin visitar: ant del {v} es {a}. Lo apilamos."
                else:
                    nar = f"El {v} está sin visitar: ant del {v} es {a}. Lo apilamos."
            if not A13[v]:
                nar += " No tiene sucesores: sale de la pila enseguida."
            prev = v
        else:
            cap = f"{v} → {w}: el {w} está visitado Y apilado  ⇒  CICLO"
            nar = f"Del {v} al {w}: el {w} ya está visitado, y además sigue apilado. Hemos vuelto a un antecesor: hay un ciclo."
        s.caption(cap, y=618)
        segs.append((s, nar, 0))

    # ---- recuperar el ciclo
    s = Slide("Recuperar el ciclo con ant", "Digrafo_algoritmos.h")
    CODER = code_lines(ALG, L_HAY, L_PF2, maxc=46)
    s.code(40, 90, 600, 220, CODER, hl={L_BACK, L_PF1, L_PF2}, title="al detectar v → w  (v = 3, w = 2)", size=16)
    s.box(660, 90, 580, 220, "ant: 0 → 5 → 4 → 2 → 3")
    cad = [0, 5, 4, 2, 3]
    for i, u in enumerate(cad):
        x = 700 + i * 115
        s.d.ellipse((x - 26, 195, x + 26, 247), fill=C["gold"] if u in (2, 3) else C["node"])
        s.text((x, 221), str(u), size=24, color="node_t", bold=True, anchor="mm")
        if i < 4:
            flecha(s, x + 30, 221, x + 85, "gold", 3)
    s.text((950, 140), "camino actual: la pila", size=18, color="muted", anchor="mm")
    s.text((950, 280), "v = 3, w = 2:  3 → 2 cierra el ciclo", size=18, color="red", bold=True, anchor="mm")
    s.bullets(60, 330, 1160, [
        "x = v = 3: se añade al ciclo (por delante). x = ant[3] = 2 = w: se para.",
        "Luego push_front(w) y push_front(v): el ciclo queda  3 → 2 → 3.",
        ("El primer y el último vértice coinciden: así se ve que es un ciclo cerrado.", "gold"),
        "Si no hay ciclo, ciclo() es una lista vacía y hayCiclo() devuelve false.",
    ], size=21, gap=14)
    segs.append((s, "Para recuperar el ciclo seguimos ant hacia atrás desde v hasta llegar a w. Aquí, v es el tres y w es el dos. "
                    "Añadimos el tres, retrocedemos al dos, que es w, y paramos. Luego añadimos w y v por delante, y el ciclo queda tres, dos, tres. "
                    "El primero y el último coinciden, porque es un ciclo cerrado. Si no hay ciclo, la lista queda vacía.", 0))

    # ---- sin ciclo: DAG
    s = Slide("En un DAG nunca se cumple el caso del ciclo", CORNER)
    ns = {u: EST_FIN for u in range(N7)}
    g7(s, ns=ns, es={(5, 2): ("blue", 7)}, title="DFS en el DAG: la arista 5 → 2")
    s.bullets(590, 110, 650, [
        "Cuando desde 5 se mira el 2, el 2 ya estaba visitado…",
        ("…pero ya había terminado: no está apilado. No es un ciclo.", "blue"),
        "Así se distingue un ciclo de un simple «camino que se vuelve a encontrar».",
        ("Si CicloDirigido no encuentra nada, el grafo es un DAG y se puede ordenar topológicamente.", "green"),
    ], size=21, gap=18)
    segs.append((s, "En un D A G el caso del ciclo nunca se da. Por ejemplo, cuando desde el cinco se mira el dos, el dos ya estaba visitado, pero ya había terminado, así que no está apilado y no es un ciclo. "
                    "Así se distingue un ciclo de un simple vértice que se vuelve a encontrar por otro camino. "
                    "Y si el detector no encuentra nada, el grafo es un D A G y se puede ordenar topológicamente.", 0))

    # ---- relación con EJ 05-3
    s = Slide("Ciclos y orden topológico, juntos", "EJ_05-3.cpp")
    filas = [("0 · sin visitar", "visit = false", "todavía no hemos llegado", "muted"),
             ("1 · en la pila", "apilado = true", "lo estamos explorando", "gold"),
             ("2 · terminado", "visit = true, apilado = false", "ya hemos explorado todo lo suyo", "green")]
    for i, (a, b, c, col) in enumerate(filas):
        y = 110 + i * 100
        s.box(60, y, 1160, 84, fill=(14, 28, 60), border=col)
        s.d.ellipse((90, y + 20, 134, y + 64), fill=C["node"] if col == "muted" else C[col])
        s.text((160, y + 42), a, size=24, bold=True, anchor="lm")
        s.text((520, y + 42), b, size=19, color="muted", mono=True, anchor="lm")
        s.text((1190, y + 42), c, size=19, color="muted", anchor="rm")
    s.bullets(70, 430, 1140, [
        "El EJ 05-3 junta las dos ideas en un solo DFS con tres estados por vértice (0, 1, 2).",
        "Un vecino en estado 1 = ciclo = «Imposible». Si no, el postorden inverso es el orden.",
    ], size=22, gap=16)
    segs.append((s, "En el ejercicio cero cinco guion tres juntamos las dos ideas en un solo D F S con tres estados por vértice: cero, sin visitar; uno, en la pila; y dos, terminado. "
                    "Un vecino en estado uno es un ciclo, y la respuesta es imposible. Si no, el postorden inverso es el orden que buscamos.", 0))


# ---------------------------------------------------------------------------
# H · extras: componentes fuertemente conexas, resumen, pistas, ejercicios
# ---------------------------------------------------------------------------
def sec_cfc(segs):
    L0 = find_line(ALG, "class CFC")
    CODE = code_lines(ALG, L0, find_line(ALG, "};", L0), maxc=56)
    L_ORD = find_line(ALG, "OrdenTopologico ord(g.inverso());", L0)
    L_FOR = find_line(ALG, "for (int v : ord.orden())", L0)
    L_DFS = find_line(ALG, "dfs(g, v);", L0)
    L_NUM = find_line(ALG, "++_num;", L0)
    L_SET = find_line(ALG, "_comp[v] = _num;", L0)

    s = Slide("EXTRA · Componentes fuertemente conexas", "Digrafo_algoritmos.h")
    s.code(40, 90, 690, 500, CODE, hl={L_ORD, L_FOR, L_DFS}, title="class CFC (algoritmo de Kosaraju)", size=14)
    s.bullets(755, 105, 485, [
        ("1. Orden: postorden inverso de un DFS sobre el grafo INVERSO.", "purple"),
        ("2. DFS sobre el grafo ORIGINAL siguiendo ese orden: cada árbol que sale es una componente.", "gold"),
        "Resuelve «¿es fuertemente conexo?», «¿están v y w en la misma componente?» y cuántas hay.",
        "Coste O(V + A): dos DFS y un inverso().",
    ], size=19, gap=14)
    segs.append((s, "Un extra que no viene en las transparencias, pero que enlaza con todo lo anterior: las componentes fuertemente conexas, con el algoritmo de Kosaraju. "
                    "Primero calculamos un orden: el postorden inverso de un D F S sobre el grafo inverso. "
                    "Después hacemos un D F S sobre el grafo original, siguiendo ese orden, y cada árbol que sale es una componente. "
                    "Cuesta uve más a: dos recorridos y un inverso.", 0))

    inv, post, orden, pasos = sim_cfc(A13)
    # orden
    s = Slide("Kosaraju · paso 1: el orden", CORNER)
    s.box(40, 90, 1200, 150)
    s.text((70, 118), "postorden en g.inverso():", size=21, color="muted", bold=True)
    chips(s, 400, 112, post, w=44, h=34, size=17)
    s.text((70, 176), "al revés (orden):", size=21, color="gold", bold=True)
    chips(s, 400, 170, orden, w=44, h=34, size=17)
    s.box(40, 260, 1200, 330, "grafo inverso g.inverso()")
    inv_edges = [(b, a) for a, b in E13]
    dgr(s, pos(REL13, 330, 300, 0.9), inv_edges, es={e: ("purple", 3) for e in inv_edges}, labels=LAB13, r=20)
    s.text((70, 330), "ady(v) en el", size=17, color="muted")
    s.text((70, 354), "inverso = quién", size=17, color="muted")
    s.text((70, 378), "llega a v en g", size=17, color="muted")
    segs.append((s, "Paso uno: hacemos el recorrido en profundidad del grafo inverso, y nos quedamos con el postorden inverso. "
                    "Sale uno, cero, dos, tres, cuatro, once, nueve, doce, diez, seis, ocho, siete, cinco. Es el orden en el que vamos a empezar los recorridos en el grafo original.", 0))

    # componentes
    for k, (v, comp, cm) in enumerate(pasos):
        s = Slide("Kosaraju · paso 2: recorremos g en ese orden", f"árbol {k + 1} de {len(pasos)}")
        s.code(24, 90, 480, 200, code_lines(ALG, L_FOR, L_NUM + 1, maxc=40), hl={L_FOR, L_DFS, L_NUM}, title="constructor", size=14)
        s.box(24, 310, 480, 280, "estado")
        s.text((44, 346), f"empezamos en {v}: el primero sin visitar", size=19, color="gold", bold=True)
        s.text((44, 384), "orden (atenuados: ya visitados)", size=15, color="muted")
        hecho = {u for u in range(N13) if cm[u] >= 0 and u not in comp}
        chips(s, 44, 408, orden, hecho=hecho, actual=v)
        s.text((44, 462), f"su DFS en g alcanza:  {{{nombres(comp)}}}", size=19, color=COMP_COL[k], bold=True)
        s.wrap(44, 500, 440, f"→ componente {k}: todos esos vértices reciben comp[] = {k}.", size=16, color="muted")
        s.box(524, 90, 730, 500, "colores: una componente por color")
        ns = {}
        for u in range(N13):
            if cm[u] >= 0:
                ns[u] = (COMP_COL[cm[u]], "node_t", None)
        for u in comp:
            ns[u] = (COMP_COL[k], "node_t", "text" if u == v else None)
        es = {}
        for a, b in E13:
            if cm[a] >= 0 and cm[a] == cm[b]:
                es[(a, b)] = (COMP_COL[cm[a]], 4)
        dgr(s, P13(550, 140, 0.92), E13, ns=ns, es={**{e: ("muted", 3) for e in E13}, **es}, labels=LAB13, r=21)
        if len(comp) == 1:
            nar = f"Empezamos en el {v}: su recorrido en el grafo original solo alcanza el propio {v}. Primera componente: el {v} solo." if k == 0 else \
                  f"Empezamos en el {v}: su recorrido solo alcanza el propio {v}. Otra componente, de un solo vértice."
        else:
            nar = f"El siguiente vértice sin visitar es el {v}. Su recorrido en el grafo original alcanza {y_lista(comp)}: son una componente."
        s.caption(f"{{{nombres(comp)}}}: componente {k}", y=618)
        segs.append((s, nar, 0))

    s = Slide("Resultado: 5 componentes", CORNER)
    ns = {}
    for k, comp in enumerate(SCC13):
        for u in comp:
            ns[u] = (COMP_COL[[0, 1, 3, 4, 2][k] if False else [c for c, cc in enumerate([p[1] for p in pasos]) if u in cc][0]], "node_t", None)
    s.box(40, 90, 780, 470)
    dgr(s, P13(), E13, ns=ns, es={e: ("muted", 3) for e in E13}, labels=LAB13, r=22)
    s.bullets(850, 110, 390, [
        "5 componentes, igual que en las transparencias.",
        "cfc.componente(v) da el número; dos vértices están en la misma si coincide.",
        ("Si hay una sola componente, el grafo es fuertemente conexo.", "gold"),
        "Si se «encoge» cada componente a un vértice sale un DAG: por eso tiene sentido ordenarlas topológicamente.",
    ], size=19, gap=14)
    segs.append((s, "Y salen las cinco componentes de las transparencias. Con componente de v sabemos a qué componente pertenece cada vértice, y dos vértices están en la misma si el número coincide. "
                    "Si solo hay una, el grafo es fuertemente conexo. Y si encogemos cada componente a un único vértice, lo que queda es un D A G, "
                    "por eso tiene sentido ordenar las componentes topológicamente.", 0))


def sec_final(segs):
    # ---- tabla resumen
    s = Slide("Resumen: problema → herramienta", CORNER)
    filas = [("¿hay camino de s a t?", "DFSDirigido / BFSDirigido", "O(V + A)"),
             ("camino con menos aristas", "BFSDirigido (dist, ant, camino)", "O(V + A)"),
             ("estados de un juego o puzle", "BFS sobre grafo implícito", "O(estados · movimientos)"),
             ("¿hay un ciclo? ¿cuál?", "CicloDirigido (apilado, ant)", "O(V + A)"),
             ("orden de tareas con dependencias", "OrdenTopologico (postorden inverso)", "O(V + A)"),
             ("¿fuertemente conexo? componentes", "CFC (Kosaraju, usa inverso)", "O(V + A)"),
             ("cierre transitivo", "un DFS desde cada vértice", "O(V · (V + A))")]
    tabla(s, 50, 105, [430, 480, 270], filas, cab=["pregunta", "herramienta", "coste"], size=20, rowh=62, hl=(5, 6))
    s.caption("Resaltados, los extras: las transparencias no traen su código.", y=635)
    segs.append((s, "Para resumir: ¿hay un camino? D F S o B F S. ¿El de menos aristas? B F S, con dist, ant y camino. Estados de un juego o puzle: B F S sobre un grafo implícito. "
                    "¿Hay un ciclo, y cuál? El detector con apilado y ant. Orden de tareas con dependencias: el postorden inverso. "
                    "Y como extras, las componentes fuertemente conexas con Kosaraju, y el cierre transitivo, con un D F S desde cada vértice. Casi todo cuesta uve más a.", 0))

    # ---- pistas del juez
    s = Slide("Cómo reconocerlo en el juez", CORNER)
    filas = [("«mínimo número de pasos / jugadas / pulsaciones»", "BFS (camino más corto)"),
             ("«¿se puede llegar de A a B?»", "DFS o BFS, mira visit[]"),
             ("«A debe hacerse antes que B»", "grafo A → B + orden topológico"),
             ("«imposible» / «dependencia circular»", "ciclo dirigido: vecino en la pila"),
             ("estados con reglas de movimiento", "grafo implícito + BFS"),
             ("«¿se puede ir y volver?»", "componentes fuertemente conexas")]
    tabla(s, 50, 100, [650, 530], filas, cab=["en el enunciado…", "piensa en…"], size=21, rowh=52, hl=())
    s.bullets(60, 500, 1160, [
        "Cuidado con los índices: si los vértices vienen numerados desde 1, resta uno (o usa el parámetro primer del constructor).",
        "La recursión llega a V niveles: con V muy grande, mejor DFS iterativo o BFS.",
    ], size=19, gap=10)
    segs.append((s, "Y unas pistas para reconocer el algoritmo en el juez. Si piden el mínimo número de pasos, jugadas o pulsaciones: B F S. "
                    "Si preguntan si se puede llegar de A a B: D F S o B F S. Si una cosa debe hacerse antes que otra: grafo y orden topológico. "
                    "Si dicen imposible o dependencia circular: ciclo dirigido. Si hay estados con reglas de movimiento: grafo implícito y B F S. "
                    "Y dos cuidados: los índices, si empiezan en uno hay que restar uno, y la profundidad de la recursión, que puede llegar a uve niveles.", 0))

    # ---- ejercicios
    s = Slide("Los ejercicios del tema", CORNER)
    ex = [("EJ 05-1", "Transformación modular", "grafo de números 0…M-1, arista x → (a·x+b) mod M", "BFS desde S, parar en T"),
          ("EJ 05-2", "La máquina calculadora", "grafo de 10.000 números, 3 aristas por vértice", "BFS, camino más corto"),
          ("EJ 05-3", "Ordenando tareas", "tareas = vértices, «A antes que B» = arista", "DFS con 3 estados: ciclo / orden")]
    for i, (c, n, m, a) in enumerate(ex):
        y = 110 + i * 130
        s.box(50, y, 1180, 110, fill=(14, 28, 60))
        s.pill(70, y + 14, c, size=20)
        s.text((210, y + 28), n, size=26, bold=True, anchor="lm")
        s.text((70, y + 76), m, size=19, color="muted", anchor="lm")
        s.text((1210, y + 76), a, size=19, color="gold", bold=True, anchor="rm")
    s.box(50, 510, 1180, 90, fill=(24, 40, 70), border="purple")
    s.wrap(74, 526, 1130, "Más recursos en el repositorio: la herramienta interactiva «Digrafo» (web) y Digrafo_demo.cpp, que ejecuta todos estos algoritmos sobre los grafos de las transparencias.", size=19)
    segs.append((s, "Los tres ejercicios del tema encajan aquí. El cero cinco guion uno, transformación modular, es un grafo de números con un B F S desde el origen. "
                    "El cero cinco guion dos, la calculadora, es un B F S sobre un grafo de diez mil números. Y el cero cinco guion tres, ordenando tareas, usa un D F S con tres estados, que da el ciclo o el orden. "
                    "En el repositorio tienes también la herramienta interactiva de digrafos, y un programa de demostración que ejecuta todos estos algoritmos.", 0))

    segs.append((cierre(NOMBRE, [
        "Digrafo: aristas con sentido, guardadas solo en la lista del origen; inverso() las da la vuelta.",
        "DFS = alcanzabilidad · BFS = camino con menos aristas (dist y ant).",
        "Grafo implícito: los adyacentes se calculan al vuelo. EMT: BFS 6 paradas, DFS 2.032.",
        "Orden topológico = postorden inverso, solo en DAG · ciclo = vecino visitado Y apilado.",
        ("Extra: componentes fuertemente conexas con Kosaraju.", "purple"),
    ]), "Resumiendo. Un digrafo guarda cada arista solo en la lista de su origen, y el inverso las da la vuelta. "
        "El D F S sirve para la alcanzabilidad, y el B F S para el camino con menos aristas. En un grafo implícito los adyacentes se calculan al vuelo, y en la E M T el B F S da seis paradas y el D F S dos mil treinta y dos. "
        "El orden topológico es el postorden inverso, solo en un D A G, y un ciclo es un vecino visitado y además apilado. "
        "Y como extra, las componentes fuertemente conexas con Kosaraju. Con esto, tienes todo el tema.", 0))


def main(preview=False):
    segs, cap = [], {}
    for titulo, f in [("Introducción y conceptos", sec_intro), ("TAD Digrafo y representaciones", sec_tad),
                      ("Recorrido en profundidad (DFS)", sec_dfs), ("Recorrido en anchura (BFS)", sec_bfs),
                      ("Máquina calculadora y grafo implícito", sec_calc), ("Autobuses de la EMT: BFS contra DFS", sec_emt),
                      ("Ordenación topológica", sec_topo), ("Detección de ciclos", sec_ciclo),
                      ("Extra: componentes fuertemente conexas", sec_cfc), ("Resumen, pistas y ejercicios", sec_final)]:
        cap[len(segs)] = titulo
        f(segs)
    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-0_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-0_grafos_dirigidos_teoria.mp4", chapters=cap)
        print(f"05-0: {t:.0f}s ({t / 60:.1f} min)")


if __name__ == "__main__":
    main("--preview" in sys.argv)
