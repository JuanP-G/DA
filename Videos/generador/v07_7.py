"""Vídeo EJ 07-7 · Ratones en un laberinto"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07b_comun import traza, slide_paso, vectores, dibuja, INF

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-7/EJ_07-7.cpp"
NOMBRE = "Ratones en un laberinto"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1: 5 celdas (vértices 0..4), salida en la celda 5, T = 20
ARCS = [(0, 1, 5), (0, 3, 10), (1, 3, 7), (2, 3, 15), (3, 4, 10)]
S, T = 4, 20
POS = {0: (740, 130), 1: (790, 335), 2: (1010, 345), 3: (990, 235), 4: (1180, 235)}
fmt = lambda d: "∞" if d >= INF else str(d)

L_INV = find_line(CPP, "DigrafoValorado<int> inv = g.inverso();")
L_INI = find_line(CPP, "dist[S] = 0;")
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_BRK = find_line(CPP, "if (dist[v] > T) break;")
L_FOR = find_line(CPP, "for (auto a : inv.ady(v)) {")
L_IF = find_line(CPP, "if (dist[w] > dist[v] + a.valor()) {")
L_SET = [find_line(CPP, "dist[w] = dist[v] + a.valor();"), find_line(CPP, "pq.update(w, dist[w]);")]
L_CNT = [find_line(CPP, "int ratones = 0;"), find_line(CPP, "if (v != S && dist[v] <= T) ++ratones;"), find_line(CPP, "cout << ratones")]
CODE = [(n, t) for n, t in code_lines(CPP, L_INV - 1, find_line(CPP, "cout << ratones"), maxc=64) if t.strip()]
CODE_C = [(n, t) for n, t in CODE if n >= L_CNT[0]]


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-7", TEMA),
             "Ratones en un laberinto. Cuántos ratones llegan a la salida a tiempo: un único Dijkstra, pero sobre el grafo inverso.", 0)]

    segs.append((ideas("El problema", [
        "Laberinto con N celdas (hasta 100.000) y P pasadizos DIRIGIDOS con tiempo 1 a 10.000.",
        "Un ratón en cada celda, menos en la salida S. Cada uno sigue el camino más rápido hacia S.",
        "Cronómetro de T segundos.",
        ("¿Cuántos ratones llegan a S en COMO MUCHO T segundos?", "gold"),
        ("Sin cuellos de botella: caben todos los ratones que sean.", "muted"),
    ]), "Tenemos un laberinto de celdas con pasadizos que solo se recorren en un sentido, cada uno con su tiempo. Hay un ratón en cada celda, menos en la salida, y todos siguen el camino más rápido hacia ella. "
        "El cronómetro empieza con T segundos. Hay que decir cuántos ratones llegan a la salida en como mucho T segundos.", 0))

    s = Slide("Cómo se plantea")
    s.bullets(70, 110, 1140, [
        "Necesitamos el tiempo de CADA celda HASTA la salida.",
        "Dijkstra normal da distancias DESDE un origen, no HACIA un destino.",
        ("camino de a hasta S en el grafo   ==   camino de S hasta a en el grafo INVERSO", "gold"),
        "Un solo Dijkstra desde S en el grafo inverso:  dist[a] = tiempo del ratón de a.",
        "Se cuentan las celdas  a ≠ S  con  dist[a] ≤ T  (el «como mucho» incluye el igual).",
        ("Celdas que no llegan a S: dist = ∞ y no cuentan.", "muted"),
    ], size=24, gap=20)
    segs.append((s, "Necesitamos el tiempo de cada celda hasta la salida. Pero Dijkstra da distancias desde un origen, no hacia un destino. "
                    "El truco: un camino de a hasta la salida en el grafo es un camino de la salida hasta a en el grafo inverso. "
                    "Así, un solo Dijkstra desde la salida en el grafo inverso nos da el tiempo del ratón de cada celda. "
                    "Contamos las celdas distintas de la salida con distancia menor o igual que T. Las que no llegan se quedan en infinito y no cuentan.", 0))

    s = Slide("El código", "EJ_07-7.cpp")
    s.code(24, 84, 700, 520, CODE, hl={L_INV, L_INI, L_BRK} | set(L_CNT[1:2]), title="resuelveCaso()")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["inv = g.inverso(): las flechas al revés.",
                              "Dijkstra desde S sobre inv.",
                              "Si sale una celda con dist > T, break: las demás tampoco llegan.",
                              "Contar las celdas v != S con dist[v] <= T."], size=20, gap=16)
    segs.append((s, "En el código, construimos el grafo inverso y ejecutamos Dijkstra desde la salida sobre él. "
                    "Si sale de la cola una celda con distancia mayor que T, paramos, porque las demás tampoco llegan. Al final contamos las celdas distintas de la salida con distancia menor o igual que T.", 0))

    s = Slide("El ejemplo 1", TEMA)
    s.box(40, 100, 700, 440, "5 celdas · salida en la 5 · T = 20")
    pl = {0: (100, 190), 1: (130, 450), 2: (460, 480), 3: (400, 330), 4: (640, 330)}
    s.dgraph(pl, [(a, b) for a, b, c in ARCS], r=26, labels=["1", "2", "3", "4", "5"],
             ns={4: ("gold", "node_t", None)}, elabels={(a, b): (str(c), "muted") for a, b, c in ARCS})
    s.bullets(770, 130, 470, ["La celda 5 es la salida (en dorado).",
                              "Los pasadizos solo se recorren en el sentido de la flecha.",
                              "Cada celda tiene un ratón, menos la 5."], size=21, gap=16)
    segs.append((s, "Ejemplo uno. Cinco celdas, salida en la cinco, y veinte segundos de cronómetro. Los pasadizos solo se recorren en el sentido de la flecha.", 0))

    pasos = traza(5, [(b, a, c) for a, b, c in ARCS], [S], und=False, corta_si=lambda d: d > T)
    pasos = [p for p in pasos]
    N = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl, cap = {L_INV, L_INI}, "grafo inverso; dist[salida] = 0"
            nar = "Construimos el grafo inverso y empezamos en la salida, con distancia cero."
        elif t == "saca":
            hl, cap = {L_POP, L_BRK}, f"Sale la celda {v + 1}: tiempo {p['dist'][v]} (T = {T})"
            nar = f"Sacamos la celda {v + 1}: su ratón tarda {p['dist'][v]} segundos."
        elif t == "corta":
            hl, cap = {L_POP, L_BRK}, f"{p['dist'][v]} > {T}: break, ya no llega nadie más"
            nar = f"La celda {v + 1} tarda {p['dist'][v]}, más que {T}: paramos, el resto tampoco llegaría."
        elif t == "mejora":
            w = p["w"]
            hl = {L_FOR, L_IF} | set(L_SET)
            ant = "∞" if p["ant"] >= INF else p["ant"]
            cap = f"{v + 1}→{w + 1} (inverso): {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: mejora"
            nar = f"En el inverso, de la {v + 1} a la {w + 1}: {p['nuevo']}. Mejora."
        else:
            w = p["w"]
            hl = {L_FOR, L_IF}
            cap = f"{v + 1}→{w + 1} (inverso): {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
            nar = f"De la {v + 1} a la {w + 1}: {p['nuevo']}, no mejora {p['dist'][w]}."
        s = slide_paso("Dijkstra desde la salida en el grafo INVERSO", "ejemplo 1", CODE, "resuelveCaso()", hl, POS, ARCS, p, True, cap, fmt, 5, k, N,
                       flip=True, gtitle="grafo inverso (flechas al revés) · tiempo bajo cada celda")
        segs.append((s, nar, 0))
    d = pasos[-1]["dist"]

    s = Slide("Contar los ratones que llegan", TEMA)
    s.code(24, 84, 600, 260, CODE_C, hl=set(L_CNT), title="contar")
    s.box(644, 84, 612, 260, "tiempo de cada ratón (T = 20)")
    celdas = [0, 1, 2, 3]
    s.cells(664, 120, "celda", [1, 2, 3, 4, 5], idx=False, cw=60)
    s.cells(664, 168, "tiempo", [fmt(x) for x in d], idx=False, cw=60,
            colors={i: ("green_d" if (i != S and d[i] <= T) else "dim") for i in range(5)})
    s.text((664, 230), "verde: llega a tiempo (≤ 20).   La 5 es la salida: no cuenta.", size=18, color="muted")
    n_ok = sum(1 for i in range(5) if i != S and d[i] <= T)
    s.box(24, 360, 1232, 244, "resultado")
    s.text((60, 410), "celda 4: 10 ≤ 20 ✓    celda 2: 17 ≤ 20 ✓    celda 1: 20 ≤ 20 ✓    celda 3: 25 > 20 ✗", size=21, mono=True)
    s.text((60, 480), f"ratones que salen:  {n_ok}", size=40, bold=True, color="gold")
    s.text((60, 550), "El de la celda 1 llega justo a los 20 segundos y cuenta (≤, no <).", size=22, color="muted")
    segs.append((s, f"Contamos las celdas distintas de la salida con tiempo menor o igual que veinte. La cuatro, diez: sí. La dos, diecisiete: sí. La uno, justo veinte: también cuenta, porque es menor o igual. "
                    f"La tres, veinticinco: no llega. En total, {n_ok} ratones.", 0))

    s = Slide("El ejemplo 2", TEMA)
    s.box(40, 100, 600, 400, "3 celdas · salida en la 1 · T = 10 · pasadizos 2→3 y 3→2")
    pl = {0: (120, 320), 1: (340, 200), 2: (540, 330)}
    s.dgraph(pl, [(1, 2), (2, 1)], r=26, labels=["1", "2", "3"], ns={0: ("gold", "node_t", None)},
             elabels={(1, 2): ("5", "muted"), (2, 1): ("6", "muted")})
    s.bullets(670, 130, 560, ["Ningún pasadizo lleva a la salida (celda 1).",
                              "Dijkstra desde la 1 en el inverso no sale de la celda 1.",
                              "dist = ∞ para las celdas 2 y 3: no cuentan.",
                              ("Salida:   0", "gold")], size=22, gap=18)
    segs.append((s, "En el segundo caso, ningún pasadizo lleva a la salida. Dijkstra desde la salida en el inverso no sale de ella, las otras celdas quedan en infinito y no cuentan. La respuesta es cero.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(P log N) por caso, un solo Dijkstra.",
        "Un Dijkstra por ratón serían N ejecuciones: demasiado.",
        "La salida no cuenta: no hay ratón en S.",
        "dist ≤ T, no dist < T.",
        ("Bucles y pasadizos repetidos no molestan a Dijkstra.", "muted"),
    ]), "El coste es el de un solo Dijkstra, P log N. Hacer un Dijkstra por ratón serían N ejecuciones, demasiado. La salida no cuenta, porque no tiene ratón. "
        "Y el límite es menor o igual que T. Los bucles y los pasadizos repetidos no molestan.", 0))

    segs.append((cierre(NOMBRE, [
        "Tiempo HASTA S de cada celda  =  Dijkstra desde S en el grafo INVERSO.",
        "Un solo Dijkstra para todos los ratones.",
        "Contar las celdas a ≠ S con dist[a] ≤ T; el resto (∞ incluido) no cuenta.",
        "Coste O(P log N).",
    ]), "Resumiendo: el tiempo de cada celda hasta la salida es un Dijkstra desde la salida en el grafo inverso. Contamos las celdas con tiempo menor o igual que T. Coste, P log N.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-7_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-7_ratones_laberinto.mp4")
        print(f"07-7: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
