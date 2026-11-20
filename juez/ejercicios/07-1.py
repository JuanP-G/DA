"""07-1 · Navegando sin teclado: juez con pruebas pensadas para cada error típico.

Dígrafo valorado con coste en las aristas (localizar y pulsar el enlace) y en los vértices
(cargar la página). Camino mínimo de la página 1 a la N contando la carga de TODAS las páginas
del camino (también la 1 y la N); IMPOSIBLE si no se llega.
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-1/EJ_07-1.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-1/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-1/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["dist[0] = carga[0];", "dist[0] = 0;"],
}

MAXT = 10_000      # todos los tiempos están entre 0 y 10.000


# ---------------------------------------------------------------- solucionador independiente
def navega(N, carga, enlaces):
    """Dijkstra sobre (página, tiempo acumulado) donde entrar en una página cuesta su carga.
    Devuelve el tiempo mínimo de 1 a N o None si no se llega."""
    ady = [[] for _ in range(N + 1)]
    for v, w, t in enlaces:
        ady[v].append((w, t))
    INF = float("inf")
    dist = [INF] * (N + 1)
    dist[1] = carga[0]
    cola = [(dist[1], 1)]
    while cola:
        d, v = heapq.heappop(cola)
        if d > dist[v]:
            continue
        for w, t in ady[v]:
            nd = d + t + carga[w - 1]
            if nd < dist[w]:
                dist[w] = nd
                heapq.heappush(cola, (nd, w))
    return None if dist[N] == INF else dist[N]


def salida_caso(caso):
    r = navega(*caso)
    return "IMPOSIBLE\n" if r is None else f"{r}\n"


def caso_a_texto(caso):
    N, carga, enlaces = caso
    return (f"{N}\n" + " ".join(map(str, carga)) + f"\n{len(enlaces)}\n"
            + "".join(f"{v} {w} {t}\n" for v, w, t in enlaces))


def valida(caso):
    """Comprueba que el caso respeta el enunciado (nunca generamos entradas fuera de él)."""
    N, carga, enlaces = caso
    assert 2 <= N <= 3000 and len(carga) == N and 0 <= len(enlaces) <= 30000
    assert all(0 <= c <= MAXT for c in carga)
    pares = set()
    for v, w, t in enlaces:
        assert 1 <= v <= N and 1 <= w <= N and v != w and 0 <= t <= MAXT
        assert (v, w) not in pares, "dos enlaces de la misma página a la misma página"
        pares.add((v, w))


# ---------------------------------------------------------------- generadores
def aleatorio(r, N, M, ceros=0.0, maxt=50):
    """Caso al azar sin enlaces repetidos ni a sí mismos. `ceros` = probabilidad de tiempo 0."""
    M = min(M, N * (N - 1))
    pares = set()
    while len(pares) < M:
        v, w = r.randint(1, N), r.randint(1, N)
        if v != w:
            pares.add((v, w))
    t = lambda: 0 if r.random() < ceros else r.randint(0, maxt)
    enlaces = [(v, w, t()) for v, w in pares]
    r.shuffle(enlaces)
    return (N, [t() for _ in range(N)], enlaces)


def grande(r, N, M):
    """Caso grande: un camino oculto de la 1 a la N con enlaces baratos y mucho ruido alrededor."""
    perm = list(range(2, N))
    r.shuffle(perm)
    camino = [1] + perm[: N // 3] + [N]
    pares = {}
    for a, b in zip(camino, camino[1:]):
        pares[(a, b)] = r.randint(0, 2000)
    while len(pares) < M:
        v, w = r.randint(1, N), r.randint(1, N)
        if v != w and (v, w) not in pares:
            pares[(v, w)] = r.randint(0, MAXT)
    enlaces = [(v, w, t) for (v, w), t in pares.items()]
    r.shuffle(enlaces)
    return (N, [r.randint(0, MAXT) for _ in range(N)], enlaces)


def cadena_maxima(N):
    """1 → 2 → … → N con todos los tiempos al máximo, y enlaces hacia atrás que no ayudan."""
    enlaces = [(i, i + 1, MAXT) for i in range(1, N)]
    enlaces += [(i + 1, i, 0) for i in range(1, N, 7)]
    return (N, [MAXT] * N, enlaces)


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(71)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (4, [10, 5, 15, 8], [(1, 2, 10), (1, 3, 20), (1, 4, 100), (2, 4, 20), (3, 4, 20)])
    ej2 = (4, [10, 5, 15, 8], [(1, 2, 10), (1, 3, 20), (2, 3, 40), (4, 2, 10)])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF: 53 (pasando por la página 2) e IMPOSIBLE.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: cómo sumas los tiempos de carga, la lectura de la entrada o el formato de la salida.",
            "rte": "Error de ejecución ya con el ejemplo: casi seguro las páginas van del 1 al N y las usas sin restar 1 (el DigrafoValorado lanza una excepción con un vértice que no existe)."},
           ["Haz a mano el primer caso: 10 (carga de la 1) + 10 (enlace) + 5 (carga de la 2) + 20 (enlace) + 8 (carga de la 4) = 53.",
            "Recuerda que la entrada empieza con el número de casos y que las páginas se numeran desde 1.",
            "Escribe solo el número (o IMPOSIBLE) y un salto de línea por caso, sin texto adicional."])
    prueba("Sin enlaces: IMPOSIBLE", "borde", [(2, [3, 4], [])],
           "Dos páginas y ningún enlace: no se puede llegar.",
           {"wa": "Cuando no se puede llegar debes escribir exactamente IMPOSIBLE (en mayúsculas y sin nada más). Si escribes un número, revisa cómo detectas que la página N no se ha alcanzado (su distancia sigue a infinito)."},
           ["¿Qué escribe tu programa si no hay ningún enlace?",
            "Inicializa todas las distancias a infinito y, al final, si la de la página N sigue a infinito, escribe IMPOSIBLE."])
    prueba("La página N solo se alcanza desde páginas inalcanzables", "borde",
           [(4, [1, 1, 1, 1], [(2, 4, 1), (3, 4, 1), (2, 3, 1), (4, 1, 1)])],
           "La página N tiene enlaces de entrada, pero salen de páginas a las que no se llega desde la 1.",
           {"wa": "Que la página N tenga enlaces que lleguen a ella no basta: tienen que salir de páginas alcanzables desde la 1. La respuesta es IMPOSIBLE."},
           ["Desde la página 1 no sale ningún enlace: no se puede ir a ningún sitio.",
            "La respuesta depende solo de la distancia calculada por Dijkstra desde la página 1: si sigue a infinito, IMPOSIBLE."])
    prueba("Enlace directo de la 1 a la N", "borde", [(2, [7, 4], [(1, 2, 9)])],
           "Lo mínimo: dos páginas y un enlace; se cargan las dos y se pulsa el enlace (7 + 9 + 4 = 20).",
           {"wa": "Con un solo enlace el resultado es carga(1) + enlace + carga(N). Si no te sale, revisa qué cargas sumas.",
            "rte": "Error de ejecución con dos páginas: las páginas van del 1 al N; resta 1 al leerlas."},
           ["Debe salir 7 + 9 + 4 = 20.",
            "La página de inicio también se carga: su tiempo va en la distancia inicial, no en 0."])
    prueba("Todos los tiempos a cero", "borde", [(3, [0, 0, 0], [(1, 2, 0), (2, 3, 0)])],
           "Tiempos de carga y de enlace iguales a 0 (el enunciado lo permite): la respuesta es 0, no IMPOSIBLE.",
           {"wa": "Si escribes IMPOSIBLE donde va 0, estás usando la distancia 0 como «no visitada». Usa un infinito de verdad para marcar lo no alcanzado."},
           ["El resultado de este caso es 0.",
            "No uses 0 como valor especial: inicializa las distancias a numeric_limits<int>::max() y compara con eso."])
    prueba("Camino de 3000 páginas con tiempos máximos", "borde", [cadena_maxima(3000)],
           "Una cadena 1 → 2 → … → 3000 con todos los tiempos a 10.000: la respuesta es 59.990.000.",
           {"wa": "El valor que usas como infinito es demasiado pequeño: el tiempo puede llegar a casi 6·10⁷. Usa numeric_limits<int>::max().",
            "tle": "Con 3000 páginas ya se nota el coste: si usas Floyd (N³ ≈ 2,7·10¹⁰) o algo parecido no termina. Basta un Dijkstra desde la página 1."},
           ["Calcula a mano el máximo posible: 3000 cargas y 2999 enlaces de 10.000.",
            "Si tu infinito es 10⁶ o 10⁷, este caso sale IMPOSIBLE: usa numeric_limits<int>::max().",
            "Solo hace falta la distancia desde la página 1: un único Dijkstra, O(M log N)."])
    prueba("Las cargas de las páginas intermedias deciden el camino", "trampa",
           [(4, [0, 100, 0, 0], [(1, 2, 1), (1, 3, 5), (2, 4, 1), (3, 4, 1)])],
           "El camino con los enlaces más rápidos pasa por una página muy lenta de cargar (las páginas 1 y N cargan en 0).",
           {"wa": "Solo sumas el tiempo de los enlaces: la carga de cada página por la que pasas también cuenta. Súmala al coste de la arista que entra en ella."},
           ["Ir por la página 2 cuesta 1 + 100 + 1 = 102 y por la 3, 5 + 0 + 1 = 6.",
            "Cada vez que llegas a una página la tienes que cargar: ese tiempo forma parte del camino.",
            "Al crear el grafo, da a la arista v → w el valor enlace + carga[w]."])
    prueba("La página de inicio también se carga", "trampa", [(3, [25, 0, 0], [(1, 2, 3), (2, 3, 4)])],
           "Solo la página 1 tiene tiempo de carga: debe sumarse aunque no se llegue a ella por ningún enlace.",
           {"wa": "Te falta la carga de la página 1: como no se entra en ella por ningún enlace, no va en ninguna arista. Empieza con dist[origen] = carga[origen] en lugar de 0."},
           ["El resultado es 25 + 3 + 4 = 32, no 7.",
            "Si sumas la carga en la arista que entra en cada página, la de la página 1 se queda fuera.",
            "Inicializa la distancia de la página 1 con su tiempo de carga."])
    prueba("La página final también se carga", "trampa", [(3, [0, 0, 25], [(1, 2, 3), (2, 3, 4)])],
           "Solo la página N tiene tiempo de carga: también se cuenta (el enunciado dice «incluidas la 1 y la N»).",
           {"wa": "Te falta la carga de la página N. Si sumas la carga de la página de la que SALE el enlace, la última nunca se suma: súmala en la arista que entra en ella."},
           ["El resultado es 3 + 4 + 25 = 32, no 7.",
            "¿Sumas carga[v] (página de salida) o carga[w] (página de llegada) en el enlace v → w?",
            "Con coste(v → w) = enlace + carga[w] y dist[1] = carga[1] se cuentan todas las páginas una vez."])
    prueba("Los enlaces tienen sentido", "trampa", [(3, [1, 1, 1], [(2, 1, 1), (3, 2, 1), (1, 3, 50)])],
           "Un enlace de v a w no permite ir de w a v (dígrafo, no grafo): aquí solo vale el enlace directo 1 → 3.",
           {"wa": "Estás recorriendo los enlaces en los dos sentidos. Cada enlace va de la página en la que está a la página a la que lleva: añade solo la arista v → w."},
           ["La respuesta es 1 + 50 + 1 = 52: los enlaces 2 → 1 y 3 → 2 no sirven para ir de la 1 a la 3.",
            "Un DigrafoValorado guarda cada arista solo en la lista de su origen; no añadas también w → v."])
    prueba("Mejorar una distancia ya encontrada", "trampa",
           [(4, [0, 0, 0, 0], [(1, 2, 100), (1, 3, 1), (3, 2, 1), (2, 4, 1)])],
           "A una página se llega primero por un camino caro y después por uno más barato: hay que actualizar su distancia.",
           {"wa": "Fijas la distancia de una página la primera vez que la ves y no la mejoras después. Eso es un recorrido en anchura, no Dijkstra: hay que relajar (si dist[v] + coste < dist[w], actualizar dist[w] y su prioridad)."},
           ["A la página 2 se llega directamente con 100, pero pasando por la 3 solo cuesta 2.",
            "Una distancia solo es definitiva cuando su página sale de la cola de prioridad, no cuando entra.",
            "Relaja cada arista: si mejora, actualiza dist[w] y llama a pq.update(w, dist[w])."])
    prueba("No parar al descubrir la página N", "trampa", [(3, [0, 0, 0], [(1, 3, 50), (1, 2, 1), (2, 3, 1)])],
           "La primera vez que se llega a la página N no tiene por qué ser por el camino más rápido.",
           {"wa": "Terminas en cuanto la página N recibe una distancia, pero esa distancia aún puede mejorar. Solo es definitiva cuando la N sale de la cola de prioridad."},
           ["El enlace directo da 50, pero 1 → 2 → 3 da 2.",
            "Si quieres parar antes, hazlo cuando saques la página N de la cola (pq.top()), no al relajar una arista que llega a ella."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio(r, 9, 30), (4, [1, 1, 1, 1], [(1, 2, 1), (2, 3, 1)]), (3, [5, 5, 5], [(1, 3, 1)]),
            (3, [1, 1, 1], [(3, 1, 1), (2, 1, 1), (3, 2, 1)]), (5, [1, 9, 1, 1, 1], [(1, 2, 0), (1, 3, 1), (3, 4, 1), (4, 2, 1), (2, 5, 1)]),
            (2, [0, 10000], [(1, 2, 10000), (2, 1, 0)]), (5, [0, 0, 0, 0, 0], [(5, 1, 0)]), aleatorio(r, 6, 12)],
           "Un caso grande seguido de otros pequeños (alguno IMPOSIBLE): nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: las distancias, la cola de prioridad o el grafo no se crean de nuevo en cada caso.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: crea el grafo, las distancias y la cola dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso (o son static).",
            "Declara el grafo, dist y la IndexPQ dentro de la función de cada caso, con el N de ese caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(2, 8), r.randint(0, 20)) for _ in range(60)],
           "60 casos pequeños al azar (algunos IMPOSIBLE).",
           {"wa": "Hay algún caso concreto que no tratas bien: mira la línea que falla (es el número de caso) y prueba ese caso a mano.",
            "rte": "Algún caso pequeño rompe el programa: revisa los índices (páginas desde 1) y los casos sin enlaces."},
           ["La línea que falla es el número de caso: búscalo en la entrada.",
            "Dibuja ese grafo con sus cargas y calcula tú el camino; compáralo con lo que hace tu programa paso a paso."])
    prueba("Aleatorios con muchos tiempos a cero", "aleatorio",
           [aleatorio(r, r.randint(2, 9), r.randint(1, 25), ceros=0.5, maxt=9) for _ in range(50)],
           "50 casos pequeños donde la mitad de los tiempos de carga y de enlace son 0.",
           {"wa": "Los tiempos 0 te dan problemas: no uses 0 como marca de «sin visitar» y no supongas que pasar por más páginas siempre cuesta más."},
           ["Busca el caso que falla y fíjate en los ceros.",
            "Dijkstra funciona con aristas de valor 0; lo que falla suele ser usar 0 como valor especial."])
    prueba("Grandes: 3000 páginas y 30.000 enlaces (5 casos)", "rendimiento",
           [grande(r, 3000, 30000) for _ in range(5)],
           "Cinco casos del tamaño máximo: mide la eficiencia.",
           {"tle": "Demasiado lento para 3000 páginas y 30.000 enlaces. Un Dijkstra con IndexPQ es O(M log N); Floyd (N³) o un Bellman-Ford (N·M) no llegan.",
            "mle": "Gastas demasiada memoria: con 3000 páginas una matriz N×N de long long ya son 72 MB; usa listas de adyacencia (DigrafoValorado).",
            "wa": "Falla solo en los grandes: revisa el valor de infinito y que no haya desbordamientos."},
           ["Solo hace falta la distancia desde la página 1: un Dijkstra, no todas las parejas.",
            "Usa DigrafoValorado (listas de adyacencia) e IndexPQ; pasa el grafo por referencia constante."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(salida_caso(c) for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


_DIJKSTRA = """    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        if (v == N - 1) break;                      // ya es definitiva la distancia al destino
        for (auto a : g.ady(v)) {
            int w = a.hasta();
            if (dist[w] > dist[v] + a.valor()) {    // relajacion
                dist[w] = dist[v] + a.valor();
                pq.update(w, dist[w]);
            }
        }
    }"""

_FLOYD = """    vector<vector<int>> D(N, vector<int>(N, INF));
    for (int v = 0; v < N; ++v) { D[v][v] = 0; for (auto a : g.ady(v)) D[v][a.hasta()] = min(D[v][a.hasta()], a.valor()); }
    for (int k = 0; k < N; ++k) for (int i = 0; i < N; ++i) if (D[i][k] != INF) for (int j = 0; j < N; ++j)
        if (D[k][j] != INF && D[i][k] + D[k][j] < D[i][j]) D[i][j] = D[i][k] + D[k][j];
    for (int v = 1; v < N; ++v) dist[v] = (D[0][v] == INF ? INF : dist[0] + D[0][v]);"""

VARIANTES = [
    Variante("solo suma los enlaces (olvida las cargas)",
             [("g.ponArista({v, w, t + carga[w]});", "g.ponArista({v, w, t});"),
              ("dist[0] = carga[0];", "dist[0] = 0;")], prueba=7, v="wa"),
    Variante("olvida la carga de la página 1", [("dist[0] = carga[0];", "dist[0] = 0;")], prueba=8, v="wa"),
    Variante("suma la carga de la página de salida (pierde la de la N)",
             [("g.ponArista({v, w, t + carga[w]});", "g.ponArista({v, w, t + carga[v]});"),
              ("dist[0] = carga[0];", "dist[0] = 0;")], prueba=9, v="wa"),
    Variante("enlaces en los dos sentidos",
             [("g.ponArista({v, w, t + carga[w]});", "g.ponArista({v, w, t + carga[w]}); g.ponArista({w, v, t + carga[v]});")],
             prueba=10, v="wa"),
    Variante("fija la distancia la primera vez (sin mejorar)",
             [("if (dist[w] > dist[v] + a.valor()) {    // relajacion", "if (dist[w] == INF) {")], prueba=11, v="wa"),
    Variante("para al descubrir la página N",
             [("                pq.update(w, dist[w]);\n",
               "                pq.update(w, dist[w]);\n                if (w == N - 1) { while (!pq.empty()) pq.pop(); break; }\n")],
             prueba=12, v="wa"),
    Variante("distancias no reiniciadas entre casos (static)",
             [("vector<int> dist(N, INF);", "static vector<int> dist; dist.resize(N, INF);")], prueba=13, v="wa"),
    Variante("usa 0 como «sin visitar»",
             [("vector<int> dist(N, INF);", "vector<int> dist(N, 0);"),
              ("if (dist[w] > dist[v] + a.valor()) {    // relajacion", "if (dist[w] == 0 || dist[w] > dist[v] + a.valor()) {"),
              ("if (dist[N - 1] == INF) cout", "if (dist[N - 1] == 0) cout")], prueba=5, v="wa"),
    Variante("infinito demasiado pequeño (10⁶)",
             [("const int INF = numeric_limits<int>::max();", "const int INF = 1000000;")], prueba=6, v="wa"),
    Variante("escribe Imposible en minúsculas", [('cout << "IMPOSIBLE\\n";', 'cout << "Imposible\\n";')], prueba=2, v="wa"),
    Variante("Floyd en lugar de Dijkstra", [(_DIJKSTRA, _FLOYD)], prueba=6, v="tle"),
]
