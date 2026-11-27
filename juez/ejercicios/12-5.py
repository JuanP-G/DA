"""12-5 · Bizcocho con frutas: juez con pruebas pensadas para cada error típico.

Entrada: casos hasta fin de fichero; N (par, 2..1.000) y N valores 0/1/2 sin dos frutas iguales
consecutivas (los ceros sí pueden repetirse, como en el ejemplo del enunciado).
Salida: máximo de días en que los dos trozos cortados por los extremos tienen la misma fruta.
El solucionador es propio: PD sobre (trozos quitados por la izquierda, trozos que quedan).
Validado contra fuerza bruta.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-5/EJ_12-5.cpp",
    "cabeceras": ["12-Evaluacion/EJ_12-5/Matriz.h"],
    "limite_ms": 3000,
    "fallo": ["max({ izquierda, derecha, unoYuno })", "unoYuno"],
}


def resuelve(f):
    n = len(f)

    def ig(a, b):
        return 1 if f[a] and f[a] == f[b] else 0
    ant = [0] * (n + 1)                     # intervalos de longitud 0
    for largo in range(2, n + 1, 2):
        act = [0] * (n - largo + 1)
        for i in range(n - largo + 1):
            j = i + largo - 1
            a = ant[i + 2] + ig(i, i + 1)
            b = ant[i] + ig(j - 1, j)
            c = ant[i + 1] + ig(i, j)
            act[i] = a if a >= b and a >= c else (b if b >= c else c)
        ant = act
    return ant[0]


def _bruta(f):
    if not f:
        return 0
    ig = lambda a, b: int(a != 0 and a == b)
    return max(ig(f[0], f[1]) + _bruta(f[2:]), ig(f[-2], f[-1]) + _bruta(f[:-2]), ig(f[0], f[-1]) + _bruta(f[1:-1]))


def bizcocho(r, n, pceros=0.4):
    f = []
    while len(f) < n:
        x = 0 if r.random() < pceros else r.choice([1, 2])
        if f and x and f[-1] == x:
            continue
        f.append(x)
    return f


_r = random.Random(5)
for _ in range(1500):
    _f = bizcocho(_r, 2 * _r.randint(1, 5))
    assert resuelve(_f) == _bruta(_f), _f


def texto(casos):
    return "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in casos)


def salida(casos):
    return "".join(f"{resuelve(a)}\n" for a in casos)


def pruebas():
    r = random.Random(125)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        for a in casos:
            assert len(a) % 2 == 0 and 2 <= len(a) <= 1000 and all(not x or x != y for x, y in zip(a, a[1:]))
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    ej = [[1, 2, 1, 2], [0, 1, 2, 0, 0, 2, 1, 2], [1, 2, 0, 0, 2, 0, 2, 1, 0, 0, 2, 0]]
    p("Ejemplo del enunciado", "enunciado", ej, "Los tres casos del PDF: 0, 2 y 2.",
      {"wa": "Falla el ejemplo: cada día hay tres jugadas (izquierda-izquierda, derecha-derecha, una de cada lado).",
       "pe": "Un entero por línea.", "ole": "Se lee hasta el fin de la entrada: comprueba !cin."},
      ["dias(i, j) con las tres jugadas.", "Caso base: sin trozos, 0."])
    p("Dos trozos", "borde", [[0, 0], [1, 2], [2, 0], [0, 1]], "Un solo día.",
      {"wa": "Con dos trozos distintos o dos ceros la respuesta es 0.", "rte": "Revisa i + 2 con N = 2."},
      ["igual(a, b) exige fruta.", "Deja filas de sobra en la tabla."])
    p("Los ceros no cuentan", "trampa", [[0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 0, 0, 2]],
      "Dos trozos sin fruta no son un día bueno.",
      {"wa": "Un par de ceros no puntúa: la fruta debe ser 1 o 2."},
      ["igual(a, b) = f_a ≠ 0 y f_a = f_b.", "Todo ceros da 0."])
    p("Un trozo de cada lado", "trampa", [[1, 2, 2 - 2, 1], [1, 0, 0, 1], [2, 1, 0, 0, 1, 2]],
      "Las parejas buenas están en extremos opuestos.",
      {"wa": "Falta la jugada de un trozo de cada lado (i y j)."},
      ["Los dos extremos pueden coincidir.", "dias(i+1, j−1) + igual(i, j)."])
    p("Hace falta cortar del mismo lado", "trampa",
      [[1, 0, 2, 0, 1, 0], [0, 0, 1, 0, 0, 1], [0, 0, 1, 2, 0, 1, 0, 2]],
      "Cortar dos del mismo lado no puntúa pero coloca las frutas en los extremos.",
      {"wa": "Aunque dos del mismo lado no den puntos, hay que considerar esas jugadas."},
      ["Son las tres opciones, siempre.", "dias(i+2, j) y dias(i, j−2)."])
    p("El voraz falla", "trampa", [[1, 2, 0, 1, 0, 2], [2, 0, 1, 2, 0, 1], [1, 0, 2, 1, 0, 2, 0, 1]],
      "Coger una pareja en cuanto se pueda no es óptimo.",
      {"wa": "Un voraz no sirve: hay que comparar las tres jugadas con la tabla."},
      ["Una pareja ahora puede romper dos después.", "Programación dinámica sobre intervalos."])
    p("Varios casos seguidos", "trampa", [bizcocho(r, 40), [1, 2], [0, 1, 1 - 1, 1], bizcocho(r, 10)],
      "Nada debe pasar de un caso a otro.",
      {"wa": "Crea la tabla en cada caso.", "rte": "La tabla anterior tenía otro tamaño."},
      ["Declara la tabla en resuelveCaso.", "Tamaño según el N de cada caso."])
    p("Bizcochos pequeños al azar", "aleatorio", [bizcocho(r, 2 * r.randint(1, 7)) for _ in range(300)],
      "300 casos cortos.", {"wa": "Busca el primer caso distinto."},
      ["Prueba las tres jugadas a mano.", "Revisa igual(a, b)."])
    p("Bizcochos medianos", "aleatorio", [bizcocho(r, 100) for _ in range(30)], "30 casos de 100 trozos.",
      {"wa": "Revisa el orden de relleno.", "tle": "La recursión sin memoria es exponencial."},
      ["Longitudes crecientes.", "O(N²)."])
    p("1.000 trozos", "rendimiento", [bizcocho(r, 1000) for _ in range(3)], "El tamaño máximo.",
      {"tle": "Debe ser O(N²) por caso.", "mle": "Una tabla de 1.000 × 1.000 enteros basta.", "rte": "No uses arrays locales enormes."},
      ["¿Calculas cada intervalo una sola vez?", "Rellena con dos bucles."])
    p("1.000 trozos con muchos ceros", "rendimiento", [bizcocho(r, 1000, 0.8), bizcocho(r, 1000, 0.1)],
      "Casos extremos de reparto de frutas.", {"tle": "O(N²) por caso.", "wa": "Los ceros no puntúan."},
      ["Igual coste sea cual sea la fruta.", "Revisa igual(a, b)."])
    return L


RECURSIVA = """int rec(vector<int> const& f, int i, int j) {
    if (i > j) return 0;
    auto ig = [&](int a, int b) { return f[a] != 0 && f[a] == f[b] ? 1 : 0; };
    return max({ rec(f, i + 2, j) + ig(i, i + 1), rec(f, i, j - 2) + ig(j - 1, j), rec(f, i + 1, j - 1) + ig(i, j) });
}

bool resuelveCaso() {
    int n0; cin >> n0; if (!cin) return false;
    vector<int> g(n0 + 1); for (int i = 1; i <= n0; ++i) cin >> g[i];
    cout << rec(g, 1, n0) << '\\n';
    return true;
}

bool resuelveCasoViejo() {
"""

VARIANTES = [
    Variante("los ceros puntúan", [("f[a] != 0 && f[a] == f[b]", "f[a] == f[b]")], prueba=[2, 3, 1], v="wa"),
    Variante("solo uno de cada lado", [("max({ izquierda, derecha, unoYuno })", "unoYuno")], prueba=[5, 6, 1], v="wa"),
    Variante("olvida uno de cada lado", [("max({ izquierda, derecha, unoYuno })", "max(izquierda, derecha)")], prueba=[4, 1], v="wa"),
    Variante("olvida la izquierda", [("max({ izquierda, derecha, unoYuno })", "max(derecha, unoYuno)")], prueba=[5, 7], v="wa"),
    Variante("recursión sin memoria", [("bool resuelveCaso() {", RECURSIVA)], prueba=[7, 9, 10], v="tle"),
]
