"""10-L · Cambio exacto: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso tiene «P N» (precio 1..10.000, N 1..100 piezas) y N valores
(1..10.000). Cada pieza se usa como mucho una vez; la suma de todas es al menos P.
Salida: «cantidad piezas»: la menor cantidad ≥ P que se puede pagar y, para ella, el menor número
de piezas. La respuesta es única.
El solucionador es propio: calcula con numpy el mínimo de piezas para TODAS las sumas posibles
(hasta la suma total, sin el tope P + máximo que usa la solución del repo) y elige la menor ≥ P.
Validado contra fuerza bruta (todos los subconjuntos) en miles de casos pequeños.
"""
import random
import numpy as np
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "10-Programacion dinamica/EJ_10-L/EJ_10-L.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["for (int s = tope; s >= v; --s)", "for (int s = v; s <= tope; ++s)"],
}

INF = 10 ** 9


def resuelve(P, piezas):
    total = sum(piezas)
    dp = np.full(total + 1, INF, dtype=np.int64)
    dp[0] = 0
    for v in piezas:
        dp[v:] = np.minimum(dp[v:], dp[:-v] + 1)       # el lado derecho se calcula con el dp antiguo: 0/1
    s = P
    while dp[s] >= INF:
        s += 1
    return s, int(dp[s])


def fuerza_bruta(P, piezas):
    mejor = None
    for m in range(1 << len(piezas)):
        s = sum(v for i, v in enumerate(piezas) if m >> i & 1)
        if s >= P and (mejor is None or (s, bin(m).count("1")) < mejor):
            mejor = (s, bin(m).count("1"))
    return mejor


def texto(casos):
    return f"{len(casos)}\n" + "".join(f"{P} {len(v)}\n{' '.join(map(str, v))}\n" for P, v in casos)


def salida(casos):
    return "".join("%d %d\n" % resuelve(P, v) for P, v in casos)


def pruebas():
    rng = random.Random(1010)
    L = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        for P, v in casos:
            assert 1 <= P <= 10000 and 1 <= len(v) <= 100 and all(1 <= x <= 10000 for x in v) and sum(v) >= P
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    def alea(n, vmax, relleno=1.0):
        v = [rng.randint(1, vmax) for _ in range(n)]
        return rng.randint(1, min(10000, max(1, int(sum(v) * relleno)))), v

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado", [(1400, [500, 1000, 2000])],
           "No se puede pagar 1.400 justo: la menor suma que llega es 1.500 (500 + 1.000), con 2 piezas.",
           {"wa": "Falla el primer ejemplo: si no se puede pagar exacto hay que buscar la MENOR suma alcanzable que sea ≥ precio (no la menor pieza que lo supere).",
            "pe": "Escribe la cantidad, un espacio y el número de piezas, en una línea por caso."},
           ["Las sumas posibles son 500, 1.000, 1.500, 2.000, 2.500, 3.000 y 3.500.",
            "Calcula para cada suma s el mínimo de piezas que da exactamente s, y busca desde s = precio hacia arriba la primera que se pueda.",
            "La respuesta es «1500 2»."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(100, [25, 50, 25, 50])],
           "Se paga justo 100, de dos formas: 50 + 50 (2 piezas) o 50 + 25 + 25 (3). Gana la de 2.",
           {"wa": "Con la misma cantidad hay que elegir la forma que usa MENOS piezas: «100 2», no «100 3»."},
           ["Hay dos formas de sumar 100: ¿cuál usa menos piezas?",
            "piezas(i, s) = min(piezas(i−1, s), piezas(i−1, s − v_i) + 1)."])

    prueba("Salida: la cantidad y luego las piezas", "trampa", [(35, [10, 25, 5]), (9, [4, 5, 1])],
           "Dos casos en los que la cantidad pagada y el número de piezas son números distintos: «35 2» y «9 2».",
           {"wa": "Escribe primero la CANTIDAD pagada y después el NÚMERO de piezas («30 3»). Si el número de piezas sale una unidad de menos (o 0), revisa que cuentas cada pieza usada (+1).",
            "pe": "La cantidad y el número de piezas van en la misma línea, separados por un espacio, con un salto de línea por caso."},
           ["En el primer caso se paga justo 35 con dos piezas (10 + 25): «35 2».",
            "La cantidad va primero. Y cada pieza que añades suma 1 al número de piezas: piezas[s − v] + 1."])

    # ------------------------------------------------------------------ bordes
    prueba("Una sola pieza", "borde", [(1, [10000]), (10000, [10000]), (7, [7]), (5000, [9999])],
           "Una pieza: se paga con ella aunque sobre muchísimo (1 céntimo con un billete de 10.000).",
           {"wa": "Con una sola pieza la respuesta es esa pieza y 1.",
            "rte": "La cantidad pagada puede ser muy superior al precio (hasta precio + 10.000): la tabla debe llegar tan lejos."},
           ["Si el precio es 1 y solo tienes una pieza de 10.000, pagas 10.000 con 1 pieza.",
            "No limites la tabla al precio: la solución puede estar por encima de él."])
    prueba("El precio es la suma de todas las piezas", "borde", [(60, [10, 20, 30]), (9, [1, 1, 1, 1, 1, 1, 1, 1, 1]), (300, [100, 100, 100])],
           "Hay que usar TODAS las piezas: no hay otra forma de llegar al precio.",
           {"wa": "Si el precio es justo la suma total, la única forma es usarlas todas: «60 3».",
            "rte": "Revisa los límites de los bucles: la suma total puede ser exactamente el tope."},
           ["Comprueba que tu tabla incluye la suma total.",
            "Con 9 monedas de 1 y precio 9 la respuesta es «9 9»."])
    prueba("Pagar más usa menos piezas, pero manda la cantidad", "trampa",
           [(100, [25, 35, 40, 150]), (50, [12, 13, 25, 60]), (20, [3, 4, 5, 6, 2, 25])],
           "Se puede pagar exacto con muchas piezas (100 = 25 + 35 + 40) o de más con una sola (150): se paga lo menos posible, así que 100 con 3.",
           {"wa": "Primero hay que minimizar la CANTIDAD pagada y solo después el número de piezas: «100 3», no «150 1»."},
           ["Mira el orden de prioridades del enunciado: ¿qué va primero, pagar poco o usar pocas piezas?",
            "Busca la primera suma s ≥ precio con piezas(N, s) finito, y de esa suma mira cuántas piezas."])
    prueba("Cada pieza se usa una vez", "trampa", [(30, [15, 7, 5, 3]), (40, [20, 10, 6, 4]), (45, [15, 13, 9, 8])],
           "Con 15, 7, 5 y 3 se paga 30 con las 4 piezas; con monedas ilimitadas bastarían dos de 15. Cada pieza es una sola.",
           {"wa": "Usas una misma pieza varias veces: cada moneda o billete es uno solo (0/1). Recorre las sumas de MAYOR a menor para no reutilizar la pieza.",
            "rte": "Revisa los límites de la tabla de sumas."},
           ["Si recorres s hacia arriba, al actualizar piezas[s] ya has actualizado piezas[s − v] con la misma pieza.",
            "Cambia el sentido del bucle: de la suma máxima hasta v."])
    prueba("Varias piezas iguales", "trampa", [(100, [25, 25, 25, 25]), (75, [25, 25, 25, 25]), (80, [25, 25, 25, 25, 50])],
           "Piezas repetidas: cada una cuenta aparte (cuatro de 25 son cuatro piezas distintas).",
           {"wa": "Las piezas iguales no son la misma: si las tratas como una sola (por ejemplo, con un set) pierdes combinaciones."},
           ["Con 4 piezas de 25 y precio 100 hay que usar las 4.",
            "No elimines duplicados: lee las N piezas y trátalas una a una."])
    prueba("No se puede pagar justo: sobre bastante", "trampa", [(9999, [10000, 5000, 5000]), (9, [4, 4, 4]), (301, [100, 100, 100, 99])],
           "El precio no se alcanza por 1 o por mucho: la respuesta es la menor suma por encima.",
           {"wa": "La menor suma ≥ precio no tiene por qué ser la de menos piezas ni la de la pieza más pequeña ≥ precio. Revisa también hasta dónde llega tu tabla de sumas: debe llegar a precio + valor máximo.",
            "tle": "Buscar la suma con un bucle que recalcula toda la tabla para cada suma es lento: calcula la tabla una sola vez."},
           ["Con 4, 4, 4 y precio 9: 4 + 4 = 8 no llega; 4 + 4 + 4 = 12 sí.",
            "Primero llena la tabla, después busca hacia arriba desde el precio."])
    prueba("La mejor suma usa una combinación inesperada", "trampa",
           [(1000, [999, 600, 600, 400, 400]), (50, [26, 24, 49, 1]), (700, [350, 349, 351, 1])],
           "La suma más pequeña posible no se consigue con las piezas más grandes ni con las más pequeñas (es una mochila, no un voraz).",
           {"wa": "Un voraz (coger las mayores, o las menores, hasta llegar) no da la suma mínima: usa la tabla de programación dinámica."},
           ["Prueba a mano: 1000 = 600 + 400 con 2 piezas; la pieza de 999 da 999 < 1000.",
            "Un voraz mira solo una pieza cada vez; la tabla considera todas las combinaciones."])
    prueba("Varios casos seguidos", "trampa",
           [(10000, [10000] * 5), (3, [1, 1, 1, 5]), (1, [1]), (20, [10, 10, 5])],
           "Un caso con valores grandes y luego otros pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla, el máximo o la suma): créalos dentro de resuelveCaso.",
            "rte": "La tabla del caso anterior tenía otro tamaño: créala en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variable vive fuera de la función.",
            "La tabla debe tener precio + máximo + 1 casillas, calculadas con los datos de ESTE caso."])
    prueba("Piezas más grandes que el precio", "trampa", [(10, [10000, 9999, 9998, 9]), (100, [101, 102, 103, 104]), (8000, [8001, 7999, 9000])],
           "Se mezcla una pieza que no llega con otras que sobran: hay que comparar sumas por debajo y por encima del precio.",
           {"wa": "Revisa que consideras las piezas mayores que el precio: la tabla debe llegar hasta precio + máximo."},
           ["Con precio 10 y las piezas 10.000, 9.999, 9.998 y 9, la menor suma ≥ 10 es 9.998 (una pieza).",
            "La tabla de sumas debe llegar hasta precio + valor máximo, no solo hasta el precio."])

    # ------------------------------------------------------------------ aleatorios
    prueba("Casos pequeños al azar", "aleatorio", [alea(rng.randint(1, 8), rng.choice([5, 30, 1000])) for _ in range(120)],
           "120 casos de hasta 8 piezas con valores pequeños (muchas formas de pagar y empates).",
           {"wa": "Algún caso falla: es pequeño, resuélvelo a mano (todas las combinaciones de piezas) y compara."},
           ["Localiza el caso en la entrada y calcula todas las sumas posibles.",
            "Revisa el orden de prioridades: primero la cantidad, luego las piezas."])
    prueba("Casos medianos al azar", "aleatorio", [alea(rng.randint(15, 40), rng.choice([50, 500, 10000])) for _ in range(40)],
           "40 casos de hasta 40 piezas.",
           {"wa": "Los pequeños salen bien y estos no: revisa el tamaño de la tabla y los límites.",
            "tle": "Probar todos los subconjuntos (2^N) no termina con 40 piezas: usa la tabla."},
           ["¿Cuántas veces recalculas el mismo piezas(i, s)? Guarda la tabla.",
            "Una sola fila de tamaño precio + máximo + 1, recorrida de mayor a menor."])

    # ------------------------------------------------------------------ rendimiento
    prueba("100 piezas grandes y precio máximo", "rendimiento", [(10000, [rng.randint(5000, 10000) for _ in range(100)])],
           "El tamaño máximo: 100 piezas de valor alto y precio 10.000.",
           {"tle": "Debe costar O(N · (precio + máximo)). Probar subconjuntos con 100 piezas es imposible.",
            "mle": "Basta una fila (o una tabla N × 20.000 de int como mucho)."},
           ["100 piezas son 2¹⁰⁰ subconjuntos: imposible probarlos.",
            "piezas[s] es una tabla de unos 20.000 enteros que se actualiza una vez por pieza."])
    prueba("100 piezas pequeñas y precio máximo", "rendimiento", [(10000, [rng.randint(100, 300) for _ in range(100)]) for _ in range(30)],
           "30 casos con muchísimas combinaciones.",
           {"tle": "Cada caso debe tardar O(N · 20.000). ¿Recalculas la tabla para cada suma, o haces recursión sin memoria?"},
           ["Son unas 2·10⁶ operaciones por caso: muy poco.",
            "No mires la tabla entera para cada pieza más de una vez."])
    prueba("Todas las piezas valen 10.000 y el precio es 10.000", "rendimiento", [(10000, [10000] * 100)],
           "100 piezas iguales de 10.000: la respuesta es una sola, «10000 1».",
           {"wa": "Con piezas iguales la respuesta es «10000 1»: revisa que no cuentas varias veces la misma suma.",
            "tle": "Aunque las piezas sean iguales, debe ser O(N · tope)."},
           ["Una sola pieza ya paga justo el precio.",
            "piezas[10000] = 1 desde la primera pieza."])
    return L


# ------------------------------------------------------------ variantes (fallos típicos)
def _asegura(casos_pequenos=400):
    r = random.Random(7)
    for _ in range(casos_pequenos):
        n = r.randint(1, 8)
        v = [r.randint(1, 30) for _ in range(n)]
        P = r.randint(1, sum(v))
        assert resuelve(P, v) == fuerza_bruta(P, v), (P, v)


_asegura()

SUBCONJUNTOS = """void resuelveCaso() {
    int p0, n0; cin >> p0 >> n0; vector<int> w(n0);
    for (int& x : w) cin >> x;
    long long bs = 1LL << 60; int bc = 0;
    function<void(int, long long, int)> f = [&](int i, long long s, int c) {
        if (i == n0) { if (s >= p0 && (s < bs || (s == bs && c < bc))) { bs = s; bc = c; } return; }
        f(i + 1, s, c); f(i + 1, s + w[i], c + 1);
    };
    f(0, 0, 0);
    cout << bs << ' ' << bc << '\\n';
    return;
"""

VARIANTES = [
    Variante("monedas ilimitadas (recorre las sumas hacia arriba)", [("for (int s = tope; s >= v; --s)", "for (int s = v; s <= tope; ++s)")], prueba=7, v="wa"),
    Variante("escribe las piezas antes que la cantidad", [("cout << s << ' ' << piezas[s] << '\\n';", "cout << piezas[s] << ' ' << s << '\\n';")], prueba=3, v="wa"),
    Variante("prefiere pocas piezas a pagar poco",
             [("    int s = precio;\n    while (piezas[s] == Infinito) ++s;\n",
               "    int s = precio;\n    for (int t = precio; t <= tope; ++t) if (piezas[t] < piezas[s] || piezas[s] == Infinito) s = t;\n")],
             prueba=6, v="wa"),
    Variante("no cuenta la pieza usada", [("piezas[s - v] + 1", "piezas[s - v]")], prueba=3, v="wa"),
    Variante("tabla solo hasta el precio (sin pasarse)", [("int tope = precio + maximo;", "int tope = precio;")], prueba=9, v="wa"),
    Variante("elimina las piezas repetidas", [("    for (int v : valor)\n", "    sort(valor.begin(), valor.end()); valor.erase(unique(valor.begin(), valor.end()), valor.end());\n    for (int v : valor)\n")], prueba=8, v="wa"),
    Variante("prueba todos los subconjuntos (2^N)", [("#include <vector>", "#include <vector>\n#include <functional>"), ("void resuelveCaso() {", SUBCONJUNTOS)], prueba=[14], v="tle"),
]

