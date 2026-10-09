"""Vídeo EJ 05-3 · Ordenando tareas"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../5-Grafos dirigidos/EJ_05-3/EJ_05-3.cpp"
NOMBRE = "Ordenando tareas"
TEMA = "Tema 5 · Grafos dirigidos"

# ejemplo 1 del enunciado (tareas 1..7 -> vértices 0..6), en el orden de entrada
ENTRADA = [(1, 2), (2, 3), (2, 4), (3, 5), (2, 5), (4, 5), (5, 6), (7, 4)]
N = 7
E = [(a - 1, b - 1) for a, b in ENTRADA]
LAB = {v: str(v + 1) for v in range(N)}
BASE = {0: (0, 1), 1: (1, 1), 2: (2, 0), 3: (2, 2), 4: (3, 1), 5: (4, 1), 6: (1, 2.3)}


def pos(ox, oy, sx, sy):
    return {v: (ox + c * sx, oy + f * sy) for v, (c, f) in BASE.items()}


L_LOOP = find_line(CPP, "for (int v = 0; v < g.V() && !hayCiclo")
L_REV = find_line(CPP, "reverse(post.begin()")
L_DFS = find_line(CPP, "void dfs(")
L_E1 = find_line(CPP, "estado[v] = 1;")
L_FOR = find_line(CPP, "for (int w : g.ady(v))", L_DFS)
L_CIC = find_line(CPP, "if (estado[w] == 1)")
L_REC = find_line(CPP, "else if (estado[w] == 0)")
L_E2 = find_line(CPP, "estado[v] = 2;")
L_POST = find_line(CPP, "post.push_back(v);")
CODE = code_lines(CPP, find_line(CPP, "class OrdenTopologico"), find_line(CPP, "};", L_DFS), maxc=64,
                  skip=[(find_line(CPP, "bool posible()"), find_line(CPP, "vector<int> const& orden()"))])


def adys():
    a = [[] for _ in range(N)]
    for v, w in E:
        a[v].append(w)
    return a


def traza():
    a = adys()
    estado = [0] * N
    pila, post, ev = [], [], []

    def dfs(v, via):
        estado[v] = 1
        pila.append(v)
        ev.append(("entra", v, via, estado[:], pila[:], post[:]))
        for w in a[v]:
            if estado[w] == 0:
                dfs(w, v)
            else:
                ev.append(("ignora", v, w, estado[:], pila[:], post[:]))
        estado[v] = 2
        pila.pop()
        post.append(v)
        ev.append(("fin", v, None, estado[:], pila[:], post[:]))

    for v in range(N):
        if estado[v] == 0:
            dfs(v, None)
    return ev, post


def estilo(estado, actual=None):
    ns = {}
    for u, e in enumerate(estado):
        if e == 1:
            ns[u] = ("gold", "node_t", None)
        elif e == 2:
            ns[u] = ("green", "node_t", None)
    if actual is not None:
        ns[actual] = (ns.get(actual, ("node",))[0], "node_t", "text")
    return ns


def slide_dfs(k, n, tipo, v, w, estado, pila, post, hl, cap):
    s = Slide("Ejecución · ejemplo 1", f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="class OrdenTopologico")
    s.box(684, 84, 572, 310, "grafo (blanco: sin visitar · amarillo: en la pila · verde: terminado)")
    es = {a: ("dim", 3) for a in E}
    if tipo == "entra" and w is not None:
        es[(w, v)] = ("gold", 6)
    if tipo == "ignora":
        es[(v, w)] = ("muted", 6)
    s.dgraph(pos(730, 150, 115, 78), E, ns=estilo(estado, v), es=es, labels=LAB, r=24)
    s.box(684, 410, 572, 194, "estado")
    s.queue_row(704, 440, "pila", [x + 1 for x in pila], size=17)
    s.queue_row(704, 500, "post", [x + 1 for x in post], size=17)
    s.text((704, 555), "post = vértices en el orden en que terminan", size=15, color="muted")
    s.caption(cap, y=628)
    return s


def arcos(s, orden, edges, y0, x0, dx, resalta=None):
    """Los vértices en fila (en el orden dado) y las flechas como arcos por encima."""
    p = {v: (x0 + i * dx, y0) for i, v in enumerate(orden)}
    for a, b in edges:
        (x1, _), (x2, _) = p[a], p[b]
        h = 22 + abs(x2 - x1) * 0.28
        pts = []
        for t in range(0, 21):
            u = t / 20
            pts.append((x1 + (x2 - x1) * u, y0 - 26 - 4 * h * u * (1 - u)))
        s.d.line(pts, fill=C["gold"], width=3)
        (px, py), (qx, qy) = pts[-2], pts[-1]
        import math
        L = math.hypot(qx - px, qy - py)
        ux, uy = (qx - px) / L, (qy - py) / L
        s.d.polygon([(qx + ux * 4, qy + uy * 4), (qx - ux * 10 - uy * 6, qy - uy * 10 + ux * 6),
                     (qx - ux * 10 + uy * 6, qy - uy * 10 - ux * 6)], fill=C["gold"])
    for i, v in enumerate(orden):
        x, y = p[v]
        s.d.ellipse((x - 25, y - 25, x + 25, y + 25), fill=C["node"])
        s.text((x, y), str(v + 1), size=22, color="node_t", bold=True, anchor="mm")
    return p


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-3", TEMA),
             "Ordenando tareas. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    segs.append((ideas("El problema", [
        "N tareas numeradas de 1 a N.",
        "Algunas dependencias: «A debe hacerse antes que B».",
        "Hay que dar un orden en que se respeten TODAS las dependencias.",
        "Si es imposible, se escribe «Imposible». Vale cualquier orden correcto.",
    ]), "Tenemos tareas, y algunas dependen de otras: una tarea A debe hacerse antes que una tarea B. "
        "Hay que dar un orden en el que se respeten todas las dependencias, y si no es posible, escribir imposible. "
        "Vale cualquier orden correcto.", 0))

    # modelo
    s = Slide("La clave: un grafo dirigido")
    s.box(40, 90, 700, 440, "ejemplo 1: 7 tareas, 8 dependencias")
    s.dgraph(pos(110, 190, 130, 105), E, labels=LAB, r=27, es={a: ("muted", 3) for a in E})
    s.bullets(770, 110, 470, [
        "Cada tarea es un vértice.",
        ("A debe ir antes que B  ⇒  arista A → B.", "gold"),
        "Un orden válido es un ORDEN TOPOLÓGICO: todas las flechas van de izquierda a derecha.",
        "Existe  ⇔  el grafo NO tiene ciclos.",
    ], size=21, gap=16)
    segs.append((s, "Cada tarea es un vértice, y cada dependencia es una flecha: de A hacia B si A debe hacerse antes que B. "
                    "Un orden válido es lo que se llama un orden topológico: todas las flechas van de izquierda a derecha.", 0))
    segs.append((s, "Y ese orden existe si y solo si el grafo no tiene ciclos.", 0))

    # orden de ejemplo con arcos
    s = Slide("Orden topológico: todas las flechas hacia la derecha")
    s.box(40, 90, 1200, 330)
    arcos(s, [0, 1, 6, 2, 3, 4, 5], E, 330, 150, 150)
    s.wrap(60, 440, 1160, "Orden del enunciado: 1 2 7 3 4 5 6.  También valdría 7 1 2 4 3 5 6: hay muchos órdenes correctos.",
           size=22, center=True)
    s.wrap(60, 490, 1160, "El 7 solo tiene que estar antes que el 4; el 3 y el 4 no dependen entre sí.", size=21, color="muted", center=True)
    segs.append((s, "Aquí está el orden del enunciado: uno, dos, siete, tres, cuatro, cinco, seis. Todas las flechas van hacia la derecha. "
                    "Pero hay muchos órdenes correctos: el siete solo tiene que ir antes que el cuatro, y el tres y el cuatro no dependen entre sí. Vale cualquiera.", 0))

    # ciclo
    s = Slide("Con un ciclo es imposible")
    s.box(60, 100, 600, 380, "ejemplo 2: 1 antes que 2, y 2 antes que 1")
    s.dgraph({0: (200, 290), 1: (500, 290)}, [(0, 1), (1, 0)], r=36, labels={0: "1", 1: "2"},
             ns={0: ("red", "node_t", None), 1: ("red", "node_t", None)}, es={(0, 1): ("red", 5), (1, 0): ("red", 5)})
    s.bullets(690, 120, 540, [
        "La 1 espera a la 2 y la 2 espera a la 1.",
        "Ninguna de las dos puede empezar.",
        ("Un ciclo  ⇒  Imposible.", "red"),
    ], size=22, gap=18)
    segs.append((s, "En el segundo ejemplo, la tarea uno va antes que la dos, y la dos antes que la uno. Ninguna puede empezar. "
                    "Siempre que hay un ciclo, la respuesta es imposible.", 0))

    # idea dfs
    segs.append((ideas("¿Cómo se calcula? DFS y postorden inverso", [
        "Recorremos el grafo con un DFS. Cuando TERMINA un vértice v, ya han terminado todos sus sucesores.",
        "Entonces v debe ir ANTES que todos ellos.",
        ("Orden topológico = vértices por orden de terminación, al revés (postorden inverso).", "gold"),
        "El mismo DFS detecta ciclos: si desde v vemos un vértice que sigue en la pila, hay ciclo.",
    ]), "Lo calculamos con un D F S. Cuando termina un vértice, ya han terminado todos los que dependen de él, "
        "así que debe ir antes que todos ellos. Por eso, el orden topológico es el orden en que terminan los vértices, pero al revés. "
        "Y el mismo recorrido detecta los ciclos.", 0))

    # tres estados
    s = Slide("Tres estados por vértice")
    s.box(60, 100, 1160, 300)
    for i, (fill, t1, t2) in enumerate([("node", "0 · sin visitar", "todavía no hemos llegado"),
                                         ("gold", "1 · en la pila", "lo estamos explorando"),
                                         ("green", "2 · terminado", "ya hemos explorado todo lo suyo")]):
        x = 220 + i * 360
        s.d.ellipse((x - 40, 160, x + 40, 240), fill=C[fill])
        s.text((x, 280), t1, size=24, bold=True, anchor="mm")
        s.text((x, 320), t2, size=19, color="muted", anchor="mm")
    s.wrap(60, 430, 1160, "Si desde v vemos un vecino en estado 1, ese vecino es un antecesor de v en el recorrido: v → w cierra un ciclo.",
           size=22, color="gold", center=True)
    s.wrap(60, 490, 1160, "Ver un vecino en estado 2 es normal: ya está terminado, no hay ciclo.", size=21, color="muted", center=True)
    segs.append((s, "Cada vértice tiene tres estados: sin visitar, en la pila mientras lo exploramos, y terminado. "
                    "Si desde un vértice vemos un vecino que sigue en la pila, ese vecino es un antecesor, y la flecha cierra un ciclo. "
                    "Ver un vecino terminado es normal, no hay ciclo.", 0))

    # código
    s = Slide("El código", "EJ_05-3.cpp")
    s.code(24, 84, 700, 520, CODE, hl={L_E1, L_CIC, L_REC, L_E2, L_POST}, title="class OrdenTopologico")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["estado[v]: 0 sin visitar, 1 en la pila, 2 terminado.",
                              "Un vecino en estado 1: ciclo.",
                              "Un vecino en estado 0: seguimos el DFS por él.",
                              "Al terminar v: estado 2 y v va a post.",
                              "Al final, reverse(post) es el orden topológico."], size=20, gap=14)
    segs.append((s, "En el código, estado vale cero, uno o dos. Para cada vecino, si está en uno hay un ciclo, y si está en cero seguimos el D F S por él. "
                    "Al terminar un vértice, lo marcamos como terminado y lo guardamos en post. Al final, le damos la vuelta a post, y ese es el orden.", 0))

    # traza
    ev, post_final = traza()
    n = len(ev)
    for k, (tipo, v, w, estado, pila, post) in enumerate(ev, 1):
        if tipo == "entra":
            if w is None:
                cap = f"Empezamos un DFS en {v + 1}: entra en la pila (estado 1)"
                nar = f"Empezamos un D F S en la tarea {v + 1}: entra en la pila."
            else:
                cap = f"Desde {w + 1} el vecino {v + 1} está sin visitar: entramos (estado 1)"
                nar = f"Desde la {w + 1}, el vecino {v + 1} está sin visitar: entramos en él."
            hl = {L_E1, L_FOR, L_REC} if w is not None else {L_LOOP, L_E1}
            segs.append((slide_dfs(k, n, tipo, v, w, estado, pila, post, hl, cap), nar, 0))
        elif tipo == "ignora":
            cap = f"{v + 1} → {w + 1}: el {w + 1} ya está terminado (estado 2), no hay ciclo"
            nar = f"De la {v + 1} a la {w + 1}: la {w + 1} ya está terminada, así que no hay ciclo."
            segs.append((slide_dfs(k, n, tipo, v, w, estado, pila, post, {L_FOR, L_CIC, L_REC}, cap), nar, 0))
        else:
            cap = f"{v + 1} termina (estado 2) y va a post: post = {' '.join(str(x + 1) for x in post)}"
            nar = f"La {v + 1} no tiene más vecinos: termina, y se añade a post."
            segs.append((slide_dfs(k, n, tipo, v, w, estado, pila, post, {L_E2, L_POST}, cap), nar, 0))

    # postorden inverso
    s = Slide("Postorden inverso = orden topológico")
    s.box(60, 100, 1160, 160)
    s.text((90, 120), "post:", size=24, color="muted", bold=True)
    s.queue_row(190, 118, "", [x + 1 for x in post_final], size=24)
    s.text((90, 190), "al revés:", size=24, color="muted", bold=True)
    s.queue_row(190, 188, "", [x + 1 for x in reversed(post_final)], size=24)
    s.box(40, 280, 1200, 280)
    arcos(s, list(reversed(post_final)), E, 440, 150, 150)
    s.caption("Todas las flechas van hacia la derecha: 7 1 2 4 3 5 6 es un orden válido.", y=580)
    segs.append((s, "Al terminar, post vale seis, cinco, tres, cuatro, dos, uno, siete. Le damos la vuelta: siete, uno, dos, cuatro, tres, cinco, seis. "
                    "Comprobamos que todas las flechas van hacia la derecha: es un orden válido, distinto del del enunciado, pero igual de bueno.", 0))

    # ciclo traza
    P2 = {0: (200, 290), 1: (500, 290)}
    E2 = [(0, 1), (1, 0)]

    def sc(k, estado, actual, es, cap, hl):
        s = Slide("Detectando el ciclo · ejemplo 2", f"paso {k} de 3")
        s.code(24, 84, 640, 520, CODE, hl=hl, title="class OrdenTopologico")
        s.box(684, 84, 572, 390, "grafo")
        s.dgraph({v: (x + 560, y - 40) for v, (x, y) in P2.items()}, E2, ns=estilo(estado, actual), es=es,
                 labels={0: "1", 1: "2"}, r=30)
        s.caption(cap, y=628)
        return s
    segs.append((sc(1, [1, 0], 0, {(0, 1): ("dim", 3), (1, 0): ("dim", 3)}, "DFS en 1: entra en la pila (estado 1)", {L_LOOP, L_E1}),
                 "Con el segundo ejemplo: empezamos en la tarea uno, que entra en la pila.", 0))
    segs.append((sc(2, [1, 1], 1, {(0, 1): ("gold", 6), (1, 0): ("dim", 3)}, "Del 1 pasamos al 2: también en la pila (estado 1)", {L_E1, L_FOR, L_REC}),
                 "Su vecino, la tarea dos, está sin visitar: entramos, y también queda en la pila.", 0))
    segs.append((sc(3, [1, 1], 1, {(0, 1): ("dim", 3), (1, 0): ("red", 7)}, "2 → 1: el 1 sigue en la pila (estado 1)  ⇒  CICLO  ⇒  Imposible", {L_FOR, L_CIC}),
                 "Pero el vecino de la dos es la uno, que sigue en la pila: estado uno. Hemos vuelto a un antecesor: hay un ciclo, y la respuesta es imposible.", 0))

    segs.append((ideas("Resultado y coste", [
        "Ejemplo 1: orden  7 1 2 4 3 5 6  (válido; vale cualquiera).",
        "Ejemplo 2: ciclo 1 ⇄ 2  ⇒  Imposible.",
        "Coste: O(N + M), cada vértice y cada arista se miran una vez.",
        "Profundidad de recursión ≤ N = 10.000: no hay problema de pila.",
        ("Alternativa: algoritmo de Kahn (quitar vértices sin dependencias pendientes).", "muted"),
    ]), "En el primer ejemplo sale siete, uno, dos, cuatro, tres, cinco, seis, que es válido. En el segundo, hay un ciclo y sale imposible. "
        "El coste es lineal en tareas más dependencias. La recursión llega como mucho a diez mil niveles, así que no hay problema con la pila.", 0))

    segs.append((cierre(NOMBRE, [
        "Tareas = vértices; «A antes que B» = arista A → B.",
        "Orden válido = orden topológico = postorden inverso del DFS.",
        "Un vecino en la pila (estado 1) = ciclo = Imposible.",
        "Coste O(N + M).",
    ]), "Resumiendo: las tareas son vértices y cada dependencia es una flecha. Un orden válido es el postorden inverso de un D F S, "
        "y si en algún momento vemos un vecino que sigue en la pila, hay un ciclo y la respuesta es imposible.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-3_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-3_ordenando_tareas.mp4")
        print(f"05-3: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
