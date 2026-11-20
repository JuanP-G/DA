"""07-7 · Ratones en un laberinto: juez con pruebas pensadas para cada error típico.

Dígrafo valorado (puede haber lazos y varios pasadizos A → B). Cuántas celdas distintas de la
salida S pueden llegar a S en como mucho T segundos: un Dijkstra desde S en el grafo inverso.
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-7/EJ_07-7.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-7/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-7/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["dist[v] <= T) ++ratones;", "dist[v] < T) ++ratones;"],
}

MAXT = 10_000
MAXCRONO = 1_000_000


# ---------------------------------------------------------------- solucionador independiente
def ratones(N, S, T, pasadizos):
    entra = [[] for _ in range(N + 1)]          # entra[b] = [(a, t)] : pasadizos a → b
    for a, b, t in pasadizos:
        entra[b].append((a, t))
    INF = float("inf")
    dist = [INF] * (N + 1)
    dist[S] = 0
    cola = [(0, S)]
    while cola:
        d, v = heapq.heappop(cola)
        if d > dist[v]:
            continue
        for a, t in entra[v]:
            if d + t < dist[a]:
                dist[a] = d + t
                heapq.heappush(cola, (d + t, a))
    return sum(1 for v in range(1, N + 1) if v != S and dist[v] <= T)


def valida(caso):
    N, S, T, pasadizos = caso
    assert 1 <= N <= 100_000 and 1 <= S <= N and 1 <= T <= MAXCRONO and 0 <= len(pasadizos) <= 200_000
    for a, b, t in pasadizos:
        assert 1 <= a <= N and 1 <= b <= N and 1 <= t <= MAXT


def caso_a_texto(caso):
    N, S, T, pasadizos = caso
    return f"{N} {S} {T} {len(pasadizos)}\n" + "".join(f"{a} {b} {t}\n" for a, b, t in pasadizos)


# ---------------------------------------------------------------- generadores
def aleatorio(r, N, P, maxt, raros=0.0):
    pasadizos = []
    for _ in range(P):
        x = r.random()
        if pasadizos and x < raros / 2:
            a, b, _t = r.choice(pasadizos)
        elif x < raros:
            a = b = r.randint(1, N)
        else:
            a, b = r.randint(1, N), r.randint(1, N)
        pasadizos.append((a, b, r.randint(1, maxt)))
    T = r.randint(1, 3 * maxt)
    return (N, r.randint(1, N), T, pasadizos)


def grande(r, N, P):
    perm = list(range(1, N + 1))
    r.shuffle(perm)
    pasadizos = [(perm[i], perm[(i + 1) % N], r.randint(1, MAXT)) for i in range(N)]
    while len(pasadizos) < P:
        pasadizos.append((r.randint(1, N), r.randint(1, N), r.randint(1, MAXT)))
    r.shuffle(pasadizos)
    return (N, r.randint(1, N), MAXCRONO, pasadizos)


def cadena(r, N):
    """Celdas en fila que desembocan en la salida (la N): solo las más cercanas llegan."""
    pasadizos = [(i, i + 1, r.randint(1, MAXT)) for i in range(1, N)]
    pasadizos += [(i + 1, i, 1) for i in range(1, N, 3)]            # hacia atrás: no ayudan
    r.shuffle(pasadizos)
    return (N, N, MAXCRONO, pasadizos)


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(77)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (5, 5, 20, [(1, 2, 5), (1, 4, 10), (2, 4, 7), (3, 4, 15), (4, 5, 10)])
    ej2 = (3, 1, 10, [(2, 3, 5), (3, 2, 6)])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF: 3 ratones y 0.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: hace falta el tiempo de cada celda HASTA la salida (no desde ella) y cuentan los que tardan como mucho T.",
            "rte": "Error de ejecución con el ejemplo: las celdas van del 1 al N (resta 1 a S y a las celdas de cada pasadizo)."},
           ["En el primer caso el ratón de la celda 1 tarda exactamente 20 y cuenta.",
            "La primera línea de cada caso trae N, S, T y P, en ese orden."])
    prueba("Una sola celda", "borde", [(1, 1, 5, [])],
           "N = 1: solo está la celda de salida, que no tiene ratón. Sale 0.",
           {"wa": "Con una sola celda no hay ningún ratón: la de salida no cuenta.",
            "rte": "Con N = 1 y ningún pasadizo algo se sale del vector: revisa los índices."},
           ["Debe salir 0.",
            "No se coloca ratón en la celda de salida."])
    prueba("Sin pasadizos", "borde", [(3, 2, 10, [])],
           "Ningún pasadizo: ningún ratón puede salir.",
           {"wa": "Sin pasadizos ningún ratón llega: 0. Revisa que solo cuentas las celdas con distancia finita ≤ T y que no cuentas la salida."},
           ["Debe salir 0.",
            "Inicializa las distancias a infinito, salvo la de la salida."])
    prueba("Ningún ratón llega a tiempo", "borde", [(3, 1, 1, [(2, 1, 2), (3, 1, 5), (3, 2, 1)])],
           "Con T = 1 y pasadizos de 2 o más segundos, nadie sale.",
           {"wa": "Ningún ratón tarda 1 segundo o menos: 0. Revisa la comparación con T y que no cuentas la salida."},
           ["Debe salir 0.",
            "Cuenta las celdas v ≠ S con dist[v] ≤ T."])
    prueba("Todos los ratones salen", "borde",
           [(4, 2, MAXCRONO, [(1, 2, 10000), (3, 1, 10000), (4, 3, 10000), (2, 4, 10000)])],
           "Con T = 10⁶ todos los ratones llegan (el más lejano tarda 30.000).",
           {"wa": "Todos llegan: debe salir N − 1 = 3. Si sale menos, algún ratón no encuentra su camino (¿usas el grafo inverso?); si sale N, cuentas la salida."},
           ["Debe salir 3.",
            "Cada ratón sigue los pasadizos en su sentido hasta la salida."])
    prueba("La celda de salida no tiene ratón", "trampa", [(2, 1, 10, [(2, 1, 5), (1, 2, 5)])],
           "Dos celdas y la salida en la 1: solo hay un ratón (el de la 2).",
           {"wa": "Cuentas también la celda de salida (su distancia es 0 ≤ T). El enunciado coloca un ratón en cada celda EXCEPTO en la de salida."},
           ["Debe salir 1.",
            "Al contar, salta la celda S."])
    prueba("Distancias hacia la salida, no desde ella", "trampa",
           [(4, 4, 10, [(1, 4, 5), (2, 4, 5), (4, 3, 100)])],
           "Las celdas 1 y 2 llegan a la salida en 5 s; desde la salida a la 3 hay un pasadizo, pero eso no le sirve al ratón de la 3.",
           {"wa": "Calculas las distancias DESDE la salida a cada celda, pero los ratones van HACIA la salida. Haz el Dijkstra desde S en el grafo inverso (g.inverso())."},
           ["Debe salir 2.",
            "El tiempo de v a S en el grafo es el tiempo de S a v en el grafo con las aristas al revés.",
            "Un único Dijkstra desde S sobre g.inverso() da el tiempo de TODAS las celdas hasta la salida."])
    prueba("Pasadizos de un solo sentido", "trampa", [(3, 3, 5, [(3, 1, 3), (2, 3, 4)])],
           "La 1 no tiene ningún pasadizo hacia la salida (solo hay uno de la salida a ella): solo sale el ratón de la 2.",
           {"wa": "Recorres los pasadizos en los dos sentidos. Cada uno va solo de A a B; para volver tendría que aparecer otra línea."},
           ["Debe salir 1.",
            "Añade solo la arista A → B (y usa su inverso para el Dijkstra)."])
    prueba("Llegar justo a tiempo cuenta", "trampa", [(3, 3, 7, [(1, 3, 7), (2, 3, 8)])],
           "El ratón de la celda 1 tarda exactamente T = 7 segundos: cuenta («en como mucho T segundos»).",
           {"wa": "Cuentas solo los que tardan menos de T. El enunciado dice «como mucho T»: usa ≤."},
           ["Debe salir 1.",
            "Compara con dist[v] <= T."])
    prueba("Mejorar un tiempo ya encontrado", "trampa", [(4, 4, 5, [(1, 4, 10), (1, 2, 1), (2, 4, 1), (3, 1, 2)])],
           "La celda 1 tiene un pasadizo directo de 10 s, pero pasando por la 2 tarda 2: hay que actualizar su tiempo.",
           {"wa": "Fijas el tiempo de una celda la primera vez que la ves y no lo mejoras después: hay que relajar (si mejora, actualizar dist y la prioridad)."},
           ["Debe salir 3: las celdas 1 (2 s), 2 (1 s) y 3 (4 s).",
            "Una distancia solo es definitiva cuando su celda sale de la cola de prioridad."])
    prueba("Varios pasadizos entre dos celdas y lazos", "trampa",
           [(3, 2, 5, [(1, 2, 9), (2, 2, 1), (1, 2, 2), (1, 1, 1), (3, 2, 6)])],
           "De la 1 a la 2 hay dos pasadizos (9 y 2) y hay lazos: hay que usar el más rápido.",
           {"wa": "Te quedas con un solo pasadizo entre dos celdas (el primero o el último que lees). Guarda todos: Dijkstra elige el mejor."},
           ["Debe salir 1 (la celda 1 tarda 2; la 3 tarda 6 > 5).",
            "No compruebes si ya existe la arista antes de añadirla ni uses una matriz que se sobrescribe."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio(r, 9, 20, 9), (4, 4, 5, [(1, 4, 9)]), ej2, aleatorio(r, 6, 8, 5), (2, 2, 3, [(1, 2, 4)])],
           "Un caso con muchas celdas seguido de otros más pequeños: nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: las distancias, el contador o el grafo no se crean de nuevo en cada caso.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: créalas dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso (o son static).",
            "Declara el grafo, dist, la cola y el contador dentro de resuelveCaso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(1, 9), r.randint(0, 20), r.choice([3, 20, 10000])) for _ in range(50)],
           "50 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas bien: la línea que falla es el número de caso; calcula a mano el tiempo de cada celda hasta la salida."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Dibuja los pasadizos con flechas y sigue, desde cada celda, el camino más rápido hasta S."])
    prueba("Aleatorios con lazos y pasadizos repetidos", "aleatorio",
           [aleatorio(r, r.randint(2, 8), r.randint(5, 25), 9, raros=0.4) for _ in range(40)],
           "40 casos con muchos lazos y pasadizos repetidos.",
           {"wa": "Algún caso con lazos o pasadizos repetidos falla: guarda todas las aristas, Dijkstra se queda con la mejor."},
           ["Busca el caso que falla.",
            "Los lazos no estorban a Dijkstra."])
    prueba("Grande: 60.000 celdas y 130.000 pasadizos", "rendimiento", [grande(r, 60_000, 130_000)],
           "Un laberinto grande en el que casi todos los ratones salen (T = 10⁶).",
           {"tle": "Haces un Dijkstra (o un recorrido) desde cada celda hasta la salida: con 60.000 celdas no termina. Basta UNO desde la salida en el grafo inverso. También es lento buscar el mínimo recorriendo el vector (O(N²)).",
            "mle": "Gastas demasiada memoria: no guardes una matriz de distancias.",
            "wa": "Solo falla en el grande: revisa el valor de infinito y la comparación con T."},
           ["¿Cuántos Dijkstra haces? Debería ser uno.",
            "Invierte el grafo (g.inverso()) y lanza Dijkstra desde S con IndexPQ."])
    prueba("Fila de 60.000 celdas", "rendimiento", [cadena(r, 60_000)],
           "Una fila de celdas que desemboca en la salida: solo las ~200 más cercanas llegan en 10⁶ segundos.",
           {"tle": "Demasiado lento: un Dijkstra con IndexPQ basta (y puede parar en cuanto la distancia supera T).",
            "wa": "Las distancias de la fila llegan a 3·10⁸: revisa que no se desborda nada y la comparación con T."},
           ["Puedes cortar el Dijkstra cuando la celda que sale de la cola ya tarda más de T.",
            "Usa la IndexPQ, no un recorrido del vector para buscar el mínimo."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(f"{ratones(*c)}\n" for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


_LINEAL = ("    vector<bool> hecho(N, false);\n    while (true) {\n        int v = -1;\n"
           "        for (int u = 0; u < N; ++u) if (!hecho[u] && dist[u] != INF && (v == -1 || dist[u] < dist[v])) v = u;\n"
           "        if (v == -1) break;\n        hecho[v] = true;\n")

_CONTAR = """    int ratones = 0;
    for (int v = 0; v < N; ++v)
        if (v != S && dist[v] <= T) ++ratones;
    cout << ratones << '\\n';"""

_UNO_POR_CELDA = """    int ratones = 0;
    for (int s0 = 0; s0 < N; ++s0) {
        if (s0 == S) continue;
        vector<int> d(N, INF);
        IndexPQ<int> q(N);
        d[s0] = 0; q.push(s0, 0);
        while (!q.empty()) {
            int v = q.top().elem; q.pop();
            if (v == S || d[v] > T) break;
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                if (d[w] > d[v] + a.valor()) { d[w] = d[v] + a.valor(); q.update(w, d[w]); }
            }
        }
        if (d[S] <= T) ++ratones;
    }
    cout << ratones << '\\n';"""

VARIANTES = [
    Variante("cuenta también la celda de salida", [("if (v != S && dist[v] <= T)", "if (dist[v] <= T)")], prueba=6, v="wa"),
    Variante("Dijkstra en el grafo original (desde la salida)", [("for (auto a : inv.ady(v))", "for (auto a : g.ady(v))")],
             prueba=7, v="wa"),
    Variante("pasadizos en los dos sentidos",
             [("g.ponArista({a - 1, b - 1, t});", "g.ponArista({a - 1, b - 1, t}); g.ponArista({b - 1, a - 1, t});")], prueba=8, v="wa"),
    Variante("cuenta solo los que tardan menos de T", [("dist[v] <= T) ++ratones;", "dist[v] < T) ++ratones;")], prueba=9, v="wa"),
    Variante("fija el tiempo la primera vez (sin mejorar)", [("if (dist[w] > dist[v] + a.valor()) {", "if (dist[w] == INF) {")],
             prueba=10, v="wa"),
    Variante("solo el primer pasadizo entre dos celdas",
             [("g.ponArista({a - 1, b - 1, t});", "if (!g.hayArista(a - 1, b - 1)) g.ponArista({a - 1, b - 1, t});")], prueba=11, v="wa"),
    Variante("distancias no reiniciadas entre casos (static)",
             [("vector<int> dist(N, INF);", "static vector<int> dist; dist.resize(N, INF);")], prueba=12, v="wa"),
    Variante("un Dijkstra desde cada celda", [(_CONTAR, _UNO_POR_CELDA)], prueba=15, v="tle"),
    Variante("Dijkstra buscando el mínimo en el vector (O(N²))",
             [("    while (!pq.empty()) {\n        int v = pq.top().elem; pq.pop();\n", _LINEAL)], prueba=15, v="tle"),
]
