"""07-5 · ¿Cuál es el mejor camino?: juez con pruebas pensadas para cada error típico.

Grafo no dirigido valorado. Para cada consulta: distancia mínima y SI si algún camino de esa
distancia usa además el menor número de calles posible entre los dos puntos (NO si no), o
SIN CAMINO; «---» tras cada caso. En el juez de la asignatura la entrada empieza con el número
de casos (el ejemplo del PDF, sacado de Acepta el Reto, no lo trae: aquí se le añade).
"""
import heapq
from collections import deque
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-5/EJ_07-5.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-5/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-5/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["if (nuevo < mejor[w]) {", "if (nuevo.first < mejor[w].first) {"],
}

MAXL = 5000


# ---------------------------------------------------------------- solucionador independiente
def consulta(N, ady, o, d):
    """(distancia, ¿SI?) o None. Dijkstra normal; luego, recorriendo los vértices en orden de
    distancia, el mínimo de calles entre los caminos más cortos; y un BFS para el mínimo absoluto."""
    INF = float("inf")
    dist = [INF] * (N + 1)
    dist[o] = 0
    cola = [(0, o)]
    orden = []
    while cola:
        x, v = heapq.heappop(cola)
        if x > dist[v]:
            continue
        orden.append(v)
        for w, l in ady[v]:
            if x + l < dist[w]:
                dist[w] = x + l
                heapq.heappush(cola, (x + l, w))
    if dist[d] == INF:
        return None
    pocas = [INF] * (N + 1)          # menos calles entre los caminos de distancia mínima
    pocas[o] = 0
    for v in orden:
        for w, l in ady[v]:
            if dist[v] + l == dist[w]:
                pocas[w] = min(pocas[w], pocas[v] + 1)
    saltos = [-1] * (N + 1)
    saltos[o] = 0
    q = deque([o])
    while q:
        v = q.popleft()
        for w, _ in ady[v]:
            if saltos[w] < 0:
                saltos[w] = saltos[v] + 1
                q.append(w)
    return dist[d], pocas[d] == saltos[d]


def salida_caso(caso):
    N, calles, consultas = caso
    ady = [[] for _ in range(N + 1)]
    for u, v, l in calles:
        ady[u].append((v, l))
        ady[v].append((u, l))
    s = ""
    for o, d in consultas:
        r = consulta(N, ady, o, d)
        s += "SIN CAMINO\n" if r is None else f"{r[0]} {'SI' if r[1] else 'NO'}\n"
    return s + "---\n"


def valida(caso):
    N, calles, consultas = caso
    assert 2 <= N <= 20000 and 0 <= len(calles) <= 100000 and 1 <= len(consultas) <= 10
    pares = set()
    for u, v, l in calles:
        assert 1 <= u <= N and 1 <= v <= N and u != v and 1 <= l <= MAXL
        k = (min(u, v), max(u, v))
        assert k not in pares, "calle repetida (el enunciado no lo prohíbe, pero no lo usamos)"
        pares.add(k)
    for o, d in consultas:
        assert 1 <= o <= N and 1 <= d <= N and o != d


def caso_a_texto(caso):
    N, calles, consultas = caso
    return (f"{N}\n{len(calles)}\n" + "".join(f"{u} {v} {l}\n" for u, v, l in calles)
            + f"{len(consultas)}\n" + "".join(f"{o} {d}\n" for o, d in consultas))


# ---------------------------------------------------------------- generadores
def consultas_al_azar(r, N, K):
    out = []
    while len(out) < K:
        o, d = r.randint(1, N), r.randint(1, N)
        if o != d:
            out.append((o, d))
    return out


def aleatorio(r, N, C, K, maxl):
    C = min(C, N * (N - 1) // 2)
    pares = set()
    while len(pares) < C:
        u, v = r.sample(range(1, N + 1), 2)
        pares.add((min(u, v), max(u, v)))
    calles = [((u, v) if r.random() < .5 else (v, u)) + (r.randint(1, maxl),) for u, v in pares]
    r.shuffle(calles)
    return (N, calles, consultas_al_azar(r, N, K))


def grande(r, N, C, K):
    pares = set()
    calles = []
    for i in range(2, N + 1):
        u = r.randint(max(1, i - 50), i - 1)        # conexo y con caminos largos
        pares.add((u, i))
        calles.append((u, i, r.randint(1, MAXL)))
    while len(calles) < C:
        u, v = r.sample(range(1, N + 1), 2)
        if abs(u - v) > 60:
            continue
        k = (min(u, v), max(u, v))
        if k not in pares:
            pares.add(k)
            calles.append((u, v, r.randint(1, MAXL)))
    r.shuffle(calles)
    consultas = [(r.randint(1, 100), r.randint(N - 100, N)) for _ in range(K)]
    return (N, calles, consultas)


def rejilla(r, F, C, K):
    """Rejilla F×C con calles de longitud 1 o 2: muchísimos caminos empatados."""
    num = lambda i, j: i * C + j + 1
    calles = []
    for i in range(F):
        for j in range(C):
            if i + 1 < F: calles.append((num(i, j), num(i + 1, j), r.randint(1, 2)))
            if j + 1 < C: calles.append((num(i, j), num(i, j + 1), r.randint(1, 2)))
    r.shuffle(calles)
    consultas = [(num(r.randrange(F // 4), r.randrange(C)), num(F - 1 - r.randrange(F // 4), r.randrange(C))) for _ in range(K)]
    return (F * C, calles, consultas)


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(75)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (7, [(1, 2, 10), (2, 3, 7), (3, 5, 10), (1, 4, 15), (4, 5, 15), (4, 6, 5), (5, 7, 4), (6, 7, 15)], [(1, 5), (6, 5)])
    ej2 = (5, [(1, 2, 5), (2, 3, 5), (3, 1, 5), (4, 5, 10)], [(1, 2), (1, 5)])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF (con el número de casos delante): «27 NO», «19 SI», «5 SI», «SIN CAMINO».",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: hay que comparar las calles del camino más corto (el de menos calles entre los más cortos) con el menor número de calles posible (anchura).",
            "pe": "Los datos están bien pero el formato no: un espacio entre la distancia y SI/NO, un salto de línea por consulta y --- tras cada caso.",
            "rte": "Error de ejecución con el ejemplo: la entrada empieza con el número de casos; si lees hasta fin de fichero o no restas 1 a las intersecciones, se rompe."},
           ["En el juez de la asignatura la primera línea es el número de casos (plantilla de número de casos).",
            "1 → 5: el más corto (27) usa 3 calles y 1 → 4 → 5 solo 2: NO.",
            "Escribe --- después de todas las consultas de cada caso."])
    prueba("Calle directa", "borde", [(2, [(1, 2, 7)], [(1, 2)])],
           "Dos intersecciones y una calle: «7 SI».",
           {"wa": "Con una sola calle el camino más corto es también el de menos calles: «7 SI».",
            "rte": "Error de ejecución en el caso más pequeño: revisa los índices (desde 1) y la lectura."},
           ["Debe salir «7 SI».",
            "La distancia y la palabra van en la misma línea, separadas por un espacio."])
    prueba("Sin calles: SIN CAMINO", "borde", [(3, [], [(1, 2), (3, 1)])],
           "Ninguna calle: todas las consultas son SIN CAMINO (sin distancia) y aun así se escribe ---.",
           {"wa": "Si no hay camino se escribe solo SIN CAMINO (sin distancia ni SI/NO) y, al acabar el caso, ---."},
           ["Comprueba si la distancia al destino sigue a infinito antes de escribir nada más.",
            "La línea --- se escribe siempre al acabar el caso."])
    prueba("Calles de doble sentido", "trampa", [(3, [(2, 1, 4), (3, 2, 4)], [(1, 3)])],
           "Las calles vienen escritas «hacia atrás» (2 1 y 3 2): se recorren en los dos sentidos.",
           {"wa": "Solo añades cada calle en un sentido. Son de doble sentido: pon las dos aristas, u → v y v → u (también para la anchura)."},
           ["Debe salir «8 SI».",
            "Por cada calle llama dos veces a ponArista."])
    prueba("El camino más corto usa más calles: NO", "trampa", [(5, [(1, 4, 5), (1, 2, 1), (4, 5, 5), (2, 3, 1), (3, 5, 1)], [(1, 5)])],
           "1-4-5 tiene dos calles pero mide 10; 1-2-3-5 tiene tres y mide 3: «3 NO».",
           {"wa": "La distancia que escribes no es la mínima: lo primero es la distancia (Dijkstra) y solo para desempatar se miran las calles. La prioridad es (distancia, calles), en ese orden."},
           ["Debe salir «3 NO»: el más corto mide 3 y usa 3 calles, pero se puede llegar con 2.",
            "Compara las parejas en orden lexicográfico: primero la distancia, luego las calles."])
    prueba("No parar al descubrir el destino", "trampa",
           [(4, [(1, 2, 1), (2, 4, 1), (1, 4, 5), (3, 4, 7)], [(1, 4)])],
           "La primera vez que se llega al destino es por la calle directa (5), pero por la 2 se recorren 2: «2 NO».",
           {"wa": "Paras en cuanto el destino recibe una distancia, pero aún puede mejorar. Solo es definitiva cuando el destino sale de la cola."},
           ["Debe salir «2 NO».",
            "Puedes parar cuando el destino esté en la cabeza de la cola, no al relajar una calle que llega a él."])
    prueba("Empate en distancia: el de menos calles se descubre después", "trampa",
           [(5, [(1, 2, 1), (2, 3, 1), (3, 5, 8), (1, 4, 9), (4, 5, 1)], [(1, 5)])],
           "Dos caminos de 10: 1-2-3-5 (3 calles, se encuentra antes) y 1-4-5 (2 calles, después). Hay que quedarse con el de 2: «10 SI».",
           {"wa": "Ante un empate en distancia te quedas con el primer camino encontrado. Entre los caminos de distancia mínima hay que quedarse con el de MENOS calles: actualiza también si la distancia empata y las calles mejoran."},
           ["Debe salir «10 SI».",
            "Guarda para cada vértice la pareja (distancia, calles) y actualiza si la nueva pareja es menor en orden lexicográfico.",
            "Con pair<int,int> basta comparar «nuevo < mejor[w]»; la IndexPQ<pair<int,int>> ordena igual."])
    prueba("Empate en distancia: el de menos calles se descubre antes", "trampa",
           [(5, [(1, 4, 1), (4, 5, 9), (1, 2, 2), (2, 3, 2), (3, 5, 6)], [(1, 5)])],
           "Dos caminos de 10: 1-4-5 (2 calles, se encuentra antes) y 1-2-3-5 (3 calles, después). No hay que cambiarlo: «10 SI».",
           {"wa": "Cambias el camino de un vértice cuando la distancia empata aunque tenga más calles (≤ en vez de <). Solo hay que cambiar si la distancia mejora o, empatando, las calles mejoran."},
           ["Debe salir «10 SI».",
            "Si comparas solo distancias con ≤, el último camino empatado sustituye al anterior aunque sea peor en calles."])
    prueba("Varias consultas desde distintos orígenes", "trampa",
           [(6, [(1, 2, 2), (2, 3, 2), (3, 4, 2), (4, 5, 2), (5, 6, 2), (1, 6, 3), (2, 5, 9)], [(1, 4), (6, 3), (4, 1), (5, 2), (3, 6)])],
           "Cuatro consultas en el mismo caso, cada una desde un origen distinto: cada una empieza de cero.",
           {"wa": "La primera consulta sale bien y las siguientes no: los vectores del Dijkstra o de la anchura de la consulta anterior se quedan. Créalos de nuevo en cada consulta."},
           ["Si la primera consulta sale bien y la segunda no, mira qué se reutiliza entre consultas.",
            "Declara los vectores (distancias, calles) y la cola dentro del bucle de las consultas."])
    prueba("SIN CAMINO entre otras consultas", "trampa",
           [(5, [(1, 2, 3), (3, 4, 1), (4, 5, 1), (3, 5, 3)], [(2, 1), (1, 5), (5, 3)])],
           "Una consulta sin camino en medio de otras: las demás deben salir bien y --- solo al final.",
           {"wa": "Tras un SIN CAMINO algo se descoloca: revisa que no escribes --- tras cada consulta ni dejas de leer las siguientes."},
           ["Debe salir «3 SI», «SIN CAMINO», «2 NO» y ---.",
            "El --- va una vez por caso, después del bucle de las consultas."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio(r, 9, 14, 4, 3), ej2, (3, [(1, 2, 1), (2, 3, 1), (1, 3, 2)], [(1, 3), (3, 1)]), aleatorio(r, 5, 4, 2, 9),
            (2, [], [(2, 1)])],
           "Un caso con varias consultas seguido de otros más pequeños: nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: el grafo o los vectores de distancias y calles no se crean de nuevo en cada caso.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: créalas dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo dentro de resuelveCaso y los vectores dentro del bucle de consultas."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(2, 9), r.randint(0, 16), r.randint(1, 4), r.choice([3, 10, 5000])) for _ in range(50)],
           "50 casos pequeños al azar.",
           {"wa": "Hay alguna consulta que no tratas bien: localiza el caso contando las líneas --- y prueba ese grafo a mano."},
           ["Cada caso termina en ---: así localizas el caso que falla.",
            "Calcula a mano la distancia mínima, las calles del camino más corto con menos calles y el mínimo de calles posible."])
    prueba("Aleatorios con muchos empates", "aleatorio",
           [aleatorio(r, r.randint(6, 16), r.randint(10, 40), 10, 2) for _ in range(40)],
           "40 casos con calles de longitud 1 o 2: hay muchos caminos de la misma distancia con distinto número de calles.",
           {"wa": "Con empates en distancia algo falla: entre los caminos más cortos hay que quedarse con el de menos calles."},
           ["Busca la consulta que falla y enumera a mano los caminos más cortos.",
            "La prioridad (distancia, calles) se compara en orden lexicográfico."])
    prueba("Grande: 20.000 intersecciones y 100.000 calles", "rendimiento", [grande(r, 20000, 100000, 10)],
           "El tamaño máximo con 10 consultas entre puntos lejanos.",
           {"tle": "Demasiado lento: cada consulta necesita un Dijkstra O(C log N) con IndexPQ y una anchura O(N + C). Si buscas el mínimo recorriendo el vector (O(N²)), con 20.000 intersecciones y 10 consultas no llega.",
            "mle": "Gastas demasiada memoria: no uses una matriz N×N.",
            "wa": "Solo falla en el grande: revisa el valor de infinito."},
           ["Usa una IndexPQ para elegir el siguiente vértice.",
            "Construye el grafo una vez por caso y haz los dos recorridos por consulta."])
    prueba("Rejilla con muchísimos empates", "rendimiento", [rejilla(r, 140, 140, 10)],
           "Rejilla de 140×140 con calles de longitud 1 o 2 y 10 consultas de arriba abajo.",
           {"tle": "Demasiado lento en una rejilla de casi 20.000 intersecciones: revisa la complejidad del Dijkstra y de la anchura.",
            "wa": "Con muchísimos empates algo falla: entre los caminos más cortos hay que quedarse con el de menos calles."},
           ["La prioridad (distancia, calles) resuelve los empates sin coste extra.",
            "Marca los visitados de la anchura al meterlos en la cola, no al sacarlos."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(salida_caso(c) for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


_LINEAL = ("        vector<bool> hecho(N, false);\n        while (true) {\n            int v = -1;\n"
           "            for (int u = 0; u < N; ++u) if (!hecho[u] && mejor[u].first != INF && (v == -1 || mejor[u] < mejor[v])) v = u;\n"
           "            if (v == -1 || v == destino) break;\n            hecho[v] = true;\n")

VARIANTES = [
    Variante("calles de un solo sentido", [("        g.ponArista({v, u, d});\n", "")], prueba=4, v="wa"),
    Variante("prioridad (calles, distancia) en vez de (distancia, calles)",
             [("if (nuevo < mejor[w]) {", "if (Par(nuevo.second, nuevo.first) < Par(mejor[w].second, mejor[w].first)) {"),
              ("pq.update(w, nuevo);", "pq.update(w, Par(nuevo.second, nuevo.first));")], prueba=5, v="wa"),
    Variante("solo compara distancias (se queda el primer empate)",
             [("if (nuevo < mejor[w]) {", "if (nuevo.first < mejor[w].first) {")], prueba=7, v="wa"),
    Variante("compara distancias con ≤ (se queda el último empate)",
             [("if (nuevo < mejor[w]) {", "if (nuevo.first <= mejor[w].first) {")], prueba=8, v="wa"),
    Variante("vector del Dijkstra compartido entre consultas",
             [("        vector<Par> mejor(N, {INF, INF});\n", ""),
              ("    int K; cin >> K;\n", "    int K; cin >> K;\n    vector<Par> mejor(N, {INF, INF});\n")], prueba=9, v="wa"),
    Variante("para al descubrir el destino",
             [("                    pq.update(w, nuevo);\n",
               "                    pq.update(w, nuevo);\n                    if (w == destino) { while (!pq.empty()) pq.pop(); break; }\n")],
             prueba=6, v="wa"),
    Variante("dos espacios antes de SI/NO", [('" SI\\n" : " NO\\n"', '"  SI\\n" : "  NO\\n"')], prueba=1, v="pe"),
    Variante("Dijkstra buscando el mínimo en el vector (O(N²))",
             [("        while (!pq.empty() && pq.top().elem != destino) {\n            int v = pq.top().elem; pq.pop();\n", _LINEAL)],
             prueba=14, v="tle"),
]
