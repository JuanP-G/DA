"""05-6 · Sistema de inecuaciones: juez con pruebas pensadas para cada error típico.

El enunciado admite cualquier asignación válida y el juez la acepta: juez/ejercicios/comprobadores/
05-6.py (servidor) y 05-6.js (navegador) comprueban que la salida cumple todas las inecuaciones.
La salida esperada (la posición de cada variable en el orden topológico, desde 1) es solo una de
ellas. ALTERNATIVA da otra distinta y el verificador comprueba que también se acepta.
El solucionador es propio (DFS iterativo con tres colores), validado contra fuerza bruta.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-6/EJ_05-6.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-6/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["valor[post[i]] = n - i;", "valor[post[i]] = i + 1;"],
}


def asigna(n, aristas):
    """Posición (1…n) en el postorden inverso del DFS, o None si hay ciclo."""
    ady = [[] for _ in range(n + 1)]
    for a, b in aristas:
        ady[a].append(b)
    color = [0] * (n + 1)
    post = []
    for r in range(1, n + 1):
        if color[r]:
            continue
        color[r] = 1
        pila = [(r, 0)]
        while pila:
            v, i = pila[-1]
            if i < len(ady[v]):
                pila[-1] = (v, i + 1)
                w = ady[v][i]
                if color[w] == 1:
                    return None
                if color[w] == 0:
                    color[w] = 1
                    pila.append((w, 0))
            else:
                color[v] = 2
                post.append(v)
                pila.pop()
    valor = [0] * (n + 1)
    for i, v in enumerate(post):
        valor[v] = n - i
    return valor[1:]


def salida(n, aristas):
    v = asigna(n, aristas)
    return "NO\n" if v is None else "SI " + " ".join(map(str, v)) + "\n"


def dag_unico(rng, n, extra, ciclo=False, repetidas=0):
    p = list(range(1, n + 1))
    rng.shuffle(p)
    aristas = {(p[i], p[i + 1]) for i in range(n - 1)}
    tope = n * (n - 1) // 2
    while len(aristas) < min(tope, n - 1 + extra):
        i, j = sorted(rng.sample(range(n), 2))
        aristas.add((p[i], p[j]))
    aristas = list(aristas)
    if aristas:
        aristas += [rng.choice(aristas) for _ in range(repetidas)]
    if ciclo and n >= 2:
        i, j = sorted(rng.sample(range(n), 2))
        aristas.append((p[j], p[i]))
    rng.shuffle(aristas)
    return n, aristas


def caso_a_texto(c):
    n, aristas = c
    return f"{n}\n{len(aristas)}\n" + "".join(f"{a} {b}\n" for a, b in aristas)


CONVENIO = "Vale cualquier asignación que cumpla todas las inecuaciones: la salida esperada es solo una de ellas."


def pruebas():
    rng = random.Random(566)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(salida(*c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado", [(4, [(1, 3), (3, 2), (2, 4), (3, 4), (1, 4)])],
           "El primer ejemplo del PDF: cinco inecuaciones. " + CONVENIO + " (por ejemplo «SI 2 5 3 7», la del PDF).",
           {"wa": "Tu asignación no cumple alguna inecuación (el «Por qué» te dice cuál) o le falta el valor de alguna variable. Revisa el orden topológico y el sentido de cada inecuación.",
            "pe": "Los valores son correctos pero el formato no: «SI» y los N valores en UNA línea, separados por espacios.",
            "rte": "Se rompe con el ejemplo: las variables van de 1 a N; lee con Digrafo g(cin, 1) o resta 1."},
           ["Comprueba a mano que tu asignación cumple las cinco inecuaciones.",
            "Calcula un orden topológico (postorden inverso del DFS) y da a cada variable su posición en él: así se cumplen todas.",
            "Con el postorden post (en el orden en que terminan), por ejemplo valor[post[i]] = N − i."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(3, [(1, 2), (2, 1)])],
           "El segundo ejemplo: x1 < x2 y x2 < x1 a la vez es imposible: «NO».",
           {"wa": "Con un ciclo hay que escribir «NO» (sin valores). Si escribes «SI…», no detectas los ciclos."},
           ["¿Hay algún par de valores que cumpla x1 < x2 y x2 < x1?",
            "En el DFS, un vecino que sigue en la pila (estado 1) cierra un ciclo."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [(3, [(3, 1)])],
           "El tercer ejemplo: x2 no aparece en ninguna inecuación y aun así necesita valor. " + CONVENIO,
           {"wa": "Te falta el valor de alguna variable (x2 también lo necesita) o no se cumple x3 < x1.",
            "pe": "Formato: «SI» y los valores en una sola línea."},
           ["Toda variable, aparezca o no, lleva valor.",
            "Lanza el DFS desde cada variable sin visitar (también x2) y da a cada una su posición en el orden."])

    # ------------------------------------------------------------------ borde
    prueba("Dos variables", "borde", [(2, [(1, 2)]), (2, [(2, 1)]), (2, [(1, 2), (1, 2)])],
           "Dos variables con una inecuación (una vez repetida).",
           {"wa": "Revisa el sentido: «i j» significa xi < xj, así que xi necesita un valor MENOR que xj."},
           ["«2 1» significa x2 < x1: x2 va primero y vale 1.",
            "Si das a cada variable su posición en el orden topológico, se cumplen todas."])

    # ------------------------------------------------------------------ trampas
    prueba("Una variable y ninguna inecuación", "trampa", [(1, [])],
           "Una sola variable sin inecuaciones: siempre hay solución, «SI» y un valor cualquiera.",
           {"wa": "Sin inecuaciones siempre hay solución: hay que escribir SI y un valor (por ejemplo «SI 1»). Si sale NO o falta el valor, revisa el caso M = 0.",
            "rte": "Con N = 1 y M = 0 algo se sale de rango: revisa los índices."},
           ["Sin inecuaciones, ¿puede no haber solución?",
            "Escribe SI y un valor por cada variable, aunque no aparezca en ninguna inecuación."])
    prueba("El primero en terminar es el mayor", "trampa", [(3, [(1, 2), (2, 3)])],
           "x1 < x2 < x3: «SI 1 2 3».",
           {"wa": "Escribes «SI 3 2 1»: asignas los valores al revés (el primero en terminar el DFS recibe 1) o has puesto las aristas al revés. La arista de «i j» es i → j y j termina antes que i."},
           ["¿Qué variable termina primero el DFS que empieza en x1?",
            "La que termina primero es la última del orden: debe recibir el valor más alto, N.",
            "Comprueba también el sentido: «i j» es xi < xj, arista i → j."])
    prueba("Llegar dos veces a una variable no es un ciclo", "trampa", [(3, [(1, 2), (2, 3), (1, 3)])],
           "x3 se alcanza desde x1 y desde x2, pero no hay ciclo: «SI 1 2 3».",
           {"wa": "Escribes «NO»: tomas cualquier vecino ya visitado como un ciclo. Solo hay ciclo si el vecino sigue en la pila del DFS (estado 1)."},
           ["Cuando el DFS vuelve a x1, su vecino x3 ya ha terminado: no está en el camino actual.",
            "Usa tres estados: 0 sin visitar, 1 en la pila, 2 terminado; ciclo solo con estado 1."])
    prueba("El orden de visita (preorden) no sirve", "trampa", [(3, [(1, 2), (1, 3), (3, 2)])],
           "x1 < x2, x1 < x3 y x3 < x2: «SI 1 3 2».",
           {"wa": "Escribes «SI 1 2 3»: das valores crecientes en el orden en que el DFS ENTRA en las variables. Hay que usar el orden en que TERMINAN (postorden) e invertirlo."},
           ["El DFS desde x1 entra antes en x2 que en x3, pero x3 < x2.",
            "Guarda cada variable al terminar su DFS; el postorden al revés es el orden topológico."])
    prueba("Variables a las que no se llega desde x1", "trampa", [(3, [(2, 1), (3, 2)])],
           "x3 < x2 < x1: «SI 3 2 1». Desde x1 no sale ninguna inecuación.",
           {"wa": "Te faltan valores (salen 0 o basura): lanzas el DFS solo desde x1. Hay que lanzarlo desde CADA variable sin visitar."},
           ["¿Qué valor das a x2 y x3?",
            "Recorre v = 1…N y lanza el DFS desde cada v no visitada."])
    prueba("Ciclo de dos que no incluye x1", "trampa", [(3, [(1, 2), (2, 3), (3, 2)])],
           "x2 < x3 y x3 < x2: «NO», aunque x1 no esté en el ciclo.",
           {"wa": "Escribes «SI…»: no detectas el ciclo. Un vecino que sigue en la pila cierra un ciclo, sea cual sea la variable de partida."},
           ["Sigue el DFS: x1 → x2 → x3, y desde x3 se ve x2, que sigue en la pila.",
            "Si hay ciclo, escribe solo «NO»."])
    prueba("Ciclo de tres variables", "trampa", [(4, [(1, 2), (2, 3), (3, 4), (4, 2)])],
           "x2 < x3 < x4 < x2: «NO».",
           {"wa": "Detectas ciclos de dos variables pero no los más largos: no basta con mirar si están «i j» y «j i». Usa el estado «en la pila»."},
           ["Un ciclo puede tener cualquier longitud.",
            "Vecino en estado 1 ⇒ ciclo, mida lo que mida."])
    prueba("Inecuaciones repetidas", "trampa", [(3, [(1, 2), (2, 3), (1, 2), (2, 3), (1, 2)])],
           "La misma inecuación puede aparecer varias veces (lo permite el enunciado): no es un ciclo. «SI 1 2 3».",
           {"wa": "Una inecuación repetida no cambia nada: ¿la tomas por un ciclo, o tu algoritmo de Kahn resta mal los grados de entrada?"},
           ["Una arista repetida lleva a una variable ya terminada: no está en la pila.",
            "Con Kahn, cada repetición suma 1 al grado de entrada y también resta 1 al procesarla."])
    casos = [dag_unico(rng, 6, 3, ciclo=True), dag_unico(rng, 5, 2), (1, []), dag_unico(rng, 7, 4, ciclo=True),
             dag_unico(rng, 4, 1, repetidas=2), (2, [(1, 2), (2, 1)]), dag_unico(rng, 8, 6)]
    prueba("Varios casos seguidos", "trampa", casos,
           "Sistemas con y sin solución alternados: nada de un caso (estados, «hay ciclo», el postorden, los valores) debe pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: algo no se reinicia entre casos (el indicador de ciclo, los estados o la lista del postorden).",
            "rte": "Un vector del caso anterior con otro tamaño: créalos dentro de cada caso."},
           ["Tras un «NO», ¿vuelves a poner «no hay ciclo»?",
            "Declara todo (grafo, estados, postorden, valores, indicador) dentro de resuelveCaso o en un objeto nuevo por caso."])
    prueba("Muchas inecuaciones sin ciclo", "trampa", [dag_unico(rng, 9, 40, repetidas=10)],
           "Nueve variables con todas las inecuaciones posibles hacia delante (y algunas repetidas): más inecuaciones que variables no implica ciclo.",
           {"wa": "Hay muchas aristas hacia variables ya terminadas y ninguna cierra un ciclo: ¿deduces «NO» por el número de inecuaciones o por ver una variable ya visitada?"},
           ["Sin ciclos puede haber muchísimas aristas.",
            "Solo hay ciclo con un vecino que está en la pila en ese momento."])

    # ------------------------------------------------------------------ aleatorios
    casos = [dag_unico(rng, rng.randint(1, 8), rng.randint(0, 8), ciclo=rng.random() < .3, repetidas=rng.randint(0, 2))
             for _ in range(120)]
    casos[0] = dag_unico(rng, 5, 2, ciclo=True)
    prueba("Sistemas pequeños al azar (orden único)", "aleatorio", casos,
           "120 sistemas de hasta 8 variables; los que tienen solución admiten un único orden.",
           {"wa": "Algún caso falla: localiza la línea, busca el sistema y compruébalo a mano."},
           ["La línea que falla es el número de caso.",
            "Comprueba si es un ciclo que no detectas o una inecuación que tu asignación no cumple."])
    casos = [dag_unico(rng, rng.randint(50, 300), rng.randint(0, 600), ciclo=rng.random() < .3, repetidas=rng.randint(0, 20))
             for _ in range(30)]
    prueba("Sistemas medianos al azar (orden único)", "aleatorio", casos,
           "30 sistemas de 50 a 300 variables, con y sin solución.",
           {"wa": "Algún caso falla: si debía ser «NO», revisa la detección de ciclos; si no, comprueba que cada xi < xj se cumple con tus valores."},
           ["Comprueba tu salida: para cada «i j», el valor de xi debe ser menor que el de xj.",
            "Un ciclo largo solo se detecta con el estado «en la pila»."])

    # ------------------------------------------------------------------ rendimiento
    prueba("10.000 variables en cadena y 100.000 inecuaciones", "rendimiento", [dag_unico(rng, 10000, 80001, repetidas=10000)],
           "El caso más grande: un único orden posible y una recursión de 10.000 niveles.",
           {"tle": "Debe ser O(N + M). ¿Matriz de adyacencia, Kahn buscando la siguiente variable recorriendo todas, o copiar el grafo en cada llamada?",
            "mle": "Demasiada memoria: una matriz N × N o copiar el grafo en cada llamada recursiva. Pasa el grafo por referencia (const&).",
            "rte": "Con 10.000 niveles de recursión no debería romperse aquí; revisa que no declaras vectores grandes dentro de la función recursiva.",
            "wa": "En el caso grande falla algo: revisa el postorden y la asignación de posiciones."},
           ["Pasa el grafo por referencia (Digrafo const& g) a la función recursiva.",
            "Cada variable y cada inecuación se procesan una vez: O(N + M)."])
    casos = []
    for _ in range(50):
        a, b = rng.sample(range(1, 10001), 2)
        casos.append((10000, [(a, b), (b, a)]))
    prueba("50 sistemas de 10.000 variables con un ciclo", "rendimiento", casos,
           "La suma de N llega al máximo (500.000) con casi todas las variables sueltas: mide el coste por variable.",
           {"tle": "Algo cuesta O(N²) por caso: una matriz N × N, Kahn buscando la siguiente variable libre recorriendo todas, o copiar el grafo en cada llamada al DFS."},
           ["Con 10.000 variables, O(N²) son 10⁸ operaciones por caso: demasiado con 50 casos.",
            "Usa listas de adyacencia y pasa el grafo por referencia."])
    n = 10000
    prueba("Ciclo que pasa por las 10.000 variables", "rendimiento", [(n, [(i, i + 1) for i in range(1, n)] + [(n, 1)])],
           "x1 < x2 < … < x10.000 < x1: un ciclo enorme detectado en lo más profundo de la recursión.",
           {"wa": "Un ciclo muy largo también hace el sistema imposible: «NO».",
            "tle": "Detectar el ciclo debe costar O(N + M).",
            "mle": "Demasiada memoria en una recursión de 10.000 niveles: ¿copias el grafo o vectores en cada llamada?"},
           ["El DFS llega a x10.000 y ve x1, que sigue en la pila.",
            "Pasa todo por referencia en la recursión."])
    return P


VARIANTES = [
    Variante("valores al revés", [("valor[post[i]] = n - i;", "valor[post[i]] = i + 1;")], prueba=6, v="wa"),
    Variante("inecuaciones al revés", [("Digrafo g(cin, 1);", "Digrafo g0(cin, 1); Digrafo g = g0.inverso();")], prueba=6, v="wa"),
    Variante("cualquier visitado es un ciclo", [("if (estado[w] == 1) hayCiclo = true;", "if (estado[w] != 0) hayCiclo = true;")], prueba=7, v="wa"),
    Variante("valores en preorden",
             [("        estado[v] = 1;\n        for", "        estado[v] = 1;\n        post.push_back(v);\n        for"),
              ("        estado[v] = 2;\n        post.push_back(v);", "        estado[v] = 2;"),
              ("valor[post[i]] = n - i;", "valor[post[i]] = i + 1;")],
             prueba=8, v="wa"),
    Variante("DFS solo desde x1",
             [("for (int v = 0; v < g.V() && !hayCiclo; ++v)\n            if (estado[v] == 0) dfs(g, v);", "dfs(g, 0);")],
             prueba=9, v="wa"),
    Variante("no detecta ciclos", [("if (estado[w] == 1) hayCiclo = true;        // w sigue en la pila: ciclo\n            else ", "")], prueba=10, v="wa"),
    Variante("solo detecta ciclos de dos",
             [("if (estado[w] == 1) hayCiclo = true;", "if (estado[w] == 1 && g.hayArista(w, v)) hayCiclo = true;")], prueba=11, v="wa"),
    Variante("«hay ciclo» sin reiniciar entre casos",
             [("class Inecuaciones {", "bool hayCiclo = false;\nclass Inecuaciones {"),
              ("valor(g.V()), hayCiclo(false) {", "valor(g.V()) {"),
              ("    bool hayCiclo;\n", "")],
             prueba=13, v="wa"),
    Variante("copia el grafo en cada llamada", [("void dfs(Digrafo const& g, int v) {", "void dfs(Digrafo g, int v) {")], prueba=[17, 18], v="tle"),
    Variante("un valor por línea", [("for (int v = 0; v < n; ++v) cout << ' ' << sis.valorDe(v);", "for (int v = 0; v < n; ++v) cout << '\\n' << sis.valorDe(v);")], prueba=1, v="pe"),
]


# ---------------------------------------------------------------- respuesta alternativa
def ALTERNATIVA(entrada):
    """Otra respuesta correcta (vale cualquier asignación que cumpla todo): orden de Kahn eligiendo la
    variable libre de número MAYOR y valores 7, 10, 13... El verificador comprueba que se acepta."""
    import heapq
    v = list(map(int, entrada.split()))
    p, out = 1, []
    for _ in range(v[0]):
        n, m = v[p], v[p + 1]
        p += 2
        suc, grado = [[] for _ in range(n + 1)], [0] * (n + 1)
        for _ in range(m):
            a, b = v[p], v[p + 1]
            p += 2
            suc[a].append(b)
            grado[b] += 1
        libres = [-x for x in range(1, n + 1) if grado[x] == 0]
        heapq.heapify(libres)
        valor, k = [0] * (n + 1), 0
        while libres:
            x = -heapq.heappop(libres)
            valor[x] = 7 + 3 * k
            k += 1
            for y in suc[x]:
                grado[y] -= 1
                if grado[y] == 0:
                    heapq.heappush(libres, -y)
        out.append("SI " + " ".join(map(str, valor[1:])) if k == n else "NO")
    return "\n".join(out) + "\n"
