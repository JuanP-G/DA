"""02-6 · Coleccionando cómics: juez con pruebas pensadas para cada error típico.

Formato: casos hasta fin de fichero; cada uno «N» (1..10⁵ pilas) y N líneas «K id₁ ... id_K»
(1 ≤ K ≤ 100, del fondo a la cima; ids distintos entre 1 y 10⁸; suma de K ≤ 10⁶).
Salida: por caso, el puesto (desde 1) para llevarse el menor identificador de la tienda.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "2-Colas de prioridad/EJ_02-6/EJ_02-6.cpp",
    "cabeceras": ["2-Colas de prioridad/EJ_02-6/Pila.h"],
    "limite_ms": 3000,
    "fallo": ["int puesto = 1;", "int puesto = 0;"],
}

MAXID = 10 ** 8


def puesto(pilas):
    """Simula la venta: cada cliente se lleva el menor de las cimas (último de cada lista)."""
    mejor = min(min(p) for p in pilas)
    pos = [len(p) - 1 for p in pilas]
    h = [(p[-1], i) for i, p in enumerate(pilas)]
    heapq.heapify(h)
    turno = 1
    while h[0][0] != mejor:
        _, i = heapq.heappop(h)
        pos[i] -= 1
        if pos[i] >= 0:
            heapq.heappush(h, (pilas[i][pos[i]], i))
        turno += 1
    return turno


def texto_entrada(casos):
    out = []
    for pilas in casos:
        out.append(f"{len(pilas)}\n")
        out.extend(f"{len(p)} {' '.join(map(str, p))}\n" for p in pilas)
    return "".join(out)


def caso_al_azar(r, npilas, maxk, maxid):
    tam = [r.randint(1, maxk) for _ in range(npilas)]
    ids = r.sample(range(1, maxid + 1), sum(tam))
    pilas, k = [], 0
    for t in tam:
        pilas.append(ids[k:k + t])
        k += t
    return pilas


def pruebas():
    r = random.Random(606)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, casos, comprueba, si, pistas))

    prueba("Ejemplos del enunciado", "enunciado",
           [[[5, 2, 3, 1, 20], [9, 12, 44, 13, 4, 7, 8]], [[4, 5, 6], [3, 2], [11, 8, 9, 7]], [[7, 3], [4], [20, 1, 9]]],
           "Los tres casos del PDF (la entrada acaba con el fin del fichero).",
           {"wa": "Si fallan hasta los ejemplos, revisa la base: la cima de cada pila es el ÚLTIMO número de su línea, cada cliente se lleva el menor de las cimas, y el puesto se cuenta desde 1.",
            "pe": "El puesto está bien pero no el formato: un número por línea.",
            "rte": "Se rompe con los ejemplos: ¿miras la cima de una pila que se ha quedado vacía?"},
           ["Sigue las notas del enunciado: en el primer caso se venden 8, 7, 4, 13 y 20, y el puesto es el 6.",
            "No hay número de casos ni centinela: lee hasta que falle la lectura de N (plantilla de casos ilimitados)."])
    prueba("El mejor ya está a la vista (puesto 1)", "trampa",
           [[[5]], [[9], [2], [7]]],
           "Si el mejor ejemplar ya está en una cima, basta con ser el primero: puesto 1 (no 0).",
           {"wa": "Los puestos se numeran desde 1: si el mejor está a la vista, la respuesta es 1. Si escribes 0, empieza a contar en 1 (o suma 1 al final)."},
           ["Con una sola pila de un cómic, ¿qué puesto necesitas?",
            "Cuenta el puesto del cliente que se lleva el mejor, no cuántos clientes van delante.",
            "Inicializa el contador de puestos a 1 y súmale 1 por cada cliente que compra antes que tú."])
    prueba("El mejor puede estar tapado", "trampa",
           [[[8, 1, 9]]],
           "El mejor ejemplar (el 1) está en el medio de la pila, bajo el 9: hay que buscarlo entre TODOS, no solo entre las cimas.",
           {"wa": "Buscas el mejor solo entre los que están a la vista. El que quieres es el menor de toda la tienda, aunque esté tapado: calcúlalo al leer todos los identificadores.",
            "rte": "Te quedas sin nada en la cola antes de llegar al mejor: después de vender el 9 tiene que asomar el 1. ¿Vuelves a meter en la cola la nueva cima de la pila tras cada venta?"},
           ["El mejor de la tienda es el 1; el primer cliente se lleva el 9 y tú eres el segundo.",
            "¿Dónde calculas «mejor»: con las cimas o con todos los números leídos?",
            "Actualiza mejor = min(mejor, id) con cada identificador que lees."])
    prueba("La cima es el número de la derecha", "trampa",
           [[[1, 5, 3]]],
           "Los cómics vienen del fondo a la cima: el último de la línea es el que está arriba.",
           {"wa": "Has apilado al revés: el primer número de cada línea es el FONDO y el último la CIMA. Apila en el orden en que lees (el último apilado queda arriba)."},
           ["En la pila «1 5 3» la cima es el 3: se venden el 3 y el 5, y tú eres el tercero.",
            "Si guardas cada pila en un vector, la cima es v.back(), no v[0].",
            "Lee los K números y apílalos uno a uno: el último leído queda en la cima."])
    prueba("Cada cliente se lleva el menor de las cimas", "trampa",
           [[[1, 50], [60, 9, 10]]],
           "Hay que vender siempre el MENOR de los que están a la vista: 10, 9 y 50, y luego asoma el 1.",
           {"wa": "Sale primero el MAYOR de las cimas: priority_queue<pair<int,int>> a secas es de máximos. Usa greater<> para que la cima sea el menor identificador."},
           ["Las cimas son 50 y 10: el primer cliente se lleva el 10, no el 50.",
            "¿Qué devuelve top() en una priority_queue por defecto?",
            "priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>>, con pares (identificador, número de pila)."])
    prueba("Pilas que se agotan", "trampa",
           [[[7, 3], [4], [20, 1, 9]]],
           "Antes de llegar al mejor, dos pilas se quedan vacías y dejan de ofrecer nada.",
           {"rte": "Cuando una pila se vacía, intentas consultar su cima (o desapilar de ella): la Pila lanza una excepción. Antes de volver a meter su nueva cima en la cola, comprueba que no esté vacía.",
            "wa": "Cuando una pila se vacía sigues contando con ella (por ejemplo, metiendo un valor basura en la cola). Si se vacía, simplemente no se vuelve a meter nada de ella."},
           ["Se venden 3 y 4: las dos primeras pilas se agotan.",
            "Después de desapilar, ¿qué pasa si la pila ya no tiene nada?",
            "if (!pilas[p].esVacia()) cola.push({pilas[p].cima(), p});"])
    prueba("Tras cada venta asoma el siguiente", "trampa",
           [[[3, 1, 20, 6], [30, 2, 7, 5]], [[100, 4, 2, 8], [9, 3], [50, 1, 60]]],
           "Las ventas alternan entre pilas: cada vez que se vende una cima, el cómic de debajo pasa a competir.",
           {"wa": "Después de vender una cima no vuelves a meter en la cola el cómic que queda al descubierto (o metes otro). Cada venta: pop de la cola, desapilar esa pila y, si queda algo, push de su nueva cima.",
            "rte": "Te quedas sin nada en la cola antes de llegar al mejor: tras cada venta hay que meter la nueva cima de esa pila.",
            "tle": "El bucle no termina: tras cada venta hay que meter la nueva cima de esa pila en la cola."},
           ["En el primer caso se venden 5, 6, 7, 20 (y asoma el 1): tu puesto es el 5.",
            "La cola debe tener siempre exactamente una entrada por cada pila no vacía.",
            "Guarda en la cola el par (cima, número de pila) para saber de qué pila reponer."])
    prueba("Identificadores grandes (hasta 10⁸)", "trampa",
           [[[MAXID, 99999999], [50000000, 70000000], [12345678]]],
           "Todos los identificadores son mayores que 10⁶: el valor inicial del mínimo tiene que ser mayor que cualquiera.",
           {"wa": "El mejor no se calcula bien con identificadores grandes: si inicializas el mínimo con un valor pequeño (10⁶, 100.000...), nunca se actualiza. Usa INT_MAX o el primer identificador leído.",
            "rte": "Con identificadores grandes no encuentras nunca el mejor y vacías la cola: inicializa el mínimo con INT_MAX (o con el primer identificador).",
            "tle": "No encuentras nunca el mejor y el bucle no termina: revisa el valor inicial del mínimo."},
           ["Los identificadores llegan hasta 100.000.000.",
            "¿Con qué valor empieza tu variable «mejor»?",
            "int mejor = INT_MAX; (de <climits>)."])
    prueba("Una sola pila", "borde",
           [[[3, 2, 1]], [[1, 2, 3]], [list(range(100, 0, -1))], [list(range(1, 101))]],
           "Una única pila (hasta 100 cómics): el puesto es la profundidad del mejor contando desde la cima.",
           {"wa": "Con una sola pila la respuesta es la posición del mejor contando desde la cima (empezando en 1).",
            "rte": "Con una sola pila la cola se queda vacía en algún momento: revisa la comprobación de pila vacía."},
           ["En «1 2 3» el mejor (1) está en el fondo: se venden 3 y 2 y tu puesto es el 3.",
            "Con 100 cómics del 1 al 100 (el 100 en la cima) necesitas el puesto 100."])
    prueba("El mejor, en el fondo de todo", "borde",
           [[[2, 1000]] + [[x] for x in range(999, 2, -1)], [list(range(500, 400, -1)), [1] + list(range(1000, 901, -1)), [10 ** 6] + list(range(300, 201, -1))]],
           "El mejor está en el fondo de una pila y tapado por el mayor de todos: se vende toda la tienda menos él.",
           {"wa": "Cuando hay que vender casi todo, el puesto es el número de cómics vendidos antes más 1: revisa el contador y las pilas que se agotan.",
            "rte": "Se agotan muchísimas pilas: revisa la comprobación de pila vacía antes de mirar la cima."},
           ["En el primer caso hay 997 pilas de un cómic y una pila «2 1000»: se venden todos los demás y luego el 1000.",
            "Cuenta un puesto por cada cómic vendido antes que el tuyo, y súmale 1."])
    prueba("Muchas pilas de un solo cómic", "borde",
           [[[x] for x in r.sample(range(1, 1000), 200)], [[x] for x in range(100000, 0, -1)]],
           "Muchas pilas con un cómic cada una: el mejor siempre está a la vista.",
           {"wa": "Si todas las pilas tienen un cómic, el mejor está en una cima y la respuesta es 1.",
            "tle": "Con 100.000 pilas algo es lento: ¿recorres todas las cimas en cada turno?"},
           ["Con todos los cómics a la vista, el primero de la fila se lleva el mejor.",
            "No hace falta simular nada si el mejor es la cima de la cola desde el principio."])
    prueba("Varios casos seguidos", "trampa",
           [[[5, 2, 3, 1, 20], [9, 12, 44, 13, 4, 7, 8]], [[50, 60], [70]], [[1000, 999, 998]], [[3], [1, 2]]],
           "Varios casos seguidos: el mínimo, las pilas y la cola empiezan de cero en cada caso.",
           {"wa": "El primer caso sale bien y los siguientes no: algo se arrastra entre casos (el mínimo, la cola o las pilas declarados fuera de resuelveCaso).",
            "rte": "Restos del caso anterior: si el mínimo no se reinicia, puede que no lo encuentres nunca y vacíes la cola.",
            "tle": "Si el mínimo del caso anterior no se reinicia, el bucle puede no terminar nunca."},
           ["Si el primer caso sale bien y el segundo no, mira qué variables viven fuera de resuelveCaso.",
            "Declara mejor, la cola y el vector de pilas dentro de resuelveCaso."])
    casos = [caso_al_azar(r, r.randint(1, 5), r.randint(1, 6), r.choice([30, 1000, MAXID])) for _ in range(300)]
    prueba("Aleatorios pequeños", "aleatorio", casos,
           "300 casos pequeños al azar (hasta 5 pilas de 6 cómics).",
           {"wa": "Algún caso concreto falla: la línea que falla es el número de caso; búscalo en la entrada y simúlalo a mano.",
            "rte": "Algún caso pequeño rompe el programa: casi seguro, una pila que se agota."},
           ["Localiza el caso por el número de línea.",
            "Dibuja las pilas y ve quitando en cada turno el menor de las cimas."])
    casos = [caso_al_azar(r, r.randint(10, 2000), r.randint(1, 100), MAXID) for _ in range(10)]
    prueba("Aleatorios medianos", "aleatorio", casos,
           "10 casos de hasta 2000 pilas de hasta 100 cómics.",
           {"wa": "Con casos medianos falla algo que en los pequeños no: revisa el valor inicial del mínimo y las pilas que se agotan.",
            "tle": "Ya con casos medianos va lento: ¿buscas el menor de las cimas recorriéndolas todas?"},
           ["Cada turno debe ser un pop y, como mucho, un push.",
            "Comprueba la condición de parada: la cima de la cola es el mejor."])
    # Grande: el mejor está en el fondo de una pila tapado por el mayor de todos: se vende casi todo.
    npilas, k = 50000, 5
    ids = r.sample(range(2, 260001), npilas * k - 2)
    pilas = [ids[i * k:(i + 1) * k] for i in range(npilas - 1)]
    pilas.append([1, 260001] + ids[(npilas - 1) * k:])
    r.shuffle(pilas)
    prueba("Grande: 50.000 pilas y casi todo se vende", "rendimiento",
           [pilas],
           "250.000 cómics en 50.000 pilas; el mejor está tapado por el mayor de todos, así que antes se vende casi toda la tienda.",
           {"tle": "Buscar el menor de las cimas recorriendo las N pilas en cada turno cuesta O(N·T) ≈ 10¹⁰: usa una cola de prioridad con una cima por pila.",
            "mle": "Gastas demasiada memoria: ¿copias las pilas? Guarda cada una una sola vez.",
            "rte": "Con tantas pilas se rompe algo: revisa las pilas que se agotan."},
           ["¿Cuánto cuesta cada turno? Puede haber cientos de miles.",
            "Con una cola de mínimos de pares (cima, pila), cada turno es un pop y un push: O(log N)."])
    return [Prueba(nombre, tipo, entrada=texto_entrada(c), salida="".join(f"{puesto(p)}\n" for p in c),
                   casos=len(c), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, c, comprueba, si, pistas in P]


COLA = "priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;"

VARIANTES = [
    Variante("cuenta el puesto desde 0", [("int puesto = 1;", "int puesto = 0;")], prueba=2, v="wa"),
    Variante("busca el mejor solo entre las cimas",
             [("if (id < mejor) mejor = id;", ""),
              ("cola.push({ pilas[i].cima(), i });     // la cima", "if (pilas[i].cima() < mejor) mejor = pilas[i].cima();\n        cola.push({ pilas[i].cima(), i });     // la cima")],
             prueba=3, v="wa"),
    Variante("apila al revés (el primer número en la cima)",
             [("cin >> nComics;\n", "cin >> nComics;\n        vector<int> tmp;\n"),
              ("pilas[i].apila(id);", "tmp.push_back(id);"),
              ("cola.push({ pilas[i].cima(), i });     // la cima", "for (int j = nComics - 1; j >= 0; --j) pilas[i].apila(tmp[j]);\n        cola.push({ pilas[i].cima(), i });     // la cima")],
             prueba=4, v="wa"),
    Variante("cola de máximos (sin greater)", [(COLA, "priority_queue<pair<int, int>> cola;")], prueba=5, v="wa"),
    Variante("no comprueba si la pila se ha vaciado",
             [("if (!pilas[p].esVacia())             // si queda algo, asoma el siguiente\n", "")], prueba=6, v="rte"),
    Variante("mínimo inicializado a 10⁶", [("int mejor = INT_MAX;", "int mejor = 1000000;")], prueba=8, v="rte"),
    Variante("no repone la nueva cima tras vender",
             [("            cola.push({ pilas[p].cima(), p });\n", "            ;\n")], prueba=[3, 7], v="rte"),
    Variante("formato: todo en una línea", [("cout << puesto << '\\n';", "cout << puesto << ' ';")], prueba=1, v="pe"),
    Variante("busca el menor de las cimas recorriendo todas las pilas (O(N·T))",
             [("""    int puesto = 1;
    while (cola.top().first != mejor) {
        int p = cola.top().second;
        cola.pop();
        pilas[p].desapila();                 // ese cliente se lleva la cima
        if (!pilas[p].esVacia())             // si queda algo, asoma el siguiente
            cola.push({ pilas[p].cima(), p });
        ++puesto;
    }""", """    int puesto = 1;
    while (true) {
        int p = -1;
        for (int j = 0; j < n; ++j)
            if (!pilas[j].esVacia() && (p == -1 || pilas[j].cima() < pilas[p].cima())) p = j;
        if (pilas[p].cima() == mejor) break;
        pilas[p].desapila();
        ++puesto;
    }""")], prueba=15, v="tle"),
]
