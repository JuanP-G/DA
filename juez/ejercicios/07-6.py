"""07-6 · Repartiendo paquetes: juez con pruebas pensadas para cada error típico.

Dígrafo valorado (puede haber lazos y varias conexiones entre dos casas). El repartidor va de la
oficina a cada destino y vuelve; esfuerzo total = Σ (ida + vuelta) por paquete, o Imposible si
algún destino no se puede alcanzar o no se puede volver de él. Dos Dijkstra desde la oficina:
en el grafo y en el grafo inverso.
"""
import heapq
from _comun import Prueba, Variante, rng

CONFIG = {
    "solucion": "7-Digrafos valorados y caminos minimos/EJ_07-6/EJ_07-6.cpp",
    "cabeceras": ["7-Digrafos valorados y caminos minimos/EJ_07-6/DigrafoValorado.h",
                  "7-Digrafos valorados y caminos minimos/EJ_07-6/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["dijkstra(g.inverso(), oficina)", "dijkstra(g, oficina)"],
}

MAXE = 10_000


# ---------------------------------------------------------------- solucionador independiente
def dijkstra(N, ady, s):
    INF = float("inf")
    dist = [INF] * (N + 1)
    dist[s] = 0
    cola = [(0, s)]
    while cola:
        d, v = heapq.heappop(cola)
        if d > dist[v]:
            continue
        for w, e in ady[v]:
            if d + e < dist[w]:
                dist[w] = d + e
                heapq.heappush(cola, (d + e, w))
    return dist


def reparto(N, conexiones, O, destinos):
    """Esfuerzo total o None si es imposible."""
    ady = [[] for _ in range(N + 1)]
    inv = [[] for _ in range(N + 1)]
    for a, b, e in conexiones:
        ady[a].append((b, e))
        inv[b].append((a, e))
    ida, vuelta = dijkstra(N, ady, O), dijkstra(N, inv, O)
    total = 0
    for d in destinos:
        if ida[d] == float("inf") or vuelta[d] == float("inf"):
            return None
        total += ida[d] + vuelta[d]
    return total


def salida_caso(caso):
    r = reparto(*caso)
    return "Imposible\n" if r is None else f"{r}\n"


def valida(caso):
    N, conexiones, O, destinos = caso
    assert 1 <= N <= 100_000 and 1 <= len(conexiones) <= 200_000
    for a, b, e in conexiones:
        assert 1 <= a <= N and 1 <= b <= N and 1 <= e <= MAXE
    assert 1 <= O <= N and 1 <= len(destinos) <= N and all(1 <= d <= N for d in destinos)
    r = reparto(*caso)
    assert r is None or r <= 10 ** 9


def caso_a_texto(caso):
    N, conexiones, O, destinos = caso
    return (f"{N}\n{len(conexiones)}\n" + "".join(f"{a} {b} {e}\n" for a, b, e in conexiones)
            + f"{O} {len(destinos)}\n" + " ".join(map(str, destinos)) + "\n")


# ---------------------------------------------------------------- generadores
def aleatorio(r, N, C, P, maxe=MAXE, raros=0.0):
    """Dígrafo al azar; `raros` = probabilidad de lazo o de repetir una conexión anterior."""
    conexiones = []
    for _ in range(C):
        x = r.random()
        if conexiones and x < raros / 2:
            a, b, _e = r.choice(conexiones)
        elif x < raros:
            a = b = r.randint(1, N)
        else:
            a, b = r.randint(1, N), r.randint(1, N)
        conexiones.append((a, b, r.randint(1, maxe)))
    return (N, conexiones, r.randint(1, N), [r.randint(1, N) for _ in range(min(P, N))])


def aleatorio_posible(r, N, C, P, maxe):
    """Como aleatorio pero con un ciclo que recorre todas las casas: siempre es posible."""
    perm = list(range(1, N + 1))
    r.shuffle(perm)
    conexiones = [(perm[i], perm[(i + 1) % N], r.randint(1, maxe)) for i in range(N)] if N > 1 else [(1, 1, 1)]
    while len(conexiones) < C:
        conexiones.append((r.randint(1, N), r.randint(1, N), r.randint(1, maxe)))
    r.shuffle(conexiones)
    return (N, conexiones, r.randint(1, N), [r.randint(1, N) for _ in range(min(P, N))])


def cadena(N, e):
    """Casas en fila con conexiones en los dos sentidos; un paquete a la última casa."""
    conexiones = [(i, i + 1, e) for i in range(1, N)] + [(i + 1, i, e) for i in range(1, N)]
    rng(N).shuffle(conexiones)
    return (N, conexiones, 1, [N])


def grande(r, N, C, P):
    """Fuertemente conexo (un ciclo con esfuerzos altos) y muchas conexiones baratas."""
    perm = list(range(1, N + 1))
    r.shuffle(perm)
    conexiones = [(perm[i], perm[(i + 1) % N], MAXE) for i in range(N)]
    while len(conexiones) < C:
        conexiones.append((r.randint(1, N), r.randint(1, N), r.randint(1, 100)))
    r.shuffle(conexiones)
    return (N, conexiones, r.randint(1, N), [r.randint(1, N) for _ in range(min(P, N))])


# ---------------------------------------------------------------- pruebas
def pruebas():
    r = rng(76)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ej1 = (4, [(1, 2, 5), (2, 3, 2), (3, 1, 8), (1, 4, 2), (4, 1, 3)], 1, [2, 3, 4])
    ej2 = (4, [(1, 3, 2), (3, 1, 3), (3, 4, 5)], 1, [2, 3])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF: 35 e Imposible.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: cada paquete cuesta lo que cuesta ir de la oficina a la casa MÁS lo que cuesta volver, y la vuelta puede ir por otro camino.",
            "rte": "Error de ejecución con el ejemplo: las casas van del 1 al N (resta 1) y la entrada pone N y C en líneas distintas y luego «O P» y la lista de destinos."},
           ["En el primer caso: (5 + 10) + (7 + 8) + (2 + 3) = 35.",
            "La vuelta de la casa 2 no es 5: no hay conexión 2 → 1 y hay que pasar por la 3."])
    prueba("Una sola casa", "borde", [(1, [(1, 1, 5)], 1, [1])],
           "N = 1 con un lazo: el único paquete es para la propia oficina, esfuerzo 0.",
           {"wa": "Un paquete para la casa de la oficina no cuesta nada: ida y vuelta son 0 (el lazo no sirve de nada).",
            "rte": "Con una sola casa algo se sale del vector: revisa los índices desde 1."},
           ["Debe salir 0.",
            "La distancia de la oficina a sí misma es 0 en los dos Dijkstra."])
    prueba("Paquete para la propia oficina", "borde", [(3, [(1, 2, 4), (2, 1, 6), (3, 3, 2)], 1, [1, 2])],
           "Uno de los paquetes es para la casa de la oficina (cuesta 0); el otro, 4 + 6.",
           {"wa": "El paquete para la oficina no cuesta nada; la casa 3 (aislada salvo un lazo) no recibe paquetes, así que el reparto es posible: 10."},
           ["Debe salir 10.",
            "Solo importa que se pueda ir y volver de las casas que reciben paquetes."])
    prueba("Fila de 40.000 casas con esfuerzos máximos", "borde", [cadena(40_000, MAXE)],
           "Un solo paquete a la otra punta de una fila de 40.000 casas: 799.980.000.",
           {"wa": "El esfuerzo llega a casi 8·10⁸: revisa el valor de infinito (si es 10⁶ o 10⁷ la casa parece inalcanzable) y que no se desborda nada.",
            "tle": "Con 40.000 casas tu Dijkstra es demasiado lento: usa la IndexPQ.",
            "rte": "¿Una recursión de 40.000 niveles? Dijkstra con IndexPQ no la necesita."},
           ["Calcula a mano: 39.999 conexiones de 10.000 para ir y otras tantas para volver.",
            "Usa como infinito numeric_limits<int>::max() o, mejor, long long."])
    prueba("Conexiones de un solo sentido", "trampa", [(3, [(1, 2, 10), (2, 1, 10), (1, 3, 1), (2, 3, 1)], 1, [2])],
           "1 → 3 y 2 → 3 no permiten ir de 1 a 2 pasando por la 3: solo vale la conexión directa (10 + 10).",
           {"wa": "Recorres las conexiones en los dos sentidos. Cada conexión va solo de origen a destino; si se puede volver, viene otra línea."},
           ["Debe salir 20.",
            "Añade solo la arista origen → destino al DigrafoValorado."])
    prueba("La vuelta no es la ida al revés", "trampa", [(3, [(1, 2, 1), (2, 3, 1), (3, 1, 1)], 1, [2])],
           "Para ir a la casa 2 basta 1 → 2 (1), pero para volver hay que dar la vuelta 2 → 3 → 1 (2).",
           {"wa": "Calculas la vuelta igual que la ida (o la ida dos veces). El esfuerzo de volver de cada casa a la oficina es la distancia en el grafo INVERSO desde la oficina."},
           ["Debe salir 3.",
            "Ir de la casa d a la oficina en el grafo es lo mismo que ir de la oficina a d en el grafo con las aristas al revés.",
            "Un Dijkstra desde la oficina en g y otro en g.inverso(): ida[d] + vuelta[d]."])
    prueba("Se puede ir pero no volver: Imposible", "trampa", [(3, [(1, 2, 3), (2, 3, 1), (3, 2, 1)], 1, [3])],
           "La casa 3 es alcanzable desde la oficina, pero desde ella no se puede regresar.",
           {"wa": "Solo compruebas que se puede llegar. También hay que poder volver: si ida o vuelta es infinito, el reparto es Imposible (y no sumes infinitos: se desbordan)."},
           ["Debe salir Imposible.",
            "Comprueba los dos vectores (ida y vuelta) antes de sumar."])
    prueba("Varios paquetes para la misma casa", "trampa", [(3, [(1, 2, 2), (2, 1, 3), (3, 1, 7)], 1, [2, 2, 2])],
           "Tres paquetes para la casa 2: hay que hacer tres viajes de ida y vuelta.",
           {"wa": "Cuentas una sola vez las casas repetidas. La moto solo lleva un paquete: cada paquete es un viaje completo."},
           ["Debe salir 3 · (2 + 3) = 15.",
            "Suma ida[d] + vuelta[d] por cada número de la lista de destinos, aunque se repita."])
    prueba("Varias conexiones entre dos casas y lazos", "trampa",
           [(2, [(1, 2, 9), (2, 2, 1), (1, 2, 4), (2, 1, 5), (1, 1, 3), (2, 1, 2)], 1, [2])],
           "Entre 1 y 2 hay varias conexiones en cada sentido y lazos: hay que usar las más baratas (4 y 2).",
           {"wa": "Te quedas con una sola conexión entre dos casas (la primera o la última que lees). Guarda todas: Dijkstra elige la mejor."},
           ["Debe salir 6.",
            "No compruebes si ya existe la arista antes de añadirla ni uses una matriz que se sobrescribe."])
    prueba("La oficina no está en la casa 1", "trampa", [(3, [(3, 2, 1), (2, 3, 1), (1, 3, 5), (3, 1, 5)], 2, [3])],
           "La oficina está en la casa 2: todo se mide desde ahí.",
           {"wa": "Supones que la oficina es la casa 1. Su número viene en la línea «O P» después de las conexiones."},
           ["Debe salir 2.",
            "Lanza los dos Dijkstra desde O − 1."])
    prueba("Varios casos seguidos", "trampa",
           [aleatorio_posible(r, 8, 20, 4, 9), (3, [(1, 2, 1), (2, 3, 1), (3, 1, 1)], 2, [1]), ej1,
            aleatorio_posible(r, 5, 9, 2, 20), (1, [(1, 1, 1)], 1, [1])],
           "Varios repartos posibles seguidos: nada de un caso (el total, las distancias) debe quedar para el siguiente.",
           {"wa": "Algo se arrastra de un caso al siguiente: el total acumulado, la marca de imposible o las distancias no se reinician en cada caso.",
            "rte": "Usas en un caso una estructura con el tamaño de otro caso anterior: créalas dentro de resuelveCaso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso (o son static).",
            "El total empieza en 0 en cada caso."])
    prueba("Varios casos: un reparto imposible a mitad", "trampa",
           [(4, [(1, 2, 1), (2, 1, 1)], 1, [3, 2, 4]), (2, [(1, 2, 2), (2, 1, 2)], 2, [1, 1]), ej1],
           "El primer caso es imposible ya por el primer destino, pero hay que leer los demás destinos antes de pasar al siguiente caso.",
           {"wa": "Tras un Imposible el siguiente caso sale mal: dejas de leer la lista de destinos en cuanto encuentras uno imposible, y los que quedan se leen como si fueran el caso siguiente. Lee siempre los P destinos.",
            "rte": "Tras un Imposible el programa se rompe: dejas destinos sin leer y el caso siguiente lee esos números como N, C o conexiones (casas que no existen). Lee siempre los P destinos aunque ya sepas que es imposible."},
           ["El primer caso es Imposible; el segundo debe dar 8.",
            "No hagas return ni break dentro del bucle de lectura de destinos: marca que es imposible y sigue leyendo."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(1, 8), r.randint(1, 20), r.randint(1, 4), maxe=r.choice([5, 10000])) for _ in range(50)],
           "50 casos pequeños al azar (muchos imposibles).",
           {"wa": "Hay algún caso concreto que no tratas bien: la línea que falla es el número de caso; calcula a mano la ida y la vuelta de cada destino."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Dibuja el dígrafo con flechas: la vuelta usa las flechas en su sentido, desde la casa hasta la oficina."])
    prueba("Aleatorios con lazos y conexiones repetidas", "aleatorio",
           [aleatorio_posible(r, r.randint(2, 10), r.randint(10, 30), r.randint(1, 6), 30) for _ in range(20)]
           + [aleatorio(r, r.randint(2, 6), r.randint(5, 20), r.randint(1, 5), maxe=9, raros=0.4) for _ in range(20)],
           "40 casos con lazos, conexiones repetidas y destinos repetidos.",
           {"wa": "Algún caso con lazos, conexiones repetidas o destinos repetidos falla: guarda todas las aristas y cuenta cada paquete."},
           ["Busca el caso que falla.",
            "Los lazos no estorban a Dijkstra; las conexiones repetidas tampoco si las guardas todas."])
    prueba("Grande: 30.000 casas y 30.000 paquetes", "rendimiento", [grande(r, 30_000, 120_000, 30_000)],
           "Un caso grande con un paquete para casi cada casa.",
           {"tle": "Haces un Dijkstra por cada paquete (por ejemplo, desde cada casa hasta la oficina para la vuelta). Basta con dos: uno desde la oficina en el grafo y otro en el grafo inverso.",
            "mle": "Gastas demasiada memoria: no guardes las distancias de cada casa por separado.",
            "wa": "Solo falla en el grande: revisa los desbordamientos al sumar."},
           ["¿Cuántos Dijkstra haces? Deberían ser exactamente dos.",
            "La vuelta de TODAS las casas a la oficina sale de un único Dijkstra desde la oficina en g.inverso()."])

    out = []
    for nombre, tipo, casos, comprueba, si, pistas in P:
        for c in casos:
            valida(c)
        out.append(Prueba(nombre, tipo,
                          entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                          salida="".join(salida_caso(c) for c in casos),
                          casos=len(casos), comprueba=comprueba, si=si, pistas=pistas))
    return out


VARIANTES = [
    Variante("conexiones en los dos sentidos",
             [("g.ponArista({u - 1, v - 1, e});", "g.ponArista({u - 1, v - 1, e}); g.ponArista({v - 1, u - 1, e});")], prueba=5, v="wa"),
    Variante("la vuelta calculada como la ida", [("dijkstra(g.inverso(), oficina)", "dijkstra(g, oficina)")], prueba=6, v="wa"),
    Variante("solo comprueba que se puede ir",
             [("if (ida[d] == INF || vuelta[d] == INF)", "if (ida[d] == INF)")], prueba=7, v="wa"),
    Variante("cuenta una vez las casas repetidas",
             [("    while (P--) {\n        int d; cin >> d; --d;\n",
               "    vector<bool> visto(N, false);\n    while (P--) {\n        int d; cin >> d; --d;\n        if (visto[d]) continue;\n        visto[d] = true;\n")],
             prueba=8, v="wa"),
    Variante("solo la primera conexión entre dos casas",
             [("g.ponArista({u - 1, v - 1, e});", "if (!g.hayArista(u - 1, v - 1)) g.ponArista({u - 1, v - 1, e});")], prueba=9, v="wa"),
    Variante("supone la oficina en la casa 1", [("--oficina;", "oficina = 0;")], prueba=10, v="wa"),
    Variante("total no reiniciado entre casos (static)", [("long long total = 0;", "static long long total = 0;")], prueba=11, v="wa"),
    Variante("deja de leer destinos al ver un imposible",
             [("if (ida[d] == INF || vuelta[d] == INF) posible = false;",
               "if (ida[d] == INF || vuelta[d] == INF) { cout << \"Imposible\\n\"; return; }")], prueba=12, v="rte"),
    Variante("infinito demasiado pequeño (10⁶)",
             [("const long long INF = numeric_limits<long long>::max();", "const long long INF = 1000000;")], prueba=4, v="wa"),
    Variante("un Dijkstra por paquete para la vuelta",
             [("if (ida[d] == INF || vuelta[d] == INF) posible = false;\n        else total += ida[d] + vuelta[d];",
               "long long vd = dijkstra(g, d)[oficina];\n        if (ida[d] == INF || vd == INF) posible = false;\n        else total += ida[d] + vd;")],
             prueba=15, v="tle"),
]
