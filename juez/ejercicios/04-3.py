"""04-3 · Detección de manchas negras: juez con pruebas pensadas para cada error típico."""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "4-Grafos no dirigidos/EJ_04-3/EJ_04-3.cpp",
    "cabeceras": ["4-Grafos no dirigidos/EJ_04-3/Grafo.h"],
    "limite_ms": 3000,
    "fallo": ["m.numero() << ' ' << m.mayor()", "m.mayor() << ' ' << m.numero()"],
}


def manchas(F, C, filas):
    visto = [[False] * C for _ in range(F)]
    n = mayor = 0
    for i in range(F):
        for j in range(C):
            if filas[i][j] == "#" and not visto[i][j]:
                n += 1
                tam = 0
                cola = deque([(i, j)])
                visto[i][j] = True
                while cola:
                    a, b = cola.popleft()
                    tam += 1
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        x, y = a + da, b + db
                        if 0 <= x < F and 0 <= y < C and filas[x][y] == "#" and not visto[x][y]:
                            visto[x][y] = True
                            cola.append((x, y))
                mayor = max(mayor, tam)
    return n, mayor


def aleatorio(rng, F, C, p):
    return ["".join("#" if rng.random() < p else "-" for _ in range(C)) for _ in range(F)]


def caso_a_texto(filas):
    return f"{len(filas)} {len(filas[0])}\n" + "\n".join(filas) + "\n"


def serpiente(F, C):
    """Una sola mancha muy larga en zigzag: filas pares llenas, enlazadas por un extremo."""
    filas = []
    for i in range(F):
        if i % 2 == 0:
            filas.append("#" * C)
        else:
            filas.append(("-" * (C - 1) + "#") if i % 4 == 1 else ("#" + "-" * (C - 1)))
    return filas


def pruebas():
    """Cada prueba busca UN error típico. Campos: nombre, comprueba (qué mira), tipo
    (enunciado | borde | trampa | aleatorio | rendimiento), si (qué suele significar fallarla,
    por veredicto) y pistas (de menos a más)."""
    rng = random.Random(43)
    ejemplo1 = ["-#-#---#", "-###---#", "----####", "-#------", "-#-#----", "-###-##-", "###--##-", "--#-----"]
    ejemplo2 = ["#-#-#-###-", "#-#-#-#-#-", "#-#-#-#-#-", "#-#-#-#-#-"]
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [ejemplo1],
           "El primer ejemplo del PDF: dos manchas que se tocan solo por una esquina.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: lectura de la entrada, formato de la salida o la idea del recorrido."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "Comprueba que escribes «número de manchas, espacio, tamaño de la mayor» y un salto de línea por caso.",
            "Recuerda que la entrada empieza con el número de casos: usa la plantilla de número de casos."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [ejemplo2],
           "El segundo ejemplo: columnas que solo se unen por arriba.",
           {"wa": "Las manchas de este ejemplo solo se unen por la primera fila: si sale de más, tu recorrido no sigue la mancha por todas las direcciones."},
           ["La mancha grande (9 píxeles) baja por dos columnas unidas solo por arriba.",
            "Desde cada píxel hay que poder ir hacia arriba, abajo, izquierda y derecha (en el grafo, las aristas son no dirigidas)."])
    prueba("Sin ningún píxel negro", "borde", [["-"], ["---", "---"]],
           "Un bitmap todo blanco: debe salir «0 0».",
           {"wa": "Con cero manchas el tamaño de la mayor debe ser 0. Suele fallar por inicializar el máximo a otra cosa o por dividir el caso «sin manchas»."},
           ["¿Qué escribe tu programa si no hay ningún «#»?",
            "Inicializa el contador de manchas y el tamaño máximo a 0 en cada caso."])
    prueba("Un único píxel", "borde", [["#"], ["-#-"], ["-", "#", "-"]],
           "Bitmaps mínimos con un solo píxel negro: «1 1».",
           {"rte": "Con una sola fila o columna, mirar el vecino de abajo o de la derecha se sale del bitmap si no compruebas los bordes."},
           ["Antes de mirar un vecino, comprueba que está dentro: 0 ≤ i < F y 0 ≤ j < C."])
    prueba("Todo negro", "borde", [["#" * 7], ["####", "####", "####"]],
           "Todo el bitmap es una sola mancha: «1 F·C».",
           {"wa": "Si cuentas más de una mancha, no se marcan bien los visitados o no se recorren todos los vecinos."},
           ["Un solo DFS desde el primer píxel tiene que llegar a todos.",
            "Marca un píxel como visitado al entrar en él, no al salir."])
    prueba("Las diagonales no unen", "trampa", [["#-", "-#"], ["#-#", "-#-", "#-#"]],
           "Píxeles que solo se tocan en diagonal son manchas distintas.",
           {"wa": "Estás uniendo píxeles en diagonal. Solo cuentan los 4 vecinos: arriba, abajo, izquierda y derecha."},
           ["En «#-» / «-#» hay dos manchas, no una.",
            "Quita los vecinos diagonales (i±1, j±1) del recorrido."])
    prueba("Una sola fila y una sola columna", "borde", [["#-##-###"], ["#", "#", "-", "#"]],
           "Bitmaps de 1×C y F×1.",
           {"wa": "Con una sola fila o columna fallan los índices: revisa cómo pasas de (i, j) a número de vértice.",
            "rte": "Te sales del bitmap al mirar vecinos en una fila o columna única."},
           ["Prueba a mano 1 8 y «#-##-###»: deben salir 3 manchas, la mayor de 3.",
            "El vértice del píxel (i, j) es i·C + j (C = columnas), no i·F + j."])
    prueba("Bitmap no cuadrado", "trampa", [["#--#---", "#--#---", "-------"], ["#--", "#--", "---", "-##", "---", "--#", "--#"]],
           "Filas y columnas distintas (3×7 y 7×3).",
           {"wa": "Funciona con cuadrados pero no con rectángulos: casi seguro has cruzado F y C en algún sitio (al numerar i·C + j o al leer).",
            "rte": "Con F ≠ C te sales del vector: revisa que usas C para numerar y F para el número de filas."},
           ["La entrada da primero las FILAS y luego las COLUMNAS.",
            "Busca en tu código cada «F» y «C» y comprueba que no están cambiadas (por ejemplo i*F+j)."])
    prueba("Final de una fila y principio de la siguiente", "trampa", [["---#", "#---"], ["--#", "#-#", "#--"]],
           "El último píxel de una fila y el primero de la siguiente NO son vecinos aunque sus números sean seguidos.",
           {"wa": "Unes v con v+1 sin comprobar que v no es el último de su fila: con la numeración i·C + j, el píxel (i, C-1) más uno es (i+1, 0)."},
           ["En «---#» / «#---» hay 2 manchas de 1 píxel.",
            "Para unir con el de la derecha, comprueba j + 1 < C antes de usar v + 1."])
    prueba("Manchas en la última fila y columna", "borde", [["----", "---#", "--##"], ["#--", "#--", "###"]],
           "Manchas pegadas al borde de abajo y de la derecha.",
           {"rte": "Al mirar el vecino de abajo (v + C) desde la última fila te sales del bitmap.",
            "wa": "No recorres bien los bordes: revisa que los bucles van hasta F-1 y C-1 incluidos."},
           ["Comprueba i + 1 < F antes de mirar el de abajo.",
            "Revisa que tus bucles son i < F y j < C (no ≤ ni F-1)."])
    prueba("Forma de U", "trampa", [["#-#", "#-#", "###"], ["#-#-#", "#-#-#", "#####"]],
           "Partes de una mancha que solo se juntan al final (abajo).",
           {"wa": "Tu método cuenta las patas de la U como manchas distintas. Hace falta un recorrido (DFS/BFS) o conjuntos disjuntos, no una sola pasada mirando arriba e izquierda."},
           ["La U «#-#»/«#-#»/«###» es una sola mancha de 7.",
            "Al descubrir un píxel nuevo, recorre toda su mancha antes de seguir buscando."])
    prueba("Varios casos seguidos", "trampa", [["####", "####"], ["#-", "-#"], ["-"], ["##", "#-"]],
           "Un caso grande seguido de otros pequeños: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: un vector de visitados, un contador o el máximo global que no se reinicia.",
            "rte": "Un vector de un caso anterior con otro tamaño: créalo dentro de resuelveCaso (o redimensiónalo en cada caso)."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara el grafo, los visitados y los contadores dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(rng, rng.randint(1, 9), rng.randint(1, 9), rng.choice([.3, .5, .7])) for _ in range(40)],
           "40 bitmaps pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: mira la línea que falla, cuenta qué caso es y prueba ese bitmap a mano."},
           ["La línea que falla es el número de caso: busca ese bitmap en la entrada.",
            "Dibuja ese caso en papel y sigue tu recorrido paso a paso."])
    prueba("Grande aleatorio (1000×1000)", "rendimiento", [aleatorio(rng, 1000, 1000, .4)],
           "El tamaño máximo (F·C = 10⁶): mide la eficiencia.",
           {"tle": "Tu solución es lenta para 10⁶ píxeles. Debe ser O(F·C): cada píxel se visita una vez.",
            "mle": "Gastas demasiada memoria: con 10⁶ píxeles, evita matrices F·C × F·C o copiar el bitmap en cada llamada.",
            "rte": "Con 10⁶ píxeles se rompe: revisa tamaños de vectores y pasa el grafo/bitmap por referencia."},
           ["¿Vuelves a recorrer píxeles ya visitados? Cada uno debe procesarse una vez.",
            "Pasa los vectores por referencia (const&) a las funciones recursivas; copiarlos en cada llamada es muy caro.",
            "Si usas una matriz de adyacencia (F·C)², cámbiala por listas de adyacencia (la clase Grafo)."])
    prueba("Mancha muy larga (serpiente de ~50.000 píxeles)", "rendimiento", [serpiente(199, 495)],
           "Una mancha en zigzag con el máximo de píxeles: recursión muy profunda.",
           {"rte": "La recursión del DFS es muy profunda. Aquí no debería romperse (el juez da pila de sobra); revisa que no reservas arrays grandes dentro de la función recursiva.",
            "tle": "Algo se repite de más al seguir la mancha: ¿marcas los visitados al entrar?",
            "wa": "Pierdes parte de la mancha al recorrerla: revisa los vecinos de los extremos de cada fila."},
           ["No declares vectores ni arrays locales dentro de la función recursiva.",
            "Si tu DFS es iterativo con una pila, marca visitado al apilar, no al desapilar."])
    prueba("Muchas manchas diminutas", "rendimiento", [["#-" * 250 if i % 2 == 0 else "-#" * 250 for i in range(1000)]],
           "Un tablero de ajedrez de 1000×500: 250.000 manchas de 1 píxel.",
           {"tle": "Algo cuesta por cada mancha más de lo que debería: ¿reinicias un vector entero de visitados cada vez que empiezas una mancha?",
            "wa": "Con muchas manchas, ¿usas int para contar? Debería bastar; revisa que no se mezclan diagonales."},
           ["Los visitados se crean una vez por caso, no una vez por mancha."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d %d\n" % manchas(len(c), len(c[0]), c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]



VARIANTES = [
    Variante("une el final de una fila con la siguiente",
             [("if (j + 1 < C && bitmap[i][j + 1] == '#')", "if (v + 1 < F * C && (j + 1 < C ? bitmap[i][j + 1] : bitmap[i + 1][0]) == '#')")], prueba=9, v="wa"),
    Variante("cruza F y C al numerar", [("int v = i * C + j;", "int v = i * F + j;"), ("g.ponArista(v, v + C);", "g.ponArista(v, v + F);")], prueba=8, v="rte"),
    Variante("une diagonales", [("if (i + 1 < F && bitmap[i + 1][j] == '#') g.ponArista(v, v + C);   // abajo",
                                "if (i + 1 < F && bitmap[i + 1][j] == '#') g.ponArista(v, v + C);\n if (i + 1 < F && j + 1 < C && bitmap[i + 1][j + 1] == '#') g.ponArista(v, v + C + 1);")], prueba=6, v="wa"),
    Variante("no reinicia entre casos", [("Grafo g(F * C);\n    vector<bool> negro(F * C, false);",
                                          "Grafo g(F * C);\n    static vector<bool> negro; if (negro.size() < (size_t)(F * C)) negro.resize(F * C);")], prueba=12, v="wa"),
    Variante("formato con salto de línea", [("cout << m.numero() << ' ' << m.mayor() << '\\n';", "cout << m.numero() << '\\n' << m.mayor() << '\\n';")], prueba=1, v="pe"),
    Variante("copia el grafo en cada llamada", [("int dfs(Grafo const& g, int v) {", "int dfs(Grafo g, int v) {")], prueba=14, v="mle"),
    Variante("máximo inicializado a 1", [("visit(g.V(), false), num(0), maxim(0)", "visit(g.V(), false), num(0), maxim(1)")], prueba=3, v="wa"),
]
