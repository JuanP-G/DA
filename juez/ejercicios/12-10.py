"""12-10 · Megaautopista de Oriente: juez con pruebas pensadas para cada error típico.

Entrada: casos hasta fin de fichero: «N D», N posiciones crecientes y N beneficios (1..1.000).
Salida: dos líneas por caso: beneficio máximo y posiciones elegidas (separadas por D km o más).
Hay empates: se usa comprobador (comprobadores/12-10.py y .js) y ALTERNATIVA da otra solución.
El solucionador es propio: tabla por SUFIJOS con búsqueda binaria y reconstrucción hacia delante.
Validado contra fuerza bruta.
"""
import random
from bisect import bisect_left
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-10/EJ_12-10.cpp",
    "cabeceras": [],
    "limite_ms": 4000,
    "fallo": ["x[j + 1] <= x[i] - d", "x[j + 1] < x[i] - d"],
}


def resuelve(D, x, b, alt=False):
    n = len(x)
    g = [0] * (n + 1)
    sig = [0] * n
    for i in range(n - 1, -1, -1):
        sig[i] = bisect_left(x, x[i] + D, i + 1)
        c = b[i] + g[sig[i]]
        g[i] = c if c > g[i + 1] else g[i + 1]
    elegidas, i = [], 0
    while i < n:
        pon = b[i] + g[sig[i]] == g[i]
        salta = g[i + 1] == g[i]
        if pon and (not salta or not alt):
            elegidas.append(x[i])
            i = sig[i]
        else:
            i += 1
    return g[0], elegidas


def _bruta(D, x, b):
    mejor = 0
    for m in range(1 << len(x)):
        s = [i for i in range(len(x)) if m >> i & 1]
        if all(x[q] - x[p] >= D for p, q in zip(s, s[1:])):
            mejor = max(mejor, sum(b[i] for i in s))
    return mejor


def autopista(r, n, D, hueco=10, bmax=1000):
    x, pos = [], 0
    for _ in range(n):
        pos += r.randint(1, hueco)
        x.append(pos)
    assert pos <= 10**7
    return (D, x, [r.randint(1, bmax) for _ in range(n)])


_r = random.Random(10)
for _ in range(1500):
    _D, _x, _b = autopista(_r, _r.randint(1, 9), _r.randint(1, 20), 8, 9)
    _v, _s = resuelve(_D, _x, _b)
    assert _v == _bruta(_D, _x, _b) == sum(_b[_x.index(p)] for p in _s)


def texto(casos):
    return "".join(f"{len(x)} {D}\n{' '.join(map(str, x))}\n{' '.join(map(str, b))}\n" for D, x, b in casos)


def salida(casos, alt=False):
    t = ""
    for D, x, b in casos:
        v, s = resuelve(D, x, b, alt)
        t += f"{v}\n{' '.join(map(str, s))}\n"
    return t


def ALTERNATIVA(entrada):
    d = iter(map(int, entrada.split()))
    casos = []
    for n in d:
        D = next(d)
        x = [next(d) for _ in range(n)]
        casos.append((D, x, [next(d) for _ in range(n)]))
    return salida(casos, alt=True)


def pruebas():
    r = random.Random(1210)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    p("Ejemplo del enunciado", "enunciado",
      [(10, [10, 20, 30], [20, 40, 10]), (15, [10, 20, 30], [20, 40, 10]), (15, [10, 20, 30], [20, 40, 20])],
      "Los tres casos del PDF.",
      {"wa": "Falla el ejemplo: primera línea el beneficio y segunda las posiciones, de menor a mayor.",
       "pe": "Posiciones separadas por un espacio.", "ole": "Se lee hasta el fin de la entrada."},
      ["gana(i) = max(gana(i−1), gana(antes(i)) + b_i).", "Escribe puntos kilométricos, no índices."])
    p("Una sola área", "borde", [(1, [5], [7]), (1000000, [10000000], [1000])], "N = 1.",
      {"wa": "Con un área se construye en ella.", "rte": "antes(1) = 0."},
      ["gana(0) = 0.", "La posición, no el índice."])
    p("Separación exacta", "trampa", [(10, [10, 20, 30], [5, 5, 5]), (7, [3, 10, 17], [9, 1, 9]), (5, [1, 6], [4, 4])],
      "A exactamente D km sí se puede.",
      {"wa": "«No a menos de D»: con distancia igual a D son compatibles (x_j ≤ x_i − D)."},
      ["Usa ≤, no <.", "10 y 20 con D = 10 valen las dos."])
    p("El voraz falla", "trampa", [(10, [10, 15, 20], [6, 10, 6]), (3, [1, 3, 5, 7], [8, 9, 8, 1]), (100, [1, 50, 120], [500, 900, 500])],
      "Coger el área de más beneficio no es óptimo.",
      {"wa": "Un voraz no sirve: dos áreas medianas pueden sumar más que la mejor."},
      ["6 + 6 > 10.", "Programación dinámica."])
    p("Distancia en kilómetros, no en áreas", "trampa", [(100, [1, 2, 3, 200], [5, 6, 5, 4]), (50, [10, 20, 30, 40, 100], [3, 3, 9, 3, 2])],
      "Varias áreas seguidas pueden estar demasiado cerca.",
      {"wa": "No basta con saltarse el área anterior: hay que saltarse todas las que estén a menos de D km."},
      ["antes(i) puede quedar muy atrás.", "Mueve un puntero."])
    p("Todas compatibles o ninguna", "trampa", [(1, [1, 2, 3, 4], [4, 3, 2, 1]), (1000000, [1, 2, 3, 4], [4, 3, 9, 1])],
      "Casos extremos de D.", {"wa": "Con D = 1 se construye en todas; con D enorme, solo en la mejor.", "rte": "Cuidado con el puntero."},
      ["Reconstruye hasta i = 0.", "Una sola posición si D es enorme."])
    p("Varios casos seguidos", "trampa", [autopista(r, 40, 20), (1, [1], [1]), autopista(r, 5, 3)],
      "Nada debe pasar de un caso a otro.", {"wa": "Reinicia el puntero y las tablas en cada caso.", "rte": "Tamaños distintos."},
      ["Todo dentro de resuelveCaso.", "j = 0 en cada caso."])
    p("Autopistas cortas al azar", "aleatorio", [autopista(r, r.randint(1, 10), r.randint(1, 30), 10, 20) for _ in range(300)],
      "300 casos cortos.", {"wa": "Busca el primer caso distinto."}, ["Hazlo a mano.", "Revisa la reconstrucción."])
    p("Autopistas medianas", "aleatorio", [autopista(r, 500, r.randint(1, 100)) for _ in range(20)],
      "20 casos de 500 áreas.", {"wa": "Revisa la reconstrucción.", "tle": "La recursión sin memoria es exponencial."},
      ["Una sola pasada.", "O(N)."])
    p("180.000 áreas con D grande", "rendimiento", [autopista(r, 180000, 1000000, 6)],
      "Buscar antes(i) retrocediendo de una en una sería cuadrático.",
      {"tle": "antes(i) no retrocede nunca: mantén un puntero (o búsqueda binaria).", "mle": "Vectores de N enteros bastan."},
      ["No recorras hacia atrás desde cada i.", "Dos punteros."])
    p("Muchos restaurantes", "rendimiento", [autopista(r, 90000, 1, 3)],
      "Se construye en todas las áreas.", {"rte": "No reconstruyas con recursión profunda.", "tle": "No insertes por delante en un vector."},
      ["Reconstrucción iterativa.", "Guarda al final y escribe al revés."])
    return L


CUADRATICO = """        int j2 = i - 1;
        while (j2 > 0 && x[j2] > x[i] - d) --j2;
        j = j2;
"""

VARIANTES = [
    Variante("distancia estrictamente mayor que D", [("x[j + 1] <= x[i] - d", "x[j + 1] < x[i] - d")], prueba=[3, 1], v="wa"),
    Variante("posiciones en orden inverso", [("for (int k = (int)elegidas.size() - 1; k >= 0; --k)", "for (int k = 0; k < (int)elegidas.size(); ++k)"),
                                              ('(k > 0 ? " " : "")', '(k + 1 < (int)elegidas.size() ? " " : "")')], prueba=list(range(1, 8)), v="wa"),
    Variante("escribe índices en vez de posiciones", [("elegidas.push_back(x[i]);", "elegidas.push_back(i);")], prueba=list(range(1, 8)), v="wa"),
    Variante("solo salta el área anterior", [("antes[i] = j;", "antes[i] = max(0, i - 2); j = antes[i];")], prueba=[5, 4, 3, 6, 1, 2], v="wa"),
    Variante("busca antes(i) retrocediendo", [("while (x[j + 1] <= x[i] - d) ++j;", CUADRATICO)], prueba=[10], v="tle"),
]
