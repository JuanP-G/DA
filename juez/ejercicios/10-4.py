"""10-4 · ¿Por dónde hay que subir?: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno N (3..1.000) y un tablero N×N con números 1..10.000.
Salida: la suma máxima de un recorrido que sube desde la última fila hasta la primera (en cada
paso, vertical o diagonal) y la columna (1..N) de la última fila donde empieza; si hay varias,
la de más a la izquierda.
El solucionador es propio: calcula, de abajo arriba, la mejor suma desde cada casilla de la
última fila hasta cada casilla (avanza hacia ARRIBA, al revés que la solución del repo, que
acumula desde la primera fila). Validado contra fuerza bruta (todos los recorridos) en miles de
tableros pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "10-Programacion dinamica/EJ_10-4/EJ_10-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["if (mejor[N - 1][j] > mejor[N - 1][col]) col = j;", "if (mejor[N - 1][j] >= mejor[N - 1][col]) col = j;"],
}


def resuelve(t):
    """Para cada columna de salida c, la mejor suma subiendo desde (N-1, c). Se hace al revés:
    sube[j] = mejor suma de un camino desde la primera fila hasta la casilla (i, j) bajando, y por
    simetría es lo mismo que subir desde (i, j) hasta la primera fila."""
    N = len(t)
    sube = list(t[0])
    for i in range(1, N):
        fila = t[i]
        sube = [fila[j] + max(sube[max(0, j - 1):j + 2]) for j in range(N)]
    mejor = max(sube)
    return mejor, sube.index(mejor) + 1


def fuerza_bruta(t):
    N = len(t)
    mejor, col = -1, None
    for c in range(N):
        def rec(i, j):
            if i == 0:
                return t[0][j]
            return t[i][j] + max(rec(i - 1, k) for k in (j - 1, j, j + 1) if 0 <= k < N)
        s = rec(N - 1, c)
        if s > mejor:
            mejor, col = s, c + 1
    return mejor, col


def aleatorio(rng, N, vmax):
    return [[rng.randint(1, vmax) for _ in range(N)] for _ in range(N)]


def caso_a_texto(t):
    return f"{len(t)}\n" + "".join(" ".join(map(str, f)) + "\n" for f in t)


def pruebas():
    rng = random.Random(1004)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [[[2, 5, 8, 3], [1, 4, 2, 9], [9, 2, 8, 5], [3, 5, 2, 1]]],
           "El tablero de la figura: se empieza en la columna 2 y se consigue 30.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: la mejor suma desde una casilla es su valor más la mejor de las (hasta) tres casillas de encima.",
            "pe": "Escribe la suma, un espacio y la columna, con un salto de línea por caso."},
           ["Calcula a mano la tabla para este tablero, fila a fila, y compárala con la tuya.",
            "mejor(i, j) = t(i, j) + máximo de mejor(i−1, j−1), mejor(i−1, j), mejor(i−1, j+1) (solo las que existen).",
            "La respuesta es el máximo de la última fila de la tabla y su columna, contada desde 1."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [[[1, 1, 1], [1, 1, 1], [1, 1, 1]]],
           "Todo unos: cualquier columna vale; se prefiere la de más a la izquierda (3 1).",
           {"wa": "Con empate hay que dar la columna de más a la izquierda: la 1, no la última."},
           ["Si escribes «3 3», te quedas con la última columna que empata.",
            "Al buscar el máximo de izquierda a derecha, cambia de columna solo si la nueva es estrictamente mayor (>)."])
    prueba("Tablero mínimo (3×3)", "borde", [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[9, 1, 1], [1, 1, 9], [1, 9, 1]]],
           "Tableros de 3×3, el tamaño más pequeño permitido.",
           {"wa": "Con N = 3 la columna del centro tiene tres casillas encima y las de los lados solo dos: revisa los bordes.",
            "rte": "Te sales del tablero al mirar la diagonal desde la primera o la última columna."},
           ["Haz a mano el segundo tablero: 9 → 9 → 9 subiendo en zigzag.",
            "Antes de mirar j − 1 comprueba j > 0, y antes de mirar j + 1, j + 1 < N."])
    prueba("Columnas numeradas desde 1", "trampa", [[[1, 1, 5], [1, 1, 1], [1, 1, 5]]],
           "El mejor recorrido empieza en la última columna: debe salir «11 3».",
           {"wa": "Escribes la columna contando desde 0. El enunciado numera las columnas de 1 a N."},
           ["¿Qué número escribes para la última columna de un tablero de 3×3?",
            "Si guardas la columna como índice de un vector (desde 0), súmale 1 al escribirla."])
    prueba("Subir en vertical", "trampa", [[[1, 1, 9, 1, 1], [1, 1, 9, 1, 1], [1, 1, 9, 1, 1], [1, 1, 9, 1, 1], [1, 1, 9, 1, 1]]],
           "La mejor forma es subir recto por una columna (45, columna 3).",
           {"wa": "No tienes en cuenta la casilla que está justo encima: los movimientos son vertical y las dos diagonales."},
           ["¿Puede tu programa ir de (i, j) a (i−1, j)?",
            "El máximo de arriba tiene que considerar las tres casillas: j−1, j y j+1."])
    prueba("Subir en diagonal", "trampa", [[[1, 1, 9, 1, 1], [1, 9, 1, 1, 1], [1, 1, 9, 1, 1], [1, 1, 1, 9, 1], [1, 1, 9, 1, 1]]],
           "El mejor recorrido sube en zigzag: unas veces en diagonal hacia la izquierda y otras hacia la derecha.",
           {"wa": "Te falta alguna de las dos diagonales (o solo miras una): desde (i, j) se puede ir a (i−1, j−1) y a (i−1, j+1)."},
           ["El mejor recorrido suma 45 y pasa por los cinco 9: dibújalo.",
            "Comprueba que en el máximo entran j − 1 y j + 1, cada una con su comprobación de borde."])
    prueba("No se puede dar la vuelta por los lados", "trampa", [[[1, 1, 1, 50], [1, 1, 1, 1], [50, 1, 1, 1], [1, 1, 1, 2]]],
           "La primera y la última columna NO son vecinas: el tablero no da la vuelta.",
           {"wa": "Tratas el tablero como si fuera circular (desde la columna 1 se llega a la N o al revés). Los movimientos no pueden salirse del tablero."},
           ["Desde la columna 1 solo se puede subir a las columnas 1 y 2.",
            "No uses índices módulo N: si j − 1 < 0 o j + 1 ≥ N, esa casilla no existe."])
    prueba("La columna es la de la última fila", "trampa", [[[1, 1, 1, 9], [1, 1, 9, 1], [1, 9, 1, 1], [1, 2, 1, 1]]],
           "El recorrido óptimo empieza abajo en una columna (2) y acaba arriba en otra (4): se pide la de ABAJO.",
           {"wa": "Escribes la columna donde ACABA el recorrido (la de la primera fila) en vez de aquella donde empieza (la de la última fila)."},
           ["El juego empieza en la última fila y sube: la columna que se pide es la de la fila N.",
            "Si rellenas la tabla de abajo arriba, al final tienes el mejor valor de cada casilla de la fila 1, que no es lo que se pide: rellénala de arriba abajo (o guarda dónde empezó cada camino)."])
    prueba("Lo más grande de arriba no siempre conviene", "trampa", [[[1, 1, 1, 1, 90], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [5, 1, 1, 1, 1], [1, 2, 1, 1, 1]]],
           "Ir siempre a la casilla mayor de encima (voraz) lleva a un recorrido peor.",
           {"wa": "Eliges en cada paso la casilla mayor de las de encima: eso es un voraz y no da el óptimo. Hace falta la tabla de programación dinámica."},
           ["Desde la columna 2 de abajo, el 5 de la izquierda parece mejor, pero arriba a la derecha hay un 90.",
            "La decisión de cada paso depende de lo que queda por encima: calcula mejor(i, j) para todas las casillas.",
            "mejor(i, j) = t(i, j) + máximo de los mejor(i−1, ·) de las tres casillas de encima."])
    prueba("Empate entre columnas que no son la primera", "trampa", [[[1, 1, 1, 1, 1]] * 4 + [[1, 7, 1, 7, 1]],
                                                                    [[5, 1, 1, 1, 5]] + [[1, 1, 1, 1, 1]] * 3 + [[1, 1, 3, 1, 1]]],
           "Varias columnas empatan con la suma máxima: hay que quedarse con la de más a la izquierda.",
           {"wa": "Ante un empate te quedas con una columna que no es la de más a la izquierda (sueles usar ≥ en vez de >, o recorres de derecha a izquierda)."},
           ["En el primer tablero empatan las columnas 2 y 4: la respuesta es «9 2».",
            "Recorre la última fila de izquierda a derecha y cambia de columna solo si la suma es estrictamente mayor."])
    prueba("Valores grandes", "trampa", [[[10000] * 3] * 3, [[10000, 1, 10000, 1], [1, 10000, 1, 10000], [10000, 1, 10000, 1], [1, 10000, 1, 10000]]],
           "Casillas con el valor máximo (10.000).",
           {"wa": "Con valores de hasta 10.000, ¿lees bien los números o los guardas en un tipo pequeño (char, short)?"},
           ["La suma máxima es 10.000 · 1.000 = 10⁷: cabe en int, pero no en short.",
            "Usa int para el tablero y para la tabla."])
    prueba("Varios casos seguidos", "trampa",
           [[[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [9, 5, 5, 5, 5, 5]],
            [[1, 2, 1], [1, 1, 2], [1, 1, 1]], [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 2]]],
           "Un tablero grande y luego otros más pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla, el máximo o la columna): créalos dentro de la función de cada caso.",
            "rte": "La tabla de un caso anterior tiene otro tamaño: créala (o redimensiónala) en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara la tabla, el máximo y la columna dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio(rng, rng.randint(3, 8), rng.choice([3, 20, 10000])) for _ in range(60)],
           "60 tableros pequeños al azar (con muchos empates en algunos).",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla y hazlo en papel.",
            "Revisa los bordes y los empates, que son lo que más falla."])
    prueba("Aleatorios medianos", "aleatorio", [aleatorio(rng, rng.randint(20, 60), 10000) for _ in range(10)],
           "10 tableros de hasta 60×60 con valores de hasta 10.000.",
           {"wa": "Falla en tableros algo mayores: revisa los bordes y que se lea el tablero entero.",
            "tle": "Una recursión sin memoria (probar todos los recorridos) crece como 3^N: aquí ya no termina. Guarda cada mejor(i, j) en una tabla."},
           ["¿Calculas el mismo mejor(i, j) muchas veces? Apúntalo en una tabla la primera vez.",
            "Rellena la tabla fila a fila: cada fila solo necesita la de encima."])
    prueba("Tablero 1000×1000 al azar", "rendimiento", [aleatorio(rng, 1000, 9)],
           "El tamaño máximo (10⁶ casillas).",
           {"tle": "Tu solución es lenta para 1000×1000. Debe ser O(N²): cada casilla mira solo tres de la fila de encima.",
            "mle": "Gastas demasiada memoria: basta la fila anterior (o una tabla N×N de int).",
            "rte": "Con N = 1000 se rompe: una tabla tan grande no puede ser un array local (pila); usa vector."},
           ["¿Haces algo más que mirar tres casillas por cada casilla?",
            "Si usas recursión, que sea con memoria; o mejor, rellena la tabla con dos bucles.",
            "Una matriz local int t[1000][1000] desborda la pila: usa vector<vector<int>> o solo dos filas."])
    t = [[1] * 1000 for _ in range(1000)]
    prueba("Tablero 1000×1000 todo unos", "rendimiento", [t],
           "Todo empata en el tamaño máximo: «1000 1».",
           {"tle": "Tu solución es lenta para 1000×1000: debe ser O(N²).",
            "wa": "Con todo empatado hay que dar la columna 1."},
           ["Un recorrido sin memoria tarda 3^N: imposible con N = 1000.",
            "En el empate, cambia de columna solo con > estricto."])
    for c in (c for x in P for c in x[2]):
        assert 3 <= len(c) <= 1000 and all(len(f) == len(c) and all(1 <= v <= 10000 for v in f) for f in c)
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d %d\n" % resuelve(c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("columna desde 0", [("cout << mejor[N - 1][col] << ' ' << col + 1", "cout << mejor[N - 1][col] << ' ' << col")], prueba=4, v="wa"),
    Variante("olvida subir en vertical", [("int mejorArriba = mejor[i - 1][j];", "int mejorArriba = 0;")], prueba=5, v="wa"),
    Variante("solo una diagonal", [("if (j + 1 < N) mejorArriba = max(mejorArriba, mejor[i - 1][j + 1]);", "")], prueba=6, v="wa"),
    Variante("tablero circular", [("if (j > 0) mejorArriba = max(mejorArriba, mejor[i - 1][j - 1]);",
                                   "mejorArriba = max(mejorArriba, mejor[i - 1][(j + N - 1) % N]);")], prueba=7, v="wa"),
    Variante("voraz: sube por la mayor de encima",
             [("void resuelveCaso() {",
               "void resuelveCaso() {\n    int n0; cin >> n0; vector<vector<int>> T(n0, vector<int>(n0));\n"
               "    for (auto& f : T) for (int& x : f) cin >> x;\n    int best = -1, bc = 0;\n"
               "    for (int c = 0; c < n0; ++c) { int s = T[n0-1][c], j = c;\n"
               "        for (int i = n0 - 2; i >= 0; --i) { int bj = j; for (int k = j - 1; k <= j + 1; ++k) if (k >= 0 && k < n0 && T[i][k] > T[i][bj]) bj = k; j = bj; s += T[i][j]; }\n"
               "        if (s > best) { best = s; bc = c; } }\n    cout << best << ' ' << bc + 1 << '\\n'; return;\n")], prueba=9, v="wa"),
    Variante("empate: se queda la de la derecha", [("if (mejor[N - 1][j] > mejor[N - 1][col]) col = j;", "if (mejor[N - 1][j] >= mejor[N - 1][col]) col = j;")], prueba=10, v="wa"),
    Variante("da la columna de la primera fila (rellena de abajo arriba)",
             [("void resuelveCaso() {",
               "void resuelveCaso() {\n    int n0; cin >> n0; vector<vector<int>> T(n0, vector<int>(n0));\n"
               "    for (auto& f : T) for (int& x : f) cin >> x;\n    vector<int> a = T[n0 - 1];\n"
               "    for (int i = n0 - 2; i >= 0; --i) { vector<int> b(n0); for (int j = 0; j < n0; ++j) { int m = a[j];\n"
               "        if (j > 0) m = max(m, a[j - 1]); if (j + 1 < n0) m = max(m, a[j + 1]); b[j] = T[i][j] + m; } a = b; }\n"
               "    int c = 0; for (int j = 1; j < n0; ++j) if (a[j] > a[c]) c = j;\n    cout << a[c] << ' ' << c + 1 << '\\n'; return;\n")], prueba=8, v="wa"),
    Variante("recursión sin memoria (3^N)",
             [("void resuelveCaso() {",
               "int rec(const vector<vector<int>>& T, int i, int j) {\n    if (j < 0 || j >= (int)T.size()) return -1;\n"
               "    if (i == 0) return T[0][j];\n    return T[i][j] + max(rec(T, i - 1, j - 1), max(rec(T, i - 1, j), rec(T, i - 1, j + 1)));\n}\n"
               "void resuelveCaso() {\n    int n0; cin >> n0; vector<vector<int>> T(n0, vector<int>(n0));\n"
               "    for (auto& f : T) for (int& x : f) cin >> x;\n    int best = -1, bc = 0;\n"
               "    for (int c = 0; c < n0; ++c) { int s = rec(T, n0 - 1, c); if (s > best) { best = s; bc = c; } }\n"
               "    cout << best << ' ' << bc + 1 << '\\n'; return;\n")], prueba=14, v="tle"),
]
