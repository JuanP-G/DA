"""06-2 · Camiones de reparto: juez con pruebas pensadas para cada error típico.

Cada caso: V (línea), E (línea), E calles «u v anchura», K y K consultas «origen destino anchura».
Salida: una línea por consulta, SI si hay un camino con todas las calles de anchura ≥ la del camión.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-2/EJ_06-2.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-2/GrafoValorado.h"],
    "limite_ms": 3000,
    "fallo": ["if (a.valor() >= ancho && !visitado[w]) dfs(g, w);", "if (a.valor() > ancho && !visitado[w]) dfs(g, w);"],
}


def resuelve(V, calles, consultas):
    """Solucionador independiente: BFS desde el origen por las calles lo bastante anchas."""
    ady = [[] for _ in range(V + 1)]
    for u, v, a in calles:
        ady[u].append((v, a))
        ady[v].append((u, a))
    res = []
    for o, d, a in consultas:
        visto = bytearray(V + 1)
        visto[o] = 1
        cola = deque([o])
        while cola:
            x = cola.popleft()
            for y, b in ady[x]:
                if b >= a and not visto[y]:
                    visto[y] = 1
                    cola.append(y)
        res.append("SI" if visto[d] else "NO")
    return "".join(r + "\n" for r in res)


def caso_a_texto(V, calles, consultas):
    return (f"{V}\n{len(calles)}\n" + "".join(f"{u} {v} {a}\n" for u, v, a in calles)
            + f"{len(consultas)}\n" + "".join(f"{o} {d} {a}\n" for o, d, a in consultas))


def consulta_al(rng, V, anchos):
    o = rng.randint(1, V)
    d = rng.randint(1, V - 1)
    if d >= o:
        d += 1
    return (o, d, rng.choice(anchos) + rng.choice([-1, 0, 0, 1]) if anchos else rng.randint(1, 20))


def aleatorio(rng, V, E, amax):
    calles = []
    for _ in range(E):
        u = rng.randint(1, V)
        v = rng.randint(1, V - 1)
        if v >= u:
            v += 1
        calles.append((u, v, rng.randint(1, amax)))
    anchos = [a for _, _, a in calles]
    consultas = []
    for _ in range(rng.randint(1, 10)):
        o, d, a = consulta_al(rng, V, anchos)
        consultas.append((o, d, max(1, min(1000000, a))))
    return V, calles, consultas


def grande(rng):
    V, E = 10000, 100000
    calles = []
    for _ in range(E):
        u = rng.randint(1, V)
        v = rng.randint(1, V - 1)
        if v >= u:
            v += 1
        calles.append((u, v, rng.randint(1, 1000000)))
    consultas = [(rng.randint(1, 5000), rng.randint(5001, V), rng.choice([300000, 450000, 500000, 550000, 600000, 700000, 900000]))
                 for _ in range(10)]
    return V, calles, consultas


def cadena(rng):
    """Una única calle larga 1 - 2 - ... - V (desordenada): el DFS baja 10.000 niveles."""
    V = 10000
    calles = [(i, i + 1, 500000 + rng.randint(0, 1000)) for i in range(1, V)]
    calles[V // 2] = (V // 2 + 1, V // 2 + 2, 499999)          # el cuello de botella
    rng.shuffle(calles)
    consultas = [(1, V, 500000), (V, 1, 499999), (1, V // 2 + 1, 500000), (V, V // 2 + 2, 500000),
                 (1, V, 1), (V // 2 + 2, V // 2 + 1, 500000), (V // 2 + 2, V // 2 + 1, 499999),
                 (2, V - 1, 1000000), (3, V, 499000), (1, 2, 500001)]
    return V, calles, consultas


def pruebas():
    rng = random.Random(62)
    ejemplo = (5, [(1, 2, 10), (1, 3, 30), (2, 4, 20), (3, 4, 15), (4, 5, 12)],
               [(1, 5, 8), (1, 4, 12), (1, 4, 15), (2, 5, 15)])
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado", [ejemplo],
           "El ejemplo del PDF: una ciudad con 5 intersecciones y 4 consultas («SI SI SI NO», una por línea).",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (V y E van en líneas distintas), la comparación de anchuras o el texto («SI» y «NO», en mayúsculas y sin tilde).",
            "pe": "Las respuestas están bien pero el formato no: cada consulta va en su propia línea."},
           ["Ejecútalo en tu ordenador con el ejemplo y compara línea a línea.",
            "Escribe exactamente «SI» o «NO» (sin tilde), una línea por consulta.",
            "Lee el grafo, luego K y después las K consultas; responde cada una al leerla."])
    # --- Trampas. El orden importa: las primeras no deben fallar por los errores que buscan las siguientes.
    prueba("Intersecciones numeradas desde 1", "trampa",
           [(3, [(3, 1, 7), (2, 3, 4)], [(1, 3, 8), (3, 1, 5)])],
           "Consultas que salen de la intersección V y llegan a la 1: hay que pasar de 1..V a 0..V−1 en las calles Y en las consultas.",
           {"rte": "Usas el número de intersección tal cual en algún sitio (en las calles o en las consultas): la intersección V se sale del grafo. Resta 1 también al origen y al destino.",
            "wa": "El origen o el destino caen en otra intersección: resta 1 a los dos, igual que a los extremos de las calles."},
           ["La consulta «3 1 5» sale de la última intersección: ¿existe el vértice 3 en tu grafo?",
            "Si lees el grafo con GrafoValorado<int>(cin, 1), los vértices van de 0 a V − 1: resta 1 también al origen y al destino de cada consulta."])
    prueba("No basta con la calle directa", "trampa",
           [(4, [(1, 4, 3), (1, 2, 9), (2, 3, 9), (3, 4, 9)], [(1, 4, 8), (4, 1, 3), (1, 3, 9), (2, 4, 9)])],
           "El camión puede pasar por cualquier número de intersecciones: la calle directa es estrecha, pero el rodeo no.",
           {"wa": "Solo miras las calles que salen del origen (o un paso de recorrido). Hay que hacer un recorrido completo (DFS o BFS) por las calles lo bastante anchas."},
           ["En el primer caso la calle 1–4 es estrecha (3), pero 1–2–3–4 admite anchura 9: SI.",
            "Haz un DFS o BFS desde el origen que solo cruce calles con anchura ≥ la del camión y mira si llega al destino."])
    prueba("Varias consultas en la misma ciudad", "trampa",
           [(4, [(1, 2, 10), (2, 3, 10), (3, 4, 5)], [(1, 4, 4), (1, 4, 6), (1, 3, 8), (1, 4, 9), (2, 1, 11)])],
           "Cada consulta es independiente: lo visitado en la anterior no vale para la siguiente.",
           {"wa": "Reutilizas el vector de visitados de una consulta a otra: tras una consulta que llega a todas partes, las siguientes dicen SI aunque su camión sea más ancho. Crea los visitados de nuevo en cada consulta."},
           ["Tras «1 4 4» (SI), la consulta «1 4 6» debe dar NO: la calle 3–4 solo admite anchura 5.",
            "¿Dónde creas el vector de visitados? Debe empezar todo a false en cada consulta."])
    prueba("Calle justo de la anchura del camión", "trampa",
           [(2, [(1, 2, 15)], [(1, 2, 15), (2, 1, 16), (1, 2, 14)]), (3, [(1, 2, 7), (2, 3, 9)], [(3, 1, 7), (1, 3, 8)])],
           "La anchura de una calle es la MÁXIMA del camión que pasa: un camión de anchura 15 cabe por una calle de 15.",
           {"wa": "Comparas con > en vez de ≥: un camión exactamente igual de ancho que la calle sí pasa."},
           ["Con una calle de anchura 15, un camión de anchura 15 puede pasar: la respuesta es SI.",
            "La condición para usar una calle es anchura_calle ≥ anchura_camión."])
    prueba("Las calles son de doble sentido", "trampa",
           [(4, [(2, 1, 10), (3, 2, 10), (4, 3, 5)], [(1, 3, 10), (4, 1, 5), (1, 4, 3), (2, 4, 1)])],
           "Las calles se escriben «u v», pero se pueden recorrer de v a u.",
           {"wa": "Tratas las calles como de un solo sentido: solo vas de u a v. Cada calle debe estar en la lista de adyacentes de sus DOS extremos (o usa a.otro(v))."},
           ["La calle «2 1» sirve para ir de 1 a 2.",
            "Con GrafoValorado, recorre g.ady(v) y usa w = a.otro(v): da el otro extremo sea cual sea el orden en que se escribió."])
    prueba("Varias calles entre las mismas intersecciones", "trampa",
           [(2, [(1, 2, 20), (1, 2, 5)], [(1, 2, 10)]), (2, [(1, 2, 5), (2, 1, 20)], [(2, 1, 10)]), (3, [(1, 2, 8), (2, 3, 2), (3, 2, 9), (1, 2, 1)], [(1, 3, 8), (1, 3, 10)])],
           "Puede haber varias calles entre el mismo par de intersecciones, cada una con su anchura: basta con que una sea lo bastante ancha.",
           {"wa": "Guardas una sola calle por par de intersecciones (la primera o la última que lees). Hay que guardarlas todas (listas de adyacencia) o quedarse con la más ancha."},
           ["En el primer caso hay una calle 1–2 de anchura 20 y otra de 5: un camión de 10 pasa por la de 20.",
            "Si usas una matriz o un mapa por pares, no sobrescribas: quédate con el máximo. Más sencillo: listas de adyacencia, donde caben todas."])
    prueba("Un camino es tan ancho como su calle más estrecha", "trampa",
           [(4, [(1, 2, 100), (2, 3, 1), (3, 4, 100)], [(1, 4, 50), (1, 4, 1)]), (3, [(1, 2, 3), (2, 3, 30)], [(3, 1, 10), (2, 3, 30)])],
           "Una sola calle estrecha corta el camino, aunque las demás sean anchísimas.",
           {"wa": "No compruebas la anchura de TODAS las calles del camino: basta una demasiado estrecha para que el camión no pueda pasar por ahí."},
           ["En el primer caso, la calle 2–3 de anchura 1 impide que un camión de 50 vaya de 1 a 4.",
            "La condición de anchura se comprueba en cada calle que cruza el recorrido, no solo en la primera o la última."])
    prueba("Destino en otra parte de la ciudad", "trampa",
           [(6, [(1, 2, 50), (2, 3, 50), (4, 5, 50), (5, 6, 50)], [(1, 6, 1), (4, 6, 50), (3, 4, 2)])],
           "Intersecciones que no están unidas por ninguna calle: ningún camión puede ir de una a otra.",
           {"wa": "Respondes SI aunque no haya ningún camino: revisa que miras si el DESTINO concreto ha quedado visitado."},
           ["La intersección 1 y la 6 no están unidas por ninguna sucesión de calles: NO, aunque el camión mida 1.",
            "Tras el recorrido desde el origen, la respuesta es visitado[destino]."])
    prueba("Ciudad sin calles (E = 0)", "borde",
           [(2, [], [(1, 2, 1)]), (5, [], [(5, 1, 1000000), (2, 3, 1)])],
           "Sin calles no se puede ir a ningún sitio: todo NO.",
           {"wa": "Con E = 0 todas las respuestas son NO.",
            "rte": "Con E = 0 algo se rompe: revisa la lectura (después de E viene directamente K)."},
           ["Tras la línea con E = 0 viene directamente K.",
            "Sin calles, el recorrido desde el origen solo visita el origen."])
    prueba("Anchuras extremas (1 y 1.000.000)", "borde",
           [(3, [(1, 2, 1000000), (2, 3, 1)], [(1, 2, 1000000), (1, 3, 1), (1, 3, 2), (3, 2, 1000000)])],
           "Calles y camiones de anchura 1 y 1.000.000.",
           {"wa": "Con los valores extremos algo falla: ¿inicializas algún mínimo o máximo con un valor que no llega a 1.000.000?"},
           ["Un camión de 1.000.000 pasa por una calle de 1.000.000.",
            "Si guardas «la mayor anchura posible» empieza en un valor mayor que 1.000.000 (o en INT_MAX)."])
    prueba("Varios casos seguidos", "trampa",
           [(6, [(1, 2, 9), (2, 3, 9), (3, 4, 9), (4, 5, 9), (5, 6, 9)], [(1, 6, 9)]),
            (6, [(1, 2, 9)], [(1, 6, 9), (3, 4, 1)]),
            (3, [(2, 3, 4)], [(1, 3, 4), (2, 3, 4)]),
            (2, [], [(1, 2, 1)])],
           "Una ciudad grande seguida de otras pequeñas: nada de la anterior debe quedar (ni calles ni visitados).",
           {"wa": "Algo se arrastra de un caso al siguiente: el grafo o los visitados se crean fuera de resuelveCaso (o en un vector global que no se vacía).",
            "rte": "Un vector de un caso anterior con otro tamaño: crea el grafo y los visitados en cada caso con el V de ese caso."},
           ["Si la primera ciudad sale bien y las siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo dentro de resuelveCaso y los visitados dentro de cada consulta."])
    casos_al = [aleatorio(rng, rng.randint(2, 8), rng.randint(0, 12), rng.choice([5, 20])) for _ in range(80)]
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "80 ciudades pequeñas al azar, con calles repetidas y anchuras que empatan.",
           {"wa": "Hay alguna consulta concreta que no tratas: cuenta en qué línea falla para saber qué consulta es y síguela a mano."},
           ["Cada línea de la salida es una consulta: localiza la que falla en la entrada.",
            "Dibuja esa ciudad y marca solo las calles con anchura ≥ la del camión."])
    prueba("Ciudad grande al azar (10.000 intersecciones, 100.000 calles)", "rendimiento", [grande(rng)],
           "El tamaño máximo: 10 consultas, cada una con un recorrido de coste O(V + E).",
           {"tle": "Cada consulta debe costar O(V + E). ¿Copias el grafo al llamar a una función (pásalo por referencia const&) o repites el recorrido más de una vez por consulta?",
            "mle": "Gastas demasiada memoria: con V = 10.000, una matriz de adyacencia V × V ocupa cientos de MB (usa listas de adyacencia, GrafoValorado), o copias el grafo en cada llamada recursiva (pásalo por referencia const&)."},
           ["Pasa el grafo por referencia (GrafoValorado<int> const& g) a las funciones recursivas.",
            "No uses una matriz V × V: con 10.000 intersecciones son 10⁸ casillas.",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    prueba("Calle larga de 10.000 intersecciones", "rendimiento", [cadena(rng)],
           "Las intersecciones forman una sola cadena: el recorrido baja 10.000 niveles y el cuello de botella está en medio.",
           {"tle": "Algo se repite de más en cada paso del recorrido: ¿copias el grafo o el vector de visitados en cada llamada?",
            "mle": "Cada nivel de la recursión ocupa demasiado: si pasas el grafo por valor, se copia en cada una de las 10.000 llamadas. Pásalo por referencia const&.",
            "rte": "La recursión baja 10.000 niveles: no debería romperse, pero no declares vectores grandes dentro de la función recursiva.",
            "wa": "En una cadena larga falla el filtro: la calle del medio tiene anchura 499.999."},
           ["Pasa el grafo y los visitados por referencia a la función recursiva.",
            "Si tu DFS es iterativo con una pila, marca visitado al apilar."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(*c) for c in casos),
                   salida="".join(resuelve(*c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("no resta 1 en las consultas", [("Alcanzables a(g, origen - 1, ancho);", "Alcanzables a(g, origen, ancho);"),
                                             ("a.alcanzable(destino - 1)", "a.alcanzable(destino)")], prueba=2, v="rte"),
    Variante("solo mira las calles que salen del origen", [("if (a.valor() >= ancho && !visitado[w]) dfs(g, w);", "if (a.valor() >= ancho && !visitado[w]) visitado[w] = true;")], prueba=3, v="wa"),
    Variante("visitados compartidos entre consultas", [(": visitado(g.V(), false), ancho(ancho) {", ": ancho(ancho) {\n        if (visitado.empty()) visitado.assign(10000, false);"),
                                                        ("    vector<bool> visitado;\n    int ancho;", "    static vector<bool> visitado;\n    int ancho;"),
                                                        ("};\n\nvoid resuelveCaso() {", "};\nvector<bool> Alcanzables::visitado;\n\nvoid resuelveCaso() {")], prueba=4, v="wa"),
    Variante("> en vez de ≥", [("if (a.valor() >= ancho && !visitado[w]) dfs(g, w);", "if (a.valor() > ancho && !visitado[w]) dfs(g, w);")], prueba=5, v="wa"),
    Variante("calles de un solo sentido", [("int w = a.otro(v);", "if (a.uno() != v) continue;\n            int w = a.otro(v);")], prueba=6, v="wa"),
    Variante("matriz de adyacencia V × V", [("GrafoValorado<int> g(cin, 1);   // V, E y E calles; intersecciones numeradas desde 1",
                                             "GrafoValorado<int> g(cin, 1);\n    vector<vector<int>> mat(g.V(), vector<int>(g.V(), 0));\n    for (auto const& a : g.aristas()) { int u = a.uno(), w = a.otro(u); mat[u][w] = mat[w][u] = max(mat[u][w], a.valor()); }")],
             prueba=14, v="mle"),
    Variante("copia el grafo en cada llamada", [("void dfs(GrafoValorado<int> const& g, int v) {", "void dfs(GrafoValorado<int> g, int v) {")], prueba=14, v="mle"),
    Variante("todas las respuestas en una línea", [("cout << (a.alcanzable(destino - 1) ? \"SI\" : \"NO\") << '\\n';",
                                                    "cout << (a.alcanzable(destino - 1) ? \"SI\" : \"NO\") << (k ? ' ' : '\\n');")], prueba=1, v="pe"),
]
