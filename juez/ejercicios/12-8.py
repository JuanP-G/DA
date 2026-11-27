"""12-8 · Volando entre pivotes: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso es una línea con N (2..100.000) y K (0..10).
Salida: formas de ir del pivote 1 al N saltando como mucho K pivotes, módulo 1.000.000.007.
El solucionador es propio: «hacia delante» (cada pivote reparte sus formas a los siguientes),
al revés que la ventana de la solución del repo. Validado contra fuerza bruta.
"""
import random
from functools import lru_cache
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-8/EJ_12-8.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["ventana - formas[i - k - 1] + MOD", "ventana - formas[i - k] + MOD"],
}
M = 10**9 + 7


def resuelve(n, k):
    dif = [0] * (n + k + 3)
    act, f = 0, 0
    for i in range(1, n + 1):
        act = (act + dif[i]) % M
        f = 1 if i == 1 else act
        dif[i + 1] += f
        dif[i + k + 2] -= f
    return f


@lru_cache(maxsize=None)
def _bruta(n, k):
    return 1 if n == 1 else sum(_bruta(n - d, k) for d in range(1, k + 2) if n - d >= 1)


for _n in range(2, 30):
    for _k in range(0, 11):
        assert resuelve(_n, _k) == _bruta(_n, _k) % M, (_n, _k)


def texto(casos):
    return f"{len(casos)}\n" + "".join(f"{n} {k}\n" for n, k in casos)


def salida(casos):
    return "".join(f"{resuelve(n, k)}\n" for n, k in casos)


def pruebas():
    r = random.Random(128)
    L = []

    def p(nombre, tipo, casos, comprueba, si, pistas):
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    p("Ejemplo del enunciado", "enunciado", [(10, 0), (3, 1), (4, 2), (2, 4)],
      "Los cuatro casos del PDF: 1, 2, 4 y 1.",
      {"wa": "Falla el ejemplo: desde un pivote se avanza entre 1 y K+1 posiciones.", "pe": "Un número por línea."},
      ["Con K = 0 solo hay una forma.", "formas(i) = suma de las K+1 anteriores, con formas(1) = 1."])
    p("Dos pivotes", "borde", [(2, k) for k in range(11)],
      "Con dos pivotes siempre hay una forma, sea cual sea K.",
      {"wa": "Los índices menores que 1 no existen: no los sumes.", "rte": "Cuidado con i − K − 1 negativo."},
      ["Solo se puede ir del 1 al 2.", "Suma solo los pivotes con índice ≥ 1."])
    p("Sin saltarse ninguno", "borde", [(5, 0), (100000, 0), (3, 0)],
      "K = 0: siempre 1.",
      {"wa": "Con K = 0 la ventana tiene un solo elemento."},
      ["formas(i) = formas(i−1).", "Revisa qué sale de la ventana."])
    p("K + 1 posiciones, no K", "trampa", [(3, 1), (4, 1), (5, 2), (6, 3)],
      "Saltarse K pivotes permite avanzar hasta K+1.",
      {"wa": "La ventana debe tener K+1 elementos: con K = 1 se llega desde i−1 y desde i−2."},
      ["Con K = 1 sale Fibonacci.", "Resta formas(i−K−1), no formas(i−K)."])
    p("N pequeño y K grande", "trampa", [(3, 10), (5, 10), (11, 10), (12, 10), (13, 10)],
      "Mientras i ≤ K+1 todos los anteriores cuentan (potencias de 2).",
      {"wa": "Al principio la ventana está incompleta: no restes nada hasta que haya K+1 anteriores.",
       "rte": "No leas posiciones antes del pivote 1."},
      ["Con K grande, formas(i) = 2^(i−2) al principio.", "Resta solo si i − K − 1 ≥ 1."])
    p("Aparece el módulo", "trampa", [(45, 1), (60, 1), (100, 2), (200, 10)],
      "Los valores pasan de 10^9+7: hay que reducir en cada paso.",
      {"wa": "Reduce módulo 1.000.000.007 en cada suma; al restar, suma antes el módulo para no quedar negativo."},
      ["Si sale un número negativo, es la resta.", "(a − b + MOD) % MOD."])
    p("Varios casos seguidos", "trampa", [(50, 3), (5, 1), (40, 7), (2, 0), (6, 2)],
      "Un caso grande y luego pequeños: nada debe quedar de uno a otro.",
      {"wa": "Reinicia la ventana y la tabla en cada caso."},
      ["¿Dónde declaras la suma acumulada?", "Todo dentro de resuelveCaso."])
    p("Todos los N hasta 40", "aleatorio", [(n, k) for n in range(2, 41) for k in (1, 3)],
      "Valores consecutivos con K = 1 y K = 3.",
      {"wa": "Calcula a mano el primer N que falla."},
      ["Escribe la fila formas(1..N).", "Compárala con la suma directa."])
    p("Casos al azar", "aleatorio", [(r.randint(2, 500), r.randint(0, 10)) for _ in range(200)],
      "200 casos medianos.", {"wa": "Algún valor de K falla: pruébalos todos de 0 a 10."},
      ["Mira el primer caso distinto.", "Revisa los extremos K = 0 y K = 10."])
    p("Casos grandes al azar", "rendimiento", [(r.randint(50000, 100000), r.randint(0, 10)) for _ in range(30)],
      "30 casos con cientos de miles de pivotes en total.",
      {"tle": "Cada caso debe costar O(N) u O(N·K).", "wa": "Con valores grandes reduce módulo en cada paso.",
       "rte": "No uses un array local fijo demasiado pequeño."},
      ["La recursión sin memoria es exponencial.", "Rellena la tabla de 1 a N."])
    p("N máximo y K máximo", "rendimiento", [(100000, 10)] * 20 + [(100000, 1)] * 5,
      "El tamaño máximo, muchas veces.",
      {"tle": "Rellena la tabla una vez por caso, en O(N·K) como mucho.", "mle": "Un vector de N enteros basta.",
       "wa": "Revisa el módulo."},
      ["No recalcules lo ya calculado.", "Programación dinámica ascendente."])
    return L


RECURSIVA = """long long rec(int i, int k) {
    if (i == 1) return 1;
    long long s = 0;
    for (int d = 1; d <= k + 1 && i - d >= 1; ++d) s = (s + rec(i - d, k)) % MOD;
    return s;
}

void resuelveCaso() {
    int n0, k0; cin >> n0 >> k0;
    cout << rec(n0, k0) << '\\n';
    return;
"""

VARIANTES = [
    Variante("ventana de K en vez de K+1", [("if (i - k - 1 >= 1)", "if (i - k >= 1)"), ("formas[i - k - 1]", "formas[i - k]")], prueba=[4, 3, 2], v="wa"),
    Variante("sin módulo en la suma", [("(ventana + formas[i]) % MOD", "(ventana + formas[i])"), ("(ventana - formas[i - k - 1] + MOD) % MOD", "(ventana - formas[i - k - 1])")], prueba=[6], v="wa"),
    Variante("nunca saca de la ventana", [("if (i - k - 1 >= 1)", "if (false)")], prueba=[6, 3, 4], v="wa"),
    Variante("la ventana no se reinicia", [("    long long ventana = 1;", "    static long long ventana = 1;")], prueba=list(range(1, 8)), v="wa"),
    Variante("recursión sin memoria", [("void resuelveCaso() {", RECURSIVA)], prueba=[6, 7, 8], v="tle"),
]
