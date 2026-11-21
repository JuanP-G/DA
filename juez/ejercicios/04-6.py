"""04-6 · Un nodo muy muy lejano: juez con pruebas pensadas para cada error típico.

Entrada: número de redes; cada una «N» (1..10.000) y «C» (0..50.000), C conexiones «a b» (1..N,
distintos, sin repetir), K consultas (1..10) y K líneas «origen TTL» (TTL 0..20.000).
Salida: por consulta, cuántos nodos NO recibe el mensaje (los que están a más de TTL saltos del
origen), y «---» al acabar cada red.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-6/EJ_04-6.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-6/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["if (dist[v] != ttl) {", "if (dist[v] + 1 < ttl) {"],
}


# ---------------------------------------------------------------- solucionador independiente
def inalcanzables(N, aristas, origen, ttl):
    """BFS completo (sin cortar) y se cuentan los nodos con distancia > TTL o sin camino."""
    ady = [[] for _ in range(N + 1)]
    for a, b in aristas:
        ady[a].append(b)
        ady[b].append(a)
    dist = [-1] * (N + 1)
    dist[origen] = 0
    cola = deque([origen])
    while cola:
        v = cola.popleft()
        for w in ady[v]:
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                cola.append(w)
    return sum(1 for v in range(1, N + 1) if dist[v] < 0 or dist[v] > ttl)


def caso_a_texto(caso):
    N, aristas, consultas = caso
    return (f"{N}\n{len(aristas)}\n" + "".join(f"{a} {b}\n" for a, b in aristas)
            + f"{len(consultas)}\n" + "".join(f"{o} {t}\n" for o, t in consultas))


def caso_a_salida(caso):
    N, aristas, consultas = caso
    return "".join(f"{inalcanzables(N, aristas, o, t)}\n" for o, t in consultas) + "---\n"


# ---------------------------------------------------------------- generadores
def aleatorio_pequeno(rng):
    N = rng.randint(1, 10)
    pos = [(a, b) for a in range(1, N + 1) for b in range(a + 1, N + 1)]
    ar = rng.sample(pos, rng.randint(0, min(len(pos), N + 3)))
    ar = [(a, b) if rng.random() < .5 else (b, a) for a, b in ar]
    consultas = [(rng.randint(1, N), rng.choice([0, 1, 1, 2, 2, 3, 4, 20000])) for _ in range(rng.randint(1, 10))]
    return (N, ar, consultas)


def grande(rng, N, C):
    """Red conexa de N nodos (un árbol aleatorio poco profundo) más aristas al azar hasta C."""
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    ar = set()
    for i in range(1, N):
        j = rng.randrange(max(0, i - 3), i)          # árbol «estirado»: distancias grandes
        ar.add((min(perm[i], perm[j]), max(perm[i], perm[j])))
    while len(ar) < C:
        a, b = rng.sample(range(1, N + 1), 2)
        ar.add((min(a, b), max(a, b)))
    ar = list(ar)
    rng.shuffle(ar)
    return ar


def pruebas():
    rng = random.Random(46)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(7, [(1, 2), (2, 3), (1, 4), (4, 5), (5, 6), (4, 6), (6, 7)], [(4, 2), (4, 3), (7, 3), (1, 0)]),
            (6, [(1, 3), (3, 5), (5, 1), (2, 4), (2, 6)], [(1, 2), (2, 1)])],
           "Las dos redes del PDF, con una consulta de TTL 0 y una red partida en dos trozos.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: el mensaje llega a los nodos a distancia ≤ TTL del origen, se cuentan los que NO llegan, y tras cada red va una línea «---».",
            "pe": "Los números están bien pero el formato no: un número por línea y «---» tras cada red."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "Desde 4 con TTL 2 llegan 4, 1, 5, 6 (a 1 salto) y 2, 7 (a 2 saltos): solo falta el 3.",
            "Calcula las distancias mínimas con un BFS desde el origen y cuenta los nodos con distancia > TTL o sin camino."])
    prueba("Un solo nodo", "borde", [(1, [], [(1, 0), (1, 5)])],
           "N = 1: el origen siempre recibe su propio mensaje (0 inalcanzables).",
           {"wa": "El origen cuenta como alcanzado: con un solo nodo la respuesta es 0."},
           ["¿Cuántos nodos quedan sin mensaje si solo existe el origen?",
            "Cuenta el origen como alcanzado nada más empezar."])
    prueba("Sin ninguna conexión", "borde", [(5, [], [(3, 4), (5, 0)])],
           "C = 0: el mensaje no sale del origen; los otros 4 nodos son inalcanzables.",
           {"wa": "Sin conexiones solo se entera el origen: N − 1 inalcanzables."},
           ["Con 5 nodos y ninguna conexión, la respuesta es 4.",
            "Comprueba que lees bien C = 0 (no hay líneas de conexiones) y luego K."])
    prueba("Nodos numerados de 1 a N", "trampa", [(4, [(4, 1), (1, 2), (2, 3)], [(4, 1), (4, 3)])],
           "El nodo N aparece en las conexiones y como origen.",
           {"rte": "Los nodos van de 1 a N: hay que restar 1 tanto al leer las conexiones (Grafo(cin, 1)) como al origen de cada consulta."},
           ["El nodo 4 existe cuando N = 4.",
            "¿Restas 1 al origen de la consulta igual que a las conexiones?",
            "Usa Grafo(cin, 1) y pasa origen − 1 al BFS."])
    prueba("TTL 0: solo se entera el origen", "trampa",
           [(3, [(1, 2), (2, 3)], [(2, 0)]),
            (5, [(1, 2), (1, 3), (1, 4), (1, 5)], [(1, 0)]),
            (4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(3, 0)])],
           "Consultas con TTL 0: el origen tiene el mensaje pero no lo reenvía (N − 1 inalcanzables).",
           {"wa": "Con TTL 0 el origen tiene el mensaje (cuenta como alcanzado) pero no lo reenvía. Si te sale N, no cuentas el origen; si te sale menos de N − 1, reenvías aunque el TTL ya no lo permita."},
           ["En la primera red, desde 2 con TTL 0 solo lo tiene el 2: la respuesta es 2.",
            "Un nodo a distancia d recibe el mensaje si d ≤ TTL; el origen está a distancia 0.",
            "Cuenta el origen al empezar y no expandas un nodo cuya distancia ya es igual al TTL."])
    prueba("TTL 1: llegan exactamente los vecinos", "trampa",
           [(6, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6)], [(2, 1)]),
            (7, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)], [(4, 1)])],
           "Con TTL 1 el mensaje llega a los vecinos del origen y a nadie más.",
           {"wa": "El último salto permitido sí llega: un nodo a distancia igual al TTL recibe el mensaje (y ya no lo reenvía). Te sobra o te falta un nivel."},
           ["Desde 2 con TTL 1 lo reciben 2, 1, 3 y 5: faltan 4 y 6, la respuesta es 2.",
            "Revisa la condición de corte: ¿es dist < TTL, dist ≤ TTL, dist + 1 < TTL...?",
            "Un nodo v se expande si dist[v] < TTL; así los de distancia TTL reciben el mensaje pero no lo reenvían."])
    prueba("Varias consultas sobre la misma red", "trampa",
           [(7, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7)], [(1, 10), (6, 1), (7, 2), (1, 0), (6, 4)])],
           "Cinco consultas con orígenes distintos sobre la misma red: cada una empieza de cero.",
           {"wa": "Las distancias (o los visitados) de una consulta se quedan para la siguiente. Hay que empezar cada consulta con todo sin visitar."},
           ["La primera consulta sale bien y la segunda no: ¿qué conserva tu programa entre consultas?",
            "Crea el vector de distancias dentro de cada consulta (o reinícialo a −1 entero)."])
    prueba("El camino corto no es el primero que se encuentra", "trampa",
           [(6, [(1, 2), (1, 3), (3, 4), (4, 5), (2, 5), (5, 6)], [(1, 3), (1, 2)])],
           "Al nodo 5 se llega en 2 saltos por 1-2-5, aunque también por el camino largo 1-3-4-5; el 6 está a 3.",
           {"wa": "Un DFS (o una pila en lugar de una cola) no calcula distancias mínimas: puede llegar al 6 por el camino largo y darlo por inalcanzable. Hace falta un BFS."},
           ["Desde 1 con TTL 3 llega a todos: la respuesta es 0. Si llegas al 5 por 1-3-4-5 te quedas sin TTL para el 6.",
            "El BFS visita por orden de distancia; el DFS no.",
            "Usa una cola (queue): la primera vez que llegas a un nodo es por el camino más corto."])
    prueba("Origen aislado en una red partida", "trampa",
           [(6, [(1, 2), (2, 3), (4, 5)], [(6, 3), (1, 100), (4, 1)])],
           "Una red en tres trozos y un nodo sin conexiones como origen.",
           {"wa": "Los nodos de otros trozos nunca reciben el mensaje, por grande que sea el TTL; y un origen aislado solo se tiene a sí mismo."},
           ["Desde 6 (aislado) la respuesta es 5; desde 1 con TTL 100, 3.",
            "Los nodos que el BFS no visita también son inalcanzables: N − alcanzados."])
    prueba("TTL mayor que cualquier distancia", "trampa",
           [(8, [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7)], [(1, 20000), (7, 20000), (8, 19999)])],
           "TTL de 20.000 en una red pequeña: llega a todo su trozo.",
           {"wa": "Un TTL enorme no debe dar problemas: el BFS se acaba al no quedar nodos nuevos.",
            "rte": "¿Reservas algo del tamaño del TTL o indexas con él?",
            "tle": "No hagas un paso por cada unidad de TTL: el BFS termina en O(N + C) aunque el TTL sea 20.000."},
           ["Desde 1 llega a 1, 2, 3, 4: la respuesta es 4.",
            "No uses el TTL como tamaño de nada ni como número de vueltas de un bucle."])
    prueba("Ciclos: cada nodo se cuenta una vez", "trampa",
           [(6, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 4)], [(1, 1), (2, 2), (5, 5)])],
           "Muchos ciclos: a cada nodo se llega por varios caminos, pero se cuenta una sola vez.",
           {"wa": "Si cuentas un nodo cada vez que llegas a él (y no solo la primera), te salen más alcanzados de la cuenta."},
           ["Desde 1 con TTL 1 llegan 1, 2, 3, 4: la respuesta es 2.",
            "Cuenta un nodo solo cuando lo descubres por primera vez (dist == −1)."])
    prueba("Varias redes seguidas", "trampa",
           [(9, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)], [(1, 3)]),
            (4, [(1, 2), (3, 4)], [(1, 5), (4, 0)]),
            (3, [], [(2, 1)]),
            (5, [(1, 2), (2, 3), (3, 4), (4, 5)], [(5, 2)])],
           "Redes de distintos tamaños seguidas: nada de la red anterior debe quedar.",
           {"wa": "Algo se arrastra de una red a la siguiente: el grafo, las distancias o el contador están declarados fuera de la función de cada caso."},
           ["Si la primera red sale bien y la segunda no, mira qué variables viven fuera de resuelveCaso.",
            "Lee el grafo y crea las distancias dentro de la función de cada caso (y de cada consulta)."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(40)],
           "40 redes pequeñas al azar con consultas de todo tipo (TTL 0, 1, 2... y 20.000).",
           {"wa": "Hay alguna consulta concreta que no tratas: localiza su red (cada red acaba en «---») y calcula a mano las distancias."},
           ["Busca la red y la consulta de la línea que falla y dibuja la red.",
            "Calcula las distancias desde el origen por capas y cuenta las que pasan del TTL."])
    # ---- grandes
    N = 10000
    redes = []
    for _ in range(2):
        ar = grande(rng, N, 50000)
        redes.append((N, ar, [(rng.randint(1, N), 20000) for _ in range(5)] + [(rng.randint(1, N), rng.randint(1, 12)) for _ in range(5)]))
    for _ in range(6):
        ar = grande(rng, N, N - 1)
        redes.append((N, ar, [(rng.randint(1, N), 20000 - k) for k in range(10)]))
    prueba("Red grande con TTL enorme", "rendimiento", redes,
           "Ocho redes de 10.000 nodos (dos con 50.000 conexiones), con 10 consultas cada una y TTL de hasta 20.000.",
           {"tle": "Cada consulta debe costar O(N + C). Si das una vuelta a todos los nodos por cada nivel de TTL, son 20.000 × 10.000 pasos por consulta.",
            "mle": "Una matriz de adyacencia 10.000 × 10.000 de enteros no cabe: usa listas de adyacencia (la clase Grafo)."},
           ["¿Cuánto cuesta una consulta en función del TTL?",
            "Con una cola, cada nodo entra una vez y cada conexión se mira dos veces: el TTL no influye en el coste.",
            "No busques «los nodos del nivel d» recorriendo todos los nodos: sácalos de la cola del BFS."])
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    camino = [(perm[i], perm[i + 1]) for i in range(N - 1)]
    prueba("Camino de 10.000 nodos", "rendimiento",
           [(N, camino, [(perm[0], 20000), (perm[0], 9998), (perm[N // 2], 2500), (perm[-1], 0), (perm[123], 9999)])],
           "Una red en forma de línea: distancias de hasta 9.999 saltos.",
           {"tle": "Algo se repite de más en un recorrido muy largo.",
            "rte": "Si haces un DFS recursivo, la profundidad llega a 10.000; mejor un BFS con cola."},
           ["Desde un extremo con TTL 9.998 falta exactamente un nodo.",
            "El BFS con cola recorre la línea entera en O(N)."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(caso_a_salida(c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("lee las conexiones sin restar 1", [("Grafo g(cin, 1);", "Grafo g(cin);")], prueba=4, v="rte"),
    Variante("no resta 1 al origen", [("NodosAlcanzables na(g, origen - 1, ttl);", "NodosAlcanzables na(g, origen, ttl);")], prueba=4, v="rte"),
    Variante("no cuenta el origen", [("        dist[origen] = 0;\n        ++alcanzados;", "        dist[origen] = 0;")], prueba=5, v="wa"),
    Variante("reenvía un salto de más", [("if (dist[v] != ttl) {", "if (dist[v] <= ttl) {")], prueba=5, v="wa"),
    Variante("se queda un salto corto", [("if (dist[v] != ttl) {", "if (dist[v] + 1 < ttl) {")], prueba=6, v="wa"),
    Variante("no reinicia las distancias entre consultas",
             [("NodosAlcanzables(Grafo const& g, int origen, int ttl) : dist(g.V(), -1), alcanzados(0) {",
               "NodosAlcanzables(Grafo const& g, int origen, int ttl) : alcanzados(0) {\n        if ((int)dist.size() != g.V()) dist.assign(g.V(), -1);"),
              ("    vector<int> dist;   // dist[v]", "    static inline vector<int> dist;   // dist[v]")], prueba=7, v="wa"),
    Variante("pila en lugar de cola (DFS)",
             [("#include <queue>", "#include <queue>\n#include <stack>"),
              ("queue<int> q;", "stack<int> q;"),
              ("int v = q.front(); q.pop();", "int v = q.top(); q.pop();")], prueba=8, v="wa"),
    Variante("recorre todos los nodos en cada nivel",
             [("        queue<int> q;\n        dist[origen] = 0;\n        ++alcanzados;\n        q.push(origen);",
               "        dist[origen] = 0;\n        ++alcanzados;\n"
               "        for (int d = 0; d < ttl; ++d)\n"
               "            for (int v = 0; v < g.V(); ++v)\n"
               "                if (dist[v] == d)\n"
               "                    for (int w : g.ady(v))\n"
               "                        if (dist[w] == -1) { dist[w] = d + 1; ++alcanzados; }\n"
               "        queue<int> q;")], prueba=14, v="tle"),
]
