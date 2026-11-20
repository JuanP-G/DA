"""05-1 · La máquina calculadora: juez con pruebas pensadas para cada error típico.

Marcador de 4 dígitos (0…9.999) con tres botones: +1, ×2 y ÷3, todo módulo 10.000 y la
división entera. Para cada caso, el mínimo de pulsaciones del número inicial al final.
El solucionador es un BFS propio en Python sobre los sucesores calculados al vuelo.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-1/EJ_05-1.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-1/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["g.ponArista(x, x / 3);", "g.ponArista(x, (x + 2) / 3);"],
}

MARCADOR = 10000


def sucesores(x):
    return ((x + 1) % MARCADOR, (x * 2) % MARCADOR, x // 3)


_cache = {}


def distancias(origen):
    """Pulsaciones mínimas desde «origen» a todos los números (BFS completo, con caché)."""
    if origen not in _cache:
        d = [-1] * MARCADOR
        d[origen] = 0
        cola = deque([origen])
        while cola:
            x = cola.popleft()
            for y in sucesores(x):
                if d[y] < 0:
                    d[y] = d[x] + 1
                    cola.append(y)
        _cache[origen] = d
    return _cache[origen]


def resuelve(casos):
    return "".join(f"{distancias(a)[b]}\n" for a, b in casos)


def pruebas():
    rng = random.Random(519)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(f"{a} {b}\n" for a, b in casos),
                        salida=resuelve(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado", [(0, 1024), (5000, 0), (9999, 6666), (4242, 4242)],
           "Los cuatro casos del PDF: 11, 1, 2 y 0 pulsaciones.",
           {"wa": "Si falla hasta el ejemplo, revisa lo básico: la lectura (primero el número de casos, luego «inicial final»), los tres botones y que el recorrido sea un BFS.",
            "pe": "Los números son correctos pero el formato no: escribe un número por línea, sin texto adicional.",
            "rte": "El programa se rompe con el ejemplo: casi seguro un índice fuera del marcador (un número ≥ 10.000 o negativo)."},
           ["Ejecuta tu programa con este ejemplo y compara caso a caso: ¿cuál de los cuatro sale mal?",
            "El segundo caso (5.000 → 0) necesita que ×2 «dé la vuelta»: 10.000 se ve como 0000. El tercero usa ÷3 y luego ×2.",
            "El último caso pide llegar al número que ya está en el marcador: 0 pulsaciones."])

    # ------------------------------------------------------------------ borde
    prueba("Origen igual al destino", "borde", [(1, 1), (9999, 9999), (5000, 5000), (3333, 3333)],
           "Si el número final ya está en el marcador, la respuesta es 0.",
           {"wa": "Cuando inicial y final coinciden debe salir 0. Si sale otra cosa, compruebas el destino al meter en la cola (y nunca miras el propio origen) o cuentas mal la distancia del origen."},
           ["¿Qué escribe tu programa con «1 1»?",
            "La distancia del origen a sí mismo es 0: ponla así antes de empezar el BFS.",
            "Comprueba si has llegado al destino al SACAR cada número de la cola (así el origen también se comprueba)."])
    prueba("Una sola pulsación", "borde", [(100, 101), (100, 200), (100, 33), (4999, 9998), (2, 0)],
           "Destinos a los que se llega pulsando un único botón: la respuesta es 1.",
           {"wa": "Fallas casos de una sola pulsación: revisa que los tres botones están bien programados (+1, ×2 y ÷3 con división entera) y que la distancia del vecino es la del actual más 1."},
           ["Comprueba cada botón por separado: 100 +1 = 101, 100 ×2 = 200, 100 ÷3 = 33.",
            "La distancia de un vecino recién descubierto es dist[actual] + 1, no un contador global de pasos."])
    prueba("Del 0 al 9.999 y vuelta", "borde", [(0, 9999), (9999, 0), (0, 1), (0, 2)],
           "Los dos extremos del marcador.",
           {"wa": "Algo falla en los extremos del marcador: del 9.999 se pasa al 0 con +1 (módulo 10.000), y desde el 0 solo sirve +1 al principio.",
            "rte": "Te sales del marcador en un extremo: el 9.999 +1 debe dar 0, no 10.000."},
           ["Del 9.999 al 0 basta una pulsación (+1 da la vuelta).",
            "Del 0 al 2 hacen falta dos: +1 y luego +1 o ×2 (en el 0, ×2 y ÷3 dejan 0)."])

    # ------------------------------------------------------------------ trampas
    prueba("Se cuentan pulsaciones, no números", "trampa", [(100, 101)],
           "Del 100 al 101 hay UNA pulsación (+1), aunque el camino tenga dos números.",
           {"wa": "Te sale 2: cuentas los números del camino (vértices) en vez de las pulsaciones (aristas), o empiezas la distancia del origen en 1."},
           ["Una pulsación es una arista del grafo: el camino 100 → 101 tiene una arista.",
            "La distancia del origen es 0 y la de cada vecino descubierto es la del actual más 1."])
    prueba("Del 0 al 0: los botones ×2 y ÷3 no mueven el 0", "trampa", [(0, 0)],
           "En el 0, ×2 y ÷3 vuelven al 0 (son lazos): del 0 al 0 hacen falta 0 pulsaciones, no 1.",
           {"wa": "Del 0 al 0 debe salir 0. Si sale 1, el origen no está marcado como visitado al empezar y lo «redescubres» con ×2 o ÷3 (que llevan del 0 al 0); o miras el destino solo al meter vecinos en la cola."},
           ["En el 0, pulsar ×2 o ÷3 deja otra vez 0: es una arista del 0 a sí mismo.",
            "Marca el origen como visitado (dist = 0) ANTES de empezar a sacar de la cola.",
            "Si compruebas el destino al meter un vecino, el caso origen = destino nunca pasa por ahí: compruébalo al sacar de la cola."])
    prueba("El mínimo exige un BFS (724 → 2.896)", "trampa", [(724, 2896)],
           "724 ×2 ×2 = 2.896: dos pulsaciones. Un recorrido en profundidad (DFS) encuentra antes un camino mucho más largo.",
           {"wa": "Te sale más de 2: tu recorrido no es en anchura. Con una pila (DFS) o con una recursión, la primera vez que llegas a un número no tiene por qué ser por el camino más corto.",
            "tle": "Pruebas todos los caminos (vuelta atrás o recursión sin marcar visitados): el número de caminos crece de forma exponencial. Hace falta un BFS que visite cada número una sola vez."},
           ["Para «el mínimo número de pulsaciones» la herramienta es el BFS: visita los números por capas (1 pulsación, 2, 3…).",
            "¿Usas una cola (queue) y sacas por delante? Una pila o una recursión dan un DFS.",
            "En el BFS, la distancia de un número se fija la primera vez que se descubre: dist[y] = dist[x] + 1."])
    prueba("+1 da la vuelta: 9.999 → 0", "trampa", [(9999, 0)],
           "Con 9.999 en el marcador, +1 da 10.000, que en cuatro dígitos es 0000: una sola pulsación.",
           {"wa": "Te sale más de 1: no permites pulsar +1 en el 9.999 o no aplicas el módulo. El marcador tiene 4 dígitos: (x + 1) mod 10.000.",
            "rte": "Te sales del vector: 9.999 + 1 = 10.000 (o x·2 ≥ 10.000) no es un número del marcador. Aplica «% 10000» a +1 y a ×2."},
           ["El enunciado dice que TODAS las operaciones se hacen módulo 10.000.",
            "El sucesor de x con +1 es (x + 1) % 10000, también cuando x = 9.999."])
    prueba("×2 da la vuelta: 7.500 → 5.000", "trampa", [(7500, 5000)],
           "7.500 ×2 = 15.000, que en el marcador se ve como 5.000: una sola pulsación.",
           {"wa": "Te sale más de 1: no aplicas el módulo a ×2 o prohíbes pulsarlo cuando el resultado pasa de 9.999. El marcador se queda con las cuatro últimas cifras.",
            "rte": "x·2 puede llegar a 19.998: sin «% 10000» te sales del vector de distancias."},
           ["No es que el botón no funcione: el marcador muestra las cuatro últimas cifras.",
            "El sucesor de x con ×2 es (x * 2) % 10000."])
    prueba("÷3 con resto: 9.998 → 3.332", "trampa", [(9998, 3332)],
           "9.998 / 3 = 3.332,67: la división es entera (se queda en 3.332). Una sola pulsación.",
           {"wa": "Te sale más de 1: falta el botón ÷3, o redondeas la división (hacia arriba o al más cercano) en vez de quedarte con la parte entera."},
           ["¿Tienes los tres botones? Es fácil olvidar el ÷3.",
            "La división del marcador es entera: 9.998 / 3 = 3.332 (en C++, con enteros, x / 3 ya trunca).",
            "No uses (x + 2) / 3, round ni ceil: el enunciado dice que la división es entera."])
    prueba("El grafo es dirigido: del 0 al 5.000", "trampa", [(0, 5000)],
           "5.000 ×2 = 0, pero del 0 no se llega al 5.000 con un botón: hacen falta 17 pulsaciones.",
           {"wa": "Te sale menos de 17 (seguramente 1): estás recorriendo las aristas al revés o en los dos sentidos. Pulsar un botón no se puede deshacer: el grafo es DIRIGIDO."},
           ["De 5.000 se llega a 0 con ×2. ¿Se puede ir del 0 al 5.000 con un botón?",
            "Usa la clase Digrafo (no Grafo): ponArista(v, w) añade solo v → w.",
            "Los sucesores de x son (x+1) % 10000, (x*2) % 10000 y x/3, y nada más."])
    prueba("El destino más lejano: 23 pulsaciones", "trampa", [(0, 6015)],
           "Del 0 al 6.015 hacen falta 23 pulsaciones, el máximo posible desde el 0.",
           {"wa": "En distancias largas te equivocas: ¿limitas la profundidad de la búsqueda, o paras el BFS antes de vaciar la cola?",
            "tle": "Exploras de más: cada número debe entrar en la cola una sola vez (márcalo al meterlo).",
            "mle": "La cola crece sin control: marca cada número como visitado al meterlo en la cola, no al sacarlo."},
           ["No pongas un tope a la profundidad: el BFS termina solo cuando saca el destino.",
            "Marca los números como visitados al meterlos en la cola; así la cola nunca tiene más de 10.000 elementos."])
    prueba("Varios casos seguidos", "trampa",
           [(0, 6015), (6015, 0), (0, 1024), (1024, 0), (5000, 0), (0, 5000), (17, 17), (9999, 6666)],
           "Varios casos en la misma entrada: las distancias de un caso no deben servir para el siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: el vector de distancias (o de visitados) no se reinicia entre casos.",
            "rte": "Algo de un caso anterior se reutiliza mal: crea el vector de distancias dentro de cada caso."},
           ["Si el primer caso está bien y los demás no, mira qué variables viven fuera de resuelveCaso.",
            "El grafo SÍ se puede construir una vez para todos los casos (no depende del caso), pero las distancias y visitados son de cada BFS: créalos de nuevo en cada caso."])
    prueba("Los tres botones en el mismo camino", "trampa", [(9999, 1112)],
           "9.999 ÷3 = 3.333, ÷3 = 1.111, +1 = 1.112: el camino mínimo combina ÷3 y +1.",
           {"wa": "El camino mínimo usa ÷3 dos veces y luego +1: revisa que los tres botones están en los sucesores de cada número."},
           ["Calcula a mano: 9.999 → 3.333 → 1.111 → 1.112.",
            "Cada número tiene exactamente tres sucesores: x+1, 2x y x/3 (con el módulo)."])

    # ------------------------------------------------------------------ aleatorios
    casos = [(rng.randrange(MARCADOR), rng.randrange(MARCADOR)) for _ in range(150)]
    prueba("Parejas al azar", "aleatorio", casos,
           "150 parejas de números al azar.",
           {"wa": "Hay algún caso que no tratas bien: localiza la línea que falla, busca ese caso en la entrada y sigue tu BFS a mano."},
           ["La línea que falla es el número de caso: mira qué pareja es.",
            "Comprueba si el camino mínimo de ese caso usa la vuelta del marcador (+1 en 9.999, ×2 por encima de 5.000) o el ÷3."])
    casos = []
    for _ in range(80):
        x = rng.randrange(MARCADOR)
        casos.append((x, 0) if rng.random() < .5 else (0, x))
    prueba("Hacia el 0 y desde el 0", "aleatorio", casos,
           "80 casos que salen del 0 o llegan al 0.",
           {"wa": "Fallas casos con el 0: recuerda que en el 0 ×2 y ÷3 no hacen nada y que al 0 se llega dando la vuelta (9.999 +1, 5.000 ×2) o dividiendo (1 ÷3, 2 ÷3)."},
           ["Al 0 se puede llegar de varias formas: 1 ÷3, 2 ÷3, 9.999 +1 o 5.000 ×2.",
            "Desde el 0 el único botón útil al principio es +1."])

    # ------------------------------------------------------------------ rendimiento
    fuentes = [rng.randrange(MARCADOR) for _ in range(120)]
    lejanos = []
    for _ in range(2000):
        s = rng.choice(fuentes)
        d = distancias(s)
        m = max(d)
        lejanos.append((s, rng.choice([v for v in range(MARCADOR) if d[v] >= m - 1])))
    prueba("2.000 casos con destinos muy lejanos", "rendimiento", lejanos,
           "El máximo de casos (2.000), todos con un destino entre los más lejanos: cada BFS recorre casi todo el marcador.",
           {"tle": "Cada caso debería costar O(10.000). ¿Vuelves a construir el grafo en cada caso, copias estructuras grandes o no marcas los visitados al meterlos en la cola?",
            "mle": "Demasiada memoria: no metas un número en la cola más de una vez y no guardes caminos completos.",
            "wa": "Con muchos casos seguidos algo se arrastra de uno a otro: reinicia las distancias en cada caso."},
           ["El grafo no depende del caso: puedes construirlo una sola vez (por ejemplo, static) y hacer solo el BFS en cada caso.",
            "Pasa el grafo por referencia (const&): copiarlo en cada caso o en cada llamada es muy caro.",
            "Marca un número como visitado cuando lo metes en la cola; si lo marcas al sacarlo, puede entrar muchas veces."])
    casos = [(rng.choice(fuentes), rng.randrange(MARCADOR)) for _ in range(2000)]
    prueba("2.000 casos al azar", "rendimiento", casos,
           "2.000 casos con destinos al azar.",
           {"tle": "Tu solución es lenta con el máximo de casos: cada BFS debe visitar cada número como mucho una vez.",
            "wa": "Con muchos casos aparece algún error: mira la línea que falla y reproduce ese caso."},
           ["Mide cuánto tarda un caso: con 2.000 casos, cada uno debe tardar muy poco (≈ 10⁴ operaciones).",
            "Construye el grafo una sola vez, fuera del bucle de casos."])
    return P


VARIANTES = [
    Variante("comprueba el destino al meter en la cola",
             [("if (x == final_) { pulsaciones = dist[x]; return; }   // ya no hace falta seguir", ""),
              ("dist[y] = dist[x] + 1;\n                    q.push(y);",
               "dist[y] = dist[x] + 1;\n                    if (y == final_) { pulsaciones = dist[y]; return; }\n                    q.push(y);")],
             prueba=6, v="wa"),
    Variante("DFS (pila) en vez de BFS",
             [("queue<int> q;", "deque<int> q;"), ("int x = q.front(); q.pop();", "int x = q.back(); q.pop_back();"),
              ("q.push(inicial);", "q.push_back(inicial);"), ("q.push(y);", "q.push_back(y);")],
             prueba=7, v="wa"),
    Variante("+1 no da la vuelta en el 9.999",
             [("g.ponArista(x, (x + 1) % MARCADOR);", "if (x + 1 < MARCADOR) g.ponArista(x, x + 1);")], prueba=8, v="wa"),
    Variante("×2 no da la vuelta",
             [("g.ponArista(x, (x * 2) % MARCADOR);", "if (x * 2 < MARCADOR) g.ponArista(x, x * 2);")], prueba=9, v="wa"),
    Variante("sin módulo (se sale del marcador)",
             [("g.ponArista(x, (x + 1) % MARCADOR);", "g.ponArista(x, x + 1);")], prueba=8, v="rte"),
    Variante("sin el botón ÷3", [("g.ponArista(x, x / 3);                // boton /3 (division entera)", "")], prueba=10, v="wa"),
    Variante("÷3 redondeando hacia arriba", [("g.ponArista(x, x / 3);", "g.ponArista(x, (x + 2) / 3);")], prueba=10, v="wa"),
    Variante("grafo no dirigido",
             [("g.ponArista(x, x / 3);                // boton /3 (division entera)",
               "g.ponArista(x, x / 3);\n        g.ponArista((x + 1) % MARCADOR, x); g.ponArista((x * 2) % MARCADOR, x); g.ponArista(x / 3, x);")],
             prueba=11, v="wa"),
    Variante("distancias sin reiniciar entre casos",
             [("    vector<int> dist;   // dist[x]", "    static vector<int> dist;   // dist[x]"),
              ("dist(g.V(), -1), pulsaciones(-1) {", "pulsaciones(-1) {\n        if (dist.empty()) dist.assign(g.V(), -1);"),
              ("};\n\n// el grafo de la maquina", "};\nvector<int> MaquinaCalculadora::dist;\n\n// el grafo de la maquina")],
             prueba=13, v="wa"),
    Variante("cuenta números en vez de pulsaciones", [("pulsaciones = dist[x];", "pulsaciones = dist[x] + 1;")], prueba=5, v="wa"),
    Variante("todo en una línea", [("cout << mc.minimoPulsaciones() << '\\n';", "cout << mc.minimoPulsaciones() << ' ';")], prueba=1, v="pe"),
]
