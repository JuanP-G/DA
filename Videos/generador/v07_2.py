"""Vídeo EJ 07-2 · Camino al cole"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07_comun import traza, dibuja_grafo, estado, FINITO

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-2/EJ_07-2.cpp"
NOMBRE = "Camino al cole"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1 del enunciado: 7 intersecciones, 10 calles (vértices 0..6 = intersecciones 1..7)
EDGES = [(0, 1, 5), (0, 2, 7), (1, 3, 10), (2, 3, 8), (1, 4, 30), (3, 4, 12), (3, 6, 25), (3, 5, 11), (4, 6, 13), (5, 6, 30)]
POS = {0: (730, 240), 1: (850, 150), 2: (850, 330), 3: (970, 240), 4: (1090, 150), 5: (1090, 330), 6: (1210, 240)}

L_INI = [find_line(CPP, "dist[0] = 0;"), find_line(CPP, "formas[0] = 1;"), find_line(CPP, "pq.push(0, 0);")]
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_FOR = find_line(CPP, "for (auto a : g.ady(v))")
L_D = find_line(CPP, "int d = dist[v] + a.valor();")
L_LT = [find_line(CPP, "if (d < dist[w]) {"), find_line(CPP, "dist[w] = d;"), find_line(CPP, "formas[w] = formas[v];"), find_line(CPP, "pq.update(w, d);")]
L_EQ = [find_line(CPP, "} else if (d == dist[w]) {"), find_line(CPP, "formas[w] += formas[v];")]
L_OUT = find_line(CPP, "cout << formas[N - 1]")
L_CONS = [find_line(CPP, "g.ponArista({u, v, l});"), find_line(CPP, "g.ponArista({v, u, l});")]
INI = find_line(CPP, "const int INF")
CODE = [(n, t) for n, t in code_lines(CPP, INI, L_OUT, maxc=70) if t.strip()]


def slide_paso(k, n, paso, hl, cap):
    s = Slide("Ejecución · ejemplo 1: de la 1 a la 7", f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="Dijkstra dentro de resuelveCaso")
    s.box(684, 84, 572, 300, "el pueblo (junto a cada nodo: distancia × formas)")
    dibuja_grafo(s, POS, EDGES, dict(paso, _formas=True), dirigido=False, r=20, hl_edge=paso.get("k"), first=1)
    s.box(684, 394, 572, 226, "estado")
    estado(s, 704, 412, paso, 7, contar=True, first=1, dy=56)
    s.caption(cap, y=634)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-2", TEMA),
             "Camino al cole. No basta con la distancia mínima: hay que contar de cuántas maneras se consigue. Adaptamos Dijkstra.", 0)]

    segs.append((ideas("El problema", [
        "Un pueblo con N intersecciones (hasta 100.000) y C calles con longitud.",
        "Lucas va de la intersección 1 al colegio, en la N, siempre por un camino MÍNIMO.",
        "Las calles se recorren en AMBOS sentidos.",
        "¿De cuántas formas distintas puede ir sin recorrer ni un centímetro de más?",
        ("0 si no se puede llegar; el resultado es menor que 2³¹.", "muted"),
    ]), "Lucas va en bici de su casa, la intersección uno, al colegio, que está en la última. Siempre por un camino de distancia mínima, "
        "pero le aburre repetir, así que quiere saber de cuántas formas distintas puede ir. Las calles se recorren en los dos sentidos. "
        "Si no se puede llegar, la respuesta es cero.", 0))

    # idea de contar
    s = Slide("Dijkstra que cuenta: un vector más")
    s.text((70, 100), "formas[v] = número de caminos de longitud mínima de 1 a v", size=26, bold=True, color="gold")
    filas = [("d  <  dist[w]", "más corto que todo lo visto", "dist[w] = d;   formas[w] = formas[v];", "green"),
             ("d  ==  dist[w]", "otra forma igual de buena", "formas[w] += formas[v];", "blue"),
             ("d  >  dist[w]", "no sirve", "no se hace nada", "dim")]
    for i, (c1, c2, c3, col) in enumerate(filas):
        y = 170 + i * 120
        s.box(70, y, 1140, 100, border=col)
        s.text((100, y + 20), c1, size=28, mono=True, bold=True, color=col if col != "dim" else "muted")
        s.text((100, y + 62), c2, size=20, color="muted")
        s.text((520, y + 36), c3, size=26, mono=True)
    s.text((70, 545), "con d = dist[v] + valor de la calle.   Inicio:  dist[0] = 0  y  formas[0] = 1  (no moverse).", size=22, color="text")
    segs.append((s, "La idea: un segundo vector, formas, que guarda para cada intersección cuántos caminos mínimos llegan hasta ella. "
                    "Al relajar una calle de v a w calculamos d, la distancia por v. Si d es menor que la distancia de w, hemos encontrado algo más corto: "
                    "todos los caminos anteriores dejan de valer y formas de w pasa a ser formas de v. "
                    "Si d es igual, hemos encontrado otra forma igual de buena, así que sumamos las de v. Y si es mayor, no se hace nada. "
                    "Al principio, la casa tiene una forma: no moverse.", 0))

    segs.append((ideas("¿Por qué formas[v] es definitivo?", [
        "Al sacar v de la cola, dist[v] ya es definitiva.",
        "Todo camino mínimo a v llega por un vecino u con dist[u] < dist[v] (las calles miden ≥ 1).",
        "Esos u se sacaron ANTES de la cola y ya sumaron su aportación a formas[v].",
        ("Por eso, al sacar v, formas[v] está completo y se puede propagar.", "gold"),
    ]), "¿Por qué podemos propagar formas de v cuando lo sacamos de la cola? Porque todos los caminos mínimos hasta v llegan por un vecino con distancia estrictamente menor, "
        "ya que las calles miden al menos uno. Esos vecinos salieron antes de la cola y ya sumaron su aportación. Así que formas de v está completo.", 0))

    s = Slide("Calles de doble sentido")
    s.box(60, 100, 1160, 250, "al construir el grafo")
    s.text((100, 160), "g.ponArista({u, v, l});   // u → v", size=26, mono=True, color="gold")
    s.text((100, 215), "g.ponArista({v, u, l});   // v → u", size=26, mono=True, color="gold")
    s.wrap(100, 275, 1080, "Cada calle son DOS aristas dirigidas en el DigrafoValorado. Así Dijkstra sirve tal cual.", size=22, color="text")
    s.wrap(60, 400, 1160, "N = 1: casa y colegio coinciden, hay una única forma (no moverse): formas[0] = 1 ya es la respuesta.", size=22, color="text", center=True)
    s.wrap(60, 450, 1160, "Sin camino: formas[N-1] se queda en 0.   Se usa unsigned long long para que el desbordamiento de otros vértices no estropee la respuesta.", size=22, color="muted", center=True)
    segs.append((s, "Como las calles se recorren en los dos sentidos, cada calle se añade como dos aristas dirigidas. "
                    "Si solo hay una intersección, la casa es el colegio y hay una forma, no moverse. Si no se llega, formas se queda en cero. "
                    "Usamos unsigned long long para que el número de caminos de otras intersecciones, que puede ser enorme, no estropee la respuesta.", 0))

    s = Slide("El código", "EJ_07-2.cpp")
    s.code(24, 84, 700, 520, CODE, hl=set(L_LT) | set(L_EQ), title="Dijkstra dentro de resuelveCaso")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["Dijkstra de siempre: pop del más cercano y relajar sus aristas.",
                              "d es la distancia por v.",
                              "Si mejora: sustituimos dist y formas, update.",
                              "Si empata: sumamos formas[v] a formas[w].",
                              "Al final, formas[N-1]."], size=20, gap=16)
    segs.append((s, "En el código, es el Dijkstra de siempre con un cambio. Calculamos d. Si mejora, sustituimos la distancia y las formas, y hacemos update. "
                    "Si empata, sumamos las formas de v a las de w. Al final escribimos formas de la última intersección.", 0))

    pasos = traza(7, EDGES, 0, und=True, contar=True)
    n = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl, cap = set(L_INI), "dist[1] = 0, formas[1] = 1; la intersección 1 entra en la cola"
            nar = "Empezamos en la intersección uno: distancia cero y una forma de estar ahí. Entra en la cola."
        elif t == "saca":
            hl, cap = {L_POP}, f"Sale la intersección {v + 1}, dist = {p['dist'][v]}, formas = {p['formas'][v]}: definitivas"
            nar = f"Sacamos la intersección {v + 1}: distancia {p['dist'][v]}, con {p['formas'][v]} {'forma' if p['formas'][v] == 1 else 'formas'}. Ya son definitivas."
        else:
            w = p["w"]
            if t == "mejora":
                hl = {L_FOR, L_D} | set(L_LT)
                ant = "∞" if not FINITO(p["ant"]) else p["ant"]
                cap = f"{v + 1}–{w + 1}: d = {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: mejora, formas[{w + 1}] = formas[{v + 1}] = {p['formas'][v]}"
                nar = f"Calle de {v + 1} a {w + 1}: d es {p['nuevo']}, " + ("antes infinito" if not FINITO(p["ant"]) else f"antes {p['ant']}") + f". Mejora: las formas de {w + 1} pasan a ser {p['formas'][v]}."
            elif t == "empata":
                hl = {L_FOR, L_D} | set(L_EQ)
                cap = f"{v + 1}–{w + 1}: d = {p['nuevo']} = dist[{w + 1}]: otra forma, formas[{w + 1}] = {p['formas'][w]}"
                nar = f"Calle de {v + 1} a {w + 1}: d es {p['nuevo']}, igual que la distancia de {w + 1}. Otra forma igual de buena: sumamos, y ahora hay {p['formas'][w]}."
            else:
                hl = {L_FOR, L_D, L_LT[0]}
                cap = f"{v + 1}–{w + 1}: d = {p['nuevo']} > {p['dist'][w]}: no sirve"
                nar = f"Calle de {v + 1} a {w + 1}: d es {p['nuevo']}, mayor que {p['dist'][w]}. No sirve."
        segs.append((slide_paso(k, n, p, hl, cap), nar, 0))

    fin = pasos[-1]
    s = Slide("Resultado")
    s.box(40, 90, 620, 440, "los 4 caminos de longitud 40")
    pf = dict(fin, tipo="fin", v=None, cola=[], _formas=True)
    pl = {0: (90, 310), 1: (200, 190), 2: (200, 430), 3: (330, 310), 4: (450, 190), 5: (450, 430), 6: (590, 310)}
    dibuja_grafo(s, pl, EDGES, pf, dirigido=False, r=20, first=1)
    s.bullets(690, 110, 540, [
        "1→2→4→5→7", "1→2→4→7", "1→3→4→7", "1→3→4→5→7",
        ("formas[7] = 4", "gold"),
        "Ejemplo 2: no se llega a la 4 ⇒ 0.   Ejemplo 3: N = 1 ⇒ 1.",
    ], size=23, gap=12)
    segs.append((s, "El resultado es cuatro: uno, dos, cuatro, cinco, siete; uno, dos, cuatro, siete; uno, tres, cuatro, siete; y uno, tres, cuatro, cinco, siete. "
                    "En el segundo ejemplo no se llega, y escribimos cero. En el tercero, solo hay una intersección, y hay una forma.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(C log N) por caso, el de Dijkstra; contar no añade nada.",
        "Calles de doble sentido: dos ponArista por calle.",
        "Empate ⇒ SUMAR.   Mejora ⇒ SUSTITUIR.",
        "formas en unsigned long long (los de otros vértices pueden desbordar).",
        ("Las calles miden ≥ 1: con longitud 0 el argumento de «formas definitivas» fallaría.", "muted"),
    ]), "El coste es el de Dijkstra. Las dos cosas que hay que recordar: si empata, se suma, y si mejora, se sustituye.", 0))

    segs.append((cierre(NOMBRE, [
        "Contar caminos mínimos = Dijkstra + un vector formas[].",
        "Mejora: formas[w] = formas[v].   Empate: formas[w] += formas[v].",
        "Grafo no dirigido: cada calle son dos aristas dirigidas.",
        "N = 1 ⇒ 1.   Sin camino ⇒ 0.   Coste O(C log N).",
    ]), "Resumiendo: contamos los caminos mínimos con Dijkstra más un vector. Si mejora, sustituimos; si empata, sumamos.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-2_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-2_camino_al_cole.mp4")
        print(f"07-2: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
