"""12-7 · Oposiciones a notaría: juez con pruebas pensadas para cada error típico.

Entrada: casos con n (2..200) y n tamaños (1..1.000); acaba con un 0.
Salida: tiempo mínimo para fusionar los documentos vecinos de dos en dos.
El solucionador es propio: PD por intervalos con la optimización de Knuth y memoria sobre
(principio, longitud). Validado contra fuerza bruta (todos los órdenes de fusión).
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-7/EJ_12-7.cpp",
    "cabeceras": ["12-Evaluacion/EJ_12-7/Matriz.h"],
    "limite_ms": 3000,
    "fallo": ["tiempo[i][j] = mejor + suma[j] - suma[i - 1];", "tiempo[i][j] = mejor;"],
}


def resuelve(a):
    n = len(a)
    s = [0]
    for x in a:
        s.append(s[-1] + x)
    c = [[0] * n for _ in range(n)]
    o = [[i] * n for i in range(n)]
    for d in range(1, n):
        for i in range(n - d):
            j = i + d
            lo = o[i][j - 1]
            hi = min(o[i + 1][j], j - 1)
            mejor, mk = None, lo
            for k in range(lo, hi + 1):
                v = c[i][k] + c[k + 1][j]
                if mejor is None or v < mejor:
                    mejor, mk = v, k
            c[i][j] = mejor + s[j + 1] - s[i]
            o[i][j] = mk
    return c[0][n - 1]


def _bruta(a):
    if len(a) == 1:
        return 0
    return min(a[i] + a[i + 1] + _bruta(a[:i] + [a[i] + a[i + 1]] + a[i + 2:]) for i in range(len(a) - 1))


_r = random.Random(7)
for _ in range(800):
    _a = [_r.randint(1, 30) for _ in range(_r.randint(2, 7))]
    assert resuelve(_a) == _bruta(_a), _a


def texto(casos):
    return "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in casos) + "0\n"


def salida(casos):
    return "".join(f"{resuelve(a)}\n" for a in casos)


def pruebas():
    r = random.Random(127)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    p("Ejemplo del enunciado", "enunciado", [[3, 6], [1, 1, 1], [6, 5, 4, 3]],
      "Los tres casos del PDF: 9, 5 y 36.",
      {"wa": "Falla el ejemplo: cada fusión cuesta las páginas del resultado.", "pe": "Un entero por línea.",
       "ole": "El caso con 0 documentos termina la entrada."},
      ["Con dos documentos el coste es su suma.", "tiempo(i, j) = min_k tiempo(i,k) + tiempo(k+1,j) + páginas(i..j)."])
    p("Dos documentos", "borde", [[1, 1], [1000, 1000], [1, 1000]],
      "Una única fusión.", {"wa": "Con dos documentos la respuesta es a + b.", "rte": "Revisa los índices con n = 2."},
      ["tiempo(i, i) = 0.", "Solo hay un k posible."])
    p("No se puede reordenar", "trampa", [[100, 1, 100], [50, 1, 50, 1], [10, 1, 10, 1, 10]],
      "Solo se fusionan documentos vecinos: Huffman da menos de lo posible.",
      {"wa": "No puedes juntar los dos más pequeños si no son vecinos: el orden debe conservarse."},
      ["En 100 1 100 la respuesta es 302, no 303 ni 203.", "PD sobre intervalos contiguos."])
    p("El voraz de vecinos falla", "trampa", [[3, 2, 2, 3], [4, 3, 3, 4], [6, 5, 5, 6, 2]],
      "Unir siempre el par vecino más pequeño no es óptimo.",
      {"wa": "Un voraz no sirve: en 3 2 2 3 es mejor (3 2) (2 3) que empezar por (2 2)."},
      ["Compara 5+5+10 = 20 con 4+7+10 = 21.", "Prueba todos los puntos de corte."])
    p("Incluye los extremos del corte", "trampa", [[1000, 1, 1, 1], [1, 1, 1, 1000], [900, 2, 3, 4, 5]],
      "El mejor corte puede ser k = i o k = j−1.",
      {"wa": "El bucle de k debe ir de i a j−1, los dos incluidos."},
      ["Con un documento enorme en un extremo, se une el último.", "Revisa los límites de k."])
    p("Varios casos seguidos", "trampa", [[r.randint(1, 1000) for _ in range(30)], [2, 3], [7, 7, 7]],
      "Un caso mediano y luego pequeños.",
      {"wa": "Algo se arrastra entre casos: crea la tabla y las sumas en cada caso.", "rte": "El tamaño de la tabla cambia."},
      ["Declara todo dentro de resuelveCaso.", "Sumas acumuladas nuevas en cada caso."])
    p("Casos pequeños al azar", "aleatorio", [[r.randint(1, 50) for _ in range(r.randint(2, 8))] for _ in range(200)],
      "200 casos cortos.", {"wa": "Busca el primer caso distinto."},
      ["Hazlo a mano con la tabla.", "Rellena por longitudes crecientes."])
    p("Casos medianos", "aleatorio", [[r.randint(1, 1000) for _ in range(50)] for _ in range(20)],
      "20 casos de 50 documentos.", {"wa": "Revisa el orden de relleno.", "tle": "Debe ser O(n³)."},
      ["Cada intervalo usa solo intervalos más cortos.", "No recalcules."])
    p("200 documentos al azar", "rendimiento", [[r.randint(1, 1000) for _ in range(200)] for _ in range(3)],
      "El tamaño máximo.", {"tle": "O(n³) con tabla: la recursión sin memoria no acaba.", "rte": "La tabla debe ser n × n."},
      ["¿Cuántas veces calculas cada intervalo?", "Usa una tabla."])
    p("200 documentos iguales", "rendimiento", [[1000] * 200, [1] * 200],
      "El mayor tiempo posible.", {"tle": "O(n³) con tabla.", "wa": "El resultado cabe en int."},
      ["Con todos iguales sale un árbol equilibrado.", "Programación dinámica ascendente."])
    return L


RECURSIVA = """int rec(vector<int> const& s, int i, int j) {
    if (i == j) return 0;
    int m = rec(s, i, i) + rec(s, i + 1, j);
    for (int k = i + 1; k < j; ++k) m = min(m, rec(s, i, k) + rec(s, k + 1, j));
    return m + s[j] - s[i - 1];
}

bool resuelveCaso() {
    int n0; cin >> n0; if (!cin || n0 == 0) return false;
    vector<int> s0(n0 + 1, 0);
    for (int i = 1; i <= n0; ++i) { int x; cin >> x; s0[i] = s0[i - 1] + x; }
    cout << rec(s0, 1, n0) << '\\n';
    return true;
}

bool resuelveCasoViejo() {
"""

VOZ = """bool resuelveCaso() {
    int n0; cin >> n0; if (!cin || n0 == 0) return false;
    vector<int> d(n0); for (int& x : d) cin >> x;
    int total = 0;
    while (d.size() > 1) {
        int m = 0;
        for (int i = 1; i + 1 < (int)d.size(); ++i) if (d[i] + d[i + 1] < d[m] + d[m + 1]) m = i;
        d[m] += d[m + 1]; total += d[m]; d.erase(d.begin() + m + 1);
    }
    cout << total << '\\n';
    return true;
}

bool resuelveCasoViejo() {
"""

VARIANTES = [
    Variante("olvida el coste de la última fusión", [("tiempo[i][j] = mejor + suma[j] - suma[i - 1];", "tiempo[i][j] = mejor;")], prueba=[3, 1, 2], v="wa"),
    Variante("páginas sin el primer documento", [("suma[j] - suma[i - 1]", "suma[j] - suma[i]")], prueba=[3, 1, 2], v="wa"),
    Variante("no prueba el último corte", [("k < j; ++k", "k < j - 1; ++k")], prueba=[6, 5], v="wa"),
    Variante("voraz: el par vecino más pequeño", [("bool resuelveCaso() {", VOZ)], prueba=[4, 3, 5], v="wa"),
    Variante("recursión sin memoria", [("bool resuelveCaso() {", RECURSIVA)], prueba=[6, 8], v="tle"),
]
