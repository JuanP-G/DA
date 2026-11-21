"""05-5 · Haciendo trampas en Serpientes y Escaleras: juez con pruebas pensadas para cada error típico.

Casillas 1…N²; con un dado de K caras (eliges la cara) se avanza d casillas y, si se cae en el extremo
de salida de una serpiente o escalera, se va obligatoriamente al otro extremo. Mínimo de tiradas de 1 a N².
Restricciones que respetan todas las pruebas: 2 ≤ N ≤ 100, 1 ≤ K ≤ N, serpientes bajan y escaleras suben,
extremos en filas distintas, cada casilla es extremo de como mucho una, nunca la 1 ni la N², y la meta
siempre es alcanzable. El solucionador es un BFS propio en Python.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-5/EJ_05-5.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-5/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["for (int d = 1; d <= K && v + d < casillas; ++d)", "for (int d = 1; d <= 6 && v + d < casillas; ++d)"],
}


def tiradas(N, K, serp, esc):
    C = N * N
    dest = list(range(C + 1))
    for a, b in serp + esc:
        dest[a] = b
    d = [-1] * (C + 1)
    d[1] = 0
    cola = deque([1])
    while cola:
        v = cola.popleft()
        for k in range(1, K + 1):
            if v + k > C:
                break
            w = dest[v + k]
            if d[w] < 0:
                d[w] = d[v] + 1
                cola.append(w)
    return d[C]


def valida(N, K, serp, esc):
    C = N * N
    fila = lambda c: (c - 1) // N
    assert 2 <= N <= 100 and 1 <= K <= N
    usados = []
    for a, b in serp:
        assert a > b
    for a, b in esc:
        assert a < b
    for a, b in serp + esc:
        assert 1 < a < C and 1 < b < C and fila(a) != fila(b)
        usados += [a, b]
    assert len(usados) == len(set(usados))
    assert tiradas(N, K, serp, esc) > 0


def genera(rng, N, K, ns, ne):
    C = N * N
    fila = lambda c: (c - 1) // N
    while True:
        usados = {1, C}

        def par(subir):
            for _ in range(2000):
                a, b = rng.sample(range(2, C), 2)
                if a in usados or b in usados or fila(a) == fila(b):
                    continue
                if (a < b) != subir:
                    a, b = b, a
                usados.update((a, b))
                return (a, b)
            return None

        s = [p for p in (par(False) for _ in range(ns)) if p]
        e = [p for p in (par(True) for _ in range(ne)) if p]
        if tiradas(N, K, s, e) > 0:
            return (N, K, s, e)
        ns, ne = ns * 3 // 4, ne * 3 // 4     # tablero sin salida: lo repetimos con menos serpientes


def caso_a_texto(c):
    N, K, s, e = c
    return f"{N} {K} {len(s)} {len(e)}\n" + "".join(f"{a} {b}\n" for a, b in s + e)


def pruebas():
    rng = random.Random(555)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        for c in casos:
            valida(*c)
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{tiradas(*c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [(10, 6, [(50, 13), (68, 55), (81, 16), (93, 43), (98, 36)],
             [(3, 60), (6, 47), (32, 53), (45, 86), (51, 94), (61, 83)]),
            (4, 2, [(14, 2)], [(3, 12)]), (2, 2, [], [])],
           "Los tres casos del PDF: 3, 4 y 2 tiradas.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: la lectura (N K S E y luego S + E parejas), que el tablero tiene N² casillas, que el dado va de 1 a K y que el recorrido es un BFS.",
            "pe": "Los números son correctos pero el formato no: un número por línea.",
            "rte": "Se rompe con el ejemplo: casi seguro un índice fuera del tablero (casillas 1…N², o 0…N²−1 si restas 1)."},
           ["Compara caso a caso: ¿cuál de los tres sale mal?",
            "En el segundo caso caer en la 14 obliga a bajar a la 2: por eso hacen falta 4 tiradas y no 3.",
            "El tercer caso no tiene ninguna línea de serpientes ni escaleras: no leas nada más."])

    # ------------------------------------------------------------------ borde
    prueba("Tablero mínimo 2 × 2", "borde", [(2, 1, [], []), (2, 2, [], []), (2, 1, [], [(2, 3)])],
           "El tablero más pequeño: con dado de 1 cara son 3 tiradas, con 2 caras 2, y con la escalera 2 → 3 son 2.",
           {"wa": "En el tablero de 4 casillas algo falla: la meta es la casilla N² = 4 y se empieza en la 1 sin haber tirado."},
           ["Con un dado de una cara solo se puede avanzar de una en una: 1 → 2 → 3 → 4.",
            "La meta es N², no N."])
    prueba("Tablero grande vacío", "borde", [(30, 30, [], []), (30, 1, [], []), (30, 7, [], [])],
           "Tableros de 30 × 30 sin serpientes ni escaleras: 30, 899 y 129 tiradas.",
           {"wa": "Sin serpientes ni escaleras la respuesta es ⌈(N² − 1) / K⌉. Revisa que el tablero tiene N·N casillas y que no limitas el número de tiradas.",
            "rte": "Con N = 30 hay 900 casillas: revisa el tamaño de tus vectores (N·N, no N)."},
           ["De la 1 a la 900 hay 899 casillas que avanzar.",
            "No pongas un máximo de tiradas: con K = 1 hacen falta 899."])

    # ------------------------------------------------------------------ trampas
    prueba("Se cuentan tiradas, no casillas", "trampa", [(6, 6, [], [])],
           "Tablero 6 × 6 y dado de 6: de la 1 a la 36 hacen falta 6 tiradas.",
           {"wa": "Te sale 7: cuentas las casillas del camino (vértices) en vez de las tiradas (aristas), o la distancia de la casilla 1 empieza en 1."},
           ["Antes de tirar ya estás en la casilla 1: llevas 0 tiradas.",
            "dist[inicio] = 0 y cada casilla nueva recibe dist[actual] + 1."])
    prueba("El dado no tiene por qué tener 6 caras", "trampa", [(5, 3, [], [])],
           "Dado de 3 caras en un tablero 5 × 5: de 3 en 3 hacen falta 8 tiradas.",
           {"wa": "Usas un dado de 6 caras: el dado tiene K caras (de 1 a K), y K lo da la entrada."},
           ["Mira el segundo número de la primera línea de cada caso.",
            "El bucle de las caras va de d = 1 a d = K."])
    prueba("Cada línea es «inicio fin»", "trampa", [(3, 2, [(6, 2)], [])],
           "La serpiente 6 → 2 se baja al caer en la 6 (no se sube al caer en la 2). Son 4 tiradas: 1 → 3 → 5 → 7 → 9.",
           {"wa": "Te sale 3: intercambias los extremos y la serpiente se convierte en una escalera 2 → 6. La primera casilla de cada pareja es donde se cae y la segunda a la que se llega (tanto en serpientes como en escaleras)."},
           ["En una escalera la primera casilla es la de abajo; en una serpiente, la de arriba.",
            "Guarda destino[primera] = segunda, sin mirar si sube o baja."])
    prueba("Solo escaleras (S = 0)", "trampa", [(10, 6, [], [(4, 77), (80, 98)])],
           "Ninguna serpiente y dos escaleras: hay que leer las S + E líneas, aunque S sea 0. Son 3 tiradas: 1 → 4 (sube a la 77), 77 → 80 (sube a la 98) y 98 → 100.",
           {"wa": "No aprovechas las escaleras: lees solo S líneas (las serpientes) y te olvidas de las E escaleras."},
           ["Después de la primera línea vienen S + E parejas: primero las serpientes y luego las escaleras.",
            "Serpientes y escaleras se tratan igual: destino[inicio] = fin."])
    prueba("Caer en una serpiente es obligatorio", "trampa", [(3, 2, [(7, 4)], [])],
           "Dado de 2 en un 3 × 3 con una serpiente 7 → 4: el camino 1 → 3 → 5 → 7 → 9 no vale porque en la 7 se baja a la 4. Hacen falta 5 tiradas.",
           {"wa": "Te sale 4: permites quedarte en la cabeza de la serpiente. Al caer en ella hay que bajar SIEMPRE: desde v, la tirada d lleva a destino[v + d], nunca a v + d."},
           ["Sigue tu camino de 4 tiradas: ¿pasa por la casilla 7?",
            "La casilla de la cabeza de la serpiente nunca se ocupa: se cae en ella y se baja en el mismo movimiento.",
            "Crea solo la arista v → destino[v + d], no también v → v + d."])
    prueba("Subir una escalera también es obligatorio", "trampa", [(3, 1, [], [(3, 7), (2, 5)])],
           "Dado de 1 cara: al caer en la 2 se sube a la 5 a la fuerza y ya no se puede usar la escalera de la 3. Hacen falta 5 tiradas.",
           {"wa": "Te sale 4: permites no subir la escalera de la 2 para coger luego la de la 3. Las escaleras también son obligatorias."},
           ["Con un dado de 1 cara desde la 1 solo se puede ir a la 2… y de ahí se sube a la 5.",
            "Desde v, la tirada d lleva a destino[v + d]: la casilla v + d no se ocupa si es el pie de una escalera."])
    prueba("Varios casos seguidos", "trampa",
           [(10, 6, [(50, 13), (68, 55)], [(3, 60), (6, 47), (51, 94)]), (10, 6, [], []), (3, 2, [(7, 4)], []),
            (4, 2, [], []), (2, 2, [], []), (10, 3, [(97, 2)], [])],
           "Varios tableros seguidos: las serpientes, escaleras y distancias de un caso no deben pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: el vector de destinos (o de distancias, o el grafo) no se reinicia entre casos y aparecen escaleras del caso anterior.",
            "rte": "Un vector del caso anterior con otro tamaño: créalos dentro de cada caso con N² casillas."},
           ["Si el primer caso está bien y los demás no, mira qué variables viven fuera de resuelveCaso.",
            "En cada caso, destino[c] = c para todas las casillas antes de leer las serpientes y escaleras."])
    prueba("Varias escaleras para elegir", "trampa", [(5, 3, [(24, 3)], [(2, 21), (4, 14)])],
           "Desde la casilla 1 se puede subir a la 21 o a la 14, y cerca de la meta hay una serpiente en la 24: hay que comparar todos los caminos (aquí son 3 tiradas, 1 → 2 → 21 → 23 → 25).",
           {"wa": "Eliges tiradas con una regla fija (la cara más alta, la escalera más larga…). Para el mínimo hay que explorar todas las tiradas por capas: BFS."},
           ["Una estrategia voraz no garantiza el mínimo: aquí la escalera más larga lleva a una zona con serpiente.",
            "Haz un BFS desde la casilla 1 en el que cada arista es una tirada."])

    # ------------------------------------------------------------------ aleatorios
    casos = []
    for _ in range(120):
        N = rng.randint(2, 8)
        K = rng.randint(1, N)
        m = N * N // 4
        casos.append(genera(rng, N, K, rng.randint(0, m), rng.randint(0, m)))
    prueba("Tableros pequeños al azar", "aleatorio", casos,
           "120 tableros de hasta 8 × 8 con serpientes y escaleras al azar.",
           {"wa": "Algún caso falla: localiza la línea, busca el tablero y sigue a mano tu BFS."},
           ["Dibuja el tablero del caso que falla con sus serpientes y escaleras.",
            "Revisa que al caer en un extremo siempre se va al otro."])
    casos = []
    for _ in range(25):
        N = rng.randint(10, 40)
        K = rng.randint(1, min(N, 12))
        casos.append(genera(rng, N, K, rng.randint(0, N * 2), rng.randint(0, N * 2)))
    prueba("Tableros medianos al azar", "aleatorio", casos,
           "25 tableros de 10 × 10 a 40 × 40.",
           {"wa": "Algún caso falla: revisa el número de casillas (N²), las caras del dado (K) y que lees S + E parejas."},
           ["La línea que falla es el número de caso.",
            "Prueba ese tablero con tu programa y compara."])

    # ------------------------------------------------------------------ rendimiento
    casos = [genera(rng, 100, rng.randint(90, 100), rng.randint(50, 300), rng.randint(50, 300)) for _ in range(25)]
    prueba("25 tableros 100 × 100 con dado de ~100 caras", "rendimiento", casos,
           "Tableros del tamaño máximo con casi un millón de aristas cada uno.",
           {"tle": "Cada caso debe costar O(N²·K). ¿Usas una matriz de adyacencia de 10.000 × 10.000 o buscas las aristas con hayArista?",
            "mle": "Una matriz de 10.000 × 10.000 no cabe en memoria: usa listas de adyacencia o calcula las tiradas al vuelo."},
           ["El grafo tiene N² vértices y K aristas por vértice: recórrelas una vez.",
            "Ni siquiera hace falta guardar el grafo: desde v, los vecinos son destino[v + d] para d = 1…K."])
    casos = [genera(rng, 100, 1, rng.randint(0, 20), rng.randint(0, 20)) for _ in range(30)]
    prueba("30 tableros 100 × 100 con dado de 1 cara", "rendimiento", casos,
           "Caminos de miles de tiradas en el tablero más grande.",
           {"tle": "Con caminos muy largos tu método es lento: ¿recorres todo el tablero en cada tirada en vez de usar una cola?",
            "wa": "En caminos de miles de tiradas te equivocas: ¿limitas el número de tiradas?"},
           ["El BFS procesa cada casilla una vez, por largo que sea el camino.",
            "No pongas un límite al número de tiradas."])
    return P


VARIANTES = [
    Variante("cuenta casillas en vez de tiradas", [("dist[s] = 0;", "dist[s] = 1;")], prueba=4, v="wa"),
    Variante("dado de 6 caras", [("d <= K && v + d < casillas", "d <= 6 && v + d < casillas")], prueba=5, v="wa"),
    Variante("la serpiente es opcional",
             [("g.ponArista(v, destino[v + d]);   // tirar un d desde v",
               "{ g.ponArista(v, destino[v + d]); if (destino[v + d] < v + d) g.ponArista(v, v + d); }")], prueba=8, v="wa"),
    Variante("la escalera es opcional",
             [("g.ponArista(v, destino[v + d]);   // tirar un d desde v",
               "{ g.ponArista(v, destino[v + d]); if (destino[v + d] > v + d) g.ponArista(v, v + d); }")], prueba=9, v="wa"),
    Variante("lee solo las serpientes", [("for (int i = 0; i < S + E; ++i)", "for (int i = 0; i < S; ++i)")], prueba=7, v="wa"),
    Variante("extremos al revés", [("destino[a - 1] = b - 1;", "destino[b - 1] = a - 1;")], prueba=6, v="wa"),
    Variante("destinos sin reiniciar entre casos",
             [("vector<int> destino(casillas);\n    for (int c = 0; c < casillas; ++c) destino[c] = c;",
               "static vector<int> destino;\n    if ((int)destino.size() < casillas) { int o = destino.size(); destino.resize(casillas); for (int c = o; c < casillas; ++c) destino[c] = c; }")],
             prueba=10, v="rte"),
    Variante("busca las aristas con hayArista (O(V²))",
             [("for (int w : g.ady(v)) {", "for (int w = 0; w < g.V(); ++w) if (g.hayArista(v, w)) {")], prueba=[14, 15], v="tle"),
    Variante("todo en una línea", [("cout << t.distancia(casillas - 1) << '\\n';", "cout << t.distancia(casillas - 1) << ' ';")], prueba=1, v="pe"),
]
