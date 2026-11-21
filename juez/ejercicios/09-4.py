"""09-4 · El telesilla: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno «P N» y una línea con N pesos (1..P, P ≤ 10⁹).
Salida: el mínimo número de sillas dobles (cada una con peso total ≤ P) para subir a todos.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "9-Algoritmos voraces II/EJ_09-4/EJ_09-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["peso[i] + peso[j] <= P", "peso[i] + peso[j] < P"],
}


def resuelve(P, pesos):
    """Solucionador independiente: máximo de parejas con suma ≤ P (cada ligero, empezando por el
    más ligero, se empareja con el más pesado con el que cabe); sillas = N - parejas."""
    p = sorted(pesos)
    lo, hi, parejas = 0, len(p) - 1, 0
    while lo < hi:
        if p[lo] + p[hi] <= P:
            parejas += 1
            lo += 1
        hi -= 1
    return len(p) - parejas


def caso_a_texto(c):
    P, pesos = c
    return f"{P} {len(pesos)}\n" + " ".join(map(str, pesos)) + "\n"


def aleatorio(rng, n, P):
    return (P, [rng.randint(1, P) for _ in range(n)])


def pruebas():
    rng = random.Random(904)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(20, [10, 10, 10, 10]), (30, [12, 20, 10, 16, 8]), (40, [30] * 6)],
           "Los tres ejemplos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la lectura (primero P y luego N), el criterio voraz y que escribes un número por caso."},
           ["Ejecútalo en tu ordenador con este mismo ejemplo y compara línea a línea.",
            "Ojo al orden de la primera línea de cada caso: primero el peso máximo P y después N.",
            "Ordena los pesos y mira a la vez el más ligero y el más pesado."])
    prueba("Un único usuario", "trampa", [(50, [50])],
           "Con un solo usuario hace falta un viaje.",
           {"wa": "El último usuario que queda solo no se cuenta: cuando los dos índices coinciden (i == j) todavía falta un viaje."},
           ["Con N = 1 la respuesta es 1.",
            "El bucle debe seguir mientras i ≤ j; si i == j, ese usuario sube solo."])
    prueba("Peso justo el máximo", "trampa", [(20, [10, 10])],
           "Dos usuarios que juntos pesan exactamente P pueden ir juntos.",
           {"wa": "Usas < en vez de ≤: la silla soporta P, así que una pareja de peso P cabe."},
           ["10 + 10 = 20 = P: un viaje.",
            "La condición para ir juntos es suma ≤ P."])
    prueba("Pesos de 10⁹", "borde", [(1000000000, [1000000000, 1000000000])],
           "Dos usuarios de 10⁹ con P = 10⁹: cada uno sube solo.",
           {"wa": "Con los valores máximos algo falla: revisa los tipos (P y los pesos llegan a 10⁹) y la comparación ≤."},
           ["Aquí hacen falta 2 viajes.",
            "La suma de dos pesos llega a 2·10⁹: cabe justo en un int, pero si sumas más cosas usa long long."])
    prueba("El más pesado con el siguiente más pesado no", "trampa", [(5, [1, 2, 3, 4])],
           "Emparejar a los dos más pesados (o a los dos más ligeros) desperdicia sitio.",
           {"wa": "Tu criterio de emparejamiento no es el bueno. Al más pesado le conviene ir con el MÁS LIGERO; si no cabe ni con él, sube solo."},
           ["1 + 4 y 2 + 3: bastan 2 viajes.",
            "Mira el más pesado: ¿cabe con el más ligero?"])
    prueba("El que no cabe es el pesado", "trampa", [(10, [2, 3, 9])],
           "Si el más ligero y el más pesado no caben juntos, el que sube solo es el pesado.",
           {"wa": "Cuando no caben juntos mandas solo al ligero. Es el pesado el que no cabe con nadie."},
           ["9 sube solo; 2 y 3 van juntos: 2 viajes.",
            "Si ligero + pesado > P, el pesado sube solo (j--) y el ligero sigue esperando pareja."])
    prueba("Nadie puede ir acompañado", "borde", [(40, [30, 30, 30]), (1, [1, 1, 1, 1])],
           "Todos tienen que subir solos (incluido P = 1 con pesos 1).",
           {"wa": "Si ninguna pareja cabe, salen N viajes: no supongas que siempre basta con N / 2 redondeado."},
           ["Con P = 1 y pesos 1, 1 + 1 > 1.",
            "Cada iteración del bucle es un viaje, con uno o con dos usuarios."])
    prueba("Usuarios desordenados", "trampa", [(10, [9, 1, 8, 2])],
           "Los pesos no vienen ordenados en la entrada.",
           {"wa": "Parece que no ordenas los pesos antes de emparejar."},
           ["La entrada no está ordenada.",
            "Ordena el vector antes de usar los dos índices."])
    prueba("Todos caben de dos en dos (número impar)", "trampa", [(2, [1, 1, 1, 1, 1])],
           "Cinco usuarios que caben por parejas: 3 viajes (el último va solo).",
           {"wa": "Con un número impar el último sube solo: revisa la condición del bucle cuando i == j."},
           ["Salen 3 viajes.",
            "Cuando solo queda uno (i == j), cuenta su viaje sin emparejarlo consigo mismo."])
    prueba("Cada pesado con un ligero", "trampa", [(10, [9, 1, 9, 1])],
           "Dos pesados y dos ligeros: cada pesado debe llevarse un ligero (2 viajes).",
           {"wa": "Juntas a los dos ligeros y dejas solos a los pesados. Al más pesado le toca el más ligero."},
           ["9 + 1 y 9 + 1: 2 viajes.",
            "Empieza siempre por el más pesado que queda y búscale el más ligero."])
    prueba("Pesos grandes que sí caben", "borde", [(1000000000, [500000000, 500000000, 999999999, 1])],
           "Pesos cerca de 10⁹ que caben por parejas justas.",
           {"wa": "Con pesos grandes algo falla: revisa el tipo de la suma y la comparación ≤."},
           ["Salen 2 viajes: 5·10⁸ + 5·10⁸ y 999999999 + 1.",
            "Usa long long para P y para las sumas."])
    prueba("Varios casos seguidos", "trampa",
           [(10, [5, 5, 5, 5, 5, 5]), (3, [3]), (7, [1, 6, 6]), (100, [50, 51])],
           "Varios casos seguidos: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: el contador de viajes o el vector no se reinician."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara el vector y el contador dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(rng, rng.randint(1, 9), rng.choice([1, 5, 20, 1000000000])) for _ in range(200)],
           "200 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Ordena sus pesos en papel y sigue los dos índices."])
    prueba("Aleatorios medianos con pesos grandes", "aleatorio",
           [aleatorio(rng, rng.randint(1000, 5000), rng.choice([100, 1000000000])) for _ in range(10)],
           "10 casos medianos, varios con pesos cerca de 10⁹.",
           {"wa": "Algo falla con más usuarios o con pesos grandes: revisa el tipo de la suma y el movimiento de los índices."},
           ["Reduce el caso que falla quitando usuarios mientras siga fallando.",
            "Si los pesos son grandes, la suma necesita long long."])
    prueba("500.000 usuarios", "rendimiento", [aleatorio(rng, 500000, 9999)],
           "El tamaño máximo de un caso: mide la eficiencia.",
           {"tle": "Tu solución es lenta para 500.000 usuarios: debe ser O(N log N). ¿Buscas pareja para cada uno recorriendo a los demás?"},
           ["Ordenar cuesta O(N log N); emparejar con dos índices es una sola pasada.",
            "Usa sort de la biblioteca, no una ordenación cuadrática.",
            "No borres elementos del medio de un vector: cuesta O(N) cada vez."])
    return [Prueba(nombre, tipo, entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(f"{resuelve(*c)}\n" for c in casos), casos=len(casos),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("no cuenta al último que va solo", [("while (i <= j)", "while (i < j)")], prueba=2, v="wa"),
    Variante("exige peso < P", [("peso[i] + peso[j] <= P", "peso[i] + peso[j] < P")], prueba=3, v="wa"),
    Variante("junta a los dos más pesados",
             [("if (i < j && peso[i] + peso[j] <= P) ++i;", "if (i < j && peso[j - 1] + peso[j] <= P) --j;")], prueba=5, v="wa"),
    Variante("si no caben, sube solo el ligero",
             [("if (i < j && peso[i] + peso[j] <= P) ++i;   // el mas ligero sube con el mas pesado\n        --j;",
               "if (i < j && peso[i] + peso[j] <= P) { ++i; --j; }\n        else ++i;")], prueba=6, v="wa"),
    Variante("no ordena", [("sort(peso.begin(), peso.end());", "")], prueba=8, v="wa"),
    Variante("no reinicia entre casos", [("int viajes = 0;", "static int viajes = 0;")], prueba=12, v="wa"),
    Variante("ordenación cuadrática",
             [("sort(peso.begin(), peso.end());",
               "for (int a = 1; a < N; ++a) for (int b = a; b > 0 && peso[b] < peso[b - 1]; --b) swap(peso[b], peso[b - 1]);")],
             prueba=15, v="tle"),
]
