"""07-4 · La conferencia de paz: juez con pruebas pensadas para cada error típico.

Grafo no dirigido valorado y conexo. Para cada aldea neutral, diferencia entre la distancia a la
aldea gala más cercana y a la romana más cercana; se elige la menor diferencia (en empate, el
menor índice). Dijkstra con varios orígenes, una vez por bando.
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-4/EJ_07-4.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-4/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-4/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["if (dif < difMejor)", "if (dif <= difMejor)"],
}

MAXD = 1000


# ---------------------------------------------------------------- solucionador independiente
def distancias(N, ady, fuentes):
    INF = float("inf")
    dist = [INF] * (N + 1)
    cola = []
    for f in fuentes:
        dist[f] = 0
        cola.append((0, f))
    heapq.heapify(cola)
    while cola:
        d, v = heapq.heappop(cola)
        if d > dist[v]:
            continue
        for w, l in ady[v]:
            if d + l < dist[w]:
                dist[w] = d + l
                heapq.heappush(cola, (d + l, w))
    return dist


def conferencia(N, caminos, galos, romanos):
    ady = [[] for _ in range(N + 1)]
    for u, v, l in caminos:
        ady[u].append((v, l))
        ady[v].append((u, l))
    dg, dr = distancias(N, ady, galos), distancias(N, ady, romanos)
    controladas = set(galos) | set(romanos)
    return min((abs(dg[v] - dr[v]), v) for v in range(1, N + 1) if v not in controladas)


def salida_caso(caso):
    dif, v = conferencia(*caso)
    return f"{v} {dif}\n"


def valida(caso):
    N, caminos, galos, romanos = caso
    assert 3 <= N <= 100_000 and 2 <= len(caminos) <= 200_000
    pares = set()
    padre = list(range(N + 1))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    for u, v, l in caminos:
        assert 1 <= u <= N and 1 <= v <= N and u != v and 1 <= l <= MAXD
        k = (min(u, v), max(u, v))
        assert k not in pares
        pares.add(k)
        padre[raiz(u)] = raiz(v)
    assert len({raiz(x) for x in range(1, N + 1)}) == 1, "el grafo debe ser conexo"
    assert galos and romanos and not (set(galos) & set(romanos))
    assert len(set(galos)) == len(galos) and len(set(romanos)) == len(romanos)
    assert len(galos) + len(romanos) < N, "debe haber al menos una aldea neutral"


def caso_a_texto(caso):
    N, caminos, galos, romanos = caso
    return (f"{N} {len(caminos)}\n" + "".join(f"{u} {v} {l}\n" for u, v, l in caminos)
            + " ".join(map(str, [len(galos)] + galos)) + "\n"
            + " ".join(map(str, [len(romanos)] + romanos)) + "\n")


# ---------------------------------------------------------------- generadores
def aleatorio(r, N, extra, ng, nr, maxd=MAXD):
    """Grafo conexo (árbol al azar + `extra` caminos), con ng aldeas galas y nr romanas."""
    perm = list(range(1, N + 1))
    r.shuffle(perm)
    pares = set()
    caminos = []
    for i in range(1, N):
        u, v = perm[i], perm[r.randrange(i)]
        pares.add((min(u, v), max(u, v)))
        caminos.append((u, v, r.randint(1, maxd)))
    objetivo = min(N * (N - 1) // 2, len(caminos) + extra)
    while len(caminos) < max(2, objetivo):
        u, v = r.sample(range(1, N + 1), 2)
        k = (min(u, v), max(u, v))
        if k not in pares:
            pares.add(k)
            caminos.append((u, v, r.randint(1, maxd)))
    r.shuffle(caminos)
    aldeas = list(range(1, N + 1))
    r.shuffle(aldeas)
    return (N, caminos, aldeas[:ng], aldeas[ng:ng + nr])


def aleatorio_pequeno(r):
    n = r.randint(3, 9)
    g = r.randint(1, n - 2)
    return aleatorio(r, n, r.randint(0, 6), g, r.randint(1, n - g - 1), maxd=r.choice([4, 1000]))


def cadena(N):
    """Galos en la aldea 1, romanos en la N y una cadena de caminos de longitud 1000."""
    caminos = [(i, i + 1, MAXD) for i in range(1, N)]
    rng(N).shuffle(caminos)
    return (N, caminos, [1], [N])


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(74)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (4, [(1, 2, 10), (1, 3, 4), (1, 4, 7), (2, 3, 5), (2, 4, 5)], [1], [2])
    ej2 = (6, [(1, 2, 3), (2, 3, 5), (3, 4, 4), (4, 5, 2), (5, 6, 1)], [1, 5], [3])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF: «3 1» y «2 2» (empate entre las aldeas 2 y 4).",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: para cada aldea neutral hace falta la distancia a la aldea gala MÁS CERCANA y a la romana más cercana.",
            "rte": "Error de ejecución con el ejemplo: las aldeas van del 1 al N (resta 1) y las líneas de cada bando empiezan por el número de aldeas."},
           ["En el segundo caso, para la aldea 4 la aldea gala más cercana es la 5 (a 2), no la 1.",
            "Escribe el índice de la aldea (desde 1) y la diferencia, separados por un espacio."])
    prueba("Tres aldeas en fila", "borde", [(3, [(3, 2, 4), (2, 1, 4)], [1], [3])],
           "Lo mínimo: una aldea de cada bando y la neutral en medio, a la misma distancia: «2 0».",
           {"wa": "Con tres aldeas solo hay una neutral, la 2, con diferencia 0. Revisa la lectura y que escribes el índice desde 1.",
            "rte": "Error de ejecución en el caso más pequeño: revisa los índices y la lectura de las dos líneas de bandos."},
           ["Debe salir «2 0».",
            "Las dos últimas líneas son «1 1» (una aldea gala, la 1) y «1 3» (una romana, la 3)."])
    prueba("La aldea neutral en un extremo", "borde", [(3, [(1, 2, 5), (2, 3, 7)], [2], [3])],
           "La única neutral (la 1) está detrás de la aldea gala: su romana más cercana está a 12, pasando por la gala.",
           {"wa": "La aldea neutral 1 está a 5 de los galos y a 12 de los romanos (pasando por la aldea gala): «1 7»."},
           ["Debe salir «1 7».",
            "Para ir de la aldea 1 a la romana hay que atravesar la gala, y eso está permitido."])
    prueba("Cadena de 50.000 aldeas", "borde", [cadena(50_000)],
           "Galos en un extremo y romanos en el otro, con caminos de 1000: distancias de hasta 5·10⁷.",
           {"wa": "Las distancias llegan a 5·10⁷: si tu infinito es más pequeño (10⁶, 10⁷…), algunas aldeas parecen inalcanzables. Usa numeric_limits<int>::max().",
            "tle": "Con 50.000 aldeas en fila, tu Dijkstra es demasiado lento: usa la IndexPQ, no un recorrido del vector para buscar el mínimo."},
           ["La aldea neutral del centro está a la misma distancia de los dos extremos.",
            "Revisa el valor que usas como infinito."])
    prueba("Caminos de doble sentido", "trampa", [(4, [(2, 1, 3), (3, 2, 1), (4, 3, 5)], [4], [1])],
           "Los caminos vienen escritos «hacia atrás» (2 1, 3 2, 4 3): se pueden recorrer en los dos sentidos.",
           {"wa": "Solo añades cada camino en un sentido. Son transitables en ambos: pon las dos aristas, u → v y v → u."},
           ["Debe salir «3 1»: la aldea 3 está a 5 de los galos y a 4 de los romanos (la 2 está a 6 y a 3).",
            "Por cada camino llama dos veces a ponArista."])
    prueba("Diferencia en valor absoluto", "trampa", [(4, [(1, 2, 1), (2, 4, 5), (1, 3, 3), (3, 4, 4)], [1], [4])],
           "La aldea 2 está a 1 de los galos y a 5 de los romanos (diferencia 4, no −4).",
           {"wa": "Te quedas con una diferencia negativa: la diferencia es el valor absoluto |dGalos − dRomanos|."},
           ["Debe salir «3 1».",
            "Usa abs(dGalos[v] - dRomanos[v])."])
    prueba("La aldea gala más cercana no es la primera de la lista", "trampa",
           [(6, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1)], [6, 1], [3])],
           "Hay dos aldeas galas (la 6 y la 1): para cada neutral cuenta la más cercana de las dos.",
           {"wa": "Solo tienes en cuenta una aldea de cada bando. Hay que usar todas: mete todas las aldeas del bando en la cola de prioridad con distancia 0 (un Dijkstra con varios orígenes)."},
           ["Debe salir «2 0»: la aldea 2 está a 1 de la gala 1 y a 1 de la romana 3.",
            "La distancia de una aldea a un bando es la mínima a cualquiera de sus aldeas.",
            "No hace falta un Dijkstra por aldea: empieza uno solo con todas las del bando a distancia 0."])
    prueba("Empate: la aldea de menor índice", "trampa", [(4, [(1, 2, 2), (2, 4, 2), (1, 3, 5), (3, 4, 5)], [1], [4])],
           "Las aldeas neutrales 2 y 3 tienen diferencia 0: se elige la 2.",
           {"wa": "En los empates te quedas con la última aldea. Recorre las aldeas en orden y cambia la elegida solo si la diferencia es estrictamente menor (<, no ≤)."},
           ["Debe salir «2 0».",
            "Con «if (dif <= mejor)» gana la última de las empatadas; con «<», la primera."])
    prueba("Se puede pasar por las aldeas de un bando", "trampa", [(4, [(1, 2, 2), (2, 3, 3), (3, 4, 10)], [2], [3])],
           "Para ir de la aldea 1 a la romana hay que atravesar la gala (y de la 4 a la gala, la romana): en tregua se puede.",
           {"wa": "No dejas que los caminos atraviesen aldeas controladas. El enunciado dice que en tregua se puede pasar por cualquier aldea: no cortes el Dijkstra en ellas."},
           ["Debe salir «1 3».",
            "Las aldeas de los bandos son vértices normales del grafo: Dijkstra debe seguir relajando sus aristas."])
    prueba("Solo cuentan las aldeas neutrales", "trampa", [(4, [(2, 3, 1), (2, 4, 100), (4, 1, 1)], [2, 4], [3])],
           "Las aldeas 2 (gala) y 3 (romana) tienen diferencia 1, pero la conferencia tiene que ser en una neutral: la 1, con 101.",
           {"wa": "Estás eligiendo una aldea de un bando. La conferencia se celebra en una aldea neutral: sáltate las que pertenecen a galos o romanos."},
           ["Debe salir «1 101».",
            "Marca a qué bando pertenece cada aldea al leer las dos últimas líneas y, al buscar la mejor, ignora las marcadas."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio(r, 12, 6, 4, 4), (3, [(1, 2, 4), (2, 3, 4)], [1], [3]), ej1, aleatorio(r, 7, 3, 1, 2),
            (5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1)], [5], [4])],
           "Un caso con muchas aldeas controladas seguido de otros más pequeños: nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: el vector que marca el bando de cada aldea, las listas de aldeas o las distancias no se crean de nuevo.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: créalas dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso (o son static).",
            "Declara el grafo, las listas de cada bando y el vector de bandos dentro de resuelveCaso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio_pequeno(r) for _ in range(50)],
           "50 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas bien: la línea que falla es el número de caso; calcula a mano las dos distancias de cada aldea neutral."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Escribe junto a cada aldea su distancia a los galos y a los romanos."])
    prueba("Aleatorios con muchas aldeas en cada bando", "aleatorio",
           [aleatorio(r, n, r.randint(5, 40), n // 3, n // 3, maxd=r.choice([5, 1000])) for n in
            (r.randint(10, 40) for _ in range(30))],
           "30 casos de 10 a 40 aldeas, un tercio de cada bando, con caminos cortos para que haya empates.",
           {"wa": "Con muchas aldeas por bando algo falla: ¿usas todas las del bando como orígenes? ¿desempatas por el menor índice?"},
           ["Busca el caso que falla y comprueba la aldea elegida y su diferencia.",
            "Las aldeas de un bando son todas orígenes a distancia 0."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, n, n, r.randint(1, 20), r.randint(1, 20)) for n in (r.randint(50, 400) for _ in range(10))],
           "10 casos de 50 a 400 aldeas.",
           {"wa": "En grafos más grandes algo falla: revisa la relajación y la elección de la aldea."},
           ["Busca el caso que falla.",
            "Comprueba que los dos Dijkstra (galos y romanos) recorren todo el grafo."])
    prueba("Grande: 60.000 aldeas, 15.000 de cada bando", "rendimiento", [aleatorio(r, 60_000, 60_000, 15_000, 15_000)],
           "Un caso grande con muchísimas aldeas en cada bando.",
           {"tle": "Haces un Dijkstra por cada aldea de un bando (o por cada neutral): con 15.000 aldeas por bando no termina. Basta UN Dijkstra por bando con todas sus aldeas como orígenes.",
            "mle": "Gastas demasiada memoria: no guardes las distancias desde cada aldea por separado.",
            "wa": "Solo falla en el grande: revisa el infinito y la lectura de las listas de aldeas."},
           ["¿Cuántos Dijkstra haces? Deberían ser exactamente dos.",
            "Mete todas las aldeas galas en la cola con distancia 0 y lanza un Dijkstra; lo mismo con las romanas."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(salida_caso(c) for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


_UNA_A_UNA = """    return dist;
}

vector<int> distanciaMinimaVarias(DigrafoValorado<int> const& g, vector<int> const& origenes) {
    vector<int> res(g.V(), numeric_limits<int>::max());
    for (int o : origenes) {
        vector<int> d = distanciaMinima(g, vector<int>{o});
        for (int v = 0; v < g.V(); ++v) res[v] = min(res[v], d[v]);
    }
    return res;
}"""

VARIANTES = [
    Variante("caminos de un solo sentido", [("        g.ponArista({v, u, d});\n", "")], prueba=5, v="wa"),
    Variante("solo la primera aldea de cada bando", [("for (int o : origenes) {", "for (int o : {origenes[0]}) {")],
             prueba=7, v="wa"),
    Variante("sin valor absoluto", [("int dif = abs(dGalos[v] - dRomanos[v]);", "int dif = dGalos[v] - dRomanos[v];")],
             prueba=6, v="wa"),
    Variante("desempata por el mayor índice", [("if (dif < difMejor)", "if (dif <= difMejor)")], prueba=8, v="wa"),
    Variante("considera también las aldeas de los bandos",
             [("        if (bando[v] != 0) continue;          // solo aldeas neutrales\n", "")], prueba=10, v="wa"),
    Variante("no deja pasar por aldeas controladas",
             [("vector<int> distanciaMinima(DigrafoValorado<int> const& g, vector<int> const& origenes) {",
               "vector<int> distanciaMinima(DigrafoValorado<int> const& g, vector<int> const& origenes, vector<int> const& bando) {"),
              ("int v = pq.top().elem; pq.pop();", "int v = pq.top().elem; pq.pop();\n        if (bando[v] != 0 && dist[v] != 0) continue;"),
              ("distanciaMinima(g, galos);", "distanciaMinima(g, galos, bando);"),
              ("distanciaMinima(g, romanos);", "distanciaMinima(g, romanos, bando);")], prueba=9, v="wa"),
    Variante("bandos no reiniciados entre casos (static)",
             [("vector<int> bando(N, 0);", "static vector<int> bando; bando.resize(N, 0);")], prueba=11, v="wa"),
    Variante("infinito demasiado pequeño (10⁶)",
             [("const int INF = numeric_limits<int>::max();", "const int INF = 1000000;")], prueba=4, v="wa"),
    Variante("un Dijkstra por cada aldea del bando",
             [("    return dist;\n}", _UNA_A_UNA),
              ("distanciaMinima(g, galos);", "distanciaMinimaVarias(g, galos);"),
              ("distanciaMinima(g, romanos);", "distanciaMinimaVarias(g, romanos);")], prueba=15, v="tle"),
]
