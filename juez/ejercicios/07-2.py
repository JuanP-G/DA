"""07-2 · Camino al cole: juez con pruebas pensadas para cada error típico.

Grafo NO dirigido valorado; hay que contar cuántos caminos de longitud mínima van de la
intersección 1 a la N (0 si no hay camino; 1 si N = 1).
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-2/EJ_07-2.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-2/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-2/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["formas[w] += formas[v];", "formas[w] += 1;"],
}

MAXL = 10_000


# ---------------------------------------------------------------- solucionador independiente
def formas(N, calles):
    """Cuenta los caminos mínimos de 1 a N: Dijkstra y, después, programación dinámica sobre
    los vértices en orden de distancia (los predecesores de v en caminos mínimos están antes)."""
    ady = [[] for _ in range(N + 1)]
    for u, v, l in calles:
        ady[u].append((v, l))
        ady[v].append((u, l))
    INF = float("inf")
    dist = [INF] * (N + 1)
    dist[1] = 0
    cola = [(0, 1)]
    orden = []
    while cola:
        d, v = heapq.heappop(cola)
        if d > dist[v]:
            continue
        orden.append(v)
        for w, l in ady[v]:
            if d + l < dist[w]:
                dist[w] = d + l
                heapq.heappush(cola, (d + l, w))
    cuenta = [0] * (N + 1)
    cuenta[1] = 1
    for v in orden:                       # orden creciente de distancia (las calles miden ≥ 1)
        for w, l in ady[v]:
            if dist[v] + l == dist[w]:
                cuenta[w] += cuenta[v]
    return cuenta[N]


def valida(caso):
    N, calles = caso
    assert 1 <= N <= 100_000 and 0 <= len(calles) <= 200_000
    pares = set()
    for u, v, l in calles:
        assert 1 <= u <= N and 1 <= v <= N and u != v and 1 <= l <= MAXL
        k = (min(u, v), max(u, v))
        assert k not in pares, "dos calles entre el mismo par de intersecciones"
        pares.add(k)
    assert formas(N, calles) < 2 ** 31


def caso_a_texto(caso):
    N, calles = caso
    return f"{N}\n{len(calles)}\n" + "".join(f"{u} {v} {l}\n" for u, v, l in calles)


# ---------------------------------------------------------------- generadores
def aleatorio(r, N, C, maxl):
    C = min(C, N * (N - 1) // 2)
    pares = set()
    while len(pares) < C:
        u, v = r.randint(1, N), r.randint(1, N)
        if u != v:
            pares.add((min(u, v), max(u, v)))
    calles = [((u, v) if r.random() < .5 else (v, u)) + (r.randint(1, maxl),) for u, v in pares]
    r.shuffle(calles)
    return (N, calles)


def diamantes(k):
    """k rombos seguidos con lados de longitud 1: 2^k caminos mínimos de 1 a N."""
    calles, s, n = [], 1, 1
    for _ in range(k):
        a, b, t = n + 1, n + 2, n + 3
        calles += [(s, a, 1), (s, b, 1), (a, t, 1), (b, t, 1)]
        s, n = t, n + 3
    return (n, calles)


def cadena(N, l):
    """1 - 2 - … - N, todas de longitud l, escritas en orden aleatorio y sentido al azar."""
    r = rng(N)
    calles = [((i, i + 1) if r.random() < .5 else (i + 1, i)) + (l,) for i in range(1, N)]
    r.shuffle(calles)
    return (N, calles)


def rejilla(r, F, C, fila, col):
    """Rejilla F×C con calles de longitud 1, numerada al azar: la casa en la esquina (0, 0) y el
    colegio en (fila, col). Hay muchísimos empates (en el resto de la rejilla el número de caminos
    mínimos no cabe ni en 64 bits), pero al colegio llegan C(fila+col, fila) caminos."""
    ids = list(range(2, F * C))
    r.shuffle(ids)
    num, k = {}, 0
    for i in range(F):
        for j in range(C):
            if (i, j) == (0, 0):
                num[i, j] = 1
            elif (i, j) == (fila, col):
                num[i, j] = F * C
            else:
                num[i, j] = ids[k]; k += 1
    calles = []
    for i in range(F):
        for j in range(C):
            if i + 1 < F: calles.append((num[i, j], num[i + 1, j], 1))
            if j + 1 < C: calles.append((num[i, j], num[i, j + 1], 1))
    r.shuffle(calles)
    return (F * C, calles)


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(72)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (7, [(1, 2, 5), (1, 3, 7), (2, 4, 10), (3, 4, 8), (2, 5, 30), (4, 5, 12), (4, 7, 25), (4, 6, 11), (5, 7, 13), (6, 7, 30)])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, (4, [(1, 2, 3), (3, 4, 5)]), (1, [])],
           "Los tres casos del PDF: 4 formas, 0 (no se llega) y 1 (casa y colegio en el mismo sitio).",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: además de la distancia mínima hay que llevar, para cada intersección, cuántos caminos mínimos llegan a ella.",
            "rte": "Error de ejecución con el ejemplo: las intersecciones van del 1 al N (resta 1) y N puede ser 1 sin ninguna calle."},
           ["En el dibujo hay 4 caminos de longitud 40 de la 1 a la 7: sigue tu programa a mano con ese grafo.",
            "Lleva un vector formas[v]: cuántos caminos mínimos hay de la 1 a v.",
            "Al relajar v → w: si mejora, formas[w] = formas[v]; si empata, formas[w] += formas[v]."])
    prueba("Una sola intersección", "borde", [(1, [])],
           "N = 1: la casa es el colegio y hay exactamente una forma de ir (no moverse).",
           {"wa": "Con N = 1 la respuesta es 1, no 0: el número de formas de llegar al origen es 1 (formas[origen] = 1 al empezar).",
            "rte": "Con N = 1 y ninguna calle algo se sale del vector o accede a una posición que no existe."},
           ["¿Cuánto vale formas de la intersección de partida antes de empezar?",
            "Inicializa formas[0] = 1 (el camino vacío) y no trates el origen como un caso especial al relajar."])
    prueba("Sin calles", "borde", [(2, [])],
           "Dos intersecciones y ninguna calle: 0 formas.",
           {"wa": "Si no se puede llegar al colegio, el número de formas es 0."},
           ["Si nunca se relaja ninguna arista, formas[N-1] debe quedarse en 0.",
            "No escribas la distancia ni ningún texto: solo el número de formas."])
    prueba("Colegio en otra zona del pueblo", "borde", [(5, [(1, 2, 3), (2, 3, 4), (4, 5, 2)])],
           "Las calles no conectan la casa con el colegio: 0 formas.",
           {"wa": "El colegio está en otra componente: la respuesta es 0. Revisa que formas empiece a 0 para todos menos el origen."},
           ["Desde la 1 solo se llega a la 2 y la 3.",
            "Inicializa formas a 0 en todos los vértices salvo el origen."])
    prueba("Un único camino", "borde", [(5, [(4, 5, 7), (1, 2, 3), (3, 4, 1), (2, 3, 9)])],
           "Una cadena 1 - 2 - 3 - 4 - 5: una sola forma.",
           {"wa": "Solo hay un camino posible: si sale otra cosa, revisa la inicialización de formas o la lectura de las calles."},
           ["Debe salir 1.",
            "Cada vez que mejoras dist[w], formas[w] pasa a valer formas[v]."])
    prueba("Calles de doble sentido", "trampa", [(3, [(2, 1, 4), (3, 2, 4)])],
           "Las calles vienen escritas «hacia atrás» (2 1 y 3 2): Lucas puede recorrerlas en los dos sentidos.",
           {"wa": "Solo añades cada calle en un sentido. Lucas no respeta el sentido: en el DigrafoValorado hay que poner las dos aristas, u → v y v → u."},
           ["Con las calles «2 1» y «3 2» hay que poder ir 1 → 2 → 3.",
            "Por cada calle llama dos veces a ponArista: {u, v, l} y {v, u, l}."])
    prueba("Dos caminos de igual longitud", "trampa", [(4, [(1, 2, 1), (1, 3, 1), (2, 4, 1), (3, 4, 1)])],
           "Un rombo: dos caminos de longitud 2 (1-2-4 y 1-3-4).",
           {"wa": "Solo cuentas un camino: cuando dist[v] + l == dist[w] (empate) también hay que sumar. También pasa si terminas en cuanto el colegio recibe su primera distancia: puede llegar otro camino igual de corto después."},
           ["La respuesta es 2.",
            "En Dijkstra normal, si la nueva distancia es igual no se hace nada; aquí sí: es otra manera de llegar.",
            "Si empata: formas[w] += formas[v]. Y si quieres parar antes, hazlo al SACAR el colegio de la cola, nunca al descubrirlo."])
    prueba("Al empatar se suman las formas del vecino", "trampa",
           [(7, [(1, 2, 1), (1, 3, 1), (2, 4, 1), (3, 4, 1), (4, 5, 1), (4, 6, 1), (5, 7, 1), (6, 7, 1)])],
           "Dos rombos seguidos: 2 · 2 = 4 caminos. Al empatar no se suma 1, se suman las formas del vecino.",
           {"wa": "Al empatar sumas 1, pero por el vecino pueden llegar muchos caminos mínimos: hay que sumar formas[v], no 1."},
           ["La respuesta es 4: a la intersección 4 llegan 2 caminos y cada uno sigue de 2 maneras.",
            "Si a v llegan formas[v] caminos mínimos, cada uno se puede alargar con la calle v → w.",
            "Empate: formas[w] += formas[v]."])
    prueba("Un camino más corto anula los anteriores", "trampa", [(4, [(1, 3, 10), (1, 2, 1), (2, 3, 1), (3, 4, 1)])],
           "A la 3 se llega primero por la calle directa (10) y luego por la 2 (2): el camino de 10 ya no cuenta.",
           {"wa": "Cuando encuentras un camino más corto sumas en vez de sustituir: los caminos anteriores dejan de ser mínimos. Si mejora, formas[w] = formas[v]."},
           ["La respuesta es 1: solo 1-2-3-4 mide 3.",
            "Distingue los dos casos: si dist[v] + l < dist[w], formas[w] = formas[v] (se olvida lo anterior); si es igual, formas[w] += formas[v]."])
    prueba("El camino con menos calles no es el más corto", "trampa",
           [(4, [(1, 4, 10), (1, 2, 1), (2, 4, 1), (1, 3, 1), (3, 4, 1)])],
           "La calle directa 1-4 mide 10; los dos caminos de dos calles miden 2: hay 2 formas.",
           {"wa": "Cuentas caminos con el menor número de calles (recorrido en anchura), pero lo que cuenta es la longitud: usa Dijkstra con las longitudes de las calles."},
           ["La respuesta es 2 (1-2-4 y 1-3-4), no 1.",
            "Un BFS solo sirve si todas las calles miden lo mismo; aquí hay que usar Dijkstra."])
    prueba("Varios casos seguidos", "trampa",
           [(5, [(1, 2, 1), (1, 3, 1), (2, 4, 1), (3, 4, 1), (4, 5, 1)]), (4, [(1, 2, 2), (3, 4, 2)]),
            aleatorio(r, 9, 16, 3), (3, [(1, 2, 1), (2, 3, 1), (1, 3, 2)]), (2, []), (1, []), aleatorio(r, 6, 8, 2)],
           "Un caso con caminos seguido de otro en el que no se llega (y más casos): nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: el vector de formas, las distancias o el grafo no se crean de nuevo en cada caso. Fíjate en el caso sin camino: debe dar 0.",
            "rte": "Usas en un caso una estructura con el tamaño de un caso anterior: créalas dentro de resuelveCaso con el N de ese caso."},
           ["El segundo caso no tiene camino: si escribes algo distinto de 0, es un valor del caso anterior.",
            "Declara el grafo, dist, formas y la cola dentro de resuelveCaso."])
    prueba("Muchísimos caminos mínimos (2³⁰)", "trampa", [diamantes(30)],
           "30 rombos seguidos: 2³⁰ = 1.073.741.824 caminos mínimos en un grafo de solo 91 intersecciones.",
           {"tle": "Estás recorriendo los caminos uno a uno (con una búsqueda en profundidad o recursión sin memoria): con 2³⁰ caminos no termina. Hay que contarlos dentro del propio Dijkstra.",
            "wa": "El número no te cabe: 2³⁰ cabe en int, pero si usas short o haces alguna multiplicación intermedia, se desborda."},
           ["No hace falta enumerar los caminos, solo contarlos.",
            "Cada intersección guarda cuántos caminos mínimos llegan a ella; se calcula a partir de los de sus vecinos ya definitivos.",
            "Cuéntalo en el mismo Dijkstra: al mejorar, formas[w] = formas[v]; al empatar, formas[w] += formas[v]."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(1, 9), r.randint(0, 20), r.choice([1, 2, 3, 10])) for _ in range(60)],
           "60 casos pequeños al azar, con calles cortas para que haya muchos empates.",
           {"wa": "Hay algún caso concreto que no tratas bien: la línea que falla es el número de caso; dibújalo y cuenta los caminos a mano.",
            "rte": "Algún caso pequeño rompe el programa: revisa N = 1, los casos sin calles y los índices desde 1."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Dibuja el grafo y escribe junto a cada intersección su distancia y su número de caminos mínimos."])
    prueba("Aleatorios con muchos empates", "aleatorio",
           [aleatorio(r, r.randint(5, 14), r.randint(8, 40), 2) for _ in range(40)],
           "40 casos algo más densos con calles de longitud 1 o 2.",
           {"wa": "Con muchos empates algo se cuenta mal: comprueba que sumas en los empates y sustituyes al mejorar."},
           ["Busca el caso que falla y cuenta a mano los caminos mínimos de cada intersección.",
            "formas[v] es definitivo cuando v sale de la cola; a partir de entonces solo se usa para sumar a sus vecinos."])
    prueba("Camino de 100.000 intersecciones", "rendimiento", [cadena(100_000, MAXL)],
           "Una cadena de 100.000 intersecciones con calles de 10.000: distancias de casi 10⁹.",
           {"tle": "Tu Dijkstra no es O(C log N): si buscas el mínimo recorriendo todo el vector de distancias cada vez, con 100.000 intersecciones son 10¹⁰ pasos. Usa la IndexPQ.",
            "wa": "La distancia llega a casi 10⁹: comprueba que tu infinito es mayor (numeric_limits<int>::max()).",
            "rte": "Con 100.000 intersecciones algo se rompe: ¿una recursión de 100.000 niveles o un vector demasiado grande?"},
           ["Usa una cola de prioridad indexada (IndexPQ) para sacar el vértice más cercano.",
            "Comprueba el valor de infinito: las distancias llegan a 999.990.000."])
    prueba("Rejilla con muchísimos empates", "rendimiento", [rejilla(r, 250, 250, 15, 15)],
           "Una rejilla de 250×250 con calles de longitud 1 (unos 125.000 tramos): al colegio llegan C(30,15) = 155.117.520 caminos.",
           {"tle": "Demasiado lento con 62.500 intersecciones: el Dijkstra debe ser O(C log N) y el recuento, parte del mismo recorrido.",
            "wa": "En el resto de la rejilla el número de caminos es gigantesco y se desborda; eso no debe afectar al colegio. Si falla, revisa que sumas y sustituyes en el orden correcto."},
           ["El número de caminos de otras intersecciones puede desbordarse sin problema (con unsigned no afecta al resultado).",
            "Lo que no puede ser es recorrer los caminos uno a uno: cuéntalos dentro de Dijkstra."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(f"{formas(*c)}\n" for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


_LINEAL = ("    vector<bool> hecho(N, false);\n    while (true) {\n        int v = -1;\n"
           "        for (int u = 0; u < N; ++u) if (!hecho[u] && dist[u] != INF && (v == -1 || dist[u] < dist[v])) v = u;\n"
           "        if (v == -1) break;\n        hecho[v] = true;\n")

_DFS = """    auto cuenta = [&](auto&& self, int v) -> unsigned long long {
        if (v == N - 1) return 1;
        unsigned long long s = 0;
        for (auto a : g.ady(v))
            if (dist[a.hasta()] != INF && dist[a.hasta()] == dist[v] + a.valor()) s += self(self, a.hasta());
        return s;
    };
    cout << (dist[N - 1] == INF ? 0ULL : cuenta(cuenta, 0)) << '\\n';"""

VARIANTES = [
    Variante("calles de un solo sentido", [("        g.ponArista({v, u, l});\n", "")], prueba=6, v="wa"),
    Variante("no suma en los empates", [("            } else if (d == dist[w]) {\n                formas[w] += formas[v];\n            }",
                                         "            }")], prueba=7, v="wa"),
    Variante("para al descubrir el colegio",
             [("                pq.update(w, d);\n", "                pq.update(w, d);\n                if (w == N - 1) { while (!pq.empty()) pq.pop(); break; }\n")],
             prueba=7, v="wa"),
    Variante("al empatar suma 1", [("formas[w] += formas[v];", "formas[w] += 1;")], prueba=8, v="wa"),
    Variante("al mejorar suma en vez de sustituir", [("formas[w] = formas[v];", "formas[w] += formas[v];")], prueba=9, v="wa"),
    Variante("el origen como caso especial (N = 1 da 0)",
             [("formas[0] = 1;", "formas[0] = 0;"), ("formas[w] = formas[v];", "formas[w] = (v == 0 ? 1 : formas[v]);")],
             prueba=2, v="wa"),
    Variante("cuenta caminos con menos calles (BFS)",
             [("g.ponArista({u, v, l});", "g.ponArista({u, v, 1});"), ("g.ponArista({v, u, l});", "g.ponArista({v, u, 1});")],
             prueba=10, v="wa"),
    Variante("formas no reiniciado entre casos (static)",
             [("vector<unsigned long long> formas(N, 0);", "static vector<unsigned long long> formas; formas.resize(N, 0);")],
             prueba=11, v="wa"),
    Variante("cuenta los caminos con una DFS sin memoria", [("    cout << formas[N - 1] << '\\n';   // 0 si no se llega", _DFS)],
             prueba=12, v="tle"),
    Variante("Dijkstra buscando el mínimo en el vector (O(N²))",
             [("    while (!pq.empty()) {\n        int v = pq.top().elem; pq.pop();\n", _LINEAL)], prueba=15, v="tle"),
]
