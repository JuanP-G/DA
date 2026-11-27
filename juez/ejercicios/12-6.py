"""12-6 · Alineamiento de secuencias: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso es una matriz 5×5 (orden A C G T -), el número de pares y,
por cada par, dos líneas con las cadenas (1..1.000 bases).
Salida: la puntuación máxima de cada par.
El solucionador es propio: tabla por SUFIJOS (de atrás hacia delante), al revés que la solución.
Validado contra fuerza bruta (todos los alineamientos) en miles de casos pequeños.
"""
import random
from functools import lru_cache
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-6/EJ_12-6.cpp",
    "cabeceras": [],
    "limite_ms": 4000,
    "fallo": ["diagonal = arriba;", "diagonal = mejor[j];"],
}
B = "ACGT"
EJEMPLO = [[2, -2, 1, 1, -1], [-2, 12, -3, -2, -1], [1, -3, 5, 0, -1], [1, -2, 0, 3, -1], [-1, -1, -1, -1, -1]]


def resuelve(S, a, b):
    ia = [B.index(c) for c in a]
    ib = [B.index(c) for c in b]
    m = len(ib)
    sig = [0] * (m + 1)                      # fila i = n
    for j in range(m - 1, -1, -1):
        sig[j] = sig[j + 1] + S[4][ib[j]]
    for i in range(len(ia) - 1, -1, -1):
        fila = S[ia[i]]
        g = fila[4]
        act = [0] * (m + 1)
        act[m] = sig[m] + g
        for j in range(m - 1, -1, -1):
            y = ib[j]
            v = sig[j + 1] + fila[y]
            w = sig[j] + g
            z = act[j + 1] + S[4][y]
            if w > v:
                v = w
            act[j] = z if z > v else v
        sig = act
    return sig[0]


def _bruta(S, a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) and j == len(b):
            return 0
        ops = []
        if i < len(a) and j < len(b):
            ops.append(S[B.index(a[i])][B.index(b[j])] + f(i + 1, j + 1))
        if i < len(a):
            ops.append(S[B.index(a[i])][4] + f(i + 1, j))
        if j < len(b):
            ops.append(S[4][B.index(b[j])] + f(i, j + 1))
        return max(ops)
    return f(0, 0)


def cad(r, n):
    return "".join(r.choice(B) for _ in range(n))


def matriz(r, lo=-10, hi=10):
    return [[r.randint(lo, hi) for _ in range(5)] for _ in range(5)]


assert resuelve(EJEMPLO, "ATGCC", "TACGCA") == 25 and resuelve(EJEMPLO, "CGGATA", "TTAG") == 2
_r = random.Random(6)
for _ in range(800):
    _S, _a, _b = matriz(_r), cad(_r, _r.randint(1, 6)), cad(_r, _r.randint(1, 6))
    assert resuelve(_S, _a, _b) == _bruta(_S, _a, _b)


def texto(casos):
    t = f"{len(casos)}\n"
    for S, pares in casos:
        t += "".join(" ".join(map(str, f)) + "\n" for f in S) + f"{len(pares)}\n"
        t += "".join(f"{a}\n{b}\n" for a, b in pares)
    return t


def salida(casos):
    return "".join(f"{resuelve(S, a, b)}\n" for S, pares in casos for a, b in pares)


def pruebas():
    r = random.Random(126)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # matriz «normal»: acierto +5, fallo -4, hueco -3
    N = [[5 if i == j else -4 for j in range(4)] + [-3] for i in range(4)] + [[-3] * 4 + [0]]
    p("Ejemplo del enunciado", "enunciado", [(EJEMPLO, [("ATGCC", "TACGCA"), ("CGGATA", "TTAG")])],
      "El caso del PDF: 25 y 2.",
      {"wa": "Falla el ejemplo: tres opciones por casilla (emparejar, hueco abajo, hueco arriba). Cada par se escribe en su línea.",
       "pe": "Un entero por par."},
      ["Lee la matriz una vez y después todos los pares.", "mejor(i, 0) y mejor(0, j) son sumas de huecos, no ceros."])
    p("Una sola base", "borde", [(N, [("A", "A"), ("A", "C"), ("G", "T")])], "Cadenas de longitud 1.",
      {"wa": "Con una base por cadena se elige entre emparejarlas (5 o −4) o dos huecos (−6).", "rte": "Revisa los índices."},
      ["A con A puntúa 5.", "Dos columnas con hueco valen −6."])
    p("Una cadena mucho más larga", "trampa", [(N, [("A", "ACGTACGT"), ("ACGTACGT", "A"), ("GG", "TTTTTT")])],
      "Los casos base obligan a pagar huecos.",
      {"wa": "mejor(i, 0) y mejor(0, j) no son 0: cada base sin pareja paga su hueco."},
      ["Acumula S[x][-] en la primera columna.", "Acumula S[-][y] en la primera fila."])
    asim = [[1, 2, 3, 4, -1], [-5, 1, -5, -5, -9], [-6, -6, 1, -6, -2], [-7, -7, -7, 1, -3], [-8, -4, -1, -6, 0]]
    p("La matriz no es simétrica", "trampa", [(asim, [("AAAA", "TTTT"), ("TTTT", "AAAA"), ("ACG", "GT"), ("GT", "ACG")])],
      "La primera cadena indexa filas y la segunda columnas.",
      {"wa": "Usa S[a_i][b_j], S[a_i][-] y S[-][b_j]: el orden importa porque la matriz puede no ser simétrica."},
      ["Fila: base de la primera cadena.", "La columna 4 y la fila 4 son los huecos."])
    huecos = [[-5] * 4 + [2] for _ in range(4)] + [[3] * 4 + [0]]
    p("Compensa poner huecos", "trampa", [(huecos, [("ACG", "TT"), ("A", "A"), ("ACGTAC", "GTA")])],
      "Los huecos puntúan en positivo.",
      {"wa": "No supongas que emparejar es siempre mejor ni que los huecos restan."},
      ["Aquí la mejor opción es no emparejar nada.", "Toma el máximo de las tres, sin atajos."])
    neg = [[-10] * 5 for _ in range(5)]
    p("Resultado negativo", "trampa", [(neg, [("ACGT", "AC"), ("A", "A")])], "Todas las puntuaciones son negativas.",
      {"wa": "El máximo puede ser negativo: no inicialices con 0."}, ["Empieza desde los casos base.", "No uses max(0, ...)."])
    p("Varias matrices", "trampa", [(N, [("ACGT", "ACGT")]), (EJEMPLO, [("ACGT", "ACGT"), ("TT", "T")]), (neg, [("AC", "AC")])],
      "Cada caso trae su matriz y su número de pares.",
      {"wa": "Lee de nuevo la matriz y el número de pares en cada caso.", "rte": "La lectura se ha desalineado."},
      ["Caso: matriz, K, 2K cadenas.", "No reutilices la matriz anterior."])
    p("Cadenas cortas al azar", "aleatorio",
      [(matriz(r), [(cad(r, r.randint(1, 8)), cad(r, r.randint(1, 8))) for _ in range(40)]) for _ in range(8)],
      "320 pares cortos.", {"wa": "Busca el primer par distinto."}, ["Haz la tabla a mano.", "Revisa la diagonal."])
    p("Cadenas medianas al azar", "aleatorio", [(matriz(r, -100, 100), [(cad(r, 100), cad(r, 90)) for _ in range(5)]) for _ in range(4)],
      "20 pares de unas 100 bases.", {"wa": "Revisa qué guardas antes de pisar la casilla.", "tle": "La recursión sin memoria es exponencial."},
      ["Guarda la diagonal antes de actualizar.", "O(n·m)."])
    p("1.000 bases", "rendimiento", [(matriz(r, -50000, 50000), [(cad(r, 1000), cad(r, 1000)) for _ in range(3)])],
      "El tamaño máximo.", {"tle": "Debe ser O(n·m) por par.", "mle": "Basta una fila, o una tabla de 1.001 × 1.001 enteros.",
                            "rte": "No declares una tabla enorme en la pila."},
      ["No recalcules casillas.", "Rellena en orden."])
    p("Puntuaciones máximas", "rendimiento", [([[50000] * 5 for _ in range(5)], [(cad(r, 1000), cad(r, 1000))])],
      "El mayor resultado posible: 100.000.000.", {"wa": "Con todo a 50.000 lo mejor es no emparejar nunca: 2.000 columnas.", "tle": "O(n·m)."},
      ["Cabe en int.", "No limites el número de columnas."])
    return L


RECURSIVA = """int rec(string const& a, string const& b, const int S[5][5], int i, int j) {
    if (i == 0 && j == 0) return 0;
    if (i == 0) return rec(a, b, S, 0, j - 1) + S[4][indice(b[j - 1])];
    if (j == 0) return rec(a, b, S, i - 1, 0) + S[indice(a[i - 1])][4];
    return max({ rec(a, b, S, i - 1, j - 1) + S[indice(a[i - 1])][indice(b[j - 1])],
                 rec(a, b, S, i - 1, j) + S[indice(a[i - 1])][4], rec(a, b, S, i, j - 1) + S[4][indice(b[j - 1])] });
}

void resuelvePar(const int S[5][5]) {
    string a, b;
    cin >> a >> b;
    cout << rec(a, b, S, a.size(), b.size()) << '\\n';
    return;
}

void resuelveParViejo(const int S[5][5]) {
"""

VARIANTES = [
    Variante("pierde la diagonal", [("diagonal = arriba;", "diagonal = mejor[j];")], prueba=list(range(1, 8)), v="wa"),
    Variante("primera fila a cero", [("mejor[j] = mejor[j - 1] + S[HUECO][indice(b[j - 1])];", "mejor[j] = 0;")], prueba=list(range(1, 8)), v="wa"),
    Variante("matriz traspuesta", [("diagonal + S[x][y]", "diagonal + S[y][x]")], prueba=[4, 7, 1], v="wa"),
    Variante("sin huecos en la segunda cadena", [(", mejor[j - 1] + S[HUECO][y] });", " });")], prueba=list(range(1, 8)), v="wa"),
    Variante("recursión sin memoria", [("void resuelvePar(const int S[5][5]) {", RECURSIVA)], prueba=[9, 10], v="tle"),
]
