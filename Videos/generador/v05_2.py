"""Vídeo EJ 05-2 · La máquina calculadora"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C, font

CPP = "../../EJ_05-2/EJ_05-2.cpp"
NOMBRE = "La máquina calculadora"
TEMA = "Tema 5 · Grafos dirigidos"
MARC = 10000
OPN = ["+1", "×2", "÷3"]
OPC = ["blue", "gold", "green"]


def vec(x):
    return [(x + 1) % MARC, (x * 2) % MARC, x // 3]


L_BFS = find_line(CPP, "void bfs(")
L_INI = [find_line(CPP, "dist[inicial] = 0;"), find_line(CPP, "q.push(inicial);")]
L_POP = find_line(CPP, "int x = q.front(); q.pop();")
L_FIN = find_line(CPP, "if (x == final_)")
L_VECS = {find_line(CPP, "for (int y : g.ady(x))")}
L_C0 = find_line(CPP, "Digrafo construyeMaquina")
L_CONS = [find_line(CPP, "g.ponArista(x, (x + 1)"), find_line(CPP, "g.ponArista(x, (x * 2)"), find_line(CPP, "g.ponArista(x, x / 3)")]
CODE_CONS = code_lines(CPP, L_C0 - 1, find_line(CPP, "return g;") + 1, maxc=80)
L_NEW = find_line(CPP, "if (dist[y] == -1)")
L_SET = [find_line(CPP, "dist[y] = dist[x] + 1;"), find_line(CPP, "q.push(y);")]
CODE = code_lines(CPP, find_line(CPP, "class MaquinaCalculadora"), find_line(CPP, "};", L_BFS), maxc=64,
                  skip=[(find_line(CPP, "MaquinaCalculadora(Digrafo"), find_line(CPP, "MaquinaCalculadora(Digrafo") + 4),
                        (find_line(CPP, "int minimoPulsaciones") - 1, find_line(CPP, "int minimoPulsaciones") + 1)])


# ---- simulación del mismo BFS (9999 -> 6666) ----
def simula(ini, fin):
    dist = {ini: 0}
    padre = {}
    q = deque([ini])
    orden = [ini]
    pops = []
    while q:
        x = q.popleft()
        pops.append(x)
        if x == fin:
            break
        for i, y in enumerate(vec(x)):
            if y not in dist:
                dist[y] = dist[x] + 1
                padre[y] = (x, i)
                q.append(y)
                orden.append(y)
    return dist, padre, orden, pops


INI, FIN = 9999, 6666
DIST, PADRE, ORDEN, POPS = simula(INI, FIN)
assert DIST[FIN] == 2 and POPS[:5] == [9999, 0, 9998, 3333, 1]
L2 = [v for v in ORDEN if DIST[v] == 2]
assert L2[:6] == [1, 9996, 3332, 3334, 6666, 1111]
Y2 = {v: 150 + 46 * i for i, v in enumerate(L2)}
POS = {INI: (725, 0), 0: (900, Y2[1]), 9998: (900, (Y2[9996] + Y2[3332]) / 2), 3333: (900, (Y2[3334] + Y2[6666] + Y2[1111]) / 3 + 0)}
POS[3333] = (900, (Y2[3334] + Y2[1111]) / 2)
POS[INI] = (725, (POS[0][1] + POS[9998][1] + POS[3333][1]) / 3)
for v in L2:
    POS[v] = (1130, Y2[v])


def slide_arbol(k, n, nodos, aristas, actual, cola, nota, cap, hl, camino=False):
    s = Slide("Ejecución · de 9999 a 6666", f"paso {k} de {n}")
    s.code(24, 84, 640, 520, CODE, hl=hl, title="class MaquinaCalculadora")
    s.box(684, 84, 572, 340, "árbol del BFS (cada flecha es un botón)")
    p = {v: POS[v] for v in nodos}
    es = {a: ("dim", 3) for a in aristas}
    el = {a: (OPN[PADRE[a[1]][1]], OPC[PADRE[a[1]][1]]) for a in aristas}
    if camino:
        for a in [(9999, 3333), (3333, 6666)]:
            es[a] = ("gold", 6)
    ns = {v: (["gold", "blue", "purple"][DIST[v]], "node_t", None) for v in nodos}
    if actual is not None:
        ns[actual] = (ns[actual][0], "node_t", "text")
    s.dgraph(p, aristas, ns=ns, es=es, r=23, labels={v: str(v) for v in nodos}, lsize=14, elabels=el)
    s.box(684, 438, 572, 166, "estado")
    s.queue_row(704, 466, "cola", cola, size=15)
    s.wrap(704, 520, 530, nota, size=16, color="muted")
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 05-2", TEMA),
             "La máquina calculadora. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    # la máquina
    s = Slide("El problema: una calculadora con tres botones")
    s.box(60, 90, 560, 330)
    s.d.rounded_rectangle((120, 130, 560, 240), 14, fill=(12, 40, 36), outline=C["green"], width=3)
    s.text((340, 185), "0 0 4 2", size=64, color="green", bold=True, anchor="mm", mono=True)
    for i, (t, col) in enumerate(zip(OPN, OPC)):
        x = 130 + i * 145
        s.d.rounded_rectangle((x, 285, x + 125, 365), 16, fill=C[col + "_d"], outline=C[col], width=3)
        s.text((x + 62, 325), t, size=40, color=col, bold=True, anchor="mm")
    s.bullets(660, 110, 580, [
        "Marcador de 4 dígitos: de 0 a 9.999.",
        "Botones: +1, ×2 y ÷3 (división entera).",
        "Todo módulo 10.000: 5.000 × 2 = 10.000 → 0.",
        ("Piden: mínimo de pulsaciones de inicial a final.", "gold"),
    ], size=22, gap=16)
    segs.append((s, "La máquina tiene un marcador de cuatro dígitos y tres botones: más uno, por dos, y dividir entre tres, con división entera. "
                    "Como solo hay cuatro dígitos, todo se hace módulo diez mil: cinco mil por dos son diez mil, que en el marcador es cero. "
                    "Nos piden el menor número de pulsaciones para pasar de un número a otro.", 0))

    # modelo
    s = Slide("La clave: cada número del marcador es un vértice")
    s.box(40, 90, 700, 440, "desde 4242, un botón lleva a...")
    P = {4242: (150, 310), 4243: (520, 170), 8484: (520, 310), 1414: (520, 450)}
    E = [(4242, 4243), (4242, 8484), (4242, 1414)]
    s.dgraph(P, E, ns={4242: ("gold", "node_t", None)}, r=36, labels={v: str(v) for v in P}, lsize=18,
             es={(4242, 4243): ("blue", 5), (4242, 8484): ("gold", 5), (4242, 1414): ("green", 5)},
             elabels={(4242, 4243): ("+1", "blue"), (4242, 8484): ("×2", "gold"), (4242, 1414): ("÷3", "green")})
    s.bullets(770, 110, 470, [
        "10.000 vértices: 0 … 9.999.",
        ("Cada vértice tiene 3 aristas de salida, una por botón.", "gold"),
        "Pulsaciones mínimas = camino más corto de inicial a final.",
        "Sin pesos  ⇒  BFS desde el inicial.",
        "El Digrafo se construye UNA vez (30.000 aristas) y vale para los 2.000 casos.",
    ], size=21, gap=14)
    segs.append((s, "La clave es ver cada número del marcador como un vértice. Desde cada uno salen tres aristas, una por botón. "
                    "Por ejemplo, desde cuatro mil doscientos cuarenta y dos se llega a cuatro mil doscientos cuarenta y tres, a ocho mil cuatrocientos ochenta y cuatro, o a mil cuatrocientos catorce.", 0))
    segs.append((s, "Las pulsaciones mínimas son el camino más corto, y como las aristas no pesan, usamos un B F S desde el número inicial. "
                    "Construimos el grafo una sola vez, porque siempre es el mismo marcador, y lo reutilizamos en todos los casos.", 0))

    # dirigido
    s = Slide("Es un grafo dirigido")
    s.box(60, 90, 640, 400, "5.000 y 0")
    P = {5000: (190, 290), 0: (480, 290), 1: (480, 430)}
    E = [(5000, 0), (0, 0), (0, 1)]
    s.dgraph(P, E, ns={5000: ("blue", "node_t", None), 0: ("gold", "node_t", None)}, r=36, labels={v: str(v) for v in P}, lsize=18,
             es={(5000, 0): ("gold", 5), (0, 0): ("muted", 4), (0, 1): ("blue", 5)},
             elabels={(5000, 0): ("×2", "gold"), (0, 0): ("×2, ÷3", "muted"), (0, 1): ("+1", "blue")})
    s.bullets(730, 110, 500, [
        "5.000 → 0 con ×2 (5.000 · 2 = 10.000 ≡ 0).",
        "Pero desde 0 no se vuelve al 5.000 con un botón: la flecha solo va en un sentido.",
        "En el 0, ×2 y ÷3 dan 0 otra vez: un lazo. No pasa nada, el 0 ya está visitado.",
        ("Siempre hay camino: con +1 se llega a cualquier número.", "muted"),
    ], size=20, gap=14)
    segs.append((s, "Es un grafo dirigido. Desde cinco mil, con por dos, se llega a cero, pero desde cero no se vuelve a cinco mil con un solo botón. "
                    "Además, en el cero, por dos y dividir entre tres devuelven al cero: son lazos, y no pasa nada porque el cero ya está visitado. "
                    "Siempre hay camino, porque con más uno se llega a cualquier número.", 0))

    # ejemplo 0 -> 1024
    s = Slide("Ejemplo: de 0 a 1.024 en 11 pulsaciones")
    s.box(40, 100, 1200, 250)
    cadena = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    ops = ["+1"] + ["×2"] * 10
    for i, v in enumerate(cadena):
        x = 60 + i * 98
        s.d.rounded_rectangle((x, 170, x + 80, 230), 10, fill=C["blue_d"] if i not in (0, 11) else C["gold_d"],
                              outline=C["gold"] if i in (0, 11) else C["blue"], width=2)
        s.text((x + 40, 200), str(v), size=22 if v < 1000 else 20, bold=True, anchor="mm")
        if i < 11:
            s.text((x + 90, 150), ops[i], size=17, color="gold" if ops[i] == "×2" else "blue", bold=True, anchor="mm")
    s.wrap(60, 270, 1160, "Desde 0, ×2 no lleva a ninguna parte (da 0): hay que pulsar +1 para salir. Luego se va duplicando.", size=22, center=True)
    s.wrap(60, 400, 1160, "Del 1 al 2 valen +1 y ×2: hay dos formas de hacerlo en 11 pulsaciones. El BFS da el mínimo, no importa cuál.", size=22, color="muted", center=True)
    segs.append((s, "Veamos el primer ejemplo: de cero a mil veinticuatro hacen falta once pulsaciones. Desde cero, por dos no lleva a ninguna parte, así que hay que pulsar más uno. "
                    "Después se va duplicando hasta mil veinticuatro. El B F S nos da el mínimo sin que tengamos que pensar cuál es el truco.", 0))

    # construcción del grafo
    s = Slide("Construir el Digrafo (una sola vez)", "EJ_05-2.cpp")
    s.code(24, 84, 700, 330, CODE_CONS, hl=set(L_CONS), title="construyeMaquina")
    s.box(744, 84, 512, 330, "qué hace")
    s.bullets(764, 130, 470, ["10.000 vértices: los números del marcador.",
                              "3 aristas por vértice: una por botón.",
                              "Los lazos (0 → 0) no molestan al BFS."], size=20, gap=16)
    s.box(24, 434, 1232, 170, fill=(30, 52, 90), border="gold")
    s.wrap(44, 456, 1192, "El grafo no depende del caso: se construye en main antes de leer los casos y se pasa por referencia a cada uno. Cada caso es solo un BFS de O(10.000).", size=22)
    segs.append((s, "Construimos el grafo con tres llamadas a ponArista por cada número: una por botón. "
                    "Como siempre es el mismo marcador, se construye una sola vez, antes de leer los casos, y cada caso es solo un B F S.", 0))

    # código
    s = Slide("El código", "EJ_05-2.cpp")
    s.code(24, 84, 700, 520, CODE, hl={L_FIN} | L_VECS | {L_NEW} | set(L_SET), title="class MaquinaCalculadora")
    s.box(744, 84, 512, 520, "qué hace")
    s.bullets(764, 130, 470, ["dist[x] = -1: aún sin visitar.",
                              "g.ady(x): los 3 números a los que lleva cada botón desde x.",
                              "Si x es el número final, ya tiene su distancia mínima: paramos.",
                              "Cada vecino nuevo: dist + 1 y a la cola."], size=20, gap=16)
    segs.append((s, "En el código, g punto ady de x tiene los tres resultados de pulsar cada botón desde x. "
                    "Sacamos x de la cola, y si es el número final ya tiene su distancia mínima y paramos. "
                    "Si no, cada vecino nuevo recibe la distancia más uno y entra en la cola.", 0))

    # traza
    n = 6
    nodos = [INI]
    aristas = []
    segs.append((slide_arbol(1, n, nodos, aristas, INI, [INI], "dist[9999] = 0, el 9999 entra en la cola", "Empezamos en 9999: distancia 0 y a la cola", set(L_INI)),
                 "Empezamos en nueve mil novecientos noventa y nueve: distancia cero, y a la cola.", 0))
    q = deque([INI])
    cola_txt = [INI]
    pasos_pop = [(9999, "Sacamos 9999: +1 → 0, ×2 → 9998, ÷3 → 3333. Los tres son nuevos (dist 1)",
                  "Sacamos el nueve mil novecientos noventa y nueve. Más uno da cero, por dos da nueve mil novecientos noventa y ocho, y entre tres, tres mil trescientos treinta y tres. Los tres son nuevos, a distancia uno."),
                 (0, "Sacamos 0: +1 → 1 (nuevo); ×2 → 0 y ÷3 → 0 ya visitados",
                  "Sacamos el cero. Más uno da uno, que es nuevo. Por dos y entre tres dan cero otra vez, que ya está visitado."),
                 (9998, "Sacamos 9998: +1 → 9999 (visitado); ×2 → 9996 y ÷3 → 3332 nuevos",
                  "Sacamos el nueve mil novecientos noventa y ocho. Más uno vuelve al nueve mil novecientos noventa y nueve, ya visitado. Por dos da nueve mil novecientos noventa y seis, y entre tres, tres mil trescientos treinta y dos: nuevos, a distancia dos."),
                 (3333, "Sacamos 3333: +1 → 3334, ×2 → 6666 (el objetivo), ÷3 → 1111, nuevos",
                  "Sacamos el tres mil trescientos treinta y tres. Más uno da tres mil trescientos treinta y cuatro, por dos da seis mil seiscientos sesenta y seis, que es el objetivo, y entre tres, mil ciento once. Los tres son nuevos, a distancia dos.")]
    vistos = {INI}
    cola = [INI]
    for k, (x, cap, nar) in enumerate(pasos_pop, 2):
        cola.pop(0)
        for i, y in enumerate(vec(x)):
            if y not in vistos:
                vistos.add(y)
                cola.append(y)
                if DIST[y] <= 2:
                    nodos = nodos + [y]
                    aristas = aristas + [(x, y)]
        segs.append((slide_arbol(k, n, list(nodos), list(aristas), x, list(cola), "", cap, {L_POP} | L_VECS | {L_NEW} | set(L_SET)), nar, 0))
    cola_fin = [6666, 1111, "…"]
    segs.append((slide_arbol(6, n, list(nodos), list(aristas), 6666, cola_fin,
                             "(Antes salen 1, 9996, 3332 y 3334: sus vecinos están en el nivel 3 y no cambian el resultado.)",
                             "Sacamos 6666 = final: distancia 2. Camino: 9999 → 3333 → 6666 (÷3, ×2)", {L_POP, L_FIN}, camino=True),
                 "La cola sigue: salen uno, nueve mil novecientos noventa y seis, tres mil trescientos treinta y dos y tres mil trescientos treinta y cuatro, "
                 "pero sus vecinos están más lejos. Cuando sale seis mil seiscientos sesenta y seis, que es el final, su distancia es dos: dividir entre tres y luego por dos.", 0))

    segs.append((ideas("Resultado y coste", [
        "9999 → 6666: ÷3 y después ×2  ⇒  2 pulsaciones.",
        "5000 → 0: un solo ×2  ⇒  1.",
        "4242 → 4242: no se pulsa nada  ⇒  0 (dist[inicial] = 0).",
        "Coste por caso: O(10.000) vértices · 3 vecinos = unas 3·10⁴ operaciones.",
        ("Con 2.000 casos: unas 6·10⁷ operaciones en total.", "muted"),
    ]), "Los demás ejemplos: de nueve mil novecientos noventa y nueve a seis mil seiscientos sesenta y seis, dos pulsaciones. De cinco mil a cero, una. "
        "Y si el inicial es igual al final, cero. El coste por caso es lineal en diez mil vértices, con tres vecinos cada uno.", 0))

    segs.append((cierre(NOMBRE, [
        "Cada número del marcador (0 … 9.999) es un vértice; cada botón, una arista dirigida.",
        "Mínimo de pulsaciones = camino más corto  ⇒  BFS desde el inicial.",
        "Aristas de x: (x+1) % 10000, (x·2) % 10000, x / 3.",
        "Se para al sacar el final.   Coste O(10.000) por caso.",
    ]), "Resumiendo: cada número del marcador es un vértice y cada botón una arista dirigida. "
        "El mínimo de pulsaciones es el camino más corto, que calculamos con un B F S, sobre el grafo que construimos una vez, y parando al sacar el número final.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/05-2_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../05-2_maquina_calculadora.mp4")
        print(f"05-2: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
