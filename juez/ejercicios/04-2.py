"""04-2 · Los amigos de mis amigos son mis amigos: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso «N M» (1 ≤ N ≤ 20.000, 0 ≤ M ≤ 200.000) y M parejas «A B»
(1 ≤ A, B ≤ N, A ≠ B), que pueden repetirse y en cualquier orden. Salida: tamaño del mayor grupo
de amigos (la mayor componente conexa), uno por línea.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-2/EJ_04-2.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-2/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["maxim = max(maxim, tam);", "maxim = max(maxim, tam - 1);"],
}


# ---------------------------------------------------------------- solucionador independiente
def mayor_grupo(N, parejas):
    """BFS iterativo por cada persona sin grupo (personas de 1 a N)."""
    ady = [[] for _ in range(N + 1)]
    for a, b in parejas:
        ady[a].append(b)
        ady[b].append(a)
    visto = [False] * (N + 1)
    mejor = 0
    for s in range(1, N + 1):
        if not visto[s]:
            visto[s] = True
            cola, tam = deque([s]), 0
            while cola:
                v = cola.popleft()
                tam += 1
                for w in ady[v]:
                    if not visto[w]:
                        visto[w] = True
                        cola.append(w)
            mejor = max(mejor, tam)
    return mejor


def caso_a_texto(caso):
    N, parejas = caso
    return f"{N} {len(parejas)}\n" + "".join(f"{a} {b}\n" for a, b in parejas)


# ---------------------------------------------------------------- generadores
def aleatorio_pequeno(rng):
    N = rng.randint(1, 10)
    M = rng.randint(0, 12) if N > 1 else 0
    parejas = []
    for _ in range(M):
        a, b = rng.sample(range(1, N + 1), 2)
        parejas.append((a, b))
    if parejas and rng.random() < .4:            # alguna repetida, a veces al revés
        a, b = rng.choice(parejas)
        parejas.insert(rng.randrange(len(parejas) + 1), (b, a) if rng.random() < .5 else (a, b))
    return (N, parejas)


def grupos_grandes(rng, N, M):
    """Personas repartidas en grupos de tamaños muy distintos; M amistades (con repeticiones)."""
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    grupos, i = [], 0
    while i < N:
        t = min(N - i, rng.choice([1, 1, 2, 5, 50, 500, 3000, 6000]))
        grupos.append(perm[i:i + t])
        i += t
    parejas = []
    for g in grupos:                              # un árbol por grupo para que quede unido
        for k in range(1, len(g)):
            parejas.append((g[k], g[rng.randrange(k)]))
    grandes = [g for g in grupos if len(g) > 1]
    while len(parejas) < M:
        g = rng.choice(grandes)
        a, b = rng.sample(g, 2)
        parejas.append((a, b))
    rng.shuffle(parejas)
    return (N, parejas[:M])


def pruebas():
    rng = random.Random(42)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ejemplo = [(3, [(1, 2), (2, 3)]),
               (10, [(1, 2), (3, 1), (3, 4), (5, 4), (3, 5), (4, 6), (5, 2), (7, 10), (9, 10), (8, 9)]),
               (7, [(1, 2), (2, 3), (3, 2), (6, 7)])]
    prueba("Ejemplo del enunciado", "enunciado", ejemplo,
           "Los tres casos del PDF, con una pareja repetida al revés y personas sin amigos.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: que las personas van de 1 a N, que escribes un número por línea y que un grupo es una componente conexa entera (no solo los amigos directos).",
            "pe": "Los números están bien pero el formato no: un número por línea, sin texto extra."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "En el primer caso, 1 y 3 no son amigos directos, pero sí por medio de 2: el grupo tiene 3 personas.",
            "Un grupo de amigos es una componente conexa del grafo: haz un recorrido (DFS o BFS) desde cada persona sin visitar."])
    prueba("Una sola persona", "borde", [(1, [])],
           "N = 1 y ninguna amistad: el mayor grupo es esa persona sola (1).",
           {"wa": "Una persona sin amigos forma su propio grupo de tamaño 1. Si sale 0, solo cuentas grupos que tienen alguna amistad, o el máximo no se actualiza con el último grupo.",
            "rte": "Con N = 1 solo existe la persona 1 (vértice 0): revisa los índices del vector."},
           ["¿Qué escribe tu programa con «1 0»?",
            "Las personas sin amigos también son un grupo (de una sola persona).",
            "Lanza el recorrido desde TODAS las personas sin visitar, tengan o no amigos, y actualiza el máximo después de cada recorrido."])
    prueba("Nadie es amigo de nadie", "borde", [(7, []), (20000, [])],
           "M = 0: cada persona es su propio grupo; el mayor tiene 1 persona.",
           {"wa": "Sin amistades la respuesta es 1, no 0: cada persona es un grupo de una."},
           ["Con M = 0, ¿cuántas personas tiene cada grupo?",
            "Inicializa bien el máximo y cuenta también los grupos de una sola persona."])
    prueba("Todos amigos de todos", "borde", [(6, [(a, b) for a in range(1, 7) for b in range(a + 1, 7)])],
           "Seis personas y las 15 parejas posibles: un solo grupo de 6.",
           {"wa": "Si sale más de 6, cuentas personas varias veces (por cada amistad en lugar de una vez por persona). Si sale menos, el recorrido no llega a todos."},
           ["El grupo tiene 6 personas aunque haya 15 amistades.",
            "Cuenta vértices visitados, no aristas recorridas: marca cada persona al visitarla y no la vuelvas a contar."])
    prueba("Amigos de amigos (una cadena)", "trampa", [(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])],
           "Una cadena 1-2-3-4-5-6-7 y una persona suelta: por el refrán, los siete son del mismo grupo.",
           {"wa": "No basta con contar los amigos directos: el amigo de un amigo también es amigo. El grupo es todo lo que se alcanza siguiendo amistades."},
           ["1 y 7 no son amigos directos, pero hay una cadena de amistades que los une.",
            "El tamaño del grupo es el número de personas que alcanza un recorrido (DFS/BFS), no el grado de una persona.",
            "En el DFS, llama recursivamente a dfs(w) para cada amigo w sin visitar y suma lo que devuelve."])
    prueba("Una pareja repetida y al revés", "trampa", [(4, [(1, 2), (2, 1), (1, 2), (3, 4)])],
           "La misma amistad 1-2 aparece tres veces (una al revés): sigue siendo un grupo de 2.",
           {"wa": "Una amistad repetida no añade personas. Si sale más de 2, sumas tamaños al unir dos personas que ya estaban en el mismo grupo (o cuentas aristas en lugar de personas)."},
           ["«1 2», «2 1» y «1 2» son la misma pareja: el grupo {1, 2} tiene 2 personas.",
            "Si usas conjuntos disjuntos, antes de unir comprueba que los representantes son distintos.",
            "Con un DFS que marca a cada persona al visitarla, las repeticiones no importan: el vecino ya visitado no se vuelve a contar."])
    prueba("Un grupo con un ciclo", "trampa", [(5, [(1, 2), (2, 3), (3, 1), (4, 5)])],
           "Un triángulo 1-2-3: la última amistad une a dos personas que ya estaban en el mismo grupo.",
           {"wa": "La amistad 3-1 no trae a nadie nuevo. Si te sale más de 3, sumas tamaños sin comprobar si ya estaban juntos o cuentas a alguien dos veces."},
           ["Cuando llega «3 1», 1 y 3 ya son del mismo grupo.",
            "Al unir dos grupos, suma los tamaños solo si son grupos distintos."])
    prueba("Personas numeradas de 1 a N", "trampa", [(3, [(3, 1), (2, 3)])],
           "Las personas van de 1 a N y la persona N también aparece.",
           {"rte": "Las personas van de 1 a N: si creas un grafo de N vértices y no restas 1, la persona N se sale (Grafo(cin, 1) resta el 1 al leer)."},
           ["La persona 3 existe cuando N = 3.",
            "Usa Grafo(cin, 1), o resta 1 a cada persona al leerla, o crea N + 1 vértices y no uses el 0."])
    prueba("El grupo mayor es el último", "trampa", [(7, [(1, 2), (4, 5), (5, 6), (6, 7)])],
           "Los grupos son {1, 2}, {3} y {4, 5, 6, 7}: el mayor es el último que se recorre.",
           {"wa": "El máximo se queda sin mirar el último grupo: actualízalo justo después de recorrer cada grupo, no al empezar el siguiente."},
           ["La respuesta es 4: el grupo de las personas 4 a 7.",
            "¿Dónde actualizas el máximo? Si es al encontrar un grupo nuevo, el último nunca se compara.",
            "Pon maxim = max(maxim, dfs(v)) justo después de cada recorrido."])
    prueba("Dos grupos que se unen al final", "trampa", [(4, [(1, 2), (3, 4), (2, 3)])],
           "Primero {1, 2} y {3, 4} por separado; la última amistad 2-3 los junta en un grupo de 4.",
           {"wa": "Si pones a cada persona una etiqueta de grupo según van llegando las amistades, cuando una amistad une dos grupos ya formados hay que fusionarlos (cambiar la etiqueta de todo un grupo)."},
           ["Con «2 3», los grupos {1, 2} y {3, 4} pasan a ser uno solo.",
            "Etiquetar al leer no basta si no fusionas grupos; es más sencillo construir el grafo y recorrerlo después.",
            "Construye el grafo con todas las amistades y luego recorre cada componente con un DFS."])
    prueba("Varios casos seguidos", "trampa",
           [(10, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]),
            (4, [(1, 2), (3, 4)]),
            (3, []),
            (5, [(1, 2), (2, 3)])],
           "Un caso con un grupo grande seguido de otros con grupos pequeños: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el máximo, el vector de visitados o el grafo están declarados fuera de la función de cada caso."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "El máximo empieza en 0 en cada caso: créalo (y los visitados) dentro de la función de cada caso."])
    prueba("Más grupos variados", "trampa",
           [(6, [(6, 5), (4, 6), (2, 1)]),
            (9, [(1, 9), (9, 2), (2, 8), (8, 3), (3, 7)]),
            (8, [(1, 2), (3, 4), (5, 6), (7, 8), (2, 3), (6, 7), (4, 5)]),
            (6, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (6, 1), (5, 1)]),
            (12, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 7), (7, 4), (8, 9)]),
            (2, [(2, 1), (1, 2)])],
           "Estrellas, cadenas en desorden, grupos que se van uniendo y parejas repetidas.",
           {"wa": "Alguno de estos grupos te engaña: la línea que falla es el número de caso; dibuja sus amistades."},
           ["Busca el caso de la línea que falla y dibújalo.",
            "Comprueba que cuentas cada persona una sola vez y que sigues las amistades en los dos sentidos."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(60)],
           "60 casos pequeños al azar, con alguna pareja repetida.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja ese grafo y sigue tu programa a mano."},
           ["Busca en la entrada el caso de la línea que falla y dibújalo.",
            "Comprueba a mano qué grupos salen y cuál es el mayor."])
    # ---- grandes
    N = 20000
    perm = list(range(1, N + 1))
    rng.shuffle(perm)
    cadena = [(perm[i], perm[i + 1]) for i in range(N - 1)]
    prueba("Cadena de 20.000 personas", "rendimiento", [(N, cadena)],
           "Una sola cadena con todas las personas: el DFS recursivo baja 20.000 niveles.",
           {"mle": "Gastas demasiada memoria en la recursión: ¿pasas el grafo por valor (Grafo g)? Se copia entero en cada llamada.",
            "tle": "Algo se repite de más: ¿lanzas un recorrido desde cada persona, o copias el grafo o los visitados en cada llamada?",
            "rte": "La recursión es muy profunda. En el juez hay pila de sobra; revisa que no declaras vectores grandes dentro de la función recursiva."},
           ["Mira la cabecera de tu función recursiva: ¿cómo recibe el grafo?",
            "Pasa el grafo por referencia (Grafo const& g) y el vector de visitados como atributo o por referencia.",
            "Un único recorrido por componente: no reinicies los visitados para cada persona."])
    prueba("Máximo de personas y amistades", "rendimiento",
           [grupos_grandes(rng, N, 200000)],
           "N = 20.000 y M = 200.000 (con repeticiones), en grupos de tamaños muy distintos.",
           {"tle": "Hay que ir en O(N + M). Si lanzas un recorrido completo desde cada persona (o reinicias los visitados cada vez), es O(N·(N + M)).",
            "mle": "Una matriz de adyacencia de 20.000 × 20.000 no cabe: usa listas de adyacencia (la clase Grafo)."},
           ["Cada persona debe visitarse una sola vez en todo el caso.",
            "Crea el vector de visitados una vez por caso y lanza el DFS solo desde las personas que aún no se han visitado."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{mayor_grupo(*c)}\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_LECTURA = "    Grafo g(cin, 1);   // lee N, M y las M amistades (de 1 a N)\n\n    MaximaCompConexa mcc(g);\n    cout << mcc.maximo() << '\\n';"

VARIANTES = [
    Variante("no resta 1 a las personas", [("Grafo g(cin, 1);", "Grafo g(cin);")], prueba=8, v="rte"),
    Variante("solo cuenta los amigos directos",
             [("if (!visit[w]) tam += dfs(g, w);", "if (!visit[w]) { visit[w] = true; ++tam; }")], prueba=5, v="wa"),
    Variante("conjuntos disjuntos que suman sin comprobar",
             [(_LECTURA,
               "    int n, m; cin >> n >> m;\n"
               "    vector<int> padre(n), tam(n, 1);\n"
               "    for (int i = 0; i < n; ++i) padre[i] = i;\n"
               "    auto raiz = [&](int x) { while (padre[x] != x) x = padre[x] = padre[padre[x]]; return x; };\n"
               "    int mejor = 1;\n"
               "    for (int i = 0; i < m; ++i) {\n"
               "        int a, b; cin >> a >> b;\n"
               "        int ra = raiz(a - 1), rb = raiz(b - 1);\n"
               "        padre[ra] = rb; tam[rb] += tam[ra];   // falta: if (ra != rb)\n"
               "        mejor = max(mejor, tam[rb]);\n"
               "    }\n"
               "    cout << mejor << '\\n';")], prueba=[6, 7], v="wa"),
    Variante("no cuenta a las personas sin amigos",
             [("if (!visit[v]) {   // v empieza una componente nueva", "if (!visit[v] && !g.ady(v).empty()) {   // v empieza una componente nueva")], prueba=2, v="wa"),
    Variante("no compara el último grupo",
             [("visit(g.V(), false), maxim(0) {", "visit(g.V(), false), maxim(0) {\n        int ultimo = 0;"),
              ("int tam = dfs(g, v);\n                maxim = max(maxim, tam);", "maxim = max(maxim, ultimo);\n                ultimo = dfs(g, v);")], prueba=9, v="wa"),
    Variante("etiqueta grupos al leer sin fusionarlos",
             [(_LECTURA,
               "    int n, m; cin >> n >> m;\n"
               "    vector<int> grupo(n + 1, 0); int sig = 0;\n"
               "    for (int i = 0; i < m; ++i) {\n"
               "        int a, b; cin >> a >> b;\n"
               "        if (!grupo[a] && !grupo[b]) grupo[a] = grupo[b] = ++sig;\n"
               "        else if (!grupo[a]) grupo[a] = grupo[b];\n"
               "        else if (!grupo[b]) grupo[b] = grupo[a];\n"
               "    }\n"
               "    vector<int> cuenta(sig + 1, 0); int mejor = 1;\n"
               "    for (int v = 1; v <= n; ++v) if (grupo[v]) mejor = max(mejor, ++cuenta[grupo[v]]);\n"
               "    cout << mejor << '\\n';")], prueba=10, v="wa"),
    Variante("el máximo no se reinicia entre casos",
             [("visit(g.V(), false), maxim(0) {", "visit(g.V(), false) {"),
              ("    int maxim;            // tamano de la mayor componente encontrada", "    static inline int maxim = 0;")], prueba=11, v="wa"),
    Variante("copia el grafo en cada llamada", [("int dfs(Grafo const& g, int v) {", "int dfs(Grafo g, int v) {")], prueba=14, v="mle"),
    Variante("un recorrido completo desde cada persona",
             [("if (!visit[v]) {   // v empieza una componente nueva", "{ visit.assign(g.V(), false);   // recorre desde cada persona")], prueba=[14, 15], v="tle"),
]
