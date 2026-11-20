"""eval-4 · El carpintero Ebanisto: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno L (10..10⁶) y N (1..500) y N marcas 0 < c < L en orden creciente.
Salida: el mínimo esfuerzo para hacer todos los cortes (cortar un trozo cuesta el doble de su longitud).

El solucionador es propio: programación dinámica sobre intervalos con la optimización de Knuth
(la mejor marca del trozo (i, j) está entre la mejor de (i, j−1) y la de (i+1, j)), O(N²) por caso,
distinta de la O(N³) del repo. Se ha validado contra fuerza bruta (todos los órdenes de corte) y
contra la recurrencia O(N³) sin optimizar en miles de casos pequeños.
Con L ≤ 10⁶ y N ≤ 500 el esfuerzo es como mucho 2·L·N ≤ 10⁹: no hay desbordamiento de int posible
dentro de los rangos, así que no hay prueba para eso.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_Eval-4/EJ_Eval-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["esfuerzo[i][j] = 2 * (p[j] - p[i]) + mejor;", "esfuerzo[i][j] = (p[j] - p[i]) + mejor;"],
}


def resuelve(L, marcas):
    p = [0] + list(marcas) + [L]
    P = len(p)
    e = [[0] * P for _ in range(P)]
    opt = [[0] * P for _ in range(P)]
    for d in range(2, P):
        for i in range(P - d):
            j = i + d
            lo, hi = (i + 1, i + 1) if d == 2 else (opt[i][j - 1], opt[i + 1][j])
            ei, mejor, km = e[i], None, 0
            for k in range(lo, hi + 1):
                v = ei[k] + e[k][j]
                if mejor is None or v < mejor:
                    mejor, km = v, k
            e[i][j] = 2 * (p[j] - p[i]) + mejor
            opt[i][j] = km
    return e[0][P - 1]


def cubica(L, marcas):
    p = [0] + list(marcas) + [L]
    P = len(p)
    e = [[0] * P for _ in range(P)]
    for d in range(2, P):
        for i in range(P - d):
            j = i + d
            e[i][j] = 2 * (p[j] - p[i]) + min(e[i][k] + e[k][j] for k in range(i + 1, j))
    return e[0][P - 1]


def fuerza_bruta(L, marcas):
    """Prueba todos los órdenes de corte."""
    import itertools
    mejor = None
    for orden in itertools.permutations(marcas):
        puntos, s = [0, L], 0
        for c in orden:
            a = max(x for x in puntos if x < c)
            b = min(x for x in puntos if x > c)
            s += 2 * (b - a)
            puntos.append(c)
        mejor = s if mejor is None else min(mejor, s)
    return mejor


def aleatorio(rng, nmax, lmax):
    L = rng.randint(10, lmax)
    n = rng.randint(1, min(nmax, L - 1))
    return (L, sorted(rng.sample(range(1, L), n)))


def caso_a_texto(c):
    L, m = c
    return f"{L} {len(m)}\n" + " ".join(map(str, m)) + "\n"


def pruebas():
    rng = random.Random(4004)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [(10, [3, 6, 8])],
           "El tablón de 10 m con marcas en 3, 6 y 8: lo mejor es cortar primero por el 6 (40).",
           {"wa": "Falla el ejemplo: revisa la recurrencia. El primer corte de un trozo cuesta el doble de su longitud, elijas la marca que elijas; luego cada mitad se corta por separado.",
            "pe": "Escribe solo el número, con un salto de línea por caso."},
           ["Haz a mano los tres órdenes que empiezan por cada marca: 3, 6 u 8.",
            "esfuerzo(i, j) = 2·(p_j − p_i) + mínimo de esfuerzo(i, k) + esfuerzo(k, j) para las marcas k entre i y j.",
            "La respuesta es esfuerzo(0, N+1), con p_0 = 0 y p_{N+1} = L."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(20, [8, 10, 15, 17])],
           "El segundo ejemplo del PDF (88).",
           {"wa": "Falla el segundo ejemplo: comprueba que pruebas todas las marcas k de cada trozo, no solo alguna."},
           ["El primer corte bueno es el del 8, no el más centrado.",
            "Para cada trozo hay que probar todas las marcas que tiene dentro y quedarse con la mínima."])
    prueba("El esfuerzo es el doble de la longitud", "trampa", [(1000, [300])],
           "Una sola marca en un tablón de 1000: un único corte que cuesta 2 · 1000 = 2000.",
           {"wa": "Sumas la longitud del trozo y no el doble. Cortar un trozo de longitud x cuesta 2·x."},
           ["Con una sola marca hay un solo corte: ¿cuánto cuesta cortar el tablón entero?",
            "El coste de cortar el trozo (p_i, p_j) es 2·(p_j − p_i)."])
    prueba("Hay que cortar después cada mitad", "trampa", [(10, [8, 9])],
           "Dos marcas: el primer corte (20) y luego el corte de uno de los trozos (4). Total 24.",
           {"wa": "Solo cuentas el primer corte: casi seguro la tabla se rellena en un orden en el que esfuerzo(k, j) aún no está calculado cuando lo usas (vale 0)."},
           ["Si escribes 20, solo cuentas el corte del tablón entero.",
            "esfuerzo(i, j) usa trozos más cortos: rellena la tabla por longitud del trozo (j − i = 2, 3, ...), no por i creciente.",
            "Otra forma: recorre i de mayor a menor y j de menor a mayor; o usa recursión con memoria."])
    prueba("Cortar en el orden de las marcas no sirve", "trampa", [(10, [1, 6, 7])],
           "Cortar de izquierda a derecha (1, 6, 7) cuesta 44; lo mejor es 40.",
           {"wa": "Cortas en el orden en que vienen las marcas. El orden importa: hay que probar todas las marcas como primer corte de cada trozo."},
           ["Compara a mano cortar primero por el 1 o primero por el 6.",
            "No hay un orden fijo bueno: la tabla esfuerzo(i, j) prueba cada marca k del trozo como primer corte."])
    prueba("Cortar por la marca de en medio no siempre es lo mejor", "trampa", [(10, [6, 7, 9])],
           "Cortar siempre por la marca central de la lista (7) cuesta 36; lo mejor es 34, empezando por el 6.",
           {"wa": "Eliges como primer corte la marca que ocupa el centro de la lista: es un voraz y no da el óptimo."},
           ["Prueba a mano a empezar por el 6 y por el 7.",
            "Ninguna regla fija acierta siempre: hay que probar todas las marcas k del trozo y quedarse con la mejor."])
    prueba("Cortar por la marca más cercana al centro tampoco", "trampa", [(10, [3, 4, 6, 8, 9])],
           "Cortar siempre por la marca más cercana a la mitad del trozo no da el óptimo (50).",
           {"wa": "Eliges la marca más cercana a la mitad del trozo: es un voraz y aquí falla. Hace falta la programación dinámica."},
           ["La mitad del tablón es el 5; el 4 y el 6 están igual de cerca, pero ninguno de los dos es lo mejor como primer corte.",
            "Calcula esfuerzo(i, j) para todos los trozos probando todas las marcas k; no decidas por la posición."])
    prueba("Una sola marca", "borde", [(10, [5]), (10, [1]), (1000000, [999999])],
           "Tablones con una sola marca: el esfuerzo es 2·L.",
           {"wa": "Con N = 1 solo hay un corte: el del tablón entero, que cuesta 2·L.",
            "rte": "Con una sola marca te sales de la tabla: revisa los índices de p (0..N+1)."},
           ["La tabla tiene N + 2 puntos: 0, la marca y L.",
            "esfuerzo(0, 2) = 2·(L − 0) + esfuerzo(0, 1) + esfuerzo(1, 2) = 2·L."])
    prueba("Los extremos 0 y L cuentan", "trampa", [(1000000, [1, 2])],
           "Marcas pegadas al principio de un tablón muy largo: el primer corte siempre es del tablón entero (de 0 a L).",
           {"wa": "Te olvidas de los extremos 0 y L: el primer corte cuesta 2·L, y cada trozo va de una marca o un extremo al siguiente."},
           ["Añade a las marcas los puntos 0 (al principio) y L (al final).",
            "p_0 = 0, p_1..p_N las marcas, p_{N+1} = L; la respuesta es esfuerzo(0, N+1)."])
    prueba("Marcas en todos los metros", "borde", [(10, list(range(1, 10))), (12, list(range(1, 12)))],
           "Todas las marcas posibles en tablones cortos.",
           {"wa": "Revisa la recurrencia con trozos de longitud 1 entre marcas seguidas."},
           ["Haz a mano el tablón de 10 con marcas en 1..9 (es largo: compáralo con tu tabla por trozos).",
            "Un trozo entre dos puntos seguidos no tiene marcas y cuesta 0."])
    prueba("Varios casos seguidos", "trampa", [(1000000, sorted(rng.sample(range(1, 1000000), 9))), (10, [3, 6, 8]), (15, [7])],
           "Un caso grande y luego otros pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla o las marcas): créalos dentro de la función de cada caso.",
            "rte": "La tabla de un caso anterior tiene otro tamaño: créala en cada caso con N + 2 puntos."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara la tabla y el vector de puntos dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio(rng, 8, rng.choice([12, 30, 1000])) for _ in range(150)],
           "150 tablones al azar con hasta 8 marcas.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla y hazlo en papel.",
            "Revisa la recurrencia: todas las marcas k del trozo, y el doble de la longitud."])
    prueba("Aleatorios con hasta 12 marcas", "aleatorio", [aleatorio(rng, 12, 1000000) for _ in range(20)],
           "20 tablones largos con hasta 12 marcas.",
           {"wa": "Falla con algo más de marcas: revisa los índices de la tabla.",
            "tle": "Incluso con 12 marcas va lento: la recursión sin memoria repite muchísimo trabajo."},
           ["¿Calculas el mismo esfuerzo(i, j) muchas veces? Apúntalo en una tabla.",
            "Rellena la tabla por longitud de trozo."])
    casos_r = [(1000000, sorted(rng.sample(range(1, 1000000), 500))) for _ in range(4)]
    prueba("500 marcas al azar", "rendimiento", casos_r,
           "Cuatro tablones de 10⁶ con 500 marcas (el máximo).",
           {"tle": "Es lento con 500 marcas. Probar todos los órdenes (N!) o la recursión sin memoria no terminan: guarda esfuerzo(i, j) en una tabla. Con la tabla es O(N³), unos 2·10⁷ pasos por caso.",
            "mle": "La tabla de (N+2)×(N+2) es pequeña: ¿creas tablas o vectores dentro de los bucles?"},
           ["Hay unos N²/2 trozos distintos: calcula cada uno una sola vez.",
            "Rellena esfuerzo(i, j) por longitud de trozo creciente, con tres bucles (longitud, i, k)."])
    prueba("500 marcas seguidas", "rendimiento", [(1000000, list(range(1, 501))), (1000000, list(range(999500, 1000000))), (1000, list(range(1, 501)))],
           "Tres casos con 500 marcas en metros seguidos.",
           {"tle": "Es lento con 500 marcas: la solución debe ser O(N³) como mucho.",
            "wa": "Con muchas marcas el resultado es grande (hasta unos 10⁹): ¿lo guardas en un tipo pequeño?"},
           ["Calcula cada trozo una sola vez, guardado en una tabla.",
            "Tres bucles: longitud del trozo, inicio i y marca k."])
    for c in (c for x in P for c in x[2]):
        L, m = c
        assert 10 <= L <= 1000000 and 1 <= len(m) <= 500 and all(0 < a < L for a in m)
        assert all(m[i] < m[i + 1] for i in range(len(m) - 1))
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d\n" % resuelve(*c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_VORAZ = ("void resuelveCaso() {",
          "long long vz(const vector<long long>& c, int lo, int hi, long long a, long long b) {\n"
          "    if (lo >= hi) return 0;\n    int m = ELIGE;\n"
          "    return 2 * (b - a) + vz(c, lo, m, a, c[m]) + vz(c, m + 1, hi, c[m], b);\n}\n"
          "void resuelveCaso() {\n    int L0, N0; cin >> L0 >> N0; vector<long long> c0(N0);\n"
          "    for (auto& x : c0) cin >> x;\n    cout << vz(c0, 0, N0, 0, L0) << '\\n'; return;\n")

VARIANTES = [
    Variante("sin el doble", [("esfuerzo[i][j] = 2 * (p[j] - p[i]) + mejor;", "esfuerzo[i][j] = (p[j] - p[i]) + mejor;")], prueba=3, v="wa"),
    Variante("rellena la tabla por i creciente",
             [("for (int d = 2; d < P; ++d) {                // d = j - i\n        for (int i = 0; i + d < P; ++i) {\n            int j = i + d;",
               "for (int i = 0; i < P; ++i) {\n        for (int j = i + 2; j < P; ++j) {")], prueba=4, v="wa"),
    Variante("voraz: corta en el orden de las marcas",
             [("void resuelveCaso() {",
               "void resuelveCaso() {\n    int L0, N0; cin >> L0 >> N0; long long s = 0, a = 0;\n"
               "    for (int i = 0; i < N0; ++i) { long long x; cin >> x; s += 2 * (L0 - a); a = x; }\n"
               "    cout << s << '\\n'; return;\n")], prueba=5, v="wa"),
    Variante("voraz: la marca central de la lista", [(_VORAZ[0], _VORAZ[1].replace("ELIGE", "lo + (hi - lo - 1) / 2"))], prueba=6, v="wa"),
    Variante("voraz: la marca más cercana a la mitad",
             [(_VORAZ[0], _VORAZ[1].replace("int m = ELIGE;",
               "int m = lo;\n    for (int k = lo; k < hi; ++k) if (llabs(2 * c[k] - a - b) < llabs(2 * c[m] - a - b)) m = k;"))], prueba=7, v="wa"),
    Variante("recursión sin memoria",
             [("void resuelveCaso() {",
               "long long rec(const vector<long long>& p, int i, int j) {\n    if (j - i < 2) return 0;\n    long long m = -1;\n"
               "    for (int k = i + 1; k < j; ++k) { long long e = rec(p, i, k) + rec(p, k, j); if (m < 0 || e < m) m = e; }\n"
               "    return 2 * (p[j] - p[i]) + m;\n}\n"
               "void resuelveCaso() {\n    int L0, N0; cin >> L0 >> N0; vector<long long> q(N0 + 2, 0);\n"
               "    for (int i = 1; i <= N0; ++i) cin >> q[i];\n    q[N0 + 1] = L0;\n"
               "    cout << rec(q, 0, N0 + 1) << '\\n'; return;\n")], prueba=14, v="tle"),
]
