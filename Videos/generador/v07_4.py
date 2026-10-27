"""Vídeo EJ 07-4 · La conferencia de paz"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07b_comun import traza, slide_paso, vectores, dibuja, INF

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-4/EJ_07-4.cpp"
NOMBRE = "La conferencia de paz"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 2: 6 aldeas en fila; galos {1, 5}, romanos {3}  (vértices 0..5)
ARCS = [(0, 1, 3), (1, 2, 5), (2, 3, 4), (3, 4, 2), (4, 5, 1)]
POS = {0: (730, 250), 1: (850, 160), 2: (980, 250), 3: (1090, 160), 4: (1160, 290), 5: (1220, 170)}
POS = {0: (730, 230), 1: (840, 140), 2: (960, 230), 3: (1070, 140), 4: (1170, 230), 5: (1170, 340)}
GALOS, ROMANOS = [0, 4], [2]
BASE_G = {0: "blue", 4: "blue"}
BASE_R = {2: "red"}
fmt = lambda d: "∞" if d >= INF else str(d)

L_INI = find_line(CPP, "for (int o : origenes) {")
L_DIST = find_line(CPP, "dist[o] = 0;")
L_PUSH = find_line(CPP, "pq.update(o, 0);")
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_FOR = find_line(CPP, "for (auto a : g.ady(v)) {")
L_IF = find_line(CPP, "if (dist[w] > dist[v] + a.valor()) {")
L_SET = [find_line(CPP, "dist[w] = dist[v] + a.valor();"), find_line(CPP, "pq.update(w, dist[w]);")]
L_NEU = find_line(CPP, "if (bando[v] != 0) continue;")
L_DIF = find_line(CPP, "int dif = abs(dGalos[v] - dRomanos[v]);")
L_MEJ = find_line(CPP, "if (dif < difMejor)")
CODE_D = [(n, t) for n, t in code_lines(CPP, find_line(CPP, "vector<int> distanciaMinima"), find_line(CPP, "return dist;"), maxc=60) if t.strip()]
CODE_E = [(n, t) for n, t in code_lines(CPP, find_line(CPP, "vector<int> dGalos"), find_line(CPP, "cout << mejor + 1"), maxc=64) if t.strip()]


def traza_bando(titulo, srcs, base, nombre, segs, solo_clave=False):
    pasos = traza(6, ARCS, srcs, und=True)
    if solo_clave:
        pasos = [p for p in pasos if p["tipo"] in ("ini", "saca", "mejora")]
    N = len(pasos)
    for k, p in enumerate(pasos, 1):
        t, v = p["tipo"], p.get("v")
        if t == "ini":
            hl = {L_INI, L_DIST, L_PUSH}
            cap = f"Todas las aldeas {nombre} entran a la vez con dist = 0"
            nar = f"Metemos a la vez todas las aldeas {nombre}, cada una con distancia cero."
        elif t == "saca":
            hl, cap = {L_POP}, f"Sale la aldea {v + 1}, dist = {p['dist'][v]}: definitiva"
            nar = f"Sacamos la aldea {v + 1}, con distancia {p['dist'][v]}."
        elif t == "mejora":
            w = p["w"]
            hl = {L_FOR, L_IF} | set(L_SET)
            ant = "∞" if p["ant"] >= INF else p["ant"]
            cap = f"{v + 1}–{w + 1}: {p['dist'][v]} + {p['c']} = {p['nuevo']} < {ant}: mejora"
            nar = f"De la {v + 1} a la {w + 1}: {p['nuevo']}, mejor que " + ("infinito" if p["ant"] >= INF else str(p["ant"])) + "."
        else:
            w = p["w"]
            hl = {L_FOR, L_IF}
            cap = f"{v + 1}–{w + 1}: {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
            nar = f"De la {v + 1} a la {w + 1}: {p['nuevo']}, no mejora {p['dist'][w]}."
        s = slide_paso(titulo, "Dijkstra", CODE_D, "distanciaMinima()", hl, POS, ARCS, p, False, cap, fmt, 6, k, N,
                       base=base, gtitle=f"aldeas {nombre} a dist 0 (el camino mide el valor de cada línea)", etq="dist")
        segs.append((s, nar, 0))
    return pasos[-1]


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-4", TEMA),
             "La conferencia de paz. Hay que elegir una aldea neutral lo más equidistante posible de galos y romanos: dos Dijkstra con varios orígenes a la vez.", 0)]

    segs.append((ideas("El problema", [
        "N aldeas (hasta 100.000) unidas por caminos de doble sentido, longitud 1 a 1.000. El grafo es conexo.",
        "Unas aldeas son de los galos, otras de los romanos y el resto, neutrales.",
        "Elegir una aldea NEUTRAL cuya distancia a la aldea gala más cercana y a la romana más cercana se diferencien lo MENOS posible.",
        "Empate: la de índice menor.  Salida: el índice y la diferencia.",
        ("Se puede pasar por cualquier aldea, sea de quien sea.", "muted"),
    ]), "Tenemos aldeas unidas por caminos de doble sentido. Unas son de los galos, otras de los romanos y el resto neutrales. "
        "Hay que elegir una aldea neutral tal que la distancia a la aldea gala más cercana y a la romana más cercana se diferencien lo menos posible. "
        "Si hay empate, la de índice menor. Y se puede pasar por cualquier aldea.", 0))

    s = Slide("Cómo se plantea")
    s.bullets(70, 110, 1140, [
        "Para cada aldea necesitamos DOS números:",
        ("dGalos[v] = distancia a la aldea gala MÁS CERCANA", "gold"),
        ("dRomanos[v] = distancia a la aldea romana MÁS CERCANA", "gold"),
        "Es un Dijkstra con VARIOS orígenes: se meten todas las aldeas del bando en la cola con distancia 0.",
        "Es lo mismo que un vértice falso unido con coste 0 a todo el bando, pero sin construirlo.",
        "Después, recorrer las aldeas neutrales en orden y quedarse con la de menor |dGalos − dRomanos|.",
    ], size=24, gap=20)
    segs.append((s, "Para cada aldea necesitamos dos números: la distancia a la aldea gala más cercana, y la distancia a la romana más cercana. "
                    "Cada uno se calcula con un Dijkstra con varios orígenes: metemos todas las aldeas del bando en la cola, con distancia cero. "
                    "Es lo mismo que añadir un vértice falso unido con coste cero a todo el bando, pero sin construirlo. "
                    "Después recorremos las aldeas neutrales en orden y nos quedamos con la de menor diferencia.", 0))

    s = Slide("El código: Dijkstra con varios orígenes", "EJ_07-4.cpp")
    s.code(24, 84, 700, 520, CODE_D, hl={L_INI, L_DIST, L_PUSH, L_POP}, title="distanciaMinima()")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["Recibe la LISTA de orígenes del bando.",
                              "Todos arrancan con dist = 0 y entran en la cola.",
                              "Lo demás es el Dijkstra de siempre.",
                              "Se llama dos veces: galos y romanos."], size=20, gap=16)
    segs.append((s, "El código recibe la lista de orígenes del bando. Todos arrancan con distancia cero y entran en la cola. Lo demás es el Dijkstra de siempre. "
                    "Lo llamamos dos veces, una para los galos y otra para los romanos.", 0))

    s = Slide("El ejemplo 2", TEMA)
    s.box(40, 100, 700, 440, "6 aldeas · galos {1, 5} · romanos {3}")
    from v07_comun import etiquetas
    pl = {0: (100, 320), 1: (230, 200), 2: (370, 320), 3: (500, 200), 4: (620, 320), 5: (620, 460)}
    ns = {0: ("blue", "node_t", None), 4: ("blue", "node_t", None), 2: ("red", "node_t", None)}
    pl = {0: (110, 340), 1: (230, 210), 2: (360, 340), 3: (490, 210), 4: (610, 340), 5: (610, 470)}
    s.graph(pl, [(a, b) for a, b, c in ARCS], ns=ns, r=24, labels=[str(i + 1) for i in range(6)])
    etiquetas(s, pl, ARCS)
    s.bullets(770, 130, 470, [("azul: aldeas galas (1 y 5)", "blue"), ("rojo: aldea romana (3)", "red"),
                              "gris: neutrales (2, 4 y 6)",
                              "Los números de las líneas son las longitudes."], size=21, gap=16)
    segs.append((s, "Vamos al ejemplo dos. Seis aldeas en fila. Los galos controlan la uno y la cinco, los romanos la tres, y las neutrales son la dos, la cuatro y la seis.", 0))

    pg = traza_bando("Dijkstra desde los galos", GALOS, BASE_G, "galas", segs)
    pr = traza_bando("Dijkstra desde los romanos", ROMANOS, BASE_R, "romanas", segs, solo_clave=True)

    # tabla final
    s = Slide("Elegir la aldea neutral", TEMA)
    s.code(24, 84, 600, 300, CODE_E[-8:], hl={L_NEU, L_DIF, L_MEJ}, title="recorrer las neutrales")
    s.box(644, 84, 612, 300, "resultado del ejemplo 2")
    dG, dR = pg["dist"], pr["dist"]
    neu = [1, 3, 5]
    s.cells(664, 120, "aldea", [i + 1 for i in range(6)], idx=False, cw=50)
    s.cells(664, 168, "dGalos", dG, idx=False, cw=50)
    s.cells(664, 216, "dRomanos", dR, idx=False, cw=50,)
    s.cells(664, 264, "|dif|", ["·" if i not in neu else abs(dG[i] - dR[i]) for i in range(6)], idx=False, cw=50,
            colors={1: "gold_d", 3: "gold_d"} if False else {})
    s.text((664, 330), "neutrales: 2, 4 y 6 (la 1, 3 y 5 son de un bando)", size=18, color="muted")
    s.box(24, 400, 1232, 200, "comparación")
    s.text((60, 440), f"aldea 2: |{dG[1]} − {dR[1]}| = {abs(dG[1] - dR[1])}      aldea 4: |{dG[3]} − {dR[3]}| = {abs(dG[3] - dR[3])}      aldea 6: |{dG[5]} − {dR[5]}| = {abs(dG[5] - dR[5])}", size=26, mono=True)
    s.text((60, 500), "Empatan la 2 y la 4 con diferencia 2; gana la de índice menor:", size=24)
    s.text((60, 545), "2 2", size=44, bold=True, color="gold")
    segs.append((s, f"Ahora recorremos las aldeas neutrales en orden. La dos tiene distancia {dG[1]} a los galos y {dR[1]} a los romanos: diferencia {abs(dG[1] - dR[1])}. "
                    f"La cuatro, {dG[3]} y {dR[3]}: también {abs(dG[3] - dR[3])}. Y la seis, {dG[5]} y {dR[5]}: diferencia {abs(dG[5] - dR[5])}. "
                    "Empatan la dos y la cuatro, y como el signo menor estricto se queda con la primera, que es la de índice menor, la respuesta es dos dos.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(C log N) por caso: dos Dijkstra.",
        "Solo se eligen aldeas NEUTRALES, pero los caminos pueden atravesar aldeas de cualquier bando.",
        "Con «<» estricto, al recorrer en orden creciente, el empate lo gana el índice menor.",
        "Camino de doble sentido: dos aristas dirigidas.",
        ("Distancias ≤ 10⁸: caben en int.", "muted"),
    ]), "El coste es el de dos Dijkstra, linealítmico en el número de caminos. Solo elegimos aldeas neutrales, pero los caminos pueden atravesar aldeas de cualquier bando. "
        "Con el menor estricto y recorriendo en orden creciente, el empate lo gana el índice menor. Y cada camino son dos aristas dirigidas.", 0))

    segs.append((cierre(NOMBRE, [
        "dGalos y dRomanos: dos Dijkstra con VARIOS orígenes (todo el bando a dist 0).",
        "Recorrer las aldeas neutrales en orden creciente.",
        "Quedarse con la de menor |dGalos − dRomanos| (con «<» estricto).",
        "Coste O(C log N).",
    ]), "Resumiendo: dos Dijkstra con varios orígenes, uno por bando. Después, recorrer las neutrales en orden y quedarse con la de menor diferencia. Coste, C log N.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-4_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-4_conferencia_de_paz.mp4")
        print(f"07-4: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
