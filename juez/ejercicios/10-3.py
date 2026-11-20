"""10-3 · Esquivando las obras en los cruces: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «N M» (1..50) y N líneas de M caracteres ('.' libre, 'X' obras).
Las esquinas noroeste y sureste nunca tienen obras y la respuesta es siempre < 10⁹.
Salida: el número de caminos más cortos (solo sur y este) de la esquina noroeste a la sureste que
no pasan por obras.
El solucionador es propio: cuenta HACIA ATRÁS, los caminos desde cada cruce hasta la estación
(recorre la ciudad desde la esquina sureste), al revés que la solución del repo. Validado contra
fuerza bruta (todas las secuencias de S y E) en miles de ciudades pequeñas.
"""
import random
from itertools import combinations
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "10-Programacion dinamica/EJ_10-3/EJ_10-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["if (fila[j] == 'X') caminos[j] = 0;", "if (fila[j] == 'X') caminos[j] = 1;"],
}


def resuelve(c):
    """hasta[i][j] = caminos desde (i, j) hasta (N-1, M-1) yendo al sur o al este sin obras."""
    N, M = len(c), len(c[0])
    hasta = [[0] * (M + 1) for _ in range(N + 1)]
    for i in range(N - 1, -1, -1):
        for j in range(M - 1, -1, -1):
            if c[i][j] == "X":
                hasta[i][j] = 0
            elif i == N - 1 and j == M - 1:
                hasta[i][j] = 1
            else:
                hasta[i][j] = hasta[i + 1][j] + hasta[i][j + 1]
    return hasta[0][0]


def fuerza_bruta(c):
    N, M = len(c), len(c[0])
    total = 0
    for sur in combinations(range(N + M - 2), N - 1):
        i = j = 0
        ok = c[0][0] == "."
        s = set(sur)
        for k in range(N + M - 2):
            if k in s:
                i += 1
            else:
                j += 1
            ok = ok and c[i][j] == "."
        total += ok
    return total


def aleatorio(rng, N, M, p):
    c = [["X" if rng.random() < p else "." for _ in range(M)] for _ in range(N)]
    c[0][0] = c[N - 1][M - 1] = "."
    return ["".join(f) for f in c]


def caso_a_texto(c):
    return f"{len(c)} {len(c[0])}\n" + "\n".join(c) + "\n"


def pruebas():
    rng = random.Random(1003)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [[".....", ".X...", "..X.X", "....."]],
           "La ciudad de la figura: 4 caminos que esquivan las obras.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: a un cruce solo se llega desde el de arriba o el de la izquierda, y a un cruce con obras no se llega nunca."},
           ["Escribe en papel, sobre la cuadrícula, cuántos caminos llegan a cada cruce.",
            "caminos(i, j) = caminos(i−1, j) + caminos(i, j−1), y 0 si (i, j) tiene obras.",
            "El caso base es caminos(0, 0) = 1; fuera de la ciudad cuenta como 0."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [[".X...", "...X.", "XXX.."]],
           "El segundo ejemplo: se puede llegar dando un rodeo, pero no por un camino de longitud mínima (0).",
           {"wa": "Cuentas caminos que no son de longitud mínima (que suben o van hacia el oeste). Solo valen los que van al sur o al este."},
           ["Hay un camino de 8 manzanas, pero el mínimo es de 6: no cuenta.",
            "No hagas un recorrido en anchura por toda la ciudad: un camino mínimo solo avanza hacia el sur o hacia el este."])
    prueba("Ciudad de un solo cruce", "borde", [["."]],
           "N = M = 1: la estación está en el mismo cruce; hay 1 camino (quedarse).",
           {"wa": "Con un solo cruce hay exactamente un camino (el vacío): revisa el caso base.",
            "rte": "Con N = M = 1 accedes a una posición que no existe (j − 1 o i − 1)."},
           ["¿Qué escribes con «1 1» y «.»?",
            "El caso base caminos(0, 0) = 1 ya es la respuesta cuando N = M = 1."])
    prueba("Una sola calle", "borde", [["......"], [".", ".", ".", "."]],
           "Una sola fila y una sola columna, sin obras: 1 camino.",
           {"wa": "Con una sola fila o columna hay un único camino: revisa los bordes de la tabla.",
            "rte": "Te sales de la tabla con una sola fila o columna: comprueba i > 0 y j > 0 antes de mirar arriba o a la izquierda."},
           ["Prueba «1 6» con «......»: debe salir 1.",
            "Lo que está fuera de la ciudad cuenta 0 caminos: no lo leas del vector."])
    prueba("Ciudad no cuadrada", "trampa", [["......", "......"], ["..", "..", "..", "..", "..", "..", ".."]],
           "Ciudades sin obras de 2×6 y 7×2: N filas (calles este-oeste) de M caracteres.",
           {"wa": "Funciona con ciudades cuadradas pero no con rectangulares: ¿has cruzado N y M al leer o al recorrer?",
            "rte": "Con N ≠ M te sales del vector: N es el número de líneas y M el de caracteres de cada línea."},
           ["La primera línea da N (filas) y luego M (columnas).",
            "Repasa cada bucle: las filas van de 0 a N−1 y las columnas de 0 a M−1."])
    prueba("Una obra en medio", "trampa", [["...", ".X.", "..."]],
           "Una única obra en el centro de una ciudad 3×3: quedan 2 de los 6 caminos.",
           {"wa": "No anulas los cruces con obras: a un cruce con obras llegan 0 caminos aunque arriba y a la izquierda haya caminos."},
           ["Sin la obra habría 6 caminos; ¿cuántos pasan por el centro?",
            "Si usas un solo vector, en un cruce con obras hay que poner caminos[j] = 0 (no basta con no sumar: ahí queda el valor de la fila de arriba)."])
    prueba("Obra en la primera calle", "trampa", [["..X..", ".....", "....."]],
           "Una obra en la primera fila corta todos los cruces que quedan a su derecha en esa fila.",
           {"wa": "Inicializas toda la primera fila a 1 sin mirar las obras: los cruces a la derecha de una obra de la primera fila solo se alcanzan desde arriba... que no existe, así que valen 0."},
           ["¿Cuántos caminos llegan al cruce (0, 3)? Para llegar hay que pasar por (0, 2), que tiene obras.",
            "Trata la primera fila con la misma regla que las demás (arriba vale 0) en vez de ponerla entera a 1."])
    prueba("Obra en la primera columna", "trampa", [["...", "...", "X..", "...", "..."]],
           "Una obra en la primera columna corta todos los cruces que quedan debajo en esa columna.",
           {"wa": "Inicializas toda la primera columna a 1 sin mirar las obras: debajo de una obra de la primera columna no llega ningún camino."},
           ["¿Cuántos caminos llegan al cruce (3, 0)?",
            "La primera columna también sigue la regla general (a su izquierda hay 0 caminos)."])
    prueba("Ningún camino posible", "trampa", [["..X", ".X.", "X.."], ["....", "...X", "..X.", ".X..", "X..."]],
           "Una barrera diagonal de obras: la respuesta es 0.",
           {"wa": "Cuando ningún camino llega, la respuesta es 0: ¿escribes otra cosa o cuentas caminos que atraviesan obras?"},
           ["Dibuja la ciudad: la diagonal de obras separa la salida de la estación.",
            "Si la tabla está bien, la casilla final vale 0 sin tratar este caso aparte."])
    prueba("El rodeo no cuenta", "trampa", [["...", "XX.", "...", ".XX", "..."]],
           "Solo se llega a la estación yendo un tramo hacia el oeste: no hay ningún camino mínimo (0).",
           {"wa": "Estás contando caminos que no son de longitud mínima (con BFS o moviéndote en las 4 direcciones). Solo valen sur y este."},
           ["Los caminos más cortos tienen exactamente (N−1) + (M−1) manzanas.",
            "A un cruce solo se puede llegar desde el de arriba o el de la izquierda."])
    prueba("Respuesta grande (cerca de 10⁹)", "trampa", [["." * 17] * 17, ["." * 34, "." * 34, "." * 34] + ["X" + "." * 33]],
           "Ciudades sin apenas obras con cientos de millones de caminos.",
           {"wa": "Con respuestas grandes algo desborda: ¿usas short o sumas en un tipo pequeño? El resultado cabe en int.",
            "tle": "Cuentas los caminos uno a uno (recursión sin memoria): con cientos de millones no acaba. Guarda en una tabla los caminos de cada cruce."},
           ["Una ciudad 17×17 sin obras tiene C(32, 16) = 601.080.390 caminos.",
            "Cada cruce se calcula una vez sumando dos casillas: no recorras los caminos."])
    prueba("Varios casos seguidos", "trampa",
           [["......", "......", "......", "......"], ["...", "X..", "..."], [".X", ".."], ["."]],
           "Una ciudad grande y luego otras más pequeñas: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: la tabla (o el vector) de caminos debe crearse a ceros en cada caso.",
            "rte": "Una tabla de un caso anterior con otro tamaño: créala dentro de la función de cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara la tabla dentro de la función de cada caso, inicializada a 0."])
    peq = [aleatorio(rng, rng.randint(1, 7), rng.randint(1, 7), rng.choice([.1, .25, .4])) for _ in range(80)]
    prueba("Aleatorias pequeñas", "aleatorio", peq,
           "80 ciudades pequeñas al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibújalo y cuenta a mano."},
           ["Busca en la entrada la ciudad de la línea que falla.",
            "Revisa obras en la primera fila o columna y ciudades de una sola calle."])
    grandes = []
    while len(grandes) < 30:
        c = aleatorio(rng, rng.randint(30, 50), rng.randint(30, 50), rng.choice([.25, .3, .35]))
        if resuelve(c) < 10 ** 9:
            grandes.append(c)
    prueba("Aleatorias grandes", "aleatorio", grandes,
           "30 ciudades de hasta 50×50 con bastantes obras.",
           {"wa": "Falla en ciudades grandes: revisa los bordes y que se lean todas las líneas.",
            "tle": "Cuentas los caminos uno a uno: en una ciudad de 50×50 hay demasiados. Usa una tabla."},
           ["¿Calculas los caminos de un mismo cruce varias veces? Apúntalos en una tabla.",
            "Rellena la tabla por filas: cada cruce suma el de arriba y el de la izquierda."])
    abierta = ["." * 50] * 48 + ["." * 49 + "X" if False else "." * 49 + ".", "." * 50]
    sin_final = ["." * 50] * 48 + ["." * 49 + "X", "." * 48 + "X."]
    sin_salida = [".X" + "." * 48, "X" + "." * 49] + ["." * 50] * 48
    prueba("Ciudades 50×50 con millones de callejones", "rendimiento", [sin_final, sin_salida] * 50,
           "100 ciudades de 50×50 sin obras salvo junto a la estación (o a la salida): 0 caminos, pero muchísimos caminos a medias.",
           {"tle": "Exploras los caminos uno a uno (recursión sin memoria o backtracking): con 50×50 hay del orden de 10²⁸. La tabla hace que cada cruce cueste O(1).",
            "wa": "Cuando las obras rodean la estación (o la salida) la respuesta es 0."},
           ["Una recursión que prueba sur y este en cada cruce tarda 2^(N+M): imposible aquí.",
            "Guarda cuántos caminos llegan a cada cruce y reutilízalo (programación dinámica): O(N·M) por ciudad."])
    del abierta
    for c in (c for x in P for c in x[2]):
        assert 1 <= len(c) <= 50 and all(len(f) == len(c[0]) and set(f) <= {".", "X"} for f in c) and 1 <= len(c[0]) <= 50
        assert c[0][0] == "." and c[-1][-1] == "." and resuelve(c) < 10 ** 9
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d\n" % resuelve(c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("no anula los cruces con obras", [("if (fila[j] == 'X') caminos[j] = 0;\n            else if (j > 0)", "if (fila[j] != 'X' && j > 0)")], prueba=6, v="wa"),
    Variante("primera fila entera a 1", [("if (fila[j] == 'X') caminos[j] = 0;", "if (fila[j] == 'X' && i > 0) caminos[j] = 0;\n            else if (i == 0) caminos[j] = 1;")], prueba=7, v="wa"),
    Variante("primera columna entera a 1", [("if (fila[j] == 'X') caminos[j] = 0;", "if (fila[j] == 'X' && j > 0) caminos[j] = 0;")], prueba=8, v="wa"),
    Variante("cruza N y M", [("cin >> N >> M;", "cin >> M >> N;")], prueba=5, v="rte"),
    Variante("cuenta en short", [("vector<long long> caminos(M, 0);", "vector<short> caminos(M, 0);")], prueba=11, v="wa"),
    Variante("no reinicia la tabla entre casos", [("vector<long long> caminos(M, 0);", "static vector<long long> caminos(50, 0);")], prueba=12, v="wa"),
    Variante("rodeos: BFS en 4 direcciones (cuenta caminos mínimos del grafo)",
             [("void resuelveCaso() {",
               "void resuelveCaso() {\n    int n0, m0; cin >> n0 >> m0; vector<string> g(n0); for (auto& f : g) cin >> f;\n"
               "    vector<vector<int>> d(n0, vector<int>(m0, -1)); vector<vector<long long>> w(n0, vector<long long>(m0, 0));\n"
               "    vector<pair<int,int>> q{{0, 0}}; d[0][0] = 0; w[0][0] = 1;\n"
               "    for (size_t h = 0; h < q.size(); ++h) { auto [a, b] = q[h]; int da[] = {1, -1, 0, 0}, db[] = {0, 0, 1, -1};\n"
               "        for (int k = 0; k < 4; ++k) { int x = a + da[k], y = b + db[k]; if (x < 0 || y < 0 || x >= n0 || y >= m0 || g[x][y] == 'X') continue;\n"
               "            if (d[x][y] < 0) { d[x][y] = d[a][b] + 1; q.push_back({x, y}); } if (d[x][y] == d[a][b] + 1) w[x][y] += w[a][b]; } }\n"
               "    cout << w[n0 - 1][m0 - 1] << '\\n'; return;\n")], prueba=[2, 10], v="wa"),
    Variante("recursión sin memoria",
             [("void resuelveCaso() {",
               "long long rec(const vector<string>& g, int i, int j) {\n    if (i >= (int)g.size() || j >= (int)g[0].size() || g[i][j] == 'X') return 0;\n"
               "    if (i == (int)g.size() - 1 && j == (int)g[0].size() - 1) return 1;\n    return rec(g, i + 1, j) + rec(g, i, j + 1);\n}\n"
               "void resuelveCaso() {\n    int n0, m0; cin >> n0 >> m0; vector<string> g(n0); for (auto& f : g) cin >> f;\n"
               "    cout << rec(g, 0, 0) << '\\n'; return;\n")], prueba=11, v="tle"),
]
