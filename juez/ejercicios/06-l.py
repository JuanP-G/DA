"""06-L · ¿Dónde construimos los aeropuertos?: juez con pruebas pensadas para cada error típico.

Cada caso: «N M A» y M carreteras «X Y C» (X ≠ Y, puede haber varias entre el mismo par).
Salida: «coste aeropuertos», el coste mínimo y, entre las de coste mínimo, la que más aeropuertos tiene.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-L/EJ_06-L.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-L/GrafoValorado.h",
                  "6-Conjuntos disjuntos y grafos valorados/EJ_06-L/ConjuntosDisjuntos.h"],
    "limite_ms": 3000,
    "fallo": ["if (c.valor() >= A) break;", "if (c.valor() > A) break;"],
}


def resuelve(N, A, carreteras):
    """Solucionador independiente: vértice 0 «cielo» unido a cada localidad con una arista de
    coste A (el aeropuerto). Árbol de recubrimiento mínimo de N + 1 vértices; en caso de empate
    se prefieren los aeropuertos (van antes que las carreteras del mismo coste)."""
    aristas = [(A, 0, 0, i) for i in range(1, N + 1)] + [(c, 1, x, y) for x, y, c in carreteras]
    aristas.sort(key=lambda a: (a[0], a[1]))
    padre = list(range(N + 1))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    coste = aeropuertos = 0
    for c, es_carretera, x, y in aristas:
        a, b = raiz(x), raiz(y)
        if a != b:
            padre[a] = b
            coste += c
            aeropuertos += 1 - es_carretera
    return f"{coste} {aeropuertos}\n"


def caso_a_texto(N, A, carreteras):
    return f"{N} {len(carreteras)} {A}\n" + "".join(f"{x} {y} {c}\n" for x, y, c in carreteras)


def aleatorio(rng, N, M, A, cmax):
    cs = []
    for _ in range(M if N > 1 else 0):
        x = rng.randint(1, N)
        y = rng.randint(1, N - 1)
        if y >= x:
            y += 1
        cs.append((x, y, rng.randint(1, cmax)))
    return N, A, cs


def grande(rng):
    """10.000 localidades y 100.000 carreteras, todas más baratas que un aeropuerto salvo unas pocas."""
    N, A = 10000, 100000
    cs = []
    for _ in range(99000):
        x = rng.randint(1, N)
        y = rng.randint(1, N - 1)
        if y >= x:
            y += 1
        cs.append((x, y, rng.randint(1, 99999)))
    for _ in range(1000):
        x = rng.randint(1, N)
        y = rng.randint(1, N - 1)
        if y >= x:
            y += 1
        cs.append((x, y, rng.randint(99990, 100000)))
    rng.shuffle(cs)
    return N, A, cs


def cadena_profunda():
    """Para conjuntos disjuntos sin unión por tamaños ni compresión: las carreteras «k k+1»
    forman una cadena de 9.999 localidades y luego muchas que sobran entre las del principio."""
    N, A = 10000, 100000
    cs = [(k, k + 1, k) for k in range(1, N - 1)]
    extra, m = [], 0
    while len(extra) < 85000:
        m += 1
        for a in range(1, m - 1):
            extra.append((a, m, 10000 + len(extra)))
    cs += extra[:85000]
    cs.append((N - 1, N, 99999))
    return N, A, cs


def pruebas():
    rng = random.Random(66)
    ej1 = (4, 100, [(1, 2, 10), (2, 3, 30), (4, 1, 40), (4, 3, 20)])
    ej2 = (5, 1000, [(4, 5, 10), (1, 2, 20), (3, 2, 30)])
    ej3 = (3, 50, [(1, 2, 20), (2, 3, 50), (1, 3, 80)])
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ej1],
           "El primer ejemplo del PDF: todas las carreteras cuestan menos que un aeropuerto; «160 1».",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura («N M A» en la misma línea), el orden de la salida (primero el coste y luego los aeropuertos) o la idea de Kruskal.",
            "pe": "Los números están bien pero el formato no: coste y aeropuertos en la misma línea, separados por un espacio."},
           ["Ejecútalo en tu ordenador con el ejemplo y compara.",
            "Se construyen las carreteras de 10, 20 y 30 (la de 40 cerraría un ciclo) y un aeropuerto: 60 + 100.",
            "Kruskal sobre las carreteras y un aeropuerto por cada grupo de localidades que quede."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ej2],
           "El segundo ejemplo: dos grupos de localidades sin carretera entre ellos; «2060 2».",
           {"wa": "Cada grupo de localidades que no se puede unir por carretera necesita su propio aeropuerto: el número de aeropuertos es el número de conjuntos que quedan."},
           ["Las localidades {1, 2, 3} y {4, 5} no se unen con ninguna carretera.",
            "Al acabar Kruskal, aeropuertos = num_cjtos()."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [ej3],
           "El tercer ejemplo: una carretera cuesta lo mismo que un aeropuerto y otra más; «120 2».",
           {"wa": "Una carretera que cuesta igual que un aeropuerto NO se construye: a igual coste se prefieren más aeropuertos. Y una más cara, nunca."},
           ["Construir la carretera de 50 y un aeropuerto cuesta lo mismo que dos aeropuertos: gana la opción con más aeropuertos.",
            "Solo compensa una carretera si su coste es estrictamente menor que A."])
    prueba("Una sola localidad", "borde", [(1, 7, []), (1, 100000, [])],
           "Con una localidad hace falta un aeropuerto y ninguna carretera: «A 1».",
           {"wa": "Con N = 1 la respuesta es el coste de un aeropuerto y 1 aeropuerto."},
           ["¿Qué escribe tu programa con «1 0 7»? Debe ser «7 1».",
            "Cada grupo (aquí, uno) lleva su aeropuerto."])
    prueba("Ninguna carretera posible", "borde", [(3, 10, []), (2, 1, [])],
           "Sin carreteras, cada localidad necesita su aeropuerto: «N·A N».",
           {"wa": "Sin carreteras hay N grupos y N aeropuertos.",
            "rte": "Con M = 0 algo se rompe: tras la línea «N 0 A» empieza el caso siguiente."},
           ["Con 3 localidades, M = 0 y A = 10 la respuesta es «30 3».",
            "num_cjtos() empieza valiendo N."])
    # --- Trampas. El orden importa: las primeras no deben fallar por los errores que buscan las siguientes.
    prueba("Localidades numeradas desde 1", "trampa", [(2, 10, [(2, 1, 5)])],
           "Una carretera que toca la localidad N: hay que pasar de 1..N a 0..N−1.",
           {"rte": "Usas el número de localidad tal cual: la localidad N se sale del grafo. Resta 1 a X y a Y.",
            "wa": "Las localidades se desplazan: resta 1 a las dos localidades de cada carretera."},
           ["La carretera «2 1 5» toca la última localidad: ¿existe el vértice 2 en tu grafo?",
            "Al poner la arista, usa x − 1 e y − 1."])
    prueba("Cada grupo necesita su aeropuerto", "trampa",
           [(4, 10, [(1, 2, 1), (3, 4, 1)]), (5, 3, [(1, 2, 1)])],
           "Si quedan varios grupos de localidades, hace falta un aeropuerto en cada uno.",
           {"wa": "El número de aeropuertos no es siempre 1: es el número de grupos que quedan al acabar (num_cjtos())."},
           ["En el primer caso quedan {1, 2} y {3, 4}: dos aeropuertos, «22 2».",
            "aeropuertos = cd.num_cjtos(); coste += aeropuertos · A."])
    prueba("Carretera más cara que un aeropuerto", "trampa",
           [(2, 10, [(1, 2, 11)]), (3, 100, [(1, 2, 30), (2, 3, 500)])],
           "Si una carretera cuesta más que un aeropuerto, sale más barato poner otro aeropuerto.",
           {"wa": "Construyes todas las carreteras del árbol de recubrimiento. Una carretera de coste C ahorra un aeropuerto de coste A: solo compensa si C < A."},
           ["En el primer caso: dos aeropuertos (20) son más baratos que la carretera y uno (21).",
            "Recorre las carreteras por coste creciente y para (o sáltatelas) en cuanto C ≥ A."])
    prueba("Carretera que cuesta lo mismo que un aeropuerto", "trampa",
           [(2, 10, [(1, 2, 10)]), (4, 7, [(1, 2, 3), (2, 3, 7), (3, 4, 6)])],
           "Empate: construir la carretera cuesta lo mismo que el aeropuerto que ahorra, y se prefieren más aeropuertos.",
           {"wa": "Construyes las carreteras con C = A. Con el mismo coste total, el enunciado pide la opción con MÁS aeropuertos: la condición es C < A, estricta."},
           ["En el primer caso, carretera + un aeropuerto = 20 = dos aeropuertos: la respuesta es «20 2».",
            "Cambia C ≤ A por C < A (o para con C ≥ A)."])
    prueba("Carreteras en cualquier orden", "trampa",
           [(3, 100, [(1, 2, 200), (2, 3, 5)]), (3, 100, [(1, 2, 50), (1, 3, 40), (2, 3, 1)])],
           "Las carreteras no vienen ordenadas: hay que mirarlas de la más barata a la más cara.",
           {"wa": "No ordenas las carreteras por coste (o paras al ver la primera cara sin haberlas ordenado). Kruskal necesita mirarlas de menor a mayor coste."},
           ["En el primer caso la carretera de 200 va primero, pero la de 5 sí compensa: «205 2».",
            "Ordena las aristas por su valor antes del bucle."])
    prueba("Carretera que cerraría un ciclo", "trampa",
           [(3, 100, [(1, 2, 10), (2, 3, 20), (1, 3, 30)]), (4, 50, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (3, 4, 2), (4, 2, 3)])],
           "Una carretera entre dos localidades ya comunicadas no hace falta, aunque sea barata.",
           {"wa": "Construyes carreteras que cierran un ciclo: antes de construir una, comprueba que sus localidades no están ya unidas."},
           ["En el primer caso la carretera 1–3 (30) sobra: 1 y 3 ya se comunican por 2. «130 1».",
            "Construye solo si !unidos(x, y); después, unir(x, y)."])
    prueba("Varias carreteras entre las mismas localidades", "trampa",
           [(2, 50, [(1, 2, 90), (2, 1, 10)]), (3, 100, [(1, 2, 5), (2, 3, 80), (3, 2, 7), (2, 1, 99)])],
           "Puede haber varias carreteras posibles entre dos localidades: vale la más barata.",
           {"wa": "Guardas una sola carretera por par de localidades (la primera o la última que lees). Guárdalas todas: Kruskal se queda con la más barata."},
           ["En el primer caso la carretera de 10 compensa (10 < 50): «60 1».",
            "Con listas de aristas no tienes que hacer nada especial: la más barata se mira antes."])
    prueba("Coste total de 10⁹", "borde",
           [(10000, 100000, []), (10000, 100000, [(k, k + 1, 99999) for k in range(1, 10000)])],
           "Los valores más grandes: 10.000 aeropuertos de 100.000 (10⁹), o 9.999 carreteras de 99.999 y un aeropuerto.",
           {"wa": "Con valores grandes algo falla: el coste llega a 10⁹ (cabe en int, justo); revisa el tipo y las multiplicaciones (aeropuertos · A)."},
           ["10.000 · 100.000 = 1.000.000.000.",
            "Si usas int para el coste vale, pero no multipliques en un tipo más pequeño; long long es lo más seguro."])
    prueba("Varios casos seguidos", "trampa",
           [(4, 100, [(1, 2, 10), (2, 3, 10), (3, 4, 10)]), (2, 5, [(1, 2, 9)]), (1, 3, []), (3, 1, [(1, 2, 1)])],
           "Un caso caro seguido de otros pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el coste o la partición se declaran fuera de resuelveCaso (o como static).",
            "rte": "Un vector de un caso anterior con otro tamaño: crea el grafo y los conjuntos disjuntos en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "El coste tiene que empezar en 0 en cada caso."])
    casos_al = []
    for _ in range(120):
        A = rng.randint(1, 12)
        casos_al.append(aleatorio(rng, rng.randint(1, 7), rng.randint(0, 12), A, 15))
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "120 casos pequeños al azar, con muchas carreteras que cuestan justo lo mismo que un aeropuerto.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; búscalo y haz Kruskal a mano."},
           ["La línea que falla es el número de caso: búscalo en la entrada.",
            "Ordena sus carreteras, construye las que unan grupos distintos y cuesten menos que A, y cuenta los grupos."])
    prueba("Región grande con casi todas las carreteras baratas", "rendimiento", [grande(rng)],
           "10.000 localidades y 100.000 carreteras, casi todas más baratas que un aeropuerto: hay que recorrerlas casi todas.",
           {"tle": "Tu solución no es O(M log M): ¿llamas a g.aristas() (que crea un vector nuevo) dentro del bucle, o cuentas los grupos recorriendo todas las localidades en cada vuelta?",
            "mle": "Gastas demasiada memoria: no copies el vector de carreteras ni uses matrices N × N."},
           ["Ordena las carreteras UNA vez y recórrelas en ese orden.",
            "num_cjtos() da el número de grupos en O(1).",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    prueba("Cadena larga de localidades", "rendimiento", [cadena_profunda()],
           "Las carreteras baratas forman una fila de 10.000 localidades y después hay muchas que sobran entre las del principio.",
           {"tle": "Tus conjuntos disjuntos forman árboles muy altos: usa unión por tamaños y compresión de caminos (como ConjuntosDisjuntos.h).",
            "rte": "La búsqueda recursiva baja demasiado: con unión por tamaños la altura es como mucho log N."},
           ["Sin unión por tamaños, unir la fila localidad a localidad deja una cadena: buscar el representante cuesta N pasos.",
            "Usa la clase ConjuntosDisjuntos de la asignatura."])
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
    Variante("no resta 1 a las localidades", [("g.ponArista({x - 1, y - 1, c});", "g.ponArista({x, y, c});")], prueba=6, v="rte"),
    Variante("construye todas las carreteras del árbol", [("if (c.valor() >= A) break;", "")], prueba=8, v="wa"),
    Variante("construye también con C = A", [("if (c.valor() >= A) break;", "if (c.valor() > A) break;")], prueba=9, v="wa"),
    Variante("no ordena las carreteras", [("sort(carreteras.begin(), carreteras.end());", "")], prueba=10, v="wa"),
    Variante("no comprueba si ya estaban unidas", [("if (!cd.unidos(u, v)) {", "if (true) {")], prueba=11, v="wa"),
    Variante("un solo aeropuerto", [("int aeropuertos = cd.num_cjtos();", "int aeropuertos = 1;")], prueba=7, v="wa"),
    Variante("coste acumulado entre casos", [("long long coste = 0;", "static long long coste = 0;")], prueba=14, v="wa"),
    Variante("llama a g.aristas() en cada vuelta", [("for (auto const& c : carreteras) {", "for (size_t k = 0; k < g.aristas().size(); ++k) {\n        auto const& c = carreteras[k];")], prueba=16, v="tle"),
    Variante("conjuntos disjuntos sin optimizar", [('#include "ConjuntosDisjuntos.h"  // estructuras de datos de clase', INGENUA)], prueba=17, v="tle"),
]
