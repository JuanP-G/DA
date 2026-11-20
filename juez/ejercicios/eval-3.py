"""eval-3 · Cine romántico a raudales: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada uno N (1..300.000) y N películas «D HH:MM duración» (D 1..100.000,
duración 1..10⁶); la suma de N no pasa de 500.000.
Salida: el máximo de minutos viendo películas, con 10 minutos libres entre una y la siguiente.

El solucionador es propio: ordena por FIN y hace best[i] = max(best[i−1], dur_i + best[j]) con j
el número de películas que acaban como tarde 10 minutos antes de que empiece la i (bisect sobre los
finales), al revés que la solución del repo (ordena por inicio y busca la siguiente). Validado
contra fuerza bruta (todos los subconjuntos) en miles de casos pequeños.

Notas sobre los rangos:
- Las películas vistas no se solapan, así que el total es como mucho el tiempo que va del primer
  minuto al final de la última: 100.000 · 1.440 + 10⁶ ≈ 1,45·10⁸ < 2³¹. Dentro de los rangos el
  total NO desborda un int (el comentario de la solución del repo sobre long long es prudente pero
  no necesario); por eso no hay variante de desbordamiento, aunque sí una prueba con el total más
  grande posible.
- Con el formato «D HH:MM duración» cada película ocupa al menos 10 bytes, así que N = 300.000 no
  cabe en el límite de 2,5 MB por fichero: las pruebas de rendimiento usan N = 150.000, que basta
  para que una búsqueda lineal de la siguiente película (O(N²)) pase de largo del límite.
"""
import bisect
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_Eval-3/EJ_Eval-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["p[i].fin + 10", "p[i].fin"],
}


def intervalo(f):
    D, h, m, dur = f
    ini = (D - 1) * 1440 + h * 60 + m
    return ini, ini + dur


def resuelve(pelis):
    iv = sorted((intervalo(f) for f in pelis), key=lambda x: x[1])
    fines = [b for _, b in iv]
    best = [0] * (len(iv) + 1)
    for i, (a, b) in enumerate(iv, 1):
        j = bisect.bisect_right(fines, a - 10, 0, i - 1)
        best[i] = max(best[i - 1], (b - a) + best[j])
    return best[-1]


def fuerza_bruta(pelis):
    iv = sorted(intervalo(f) for f in pelis)
    n, mejor = len(iv), 0
    for mask in range(1 << n):
        sel = [iv[k] for k in range(n) if mask >> k & 1]
        if all(sel[k + 1][0] >= sel[k][1] + 10 for k in range(len(sel) - 1)):
            mejor = max(mejor, sum(b - a for a, b in sel))
    return mejor


def peli(rng, dmax, durmax, durmin=1):
    return (rng.randint(1, dmax), rng.randint(0, 23), rng.randint(0, 59), rng.randint(durmin, durmax))


def aleatorio(rng, nmax, dmax, durmax):
    return [peli(rng, dmax, durmax) for _ in range(rng.randint(1, nmax))]


def h(D, hhmm, dur):
    hh, mm = map(int, hhmm.split(":"))
    return (D, hh, mm, dur)


def caso_a_texto(c):
    return f"{len(c)}\n" + "".join(f"{D} {hh:02d}:{mm:02d} {dur}\n" for D, hh, mm, dur in c)


def pruebas():
    rng = random.Random(3003)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo 1 del enunciado", "enunciado", [[h(1, "11:00", 90), h(1, "12:30", 90), h(1, "12:45", 60)]],
           "La de las 12:30 empieza justo cuando acaba la de las 11:00: sin 10 minutos libres no se pueden ver las dos (150).",
           {"wa": "Falla el primer ejemplo: entre una película y la siguiente hacen falta 10 minutos libres (inicio ≥ fin + 10).",
            "pe": "Escribe solo el número de minutos, con un salto de línea por caso."},
           ["Pasa cada película a minutos: empieza en (D−1)·1440 + HH·60 + MM y acaba al sumar la duración.",
            "minutos(i) = máximo de minutos(i+1) (no verla) y dur_i + minutos(sig(i)) (verla).",
            "sig(i) es la primera película (ordenadas por inicio) que empieza en fin_i + 10 o después."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [[h(1, "11:00", 90), h(1, "12:45", 60), h(1, "11:00", 180)]],
           "Dos películas suman 150 minutos, pero compensa más la de 180 sola.",
           {"wa": "Falla el segundo ejemplo: no se busca ver muchas películas sino estar más tiempo viéndolas."},
           ["Compara ver la de 90 y la de 60 con ver solo la de 180.",
            "Para cada película decide verla o no con la recurrencia, sin reglas voraces."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [[h(2, "12:00", 80), h(1, "20:00", 80)]],
           "Películas en días distintos y desordenadas: se ven las dos (160).",
           {"wa": "Falla el tercer ejemplo: el día cuenta (cada día son 1440 minutos) y las películas no vienen ordenadas."},
           ["¿Ordenas las películas antes de la programación dinámica?",
            "El inicio absoluto es (D−1)·1440 + HH·60 + MM."])
    prueba("Ninguna es compatible con otra", "trampa", [[h(1, "10:00", 120), h(1, "11:00", 70), h(1, "11:50", 30)]],
           "Las tres se solapan entre sí: solo se puede ver una, la más larga (120).",
           {"wa": "Sumas películas que se solapan: al ver la película i, lo siguiente que se puede ver es sig(i), no la i+1."},
           ["Si escribes 220, sumas las tres aunque se solapan.",
            "En la opción «verla» se suma minutos(sig(i)), con sig(i) la primera que empieza en fin_i + 10 o después."])
    prueba("Empieza justo cuando acaba la otra", "trampa", [[h(1, "10:00", 60), h(1, "11:00", 60)]],
           "La segunda empieza a la misma hora a la que acaba la primera: no hay 10 minutos libres (60).",
           {"wa": "No dejas los 10 minutos libres entre película y película. La siguiente tiene que empezar en fin + 10 o después."},
           ["Si escribes 120, te falta el descanso.",
            "Busca la primera película con inicio ≥ fin + 10, no inicio ≥ fin."])
    prueba("Exactamente 10 minutos libres", "trampa", [[h(1, "10:00", 60), h(1, "11:10", 60)]],
           "La segunda empieza justo 10 minutos después de que acabe la primera: sí se pueden ver las dos (120).",
           {"wa": "Con exactamente 10 minutos libres sí da tiempo: la condición es inicio ≥ fin + 10 (no >). Si usas upper_bound, cambia a lower_bound."},
           ["Si escribes 60, exiges más de 10 minutos.",
            "lower_bound(fin + 10) da la primera con inicio ≥ fin + 10; upper_bound, la primera con inicio > fin + 10."])
    prueba("Nueve minutos no bastan", "trampa", [[h(1, "10:00", 60), h(1, "11:09", 30)]],
           "Solo hay 9 minutos entre las dos: no se pueden ver juntas (60).",
           {"wa": "Das por buenas películas con menos de 10 minutos libres: revisa el + 10 de la condición."},
           ["Si escribes 90, el descanso que exiges es menor de 10 minutos.",
            "La condición es inicio ≥ fin + 10, con los minutos contados desde el principio del maratón."])
    prueba("Mismo horario en días distintos", "trampa", [[h(1, "10:00", 60), h(2, "10:00", 60), h(3, "10:00", 60)]],
           "Tres películas a la misma hora en días distintos: se ven las tres (180).",
           {"wa": "No tienes en cuenta el día: dos películas a la misma hora en días distintos no se solapan. Cada día son 1440 minutos."},
           ["Si escribes 60, comparas solo las horas.",
            "El inicio absoluto es (D−1)·1440 + HH·60 + MM."])
    prueba("Una película pasa de medianoche", "trampa", [[h(1, "23:00", 120), h(2, "00:50", 30)]],
           "La primera acaba a la 01:00 del día 2 y la segunda empieza a las 00:50: se solapan (120).",
           {"wa": "Una película que pasa de medianoche ocupa también el día siguiente: con minutos absolutos (día incluido) sale sola."},
           ["¿A qué hora y qué día acaba la película de las 23:00 que dura 120 minutos?",
            "Calcula fin = inicio + duración en minutos absolutos; no lo reduzcas a la hora del día."])
    prueba("Más películas no es más tiempo", "trampa", [[h(1, "10:00", 200), h(1, "10:00", 30), h(1, "10:40", 30)]],
           "Ver las dos cortas (la estrategia de «la que antes acaba») da 60 minutos; la larga sola da 200.",
           {"wa": "Usas el voraz de «la que antes acaba» (el del maratón de terror): maximiza el número de películas, no los minutos. Hace falta programación dinámica."},
           ["Si escribes 60, eliges como en el 08-4.",
            "Con pesos (duraciones) el voraz no sirve: minutos(i) = max(minutos(i+1), dur_i + minutos(sig(i)))."])
    prueba("Entrada desordenada", "trampa", [[h(1, "14:00", 60), h(1, "12:00", 60), h(1, "10:00", 60)]],
           "Las películas vienen al revés: hay que ordenarlas para buscar la siguiente (180).",
           {"wa": "No ordenas las películas por inicio antes de la búsqueda binaria: lower_bound solo funciona sobre un vector ordenado."},
           ["¿Está ordenado el vector en el que haces lower_bound?",
            "Ordena las películas por su inicio absoluto antes de rellenar la tabla."])
    prueba("Una sola película", "borde", [[h(1, "00:00", 1)], [h(100000, "23:59", 1000000)], [h(50000, "12:00", 777)]],
           "Una película por caso, con los valores mínimos y máximos.",
           {"wa": "Con una sola película la respuesta es su duración.",
            "rte": "Con N = 1 te sales del vector: la tabla tiene N + 1 posiciones."},
           ["La tabla minutos tiene N + 1 posiciones y minutos(N) = 0.",
            "sig(i) puede ser N (no hay ninguna después)."])
    largo = [(1 + 695 * k, 0, 0, 1000000) for k in range(144)]
    prueba("El total más grande posible", "borde", [largo],
           "144 películas de 10⁶ minutos, una tras otra con 80 minutos libres: el total es 1,44·10⁸.",
           {"wa": "Con duraciones enormes el total es grande: revisa los tipos de los inicios, los finales y la tabla."},
           ["Cada película acaba 10⁶ minutos después de empezar, varios días más tarde.",
            "Calcula los minutos absolutos con un tipo entero que no se quede corto (long long es lo más cómodo)."])
    prueba("Varios casos seguidos", "trampa", [aleatorio(rng, 300, 3, 300), [h(1, "10:00", 60)], [h(1, "10:00", 5), h(1, "10:15", 5)]],
           "Un caso grande y luego otros pequeños: nada del anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente (el vector de películas o la tabla): créalos dentro de la función de cada caso.",
            "rte": "La tabla de un caso anterior tiene otro tamaño: créala en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de resuelveCaso.",
            "Declara el vector y la tabla dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio", [aleatorio(rng, 8, rng.choice([1, 2, 5]), rng.choice([30, 200, 2000])) for _ in range(300)],
           "300 casos al azar con hasta 8 películas.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; pruébalo a mano."},
           ["Busca en la entrada el caso de la línea que falla y hazlo en papel.",
            "Revisa los 10 minutos, los días y el orden de las películas."])
    prueba("Aleatorios medianos", "aleatorio", [aleatorio(rng, 1000, rng.choice([3, 30, 1000]), rng.choice([200, 5000])) for _ in range(30)],
           "30 casos al azar con hasta 1000 películas.",
           {"wa": "Falla en casos más grandes: revisa la búsqueda de la siguiente película."},
           ["Busca en la entrada el caso de la línea que falla.",
            "Comprueba la búsqueda binaria sobre los inicios ordenados."])
    prueba("150.000 películas muy largas", "rendimiento", [[peli(rng, 9, 999999, 100000) for _ in range(150000)]],
           "Todas las películas se solapan con casi todas las demás: buscar la siguiente recorriendo es O(N²).",
           {"tle": "Buscas sig(i) recorriendo las películas siguientes (o comparas todas con todas): O(N²) no da tiempo. Usa búsqueda binaria (lower_bound) sobre los inicios ordenados.",
            "wa": "Falla con películas que duran días: revisa que calculas los minutos absolutos con el día."},
           ["¿Cuántas películas miras para encontrar sig(i) cuando todas se solapan?",
            "Los inicios están ordenados: la primera con inicio ≥ fin + 10 se encuentra con búsqueda binaria en O(log N)."])
    prueba("150.000 películas al azar", "rendimiento", [[peli(rng, 100000, 1000) for _ in range(130000)], [peli(rng, 3, 300) for _ in range(20000)]],
           "Un caso de 130.000 películas repartidas en 100.000 días y otro de 20.000 en 3 días.",
           {"tle": "Es lento: debe ser O(N log N) (ordenar y una búsqueda binaria por película). Lee la entrada con cin sin cosas raras.",
            "mle": "Gastas demasiada memoria: basta un vector de películas y otro de N + 1 para la tabla."},
           ["Ordenar es O(N log N); cada sig(i) con lower_bound, O(log N).",
            "No copies vectores dentro del bucle."])
    total = 0
    for c in (c for x in P for c in x[2]):
        assert 1 <= len(c) <= 300000 and all(1 <= D <= 100000 and 0 <= hh < 24 and 0 <= mm < 60 and 1 <= d <= 1000000 for D, hh, mm, d in c)
    for x in P:
        assert sum(len(c) for c in x[2]) <= 500000
    return [Prueba(nombre, tipo,
                   entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                   salida="".join("%d\n" % resuelve(c) for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


VARIANTES = [
    Variante("suma películas solapadas", [("(p[i].fin - p[i].ini) + minutos[sig]", "(p[i].fin - p[i].ini) + minutos[i + 1]")], prueba=4, v="wa"),
    Variante("sin los 10 minutos", [("p[i].fin + 10", "p[i].fin")], prueba=5, v="wa"),
    Variante("exige más de 10 minutos (upper_bound)", [("lower_bound(inicios.begin(), inicios.end(), p[i].fin + 10)", "upper_bound(inicios.begin(), inicios.end(), p[i].fin + 10)")], prueba=6, v="wa"),
    Variante("ignora el día", [("p[i].ini = (d - 1) * 1440 + hh * 60 + mm;", "p[i].ini = hh * 60 + mm;")], prueba=8, v="wa"),
    Variante("voraz del 08-4 (la que antes acaba)",
             [("void resuelveCaso() {",
               "void resuelveCaso() {\n    int N0; cin >> N0; vector<pair<long long, long long>> v(N0);\n"
               "    for (auto& x : v) { long long d, du; int hh, mm; char dp; cin >> d >> hh >> dp >> mm >> du;\n"
               "        long long a = (d - 1) * 1440 + hh * 60 + mm; x = {a + du, a}; }\n"
               "    sort(v.begin(), v.end()); long long ult = -1000000000LL, tot = 0;\n"
               "    for (auto& x : v) if (x.second >= ult + 10) { tot += x.first - x.second; ult = x.first; }\n"
               "    cout << tot << '\\n'; return;\n")], prueba=10, v="wa"),
    Variante("no ordena", [("sort(p.begin(), p.end());", "")], prueba=11, v="wa"),
    Variante("busca la siguiente recorriendo (O(N²))",
             [("int sig = lower_bound(inicios.begin(), inicios.end(), p[i].fin + 10) - inicios.begin();",
               "int sig = i + 1;\n        while (sig < N && inicios[sig] < p[i].fin + 10) ++sig;")], prueba=17, v="tle"),
]
