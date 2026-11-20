"""06-1 · Petroleros hundidos: juez con pruebas pensadas para cada error típico.

Cada caso: rejilla F × C ('-' mar, '#' petróleo), N celdas nuevas (fila, columna desde 1).
Salida: tamaño de la mayor mancha (8 direcciones) al principio y tras cada celda nueva.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "6-Conjuntos disjuntos y grafos valorados/EJ_06-1/EJ_06-1.cpp",
    "cabeceras": ["6-Conjuntos disjuntos y grafos valorados/EJ_06-1/ConjuntosDisjuntos.h"],
    "limite_ms": 3000,
    "fallo": ["if (di == 0 && dj == 0) continue;", "if (di == dj || di == -dj) continue;"],
}

VECINOS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def resuelve(F, C, filas, nuevas):
    """Solucionador independiente: unión-búsqueda con tamaños y división de caminos."""
    padre = list(range(F * C))
    tam = [1] * (F * C)
    negro = bytearray(F * C)

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    def une(x, y):
        x, y = raiz(x), raiz(y)
        if x == y:
            return tam[x]
        if tam[x] < tam[y]:
            x, y = y, x
        padre[y] = x
        tam[x] += tam[y]
        return tam[x]

    mayor = 0
    for i in range(F):
        fila = filas[i]
        for j in range(C):
            if fila[j] == "#":
                v = i * C + j
                negro[v] = 1
                t = 1
                # basta con las vecinas ya vistas (arriba y a la izquierda): la unión es simétrica
                for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, -1)):
                    a, b = i + di, j + dj
                    if 0 <= a < F and 0 <= b < C and negro[a * C + b]:
                        t = une(v, a * C + b)
                if t > mayor:
                    mayor = t
    res = [mayor]
    for f, c in nuevas:
        i, j = f - 1, c - 1
        v = i * C + j
        assert not negro[v]
        negro[v] = 1
        t = 1
        for di, dj in VECINOS:
            a, b = i + di, j + dj
            if 0 <= a < F and 0 <= b < C and negro[a * C + b]:
                t = une(v, a * C + b)
        if t > mayor:
            mayor = t
        res.append(mayor)
    return " ".join(map(str, res)) + "\n"


def caso_a_texto(filas, nuevas):
    F, C = len(filas), len(filas[0])
    return (f"{F} {C}\n" + "\n".join(filas) + f"\n{len(nuevas)}\n"
            + "".join(f"{f} {c}\n" for f, c in nuevas))


def aleatorio(rng, F, C, p, n):
    filas = ["".join("#" if rng.random() < p else "-" for _ in range(C)) for _ in range(F)]
    mar = [(i + 1, j + 1) for i in range(F) for j in range(C) if filas[i][j] == "-"]
    rng.shuffle(mar)
    return filas, mar[:min(n, len(mar))]


def grande(rng):
    """800 × 800 con un 35 % de petróleo y 100.000 celdas nuevas en el mar."""
    F = C = 800
    filas = []
    for _ in range(F):
        filas.append("".join("#" if x < 0.35 else "-" for x in (rng.random() for _ in range(C))))
    elegidas, vistas = [], set()
    while len(elegidas) < 100000:
        i, j = rng.randrange(F), rng.randrange(C)
        if filas[i][j] == "-" and (i, j) not in vistas:
            vistas.add((i, j))
            elegidas.append((i + 1, j + 1))
    return filas, elegidas


def pruebas():
    rng = random.Random(61)
    ej1 = (["-#-#---#", "-###--##", "-----###", "-#------", "-#-#----", "-###-##-", "###--##-", "--#-----"],
           [(6, 8), (2, 5), (6, 5)])
    ej2 = (["----", "----", "----"], [(2, 2), (3, 4), (2, 3)])
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ej1],
           "El primer ejemplo del PDF: la rejilla del dibujo y tres celdas nuevas («10 10 12 16»).",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura, las 8 direcciones o cómo se actualiza el máximo.",
            "pe": "Los números están bien pero el formato no: van todos en UNA línea por caso, separados por un espacio."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara número a número.",
            "La primera cifra es la mancha mayor de la rejilla inicial, ANTES de añadir ninguna celda.",
            "Usa la plantilla de número de casos y, por cada caso, una sola línea con N + 1 números."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ej2],
           "El segundo ejemplo: rejilla sin petróleo y tres celdas nuevas, la última une dos manchas en diagonal («0 1 1 3»).",
           {"wa": "Mira qué número no coincide: si es el primero, no tratas bien la rejilla vacía (debe ser 0); si es el último, la diagonal no une."},
           ["Sin ninguna celda negra la mayor mancha mide 0.",
            "La celda (2, 3) toca a la (2, 2) en horizontal y a la (3, 4) en diagonal: las tres forman una mancha."])
    prueba("Rejilla de 1 × 1", "borde", [(["-"], []), (["#"], []), (["-"], [(1, 1)])],
           "La rejilla más pequeña: solo mar («0»), solo petróleo («1») y mar que se contamina («0 1»).",
           {"wa": "Con una sola celda la respuesta es evidente: revisa cómo inicializas el máximo y si escribes el valor inicial.",
            "rte": "Con una rejilla de 1 × 1 cualquier vecina está fuera: comprueba los límites ANTES de mirar la celda vecina."},
           ["¿Qué escribe tu programa con una rejilla «-» y N = 0? Debe ser solo «0».",
            "Antes de mirar una vecina (i + di, j + dj), comprueba 0 ≤ i + di < F y 0 ≤ j + dj < C."])
    prueba("Sin celdas nuevas (N = 0)", "borde",
           [(["##-", "--#", "#--"], []), (["#-#-#"], [])],
           "Si no hay imágenes adicionales, la línea tiene un único número: la mayor mancha inicial.",
           {"wa": "Con N = 0 hay que escribir solo el tamaño inicial. Revisa que no te saltas el primer número ni lees de más.",
            "pe": "Con N = 0 la línea es un solo número, sin nada más (ni líneas vacías entre casos)."},
           ["La salida de cada caso tiene N + 1 números: con N = 0, uno.",
            "Escribe el máximo inicial antes del bucle de las celdas nuevas, y el salto de línea después del bucle."])
    # --- Trampas de la rejilla inicial (sin celdas nuevas). El orden importa: las primeras
    #     no deben fallar por los errores que buscan las siguientes.
    prueba("Unir solo con vecinas que sean petróleo", "trampa",
           [(["##-"], []), (["-##-", "----"], []), (["-#-", "---"], [])],
           "Una celda de mar al lado NO forma parte de la mancha.",
           {"wa": "Unes la celda con sus vecinas aunque sean mar: el cardinal cuenta celdas azules. Comprueba que la vecina es petróleo antes de unir."},
           ["Con «##-» la mayor mancha mide 2, no 3.",
            "Antes de unir con una vecina, mira si ya está marcada como petróleo."])
    prueba("Manchas de una sola celda", "trampa",
           [(["#-"], []), (["#-#", "---", "#-#"], [])],
           "Si todas las manchas son de una celda, la respuesta es 1 aunque no se haya unido nada.",
           {"wa": "Solo actualizas el máximo cuando una celda se une con alguna vecina. Una celda sola ya es una mancha de tamaño 1: compara el máximo con su cardinal siempre."},
           ["Con «#-» la salida es «1», no «0».",
            "Actualiza el máximo después del bucle de las vecinas, no dentro del «if» que une."])
    prueba("La misma mancha tocada por varios lados", "trampa",
           [(["##", "##"], []), (["###", "#-#", "###"], [(2, 2)])],
           "Una celda cuyas vecinas son todas de la misma mancha: esa mancha no se cuenta varias veces.",
           {"wa": "Sumas a mano los tamaños de las manchas vecinas y cuentas la misma mancha varias veces. Con conjuntos disjuntos basta unir y preguntar cardinal."},
           ["Un bloque 2 × 2 de petróleo es una mancha de 4.",
            "En el segundo caso, la celda (2, 2) tiene 8 vecinas de la misma mancha de 8: el resultado es «8 9», no 1 + 8·8.",
            "Si quieres sumar a mano, quédate solo con los representantes distintos; es más fácil unir y luego preguntar cardinal(celda)."])
    prueba("Las diagonales también unen", "trampa",
           [(["-#", "#-"], []), (["#-", "-#"], []), (["#-#", "-#-", "#-#"], [])],
           "Celdas que solo se tocan por una esquina son de la MISMA mancha (8 direcciones).",
           {"wa": "Solo unes en 4 direcciones (o te falta alguna diagonal). El enunciado dice 8: horizontal, vertical y las dos diagonales."},
           ["En «-#» / «#-» hay una sola mancha de tamaño 2.",
            "Fíjate también en la diagonal «hacia arriba a la derecha»: si solo miras las vecinas ya vistas, son cuatro (arriba-izquierda, arriba, arriba-derecha e izquierda).",
            "Recorre di y dj de −1 a 1 (salvo los dos a 0) para tener las 8 vecinas."])
    prueba("El máximo nunca baja", "trampa",
           [(["###", "---", "--#"], []), (["#-#", "#-#", "#--"], [(3, 3), (1, 2)])],
           "La mancha más grande no tiene por qué ser la de la última celda que se mira.",
           {"wa": "Escribes el tamaño de la mancha de la última celda en vez del de la MAYOR. El máximo es max(máximo, tamaño de la mancha de la celda)."},
           ["En el primer caso la mancha de arriba mide 3; la celda (3, 3) forma otra de 1 y la respuesta es 3.",
            "No sustituyas el máximo: quédate con el mayor de los dos."])
    prueba("Rejilla no cuadrada", "trampa",
           [(["#-", "--", "-#"], []), (["#", "#", "-", "#", "#"], [(3, 1)]), (["#-#-#", "-----", "-----"], [(2, 2), (2, 4)])],
           "Rejillas de 3 × 2, 5 × 1 y 3 × 5: si cruzas F y C al numerar las celdas se nota aquí.",
           {"rte": "Con F ≠ C te sales del vector: el número de la celda (i, j) es i·C + j (C = columnas), no i·F + j.",
            "wa": "Funciona con cuadradas pero no con rectangulares: casi seguro numeras con i·F + j en vez de i·C + j, o has cruzado F y C al leer."},
           ["La entrada da primero las FILAS y luego las COLUMNAS.",
            "Busca cada «F» y cada «C» de tu código y comprueba que no están cambiadas (por ejemplo i*F + j)."])
    prueba("Fin de una fila y principio de la siguiente", "trampa",
           [(["--#", "#--"], []), (["#--", "--#"], []), (["---", "---", "---"], [(1, 3), (2, 1)]), (["---", "---", "---"], [(2, 1), (1, 3)])],
           "La última celda de una fila y la primera de la siguiente NO son vecinas, aunque i·C + j dé números seguidos.",
           {"wa": "Te falta comprobar la COLUMNA de la vecina: con j = C − 1, la vecina «j + 1» cae al principio de la fila siguiente (y con j = 0, «j − 1» al final de la anterior).",
            "rte": "Te sales de la rejilla al mirar una vecina: comprueba 0 ≤ j + dj < C además de la fila."},
           ["En «--#» / «#--» hay dos manchas de una celda: la respuesta es 1.",
            "Comprobar solo que el número i·C + j está entre 0 y F·C − 1 no basta.",
            "Comprueba fila y columna por separado: 0 ≤ a < F y 0 ≤ b < C."])
    # --- Trampas de las celdas nuevas
    prueba("Las celdas nuevas se numeran desde 1", "trampa",
           [(["--", "--"], [(2, 2)]), (["---"], [(1, 3), (1, 2)]), (["--", "--"], [(1, 1)])],
           "Celdas nuevas en la última fila y la última columna: hay que restar 1 a la fila y a la columna.",
           {"rte": "Usas la fila y la columna tal cual: la celda (F, C) se sale de la rejilla. Resta 1 a las dos.",
            "wa": "La celda nueva cae en otro sitio: resta 1 a la fila y a la columna (la entrada cuenta desde 1)."},
           ["La celda (2, 2) de una rejilla 2 × 2 es la de abajo a la derecha: en base 0, (1, 1).",
            "Haz «f − 1» y «c − 1» justo al leerlas."])
    prueba("Primero la fila, luego la columna", "trampa",
           [(["##-", "---", "---"], [(1, 3)]), (["#---", "----"], [(1, 2), (2, 4)])],
           "Cada celda nueva viene como «fila columna» (no «x y»).",
           {"wa": "Has cruzado la fila y la columna de la celda nueva: la celda (1, 3) está en la PRIMERA fila, tercera columna.",
            "rte": "Has cruzado fila y columna de la celda nueva y en una rejilla rectangular se sale."},
           ["En el primer caso, (1, 3) está pegada a la mancha «##» de la fila 1: el resultado es «2 3».",
            "Lee «f c» y usa f como fila (i) y c como columna (j)."])
    prueba("La celda nueva se une con vecinas de abajo y de la derecha", "trampa",
           [(["--", "-#"], [(1, 1)]), (["---", "---", "#-#"], [(2, 2)]), (["--", "#-"], [(1, 2)])],
           "Una celda nueva tiene que mirar sus 8 vecinas, también las de filas posteriores.",
           {"wa": "Para la rejilla inicial basta mirar las vecinas ya vistas (arriba e izquierda), pero una celda NUEVA puede tocar petróleo por abajo o por la derecha: mira las 8."},
           ["En el primer caso, la celda (1, 1) toca en diagonal a la (2, 2): la salida es «1 2».",
            "Si reutilizas la función de la rejilla inicial, haz que recorra di y dj de −1 a 1."])
    prueba("Celdas nuevas que se tocan entre sí", "trampa",
           [(["----"], [(1, 1), (1, 2), (1, 3), (1, 4)]), (["---", "---", "---"], [(1, 1), (2, 2), (3, 3)])],
           "Una celda nueva tiene que quedar marcada como petróleo para que las siguientes se unan a ella.",
           {"wa": "Las celdas nuevas no se marcan como petróleo (solo las de la rejilla inicial): la siguiente celda nueva no se une con ellas."},
           ["La salida del primer caso es «0 1 2 3 4».",
            "Marca la celda como petróleo al añadirla, igual que las de la rejilla inicial."])
    prueba("Celda nueva aislada", "trampa",
           [(["---", "---"], [(1, 1)]), (["##--", "----", "---#"], [(2, 4), (1, 4)])],
           "Una celda nueva que no toca a nadie es una mancha de tamaño 1 y también cuenta para el máximo.",
           {"wa": "Solo actualizas el máximo cuando la celda nueva se une con alguna vecina. Hay que compararlo siempre con el tamaño de su mancha."},
           ["Con la rejilla vacía y la celda (1, 1) la salida es «0 1».",
            "Actualiza el máximo después del bucle de las vecinas, no dentro."])
    prueba("La celda nueva funde dos manchas", "trampa",
           [(["#-#"], [(1, 2)]), (["##--", "----", "--##"], [(2, 2)]), (["#---#", "-----", "#---#"], [(2, 2), (2, 4), (2, 3)])],
           "Una celda nueva que une dos manchas: el tamaño es la suma de las dos más ella.",
           {"wa": "El tamaño se mira ANTES de unir, o no se unen las dos manchas. Primero une con todas las vecinas y después pregunta el cardinal."},
           ["En «#-#» con la celda (1, 2) la salida es «1 3».",
            "El orden importa: une con las 8 vecinas y solo al final consulta cardinal(celda)."])
    prueba("Celdas nuevas en las cuatro esquinas", "borde",
           [(["----", "-##-", "----"], [(1, 1), (1, 4), (3, 1), (3, 4)]), (["-#-", "---"], [(2, 3), (2, 1), (1, 1)])],
           "Celdas en las esquinas: algunas vecinas quedan fuera de la rejilla.",
           {"rte": "Te sales de la rejilla al mirar las vecinas de una esquina: comprueba los límites de fila Y de columna.",
            "wa": "En las esquinas algo falla: revisa los límites (< F y < C, no ≤)."},
           ["Prueba a mano la celda (1, 1): solo tiene 3 vecinas dentro.",
            "Comprueba 0 ≤ a < F y 0 ≤ b < C antes de acceder a la vecina."])
    prueba("Una sola fila y una sola columna", "borde",
           [(["#-##-#"], [(1, 2), (1, 5)]), (["#", "-", "#", "#"], [(2, 1)])],
           "Rejillas de 1 × C y F × 1.",
           {"wa": "Con una sola fila o columna fallan los índices: revisa cómo pasas de (i, j) a número de celda.",
            "rte": "Te sales de la rejilla al mirar vecinas en una fila o columna única."},
           ["En «#-##-#» la mayor mancha inicial mide 2; al añadir (1, 2) mide 4 y al añadir (1, 5), 6.",
            "La celda (i, j) es la número i·C + j."])
    prueba("Toda la rejilla es petróleo", "borde",
           [(["####", "####", "####"], []), (["#####"] * 6, [])],
           "Una sola mancha que ocupa toda la rejilla: F·C.",
           {"wa": "Si sale menos de F·C, alguna celda no se une a la mancha: revisa las vecinas y los límites."},
           ["Con 3 × 4 todo «#» la respuesta es 12.",
            "Cada celda se une con las vecinas ya vistas: todas acaban en el mismo conjunto."])
    prueba("Varios casos seguidos", "trampa",
           [(["####", "####", "####"], []), (["#-", "--"], [(2, 2)]), (["-"], []), (["--", "--"], [(1, 1), (2, 1)])],
           "Un caso con una mancha grande seguido de otros pequeños: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el máximo, la rejilla o la partición se crean fuera de resuelveCaso.",
            "rte": "Un vector de un caso anterior con otro tamaño: crea la rejilla y los conjuntos disjuntos dentro de cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "El máximo debe empezar en 0 en cada caso."])
    casos_al = []
    for _ in range(60):
        F, C = rng.randint(1, 7), rng.randint(1, 7)
        casos_al.append(aleatorio(rng, F, C, rng.choice([0.2, 0.4, 0.6]), rng.randint(0, 12)))
    prueba("Aleatorios pequeños", "aleatorio", casos_al,
           "60 rejillas pequeñas al azar con celdas nuevas.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; busca esa rejilla y síguela a mano."},
           ["La línea que falla es el número de caso: busca esa rejilla en la entrada.",
            "Dibuja la rejilla en papel y añade las celdas nuevas una a una."])
    pequenos = [aleatorio(rng, 3, 3, 0.4, 2) for _ in range(20000)]
    prueba("Muchos casos pequeños", "rendimiento", pequenos,
           "20.000 rejillas de 3 × 3: el trabajo de cada caso debe depender de su tamaño, no del máximo posible.",
           {"tle": "Reservas (o limpias) la rejilla o la partición con el tamaño máximo (1000 × 1000) en cada caso. Créalas con F·C elementos.",
            "mle": "Reservas memoria del tamaño máximo en cada caso y no la liberas."},
           ["¿Cuánto cuesta preparar un caso de 3 × 3 en tu programa? Debería ser unas 9 operaciones, no 10⁶.",
            "Crea ConjuntosDisjuntos(F * C) y el vector de la rejilla con F·C elementos dentro de cada caso."])
    prueba("Rejilla 800 × 800 con 100.000 celdas nuevas", "rendimiento", [grande(rng)],
           "Una rejilla grande y el máximo de celdas nuevas: cada celda nueva debe costar unas pocas operaciones.",
           {"tle": "Recalculas algo de toda la rejilla tras cada celda nueva (un DFS/BFS completo o recorrer todos los conjuntos para buscar el máximo). Con conjuntos disjuntos cada celda nueva solo mira sus 8 vecinas.",
            "mle": "Gastas demasiada memoria: con 10⁶ celdas no construyas listas de adyacencia ni copies la rejilla.",
            "rte": "Con 10⁶ celdas se rompe: revisa los tamaños de los vectores y no uses recursión muy profunda."},
           ["Como las manchas solo crecen, la única que cambia es la de la celda nueva.",
            "El máximo se actualiza con max(máximo, cardinal(celda)): no hace falta recorrer todas las manchas.",
            "Pon ios::sync_with_stdio(false) y cin.tie(nullptr) para leer rápido."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(f, n) for f, n in casos),
                   salida="".join(resuelve(len(f), len(f[0]), f, n) for f, n in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("une con celdas de mar", [("if (petroleo[a * C + b]) cd.unir(celda, a * C + b);", "cd.unir(celda, a * C + b);")], prueba=5, v="wa"),
    Variante("máximo solo al unir", [("if (petroleo[a * C + b]) cd.unir(celda, a * C + b);",
                                      "if (petroleo[a * C + b]) { cd.unir(celda, a * C + b); mayor = max(mayor, cd.cardinal(celda)); }"),
                                     ("        mayor = max(mayor, cd.cardinal(celda));\n    }", "    }")], prueba=6, v="wa"),
    Variante("suma tamaños sin quitar repetidos", [("if (petroleo[a * C + b]) cd.unir(celda, a * C + b);\n            }\n        mayor = max(mayor, cd.cardinal(celda));",
                                                    "if (petroleo[a * C + b]) { suma += cd.cardinal(a * C + b); cd.unir(celda, a * C + b); }\n            }\n        mayor = max(mayor, suma);"),
                                                   ("petroleo[celda] = true;\n", "petroleo[celda] = true;\n        int suma = 1;\n")], prueba=7, v="wa"),
    Variante("solo 4 direcciones", [("if (di == 0 && dj == 0) continue;", "if (di == dj || di == -dj) continue;")], prueba=8, v="wa"),
    Variante("máximo = mancha de la última celda", [("mayor = max(mayor, cd.cardinal(celda));", "mayor = cd.cardinal(celda);")], prueba=9, v="wa"),
    Variante("numera con i·F + j", [(" * C + ", " * F + ")], prueba=10, v="rte"),
    Variante("no comprueba la columna de la vecina", [("if (a < 0 || a >= F || b < 0 || b >= C) continue;",
                                                     "if (a * C + b < 0 || a * C + b >= F * C) continue;")], prueba=11, v="wa"),
    Variante("no resta 1 a las celdas nuevas", [("m.anade(f - 1, c - 1);", "m.anade(f, c);")], prueba=12, v="rte"),
    Variante("celdas nuevas: solo vecinas ya vistas", [("for (int di = -1; di <= 1; ++di)", "for (int di = -1; di <= 0; ++di)"),
                                                       ("for (int dj = -1; dj <= 1; ++dj) {", "for (int dj = -1; dj <= (di < 0 ? 1 : -1); ++dj) {")], prueba=14, v="wa"),
    Variante("no marca las celdas nuevas", [("void anade(int i, int j) {\n        int celda = i * C + j;\n        petroleo[celda] = true;",
                                             "void anade(int i, int j, bool inicial = false) {\n        int celda = i * C + j;\n        if (inicial) petroleo[celda] = true;"),
                                            ("if (fila[j] == '#') m.anade(i, j);", "if (fila[j] == '#') m.anade(i, j, true);")], prueba=15, v="wa"),
    Variante("máximo global sin reiniciar", [(", cd(filas * columnas), mayor(0) {}", ", cd(filas * columnas) {}"),
                                             ("    int mayor;\n};", "    static int mayor;\n};\nint Manchas::mayor = 0;")], prueba=21, v="wa"),
    Variante("recorre todas las celdas para el máximo", [("int masGrande() const { return mayor; }",
                                                          "int masGrande() const { int r = 0; for (int x = 0; x < F * C; ++x) if (petroleo[x]) r = max(r, cd.cardinal(x)); return r; }")], prueba=24, v="tle"),
]
