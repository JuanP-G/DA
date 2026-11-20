"""08-2 · ¡Nos invaden!: juez con pruebas pensadas para cada error típico.

El solucionador (para cada equipo, de menor a mayor, la ciudad más fácil que aún no se ha ganado si
puede con ella) se ha validado contra fuerza bruta (todas las permutaciones de equipos) en miles de
casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "8-Algoritmos voraces/EJ_08-2/EJ_08-2.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["if (equipos[j] >= enemigos[i]) {", "if (equipos[j] > enemigos[i]) {"],
}


def victorias(enemigos, equipos):
    ciudades = sorted(enemigos)
    i = 0
    for e in sorted(equipos):
        if i < len(ciudades) and e >= ciudades[i]:
            i += 1
    return i


def caso_a_texto(c):
    a, b = c
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"


def al_azar(rng, n, tope):
    return ([rng.randint(1, tope) for _ in range(n)], [rng.randint(1, tope) for _ in range(n)])


def pruebas():
    rng = random.Random(802)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{victorias(*c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [([40, 20, 80, 30], [25, 50, 35, 40]), ([40, 50, 60, 70], [99, 25, 30, 50])],
           "Los dos casos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: ordenar ciudades y equipos y dar a cada ciudad, de la más fácil a la más difícil, el equipo más pequeño que la gane.",
            "pe": "Los números están bien pero el formato no: un número por línea, uno por caso."},
           ["Sigue a mano el primer caso con los dos vectores ordenados: 20 30 40 80 y 25 35 40 50.",
            "La primera línea del caso es N; luego vienen los N enemigos y después los N equipos.",
            "Con dos índices: si el equipo j gana a la ciudad i, victoria y avanzan los dos; si no, solo avanza j."])

    # ------------------------------------------------------------------ borde
    prueba("Ninguna victoria posible", "borde", [([50, 60, 70], [10, 20, 49])],
           "Todos los equipos son más pequeños que la ciudad más fácil: 0 victorias.",
           {"wa": "Si no puedes ganar en ninguna ciudad, la respuesta es 0. ¿Cuentas alguna victoria sin comprobar que el equipo gana?"},
           ["¿Hay algún equipo con al menos 50 efectivos?",
            "Solo cuenta una victoria cuando equipo ≥ enemigo."])
    prueba("Valores en los extremos (1 y 10⁶)", "borde", [([1, 1000000, 1000000], [1000000, 1, 999999])],
           "Efectivos de 1 y de 1.000.000: el 1 gana al 1 y el 10⁶ a uno de los 10⁶ (2 victorias).",
           {"wa": "Con los valores extremos algo falla: revisa la comparación (≥) y que lees todos los valores."},
           ["El equipo de 999.999 no puede con 10⁶.",
            "Ordena los dos vectores y compáralos con ≥."])

    # ------------------------------------------------------------------ trampas
    prueba("Empate: tantos efectivos como el enemigo", "trampa", [([5], [5])],
           "Una ciudad con 5 enemigos y un equipo de 5: la victoria está garantizada (1).",
           {"wa": "Sale 0: usas > en lugar de ≥. Basta con tener TANTOS efectivos como el enemigo."},
           ["Relee el enunciado: «al menos tantos efectivos de defensa como el enemigo».",
            "La condición de victoria es equipo ≥ enemigo."])
    prueba("Ciudades desordenadas", "trampa", [([9, 1], [1, 9])],
           "Enemigos 9 1 y equipos 1 9 (ya ordenados): 2 victorias. Hay que ordenar también las ciudades.",
           {"wa": "Sale 1: no ordenas las ciudades. El recorrido con dos índices solo funciona si los DOS vectores están ordenados."},
           ["¿Qué pasa si recorres las ciudades en el orden de la entrada?",
            "Ordena el vector de enemigos además del de equipos."])
    prueba("Equipos desordenados", "trampa", [([1, 9], [9, 1])],
           "Enemigos 1 9 (ya ordenados) y equipos 9 1: 2 victorias. Hay que ordenar los equipos de menor a mayor.",
           {"wa": "Sale 1: no ordenas los equipos (o los ordenas de mayor a menor) y gastas el equipo grande en la ciudad fácil."},
           ["El equipo de 9 debe ir a la ciudad de 9; el de 1, a la de 1.",
            "Ordena los equipos de MENOR a MAYOR, igual que las ciudades."])
    prueba("Un equipo que no gana a la más fácil no sirve", "trampa", [([2, 3], [1, 3])],
           "Enemigos 2 3 y equipos 1 3: el equipo de 1 no gana en ninguna parte, pero el de 3 sí (1 victoria).",
           {"wa": "Sale 0: cuando un equipo pierde contra la ciudad más fácil, descartas la CIUDAD. Hay que descartar el EQUIPO (si no gana a la más fácil, no gana a ninguna)."},
           ["Si el equipo de 1 no gana a la ciudad de 2, ¿puede ganar a la de 3?",
            "Cuando equipo[j] < enemigo[i], avanza j (el equipo no sirve), no i.",
            "La ciudad i solo avanza cuando la ganas."])
    prueba("Emparejar posición a posición no basta", "trampa", [([2, 3, 9], [1, 2, 3])],
           "Enemigos 2 3 9 y equipos 1 2 3: el 2 gana al 2 y el 3 al 3 (2 victorias), aunque al emparejar por posiciones no gane ninguno.",
           {"wa": "Sale 0: comparas equipo[i] con enemigo[i] tras ordenar. Los equipos pequeños que no sirven hay que saltarlos para que los demás se desplacen."},
           ["Tras ordenar, el equipo 1 no gana a nadie; el 2 debería ir a la ciudad de 2.",
            "Usa dos índices distintos: uno para la ciudad más fácil sin ganar y otro para el equipo."])
    prueba("No gastar el equipo grande en la ciudad fácil", "trampa", [([1, 10], [2, 10])],
           "Enemigos 1 10 y equipos 2 10: el 2 a la ciudad de 1 y el 10 a la de 10 (2 victorias).",
           {"wa": "Sale 1: usas el equipo más grande para la ciudad más fácil. Para cada ciudad hay que usar el equipo MÁS PEQUEÑO que la gane."},
           ["Si el equipo de 10 va a la ciudad de 1, ¿quién defiende la de 10?",
            "Para la ciudad más fácil, elige el equipo más pequeño que gane allí."])
    prueba("Ciudades y equipos repetidos", "trampa", [([5, 5, 5, 3], [5, 4, 5, 2])],
           "Enemigos 5 5 5 3 y equipos 5 4 5 2: el 4 gana al 3 y los dos de 5 a dos ciudades de 5 (3 victorias).",
           {"wa": "Con valores repetidos falla: cada equipo solo puede usarse una vez y cada ciudad solo se gana una vez. Revisa que avanzas los dos índices tras una victoria."},
           ["Cuenta a mano: ¿cuántas ciudades de 5 pueden defender dos equipos de 5?",
            "Tras una victoria avanzan la ciudad y el equipo; tras una derrota, solo el equipo."])
    prueba("Varios casos seguidos", "trampa",
           [([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), ([100], [1]), ([7, 7], [7, 7]), ([2, 3], [1, 3])],
           "Varios casos con tamaños distintos: nada del caso anterior debe quedar.",
           {"wa": "El primer caso sale bien y los siguientes no: el contador de victorias o los vectores no se reinician en cada caso.",
            "rte": "Un vector de un caso anterior con otro tamaño: créalos dentro de resuelveCaso."},
           ["Mira qué variables están fuera de la función de cada caso.",
            "Declara los vectores y el contador dentro de resuelveCaso (sin static)."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 7), rng.choice([5, 10, 30])) for _ in range(200)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 casos de hasta 7 ciudades, con muchos empates.",
           {"wa": "Algún caso falla: localiza la línea, busca el caso y prueba a mano con los dos vectores ordenados."},
           ["La línea que falla es el número de caso.",
            "Comprueba los empates (≥) y qué índice avanzas cuando el equipo pierde."])
    casos = [al_azar(rng, rng.randint(100, 3000), rng.choice([100, 10 ** 4, 10 ** 6])) for _ in range(30)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "30 casos de 100 a 3.000 ciudades.",
           {"wa": "Algún caso mediano falla: prueba primero los pequeños al azar, que son más fáciles de seguir."},
           ["Compara con un caso pequeño parecido.",
            "Revisa que ordenas los dos vectores de menor a mayor."])

    # ------------------------------------------------------------------ rendimiento
    prueba("300.000 ciudades con valores pequeños", "rendimiento", [al_azar(rng, 300000, 99)],
           "El tamaño máximo (N = 300.000): la solución debe ser O(N log N).",
           {"tle": "Algo cuesta O(N²): ¿buscas para cada ciudad el mejor equipo recorriendo todos los equipos (y marcando los usados)?"},
           ["Con N = 300.000, O(N²) son 9·10¹⁰ operaciones: demasiado.",
            "Ordenar cuesta O(N log N) y después basta un recorrido con dos índices.",
            "Si prefieres buscar, usa un multiset con lower_bound, nunca un recorrido lineal por ciudad."])
    prueba("100.000 ciudades con valores grandes", "rendimiento", [al_azar(rng, 100000, 10 ** 6)],
           "Un caso grande con efectivos hasta 10⁶.",
           {"tle": "Debe ser O(N log N): ordenar y un recorrido con dos índices.",
            "wa": "En el caso grande falla: revisa qué índice avanzas cuando un equipo pierde."},
           ["Ordena los dos vectores con sort.",
            "Un solo recorrido con dos índices basta."])
    return P


VARIANTES = [
    Variante("> en lugar de ≥", [("if (equipos[j] >= enemigos[i]) {", "if (equipos[j] > enemigos[i]) {")], prueba=4, v="wa"),
    Variante("no ordena las ciudades", [("sort(enemigos.begin(), enemigos.end());", "")], prueba=5, v="wa"),
    Variante("no ordena los equipos", [("sort(equipos.begin(), equipos.end());", "")], prueba=6, v="wa"),
    Variante("equipos de mayor a menor", [("sort(equipos.begin(), equipos.end());", "sort(equipos.rbegin(), equipos.rend());")], prueba=[5, 6], v="wa"),
    Variante("descarta la ciudad cuando el equipo pierde",
             [("for (int j = 0; j < N && i < N; ++j) {\n        if (equipos[j] >= enemigos[i]) {\n            ++victorias;\n            ++i;\n        }\n    }",
               "int j = 0;\n    for (; i < N && j < N; ++i) {\n        if (equipos[j] >= enemigos[i]) {\n            ++victorias;\n            ++j;\n        }\n    }")],
             prueba=7, v="wa"),
    Variante("empareja posición a posición",
             [("if (equipos[j] >= enemigos[i]) {", "if (equipos[j] >= enemigos[j]) {")], prueba=8, v="wa"),
    Variante("contador sin reiniciar", [("int victorias = 0, i = 0;", "static int victorias = 0; int i = 0;")], prueba=11, v="wa"),
    Variante("busca el mejor equipo para cada ciudad (O(N²))",
             [("int victorias = 0, i = 0;          // i = ciudad mas facil aun sin defender\n    for (int j = 0; j < N && i < N; ++j) {\n        if (equipos[j] >= enemigos[i]) {\n            ++victorias;\n            ++i;\n        }\n    }",
               "int victorias = 0;\n    vector<bool> usado(N, false);\n    for (int i = 0; i < N; ++i)\n        for (int j = 0; j < N; ++j)\n            if (!usado[j] && equipos[j] >= enemigos[i]) { usado[j] = true; ++victorias; break; }")],
             prueba=14, v="tle"),
    Variante("salida separada por espacios", [("cout << victorias << '\\n';", "cout << victorias << ' ';")], prueba=1, v="pe"),
]
