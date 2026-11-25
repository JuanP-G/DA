"""11-5 · Las vacas pensantes: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso tiene N (1..1.000) y N cantidades distintas (1..10.000) de
izquierda a derecha. Dos vacas se alternan cogiendo uno de los dos extremos; Devoradora siempre
coge el extremo MAYOR. Empieza nuestra vaca.
Salida: lo máximo que puede comer nuestra vaca. La respuesta es única.
El solucionador es propio: recursión con memoria (de arriba abajo) sobre el intervalo que queda,
al revés que la solución del repo (tabla por longitudes). Validado contra fuerza bruta
(todas las partidas posibles) en miles de hileras pequeñas.
"""
import random
import sys
from functools import lru_cache
from _comun import Prueba, Variante

sys.setrecursionlimit(10000)

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-5/EJ_11-5.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["return a[l] > a[r] ? come[l + 1][r] : come[l][r - 1];", "return min(come[l + 1][r], come[l][r - 1]);"],
}


def resuelve(a):
    n = len(a)

    @lru_cache(maxsize=None)
    def yo(i, j):                 # me toca a mí con a[i..j]
        if i > j:
            return 0
        return max(a[i] + ella(i + 1, j), a[j] + ella(i, j - 1))

    @lru_cache(maxsize=None)
    def ella(i, j):               # acabo de comer y le toca a Devoradora con a[i..j]
        if i > j:
            return 0
        return yo(i + 1, j) if a[i] > a[j] else yo(i, j - 1)

    r = yo(0, n - 1)
    yo.cache_clear(); ella.cache_clear()
    return r


def fuerza_bruta(a):
    a = list(a)

    def f(l, r, mia):
        if l > r:
            return 0
        if mia:
            return max(a[l] + f(l + 1, r, False), a[r] + f(l, r - 1, False))
        if a[l] > a[r]:
            return f(l + 1, r, True)
        return f(l, r - 1, True)
    return f(0, len(a) - 1, True)


def _variantes_erroneas(a):
    """Respuestas de las soluciones con fallos típicos (para escoger casos que las distinguen)."""
    n = len(a)

    def voraz():
        l, r, yo, mio = 0, n - 1, 0, True
        while l <= r:
            if mio:
                if a[l] >= a[r]: yo += a[l]; l += 1
                else: yo += a[r]; r -= 1
            else:
                if a[l] > a[r]: l += 1
                else: r -= 1
            mio = not mio
        return yo

    @lru_cache(maxsize=None)
    def minimax(i, j):
        if i > j: return 0
        def tras(l, r):
            if l > r: return 0
            return min(minimax(l + 1, r), minimax(l, r - 1))
        return max(a[i] + tras(i + 1, j), a[j] + tras(i, j - 1))

    @lru_cache(maxsize=None)
    def menor(i, j):
        if i > j: return 0
        def tras(l, r):
            if l > r: return 0
            return menor(l + 1, r) if a[l] < a[r] else menor(l, r - 1)
        return max(a[i] + tras(i + 1, j), a[j] + tras(i, j - 1))

    @lru_cache(maxsize=None)
    def seguidas(i, j):
        if i > j: return 0
        return max(a[i] + seguidas(i + 1, j), a[j] + seguidas(i, j - 1))
    return voraz(), minimax(0, n - 1), menor(0, n - 1), seguidas(0, n - 1)


def _casos_solo_mal_si_devoradora_falla(rng, cuantos):
    """Hileras donde el voraz acierta pero (minimax, extremo menor, jugar seguidas) fallan."""
    ok = []
    while len(ok) < cuantos:
        a = rng.sample(range(1, 30), rng.randint(4, 7))
        v, mm, me, se = _variantes_erroneas(a)
        c = resuelve(tuple(a))
        if v == c and mm != c and me != c and se != c:
            ok.append(a)
    return ok


def texto(casos):
    return f"{len(casos)}\n" + "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in casos)


def salida(casos):
    return "".join(f"{resuelve(tuple(a))}\n" for a in casos)


_r = random.Random(11)
for _ in range(600):
    _a = _r.sample(range(1, 60), _r.randint(1, 11))
    assert resuelve(tuple(_a)) == fuerza_bruta(_a), _a


def pruebas():
    rng = random.Random(1105)
    L = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        for a in casos:
            assert 1 <= len(a) <= 1000 and len(set(a)) == len(a) and all(1 <= x <= 10000 for x in a)
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado", [[8, 7, 1, 4]],
           "8 7 1 4: se empieza por el 8 (Devoradora coge el 7) y luego el 4: 12.",
           {"wa": "Falla el primer ejemplo: Devoradora responde siempre con el extremo MAYOR; compara las dos jugadas posibles con esa respuesta.",
            "pe": "Un entero por caso, en su propia línea."},
           ["Si empiezas por el 4 (derecha), Devoradora coge el 8 y tú llegas a 4 + 7 = 11.",
            "come(i, j) = max(a_i + lo que queda tras la respuesta de Devoradora a (i+1, j), a_j + lo que queda tras su respuesta a (i, j−1)).",
            "Respuesta esperada: 12."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [[2, 4, 15, 5]],
           "2 4 15 5: no conviene coger el mayor extremo (5): empezando por el 2 se llega a 17.",
           {"wa": "Coger siempre el extremo mayor no es óptimo: hay que mirar lo que deja la jugada para después."},
           ["Si coges el 5, Devoradora se queda el 15 y a ti te queda el 4: 9.",
            "Si coges el 2, Devoradora coge el 5 (4 < 5) y te deja el 15 al alcance."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [[6, 11, 3, 15, 9, 4, 12]],
           "La hilera del dibujo (7 cubos): 35.",
           {"wa": "Revisa la recurrencia sobre intervalos: ¿tienes en cuenta el turno de Devoradora después del tuyo?"},
           ["Los primeros movimientos: tú 12, ella 6, tú 11, ella 4.",
            "Después quedan 3 15 9: da igual lo que cojas, Devoradora se lleva el 15 y tú el otro extremo."])

    # ------------------------------------------------------------------ bordes
    prueba("Uno y dos cubos", "borde", [[5], [10000], [3, 8], [8, 3], [1, 2], [10000, 9999]],
           "Hileras mínimas: con un cubo te lo comes tú; con dos eliges el mayor.",
           {"wa": "Con un solo cubo es tuyo; con dos coges el mayor y Devoradora el otro.",
            "rte": "Cuidado con los índices en hileras de 1 o 2 cubos: intervalos vacíos (i > j) valen 0."},
           ["Con 1 cubo, come(i, i) = a_i (lo que queda después es el intervalo vacío).",
            "Con 2 cubos coges el mayor: máx(a_i, a_j)."])
    prueba("Tres cubos", "borde", [[1, 100, 2], [100, 1, 2], [2, 1, 100], [5, 3, 4], [4, 3, 5]],
           "Tres cubos: tras tu jugada Devoradora elige entre dos extremos y a ti te queda el otro.",
           {"wa": "Con tres cubos, tras tu primera jugada Devoradora coge el mayor de los dos extremos restantes y te queda el cubo contrario (o el del medio).",
            "rte": "Revisa los índices al pasar de un intervalo de 3 cubos al de 1."},
           ["En [1, 100, 2]: coges el 2; Devoradora coge el 100; te queda el 1: 3. Si coges el 1, Devoradora coge el 2 y te queda el 100: 101.",
            "Calcula a mano los dos caminos y quédate con el máximo."])

    # ------------------------------------------------------------------ trampas
    prueba("Cómo juega Devoradora", "trampa", _casos_solo_mal_si_devoradora_falla(rng, 5),
           "Hileras pequeñas donde coger el mayor extremo acierta, pero hay que simular bien a Devoradora: tras tu jugada ella coge SIEMPRE el mayor de los extremos que quedan, y luego te toca otra vez a ti.",
           {"wa": "Algo falla al simular a Devoradora: tras TU jugada ella coge el MAYOR de los dos extremos que quedan (no el menor, no «el mejor para ella») y después vuelve a tocarte a ti. Revisa también que rellenas la tabla en un orden en que cada casilla usa casillas ya calculadas."},
           ["Tras tu jugada, el intervalo que queda es (i+1, j) o (i, j−1): ahí Devoradora compara sus dos extremos y se come el mayor.",
            "despues(l, r) = come(l+1, r) si a_l > a_r, y come(l, r−1) si no. Nada de min, y tampoco «a_i + come(i+1, j)» (eso sería jugar dos veces seguidas).",
            "Con la tabla por longitudes crecientes, cada come(i, j) usa solo intervalos más cortos ya calculados."])
    prueba("El mayor de los extremos no siempre conviene", "trampa", [[2, 4, 15, 5], [1, 9, 8, 2], [5, 50, 4, 6, 1]],
           "Un voraz (coger el extremo mayor) da menos: hay que mirar lo que deja la jugada.",
           {"wa": "Coges siempre el extremo mayor: eso es un voraz y falla. Compara las dos jugadas con la tabla."},
           ["En [2, 4, 15, 5], coger el 5 deja a Devoradora el 15: 9. Coger el 2 te deja el 15: 17.",
            "come(i, j) = max(a_i + ..., a_j + ...): prueba las dos opciones en cada paso."])
    prueba("Orden de relleno por longitudes", "trampa", [[5, 3, 7, 4], [10, 1, 3, 2, 9], [2, 9, 4, 8, 1, 3]],
           "La tabla de un intervalo depende de intervalos más cortos: rellenar por filas sin cuidado lee casillas vacías.",
           {"wa": "Rellenas la tabla en un orden en el que una casilla usa otras que aún no has calculado: hay que ir por longitudes crecientes (o por i decreciente y j creciente)."},
           ["come(i, j) usa intervalos con dos cubos menos (i+2, j), (i+1, j−1) o (i, j−2) y con uno menos.",
            "Rellena primero todos los intervalos de longitud 1, luego los de 2, etc."])
    prueba("Nuestra vaca come lo que no coge Devoradora", "trampa", [[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], [1, 10, 2, 9, 3, 8]],
           "Sumar los cubos que te llevas con la jugada de cada intervalo, no restar el total.",
           {"wa": "El total que comes no es «suma de todo menos lo que come Devoradora» salvo que lo calcules con su estrategia fija; revisa que tu recurrencia suma a_i o a_j en tu turno."},
           ["En [1, 2, 3, 4, 5, 6] coges 6 + ... piénsalo turno a turno.",
            "come(i, j) suma lo que comes tú en TU turno y lo que comerás después, no lo de Devoradora."])
    prueba("Varios casos seguidos", "trampa",
           [[rng.randint(1, 10000) for _ in range(1)], rng.sample(range(1, 10001), 30), [1, 5, 2], rng.sample(range(1, 10001), 7)],
           "Un caso mediano y luego otros pequeños: nada del anterior debe quedar en la tabla.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla): créala dentro de resuelveCaso con el tamaño de cada caso.",
            "rte": "La tabla de un caso anterior tenía otro tamaño: créala en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de la función.",
            "Declara la tabla como variable local de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    prueba("Hileras pequeñas al azar", "aleatorio", [rng.sample(range(1, 40), rng.randint(1, 9)) for _ in range(200)],
           "200 hileras de hasta 9 cubos con valores pequeños.",
           {"wa": "Algún caso falla: es pequeño, juega la partida a mano con la estrategia de Devoradora."},
           ["Localiza el caso en la entrada y prueba las dos jugadas iniciales.",
            "Revisa el desempate: las cantidades son distintas, no hay empates."])
    prueba("Hileras medianas al azar", "aleatorio", [rng.sample(range(1, 10001), rng.randint(20, 80)) for _ in range(40)],
           "40 hileras de hasta 80 cubos.",
           {"wa": "Los pequeños salen y estos no: revisa los tamaños de la tabla (N + 2 por lado) y el orden de relleno.",
            "tle": "Una recursión sin memoria crece como 2^N: guarda cada come(i, j) en una tabla."},
           ["¿Calculas el mismo come(i, j) muchas veces? Apúntalo en una tabla.",
            "Tabla (N + 2) × (N + 2) para no salirte con i + 2 o j − 2."])

    # ------------------------------------------------------------------ rendimiento
    prueba("1000 cubos al azar", "rendimiento", [rng.sample(range(1, 10001), 1000)],
           "El tamaño máximo: 1.000 cubos, unas 500.000 casillas útiles.",
           {"tle": "Debe ser O(N²): una recursión sin memoria (2^N) no termina.",
            "mle": "La tabla de 1.000 × 1.000 enteros son 4 MB: no necesitas más.",
            "rte": "Con N = 1000 no uses un array local enorme (pila); usa Matriz o vector."},
           ["¿Cuántas veces calculas el mismo come(i, j)?",
            "Rellena la tabla con dos bucles: O(N²)."])
    prueba("1000 cubos crecientes y decrecientes", "rendimiento",
           [list(range(1, 1001)), list(range(1000, 0, -1)), list(range(1, 2000, 2)), list(range(10000, 9000, -1))],
           "Hileras ordenadas de 1.000 cubos: siempre gana el mismo lado.",
           {"wa": "Con la hilera ordenada Devoradora siempre come de un extremo; revisa que tu tabla tiene en cuenta el orden entre extremos.",
            "tle": "Debe ser O(N²) por caso."},
           ["Con una hilera creciente el extremo mayor siempre es el derecho.",
            "Rellena la tabla por longitudes crecientes: O(N²)."])
    prueba("5 hileras de 1000 cubos", "rendimiento", [rng.sample(range(1, 10001), 1000) for _ in range(5)],
           "Varios casos de tamaño máximo seguidos.",
           {"tle": "Debe ser O(N²) por caso: cinco casos son unos 2,5 millones de casillas.",
            "mle": "Crea la tabla dentro del caso para que se libere al terminar."},
           ["Si un caso tarda mucho, cinco tardan cinco veces más.",
            "Evita copiar la tabla al llamar a una función: pásala por referencia."])
    return L


# ------------------------------------------------------------ variantes (fallos típicos)
VORAZ = """void resuelveCaso() {
    int n0; cin >> n0; deque<int> d(n0);
    for (int& x : d) cin >> x;
    int yo = 0; bool mio = true;
    while (!d.empty()) {
        int v;
        if (mio) { if (d.front() >= d.back()) { v = d.front(); d.pop_front(); } else { v = d.back(); d.pop_back(); } yo += v; }
        else { if (d.front() > d.back()) d.pop_front(); else d.pop_back(); }
        mio = !mio;
    }
    cout << yo << '\\n';
    return;
"""

RECURSIVA = """int rec(vector<int> const& a, int i, int j) {
    if (i > j) return 0;
    int s1 = a[i] + ((i + 1 > j) ? 0 : (a[i + 1] > a[j] ? rec(a, i + 2, j) : rec(a, i + 1, j - 1)));
    int s2 = a[j] + ((i > j - 1) ? 0 : (a[i] > a[j - 1] ? rec(a, i + 1, j - 1) : rec(a, i, j - 2)));
    return max(s1, s2);
}

void resuelveCaso() {
    int n0; cin >> n0; vector<int> w0(n0);
    for (int& x : w0) cin >> x;
    cout << rec(w0, 0, n0 - 1) << '\\n';
    return;
"""

VARIANTES = [
    Variante("voraz: coge siempre el extremo mayor", [("#include <vector>", "#include <vector>\n#include <deque>"), ("void resuelveCaso() {", VORAZ)], prueba=7, v="wa"),
    Variante("Devoradora óptima (minimax)", [("return a[l] > a[r] ? come[l + 1][r] : come[l][r - 1];", "return min(come[l + 1][r], come[l][r - 1]);")], prueba=6, v="wa"),
    Variante("Devoradora coge el extremo menor", [("return a[l] > a[r] ? come[l + 1][r] : come[l][r - 1];", "return a[l] < a[r] ? come[l + 1][r] : come[l][r - 1];")], prueba=6, v="wa"),
    Variante("olvida el turno de Devoradora", [("a[i] + despues(i + 1, j)", "a[i] + come[i + 1][j]"), ("a[j] + despues(i, j - 1)", "a[j] + come[i][j - 1]")], prueba=6, v="wa"),
    Variante("rellena por filas (usa casillas sin calcular)",
             [("    for (int largo = 1; largo <= n; ++largo)\n        for (int i = 1; i + largo - 1 <= n; ++i) {\n            int j = i + largo - 1;",
               "    for (int i = 1; i <= n; ++i)\n        for (int j = i; j <= n; ++j) {")], prueba=6, v="wa"),
    Variante("recursión sin memoria (2^N)", [("void resuelveCaso() {", RECURSIVA)], prueba=[12], v="tle"),
]
