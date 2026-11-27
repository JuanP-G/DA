"""12-4 · Mejor no llevar muchas monedas: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso: N, N valores, N cantidades y el precio P.
Salida: «SI k1 … kN» con el menor número de monedas, o «NO». Hay empates: se usa comprobador
(comprobadores/12-4.py y .js) y ALTERNATIVA da otra solución óptima.
El solucionador es propio: troceado binario de cada tipo en paquetes (mochila 0/1) y reconstrucción
por decisiones guardadas. Validado contra fuerza bruta.
"""
import itertools
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-4/EJ_12-4.cpp",
    "cabeceras": ["12-Evaluacion/EJ_12-4/EnterosInf.h", "12-Evaluacion/EJ_12-4/Matriz.h"],
    "limite_ms": 4000,
    "fallo": ["k <= c[i] && k * v[i] <= j", "k * v[i] <= j"],
}
INF = 10**9


def resuelve(v, c, P, alt=False):
    paquetes = []
    orden = range(len(v) - 1, -1, -1) if alt else range(len(v))
    for i in orden:
        quedan, t = min(c[i], P // v[i]), 1
        while quedan:
            k = min(t, quedan)
            paquetes.append((i, k, k * v[i]))
            quedan -= k
            t *= 2
    mejor = [0] + [INF] * P
    usa = []
    for i, k, peso in paquetes:
        cand = mejor[:P + 1 - peso]
        nuevo = mejor[:]
        marca = bytearray(P + 1)
        for j, x in enumerate(cand, peso):
            if x + k < nuevo[j]:
                nuevo[j] = x + k
                marca[j] = 1
        mejor = nuevo
        usa.append(marca)
    if mejor[P] >= INF:
        return None
    res, j = [0] * len(v), P
    for (i, k, peso), marca in zip(reversed(paquetes), reversed(usa)):
        if marca[j]:
            res[i] += k
            j -= peso
    assert j == 0
    return res


def _bruta(v, c, P):
    ops = [sum(k) for k in itertools.product(*[range(x + 1) for x in c]) if sum(a * b for a, b in zip(k, v)) == P]
    return min(ops) if ops else None


_r = random.Random(4)
for _ in range(1500):
    _n = _r.randint(1, 4)
    _v = [_r.randint(1, 12) for _ in range(_n)]
    _c = [_r.randint(1, 4) for _ in range(_n)]
    _P = _r.randint(1, 40)
    _s = resuelve(_v, _c, _P)
    assert (None if _s is None else sum(_s)) == _bruta(_v, _c, _P), (_v, _c, _P)


def texto(casos):
    return f"{len(casos)}\n" + "".join(
        f"{len(v)}\n{' '.join(map(str, v))}\n{' '.join(map(str, c))}\n{P}\n" for v, c, P in casos)


def salida(casos, alt=False):
    t = ""
    for v, c, P in casos:
        s = resuelve(v, c, P, alt)
        t += "NO\n" if s is None else "SI " + " ".join(map(str, s)) + "\n"
    return t


def ALTERNATIVA(entrada):
    d = iter(map(int, entrada.split()))
    casos = []
    for _ in range(next(d)):
        n = next(d)
        v = [next(d) for _ in range(n)]
        c = [next(d) for _ in range(n)]
        casos.append((v, c, next(d)))
    return salida(casos, alt=True)


def pruebas():
    r = random.Random(124)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    def al_azar(n, vmax, cmax, P):
        return ([r.randint(1, vmax) for _ in range(n)], [r.randint(1, cmax) for _ in range(n)], P)

    p("Ejemplo del enunciado", "enunciado",
      [([1, 5, 10, 50], [10, 2, 5, 4], 260), ([1, 10, 100], [3, 2, 2], 114), ([15, 10, 5], [2, 2, 2], 20)],
      "Los tres casos del PDF.",
      {"wa": "Falla el ejemplo: mínimo de monedas respetando cuántas hay de cada tipo.",
       "pe": "SI y los N números separados por un espacio, en el orden de la entrada."},
      ["monedas(i, j) = min_k monedas(i−1, j − k·v_i) + k, con k ≤ c_i.", "Escribe también los ceros."])
    p("Un solo tipo", "borde", [([5], [3], 15), ([5], [3], 20), ([5], [3], 7), ([1], [1], 1), ([1000], [1000], 10000)],
      "Con un tipo hace falta que P sea múltiplo y que haya bastantes.",
      {"wa": "Comprueba P % v = 0 y P / v ≤ c.", "rte": "Revisa los índices con N = 1."},
      ["20 con tres monedas de 5 es NO.", "monedas(0, j > 0) = +Inf."])
    p("No hay monedas suficientes", "trampa", [([1, 10], [3, 5], 14), ([7], [2], 21), ([2, 5], [2, 1], 11), ([3, 4], [1, 1], 8)],
      "Las cantidades son limitadas.",
      {"wa": "No puedes usar más monedas de un tipo de las que hay: k ≤ c_i."},
      ["No es el cambio con monedas ilimitadas.", "Usa la fila anterior, no la misma."])
    p("El voraz falla", "trampa", [([15, 10], [1, 2], 20), ([25, 10, 1], [4, 4, 10], 30), ([9, 6, 1], [3, 3, 20], 12)],
      "Coger primero la mayor no sirve.",
      {"wa": "Un voraz no es óptimo: hay que probar cuántas monedas de cada tipo usar."},
      ["20 = 10 + 10, no 15 + ...", "Programación dinámica."])
    p("El menor número de monedas", "trampa", [([1, 5], [100, 10], 50), ([1, 2, 50], [50, 25, 1], 50), ([2, 3, 6], [10, 10, 10], 18)],
      "No vale cualquier forma de pagar.",
      {"wa": "Quédate con el mínimo número de monedas, no con la primera combinación que sume P."},
      ["Compara todas las k.", "min, no el primero que no sea infinito."])
    p("Precio imposible y posible", "trampa", [([4, 6], [100, 100], 9), ([4, 6], [100, 100], 10), ([10], [1], 1)],
      "NO cuando la casilla queda en infinito.", {"wa": "Si monedas(N, P) es +Inf se escribe NO.", "rte": "No reconstruyas si no hay solución."},
      ["Comprueba antes de reconstruir.", "Infinito + k sigue siendo infinito."])
    p("Varios casos seguidos", "trampa", [al_azar(8, 50, 10, 400), ([2], [1], 2), ([3], [1], 2), al_azar(3, 10, 10, 30)],
      "Casos de tamaños distintos.", {"wa": "Crea la tabla en cada caso.", "rte": "Los tamaños cambian entre casos."},
      ["Declara todo en resuelveCaso.", "Tabla (N+1) × (P+1)."])
    p("Casos pequeños al azar", "aleatorio", [al_azar(r.randint(1, 5), 20, 6, r.randint(1, 80)) for _ in range(200)],
      "200 casos cortos.", {"wa": "Busca el primer caso distinto."}, ["Haz la tabla a mano.", "Revisa la reconstrucción."])
    p("Casos medianos", "aleatorio", [al_azar(30, 100, 20, r.randint(500, 1500)) for _ in range(20)],
      "20 casos con 30 tipos.", {"wa": "Revisa la reconstrucción.", "tle": "La recursión sin memoria es exponencial."},
      ["Rellena la tabla una vez.", "Reconstruye hacia atrás."])
    p("Precio máximo con 100 tipos", "rendimiento", [al_azar(100, 1000, 1000, 10000) for _ in range(4)],
      "Tamaño máximo con valores variados.", {"tle": "Limita k a j / v_i y a c_i.", "mle": "Una tabla de 101 × 10.001 basta.", "rte": "No uses la pila para la tabla."},
      ["No probamos k que se pasan del precio.", "Tabla en vector."])
    p("Muchas monedas pequeñas", "rendimiento", [al_azar(100, 20, 1000, 4000)],
      "Valores pequeños: muchas k por casilla.", {"tle": "El bucle de k debe cortar en k·v ≤ j.", "wa": "Revisa k ≤ c_i."},
      ["Compila con optimización.", "Corta el bucle en cuanto te pases."])
    return L


RECURSIVA = """int rec(vector<int> const& v, vector<int> const& c, int i, int j) {
    if (j == 0) return 0;
    if (i == 0) return 1000000;
    int m = 1000000;
    for (int k = 0; k <= c[i] && k * v[i] <= j; ++k) m = min(m, rec(v, c, i - 1, j - k * v[i]) + k);
    return m;
}

void resuelveCaso() {
    int n0, P0; cin >> n0;
    vector<int> v0(n0 + 1), c0(n0 + 1);
    for (int i = 1; i <= n0; ++i) cin >> v0[i];
    for (int i = 1; i <= n0; ++i) cin >> c0[i];
    cin >> P0;
    if (rec(v0, c0, n0, P0) >= 1000000) { cout << "NO\\n"; return; }
    cout << "SI";
    int jj = P0;
    for (int i = n0; i >= 1; --i) {
        int k = 0;
        while (rec(v0, c0, i - 1, jj - k * v0[i]) + k != rec(v0, c0, i, jj)) ++k;
        c0[i] = k; jj -= k * v0[i];
    }
    for (int i = 1; i <= n0; ++i) cout << ' ' << c0[i];
    cout << '\\n';
    return;
"""

VARIANTES = [
    Variante("monedas ilimitadas de cada tipo", [("k <= c[i] && k * v[i] <= j", "k * v[i] <= j")], prueba=[3, 2, 1], v="wa"),
    Variante("como mucho una moneda de cada", [("k <= c[i] && k * v[i] <= j", "k <= 1 && k * v[i] <= j")], prueba=[4, 5, 3, 6, 2, 1], v="wa"),
    Variante("se queda con la primera forma", [("if (con < monedas[i][j])", "if (monedas[i][j] == Infinito)")], prueba=[5, 4, 1], v="wa"),
    Variante("escribe solo las monedas usadas", [("cout << ' ' << usadas[i];", "if (usadas[i] > 0) cout << ' ' << usadas[i];")], prueba=[1, 3, 4, 5, 2], v="wa"),
    Variante("recursión sin memoria", [("void resuelveCaso() {", RECURSIVA)], prueba=[8, 9, 10], v="tle"),
]
