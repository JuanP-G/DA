"""09-1 · ¡En primera línea de playa!: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «N» y N líneas «W E» (W < E, enteros 0..10⁹).
Salida: el mínimo número de pasadizos de 1 metro (el del metro [x, x+1] sirve a [W, E] si
W ≤ x y x + 1 ≤ E) para servir a todos los edificios.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "9-Algoritmos voraces II/EJ_09-1/EJ_09-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["x = E - 1;", "x = E;"],
}


def resuelve(edif):
    """Solucionador independiente: cada edificio es el conjunto de metros x con W ≤ x ≤ E - 1.
    Se recorren por el último metro que ocupan y se pone un pasadizo cuando hace falta."""
    n, ultimo = 0, None
    for w, e in sorted(edif, key=lambda t: t[1]):
        if ultimo is None or w > ultimo:
            n += 1
            ultimo = e - 1
    return n


def caso_a_texto(edif):
    return f"{len(edif)}\n" + "".join(f"{w} {e}\n" for w, e in edif)


def aleatorio(rng, n, maxc, maxlong):
    out = []
    for _ in range(n):
        w = rng.randint(0, maxc - 1)
        e = min(maxc, w + rng.randint(1, maxlong))
        out.append((w, e))
    return out


def pruebas():
    rng = random.Random(901)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [[(1, 4), (6, 15), (2, 10), (12, 20)], [(1, 4), (4, 8)], [(1, 4), (3, 8)]],
           "Los tres ejemplos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la lectura (primero W y luego E), la idea voraz o la salida: un número por línea.",
            "pe": "Los números están bien pero el formato no: un número por caso y un salto de línea detrás."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "El segundo caso es el delicado: [1, 4] y [4, 8] solo se tocan en un punto.",
            "Ordena los edificios por su extremo oriental y pon cada pasadizo lo más al este posible."])
    prueba("Un único edificio", "borde", [[(5, 9)]],
           "Con un solo edificio hace falta exactamente un pasadizo.",
           {"wa": "Con un edificio la respuesta es 1: revisa cómo inicializas el contador y la posición del último pasadizo."},
           ["¿Qué escribe tu programa con «1» y «5 9»?",
            "El primer edificio siempre necesita un pasadizo nuevo, sea cual sea la posición inicial."])
    prueba("Edificio que empieza en el metro 0", "trampa", [[(0, 1)]],
           "Edificios con W = 0: no deben darse por servidos por un pasadizo «inicial» imaginario.",
           {"wa": "Sale 0 o menos de lo debido: el «último pasadizo» empieza en una posición (0, por ejemplo) que ya sirve a un edificio que empieza en 0."},
           ["Antes de poner ningún pasadizo, ¿en qué metro crees que está «el último»?",
            "Inicializa la posición del último pasadizo a un valor imposible (por ejemplo -1) o trata aparte el primer edificio."])
    prueba("Ordenar al revés (de este a oeste) falla", "trampa", [[(1, 5), (2, 8), (6, 9)]],
           "Recorrer los edificios del que acaba más tarde al que acaba antes, poniendo el pasadizo al final, no es óptimo.",
           {"wa": "Ordenas de mayor a menor extremo oriental (o pones el pasadizo en el lado equivocado). La regla es: el que acaba antes, con el pasadizo lo más al este posible."},
           ["Con [1, 5], [2, 8] y [6, 9] hacen falta 2 pasadizos: [6, 9] y [1, 5] no comparten ningún metro.",
            "Si vas de este a oeste, el pasadizo debe ir lo más al OESTE posible (W); lo más simple es ir de oeste a este por E."])
    prueba("Edificios que solo se tocan en un punto", "trampa", [[(1, 4), (4, 8), (8, 9)]],
           "[1, 4], [4, 8] y [8, 9] se tocan en un punto pero no comparten ningún metro: hacen falta 3.",
           {"wa": "Tratas los edificios como si un punto común bastara. El pasadizo mide 1 metro: el del metro [x, x+1] sirve a [W, E] solo si W ≤ x y x + 1 ≤ E."},
           ["Dibuja [1, 4] y [4, 8]: ¿hay algún metro entero debajo de los dos?",
            "Si pones el pasadizo en el extremo E, en realidad lo estás poniendo fuera del edificio.",
            "Pon el pasadizo en el metro [E - 1, E] y considera servido al siguiente edificio solo si W ≤ E - 1."])
    prueba("Comparten justo un metro", "trampa", [[(1, 5), (4, 9)]],
           "[1, 5] y [4, 9] comparten el metro [4, 5]: basta un pasadizo.",
           {"wa": "Pides demasiado solapamiento: con que compartan un metro (W ≤ E - 1 del otro) basta. Revisa < frente a ≤."},
           ["El metro [4, 5] está completamente debajo de los dos.",
            "Un edificio está servido por el pasadizo [x, x+1] si W ≤ x (no W < x)."])
    prueba("Edificios de un metro de ancho", "borde", [[(2, 3), (3, 4), (3, 4), (4, 5)]],
           "Edificios de anchura 1: el pasadizo tiene que ir justo en su único metro.",
           {"wa": "Un edificio [W, W+1] solo admite el pasadizo del metro [W, W+1]: revisa los cálculos con E - 1."},
           ["Con [3, 4] el pasadizo solo puede ir en el metro 3.",
            "Los edificios repetidos comparten pasadizo; [4, 5] y [2, 3] necesitan cada uno el suyo."])
    prueba("Edificios desordenados", "trampa", [[(10, 12), (0, 2), (5, 7), (1, 3), (11, 13)]],
           "Los edificios no vienen ordenados en la entrada.",
           {"wa": "Parece que recorres los edificios en el orden de la entrada: hay que ordenarlos antes."},
           ["La entrada no garantiza ningún orden.",
            "Ordena los edificios (por su extremo oriental) antes de recorrerlos."])
    prueba("Ordenar por el extremo occidental no basta", "trampa", [[(1, 10), (2, 3), (5, 6)]],
           "Un edificio largo que empieza antes que otros cortos: ordenar por W y poner el pasadizo al final del primero falla.",
           {"wa": "Ordenas por el extremo occidental (W). El edificio [1, 10] empieza antes pero acaba tarde: su pasadizo en el metro 9 no sirve a [2, 3]."},
           ["Aquí hacen falta 2: uno en [2, 3] (que sirve también a [1, 10]) y otro en [5, 6].",
            "¿Qué edificio te obliga primero a poner un pasadizo? El que ACABA antes.",
            "Ordena por E y pon cada pasadizo en el metro [E - 1, E]."])
    prueba("Edificios anidados", "trampa", [[(0, 20), (3, 5), (8, 9), (14, 18)]],
           "Un edificio enorme que contiene a otros pequeños separados.",
           {"wa": "El edificio grande no debe decidir dónde van los pasadizos: lo hacen los pequeños, que acaban antes."},
           ["Bastan 3: uno por cada edificio pequeño, y cualquiera sirve al grande.",
            "Ordena por E: los pequeños salen antes que el grande."])
    prueba("Ordenar por longitud falla", "trampa", [[(0, 4), (3, 6), (5, 9)]],
           "Atender primero al edificio más corto no es un buen criterio.",
           {"wa": "Elegir el edificio más corto (o el que más se solapa) no es óptimo. El criterio correcto es el extremo oriental."},
           ["Aquí bastan 2: el metro [3, 4] sirve a los dos primeros y el [5, 6] a los dos últimos.",
            "Ordena por E y pon el pasadizo en el último metro del edificio que acaba antes."])
    prueba("Mismo extremo oriental", "trampa", [[(4, 9), (0, 9), (8, 9), (7, 12)]],
           "Varios edificios que acaban en el mismo punto (empates al ordenar).",
           {"wa": "Con empates en E, el resultado no debe depender de cuál vaya primero: todos admiten el metro [E - 1, E]."},
           ["Los cuatro comparten el metro [8, 9]: basta 1.",
            "Comprueba que, tras poner el pasadizo en [E - 1, E], los demás con el mismo E quedan servidos."])
    prueba("Coordenadas hasta 10⁹", "borde", [[(0, 1000000000), (999999999, 1000000000), (0, 1)]],
           "Extremos en los valores máximos que permite el enunciado.",
           {"wa": "Con valores cerca de 10⁹ algo se sale de rango: revisa los tipos y el valor inicial de la posición del último pasadizo."},
           ["Bastan 2: el metro [0, 1] y el [999999999, 1000000000].",
            "10⁹ cabe en int, pero no inventes centinelas como 10⁹ + 1 en un int sin pensarlo."])
    prueba("Varios casos seguidos", "trampa",
           [[(0, 5), (6, 10), (11, 15), (16, 20)], [(1, 3)], [(2, 5), (3, 6)], [(0, 2), (1, 3), (2, 4)]],
           "Un caso con muchos pasadizos seguido de otros: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el contador o la posición del último pasadizo no se reinician."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara el contador, el vector y la posición del último pasadizo dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(rng, rng.randint(1, 8), 15, rng.choice([1, 3, 6])) for _ in range(150)],
           "150 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; dibújalo en papel."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Dibuja los edificios sobre una recta y sigue tu algoritmo paso a paso."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(rng, rng.randint(50, 300), rng.choice([100, 10000, 1000000000]), rng.choice([2, 50, 100000000])) for _ in range(40)],
           "40 casos medianos con coordenadas variadas.",
           {"wa": "Algo falla con más edificios: revisa los empates y los edificios que se tocan en un punto."},
           ["Busca el caso que falla y redúcelo quitando edificios mientras siga fallando.",
            "Compara con un recorrido ordenado por E poniendo el pasadizo en [E - 1, E]."])
    prueba("100.000 edificios", "rendimiento", [aleatorio(rng, 100000, 1000000000, 3000000)],
           "El tamaño máximo de un caso: mide la eficiencia.",
           {"tle": "Tu solución es lenta para 100.000 edificios: debe ser O(N log N). ¿Comparas cada edificio con todos los demás o con todos los pasadizos?"},
           ["Ordenar cuesta O(N log N); el recorrido posterior debe ser una sola pasada.",
            "Basta con recordar el último pasadizo puesto; no hace falta mirar los anteriores.",
            "Usa sort de la biblioteca, no una ordenación cuadrática hecha a mano."])
    return [Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{resuelve(c)}\n" for c in casos), casos=len(casos),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("pasadizo en el punto E (un punto común basta)", [("x = E - 1;", "x = E;")], prueba=5, v="wa"),
    Variante("exige W < x (más solape del necesario)", [("W > x", "W >= x")], prueba=6, v="wa"),
    Variante("ordena por el extremo occidental",
             [("sort(edif.begin(), edif.end());",
               "sort(edif.begin(), edif.end(), [](auto a, auto b) { return a.second < b.second; });")], prueba=9, v="wa"),
    Variante("ordena de mayor a menor", [("sort(edif.begin(), edif.end());", "sort(edif.rbegin(), edif.rend());")], prueba=4, v="wa"),
    Variante("no ordena", [("sort(edif.begin(), edif.end());", "")], prueba=8, v="wa"),
    Variante("último pasadizo inicial en el metro 0",
             [("pasadizos == 0 || W > x", "W > x"), ("long long x = -1;", "long long x = 0;")], prueba=3, v="wa"),
    Variante("no reinicia entre casos", [("int pasadizos = 0;", "static int pasadizos = 0;")], prueba=14, v="wa"),
    Variante("ordenación cuadrática",
             [("sort(edif.begin(), edif.end());",
               "for (int a = 1; a < N; ++a) for (int b = a; b > 0 && edif[b] < edif[b - 1]; --b) swap(edif[b], edif[b - 1]);")],
             prueba=17, v="tle"),
]
