"""08-3 · Comienza la temporada: juez con pruebas pensadas para cada error típico.

El solucionador (emparejamiento voraz por tallas con dos índices sobre las listas ordenadas) se ha
validado contra fuerza bruta (emparejamiento bipartito máximo por caminos de aumento) en miles de
casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "8-Algoritmos voraces/EJ_08-3/EJ_08-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["int deUnaMas = min(faltan, equipaciones[t + 1]);", "int deUnaMas = min(faltan, equipaciones[t - 1]);"],
}


def comprar(jug, equ):
    """Jugadores de menor a mayor; cada uno toma la equipación libre más pequeña que le vale."""
    j, e = sorted(jug), sorted(equ)
    k = usadas = 0
    for t in j:
        while k < len(e) and e[k] < t:
            k += 1
        if k < len(e) and e[k] <= t + 1:
            usadas += 1
            k += 1
    return len(j) - usadas


def caso_a_texto(c):
    a, b = c
    return f"{len(a)} {len(b)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"


def al_azar(rng, n, m, lo, hi):
    return ([rng.randint(lo, hi) for _ in range(n)], [rng.randint(lo, hi) for _ in range(m)])


def pruebas():
    rng = random.Random(803)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{comprar(*c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [([12] * 5, [13, 14, 12, 10]), ([13, 10, 12], [15, 11, 12, 14]), ([10, 14, 17], [6, 4, 50])],
           "Los tres casos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la regla: a un jugador de talla t le vale una equipación de talla t o de talla t + 1, nada más.",
            "pe": "Los números están bien pero el formato no: un número por línea, uno por caso."},
           ["Sigue a mano el primer caso: a los de talla 12 solo les valen la 12 y la 13.",
            "La primera línea del caso trae N (jugadores) y M (equipaciones): la lista de jugadores tiene N tallas y la de equipaciones M.",
            "Como solo hay 100 tallas, cuenta cuántos jugadores y equipaciones hay de cada una y recórrelas de menor a mayor."])

    # ------------------------------------------------------------------ borde
    prueba("Cada jugador tiene la suya", "borde", [([3, 1, 2], [2, 3, 1])],
           "Tres jugadores y una equipación exacta para cada uno (en otro orden): no hay que comprar ninguna.",
           {"wa": "Con una equipación de su talla para cada jugador la respuesta es 0: ¿comparas posición a posición sin ordenar ni contar por tallas?"},
           ["El orden de la entrada no importa: lo que cuenta es cuántos hay de cada talla.",
            "Cuenta jugadores y equipaciones por talla."])
    prueba("Tallas 1 y 100", "borde", [([1, 100, 100], [2, 100])],
           "Las tallas de los extremos: el de talla 1 usa la 2 y solo uno de los de 100 tiene equipación (hay que comprar 1).",
           {"wa": "Algo falla en las tallas de los extremos: ¿recorres de 1 a 100, ambas incluidas?",
            "rte": "Con talla 100 miras la talla 101: el vector de contadores necesita al menos 102 posiciones."},
           ["Revisa el bucle de tallas: t = 1 … 100 incluidos.",
            "Para mirar la talla t + 1 con t = 100, el vector de contadores debe tener tamaño 102."])

    # ------------------------------------------------------------------ trampas
    prueba("Una talla menos no sirve", "trampa", [([12, 12], [11, 11])],
           "Dos jugadores de talla 12 y equipaciones de talla 11: les quedan pequeñas, hay que comprar 2.",
           {"wa": "Sale menos de 2: dejas usar una equipación de una talla MENOS. Solo valen la propia y la de una talla MÁS (t + 1)."},
           ["«Se les llega a caer como ocurriría con las tallas más pequeñas…»: ¿le vale la 11 a uno de la 12?",
            "Al jugador de talla t solo le valen equipaciones[t] y equipaciones[t + 1]."])
    prueba("Dos tallas más no sirven", "trampa", [([12], [14])],
           "Un jugador de talla 12 y una equipación de talla 14: le queda grande, hay que comprar 1.",
           {"wa": "Sale 0: dejas usar equipaciones de dos (o más) tallas más. Solo vale UNA talla más."},
           ["¿Puede un jugador de la 12 usar la 14? Relee la nota del primer ejemplo.",
            "Mira solo las tallas t y t + 1."])
    prueba("Primero la de su propia talla", "trampa", [([12, 13], [12, 13])],
           "Jugadores 12 y 13 con equipaciones 12 y 13: cada uno la suya (0). Si el de 12 coge la 13, el de 13 se queda sin nada.",
           {"wa": "Sale 1: el jugador de talla t coge antes la de t + 1 que la suya. Primero hay que gastar las de su talla, que nadie más puede usar."},
           ["La equipación de talla 12 solo le vale a los de la 12 (y a los de la 11).",
            "Para la talla t: primero min(jugadores, equipaciones[t]); solo a los que falten, las de t + 1."])
    prueba("Cada equipación la usa un solo jugador", "trampa", [([12, 13], [13])],
           "Jugadores 12 y 13 y una sola equipación de talla 13: uno de los dos se queda sin ella (comprar 1).",
           {"wa": "Sale 0: la misma equipación de talla t + 1 la usan un jugador de t y otro de t + 1. Al darla, hay que descontarla."},
           ["¿Cuántas equipaciones hay en total? ¿Y cuántos jugadores?",
            "Cuando los de talla t usan equipaciones de t + 1, réstalas de equipaciones[t + 1]."])
    prueba("Hay que ir de la talla menor a la mayor", "trampa", [([12, 13], [13, 14])],
           "Jugadores 12 y 13 con equipaciones 13 y 14: el de 12 usa la 13 y el de 13 la 14 (0).",
           {"wa": "Sale 1: recorres las tallas de mayor a menor y el de la 13 se queda la 13, que era la única que le valía al de la 12. Hay que empezar por la talla más pequeña."},
           ["Al jugador de la 12 solo le vale la 13; al de la 13, la 13 o la 14.",
            "Recorre t = 1, 2, …, 100 (de menor a mayor): así los de talla t + 1 aún pueden tirar de t + 2."])
    prueba("Sobran equipaciones pero no valen", "trampa", [([5, 5], [1, 1, 1])],
           "Dos jugadores de talla 5 y tres equipaciones de talla 1: hay más equipaciones que jugadores, pero hay que comprar 2.",
           {"wa": "Sale 0: no basta con comparar cuántos jugadores y cuántas equipaciones hay. Cada equipación tiene que valerle al jugador."},
           ["¿Le vale a alguien de talla 5 una de talla 1?",
            "Empareja por tallas, no por cantidades totales."])
    prueba("Jugadores de una talla que tiran de la siguiente", "trampa", [([10, 10, 10, 11, 11], [10, 11, 11, 11, 12])],
           "Tres de la 10 (usan la 10 y dos de la 11), dos de la 11 (la 11 que queda y la 12): no hay que comprar ninguna.",
           {"wa": "Con varias tallas encadenadas falla: revisa cuántas equipaciones de t + 1 se descuentan y que los de t + 1 usan después las que quedan."},
           ["Sigue la cuenta talla a talla: tras los de la 10, ¿cuántas de la 11 quedan?",
            "Los que no consigan equipación con t ni con t + 1 se suman a «comprar»."])
    prueba("Varios casos seguidos", "trampa",
           [([20, 20, 21], [20, 21, 22]), ([20], [19]), ([20, 21], [21]), ([1, 100], [2, 100])],
           "Casos con las mismas tallas seguidos: nada del caso anterior (contadores por talla) debe quedar.",
           {"wa": "El primer caso sale bien y los siguientes no: los contadores por talla o el total a comprar no se reinician en cada caso."},
           ["Si los vectores de contadores son globales, ¿los pones a cero al empezar cada caso?",
            "Declara los contadores dentro de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 7), rng.randint(1, 7), lo, lo + rng.randint(1, 4))
             for lo in [rng.randint(1, 96) for _ in range(200)]]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 casos de hasta 7 jugadores y 7 equipaciones con tallas muy parecidas.",
           {"wa": "Algún caso falla: localiza la línea, busca el caso y empareja a mano talla a talla."},
           ["La línea que falla es el número de caso.",
            "Revisa el orden de preferencia (primero su talla) y que descuentas las de t + 1."])
    casos = [al_azar(rng, rng.randint(50, 2000), rng.randint(50, 2000), 1, 100) for _ in range(30)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "30 casos con todas las tallas de 1 a 100.",
           {"wa": "Algún caso mediano falla: suele ser una talla de los extremos o el orden del recorrido."},
           ["Comprueba las tallas 1 y 100.",
            "Recorre las tallas de menor a mayor."])

    # ------------------------------------------------------------------ rendimiento
    prueba("100.000 jugadores sin ninguna equipación que les valga", "rendimiento", [([50] * 100000, [1] * 100000)],
           "N = M = 100.000: buscar una equipación para cada jugador recorriendo todas cuesta 10¹⁰.",
           {"tle": "Algo cuesta O(N·M): ¿buscas para cada jugador una equipación recorriendo la lista entera?"},
           ["Con 100.000 jugadores y 100.000 equipaciones, O(N·M) es demasiado.",
            "Solo hay 100 tallas: cuenta cuántos hay de cada una y trabaja con los contadores (O(N + M + 100)).",
            "Otra opción es ordenar las dos listas y recorrerlas con dos índices."])
    casos = [al_azar(rng, 100000, 100000, 1, 100) for _ in range(3)]
    prueba("Tres casos de 100.000 jugadores y equipaciones", "rendimiento", casos,
           "Casos grandes al azar con todas las tallas.",
           {"tle": "Debe ser lineal (o N log N) por caso.",
            "wa": "En los casos grandes falla: revisa el orden de preferencia y el descuento de las equipaciones de t + 1."},
           ["Cuenta por tallas: dos vectores de 102 enteros.",
            "Un recorrido de la talla 1 a la 100 basta."])
    return P


_BLOQUE = """        int deSuTalla = min(faltan, equipaciones[t]);
        faltan -= deSuTalla;
        int deUnaMas = min(faltan, equipaciones[t + 1]);
        equipaciones[t + 1] -= deUnaMas;
        faltan -= deUnaMas;"""

VARIANTES = [
    Variante("deja usar una talla menos", [("equipaciones[t + 1]", "equipaciones[t - 1]")], prueba=4, v="wa"),
    Variante("deja usar dos tallas más",
             [("MAX_TALLA + 2, 0), equipaciones(MAX_TALLA + 2, 0)", "MAX_TALLA + 3, 0), equipaciones(MAX_TALLA + 3, 0)"),
              ("        faltan -= deUnaMas;", "        faltan -= deUnaMas;\n        int deDos = min(faltan, equipaciones[t + 2]);\n        equipaciones[t + 2] -= deDos;\n        faltan -= deDos;")],
             prueba=5, v="wa"),
    Variante("primero la de una talla más",
             [(_BLOQUE, """        int deUnaMas = min(faltan, equipaciones[t + 1]);
        equipaciones[t + 1] -= deUnaMas;
        faltan -= deUnaMas;
        int deSuTalla = min(faltan, equipaciones[t]);
        faltan -= deSuTalla;""")], prueba=6, v="wa"),
    Variante("no descuenta las de una talla más", [("        equipaciones[t + 1] -= deUnaMas;\n", "")], prueba=7, v="wa"),
    Variante("tallas de mayor a menor", [("for (int t = 1; t <= MAX_TALLA; ++t)", "for (int t = MAX_TALLA; t >= 1; --t)"),
              ("        faltan -= deSuTalla;", "        equipaciones[t] -= deSuTalla;\n        faltan -= deSuTalla;")], prueba=8, v="wa"),
    Variante("solo compara cantidades", [("cout << comprar << '\\n';", "cout << max(0, N - M) << '\\n';")], prueba=[4, 5], v="wa"),
    Variante("contadores sin reiniciar",
             [("vector<int> jugadores(MAX_TALLA + 2, 0), equipaciones(MAX_TALLA + 2, 0);",
               "static vector<int> jugadores(MAX_TALLA + 2, 0), equipaciones(MAX_TALLA + 2, 0);")], prueba=11, v="wa"),
    Variante("busca una equipación para cada jugador (O(N·M))",
             [("""    vector<int> jugadores(MAX_TALLA + 2, 0), equipaciones(MAX_TALLA + 2, 0);
    for (int i = 0; i < N; ++i) { int t; cin >> t; ++jugadores[t]; }
    for (int i = 0; i < M; ++i) { int t; cin >> t; ++equipaciones[t]; }

    int comprar = 0;
    for (int t = 1; t <= MAX_TALLA; ++t) {
        int faltan = jugadores[t];
""" + _BLOQUE + """
        comprar += faltan;
    }""", """    vector<int> jug(N), equ(M);
    for (int& x : jug) cin >> x;
    for (int& x : equ) cin >> x;
    vector<bool> usada(M, false);
    int comprar = 0;
    for (int t = 1; t <= MAX_TALLA; ++t)
        for (int i = 0; i < N; ++i) {
            if (jug[i] != t) continue;
            int elegida = -1;
            for (int k = 0; k < M; ++k) if (!usada[k] && equ[k] == t) { elegida = k; break; }
            if (elegida < 0) for (int k = 0; k < M; ++k) if (!usada[k] && equ[k] == t + 1) { elegida = k; break; }
            if (elegida < 0) ++comprar; else usada[elegida] = true;
        }""")], prueba=14, v="tle"),
    Variante("salida separada por espacios", [("cout << comprar << '\\n';", "cout << comprar << ' ';")], prueba=1, v="pe"),
]
