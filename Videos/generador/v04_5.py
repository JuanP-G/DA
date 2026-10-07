"""Vídeo EJ 04-5 · ¡Las noticias vuelan!"""
import sys
import math
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line

CPP = "../../EJ_04-5/EJ_04-5.cpp"
NOMBRE = "¡Las noticias vuelan!"

N = 7
GRUPOS = [[2, 5, 4], [], [1, 2], [1], [6, 7]]
LAB = {v: str(v + 1) for v in range(N)}
P = {0: (740, 160), 1: (870, 230), 4: (1000, 160), 3: (1000, 310), 2: (740, 330), 5: (1120, 170), 6: (1180, 310)}

L_RD0 = find_line(CPP, "int k; cin >> k;")
L_EMPTY = find_line(CPP, "if (k == 0) continue;")
L_PRIM = find_line(CPP, "int primero; cin >> primero;")
L_STAR = find_line(CPP, "g.ponArista(primero - 1, otro - 1);")
L_NEWC = find_line(CPP, "if (comp[v] == -1) {")
L_PUSH = find_line(CPP, "tam.push_back(bfs(g, v, c));")
L_BFS = find_line(CPP, "int bfs(")
L_B0 = [find_line(CPP, "comp[origen] = c;"), find_line(CPP, "q.push(origen);"), find_line(CPP, "int cuantos = 1;")]
L_POP = find_line(CPP, "int v = q.front(); q.pop();", L_BFS)
L_DESC = [find_line(CPP, "if (comp[w] == -1) {", L_BFS), find_line(CPP, "comp[w] = c;"), find_line(CPP, "++cuantos;"), find_line(CPP, "q.push(w);", L_BFS)]
L_RET = find_line(CPP, "return cuantos;")
L_OUT = find_line(CPP, "cout << tc.tamano(v)")
CODE_LEER = code_lines(CPP, find_line(CPP, "Grafo g(usuarios);"), find_line(CPP, "}", L_STAR + 1), maxc=54)
CODE_CONS = code_lines(CPP, find_line(CPP, "TamComponentes(Grafo const& g)"), find_line(CPP, "int tamano(int v)"))
CODE_BFS = code_lines(CPP, L_BFS, find_line(CPP, "return cuantos;") + 1)
COMP_COL = ["blue", "purple", "green", "gold"]


def aristas():
    E = []
    for g in GRUPOS:
        for o in g[1:]:
            E.append((g[0] - 1, o - 1))
    return E


E = aristas()


def traza():
    a = [[] for _ in range(N)]
    for v, w in E:
        a[v].append(w)
        a[w].append(v)
    comp, tam = [-1] * N, []
    pasos = []
    for v in range(N):
        if comp[v] == -1:
            c = len(tam)
            q = deque([v])
            comp[v] = c
            cu = 1
            pasos.append(("nueva", v, None, comp[:], list(q), tam[:], cu))
            while q:
                x = q.popleft()
                pasos.append(("saca", x, None, comp[:], list(q), tam[:], cu))
                for w in a[x]:
                    if comp[w] == -1:
                        comp[w] = c
                        cu += 1
                        q.append(w)
                        pasos.append(("descubre", x, w, comp[:], list(q), tam[:], cu))
            tam.append(cu)
            pasos.append(("fin", v, None, comp[:], [], tam[:], cu))
    return pasos, comp, tam


def slide_paso(k, n, tipo, v, w, comp, q, tam, cu, hl, cap):
    s = Slide("Ejecución · componentes con BFS", f"paso {k} de {n}")
    if tipo in ("nueva", "fin"):
        s.code(24, 84, 610, 520, CODE_CONS, hl=hl, title="TamComponentes (constructor)", size=17)
    else:
        s.code(24, 84, 610, 520, CODE_BFS, hl=hl, title="TamComponentes::bfs", size=17)
    s.box(652, 84, 604, 330, "amigos (aristas en estrella)")
    ns = {u: (COMP_COL[c], "node_t", None) for u, c in enumerate(comp) if c != -1}
    if v is not None and tipo != "fin":
        ns[v] = (ns.get(v, ("node",))[0], "node_t", "text")
    es = {(v, w): ("gold", 6)} if w is not None else None
    s.graph(P, E, ns=ns, es=es, labels=LAB)
    s.box(652, 430, 604, 174, "estado")
    s.cells(672, 464, "comp", [c if c != -1 else "·" for c in comp], first=1,
            colors={u: {0: "blue_d", 1: "purple_d", 2: "green_d"}.get(c, "blue_d") for u, c in enumerate(comp) if c != -1},
            hl={w} if w is not None else None, cw=40)
    s.queue_row(672, 520, "cola", [u + 1 for u in q])
    s.text((672, 570), "tam", size=17, color="muted", bold=True)
    x = 782
    for c, t in enumerate(tam):
        x = s.pill(x, 564, f"c{c}: {t}", fill=COMP_COL[c], size=15) + 8
    if tipo != "fin":
        s.text((1080, 570), "cuantos", size=17, color="muted", bold=True)
        s.pill(1170, 564, str(cu), fill="gold", size=15)
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-5"),
             "Las noticias vuelan. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    segs.append((ideas("El problema", [
        "Usuarios en grupos de WhatsApp. Dos usuarios son amigos si comparten algún grupo.",
        "Una noticia se cuenta a todos los amigos, que la cuentan a los suyos... hasta que no queda nadie por enterarse.",
        "Para CADA usuario: ¿a cuántos llegaría la noticia si empezara en él?",
        ("N y M hasta 100.000, y la suma de tamaños de grupo hasta 1.000.000.", "muted"),
    ]), "Tenemos usuarios repartidos en grupos de WhatsApp, y dos usuarios son amigos si comparten algún grupo. "
        "Una noticia se va contando de amigo en amigo hasta que no queda nadie por enterarse. "
        "Para cada usuario, nos piden a cuántos llegaría la noticia si empezara en él.", 0))

    s = Slide("Cómo se plantea")
    s.box(60, 90, 560, 380, "caso 1: grupos {2,5,4} {} {1,2} {1} {6,7}")
    s.graph({u: (x - 640, y + 30) for u, (x, y) in P.items()}, [(0, 1), (1, 4), (1, 3), (4, 3), (5, 6)], labels=LAB,
            ns={0: ("blue", "node_t", None), 1: ("blue", "node_t", None), 3: ("blue", "node_t", None), 4: ("blue", "node_t", None),
                2: ("purple", "node_t", None), 5: ("green", "node_t", None), 6: ("green", "node_t", None)})
    s.bullets(660, 110, 560, [
        "Usuario → vértice.  Comparten grupo → arista.",
        "La noticia llega exactamente a la COMPONENTE CONEXA del que empieza.",
        ("Respuesta de i = tamaño de la componente de i.", "gold"),
        "Aquí: {1,2,4,5} → 4,  {3} → 1,  {6,7} → 2",
        "Salida: 4 4 1 4 4 2 2",
    ], size=22)
    segs.append((s, "Si cada usuario es un vértice y unimos a los que comparten grupo, la noticia llega exactamente a la componente conexa del que la empieza, "
                    "ni más ni menos. Así que la respuesta de cada usuario es el tamaño de su componente conexa.", 0))
    segs.append((s, "En el ejemplo hay tres componentes: uno, dos, cuatro y cinco, con cuatro usuarios; el tres solo; y seis y siete. "
                    "Fíjate en que uno y cinco no comparten grupo, pero la noticia les llega igual a través del dos.", 0))

    # problema 1: aristas
    s = Slide("Problema 1 · demasiadas aristas")
    cx1, cx2, cy, R = 330, 950, 290, 120
    pa = {i: (cx1 + R * math.cos(2 * math.pi * i / 7 - math.pi / 2), cy + R * math.sin(2 * math.pi * i / 7 - math.pi / 2)) for i in range(7)}
    s.box(60, 90, 540, 400, "todos con todos: k(k-1)/2")
    s.graph(pa, [(i, j) for i in range(7) for j in range(i + 1, 7)], labels={i: f"u{i + 1}" for i in range(7)},
            es={(i, j): ("red", 2) for i in range(7) for j in range(i + 1, 7)}, r=21)
    pb = {i: (cx2 + R * math.cos(2 * math.pi * i / 7 - math.pi / 2), cy + R * math.sin(2 * math.pi * i / 7 - math.pi / 2)) for i in range(7)}
    s.box(680, 90, 540, 400, "todos con el primero: k-1")
    s.graph(pb, [(0, i) for i in range(1, 7)], labels={i: f"u{i + 1}" for i in range(7)},
            ns={0: ("gold", "node_t", None)}, es={(0, i): ("green", 3) for i in range(1, 7)}, r=21)
    s.caption("Un grupo de 100.000: ~5.000 millones de aristas  vs  99.999", y=515)
    s.caption("Solo importa QUIÉN está conectado (no a qué distancia): la estrella basta", y=560)
    segs.append((s, "Primer problema: si unimos a todos los miembros de un grupo entre sí, un grupo de ka usuarios da ka por ka menos uno partido por dos aristas. "
                    "Con un grupo de cien mil son unos cinco mil millones. Imposible.", 0))
    segs.append((s, "Pero aquí solo importa quién está conectado con quién, no a qué distancia. Así que basta con unir a todos con el primero del grupo, "
                    "como una estrella: ka menos una aristas, y el grupo sigue en una sola componente. "
                    "En los números de Bacon esto no servía, porque allí sí importaban las distancias.", 0))

    # lectura del grafo
    acum = []
    for gi, g in enumerate(GRUPOS):
        nuevas = [(g[0] - 1, o - 1) for o in g[1:]]
        acum += nuevas
        s = Slide("Construir el grafo", f"grupo {gi + 1} de {len(GRUPOS)}")
        hl = {L_RD0, L_EMPTY} if not g else ({L_PRIM, L_STAR} if len(g) > 1 else {L_PRIM})
        s.code(24, 84, 610, 360, CODE_LEER, hl=hl, title="resuelveCaso (lectura)", size=17)
        s.box(652, 84, 604, 360, "grafo")
        s.graph(P, acum, labels=LAB, es={e: ("green", 6) for e in nuevas},
                ns={g[0] - 1: ("gold", "node_t", None)} if g else None)
        if not g:
            cap, nar = "Grupo vacío: no une a nadie", "El segundo grupo está vacío: no pone ninguna arista."
        elif len(g) == 1:
            cap, nar = f"Grupo {{{g[0]}}}: un solo usuario, ninguna arista", f"El grupo con solo el {g[0]} tampoco pone ninguna arista."
        else:
            cap = f"Grupo {{{', '.join(map(str, g))}}}: aristas " + ", ".join(f"{g[0]}-{o}" for o in g[1:])
            nar = f"Grupo {', '.join(map(str, g))}: unimos al primero, el {g[0]}, con " + " y ".join(f"el {o}" for o in g[1:]) + "."
        s.caption(cap, y=480)
        segs.append((s, nar, 0))

    segs.append((ideas("Problema 2 · responder a todos", [
        "Un recorrido POR USUARIO sería cuadrático (cada uno recorre su componente entera).",
        "Mejor: UN recorrido POR COMPONENTE.",
        "comp[v] = número de la componente de v.   tam[c] = tamaño de la componente c.",
        ("Respuesta de v = tam[comp[v]].", "gold"),
        "Y con BFS iterativo: un dfs recursivo de 100.000 niveles podría desbordar la pila.",
    ]), "Segundo problema: si hacemos un recorrido por cada usuario, repetimos el mismo trabajo muchas veces y el coste es cuadrático. "
        "En su lugar hacemos un recorrido por componente: guardamos en comp el número de componente de cada usuario y en tam el tamaño de cada componente. "
        "La respuesta de cada usuario es el tamaño de su componente.", 0))
    segs.append((segs[-1][0], "Además usamos un B F S con cola en lugar de un D F S recursivo, porque una componente puede tener cien mil usuarios "
                              "y una recursión tan profunda podría desbordar la pila. Para contar una componente da igual el orden.", 0))

    pasos, comp, tam = traza()
    n = len(pasos)
    for k, (tipo, v, w, cp, q, tm, cu) in enumerate(pasos, 1):
        c = cp[v]
        if tipo == "nueva":
            hl, cap = {L_NEWC, L_PUSH}, f"{v + 1} no tiene componente: empieza la componente {c}"
            nar = f"El usuario {v + 1} todavía no tiene componente: empieza la componente {c}, y lanzamos un B F S desde él."
        elif tipo == "saca":
            hl, cap = {L_POP}, f"Sacamos el {v + 1} de la cola"
            nar = f"Sacamos el {v + 1} de la cola y miramos sus vecinos."
        elif tipo == "descubre":
            hl, cap = set(L_DESC), f"{w + 1} es nuevo: comp[{w + 1}] = {c}, cuantos = {cu}"
            nar = f"El {w + 1} es nuevo: pertenece a la componente {c}. Ya van {cu}."
        else:
            hl, cap = {L_RET, L_PUSH}, f"Cola vacía: la componente {c} tiene {tm[-1]} usuario{'s' if tm[-1] > 1 else ''}"
            nar = f"La cola se ha vaciado: la componente {c} tiene {tm[-1]}."
        segs.append((slide_paso(k, n, tipo, v, w, cp, q, tm, cu, hl, cap), nar, 0))

    s = Slide("Salida")
    s.graph({u: (x - 300, y + 40) for u, (x, y) in P.items()}, E, labels=LAB,
            ns={u: (COMP_COL[c], "node_t", None) for u, c in enumerate(comp)})
    s.cells(330, 470, "tam[comp[v]]", [tam[comp[u]] for u in range(N)], first=1, cw=56, size=22)
    s.caption("4 4 1 4 4 2 2", y=560)
    segs.append((s, "Para escribir la salida, la respuesta de cada usuario es el tamaño de su componente: cuatro, cuatro, uno, cuatro, cuatro, dos, dos.", 0))

    segs.append((cierre(NOMBRE, [
        "La noticia llega a la componente conexa: respuesta = su tamaño.",
        "Aristas en estrella (k-1 por grupo): solo importa la conexión, no la distancia.",
        "Un recorrido por componente: comp[v] y tam[c]; respuesta tam[comp[v]].",
        "BFS iterativo para no desbordar la pila con componentes enormes.",
        "Coste: O(N + suma de tamaños de grupo): lineal en la entrada.",
    ]), "Resumiendo: la respuesta de cada usuario es el tamaño de su componente conexa. Para no tener demasiadas aristas unimos cada grupo en estrella, "
        "recorremos cada componente una sola vez con un B F S, y respondemos con el tamaño de la componente de cada usuario. El coste es lineal en el tamaño de la entrada.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-5_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-5_las_noticias_vuelan.mp4")
        print(f"04-5: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
