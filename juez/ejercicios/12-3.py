"""12-3 · Bollos preñaos: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno N (1..50) y M (1..1.000) y N líneas g c m p (todos 1..100):
gramos de chorizo de ese tipo, gramos de chorizo y de masa por bollo y precio del bollo.
Salida: el máximo de euros. Es una mochila con cantidades acotadas: del tipo i hay k_i = g_i / c_i
bollos (división entera) y la masa es la capacidad.

El solucionador es propio: descompone cada tipo en lotes de 1, 2, 4, ... bollos (descomposición
binaria) y hace una mochila 0/1 sobre la masa, recorriendo j de mayor a menor (distinto de la
solución del repo, que prueba cada cantidad t con una copia de la fila). Validado contra fuerza
bruta (todas las combinaciones de cantidades) en miles de casos pequeños.
La respuesta cabe de sobra en int (como mucho 50 · 100 · 100 = 500.000): no hay prueba de desbordamiento.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_12-3/EJ_12-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["int k = g / c;", "int k = M / m;"],
}


def resuelve(M, tipos):
    best = [0] * (M + 1)
    for g, c, m, p in tipos:
        k, lote = g // c, 1
        while k > 0:
            q = min(lote, k)
            k -= q
            w, v = q * m, q * p
            for j in range(M, w - 1, -1):
                if best[j - w] + v > best[j]:
                    best[j] = best[j - w] + v
            lote *= 2
    return best[M]


def fuerza_bruta(M, tipos):
    def rec(i, resto):
        if i == len(tipos):
            return 0
        g, c, m, p = tipos[i]
        return max(t * p + rec(i + 1, resto - t * m) for t in range(0, g // c + 1) if t * m <= resto)
    return rec(0, M)


def aleatorio(rng, nmax, mmax, vmax):
    n = rng.randint(1, nmax)
    return (rng.randint(1, mmax), [tuple(rng.randint(1, vmax) for _ in range(4)) for _ in range(n)])


def caso_a_texto(c):
    M, t = c
    return f"{len(t)} {M}\n" + "".join("%d %d %d %d\n" % x for x in t)


RELLENO = (100, 1, 1, 1)   # tipo de 1 € por gramo de masa, sin límite práctico: hace que se gaste toda la masa


def pruebas():
    rng = random.Random(2002)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [(100, [(15, 5, 20, 10)])],
           "Un solo tipo: la masa da para 5 bollos pero el chorizo solo para 3 (30 €).",
           {"wa": "Falla el primer ejemplo: el número de bollos de un tipo lo limitan a la vez su chorizo (g / c) y la masa (M / m).",
            "pe": "Escribe solo el número de euros, con un salto de línea por caso."},
           ["Con 15 g de chorizo y 5 por bollo, ¿cuántos bollos salen?",
            "bollos(i, j) = máximo de bollos(i−1, j − t·m_i) + t·p_i para t = 0..k_i con t·m_i ≤ j.",
            "La respuesta es bollos(N, M)."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(8, [(18, 3, 1, 10), (7, 3, 2, 100)])],
           "Dos bollos del segundo tipo y cuatro del primero con la masa que queda (240 €).",
           {"wa": "Falla el segundo ejemplo: hay que combinar tipos; prueba todas las cantidades de cada tipo con la masa que queda."},
           ["Del segundo tipo salen 7 / 3 = 2 bollos, que gastan 4 g de masa.",
            "Con la tabla, para cada tipo y cada cantidad de masa j se prueba cuántos bollos t hacer de ese tipo."])
    prueba("No da para ningún bollo", "borde", [(1, [(100, 1, 2, 100)]), (100, [(2, 3, 1, 100)]), (1, [(1, 1, 1, 1)])],
           "Casos donde no llega la masa o el chorizo (0 €) y el caso más pequeño con un bollo (1 €).",
           {"wa": "Cuando no se puede hacer ningún bollo la respuesta es 0: el chorizo (g < c) o la masa (m > M) no llegan.",
            "rte": "Con M = 1 o k = 0 te sales de la tabla: revisa que j − t·m ≥ 0."},
           ["Con 2 g de chorizo y 3 por bollo, ¿cuántos bollos salen?",
            "Si k = 0 o m > j, el único valor posible es no hacer ningún bollo de ese tipo (t = 0)."])
    prueba("Varios bollos del mismo tipo", "trampa", [(9, [(6, 2, 3, 10)])],
           "Del mismo tipo se pueden hacer varios bollos: aquí 3, que gastan toda la masa (30 €).",
           {"wa": "Solo haces un bollo de cada tipo (mochila 0/1). De cada tipo se pueden hacer hasta k = g / c bollos."},
           ["Con 6 g de chorizo, 2 por bollo y 9 g de masa, salen 3 bollos.",
            "En la recurrencia, elige cuántos bollos t (de 0 a k) haces del tipo i, no solo si lo usas o no."])
    prueba("El chorizo limita cuántos bollos salen", "trampa", [(10, [(10, 5, 1, 50), RELLENO])],
           "El primer tipo vale mucho y gasta poca masa, pero su chorizo solo da para 2 bollos (2 · 50 + 8 · 1 = 108).",
           {"wa": "Haces más bollos de un tipo de los que permite su chorizo (o cuentas dos veces bollos del mismo tipo al rellenar la fila). Como mucho k = g / c."},
           ["Con 10 g de chorizo y 5 por bollo, ¿cuántos bollos del primer tipo puedes hacer?",
            "El bucle de t tiene que parar en k = g / c además de en t·m ≤ j.",
            "Si actualizas la misma fila que lees, un bollo del tipo i se puede volver a usar: calcula la fila nueva a partir de una copia de la anterior."])
    prueba("Bollos por tipo: división entera", "trampa", [(10, [(7, 3, 1, 10), RELLENO])],
           "Con 7 g de chorizo y 3 por bollo salen 2 bollos, no 3 (20 + 8 = 28).",
           {"wa": "Redondeas hacia arriba el número de bollos de un tipo. k = g / c es la división entera: el chorizo que sobra no da para otro bollo."},
           ["¿Cuántos bollos de 3 g salen con 7 g de chorizo?",
            "Usa la división entera g / c, sin redondear hacia arriba."])
    prueba("Puede sobrar masa", "trampa", [(9, [(100, 1, 2, 7)])],
           "Los bollos gastan 2 g de masa y hay 9: se hacen 4 y sobra 1 g (28 €).",
           {"wa": "Exiges gastar toda la masa. La tabla debe guardar lo mejor con COMO MUCHO j gramos: empieza con 0 en todas las casillas, no con −∞."},
           ["Con 9 g y bollos de 2 g, ¿se puede gastar toda la masa?",
            "bollos(0, j) = 0 para todo j: no hacer nada siempre vale."])
    prueba("Cada tipo tiene su propio chorizo", "trampa", [(12, [(4, 4, 3, 30), (4, 4, 3, 30), (8, 4, 3, 30)])],
           "Cada tipo gasta solo su chorizo: del primero y del segundo sale 1 bollo y del tercero 2 (120 €).",
           {"wa": "El chorizo no es una segunda capacidad compartida: cada tipo tiene el suyo, que solo sirve para calcular su tope k = g / c."},
           ["¿Cuántos bollos salen de cada tipo por separado?",
            "La única capacidad compartida es la masa; el chorizo se convierte en el tope k de cada tipo."])
    prueba("Lo más caro primero no siempre conviene", "trampa", [(10, [(1, 1, 10, 100), (2, 1, 5, 60)])],
           "El bollo más caro gasta toda la masa (100 €); dos del otro tipo dan 120 €.",
           {"wa": "Haces primero los bollos más caros (voraz por precio): no da el óptimo. Hace falta la tabla de programación dinámica."},
           ["Compara un bollo de 100 € que gasta 10 g con dos de 60 € que gastan 5 g cada uno.",
            "Ninguna regla de orden sirve: la tabla prueba todas las cantidades de cada tipo."])
    prueba("Lo de más euros por gramo de masa tampoco", "trampa", [(10, [(1, 1, 6, 60), (2, 1, 5, 45)])],
           "El primer tipo da 10 €/g y el segundo 9 €/g, pero tras el primero sobran 4 g inútiles: mejor dos del segundo (90 €).",
           {"wa": "Eliges por euros por gramo de masa (voraz): la masa que sobra y el tope de chorizo lo estropean. Hace falta la tabla."},
           ["Con un bollo del primer tipo sobran 4 g, que no dan para nada.",
            "La mochila con cantidades acotadas no se resuelve con un voraz: rellena la tabla bollos(i, j)."])
    prueba("Valores máximos", "borde", [(1000, [(100, 100, 100, 100)] * 50), (1000, [(100, 1, 1, 100)] * 50)],
           "50 tipos con todos los valores a 100 (1000 €) y 50 tipos de 1 g de masa y 100 bollos cada uno (100.000 €).",
           {"wa": "Con los valores máximos falla: revisa el tamaño de la tabla (M + 1) y que el bucle de t llegue a k."},
           ["En el segundo caso hay 5000 bollos posibles y masa para 1000: la respuesta es 1000 · 100.",
            "Tabla de M + 1 posiciones, j de 0 a M incluido."])
    prueba("Varios casos seguidos", "trampa", [(1000, [(100, 1, 7, 93), (50, 3, 11, 40), (90, 9, 2, 17)]), (5, [(5, 1, 1, 1)]), (3, [(9, 3, 1, 4), (1, 1, 1, 50)])],
           "Un caso grande y luego otros pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla): créala dentro de la función de cada caso con M + 1 posiciones.",
            "rte": "La tabla de un caso anterior tiene otro tamaño: créala en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara la tabla dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio(rng, 5, rng.choice([10, 40, 100]), rng.choice([10, 30, 100])) for _ in range(200)],
           "200 casos al azar con hasta 5 tipos.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla y hazlo en papel.",
            "Revisa el tope k = g / c, que puede sobrar masa y que se prueban todas las cantidades t."])
    prueba("Aleatorios medianos", "aleatorio", [aleatorio(rng, 50, 1000, 100) for _ in range(30)],
           "30 casos al azar con hasta 50 tipos y 1000 g de masa.",
           {"wa": "Falla en casos más grandes: revisa los bordes de la tabla.",
            "tle": "Una recursión sin memoria no termina con 50 tipos: guarda bollos(i, j) en una tabla."},
           ["¿Calculas el mismo bollos(i, j) muchas veces? Apúntalo en una tabla.",
            "Rellena la tabla tipo a tipo: cada fila solo necesita la anterior."])
    peor = [(1000, [(100, 1, 1, rng.randint(1, 100)) for _ in range(50)]) for _ in range(12)]
    prueba("Muchos bollos posibles", "rendimiento", peor,
           "12 casos con 50 tipos de los que salen 100 bollos de 1 g de masa: el peor caso de la tabla.",
           {"tle": "Es lento: la tabla tiene M + 1 columnas por tipo y en cada casilla se prueban hasta k cantidades; O(M · suma de k) por caso, unos 5·10⁶ pasos. ¿Haces algo más?",
            "mle": "Basta una fila de M + 1 (o N + 1 filas): no hace falta una dimensión para el chorizo."},
           ["Cuenta las operaciones: tipos × masa × bollos posibles.",
            "No añadas una dimensión de chorizo a la tabla: cada tipo tiene su propio tope k."])
    prueba("Casos grandes al azar", "rendimiento", [aleatorio(rng, 50, 1000, 100) for _ in range(40)] + [(1000, [(100, 1, 1, 1)] * 50)],
           "40 casos grandes al azar y uno con todo al mínimo de precio.",
           {"tle": "Es lento con muchos casos grandes: el coste por caso debe ser O(M · suma de k).",
            "wa": "Falla algún caso grande: busca la línea que falla en la entrada."},
           ["Comprueba que no recorres más de lo necesario en el bucle de t (para cuando t·m > j).",
            "Una fila de M + 1 enteros por tipo basta."])
    for c in (c for x in P for c in x[2]):
        M, t = c
        assert 1 <= M <= 1000 and 1 <= len(t) <= 50 and all(1 <= v <= 100 for x in t for v in x)
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d\n" % resuelve(*c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


def _voraz(clave):
    return ("void resuelveCaso() {",
            "void resuelveCaso() {\n    int N0, M0; cin >> N0 >> M0; vector<vector<int>> T(N0, vector<int>(4));\n"
            "    for (auto& x : T) cin >> x[0] >> x[1] >> x[2] >> x[3];\n"
            "    sort(T.begin(), T.end(), [](const vector<int>& a, const vector<int>& b) { return " + clave + "; });\n"
            "    int resto = M0, total = 0;\n"
            "    for (auto& x : T) { int t = min(x[0] / x[1], resto / x[2]); resto -= t * x[2]; total += t * x[3]; }\n"
            "    cout << total << '\\n'; return;\n")


VARIANTES = [
    Variante("un bollo por tipo (mochila 0/1)", [("for (int t = 1; t <= k && t * m <= j; ++t)", "for (int t = 1; t <= min(k, 1) && t * m <= j; ++t)")], prueba=4, v="wa"),
    Variante("sin tope de chorizo", [("for (int t = 1; t <= k && t * m <= j; ++t)", "for (int t = 1; t * m <= j; ++t)")], prueba=5, v="wa"),
    Variante("actualiza la misma fila", [("nueva[j] = max(nueva[j], euros[j - t * m] + t * p);", "nueva[j] = max(nueva[j], nueva[j - t * m] + t * p);")], prueba=5, v="wa"),
    Variante("redondea hacia arriba", [("int k = g / c;", "int k = (g + c - 1) / c;")], prueba=6, v="wa"),
    Variante("exige gastar toda la masa", [("vector<int> euros(M + 1, 0);", "vector<int> euros(M + 1, -1000000);\n    euros[0] = 0;")], prueba=7, v="wa"),
    Variante("voraz por precio", [_voraz("a[3] > b[3]")], prueba=9, v="wa"),
    Variante("voraz por euros por gramo de masa", [_voraz("a[3] * b[2] > b[3] * a[2]")], prueba=10, v="wa"),
]
