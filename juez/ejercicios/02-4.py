"""02-4 · La ley D'Hondt: juez con pruebas pensadas para cada error típico.

Formato: varios casos; cada uno «C N» y una línea con los C votos. Acaba con «0 0».
Salida: por caso, los escaños de cada candidatura en el orden de la entrada, separados por espacios.

El enunciado no da rangos. Las pruebas se mantienen en lo razonable: 1 ≤ C ≤ 100.000,
1 ≤ N ≤ 100.000 y votos entre 1 y 10⁹ (caben en int, pero votos·(1 + escaños) no).
"""
import heapq
import random
from fractions import Fraction
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-4/EJ_02-4.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["return orden > o.orden;", "return orden < o.orden;"],
}

MAXV = 10 ** 9


class Clave:
    """Orden de prioridad del enunciado: mayor coeficiente; a igualdad, más votos; luego menor índice.
    Se compara con fracciones exactas (sin productos cruzados) para ser independiente de la solución."""
    __slots__ = ("coef", "v", "k")

    def __init__(self, v, e, k):
        self.coef, self.v, self.k = Fraction(v, 1 + e), v, k

    def __lt__(self, o):   # «sale antes que o» (heapq es de mínimos)
        if self.coef != o.coef:
            return self.coef > o.coef
        if self.v != o.v:
            return self.v > o.v
        return self.k < o.k


def dhondt(votos, N):
    esc = [0] * len(votos)
    h = [Clave(v, 0, k) for k, v in enumerate(votos)]
    heapq.heapify(h)
    for _ in range(N):
        c = heapq.heappop(h)
        esc[c.k] += 1
        heapq.heappush(h, Clave(c.v, esc[c.k], c.k))
    return esc


def texto_entrada(casos):
    return "".join(f"{len(v)} {N}\n{' '.join(map(str, v))}\n" for v, N in casos) + "0 0\n"


def texto_salida(casos):
    return "".join(" ".join(map(str, dhondt(v, N))) + "\n" for v, N in casos)


def pruebas():
    r = random.Random(1978)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [([100, 226, 20, 80, 170], 4), ([60, 28, 60], 3)],
           "Los dos casos del PDF, terminados con «0 0».",
           {"wa": "Si fallan hasta los ejemplos, revisa la base: cada escaño va a la candidatura de MAYOR coeficiente votos/(1 + escaños), y la salida va en el orden de la entrada.",
            "pe": "Los números están bien pero no el formato: los escaños de un caso en UNA línea, separados por un espacio."},
           ["Haz a mano el primer caso: los escaños van a 226, 170, 226 (113) y 100.",
            "En el segundo caso hay empates: a igual coeficiente, más votos; y a igualdad de votos, la que aparece antes.",
            "La entrada acaba con «0 0»: usa la plantilla de centinela."])
    prueba("Una sola candidatura", "borde",
           [([5], 1), ([1], 7), ([MAXV], 3)],
           "Con una única candidatura, todos los escaños son suyos.",
           {"wa": "Con una sola candidatura debe salir N: revisa que vuelves a meterla en la cola tras darle cada escaño.",
            "rte": "Con una sola candidatura la cola se queda vacía: después de sacar la cima hay que volver a meterla con un escaño más."},
           ["Con «1 7 / 1» la salida es 7.",
            "Cada escaño: saca la cima, súmale un escaño y vuelve a meterla."])
    prueba("El escaño va al MAYOR coeficiente", "trampa",
           [([10, 1], 1)],
           "Un solo escaño entre 10 y 1 votos: es para la de 10.",
           {"wa": "Das el escaño al coeficiente MENOR: tu comparador está al revés. Con priority_queue (de máximos) operator< debe devolver true cuando this tiene MENOS prioridad que o, es decir, menor coeficiente."},
           ["Con un solo escaño, ¿quién debería llevárselo, la de 10 votos o la de 1?",
            "priority_queue deja arriba el elemento «mayor» según operator<.",
            "En operator<, si los coeficientes difieren, return coef(this) < coef(o) (con productos cruzados: v·(1 + e') < v'·(1 + e))."])
    prueba("Empate de coeficiente: gana la de más votos", "trampa",
           [([30, 60], 2)],
           "El segundo escaño empata a coeficiente 30 (30/1 y 60/2): gana la de 60 votos aunque aparezca después.",
           {"wa": "En el empate de coeficientes no das el escaño a la candidatura con más votos (o lo das por índice, o al revés). El enunciado: a igual coeficiente, más votos; solo si también empatan a votos, la de índice menor."},
           ["Escaño 1: 60 (coef. 60). Escaño 2: coef. 30 (60/2) frente a 30 (30/1), empate: gana 60 por tener más votos.",
            "El orden de los criterios importa: coeficiente, luego votos, luego índice.",
            "En operator<: if (coefs distintos) ...; if (votos != o.votos) return votos < o.votos; return orden > o.orden;"])
    prueba("Salida en el orden de la entrada", "trampa",
           [([100, 300, 200], 3)],
           "Los escaños se escriben en el orden en que aparecen los votos, no en el orden en que salen de la cola.",
           {"wa": "Escribes los escaños en el orden en que salen de la cola de prioridad. Guarda en cada candidatura su posición en la entrada y recoloca los resultados (res[orden] = escaños) antes de escribirlos."},
           ["Hazlo a mano: los escaños van a 300, a 200 y a 300 otra vez (150 > 100), así que la salida es «0 2 1».",
            "La cola no devuelve las candidaturas en el orden de la entrada.",
            "Al vaciar la cola, guarda los escaños en un vector indexado por la posición original y escribe ese vector."])
    prueba("Empate total: gana la de índice menor", "trampa",
           [([50, 50, 50], 2)],
           "Tres candidaturas con los mismos votos y dos escaños: van a la primera y a la segunda.",
           {"wa": "Con empate de coeficiente y de votos, el escaño es de la candidatura que aparece ANTES en la entrada. Si salen al revés, en operator< el último criterio debe ser orden > o.orden (tiene menos prioridad la que aparece después)."},
           ["La salida correcta es «1 1 0».",
            "Recuerda que operator< significa «tiene menos prioridad que»: ¿quién tiene menos prioridad, la que aparece antes o la de después?",
            "La última línea del comparador: return orden > o.orden;"])
    prueba("Sin truncar los coeficientes", "trampa",
           [([10, 7], 4)],
           "El cuarto escaño: 10/3 = 3,33 frente a 7/2 = 3,5. Con división entera los dos valdrían 3.",
           {"wa": "Calculas el coeficiente con división ENTERA (votos / (1 + escaños) entre enteros) y pierdes los decimales: 10/3 y 7/2 salen los dos 3. Compara con productos cruzados: v₁·(1 + e₂) < v₂·(1 + e₁)."},
           ["Escaños: 10, 7, 10 (10/2 = 5 > 3,5) y el cuarto: 3,33 frente a 3,5, es para la de 7.",
            "¿Qué tipo tiene la división votos / (1 + escaños) en tu código?",
            "No dividas: a/b < c/d ⇔ a·d < c·b (con b, d positivos). Así no hay decimales ni redondeos."])
    prueba("Coeficientes casi iguales (precisión)", "trampa",
           [([16777217, 16777216], 1), ([33554433, 16777217], 2), ([100000001, 100000000, 99999999], 3)],
           "Votos de unos 10⁷-10⁸ que solo se diferencian en una unidad: un float no los distingue.",
           {"wa": "Comparas los coeficientes con float (o con una tolerancia tipo 1e-6) y dos coeficientes distintos te salen iguales. Compara con enteros mediante productos cruzados (en long long)."},
           ["16.777.217 y 16.777.216 son distintos, pero en float se redondean al mismo número.",
            "Evita los números reales: compara v₁·(1 + e₂) con v₂·(1 + e₁) en long long."])
    grandes = [r.randint(5 * 10 ** 8, MAXV) for _ in range(6)]
    prueba("Productos que no caben en int", "trampa",
           [(grandes, 40), ([MAXV, MAXV - 1, 7 * 10 ** 8], 30), ([3 * 10 ** 7, 2 * 10 ** 7, 10 ** 7, 5 * 10 ** 6], 350)],
           "Votos grandes (hasta 10⁹, o como unas elecciones generales con 350 escaños): votos·(1 + escaños) pasa de 2³¹ − 1.",
           {"wa": "Los productos cruzados votos·(1 + escaños) no caben en int: con 10⁹ votos ya desborda al multiplicar por 3. Haz los productos en long long (los votos guárdalos como long long o convierte antes de multiplicar)."},
           ["10⁹ · 3 = 3·10⁹, y el máximo de un int es 2.147.483.647.",
            "Aunque los votos quepan en int, su producto no: el tipo de la multiplicación es el de los operandos.",
            "Declara votos como long long (o escribe (long long)votos * (1 + o.escanios))."])
    prueba("Más escaños que candidaturas", "borde",
           [([3, 2, 1], 12), ([1, 1], 5), ([7, 5, 3, 1], 20)],
           "Muchos más escaños que candidaturas: cada una recibe varios.",
           {"wa": "Con muchos escaños por candidatura los coeficientes bajan mucho y aparecen empates: revisa el desempate por votos y por índice, y que el coeficiente usa 1 + escaños."},
           ["Con «1 1» y 5 escaños: empates continuos, ganan alternativamente la primera y la segunda: «3 2».",
            "El coeficiente es votos / (1 + escaños YA asignados)."])
    prueba("Menos escaños que candidaturas", "borde",
           [([5, 9, 2, 9, 1, 3], 2), ([4, 8, 15, 16, 23, 42], 1)],
           "Pocos escaños: la mayoría de candidaturas se queda con 0, y hay que escribirlo.",
           {"wa": "Las candidaturas sin escaños también se escriben (con un 0), en su sitio."},
           ["En el primer caso los dos escaños van a las dos candidaturas de 9 votos: «0 1 0 1 0 0».",
            "El vector de resultados debe tener C posiciones inicializadas a 0."])
    prueba("Varios casos seguidos", "trampa",
           [([100, 226, 20, 80, 170], 4), ([5], 2), ([1, 2, 3], 6), ([60, 28, 60], 3)],
           "Varios casos seguidos de distinto tamaño: nada debe arrastrarse de uno a otro.",
           {"wa": "El primer caso sale bien y los siguientes no: algo se arrastra entre casos (la cola o el vector de resultados fuera de resuelveCaso).",
            "rte": "Un vector del caso anterior con otro tamaño: créalo dentro de resuelveCaso."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de la función de cada caso.",
            "Declara la cola y el vector de resultados dentro de resuelveCaso."])
    casos = []
    for _ in range(300):
        C = r.randint(1, 6)
        casos.append(([r.randint(1, r.choice([4, 12, 100])) for _ in range(C)], r.randint(1, 12)))
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "300 casos pequeños con pocos votos: muchísimos empates de todo tipo.",
           {"wa": "Algún caso concreto falla: la línea que falla es el número de caso; búscalo en la entrada y reparte los escaños a mano."},
           ["Localiza el caso por el número de línea.",
            "Haz la tabla de coeficientes v/1, v/2, v/3... de cada candidatura y ve eligiendo el mayor (con los desempates)."])
    casos = []
    for _ in range(30):
        C = r.randint(2, 300)
        casos.append(([r.randint(1, MAXV) for _ in range(C)], r.randint(1, 3000)))
    prueba("Aleatorios con votos grandes", "aleatorio", casos,
           "30 casos de hasta 300 candidaturas y 3000 escaños con votos hasta 10⁹.",
           {"wa": "Con votos grandes falla algo: revisa que los productos cruzados se hacen en long long y que no usas float."},
           ["Comprueba los tipos de todas las variables que intervienen en el comparador.",
            "votos · (1 + escaños) puede llegar a 10⁹ · 3001."])
    prueba("Grande: 100.000 candidaturas y 100.000 escaños", "rendimiento",
           [([r.randint(1, MAXV) for _ in range(100000)], 100000)],
           "Tamaño grande: mide la eficiencia (debe ser O((C + N) log C)).",
           {"tle": "Buscar la candidatura de mayor coeficiente recorriéndolas todas en cada escaño cuesta O(N·C) = 10¹⁰: usa una cola de prioridad de máximos.",
            "wa": "Con muchos datos falla algo: revisa los productos en long long."},
           ["¿Cuánto cuesta decidir cada escaño? Hay 100.000.",
            "Con una cola de prioridad cada escaño es un pop y un push: O(log C)."])
    prueba("Grande: votos iguales (empates masivos)", "rendimiento",
           [([777] * 100000, 150000)],
           "100.000 candidaturas con los mismos votos y 150.000 escaños: todos los escaños se deciden por desempate.",
           {"tle": "Con empates masivos tu solución es lenta: el desempate debe estar en el comparador de la cola, no en una búsqueda aparte.",
            "wa": "Con todo empatado los escaños van por orden de aparición: las 50.000 primeras candidaturas reciben 2 y el resto 1."},
           ["Con todos los votos iguales el reparto es por turnos en orden de índice.",
            "El comparador debe desempatar por votos y por índice en O(1)."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida=texto_salida(c), casos=len(c),
                   comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


VARIANTES = [
    Variante("comparador al revés (da el escaño al menor coeficiente)",
             [("if (izq != der) return izq < der;", "if (izq != der) return izq > der;")], prueba=3, v="wa"),
    Variante("desempata por índice sin mirar los votos",
             [("if (votos != o.votos) return votos < o.votos;  // menos votos", "")], prueba=4, v="wa"),
    Variante("desempate por votos al revés",
             [("if (votos != o.votos) return votos < o.votos;", "if (votos != o.votos) return votos > o.votos;")],
             prueba=4, v="wa"),
    Variante("desempate por índice al revés", [("return orden > o.orden;", "return orden < o.orden;")], prueba=6, v="wa"),
    Variante("escribe en el orden en que salen de la cola",
             [("res[cola.top().orden] = cola.top().escanios;", "res[candidaturas - (int)cola.size()] = cola.top().escanios;")],
             prueba=5, v="wa"),
    Variante("coeficiente con división entera",
             [("long long izq = votos * (1 + o.escanios);\n        long long der = o.votos * (1 + escanios);",
               "long long izq = votos / (1 + escanios);\n        long long der = o.votos / (1 + o.escanios);")],
             prueba=7, v="wa"),
    Variante("coeficiente en float",
             [("long long izq = votos * (1 + o.escanios);\n        long long der = o.votos * (1 + escanios);",
               "float izq = (float)votos / (1 + escanios);\n        float der = (float)o.votos / (1 + o.escanios);")],
             prueba=8, v="wa"),
    Variante("votos en int (el producto desborda)",
             [("    long long votos;\n    int escanios;", "    int votos;\n    int escanios;"),
              ("long long izq = votos * (1 + o.escanios);\n        long long der = o.votos * (1 + escanios);",
               "int izq = votos * (1 + o.escanios);\n        int der = o.votos * (1 + escanios);"),
              ("        long long votos;\n        cin >> votos;", "        int votos;\n        cin >> votos;")],
             prueba=9, v="wa"),
    Variante("formato: un número por línea", [('cout << (i > 0 ? " " : "") << res[i];', 'cout << (i > 0 ? "\\n" : "") << res[i];')],
             prueba=1, v="pe"),
    Variante("busca el máximo recorriendo todas las candidaturas (O(N·C))",
             [("""    for (int i = 0; i < escanios; ++i) {
        Candidatura c = cola.top(); cola.pop();
        ++c.escanios;
		cola.push(c);
    }""", """    vector<Candidatura> v;
    while (!cola.empty()) { v.push_back(cola.top()); cola.pop(); }
    for (int i = 0; i < escanios; ++i) {
        int m = 0;
        for (int j = 1; j < (int)v.size(); ++j) if (v[m] < v[j]) m = j;
        ++v[m].escanios;
    }
    for (auto& c : v) cola.push(c);""")], prueba=15, v="tle"),
]
