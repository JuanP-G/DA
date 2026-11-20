"""07-3 · RapidEats con ruta: juez con pruebas pensadas para cada error típico.

Grafo NO dirigido valorado (puede haber varios tramos entre los mismos puntos). Para cada pedido,
tiempo mínimo y el camino «t: a -> b -> c», o NO LLEGA; «---» tras cada caso.
El enunciado admite cualquier camino mínimo, pero el juez compara el texto exacto: por eso TODAS
las consultas de las pruebas tienen un único camino mínimo (lo comprueba el generador).
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-3/EJ_07-3.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-3/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-3/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["camino.push_front(v);", "camino.push_back(v);"],
}

MAXT = 500


# ---------------------------------------------------------------- solucionador independiente
def adyacencia(N, tramos):
    """Lista de adyacencia con un solo tramo (el más rápido) por pareja de puntos."""
    mejor = {}
    for u, v, t in tramos:
        for a, b in ((u, v), (v, u)):
            if t < mejor.get((a, b), 10 ** 9):
                mejor[a, b] = t
    ady = [[] for _ in range(N + 1)]
    for (a, b), t in mejor.items():
        ady[a].append((b, t))
    return ady


def ruta(N, ady, o, d):
    """(tiempo, camino, nº de caminos mínimos distintos hasta 2) o None si no se llega."""
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
        for w, t in ady[v]:
            if x + t < dist[w]:
                dist[w] = x + t
                heapq.heappush(cola, (x + t, w))
    if dist[d] == INF:
        return None
    cnt = [0] * (N + 1)
    pred = [0] * (N + 1)
    cnt[o] = 1
    for v in orden:
        for w, t in ady[v]:
            if dist[v] + t == dist[w]:
                cnt[w] = min(2, cnt[w] + cnt[v])
                pred[w] = v
    camino = [d]
    while camino[-1] != o:
        camino.append(pred[camino[-1]])
    return dist[d], camino[::-1], cnt[d]


def salida_caso(caso):
    N, tramos, pedidos = caso
    ady = adyacencia(N, tramos)
    s = ""
    for o, d in pedidos:
        r = ruta(N, ady, o, d)
        if r is None:
            s += "NO LLEGA\n"
        else:
            assert r[2] == 1, ("camino mínimo no único", o, d)
            s += f"{r[0]}: " + " -> ".join(map(str, r[1])) + "\n"
    return s + "---\n"


def valida(caso):
    N, tramos, pedidos = caso
    assert 2 <= N <= 20000 and 0 <= len(tramos) <= 100000 and 1 <= len(pedidos) <= 10
    for u, v, t in tramos:
        assert 1 <= u <= N and 1 <= v <= N and u != v and 1 <= t <= MAXT
    for o, d in pedidos:
        assert 1 <= o <= N and 1 <= d <= N and o != d


def caso_a_texto(caso):
    N, tramos, pedidos = caso
    return (f"{N} {len(tramos)}\n" + "".join(f"{u} {v} {t}\n" for u, v, t in tramos)
            + f"{len(pedidos)}\n" + "".join(f"{o} {d}\n" for o, d in pedidos))


# ---------------------------------------------------------------- generadores
def pedidos_unicos(r, N, tramos, K, lejos=False, intentos=400):
    """K pedidos cuyo camino mínimo es único (o que no llegan). Con lejos=True se prefieren
    destinos con caminos largos (para que no se pueda parar pronto)."""
    ady = adyacencia(N, tramos)
    elegidos = []
    for _ in range(intentos):
        if len(elegidos) == K:
            break
        o, d = r.randint(1, N), r.randint(1, N)
        if o == d:
            continue
        x = ruta(N, ady, o, d)
        if x is not None and x[2] != 1:
            continue
        if lejos and (x is None or len(x[1]) < 8):
            continue
        elegidos.append((o, d))
    assert elegidos
    return elegidos


def aleatorio(r, N, C, K, maxt=MAXT, paralelos=0.1):
    tramos = []
    for _ in range(C):
        if tramos and r.random() < paralelos:
            u, v, _t = r.choice(tramos)
        else:
            u, v = r.sample(range(1, N + 1), 2)
        tramos.append((u, v, r.randint(1, maxt)))
    return (N, tramos, pedidos_unicos(r, N, tramos, K))


def grande(r, N, C, K):
    tramos = [(r.randint(1, i - 1), i, r.randint(1, MAXT)) for i in range(2, N + 1)]   # conexo
    while len(tramos) < C:
        u, v = r.sample(range(1, N + 1), 2)
        tramos.append((u, v, r.randint(1, MAXT)))
    r.shuffle(tramos)
    tramos = [(v, u, t) if r.random() < .5 else (u, v, t) for u, v, t in tramos]
    return (N, tramos, pedidos_unicos(r, N, tramos, K, lejos=True, intentos=200))


def cadena_larga(r, N):
    """Una cadena con los puntos en orden aleatorio y atajos que no lo son: caminos de N puntos."""
    perm = list(range(1, N + 1))
    r.shuffle(perm)
    tramos = [(perm[i], perm[i + 1], r.randint(1, 3)) for i in range(N - 1)]
    for i in range(0, N - 5, 97):
        tramos.append((perm[i], perm[i + 4], MAXT))
    r.shuffle(tramos)
    a, b = perm[0], perm[-1]
    pedidos = [(a, b), (b, a)] * 5
    return (N, tramos, pedidos)


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(73)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (4, [(1, 2, 15), (1, 3, 30), (2, 3, 20), (4, 3, 10)], [(1, 3), (4, 1)])
    ej2 = (4, [(1, 3, 10), (2, 4, 20)], [(1, 2), (3, 1)])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF, con sus pedidos, NO LLEGA y las líneas ---.",
           {"wa": "Si falla hasta el ejemplo, compara carácter a carácter: «tiempo: a -> b -> c», con los dos puntos pegados al tiempo, flechas con un espacio a cada lado y --- tras cada caso.",
            "pe": "Los datos están bien pero el formato no: espacios o saltos de línea de más o de menos (por ejemplo, entre el tiempo y el camino).",
            "rte": "Error de ejecución con el ejemplo: los puntos van del 1 al N (resta 1 al leer) o la reconstrucción del camino se sale del vector."},
           ["Compara tu salida con «30: 1 -> 3» y «40: 4 -> 3 -> 1».",
            "La entrada pone N y C en la misma línea; después de los tramos vienen K y los K pedidos.",
            "Escribe --- después de todos los pedidos de cada caso."])
    prueba("Tramo directo", "borde", [(2, [(1, 2, 5)], [(1, 2)])],
           "Dos puntos y un tramo: «5: 1 -> 2».",
           {"wa": "Con un solo tramo debe salir «5: 1 -> 2». Revisa que escribes el origen, el destino y que sumas 1 a los índices al escribir.",
            "rte": "Error de ejecución en el caso más pequeño: revisa los índices (desde 1) y la reconstrucción del camino."},
           ["El camino tiene dos puntos: el origen y el destino.",
            "Al reconstruir con ulti[] desde el destino, el bucle para al llegar al origen: añádelo tú."])
    prueba("Sin tramos: NO LLEGA", "borde", [(3, [], [(1, 2), (3, 1)])],
           "Ningún tramo: todos los pedidos son NO LLEGA y aun así se escribe ---.",
           {"wa": "Cuando no hay camino se escribe exactamente NO LLEGA (sin tiempo) y, al terminar los pedidos del caso, ---.",
            "rte": "Si no hay camino no intentes reconstruirlo: ulti del destino no existe."},
           ["Comprueba si la distancia al destino sigue a infinito antes de reconstruir el camino.",
            "La línea --- se escribe siempre al acabar el caso."])
    prueba("Camino de varios tramos, completo y en orden", "trampa",
           [(5, [(4, 1, 2), (3, 2, 10), (1, 5, 4), (2, 4, 3)], [(2, 5)])],
           "El camino 2 -> 4 -> 1 -> 5 debe escribirse del origen al destino, con los dos extremos y numerado desde 1.",
           {"wa": "El camino sale mal escrito: al revés (del destino al origen), sin el origen o sin el destino, o con los puntos numerados desde 0."},
           ["Debe salir «9: 2 -> 4 -> 1 -> 5».",
            "ulti[] te da el camino hacia atrás: mételo por delante (push_front en un deque) o dale la vuelta al final.",
            "El bucle «for (v = destino; v != origen; v = ulti[v])» no añade el origen: añádelo después. Y suma 1 a cada punto al escribirlo."])
    prueba("Tramos de doble sentido", "trampa", [(3, [(2, 1, 4), (3, 2, 4)], [(1, 3)])],
           "Los tramos vienen escritos «hacia atrás» (2 1 y 3 2): se recorren en los dos sentidos.",
           {"wa": "Solo añades cada tramo en un sentido. Las calles son de doble sentido: pon las dos aristas, u → v y v → u."},
           ["Debe salir «8: 1 -> 2 -> 3».",
            "Por cada tramo llama dos veces a ponArista."])
    prueba("Varios pedidos desde distintos orígenes", "trampa",
           [(6, [(1, 2, 2), (2, 3, 2), (3, 4, 2), (4, 5, 2), (5, 6, 2), (1, 6, 7)], [(1, 4), (6, 3), (4, 1), (5, 2)])],
           "Cuatro pedidos en el mismo caso, cada uno desde un origen distinto: cada uno empieza de cero.",
           {"wa": "El primer pedido sale bien y los siguientes no: las distancias o ulti[] del pedido anterior se quedan. Hay que hacer un Dijkstra nuevo (con vectores nuevos) por cada pedido.",
            "tle": "La reconstrucción del camino entra en un bucle: ulti[] tiene restos del pedido anterior. Crea dist y ulti de nuevo en cada pedido.",
            "mle": "La reconstrucción del camino no termina y llena la memoria: ulti[] tiene restos del pedido anterior y forma un ciclo. Crea dist y ulti de nuevo en cada pedido.",
            "rte": "La reconstrucción del camino se sale del vector: ulti[] tiene restos del pedido anterior."},
           ["Si el primer pedido sale bien y el segundo no, mira qué se reutiliza entre pedidos.",
            "Declara dist, ulti y la cola dentro del bucle de los pedidos."])
    prueba("El camino con menos tramos no es el más rápido", "trampa",
           [(5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (1, 5, 10), (5, 4, 10)], [(1, 4)])],
           "1 -> 5 -> 4 tiene dos tramos pero tarda 20; 1 -> 2 -> 3 -> 4 tarda 3.",
           {"wa": "Buscas el camino con menos tramos (anchura). Hay que minimizar el tiempo: Dijkstra con los minutos de cada tramo."},
           ["Debe salir «3: 1 -> 2 -> 3 -> 4».",
            "Un BFS solo sirve si todos los tramos tardan lo mismo."])
    prueba("Mejorar el camino de un punto ya alcanzado", "trampa",
           [(4, [(1, 3, 10), (1, 2, 1), (2, 3, 1), (3, 4, 1)], [(1, 4)])],
           "Al punto 3 se llega primero directamente (10) y luego por el 2 (2): su «último tramo» debe cambiar.",
           {"wa": "El tiempo sale bien pero el camino no: cuando mejoras dist[w] también hay que actualizar ulti[w] (por dónde se llega)."},
           ["Debe salir «3: 1 -> 2 -> 3 -> 4».",
            "En la relajación, si mejora, actualiza a la vez dist[w], ulti[w] y la prioridad de w."])
    prueba("No parar al descubrir el destino", "trampa",
           [(4, [(1, 2, 1), (2, 4, 1), (1, 4, 5), (3, 4, 7)], [(1, 4)])],
           "La primera vez que se llega al destino es por el tramo directo (5), pero pasando por el 2 se tarda 2.",
           {"wa": "Paras en cuanto el destino recibe una distancia, pero aún puede mejorar. Solo es definitiva cuando el destino sale de la cola."},
           ["Debe salir «2: 1 -> 2 -> 4».",
            "Puedes parar al SACAR el destino de la cola (pq.top()), no al relajar un tramo que llega a él."])
    prueba("Varios tramos entre los mismos puntos", "trampa",
           [(3, [(1, 2, 10), (2, 3, 4), (2, 1, 3), (1, 3, 9)], [(1, 3)])],
           "Entre 1 y 2 hay dos tramos (10 y 3): hay que usar el más rápido, aunque venga después.",
           {"wa": "Te quedas con un solo tramo entre dos puntos (el primero o el último que lees). Todos cuentan: guarda todas las aristas, Dijkstra elige solo la mejor."},
           ["Debe salir «7: 1 -> 2 -> 3».",
            "No compruebes si ya existe la arista antes de añadirla, ni uses una matriz que se sobrescribe."])
    prueba("NO LLEGA entre otros pedidos", "trampa",
           [(5, [(1, 2, 3), (3, 4, 1), (4, 5, 1)], [(2, 1), (1, 5), (5, 3)])],
           "Un pedido imposible en medio de otros: los demás deben salir bien y --- solo al final.",
           {"wa": "Tras un NO LLEGA algo se descoloca: revisa que no escribes --- después de cada pedido ni te saltas la lectura de los siguientes."},
           ["Debe salir «3: 2 -> 1», «NO LLEGA», «2: 5 -> 4 -> 3» y ---.",
            "El --- va una vez por caso, después del bucle de los pedidos."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio(r, 9, 16, 3), ej2, (3, [(1, 2, 1), (2, 3, 1)], [(3, 1)]), aleatorio(r, 5, 6, 2),
            (2, [(2, 1, 500)], [(2, 1)])],
           "Un caso con varios pedidos seguido de otros más pequeños: nada de un caso debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: el grafo, las distancias o ulti[] no se crean de nuevo en cada caso.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: créalas dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo dentro de resuelveCaso y dist/ulti dentro del bucle de pedidos."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(2, 9), r.randint(0, 16), r.randint(1, 4), maxt=r.choice([20, 500])) for _ in range(50)],
           "50 casos pequeños al azar (con tramos repetidos y pedidos que no llegan).",
           {"wa": "Hay algún pedido que no tratas bien: busca qué caso es contando las líneas --- y prueba ese grafo a mano.",
            "rte": "Algún caso pequeño rompe el programa: revisa los índices y la reconstrucción del camino."},
           ["Cada caso termina en ---: así localizas el caso que falla.",
            "Dibuja ese grafo y sigue Dijkstra a mano anotando dist y ulti."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, r.randint(20, 60), r.randint(30, 150), 10) for _ in range(15)],
           "15 casos de 20 a 60 puntos con 10 pedidos cada uno: caminos más largos.",
           {"wa": "Con caminos más largos algo falla: revisa la reconstrucción con ulti[] y que se actualiza al mejorar."},
           ["Busca el pedido que falla y compara tu camino con el esperado: ¿cuál es más rápido?",
            "Si tu tiempo es correcto pero el camino no, el problema está en ulti[]."])
    prueba("Grande: 20.000 puntos y 100.000 tramos", "rendimiento", [grande(r, 20000, 100000, 10)],
           "El tamaño máximo con 10 pedidos a destinos lejanos: un Dijkstra por pedido.",
           {"tle": "Demasiado lento: cada pedido necesita un Dijkstra O(C log N) con IndexPQ. Si buscas el mínimo recorriendo el vector (O(N²)), con 20.000 puntos y 10 pedidos no llega.",
            "mle": "Gastas demasiada memoria: no uses una matriz N×N; usa DigrafoValorado (listas de adyacencia).",
            "wa": "Solo falla en el grande: revisa el valor de infinito y los tramos repetidos."},
           ["Usa una IndexPQ para elegir el siguiente punto, no un recorrido de todo el vector.",
            "Construye el grafo una vez por caso y haz un Dijkstra por pedido."])
    prueba("Caminos de 20.000 puntos", "rendimiento", [cadena_larga(r, 20000)],
           "10 pedidos cuyo camino pasa por los 20.000 puntos: la reconstrucción y la escritura deben ser lineales.",
           {"tle": "Reconstruyes o escribes el camino en tiempo cuadrático: por ejemplo, concatenando por delante en un string (s = x + \" -> \" + s copia todo cada vez). Usa un deque/vector y escribe al final.",
            "wa": "Con caminos tan largos algo se corta: revisa la reconstrucción con ulti[].",
            "rte": "¿Reconstruyes el camino con recursión? Con 20.000 niveles puede bastar, pero revisa que no haya bucles en ulti[]."},
           ["Cuenta cuántas operaciones hace tu reconstrucción para un camino de L puntos.",
            "Guarda los puntos en un deque (push_front) o en un vector que luego recorres al revés, y escribe con cout directamente."])

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
           "            for (int u = 0; u < N; ++u) if (!hecho[u] && dist[u] != INF && (v == -1 || dist[u] < dist[v])) v = u;\n"
           "            if (v == -1) break;\n            hecho[v] = true;\n")

VARIANTES = [
    Variante("tramos de un solo sentido", [("        g.ponArista({v, u, t});\n", "")], prueba=5, v="wa"),
    Variante("camino al revés", [("camino.push_front(v);", "camino.push_back(v);"),
                                 ("camino.push_front(origen);", "camino.push_back(origen);")], prueba=4, v="wa"),
    Variante("falta el origen en el camino", [("            camino.push_front(origen);\n", "")], prueba=4, v="wa"),
    Variante("escribe los puntos desde 0", [("<< camino[i] + 1;", "<< camino[i];")], prueba=4, v="wa"),
    Variante("dist y ulti compartidos entre pedidos",
             [("        vector<int> dist(N, INF);\n        vector<int> ulti(N, -1);          // vertice anterior en el camino minimo\n", ""),
              ("    int K; cin >> K;\n", "    int K; cin >> K;\n    vector<int> dist(N, INF);\n    vector<int> ulti(N, -1);\n")],
             prueba=6, v="mle"),
    Variante("elige el camino con menos tramos (anchura)",
             [("vector<int> ulti(N, -1);          // vertice anterior en el camino minimo\n",
               "vector<int> ulti(N, -1);\n        vector<int> saltos(N, INF); saltos[origen] = 0;\n"),
              ("if (dist[w] > dist[v] + a.valor()) {", "if (saltos[w] > saltos[v] + 1) {\n                    saltos[w] = saltos[v] + 1;"),
              ("pq.update(w, dist[w]);", "pq.update(w, saltos[w]);")],
             prueba=7, v="wa"),
    Variante("no actualiza ulti al mejorar", [("ulti[w] = v;", "if (ulti[w] == -1) ulti[w] = v;")], prueba=8, v="wa"),
    Variante("para al descubrir el destino",
             [("                    pq.update(w, dist[w]);\n",
               "                    pq.update(w, dist[w]);\n                    if (w == destino) { while (!pq.empty()) pq.pop(); break; }\n")],
             prueba=9, v="wa"),
    Variante("solo el primer tramo entre dos puntos",
             [("        g.ponArista({u, v, t});\n        g.ponArista({v, u, t});\n",
               "        if (!g.hayArista(u, v)) { g.ponArista({u, v, t}); g.ponArista({v, u, t}); }\n")],
             prueba=10, v="wa"),
    Variante("Dijkstra buscando el mínimo en el vector (O(N²))",
             [("        while (!pq.empty()) {\n            int v = pq.top().elem; pq.pop();\n", _LINEAL)], prueba=15, v="tle"),
]
