"""Vídeo EJ 05-L · El Necronomicón de la informática"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../5-Grafos dirigidos/EJ_05-L/EJ_05-L.cpp"
NOMBRE = "El Necronomicón de la informática"
TEMA = "Tema 5 · Grafos dirigidos"

# programas de los tres ejemplos del enunciado: lista de (tipo, destino)
P1 = [("A", 0), ("A", 0), ("J", 1)]
P2 = [("A", 0), ("J", 4), ("J", 5), ("C", 3), ("A", 0)]
P3 = [("A", 0), ("A", 0), ("C", 2), ("A", 0)]
POS1 = {0: (720, 320), 1: (860, 170), 2: (1000, 320), 3: (1160, 200)}
POS2 = {0: (700, 170), 1: (820, 170), 3: (940, 170), 2: (880, 310), 4: (1090, 310), 5: (1200, 170)}
POS3 = {0: (700, 250), 1: (820, 250), 2: (940, 250), 3: (1060, 250), 4: (1180, 250)}

L_CLASS = find_line(CPP, "class ProgramaOscuro")
L_DFS0 = find_line(CPP, "dfs(g, 0);")
L_ALC = find_line(CPP, "alcanzaFin = (")
L_ENT = find_line(CPP, "estado[v] = 1;")
L_CIC = find_line(CPP, "if (estado[w] == 1) hayCiclo = true;")
L_REC = find_line(CPP, "else if (estado[w] == 0) dfs(g, w);")
L_FIN = find_line(CPP, "estado[v] = 2;")
L_A = find_line(CPP, "g.ponArista(i, i + 1);")
L_J = find_line(CPP, "g.ponArista(i, destino - 1);")
L_C = find_line(CPP, "if (tipo == 'C')")
L_RES = find_line(CPP, 'if (!p.terminaAlgunaVez())')
CODE = code_lines(CPP, L_CLASS, find_line(CPP, "};", L_CLASS), maxc=54)
CODE_L = code_lines(CPP, find_line(CPP, "void resuelveCaso()"), L_RES + 3, maxc=64)


def aristas(prog):
    """Mismo orden que EJ_05-L.cpp: J/C primero el salto, luego (si C) la siguiente."""
    E = []
    for i, (t, n) in enumerate(prog):
        if t == "A":
            E.append((i, i + 1))
        else:
            E.append((i, n - 1))
            if t == "C":
                E.append((i, i + 1))
    return E


def texto(prog):
    return [f"{i + 1}:  " + (t if t == "A" else f"{t} {n}") for i, (t, n) in enumerate(prog)]


def etiquetas(L):
    d = {v: str(v + 1) for v in range(L)}
    d[L] = "F"
    return d


def traza(prog):
    """Mismo DFS que el .cpp; eventos con el estado de cada vértice."""
    L = len(prog)
    E = aristas(prog)
    ady = [[] for _ in range(L + 1)]
    for a, b in E:
        ady[a].append(b)
    estado = [0] * (L + 1)
    pila, ev = [], []
    hay = [False]

    def dfs(v, via):
        estado[v] = 1
        pila.append(v)
        ev.append(("entra", v, via, estado[:], pila[:]))
        for w in ady[v]:
            if estado[w] == 1:
                hay[0] = True
                ev.append(("ciclo", v, w, estado[:], pila[:]))
            elif estado[w] == 0:
                dfs(w, v)
            else:
                ev.append(("visto", v, w, estado[:], pila[:]))
        estado[v] = 2
        pila.pop()

    dfs(0, None)
    ev.append(("fin", 0, None, estado[:], []))
    return ev, estado[L] != 0, hay[0]


def estilo(estado, L, actual=None):
    ns = {}
    for u, e in enumerate(estado):
        if e == 1:
            ns[u] = ("gold", "node_t", None)
        elif e == 2:
            ns[u] = ("green", "node_t", None)
    if L in ns and estado[L] != 0:
        ns[L] = ("green", "node_t", "gold")
    elif L not in ns:
        ns[L] = ("purple", "node_t", None)
    if actual is not None:
        ns[actual] = (ns.get(actual, ("node",))[0], "node_t", "text")
    return ns


def slide_dfs(titulo, corner, prog, posd, tipo, v, w, estado, pila, hl, cap):
    L = len(prog)
    E = aristas(prog)
    s = Slide(titulo, corner)
    s.code(24, 84, 600, 520, CODE, hl=hl, title="class ProgramaOscuro")
    s.box(644, 84, 612, 300, "el programa como digrafo (F = el programa ha terminado)")
    es = {e: ("dim", 3) for e in E}
    if tipo == "entra" and w is not None:
        es[(w, v)] = ("gold", 6)
    if tipo == "visto":
        es[(v, w)] = ("muted", 6)
    if tipo == "ciclo":
        es[(v, w)] = ("red", 7)
    s.dgraph(posd, E, ns=estilo(estado, L, v), es=es, labels=etiquetas(L), r=24)
    s.box(644, 400, 612, 204, "programa y pila")
    for i, t in enumerate(texto(prog)):
        s.text((664 + (i // 3) * 110, 440 + (i % 3) * 34), t, size=20, mono=True, color="text")
    s.queue_row(900, 440, "pila", [u + 1 if u < L else "F" for u in pila], size=17)
    s.text((900, 500), "amarillo: en la pila · verde: terminado", size=15, color="muted")
    s.caption(cap, y=628)
    return s


def narra(prog, posd, titulo):
    ev, fin, ciclo = traza(prog)
    L = len(prog)
    out = []
    n = len(ev)

    def x(u):
        return "F" if u == L else str(u + 1)

    def xn(u):
        return "el final" if u == L else f"la instrucción {u + 1}"

    for k, (tipo, v, w, estado, pila) in enumerate(ev, 1):
        if tipo == "fin":
            continue
        if tipo == "entra":
            if w is None:
                cap = "DFS desde la instrucción 1 (vértice 0): entra en la pila"
                nar = "Lanzamos el D F S desde la primera instrucción."
                hl = {L_DFS0, L_ENT}
            else:
                cap = f"{x(w)} → {x(v)}: {x(v)} está sin visitar, entramos" + ("  (¡el final!)" if v == L else "")
                nar = (f"De {xn(w)} a {xn(v)}, que está sin visitar: entramos." +
                       (" Hemos alcanzado el final: el programa puede terminar." if v == L else ""))
                hl = {L_ENT, L_REC}
        elif tipo == "visto":
            cap = f"{x(v)} → {x(w)}: {x(w)} ya terminó (no está en la pila)  ⇒  no es un ciclo"
            nar = f"De {xn(v)} a {xn(w)}: ya había terminado, no está en la pila, así que no es un ciclo."
            hl = {L_CIC, L_REC}
        else:
            cap = f"{x(v)} → {x(w)}: {x(w)} sigue en la pila (estado 1)  ⇒  CICLO alcanzable"
            nar = f"De {xn(v)} a {xn(w)}: pero {xn(w)} sigue en la pila. Hay un ciclo alcanzable: se puede dar vueltas para siempre."
            hl = {L_CIC}
        out.append((slide_dfs(titulo, f"paso {k} de {n - 1}", prog, posd, tipo, v, w, estado, pila, hl, cap), nar, 0))
    return out, ev, fin, ciclo


def slide_conclusion(titulo, prog, posd, ev, fin, ciclo, resp, nar):
    L = len(prog)
    estado = ev[-1][3]
    s = Slide(titulo, TEMA)
    s.box(24, 84, 600, 300, "el programa")
    for i, t in enumerate(texto(prog)):
        s.text((60 + (i // 3) * 200, 130 + (i % 3) * 50), t, size=28, mono=True, color="text")
    s.box(644, 84, 612, 300, "tras el DFS desde la instrucción 1")
    E = aristas(prog)
    s.dgraph(posd, E, ns=estilo(estado, L), es={e: ("dim", 3) for e in E}, labels=etiquetas(L), r=24)
    s.box(24, 400, 1232, 204)
    s.text((60, 424), f"¿se alcanza el final F?   {'SÍ' if fin else 'NO'}", size=26, bold=True, color="green" if fin else "red")
    s.text((60, 474), f"¿hay un ciclo alcanzable?   {'SÍ' if ciclo else 'NO'}", size=26, bold=True, color="red" if ciclo else "green")
    s.text((60, 540), "respuesta:", size=26, color="muted")
    s.text((250, 530), resp, size=44, bold=True, color="gold")
    return s, nar, 0


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-L", TEMA),
             "El Necronomicón de la informática. Un programa oscuro con saltos impredecibles: vemos cómo se convierte en un grafo dirigido "
             "y cómo un único recorrido en profundidad decide si siempre termina, nunca termina, o a veces sí y a veces no.", 0)]

    segs.append((ideas("El problema", [
        "Programa de L instrucciones (1 … 10.000), la primera es la 1; termina al llegar DETRÁS de la última.",
        "A: instrucción normal (pasa a la siguiente).     J N: salta a la N.",
        "C N: salta a la N O pasa a la siguiente, y no se puede predecir.",
        ("¿El programa SIEMPRE termina, NUNCA termina, o A VECES (según los saltos condicionales)?", "gold"),
    ]), "Un programa oscuro tiene hasta diez mil instrucciones de tres tipos. A es una instrucción normal, que pasa a la siguiente. "
        "J N salta a la instrucción N. Y C N es un salto condicional impredecible: salta a la N o pasa a la siguiente. "
        "El programa termina cuando se llega detrás de la última instrucción. Hay que decir si siempre termina, nunca termina, o a veces sí y a veces no.", 0))

    # modelo
    ev2, _, _ = traza(P2)
    s = Slide("Cada ejecución posible es un camino", TEMA)
    s.box(24, 90, 400, 360, "ejemplo 2")
    for i, t in enumerate(texto(P2)):
        s.text((60, 140 + i * 52), t, size=30, mono=True, color="text")
    E = aristas(P2)
    s.box(444, 90, 812, 360, "digrafo: instrucción i = vértice i − 1; el vértice L (F) = «terminado»")
    s.dgraph({v: (p[0] - 160, p[1] + 50) for v, p in POS2.items()}, E, labels=etiquetas(5), r=26,
             ns={5: ("purple", "node_t", None)}, es={e: ("muted", 4) for e in E})
    s.bullets(40, 470, 1200, [
        ("A → una arista a la siguiente.     J N → una arista a la N.     C N → LAS DOS aristas.", "gold"),
        "Una ejecución del programa es un camino que empieza en el vértice 0. Solo el final F no tiene sucesores.",
    ], size=21, gap=12)
    segs.append((s, "Convertimos el programa en un grafo dirigido: la instrucción i es el vértice i menos uno, y añadimos un vértice F, que significa programa terminado. "
                    "Una instrucción normal tiene una arista a la siguiente; un salto, una arista a su destino; y un salto condicional tiene las dos. "
                    "Cada ejecución posible es un camino que empieza en el primer vértice, y solo el final no tiene sucesores.", 0))

    # las tres respuestas
    s = Slide("Un solo DFS desde la instrucción 1", TEMA)
    s.box(40, 100, 1200, 330, "tres respuestas")
    filas = [("NUNCA", "red", "el final F NO se alcanza desde la instrucción 1", "ningún camino llega a F"),
             ("SIEMPRE", "green", "se alcanza F y NO hay ciclo alcanzable", "sin ciclos todo camino es finito y acaba en F"),
             ("A VECES", "gold", "se alcanza F y SÍ hay un ciclo alcanzable", "unas ejecuciones llegan a F y otras dan vueltas")]
    for i, (a, col, b, c) in enumerate(filas):
        y = 150 + i * 90
        s.pill(70, y, a, fill=col, size=26, padx=18, pady=10)
        s.text((290, y - 2), b, size=24, bold=True)
        s.text((290, y + 34), c, size=19, color="muted")
    s.bullets(60, 460, 1160, [
        "El ciclo se detecta como siempre: un vecino que sigue en la pila.",
        "Solo cuenta lo que se alcanza desde la instrucción 1: por eso el DFS parte del vértice 0, no de todos.",
    ], size=21, gap=12)
    segs.append((s, "Un solo recorrido en profundidad desde la primera instrucción responde a todo. "
                    "Si el final no se alcanza, nunca termina. Si se alcanza y no hay ningún ciclo alcanzable, siempre termina, porque sin ciclos todo camino es finito y acaba en el final. "
                    "Y si se alcanza y además hay un ciclo alcanzable, a veces: unas ejecuciones llegan al final y otras dan vueltas al ciclo. "
                    "El ciclo se detecta como siempre, con un vecino que sigue en la pila, y el recorrido parte solo de la primera instrucción, porque lo que no se alcanza no cuenta.", 0))

    # código
    s = Slide("El código (1): leer el programa", "EJ_05-L.cpp")
    s.code(24, 84, 760, 520, CODE_L, hl={L_A, L_J, L_C, L_RES}, title="resuelveCaso()")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["Digrafo con L + 1 vértices: el último es «terminado».",
                              "A: arista i → i + 1.",
                              "J N: arista i → N − 1.",
                              "C N: la del salto Y la de la siguiente.",
                              "Al final se decide con las dos preguntas."], size=19, gap=14)
    segs.append((s, "En el código, se crea un digrafo con L más uno vértices. Para cada instrucción, una A añade la arista a la siguiente; un salto añade la arista a su destino menos uno; "
                    "y si es condicional, se añade además la de la siguiente. Al final se decide con las dos preguntas: si se alcanza el final, y si hay un ciclo.", 0))
    s = Slide("El código (2): el DFS", "EJ_05-L.cpp")
    s.code(24, 84, 760, 520, code_lines(CPP, L_CLASS, find_line(CPP, "};", L_CLASS), maxc=64),
           hl={L_DFS0, L_ALC, L_ENT, L_CIC, L_FIN}, title="class ProgramaOscuro")
    s.box(804, 84, 452, 520, "qué hace")
    s.bullets(824, 130, 410, ["dfs(g, 0): solo desde la instrucción 1.",
                              "estado 0 sin visitar, 1 en la pila, 2 terminado.",
                              "Vecino en estado 1  ⇒  hayCiclo = true.",
                              "alcanzaFin: el último vértice se ha visitado."], size=19, gap=14)
    segs.append((s, "El recorrido solo parte del vértice cero. Cada vértice tiene tres estados: sin visitar, en la pila y terminado. "
                    "Si un vecino está en la pila, hay un ciclo. Y al terminar, el final se alcanza si su estado ya no es cero.", 0))

    # trazas
    tr1, ev1, fin1, ci1 = narra(P1, POS1, "Ejemplo 1: el DFS")
    segs += tr1
    segs.append(slide_conclusion("Ejemplo 1: conclusión", P1, POS1, ev1, fin1, ci1, "NUNCA",
                                 "El final no se ha alcanzado nunca, y hay un ciclo. Respuesta: nunca."))

    tr2, ev2, fin2, ci2 = narra(P2, POS2, "Ejemplo 2: el DFS")
    segs += tr2
    segs.append(slide_conclusion("Ejemplo 2: conclusión", P2, POS2, ev2, fin2, ci2, "SIEMPRE",
                                 "Se alcanza el final y no hay ningún ciclo. Que la instrucción 4 salte hacia atrás, a la 3, no crea un ciclo: desde la 3 se va a la 5 y no se vuelve. "
                                 "Respuesta: siempre."))

    tr3, ev3, fin3, ci3 = narra(P3, POS3, "Ejemplo 3: el DFS")
    segs += tr3
    segs.append(slide_conclusion("Ejemplo 3: conclusión", P3, POS3, ev3, fin3, ci3, "A VECES",
                                 "Se alcanza el final, pero además hay un ciclo alcanzable entre la instrucción 2 y la 3. "
                                 "Si el salto condicional se toma siempre, no termina; si alguna vez no se toma, termina. Respuesta: a veces."))

    segs.append((ideas("Detalles y coste", [
        "Un salto hacia atrás NO es un ciclo si no se puede volver a él (ejemplo 2).",
        "Un ciclo que no se alcanza desde la instrucción 1 no cuenta: el DFS solo parte del vértice 0.",
        "C N con N = i + 1 crea una arista repetida: no molesta.",
        "Profundidad de la recursión ≤ L = 10.000: no hay problema de pila.",
        ("Coste: O(L) por caso (cada instrucción aporta como mucho 2 aristas).", "gold"),
    ]), "Algunos detalles. Un salto hacia atrás no es un ciclo si no se puede volver a él. Un ciclo que no se alcanza desde la primera instrucción no cuenta. "
        "Una arista repetida no molesta. La recursión llega como mucho a diez mil niveles, y el coste es lineal en el número de instrucciones.", 0))

    segs.append((cierre(NOMBRE, [
        "Instrucción i = vértice i − 1; vértice extra F = «terminado».",
        "A: i → i+1.   J N: i → N−1.   C N: las dos.",
        "Un DFS desde la instrucción 1:  F no alcanzado ⇒ NUNCA.",
        "F alcanzado y sin ciclo alcanzable ⇒ SIEMPRE;  con ciclo ⇒ A VECES.",
        "Coste O(L).",
    ]), "Resumiendo: cada instrucción es un vértice, y añadimos uno más para el final. "
        "Con un único recorrido en profundidad desde la primera instrucción: si no se alcanza el final, nunca termina; si se alcanza y no hay ciclo alcanzable, siempre termina; "
        "y si se alcanza y hay un ciclo alcanzable, a veces. El coste es lineal.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-L_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-L_necronomicon.mp4")
        print(f"05-L: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
