"""02-1 · Lo que cuesta sumar: juez con pruebas pensadas para cada error típico.

Formato: varios casos; cada uno «N» y una línea con N sumandos (1 ≤ N ≤ 100.000, 1 ≤ x ≤ 10⁶).
La entrada acaba con N = 0, que no se procesa. Por caso, una línea con el esfuerzo mínimo.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-1/EJ_02-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["vector<long long>, greater<long long>> cola", "vector<long long>, less<long long>> cola"],
}

MAXV = 1_000_000
MAXN = 100_000


def esfuerzo(nums):
    """Voraz de Huffman: siempre se suman los dos menores y el resultado vuelve al montón."""
    h = list(nums)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def entrada(casos):
    return "".join(f"{len(c)}\n{' '.join(map(str, c))}\n" for c in casos) + "0\n"


def pruebas():
    r = random.Random(2021)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [[1, 2, 3], [3, 1, 4, 2], [30, 40, 50, 60], [7, 5], [5]],
           "Los cinco casos del PDF, terminados con el 0.",
           {"wa": "Si fallan hasta los ejemplos, revisa la idea de base: hay que sumar siempre los dos números más pequeños que haya en ese momento (incluidos los resultados parciales).",
            "pe": "Los números están bien pero el formato no: un esfuerzo por línea, sin espacios ni texto extra.",
            "rte": "Se rompe con los ejemplos: ¿haces top() o pop() sobre una cola vacía (por ejemplo, en el caso con un solo sumando)?"},
           ["Haz a mano el caso «30 40 50 60»: la respuesta es 360, no 370.",
            "Comprueba que escribes un número por caso y un salto de línea, nada más.",
            "La entrada termina con un caso con N = 0: usa la plantilla de centinela."])
    prueba("El 0 final no se procesa", "trampa",
           [[7, 5], [9], [1, 1]],
           "Casos de uno o dos sumandos (donde no hay forma de equivocarse sumando) seguidos del 0 final.",
           {"wa": "Escribes una línea de más al final: estás procesando el caso N = 0 como si fuera uno más (y sale un 0 extra). El 0 solo marca el final.",
            "ole": "El programa no termina de escribir: no detectas el 0 final y sigues leyendo (y escribiendo) sin fin.",
            "tle": "El programa no termina: el bucle de casos no se detiene al leer N = 0."},
           ["Mira la última línea de tu salida: ¿hay un 0 que no se espera?",
            "Lee N y, si es 0, termina SIN escribir nada (return false en resuelveCaso).",
            "Con la plantilla de centinela: «cin >> N; if (N == 0) return false;» antes de hacer nada más."])
    prueba("Un solo sumando", "borde",
           [[MAXV]],
           "Un único sumando (de valor 10⁶): no hay ninguna suma que hacer, así que el esfuerzo es 0.",
           {"wa": "Con un solo sumando hay que escribir 0. Si escribes el propio número, estás contando como esfuerzo algo que no es una suma.",
            "rte": "Con un solo número sacas dos elementos de la cola: el segundo top()/pop() es sobre una cola vacía."},
           ["¿Cuántas sumas hacen falta para «sumar» un único número?",
            "El bucle debe repetirse mientras queden AL MENOS DOS números en la cola (size() > 1); con uno solo no entra y el esfuerzo se queda en 0."])
    prueba("Dos sumandos", "borde",
           [[7, 5], [1, 1], [MAXV, MAXV], [1, MAXV]],
           "Con dos números hay una sola suma: el esfuerzo es su suma.",
           {"wa": "Con dos números el esfuerzo es exactamente a + b. Si no sale, revisa qué acumulas en cada paso (debe ser a + b, no solo el resultado final ni a·b).",
            "rte": "Con dos números haces más sumas de la cuenta y la cola se queda vacía."},
           ["Con «7 5» se hace una única suma, 7 + 5 = 12, y ya está.",
            "Cada vuelta del bucle saca dos números, suma a + b al esfuerzo y mete a + b en la cola; con dos números solo hay una vuelta."])
    prueba("Siempre los dos menores (no los mayores)", "trampa",
           [[1, 2, 3], [10, 1, 100], [5, 4, 3], [1, 1, 1000000]],
           "Tres sumandos: lo mejor es sumar primero los dos menores.",
           {"wa": "Estás sumando los dos MAYORES: priority_queue<long long> a secas es una cola de MÁXIMOS. Para sumar siempre los menores necesitas una cola de mínimos."},
           ["Con «1 2 3» lo mejor es 1+2 = 3 y luego 3+3 = 6: total 9. Si te sale 11, estás empezando por los grandes.",
            "¿Qué elemento devuelve top() en una priority_queue por defecto, el mayor o el menor?",
            "Declárala como priority_queue<long long, vector<long long>, greater<long long>> para que top() sea el mínimo."])
    prueba("Los resultados parciales vuelven a la cola", "trampa",
           [[10, 10, 10, 10]],
           "Cuatro sumandos iguales: ir arrastrando un único resultado parcial (ordenar y sumar de izquierda a derecha) NO es lo óptimo.",
           {"wa": "Ordenas una vez y vas sumando de uno en uno arrastrando el total. No es óptimo: el resultado parcial puede ser mayor que números que aún no has usado, y entonces conviene sumar esos antes."},
           ["Con «10 10 10 10»: (10+10) + (10+10) + (20+20) = 80, mejor que 20 + 30 + 40 = 90.",
            "Después de cada suma, el resultado es un número más: tiene que competir con los demás por ser de los dos menores.",
            "Mete a + b de nuevo en la cola de prioridad en cada paso, en vez de guardarlo en un acumulador aparte."])
    prueba("Todos los sumandos iguales", "borde",
           [[1] * 8, [3] * 7, [MAXV] * 5, [2] * 16],
           "Muchos números iguales: hay empates en todos los pasos.",
           {"wa": "Con todos iguales los empates no importan, así que el fallo está en otra parte: ¿vuelves a meter cada suma en la cola y la acumulas una sola vez?"},
           ["Con ocho unos: 4 sumas de 1+1, 2 sumas de 2+2 y una de 4+4: total 8 + 8 + 8 = 24.",
            "Cada vuelta suma a + b al esfuerzo una única vez y mete a + b en la cola."])
    prueba("Sumandos desordenados", "trampa",
           [[60, 50, 40, 30], [9, 1, 8, 2, 7, 3, 6, 4, 5], [100, 99, 98, 97, 96, 1]],
           "Los sumandos no vienen ordenados en la entrada (incluso en orden decreciente).",
           {"wa": "Supones que la entrada viene ordenada. No lo dice el enunciado: mete todos los números en la cola de prioridad y que sea ella quien te dé los menores."},
           ["Si tu método funciona con «30 40 50 60» pero no con «60 50 40 30», dependes del orden de la entrada.",
            "No uses la posición en la entrada para nada: la cola de prioridad ordena por ti."])
    prueba("Esfuerzo que no cabe en int", "trampa",
           [[MAXV] * 300, [MAXV - 1] * 301],
           "300 sumandos de 10⁶: las sumas parciales caben en int, pero el esfuerzo total pasa de 2.147.483.647.",
           {"wa": "El esfuerzo total no cabe en int (pasa de 2³¹ − 1): declara el acumulador del esfuerzo como long long."},
           ["300 sumandos de 10⁶ suman 3·10⁸, pero cada número se paga en unas 8 sumas: el esfuerzo ronda 2,5·10⁹.",
            "¿De qué tipo es la variable donde acumulas el esfuerzo? El máximo de un int es 2.147.483.647.",
            "Usa long long para el esfuerzo (y escríbelo tal cual, sin convertirlo a int)."])
    prueba("Sumas parciales que no caben en int", "trampa",
           [[MAXV] * 6000],
           "6.000 sumandos de 10⁶: los propios resultados parciales (no solo el esfuerzo) pasan de 2³¹ − 1 y vuelven a la cola.",
           {"wa": "Los resultados parciales que vuelves a meter en la cola no caben en int: la cola tiene que ser de long long, no de int (aunque los sumandos se lean como int)."},
           ["Con 6000 sumandos de 10⁶ la suma total es 6·10⁹: los últimos resultados parciales ya no caben en un int.",
            "Revisa el tipo de los elementos de la cola y de las variables a y b donde sacas los dos menores.",
            "Declara la cola como priority_queue<long long, vector<long long>, greater<long long>>; a + b debe calcularse en long long."])
    prueba("Varios casos seguidos", "trampa",
           [[30, 40, 50, 60], [5], [7, 5], [1, 2, 3], [10, 10, 10]],
           "Varios casos uno tras otro: el esfuerzo y la cola deben empezar de cero en cada caso.",
           {"wa": "El primer caso sale bien y los siguientes no: algo se arrastra de un caso al siguiente (el esfuerzo o la cola declarados fuera de resuelveCaso, o un static).",
            "rte": "La cola o algún vector conserva datos del caso anterior."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de la función de cada caso.",
            "Al acabar un caso, en la cola queda un número (la suma total). Si la cola es global, ese número se cuela en el siguiente caso.",
            "Declara la cola y el esfuerzo dentro de resuelveCaso, con el esfuerzo inicializado a 0."])
    prueba("Valores mínimos y máximos mezclados", "borde",
           [[1, MAXV, 1, MAXV], [MAXV, 1, 1, 1, 1, 1], [1, 1, MAXV, MAXV, MAXV]],
           "Mezcla de sumandos de valor 1 y de valor 10⁶.",
           {"wa": "Con números muy distintos el orden en que se suman cambia mucho el esfuerzo: comprueba que en cada paso sacas de verdad los dos menores (incluidos los resultados parciales)."},
           ["Haz a mano «1 1000000 1 1000000»: 1+1 = 2, 2+10⁶, y luego la suma de los dos mayores.",
            "Los resultados parciales pequeños tienen que volver a salir antes que los 10⁶."])
    casos = []
    for _ in range(300):
        n = r.randint(1, 9)
        tope = r.choice([3, 10, 50, MAXV])
        casos.append([r.randint(1, tope) for _ in range(n)])
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "300 casos pequeños al azar (hasta 9 sumandos), con muchos repetidos.",
           {"wa": "Hay algún caso concreto que no tratas bien: la línea que falla es el número de caso; búscalo en la entrada y hazlo a mano.",
            "rte": "Algún caso pequeño rompe el programa: revisa los casos de 1 o 2 sumandos."},
           ["La línea que falla te dice qué caso es: cuéntalos en la entrada.",
            "Haz ese caso a mano siempre sumando los dos menores que haya en cada momento."])
    casos = []
    for _ in range(40):
        n = r.randint(100, 2000)
        tope = r.choice([100, MAXV])
        casos.append([r.randint(1, tope) for _ in range(n)])
    prueba("Aleatorios medianos", "aleatorio", casos,
           "40 casos de entre 100 y 2000 sumandos al azar.",
           {"wa": "Con casos medianos falla algo que con los pequeños no: revisa el tipo de las variables (long long) y que vuelves a meter cada suma en la cola."},
           ["Si los pequeños salen bien, sospecha del tamaño de los números: ¿usas long long en todas partes?",
            "Comprueba que la cola es de mínimos y guarda long long."])
    prueba("Muchos casos diminutos", "rendimiento",
           [[r.randint(1, MAXV)] if i % 2 else [r.randint(1, 9), r.randint(1, 9)] for i in range(60000)],
           "60.000 casos de uno o dos sumandos: el trabajo por caso debe ser proporcional a N, no al máximo posible.",
           {"tle": "Haces en cada caso un trabajo que no depende de N (por ejemplo, crear o limpiar un vector de 100.000 posiciones): con muchos casos pequeños eso se nota.",
            "wa": "Con muchos casos seguidos algo se acumula de un caso al siguiente."},
           ["¿Reservas un vector del tamaño máximo en cada caso? Crea solo lo que necesitas para N.",
            "Una cola de prioridad local a resuelveCaso empieza vacía y no cuesta nada crearla."])
    prueba("Grande: 100.000 sumandos (dos casos)", "rendimiento",
           [[r.randint(1, MAXV) for _ in range(MAXN)], [r.randint(1, 1000) for _ in range(MAXN)]],
           "El tamaño máximo, N = 100.000, dos veces: mide la eficiencia (debe ser O(N log N)).",
           {"tle": "Tu solución es cuadrática: ordenar el vector en cada paso o buscar los dos menores recorriéndolo entero cuesta O(N²) con N = 100.000. Usa una cola de prioridad: cada paso cuesta O(log N).",
            "wa": "Con N = 100.000 el esfuerzo llega a ~10¹²: tiene que ser long long, y la cola también."},
           ["¿Cuánto cuesta cada paso de tu bucle? Hay N − 1 pasos.",
            "Ordenar en cada paso son N − 1 ordenaciones: demasiado. Insertar en un vector ordenado también es O(N) por paso.",
            "Con priority_queue cada push y pop es O(log N): en total O(N log N)."])
    return [Prueba(nombre, tipo, entrada=entrada(c), salida="".join(f"{esfuerzo(x)}\n" for x in c),
                   casos=len(c), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


VARIANTES = [
    Variante("cola de máximos (sin greater)",
             [("priority_queue<long long, vector<long long>, greater<long long>> cola;", "priority_queue<long long> cola;")],
             prueba=5, v="wa"),
    Variante("ordena una vez y arrastra un único acumulado",
             [("""    while (cola.size() > 1) {
        long long a = cola.top(); cola.pop();
        long long b = cola.top(); cola.pop();
        esfuerzo += a + b;   // actualizar esfuerzo
        cola.push(a + b);   // devolver el resultado a la cola
    }""", """    long long acum = cola.top(); cola.pop();
    while (!cola.empty()) {
        acum += cola.top(); cola.pop();
        esfuerzo += acum;
    }""")], prueba=6, v="wa"),
    Variante("esfuerzo en int", [("long long esfuerzo = 0;", "int esfuerzo = 0;")], prueba=9, v="wa"),
    Variante("cola de int (sumas parciales en int)",
             [("priority_queue<long long, vector<long long>, greater<long long>> cola;",
               "priority_queue<int, vector<int>, greater<int>> cola;")], prueba=10, v="wa"),
    Variante("procesa el caso N = 0", [("if (N == 0) return false;", "if (!cin) return false;")], prueba=2, v="wa"),
    Variante("no reinicia el esfuerzo entre casos", [("long long esfuerzo = 0;", "static long long esfuerzo = 0;")],
             prueba=11, v="wa"),
    Variante("cola global que no se vacía",
             [("bool resuelveCaso() {", "priority_queue<long long, vector<long long>, greater<long long>> cola;\nbool resuelveCaso() {"),
              ("    priority_queue<long long, vector<long long>, greater<long long>> cola;\n    for", "    for")],
             prueba=11, v="wa"),
    Variante("con un sumando escribe el propio número",
             [("cout << esfuerzo << '\\n';", "cout << (N == 1 ? cola.top() : esfuerzo) << '\\n';")], prueba=3, v="wa"),
    Variante("formato: todo en una línea", [("cout << esfuerzo << '\\n';", "cout << esfuerzo << ' ';")], prueba=1, v="pe"),
    Variante("ordena el vector en cada paso (O(N² log N))",
             [("#include <queue>", "#include <queue>\n#include <algorithm>"),
              ("""    while (cola.size() > 1) {
        long long a = cola.top(); cola.pop();
        long long b = cola.top(); cola.pop();
        esfuerzo += a + b;   // actualizar esfuerzo
        cola.push(a + b);   // devolver el resultado a la cola
    }""", """    vector<long long> v;
    while (!cola.empty()) { v.push_back(cola.top()); cola.pop(); }
    while (v.size() > 1) {
        sort(v.begin(), v.end(), greater<long long>());
        long long a = v.back(); v.pop_back();
        long long b = v.back(); v.pop_back();
        esfuerzo += a + b;
        v.push_back(a + b);
    }""")], prueba=16, v="tle"),
]
