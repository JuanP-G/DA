"""04-4 · Los números de Bacon: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso P películas (1..5.000), una por línea «título k actor1 ... actork»
(k ≥ 1, actores sin repetir en la película, en total como mucho 100.000), luego N consultas
(1..100.000), cada una el nombre de un actor que sale en alguna película. Salida: «nombre número»
(o «nombre INF» si no se puede llegar a KevinBacon) por consulta y «---» al final de cada caso.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-4/EJ_04-4.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-4/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["caminos.distancia(v) / 2", "caminos.distancia(v)"],
}
BACON = "KevinBacon"


# ---------------------------------------------------------------- solucionador independiente
def numeros(peliculas, consultas):
    """BFS por actores: desde un actor se pasa a todos los de sus películas; cada película se
    expande una sola vez (sin construir el grafo actor-película de la solución del repo)."""
    pelis_de = {}
    for i, (_, reparto) in enumerate(peliculas):
        for a in reparto:
            pelis_de.setdefault(a, []).append(i)
    dist = {}
    if BACON in pelis_de:
        dist[BACON] = 0
        usada = [False] * len(peliculas)
        cola = deque([BACON])
        while cola:
            a = cola.popleft()
            for p in pelis_de[a]:
                if not usada[p]:
                    usada[p] = True
                    for b in peliculas[p][1]:
                        if b not in dist:
                            dist[b] = dist[a] + 1
                            cola.append(b)
    return [f"{c} {dist[c]}" if c in dist else f"{c} INF" for c in consultas]


def caso_a_texto(caso):
    peliculas, consultas = caso
    return (f"{len(peliculas)}\n" + "".join(f"{t} {len(r)} {' '.join(r)}\n" for t, r in peliculas)
            + f"{len(consultas)}\n" + "".join(c + "\n" for c in consultas))


def caso_a_salida(caso):
    return "".join(l + "\n" for l in numeros(*caso)) + "---\n"


# ---------------------------------------------------------------- generadores
def nombre(i, pre="a"):
    """Nombre corto y único (base 36): a0, a1, ..., azz..."""
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    s = ""
    while True:
        s = d[i % 36] + s
        i //= 36
        if not i:
            return pre + s


def pel(texto):
    """«Titulo A B C» → (titulo, [A, B, C])"""
    t, *r = texto.split()
    return (t, r)


def aleatorio_pequeno(rng):
    actores = [nombre(i, "Act") for i in range(rng.randint(2, 9))]
    if rng.random() < .8:
        actores[0] = BACON
    pelis = []
    for p in range(rng.randint(1, 7)):
        pelis.append((f"Peli{p}", rng.sample(actores, rng.randint(1, min(4, len(actores))))))
    conocidos = sorted({a for _, r in pelis for a in r})
    consultas = [rng.choice(conocidos) for _ in range(rng.randint(1, 6))]
    return (pelis, consultas)


def pruebas():
    rng = random.Random(44)
    P = []

    def prueba(nombre_, tipo, casos, comprueba, si, pistas):
        P.append((nombre_, tipo, casos, comprueba, si, pistas))

    ej1 = ([pel("AlgunosHombresBuenos TomCruise JackNicholson DemiMoore KevinBacon"),
            pel("RainMan DustinHoffman TomCruise ValeriaGolino"),
            pel("Apolo13 TomHanks KevinBacon EdHarris KathleenQuinlan"),
            pel("MejorImposible JackNicholson HelenHunt GregKinnear CubaGoodingJr"),
            pel("LoQueLaNocheEsconde TyeSheridan AnaDeArmas JohnLeguizamo HelenHunt"),
            pel("Sleepers RobertDeNiro DustinHoffman BradPitt KevinBacon"),
            pel("ExperimentoIndie SarahDavis JohnDoe MichaelAnderson")],
           ["TomCruise", "DustinHoffman", "TomHanks", "HelenHunt", "AnaDeArmas", "KevinBacon", "JohnDoe"])
    ej2 = ([pel("MejorImposible JackNicholson HelenHunt GregKinnear CubaGoodingJr"),
            pel("LoQueLaNocheEsconde TyeSheridan AnaDeArmas JohnLeguizamo HelenHunt")],
           ["HelenHunt", "AnaDeArmas"])
    prueba("Ejemplo del enunciado", "enunciado", [ej1, ej2],
           "Los dos casos del PDF: números 0, 1, 2, 3, INF y una base de datos sin Kevin Bacon.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: «nombre número» por consulta, INF cuando no hay cadena y «---» al final de cada caso.",
            "pe": "Los números están bien pero el formato no: «nombre», un espacio y el número (o INF), una consulta por línea."},
           ["Ejecuta tu programa con este mismo ejemplo y compara línea a línea.",
            "Dustin Hoffman tiene número 1 (por Sleepers), aunque por Rain Man saldría 2: se pide el mínimo.",
            "El número de Bacon es la distancia mínima en un grafo sin pesos: BFS desde KevinBacon."])
    prueba("Kevin Bacon y sus compañeros de reparto", "borde",
           [([pel("Tremors KevinBacon FredWard RebaMcEntire")], ["FredWard", "RebaMcEntire", "FredWard"])],
           "Una sola película con Kevin Bacon: sus compañeros tienen número 1.",
           {"wa": "Los que han trabajado con Kevin Bacon tienen número 1. Si te sale 2, usas las películas como vértices y no divides la distancia entre 2."},
           ["¿Cuántas películas hay que encadenar para ir de FredWard a Kevin Bacon?",
            "Si las películas son vértices, cada paso actor → película → actor son dos aristas: el número es distancia / 2."])
    prueba("Películas de un solo actor", "borde",
           [([pel("Monologo1 AnaPrieto"), pel("Monologo2 KevinBacon"), pel("Monologo3 LuisRey")], ["AnaPrieto", "LuisRey", "KevinBacon"])],
           "Películas con un único actor: nadie está conectado con nadie (INF), salvo Kevin Bacon consigo mismo (0).",
           {"wa": "Una película de un solo actor no conecta a nadie. Si sale un número en lugar de INF, revisa cómo detectas que no hay camino."},
           ["AnaPrieto no comparte película con nadie: su número es INF.",
            "Distingue «no visitado por el BFS» (INF) de «distancia 0» (solo Kevin Bacon)."])
    prueba("El separador --- tras cada caso", "trampa",
           [([pel("Corto1 AnaPrieto"), pel("Corto2 LuisRey")], ["LuisRey"])] * 2,
           "Dos casos iguales y muy sencillos (sin Kevin Bacon): detrás de las respuestas de cada caso va una línea «---».",
           {"wa": "La salida de cada caso termina con una línea «---» (tres guiones), también la del último caso."},
           ["Mira la línea que falla: ¿esperaba «---»?",
            "Escribe «---» después de contestar todas las consultas de cada caso, no solo entre casos."])
    prueba("Kevin Bacon no sale en ninguna película", "trampa",
           [([pel("Casablanca HumphreyBogart IngridBergman PaulHenreid"), pel("Gilda RitaHayworth GlennFord")],
             ["HumphreyBogart", "GlennFord", "IngridBergman"])],
           "Base de datos sin Kevin Bacon: todos los números son INF.",
           {"wa": "Si Kevin Bacon no está en la base de datos, nadie puede conectarse con él: todo INF. Revisa qué haces cuando no lo encuentras (¿lanzas el BFS desde otro actor? ¿id[\"KevinBacon\"] te crea un actor nuevo?).",
            "rte": "Buscar a KevinBacon cuando no existe: con id[\"KevinBacon\"] el map crea una entrada nueva cuyo número no es ningún vértice del grafo."},
           ["Aquí todas las respuestas son INF.",
            "Usa find (o count) para saber si KevinBacon existe; no uses id[\"KevinBacon\"], que lo crea.",
            "Si no existe, contesta INF a todas las consultas sin hacer el BFS (o haciéndolo pero sin usarlo)."])
    prueba("Actores que no pueden llegar a Bacon", "trampa",
           [([pel("Footloose KevinBacon LoriSinger"), pel("Psicosis AnthonyPerkins JanetLeigh"), pel("Vertigo JamesStewart KimNovak JanetLeigh")],
             ["AnthonyPerkins", "KimNovak", "JamesStewart"])],
           "Kevin Bacon está, pero estos actores están en otra parte del grafo: INF.",
           {"wa": "Un actor al que el BFS no llega tiene número INF. Si te sale 0, estás dividiendo la marca de «no visitado» (−1) entre 2: en C++ −1 / 2 vale 0."},
           ["AnthonyPerkins nunca coincide con nadie conectado con Kevin Bacon.",
            "¿Qué valor tiene dist de un vértice no alcanzado? ¿Lo compruebas antes de dividir?",
            "Comprueba primero si dist[v] == −1 y escribe INF; solo si no, escribe dist[v] / 2."])
    prueba("Preguntan por el propio Kevin Bacon", "trampa",
           [([pel("Diner KevinBacon MickeyRourke"), pel("Wild MickeyRourke KevinBacon")], ["KevinBacon", "MickeyRourke"])],
           "Kevin Bacon tiene número 0, aunque haya películas que vuelven a él.",
           {"wa": "El número de Kevin Bacon es 0. Si usas 0 en dist para «no visitado», el BFS vuelve a visitar a Kevin Bacon y le pone otra distancia."},
           ["La primera respuesta debe ser «KevinBacon 0».",
            "No uses 0 como marca de «no visitado»: el origen tiene distancia 0. Usa −1 (o un vector de visitados aparte)."])
    prueba("Cada salto son dos aristas", "trampa",
           [([pel("PeliA KevinBacon Uno"), pel("PeliB Uno Dos"), pel("PeliC Dos Tres"), pel("PeliD Tres Cuatro")],
             ["Uno", "Dos", "Tres", "Cuatro"])],
           "Una cadena de películas: números 1, 2, 3 y 4.",
           {"wa": "Con las películas como vértices, ir de un actor a otro cuesta 2 aristas (actor → película → actor). Si sale el doble, divide la distancia entre 2."},
           ["«Uno» trabajó con Kevin Bacon: su número es 1, no 2.",
            "Si en tu grafo las películas son vértices, el número de Bacon es distancia / 2."])
    prueba("El camino más corto no es el primero que se encuentra", "trampa",
           [([pel("Larga1 KevinBacon Ana"), pel("Larga2 Ana Bea"), pel("Larga3 Bea Carla"), pel("Corta KevinBacon Carla")],
             ["Ana", "Bea", "Carla"])],
           "Ana trabajó con Kevin Bacon (1), aunque también se llega a ella dando la vuelta por Carla y Bea.",
           {"wa": "Un recorrido en profundidad (DFS, o una pila en lugar de una cola) no da distancias mínimas: puede llegar a un actor por un camino largo. Hace falta un BFS."},
           ["Ana tiene número 1: salió en Larga1 con Kevin Bacon.",
            "El DFS no visita por orden de distancia; el BFS sí (con una cola, no una pila).",
            "Usa un BFS con queue: la primera vez que llegas a un vértice es por el camino más corto."])
    prueba("Una película que se llama como un actor", "trampa",
           [([pel("RayCharles JamieFoxx KerryWashington"), pel("ElJuego KevinBacon KerryWashington"), pel("Biopic RayCharles ReginaKing")],
             ["RayCharles", "JamieFoxx", "ReginaKing"])],
           "Hay una película titulada «RayCharles» y también un actor RayCharles: son cosas distintas.",
           {"wa": "Los títulos y los actores son cosas distintas aunque se escriban igual. Si guardas películas y actores en el mismo map por nombre, se mezclan."},
           ["El actor RayCharles solo sale en Biopic, con ReginaKing: no puede llegar a Kevin Bacon.",
            "No metas los títulos en el mismo map que los actores; a las películas basta con darles un número (actores + p)."])
    prueba("Consultas repetidas y actores en muchas películas", "trampa",
           [([pel("Uno KevinBacon Marta"), pel("Dos Marta Nico"), pel("Tres Nico Olga Marta"), pel("Cuatro Olga KevinBacon"),
              pel("Cinco Pablo Olga"), pel("Seis Pablo Nico Marta Quique")],
             ["Quique", "Marta", "Quique", "KevinBacon", "Pablo", "Nico", "Marta"])],
           "Actores que salen en varias películas y la misma consulta repetida: cada respuesta es independiente.",
           {"wa": "Si una consulta repetida cambia de respuesta, algo de una consulta afecta a la siguiente (¿modificas las distancias al contestar? ¿usas id[nombre] y creas actores nuevos?)."},
           ["Quique sale en la consulta 1 y en la 3: las dos respuestas deben ser iguales (2).",
            "Contestar una consulta no debe cambiar nada: solo mira la distancia ya calculada."])
    prueba("Varios casos seguidos", "trampa",
           [([pel("P1 Xavi Yago KevinBacon")], ["Xavi"]),
            ([pel("Q1 Bruno Celia"), pel("Q2 KevinBacon Dario")], ["Bruno", "Dario", "Celia"]),
            ([pel("R1 Elsa"), pel("R2 Fede Gema"), pel("R3 Gema KevinBacon")], ["Elsa", "Fede"])],
           "Tres bases de datos distintas seguidas: nada del caso anterior debe quedar (repartos, nombres, distancias).",
           {"wa": "Algo se arrastra de un caso al siguiente: los repartos, el map de nombres o las distancias están declarados fuera de la función de cada caso y no se vacían."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Declara el map, los repartos y el grafo dentro de la función de cada caso (resize no borra lo que ya había)."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio_pequeno(rng) for _ in range(40)],
           "40 bases de datos pequeñas al azar, con y sin Kevin Bacon.",
           {"wa": "Hay algún caso concreto que no tratas: cuenta en qué caso cae la línea que falla y dibuja sus películas."},
           ["Busca el caso de la línea que falla (cada caso termina en «---») y dibuja el grafo.",
            "Calcula a mano las distancias desde Kevin Bacon en ese caso."])
    # ---- grandes
    todos = [nombre(i) for i in range(99999)]
    reparto = todos + [BACON]
    rng.shuffle(reparto)
    consultas = [rng.choice(reparto) for _ in range(100000)]
    prueba("Una película con 100.000 actores", "rendimiento", [([("Multitudinaria", reparto)], consultas)],
           "Una sola película con el máximo de actores y 100.000 consultas.",
           {"mle": "Unir cada par de actores de una película son k·(k − 1)/2 aristas: con 100.000 actores, 5.000 millones. Mete las películas como vértices.",
            "tle": "O unes cada par de actores de la película (cuadrático) o haces un BFS por consulta. Con un solo BFS desde Kevin Bacon y películas como vértices es lineal."},
           ["¿Cuántas aristas pones para una película de k actores?",
            "Haz que cada película sea un vértice unido a sus actores: k aristas por película.",
            "Haz un único BFS desde Kevin Bacon antes de leer las consultas y contesta cada una mirando su distancia."])
    pelis, sig, prev = [], 0, None
    for p in range(5000):
        r = []
        if p % 250 != 0 and prev is not None:          # cada 250 películas empieza un trozo nuevo
            r.append(rng.choice(prev))
        while len(r) < 20:
            r.append(nombre(sig, "b"))
            sig += 1
        if p == 0:
            r[rng.randrange(20)] = BACON
        rng.shuffle(r)
        pelis.append((nombre(p, "T"), r))
        prev = r
    conocidos = sorted({a for _, r in pelis for a in r})
    consultas = [rng.choice(conocidos) for _ in range(100000)]
    prueba("5.000 películas y 100.000 consultas", "rendimiento", [(pelis, consultas)],
           "El máximo de películas, casi 100.000 actores y 100.000 consultas: cadenas largas de películas.",
           {"tle": "Un BFS por consulta es demasiado: haz uno solo desde Kevin Bacon y guarda las distancias.",
            "mle": "Revisa cuántas aristas pones y que no copias el grafo al pasarlo a funciones."},
           ["Cuenta cuántos BFS haces por caso: debería ser uno.",
            "Calcula todas las distancias desde Kevin Bacon una vez y luego cada consulta es una búsqueda en el map."])
    return [Prueba(nombre_, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(caso_a_salida(c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre_, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("no escribe el separador", [('    cout << "---\\n";', "")], prueba=4, v="wa"),
    Variante("hace el BFS aunque no esté Kevin Bacon",
             [("if (hayBacon && caminos.hayCamino(v))", "if (caminos.hayCamino(v))")], prueba=5, v="wa"),
    Variante("divide −1 entre 2 (no comprueba si hay camino)",
             [("if (hayBacon && caminos.hayCamino(v))", "if (hayBacon)")], prueba=6, v="wa"),
    Variante("usa 0 como «no visitado»",
             [("dist(g.V(), -1) {", "dist(g.V(), 0) {"),
              ("return dist[v] != -1;", "return dist[v] != 0;"),
              ("if (dist[w] == -1) {", "if (dist[w] == 0) {")], prueba=7, v="wa"),
    Variante("no divide entre 2", [("caminos.distancia(v) / 2", "caminos.distancia(v)")], prueba=8, v="wa"),
    Variante("pila en lugar de cola (DFS)",
             [("#include <queue>", "#include <queue>\n#include <stack>"),
              ("queue<int> q;", "stack<int> q;"),
              ("int v = q.front(); q.pop();", "int v = q.top(); q.pop();")], prueba=9, v="wa"),
    Variante("repartos que no se vacían entre casos",
             [("vector<vector<int>> reparto(peliculas);", "static vector<vector<int>> reparto; reparto.resize(peliculas);")], prueba=12, v="wa"),
    Variante("une cada par de actores de la película",
             [("        for (int a : reparto[p])\n            g.ponArista(a, actores + p);",
               "        for (size_t i = 0; i < reparto[p].size(); ++i)\n"
               "            for (size_t j = i + 1; j < reparto[p].size(); ++j) g.ponArista(reparto[p][i], reparto[p][j]);"),
              ("caminos.distancia(v) / 2", "caminos.distancia(v)")], prueba=14, v="mle"),
    Variante("un BFS por consulta",
             [("    CaminosBFS caminos(g, hayBacon ? itBacon->second : 0);   // si no esta, el BFS da igual", ""),
              ("int v = id[actor];", "int v = id[actor];\n        CaminosBFS caminos(g, hayBacon ? itBacon->second : 0);")], prueba=[14, 15], v="tle"),
]
