"""Vídeo EJ 07-5 · ¿Cuál es el mejor camino?"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07b_comun import traza, slide_paso, vectores, dibuja, INF

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-5/EJ_07-5.cpp"
NOMBRE = "¿Cuál es el mejor camino?"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1 del enunciado (vértices 0..6 = intersecciones 1..7)
ARCS = [(0, 1, 10), (1, 2, 7), (2, 4, 10), (0, 3, 15), (3, 4, 15), (3, 5, 5), (4, 6, 4), (5, 6, 15)]
POS = {0: (730, 235), 1: (830, 130), 2: (1010, 130), 3: (880, 235), 4: (1130, 235), 5: (940, 340), 6: (1170, 340)}
ADD = lambda d, c: (d[0] + c, d[1] + 1)
fmt = lambda d: "∞" if d[0] >= INF else f"{d[0]}·{d[1]}"

L_INIT = find_line(CPP, "mejor[origen] = {0, 0};")
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_FOR = find_line(CPP, "for (auto a : g.ady(v)) {")
L_NUEVO = find_line(CPP, "Par nuevo = {mejor[v].first + a.valor(), mejor[v].second + 1};")
L_IF = find_line(CPP, "if (nuevo < mejor[w]) {")
L_SET = [find_line(CPP, "mejor[w] = nuevo;"), find_line(CPP, "pq.update(w, nuevo);")]
L_BFS = find_line(CPP, "calles[origen] = 0;")
L_BFSW = find_line(CPP, "if (calles[w] == -1) {")
L_RES = find_line(CPP, "cout << mejor[destino].first <<")
L_SIN = find_line(CPP, 'cout << "SIN CAMINO\\n";')
CODE_D = [(n, t) for n, t in code_lines(CPP, find_line(CPP, "// Dijkstra con prioridad"), find_line(CPP, "if (mejor[destino].first == INF) {") - 1, maxc=64) if t.strip()]
CODE_B = [(n, t) for n, t in code_lines(CPP, find_line(CPP, "// Anchura:"), L_RES, maxc=70) if t.strip()]


def anchura(n, arcs, o):
    adj = [[] for _ in range(n)]
    for a, b, c in arcs:
        adj[a].append(b)
        adj[b].append(a)
    d = [-1] * n
    d[o] = 0
    q = deque([o])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if d[w] == -1:
                d[w] = d[v] + 1
                q.append(w)
    return d


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-5", TEMA),
             "¿Cuál es el mejor camino? ¿El camino más corto en distancia es también el que pasa por menos calles? Dijkstra con dos criterios y un recorrido en anchura.", 0)]

    segs.append((ideas("El problema", [
        "Ciudad con N intersecciones (hasta 20.000) y C calles de doble sentido, longitud 1 a 5.000.",
        "K ≤ 10 consultas por caso: origen y destino distintos.",
        "Para cada una: la distancia mínima y",
        ("SI si algún camino de esa distancia usa el MENOR número de calles posible; NO si no; SIN CAMINO si no se llega.", "gold"),
        ("Tras cada caso, una línea ---.  La entrada termina con el fichero.", "muted"),
    ]), "Tenemos una ciudad con intersecciones y calles de doble sentido. Para cada consulta, con un origen y un destino, hay que escribir la distancia mínima, "
        "y sí, si algún camino de esa distancia usa además el menor número de calles posible entre los dos puntos; no, si no; o sin camino. Después de cada caso, una línea de guiones.", 0))

    s = Slide("Cómo se plantea")
    s.bullets(70, 110, 1140, [
        "Dos preguntas distintas desde el origen:",
        ("1.  ¿Cuántas calles hay como MÍNIMO, sin mirar la longitud?  →  recorrido en ANCHURA", "gold"),
        ("2.  ¿Distancia mínima y, entre esos caminos, menos calles?  →  Dijkstra con prioridad (distancia, calles)", "gold"),
        "La pareja se compara en orden lexicográfico: primero la distancia, y a igualdad, las calles.",
        "Respuesta:  SI  si  pasos[destino] == calles[destino];  NO  si  pasos > calles.",
    ], size=24, gap=22)
    segs.append((s, "Hay que contestar dos preguntas distintas desde el origen. Primera: cuántas calles hacen falta como mínimo, sin mirar la longitud. Eso es un recorrido en anchura. "
                    "Segunda: cuál es la distancia mínima y, entre los caminos que la consiguen, el que menos calles usa. Eso es Dijkstra, con una pareja como prioridad: primero la distancia, y a igualdad, las calles. "
                    "Si las calles del mejor camino en distancia coinciden con el mínimo de calles, respondemos sí. Si son más, no.", 0))

    s = Slide("El código: Dijkstra con pareja", "EJ_07-5.cpp")
    s.code(24, 84, 700, 520, CODE_D, hl={L_NUEVO, L_IF} | set(L_SET), title="Dijkstra con (distancia, calles)")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["mejor[v] = (distancia, calles).",
                              "Al recorrer una calle se suma (valor, 1).",
                              "pair compara primero la distancia y, si empatan, las calles: justo lo que queremos.",
                              "Sumar lo mismo a dos parejas conserva el orden: Dijkstra sigue siendo correcto."], size=20, gap=16)
    segs.append((s, "En el código, mejor de v es una pareja de distancia y calles. Al recorrer una calle sumamos su valor y una calle más. "
                    "La comparación de parejas mira primero la distancia y, si empatan, las calles, que es justo lo que queremos. "
                    "Y como sumar lo mismo a dos parejas no cambia cuál es la menor, Dijkstra sigue siendo correcto.", 0))

    s = Slide("El ejemplo 1: consulta 1 → 5", TEMA)
    s.box(40, 100, 700, 440, "7 intersecciones y 8 calles")
    pl = {0: (100, 330), 1: (200, 190), 2: (380, 190), 3: (260, 330), 4: (520, 330), 5: (320, 470), 6: (560, 470)}
    from v07_comun import etiquetas
    s.graph(pl, [(a, b) for a, b, c in ARCS], r=24, labels=[str(i + 1) for i in range(7)])
    etiquetas(s, pl, ARCS)
    s.bullets(770, 130, 470, ["Camino 1→2→3→5:  longitud 27, 3 calles.",
                              "Camino 1→4→5:  longitud 30, 2 calles.",
                              ("El más corto en distancia NO es el de menos calles.", "gold")], size=21, gap=16)
    segs.append((s, "El ejemplo uno. Del punto uno al cinco, el camino uno, dos, tres, cinco mide veintisiete y pasa por tres calles. El camino uno, cuatro, cinco mide treinta pero solo pasa por dos calles. "
                    "El más corto en distancia no es el de menos calles.", 0))

    # Dijkstra: solo los pasos que cambian algo
    pasos = traza(7, ARCS, [0], und=True, add=ADD, zero=(0, 0), inf=(INF, INF))
    pasos = [p for p in pasos if p["tipo"] in ("ini", "saca", "mejora")]
    N = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl, cap = {L_INIT}, "mejor[1] = (0, 0): empezamos en la intersección 1"
            nar = "Empezamos en la intersección uno, con distancia cero y cero calles."
        elif t == "saca":
            d = p["dist"][v]
            hl, cap = {L_POP}, f"Sale la {v + 1}: distancia {d[0]} con {d[1]} calles"
            nar = f"Sacamos la intersección {v + 1}: distancia {d[0]}, con {d[1]} calles."
        else:
            w = p["w"]
            hl = {L_FOR, L_NUEVO, L_IF} | set(L_SET)
            nu = p["nuevo"]
            cap = f"{v + 1}→{w + 1}: nuevo = ({nu[0]}, {nu[1]}) mejora a {fmt(p['ant']).replace('·', ', ')}"
            nar = f"De la {v + 1} a la {w + 1}: distancia {nu[0]} con {nu[1]} calles. Mejora."
        s = slide_paso("Dijkstra con (distancia, calles) desde la 1", "ejemplo 1", CODE_D, "Dijkstra con (distancia, calles)", hl,
                       POS, ARCS, p, False, cap, fmt, 7, k, N, cw=52, gtitle="distancia·calles bajo cada nodo", etq="mejor")
        segs.append((s, nar, 0))
    fin = pasos[-1]
    dist5, calles5 = fin["dist"][4]

    # anchura
    cal = anchura(7, ARCS, 0)
    s = Slide("Recorrido en anchura: menos calles posible", "EJ_07-5.cpp")
    s.code(24, 84, 640, 300, CODE_B[:16], hl={L_BFS, L_BFSW}, title="anchura desde el origen")
    s.box(684, 84, 572, 310, "calles mínimas desde la 1 (sin mirar la longitud)")
    colores = {0: "green", 1: "gold", 3: "gold", 2: "purple", 4: "purple", 5: "purple", 6: "blue"}
    ns = {u: (colores[cal[u]] if cal[u] in colores else "node", "node_t", None) for u in range(7)}
    s.graph(POS, [(a, b) for a, b, c in ARCS], ns=ns, r=22, labels=[str(i + 1) for i in range(7)],
            under={u: str(cal[u]) for u in range(7)})
    from v07_comun import etiquetas
    etiquetas(s, POS, ARCS)
    s.box(24, 400, 1232, 204, "comparar")
    s.text((60, 440), f"Dijkstra:   distancia {dist5} con {calles5} calles", size=26, mono=True)
    s.text((60, 490), f"Anchura:    como mínimo {cal[4]} calles", size=26, mono=True)
    s.text((60, 545), f"{calles5} ≠ {cal[4]}   →", size=28, mono=True, color="muted")
    s.text((300, 540), f"{dist5} NO", size=44, bold=True, color="gold")
    segs.append((s, f"Ahora el recorrido en anchura desde la uno, que cuenta calles sin mirar la longitud: al cinco se llega con {cal[4]} calles como mínimo. "
                    f"Dijkstra nos dio distancia {dist5} con {calles5} calles. Como {calles5} es mayor que {cal[4]}, el camino más corto en distancia no es de los de menos calles: escribimos {dist5} no.", 0))

    # segunda consulta
    p2 = traza(7, ARCS, [5], und=True, add=ADD, zero=(0, 0), inf=(INF, INF))[-1]
    d2, c2 = p2["dist"][4]
    cal2 = anchura(7, ARCS, 5)[4]
    s = Slide("Consulta 6 → 5", TEMA)
    s.box(40, 100, 600, 440, "segunda consulta del ejemplo")
    s.text((70, 150), "Caminos de 6 a 5:", size=24, bold=True)
    s.text((70, 200), "6→7→5:   15 + 4 = 19,   2 calles", size=24, mono=True, color="gold")
    s.text((70, 250), "6→4→5:   5 + 15 = 20,   2 calles", size=24, mono=True)
    s.text((70, 320), f"Dijkstra:  ({d2}, {c2})", size=26, mono=True)
    s.text((70, 370), f"Anchura:   {cal2} calles como mínimo", size=26, mono=True)
    s.text((70, 440), f"{c2} = {cal2}   →   {d2} SI", size=40, bold=True, color="gold")
    s.box(660, 100, 580, 440, "ejemplo 2 del enunciado")
    s.text((690, 150), "Intersecciones 1, 2, 3 conectadas; 4 y 5 aparte.", size=20)
    s.text((690, 210), "1 → 2:  una calle, 5 SI", size=24, mono=True)
    s.text((690, 260), "1 → 5:  no hay camino: SIN CAMINO", size=24, mono=True, color="red")
    s.text((690, 330), "Después de cada caso:  ---", size=24, mono=True, color="muted")
    segs.append((s, f"En la segunda consulta, del seis al cinco, el mejor camino mide {d2} y usa {c2} calles, que es el mínimo posible: escribimos {d2} sí. "
                    "En el segundo caso, del uno al cinco no hay camino, y escribimos sin camino. Y después de cada caso, la línea de guiones.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(K · C log N) por caso: un Dijkstra y una anchura por consulta.",
        "Sumar (c, 1) conserva el orden lexicográfico: Dijkstra con pareja es correcto.",
        "Entre caminos de igual distancia, pasos[v] es el que menos calles usa.",
        "SIN CAMINO va solo, sin distancia.   --- tras cada caso, aunque todo sea SIN CAMINO.",
        ("Intersecciones desde 1: restar 1 al leer.", "muted"),
    ]), "El coste es K por C por logaritmo de N, porque hacemos un Dijkstra y una anchura por consulta. Sumar valor y una calle conserva el orden, así que Dijkstra con pareja es correcto. "
        "Sin camino se escribe solo, sin distancia, y los guiones van después de cada caso.", 0))

    segs.append((cierre(NOMBRE, [
        "Anchura  ⇒  mínimo de calles posible (sin mirar longitud).",
        "Dijkstra con prioridad (distancia, calles)  ⇒  menos calles entre los más cortos.",
        "SI  si pasos[destino] == calles[destino];  NO  si no;  SIN CAMINO si no se llega.",
        "Coste O(K · C log N).",
    ]), "Resumiendo: una anchura para el mínimo de calles y un Dijkstra con pareja de distancia y calles. Si coinciden, sí; si no, no; y si no se llega, sin camino.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-5_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-5_mejor_camino.mp4")
        print(f"07-5: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
