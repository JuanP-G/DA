"""Vídeo EJ 07-1 · Navegando sin teclado"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C
from v07_comun import traza, dibuja_grafo, estado, etiquetas, FINITO

CPP = "../../7-Digrafos valorados y caminos minimos/EJ_07-1/EJ_07-1.cpp"
NOMBRE = "Navegando sin teclado"
TEMA = "Tema 7 · Dígrafos valorados y caminos mínimos"

# ejemplo 1 del enunciado: 4 páginas, cargas 10 5 15 8, enlaces (página origen, destino, tiempo)
CARGA = [10, 5, 15, 8]
EDGES = [(0, 1, 10), (0, 2, 20), (0, 3, 100), (1, 3, 20), (2, 3, 20)]
POS = {0: (750, 270), 1: (960, 170), 2: (960, 350), 3: (1170, 270)}
EFECTIVO = {k: c + CARGA[b] for k, (a, b, c) in enumerate(EDGES)}      # t + carga[w]

L_INI = [find_line(CPP, "dist[0] = carga[0];"), find_line(CPP, "pq.push(0, dist[0]);")]
L_POP = find_line(CPP, "int v = pq.top().elem; pq.pop();")
L_BRK = find_line(CPP, "if (v == N - 1) break;")
L_FOR = find_line(CPP, "for (auto a : g.ady(v))")
L_IF = find_line(CPP, "if (dist[w] > dist[v] + a.valor())")
L_SET = [find_line(CPP, "dist[w] = dist[v] + a.valor();"), find_line(CPP, "pq.update(w, dist[w]);")]
L_CONS = find_line(CPP, "g.ponArista({v, w, t + carga[w]});")
L_FIN = find_line(CPP, 'if (dist[N - 1] == INF)')
CODE = code_lines(CPP, find_line(CPP, "const int INF"), L_FIN + 1, maxc=70, skip=[(find_line(CPP, "const int INF") + 16, find_line(CPP, "const int INF") + 16)])
CODE = [(n, t) for n, t in CODE if t.strip()]


def slide_paso(k, n, paso, hl, cap):
    s = Slide("Ejecución · ejemplo 1: de la página 1 a la 4", f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="Dijkstra dentro de resuelveCaso")
    s.box(684, 84, 572, 310, "el digrafo (valor = enlace + carga de la página a la que llega)")
    k_hl = paso.get("k")
    dibuja_grafo(s, POS, EDGES, paso, dirigido=True, carga=CARGA, hl_edge=k_hl, etiq=EFECTIVO, first=1)
    s.box(684, 410, 572, 194, "estado")
    estado(s, 704, 436, paso, 4, first=1)
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 07-1", TEMA),
             "Navegando sin teclado. Un problema de caminos mínimos con dos tipos de coste: veamos cómo se plantea y cómo se ejecuta.", 0)]

    segs.append((ideas("El problema", [
        "Hay N páginas web (hasta 3.000) y M enlaces entre ellas, con sentido.",
        "Se empieza en la página 1 y se quiere llegar a la página N.",
        "Cada página tarda un tiempo en CARGAR; cada enlace, un tiempo en localizarse y pulsarse.",
        "Piden el tiempo mínimo, contando la carga de TODAS las páginas visitadas (también la 1 y la N), o IMPOSIBLE.",
    ]), "Tenemos páginas web con enlaces dirigidos. Empezamos en la página uno y queremos llegar a la última. "
        "Cada página tarda un tiempo en cargar, y cada enlace tarda un tiempo en encontrarlo y pulsarlo. "
        "Hay que dar el tiempo mínimo, contando la carga de todas las páginas por las que pasamos, incluida la primera y la última. "
        "Si no se puede llegar, escribimos imposible.", 0))

    # dos costes
    s = Slide("Dos tipos de coste: ¿cómo lo resolvemos?")
    s.box(40, 90, 620, 440, "ejemplo 1: cargas  10  5  15  8")
    paso0 = traza(4, EDGES, 0, carga=CARGA)[0]
    paso0 = dict(paso0, done=[False] * 4, cola=[], dist=[10 ** 9] * 4)
    pl = {0: (130, 310), 1: (330, 190), 2: (330, 430), 3: (560, 310)}
    dibuja_grafo(s, pl, EDGES, paso0, dirigido=True, carga=CARGA, first=1)
    s.bullets(690, 120, 540, [
        "Dijkstra solo sabe de costes en las ARISTAS.",
        ("Pero la carga está en los VÉRTICES.", "gold"),
        "Truco: la carga de una página se paga cada vez que se LLEGA a ella.",
        ("coste de v → w  =  enlace  +  carga[w]", "green"),
        "La página de partida se carga siempre: dist[origen] = carga[origen].",
    ], size=21, gap=14)
    segs.append((s, "Aquí hay dos tipos de coste: el de los enlaces, que está en las aristas, y el de carga, que está en los vértices. "
                    "Dijkstra solo sabe de costes en aristas. El truco es que la carga de una página se paga siempre que llegamos a ella. "
                    "Así que sumamos esa carga al valor de la arista que entra: el coste de ir de v a w es el enlace más la carga de w. "
                    "Y la página de partida, que se carga siempre, va en la distancia inicial.", 0))

    s = Slide("Las aristas con la carga sumada")
    s.box(40, 90, 620, 440, "coste efectivo = enlace + carga del destino")
    paso0 = dict(paso0)
    dibuja_grafo(s, pl, EDGES, paso0, dirigido=True, carga=CARGA, etiq=EFECTIVO, first=1)
    filas = [f"{a + 1} → {b + 1}:  {c} + {CARGA[b]} = {c + CARGA[b]}" for (a, b, c) in EDGES]
    s.bullets(690, 120, 540, filas, size=22, gap=10, mark="›")
    s.wrap(690, 360, 540, "En el código: g.ponArista({v, w, t + carga[w]}) y dist[0] = carga[0].", size=21, color="gold")
    segs.append((s, "En el ejemplo, la arista de uno a dos cuesta diez más cinco, quince. La de uno a tres, veinte más quince, treinta y cinco. "
                    "La de uno a cuatro, cien más ocho. Y las otras dos, veinte más ocho. En el código, la arista se crea con t más carga de w, "
                    "y la distancia inicial es la carga de la página uno.", 0))

    # código
    s = Slide("El código", "EJ_07-1.cpp")
    s.code(24, 84, 700, 520, CODE, hl={L_BRK, L_IF} | set(L_SET), title="Dijkstra dentro de resuelveCaso")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["dist[0] = carga[0]: la primera página se carga siempre.",
                              "IndexPQ: la cola de prioridad variable del tema 3.",
                              "Sacamos el de menor dist: ya es definitivo.",
                              "Relajar: si el camino por v es mejor, update.",
                              "Al sacar el destino se puede parar."], size=20, gap=16)
    segs.append((s, "En el código, partimos de la distancia cero con la carga de la primera página y la metemos en la cola de prioridad. "
                    "Mientras haya cola, sacamos el vértice de menor distancia, cuya distancia ya es definitiva, y relajamos sus aristas: "
                    "si el camino por él mejora la distancia de un vecino, la actualizamos con update. Si sacamos el destino, podemos parar.", 0))

    # traza
    pasos = traza(4, EDGES, 0, carga=CARGA, parar=3)
    n = len(pasos)
    for k, p in enumerate(pasos, 1):
        t = p["tipo"]
        v = p.get("v")
        if t == "ini":
            hl, cap = set(L_INI), "dist[1] = carga = 10 y la página 1 entra en la cola"
            nar = "Empezamos en la página uno. Hay que cargarla: su distancia es diez, y entra en la cola."
        elif t == "saca":
            hl, cap = {L_POP}, f"Sale de la cola la página {v + 1}, dist = {p['dist'][v]}: ya es definitiva"
            nar = f"Sacamos la página {v + 1}, con distancia {p['dist'][v]}. Esa distancia ya es definitiva."
        elif t == "fin":
            hl, cap = {L_POP, L_BRK}, f"Es el destino: dist = {p['dist'][v]}, paramos"
            nar = f"Es la última página, la {v + 1}: su distancia es {p['dist'][v]}. Esa es la respuesta, y paramos."
        else:
            w = p["w"]
            f = f"{p['dist'][v]} + {p['c']} + {CARGA[w]}"
            if t == "mejora":
                hl = {L_FOR, L_IF} | set(L_SET)
                ant = "∞" if not FINITO(p["ant"]) else p["ant"]
                cap = f"{v + 1} → {w + 1}: {f} = {p['nuevo']} < {ant}: mejora, dist[{w + 1}] = {p['nuevo']}"
                nar = (f"Relajamos la arista de {v + 1} a {w + 1}: {p['dist'][v]} más enlace {p['c']} más carga {CARGA[w]}, son {p['nuevo']}. "
                       + ("Antes era infinito: mejora." if not FINITO(p["ant"]) else f"Antes era {p['ant']}: mejora."))
            else:
                hl = {L_FOR, L_IF}
                cap = f"{v + 1} → {w + 1}: {f} = {p['nuevo']} ≥ {p['dist'][w]}: no mejora"
                nar = f"Arista de {v + 1} a {w + 1}: {p['nuevo']}, que no mejora el {p['dist'][w]} que ya teníamos."
        segs.append((slide_paso(k, n, p, hl, cap), nar, 0))

    # imposible
    s = Slide("El segundo ejemplo: IMPOSIBLE")
    s.box(40, 90, 620, 440, "enlaces 1→2, 1→3, 2→3 y 4→2")
    E2 = [(0, 1, 10), (0, 2, 20), (1, 2, 40), (3, 1, 10)]
    p2 = dict(traza(4, E2, 0, carga=CARGA)[-1])
    p2.update(tipo="fin", v=None, cola=[])
    dibuja_grafo(s, pl, E2, p2, dirigido=True, carga=CARGA, extra_ns={3: ("red", "node_t", None)}, first=1,
                 etiq={k: c + CARGA[b] for k, (a, b, c) in enumerate(E2)})
    s.bullets(690, 120, 540, [
        "Desde la 1 se alcanzan la 2 y la 3.",
        ("A la 4 no llega ningún enlace: dist sigue en INF.", "red"),
        "Se escribe IMPOSIBLE.",
    ], size=22, gap=16)
    segs.append((s, "En el segundo ejemplo, ningún enlace llega a la página cuatro. Su distancia se queda en infinito, y escribimos imposible.", 0))

    segs.append((ideas("Coste y detalles", [
        "Coste: O(M log N) por caso (Dijkstra con cola de prioridad variable).",
        "Todos los tiempos son ≥ 0: justo lo que exige Dijkstra.",
        "El mayor coste, 3.000 · 20.000 = 6·10⁷, cabe en un int.",
        "Las páginas van de 1 a N: restar 1 al leer.",
        ("Hay varios casos: los vectores se crean dentro de resuelveCaso.", "muted"),
    ]), "El coste es M por logaritmo de N en cada caso. Todos los tiempos son mayores o iguales que cero, que es lo que pide Dijkstra, "
        "y el tiempo total más grande cabe en un entero. Ojo con restar uno al leer las páginas, y con crear los vectores dentro de cada caso.", 0))

    segs.append((cierre(NOMBRE, [
        "Digrafo valorado + camino de coste mínimo  ⇒  Dijkstra con IndexPQ.",
        "Coste en los vértices: súmalo a la arista que entra (t + carga[w]).",
        "La página inicial: dist[origen] = carga[origen].",
        "Sin camino: dist[N-1] = INF  ⇒  IMPOSIBLE.   Coste O(M log N).",
    ]), "Resumiendo: es un camino de coste mínimo en un dígrafo valorado, y se resuelve con Dijkstra. "
        "El coste de las páginas se suma a la arista que entra, y la primera se carga en la distancia inicial. Si no hay camino, imposible.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/07-1_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../07-1_navegando_sin_teclado.mp4")
        print(f"07-1: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
