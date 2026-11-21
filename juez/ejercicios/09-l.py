"""09-L · Necesitamos agua: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «N M» (N par) y M líneas «u v coste» (carreteras de doble
sentido, grafo conexo, sin lazos ni repetidas). La planta norte es el punto 1 y la sur el N.
Salida: el coste mínimo (ida y vuelta) de servir (N-2)/2 pueblos desde cada planta.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "9-Algoritmos voraces II/EJ_09-L/EJ_09-L.cpp",
    "cabeceras": ["9-Algoritmos voraces II/EJ_09-L/GrafoValorado.h", "9-Algoritmos voraces II/EJ_09-L/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["cout << 2 * total << '\\n';", "cout << total << '\\n';"],
}


def distancias(N, ady, s):
    d = [None] * (N + 1)
    d[s] = 0
    h = [(0, s)]
    while h:
        dv, v = heapq.heappop(h)
        if dv > d[v]:
            continue
        for w, c in ady[v]:
            if d[w] is None or dv + c < d[w]:
                d[w] = dv + c
                heapq.heappush(h, (d[w], w))
    return d


def resuelve(N, aristas):
    """Solucionador independiente: distancias desde las dos plantas; el norte se queda con los
    pueblos en los que dN - dS es menor (lo que más se ahorra, o lo que menos se pierde)."""
    ady = [[] for _ in range(N + 1)]
    for u, v, c in aristas:
        ady[u].append((v, c))
        ady[v].append((u, c))
    dn, ds = distancias(N, ady, 1), distancias(N, ady, N)
    pueblos = sorted(range(2, N), key=lambda v: dn[v] - ds[v])
    k = (N - 2) // 2
    return 2 * (sum(dn[v] for v in pueblos[:k]) + sum(ds[v] for v in pueblos[k:]))


def caso_a_texto(c):
    N, aristas = c
    return f"{N} {len(aristas)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in aristas)


def aleatorio(rng, N, extra, cmax):
    """Grafo conexo: un árbol al azar más 'extra' carreteras distintas, con etiquetas barajadas."""
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    usadas, aristas = set(), []

    def pon(a, b):
        if a != b and (min(a, b), max(a, b)) not in usadas:
            usadas.add((min(a, b), max(a, b)))
            aristas.append((a, b, rng.randint(1, cmax)) if rng.random() < .5 else (b, a, rng.randint(1, cmax)))
            return True
        return False

    for k in range(1, N):
        pon(perm[k], perm[rng.randint(max(0, k - 50), k - 1)] if N > 1000 else perm[rng.randint(0, k - 1)])
    maxm = N * (N - 1) // 2
    objetivo = min(maxm, N - 1 + extra)
    intentos = 0
    while len(aristas) < objetivo and intentos < 50 * objetivo:
        intentos += 1
        pon(rng.randint(1, N), rng.randint(1, N))
    rng.shuffle(aristas)
    return (N, aristas)


def pruebas():
    rng = random.Random(9010)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(4, [(1, 2, 5), (1, 3, 20), (4, 2, 15), (3, 4, 10)]),
            (6, [(1, 2, 15), (2, 3, 5), (3, 6, 100), (1, 4, 5), (4, 6, 100), (6, 5, 100), (1, 5, 20)])],
           "Los dos ejemplos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la lectura (vértices numerados desde 1), que cuentas ida y vuelta (×2) y el reparto mitad y mitad."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "En el segundo caso todos los pueblos están más cerca del norte, pero el norte solo puede servir a dos.",
            "Calcula las distancias desde las dos plantas (dos Dijkstra) y reparte los pueblos según dN - dS."])
    prueba("Sin pueblos", "borde", [(2, [(1, 2, 7)])],
           "Solo las dos plantas (N = 2): no hay que servir a nadie, coste 0.",
           {"wa": "Con N = 2 no hay pueblos: el coste es 0.",
            "rte": "Con N = 2 no hay pueblos: no accedas a posiciones de un vector vacío."},
           ["¿Qué escribe tu programa si (N - 2) / 2 = 0?",
            "Los pueblos son los puntos 2..N-1: con N = 2 no hay ninguno."])
    prueba("Ida y vuelta", "trampa", [(4, [(1, 2, 3), (2, 4, 3), (1, 3, 3), (3, 4, 3)])],
           "Cada camión va al pueblo y vuelve: el coste de cada trayecto cuenta dos veces.",
           {"wa": "Te sale la mitad (o el doble): el camión hace la ida y la vuelta, así que el coste es 2 · (distancia)."},
           ["Aquí cada pueblo está a 3 de las dos plantas: 2 · (3 + 3) = 12.",
            "Multiplica por 2 la suma de las distancias al final."])
    prueba("La planta más cercana no basta", "trampa", [(4, [(1, 2, 1), (1, 3, 2), (2, 4, 10), (3, 4, 20)])],
           "Los dos pueblos prefieren el norte, pero el norte solo puede servir a uno.",
           {"wa": "Mandas cada pueblo a su planta más cercana sin respetar que cada planta sirve exactamente a la mitad."},
           ["El norte tiene camiones para (N - 2) / 2 pueblos, ni uno más.",
            "Coge exactamente (N - 2) / 2 pueblos para el norte: los de menor dN - dS."])
    prueba("Elegir por la diferencia, no por la distancia", "trampa",
           [(4, [(1, 2, 1), (2, 4, 1), (1, 3, 2), (3, 4, 100)])],
           "Darle al norte los pueblos más cercanos a él no es óptimo: importa cuánto se ahorra respecto al sur.",
           {"wa": "Eliges para el norte los pueblos con menor distancia al norte. El criterio es la DIFERENCIA dN - dS: el pueblo 3 pierde mucho si va al sur."},
           ["El pueblo 2 está a 1 de las dos plantas; el 3 está a 2 del norte y a 4 del sur (dando la vuelta por el 1 y el 2).",
            "Si todos fueran al sur, pasar el pueblo v al norte cambia el coste en dN[v] - dS[v].",
            "Ordena los pueblos por dN - dS y da al norte los (N - 2) / 2 primeros."])
    prueba("El camino corto da un rodeo", "trampa",
           [(4, [(1, 2, 50), (1, 3, 1), (3, 2, 1), (2, 4, 1), (3, 4, 60)])],
           "La distancia mínima no es la carretera directa: hay que hacer Dijkstra, no mirar solo las aristas.",
           {"wa": "No calculas bien las distancias mínimas: el camino más barato puede pasar por otros pueblos (o por la otra planta)."},
           ["Del norte al pueblo 2 cuesta 2 yendo por el 3, no 50.",
            "Usa Dijkstra desde cada planta; ni BFS (cuenta carreteras, no costes) ni solo las carreteras directas sirven."])
    prueba("Pasar por la otra planta", "trampa",
           [(6, [(1, 6, 1), (6, 2, 1), (6, 3, 1), (6, 4, 1), (6, 5, 1)])],
           "Todos los pueblos cuelgan de la planta sur; desde el norte hay que pasar por ella.",
           {"wa": "Los caminos pueden atravesar la otra planta y otros pueblos: no la quites del grafo ni la trates distinto en Dijkstra."},
           ["Desde el norte, cada pueblo está a 2 (pasando por la sur).",
            "Coste: dos pueblos al norte (2 + 2) y dos al sur (1 + 1), por 2: 12."])
    prueba("La planta sur es el punto N", "trampa",
           [(6, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1)])],
           "Una carretera en línea 1-2-3-4-5-6: el sur es el 6, no el 2 ni el N-1.",
           {"wa": "Haces Dijkstra desde un punto equivocado: el norte es el 1 y el sur el N (en índices desde 0, el 0 y el N-1)."},
           ["Los pueblos 2 y 3 van al norte (1 + 2) y el 4 y 5 al sur (2 + 1): 2 · 6 = 12.",
            "Si restas 1 a los vértices al leer, el sur es el N - 1."])
    prueba("Reparto al revés", "trampa",
           [(6, [(1, 2, 1), (1, 3, 1), (2, 6, 9), (3, 6, 9), (4, 6, 1), (5, 6, 1), (1, 4, 9), (1, 5, 9)])],
           "Pueblos claramente de un lado y del otro: el reparto debe darle al norte los suyos.",
           {"wa": "Das al norte los pueblos de MAYOR dN - dS (o sumas las distancias cambiadas): ordena de menor a mayor."},
           ["Los pueblos 2 y 3 al norte y el 4 y 5 al sur: 2 · 4 = 8.",
            "Al norte le convienen los de menor dN - dS (lo que más se ahorra)."])
    prueba("Varios casos seguidos", "trampa",
           [(6, [(1, 2, 3), (2, 3, 3), (3, 4, 3), (4, 5, 3), (5, 6, 3)]), (2, [(2, 1, 5)]),
            (4, [(1, 2, 1), (2, 3, 1), (3, 4, 1)]), (4, [(1, 3, 2), (3, 2, 2), (2, 4, 2)])],
           "Varios casos seguidos: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el vector de diferencias, las distancias o el total no se reinician."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo, las distancias y el vector de diferencias dentro de la función de cada caso."])
    prueba("Grafo completo pequeño", "borde",
           [(6, [(u, v, (u * 7 + v * 3) % 20 + 1) for u in range(1, 7) for v in range(u + 1, 7)])],
           "Todas las carreteras posibles entre 6 puntos.",
           {"wa": "Con muchas carreteras algo falla: revisa que Dijkstra relaja todas las aristas de cada vértice."},
           ["Hay N(N - 1)/2 = 15 carreteras.",
            "Comprueba tus distancias a mano para un par de pueblos."])
    cadena = [(k, k + 1, 100000) for k in range(1, 30000)]
    rng.shuffle(cadena)
    prueba("Distancias enormes (long long)", "trampa", [(30000, cadena)],
           "Una carretera en línea de 30.000 puntos con coste 100.000: las distancias y el total no caben en int.",
           {"wa": "Algo se desborda: una distancia puede llegar a 100.000 · 200.000 y el total a mucho más. Usa long long para distancias y sumas."},
           ["Calcula el orden de magnitud: ¿cuánto puede valer la suma de todas las distancias?",
            "Usa long long en las distancias, en las diferencias y en el total."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(rng, rng.choice([2, 4, 4, 6, 6, 8, 8]), rng.randint(0, 8), rng.choice([3, 20, 100000])) for _ in range(150)],
           "150 islas pequeñas al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja ese grafo."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Calcula a mano dN y dS de cada pueblo y ordena las diferencias."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(rng, 2 * rng.randint(20, 500), rng.randint(0, 1500), rng.choice([10, 100000])) for _ in range(20)],
           "20 islas medianas.",
           {"wa": "Algo falla con grafos más grandes: revisa Dijkstra (la cola con prioridad) y la suma final."},
           ["Reduce el caso que falla si puedes.",
            "Comprueba que Dijkstra actualiza la prioridad de un vértice cuando mejora su distancia."])
    prueba("100.000 puntos", "rendimiento", [aleatorio(rng, 100000, 15000, 100000)],
           "Una isla grande: mide la eficiencia de los dos Dijkstra y del reparto.",
           {"tle": "Tu solución es lenta: los Dijkstra deben ser O(M log N) con cola con prioridad y el reparto O(N log N) (ordenar las diferencias)."},
           ["No busques el mínimo recorriendo todos los vértices (ni en Dijkstra ni al repartir): eso es cuadrático.",
            "Usa IndexPQ (o priority_queue) en Dijkstra y sort para las diferencias.",
            "Pasa el grafo por referencia constante a Dijkstra."])
    return [Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{resuelve(*c)}\n" for c in casos), casos=len(casos),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("olvida la vuelta (sin ×2)", [("cout << 2 * total << '\\n';", "cout << total << '\\n';")], prueba=3, v="wa"),
    Variante("cada pueblo a su planta más cercana",
             [("for (int k = 0; k < (N - 2) / 2; ++k) total += dif[k];", "for (long long d : dif) if (d < 0) total += d;")], prueba=4, v="wa"),
    Variante("ordena las diferencias al revés", [("sort(dif.begin(), dif.end());", "sort(dif.rbegin(), dif.rend());")], prueba=4, v="wa"),
    Variante("no reinicia entre casos", [("vector<long long> dif;", "static vector<long long> dif;")], prueba=10, v="wa"),
    Variante("total en int", [("long long total = 0;", "int total = 0;")], prueba=12, v="wa"),
    Variante("elige el mínimo recorriendo todo",
             [("sort(dif.begin(), dif.end());\n    for (int k = 0; k < (N - 2) / 2; ++k) total += dif[k];",
               "for (int k = 0; k < (N - 2) / 2; ++k) { auto it = min_element(dif.begin(), dif.end()); total += *it; *it = numeric_limits<long long>::max(); }")],
             prueba=15, v="tle"),
]
