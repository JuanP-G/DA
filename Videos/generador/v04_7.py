"""Vídeo EJ 04-7 · Grafo bipartito"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line

CPP = "../../4-Grafos no dirigidos/EJ_04-7/EJ_04-7.cpp"
NOMBRE = "Grafo bipartito"

P1 = {0: (820, 140), 2: (960, 140), 1: (735, 235), 6: (1095, 235), 4: (950, 270), 5: (1050, 360), 3: (850, 365)}
E1 = [(0, 2), (0, 4), (1, 6), (1, 3), (2, 6), (2, 5), (4, 6), (4, 5), (4, 3)]
P2 = {0: (820, 140), 2: (980, 140), 4: (1110, 235), 3: (950, 265), 1: (790, 345), 5: (1030, 370)}
E2 = [(0, 2), (0, 3), (2, 3), (2, 4), (4, 3), (3, 1), (3, 5), (1, 5)]

L_NEW = find_line(CPP, "if (!visit[v]) {")
L_C0 = find_line(CPP, "color[v] = false;")
L_DFS = find_line(CPP, "void dfs(")
L_VIS = find_line(CPP, "visit[v] = true;", L_DFS)
L_STOP = find_line(CPP, "if (!bipar) return;")
L_NV = find_line(CPP, "if (!visit[w]) {", L_DFS)
L_COL = find_line(CPP, "color[w] = !color[v];")
L_REC = find_line(CPP, "dfs(g, w);", L_DFS)
L_CHK = find_line(CPP, "else if (color[w] == color[v])")
CODE = code_lines(CPP, find_line(CPP, "class Bipartito"), find_line(CPP, "};", L_DFS),
                  skip=[(find_line(CPP, "bool esBipartito"), find_line(CPP, "bool bipar;"))])
COL = {False: "blue", True: "purple"}
NOMCOL = {False: "azul", True: "morado"}
PLURAL = {False: "azules", True: "morados"}


def traza(V, edges):
    a = [[] for _ in range(V)]
    for v, w in edges:
        a[v].append(w)
        a[w].append(v)
    visit, color = [False] * V, [False] * V
    st = dict(bipar=True)
    pasos, pila = [], []

    def snap(tipo, v, w=None):
        pasos.append((tipo, v, w, visit[:], color[:], pila[:], st["bipar"]))

    def dfs(v):
        visit[v] = True
        pila.append(v)
        snap("entra", v)
        for w in a[v]:
            if not st["bipar"]:
                break
            if not visit[w]:
                color[w] = not color[v]
                dfs(w)
            elif color[w] == color[v]:
                st["bipar"] = False
                snap("choque", v, w)
            else:
                snap("bien", v, w)
        pila.pop()

    for v in range(V):
        if not st["bipar"]:
            break
        if not visit[v]:
            color[v] = False
            snap("nueva", v)
            dfs(v)
    return pasos, st["bipar"]


def slide_paso(caso, pos, edges, k, n, tipo, v, w, visit, color, pila, bipar, hl, cap):
    s = Slide(f"Ejecución · Caso {caso}", f"paso {k} de {n}")
    s.code(24, 84, 610, 520, CODE, hl=hl, title="class Bipartito")
    s.box(652, 84, 604, 330, "grafo")
    ns = {u: (COL[color[u]], "node_t", None) for u in range(len(visit)) if visit[u]}
    if v is not None:
        ns[v] = (ns.get(v, ("node",))[0], "node_t", "gold")
    es = {}
    for i in range(1, len(pila)):
        es[(pila[i - 1], pila[i])] = ("gold", 5)
    if tipo == "choque":
        es[(v, w)] = ("red", 7)
    elif tipo == "bien":
        es[(v, w)] = ("green", 5)
    s.graph(pos, edges, ns=ns, es=es)
    s.box(652, 430, 604, 174, "estado")
    V = len(visit)
    s.cells(672, 462, "color", [("A" if not color[u] else "M") if visit[u] else "·" for u in range(V)],
            colors={u: ("blue_d" if not color[u] else "purple_d") for u in range(V) if visit[u]},
            hl={v} if v is not None else None)
    s.text((672, 540), "bipar", size=17, color="muted", bold=True)
    s.pill(750, 532, "true" if bipar else "false", fill="green" if bipar else "red")
    s.text((850, 540), "A = azul, M = morado", size=16, color="muted")
    s.caption(cap, y=628)
    return s


def ejecucion(caso, pos, edges, V, solo_entradas=False):
    pasos, res = traza(V, edges)
    if solo_entradas:
        pasos = [p for p in pasos if p[0] in ("nueva", "entra", "choque")]
    n = len(pasos)
    segs = []
    for k, (tipo, v, w, visit, color, pila, bipar) in enumerate(pasos, 1):
        if tipo == "nueva":
            hl, cap = {L_NEW, L_C0}, f"{v} no está visitado: empieza componente, color {NOMCOL[False]}"
            nar = f"El {v} no está visitado: empieza una componente y le damos el color azul."
        elif tipo == "entra":
            if len(pila) == 1:
                hl, cap = {L_VIS}, f"dfs({v}): lo marcamos"
                nar = f"Entramos en el {v}."
            else:
                p = pila[-2]
                hl = {L_COL, L_REC}
                cap = f"{v} es vecino nuevo de {p} ({NOMCOL[color[p]]}) → {v} va de {NOMCOL[color[v]]}"
                nar = f"El {v} es un vecino nuevo del {p}, así que lleva el color contrario: {NOMCOL[color[v]]}."
        elif tipo == "bien":
            hl, cap = {L_CHK}, f"{w} ya visitado y de color distinto a {v}: la arista {v}-{w} está bien"
            nar = f"El {w} ya tiene color, y es distinto al del {v}. Esa arista está bien."
        else:
            hl = {L_CHK}
            cap = f"¡{v} y {w} son los dos {PLURAL[color[v]]}! bipar = false"
            nar = f"El {w} ya tiene color y es el mismo que el del {v}: los dos son {PLURAL[color[v]]}. Conflicto: no es bipartito."
        segs.append((slide_paso(caso, pos, edges, k, n, tipo, v, w, visit, color, pila, bipar, hl, cap), nar, 0))
    return segs, res, pasos[-1]


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-7"),
             "Grafo bipartito. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    s = Slide("El problema")
    s.box(60, 90, 560, 380, "caso 1: SI")
    s.box(660, 90, 560, 380, "caso 2: NO")
    s.graph({v: (x - 640, y + 20) for v, (x, y) in P1.items()}, E1,
            ns={v: ("blue" if v in (0, 3, 5, 6) else "purple", "node_t", None) for v in P1})
    s.graph({v: (x - 50, y + 20) for v, (x, y) in P2.items()}, E2,
            es={(0, 2): ("red", 5), (2, 3): ("red", 5), (0, 3): ("red", 5)})
    s.caption("Bipartito: se puede pintar con 2 colores sin que una arista una dos del mismo color", y=505)
    s.caption("En el caso 2, el triángulo 0-2-3 lo hace imposible", y=550)
    segs.append((s, "Un grafo es bipartito si podemos pintar sus vértices con dos colores, de forma que ninguna arista una dos vértices del mismo color.", 0))
    segs.append((s, "El primero lo es: azules a un lado, morados al otro. El segundo no: el cero, el dos y el tres están unidos entre sí, "
                    "y con solo dos colores dos de ellos tendrían que repetir.", 0))

    segs.append((ideas("La idea clave", [
        "No hay que probar combinaciones de colores.",
        "El color de un vértice OBLIGA el de sus vecinos: si v es azul, todos sus vecinos son morados.",
        "Pinto el primero de cualquier color y hago un dfs: cada vecino nuevo, el color contrario.",
        "Si encuentro un vecino YA pintado del MISMO color → conflicto → NO es bipartito.",
    ], note="Cada componente se colorea por separado: hay que lanzar el dfs desde cada vértice no visitado."),
        "La idea clave es que no hay que probar combinaciones. El color de un vértice obliga el de sus vecinos: si uno es azul, "
        "todos sus vecinos tienen que ser morados. Así que pinto el primero de cualquier color y hago un D F S en el que cada vecino nuevo "
        "recibe el color contrario.", 0))
    segs.append((segs[-1][0], "Si en algún momento encuentro un vecino que ya estaba pintado y tiene el mismo color, hay conflicto y el grafo no es bipartito. "
                              "Y como el grafo puede no ser conexo, hay que lanzar el recorrido desde cada vértice sin visitar.", 0))

    segs.append((ideas("¿Por qué es correcto?", [
        "Dentro de una componente, el color del primer vértice decide TODOS los demás.",
        "Solo hay dos coloreados posibles, y uno es el otro con los colores cambiados.",
        "Si el que fuerza el dfs falla, cualquier otro falla también.",
        ("El conflicto aparece justo cuando hay un ciclo de longitud IMPAR.", "gold"),
    ]), "¿Por qué es correcto? Dentro de una componente, el color del primer vértice decide todos los demás. "
        "Solo hay dos coloreados posibles y uno es el otro con los colores intercambiados, así que si el que fuerza el recorrido falla, "
        "no hay ninguno que funcione. El conflicto aparece exactamente cuando hay un ciclo de longitud impar.", 0))

    s = Slide("El código", "EJ_04-7.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_C0, L_COL, L_CHK, L_STOP}, title="class Bipartito")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, [
        "visit: ya tiene color.  color: false / true.",
        "Vecino nuevo → color contrario y dfs.",
        "Vecino visitado del mismo color → bipar = false.",
        "En cuanto bipar es false se deja de recorrer.",
    ], size=20, gap=16)
    segs.append((s, "En el código hay dos vectores: visit dice si un vértice ya tiene color, y color guarda cuál. "
                    "A un vecino nuevo se le pone el color contrario y se sigue el recorrido. Si un vecino ya visitado tiene el mismo color, "
                    "bipar pasa a falso, y a partir de ahí se deja de recorrer porque la respuesta ya es no.", 0))

    segs.append((ideas("Ejecución · Caso 2", ["6 vértices, 8 aristas.", "Esperamos NO: hay un triángulo 0-2-3."]),
                 "Veamos primero el caso que no es bipartito.", 0))
    e2, r2, _ = ejecucion(2, P2, E2, 6)
    segs += e2
    segs.append((ideas("Caso 2 · resultado", ["bipar = false  ⇒  se escribe NO",
                                              "El ciclo 0-2-3 tiene 3 aristas (impar): imposible con 2 colores."]),
                 "Resultado: no es bipartito. El ciclo cero, dos, tres tiene tres aristas, un número impar, y con dos colores es imposible.", 0))

    segs.append((ideas("Ejecución · Caso 1", ["7 vértices, 9 aristas.", "Solo enseñamos cuándo se pinta cada vértice."]),
                 "Ahora el primer caso. Para no alargarlo, solo vemos cuándo se pinta cada vértice.", 0))
    e1, r1, _ = ejecucion(1, P1, E1, 7, solo_entradas=True)
    segs += e1
    s = Slide("Caso 1 · resultado")
    s.graph({v: (x - 320, y + 40) for v, (x, y) in P1.items()}, E1,
            ns={v: ("blue" if v in (0, 3, 5, 6) else "purple", "node_t", None) for v in P1},
            es={e: ("green", 4) for e in E1})
    s.caption("Todas las aristas unen un azul con un morado  ⇒  SI", y=480)
    s.caption("Azules {0,3,5,6}   ·   Morados {1,2,4}", y=525)
    segs.append((s, "Todas las aristas unen un azul con un morado, así que es bipartito. Los dos conjuntos son cero, tres, cinco y seis por un lado, "
                    "y uno, dos y cuatro por el otro.", 0))

    segs.append((cierre(NOMBRE, [
        "El color de un vértice obliga el de sus vecinos: un dfs que va alternando colores.",
        "Vecino ya pintado del mismo color ⇒ NO (hay un ciclo impar).",
        "Lanzar el dfs desde cada vértice no visitado (el grafo puede no ser conexo).",
        "Coste: O(V + A) por caso.",
    ]), "Resumiendo: hacemos un D F S que va alternando colores. Si un vecino ya pintado tiene el mismo color, no es bipartito. "
        "No hay que olvidar lanzar el recorrido en todas las componentes. El coste es lineal en vértices más aristas.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-7_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-7_grafo_bipartito.mp4")
        print(f"04-7: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
