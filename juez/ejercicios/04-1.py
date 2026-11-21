"""04-1 · Árboles libres: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso es V (1..10.000), A (0..100.000) y A aristas «v w» con
vértices de 0 a V-1, sin bucles ni aristas repetidas. Salida: SI si el grafo es árbol libre
(conexo y acíclico) y NO si no lo es.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-1/EJ_04-1.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-1/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["arbol = conexo && g.A() == g.V() - 1;", "arbol = g.A() == g.V() - 1;"],
}


# ---------------------------------------------------------------- solucionador independiente
def es_arbol(V, aristas):
    """Árbol libre ⇔ no hay ninguna arista que cierre un ciclo y queda una sola componente.
    Se hace con conjuntos disjuntos (no con la propiedad A = V - 1 de la solución del repo)."""
    padre = list(range(V))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    componentes = V
    for v, w in aristas:
        a, b = raiz(v), raiz(w)
        if a == b:
            return False          # esta arista cierra un ciclo
        padre[a] = b
        componentes -= 1
    return componentes == 1


def caso_a_texto(caso):
    V, aristas = caso
    return f"{V}\n{len(aristas)}\n" + "".join(f"{v} {w}\n" for v, w in aristas)


# ---------------------------------------------------------------- generadores de grafos
def mezcla(rng, V, aristas, fijo0=False):
    """Renombra los vértices al azar (salvo el 0 si fijo0), da la vuelta a algunas aristas y las
    desordena. No cambia la respuesta."""
    nombres = list(range(V))
    if fijo0:
        resto = nombres[1:]
        rng.shuffle(resto)
        nombres = [0] + resto
    else:
        rng.shuffle(nombres)
    res = [(nombres[v], nombres[w]) if rng.random() < .5 else (nombres[w], nombres[v]) for v, w in aristas]
    rng.shuffle(res)
    return res


def arbol_aleatorio(rng, V):
    return [(v, rng.randrange(v)) for v in range(1, V)]


def camino(V):
    return [(v, v + 1) for v in range(V - 1)]


def ciclo(V, desde=0):
    return [(desde + v, desde + (v + 1) % V) for v in range(V)]


def aleatorio_pequeno(rng):
    V = rng.randint(1, 9)
    tipo = rng.random()
    if tipo < .35:                                # árbol
        ar = arbol_aleatorio(rng, V)
    elif tipo < .55 and V >= 3:                   # árbol + una arista (un ciclo)
        ar = arbol_aleatorio(rng, V)
        posibles = [(a, b) for a in range(V) for b in range(a + 1, V) if (a, b) not in ar and (b, a) not in ar]
        ar = ar + [rng.choice(posibles)]
    elif tipo < .75 and V >= 2:                   # bosque (le falta alguna arista)
        ar = arbol_aleatorio(rng, V)
        ar = rng.sample(ar, rng.randrange(len(ar)))
    else:                                         # cualquiera
        posibles = [(a, b) for a in range(V) for b in range(a + 1, V)]
        ar = rng.sample(posibles, rng.randint(0, len(posibles)))
    return (V, mezcla(rng, V, ar))


def denso_conexo(rng, V, A):
    """Grafo conexo con A aristas (un árbol más aristas al azar, sin repetir)."""
    ar = set()
    for v in range(1, V):
        ar.add((rng.randrange(v), v))
    while len(ar) < A:
        a, b = rng.randrange(V), rng.randrange(V)
        if a != b:
            ar.add((min(a, b), max(a, b)))
    return mezcla(rng, V, list(ar))


def pruebas():
    rng = random.Random(41)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    ejemplo = [(6, [(0, 5), (0, 2), (2, 1), (2, 3), (4, 3)]),
               (6, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5)]),
               (1, [])]
    prueba("Ejemplo del enunciado", "enunciado", ejemplo,
           "Los tres casos del PDF: un árbol, un grafo con V − 1 aristas que no es árbol y un único vértice.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: que lees V y A en líneas distintas, que escribes SI/NO en mayúsculas y sin tilde, y la idea (conexo y sin ciclos).",
            "pe": "Las respuestas están bien pero el formato no: una palabra por línea, sin espacios ni texto extra."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "Escribe exactamente «SI» o «NO» (sin tilde, en mayúsculas) y un salto de línea por caso.",
            "El segundo caso tiene V − 1 aristas y aun así no es árbol: además del número de aristas hay que comprobar que es conexo."])
    prueba("Un único vértice", "borde", [(1, [])],
           "V = 1 y ninguna arista: es un árbol libre (SI).",
           {"wa": "Con un solo vértice el grafo es conexo y no tiene ciclos: es árbol. Suele fallar por exigir al menos una arista o por tratar «A = 0» como caso especial.",
            "rte": "Con V = 1 solo existe el vértice 0: ¿empiezas el recorrido en el vértice 1 o miras ady(1)?"},
           ["¿Qué escribe tu programa con «1» vértice y «0» aristas?",
            "1 vértice y 0 aristas cumple A = V − 1 y el recorrido desde 0 llega a todos (al único que hay).",
            "No hace falta ningún caso especial: quita cualquier condición del tipo «si A == 0 entonces NO»."])
    prueba("Dos vértices", "borde", [(2, [(0, 1)]), (2, [])],
           "El árbol más pequeño con una arista (SI) y dos vértices sueltos (NO).",
           {"wa": "Con una sola arista no hay ciclo. Si dices NO al primero, probablemente tomas la arista de vuelta al padre (1 → 0) como si cerrara un ciclo."},
           ["«0 1» es un árbol; «2 vértices, 0 aristas» no es conexo.",
            "En un DFS que busca ciclos, el vecino del que vienes (el padre) ya está visitado pero NO forma un ciclo."])
    prueba("Muchos vértices y ninguna arista", "borde", [(10000, []), (3, [])],
           "V = 10.000 sin aristas: no es conexo (NO).",
           {"wa": "Sin aristas tampoco hay ciclos, pero el grafo no es conexo. Si dices SI, solo estás comprobando que no hay ciclos."},
           ["Un grafo sin aristas y con más de un vértice tiene V componentes.",
            "Además de no tener ciclos, el árbol tiene que ser conexo: cuenta cuántos vértices alcanza un recorrido desde el 0."])
    prueba("V − 1 aristas pero no es conexo", "trampa",
           [(5, [(0, 1), (1, 2), (2, 0), (3, 4)])],
           "Un triángulo y una arista suelta: V − 1 aristas, todos los vértices con algún vecino… y no es conexo (NO).",
           {"wa": "Contar aristas no basta: con V − 1 aristas el grafo puede tener un ciclo y quedar partido en trozos. Tampoco basta con que todos los vértices tengan algún vecino."},
           ["Hay 4 aristas y 5 vértices, todos con algún vecino… y no es árbol: el triángulo 0-1-2 y la arista 3-4 no se tocan.",
            "Que todo vértice tenga grado ≥ 1 no significa que el grafo sea conexo.",
            "Comprueba de verdad la conexión: un DFS desde el 0 tiene que visitar los V vértices, además de que A = V − 1."])
    prueba("Hay que leer todas las aristas aunque ya sepas la respuesta", "trampa",
           [(6, [(0, 1), (1, 2), (2, 0), (3, 4)]),
            (4, [(0, 1), (1, 2), (1, 3)]),
            (5, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4)]),
            (3, [(2, 0), (1, 2)])],
           "Un caso con A ≠ V − 1 seguido de otros: aunque ya sepas que es NO, sus aristas siguen en la entrada.",
           {"wa": "Si contestas NO en cuanto ves que A ≠ V − 1 y pasas al siguiente caso sin leer sus A aristas, esas aristas se leen como si fueran el caso siguiente y todo se descoloca.",
},
           ["El primer caso es NO, pero el segundo es SI: ¿tu programa contesta bien al segundo?",
            "Mira qué pasa con las líneas «0 1», «1 2»… del primer caso si no las lees.",
            "Lee siempre el caso completo (V, A y las A aristas) antes de decidir nada; Grafo(cin) ya lo hace."])
    prueba("Conexo pero con ciclos", "trampa",
           [(3, [(0, 1), (1, 2), (2, 0)])],
           "Un triángulo: es conexo pero tiene un ciclo, así que no es árbol (NO).",
           {"wa": "Ser conexo no basta: un árbol tampoco puede tener ciclos. Si dices SI, solo compruebas la conexión."},
           ["El triángulo 0-1-2 es conexo, pero no es un árbol.",
            "Un árbol con V vértices tiene exactamente V − 1 aristas; si hay más, hay algún ciclo.",
            "Añade la segunda condición: conexo Y A == V − 1 (o busca ciclos en el DFS)."])
    prueba("Bosque: sin ciclos pero no conexo", "trampa",
           [(4, [(0, 1), (2, 3)])],
           "Dos árboles separados (un bosque): no hay ciclos, pero tampoco es conexo (NO).",
           {"wa": "No tener ciclos no basta: tiene que ser conexo. Si solo buscas ciclos desde el vértice 0, los demás trozos ni se miran."},
           ["En «0-1» y «2-3» no hay ningún ciclo, y aun así no es un árbol.",
            "Después del DFS desde el 0, ¿has comprobado que se ha visitado a todos?",
            "Cuenta los vértices que visita el recorrido desde el 0: si no son V, la respuesta es NO."])
    prueba("La arista de vuelta al padre no es un ciclo", "trampa",
           [(7, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])],
           "Un árbol binario de 7 vértices (SI): al bajar por cada arista, el hijo vuelve a ver a su padre.",
           {"wa": "Si buscas ciclos con un DFS, al mirar los adyacentes de w aparece su padre v, que ya está visitado. Eso no es un ciclo: hay que ignorar al padre."},
           ["Dibuja el árbol y sigue tu DFS: al llegar al 1 desde el 0, ¿qué pasa cuando miras ady(1)?",
            "En un grafo no dirigido la arista v-w aparece en ady(v) y en ady(w): al bajar de v a w, w ve otra vez a v.",
            "Pasa el padre al DFS (dfs(w, v)) y solo cuenta como ciclo un vecino visitado que no sea el padre; o usa la condición A == V − 1."])
    prueba("Vértices numerados desde 0 hasta V − 1", "trampa",
           [(3, [(0, 2), (2, 1)]),
            (4, [(3, 0), (0, 1), (1, 2)]),
            (5, [(4, 3), (3, 2), (2, 1), (1, 0)])],
           "Aristas que usan el vértice 0 y el V − 1.",
           {"rte": "Los vértices van de 0 a V − 1. Si les restas 1 al leerlos (Grafo(cin, 1)) el 0 se convierte en −1, y si reservas V posiciones y usas el número tal cual no cabe el V."},
           ["El enunciado numera los vértices desde 0, no desde 1.",
            "Usa Grafo(cin) (sin el segundo parámetro) o, si lees a mano, no restes 1."])
    prueba("Aristas en cualquier orden", "trampa",
           [(4, [(0, 1), (2, 3), (1, 2)]),
            (6, [(4, 5), (2, 3), (0, 1), (3, 4), (1, 2)]),
            (5, [(3, 4), (1, 2), (2, 3), (0, 4)])],
           "Árboles cuyas aristas llegan desordenadas: la última arista une dos trozos ya empezados (SI).",
           {"wa": "Mirar si los dos extremos de una arista «ya han aparecido» no detecta ciclos: en «0 1», «2 3», «1 2» la última arista une dos trozos distintos y no cierra ningún ciclo."},
           ["En el primer caso, la tercera arista tiene los dos extremos ya vistos y sin embargo es un camino 0-1-2-3.",
            "Un ciclo aparece cuando los dos extremos ya están en el MISMO trozo, no simplemente cuando ya han salido.",
            "Haz un recorrido sobre el grafo completo (DFS) o usa conjuntos disjuntos para saber si dos vértices están ya conectados."])
    prueba("Varios casos seguidos", "trampa",
           [(6, [(0, 5), (5, 4), (4, 3), (3, 2), (2, 1)]),
            (3, [(0, 1), (1, 2)]),
            (4, [(0, 1), (1, 2), (2, 0)]),
            (2, [(0, 1)]),
            (1, [])],
           "Un árbol grande seguido de otros más pequeños: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el vector de visitados, el contador de vértices alcanzados o el grafo, declarados fuera de la función de cada caso."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el grafo, los visitados y los contadores dentro de la función de cada caso (o reinícialos)."])
    prueba("Más árboles y casi árboles", "trampa",
           [(6, [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5)]),
            (4, [(1, 2), (2, 3), (3, 1)]),
            (7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (5, 6)]),
            (5, [(0, 1), (0, 2), (0, 3), (0, 4)]),
            (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
            (6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (4, 5)]),
            (5, [(0, 1), (1, 2), (3, 4)]),
            (7, [(0, 3), (3, 5), (5, 1)]),
            (5, [(3, 4), (2, 3), (1, 2), (0, 1)]),
            (2, []),
            (8, [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7), (3, 4)]),
            (8, [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7), (7, 4)])],
           "Doce grafos parecidos a árboles: con un ciclo, con trozos sueltos, con el 0 aislado, caminos y estrellas.",
           {"wa": "Alguno de estos casi-árboles te engaña: mira el número de caso que falla. Recuerda: árbol = conexo y sin ciclos (o conexo y A = V − 1)."},
           ["La línea que falla es el número de caso: dibuja ese grafo.",
            "Comprueba por separado: ¿llega el DFS desde 0 a todos?, ¿hay exactamente V − 1 aristas?"])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(80)],
           "80 grafos pequeños al azar: árboles, árboles con una arista de más, bosques y grafos cualesquiera.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja ese grafo y sigue tu programa a mano."},
           ["Busca en la entrada el caso de la línea que falla y dibújalo.",
            "Comprueba por separado las dos condiciones (conexo, sin ciclos) en ese caso."])
    # ---- grandes
    V = 10000
    nombres = list(range(V))
    rng.shuffle(nombres)
    camino_ord = [(nombres[i], nombres[i + 1]) for i in range(V - 1)]
    prueba("Camino de 10.000 vértices", "rendimiento",
           [(V, camino_ord), (V, camino_ord[:-1] + [(nombres[0], nombres[V - 1])]), (V, camino_ord[:V // 2] + camino_ord[V // 2 + 1:] + [(nombres[0], nombres[V // 2])])],
           "Un camino con el máximo de vértices: el DFS recursivo baja 10.000 niveles.",
           {"mle": "Gastas demasiada memoria en la recursión: ¿pasas el grafo por valor (Grafo g) en vez de por referencia (Grafo const& g)? Se copia entero en cada llamada.",
            "tle": "Algo se repite de más: copiar el grafo o el vector de visitados en cada llamada recursiva es muy caro.",
            "rte": "La recursión es muy profunda. En el juez hay pila de sobra; revisa que no declaras vectores grandes dentro de la función recursiva."},
           ["Mira la cabecera de tu función recursiva: ¿cómo recibe el grafo?",
            "Pasa siempre el grafo y los vectores grandes por referencia (const& o &).",
            "dfs(Grafo const& g, int v): sin el & cada llamada copia el grafo entero."])
    denso = [denso_conexo(rng, V, 100000) for _ in range(2)]
    prueba("Grafo con 100.000 aristas", "rendimiento",
           [(V, denso[0]), (V, denso[1]), (V, mezcla(rng, V, arbol_aleatorio(rng, V)))],
           "El máximo de aristas (con muchos ciclos) y un árbol aleatorio de 10.000 vértices.",
           {"tle": "Para 100.000 aristas hay que ir en O(V + A). ¿Usas una matriz de adyacencia o recorres el grafo varias veces?",
            "mle": "Una matriz de adyacencia de 10.000 × 10.000 enteros no cabe en memoria: usa listas de adyacencia (la clase Grafo)."},
           ["Un único recorrido por caso basta: cada vértice y cada arista se miran una vez.",
            "Si usas una matriz de adyacencia, cámbiala por la clase Grafo (listas de adyacencia)."])
    prueba("Muchos grafos grandes sin aristas", "rendimiento", [(V, []) for _ in range(60)] + [(V, camino_ord)],
           "60 casos de 10.000 vértices: lo que cueste V² por caso no llega a tiempo.",
           {"tle": "Algo cuesta V² por caso (una matriz de adyacencia, un bucle doble sobre los vértices...). Con listas de adyacencia es O(V + A).",
            "mle": "Reservas demasiada memoria por caso: con V = 10.000 una matriz V × V de enteros ocupa 400 MB."},
           ["¿Qué estructura creas al empezar cada caso y cuánto ocupa con V = 10.000?",
            "Usa la clase Grafo (listas de adyacencia): crearla cuesta O(V), no O(V²)."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(("SI" if es_arbol(V, ar) else "NO") + "\n" for V, ar in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("solo cuenta las aristas", [("arbol = conexo && g.A() == g.V() - 1;", "arbol = g.A() == g.V() - 1;")], prueba=5, v="wa"),
    Variante("conexo si todos tienen algún vecino",
             [("bool conexo = (alcanzados == g.V());",
               "bool conexo = true;\n        for (int u = 0; u < g.V(); ++u) if (g.V() > 1 && g.ady(u).empty()) conexo = false;")], prueba=5, v="wa"),
    Variante("contesta NO sin leer las aristas",
             [("Grafo g(cin);   // lee V, A y las A aristas (vertices desde 0)",
               "int V0, A0; cin >> V0 >> A0;\n    if (A0 != V0 - 1) { cout << \"NO\\n\"; return; }\n"
               "    Grafo g(V0);\n    for (int i = 0; i < A0; ++i) { int x, y; cin >> x >> y; g.ponArista(x, y); }")], prueba=6, v="wa"),
    Variante("solo comprueba que es conexo", [("arbol = conexo && g.A() == g.V() - 1;", "arbol = conexo;")], prueba=7, v="wa"),
    Variante("solo busca ciclos (no mira si es conexo)",
             [("void dfs(Grafo const& g, int v) {", "void dfs(Grafo const& g, int v, int p = -1) {"),
              ("if (!visit[w]) dfs(g, w);", "if (!visit[w]) dfs(g, w, v); else if (w != p) ciclo = true;"),
              ("bool arbol;", "bool arbol; bool ciclo = false;"),
              ("arbol = conexo && g.A() == g.V() - 1;", "arbol = !ciclo;")], prueba=8, v="wa"),
    Variante("toma al padre por un ciclo",
             [("if (!visit[w]) dfs(g, w);", "if (!visit[w]) dfs(g, w); else ciclo = true;"),
              ("bool arbol;", "bool arbol; bool ciclo = false;"),
              ("arbol = conexo && g.A() == g.V() - 1;", "arbol = conexo && !ciclo;")], prueba=9, v="wa"),
    Variante("resta 1 a los vértices", [("Grafo g(cin);", "Grafo g(cin, 1);")], prueba=10, v="rte"),
    Variante("contador de alcanzados global",
             [("class ArbolLibre {", "int alcGlobal = 0;\nclass ArbolLibre {"),
              ("++alcanzados;", "++alcGlobal; alcanzados = alcGlobal;")], prueba=12, v="wa"),
    Variante("exige al menos una arista", [("arbol = conexo && g.A() == g.V() - 1;", "arbol = conexo && g.A() == g.V() - 1 && g.A() > 0;")], prueba=2, v="wa"),
    Variante("copia el grafo en cada llamada", [("void dfs(Grafo const& g, int v) {", "void dfs(Grafo g, int v) {")], prueba=15, v="mle"),
]
