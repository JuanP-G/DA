"""02-L · Cinemáticas digitales: juez con pruebas pensadas para cada error típico.

Formato: casos hasta fin de fichero; cada uno «R S» (1 ≤ R ≤ 2·10⁶ escenas, 1 ≤ S ≤ 10⁵ estaciones)
y R pares «minuto duración» con los minutos en orden no decreciente (el ejemplo pone un par por
línea). Salida: por caso, el máximo tiempo que una escena espera en cola antes de empezar.

El enunciado no acota los minutos ni las duraciones: las pruebas usan minutos ≥ 0 y duraciones
≥ 1 que caben en int (hasta 10⁹), pero los instantes de fin acumulados pueden pasar de 2³¹.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-L/EJ_02-L.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["long long inicio = max(libre, minuto);", "long long inicio = libre;"],
}

MAXS = 100_000


def espera_maxima(S, escenas):
    """Cada escena, en orden, a la estación que antes queda libre; empieza en max(libre, envío)."""
    h = [0] * min(S, len(escenas))      # las estaciones que nunca se usan no importan
    peor = 0
    for m, t in escenas:
        libre = heapq.heappop(h)
        inicio = max(libre, m)
        peor = max(peor, inicio - m)
        heapq.heappush(h, inicio + t)
    return peor


def texto_entrada(casos):
    return "".join(f"{len(e)} {S}\n" + "".join(f"{m} {t}\n" for m, t in e) for S, e in casos)


def al_azar(r, R, maxpaso, maxdur, maxdur_raro=None):
    m, out = 0, []
    for _ in range(R):
        m += r.randint(0, maxpaso)
        out.append((m, r.randint(1, maxdur if maxdur_raro is None or r.random() < .9 else maxdur_raro)))
    return out


def pruebas():
    r = random.Random(2000)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(2, [(0, 30), (5, 20), (10, 15), (15, 10)]), (5, [(0, 100), (5, 100), (100, 100)]),
            (2, [(0, 50), (0, 60), (10, 5), (25, 5)]), (2, [(10, 5), (10, 15), (10, 20)])],
           "Los cuatro casos del PDF (la entrada acaba con el fin del fichero).",
           {"wa": "Si fallan hasta los ejemplos, revisa la base: cada escena va a la estación que antes queda libre, empieza en max(libre, minuto de envío) y espera inicio − envío.",
            "pe": "El resultado está bien pero no el formato: un número por línea."},
           ["Haz a mano el primer caso: las esperas son 0, 0, 15 y 15.",
            "No hay número de casos ni centinela: lee «R S» hasta que falle la lectura (plantilla de casos ilimitados)."])
    prueba("La espera no incluye el renderizado", "trampa",
           [(1, [(0, 10)])],
           "Una sola escena con la estación libre: espera 0, aunque tarde 10 minutos en renderizarse.",
           {"wa": "Cuentas como espera también el tiempo de renderizado. La espera es solo lo que pasa en la cola: inicio − minuto de envío, no fin − minuto de envío."},
           ["Si la estación está libre cuando llega la escena, ¿cuánto espera?",
            "Distingue tres instantes: envío, inicio del renderizado y fin.",
            "espera = inicio − minuto; el fin (inicio + duración) solo sirve para saber cuándo vuelve a quedar libre la estación."])
    prueba("Una estación libre no adelanta el reloj", "trampa",
           [(1, [(0, 5), (100, 10), (105, 1)])],
           "La segunda escena llega en 100 con la estación libre desde 5: empieza en 100 (no en 5) y acaba en 110, así que la tercera espera 5.",
           {"wa": "Cuando la estación ya estaba libre, haces empezar la escena en el instante en que se liberó (en el pasado). Una escena no puede empezar antes de enviarse: inicio = max(libre, minuto)."},
           ["La segunda escena no puede empezar en el minuto 5: aún no se ha enviado.",
            "Si empieza en 100 y tarda 10, la estación queda libre en 110, y la tercera (enviada en 105) espera 5.",
            "inicio = max(libre, minuto); y lo que vuelves a meter en la cola es inicio + duración."])
    prueba("La estación que antes queda libre", "trampa",
           [(2, [(0, 10), (0, 100), (5, 1)])],
           "Con las dos estaciones ocupadas, la tercera escena va a la que se libera en 10, no a la que se libera en 100.",
           {"wa": "Mandas la escena a la estación que MÁS TARDE queda libre: tu cola es de máximos. priority_queue<long long> a secas devuelve el mayor; usa greater<long long>."},
           ["La tercera escena espera de 5 a 10: 5 minutos.",
            "¿Qué devuelve top() en una priority_queue por defecto?",
            "priority_queue<long long, vector<long long>, greater<long long>>."])
    prueba("Las escenas se atienden en orden de envío", "trampa",
           [(1, [(0, 10), (1, 100), (2, 1)]), (2, [(0, 5), (0, 50), (1, 50), (1, 1)])],
           "La cola de espera es por orden de envío: una escena corta no adelanta a una larga que se envió antes.",
           {"wa": "Reordenas las escenas (por ejemplo, la más corta primero). El productor quiere el orden predeterminado: cada escena, en el orden de la entrada, va a la estación que antes quede libre."},
           ["En el primer caso la escena de 1 minuto tiene que esperar a que acabe la de 100: espera 109.",
            "La cola de prioridad es de ESTACIONES (cuándo se liberan), no de escenas: las escenas se procesan tal como se leen."])
    prueba("Instantes que no caben en int", "trampa",
           [(1, [(0, 10 ** 9)] * 4)],
           "Cuatro escenas de 10⁹ minutos en una sola estación: la última espera 3·10⁹, y los instantes de fin pasan de 2³¹ − 1.",
           {"wa": "Los instantes de fin se acumulan y no caben en int: la cola, el inicio y la espera máxima tienen que ser long long (aunque cada dato de la entrada quepa en int)."},
           ["La cuarta escena empieza en 3·10⁹; el máximo de un int es 2.147.483.647.",
            "Revisa el tipo de los elementos de la cola y de las variables libre, inicio y la espera máxima.",
            "Usa priority_queue<long long, vector<long long>, greater<long long>> y long long en todo el cálculo."])
    prueba("Llega justo cuando queda libre", "borde",
           [(1, [(0, 5), (5, 5), (10, 5)]), (2, [(0, 3), (0, 4), (3, 1), (4, 2)])],
           "Escenas que llegan exactamente en el minuto en que se libera una estación: no esperan nada.",
           {"wa": "Si una escena llega justo cuando una estación se libera, empieza en ese mismo instante: espera 0. Revisa las comparaciones (< frente a ≤)."},
           ["En el primer caso cada escena llega justo cuando acaba la anterior: la respuesta es 0.",
            "Con inicio = max(libre, minuto) no hace falta ningún caso especial."])
    prueba("Nadie espera", "borde",
           [(5, [(0, 100), (5, 100), (100, 100)]), (3, [(7, 1)]), (MAXS, [(0, 1)] * 20)],
           "Hay estaciones de sobra: la respuesta es 0.",
           {"wa": "Si nadie espera hay que escribir 0: inicializa la espera máxima a 0 (no a −1 ni al primer valor).",
            "rte": "Con más estaciones que escenas te sales de algo: ¿dimensionas algún vector con R en lugar de S?"},
           ["Con más estaciones que escenas, todas empiezan nada más llegar.",
            "La espera máxima empieza en 0 en cada caso."])
    prueba("Todas en el minuto 0", "borde",
           [(3, [(0, 4), (0, 2), (0, 6), (0, 1), (0, 1), (0, 5), (0, 3)]), (1, [(0, 1)] * 6)],
           "Todas las escenas se envían a la vez: se van encadenando según se liberan las estaciones.",
           {"wa": "Con todas las escenas a la vez, cada una espera hasta que se libere la primera estación disponible: revisa que siempre coges la que antes queda libre y que actualizas su instante."},
           ["Con una sola estación y seis escenas de 1 minuto, la última espera 5.",
            "Mete de nuevo en la cola inicio + duración tras asignar cada escena."])
    prueba("Una sola escena y una sola estación", "borde",
           [(1, [(0, 1)]), (1, [(10 ** 9, 10 ** 9)])],
           "El caso mínimo: una escena nunca espera.",
           {"wa": "Con una sola escena la espera es 0."},
           ["¿Cuánto puede esperar la única escena si la estación está libre?",
            "Comprueba que la espera se calcula como inicio − minuto, no como inicio."])
    prueba("Varios casos seguidos", "trampa",
           [(1, [(0, 50), (0, 50), (0, 50)]), (2, [(0, 1), (0, 1)]), (1, [(3, 2), (4, 2)]), (4, [(0, 9)])],
           "Un caso con mucha espera seguido de otros con poca: la espera máxima y la cola empiezan de cero en cada caso.",
           {"wa": "El primer caso sale bien y los siguientes no: la espera máxima o la cola se arrastran del caso anterior (declaradas fuera de resuelveCaso o static).",
            "rte": "Restos del caso anterior: declara la cola dentro de resuelveCaso."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Declara la cola y la espera máxima (a 0) dentro de resuelveCaso."])
    casos = []
    for _ in range(300):
        casos.append((r.randint(1, 4), al_azar(r, r.randint(1, 10), r.choice([0, 3, 10]), r.choice([3, 20]))))
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "300 casos pequeños al azar, con muchos envíos simultáneos.",
           {"wa": "Algún caso concreto falla: la línea que falla es el número de caso; búscalo en la entrada y simúlalo a mano."},
           ["Localiza el caso por el número de línea.",
            "Apunta para cada estación cuándo queda libre y asigna las escenas una a una."])
    casos = []
    for _ in range(20):
        casos.append((r.randint(1, 500), al_azar(r, r.randint(100, 3000), r.choice([1, 50]), 1000, 10 ** 6)))
    prueba("Aleatorios medianos", "aleatorio", casos,
           "20 casos de hasta 3000 escenas, algunas muy largas.",
           {"wa": "Con casos medianos falla algo que con los pequeños no: revisa los tipos (long long) y el max(libre, minuto).",
            "tle": "Ya con casos medianos va lento: ¿buscas la estación libre recorriéndolas todas?"},
           ["Comprueba que cada escena hace un pop y un push.",
            "Revisa que los instantes se guardan en long long."])
    prueba("Grande: 100.000 estaciones y 150.000 escenas", "rendimiento",
           [(MAXS, al_azar(r, 150000, 1, 199999))],
           "Muchas estaciones y muchas escenas: mide la eficiencia (debe ser O((S + R) log S)).",
           {"tle": "Buscar la estación que antes queda libre recorriendo las S estaciones cuesta O(R·S) ≈ 10¹⁰: usa una cola de prioridad de mínimos.",
            "wa": "Con muchos datos falla algo: revisa los tipos y el max(libre, minuto)."},
           ["¿Cuánto cuesta asignar cada escena? Hay 150.000 y 100.000 estaciones.",
            "Con una cola de mínimos de instantes de liberación, cada escena es un pop y un push."])
    prueba("Grande: 200.000 escenas en 3 estaciones", "rendimiento",
           [(3, al_azar(r, 200000, 2, 9))],
           "Muchas escenas y pocas estaciones: la cola de espera crece sin parar.",
           {"tle": "Algo cuesta más de la cuenta por escena: ¿simulas el reloj minuto a minuto?",
            "wa": "Con mucha espera acumulada los números crecen: revisa los tipos."},
           ["No avances el tiempo de uno en uno: salta al instante en que se libera la estación.",
            "Cada escena: pop, calcular inicio y espera, push."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida="".join(f"{espera_maxima(S, e)}\n" for S, e in c),
                   casos=len(c), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


COLA = "priority_queue<long long, vector<long long>, greater<long long>> cola;"

VARIANTES = [
    Variante("cuenta el renderizado como espera", [("maxT = max(maxT, inicio - minuto);", "maxT = max(maxT, inicio + tiempo - minuto);")],
             prueba=2, v="wa"),
    Variante("empieza cuando se libera la estación aunque la escena no haya llegado",
             [("long long inicio = max(libre, minuto);", "long long inicio = libre;")], prueba=3, v="wa"),
    Variante("cola de máximos", [(COLA, "priority_queue<long long> cola;")], prueba=4, v="wa"),
    Variante("cola de int (los instantes desbordan)", [(COLA, "priority_queue<int, vector<int>, greater<int>> cola;")],
             prueba=6, v="wa"),
    Variante("no reinicia la espera máxima entre casos", [("long long maxT = 0;", "static long long maxT = 0;")],
             prueba=11, v="wa"),
    Variante("formato: todo en una línea", [("cout << maxT << '\\n';", "cout << maxT << ' ';")], prueba=1, v="pe"),
    Variante("busca la estación libre recorriéndolas todas (O(R·S))",
             [(COLA + "\n    for (int i = 0; i < estaciones; ++i)\n        cola.push(0);",
               "vector<long long> est(estaciones, 0);"),
              ("        long long libre = cola.top(); cola.pop();",
               "        int k = 0;\n        for (int j = 1; j < estaciones; ++j) if (est[j] < est[k]) k = j;\n        long long libre = est[k];"),
              ("        cola.push(inicio + tiempo);", "        est[k] = inicio + tiempo;")],
             prueba=14, v="tle"),
]
