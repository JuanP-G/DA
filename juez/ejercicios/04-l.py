"""04-L · Peaje a la sombra: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso «N C A L T» (3 ≤ N ≤ 20.000, 2 ≤ C ≤ 200.000; A, L y T
distintos entre 1 y N) y C tramos «u v» (sin bucles ni repetidos; la ciudad es conexa).
Salida: el mínimo número de tramos distintos que recorren Álex y Lucas entre los dos para llegar
al trabajo (los que recorren juntos se pagan una vez).
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-L/EJ_04-L.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-L/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["int coste = dA.distancia(m) + dL.distancia(m) + dT.distancia(m);", "int coste = dA.distancia(m) + dL.distancia(m) + dT.distancia(m) + 1;"],
}


# ---------------------------------------------------------------- solucionador independiente
def bfs(N, ady, s):
    d = [-1] * (N + 1)
    d[s] = 0
    cola = deque([s])
    while cola:
        v = cola.popleft()
        for w in ady[v]:
            if d[w] < 0:
                d[w] = d[v] + 1
                cola.append(w)
    return d


def peaje(caso):
    """Los dos recorridos forman una «Y»: cada uno solo hasta un cruce m y juntos de m al trabajo.
    Mínimo de d(A, m) + d(L, m) + d(m, T) sobre todos los cruces."""
    N, A, L, T, tramos = caso
    ady = [[] for _ in range(N + 1)]
    for u, v in tramos:
        ady[u].append(v)
        ady[v].append(u)
    dA, dL, dT = bfs(N, ady, A), bfs(N, ady, L), bfs(N, ady, T)
    return min(dA[m] + dL[m] + dT[m] for m in range(1, N + 1))


def caso_a_texto(caso):
    N, A, L, T, tramos = caso
    return f"{N} {len(tramos)} {A} {L} {T}\n" + "".join(f"{u} {v}\n" for u, v in tramos)


# ---------------------------------------------------------------- generadores
def conexo(rng, N, C):
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    ar = set()
    for i in range(1, N):
        j = rng.randrange(i)
        ar.add((min(perm[i], perm[j]), max(perm[i], perm[j])))
    while len(ar) < C:
        a, b = rng.sample(range(1, N + 1), 2)
        ar.add((min(a, b), max(a, b)))
    ar = [(a, b) if rng.random() < .5 else (b, a) for a, b in ar]
    rng.shuffle(ar)
    return ar


def aleatorio_pequeno(rng):
    N = rng.randint(3, 9)
    C = rng.randint(max(2, N - 1), min(N * (N - 1) // 2, N + 4))
    A, L, T = rng.sample(range(1, N + 1), 3)
    return (N, A, L, T, conexo(rng, N, C))


def camino(nodos):
    return [(nodos[i], nodos[i + 1]) for i in range(len(nodos) - 1)]


def pruebas():
    rng = random.Random(48)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(6, 1, 3, 6, [(1, 2), (2, 3), (2, 5), (3, 4), (5, 4), (5, 6), (4, 6)]),
            (4, 4, 1, 3, [(1, 2), (2, 3), (3, 4)])],
           "Los dos casos del PDF: quedar en el cruce 2 sale a 4; en una sola calle con el trabajo en medio, 3.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: el orden de los 5 números de la primera línea (N, C, casa de Álex, casa de Lucas, trabajo), que los cruces van de 1 a N y la idea: los tramos que hacen juntos se pagan una vez.",
            "pe": "El número está bien pero el formato no: un número por línea."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "En el primer caso, si cada uno va por su cuenta pagan 3 + 2 = 5; quedando en el cruce 2 pagan 1 + 1 + 2 = 4.",
            "Prueba todos los posibles puntos de encuentro m: coste = d(Álex, m) + d(Lucas, m) + d(m, trabajo)."])
    prueba("La ciudad más pequeña", "borde",
           [(3, 1, 3, 2, [(1, 2), (2, 3)]), (3, 1, 2, 3, [(1, 2), (2, 3)]), (3, 2, 3, 1, [(2, 1), (3, 2)])],
           "N = 3 en línea, con el trabajo en medio, al final y al principio: siempre 2.",
           {"wa": "Con tres cruces en línea la respuesta es 2 en los tres casos. Revisa que pruebas también como punto de encuentro el trabajo y las propias casas."},
           ["En el primer caso el trabajo está entre las dos casas: cada uno paga un tramo.",
            "En el segundo, Lucas vive entre Álex y el trabajo: Álex pasa a buscarle.",
            "El mínimo sobre TODOS los cruces m (casas y trabajo incluidos) cubre todas las situaciones."])
    prueba("Triángulo", "borde", [(3, 1, 2, 3, [(1, 2), (2, 3), (3, 1)])],
           "Tres cruces unidos entre sí: cada uno va directo (2).",
           {"wa": "Cada uno está a un tramo del trabajo: la respuesta es 2."},
           ["Álex y Lucas están a un tramo del trabajo.",
            "Comprueba que las distancias salen de un BFS desde cada uno."])
    prueba("Cruces numerados de 1 a N", "trampa", [(4, 1, 2, 4, [(1, 2), (2, 3), (3, 4)])],
           "El trabajo está en el cruce N y hay un tramo con el cruce N.",
           {"rte": "Los cruces van de 1 a N: hay que restar 1 a los tramos y también a las casas y al trabajo (si no, el cruce N no existe en un grafo de N vértices)."},
           ["El cruce 4 existe cuando N = 4.",
            "Resta 1 a A, L y T, además de a los extremos de cada tramo."])
    prueba("Les conviene quedar", "trampa", [(5, 1, 2, 5, [(1, 2), (2, 3), (3, 4), (4, 5)])],
           "Álex y Lucas viven en cruces vecinos lejos del trabajo: Álex pasa a buscar a Lucas (1 + 3 = 4, no 4 + 3 = 7).",
           {"wa": "Ir cada uno por su camino más corto no es lo mejor: los tramos que hacen juntos se pagan una sola vez. Hay que probar puntos de encuentro."},
           ["Si van por separado pagan 4 + 3 = 7; si Álex pasa por casa de Lucas, 1 + 3 = 4.",
            "Los caminos tienen forma de Y: cada uno solo hasta m y luego juntos hasta el trabajo.",
            "Calcula el mínimo de dA[m] + dL[m] + dT[m] para todos los cruces m."])
    prueba("Quedar en un cruce que no es ninguna casa", "trampa",
           [(7, 1, 2, 7, [(1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])],
           "Lo mejor es quedar en el cruce 3, que no es la casa de ninguno ni el trabajo (1 + 1 + 4 = 6).",
           {"wa": "El punto de encuentro puede ser cualquier cruce, no solo una de las casas o el trabajo. Prueba todos."},
           ["Quedando en casa de Álex: 0 + 2 + 5 = 7. Quedando en el cruce 3: 1 + 1 + 4 = 6.",
            "No te limites a las casas y el trabajo: recorre todos los cruces m de 1 a N."])
    prueba("No siempre compensa quedar", "trampa", [(5, 1, 5, 3, [(1, 2), (2, 3), (3, 4), (4, 5)])],
           "El trabajo está entre las dos casas: lo mejor es que cada uno vaya por su lado (2 + 2 = 4).",
           {"wa": "Quedar antes de llegar no siempre compensa: el propio trabajo también es un «punto de encuentro» válido (cada uno va solo)."},
           ["Cualquier encuentro antes del trabajo obliga a uno a pasarse y volver.",
            "Incluye m = trabajo en el mínimo (o empieza con mejor = dA[T] + dL[T])."])
    prueba("Distancias mínimas en una ciudad con ciclos", "trampa",
           [(6, 3, 1, 4, [(6, 5), (2, 1), (3, 2), (6, 1), (5, 3), (4, 1)])],
           "Una ciudad con un ciclo 1-2-3-5-6-1: las distancias tienen que ser las mínimas.",
           {"wa": "Las distancias deben ser mínimas: un DFS (o una pila en vez de una cola) puede dar a un cruce una distancia mayor de la real. Usa BFS."},
           ["Desde la casa de Álex (3) al cruce 1 hay 2 tramos por 3-2-1; un DFS puede dar la vuelta larga 3-5-6-1.",
            "Un BFS con cola visita los cruces por orden de distancia."])
    # encuentro que no está en el camino más corto de ninguno: d(A,m)=d(L,m)=2, d(m,T)=4, d(A,T)=d(L,T)=5
    #   A=1, L=2, T=3, m=4; 1-5-4, 2-6-4, 4-7-8-9-3, 1-10-11-12-13-3, 2-14-15-16-17-3
    lejos = ([(1, 5), (5, 4), (2, 6), (6, 4)] + camino([4, 7, 8, 9, 3]) + camino([1, 10, 11, 12, 13, 3]) + camino([2, 14, 15, 16, 17, 3]))
    prueba("Quedar fuera de los caminos más cortos", "trampa", [(17, 1, 2, 3, lejos)],
           "El mejor cruce para quedar (el 4) no está en el camino más corto de ninguno de los dos: 2 + 2 + 4 = 8 frente a 5 + 5 = 10.",
           {"wa": "No basta con buscar el punto de encuentro en el camino más corto de Álex (o de Lucas): puede compensar desviarse. Hay que probar todos los cruces."},
           ["Cada uno tiene un camino de 5 tramos hasta el trabajo, pero el cruce 4 está a 2 de cada uno y a 4 del trabajo.",
            "El coste de quedar en m solo depende de tres distancias: dA[m], dL[m] y dT[m].",
            "Haz tres BFS (desde Álex, desde Lucas y desde el trabajo) y prueba todos los m."])
    prueba("Una casa en el camino del otro", "trampa",
           [(8, 6, 4, 1, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (4, 7), (7, 8)])],
           "Lucas vive en el camino de Álex al trabajo: Álex pasa por su casa y siguen juntos (5).",
           {"wa": "Si uno vive en el camino del otro, lo mejor es pasar a buscarle: el coste es la distancia del más lejano al trabajo."},
           ["Álex está a 5 tramos del trabajo y pasa por casa de Lucas: 2 + 3 = 5.",
            "Ese caso está incluido en el mínimo sobre todos los cruces (m = casa de Lucas)."])
    prueba("Varios casos seguidos", "trampa",
           [(3, 1, 2, 3, [(1, 2), (2, 3)]),
            (7, 1, 2, 7, [(1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]),
            (5, 1, 5, 3, [(1, 2), (2, 3), (3, 4), (4, 5)])],
           "Un caso con respuesta pequeña seguido de otros con respuestas mayores: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el mínimo, las distancias o el grafo están fuera de la función de cada caso (o son static)."},
           ["Si el primer caso sale bien y los siguientes repiten su respuesta, revisa el mínimo.",
            "Inicializa el mínimo en cada caso (y no lo declares static)."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(60)],
           "60 ciudades pequeñas al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja la ciudad."},
           ["Busca el caso de la línea que falla y dibuja la ciudad.",
            "Calcula a mano dA, dL y dT de cada cruce y busca la menor suma."])
    # ---- grandes
    N = 20000
    A, L, T = rng.sample(range(1, N + 1), 3)
    prueba("Ciudad grande y densa", "rendimiento", [(N, A, L, T, conexo(rng, N, 200000))],
           "N = 20.000 cruces y C = 200.000 tramos.",
           {"tle": "Bastan tres BFS (desde Álex, desde Lucas y desde el trabajo). Si haces un BFS desde cada cruce m para saber su distancia al trabajo, son N recorridos.",
            "mle": "Una matriz de distancias N × N (20.000²) no cabe: guarda solo tres vectores de distancias."},
           ["¿Cuántos BFS haces por caso?",
            "Como las calles son de doble sentido, d(m, trabajo) = d(trabajo, m): un único BFS desde el trabajo las da todas."])
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    prueba("Una calle larguísima", "rendimiento",
           [(N, perm[0], perm[-1], perm[N // 2], camino(perm)), (N, perm[0], perm[1], perm[-1], camino(perm))],
           "Una sola calle de 20.000 cruces: distancias de hasta 19.999 tramos.",
           {"tle": "Algo se repite de más: ¿un BFS desde cada cruce?",
            "rte": "Con un DFS recursivo la profundidad llega a 20.000: usa BFS con cola."},
           ["En la primera calle el trabajo está en medio: 19.999 tramos en total.",
            "Tres BFS con cola recorren la calle en O(N)."])
    filas, cols = 100, 200
    rejilla = []
    for i in range(filas):
        for j in range(cols):
            v = i * cols + j + 1
            if j + 1 < cols:
                rejilla.append((v, v + 1))
            if i + 1 < filas:
                rejilla.append((v, v + cols))
    rng.shuffle(rejilla)
    prueba("Ciudad en cuadrícula", "rendimiento",
           [(N, 1, cols, N, rejilla), (N, 1, N - cols + 1, N // 2 + 77, rejilla)],
           "Una cuadrícula de 100 × 200 cruces: muchísimos caminos mínimos distintos.",
           {"tle": "Algo es más caro de lo necesario: bastan tres BFS por caso.",
            "wa": "En una cuadrícula hay muchos caminos mínimos; revisa que las distancias salen de un BFS y que pruebas todos los cruces."},
           ["Desde dos esquinas de arriba hasta la de abajo: piensa dónde conviene quedar.",
            "Tres BFS y un recorrido de los N cruces bastan."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{peaje(c)}\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_COSTE = "int coste = dA.distancia(m) + dL.distancia(m) + dT.distancia(m);"

VARIANTES = [
    Variante("no resta 1 a las casas y al trabajo", [("--a; --l; --t;", ";")], prueba=4, v="rte"),
    Variante("no resta 1 a los tramos", [("g.ponArista(u - 1, v - 1);", "g.ponArista(u, v);")], prueba=4, v="rte"),
    Variante("cada uno por su lado", [(_COSTE, "int coste = dA.distancia(t) + dL.distancia(t);")], prueba=5, v="wa"),
    Variante("solo quedan en una de las casas",
             [(_COSTE, "int coste = (m == a || m == l) ? dA.distancia(m) + dL.distancia(m) + dT.distancia(m) : mejor;")], prueba=6, v="wa"),
    Variante("siempre quedan antes del trabajo",
             [("int mejor = dA.distancia(t) + dL.distancia(t);", "int mejor = 1000000000;"),
              (_COSTE, "int coste = (m == t) ? 1000000000 : dA.distancia(m) + dL.distancia(m) + dT.distancia(m);")], prueba=7, v="wa"),
    Variante("pila en lugar de cola (DFS)",
             [("#include <queue>", "#include <queue>\n#include <stack>"),
              ("queue<int> q;", "stack<int> q;"),
              ("int v = q.front(); q.pop();", "int v = q.top(); q.pop();")], prueba=8, v="wa"),
    Variante("el mínimo es static", [("int mejor = dA.distancia(t) + dL.distancia(t);", "static int mejor = dA.distancia(t) + dL.distancia(t);")], prueba=11, v="wa"),
    Variante("un BFS desde cada cruce", [("+ dT.distancia(m);", "+ CaminosBFS(g, m).distancia(t);")], prueba=13, v="tle"),
]
