"""Vídeo EJ 05-6 · Sistema de inecuaciones"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../5-Grafos dirigidos/EJ_05-6/EJ_05-6.cpp"
NOMBRE = "Sistema de inecuaciones"
TEMA = "Tema 5 · Grafos dirigidos"

# ejemplo 1: x1<x3, x3<x2, x2<x4, x3<x4, x1<x4  (variable xk -> vértice k-1), en el orden de entrada
E1 = [(0, 2), (2, 1), (1, 3), (2, 3), (0, 3)]
N1 = 4
POS1 = {0: (0, 1), 2: (1, 0), 1: (2, 0), 3: (3, 1)}
# ejemplo 3: x3 < x1, x2 suelta
E3 = [(2, 0)]
N3 = 3
POS3 = {0: (0, 0), 1: (1, 1), 2: (2, 0)}


def lab(n):
    return {v: f"x{v + 1}" for v in range(n)}


def pos(base, ox, oy, sx, sy):
    return {v: (ox + c * sx, oy + f * sy) for v, (c, f) in base.items()}


L_LOOP = find_line(CPP, "for (int v = 0; v < g.V() && !hayCiclo")
L_VAL = find_line(CPP, "valor[post[i]] = n - i;")
L_E1 = find_line(CPP, "estado[v] = 1;")
L_FOR = find_line(CPP, "for (int w : g.ady(v))", L_E1)
L_CIC = find_line(CPP, "if (estado[w] == 1)")
L_REC = find_line(CPP, "else if (estado[w] == 0)")
L_E2 = find_line(CPP, "estado[v] = 2;")
L_POST = find_line(CPP, "post.push_back(v);")
L_CLASS = find_line(CPP, "class Inecuaciones")
CODE = code_lines(CPP, L_CLASS, find_line(CPP, "};", L_CLASS), maxc=62,
                  skip=[(find_line(CPP, "bool posible()"), find_line(CPP, "int valorDe(int v)") + 1)])
L_LEE = find_line(CPP, "Digrafo g(cin, 1);")


def adys(n, edges):
    a = [[] for _ in range(n)]
    for v, w in edges:
        a[v].append(w)
    return a


def traza(n, edges):
    """Mismo DFS que EJ_05-6.cpp. Eventos: entra / visto (terminado) / ciclo / fin."""
    a = adys(n, edges)
    estado = [0] * n
    pila, post, ev = [], [], []
    hay = [False]

    def dfs(v, via):
        estado[v] = 1
        pila.append(v)
        ev.append(("entra", v, via, estado[:], pila[:], post[:]))
        for w in a[v]:
            if hay[0]:
                return
            if estado[w] == 1:
                hay[0] = True
                ev.append(("ciclo", v, w, estado[:], pila[:], post[:]))
            elif estado[w] == 0:
                dfs(w, v)
            else:
                ev.append(("visto", v, w, estado[:], pila[:], post[:]))
        if hay[0]:
            return
        estado[v] = 2
        pila.pop()
        post.append(v)
        ev.append(("fin", v, None, estado[:], pila[:], post[:]))

    for v in range(n):
        if hay[0]:
            break
        if estado[v] == 0:
            dfs(v, None)
    return ev, post, hay[0]


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


def x(v):
    return f"x{v + 1}"


def xn(v):
    return f"equis {v + 1}"


def slide_traza(titulo, k, n_ev, tipo, v, w, estado, pila, post, n, edges, posfn, hl, cap):
    s = Slide(titulo, f"paso {k} de {n_ev}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="class Inecuaciones")
    s.box(684, 84, 572, 300, "grafo (blanco: sin visitar · amarillo: en la pila · verde: terminado)")
    es = {e: ("dim", 3) for e in edges}
    if tipo == "entra" and w is not None:
        es[(w, v)] = ("gold", 6)
    if tipo == "visto":
        es[(v, w)] = ("muted", 6)
    if tipo == "ciclo":
        es[(v, w)] = ("red", 7)
    s.dgraph(posfn, edges, ns=estilo(estado, v), es=es, labels=lab(n), r=27)
    s.box(684, 400, 572, 204, "estado")
    s.queue_row(704, 432, "pila", [x(u) for u in pila], size=17)
    s.queue_row(704, 490, "post", [x(u) for u in post], size=17)
    s.text((704, 548), "post = variables en el orden en que TERMINAN", size=15, color="muted")
    s.caption(cap, y=628)
    return s


def narra_traza(ev, edges, titulo, posfn, n):
    segs = []
    for k, (tipo, v, w, estado, pila, post) in enumerate(ev, 1):
        if tipo == "entra":
            if w is None:
                cap = f"Lanzamos un DFS desde {x(v)}: entra en la pila (estado 1)"
                nar = f"Lanzamos un D F S desde {xn(v)}, que entra en la pila."
                hl = {L_LOOP, L_E1}
            else:
                cap = f"{x(w)} → {x(v)}: {x(v)} está sin visitar, entramos (estado 1)"
                nar = f"Desde {xn(w)}, su sucesor {xn(v)} está sin visitar: entramos."
                hl = {L_E1, L_FOR, L_REC}
        elif tipo == "visto":
            cap = f"{x(v)} → {x(w)}: {x(w)} ya terminó (estado 2), no hay ciclo"
            nar = f"De {xn(v)} a {xn(w)}: {xn(w)} ya terminó, así que no hay ciclo."
            hl = {L_FOR, L_CIC, L_REC}
        elif tipo == "ciclo":
            cap = f"{x(v)} → {x(w)}: {x(w)} sigue en la pila (estado 1)  ⇒  CICLO  ⇒  NO"
            nar = (f"De {xn(v)} a {xn(w)}: pero {xn(w)} sigue en la pila. Es un antecesor: hay un ciclo, "
                   f"y la respuesta es no.")
            hl = {L_FOR, L_CIC}
        else:
            cap = f"{x(v)} termina (estado 2) y va a post:  post = {' '.join(x(u) for u in post)}"
            nar = f"{xn(v).capitalize()} no tiene más sucesores pendientes: termina y se añade a post."
            hl = {L_E2, L_POST}
        segs.append((slide_traza(titulo, k, len(ev), tipo, v, w, estado, pila, post, n, edges, posfn, hl, cap), nar, 0))
    return segs


def slide_valores(titulo, post, n, edges, nar, nota=None):
    s = Slide(titulo)
    s.code(24, 84, 640, 160, code_lines(CPP, L_VAL - 3, L_VAL, maxc=62), hl={L_VAL}, title="constructor", size=16)
    s.box(684, 84, 572, 160, "valor[post[i]] = n − i")
    for i, v in enumerate(post):
        cx = 720 + i * 120
        s.text((cx, 120), f"i = {i}", size=15, color="muted", anchor="mm")
        s.d.ellipse((cx - 26, 136, cx + 26, 188), fill=C["green"])
        s.text((cx, 162), x(v), size=20, color="node_t", bold=True, anchor="mm")
        s.text((cx, 215), f"= {n - i}", size=22, color="gold", bold=True, anchor="mm")
    val = {v: n - i for i, v in enumerate(post)}
    s.box(24, 262, 1232, 330, "comprobación: cada inecuación xi < xj")
    for k, (a, b) in enumerate(edges):
        y = 306 + k * 46
        ok = val[a] < val[b]
        s.text((60, y), f"{x(a)} < {x(b)}", size=24, bold=True)
        s.text((260, y), f"{val[a]} < {val[b]}", size=24, color="green" if ok else "red", bold=True)
        s.text((400, y), "✓" if ok else "✗", size=26, color="green" if ok else "red", bold=True)
    s.text((700, 306), "salida:", size=22, color="muted")
    s.text((700, 346), "SI " + " ".join(str(val[v]) for v in range(n)), size=34, color="gold", bold=True)
    if nota:
        s.wrap(700, 410, 520, nota, size=19, color="muted")
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-6", TEMA),
             "Sistema de inecuaciones. Vemos cómo se plantea con un grafo dirigido, cómo se detecta que no hay solución, "
             "y sobre todo cómo se asigna un valor a cada variable.", 0)]

    segs.append((ideas("El problema", [
        "Variables enteras x1 … xN.",
        "Inecuaciones de la forma  xi < xj  (pueden repetirse).",
        "¿Hay valores que cumplan TODAS? Si sí: «SI» y un valor para cada variable, de x1 a xN.",
        "Si no: «NO». Vale cualquier asignación correcta.",
    ]), "Tenemos variables enteras, de equis 1 a equis ene, e inecuaciones de la forma equis i menor que equis j. "
        "Hay que decir si existen valores que las cumplan todas y, si existen, dar uno para cada variable. Vale cualquier asignación correcta.", 0))

    # modelo
    s = Slide("La clave: un grafo dirigido")
    s.box(40, 90, 700, 440, "ejemplo 1: x1<x3, x3<x2, x2<x4, x3<x4, x1<x4")
    s.dgraph(pos(POS1, 120, 380, 170, -190), E1, labels=lab(N1), r=34, es={a: ("muted", 3) for a in E1})
    s.bullets(770, 110, 470, [
        "Cada variable es un vértice.",
        ("xi < xj  ⇒  arista i → j", "gold"),
        "La flecha va del MENOR al MAYOR.",
        "Hay que dar valores que crezcan a lo largo de todas las flechas.",
    ], size=21, gap=16)
    s.code(770, 400, 470, 100, code_lines(CPP, L_LEE, L_LEE, maxc=40), hl={L_LEE}, title="lectura", size=16)
    segs.append((s, "Cada variable es un vértice, y cada inecuación equis i menor que equis j es una flecha de i a j: va del menor al mayor. "
                    "Hay que dar valores que crezcan siguiendo todas las flechas. "
                    "La entrada tiene justo el formato que lee el constructor del digrafo, con un uno porque las variables empiezan en uno.", 0))

    # ciclo
    s = Slide("Con un ciclo no hay solución")
    s.box(60, 100, 600, 380, "ejemplo 2: x1 < x2  y  x2 < x1")
    s.dgraph({0: (200, 290), 1: (500, 290)}, [(0, 1), (1, 0)], r=40, labels=lab(2),
             ns={0: ("red", "node_t", None), 1: ("red", "node_t", None)}, es={(0, 1): ("red", 5), (1, 0): ("red", 5)})
    s.bullets(690, 120, 540, [
        "x1 < x2 < x1: x1 tendría que ser menor que sí mismo.",
        ("Un ciclo  ⇒  NO.", "red"),
        ("Sin ciclos (un DAG)  ⇒  SÍ hay solución.", "green"),
    ], size=22, gap=18)
    segs.append((s, "Si las flechas forman un ciclo, por ejemplo equis 1 menor que equis 2 y equis 2 menor que equis 1, "
                    "una variable tendría que ser menor que sí misma: imposible, respuesta no. Y si no hay ciclos, siempre hay solución.", 0))

    # idea
    segs.append((ideas("¿Qué valor le damos a cada variable?", [
        "Un DFS que, además de buscar ciclos, guarda cada vértice en post CUANDO TERMINA.",
        ("Si hay arista i → j, j termina ANTES que i: o ya había terminado, o i lo visita y espera a que acabe.", "gold"),
        "Repartimos los valores de mayor a menor en el orden de post: el primero que termina recibe N, el último 1.",
        ("valor[post[i]] = N − i   ⇒   cada flecha va de un valor menor a uno mayor.", "green"),
    ]), "¿Qué valor damos a cada variable? Hacemos un D F S que, además de buscar ciclos, guarda cada vértice en post en el momento en que termina. "
        "La clave es que si hay una flecha de i a j, j termina antes que i: o ya había terminado, o i lo visita y espera a que acabe. "
        "Así que repartimos los valores de mayor a menor siguiendo post: el primero que termina recibe ene, y el último recibe uno. "
        "Como j terminó antes, recibe un valor mayor que i, que es justo lo que pide la inecuación.", 0))

    # código
    s = Slide("El código", "EJ_05-6.cpp")
    s.code(24, 84, 760, 520, CODE, hl={L_LOOP, L_VAL, L_CIC, L_POST}, title="class Inecuaciones")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["Lanza un DFS desde CADA vértice sin visitar (también los sueltos).",
                              "estado: 0 sin visitar, 1 en la pila, 2 terminado.",
                              "Vecino en estado 1: ciclo ⇒ NO.",
                              "Al terminar v: post.push_back(v).",
                              "Al final: valor[post[i]] = n − i."], size=19, gap=14)
    segs.append((s, "En el código, el constructor lanza un D F S desde cada vértice sin visitar, también desde los que no tienen ninguna flecha. "
                    "Cada vértice tiene tres estados: sin visitar, en la pila y terminado. Un vecino en la pila es un ciclo. "
                    "Al terminar un vértice se añade a post, y al final se asignan los valores: valor de post de i es ene menos i.", 0))

    # traza ejemplo 1
    ev, post1, _ = traza(N1, E1)
    segs += narra_traza(ev, E1, "Ejemplo 1: el DFS", pos(POS1, 760, 330, 140, -120), N1)
    segs.append((slide_valores("Ejemplo 1: los valores", post1, N1, E1, None,
                               nota="El enunciado da SI 2 5 3 7: también vale. Se acepta cualquier asignación correcta."),
                 "Al terminar, post es equis 4, equis 2, equis 3, equis 1. Repartimos de mayor a menor: equis 4 vale 4, equis 2 vale 3, equis 3 vale 2 y equis 1 vale 1. "
                 "Comprobamos las cinco inecuaciones: todas se cumplen. El enunciado da otros valores, pero cualquier asignación correcta vale.", 0))

    # ejemplo 3: variable suelta
    ev3, post3, _ = traza(N3, E3)
    s = Slide("Ejemplo 3: ¿y las variables sueltas?")
    s.box(40, 90, 560, 330, "x3 < x1   ·   x2 no aparece en ninguna inecuación")
    s.dgraph(pos(POS3, 140, 190, 170, 140), E3, labels=lab(N3), r=34, es={(2, 0): ("muted", 4)},
             ns={1: ("purple", "node_t", None)})
    s.box(620, 90, 636, 330, "el bucle del constructor: un DFS por cada vértice sin visitar")
    filas = [("dfs(x1)", "x1 no tiene sucesores: termina", "post = x1"),
             ("dfs(x2)", "suelta: termina al momento", "post = x1 x2"),
             ("dfs(x3)", "su sucesor x1 ya terminó", "post = x1 x2 x3")]
    for i, (a, b, c) in enumerate(filas):
        y = 140 + i * 82
        s.text((640, y), a, size=22, color="gold", bold=True, mono=True)
        s.text((790, y + 4), b, size=18)
        s.text((790, y + 34), c, size=18, color="green", mono=True)
    s.bullets(60, 445, 1160, [
        "Una variable suelta entra en post como cualquier otra, así que también recibe un valor.",
        ("Valores: x1 = 3, x2 = 2, x3 = 1  ⇒  SI 3 2 1.   x3 < x1 se cumple; a x2 le vale cualquiera.", "gold"),
    ], size=21, gap=14)
    segs.append((s, "¿Y las variables que no aparecen en ninguna inecuación? En el tercer ejemplo, equis 2 está suelta. "
                    "El constructor lanza un D F S desde cada vértice sin visitar: desde equis 1, que termina enseguida; desde equis 2, que como no tiene flechas termina al momento; "
                    "y desde equis 3, cuyo sucesor ya había terminado. Así que equis 2 también entra en post y recibe un valor. "
                    "Salen equis 1 igual a 3, equis 2 igual a 2 y equis 3 igual a 1: equis 3 es menor que equis 1, y a equis 2, como nadie la nombra, le vale cualquiera.", 0))

    # ejemplo 2: ciclo, traza
    E2 = [(0, 1), (1, 0)]
    ev2, _, _ = traza(2, E2)
    segs += narra_traza(ev2, E2, "Ejemplo 2: el DFS encuentra el ciclo", {0: (830, 240), 1: (1110, 240)}, 2)

    segs.append((ideas("Resultado y coste", [
        "Ejemplo 1: SI 1 3 2 4.   Ejemplo 2: NO.   Ejemplo 3: SI 3 2 1.",
        "Coste O(N + M) por caso: cada vértice y cada arista se miran una vez.",
        "Inecuaciones repetidas = aristas repetidas: no molestan.",
        "Profundidad de la recursión ≤ N = 10.000: no hay problema de pila.",
        ("Es el mismo DFS que 05-3 (Ordenando tareas): solo cambia lo que se escribe.", "muted"),
    ]), "Los tres ejemplos salen: sí uno tres dos cuatro, no, y sí tres dos uno. "
        "El coste es lineal en variables más inecuaciones. Las repetidas no molestan, y la recursión llega como mucho a diez mil niveles. "
        "Es el mismo recorrido que en ordenando tareas: allí se escribía el orden, y aquí la posición de cada variable.", 0))

    segs.append((cierre(NOMBRE, [
        "xi < xj  ⇒  arista i → j (del menor al mayor).",
        "Ciclo (vecino en la pila)  ⇒  NO.",
        "Si no: post = orden de terminación; valor[post[i]] = N − i.",
        "Las variables sueltas también pasan por el DFS y reciben valor.",
        "Coste O(N + M).",
    ]), "Resumiendo: cada inecuación es una flecha del menor al mayor. Si hay un ciclo, no hay solución. "
        "Si no, guardamos los vértices en el orden en que terminan y repartimos los valores de mayor a menor, "
        "y las variables sueltas también reciben el suyo porque el D F S pasa por todos los vértices.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-6_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-6_sistema_inecuaciones.mp4")
        print(f"05-6: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
