"""02-3 · Reina del súper: juez con pruebas pensadas para cada error típico.

Formato: varios casos; cada uno «N C» (1 ≤ N ≤ 250.000 cajas, 1 ≤ C ≤ 500.000 clientes) y una
línea con C tiempos (1..100). Acaba con «0 0». Por caso, la caja (1..N) en la que acabará Ismael,
que se pone detrás del último; si se liberan varias cajas a la vez, va a la de número menor.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-3/EJ_02-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["vector<pair<int, int>>, greater<pair<int, int>>> cola", "vector<pair<int, int>>, less<pair<int, int>>> cola"],
}

MAXN = 250_000
MAXC = 500_000
MAXT = 100


def caja_de_ismael(N, tiempos):
    """Cada cliente va a la caja que antes se libera (a igualdad, la de menor número)."""
    h = [(0, i) for i in range(1, N + 1)]
    for t in tiempos:
        libre, caja = heapq.heappop(h)
        heapq.heappush(h, (libre + t, caja))
    return h[0][1]


def texto_entrada(casos):
    return "".join(f"{N} {len(ts)}\n{' '.join(map(str, ts))}\n" for N, ts in casos) + "0 0\n"


def pruebas():
    r = random.Random(341)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [(2, [10, 5]), (2, [5, 10]), (3, [5, 10]), (4, [5, 5, 3, 3, 3])],
           "Los cuatro casos del PDF, terminados con «0 0».",
           {"wa": "Si fallan hasta los ejemplos, revisa la idea: cada cliente va a la caja que ANTES queda libre (a igualdad, la de número menor), e Ismael es el cliente C + 1.",
            "pe": "La caja está bien pero no el formato: un número por línea, sin texto extra."},
           ["Haz a mano el caso «2 2 / 10 5»: el primero va a la caja 1 (hasta 10), el segundo a la 2 (hasta 5); Ismael va a la 2.",
            "Escribe solo el número de caja y un salto de línea por caso.",
            "La entrada acaba con «0 0»: usa la plantilla de centinela."])
    prueba("Una sola caja (la caja 1, no la 0)", "trampa",
           [(1, [7]), (1, [MAXT, 1, 50]), (1, [1])],
           "Con una sola caja Ismael siempre va a la caja 1: las cajas se numeran desde 1.",
           {"wa": "Escribes un número de caja desplazado: las cajas van de 1 a N. Si numeras desde 0 en tu cola, suma 1 al escribir (o mete las cajas como 1..N).",
            "rte": "Con una sola caja te sales de algún vector: revisa los índices (cajas 1..N)."},
           ["Con N = 1 la respuesta solo puede ser 1.",
            "¿Con qué números metes las cajas en la cola al principio, 0..N−1 o 1..N?",
            "Mete las cajas como (0, i) con i desde 1 hasta N, ambos incluidos."])
    prueba("Empate: va a la caja de número menor", "trampa",
           [(2, [2, 2, 1, 2, 1, 2, 1])],
           "Dos cajas que quedan libres a la vez varias veces (en 0, en 2 y en 4): se elige siempre la de número menor.",
           {"wa": "Los empates no se resuelven a favor de la caja de número menor: o desempatas al revés, o tu comparador solo mira el instante y la priority_queue elige cualquiera de las empatadas."},
           ["Al principio las dos cajas están libres: el primer cliente va a la 1. En el instante 2 se liberan las dos a la vez y el tercer cliente va otra vez a la 1.",
            "El par (instante en que se libera, número de caja) se compara primero por instante y luego por caja: con greater<> sale antes el de caja menor.",
            "Usa priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> con pares (instante, caja); no inviertas la caja ni compares solo el instante."])
    prueba("Cada cliente va a la caja que antes se libera", "trampa",
           [(3, [6, 2, 5, 1])],
           "La cima de la cola debe ser la caja que ANTES queda libre, no la que más tarde.",
           {"wa": "Eliges la caja que MÁS TARDE se libera: priority_queue<pair<int,int>> a secas es de máximos. Necesitas una cola de mínimos (greater<>)."},
           ["El 6 va a la caja 1, 2 a la 2, 5 a la 3, y el 1 va a la 2 (libre en el instante 2).",
            "¿Qué devuelve top() en una priority_queue por defecto, el mayor o el menor?",
            "Declárala con greater<pair<int,int>> para que top() sea la caja que antes se libera."])
    prueba("Ismael va detrás del último cliente", "trampa",
           [(3, [5, 3])],
           "Se pide la caja de Ismael (el cliente C + 1), no la del último cliente de la fila.",
           {"wa": "Escribes la caja del último cliente (el C-ésimo). Ismael va DETRÁS de él: su caja es la que está en la cima de la cola después de atender a los C clientes."},
           ["Los dos clientes ocupan las cajas 1 y 2; Ismael, que va detrás, va a la 3, que sigue libre.",
            "Cuando acabas de repartir los C clientes, ¿qué caja quedará libre la primera?",
            "Tras el bucle de clientes, la respuesta es cola.top().second."])
    prueba("La fila no va por turnos", "trampa",
           [(2, [10, 5])],
           "Las cajas no se van ocupando en orden 1, 2, ..., N, 1, 2...: depende de cuándo se libera cada una.",
           {"wa": "Repartes los clientes por turnos (o calculas la caja con un módulo). Hay que simular: cada cliente va a la caja que antes se libera, según los tiempos."},
           ["La caja 2 se libera en 5 y la 1 en 10: Ismael va a la 2 aunque «por turno» le tocaría la 1.",
            "Los tiempos de cada cliente importan: guárdalos sumándolos al instante en que se libera su caja."])
    prueba("Más empates y desempates", "trampa",
           [(3, [4, 4, 4]), (4, [2, 2, 2, 2, 1, 1]), (3, [5, 5, 1, 1, 3]), (5, [3, 3, 3]), (2, [5, 10]),
            (3, [7, 2, 9]), (2, [1, 50, 1, 1]), (2, [5]), (3, [1, 2, 3]), (3, [1, 100, 100, 1])],
           "Diez casos pequeños que mezclan empates, cajas sin usar y clientes de distinta duración.",
           {"wa": "Alguno de estos casos pequeños falla: localízalo por la línea y simúlalo a mano apuntando cuándo se libera cada caja. Lo más habitual es el desempate (caja de número menor) o elegir la caja que más tarde se libera."},
           ["Con «3 3 / 4 4 4» las tres cajas se liberan a la vez en 4: Ismael va a la 1.",
            "Para cada cliente: saca la caja que antes se libera (a igualdad, la de número menor), súmale su tiempo y vuelve a meterla."])
    prueba("Más cajas que clientes", "borde",
           [(5, [3, 1]), (MAXN, [MAXT]), (10, [1] * 9)],
           "Sobran cajas: Ismael va a la primera caja que nadie ha usado.",
           {"wa": "Si sobran cajas, Ismael va a la caja C + 1 (todas las libres empatan en el instante 0 y se elige la de número menor).",
            "rte": "Con N mayor que C te sales de algún vector: ¿dimensionas algo con C en lugar de N?"},
           ["Con 5 cajas y 2 clientes, las cajas 3, 4 y 5 siguen libres en el instante 0: Ismael va a la 3.",
            "Todas las cajas deben estar en la cola desde el principio, aunque no se usen."])
    prueba("Un cliente muy lento bloquea una caja", "trampa",
           [(2, [MAXT] + [1] * 30), (3, [MAXT, MAXT] + [1] * 50), (3, [1, MAXT, 1, 1, 1])],
           "Un cliente con 100 segundos ocupa una caja mientras los demás pasan por las otras.",
           {"wa": "Las cajas con clientes lentos no deben recibir a nadie hasta que se liberen: revisa que sumas el tiempo del cliente al instante de SU caja (cajero.first += tiempo)."},
           ["En el primer caso la caja 1 está ocupada hasta 100 y los 30 clientes de 1 segundo pasan por la caja 2.",
            "Cada cliente se suma al instante de la caja que saca de la cola, no a un reloj global."])
    prueba("Tiempos máximos y todas a la vez", "borde",
           [(3, [MAXT] * 7), (4, [MAXT] * 4), (2, [1] * 10)],
           "Todos los clientes tardan lo mismo: las cajas se liberan siempre en bloque.",
           {"wa": "Con todos los tiempos iguales se empata continuamente: comprueba el desempate por número de caja."},
           ["Con 4 cajas y 4 clientes de 100, las cuatro se liberan en 100: Ismael va a la 1.",
            "Revisa que el par es (instante, caja) y no (caja, instante)."])
    prueba("Varios casos seguidos", "trampa",
           [(3, [5, 1, 1, 1]), (2, [4, 4]), (1, [9]), (4, [1, 2, 3])],
           "Varios casos uno tras otro: la cola debe empezar de cero en cada caso.",
           {"wa": "El primer caso sale bien y los siguientes no: la cola (o algo) se arrastra de un caso al siguiente. Al acabar un caso la cola tiene todas sus cajas: si es global, se mezclan con las del caso siguiente.",
            "rte": "Algo del caso anterior se queda a medias: declara la cola dentro de resuelveCaso."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Declara la priority_queue dentro de resuelveCaso."])
    casos = []
    for _ in range(300):
        N = r.randint(1, 5)
        casos.append((N, [r.randint(1, r.choice([2, 5, MAXT])) for _ in range(r.randint(1, 10))]))
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "300 casos pequeños al azar, con muchos empates.",
           {"wa": "Algún caso concreto falla: la línea que falla es el número de caso; búscalo en la entrada y simúlalo a mano.",
            "rte": "Algún caso pequeño rompe el programa."},
           ["Localiza el caso por el número de línea.",
            "Apunta para cada caja el instante en que se libera y reparte los clientes uno a uno."])
    casos = []
    for _ in range(30):
        N = r.randint(1, 3000)
        casos.append((N, [r.randint(1, MAXT) for _ in range(r.randint(1, 20000))]))
    prueba("Aleatorios medianos", "aleatorio", casos,
           "30 casos de hasta 3000 cajas y 20.000 clientes.",
           {"wa": "Con casos medianos falla algo que con los pequeños no: revisa el desempate y los tipos.",
            "tle": "Ya con casos medianos va lento: ¿buscas la caja libre recorriéndolas todas?"},
           ["Comprueba que cada cliente hace un pop y un push, nada más.",
            "Revisa que el par es (instante, caja)."])
    prueba("Grande: 250.000 cajas y 500.000 clientes", "rendimiento",
           [(MAXN, [r.randint(1, MAXT) for _ in range(MAXC)])],
           "El tamaño máximo: mide la eficiencia (debe ser O((N + C) log N)).",
           {"tle": "Buscar la caja que antes se libera recorriendo las N cajas cuesta O(N·C) ≈ 10¹¹: usa la cola de prioridad, así cada cliente cuesta O(log N).",
            "wa": "Con el tamaño máximo falla algo: revisa el desempate por número de caja."},
           ["¿Cuánto cuesta atender a cada cliente? Hay 500.000.",
            "Con una cola de mínimos de pares (instante, caja), cada cliente es un pop y un push."])
    prueba("Grande: pocas cajas y 500.000 clientes", "rendimiento",
           [(7, [r.randint(1, MAXT) for _ in range(MAXC)])],
           "Muchos clientes repartidos en pocas cajas: los instantes crecen hasta millones.",
           {"wa": "Con muchos clientes los instantes llegan a ~10⁷: deben caber en int (caben), revisa que no usas short ni float.",
            "tle": "Si simulas el reloj segundo a segundo, con instantes tan grandes es demasiado lento: salta de evento en evento con la cola."},
           ["No avances el tiempo de uno en uno: la cola ya te dice qué caja se libera antes.",
            "Cada cliente: pop, sumar su tiempo, push."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida="".join(f"{caja_de_ismael(N, ts)}\n" for N, ts in c),
                   casos=len(c), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


COLA = "priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;"

VARIANTES = [
    Variante("numera las cajas desde 0", [("for (int i = 1; i <= cajas; ++i) {", "for (int i = 0; i < cajas; ++i) {")],
             prueba=2, v="wa"),
    Variante("en empate va a la caja de número mayor",
             [("cola.push(pair<int, int>(0, i));", "cola.push(pair<int, int>(0, -i));"),
              ("cout << cola.top().second << '\\n';", "cout << -cola.top().second << '\\n';")], prueba=3, v="wa"),
    Variante("comparador que solo mira el instante",
             [("bool resuelveCaso() {", "struct Cmp { bool operator()(const pair<int,int>& a, const pair<int,int>& b) const { return a.first > b.first; } };\nbool resuelveCaso() {"),
              (COLA, "priority_queue<pair<int, int>, vector<pair<int, int>>, Cmp> cola;")], prueba=3, v="wa"),
    Variante("cola de máximos (sin greater)", [(COLA, "priority_queue<pair<int, int>> cola;")], prueba=4, v="wa"),
    Variante("escribe la caja del último cliente",
             [("int clientes;", "int clientes, ultima = 0;"),
              ("pair<int, int> cajero = cola.top(); cola.pop();", "pair<int, int> cajero = cola.top(); cola.pop(); ultima = cajero.second;"),
              ("cout << cola.top().second << '\\n';", "cout << ultima << '\\n';")], prueba=5, v="wa"),
    Variante("reparte por turnos (módulo)", [("cout << cola.top().second << '\\n';", "cout << clientes % cajas + 1 << '\\n';")],
             prueba=6, v="wa"),
    Variante("cola global que no se vacía entre casos",
             [("bool resuelveCaso() {", COLA + "\nbool resuelveCaso() {"),
              ("    " + COLA + "\n\n    for", "    for")], prueba=11, v="wa"),
    Variante("formato: todo en una línea", [("cout << cola.top().second << '\\n';", "cout << cola.top().second << ' ';")],
             prueba=1, v="pe"),
    Variante("busca la caja libre recorriéndolas todas (O(N·C))",
             [("""    for (int i = 0; i < clientes; ++i) {
        int tiempo;
        cin >> tiempo;
        pair<int, int> cajero = cola.top(); cola.pop();
        cajero.first += tiempo;
        cola.push(cajero);
    }
	cout << cola.top().second << '\\n';""", """    vector<int> libre(cajas + 1, 0);
    for (int i = 0; i < clientes; ++i) {
        int tiempo;
        cin >> tiempo;
        int m = 1;
        for (int j = 2; j <= cajas; ++j) if (libre[j] < libre[m]) m = j;
        libre[m] += tiempo;
    }
    int m = 1;
    for (int j = 2; j <= cajas; ++j) if (libre[j] < libre[m]) m = j;
	cout << m << '\\n';""")], prueba=14, v="tle"),
]
