"""12-9 · Una gira agotadora: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso son dos líneas: N (1..150.000) y N recaudaciones (0..10.000).
La suma de los N no pasa de 500.000. Salida: recaudación máxima sin actuar dos días seguidos.
El solucionador es propio: autómata de dos estados (actuó ayer / no), distinto del de la solución.
Validado contra fuerza bruta (todos los calendarios) en miles de casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-9/EJ_12-9.cpp",
    "cabeceras": [],
    "limite_ms": 4000,
    "fallo": ["max(anterior, dosAtras + r)", "max(anterior, anterior + r)"],
}


def resuelve(a):
    actuo, libre = 0, 0
    for x in a:
        actuo, libre = libre + x, max(libre, actuo)
    return max(actuo, libre)


def _bruta(a):
    mejor = 0
    for m in range(1 << len(a)):
        if not m & (m >> 1):
            mejor = max(mejor, sum(x for i, x in enumerate(a) if m >> i & 1))
    return mejor


_r = random.Random(9)
for _ in range(2000):
    _a = [_r.randint(0, 20) for _ in range(_r.randint(1, 10))]
    assert resuelve(_a) == _bruta(_a), _a


def texto(casos):
    return f"{len(casos)}\n" + "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a in casos)


def salida(casos):
    return "".join(f"{resuelve(a)}\n" for a in casos)


def pruebas():
    r = random.Random(129)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        assert sum(map(len, casos)) <= 500000
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    p("Ejemplo del enunciado", "enunciado", [[10, 1, 10, 10, 1], [50], [5, 5, 5, 5], [1, 8, 1, 1, 8, 3]],
      "Los cuatro casos del PDF: 21, 50, 10 y 16.",
      {"wa": "Falla el ejemplo: cada día o se descansa o se actúa habiendo descansado el anterior.", "pe": "Un entero por línea."},
      ["gira(i) = max(gira(i−1), gira(i−2) + r_i).", "gira(0) = 0 y gira(1) = r_1."])
    p("Uno y dos días", "borde", [[0], [10000], [3, 8], [8, 3], [7, 7]],
      "Calendarios mínimos.",
      {"wa": "Con un día se actúa; con dos, el mejor de los dos.", "rte": "No accedas a gira(i−2) si no existe."},
      ["gira(1) = r_1.", "gira(2) = max(r_1, r_2)."])
    p("Días sin recaudación", "borde", [[0, 0, 0], [0, 5, 0, 5, 0], [9, 0, 0, 9]],
      "Ceros en el calendario.", {"wa": "Un día con 0 no suma, pero tampoco obliga a nada."},
      ["En [9, 0, 0, 9] se actúa el primero y el último.", "Pueden descansarse varios días seguidos."])
    p("Descansar dos días seguidos", "trampa", [[1, 8, 1, 1, 8, 3], [9, 1, 1, 9], [10, 1, 1, 1, 10]],
      "Alternar pares o impares no es óptimo.",
      {"wa": "No basta con sumar los días pares o los impares: a veces conviene descansar dos seguidos."},
      ["En [9, 1, 1, 9] lo óptimo es 18.", "Usa la recurrencia, no las dos sumas alternas."])
    p("El voraz del día más caro falla", "trampa", [[4, 5, 4], [9, 10, 9, 1], [2, 3, 2, 3, 2]],
      "Coger el mayor y tachar sus vecinos pierde dinero.",
      {"wa": "Un voraz no sirve: en 4 5 4 es mejor 4 + 4 que 5."},
      ["Compara 5 con 4 + 4.", "gira(i) compara descansar con actuar."])
    p("Varios casos seguidos", "trampa", [[100, 100, 100], [1], [2, 1], [3, 3, 3]],
      "El resultado de un caso no debe arrastrarse al siguiente.",
      {"wa": "Reinicia las dos variables en cada caso."},
      ["¿Dónde declaras las variables?", "Dentro de resuelveCaso."])
    p("Calendarios pequeños al azar", "aleatorio", [[r.randint(0, 30) for _ in range(r.randint(1, 12))] for _ in range(300)],
      "300 casos cortos.", {"wa": "Busca el primer caso distinto y hazlo a mano."},
      ["Escribe la fila gira(0..N).", "Revisa el orden al desplazar las dos variables."])
    p("Calendarios medianos", "aleatorio", [[r.randint(0, 10000) for _ in range(1000)] for _ in range(50)],
      "50 calendarios de 1.000 días.", {"wa": "Revisa la recurrencia.", "tle": "La recursión sin memoria es exponencial."},
      ["O(N) por caso.", "Basta con dos variables."])
    p("El máximo número de días", "rendimiento", [[10000] * 150000],
      "150.000 días con la máxima recaudación: 750.000.000.",
      {"tle": "O(N) por caso.", "rte": "No uses recursión de 150.000 niveles ni arrays locales enormes.",
       "wa": "El resultado cabe en int, pero no en tipos más pequeños."},
      ["Recorre una sola vez.", "Dos variables bastan."])
    p("500.000 días en total", "rendimiento", [[r.randint(0, 10000) for _ in range(125000)] for _ in range(4)],
      "El tamaño total máximo.", {"tle": "O(N) por caso.", "rte": "Cuidado con la pila."},
      ["No hagas trabajo cuadrático.", "Lee y procesa sobre la marcha."])
    return L


RECURSIVA = """int rec(vector<int> const& a, int i) {
    if (i < 0) return 0;
    return max(rec(a, i - 1), rec(a, i - 2) + a[i]);
}

void resuelveCaso() {
    int n0; cin >> n0; vector<int> w0(n0);
    for (int& x : w0) cin >> x;
    cout << rec(w0, n0 - 1) << '\\n';
    return;
"""

VARIANTES = [
    Variante("permite días seguidos", [("max(anterior, dosAtras + r)", "max(anterior, anterior + r)")], prueba=[1, 4, 5], v="wa"),
    Variante("solo alterna pares o impares", [("int actual = max(anterior, dosAtras + r);", "int actual = dosAtras + r;")], prueba=[2, 4, 5, 3], v="wa"),
    Variante("no desplaza dosAtras", [("dosAtras = anterior;", "")], prueba=[4, 5, 3, 2], v="wa"),
    Variante("las variables no se reinician", [("    int dosAtras = 0, anterior = 0;", "    static int dosAtras = 0, anterior = 0;")], prueba=list(range(1, 7)), v="wa"),
    Variante("recursión sin memoria", [("#include <algorithm>", "#include <algorithm>\n#include <vector>"), ("void resuelveCaso() {", RECURSIVA)], prueba=[8, 9], v="tle"),
]
