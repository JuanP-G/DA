"""Vídeo EJ 04-L · Peaje a la sombra"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../4-Grafos no dirigidos/EJ_04-L/EJ_04-L.cpp"
NOMBRE = "Peaje a la sombra"

# ejemplo 1 del enunciado: N=6, A=1, L=3, T=6 (vértices 0..5)
ENTRADA = [(1, 2), (2, 3), (2, 5), (3, 4), (5, 4), (5, 6), (4, 6)]
N = 6
E = [(a - 1, b - 1) for a, b in ENTRADA]
A, L, T = 0, 2, 5
LAB = {v: str(v + 1) for v in range(N)}
BASE = {0: (0, 0), 1: (1, 0), 2: (2, 0), 4: (1, 1), 3: (2, 1), 5: (1.5, 2)}   # (col, fila)


def pos(ox, oy, sx, sy):
    return {v: (ox + c * sx, oy + f * sy) for v, (c, f) in BASE.items()}


ROL = {A: ("blue", "node_t", None), L: ("green", "node_t", None), T: ("gold", "node_t", None)}
CAPA = ["gold", "blue", "purple", "green", "red"]

# líneas del código real
L_BFS = find_line(CPP, "void bfs(")
L_INI = [find_line(CPP, "dist[origen] = 0;"), find_line(CPP, "q.push(origen);")]
L_BUCLE_BFS = find_line(CPP, "for (int w : g.ady(v))")
L_NUEVO = find_line(CPP, "if (dist[w] == -1)")
L_SET = [find_line(CPP, "dist[w] = dist[v] + 1;"), find_line(CPP, "q.push(w);")]
L_TRES = find_line(CPP, "CaminosBFS dA")
L_INIT = find_line(CPP, "int mejor =")
L_FOR = find_line(CPP, "for (int m = 0;")
L_COSTE = find_line(CPP, "int coste =")
L_MIN = find_line(CPP, "mejor = min(")
L_OUT = find_line(CPP, "cout << mejor")
CODE_BFS = code_lines(CPP, find_line(CPP, "class CaminosBFS"), find_line(CPP, "};", L_BFS), maxc=78,
                      skip=[(find_line(CPP, "int distancia(") - 1, find_line(CPP, "vector<int> dist;") + 1)])
CODE_MAIN = code_lines(CPP, L_TRES, L_OUT - 2, maxc=78)


def ady(n, e):
    a = [[] for _ in range(n)]
    for v, w in e:
        a[v].append(w)
        a[w].append(v)
    return a


def bfs(n, e, s):
    a, d, q = ady(n, e), [-1] * n, deque([s])
    d[s] = 0
    while q:
        v = q.popleft()
        for w in a[v]:
            if d[w] == -1:
                d[w] = d[v] + 1
                q.append(w)
    return d


DA, DL, DT = bfs(N, E, A), bfs(N, E, L), bfs(N, E, T)
SUMA = [DA[m] + DL[m] + DT[m] for m in range(N)]
BEST = min(SUMA)
M_BEST = SUMA.index(BEST)
assert BEST == 4 and M_BEST == 1 and DA[T] + DL[T] == 5


def aristas(camino, color, g=7):
    return {(camino[i], camino[i + 1]): (color, g) for i in range(len(camino) - 1)}


def leyenda(s, x, y):
    x = s.pill(x, y, "Álex (1)", fill="blue", size=18)
    x = s.pill(x + 10, y, "Lucas (3)", fill="green", size=18)
    s.pill(x + 10, y, "trabajo (6)", fill="gold", size=18)


def slide_dist(titulo, origen, dist, nombre, cap):
    s = Slide(titulo)
    s.box(60, 90, 640, 440, f"distancia desde {nombre}")
    ns = {v: (CAPA[min(d, 4)], "node_t", None) for v, d in enumerate(dist)}
    ns[origen] = (ns[origen][0], "node_t", "text")
    s.graph(pos(190, 160, 210, 125), E, ns=ns, labels=LAB, r=27, under={v: str(d) for v, d in enumerate(dist)})
    s.box(730, 90, 490, 440, "vector de distancias")
    s.cells(750, 140, "vértice", list(range(1, N + 1)), idx=False, cw=48)
    s.cells(750, 200, {A: "dA", L: "dL", T: "dT"}[origen], dist, idx=False, cw=48,
            colors={v: "blue_d" for v in range(N)})
    s.bullets(750, 290, 440, ["Cada número es el mínimo de aristas hasta ese vértice.",
                              "Un BFS: O(N + C)."], size=20, gap=14)
    s.caption(cap, y=565)
    return s


def tabla(s, x, y, filas, resalta=None, hasta=None):
    cols = ["vértice", "dA", "dL", "dT", "suma"]
    cw = [110, 90, 90, 90, 110]
    xx = x
    for c, w in zip(cols, cw):
        s.text((xx + w / 2, y), c, size=20, color="muted", bold=True, anchor="ma")
        xx += w
    for i, fila in enumerate(filas):
        yy = y + 38 + i * 46
        if resalta is not None and i in resalta:
            s.d.rounded_rectangle((x - 8, yy - 4, x + sum(cw) + 8, yy + 38), 10, fill=C["gold_d"], outline=C["gold"], width=3)
        xx = x
        for k, (v, w) in enumerate(zip(fila, cw)):
            col = "gold" if (k == 4 and resalta is not None and i in resalta) else "text"
            s.text((xx + w / 2, yy + 2), str(v), size=24, color=col, bold=(k == 4), anchor="ma")
            xx += w


FILAS = [(m + 1, DA[m], DL[m], DT[m], SUMA[m]) for m in range(N)]


def slide_traza(k, m, mejor_antes, mejor, hl, cap, mostrados):
    s = Slide("Ejecución · ejemplo 1", f"paso {k + 1} de {N + 1}")
    s.code(24, 84, 740, 520, CODE_MAIN, hl=hl, title="resuelveCaso")
    s.box(784, 84, 472, 270, "ciudad")
    ns = dict(ROL)
    if m is not None:
        ns[m] = (ns.get(m, ("node",))[0], "node_t", "red")
    s.graph(pos(830, 150, 170, 95), E, ns=ns, labels=LAB, r=24, lsize=19)
    s.text((1236, 286), "mejor", size=17, color="muted", bold=True, anchor="ra")
    s.pill(1190, 306, str(mejor), fill="gold", size=22)
    s.box(784, 370, 472, 234, "vectores (vértices 1..6)")
    h = {m} if m is not None else None
    cb = {v: "blue_d" for v in range(N)}
    s.cells(800, 390, "dA", DA, first=1, hl=h, colors=cb, cw=46)
    s.cells(800, 444, "dL", DL, first=1, hl=h, colors=cb, cw=46)
    s.cells(800, 498, "dT", DT, first=1, hl=h, colors=cb, cw=46)
    suma = [SUMA[v] if v < mostrados else "·" for v in range(N)]
    s.cells(800, 552, "suma", suma, idx=False, hl=h, cw=46,
            colors={v: ("gold_d" if SUMA[v] == mejor else "green_d") for v in range(mostrados)})
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = []
    segs.append((portada(NOMBRE, "EJ 04-L"),
                 "Peaje a la sombra. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0))

    segs.append((ideas("El problema", [
        "Álex y Lucas viven en dos sitios distintos y trabajan en el mismo.",
        "Cada tramo de calle cuesta 1 euro. Si van juntos por un tramo, lo paga solo uno.",
        "Pueden quedar en un cruce y seguir juntos hasta el trabajo.",
        "Piden: el mínimo de euros que pagan entre los dos.",
    ]), "Álex y Lucas viven en sitios distintos y trabajan en el mismo. Cada tramo de calle cuesta un euro, "
        "pero si van juntos por un tramo, lo paga solo uno de los dos. "
        "Pueden quedar en un cruce y seguir juntos hasta el trabajo. Nos piden el mínimo de euros que pagan entre los dos.", 0))

    # ejemplo
    s = Slide("El ejemplo del enunciado")
    s.box(60, 90, 640, 440, "ciudad: 6 cruces, 7 calles")
    s.graph(pos(190, 160, 210, 125), E, ns=ROL, labels=LAB, r=27)
    leyenda(s, 730, 120)
    s.bullets(730, 190, 490, ["Cada vértice es un cruce y cada arista un tramo de calle.",
                              "Cada tramo cuesta 1: el coste es el número de aristas.",
                              "Álex sale del 1, Lucas del 3 y el trabajo es el 6."], size=22, gap=16)
    segs.append((s, "Este es el primer ejemplo. Cada vértice es un cruce y cada arista es un tramo de calle, que cuesta un euro. "
                    "Álex sale del cruce uno, Lucas del tres, y el trabajo está en el seis.", 0))

    s = Slide("Cada uno por su lado")
    s.box(60, 90, 640, 440, "caminos mínimos de cada uno")
    s.graph(pos(190, 160, 210, 125), E, ns=ROL, labels=LAB, r=27,
            es={**aristas([0, 1, 4, 5], "blue"), **aristas([2, 3, 5], "green")})
    s.bullets(730, 130, 490, [("Álex: 1 → 2 → 5 → 6   (3 tramos)", "blue"),
                              ("Lucas: 3 → 4 → 6   (2 tramos)", "green"),
                              ("Total: 5 euros", "gold")], size=22, gap=18)
    s.caption("Cada uno por su camino más corto no es la mejor opción.", y=565)
    segs.append((s, "Si cada uno va por su camino más corto, Álex hace tres tramos y Lucas dos: cinco euros en total.", 0))

    s = Slide("Quedando en el cruce 2")
    s.box(60, 90, 640, 440, "se encuentran en el 2")
    s.graph(pos(190, 160, 210, 125), E, ns={**ROL, 1: ("purple", "node_t", None)}, labels=LAB, r=27,
            es={**aristas([0, 1], "blue"), **aristas([2, 1], "green"), **aristas([1, 4, 5], "gold")})
    s.bullets(730, 130, 490, [("Álex: 1 → 2   (1)", "blue"), ("Lucas: 3 → 2   (1)", "green"),
                              ("Juntos: 2 → 5 → 6   (2, se paga una vez)", "gold"),
                              ("Total: 1 + 1 + 2 = 4 euros", "text")], size=22, gap=18)
    s.caption("Pagan 4: es el mínimo. El trozo común se cuenta una sola vez.", y=565)
    segs.append((s, "Pero si quedan en el cruce dos, Álex hace un tramo, Lucas otro, y desde allí van juntos por el cinco hasta el seis: "
                    "dos tramos que se pagan una sola vez. Uno más uno más dos, cuatro euros. Ese es el mínimo.", 0))

    # forma de Y
    s = Slide("La forma de los caminos: una Y")
    s.box(60, 90, 1160, 340)
    ym = {"A": (260, 190), "L": (260, 350), "m": (560, 270), "T": (1000, 270)}
    s.d.line((ym["A"], ym["m"]), fill=C["blue"], width=8)
    s.d.line((ym["L"], ym["m"]), fill=C["green"], width=8)
    s.d.line((ym["m"], ym["T"]), fill=C["gold"], width=8)
    for k, (fill, t) in {"A": ("blue", "Álex"), "L": ("green", "Lucas"), "m": ("purple", "m"), "T": ("gold", "trabajo")}.items():
        x, y = ym[k]
        s.d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=C[fill])
        s.text((x, y), t if k == "m" else "", size=24, color="node_t", bold=True, anchor="mm")
        s.text((x, y - 46) if k != "m" else (x + 50, y + 62), t if k != "m" else "cruce donde se encuentran", size=20, color="muted",
               bold=True, anchor="mm")
    s.text((400, 192), "dist(Álex, m)", size=20, color="blue", bold=True, anchor="mm")
    s.text((400, 350), "dist(Lucas, m)", size=20, color="green", bold=True, anchor="mm")
    s.text((780, 240), "dist(m, trabajo)", size=20, color="gold", bold=True, anchor="mm")
    s.wrap(80, 455, 1120, "Coste en m  =  dist(Álex, m) + dist(Lucas, m) + dist(m, trabajo)",
           size=25, color="gold", bold=True, center=True)
    s.caption("El trozo de m al trabajo lo hacen juntos, así que solo se suma una vez.", y=520)
    segs.append((s, "Los caminos siempre tienen forma de i griega. Álex y Lucas van cada uno por su lado hasta un cruce m, y desde m siguen juntos hasta el trabajo. "
                    "Si se encuentran en m, el coste es la distancia de Álex a m, más la de Lucas a m, más la de m al trabajo. "
                    "El último trozo se cuenta una sola vez porque lo hacen juntos.", 0))

    segs.append((ideas("¿Y qué cruce m elegimos?", [
        "Para un m fijo, lo mejor es ir por caminos MÍNIMOS: sus tres distancias.",
        "No sabemos cuál es el mejor m  ⇒  los probamos TODOS y nos quedamos con el menor.",
        "Necesitamos dist(Álex, m), dist(Lucas, m) y dist(trabajo, m) para todo m.",
        "Grafo sin pesos y distancias mínimas  ⇒  BFS desde cada uno de los tres.",
    ], note="Respuesta = mínimo sobre todos los vértices m de   dA[m] + dL[m] + dT[m]"),
        "¿Y qué cruce elegimos? Para un cruce fijo, lo mejor es ir por caminos mínimos, así que solo cuentan sus tres distancias. "
        "Como no sabemos cuál es el mejor, los probamos todos y nos quedamos con el menor. "
        "Necesitamos las distancias de Álex, de Lucas y del trabajo a todos los cruces. Es un grafo sin pesos, así que hacemos un B F S desde cada uno de los tres.", 0))

    segs.append((slide_dist("BFS desde Álex", A, DA, "Álex (1)", "El mismo BFS de siempre: por capas, a 1, a 2, a 3 aristas."),
                 "Primero, un B F S desde Álex. Los números de debajo de cada cruce son las distancias: el dos está a uno, el tres y el cinco a dos, y así.", 0))
    segs.append((slide_dist("BFS desde Lucas", L, DL, "Lucas (3)", "Otro BFS, esta vez con origen en el 3."),
                 "Después, otro B F S desde Lucas, con origen en el tres.", 0))
    segs.append((slide_dist("BFS desde el trabajo", T, DT, "el trabajo (6)", "Y un tercero desde el 6. El grafo no es dirigido: dist(m, 6) = dist(6, m)."),
                 "Y un tercero desde el trabajo. Como las calles son de doble sentido, la distancia de m al trabajo es la misma que la del trabajo a m.", 0))

    # tabla
    s = Slide("Probamos todos los cruces")
    s.box(60, 90, 640, 440)
    tabla(s, 100, 120, FILAS)
    s.box(730, 90, 490, 440, "cada fila: suma de las tres distancias")
    s.bullets(750, 140, 450, [f"Cruce {m + 1}:  {DA[m]} + {DL[m]} + {DT[m]} = {SUMA[m]}" for m in range(N)], size=22, gap=14)
    segs.append((s, "Ahora, para cada cruce sumamos las tres distancias. En el uno sale cinco. En el dos, uno más uno más dos: cuatro. En el tres, dos más cero más dos: también cuatro. Y en el cuatro, el cinco y el seis, cinco.", 0))
    s = Slide("El mínimo es 4")
    s.box(60, 90, 640, 440)
    tabla(s, 100, 120, FILAS, resalta={m for m in range(N) if SUMA[m] == BEST})
    s.box(730, 90, 490, 440, "ciudad")
    s.graph(pos(790, 190, 150, 95), E, ns={**ROL, 1: ("purple", "node_t", "text")}, labels=LAB, r=24,
            es={**aristas([0, 1], "blue", 6), **aristas([2, 1], "green", 6), **aristas([1, 4, 5], "gold", 6)})
    s.caption("Mínimo 4, en el cruce 2 (y también en el 3: Álex pasa por casa de Lucas y siguen juntos).", y=565)
    segs.append((s, "La menor suma es cuatro, y sale en el cruce dos y en el tres. En el tres, Álex pasa por la casa de Lucas y siguen juntos. Esa es la respuesta: cuatro euros.", 0))

    # caso 2
    P2 = {0: (200, 250), 1: (440, 250), 2: (680, 250), 3: (920, 250)}
    E2 = [(0, 1), (1, 2), (2, 3)]
    A2, L2, T2 = 3, 0, 2
    d2a, d2l, d2t = bfs(4, E2, A2), bfs(4, E2, L2), bfs(4, E2, T2)
    sm2 = [d2a[i] + d2l[i] + d2t[i] for i in range(4)]
    assert min(sm2) == 3 and sm2.index(3) == 2
    s = Slide("Segundo ejemplo: a veces no hace falta juntarse")
    s.box(60, 90, 1160, 270)
    s.graph(P2, E2, ns={3: ("blue", "node_t", None), 0: ("green", "node_t", None), 2: ("gold", "node_t", "text")},
            labels={i: str(i + 1) for i in range(4)}, r=30, es={**aristas([3, 2], "blue", 7), **aristas([0, 1, 2], "green", 7)})
    s.text((920, 210), "Álex", size=20, color="blue", bold=True, anchor="mm")
    s.text((200, 210), "Lucas", size=20, color="green", bold=True, anchor="mm")
    s.text((680, 210), "trabajo", size=20, color="gold", bold=True, anchor="mm")
    s.box(60, 380, 1160, 190)
    s.text((90, 400), "cruce m", size=19, color="muted", bold=True)
    for i in range(4):
        x = 330 + i * 230
        s.text((x, 400), str(i + 1), size=22, bold=True, anchor="ma", color="gold" if i == 2 else "text")
        s.text((x, 440), f"{d2a[i]}+{d2l[i]}+{d2t[i]} = {sm2[i]}", size=22, anchor="ma", color="gold" if i == 2 else "text", bold=(i == 2))
    s.text((90, 440), "dA+dL+dT", size=19, color="muted", bold=True)
    s.wrap(90, 500, 1100, "El mínimo sale en m = 3, que es el propio trabajo: cada uno va por su lado hasta allí. Total 1 + 2 = 3.", size=22, color="text")
    segs.append((s, "En el segundo ejemplo, Álex sale del cuatro, Lucas del uno y el trabajo está en el tres. Probamos todos los cruces y el mínimo sale en el tres, "
                    "que es el propio trabajo: Álex hace un tramo, Lucas hace dos, y no se juntan hasta llegar. Tres euros. "
                    "No hay que tratar este caso aparte: el cruce m puede ser el trabajo, o la casa de cualquiera de los dos.", 0))

    # código (dos diapositivas)
    s = Slide("El código · BFS", "EJ_04-L.cpp")
    s.code(24, 84, 740, 520, CODE_BFS, hl={L_NUEVO} | set(L_SET), title="class CaminosBFS")
    s.box(784, 84, 472, 520, "qué hace")
    s.bullets(804, 130, 430, ["Un objeto guarda las distancias desde UN origen.",
                              "dist[v] = -1 significa: aún sin visitar.",
                              "Cada vecino nuevo: dist + 1 y a la cola.",
                              "Lo usamos tres veces: Álex, Lucas y el trabajo."], size=20, gap=16)
    segs.append((s, "En el código, la clase CaminosBFS hace un B F S desde un origen y guarda las distancias. "
                    "Vale menos uno para los cruces sin visitar, y cada vecino nuevo recibe la distancia más uno y entra en la cola. "
                    "Es el mismo B F S de siempre, y lo vamos a usar tres veces.", 0))

    s = Slide("El código · resuelveCaso", "EJ_04-L.cpp")
    s.code(24, 84, 740, 360, CODE_MAIN, hl={L_TRES, L_INIT, L_COSTE, L_MIN}, title="resuelveCaso")
    s.box(784, 84, 472, 520, "qué hace")
    s.bullets(804, 130, 430, ["dA, dL y dT: un BFS desde cada uno.",
                              "mejor empieza con el caso «cada uno solo» (m = trabajo).",
                              "Para cada vértice m: coste = dA + dL + dT.",
                              "Nos quedamos con el menor."], size=20, gap=16)
    s.box(24, 464, 740, 140, fill=(30, 52, 90), border="gold")
    s.wrap(44, 484, 700, "Los casos «no nos juntamos» o «nos juntamos en la casa de uno» no se tratan aparte: son los m = trabajo, m = casa de Álex o m = casa de Lucas.", size=21)
    segs.append((s, "En resuelve caso creamos tres objetos: d A, desde Álex, d L, desde Lucas, y d T, desde el trabajo. "
                    "Empezamos con mejor igual al caso en que cada uno va solo, y después recorremos todos los cruces m: "
                    "el coste es la suma de las tres distancias, y nos quedamos con el menor. "
                    "Los casos en que no se juntan, o se juntan en la casa de uno, no hay que tratarlos aparte, porque son valores de m.", 0))

    # traza
    mejor = DA[T] + DL[T]
    segs.append((slide_traza(0, None, mejor, mejor, {L_TRES, L_INIT},
                             f"Tres BFS hechos. mejor = dA[6] + dL[6] = {mejor} (cada uno solo)", 0),
                 f"Con los tres B F S hechos, empezamos con mejor igual a la distancia de Álex al trabajo más la de Lucas: {mejor}.", 0))
    for m in range(N):
        antes = mejor
        mejor = min(mejor, SUMA[m])
        cap = f"m = {m + 1}: {DA[m]} + {DL[m]} + {DT[m]} = {SUMA[m]}"
        cap += f"  →  mejor baja a {mejor}" if mejor < antes else f"  →  mejor sigue en {mejor}"
        nar = f"Cruce {m + 1}: {DA[m]} más {DL[m]} más {DT[m]}, {SUMA[m]}. "
        nar += f"Es menor que {antes}: mejor pasa a valer {mejor}." if mejor < antes else f"No mejora el {mejor}."
        segs.append((slide_traza(m + 1, m, antes, mejor, {L_FOR, L_COSTE, L_MIN}, cap, m + 1), nar, 0))

    segs.append((ideas("Resultado y coste", [
        "Ejemplo 1: el mejor cruce es el 2  ⇒  4",
        "Ejemplo 2: el mejor cruce es el trabajo  ⇒  3",
        "Tres BFS + un recorrido de los vértices: O(N + C) por caso.",
        "Con N ≤ 20.000 y C ≤ 200.000 va sobrado.",
        ("Las sumas caben en un int (como mucho 3·N).", "muted"),
    ]), "Al terminar, mejor vale cuatro, que es la respuesta del primer ejemplo, y tres en el segundo. "
        "El coste son tres recorridos en anchura más una pasada por los vértices: lineal en el tamaño del grafo.", 0))

    segs.append((cierre(NOMBRE, [
        "Los caminos forman una Y: cada uno hasta m, y juntos de m al trabajo.",
        "Coste con encuentro en m  =  dA[m] + dL[m] + dT[m].",
        "Tres BFS (desde Álex, Lucas y el trabajo) dan esas distancias.",
        "Respuesta = mínimo sobre todos los m.   Coste: O(N + C).",
    ]), "Resumiendo: los caminos forman una i griega. Si se encuentran en m, el coste es la suma de las tres distancias. "
        "Con tres B F S las calculamos todas, y la respuesta es el mínimo sobre todos los cruces.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-L_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-L_peaje_a_la_sombra.mp4")
        print(f"04-L: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
