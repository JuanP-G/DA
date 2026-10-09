"""Vídeo EJ 04-4 · Los números de Bacon"""
import sys
from collections import deque
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../4-Grafos no dirigidos/EJ_04-4/EJ_04-4.cpp"
NOMBRE = "Los números de Bacon"

PELIS = [
    ("AlgunosHombresBuenos", ["TomCruise", "JackNicholson", "DemiMoore", "KevinBacon"]),
    ("RainMan", ["DustinHoffman", "TomCruise", "ValeriaGolino"]),
    ("Apolo13", ["TomHanks", "KevinBacon", "EdHarris", "KathleenQuinlan"]),
    ("MejorImposible", ["JackNicholson", "HelenHunt", "GregKinnear", "CubaGoodingJr"]),
    ("LoQueLaNocheEsconde", ["TyeSheridan", "AnaDeArmas", "JohnLeguizamo", "HelenHunt"]),
    ("Sleepers", ["RobertDeNiro", "DustinHoffman", "BradPitt", "KevinBacon"]),
    ("ExperimentoIndie", ["SarahDavis", "JohnDoe", "MichaelAnderson"]),
]
CORTO = {"AlgunosHombresBuenos": "AHB", "RainMan": "RM", "Apolo13": "A13", "MejorImposible": "MI",
         "LoQueLaNocheEsconde": "LNE", "Sleepers": "SL", "ExperimentoIndie": "EI"}
CONSULTAS = ["TomCruise", "DustinHoffman", "TomHanks", "HelenHunt", "AnaDeArmas", "KevinBacon", "JohnDoe"]


def ini(nombre):
    return "".join(c for c in nombre if c.isupper())[:3]


# --- simulación exacta de resuelveCaso: numeración de actores y grafo actor-película ---
ID, REPARTO = {}, []
for t, cast in PELIS:
    r = []
    for a in cast:
        if a not in ID:
            ID[a] = len(ID)
        r.append(ID[a])
    REPARTO.append(r)
A = len(ID)
V = A + len(PELIS)
NOMBRE_V = {i: a for a, i in ID.items()}
NOMBRE_V.update({A + p: PELIS[p][0] for p in range(len(PELIS))})
EDGES = [(a, A + p) for p, r in enumerate(REPARTO) for a in r]
ADY = [[] for _ in range(V)]
for a, b in EDGES:
    ADY[a].append(b)
    ADY[b].append(a)


def bfs(origen):
    dist = [-1] * V
    dist[origen] = 0
    q = deque([origen])
    orden = []
    while q:
        v = q.popleft()
        orden.append(v)
        for w in ADY[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                q.append(w)
    return dist, orden


DIST, ORDEN = bfs(ID["KevinBacon"])
NIVELES = {}
for v in ORDEN:
    NIVELES.setdefault(DIST[v], []).append(v)

# posiciones: una columna por nivel del BFS, los inalcanzables a la derecha
POS = {}
X0, DX = 90, 168
for d, vs in NIVELES.items():
    n = len(vs)
    for i, v in enumerate(vs):
        POS[v] = (X0 + d * DX, 135 + (i + 0.5) * (340 / n))
inalc = [v for v in range(V) if DIST[v] == -1]
inalc.sort(key=lambda v: v < A)   # la película primero
for i, v in enumerate(inalc):
    POS[v] = (1195, 135 + (i + 0.5) * (340 / len(inalc)))
LAB = {v: (CORTO[NOMBRE_V[v]] if v >= A else ini(NOMBRE_V[v])) for v in range(V)}


def estilo(hasta):
    ns = {}
    for v in range(V):
        peli = v >= A
        if DIST[v] != -1 and DIST[v] <= hasta:
            ns[v] = ("purple" if peli else ("gold" if DIST[v] == 0 else "blue"), "node_t", None)
        else:
            ns[v] = ((60, 50, 95) if peli else "node", "text" if peli else "node_t", None)
    return ns


def slide_grafo(title, hasta, cap, corner=None, extra_es=None):
    s = Slide(title, (corner + " · " if corner else "") + "actores: claros · películas: morado")
    s.box(24, 84, 1232, 400)
    es = {}
    for a, b in EDGES:
        if DIST[a] != -1 and DIST[b] != -1 and max(DIST[a], DIST[b]) <= hasta and abs(DIST[a] - DIST[b]) == 1:
            es[(a, b)] = ("gold", 3)
    if extra_es:
        es.update(extra_es)
    s.graph(POS, EDGES, ns=estilo(hasta), es=es, labels=LAB, r=17, lsize=12)
    for d in NIVELES:
        if d <= hasta:
            s.text((X0 + d * DX, 112), f"dist {d}", size=14, color="gold", anchor="mm")
    s.box(24, 500, 1232, 112, "números de Bacon de las consultas (dist / 2)")
    x = 44
    for c in CONSULTAS:
        v = ID[c]
        val = DIST[v] // 2 if DIST[v] != -1 and DIST[v] <= hasta else ("INF" if hasta >= 99 else "?")
        x = s.pill(x, 540, f"{c}: {val}", fill="gold" if val not in ("?", "INF") else ("red" if val == "INF" else (40, 60, 100)),
                   color="node_t" if val != "?" else "text", size=15, padx=10) + 8
    s.caption(cap, y=630)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-4"),
             "Los números de Bacon. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    segs.append((ideas("El problema", [
        "Dos actores están conectados si han salido en la misma película.",
        "Número de Bacon = mínimo número de películas para llegar hasta KevinBacon.",
        "KevinBacon tiene 0, sus compañeros de reparto 1, los compañeros de estos 2...",
        "Si no hay ninguna cadena posible: INF.",
    ], note="Ejemplo: DustinHoffman sale con KevinBacon en Sleepers ⇒ 1 (aunque también llegue en 2 por RainMan)."),
        "Dos actores están conectados si han trabajado juntos en una película. El número de Bacon de un actor es el mínimo número de películas "
        "que hacen falta para llegar desde él hasta Kevin Bacon. Kevin Bacon tiene cero, sus compañeros de reparto uno, y así sucesivamente. "
        "Si no hay ninguna cadena, se escribe INF.", 0))

    segs.append((ideas("Cómo se plantea", [
        "Es un camino MÍNIMO en un grafo SIN pesos  ⇒  BFS.",
        "Un único BFS desde KevinBacon: después cada consulta es mirar dist[actor].",
        "(Un BFS por consulta serían hasta 100.000 recorridos: demasiado lento.)",
        "El BFS va por capas de distancia: la 1ª vez que llega a un vértice es por el camino más corto.",
        "Tres detalles lo hacen más interesante que un BFS normal...",
    ]), "Es un camino mínimo en un grafo sin pesos, así que la herramienta es un B F S, que visita los vértices por capas de distancia: la primera vez que llega a uno, lo hace por el camino más corto. Pero ojo: no hacemos uno por consulta, "
        "que podrían ser cien mil. Hacemos un único B F S desde Kevin Bacon y luego cada consulta es solo mirar su distancia. "
        "Hay tres detalles que hacen este ejercicio más interesante.", 0))

    segs.append((ideas("Detalle 1 · los vértices tienen nombre", [
        "Grafo trabaja con vértices 0 .. V-1, pero los actores vienen por nombre.",
        "unordered_map<string,int> id: cada nombre nuevo recibe el siguiente número.",
        "TomCruise → 0,  JackNicholson → 1,  DemiMoore → 2,  KevinBacon → 3, ...",
    ]), "Primer detalle: el grafo trabaja con números de cero a uve menos uno, pero los actores vienen por nombre. "
        "Usamos un unordered map de nombre a número: cada nombre nuevo recibe el siguiente número libre.", 0))

    # detalle 2: clique vs estrella con película
    s = Slide("Detalle 2 · cómo poner las aristas")
    import math
    cx1, cx2, cy, R = 330, 950, 290, 120
    pa = {i: (cx1 + R * math.cos(2 * math.pi * i / 6 - math.pi / 2), cy + R * math.sin(2 * math.pi * i / 6 - math.pi / 2)) for i in range(6)}
    s.box(60, 90, 540, 400, "unir cada par de actores: k(k-1)/2 aristas")
    s.graph(pa, [(i, j) for i in range(6) for j in range(i + 1, 6)], labels={i: f"a{i + 1}" for i in range(6)},
            es={(i, j): ("red", 2) for i in range(6) for j in range(i + 1, 6)}, r=22)
    pb = {i: (cx2 + R * math.cos(2 * math.pi * i / 6 - math.pi / 2), cy + R * math.sin(2 * math.pi * i / 6 - math.pi / 2)) for i in range(6)}
    pb[6] = (cx2, cy)
    s.box(680, 90, 540, 400, "la película como vértice: k aristas")
    s.graph(pb, [(i, 6) for i in range(6)], labels={**{i: f"a{i + 1}" for i in range(6)}, 6: "peli"},
            ns={6: ("purple", "node_t", None)}, es={(i, 6): ("green", 3) for i in range(6)}, r=22, lsize=14)
    s.caption("6 actores: 15 aristas  vs  6.     100.000 actores: ~5.000 millones  vs  100.000", y=515)
    s.caption("Pero ahora actor → actor son 2 aristas:   número de Bacon = dist / 2", y=560)
    segs.append((s, "Segundo detalle, y es la clave: cómo poner las aristas. Lo directo sería unir cada par de actores de una película, "
                    "pero una película de ka actores da ka por ka menos uno partido por dos aristas. Con cien mil actores serían unos cinco mil millones.", 0))
    segs.append((s, "El truco es meter también las películas como vértices, unidas a sus actores. Una película de ka actores son solo ka aristas. "
                    "A cambio, pasar de un actor a otro cuesta dos aristas, actor, película, actor. Por eso el número de Bacon es la distancia entre dos.", 0))

    segs.append((ideas("Detalle 3 · V hay que saberlo antes", [
        "Grafo g(V) necesita el número de vértices al crearlo...",
        "...pero no sabemos cuántos actores hay hasta leer TODAS las películas.",
        "1) Leer las películas y guardar el reparto de cada una (ya en números).",
        "2) Crear Grafo g(actores + películas).  Vértices 0..A-1: actores.  A + p: película p.",
        "3) Poner las aristas actor – película.",
    ]), "Tercer detalle: para crear el grafo hay que saber cuántos vértices tiene, y no sabemos cuántos actores hay hasta haber leído todas las películas. "
        "Así que primero leemos y guardamos el reparto de cada película, ya con los números de los actores, "
        "y después creamos el grafo con actores más películas vértices y ponemos las aristas.", 0))

    L_R0, L_R1 = find_line(CPP, "for (int p = 0; p < peliculas; ++p) {"), find_line(CPP, "else reparto[p].push_back")
    s = Slide("El código · lectura y grafo", "EJ_04-4.cpp")
    s.code(24, 84, 1232, 540, code_lines(CPP, find_line(CPP, "int peliculas; cin >> peliculas;"), find_line(CPP, "CaminosBFS caminos"), maxc=110),
           hl={find_line(CPP, "auto it = id.find(actor);"), find_line(CPP, "int nuevo = id.size();"), find_line(CPP, "Grafo g(actores + peliculas);"),
               find_line(CPP, "g.ponArista(a, actores + p);")}, title="resuelveCaso", size=16)
    segs.append((s, "En el código: mientras leemos, si un actor no está en el mapa le damos el siguiente número. Guardamos el reparto de cada película. "
                    "Después creamos el grafo con actores más películas vértices, y unimos cada actor con el vértice de su película, que es actores más pe.", 0))
    s = Slide("El código · consultas", "EJ_04-4.cpp")
    s.code(24, 84, 1232, 420, code_lines(CPP, find_line(CPP, "auto itBacon"), find_line(CPP, 'cout << "---\\n";', find_line(CPP, "auto itBacon")), maxc=110),
           hl={find_line(CPP, "bool hayBacon"), find_line(CPP, "caminos.distancia(v) / 2")}, title="resuelveCaso", size=17)
    s.caption("Si KevinBacon no aparece en ninguna película, todos son INF", y=540)
    segs.append((s, "Para las consultas: si Kevin Bacon no aparece en la base de datos, todos son INF. Si aparece, hacemos un único B F S desde él, "
                    "y cada actor alcanzable tiene número de Bacon igual a su distancia entre dos.", 0))

    # ejecución por niveles
    maxd = max(NIVELES)
    segs.append((slide_grafo("Ejecución · BFS desde KevinBacon", 0, "dist 0: KevinBacon (KB)", "nivel 0"),
                 "Vamos con el primer caso. Este es el grafo de actores y películas, ordenado por columnas según la distancia a Kevin Bacon. Empezamos en él, con distancia cero.", 0))
    for d in range(1, maxd + 1):
        vs = NIVELES[d]
        nombres = ", ".join(LAB[v] for v in vs)
        if d % 2 == 1:
            cap = f"dist {d} (películas): {nombres}"
            pelis = " y ".join(NOMBRE_V[v] for v in vs) if len(vs) <= 3 else f"{len(vs)} películas"
            nar = f"La siguiente capa, a distancia {d}, son películas: {pelis}."
        else:
            cap = f"dist {d} (actores): {nombres}  →  número de Bacon {d // 2}"
            nar = f"A distancia {d} están los actores de esas películas: su número de Bacon es {d // 2}."
            if d == 2:
                nar += " Fíjate en Dustin Hoffman: el B F S lo alcanza aquí por Sleepers, así que tiene uno y no dos."
        segs.append((slide_grafo("Ejecución · BFS desde KevinBacon", d, cap, f"nivel {d}"), nar, 0))
    segs.append((slide_grafo("Ejecución · resultado", 99, "ExperimentoIndie y sus actores no se alcanzan: JohnDoe → INF", "fin"),
                 "La cola se vacía. Experimento Indie y sus actores no se han alcanzado nunca: John Doe no tiene camino hasta Kevin Bacon, así que es INF.", 0))

    segs.append((ideas("Salida del caso 1 y caso 2", [
        "TomCruise 1 · DustinHoffman 1 · TomHanks 1 · HelenHunt 2 · AnaDeArmas 3 · KevinBacon 0 · JohnDoe INF",
        "Caso 2: solo MejorImposible y LoQueLaNocheEsconde.",
        "KevinBacon no está en la base de datos  ⇒  HelenHunt INF, AnaDeArmas INF.",
        ("Tras cada caso se escribe ---", "muted"),
    ]), "Y esta es la salida del primer caso. En el segundo caso solo hay dos películas y Kevin Bacon no sale en ninguna, "
        "así que nadie puede conectarse con él y todos son INF.", 0))

    segs.append((cierre(NOMBRE, [
        "Camino mínimo sin pesos ⇒ un único BFS desde KevinBacon.",
        "Nombres → números con un unordered_map.",
        "Películas como vértices: k aristas por película en vez de k(k-1)/2.  Bacon = dist / 2.",
        "Leer todo antes de crear Grafo (hay que saber V).",
        "Coste: O(V + A), con V ≤ actores + películas.",
    ]), "Resumiendo: un único B F S desde Kevin Bacon. Pasamos los nombres a números con un mapa, metemos las películas como vértices para no "
        "tener demasiadas aristas, y dividimos la distancia entre dos. El coste es lineal en el tamaño del grafo.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-4_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-4_numeros_de_bacon.mp4")
        print(f"04-4: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
