"""Vídeo EJ 07-6 · Repartiendo paquetes"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07b_comun import traza, slide_paso, vectores, dibuja, INF
from v07_comun import etiquetas

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-6/EJ_07-6.cpp"
NOMBRE = "Repartiendo paquetes"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1: 4 casas (vértices 0..3), oficina en la casa 1 (vértice 0); paquetes a 2, 3, 4
ARCS = [(0, 1, 5), (1, 2, 2), (2, 0, 8), (0, 3, 2), (3, 0, 3)]
POS = {0: (760, 235), 1: (960, 130), 2: (1160, 235), 3: (960, 345)}
fmt = lambda d: "∞" if d >= INF else str(d)

L_DIJ = find_line(CPP, "vector<long long> dijkstra(")
L_INI = find_line(CPP, "dist[origen] = 0;")
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_FOR = find_line(CPP, "for (auto a : g.ady(v)) {")
L_IF = find_line(CPP, "if (dist[w] > dist[v] + a.valor()) {")
L_SET = [find_line(CPP, "dist[w] = dist[v] + a.valor();"), find_line(CPP, "pq.update(w, dist[w]);")]
L_IDA = find_line(CPP, "vector<long long> ida = dijkstra(g, oficina);")
L_VUELTA = find_line(CPP, "vector<long long> vuelta = dijkstra(g.inverso(), oficina);")
L_SUMA = find_line(CPP, "else total += ida[d] + vuelta[d];")
L_IMP = find_line(CPP, "if (ida[d] == INF || vuelta[d] == INF) posible = false;")
L_OUT = find_line(CPP, 'else cout << "Imposible\\n";')
CODE_D = [(n, t) for n, t in code_lines(CPP, L_DIJ, find_line(CPP, "return dist;"), maxc=60) if t.strip()]
CODE_R = [(n, t) for n, t in code_lines(CPP, L_IDA - 1, L_OUT, maxc=64) if t.strip()]


def traza_dij(titulo, corner, flip, segs, cap0, solo_clave=False):
    arcs = [(b, a, c) for a, b, c in ARCS] if flip else ARCS
    pasos = traza(4, arcs, [0], und=False)
    if solo_clave:
        pasos = [p for p in pasos if p["tipo"] in ("ini", "saca", "mejora")]
    N = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl, cap = {L_INI}, cap0
            nar = "Empezamos en la oficina: distancia cero."
        elif t == "saca":
            hl, cap = {L_POP}, f"Sale la casa {v + 1}: dist = {p['dist'][v]}"
            nar = f"Sacamos la casa {v + 1}, con distancia {p['dist'][v]}."
        elif t == "mejora":
            w = p["w"]
            hl = {L_FOR, L_IF} | set(L_SET)
            ant = "∞" if p["ant"] >= INF else p["ant"]
            cap = f"{v + 1}→{w + 1}: {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: mejora"
            nar = f"De la {v + 1} a la {w + 1}: {p['nuevo']}. Mejora."
        else:
            w = p["w"]
            hl = {L_FOR, L_IF}
            cap = f"{v + 1}→{w + 1}: {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
            nar = f"De la {v + 1} a la {w + 1}: {p['nuevo']}, no mejora."
        s = slide_paso(titulo, corner, CODE_D, "dijkstra()", hl, POS, ARCS, p, True, cap, fmt, 4, k, N,
                       flip=flip, gtitle="el grafo INVERSO (flechas al revés)" if flip else "el grafo (esfuerzo de cada conexión)")
        segs.append((s, nar, 0))
    return pasos[-1]


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-6", TEMA),
             "Repartiendo paquetes. Ida y vuelta por cada paquete: dos Dijkstra desde la oficina, uno en el grafo y otro en el grafo inverso.", 0)]

    segs.append((ideas("El problema", [
        "Comarca con N casas (hasta 100.000) y C conexiones DIRIGIDAS con esfuerzo 1 a 10.000.",
        "La oficina está en la casa O; hay P paquetes, cada uno con su casa destino (puede repetirse).",
        "Un paquete cada vez: de la oficina al destino y VUELTA a la oficina, por rutas que pueden ser distintas.",
        ("Esfuerzo mínimo total, o Imposible.", "gold"),
        ("El orden de reparto es libre.", "muted"),
    ]), "Tenemos casas unidas por conexiones dirigidas, cada una con su esfuerzo. La oficina está en una casa, y hay paquetes con sus destinos. "
        "El repartidor lleva un paquete cada vez: va de la oficina al destino, y vuelve a la oficina, por rutas que pueden ser distintas. "
        "Hay que dar el esfuerzo mínimo total, o imposible. Y el orden de reparto es libre.", 0))

    s = Slide("Cómo se plantea")
    s.bullets(70, 110, 1140, [
        "El orden no importa: cada paquete es un viaje independiente, ida + vuelta.",
        ("coste del paquete a la casa d  =  dist(O → d)  +  dist(d → O)", "gold"),
        "dist(O → d): un Dijkstra desde O en el grafo.",
        "dist(d → O): un Dijkstra desde O en el grafo INVERSO (con las flechas al revés).",
        "Un camino de d a O en el grafo es un camino de O a d en el inverso.",
        ("Solo DOS Dijkstra para los P paquetes, no uno por paquete.", "gold"),
    ], size=24, gap=20)
    segs.append((s, "El orden no importa: cada paquete es un viaje independiente, con coste de ida más coste de vuelta. "
                    "La ida es la distancia de la oficina al destino, un Dijkstra desde la oficina. La vuelta es la distancia del destino a la oficina. "
                    "Para calcular esa con un solo Dijkstra, damos la vuelta a todas las flechas: un camino del destino a la oficina es un camino de la oficina al destino en el grafo inverso. "
                    "Así hacen falta solo dos Dijkstra para todos los paquetes.", 0))

    s = Slide("El código", "EJ_07-6.cpp")
    s.code(24, 84, 700, 520, CODE_R, hl={L_IDA, L_VUELTA, L_SUMA, L_IMP, L_OUT}, title="resuelveCaso()")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["ida = Dijkstra desde la oficina en g.",
                              "vuelta = Dijkstra desde la oficina en g.inverso().",
                              "Por cada destino: si alguna distancia es INF, Imposible.",
                              "Si no, total += ida[d] + vuelta[d].",
                              "long long: la suma puede crecer."], size=20, gap=16)
    segs.append((s, "En el código, ida es el Dijkstra desde la oficina en el grafo, y vuelta, el Dijkstra desde la oficina en el grafo inverso. "
                    "Para cada destino, si alguna de las dos distancias es infinita, el reparto es imposible. Si no, sumamos ida más vuelta al total.", 0))

    s = Slide("El ejemplo 1", TEMA)
    s.box(40, 100, 700, 440, "4 casas · oficina en la 1 · paquetes a 2, 3 y 4")
    pl = {0: (120, 330), 1: (330, 200), 2: (560, 330), 3: (330, 470)}
    s.dgraph(pl, [(a, b) for a, b, c in ARCS], r=26, labels=["1", "2", "3", "4"],
             ns={0: ("gold", "node_t", None)}, elabels={(a, b): (str(c), "muted") for a, b, c in ARCS})
    s.bullets(770, 130, 470, ["Casa 1 = oficina (en dorado).",
                              "A la casa 2 se va por 1→2, pero se vuelve por 2→3→1.",
                              "Hay conexiones solo en un sentido: ida y vuelta pueden costar distinto."], size=21, gap=16)
    segs.append((s, "Ejemplo uno. La oficina está en la casa uno, y hay un paquete para cada una de las otras tres casas. "
                    "A la casa dos se va directamente, pero para volver hay que pasar por la tres. Las conexiones van en un solo sentido, así que ida y vuelta pueden costar distinto.", 0))

    ida = traza_dij("Ida: Dijkstra desde la oficina en el grafo", "ida", False, segs, "dist[oficina] = 0")
    vuelta = traza_dij("Vuelta: Dijkstra desde la oficina en el INVERSO", "vuelta", True, segs, "dist[oficina] = 0 (grafo inverso)", solo_clave=True)

    di, dv = ida["dist"], vuelta["dist"]
    s = Slide("Sumar los paquetes", TEMA)
    s.code(24, 84, 600, 260, CODE_R[-9:], hl={L_SUMA, L_IMP}, title="por cada paquete")
    s.box(644, 84, 612, 260, "ida y vuelta de cada casa")
    s.cells(664, 120, "casa", [1, 2, 3, 4], idx=False, cw=60)
    s.cells(664, 168, "ida", di, idx=False, cw=60)
    s.cells(664, 216, "vuelta", dv, idx=False, cw=60)
    s.cells(664, 264, "total", [di[i] + dv[i] for i in range(4)], idx=False, cw=60)
    s.box(24, 360, 1232, 244, "suma de los tres paquetes (casas 2, 3 y 4)")
    tot = sum(di[i] + dv[i] for i in (1, 2, 3))
    s.text((60, 410), f"casa 2:  {di[1]} + {dv[1]} = {di[1] + dv[1]}      casa 3:  {di[2]} + {dv[2]} = {di[2] + dv[2]}      casa 4:  {di[3]} + {dv[3]} = {di[3] + dv[3]}", size=24, mono=True)
    s.text((60, 470), f"{di[1] + dv[1]} + {di[2] + dv[2]} + {di[3] + dv[3]} = {tot}", size=34, mono=True, color="gold", bold=True)
    s.text((60, 530), "Si algún destino tuviera INF en ida o en vuelta:  Imposible.", size=22, color="muted")
    segs.append((s, f"Sumamos para cada paquete la ida y la vuelta. La casa dos: {di[1]} más {dv[1]}, {di[1] + dv[1]}. La tres: {di[2]} más {dv[2]}, {di[2] + dv[2]}. La cuatro: {di[3]} más {dv[3]}, {di[3] + dv[3]}. "
                    f"En total, {tot}. Si algún destino tuviera infinito en la ida o en la vuelta, el reparto sería imposible.", 0))

    s = Slide("El ejemplo 2: Imposible", TEMA)
    s.box(40, 100, 600, 440, "4 casas · conexiones 1→3, 3→1, 3→4 · oficina 1 · paquetes a 2 y 3")
    pl = {0: (120, 330), 1: (300, 190), 2: (330, 470), 3: (560, 330)}
    E2 = [(0, 2), (2, 0), (2, 3)]
    s.dgraph(pl, E2, r=26, labels=["1", "2", "3", "4"], ns={0: ("gold", "node_t", None), 1: ("red", "node_t", None)})
    s.text((70, 560), "La casa 2 no tiene ninguna conexión.", size=22, color="red")
    s.bullets(670, 130, 560, ["ida[2] = INF  y  vuelta[2] = INF.",
                              "Aunque el paquete de la casa 3 sí se podría repartir,",
                              ("basta UN paquete imposible para que el reparto lo sea.", "gold"),
                              "Salida:   Imposible"], size=22, gap=18)
    segs.append((s, "En el ejemplo dos, la casa dos no tiene ninguna conexión. Su distancia de ida y de vuelta es infinita, así que el paquete no se puede entregar, "
                    "y basta un solo paquete imposible para que todo el reparto lo sea. Escribimos imposible.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(C log N) por caso (dos Dijkstra) + O(P).",
        "g.inverso() construye el grafo con todas las aristas dadas la vuelta.",
        "Una casa repetida en los destinos se suma varias veces.",
        "Aristas repetidas y bucles no molestan a Dijkstra.",
        ("Comprobar Imposible para TODOS los destinos antes de escribir.", "gold"),
    ]), "El coste es el de dos Dijkstra más recorrer los paquetes. El grafo inverso se construye con todas las aristas dadas la vuelta. "
        "Si una casa se repite entre los destinos, se suma varias veces. Y hay que mirar todos los destinos antes de decidir si es imposible.", 0))

    segs.append((cierre(NOMBRE, [
        "Cada paquete cuesta ida + vuelta; el orden no importa.",
        "ida:  Dijkstra desde la oficina en g.   vuelta:  Dijkstra desde la oficina en g.inverso().",
        "Imposible si algún destino tiene INF en ida o en vuelta.",
        "Coste O(C log N): solo dos Dijkstra.",
    ]), "Resumiendo: cada paquete cuesta ida más vuelta. La ida es un Dijkstra desde la oficina y la vuelta, otro en el grafo inverso. Si algún destino es inalcanzable, imposible. Solo dos Dijkstra.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-6_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-6_repartiendo_paquetes.mp4")
        print(f"07-6: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
