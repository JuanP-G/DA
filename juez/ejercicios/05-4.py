"""05-4 · Sumidero en un grafo dirigido: juez con pruebas pensadas para cada error típico.

Sumidero: grado de salida 0 y grado de entrada V - 1. Sin número de casos: se lee hasta el final
del fichero. Sin lazos ni aristas repetidas. El solucionador (propio) cuenta los grados.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-4/EJ_05-4.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-4/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["entrada[v] == g.V() - 1", "entrada[v] >= g.V() - 2"],
}


def sumidero(V, aristas):
    sal = [0] * V
    ent = [0] * V
    for a, b in aristas:
        sal[a] += 1
        ent[b] += 1
    s = [v for v in range(V) if sal[v] == 0 and ent[v] == V - 1]
    assert len(s) <= 1
    return f"SI {s[0]}\n" if s else "NO\n"


def caso_a_texto(c):
    V, aristas = c
    return f"{V}\n{len(aristas)}\n" + "".join(f"{a} {b}\n" for a, b in aristas)


def al_azar(rng, V, p, con_sumidero):
    aristas = {(a, b) for a in range(V) for b in range(V) if a != b and rng.random() < p}
    if con_sumidero:
        s = rng.randrange(V)
        aristas = {(a, b) for a, b in aristas if a != s} | {(a, s) for a in range(V) if a != s}
        if rng.random() < .4 and V > 2:       # «casi sumidero»: le quitamos una arista de entrada
            a = rng.choice([x for x in range(V) if x != s])
            aristas.discard((a, s))
    aristas = list(aristas)
    rng.shuffle(aristas)
    return V, aristas


def grande_con_sumidero(rng, V, A):
    s = rng.randrange(V)
    aristas = {(a, s) for a in range(V) if a != s}
    while len(aristas) < A:
        a, b = rng.sample(range(V), 2)
        if a != s:
            aristas.add((a, b))
    aristas = list(aristas)
    rng.shuffle(aristas)
    return V, aristas


def pruebas():
    rng = random.Random(544)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada="".join(caso_a_texto(c) for c in casos),
                        salida="".join(sumidero(*c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [(4, [(1, 0), (0, 2), (3, 2), (1, 2)]), (4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])],
           "Los dos grafos del PDF: el primero tiene sumidero (el 2) y el segundo no.",
           {"wa": "Si falla el ejemplo, revisa lo básico: que lees hasta el final del fichero (no hay número de casos), el sentido de las aristas (origen destino) y las dos condiciones: salida 0 y entrada V - 1.",
            "pe": "La respuesta es correcta pero el formato no: «SI», un espacio y el vértice, en la misma línea; o «NO».",
            "ole": "Escribes sin parar: no detectas el final del fichero y el bucle de casos no termina nunca."},
           ["La entrada no empieza con el número de casos: usa la plantilla de casos ilimitados (resuelveCaso devuelve false al no poder leer).",
            "En el segundo grafo el 3 tiene salida 0, pero solo le llegan 2 aristas (no 3)."])

    # ------------------------------------------------------------------ borde
    prueba("Un solo vértice", "borde", [(1, [])],
           "V = 1 y ninguna arista: el vértice 0 tiene salida 0 y entrada 0 = V - 1, así que es sumidero: «SI 0».",
           {"wa": "Con un único vértice la respuesta es «SI 0»: su entrada es 0 = V - 1. ¿Exiges que tenga alguna arista de entrada?",
            "rte": "Con V = 1 y A = 0 te sales de algún vector: revisa los bucles."},
           ["Aplica la definición: salida 0 y entrada V − 1. ¿Cuánto vale V − 1 si V = 1?",
            "No hace falta tratar este caso aparte: si cuentas bien los grados, sale solo."])
    prueba("Dos vértices", "borde", [(2, [(0, 1)]), (2, []), (2, [(0, 1), (1, 0)]), (2, [(1, 0)])],
           "Todos los grafos de dos vértices: «SI 1», «NO», «NO» y «SI 0».",
           {"wa": "Con dos vértices falla algún caso: el sumidero necesita salida 0 y entrada 1."},
           ["Sin aristas, ningún vértice tiene entrada 1.",
            "Con 0 → 1 y 1 → 0, ninguno tiene salida 0."])

    # ------------------------------------------------------------------ trampas
    prueba("Nada más después del último caso", "trampa", [(3, [(0, 1), (1, 2), (2, 0)])],
           "Un solo caso (un ciclo, sin sumidero): hay que escribir «NO» y terminar, sin líneas de más.",
           {"wa": "Escribes una línea de más al final: compruebas el final del fichero DESPUÉS de procesar y escribir un caso. Hay que comprobarlo justo después de intentar leer V.",
            "rte": "Al llegar al final del fichero la lectura de V falla y aun así usas el grafo: el Digrafo leído de un flujo que ha fallado no es válido (su V queda sin valor) y el programa se rompe. Comprueba «if (!cin) return false;» justo después de leer, antes de usarlo.",
            "ole": "El bucle de casos no termina nunca: falta detectar el final del fichero."},
           ["Mira si tu salida tiene más líneas que casos.",
            "El patrón correcto es: intentar leer V; si la lectura falla, devolver false SIN escribir nada.",
            "Con Digrafo g(cin): justo después, «if (!cin) return false;» y solo entonces resolver y escribir."])
    prueba("Salida 0 no basta", "trampa", [(4, [(0, 1)])],
           "Los vértices 1, 2 y 3 no tienen aristas de salida, pero a ninguno le llegan aristas de todos los demás: «NO».",
           {"wa": "Escribes «SI»: solo miras que la salida sea 0. El sumidero también necesita entrada V − 1 (todos los demás le apuntan)."},
           ["Al vértice 1 solo le llega una arista, y harían falta tres.",
            "Comprueba las dos condiciones: ady(v).empty() y entrada[v] == V − 1."])
    prueba("Todos le apuntan, pero él apunta a otro", "trampa", [(3, [(0, 2), (1, 2), (2, 0)])],
           "Al 2 le llegan aristas de todos, pero tiene una de salida (2 → 0): «NO».",
           {"wa": "Escribes «SI 2»: solo miras la entrada. Un sumidero no puede tener aristas de salida."},
           ["¿Qué grado de salida tiene el 2?",
            "Las aristas v → s y s → v pueden existir a la vez (no son repetidas): hay que comprobar la salida."])
    prueba("Una fuente no es un sumidero", "trampa", [(4, [(0, 1), (0, 2), (0, 3)])],
           "El 0 apunta a todos y nadie le apunta: es lo contrario de un sumidero. La respuesta es «NO».",
           {"wa": "Escribes «SI 0»: estás leyendo las aristas al revés (destino → origen) o intercambias salida y entrada. Cada línea es «origen destino»."},
           ["En «0 1», la arista va del 0 al 1: sale del 0 y entra en el 1.",
            "El grado de salida de v es ady(v).size(); el de entrada se cuenta recorriendo las listas de todos."])
    prueba("El sumidero es el último vértice", "trampa", [(4, [(0, 3), (1, 3), (2, 3), (0, 1)])],
           "El sumidero es el 3 = V − 1: «SI 3».",
           {"wa": "No encuentras un sumidero en la última posición: revisa que el bucle que busca llega hasta V − 1 (v < V, no v < V − 1)."},
           ["Recorre todos los vértices: for (v = 0; v < V; ++v).",
            "Si te sale «NO», mira los límites de tus bucles."])
    prueba("El sumidero es el vértice 0", "trampa", [(4, [(1, 0), (2, 0), (3, 0), (3, 2)])],
           "El sumidero es el 0: «SI 0».",
           {"wa": "No encuentras el sumidero cuando es el 0: ¿empiezas a buscar en 1, o usas 0 para decir «no hay sumidero»? Usa -1 para «no hay»."},
           ["El vértice 0 es un vértice como los demás.",
            "Si usas una variable «sumidero = 0» para decir que no hay, se confunde con el vértice 0: usa -1."])
    prueba("Le falta una arista para ser sumidero", "trampa", [(5, [(0, 4), (1, 4), (2, 4), (3, 0), (3, 1)])],
           "Al 4 le llegan aristas del 0, del 1 y del 2, pero no del 3: entrada 3 ≠ V − 1 = 4. «NO».",
           {"wa": "Escribes «SI 4»: comparas la entrada con algo menor que V − 1 (¿V − 2?, ¿«al menos una»?) o cuentas mal los grados. Tienen que apuntarle TODOS los demás."},
           ["Cuenta a mano cuántas aristas llegan al 4.",
            "La condición es exactamente entrada[v] == V − 1."])
    densos = []
    for V in (6, 8):
        s0 = rng.randrange(V)
        ar = [(a, b) for a in range(V) for b in range(V) if a != b and a != s0]
        rng.shuffle(ar)
        densos.append((V, ar))
    prueba("Grafo completo salvo el sumidero", "trampa", densos,
           "Todos los vértices apuntan a todos, excepto el sumidero, que no apunta a nadie: hay sumidero aunque haya muchísimas aristas.",
           {"wa": "En un grafo denso no encuentras el sumidero: ¿te paras al ver muchas aristas, o cuentas como entrada las aristas que salen?"},
           ["Solo un vértice tiene salida 0; compruébale la entrada.",
            "Cuenta la entrada recorriendo todas las listas: por cada v → w, entrada[w]++."])
    casos = [al_azar(rng, 6, .3, True), (3, [(0, 1), (1, 2), (2, 0)]), (1, []), (4, [(1, 0), (0, 2), (3, 2), (1, 2)]),
             (5, [(0, 4), (1, 4), (2, 4), (3, 4)]), (2, []), (3, [(0, 2), (1, 2)])]
    prueba("Varios casos seguidos", "trampa", casos,
           "Varios grafos seguidos, de tamaños distintos: los grados de un caso no deben sumarse al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: el vector de grados de entrada (o el grafo) no se reinicia entre casos.",
            "rte": "Un vector del caso anterior con otro tamaño: créalo dentro de cada caso con tamaño V."},
           ["Si el primer caso está bien y los demás no, mira qué variables viven fuera de resuelveCaso.",
            "Crea el vector de grados de entrada dentro de cada caso, con V ceros."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 7), rng.choice([.2, .5, .8]), rng.random() < .6) for _ in range(150)]
    prueba("Grafos pequeños al azar", "aleatorio", casos,
           "150 grafos de hasta 7 vértices; muchos tienen sumidero o se quedan a una arista de tenerlo.",
           {"wa": "Algún caso falla: cuenta qué línea es, busca ese grafo en la entrada y calcula a mano los grados."},
           ["La línea que falla es el número de caso.",
            "Para ese grafo, apunta salida y entrada de cada vértice en una tabla."])

    casos = [al_azar(rng, rng.randint(20, 120), rng.choice([.02, .1, .3]), rng.random() < .6) for _ in range(30)]
    prueba("Grafos medianos al azar", "aleatorio", casos,
           "30 grafos de 20 a 120 vértices, con y sin sumidero.",
           {"wa": "Algún caso falla: localiza la línea y revisa las dos condiciones (salida 0 y entrada V − 1)."},
           ["La línea que falla es el número de caso.",
            "Comprueba que la entrada se cuenta con el destino de cada arista."])

    # ------------------------------------------------------------------ rendimiento
    prueba("10.000 vértices y 100.000 aristas", "rendimiento", [grande_con_sumidero(rng, 10000, 100000)],
           "El caso más grande, con sumidero.",
           {"tle": "Debe ser O(V + A). ¿Usas hayArista dentro de un doble bucle o calculas el inverso para cada vértice?",
            "mle": "Una matriz de adyacencia de 10.000 × 10.000 enteros no cabe: usa listas (Digrafo).",
            "wa": "En el caso grande falla la cuenta de grados: ¿usas el tipo adecuado y recorres todas las listas?"},
           ["Los grados de entrada se cuentan en una sola pasada por todas las listas: O(V + A).",
            "No llames a g.inverso() ni recorras todos los vértices dentro del bucle que busca el sumidero."])
    casos = []
    for _ in range(30):
        V = 10000
        fuentes = rng.sample(range(V), 20)
        aristas = set()
        for a in fuentes:
            for b in rng.sample(range(V), 100):
                if b != a:
                    aristas.add((a, b))
        aristas = list(aristas)
        rng.shuffle(aristas)
        casos.append((V, aristas))
    prueba("30 grafos con casi todos los vértices sin salida", "rendimiento", casos,
           "Grafos grandes donde casi todos los vértices tienen salida 0: cada uno es candidato a sumidero.",
           {"tle": "Para cada candidato haces un trabajo de O(V) o más (hayArista desde todos, recorrer la columna de una matriz, calcular el inverso…): con 10.000 candidatos es O(V²). Cuenta los grados de entrada una sola vez."},
           ["Aquí casi todos los vértices tienen salida 0: el coste por candidato debe ser O(1).",
            "Calcula antes el vector de grados de entrada (una pasada) y luego consulta entrada[v]."])
    return P


VARIANTES = [
    Variante("comprueba el final del fichero tarde",
             [("    if (!cin) return false;\n", ""), ("    return true;\n}", "    return (bool)cin;\n}")], prueba=4, v="rte"),
    Variante("solo mira la salida 0", [("g.ady(v).empty() && entrada[v] == g.V() - 1", "g.ady(v).empty()")], prueba=5, v="wa"),
    Variante("solo mira la entrada", [("g.ady(v).empty() && entrada[v] == g.V() - 1", "entrada[v] == g.V() - 1")], prueba=6, v="wa"),
    Variante("lee las aristas al revés",
             [("Digrafo g(cin);", "Digrafo g0(cin); Digrafo g = g0.inverso();")],
             prueba=7, v="wa"),
    Variante("entrada comparada con V − 2", [("entrada[v] == g.V() - 1", "entrada[v] >= g.V() - 2")], prueba=10, v="wa"),
    Variante("el bucle no llega al último vértice",
             [("for (int v = 0; v < g.V(); ++v)\n        if (g.ady(v).empty()", "for (int v = 0; v < g.V() - 1; ++v)\n        if (g.ady(v).empty()")],
             prueba=8, v="wa"),
    Variante("empieza a buscar en el 1",
             [("for (int v = 0; v < g.V(); ++v)\n        if (g.ady(v).empty()", "for (int v = 1; v < g.V(); ++v)\n        if (g.ady(v).empty()")],
             prueba=9, v="wa"),
    Variante("grados sin reiniciar entre casos",
             [("vector<int> entrada(g.V(), 0);", "static vector<int> entrada; entrada.resize(g.V(), 0);")], prueba=12, v="wa"),
    Variante("calcula el inverso para cada candidato",
             [("g.ady(v).empty() && entrada[v] == g.V() - 1", "g.ady(v).empty() && (int)g.inverso().ady(v).size() == g.V() - 1")],
             prueba=[15, 16], v="tle"),
    Variante("SI y el vértice en líneas distintas", [("cout << \"SI \" << s << '\\n';", "cout << \"SI\\n\" << s << '\\n';")], prueba=1, v="pe"),
]
