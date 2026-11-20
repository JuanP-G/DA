"""03-L · La batalla por las audiencias: juez con pruebas pensadas para cada error típico."""
import heapq
import random
from collections import Counter
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-L/EJ_03-L.cpp",
    "cabeceras": ["3-Colas de prioridad variable (Heapsort)/EJ_03-L/IndexPQ.h"],
    "limite_ms": 3000,
    "fallo": ["tiempos[pq.top().prioridad.canal - 1].audiencia += duracion - tiempoAnterior;", ""],
}


def audiencias(D, inicial, cambios):
    """Solucionador independiente: montículo de máximos con borrado perezoso (versión por canal).
    inicial: audiencias de los canales 1..C · cambios: [(m, [(canal, audiencia), ...]), ...]."""
    aud = [None] + list(inicial)
    ver = [0] * len(aud)
    monti = [(-a, c, 0) for c, a in enumerate(aud) if c]
    heapq.heapify(monti)

    def lider():
        while ver[monti[0][1]] != monti[0][2]:
            heapq.heappop(monti)
        return monti[0][1]

    minutos = Counter()
    antes = 0
    for m, pares in cambios:
        minutos[lider()] += m - antes
        for c, a in pares:
            aud[c] = a
            ver[c] += 1
            heapq.heappush(monti, (-a, c, ver[c]))
        antes = m
    minutos[lider()] += D - antes
    orden = sorted(((c, t) for c, t in minutos.items() if t > 0), key=lambda x: (-x[1], x[0]))
    return [f"{c} {t}" for c, t in orden] + ["---"]


def caso_a_texto(c):
    D, inicial, cambios = c
    s = f"{D} {len(inicial)} {len(cambios)}\n" + " ".join(map(str, inicial)) + "\n"
    for m, pares in cambios:
        s += f"{m} {len(pares)} " + " ".join(f"{a} {b}" for a, b in pares) + "\n"
    return s


def max_unico(cnt, monti, aud):
    while aud[monti[0][1]] != -monti[0][0]:
        heapq.heappop(monti)
    return cnt[-monti[0][0]] == 1


def aleatorio(r, C, N, maxA, D, maxU=3, salto=None):
    """Caso válido: audiencias distintas de la anterior, minutos crecientes < D y nunca empate en el máximo."""
    N = min(N, D - 1)
    while True:
        inicial = [r.randint(0, maxA) for _ in range(C)]
        cnt = Counter(inicial)
        if cnt[max(inicial)] == 1:
            break
    aud = [None] + inicial
    monti = [(-a, c) for c, a in enumerate(aud) if c]
    heapq.heapify(monti)
    if salto is None:
        minutos = sorted(r.sample(range(1, D), N))
    else:
        minutos, m = [], 0
        for _ in range(N):
            m += r.randint(1, salto)
            minutos.append(m)
    cambios = []
    for m in minutos:
        while True:
            canales = r.sample(range(1, C + 1), r.randint(1, min(maxU, C)))
            viejos = [(c, aud[c]) for c in canales]
            pares = []
            for c in canales:
                a = r.randint(0, maxA)
                while a == aud[c]:
                    a = r.randint(0, maxA)
                pares.append((c, a))
            for c, a in pares:
                cnt[aud[c]] -= 1
                aud[c] = a
                cnt[a] += 1
                heapq.heappush(monti, (-a, c))
            if max_unico(cnt, monti, aud):
                break
            for c, a in viejos:                     # deshacer y probar otros valores
                cnt[aud[c]] -= 1
                aud[c] = a
                cnt[a] += 1
                heapq.heappush(monti, (-a, c))
        cambios.append((m, pares))
    return D, inicial, cambios


def pruebas():
    r = random.Random(36)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(120, [9000, 1000, 15000], [(15, [(1, 13000), (3, 8000)]), (30, [(3, 11000)]), (45, [(1, 9000), (2, 3500)]),
                                         (60, [(1, 14000)]), (100, [(1, 13000), (2, 5000), (3, 10000)])]),
            (10, [50, 80, 20, 30], [(4, [(2, 10)]), (7, [(3, 90), (1, 5)])]),
            (5, [7, 3], [])],
           "Los tres casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (D, C, N; C audiencias; cada actualización «m u» y u parejas canal-audiencia), los tramos o el orden de la salida.",
            "pe": "Los datos están bien pero no el formato: «canal minutos» en cada línea y «---» al final de cada caso.",
            "rte": "Se rompe con el ejemplo: los canales van de 1 a C, así que la cola necesita sitio para el índice C (tamaño C + 1, o restar 1 al canal)."},
           ["En el primer caso el canal 3 lidera de 0 a 15 y de 45 a 60; el canal 1, el resto (90 minutos).",
            "Cada caso escribe «canal minutos» de más a menos minutos y termina con «---».",
            "La entrada empieza con el número de casos: usa la plantilla de número de casos."])
    prueba("Un solo canal", "borde",
           [(1, [5], []), (10, [3], [(2, [(1, 7)]), (9, [(1, 0)])])],
           "Con un único canal, él lidera la franja entera.",
           {"wa": "Con un solo canal debe salir «1 D». Revisa que sumas todos los tramos, también el último.",
            "rte": "Con un solo canal te sales: revisa el tamaño de la cola y de los vectores (canales numerados desde 1)."},
           ["El primer caso es «1 1»: un canal en una franja de un minuto.",
            "El segundo caso: el canal 1 lidera los 10 minutos aunque cambie su audiencia (incluso a 0)."])
    prueba("Franja enorme (D = 10⁹)", "borde",
           [(1000000000, [10, 5], [(999999999, [(2, 20)])]), (1000000000, [3], []), (1000000000, [1, 2, 3], [(1, [(3, 0)])]),
            (1000000000, [7, 8], [(500000000, [(2, 1)])]), (1000000000, [5, 4, 3], [(2, [(1, 1)]), (999999998, [(1, 9)])])],
           "Cinco franjas de D = 10⁹ minutos con pocas actualizaciones: hay que contar por tramos, no minuto a minuto.",
           {"tle": "Recorres la franja minuto a minuto: con D = 10⁹ es demasiado. Suma de golpe los minutos de cada tramo (m − minuto anterior).",
            "wa": "Con D = 10⁹ algo se desborda o se corta: los minutos caben en int, pero revisa las restas de los tramos."},
           ["En el primer caso el canal 1 lidera 999.999.999 minutos y el 2, el último: «1 999999999» y «2 1».",
            "No recorras los minutos: entre dos actualizaciones el líder no cambia, así que suma m − anterior de una vez."])
    prueba("Cada tramo es del líder de antes del cambio", "trampa",
           [(10, [5, 9], [(3, [(2, 1)]), (9, [(2, 9)])])],
           "Los minutos de un tramo son del canal que lideraba ANTES de aplicar la actualización que lo cierra.",
           {"wa": "Das los minutos del tramo al líder de después de la actualización: hay que sumarlos al líder actual ANTES de aplicar los cambios."},
           ["El canal 2 lidera [0, 3), el 1 lidera [3, 9) y el 2 otra vez [9, 10): «1 6» y «2 4».",
            "En cada actualización: primero suma m − anterior al líder actual (top), después aplica los cambios."])
    prueba("El último tramo también cuenta", "trampa",
           [(100, [1, 5], [(10, [(1, 9)])])],
           "Tras la última actualización queda el tramo hasta D, que suele olvidarse.",
           {"wa": "Te falta el último tramo: después del bucle, el líder suma D − minuto de la última actualización."},
           ["El canal 2 lidera [0, 10) y el 1 [10, 100): «1 90» y «2 10».",
            "Al acabar las actualizaciones, suma D − anterior al líder que haya en ese momento."])
    prueba("Un canal que nunca lidera no aparece", "trampa",
           [(10, [10, 0, 5], [(6, [(1, 1)])])],
           "El canal 2 nunca es el más visto: no se escribe.",
           {"wa": "Escribes canales con 0 minutos: solo aparecen los que han liderado algún minuto."},
           ["La salida es «1 6», «3 4» y «---»: el canal 2 no sale.",
            "Al escribir, sáltate los canales con 0 minutos."])
    prueba("Sin actualizaciones", "trampa",
           [(77, [3, 9, 4], [])],
           "N = 0: el líder del minuto 0 lo es durante toda la franja.",
           {"wa": "Con N = 0 no escribes nada o te equivocas de canal: el líder inicial suma los D minutos.",
            "tle": "Con N = 0 te quedas esperando más datos: no hay líneas de actualización que leer."},
           ["La respuesta es «2 77» y «---».",
            "El último tramo (de 0 a D si no hay actualizaciones) se suma fuera del bucle."])
    prueba("El líder baja sin que nadie le supere", "trampa",
           [(10, [50, 80, 20], [(4, [(2, 10)])])],
           "El canal 2 pierde casi toda su audiencia y pasa a liderar el 1, que no ha cambiado.",
           {"wa": "Cuando el líder baja no lo recolocas: guardas el líder aparte y solo lo cambias si alguien le supera, o tu montículo no hunde."},
           ["El canal 2 lidera [0, 4) y el 1 [4, 10): «1 6» y «2 4».",
            "Usa update de la IndexPQ: hunde el canal si su audiencia baja."])
    prueba("Empate en minutos: canal menor primero", "trampa",
           [(6, [1, 2, 9], [(2, [(3, 0)]), (4, [(1, 5)])])],
           "Tres canales que lideran 2 minutos cada uno: se ordenan por número de canal.",
           {"wa": "En los empates de minutos no ordenas por número de canal de menor a mayor."},
           ["Cada canal lidera 2 minutos: «1 2», «2 2», «3 2».",
            "Ordena por minutos de mayor a menor y, si empatan, por canal de menor a mayor."])
    prueba("Orden por minutos, no por canal", "trampa",
           [(10, [1, 2, 9], [(7, [(3, 0)])])],
           "El canal 3 lidera más minutos que el 2: sale primero.",
           {"wa": "Escribes los canales en orden de número: hay que ordenarlos por minutos de mayor a menor."},
           ["El canal 3 lidera 7 minutos y el 2 tres: «3 7» y «2 3».",
            "Ordena el vector de resultados por minutos (de mayor a menor) antes de escribir."])
    prueba("El canal número C", "trampa",
           [(10, [1, 2, 3, 4, 5, 6], [(5, [(6, 0), (3, 10)])])],
           "Los canales se numeran de 1 a C: el último canal (C) lidera y luego cambia.",
           {"rte": "Te sales del vector o de la cola con el canal C: los canales van de 1 a C, así que hace falta tamaño C + 1 (o restar 1 al índice).",
            "wa": "El canal C no se trata bien: revisa la traducción entre número de canal (1..C) y posición en tus vectores."},
           ["El canal 6 lidera [0, 5) y el 3 [5, 10): «3 5» y «6 5».",
            "Si la cola tiene tamaño C, el índice C no existe: créala con C + 1 o usa canal − 1."])
    prueba("Varios cambios en el mismo minuto", "trampa",
           [(10, [10, 5, 1], [(3, [(1, 3), (2, 8), (3, 9)])])],
           "En una actualización cambian varios canales a la vez: el líder nuevo se mira tras aplicarlos todos.",
           {"wa": "Con varios cambios en un mismo minuto algo falla: suma el tramo antes de aplicar el primer cambio y no vuelvas a sumar entre cambio y cambio."},
           ["El canal 1 lidera [0, 3) y el 3 [3, 10): «3 7» y «1 3».",
            "Por actualización: un único «sumar tramo» y después los u cambios seguidos."])
    prueba("El mismo canal lidera en tramos separados", "trampa",
           [(20, [5, 1], [(4, [(2, 9)]), (8, [(1, 10)]), (12, [(2, 11)]), (15, [(2, 2)])])],
           "Un canal que pierde y recupera el liderato acumula todos sus tramos.",
           {"wa": "No acumulas los minutos de un canal: cada tramo se SUMA a lo que ya llevaba."},
           ["Canal 1: [0, 4) + [8, 12) + [15, 20) = 13; canal 2: [4, 8) + [12, 15) = 7.",
            "Usa un vector de minutos por canal y súmale cada tramo con +=."])
    prueba("Varios casos seguidos", "trampa",
           [(100, [1, 9], [(60, [(1, 10)])]), (5, [4, 2], [(2, [(2, 6)])]), (3, [7], []), (8, [1, 2, 3], [(1, [(1, 5)])])],
           "Casos con distinto número de canales seguidos: cada caso empieza de cero.",
           {"wa": "Algo se arrastra de un caso a otro: los minutos por canal, el minuto de la actualización anterior o la cola deben crearse en cada caso.",
            "rte": "Una estructura de un caso anterior (con otro número de canales) se usa en el siguiente."},
           ["El primer caso acaba en el minuto 60: el segundo empieza otra vez en el minuto 0.",
            "Declara la cola, el vector de minutos y el minuto anterior dentro de resuelveCaso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(1, 5), r.randint(0, 6), 12, r.randint(1, 20)) for _ in range(60)],
           "60 casos pequeños al azar.",
           {"wa": "Hay algún caso concreto que no tratas: cuenta los «---» hasta la línea que falla y dibuja la línea de tiempo de ese caso.",
            "rte": "Algún caso pequeño hace que te salgas de un vector (¿canales desde 1?)."},
           ["Haz la línea de tiempo del caso que falla: quién lidera entre cada dos actualizaciones.",
            "Comprueba primero el orden de la salida y el último tramo."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, r.randint(5, 300), r.randint(10, 300), 1000000, r.randint(500, 1000000000)) for _ in range(15)],
           "15 casos medianos con audiencias y franjas grandes.",
           {"wa": "Falla algún caso mediano: busca entre los pequeños uno que también falle; es más fácil de seguir."},
           ["Si los pequeños salen bien, revisa lo que solo pasa a lo grande: muchos canales, D grande, varios cambios por minuto.",
            "Los minutos caben en int (≤ 10⁹), pero revisa que no multiplicas ni sumas de más."])
    prueba("100.000 canales y 50.000 actualizaciones", "rendimiento",
           [aleatorio(r, 100000, 50000, 1000000, 1000000000, maxU=2, salto=20)],
           "Muchos canales y muchas actualizaciones: buscar el líder recorriendo todos los canales es demasiado lento.",
           {"tle": "Buscar el líder recorriendo los C canales en cada actualización es O(C·N). Con una IndexPQ de máximos el líder es top() y cada cambio un update en O(log C).",
            "mle": "Gastas demasiada memoria: basta un vector de C enteros y la cola."},
           ["Con 10⁵ canales y 5·10⁴ actualizaciones, recorrer todos los canales cada vez son 5·10⁹ operaciones.",
            "Guarda los canales en una IndexPQ de máximos (índice = canal, prioridad = audiencia): el líder es top().",
            "Cada cambio de audiencia es un update(canal, nueva): sube o baja al canal en O(log C)."])
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join(l + "\n" for c in casos for l in audiencias(*c)),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("suma el tramo al líder de después del cambio",
             [("\t\tCanales lider = pq.top().prioridad;\n\t\ttiempos[lider.canal - 1].audiencia += tiempoActual - tiempoAnterior;\n", ""),
              ("\t\ttiempoAnterior = tiempoActual;",
               "\t\tCanales lider = pq.top().prioridad;\n\t\ttiempos[lider.canal - 1].audiencia += tiempoActual - tiempoAnterior;\n\t\ttiempoAnterior = tiempoActual;")],
             prueba=4, v="wa"),
    Variante("olvida el último tramo",
             [("tiempos[pq.top().prioridad.canal - 1].audiencia += duracion - tiempoAnterior;", "")], prueba=5, v="wa"),
    Variante("escribe canales con 0 minutos", [("if (tiempos[i].audiencia > 0)", "if (tiempos[i].audiencia >= 0)")], prueba=6, v="wa"),
    Variante("no ordena por minutos", [("std::sort(tiempos.begin(), tiempos.end(), greater<Canales>());", "")], prueba=10, v="wa"),
    Variante("cola de tamaño C (canales desde 1)",
             [("IndexPQ<Canales, greater<Canales>> pq(canales + 1);", "IndexPQ<Canales, greater<Canales>> pq(canales);")], prueba=11, v="rte"),
    Variante("el minuto anterior no se reinicia entre casos", [("int tiempoAnterior = 0;", "static int tiempoAnterior = 0;")], prueba=14, v="wa"),
    Variante("canal y minutos en líneas distintas",
             [("cout << tiempos[i].canal << ' ' << tiempos[i].audiencia", "cout << tiempos[i].canal << '\\n' << tiempos[i].audiencia")], prueba=1, v="pe"),
    Variante("cuenta minuto a minuto",
             [("tiempos[lider.canal - 1].audiencia += tiempoActual - tiempoAnterior;",
               "{ volatile int minuto = 1; for (int t = tiempoAnterior; t < tiempoActual; ++t) tiempos[lider.canal - 1].audiencia += minuto; }"),
              ("tiempos[pq.top().prioridad.canal - 1].audiencia += duracion - tiempoAnterior;",
               "{ volatile int minuto = 1; for (int t = tiempoAnterior; t < duracion; ++t) tiempos[pq.top().prioridad.canal - 1].audiencia += minuto; }")],
             prueba=3, v="tle"),
    Variante("busca el líder recorriendo todos los canales",
             [("Canales lider = pq.top().prioridad;",
               "Canales lider = pq.priority(1);\n\t\tfor (int k = 2; k <= canales; ++k) if (pq.priority(k) > lider) lider = pq.priority(k);")],
             prueba=17, v="tle"),
]
