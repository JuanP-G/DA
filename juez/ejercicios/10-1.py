"""10-1 · La cuerda de la cometa: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «N L» (1..1.000) y N cordeles «longitud coste» (1..1.000).
Se garantiza que ninguna longitud entre 1 y L se consigue de más de 10¹⁸ formas.
Salida: «SI formas mínimoCordeles mínimoCoste» (cada mínimo por separado) o «NO».
El solucionador es propio: va construyendo, cordel a cordel, una tabla NUEVA a partir de la
anterior (con enteros de Python, sin límite), en vez de recorrer un único vector hacia atrás como
la solución del repo. Validado contra fuerza bruta (todos los subconjuntos) en miles de casos.
Cada caso que se genera se comprueba contra la garantía de 10¹⁸ formas.
"""
import random
from itertools import combinations
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "10-Programacion dinamica/EJ_10-1/EJ_10-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["for (int j = L; j >= l; --j) {", "for (int j = l; j <= L; ++j) {"],
}

INF = float("inf")


def tablas(L, cordeles):
    formas, num, coste = [1] + [0] * L, [0] + [INF] * L, [0] + [INF] * L
    for l, c in cordeles:
        nf, nn, nc = formas[:], num[:], coste[:]
        for j in range(l, L + 1):
            if formas[j - l]:
                nf[j] += formas[j - l]
                nn[j] = min(nn[j], num[j - l] + 1)
                nc[j] = min(nc[j], coste[j - l] + c)
        formas, num, coste = nf, nn, nc
    return formas, num, coste


def resuelve(L, cordeles):
    f, n, c = tablas(L, cordeles)
    return "NO" if f[L] == 0 else f"SI {f[L]} {n[L]} {c[L]}"


def fuerza_bruta(L, cordeles):
    formas, mn, mc = 0, INF, INF
    for k in range(len(cordeles) + 1):
        for sub in combinations(cordeles, k):
            if sum(l for l, _ in sub) == L:
                formas += 1
                mn = min(mn, k)
                mc = min(mc, sum(c for _, c in sub))
    return "NO" if formas == 0 else f"SI {formas} {mn} {mc}"


def valido(L, cordeles):
    return 1 <= L <= 1000 and 1 <= len(cordeles) <= 1000 and \
        all(1 <= l <= 1000 and 1 <= c <= 1000 for l, c in cordeles) and max(tablas(L, cordeles)[0]) <= 10 ** 18


def aleatorio(rng, N, L, lmin, lmax, cmax=1000):
    while True:
        cs = [(rng.randint(lmin, lmax), rng.randint(1, cmax)) for _ in range(N)]
        if valido(L, cs):
            return L, cs


def caso_a_texto(caso):
    L, cs = caso
    return f"{len(cs)} {L}\n" + "".join(f"{l} {c}\n" for l, c in cs)


def pruebas():
    rng = random.Random(1001)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(50, [(10, 25), (20, 15), (30, 40), (40, 75)]), (10, [(1, 30), (2, 60), (3, 90)]),
            (2, [(1, 10), (1, 10), (1, 10)]), (10, [(10, 50), (5, 10), (5, 10)])],
           "Los cuatro casos de ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: es una mochila 0/1 con suma exacta, con tres tablas (formas, mínimo de cordeles y mínimo coste) sobre las longitudes 0..L.",
            "pe": "Escribe «SI», el número de formas, el mínimo de cordeles y el mínimo coste separados por un espacio; o «NO»."},
           ["Haz a mano la tabla del primer caso para las longitudes múltiplos de 10.",
            "formas[j] = número de formas de sumar exactamente j; cordeles[j] y coste[j], los mínimos para sumar j.",
            "Casos base: formas[0] = 1 y cordeles[0] = coste[0] = 0; el resto de mínimos empieza en «infinito»."])
    prueba("Un solo cordel", "borde", [(7, [(7, 3)]), (7, [(6, 3)]), (1, [(1, 1000)])],
           "N = 1: el cordel mide justo L (SI 1 1 coste) o no (NO).",
           {"wa": "Con un solo cordel la respuesta es inmediata: revisa los casos base (formas[0] = 1, cordeles[0] = coste[0] = 0)."},
           ["Con un cordel de 7 y L = 7 debe salir «SI 1 1 3».",
            "Sin el caso base formas[0] = 1 ninguna longitud se puede formar."])
    prueba("Cordeles más largos que la cuerda", "borde", [(1, [(1000, 5)]), (5, [(1000, 1), (5, 2), (999, 1)])],
           "Cordeles con longitud mayor que L: no se pueden usar y no deben romper nada.",
           {"rte": "Con un cordel más largo que L accedes a la posición j − l < 0 de la tabla. El bucle de j debe ir de L hasta l (y no hacer nada si l > L).",
            "wa": "Un cordel más largo que L no sirve para nada: no lo cuentes."},
           ["¿Qué hace tu bucle con un cordel de 1000 si L = 1?",
            "Recorre j desde L hacia abajo mientras j ≥ l: si l > L, el bucle no da ninguna vuelta."])
    prueba("SI y NO tal cual", "trampa", [(7, [(7, 3)]), (9, [(4, 1)])],
           "Una respuesta afirmativa y una negativa: «SI 1 1 3» y «NO», sin tildes ni nada más.",
           {"wa": "Revisa el texto: «SI» sin tilde seguido de los tres números, o solo «NO».",
            "pe": "Revisa los espacios: «SI», espacio, formas, espacio, cordeles, espacio, coste."},
           ["Compara tu salida carácter a carácter con «SI 1 1 3».",
            "El enunciado escribe SI sin tilde; y con NO no se escribe ningún número."])
    prueba("Infinito que desborda al sumar", "trampa", [(5, [(3, 1), (2, 1)])],
           "Al probar el cordel de 3 para la longitud 5, la longitud 2 todavía no se puede formar: su «infinito» no debe sumarse.",
           {"wa": "Sumas 1 (o el coste) a un «infinito» como INT_MAX y desborda a un número negativo, que luego gana todos los mínimos. Si j − l no se puede formar, no lo uses (o elige un infinito que no desborde al sumar)."},
           ["¿Cuánto vale INT_MAX + 1 en un int?",
            "Antes de usar cordeles[j − l] + 1 comprueba que j − l se puede formar (formas[j − l] > 0 o cordeles[j − l] != INF).",
            "Otra forma: usa como infinito un valor grande que no desborde al sumarle 1.000 (por ejemplo 10⁹)."])
    prueba("Cada cordel se usa una sola vez", "trampa", [(10, [(5, 10)])],
           "Un único cordel de 5 no forma una cuerda de 10 (no se puede usar dos veces).",
           {"wa": "Usas un mismo cordel más de una vez: con un solo vector, j tiene que ir de MAYOR a MENOR (de L hasta l), para que formas[j − l] sea todavía el de antes de este cordel."},
           ["Con un solo cordel de 5, ¿cuánto vale tu formas[10]?",
            "Si recorres j de menor a mayor, formas[j − l] ya incluye el cordel actual y lo vuelves a usar.",
            "Recorre j desde L hasta l, hacia abajo (o usa dos filas: la de antes y la nueva)."])
    prueba("Cada pregunta por separado", "trampa", [(10, [(10, 11), (4, 1), (6, 3)])],
           "La forma con menos cordeles (el de 10, que cuesta 11) no es la más barata (los de 4 y 6, que cuestan 4): «SI 2 1 4».",
           {"wa": "Das el coste de la solución con menos cordeles (o los cordeles de la más barata). Cada mínimo se calcula por separado, con su propia tabla."},
           ["El ingeniero quiere menos cordeles y el economista menos coste: pueden ser formas distintas.",
            "Lleva dos tablas independientes: cordeles[j] = min(cordeles[j], cordeles[j − l] + 1) y coste[j] = min(coste[j], coste[j − l] + c)."])
    prueba("Cordeles iguales son distintos", "trampa", [(4, [(2, 1), (2, 1), (2, 1), (2, 1)])],
           "Cuatro cordeles iguales de 2: hay C(4, 2) = 6 parejas que forman 4.",
           {"wa": "Cuentas los cordeles iguales como uno solo (o cuentas formas distintas por longitudes). Cada cordel es distinto aunque mida lo mismo."},
           ["Con los cordeles a, b, c, d las parejas son ab, ac, ad, bc, bd, cd.",
            "No elimines repetidos al leer: cada cordel se procesa por separado en la tabla."])
    prueba("El coste puede ser mayor que la longitud", "trampa", [(1000, [(500, 1000), (500, 1000)]), (3, [(1, 1000), (1, 1000), (1, 1000)])],
           "Mínimos costes de 2.000 y 3.000 con cuerdas de 1.000 y 3: el «infinito» del coste tiene que ser mayor que cualquier coste posible.",
           {"wa": "Tu «infinito» para el coste es demasiado pequeño (por ejemplo L + 1, que sirve para contar cordeles pero no para el coste). El coste puede llegar a 1.000 · 1.000."},
           ["¿Cuál es el mayor coste posible? Hasta 1.000 cordeles de 1.000 cada uno.",
            "Usa como infinito un valor mayor que 10⁶ (por ejemplo INT_MAX con cuidado al sumar, o 10⁹)."])
    prueba("Hacen falta todos los cordeles", "trampa", [(10, [(1, 1), (2, 2), (3, 3), (4, 4)]), (1000, [(250, 7)] * 4)],
           "La cuerda mide justo la suma de todos los cordeles: una única forma, con todos.",
           {"wa": "Cuando la solución usa todos los cordeles algo falla: ¿el bucle de cordeles llega al último? ¿la tabla llega hasta L incluido?",
            "rte": "La tabla debe tener L + 1 posiciones (de 0 a L)."},
           ["En el primer caso, 1 + 2 + 3 + 4 = 10: «SI 1 4 10».",
            "Revisa que la tabla tiene tamaño L + 1 y que procesas los N cordeles."])
    prueba("Más formas de las que caben en un int", "trampa", [(20, [(1, 1)] * 40)],
           "40 cordeles de 1 y L = 20: C(40, 20) = 137.846.528.820 formas.",
           {"wa": "El número de formas no cabe en int: el enunciado dice que puede llegar a 10¹⁸, así que hace falta long long.",
            "tle": "Cuentas las formas una a una (recursión sin memoria o vuelta atrás): aquí hay más de 10¹¹. Hace falta la tabla de programación dinámica."},
           ["¿Cuánto es C(40, 20)? Bastante más que 2³¹.",
            "Declara la tabla de formas como vector<long long>."])
    prueba("Cerca de 10¹⁸ formas", "trampa", [(31, [(1, k) for k in range(1, 63)])],
           "62 cordeles de 1 y L = 31: C(62, 31) = 465.428.353.255.261.088 formas.",
           {"wa": "Con tantas formas pierdes precisión o desbordas: usa long long (no double, ni float, ni int)."},
           ["El enunciado garantiza como mucho 10¹⁸ formas: cabe en long long (hasta 9,2·10¹⁸).",
            "Si usas double, a partir de 2⁵³ deja de ser exacto."])
    prueba("Varios casos seguidos", "trampa",
           [(1000, [(400, 3), (600, 4), (300, 1), (700, 9), (1000, 20)]), (300, [(100, 1), (200, 1), (300, 5)]), (10, [(5, 1)]), (7, [(3, 2), (4, 2)])],
           "Un caso grande y luego otros más pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: las tablas deben crearse (con sus casos base) dentro de la función de cada caso.",
            "rte": "Las tablas de un caso anterior tienen otro tamaño: créalas en cada caso con tamaño L + 1."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara las tres tablas dentro de la función de cada caso."])
    peq = []
    while len(peq) < 150:
        N = rng.randint(1, 10)
        cs = [(rng.randint(1, 8), rng.randint(1, 20)) for _ in range(N)]
        peq.append((rng.randint(1, 25), cs))
    prueba("Aleatorios pequeños", "aleatorio", peq,
           "150 casos pequeños al azar (hasta 10 cordeles).",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla y enumera a mano los subconjuntos.",
            "Revisa el sentido del bucle (de L hacia abajo) y los casos base."])
    grandes = [aleatorio(rng, 1000, 1000, 120, 1000) for _ in range(3)] + \
              [aleatorio(rng, rng.randint(50, 300), rng.randint(100, 1000), 30, 400) for _ in range(5)]
    prueba("Aleatorios grandes", "aleatorio", grandes,
           "8 casos con hasta 1.000 cordeles y L = 1.000.",
           {"wa": "Falla en casos grandes: revisa el desbordamiento (formas en long long, infinito que no desborde) y el tamaño de las tablas.",
            "tle": "Tu solución es lenta: debe ser O(N · L) por caso."},
           ["¿Usas long long para las formas?",
            "Cada cordel recorre la tabla una sola vez: O(N · L)."])
    expo = (60, [(1, 1000)] * 59 + [(2, 1)] + [(1000, 1)] * 2)
    prueba("Muchos subconjuntos posibles", "rendimiento", [expo],
           "59 cordeles de 1 y uno de 2 para L = 60: hay del orden de 10¹⁷ subconjuntos que no se pasan de L.",
           {"tle": "Pruebas todos los subconjuntos (recursión sin memoria o vuelta atrás): crece como 2^N. Con una tabla sobre las longitudes 0..L el coste es O(N · L).",
            "wa": "Con muchos cordeles iguales algo desborda: formas en long long."},
           ["¿Cuántas veces calculas lo mismo? «Las formas de sumar j con los cordeles 1..i» se repite muchísimo.",
            "Guarda esos valores en una tabla (o en un vector recorrido de L hacia abajo)."])
    maximos = [aleatorio(rng, 1000, 1000, 101, 1000) for _ in range(12)]
    prueba("Muchos casos de tamaño máximo", "rendimiento", maximos,
           "12 casos con N = 1.000 y L = 1.000.",
           {"tle": "Tu solución es lenta para N = L = 1.000: debe ser O(N · L) por caso, sin copiar tablas enteras por cada cordel innecesariamente.",
            "mle": "Gastas demasiada memoria: basta un vector de tamaño L + 1 por tabla (o una tabla (N + 1) × (L + 1))."},
           ["Cada cordel debe costar O(L): un recorrido de la tabla.",
            "Si copias la tabla en cada llamada recursiva o en cada cordel, cámbialo por un único vector recorrido hacia atrás."])
    for casos in (x[2] for x in P):
        for L, cs in casos:
            assert valido(L, cs), (L, cs[:5])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(resuelve(*c) + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("escribe SÍ con tilde", [('cout << "SI "', 'cout << "SÍ "')], prueba=4, v="wa"),
    Variante("suma a INT_MAX sin comprobar (desborda)", [("if (formas[j - l] == 0) continue;            // j - l no se puede formar\n", "")], prueba=5, v="wa"),
    Variante("j de menor a mayor (reutiliza cordeles)", [("for (int j = L; j >= l; --j) {", "for (int j = l; j <= L; ++j) {")], prueba=6, v="wa"),
    Variante("coste de la solución con menos cordeles",
             [("cordeles[j] = min(cordeles[j], cordeles[j - l] + 1);\n            coste[j] = min(coste[j], coste[j - l] + c);",
               "if (cordeles[j - l] + 1 < cordeles[j] || (cordeles[j - l] + 1 == cordeles[j] && coste[j - l] + c < coste[j])) {\n"
               "                cordeles[j] = cordeles[j - l] + 1; coste[j] = coste[j - l] + c; }")], prueba=7, v="wa"),
    Variante("quita repetidos al leer",
             [("cin >> l >> c;", "cin >> l >> c;\n        static int ultimaL = -1; if (k == 0) ultimaL = -1; if (l == ultimaL) continue; ultimaL = l;")], prueba=8, v="wa"),
    Variante("infinito del coste = L + 1", [("vector<int> cordeles(L + 1, INF), coste(L + 1, INF);", "vector<int> cordeles(L + 1, INF), coste(L + 1, L + 1);")], prueba=9, v="wa"),
    Variante("formas en int", [("vector<long long> formas(L + 1, 0);", "vector<int> formas(L + 1, 0);")], prueba=11, v="wa"),
    Variante("formas en double", [("vector<long long> formas(L + 1, 0);", "vector<double> formas(L + 1, 0);")], prueba=11, v="wa"),
    Variante("no reinicia las formas entre casos", [("vector<long long> formas(L + 1, 0);", "static vector<long long> formas(1001, 0);")], prueba=13, v="wa"),
    Variante("prueba todos los subconjuntos (sin memoria)",
             [("void resuelveCaso() {",
               "long long F; int MC, MK;\nvoid rec(const vector<pair<int,int>>& v, int i, int j, int k, int c) {\n"
               "    if (j == 0) { ++F; MK = min(MK, k); MC = min(MC, c); }\n    if (i == (int)v.size() || j <= 0) return;\n"
               "    if (v[i].first <= j) rec(v, i + 1, j - v[i].first, k + 1, c + v[i].second);\n    rec(v, i + 1, j, k, c);\n}\n"
               "void resuelveCaso() {\n    int n0, L0; cin >> n0 >> L0; vector<pair<int,int>> v(n0); for (auto& p : v) cin >> p.first >> p.second;\n"
               "    F = 0; MC = MK = INT_MAX; rec(v, 0, L0, 0, 0);\n"
               "    if (F == 0) cout << \"NO\\n\"; else cout << \"SI \" << F << ' ' << MK << ' ' << MC << '\\n';\n    return;\n")], prueba=[11, 16], v="tle"),
]
