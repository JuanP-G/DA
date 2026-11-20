"""03-4 · Pájaros en vuelo: juez con pruebas pensadas para cada error típico."""
import heapq
import pathlib
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "3-Colas de prioridad variable (Heapsort)/EJ_03-4/EJ_03-4.cpp",
    "cabeceras": [],
    "limite_ms": 4000,
    "fallo": ["if (edad < lider) menores.push(edad);", "if (edad < primero) menores.push(edad);"],
}


def bandada(primero, edades):
    """Solucionador independiente: mediana con dos montículos (heapq), contando cuántos hay a cada lado."""
    izq, der = [], []          # izq: máximos (con signo cambiado) · der: mínimos
    med, res = primero, []
    for k in range(0, len(edades), 2):
        for e in edades[k:k + 2]:
            if e > med:
                heapq.heappush(der, e)
            else:
                heapq.heappush(izq, -e)
        while len(izq) > len(der):
            heapq.heappush(der, med)
            med = -heapq.heappop(izq)
        while len(der) > len(izq):
            heapq.heappush(izq, -med)
            med = heapq.heappop(der)
        res.append(med)
    return res


def caso_a_texto(c):
    primero, edades = c
    return f"{primero} {len(edades) // 2}\n" + " ".join(map(str, edades)) + "\n"


def aleatorio(r, parejas, maxEdad):
    e = r.sample(range(1, maxEdad + 1), 2 * parejas + 1)
    return e[0], e[1:]


def pruebas():
    r = random.Random(34)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplo del enunciado", "enunciado",
           [(30, [10, 20, 35, 25, 5, 40]), (1, [2, 3, 4, 5, 6, 7]), (50, [40, 45, 10, 20, 1, 2])],
           "Los tres casos del ejemplo del PDF.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (edad del primero, número de PAREJAS y luego el doble de edades) o la idea de la mediana.",
            "pe": "Los números están bien pero no el formato: las edades de cada caso van en UNA línea, separadas por un espacio.",
            "tle": "No termina con el ejemplo: ¿lees bien el final «0 0»? Cada caso trae 2·P edades, no P."},
           ["En el primer caso, tras 10 y 20 la bandada es 10, 20, 30 y el del centro tiene 20.",
            "Escribe un número por pareja, todos los del caso en la misma línea.",
            "La entrada acaba con «0 0»: usa la plantilla de centinela."])
    prueba("Una sola pareja", "borde",
           [(30, [10, 40]), (30, [10, 20]), (30, [40, 50]), (30, [20, 10])],
           "Casos con una única pareja: la punta queda en el primero, por debajo o por encima.",
           {"wa": "Con una sola pareja falla alguno de los tres caminos: ambos más jóvenes, ambos más viejos o uno a cada lado.",
            "rte": "Con una sola pareja consultas la cima de un montículo vacío."},
           ["Con 30 y la pareja 10 y 20 la bandada es 10, 20, 30: la punta es 20.",
            "Tras cada pareja la bandada tiene un número impar de pájaros: la punta es el del centro."])
    prueba("Edades grandes", "borde",
           [(100000000, [99999999, 1, 99999998, 2]), (50000000, [100000000, 99999999])],
           "Edades de hasta 10⁸ segundos: caben en int.",
           {"wa": "Con edades grandes algo se corta: lee las edades en int (o long long), no en short."},
           ["Las edades llegan hasta 100.000.000, que cabe en int.",
            "Revisa el tipo de las variables y de los montículos."])
    prueba("Los dos recién llegados son más jóvenes", "trampa",
           [(50, [40, 45])],
           "Los dos van a la izquierda: la punta pasa a ser el MÁS VIEJO de los jóvenes.",
           {"wa": "Cuando los dos nuevos son más jóvenes, la nueva punta es el mayor de los jóvenes: el montículo de los jóvenes debe ser de MÁXIMOS (priority_queue<int>)."},
           ["La bandada queda 40, 45, 50: la punta es 45, no 40.",
            "Los más jóvenes que la punta van en una cola de máximos: su cima es el más cercano a la punta."])
    prueba("Los dos recién llegados son más viejos", "trampa",
           [(30, [40, 35])],
           "Los dos van a la derecha: la punta pasa a ser el MÁS JOVEN de los viejos.",
           {"wa": "Cuando los dos nuevos son más viejos, la nueva punta es el menor de los viejos: ese montículo debe ser de MÍNIMOS (priority_queue<int, vector<int>, greater<int>>)."},
           ["La bandada queda 30, 35, 40: la punta es 35, no 40.",
            "Los más viejos que la punta van en una cola de mínimos: su cima es el más cercano a la punta."])
    prueba("Uno a cada lado: la punta no cambia", "trampa",
           [(20, [10, 30, 5, 40, 25, 15])],
           "Si un pájaro entra por cada lado, la punta sigue siendo la misma.",
           {"wa": "Cambias la punta aunque los dos lados hayan quedado igual de grandes: solo hay que mover pájaros cuando un lado tiene dos más que el otro."},
           ["Cada pareja trae uno más joven y otro más viejo que 20: «20 20 20».",
            "Reequilibra solo si los tamaños son distintos (con dos pájaros nuevos, la diferencia es 0 o 2)."])
    prueba("Se compara con la punta actual, no con el primero", "trampa",
           [(50, [10, 20, 30, 40])],
           "La punta cambia: los siguientes pájaros se colocan respecto a la punta ACTUAL.",
           {"wa": "Colocas a los recién llegados comparando con el primer pájaro (o con otro fijo), no con la punta actual."},
           ["Tras 10 y 20 la punta es 20; 30 y 40 son más viejos que ella: la bandada 10, 20, 30, 40, 50 tiene punta 30.",
            "Cada pájaro nuevo va a los jóvenes si es más joven que la punta de ESE momento."])
    prueba("Siempre más viejos: la punta envejece", "trampa",
           [(1, [100, 200, 300, 400, 500, 600, 700, 800])],
           "Todas las parejas van a la derecha: cada vez hay que pasar la punta a la izquierda.",
           {"wa": "Al pasar la punta al otro lado varias veces seguidas algo se pierde: la punta antigua debe ir a los jóvenes y la cima de los viejos sube a la punta."},
           ["La bandada 1, 100, 200 tiene punta 100; luego 200, 300 y 400.",
            "Reequilibrar es: meter la punta en el lado pequeño y sacar la cima del lado grande como nueva punta."])
    prueba("Siempre más jóvenes: la punta rejuvenece", "trampa",
           [(1000, [900, 800, 700, 600, 500, 400, 300, 200])],
           "Todas las parejas van a la izquierda: el caso simétrico al anterior.",
           {"wa": "El reequilibrio hacia la derecha falla: la punta antigua debe ir a los viejos y la cima de los jóvenes sube a la punta."},
           ["La bandada 800, 900, 1000 tiene punta 900; luego 800, 700 y 600.",
            "Revisa que los dos casos de reequilibrio son simétricos."])
    prueba("Recién llegados pegados a la punta", "trampa",
           [(50, [49, 51, 1, 2, 100, 48])],
           "Pájaros de edad casi igual a la punta y otros muy lejanos: la nueva punta sale de la cima correcta.",
           {"wa": "Cuando la punta cambia, la nueva debe ser la cima del lado grande (el más cercano a la punta antigua), no cualquier pájaro de ese lado."},
           ["Tras 49 y 51 la punta sigue en 50; tras 1 y 2 la bandada es 1, 2, 49, 50, 51 y la punta es 49; tras 100 y 48, sigue 49.",
            "Comprueba en papel qué hay en cada montículo después de cada pareja."])
    prueba("Varios casos seguidos", "trampa",
           [(50, [10, 20, 30, 40]), (5, [1, 9]), (100, [200, 300]), (7, [3, 11, 1, 2])],
           "Un caso que deja pájaros en los montículos seguido de otros: cada bandada empieza vacía.",
           {"wa": "Algo se arrastra de un caso a otro: los montículos deben crearse dentro de resuelveCaso (o vaciarse al empezar cada caso)."},
           ["El primer caso deja cuatro pájaros en los montículos: el segundo no debe verlos.",
            "Declara los dos montículos dentro de la función de cada caso."])
    prueba("Aleatorios pequeños", "aleatorio",
           [aleatorio(r, r.randint(1, 6), 60) for _ in range(80)],
           "80 bandadas pequeñas al azar.",
           {"wa": "Hay algún caso concreto que no tratas: busca qué caso es (una línea por caso) y ordena a mano sus edades pareja a pareja."},
           ["Tras cada pareja, ordena las edades que llevas y mira la del centro.",
            "Comprueba qué lado (jóvenes o viejos) tiene más pájaros en el paso que falla."])
    prueba("Aleatorios medianos", "aleatorio",
           [aleatorio(r, r.randint(50, 500), 100000000) for _ in range(20)],
           "20 bandadas de cientos de parejas con edades grandes.",
           {"wa": "Falla con bandadas medianas: busca entre las pequeñas una que también falle; es más fácil de seguir."},
           ["Si las pequeñas salen bien, revisa que el reequilibrio deja SIEMPRE los dos lados del mismo tamaño.",
            "Escribe en tu ordenador, tras cada pareja, el tamaño de los dos montículos: deben ser iguales."])
    n = 100000
    prueba("100.000 parejas cada vez más jóvenes", "rendimiento",
           [(2 * n + 1, list(range(2 * n, 0, -1)))],
           "El máximo de parejas, todas más jóvenes que las anteriores: cada pájaro entra por delante.",
           {"tle": "Reordenar la bandada en cada pareja (o mantenerla ordenada en un vector) cuesta O(P) o más por pareja: con 10⁵ parejas es demasiado. Con dos montículos cada pareja cuesta O(log P)."},
           ["Insertar al principio de un vector desplaza todos los demás: con 200.000 pájaros son unos 2·10¹⁰ movimientos.",
            "No hace falta tener la bandada ordenada entera: basta saber el mayor de los jóvenes y el menor de los viejos.",
            "Usa dos priority_queue (de máximos para los jóvenes y de mínimos para los viejos) y la punta aparte."])
    prueba("100.000 parejas al azar", "rendimiento",
           [aleatorio(r, n, 999999)],
           "El máximo de parejas con edades al azar.",
           {"tle": "Tu solución es lenta para 10⁵ parejas: ¿ordenas la bandada tras cada pareja? Cada pareja debe costar O(log P)."},
           ["Cuenta las operaciones por pareja: dos inserciones y como mucho un traspaso entre montículos.",
            "No ordenes la bandada entera tras cada pareja: con dos montículos la punta sale sin ordenar nada."])
    return [Prueba(nombre, tipo,
                   entrada="".join(caso_a_texto(c) for c in casos) + "0 0\n",
                   salida="".join(" ".join(map(str, bandada(*c))) + "\n" for c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


_SOL = (pathlib.Path(__file__).resolve().parent.parent.parent / CONFIG["solucion"]).read_bytes().decode("utf-8", "replace")
_i = _SOL.index("bool resuelveCaso() {")
_RESUELVE = _SOL[_i:_SOL.index("    return true;\n}", _i) + len("    return true;\n}")]

_VECTOR_ORDENADO = """bool resuelveCaso() {
    int primero, parejas;
    cin >> primero >> parejas;

    if (primero == 0 && parejas == 0) return false;

    vector<int> v{ primero };
    for (int i = 0; i < parejas; ++i) {
        for (int j = 0; j < 2; ++j) {
            int edad; cin >> edad;
            v.push_back(edad);
        }
        sort(v.begin(), v.end());
        int lider = v[v.size() / 2];
        cout << lider << (i + 1 < parejas ? ' ' : '\\n');
    }
    return true;
}"""

VARIANTES = [
    Variante("coloca a los nuevos comparando con el primero",
             [("if (edad < lider) menores.push(edad);", "if (edad < primero) menores.push(edad);")], prueba=7, v="wa"),
    Variante("jóvenes en una cola de mínimos",
             [("priority_queue<int> menores;", "priority_queue<int, vector<int>, greater<int>> menores;")], prueba=4, v="wa"),
    Variante("viejos en una cola de máximos",
             [("priority_queue<int, vector<int>, greater<int>> mayores;", "priority_queue<int> mayores;")], prueba=5, v="wa"),
    Variante("reequilibra también con los lados iguales",
             [("else if (mayores.size() > menores.size())", "else if (mayores.size() >= menores.size())")], prueba=6, v="wa"),
    Variante("los montículos no se vacían entre casos",
             [("priority_queue<int> menores;", "static priority_queue<int> menores;"),
              ("priority_queue<int, vector<int>, greater<int>> mayores;", "static priority_queue<int, vector<int>, greater<int>> mayores;")],
             prueba=11, v="wa"),
    Variante("una edad por línea", [("(i + 1 < parejas ? ' ' : '\\n')", "'\\n'")], prueba=1, v="pe"),
    Variante("ordena la bandada tras cada pareja",
             [(_RESUELVE, _VECTOR_ORDENADO), ("#include <functional>", "#include <functional>\n#include <algorithm>")], prueba=[14, 15], v="tle"),
]
