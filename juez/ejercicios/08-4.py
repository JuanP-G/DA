"""08-4 · Maratón de cine de terror: juez con pruebas pensadas para cada error típico.

El solucionador (selección de actividades por hora de fin, con 10 minutos de descanso) se ha
validado contra fuerza bruta (todos los subconjuntos de películas) en miles de casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "8-Algoritmos voraces/EJ_08-4/EJ_08-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["return a.fin < b.fin;", "return a.inicio < b.inicio;"],
}

DESCANSO = 10


def minutos(d, hhmm):
    hh, mm = map(int, hhmm.split(":"))
    return (d * 24 + hh) * 60 + mm


def maximo(pelis):
    iv = sorted(((minutos(d, h) + dur, minutos(d, h)) for d, h, dur in pelis))
    n, libre = 0, None
    for fin, ini in iv:
        if libre is None or ini >= libre:
            n += 1
            libre = fin + DESCANSO
    return n


def caso_a_texto(pelis):
    return f"{len(pelis)}\n" + "".join(f"{d} {h} {dur}\n" for d, h, dur in pelis)


def hora(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def al_azar(rng, n, dias, durmax):
    return [(rng.randint(1, dias), hora(rng.randrange(1440)), rng.randint(1, durmax)) for _ in range(n)]


def pruebas():
    rng = random.Random(804)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(f"{maximo(c)}\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [[(1, "09:30", 90), (1, "12:00", 80), (1, "16:00", 120), (1, "17:30", 100)],
            [(1, "10:30", 90), (1, "16:00", 110), (1, "12:00", 70)],
            [(1, "23:30", 90), (2, "01:10", 70)]],
           "Los tres casos del PDF: solapes, una película que empieza justo al acabar otra y otra que pasa de un día al siguiente.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: pasar cada película a minutos absolutos, ordenarlas por hora de FIN e ir cogiendo las compatibles con la última elegida.",
            "pe": "Los números están bien pero el formato no: un número por línea, uno por caso."},
           ["Sigue a mano el segundo caso: la de las 10:30 acaba a las 12:00 y la de las 12:00 no deja 10 minutos.",
            "Lee la hora como dos enteros separados por «:» (por ejemplo, cin >> hh >> c >> mm con un char c).",
            "inicio = (D·24 + HH)·60 + MM, fin = inicio + duración, y una película es compatible si inicio ≥ fin anterior + 10."])

    # ------------------------------------------------------------------ borde
    prueba("Una sola película", "borde", [[(5, "20:00", 100)]],
           "N = 1: siempre se puede ver (1).",
           {"wa": "Con una sola película la respuesta es 1: revisa cómo inicializas «libre desde» para que la primera siempre se pueda ver."},
           ["¿Qué escribe tu programa con una única película?",
            "Inicializa el instante en que Deborah queda libre a un valor menor que cualquier comienzo."])
    prueba("Tres pases a la vez", "borde", [[(1, "18:00", 90), (1, "18:00", 90), (1, "18:00", 90)]],
           "Tres películas que empiezan y acaban a la vez: solo se puede ver una.",
           {"wa": "Películas que coinciden en el tiempo no se pueden ver juntas: ¿compruebas el solape con la última película ELEGIDA?"},
           ["Si la primera acaba a las 19:30, ¿puede empezar otra a las 18:00?",
            "Compara cada película con el final de la última que has elegido (más 10 minutos)."])

    # ------------------------------------------------------------------ trampas
    prueba("Exactamente 10 minutos de descanso", "trampa", [[(1, "10:00", 40), (1, "10:50", 60)]],
           "La primera acaba a las 10:40 y la segunda empieza a las 10:50: con 10 minutos justos se pueden ver las dos (2).",
           {"wa": "Sale 1: exiges más de 10 minutos. Con 10 minutos JUSTOS ya puede (como en el tercer ejemplo): la condición es inicio ≥ fin + 10, no >."},
           ["Relee el tercer ejemplo: acaba a la 1:00 y la siguiente empieza a la 1:10, y puede ver las dos.",
            "Usa ≥ al comparar con el final anterior más 10."])
    prueba("9 minutos no bastan", "trampa", [[(1, "10:00", 50), (1, "10:59", 30)]],
           "La primera acaba a las 10:50 y la segunda empieza a las 10:59: solo hay 9 minutos, así que solo una (1).",
           {"wa": "Sale 2: no tienes en cuenta los 10 minutos de descanso (o cuentas menos). Una película solo vale si empieza al menos 10 minutos después de que acabe la anterior."},
           ["¿Cuántos minutos hay entre las 10:50 y las 10:59?",
            "Suma 10 al final de cada película elegida antes de compararla con el comienzo de la siguiente."])
    prueba("El mismo horario en días distintos", "trampa", [[(1, "10:00", 50), (2, "10:00", 60)]],
           "Dos películas a las 10:00, una el día 1 y otra el día 2: no se solapan (2).",
           {"wa": "Sale 1: no usas el día. El instante de comienzo es (D·24 + HH)·60 + MM: sin el día, películas de días distintos parecen solaparse."},
           ["¿Coinciden de verdad dos películas a la misma hora en días diferentes?",
            "Pasa todo a minutos desde el principio: inicio = (D·24 + HH)·60 + MM."])
    prueba("Una hora tiene 60 minutos", "trampa", [[(1, "09:30", 40), (1, "10:15", 30)]],
           "La primera acaba a las 10:10 y la segunda empieza a las 10:15 (solo 5 minutos): solo una (1).",
           {"wa": "Sale 2: conviertes la hora como HH·100 + MM. Entonces 9:30 + 40 = «9:70», que no es una hora: hay que usar HH·60 + MM."},
           ["¿Cuánto es 9:30 más 40 minutos?",
            "Pasa la hora a minutos: HH·60 + MM (y el día, ·24·60)."])
    prueba("Una película que acaba pasada la medianoche", "trampa", [[(1, "23:00", 120), (2, "00:30", 60)]],
           "La de las 23:00 del día 1 acaba a la 1:00 del día 2, y la del día 2 a las 0:30 empieza antes: solo una (1).",
           {"wa": "Sale 2: el final de una película no puede quedarse dentro de su día. Si sumas la duración en minutos absolutos, el cambio de día sale solo."},
           ["¿A qué hora acaba la película de las 23:00 que dura 120 minutos?",
            "No hagas «módulo 24 horas» con el final: trabaja siempre con minutos absolutos."])
    prueba("Ordenar por hora de comienzo no sirve", "trampa",
           [[(1, "10:00", 600), (1, "11:00", 30), (1, "12:00", 40)]],
           "Una película larguísima que empieza la primera tapa a otras dos cortas: lo mejor es ver las dos cortas (2).",
           {"wa": "Sale 1: ordenas por hora de COMIENZO. Elegir la que empieza antes puede ocupar todo el día; hay que ordenar por hora de FIN."},
           ["Si eliges la de las 10:00 (dura 10 horas), ¿qué te queda?",
            "El criterio voraz correcto es: la que ACABA antes.",
            "Ordena las películas por fin (inicio + duración)."])
    prueba("La más corta no siempre es la mejor", "trampa",
           [[(1, "10:00", 100), (1, "12:00", 100), (1, "11:30", 40)]],
           "Una película corta en medio que se solapa con dos largas: lo mejor es ver las dos largas (2).",
           {"wa": "Sale 1: eliges primero las más cortas. La corta de las 11:30 impide ver las otras dos; el criterio correcto es la que acaba antes."},
           ["Si coges la de 40 minutos, ¿puedes ver alguna de las otras?",
            "Ordena por hora de fin, no por duración."])
    prueba("Películas que duran días", "trampa",
           [[(1, "00:00", 1000000), (600, "12:00", 10), (700, "00:00", 10), (695, "10:50", 5)]],
           "Una película de 10⁶ minutos (unos 694 días) y otras cortas: las tres cortas se pueden ver; la larga no compensa (3).",
           {"wa": "Con duraciones enormes falla: revisa que el fin es inicio + duración en minutos absolutos y que el tipo aguanta (≈ 1,5·10⁸ cabe en int)."},
           ["La película de 10⁶ minutos acaba el día 695 a las 10:40.",
            "Ordena por fin: las tres cortas acaban antes que la larga."])
    prueba("Horas con ceros a la izquierda", "trampa",
           [[(1, "00:05", 5), (1, "00:20", 1), (1, "08:09", 1), (1, "08:30", 9)]],
           "Horas como 00:05 y 08:09: hay que leerlas bien (4 películas).",
           {"wa": "Las horas con ceros a la izquierda se leen mal: no uses scanf con %i (lee «08» en octal) ni tomes solo un carácter.",
            "rte": "La lectura de la hora falla: lee HH, el carácter «:» y MM por separado."},
           ["Prueba a leer «08:09» y escribe lo que obtienes.",
            "Lee con cin >> hh >> dosPuntos >> mm (dosPuntos de tipo char)."])
    prueba("Varios casos seguidos", "trampa",
           [[(90000, "10:00", 30), (90000, "11:00", 30)], [(1, "10:00", 30)], [(1, "10:00", 50), (1, "11:00", 50)],
            [(2, "10:00", 30), (2, "10:00", 30)]],
           "Un caso en días muy altos seguido de otros en los primeros días: nada del caso anterior debe quedar.",
           {"wa": "El primer caso sale bien y los siguientes no: el contador o el instante «libre desde» no se reinician en cada caso."},
           ["Si «libre desde» es global, en el segundo caso ninguna película parece compatible.",
            "Declara el contador y el instante «libre desde» dentro de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 8), rng.randint(1, 2), rng.choice([60, 300, 1500])) for _ in range(200)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 casos de hasta 8 películas en uno o dos días.",
           {"wa": "Algún caso falla: localiza la línea, busca el caso y dibuja las películas en una línea de tiempo."},
           ["La línea que falla es el número de caso.",
            "Revisa el criterio de ordenación (fin) y la condición inicio ≥ fin + 10."])
    casos = [al_azar(rng, rng.randint(100, 2000), rng.choice([1, 10, 100000]), rng.choice([100, 2000, 1000000])) for _ in range(20)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "20 casos de 100 a 2.000 películas con días y duraciones muy variados.",
           {"wa": "Algún caso mediano falla: suele ser el cambio de día o una duración muy grande."},
           ["Comprueba que el día entra en la cuenta del inicio.",
            "Usa minutos absolutos para todo."])

    # ------------------------------------------------------------------ rendimiento
    pelis = [(100000 - i // 2, hora(600 - (i % 2) * 300), 9) for i in range(100000)]
    prueba("100.000 películas en orden inverso", "rendimiento", [pelis],
           "Muchas películas dadas de la última a la primera: la ordenación debe ser O(N log N).",
           {"tle": "Algo cuesta O(N²): una ordenación por inserción o burbuja, o comparar cada película con todas las demás."},
           ["Con 100.000 películas, O(N²) son 10¹⁰ operaciones.",
            "Usa sort de la biblioteca con un comparador por hora de fin.",
            "Después basta un único recorrido."])
    prueba("100.000 películas al azar", "rendimiento", [al_azar(rng, 100000, 100000, 1000)],
           "Un caso grande con días hasta 100.000.",
           {"tle": "Debe ser O(N log N): ordenar una vez y un recorrido.",
            "wa": "En el caso grande falla: revisa el día en la cuenta del inicio y el tipo de los minutos."},
           ["Ordena una sola vez por fin.",
            "Un solo recorrido con el instante «libre desde»."])
    return P


VARIANTES = [
    Variante("más de 10 minutos (>)", [("if (p.inicio >= libreDesde) {", "if (p.inicio > libreDesde) {")], prueba=4, v="wa"),
    Variante("sin descanso", [("const int DESCANSO = 10;", "const int DESCANSO = 0;")], prueba=5, v="wa"),
    Variante("no usa el día", [("p.inicio = (dia * 24 + hh) * 60 + mm;", "p.inicio = hh * 60 + mm;")], prueba=6, v="wa"),
    Variante("horas como HH·100 + MM", [("p.inicio = (dia * 24 + hh) * 60 + mm;", "p.inicio = dia * 2400 + hh * 100 + mm;")], prueba=7, v="wa"),
    Variante("ordena por comienzo", [("return a.fin < b.fin;", "return a.inicio < b.inicio;")], prueba=9, v="wa"),
    Variante("ordena por duración", [("return a.fin < b.fin;", "return a.fin - a.inicio < b.fin - b.inicio;")], prueba=10, v="wa"),
    Variante("contador sin reiniciar", [("int vistas = 0;", "static int vistas = 0;")], prueba=13, v="wa"),
    Variante("«libre desde» sin reiniciar", [("long long libreDesde = -DESCANSO;", "static long long libreDesde = -DESCANSO;")], prueba=13, v="wa"),
    Variante("ordenación por inserción (O(N²))",
             [("sort(pelis.begin(), pelis.end(), [](Peli const& a, Peli const& b) { return a.fin < b.fin; });",
               "for (int i = 1; i < N; ++i)\n        for (int k = i; k > 0 && pelis[k].fin < pelis[k - 1].fin; --k) swap(pelis[k], pelis[k - 1]);")],
             prueba=16, v="tle"),
    Variante("salida separada por espacios", [("cout << vistas << '\\n';", "cout << vistas << ' ';")], prueba=1, v="pe"),
]
