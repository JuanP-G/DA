"""05-2 · Juego de Transformación Modular: juez con pruebas pensadas para cada error típico.

Vértices 0…M-1; cada operación (a, b) da la arista x → (a·x + b) mod M. Mínimo de jugadas de S a T
con BFS, o -1. El solucionador es un BFS propio en Python con los sucesores calculados al vuelo.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-2/EJ_05-2.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-2/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["cout << tm.jugadas(t) << '\\n';", "cout << tm.jugadas(t) + 1 << '\\n';"],
}


def jugadas(M, S, T, ops):
    ops = list({(a % M, b % M) for a, b in ops})
    d = [-1] * M
    d[S] = 0
    cola = deque([S])
    while cola:
        x = cola.popleft()
        if x == T:
            break
        for a, b in ops:
            y = (a * x + b) % M
            if d[y] < 0:
                d[y] = d[x] + 1
                cola.append(y)
    return d[T]


def caso_a_texto(c):
    M, S, T, ops = c
    return f"{M} {S} {T}\n{len(ops)}\n" + "".join(f"{a} {b}\n" for a, b in ops)


def al_azar(rng, Mmax, Nmax):
    M = rng.randint(1, Mmax)
    ops = [(rng.randrange(10000), rng.randrange(10000)) for _ in range(rng.randint(1, Nmax))]
    return (M, rng.randrange(M), rng.randrange(M), ops)


def pruebas():
    rng = random.Random(522)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{jugadas(*c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [(7, 2, 6, [(3, 1), (2, 2)]), (5, 1, 0, [(2, 1), (3, 1)]), (10, 2, 1, [(2, 0)]), (6, 4, 4, [(2, 0)])],
           "Los cuatro casos del PDF: 1, 2, -1 y 0 jugadas.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: el orden de lectura (M S T, luego N y N parejas a b), el módulo y que el recorrido sea un BFS.",
            "pe": "Los números están bien pero el formato no: un número por línea y nada más.",
            "rte": "Se rompe con el ejemplo: casi seguro calculas un vértice fuera de 0…M-1 (falta aplicar el módulo al final)."},
           ["Compara caso a caso: ¿cuál de los cuatro sale mal?",
            "El tercer caso es imposible (-1) y el cuarto ya empieza en el objetivo (0).",
            "Lee en este orden: M, S, T, N y luego N parejas (a, b)."])

    # ------------------------------------------------------------------ borde
    prueba("M = 1: solo existe el 0", "borde", [(1, 0, 0, [(5, 7)]), (1, 0, 0, [(0, 0), (9999, 9999)])],
           "Con módulo 1 el único número es el 0: S = T = 0 y la respuesta es 0.",
           {"wa": "Con M = 1 debe salir 0: el objetivo ya es el número de partida.",
            "rte": "Con M = 1 hay un único vértice: revisa los tamaños de tus vectores y que todo se reduce módulo M."},
           ["¿Cuántos números hay con módulo 1?",
            "Si S y T son iguales la respuesta es 0, sin hacer ninguna jugada."])
    prueba("Origen igual al destino", "borde",
           [(10, 3, 3, [(2, 1)]), (9999, 9998, 9998, [(1, 1)]), (10000, 0, 0, [(0, 5), (3, 3)])],
           "Si S = T no hace falta ninguna jugada: 0.",
           {"wa": "Cuando S = T debe salir 0. Si sale otra cosa, compruebas el objetivo solo al meter vecinos en la cola, o la distancia de S no empieza en 0."},
           ["¿Qué sale con «10 3 3»?",
            "dist[S] = 0 antes de empezar; comprueba si has llegado a T al SACAR de la cola."])
    prueba("Factores y sumandos mayores que M", "borde",
           [(7, 1, 5, [(9999, 9998)]), (3, 0, 2, [(10, 5)]), (13, 4, 0, [(26, 13), (14, 12)])],
           "a y b pueden ser mayores que M: solo cuenta su valor módulo M.",
           {"wa": "Con a o b ≥ M algo se calcula mal: el resultado es (a·x + b) mod M; puedes reducir a y b módulo M antes, pero el módulo final no se puede quitar.",
            "rte": "(a·x + b) sin el módulo final se sale del rango 0…M-1."},
           ["Calcula a mano el primer caso: 9.999·1 + 9.998 = 19.997, y 19.997 mod 7 = 5.",
            "Aplica el módulo al resultado completo: (a * x + b) % M."])

    # ------------------------------------------------------------------ trampas
    prueba("Se cuentan jugadas, no números", "trampa", [(10, 2, 7, [(1, 5)])],
           "2 + 5 = 7: una sola jugada.",
           {"wa": "Te sale 2: cuentas los números del camino (vértices) en vez de las jugadas (aristas), o la distancia de S empieza en 1."},
           ["Una jugada es una arista: el camino 2 → 7 tiene una arista.",
            "dist[S] = 0 y cada vecino nuevo recibe dist[x] + 1."])
    prueba("S = T aunque haya una operación que vuelve a S", "trampa", [(10, 4, 4, [(1, 0), (3, 2)])],
           "La operación 1·x + 0 deja el número igual (un lazo). Aun así, de 4 a 4 hacen falta 0 jugadas.",
           {"wa": "Debe salir 0. Si sale 1 o -1: compruebas el objetivo al meter un vecino en la cola (y el lazo 4 → 4 o nada lo vuelve a meter), en vez de al sacarlo."},
           ["El número de partida ya es el objetivo: ninguna jugada.",
            "Marca S como visitado con distancia 0 al empezar.",
            "Comprueba «¿es T?» al sacar cada número de la cola: así S también se comprueba."])
    prueba("Objetivo inalcanzable: -1", "trampa", [(10, 1, 0, [(1, 2)])],
           "Sumando 2 desde el 1 solo se visitan impares: el 0 no se alcanza y hay que escribir -1.",
           {"wa": "Si no se puede llegar hay que escribir -1. Si sale un número enorme, 0 u otro valor, no tratas el caso imposible (el «infinito» de tu vector de distancias no es -1)."},
           ["¿Qué escribe tu programa si la cola se vacía sin haber visto T?",
            "Inicializa las distancias a -1 («sin visitar») y escribe dist[T] tal cual: si no se alcanza, sigue valiendo -1."])
    prueba("El módulo se aplica al resultado completo", "trampa", [(7, 6, 0, [(1, 1), (1, 6)])],
           "Con la operación x + 1, 6 + 1 = 7 y 7 mod 7 = 0: una jugada. Hay que reducir (a·x + b) entero, no solo a·x.",
           {"wa": "El resultado de cada jugada es (a·x + b) mod M. Si haces (a·x mod M) + b, el valor puede quedar ≥ M.",
            "rte": "Calculas un número ≥ M (por ejemplo (a·x) % M + b sin volver a reducir, o sin el módulo): te sales del vector o del Digrafo."},
           ["Con M = 7, x = 6 y la operación x + 1: ¿qué número sale? Tiene que estar entre 0 y 6.",
            "El vecino es (a * x + b) % M: el módulo va al final, después de sumar b."])
    prueba("El orden importa: de S a T, no de T a S", "trampa", [(10, 3, 6, [(2, 0)])],
           "De 3 se llega a 6 (3·2) en una jugada, pero de 6 nunca se vuelve a 3.",
           {"wa": "Sale -1 o un número que no es 1: estás buscando el camino de T a S (has cambiado el orden de lectura de S y T)."},
           ["La primera línea de cada caso es «M S T»: módulo, partida y objetivo.",
            "Haz el BFS desde S y mira la distancia de T."])
    prueba("Las jugadas no se pueden deshacer", "trampa", [(10, 6, 3, [(2, 0)])],
           "De 3 se llega a 6, pero de 6 solo se recorre 6 → 2 → 4 → 8 → 6: el 3 es inalcanzable (-1).",
           {"wa": "Te sale 1 (o algo distinto de -1): recorres las aristas en los dos sentidos. El grafo es DIRIGIDO: que x lleve a y no significa que y lleve a x."},
           ["De 6 con «×2 mod 10», ¿qué números salen?",
            "Usa Digrafo (no Grafo): ponArista(x, y) añade solo x → y."])
    prueba("El mínimo exige un BFS", "trampa", [(8, 2, 4, [(1, 3), (9, 1)])],
           "Con las operaciones x + 3 y x + 1 (9 mod 8 = 1), de 2 a 4 son dos jugadas (+1, +1). Un DFS encuentra antes un camino más largo.",
           {"wa": "Sale más de 2: tu recorrido no es en anchura. Con una pila o recursión (DFS) la primera vez que llegas a un número no es por el camino más corto.",
            "tle": "Pruebas todos los caminos posibles: el número crece de forma exponencial. Usa un BFS que visite cada número una vez."},
           ["Para el mínimo número de jugadas hace falta un BFS: visita los números por capas.",
            "Usa una cola (queue): saca por delante y mete por detrás.",
            "La distancia de un número se fija la primera vez que se descubre: dist[y] = dist[x] + 1."])
    prueba("Camino muy largo: 9.999 jugadas", "trampa", [(10000, 0, 9999, [(1, 1)])],
           "Con la única operación x + 1 hay que dar 9.999 pasos.",
           {"wa": "En caminos largos te equivocas: ¿limitas el número de jugadas o la profundidad de la búsqueda?",
            "tle": "Para un camino de 9.999 pasos tu método es demasiado lento: ¿repasas todos los números en cada paso? El BFS visita cada número una vez."},
           ["No pongas un tope a la profundidad: el BFS termina al sacar T o al vaciarse la cola.",
            "Cada número entra una vez en la cola: el coste total es O(M·N)."])
    prueba("Varios casos seguidos", "trampa",
           [(10000, 0, 9999, [(1, 1)]), (10, 3, 7, [(1, 1)]), (7, 2, 6, [(3, 1), (2, 2)]), (10, 1, 0, [(1, 2)]),
            (3000, 2999, 0, [(1, 1)]), (5, 1, 0, [(2, 1), (3, 1)]), (1, 0, 0, [(3, 3)])],
           "Casos con módulos distintos uno tras otro: nada de un caso debe quedar para el siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: las distancias, los visitados o el grafo vienen del caso anterior.",
            "rte": "Usas vectores con el tamaño del caso anterior (M cambia en cada caso): créalos dentro de cada caso con tamaño M."},
           ["Si el primer caso está bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "El grafo depende de M y de las operaciones: constrúyelo de nuevo en cada caso, con sus distancias."])

    # ------------------------------------------------------------------ aleatorios
    prueba("Casos pequeños al azar", "aleatorio", [al_azar(rng, 12, 3) for _ in range(150)],
           "150 casos con M ≤ 12 y hasta 3 operaciones (hay alcanzables e inalcanzables).",
           {"wa": "Algún caso concreto falla: localiza la línea, busca ese caso en la entrada y hazlo a mano (son muy pequeños)."},
           ["Con M ≤ 12 puedes dibujar el grafo entero en papel.",
            "Fíjate si el caso que falla es imposible (-1), si S = T o si alguna operación tiene a o b ≥ M."])
    prueba("Casos medianos al azar", "aleatorio", [al_azar(rng, 2000, 8) for _ in range(60)],
           "60 casos con M ≤ 2.000 y hasta 8 operaciones.",
           {"wa": "Algún caso falla: mira la línea, encuentra el caso y revisa el módulo y el -1."},
           ["La línea que falla es el número de caso.",
            "Comprueba que (a·x + b) se reduce módulo M en cada jugada."])

    # ------------------------------------------------------------------ rendimiento
    grandes = []
    for _ in range(50):
        # operaciones pares sobre M par: desde S par nunca se alcanza un T impar -> BFS completo
        ops = [(2 * rng.randrange(5000), 2 * rng.randrange(5000)) for _ in range(100)]
        grandes.append((10000, 2 * rng.randrange(5000), 2 * rng.randrange(5000) + 1, ops))
    prueba("50 casos con M = 10.000 y N = 100", "rendimiento", grandes,
           "Casos del tamaño máximo (un millón de aristas cada uno) con el objetivo inalcanzable: el BFS recorre todo.",
           {"tle": "Cada caso debe costar O(M·N). ¿Usas una matriz de adyacencia M × M, buscas aristas con hayArista o recorres todos los números en cada paso?",
            "mle": "Una matriz M × M (10⁸ casillas) no cabe: usa listas de adyacencia (Digrafo) o calcula los vecinos al vuelo.",
            "wa": "Con casos grandes falla algo: ¿el -1 de los inalcanzables?"},
           ["El grafo tiene M·N aristas como mucho: recórrelas una vez.",
            "No hace falta guardar el grafo: los vecinos de x se pueden calcular al vuelo con las N operaciones.",
            "Evita la matriz de adyacencia y hayArista: son O(M²)."])
    largos = [(10000, rng.randrange(10000), 0, [(1, 1)]) for _ in range(200)]
    largos = [(M, S, (S + 9999) % M, ops) for M, S, T, ops in largos]
    prueba("200 caminos de 9.999 jugadas", "rendimiento", largos,
           "Muchos casos donde el único camino da la vuelta entera al módulo.",
           {"tle": "Tu método es O(M²) por caso o similar: ¿repasas todos los números en cada «ronda» en vez de usar una cola?"},
           ["Un BFS con cola procesa cada número una vez: 10.000 operaciones por caso.",
            "Si en cada paso recorres todos los números buscando los de la capa actual, el coste se multiplica por la longitud del camino."])
    return P


VARIANTES = [
    Variante("cuenta números en vez de jugadas", [("dist[s] = 0;", "dist[s] = 1;")], prueba=5, v="wa"),
    Variante("no marca S como visitado al empezar",
             [("if (x == t) return;               // t ya tiene su distancia minima", ""),
              ("dist[s] = 0;", "dist[s] = 0;\n        vector<bool> visit(g.V(), false);"),
              ("if (dist[y] == -1) {", "if (!visit[y]) {\n                    visit[y] = true;")],
             prueba=6, v="wa"),
    Variante("no escribe -1 si es imposible", [("int jugadas(int t) const { return dist[t]; }", "int jugadas(int t) const { return dist[t] == -1 ? 1000000000 : dist[t]; }")], prueba=7, v="wa"),
    Variante("módulo solo de a·x", [("(op.first * x + op.second) % m", "(op.first * x) % m + op.second")], prueba=8, v="rte"),
    Variante("lee T antes que S", [("cin >> m >> s >> t >> n;", "cin >> m >> t >> s >> n;")], prueba=9, v="wa"),
    Variante("grafo no dirigido",
             [("g.ponArista(x, (op.first * x + op.second) % m);   // x --> resultado de la operacion",
               "{ g.ponArista(x, (op.first * x + op.second) % m); g.ponArista((op.first * x + op.second) % m, x); }")],
             prueba=10, v="wa"),
    Variante("DFS (pila) en vez de BFS",
             [("queue<int> q;", "deque<int> q;"), ("int x = q.front(); q.pop();", "int x = q.back(); q.pop_back();"),
              ("q.push(s);", "q.push_back(s);"), ("q.push(y);", "q.push_back(y);")],
             prueba=11, v="wa"),
    Variante("distancias sin reiniciar entre casos",
             [("    vector<int> dist;   // dist[x]", "    static vector<int> dist;   // dist[x]"),
              ("TransformacionModular(Digrafo const& g, int s, int t) : dist(g.V(), -1) {",
               "TransformacionModular(Digrafo const& g, int s, int t) {\n        if (dist.size() < (size_t)g.V()) dist.resize(g.V(), -1);"),
              ("};\n\nvoid resuelveCaso()", "};\nvector<int> TransformacionModular::dist;\n\nvoid resuelveCaso()")],
             prueba=13, v="wa"),
    Variante("busca los vecinos con hayArista (O(M²))",
             [("for (int y : g.ady(x)) {", "for (int y = 0; y < g.V(); ++y) if (g.hayArista(x, y)) {")], prueba=[16, 17], v="tle"),
    Variante("todo en una línea", [("cout << tm.jugadas(t) << '\\n';", "cout << tm.jugadas(t) << ' ';")], prueba=1, v="pe"),
]
