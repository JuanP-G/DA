"""eval-1 · MasterHash: juez con pruebas pensadas para cada error típico.

Digrafos: lo que necesita el plato P son sus antecesores (alcanzables desde P en el inverso); si S
está entre ellos (también si S == P) o hay un ciclo entre ellos, NO; si no, SI y un orden topológico
de exactamente esas elaboraciones (P sale el último). Vale CUALQUIER orden válido: el comprobador
(juez/ejercicios/comprobadores/eval-1.py y .js) mira que se escriban exactamente las necesarias,
una vez cada una, respetando todas las anotaciones entre ellas y acabando en P. ALTERNATIVA da otro
orden (Kahn sacando siempre la de MAYOR número) y el verificador comprueba que se acepta.

El solucionador es propio (antecesores con BFS y orden con DFS iterativo de tres colores, postorden
inverso) y se ha validado contra fuerza bruta (todas las permutaciones) en miles de grafos pequeños.
"""
import heapq
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "12-Evaluacion/EJ_Eval-1/EJ_Eval-1.cpp",
    "cabeceras": ["12-Evaluacion/EJ_Eval-1/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["if (necesaria[S]) { cout << \"NO\\n\"; return; }", ""],
}


def necesarias(n, aristas, P):
    pred = [[] for _ in range(n + 1)]
    for x, y in aristas:
        pred[y].append(x)
    nec = [False] * (n + 1)
    nec[P] = True
    cola = deque([P])
    while cola:
        v = cola.popleft()
        for w in pred[v]:
            if not nec[w]:
                nec[w] = True
                cola.append(w)
    return nec


def resuelve(n, aristas, S, P):
    """Lista con el orden, o None si no se puede hacer el plato."""
    nec = necesarias(n, aristas, P)
    if nec[S]:
        return None
    suc = [[] for _ in range(n + 1)]
    for x, y in aristas:
        if nec[x] and nec[y]:
            suc[x].append(y)
    color = [0] * (n + 1)
    post = []
    for r in range(1, n + 1):
        if not nec[r] or color[r]:
            continue
        color[r] = 1
        pila = [(r, 0)]
        while pila:
            v, i = pila[-1]
            if i < len(suc[v]):
                pila[-1] = (v, i + 1)
                w = suc[v][i]
                if color[w] == 1:
                    return None
                if color[w] == 0:
                    color[w] = 1
                    pila.append((w, 0))
            else:
                color[v] = 2
                post.append(v)
                pila.pop()
    return post[::-1]


def salida(n, aristas, S, P):
    o = resuelve(n, aristas, S, P)
    return "NO\n" if o is None else "SI " + " ".join(map(str, o)) + "\n"


def caso_a_texto(c):
    n, aristas, S, P = c
    return f"{n} {len(aristas)} {S} {P}\n" + "".join(f"{x} {y}\n" for x, y in aristas)


def aleatorio(rng, n, m, p_atras=0.0):
    """Grafo casi acíclico: aristas hacia delante en un orden al azar y alguna hacia atrás."""
    orden = list(range(1, n + 1))
    rng.shuffle(orden)
    m = min(m, n * (n - 1) // 2)
    ar = set()
    while len(ar) < m:
        i, j = rng.sample(range(n), 2)
        if i > j and rng.random() >= p_atras:
            i, j = j, i
        ar.add((orden[i], orden[j]))
    ar = list(ar)
    rng.shuffle(ar)
    return n, ar, rng.randint(1, n), orden[rng.randint(n // 2, n - 1)] if rng.random() < .8 else rng.randint(1, n)


def grande(rng, n, m, ciclo=False, quemado_dentro=False):
    """Cadena por las n − 1 primeras de una permutación (acaba en P) más aristas hacia delante.
    S es la última de la permutación (no la necesita nadie) salvo con quemado_dentro."""
    p = list(range(1, n + 1))
    rng.shuffle(p)
    P, S = p[n - 2], p[n - 1]
    ar = {(p[i], p[i + 1]) for i in range(n - 2)}
    while len(ar) < m - (1 if ciclo else 0):
        i, j = sorted(rng.sample(range(n), 2))
        ar.add((p[i], p[j]))
    if ciclo:
        i = rng.randint(n // 3, n // 2)
        ar.add((p[rng.randint(i + 1, n - 2)], p[i]))
    if quemado_dentro:
        S = p[rng.randint(0, n - 3)]
    ar = list(ar)
    rng.shuffle(ar)
    return n, ar, S, P


EXPLICA = "Si hay varios órdenes válidos vale cualquiera."


def pruebas():
    rng = random.Random(1201)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(salida(*c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado",
           [(7, [(2, 4), (3, 4), (4, 5), (5, 6), (6, 7), (7, 6), (1, 7)], 1, 5)],
           "El primer ejemplo del PDF: el ciclo 6 ↔ 7 y el quemado (1) no afectan al plato 5. " + EXPLICA,
           {"wa": "El plato 5 solo necesita 2, 3 y 4: si escribes NO, te afecta un ciclo o un quemado que el plato no necesita; si escribes otras elaboraciones, sobran.",
            "pe": "La respuesta es correcta pero no el formato: «SI» y los números en la misma línea, separados por un espacio."},
           ["Dibuja el grafo y marca qué elaboraciones llevan, siguiendo flechas, hasta la 5.",
            "Esas son las que se alcanzan desde la 5 en el grafo INVERSO.",
            "Ordena solo esas (orden topológico) y escribe «SI» seguido del orden."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(5, [(1, 3), (2, 3), (3, 4), (4, 5)], 2, 5)],
           "El segundo ejemplo del PDF: el plato 5 necesita, a través de 3 y 4, el 2, que es el quemado.",
           {"wa": "El 5 necesita el 2 indirectamente (2 → 3 → 4 → 5): hay que mirar todos los antecesores, no solo los directos."},
           ["¿Qué elaboraciones hacen falta para la 5, aunque sea de forma indirecta?",
            "Si el quemado está entre ellas, la respuesta es NO."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [(4, [(2, 3), (3, 2), (3, 4)], 1, 4)],
           "El tercer ejemplo del PDF: el 4 necesita el 3, y entre el 2 y el 3 hay un ciclo.",
           {"wa": "Hay un ciclo (2 ↔ 3) entre las elaboraciones que necesita el plato: la respuesta es NO."},
           ["¿Se puede empezar por el 2 o por el 3?",
            "Si el orden topológico de las necesarias no las incluye a todas, hay un ciclo: NO."])

    # ------------------------------------------------------------------ trampas
    prueba("Sin anotaciones: solo el plato", "trampa", [(3, [], 1, 2), (4, [], 4, 1)],
           "No hay anotaciones: el plato no necesita nada y se escribe «SI» y el propio plato.",
           {"wa": "Mira el «Por qué»: hay que escribir «SI» (sin tilde) y SOLO las elaboraciones necesarias, numeradas desde 1. Si escribes NO, quizá compruebas el ciclo comparando con N en vez de con el número de necesarias."},
           ["La respuesta del primer caso es exactamente «SI 2».",
            "Las elaboraciones van de 1 a N: si tu grafo usa 0…N − 1, resta 1 al leer y suma 1 al escribir.",
            "Escribe solo las que hacen falta para el plato y compara el tamaño del orden con cuántas son, no con N."])
    prueba("El plato es lo que se ha quemado", "trampa", [(1, [], 1, 1), (3, [(1, 3), (2, 3)], 3, 3)],
           "S y P coinciden: el propio plato está quemado y la respuesta es NO.",
           {"wa": "Si S == P el plato está quemado: NO. Fíjate en que el plato también es una elaboración «necesaria» (la última)."},
           ["¿Puede hacerse un plato que es justo lo que se ha quemado?",
            "Marca P como necesaria al empezar el recorrido y comprueba después si S está marcada."])
    prueba("Lo que depende del plato no hace falta", "trampa", [(3, [(1, 2), (2, 3)], 3, 2)],
           "1 → 2 → 3 con P = 2 y S = 3: el quemado necesita el plato, pero el plato no necesita el quemado (SI 1 2).",
           {"wa": "Recorres las flechas hacia delante desde P: eso da lo que NECESITA a P, no lo que P necesita. Hay que recorrer el grafo INVERSO."},
           ["«X Y» significa que X hace falta para Y. ¿Qué hace falta para el 2?",
            "Lo necesario para P son los vértices desde los que se llega a P: los alcanzables desde P en g.inverso()."])
    prueba("Depende del quemado indirectamente", "trampa", [(4, [(1, 2), (2, 3), (3, 4)], 1, 4)],
           "1 → 2 → 3 → 4 con S = 1 y P = 4: el plato necesita el sofrito a través de dos elaboraciones (NO).",
           {"wa": "Solo miras si S es necesaria directamente para P: hay que mirar todas las que necesita, directa o indirectamente (un recorrido completo)."},
           ["El 4 necesita el 3, que necesita el 2, que necesita el 1.",
            "Haz un recorrido (BFS o DFS) completo desde P en el inverso y mira si S queda marcada."])
    prueba("Solo las elaboraciones necesarias", "trampa", [(6, [(1, 3), (2, 3), (3, 4), (5, 6)], 6, 3)],
           "El plato 3 necesita el 1 y el 2; el 4, el 5 y el 6 no pintan nada (SI 1 2 3 o SI 2 1 3).",
           {"wa": "Escribes elaboraciones que el plato no necesita (o te faltan algunas): hay que escribir exactamente los antecesores de P y el propio P."},
           ["¿Hace falta el 4 para hacer el 3?",
            "Haz el orden topológico solo de las elaboraciones marcadas en el recorrido desde P en el inverso."])
    prueba("Un ciclo que no afecta al plato", "trampa", [(5, [(1, 2), (3, 4), (4, 3), (4, 5)], 5, 2)],
           "El 3 y el 4 forman un ciclo, pero el plato 2 solo necesita el 1: SI 1 2.",
           {"wa": "Escribes NO por un ciclo que el plato no necesita: busca el ciclo (o haz el orden topológico) solo entre las elaboraciones necesarias, no en todo el grafo."},
           ["¿Necesita el 2 alguna elaboración del ciclo?",
            "En Kahn, cuenta solo las aristas entre elaboraciones necesarias y mete en la cola solo las necesarias."])
    prueba("Un ciclo entre lo necesario", "trampa", [(5, [(1, 2), (2, 3), (3, 2), (3, 4)], 5, 4)],
           "El plato 4 necesita el 3, y el 2 y el 3 se necesitan mutuamente: NO.",
           {"wa": "Escribes un orden (incompleto) cuando hay un ciclo entre las necesarias: si Kahn no saca todas las necesarias, la respuesta es NO."},
           ["¿Sale el 2 o el 3 alguna vez de la cola de Kahn?",
            "Al acabar, compara cuántas has sacado con cuántas necesarias hay."])
    prueba("El plato dentro de un ciclo", "trampa", [(3, [(1, 2), (2, 1)], 3, 1)],
           "El plato 1 necesita el 2 y el 2 necesita el 1: NO.",
           {"wa": "El propio plato está en un ciclo: nunca queda libre en Kahn y la respuesta es NO."},
           ["¿Puede llegar a hacerse el 1 si antes hay que tener el 2, que necesita el 1?",
            "Si el orden no contiene todas las necesarias (aquí, ni siquiera el plato), escribe NO."])
    prueba("Llegar dos veces no es un ciclo", "trampa", [(5, [(1, 2), (1, 3), (2, 4), (3, 4)], 5, 4)],
           "Un rombo 1 → 2 → 4 y 1 → 3 → 4: el 1 hace falta por dos caminos, pero no hay ciclo (SI 1 2 3 4 o SI 1 3 2 4).",
           {"wa": "Escribes NO: tomas un vértice ya visitado como ciclo. En un DFS solo es ciclo si el vecino sigue en la pila; con Kahn esto no pasa."},
           ["El 4 se alcanza desde el 2 y desde el 3, y ninguno vuelve atrás.",
            "Con DFS hacen falta tres estados (sin visitar, en la pila, terminado); con Kahn, basta contar las entradas."])
    prueba("El orden no es el de los números", "trampa", [(4, [(3, 1), (1, 2)], 4, 2)],
           "3 antes que 1 y 1 antes que 2: la única respuesta es SI 3 1 2.",
           {"wa": "Escribes las necesarias ordenadas por número: hay que escribirlas en un orden que respete las anotaciones (orden topológico)."},
           ["«3 1» significa que el 3 hace falta para el 1: el 3 va antes.",
            "Saca las elaboraciones con Kahn (o con el postorden inverso de un DFS), no recorriendo 1…N."])
    casos = [grande(rng, 300, 600), (4, [(1, 2), (3, 4)], 1, 4), (2, [], 2, 1), (5, [(1, 2), (2, 3)], 4, 3),
             (3, [(1, 2), (2, 3)], 1, 3), (4, [(2, 1), (3, 1)], 4, 1)]
    prueba("Varios casos seguidos", "trampa", casos,
           "Un caso con 299 elaboraciones necesarias seguido de casos pequeños: nada de un caso debe pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: algo no se reinicia (las marcas de necesarias, los contadores de entrada o la cola).",
            "rte": "Un vector del caso anterior con otro tamaño: créalos dentro de cada caso con tamaño N."},
           ["Tras un caso grande, ¿quedan marcadas elaboraciones del caso anterior?",
            "Declara el grafo, las marcas, los contadores y el orden dentro de resuelveCaso."])

    prueba("Plato sin nada que lo necesite y elaboraciones extremas", "borde",
           [(2, [(1, 2)], 2, 1), (2, [(1, 2)], 1, 2), (6, [(6, 1), (1, 2), (2, 3), (3, 4), (4, 5)], 2, 6)],
           "Casos mínimos: el plato es la primera o la última elaboración, y un plato del que dependen todas las demás pero que no necesita ninguna.",
           {"wa": "Falla con casos mínimos: revisa que el recorrido sale de P en el grafo inverso, que P se marca como necesaria y que numeras desde 1.",
            "rte": "Te sales del vector con la elaboración N o con la 1: resta 1 al leer y suma 1 al escribir."},
           ["En el primer caso el plato 1 no necesita nada: «SI 1».",
            "En el último, el 6 es la base de todo pero no necesita nada: «SI 6», aunque el quemado (2) dependa de él."])

    # ------------------------------------------------------------------ aleatorios
    casos = [aleatorio(rng, rng.randint(1, 7), rng.randint(0, 10), rng.choice([0, 0, .1, .3])) for _ in range(200)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 grafos de hasta 7 elaboraciones, con y sin ciclos. " + EXPLICA,
           {"wa": "Algún caso falla: localízalo en la entrada (son pequeños) y dibújalo."},
           ["El «Por qué» te dice si sobra o falta una elaboración, si una va antes de tiempo o si la respuesta era NO.",
            "Comprueba los tres pasos: antecesores de P, ¿está S?, orden topológico solo de ellos."])
    casos = [aleatorio(rng, rng.randint(20, 300), rng.randint(0, 900), rng.choice([0, 0, .002, .01])) for _ in range(40)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "40 grafos de 20 a 300 elaboraciones.",
           {"wa": "Algún caso mediano falla: revisa que el recorrido desde P en el inverso es completo y que Kahn solo usa las necesarias."},
           ["Comprueba tu salida: cada anotación «X Y» entre elaboraciones escritas debe tener X antes que Y.",
            "Comprueba también que escribes todas las necesarias y ninguna más."])

    # ------------------------------------------------------------------ rendimiento
    prueba("100.000 elaboraciones y 190.000 anotaciones", "rendimiento", [grande(rng, 100000, 190000)],
           "El caso más grande: el plato necesita 99.999 elaboraciones en cadena (un único orden posible).",
           {"tle": "Debe costar O(N + A log N) o O(N + A). ¿Calculas el inverso dentro de un bucle, buscas la siguiente libre recorriendo todas (O(N²)) o usas una matriz de adyacencia?",
            "mle": "Una matriz N × N no cabe: usa listas de adyacencia (Digrafo).",
            "rte": "Con 100.000 elaboraciones se rompe: revisa los tamaños de los vectores y, si usas un DFS recursivo, que no copias vectores en cada llamada."},
           ["Calcula g.inverso() UNA vez, fuera de los bucles.",
            "Cada vértice y cada arista se deben procesar una vez (o un log por la cola de prioridad)."])
    casos = [grande(rng, 10000, 19000, ciclo=k % 3 == 1, quemado_dentro=k % 3 == 2) for k in range(6)]
    prueba("6 casos de 10.000 elaboraciones", "rendimiento", casos,
           "Varios casos grandes: uno con orden, otro con un ciclo escondido y otro que necesita el quemado.",
           {"tle": "Algo cuesta O(N²) por caso: el inverso calculado en cada vuelta, una matriz o buscar la siguiente libre recorriendo todas.",
            "wa": "En un caso grande falla la detección del ciclo o del quemado: revisa que el recorrido desde P es completo."},
           ["Con 10.000 elaboraciones, O(N²) son 10⁸ operaciones por caso.",
            "Recorrido O(N + A) y Kahn con una cola: nada más."])
    return P


VARIANTES = [
    Variante("escribe «SÍ» con tilde", [('cout << "SI";', 'cout << "SÍ";')], prueba=4, v="wa"),
    Variante("numera desde 0", [("cout << ' ' << v + 1;", "cout << ' ' << v;")], prueba=4, v="wa"),
    Variante("escribe todas las elaboraciones",
             [("if (!necesaria[v]) continue;\n        ++total;", "++total;"),
              ("if (necesaria[w]) ++entrada[w];", "++entrada[w];"),
              ("if (necesaria[v] && entrada[v] == 0) libres.push(v);", "if (entrada[v] == 0) libres.push(v);"),
              ("if (necesaria[w] && --entrada[w] == 0)", "if (--entrada[w] == 0)")],
             prueba=4, v="wa"),
    Variante("compara con N para ver el ciclo", [("if ((int)orden.size() < total)", "if ((int)orden.size() < N)")], prueba=4, v="wa"),
    Variante("olvida que S puede ser P", [("if (necesaria[S])", "if (S != P && necesaria[S])")], prueba=5, v="wa"),
    Variante("recorre el grafo y no el inverso", [("Digrafo inv = g.inverso();", "Digrafo inv = g;")], prueba=6, v="wa"),
    Variante("solo mira si S hace falta directamente", [("if (necesaria[S])", "if (S == P || g.hayArista(S, P))")], prueba=7, v="wa"),
    Variante("ciclos buscados en todo el grafo",
             [("if (!necesaria[v]) continue;\n        ++total;", "++total;"),
              ("if (necesaria[w]) ++entrada[w];", "++entrada[w];"),
              ("if (necesaria[v] && entrada[v] == 0) libres.push(v);", "if (entrada[v] == 0) libres.push(v);"),
              ("if (necesaria[w] && --entrada[w] == 0)", "if (--entrada[w] == 0)"),
              ("for (int v : orden) cout << ' ' << v + 1;", "for (int v : orden) if (necesaria[v]) cout << ' ' << v + 1;")],
             prueba=9, v="wa"),
    Variante("no detecta ciclos", [('if ((int)orden.size() < total) { cout << "NO\\n"; return; }', "")], prueba=10, v="wa"),
    Variante("necesarias en orden de número", [("for (int v : orden) cout << ' ' << v + 1;", "for (int v = 0; v < N; ++v) if (necesaria[v]) cout << ' ' << v + 1;")], prueba=13, v="wa"),
    Variante("marcas sin reiniciar entre casos", [("vector<bool> necesaria(N, false);", "static vector<bool> necesaria(100000, false);")], prueba=14, v="wa"),
    Variante("calcula el inverso en cada vuelta", [("int v = pila.back(); pila.pop_back();", "int v = pila.back(); pila.pop_back(); inv = g.inverso();")], prueba=[18, 19], v="tle"),
]


# ---------------------------------------------------------------- respuesta alternativa
def ALTERNATIVA(entrada):
    """Otro orden válido: Kahn entre las necesarias sacando siempre la de MAYOR número."""
    v = list(map(int, entrada.split()))
    p, out = 1, []
    for _ in range(v[0]):
        n, m, S, Pl = v[p:p + 4]
        p += 4
        ar = [(v[p + 2 * k], v[p + 2 * k + 1]) for k in range(m)]
        p += 2 * m
        nec = necesarias(n, ar, Pl)
        if nec[S]:
            out.append("NO")
            continue
        suc, grado = [[] for _ in range(n + 1)], [0] * (n + 1)
        for x, y in ar:
            if nec[x] and nec[y]:
                suc[x].append(y)
                grado[y] += 1
        libres = [-x for x in range(1, n + 1) if nec[x] and grado[x] == 0]
        heapq.heapify(libres)
        orden = []
        while libres:
            x = -heapq.heappop(libres)
            orden.append(x)
            for y in suc[x]:
                grado[y] -= 1
                if grado[y] == 0:
                    heapq.heappush(libres, -y)
        out.append("SI " + " ".join(map(str, orden)) if len(orden) == sum(nec) else "NO")
    return "\n".join(out) + "\n"
