"""04-7 · Grafo bipartito: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso V (1..100), A y A aristas «v w» (0..V-1, sin bucles ni aristas
repetidas). Salida: SI si el grafo es bipartito (se puede colorear con dos colores sin que ninguna
arista una dos vértices del mismo color) y NO si no lo es.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-7/EJ_04-7.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-7/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["color[w] = !color[v];", "color[w] = color[v];"],
}


# ---------------------------------------------------------------- solucionador independiente
def bipartito(V, aristas):
    """Conjuntos disjuntos con paridad: cada vértice guarda si tiene el mismo color que su raíz.
    Una arista entre dos vértices de la misma componente y la misma paridad cierra un ciclo impar."""
    padre = list(range(V))
    par = [0] * V            # paridad respecto al padre

    def raiz(x):
        p = 0
        while padre[x] != x:
            p ^= par[x]
            x = padre[x]
        return x, p

    for v, w in aristas:
        (rv, pv), (rw, pw) = raiz(v), raiz(w)
        if rv == rw:
            if pv == pw:
                return False
        else:
            padre[rv] = rw
            par[rv] = pv ^ pw ^ 1
    return True


def caso_a_texto(caso):
    V, aristas = caso
    return f"{V}\n{len(aristas)}\n" + "".join(f"{v} {w}\n" for v, w in aristas)


# ---------------------------------------------------------------- generadores
def mezcla(rng, V, aristas):
    nombres = list(range(V))
    rng.shuffle(nombres)
    res = [(nombres[v], nombres[w]) if rng.random() < .5 else (nombres[w], nombres[v]) for v, w in aristas]
    rng.shuffle(res)
    return res


def aleatorio_pequeno(rng):
    V = rng.randint(1, 9)
    if rng.random() < .5:                         # bipartito: aristas solo entre dos lados
        lado = [rng.random() < .5 for _ in range(V)]
        pos = [(a, b) for a in range(V) for b in range(a + 1, V) if lado[a] != lado[b]]
    else:
        pos = [(a, b) for a in range(V) for b in range(a + 1, V)]
    ar = rng.sample(pos, rng.randint(0, min(len(pos), V + 2)))
    return (V, mezcla(rng, V, ar))


def ciclo(n, desde=0):
    return [(desde + i, desde + (i + 1) % n) for i in range(n)]


def pruebas():
    rng = random.Random(47)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(7, [(0, 2), (0, 4), (1, 6), (1, 3), (2, 6), (2, 5), (4, 6), (4, 5), (4, 3)]),
            (6, [(0, 2), (0, 3), (2, 3), (2, 4), (4, 3), (3, 1), (3, 5), (1, 5)])],
           "Los dos grafos del PDF: uno bipartito y otro con un triángulo.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: V y A en líneas distintas, SI/NO en mayúsculas y sin tilde, y la idea (el color de un vértice obliga al contrario en sus vecinos).",
            "pe": "Las respuestas están bien pero el formato no: una palabra por línea."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "En el primer grafo el reparto es {0, 3, 5, 6} y {1, 2, 4}: compruébalo arista a arista.",
            "Colorea con un DFS: a cada vecino nuevo, el color contrario; si un vecino ya coloreado tiene tu mismo color, NO."])
    prueba("Un único vértice", "borde", [(1, [])],
           "V = 1 sin aristas: bipartito (SI).",
           {"wa": "Un grafo sin aristas siempre es bipartito: no hay ninguna arista que pueda unir dos del mismo color.",
            "rte": "Con V = 1 solo existe el vértice 0."},
           ["¿Qué escribe tu programa con «1» vértice y «0» aristas?",
            "Sin aristas no hay conflicto posible: SI."])
    prueba("Muchos vértices sin aristas", "borde", [(100, [])],
           "V = 100 y ninguna arista: SI.",
           {"wa": "Sin aristas cualquier coloreado vale: SI."},
           ["Con A = 0 no hay ningún conflicto.",
            "Comprueba que lees bien A = 0 (no hay líneas de aristas detrás)."])
    prueba("Una sola arista", "borde", [(2, [(0, 1)])],
           "Dos vértices unidos: uno de cada color (SI).",
           {"wa": "Con una arista basta dar a cada extremo un color distinto. Si dices NO, ¿das al vecino el MISMO color que al vértice?"},
           ["0 de un color y 1 del otro: SI.",
            "Al descubrir un vecino w desde v: color[w] = !color[v]."])
    prueba("Triángulo", "trampa", [(3, [(0, 1), (1, 2), (2, 0)])],
           "El ciclo impar más pequeño: no es bipartito (NO).",
           {"wa": "Tres vértices unidos entre sí no se pueden pintar con dos colores. Si dices SI, no compruebas los vecinos que ya tienen color."},
           ["Pinta 0 de blanco, 1 de negro, 2 de blanco… y la arista 2-0 une dos blancos.",
            "Cuando un vecino ya está visitado, compara su color con el tuyo.",
            "En el DFS: si w no está visitado, color contrario y dfs(w); si ya lo está y color[w] == color[v], el grafo no es bipartito."])
    prueba("Ciclo impar sin triángulos", "trampa", [(5, ciclo(5))],
           "Un ciclo de 5 vértices: no hay ningún triángulo y aun así no es bipartito (NO).",
           {"wa": "No basta con buscar triángulos: cualquier ciclo de longitud impar impide colorear con dos colores."},
           ["Intenta pintar a mano el ciclo 0-1-2-3-4-0 con dos colores.",
            "El problema son los ciclos de longitud IMPAR, de cualquier tamaño.",
            "Haz el coloreado con DFS/BFS en vez de buscar figuras concretas."])
    prueba("Ciclo par", "trampa", [(6, ciclo(6))],
           "Un ciclo de 6 vértices: sí es bipartito (SI).",
           {"wa": "Un ciclo par sí se puede colorear alternando colores. Si dices NO, o tratas cualquier ciclo como un problema o das el mismo color al vecino."},
           ["0 blanco, 1 negro, 2 blanco, 3 negro, 4 blanco, 5 negro: la arista 5-0 une negro y blanco.",
            "Tener ciclos no impide ser bipartito; solo los ciclos impares.",
            "Comprueba que al vecino nuevo le das el color contrario (color[w] = !color[v])."])
    prueba("El ciclo impar está en otra componente", "trampa", [(6, [(0, 1), (3, 4), (4, 5), (5, 3)])],
           "La componente del vértice 0 es bipartita, pero el triángulo 3-4-5 no (NO).",
           {"wa": "El grafo puede no ser conexo: hay que colorear TODAS las componentes, lanzando el DFS desde cada vértice aún sin visitar, no solo desde el 0."},
           ["El triángulo 3-4-5 no está unido al vértice 0.",
            "Un único DFS desde el 0 no llega a los demás trozos.",
            "Recorre los vértices y lanza un DFS desde cada uno que no esté visitado."])
    prueba("Bipartito aunque las aristas lleguen desordenadas", "trampa", [(4, [(0, 1), (2, 3), (1, 3)])],
           "El camino 0-1-3-2 dado en desorden: es bipartito (SI).",
           {"wa": "Colorear las aristas según van llegando no funciona: «0 1» y «2 3» se pintan por separado y «1 3» parece un conflicto, cuando bastaba con invertir los colores de {2, 3}."},
           ["Es un camino: 0 blanco, 1 negro, 3 blanco, 2 negro.",
            "Si coloreas al leer, dos trozos pintados por separado pueden necesitar invertir los colores de uno de ellos.",
            "Construye primero el grafo y colorea después con un recorrido: así el color de cada vértice sale de su vecino."])
    prueba("Vértices numerados desde 0 hasta V − 1", "trampa", [(3, [(0, 2), (2, 1)])],
           "Aristas que usan el vértice 0 y el V − 1.",
           {"rte": "Los vértices van de 0 a V − 1: si restas 1 al leerlos (Grafo(cin, 1)), el 0 se convierte en −1."},
           ["El enunciado numera los vértices desde 0.",
            "Usa Grafo(cin), sin el segundo parámetro."])
    prueba("Ciclo impar muy largo", "trampa", [(100, mezcla(rng, 100, ciclo(99) + [(98, 99)]))],
           "Un ciclo de 99 vértices (con una cola), con los vértices desordenados: NO.",
           {"wa": "Por largo que sea, un ciclo impar no es bipartito. ¿Limitas la profundidad del recorrido o miras solo ciclos cortos?"},
           ["Sigue el ciclo alternando colores: al cerrar los 99 vértices, dos vecinos quedan iguales.",
            "El DFS tiene que llegar hasta el final del ciclo; no limites su profundidad."])
    k33 = [(a, b) for a in range(3) for b in range(3, 6)]
    prueba("Bipartitos completos y casi", "trampa",
           [(6, k33), (6, k33 + [(0, 1)]), (7, [(0, i) for i in range(1, 7)]),
            (8, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4)]),
            (8, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 4), (7, 0)])],
           "K3,3 (SI), K3,3 con una arista dentro de un lado (NO), una estrella, dos cuadrados (SI) y un cuadrado con un triángulo aparte (NO).",
           {"wa": "Alguno de estos grafos te engaña: la línea que falla es el número de caso; dibújalo y colorea a mano."},
           ["Busca el caso de la línea que falla y dibújalo.",
            "Comprueba que miras todas las aristas de todas las componentes."])
    prueba("Varios casos seguidos", "trampa",
           [(3, [(0, 1), (1, 2), (2, 0)]), (4, [(0, 1), (1, 2), (2, 3)]), (2, [(1, 0)]), (5, ciclo(5)), (1, [])],
           "Un grafo no bipartito seguido de otros que sí lo son: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el indicador de «es bipartito», los colores o los visitados están declarados fuera de la función de cada caso."},
           ["Si tras un NO todos salen NO, mira qué variables viven fuera de resuelveCaso.",
            "Empieza cada caso con bipar = true y los vectores de colores y visitados nuevos."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(80)],
           "80 grafos pequeños al azar, la mitad construidos para ser bipartitos.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibújalo y colorea a mano."},
           ["Busca en la entrada el caso de la línea que falla y dibújalo.",
            "Si es NO, busca el ciclo impar; si es SI, busca el reparto en dos colores."])
    k100 = [(a, b) for a in range(100) for b in range(a + 1, 100)]
    k5050 = [(a, b) for a in range(0, 100, 2) for b in range(1, 100, 2)]
    prueba("Grafos completos de 100 vértices", "rendimiento",
           [(100, mezcla(rng, 100, k100)), (100, mezcla(rng, 100, k5050)), (100, mezcla(rng, 100, k5050 + [(0, 98)]))],
           "K100 (NO), el bipartito completo 50 + 50 (SI) y el mismo con una arista de más (NO): miles de aristas.",
           {"tle": "Probar todos los coloreados posibles es exponencial (2¹⁰⁰). El coloreado con DFS es O(V + A).",
            "wa": "Con muchas aristas, revisa que comparas los colores en todas, no solo en la primera que encuentras."},
           ["No pruebes combinaciones de colores: el color de un vértice obliga al de sus vecinos.",
            "Un DFS que da el color contrario a cada vecino nuevo decide en O(V + A)."])
    muchos = []
    for _ in range(300):
        V = 100
        lado = [rng.random() < .5 for _ in range(V)]
        pos = [(a, b) for a in range(V) for b in range(a + 1, V) if lado[a] != lado[b] or rng.random() < .002]
        muchos.append((V, mezcla(rng, V, rng.sample(pos, 150))))
    prueba("300 grafos de 100 vértices", "rendimiento", muchos,
           "Muchos casos medianos, casi bipartitos: algunos tienen una arista que lo estropea.",
           {"tle": "Algo es más caro de lo necesario por caso: ¿pruebas combinaciones de colores?",
            "wa": "Alguno de estos casos te engaña: la línea que falla es el número de caso."},
           ["Cada caso debe costar O(V + A).",
            "Si falla un caso concreto, cópialo y pruébalo a mano en tu ordenador."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(("SI" if bipartito(*c) else "NO") + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_FINAL = "    Bipartito b(g);\n    cout << (b.esBipartito() ? \"SI\" : \"NO\") << '\\n';"

VARIANTES = [
    Variante("no comprueba los vecinos ya coloreados", [("else if (color[w] == color[v]) bipar = false;", "")], prueba=5, v="wa"),
    Variante("solo busca triángulos",
             [(_FINAL,
               "    bool triangulo = false;\n"
               "    for (int a = 0; a < g.V(); ++a) for (int b : g.ady(a)) for (int c : g.ady(b))\n"
               "        if (c != a) for (int d : g.ady(c)) if (d == a) triangulo = true;\n"
               "    cout << (triangulo ? \"NO\" : \"SI\") << '\\n';")], prueba=6, v="wa"),
    Variante("da al vecino el mismo color", [("color[w] = !color[v];", "color[w] = color[v];")], prueba=7, v="wa"),
    Variante("solo colorea la componente del 0", [("for (int v = 0; v < g.V() && bipar; ++v) {", "for (int v = 0; v < 1 && bipar; ++v) {")], prueba=8, v="wa"),
    Variante("colorea las aristas según llegan",
             [("    Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)\n\n" + _FINAL,
               "    int V0, A0; cin >> V0 >> A0;\n"
               "    vector<int> col(V0, -1); bool ok = true;\n"
               "    for (int i = 0; i < A0; ++i) {\n"
               "        int x, y; cin >> x >> y;\n"
               "        if (col[x] == -1 && col[y] == -1) { col[x] = 0; col[y] = 1; }\n"
               "        else if (col[x] == -1) col[x] = 1 - col[y];\n"
               "        else if (col[y] == -1) col[y] = 1 - col[x];\n"
               "        else if (col[x] == col[y]) ok = false;\n"
               "    }\n"
               "    cout << (ok ? \"SI\" : \"NO\") << '\\n';")], prueba=9, v="wa"),
    Variante("resta 1 a los vértices", [("Grafo g(cin);", "Grafo g(cin, 1);")], prueba=10, v="rte"),
    Variante("el indicador no se reinicia entre casos",
             [("color(g.V(), false), bipar(true) {", "color(g.V(), false) {"),
              ("    bool bipar;", "    static inline bool bipar = true;")], prueba=13, v="wa"),
]
