"""09-2 · El alienígena infiltrado: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «C F N» y N líneas «c f» (intervalos semiabiertos [c, f)).
Salida: el mínimo número de trabajos que cubren todo [C, F), o «Imposible».
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "9-Algoritmos voraces II/EJ_09-2/EJ_09-2.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["trab[i].first <= cubierto", "trab[i].first < cubierto"],
}


def resuelve(C, F, trab):
    """Solucionador independiente: desde el punto alcanzado, entre los trabajos que empiezan como
    muy tarde en él, se coge el que llega más lejos."""
    trab = sorted(trab)
    alcanzado, n, i = C, 0, 0
    while alcanzado < F:
        mejor = alcanzado
        while i < len(trab) and trab[i][0] <= alcanzado:
            mejor = max(mejor, trab[i][1])
            i += 1
        if mejor == alcanzado:
            return "Imposible"
        alcanzado, n = mejor, n + 1
    return str(n)


def caso_a_texto(c):
    C, F, trab = c
    return f"{C} {F} {len(trab)}\n" + "".join(f"{a} {b}\n" for a, b in trab)


def aleatorio(rng, n, maxc, maxlong):
    C = rng.randint(0, maxc - 1)
    F = rng.randint(C + 1, maxc)
    trab = []
    for _ in range(n):
        a = rng.randint(0, maxc - 1)
        trab.append((a, min(maxc, a + rng.randint(1, maxlong))))
    return (C, F, trab)


def pruebas():
    rng = random.Random(902)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(1, 10, [(2, 8), (0, 5), (7, 11), (5, 10)]), (0, 3, [(0, 1), (2, 3)])],
           "Los dos ejemplos del PDF: uno se cubre con dos trabajos y otro es imposible.",
           {"wa": "Si falla hasta el ejemplo, revisa la lectura (C, F y N en la misma línea), la idea voraz y que escribes «Imposible» tal cual.",
            "tle": "Tu programa no termina: cuando hay un hueco que nadie cubre, el bucle no avanza. Detecta que ningún trabajo pasa del punto ya cubierto y para."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "En el segundo caso hay un hueco entre 1 y 2: el programa debe darse cuenta y escribir «Imposible».",
            "Si en una vuelta ningún trabajo llega más allá de lo ya cubierto, no tiene sentido seguir: es imposible."])
    prueba("Ningún trabajo propuesto", "borde", [(0, 5, [])],
           "Con N = 0 no se puede cubrir nada: «Imposible».",
           {"wa": "Con N = 0 debe salir «Imposible» (C < F siempre, así que hay algo que cubrir).",
            "rte": "Con N = 0 accedes a un trabajo que no existe (por ejemplo trab[0])."},
           ["¿Qué hace tu programa si no hay ningún trabajo?",
            "No accedas a trab[0] sin comprobar que N > 0."])
    prueba("Un trabajo que coincide con el intervalo", "borde", [(3, 9, [(3, 9)])],
           "Un único trabajo exactamente igual a [C, F): basta 1.",
           {"wa": "Un trabajo [C, F) cubre todo: revisa las comparaciones con C y con F."},
           ["El trabajo [3, 9) empieza en C y acaba en F.",
            "El intervalo es semiabierto: llegar a F ya es cubrir todo."])
    prueba("Trabajos que se tocan en un extremo", "trampa", [(0, 10, [(0, 5), (5, 10)])],
           "[0, 5) y [5, 10) no dejan hueco: el segundo empieza justo donde acaba el primero.",
           {"wa": "Exiges que el siguiente trabajo empiece ANTES de lo cubierto (<). Como los intervalos son [c, f), basta con que empiece justo ahí (≤)."},
           ["El instante 5 lo cubre el segundo trabajo: no hay hueco.",
            "Un trabajo sirve para seguir si su comienzo es ≤ que el punto hasta el que ya está cubierto."])
    prueba("Hueco de una unidad", "trampa", [(0, 3, [(0, 1), (2, 3)])],
           "[0, 1) y [2, 3) dejan sin cubrir [1, 2): «Imposible».",
           {"wa": "No detectas el hueco: o tratas los intervalos como cerrados (que [0, 1) cubre el instante 1) o, al no encontrar trabajo para seguir, escribes lo que llevas en vez de «Imposible».",
            "tle": "Al encontrar el hueco tu bucle se queda dando vueltas: si ningún trabajo pasa de lo cubierto, hay que parar."},
           ["Los intervalos no incluyen su final: [0, 1) no cubre el instante 1.",
            "Si en una vuelta ningún trabajo nuevo llega más allá de lo cubierto, el resultado es «Imposible»."])
    prueba("El primer trabajo empieza después de C", "trampa", [(2, 8, [(3, 8)])],
           "El trabajo [3, 8) no cubre [2, 3): «Imposible».",
           {"wa": "Empiezas a cubrir desde el comienzo del primer trabajo en vez de desde C."},
           ["El intervalo a cubrir empieza en C = 2, y nadie cubre el instante 2.",
            "El punto «cubierto hasta» empieza valiendo C, no el comienzo de ningún trabajo."])
    prueba("No se llega hasta F", "trampa", [(0, 10, [(0, 4), (3, 9)])],
           "Los trabajos cubren [0, 9) pero no llegan a 10: «Imposible».",
           {"wa": "Cuando se acaban los trabajos sin llegar a F, no lo detectas: el bucle debe seguir mientras lo cubierto sea < F."},
           ["Tras coger los dos trabajos solo está cubierto hasta 9.",
            "Al terminar, comprueba que lo cubierto llega al menos a F; si no, «Imposible»."])
    prueba("Trabajos que empiezan antes de C", "trampa", [(5, 10, [(0, 7), (6, 10), (5, 6)])],
           "Un trabajo que empieza antes de C también sirve: [0, 7) y [6, 10) bastan.",
           {"wa": "Descartas los trabajos que empiezan antes de C, pero también cubren el principio del intervalo."},
           ["[0, 7) cubre [5, 7) aunque empiece antes.",
            "La condición para poder elegir un trabajo es solo c ≤ cubierto (y al principio cubierto = C)."])
    prueba("Elegir el que llega más lejos", "trampa", [(0, 10, [(0, 2), (0, 10)])],
           "Entre los que empiezan a tiempo hay que coger el que acaba más tarde: [0, 10) solo.",
           {"wa": "Coges el primer trabajo que empieza a tiempo (o el que antes acaba) en vez del que llega más lejos."},
           ["Aquí basta un trabajo.",
            "Mira TODOS los trabajos que empiezan como muy tarde en lo ya cubierto y quédate con el mayor final."])
    prueba("El más largo no es el mejor", "trampa", [(0, 10, [(0, 5), (4, 10), (1, 8)])],
           "Coger primero el trabajo más largo no es óptimo: [0, 5) y [4, 10) bastan.",
           {"wa": "Eliges por longitud. El criterio correcto avanza desde C: de los que empiezan a tiempo, el que acaba más tarde."},
           ["[1, 8) es el más largo, pero con él hacen falta tres.",
            "Recorre de izquierda a derecha: el trabajo que cubra el instante C y llegue más lejos."])
    prueba("Trabajos fuera del intervalo", "trampa", [(10, 20, [(0, 5), (0, 10), (20, 30), (10, 20)])],
           "Trabajos que acaban justo en C o empiezan justo en F no sirven; [10, 20) basta.",
           {"wa": "Cuentas trabajos que no aportan nada: [0, 10) acaba justo en C y [20, 30) empieza en F."},
           ["Solo hace falta un trabajo.",
            "Un trabajo solo cuenta si hace avanzar lo cubierto (su final es mayor que lo ya cubierto)."])
    prueba("Trabajo que se pasa de F", "borde", [(0, 5, [(0, 100), (0, 3)])],
           "Un trabajo que acaba después de F cubre todo lo que falta.",
           {"wa": "Basta con llegar a F o más allá; no hace falta acabar exactamente en F."},
           ["[0, 100) cubre [0, 5) de sobra.",
            "La condición para parar es cubierto ≥ F."])
    prueba("Trabajos repetidos y contenidos", "trampa",
           [(0, 12, [(0, 6), (0, 6), (1, 3), (2, 5), (6, 12), (6, 12), (7, 9)])],
           "Trabajos repetidos o metidos dentro de otros: no deben contarse.",
           {"wa": "Cuentas trabajos de más: solo se elige uno por cada salto, el que llega más lejos."},
           ["Bastan [0, 6) y [6, 12).",
            "En cada vuelta se cuenta UN trabajo, aunque se recorran varios."])
    prueba("Extremos hasta 10⁹", "borde", [(0, 1000000000, [(0, 500000000), (500000000, 1000000000)])],
           "Valores en el máximo que permite el enunciado.",
           {"wa": "Con valores cerca de 10⁹ algo se sale de rango: revisa los tipos."},
           ["Bastan 2 trabajos.",
            "10⁹ cabe en int, pero si sumas extremos o usas centinelas, usa long long."])
    prueba("Varios casos seguidos", "trampa",
           [(0, 8, [(0, 2), (2, 4), (4, 6), (6, 8)]), (0, 2, [(0, 2)]), (0, 5, [(1, 5)]), (3, 6, [(0, 4), (4, 6)])],
           "Varios casos (posibles e imposibles) seguidos: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el contador, el vector o la marca de «imposible» no se reinician."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara todo (vector, contador, índice, «cubierto») dentro de la función de cada caso."])
    peq = [aleatorio(rng, rng.randint(0, 7), 12, rng.choice([2, 4, 8])) for _ in range(200)]
    prueba("Aleatorios pequeños", "aleatorio", peq,
           "200 casos pequeños al azar, posibles e imposibles.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibújalo en papel."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Dibuja los intervalos sobre una recta y sigue tu algoritmo paso a paso."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(rng, rng.randint(50, 400), rng.choice([1000, 1000000000]), rng.choice([60, 300000000])) for _ in range(30)],
           "30 casos medianos con coordenadas variadas.",
           {"wa": "Algo falla con más trabajos: revisa los empates y los trabajos que se tocan en un extremo."},
           ["Busca el caso que falla y redúcelo quitando trabajos mientras siga fallando.",
            "Compara con: ordenar por comienzo y, desde C, coger siempre el que llega más lejos."])
    cadena = [(k, k + 1) for k in range(150000)]
    rng.shuffle(cadena)
    prueba("Cadena de 150.000 trabajos", "rendimiento", [(0, 150000, cadena)],
           "Hacen falta todos los trabajos, uno detrás de otro: mide que no vuelvas a recorrerlos desde el principio en cada paso.",
           {"tle": "Tu solución es cuadrática: en cada paso vuelves a mirar los trabajos desde el principio. Con los trabajos ordenados, el índice solo debe avanzar."},
           ["¿Cuántas veces miras cada trabajo? Debería ser una.",
            "Ordena una vez y recorre con un índice que no se reinicia entre una elección y la siguiente."])
    prueba("100.000 trabajos al azar", "rendimiento",
           [aleatorio(rng, 100000, 1000000000, 30000)],
           "Muchos trabajos en coordenadas grandes.",
           {"tle": "Tu solución es lenta: debe ser O(N log N) (ordenar y una pasada)."},
           ["Usa sort de la biblioteca.",
            "Tras ordenar, cada trabajo se mira una sola vez."])
    return [Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(resuelve(*c) + "\n" for c in casos), casos=len(casos),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("exige empezar antes de lo cubierto (<)", [("trab[i].first <= cubierto", "trab[i].first < cubierto")], prueba=4, v="wa"),
    Variante("intervalos cerrados", [("trab[i].first <= cubierto", "trab[i].first <= cubierto + 1")], prueba=5, v="wa"),
    Variante("con un hueco escribe lo que lleva", [("{ posible = false; break; }", "break;")], prueba=5, v="wa"),
    Variante("no detecta el hueco (bucle infinito)", [("if (masLejos == cubierto) { posible = false; break; }", "")], prueba=1, v="tle"),
    Variante("empieza a cubrir desde el primer trabajo",
             [("long long cubierto = C;", "long long cubierto = N > 0 ? max(C, trab[0].first) : C;")], prueba=6, v="wa"),
    Variante("descarta los que empiezan antes de C",
             [("trab[i].first <= cubierto) {", "trab[i].first <= cubierto && trab[i].first >= C) {")], prueba=8, v="wa"),
    Variante("coge el primero que empieza a tiempo",
             [("masLejos = max(masLejos, trab[i].second);", "if (masLejos == cubierto) masLejos = max(masLejos, trab[i].second);")], prueba=9, v="wa"),
    Variante("no reinicia entre casos", [("int usados = 0, i = 0;", "static int usados = 0; int i = 0;")], prueba=15, v="wa"),
    Variante("vuelve a mirar desde el principio",
             [("long long masLejos = cubierto;", "long long masLejos = cubierto; i = 0;")], prueba=18, v="tle"),
]
