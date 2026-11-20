"""03-3 · Multitarea: juez con pruebas pensadas para cada error típico."""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-3/EJ_03-3.cpp",
    "cabeceras": ["3-Colas de prioridad variable (Heapsort)/EJ_03-3/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["if (ini < tiempoActual) hayConflictos = true;", "if (ini <= tiempoActual) hayConflictos = true;"],
}


def _choca_unica_periodica(a, b, c, f, p, T):
    """¿La tarea única [a, b) se pisa con alguna aparición [c + kp, f + kp) empezando la zona común antes de T?"""
    k = max(0, -(-(a - f + 1) // p))          # primera aparición que acaba después de a
    ini = c + k * p
    return ini < b and max(a, ini) < T


def conflicto(unicas, periodicas, T):
    """Solucionador independiente. Apariciones en orden de comienzo (fusión perezosa con heapq);
    hay conflicto si una empieza antes de que acabe alguna anterior y esa zona común empieza antes de T.
    Con muchísimas apariciones y una sola periódica, se comprueba por parejas (fórmula cerrada)."""
    if len(periodicas) == 1 and periodicas[0][2] < 50:
        c, f, p = periodicas[0]
        u = sorted(unicas)
        for (a1, b1), (a2, b2) in zip(u, u[1:]):
            if a2 < b1 and a2 < T:
                return True
        return any(_choca_unica_periodica(a, b, c, f, p, T) for a, b in unicas)
    h = [(a, b, 0) for a, b in unicas] + [(c, f, p) for c, f, p in periodicas]
    heapq.heapify(h)
    fin_max = None
    while h and h[0][0] < T:
        a, b, p = heapq.heappop(h)
        if fin_max is not None and a < fin_max:
            return True
        fin_max = b if fin_max is None else max(fin_max, b)
        if p:
            heapq.heappush(h, (a + p, b + p, p))
    return False


def caso_a_texto(c):
    unicas, periodicas, T = c
    return (f"{len(unicas)} {len(periodicas)} {T}\n" + "".join(f"{a} {b}\n" for a, b in unicas)
            + "".join(f"{a} {b} {p}\n" for a, b, p in periodicas))


def aleatorio(r, maxT, maxTareas, maxDur):
    while True:
        n, m = r.randint(0, maxTareas), r.randint(0, maxTareas)
        if n + m:
            break
    unicas = []
    for _ in range(n):
        a = r.randint(0, maxT)
        unicas.append((a, a + r.randint(1, maxDur)))
    periodicas = []
    for _ in range(m):
        a, d = r.randint(0, maxT), r.randint(1, maxDur)
        periodicas.append((a, a + d, r.randint(d, d + 3 * maxDur)))
    return unicas, periodicas, r.randint(0, maxT + maxDur)


def pruebas():
    r = random.Random(33)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [([(2, 5), (4, 6)], [], 10), ([], [(1, 4, 8), (5, 7, 8)], 10), ([(8, 20), (1, 5)], [(6, 7, 10)], 10)],
           "Los tres casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (N únicas con 2 números, M periódicas con 3), el orden de las apariciones o la ventana [0, T).",
            "pe": "Los resultados están bien pero no el formato: «SI» o «NO» (sin tilde), uno por línea.",
            "tle": "No termina ni con el ejemplo: ¿el bucle avanza siempre? Cada vuelta debe sacar la tarea única o pasar la periódica a su siguiente aparición."},
           ["En el tercer caso hay un choque en el minuto 16, pero solo interesan los conflictos que empiezan antes de T = 10.",
            "Escribe «SI» o «NO» en mayúsculas y sin tilde, una línea por caso.",
            "La entrada empieza con el número de casos: usa la plantilla de número de casos."])
    prueba("Una sola tarea", "borde",
           [([(0, 5)], [], 10), ([], [(3, 4, 7)], 100), ([(0, 100000000)], [], 100000000)],
           "Con una sola tarea nunca hay conflicto (una periódica no choca consigo misma).",
           {"wa": "Con una sola tarea sale «SI»: o comparas la tarea consigo misma o empiezas el «fin de la anterior» con un valor que no es neutro.",
            "rte": "Con una sola tarea (N = 0 o M = 0) te sales: revisa los tamaños de los vectores y de la cola (N + M)."},
           ["Una tarea sola nunca está en conflicto: la respuesta es «NO» en los tres casos.",
            "El «fin de la última aparición» debe empezar en 0 (o en algo que no choque con nada)."])
    prueba("Ventanas mínimas (T = 0 y T = 1)", "borde",
           [([(0, 3), (0, 2)], [], 1), ([(1, 3), (1, 2)], [], 1), ([(0, 3), (0, 2)], [], 0)],
           "Ventanas de un minuto o vacías: solo cuentan los conflictos que empiezan antes de T.",
           {"wa": "Con ventanas mínimas te equivocas en el borde: el conflicto debe EMPEZAR en un minuto < T. Con T = 0 no hay ningún minuto que mirar."},
           ["Primer caso: las dos tareas ocupan el minuto 0 (< 1): «SI». Segundo: chocan desde el minuto 1, que ya no cuenta: «NO».",
            "Para la apariciones, la condición de seguir es «empieza antes de T» (ini < T)."])
    prueba("Intervalos que se tocan no chocan", "trampa",
           [([(2, 8), (8, 10), (10, 11)], [], 100)],
           "[2, 8), [8, 10) y [10, 11) van seguidos: el final no está incluido, así que no hay conflicto.",
           {"wa": "Consideras conflicto que una tarea empiece justo cuando acaba otra. Los intervalos son [c, f): f no está incluido. Usa < y no ≤."},
           ["[2, 8) acaba en 8 y [8, 10) empieza en 8: no se pisan. La respuesta es «NO».",
            "Hay conflicto solo si el comienzo es ESTRICTAMENTE menor que el fin de la anterior: ini < fin."])
    prueba("Mismo instante de comienzo", "trampa",
           [([(3, 5), (3, 4)], [], 10)],
           "Dos tareas que empiezan a la vez siempre chocan (todas duran al menos un minuto).",
           {"wa": "Dos tareas que empiezan en el mismo minuto no las ves como conflicto: tras procesar la primera, la segunda empieza antes de que esta acabe."},
           ["[3, 5) y [3, 4) comparten el minuto 3: «SI».",
            "No compares los comienzos entre sí: compara el comienzo de cada aparición con el FIN de la anterior."])
    prueba("Una tarea dentro de otra", "trampa",
           [([(0, 10), (2, 3), (11, 12)], [], 20)],
           "Una tarea corta completamente dentro de una larga.",
           {"wa": "No detectas una tarea contenida en otra: compara el comienzo de cada una con el fin de la anterior, no los finales entre sí."},
           ["[2, 3) está dentro de [0, 10): «SI».",
            "Ordena por comienzo y guarda el fin de la anterior: 2 < 10, conflicto."])
    prueba("Tareas desordenadas en la entrada", "trampa",
           [([(0, 5), (10, 12), (4, 6)], [], 20)],
           "Las tareas no vienen ordenadas: hay que compararlas por orden de comienzo, no en el orden de la entrada.",
           {"wa": "Comparas cada tarea con la anterior en el orden en que llegan. Hay que procesarlas por orden de comienzo (con una cola de mínimos)."},
           ["[0, 5) y [4, 6) se pisan aunque entre ellas venga [10, 12) en la entrada: «SI».",
            "Mete todas las tareas en una cola de mínimos por (comienzo, fin) y ve sacándolas en orden."])
    prueba("Conflicto que empieza justo en T", "trampa",
           [([(0, 10), (5, 8)], [], 5)],
           "La zona común empieza en el minuto T, que ya está fuera de [0, T).",
           {"wa": "Cuentas un conflicto que empieza en el minuto T: la ventana es [0, T), así que T no está incluido. La condición es ini < T."},
           ["Las tareas chocan a partir del minuto 5, y T = 5: «NO».",
            "Deja de sacar apariciones cuando la siguiente empiece en T o más tarde (sigue solo mientras ini < T)."])
    prueba("Conflicto que empieza antes de T y sigue después", "trampa",
           [([(0, 10), (4, 6)], [], 5)],
           "Ninguna de las dos tareas acaba antes de T, pero chocan en el minuto 4 < T.",
           {"wa": "Solo miras las tareas que terminan antes de T. Una tarea cuenta si EMPIEZA antes de T, aunque acabe mucho después."},
           ["[0, 10) y [4, 6) se pisan en el minuto 4, dentro de [0, 5): «SI».",
            "La condición para seguir procesando es que la aparición empiece antes de T, no que acabe antes."])
    prueba("La periódica se repite", "trampa",
           [([(19, 25)], [(0, 2, 10)], 100)],
           "La tarea periódica no choca en su primera aparición, sino en la tercera ([20, 22)).",
           {"wa": "Tratas las periódicas como si aparecieran una sola vez: después de cada aparición hay que pasar a la siguiente (ini + p, fin + p)."},
           ["La periódica ocupa [0, 2), [10, 12), [20, 22)…; [20, 22) se pisa con [19, 25): «SI».",
            "Una periódica no se saca de la cola: se actualiza su prioridad a la siguiente aparición."])
    prueba("La repetición avanza entera (comienzo y fin)", "trampa",
           [([(11, 12)], [(0, 3, 10)], 100)],
           "La segunda aparición de la periódica es [10, 13): hay que sumar el periodo al comienzo Y al fin.",
           {"wa": "Al pasar a la siguiente aparición solo sumas el periodo al comienzo (o solo al fin). Las dos marcas se desplazan p minutos."},
           ["La periódica ocupa [0, 3), [10, 13)…; [11, 12) está dentro de [10, 13): «SI».",
            "La siguiente aparición de (ini, fin) es (ini + p, fin + p)."])
    prueba("Periódica con apariciones pegadas", "trampa",
           [([], [(0, 5, 5)], 1000)],
           "Una periódica que dura tanto como su periodo: [0, 5), [5, 10)… van seguidas y no chocan.",
           {"wa": "La periódica choca consigo misma: sus apariciones se tocan pero no se pisan ([0, 5) y [5, 10)). Revisa el < frente al ≤."},
           ["Con c = 0, f = 5 y p = 5 las apariciones van una detrás de otra: «NO».",
            "El enunciado garantiza que una periódica no se solapa consigo misma: no hace falta comprobarlo aparte."])
    prueba("Dos periódicas que chocan tarde", "trampa",
           [([], [(0, 3, 1009), (500, 504, 997)], 126126), ([], [(0, 3, 1009), (500, 504, 997)], 126125)],
           "Dos periódicas que se cruzan sin tocarse durante más de cien repeticiones: el primer conflicto empieza en el minuto 126125.",
           {"wa": "Solo miras unas pocas repeticiones (o calculas mal la siguiente). Hay que seguir avanzando apariciones mientras empiecen antes de T."},
           ["El primer choque empieza en el minuto 126125: con T = 126126 hay conflicto y con T = 126125 todavía no.",
            "No hay atajos: repite «saca la que empieza antes, compara, avanza su siguiente aparición» hasta T o hasta el primer conflicto."])
    prueba("Varios casos seguidos", "trampa",
           [([(0, 100)], [], 200), ([(5, 6)], [], 10), ([(0, 2), (1, 3)], [], 5), ([(3, 4)], [(0, 1, 2)], 10)],
           "Un caso que acaba con el «fin de la última aparición» muy alto seguido de otros: cada caso empieza de cero.",
           {"wa": "Algo se arrastra de un caso a otro: el fin de la última aparición, el indicador de conflicto o la cola deben inicializarse en cada caso."},
           ["El primer caso deja el último fin en 100: en el segundo, [5, 6) no choca con nada.",
            "Declara la cola, el vector de periodos, el último fin y el indicador dentro de resuelveCaso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, 30, 3, 6) for _ in range(150)],
           "150 casos pequeños al azar (tiempos hasta 30).",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibuja sus intervalos en papel."},
           ["Busca el caso que falla (una línea por caso) y escribe las apariciones de cada tarea hasta T.",
            "Comprueba los bordes: [c, f) no incluye f, y la ventana [0, T) no incluye T."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, 3000, 40, 15) for _ in range(40)],
           "40 casos con decenas de tareas y periodos variados.",
           {"wa": "Falla algún caso mediano: busca entre las pruebas pequeñas uno parecido que también falle; es más fácil de seguir."},
           ["Si los pequeños salen bien, revisa lo que solo pasa con muchas tareas: varias periódicas a la vez, empates en el comienzo…",
            "La cola debe ordenar por (comienzo, fin) de la próxima aparición de cada tarea."])
    # rendimiento
    unicas = [(k * 10000, k * 10000 + 9999) for k in range(10000)]
    r.shuffle(unicas)
    prueba("10.000 tareas únicas sin conflicto", "rendimiento", [(unicas, [], 100000000)],
           "El máximo de tareas, todas únicas, desordenadas y sin conflicto.",
           {"tle": "Comparar cada tarea con todas las demás es O(n²): ordénalas por comienzo (con la cola) y compara solo con la anterior."},
           ["Con 10.000 tareas, comparar todas las parejas son 5·10⁷ comparaciones por caso.",
            "Basta comparar cada tarea con la que acabó justo antes en orden de comienzo."])
    periodicas = [(k * 50, k * 50 + 10, 500000) for k in range(10000)]
    r.shuffle(periodicas)
    prueba("10.000 periódicas y un millón de apariciones", "rendimiento", [([], periodicas, 50000000)],
           "10.000 periódicas que se turnan sin chocar: hay un millón de apariciones antes de T.",
           {"tle": "Para encontrar la siguiente aparición recorres todas las tareas: O(N + M) por aparición. Con una cola de mínimos es O(log(N + M)).",
            "mle": "Generar todas las apariciones de antemano gasta demasiada memoria: genera cada una cuando haga falta (update de la periódica)."},
           ["Hay 10⁶ apariciones: si cada una cuesta recorrer 10⁴ tareas, son 10¹⁰ operaciones.",
            "Guarda en una IndexPQ la próxima aparición de cada tarea; al procesarla, update a (ini + p, fin + p)."])
    prueba("Conflicto al principio y T enorme", "rendimiento",
           [([], [(k, k + 1, 10000) for k in range(9999)] + [(0, 1, 10000)], 100000000)],
           "Dos periódicas chocan en el minuto 0 y T = 10⁸: hay que parar en el primer conflicto.",
           {"tle": "Sigues procesando apariciones después de encontrar el conflicto: en cuanto hay uno, la respuesta es «SI» y se puede parar."},
           ["Aquí hay 10⁸ apariciones antes de T, pero el conflicto está en el minuto 0.",
            "Añade a la condición del bucle «mientras no haya conflicto»."])
    prueba("Una periódica de periodo 4 y T = 10⁸", "rendimiento",
           [([(99999996, 100000000)], [(0, 1, 4)], 100000000)],
           "Una periódica con 2,5·10⁷ apariciones antes de T y un único conflicto al final del todo.",
           {"tle": "Cada aparición debe costar muy poco (un update en la cola): evita estructuras que crecen con T.",
            "mle": "No guardes un vector del tamaño de T ni todas las apariciones a la vez: 10⁸ posiciones no caben en memoria."},
           ["No reserves un vector de T minutos ni generes todas las apariciones de golpe.",
            "Con la cola solo hay N + M elementos en cada momento: la periódica se va actualizando."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(("SI" if conflicto(*c) else "NO") + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_BARRIDO_LINEAL = """vector<pair<int, int>> sig(N + M);
	for (int i = 0; i < N + M; ++i) sig[i] = cola.priority(i);
	vector<bool> vivo(N + M, true);
	int tiempoActual = 0;
	bool hayConflictos = false;
	while (!hayConflictos) {
		int elem = -1;
		for (int i = 0; i < N + M; ++i) if (vivo[i] && (elem == -1 || sig[i] < sig[elem])) elem = i;
		if (elem == -1 || sig[elem].first >= T) break;
		int ini = sig[elem].first, fin = sig[elem].second;
		if (ini < tiempoActual) hayConflictos = true;
		else {
			tiempoActual = fin;
			if (periodo[elem] != 0) sig[elem] = { ini + periodo[elem], fin + periodo[elem] };
			else vivo[elem] = false;
		}
	}"""

VARIANTES = [
    Variante("≤ en vez de < al comparar con el fin anterior",
             [("if (ini < tiempoActual) hayConflictos = true;", "if (ini <= tiempoActual) hayConflictos = true;")], prueba=4, v="wa"),
    Variante("cuenta el minuto T", [("cola.top().prioridad.first < T", "cola.top().prioridad.first <= T")], prueba=8, v="wa"),
    Variante("solo mira las tareas que acaban antes de T",
             [("cola.top().prioridad.first < T", "cola.top().prioridad.second <= T")], prueba=9, v="wa"),
    Variante("las periódicas no se repiten", [("if (periodo[elem] != 0)", "if (false)")], prueba=10, v="wa"),
    Variante("la repetición solo mueve el comienzo",
             [("{ ini + periodo[elem], fin + periodo[elem] }", "{ ini + periodo[elem], fin }")], prueba=11, v="wa"),
    Variante("el último fin no se reinicia entre casos", [("int tiempoActual = 0;", "static int tiempoActual = 0;")], prueba=14, v="wa"),
    Variante("todas las respuestas en una línea", [("<< \"\\n\";\n}", "<< \" \";\n}")], prueba=1, v="pe"),
    Variante("no para en el primer conflicto",
             [("while (!hayConflictos && !cola.empty()", "while (!cola.empty()"),
              ("if (ini < tiempoActual) hayConflictos = true;\n\t\telse {", "if (ini < tiempoActual) hayConflictos = true;\n\t\t{")],
             prueba=19, v="tle"),
    Variante("busca la siguiente aparición recorriendo todas las tareas",
             [("int tiempoActual = 0;\n\tbool hayConflictos = false;\n\twhile (!hayConflictos && !cola.empty() && cola.top().prioridad.first < T) {\n\t\tauto tarea = cola.top();\n\t\tint elem = tarea.elem;\n\t\tint ini = tarea.prioridad.first;\n\t\tint fin = tarea.prioridad.second;\n\n\t\tif (ini < tiempoActual) hayConflictos = true;\n\t\telse {\n\t\t\ttiempoActual = fin;\n\t\t\tif (periodo[elem] != 0)\n\t\t\t\tcola.update(elem, { ini + periodo[elem], fin + periodo[elem] });\n\t\t\telse\n\t\t\t\tcola.pop();\n\t\t}\n\t}",
               _BARRIDO_LINEAL)], prueba=18, v="tle"),
]
