"""06-3 · Recorriendo el archipiélago en bicicleta: juez con pruebas pensadas para cada error típico.

Cada caso: I (línea), P (línea) y P puentes «isla isla coste» (islas distintas, sin pares repetidos).
Salida: coste del árbol de recubrimiento mínimo, o «No hay puentes suficientes».
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-3/EJ_06-3.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-3/GrafoValorado.h",
                  "6-Conjuntos disjuntos y grafos valorados/EJ_06-3/ConjuntosDisjuntos.h"],
    "limite_ms": 3000,
    "fallo": ["if (!cd.unidos(u, v)) {", "if (true) {"],
}

MENSAJE = "No hay puentes suficientes"


def resuelve(I, puentes):
    """Solucionador independiente: Kruskal con unión-búsqueda propia."""
    padre = list(range(I + 1))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    total = elegidos = 0
    for u, v, c in sorted(puentes, key=lambda p: p[2]):
        a, b = raiz(u), raiz(v)
        if a != b:
            padre[a] = b
            total += c
            elegidos += 1
    return (str(total) if elegidos == I - 1 else MENSAJE) + "\n"


def caso_a_texto(I, puentes):
    return f"{I}\n{len(puentes)}\n" + "".join(f"{u} {v} {c}\n" for u, v, c in puentes)


def aleatorio(rng, I, P, cmax):
    pares = [(u, v) for u in range(1, I + 1) for v in range(u + 1, I + 1)]
    rng.shuffle(pares)
    puentes = []
    for u, v in pares[:min(P, len(pares))]:
        if rng.random() < 0.5:
            u, v = v, u
        puentes.append((u, v, rng.randint(1, cmax)))
    return I, puentes


def grande(rng):
    """10.000 islas y ~100.000 puentes; la isla 10.000 solo se alcanza por el puente más caro."""
    I = 10000
    vistos, puentes = set(), []
    for k in range(2, I):                           # un árbol aleatorio de las islas 1..9.999
        u = rng.randint(1, k - 1)
        vistos.add((u, k))
        puentes.append((k, u, rng.randint(1, 99998)))
    while len(puentes) < 99999:
        u, v = rng.randint(1, I - 1), rng.randint(1, I - 1)
        if u != v and (min(u, v), max(u, v)) not in vistos:
            vistos.add((min(u, v), max(u, v)))
            puentes.append((u, v, rng.randint(1, 99998)))
    puentes.append((I, rng.randint(1, I - 1), 100000))
    rng.shuffle(puentes)
    return I, puentes


def cadena_profunda():
    """Para conjuntos disjuntos sin unión por tamaños ni compresión de caminos: los puentes
    «k k+1» van formando una cadena de 9.999 islas y luego muchas preguntas desde el fondo."""
    I = 10000
    puentes = [(k, k + 1, k) for k in range(1, I - 1)]          # costes 1..9.998, cadena 1..9.999
    m = 0
    extra = []
    while len(extra) < 85000:
        m += 1
        for a in range(1, m):
            extra.append((a, m, 20000 + len(extra)))
    puentes += [(u, v, c) for u, v, c in extra[:85000] if v - u > 1]
    puentes.append((I - 1, I, 100000))
    return I, puentes


def pruebas():
    rng = random.Random(63)
    ej1 = (4, [(1, 2, 5), (1, 3, 10), (2, 4, 7), (1, 4, 8), (3, 4, 2)])
    ej2 = (4, [(1, 2, 3), (2, 4, 5), (4, 1, 8)])
    ej3 = (1, [])
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ej1],
           "El primer ejemplo del PDF: 4 islas y 5 puentes, coste mínimo 14.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (I y P van en líneas distintas), el orden de los puentes o la condición para elegir uno."},
           ["Ejecútalo en tu ordenador con el ejemplo y compara.",
            "Se eligen los puentes 3–4 (2), 1–2 (5) y 2–4 (7): ordénalos por coste y descarta los que unan islas ya unidas.",
            "Es un árbol de recubrimiento de coste mínimo: algoritmo de Kruskal con conjuntos disjuntos."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ej2],
           "El segundo ejemplo: 3 puentes para 4 islas, pero ninguno llega a la isla 3.",
           {"wa": "Cuando no se pueden unir todas las islas hay que escribir exactamente «No hay puentes suficientes» (sin punto final). Que haya I − 1 puentes no basta: tienen que unir islas distintas."},
           ["Cuenta los puentes que ELIGES, no los que hay en la entrada.",
            "Si al acabar Kruskal has elegido menos de I − 1 puentes, las islas no quedan todas unidas."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [ej3],
           "El tercer ejemplo: una sola isla y ningún puente; el coste es 0.",
           {"wa": "Con una sola isla no hace falta ningún puente: la respuesta es 0, no el mensaje.",
            "rte": "Con P = 0 algo se rompe: revisa que no accedes al primer puente de una lista vacía."},
           ["Con I = 1 hacen falta I − 1 = 0 puentes, y ya los tienes.",
            "No uses el coste 0 como señal de «imposible»: aquí 0 es una respuesta válida."])
    prueba("Dos islas y un puente", "borde", [(2, [(2, 1, 100000)]), (2, [(1, 2, 1)])],
           "El archipiélago más pequeño que necesita un puente.",
           {"wa": "Con dos islas y un puente la respuesta es el coste de ese puente."},
           ["Con dos islas hace falta exactamente un puente.",
            "Revisa la condición de parada: hay que llegar a I − 1 = 1 puente elegido."])
    prueba("Ningún puente presupuestado", "borde", [(3, []), (2, [])],
           "Varias islas y P = 0: no se puede.",
           {"wa": "Con varias islas y ningún puente la respuesta es «No hay puentes suficientes».",
            "rte": "Con P = 0 algo se rompe: revisa la lectura y no accedas a puentes que no existen."},
           ["Con I = 3 y P = 0 hacen falta 2 puentes y no hay ninguno.",
            "Tras la línea con P = 0 empieza el caso siguiente."])
    # --- Trampas. El orden importa: las primeras no deben fallar por los errores que buscan las siguientes.
    prueba("Islas numeradas desde 1", "trampa", [(3, [(3, 1, 4), (2, 3, 5)])],
           "Puentes que tocan la isla I: hay que pasar de 1..I a 0..I−1.",
           {"rte": "Usas el número de isla tal cual: la isla I se sale del grafo (o de los conjuntos disjuntos). Lee con GrafoValorado<int>(cin, 1) o resta 1 a cada isla.",
            "wa": "Las islas se desplazan: resta 1 a las dos islas de cada puente."},
           ["El puente «3 1 4» une la última isla con la primera: ¿existe la isla 3 en tu grafo?",
            "Los vértices van de 0 a I − 1: GrafoValorado<int>(cin, 1) resta 1 al leer."])
    prueba("Una isla sola no necesita puentes", "trampa", [(1, []), (2, [(1, 2, 3)])],
           "Con una sola isla el coste es 0 y es una respuesta válida, no el mensaje.",
           {"wa": "Usas «coste == 0» (o «ningún puente elegido») como señal de imposible. Con I = 1 se han elegido I − 1 = 0 puentes: la respuesta es 0."},
           ["¿Qué escribe tu programa con «1» y «0»? Debe ser «0».",
            "La condición correcta es «he elegido I − 1 puentes» (o «queda un solo conjunto»), no «el coste es mayor que 0»."])
    prueba("Puentes en cualquier orden", "trampa",
           [(3, [(1, 2, 50), (1, 3, 40), (2, 3, 1)]), (4, [(1, 2, 9), (1, 3, 8), (1, 4, 7), (2, 3, 1), (3, 4, 2)])],
           "Los puentes no vienen ordenados: hay que elegirlos de menor a mayor coste.",
           {"wa": "No ordenas los puentes por coste creciente (o los ordenas por isla, o de mayor a menor). Kruskal necesita mirarlos de más barato a más caro."},
           ["En el primer caso los puentes buenos son 2–3 (1) y 1–3 (40): total 41.",
            "Ordena las aristas por su valor: sort(v.begin(), v.end()) con Arista ya compara por valor.",
            "Si guardas tuplas (isla, isla, coste), ordénalas por el coste, no por la primera isla."])
    prueba("Un puente barato que cerraría un ciclo", "trampa",
           [(4, [(1, 2, 1), (2, 3, 2), (1, 3, 3), (3, 4, 10)]), (5, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (4, 5, 2), (1, 4, 9), (5, 3, 9)])],
           "Un puente entre dos islas que ya están unidas no hace falta, aunque sea barato.",
           {"wa": "Eliges puentes que cierran un ciclo: antes de elegir uno, comprueba que sus islas no están ya unidas (cd.unidos)."},
           ["En el primer caso el puente 1–3 (3) sobra: 1 y 3 ya están unidas por 1–2–3. Total: 1 + 2 + 10 = 13.",
            "Elige el puente solo si !unidos(u, v); después, unir(u, v)."])
    prueba("Faltan puentes (P < I − 1)", "trampa", [(5, [(1, 2, 4), (3, 4, 4)]), (6, [(1, 2, 1), (2, 3, 1), (3, 1, 1)])],
           "Muy pocos puentes para tantas islas: «No hay puentes suficientes».",
           {"wa": "Escribes el coste aunque no se hayan podido unir todas las islas: comprueba al final que has elegido I − 1 puentes."},
           ["Con 5 islas hacen falta al menos 4 puentes.",
            "Tras Kruskal: si elegidos == I − 1, el coste; si no, el mensaje (exactamente «No hay puentes suficientes»)."])
    prueba("Puentes de sobra, pero una isla queda aislada", "trampa",
           [(4, [(1, 2, 3), (2, 3, 4), (3, 1, 5)]),
            (5, [(1, 2, 1), (1, 3, 1), (1, 4, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1)])],
           "Hay al menos I − 1 puentes en la entrada, pero no llegan a todas las islas.",
           {"wa": "Compruebas si hay I − 1 puentes en la ENTRADA en vez de cuántos has ELEGIDO. Los que cierran ciclo no cuentan."},
           ["En el primer caso hay 3 puentes para 4 islas, pero los tres unen 1, 2 y 3: la isla 4 queda fuera.",
            "Cuenta los puentes elegidos por Kruskal (o mira num_cjtos() == 1)."])
    prueba("Varios puentes con el mismo coste", "trampa",
           [(4, [(1, 2, 7), (2, 3, 7), (3, 4, 7), (4, 1, 7), (1, 3, 7)]), (3, [(1, 2, 5), (2, 3, 5)])],
           "Puentes que empatan en coste: todos cuentan, ninguno se pierde.",
           {"wa": "Pierdes puentes con el mismo coste: ¿los guardas en un set o un map por coste? Dos puentes distintos pueden costar lo mismo."},
           ["En el primer caso hacen falta 3 puentes de coste 7: total 21.",
            "Guarda los puentes en un vector y ordénalo; un set<Arista> (que compara por valor) descarta los empates."])
    prueba("Costes máximos (total cerca de 10⁹)", "borde",
           [(10000, [(k + 1, k, 100000) for k in range(1, 10000)])],
           "10.000 islas en fila con puentes de 100.000: el total es 999.900.000.",
           {"wa": "La suma llega a casi 10⁹: cabe en un int, pero no en tipos más pequeños. Revisa también que no te paras antes de tiempo.",
            "tle": "Con 10.000 islas en fila algo es demasiado lento: ¿tus conjuntos disjuntos usan unión por tamaños y compresión de caminos?"},
           ["Son 9.999 puentes de 100.000: 999.900.000.",
            "Acumula el coste en un int (o long long) y no pares hasta tener I − 1 puentes."])
    prueba("Varios casos seguidos", "trampa",
           [(4, [(1, 2, 100), (2, 3, 100), (3, 4, 100)]), (3, [(1, 2, 1), (2, 3, 2)]), (2, []), (1, []), (3, [(3, 1, 4), (2, 1, 4)])],
           "Un caso caro seguido de otros pequeños: ni el coste ni los conjuntos del anterior deben quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el coste, el contador de puentes o la partición se declaran fuera de resuelveCaso (o como static).",
            "rte": "Un vector de un caso anterior con otro tamaño: crea el grafo y los conjuntos disjuntos dentro de cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "El coste y el número de puentes elegidos deben empezar en 0 en cada caso."])
    casos_al = [aleatorio(rng, rng.randint(1, 7), rng.randint(0, 12), rng.choice([3, 10, 100000])) for _ in range(100)]
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "100 archipiélagos pequeños al azar, conexos y no conexos, con muchos empates.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; búscalo y haz Kruskal a mano."},
           ["La línea que falla es el número de caso: busca ese archipiélago en la entrada.",
            "Ordena sus puentes a mano y ve eligiendo los que unen islas aún separadas."])
    prueba("Archipiélago grande con un puente caro imprescindible", "rendimiento", [grande(rng)],
           "10.000 islas y 100.000 puentes; la última isla solo se alcanza por el puente más caro, así que hay que mirarlos todos.",
           {"tle": "Tu solución no es O(P log P): ¿buscas el puente más barato recorriendo todos en cada paso, o llamas a g.aristas() (que crea un vector nuevo) dentro del bucle? Ordena una vez y recorre.",
            "mle": "Gastas demasiada memoria: no copies el vector de puentes ni uses matrices I × I."},
           ["Ordena los puentes UNA vez (O(P log P)) y recórrelos en ese orden.",
            "Guarda g.aristas() en una variable antes del bucle: cada llamada crea un vector nuevo con todos los puentes.",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    prueba("Cadena larga de islas", "rendimiento", [cadena_profunda()],
           "Los puentes baratos forman una fila de 10.000 islas y después hay muchos puentes que sobran entre islas del principio.",
           {"tle": "Tus conjuntos disjuntos forman árboles muy altos: usa unión por tamaños y compresión de caminos (como ConjuntosDisjuntos.h).",
            "rte": "La búsqueda recursiva baja demasiado: con unión por tamaños la altura es como mucho log I."},
           ["Sin unión por tamaños, unir la fila isla a isla deja una cadena: buscar el representante cuesta I pasos.",
            "Usa la clase ConjuntosDisjuntos de la asignatura (unión por tamaños y compresión de caminos)."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(*c) for c in casos),
                   salida="".join(resuelve(*c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


INGENUA = """class ConjuntosDisjuntos {
    std::vector<int> p; int n;
public:
    ConjuntosDisjuntos(int N) : p(N), n(N) { for (int i = 0; i < N; ++i) p[i] = i; }
    int buscar(int a) const { while (p[a] != a) a = p[a]; return a; }
    void unir(int a, int b) { int i = buscar(a), j = buscar(b); if (i != j) { p[i] = j; --n; } }
    bool unidos(int a, int b) const { return buscar(a) == buscar(b); }
    int num_cjtos() const { return n; }
};"""

VARIANTES = [
    Variante("no resta 1 a las islas", [("GrafoValorado<int> g(cin, 1);", "GrafoValorado<int> g(cin, 0);")], prueba=6, v="rte"),
    Variante("coste 0 como señal de imposible", [("if (elegidos == g.V() - 1) cout << coste << '\\n';", "if (coste > 0 && elegidos == g.V() - 1) cout << coste << '\\n';")], prueba=7, v="wa"),
    Variante("no ordena los puentes", [("sort(puentes.begin(), puentes.end());", "")], prueba=8, v="wa"),
    Variante("ordena por isla en vez de por coste", [("sort(puentes.begin(), puentes.end());",
                                                      "sort(puentes.begin(), puentes.end(), [](Arista<int> const& a, Arista<int> const& b) { return a.uno() < b.uno(); });")], prueba=8, v="wa"),
    Variante("no comprueba si ya estaban unidas", [("if (!cd.unidos(u, v)) {", "if (true) {")], prueba=9, v="wa"),
    Variante("nunca escribe el mensaje", [("if (elegidos == g.V() - 1) cout << coste << '\\n';\n    else cout << \"No hay puentes suficientes\\n\";", "cout << coste << '\\n';")], prueba=10, v="wa"),
    Variante("cuenta los puentes de la entrada", [("if (elegidos == g.V() - 1) cout << coste << '\\n';", "if (g.A() >= g.V() - 1) cout << coste << '\\n';")], prueba=11, v="wa"),
    Variante("guarda los puentes en un set", [("auto puentes = g.aristas();\n    sort(puentes.begin(), puentes.end());",
                                               "set<Arista<int>> conj; for (auto const& a : g.aristas()) conj.insert(a);\n    vector<Arista<int>> puentes(conj.begin(), conj.end());"),
                                              ("#include <algorithm>", "#include <algorithm>\n#include <set>")], prueba=12, v="wa"),
    Variante("coste acumulado entre casos", [("long long coste = 0;", "static long long coste = 0;")], prueba=14, v="wa"),
    Variante("llama a g.aristas() en cada vuelta", [("for (auto const& p : puentes) {", "for (size_t k = 0; k < g.aristas().size(); ++k) {\n        auto const& p = puentes[k];")], prueba=16, v="tle"),
    Variante("busca el más barato en cada paso", [("for (auto const& p : puentes) {\n",
                                                   "while (elegidos < g.V() - 1) {\n        int mejor = -1;\n        for (int k = 0; k < (int)puentes.size(); ++k) { int a = puentes[k].uno(), b = puentes[k].otro(a); if (!cd.unidos(a, b) && (mejor < 0 || puentes[k].valor() < puentes[mejor].valor())) mejor = k; }\n        if (mejor < 0) break;\n        auto const& p = puentes[mejor];\n"),
                                                  ("sort(puentes.begin(), puentes.end());", "")], prueba=16, v="tle"),
    Variante("conjuntos disjuntos sin optimizar", [('#include "ConjuntosDisjuntos.h"  // estructuras de datos de clase', INGENUA)], prueba=17, v="tle"),
]
