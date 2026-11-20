"""05-3 · Ordenando tareas: juez con pruebas pensadas para cada error típico.

El enunciado admite cualquier orden válido, pero el juez compara la salida exacta. Por eso:
  * casi todas las pruebas tienen UN ÚNICO orden válido (el DAG contiene un camino que pasa por
    todas las tareas), así que cualquier algoritmo correcto (DFS, Kahn...) da la misma salida;
  * solo el ejemplo 1 del PDF admite varios órdenes: ahí se espera el del DFS del tema (postorden
    inverso, lanzando el DFS desde las tareas 1, 2, …, N y siguiendo las dependencias en el orden
    de la entrada), que es lo que escribe la solución de referencia: «7 1 2 4 3 5 6».
El solucionador es propio (DFS iterativo con tres colores) y se ha validado contra fuerza bruta.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-3/EJ_05-3.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-3/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["reverse(post.begin(), post.end());", ";"],
}


def ordena(n, aristas):
    """Postorden inverso del DFS (desde 1..n, adyacentes en orden de entrada) o None si hay ciclo."""
    ady = [[] for _ in range(n + 1)]
    for a, b in aristas:
        ady[a].append(b)
    color = [0] * (n + 1)          # 0 sin visitar, 1 en el camino actual, 2 terminado
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
    return post[::-1]


def salida(n, aristas):
    o = ordena(n, aristas)
    return "Imposible\n" if o is None else " ".join(map(str, o)) + "\n"


def dag_unico(rng, n, extra, ciclo=False):
    """DAG con orden topológico único (camino por todas las tareas) y aristas extra hacia delante.
    Con ciclo=True se añade además una arista hacia atrás."""
    p = list(range(1, n + 1))
    rng.shuffle(p)
    aristas = {(p[i], p[i + 1]) for i in range(n - 1)}
    tope = n * (n - 1) // 2
    while len(aristas) < min(tope, n - 1 + extra):
        i, j = sorted(rng.sample(range(n), 2))
        aristas.add((p[i], p[j]))
    aristas = list(aristas)
    if ciclo and n >= 2:
        i, j = sorted(rng.sample(range(n), 2))
        aristas.append((p[j], p[i]))
    rng.shuffle(aristas)
    return n, aristas


def caso_a_texto(c):
    n, aristas = c
    return f"{n}\n{len(aristas)}\n" + "".join(f"{a} {b}\n" for a, b in aristas)


EXPLICA_ORDEN = ("Este caso admite varios órdenes. El enunciado acepta cualquiera, pero este juez compara la salida "
                 "exacta y espera el del DFS del tema: postorden inverso, lanzando el DFS desde las tareas 1, 2, …, N "
                 "y recorriendo las dependencias de cada tarea en el orden en que aparecen en la entrada.")


def pruebas():
    rng = random.Random(533)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(salida(*c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado",
           [(7, [(1, 2), (2, 3), (2, 4), (3, 5), (2, 5), (4, 5), (5, 6), (7, 4)])],
           "El primer ejemplo del PDF (siete tareas). " + EXPLICA_ORDEN + " Aquí sale «7 1 2 4 3 5 6».",
           {"wa": "Si tu orden respeta todas las dependencias, es correcto según el enunciado, pero no es el que espera este juez (que compara la salida exacta). " + EXPLICA_ORDEN + " Si las demás pruebas (que solo tienen un orden posible) salen bien, tu algoritmo está bien.",
            "pe": "El orden es correcto pero el formato no: las tareas van en UNA línea, separadas por un espacio.",
            "rte": "Se rompe con el ejemplo: las tareas van de 1 a N; si tu grafo tiene N vértices, resta 1 al leer."},
           ["Comprueba primero a mano que tu orden respeta las ocho dependencias.",
            "Si es válido pero distinto de «7 1 2 4 3 5 6», usa el DFS del tema: para v = 1…N, si v no está visitado, dfs(v); al terminar cada vértice, guárdalo en post.",
            "Al final, escribe post al revés (postorden inverso). Recorre los adyacentes en el orden de la entrada (ponArista los añade al final de la lista)."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(2, [(1, 2), (2, 1)])],
           "El segundo ejemplo del PDF: 1 antes que 2 y 2 antes que 1, imposible.",
           {"wa": "Con un ciclo hay que escribir exactamente «Imposible» (con mayúscula inicial y sin tilde). Si escribes un orden, no detectas los ciclos."},
           ["¿Puede empezar alguna de las dos tareas?",
            "Detecta el ciclo en el DFS: si desde v ves un vecino que todavía está en la pila (estado 1), hay ciclo."])

    # ------------------------------------------------------------------ borde
    prueba("Dos tareas", "borde", [(2, [(1, 2)]), (2, [(2, 1)])],
           "Dos tareas con una dependencia en cada sentido: «1 2» y «2 1».",
           {"wa": "Con dos tareas solo hay un orden válido en cada caso: revisa el sentido de las aristas (A → B si A va antes que B) y que inviertes el postorden."},
           ["«2 1» en la entrada significa que la 2 va antes que la 1.",
            "La arista es A → B y el orden es el postorden inverso del DFS."])

    # ------------------------------------------------------------------ trampas
    prueba("Una sola tarea (se numeran desde 1)", "trampa", [(1, [])],
           "N = 1 y ninguna dependencia: hay que escribir «1».",
           {"wa": "Escribes 0: las tareas se numeran de 1 a N. Si tu grafo usa vértices 0…N-1, suma 1 al escribir.",
            "rte": "Con N = 1 y M = 0 algo se sale de rango: revisa que restas 1 al leer (vértices 0…N-1)."},
           ["El vértice v de tu grafo es la tarea v + 1.",
            "Al leer resta 1 (ponArista(a - 1, b - 1)) y al escribir suma 1."])
    prueba("El postorden hay que darle la vuelta", "trampa", [(3, [(1, 2), (2, 3)])],
           "1 antes que 2 y 2 antes que 3: la única respuesta es «1 2 3».",
           {"wa": "Escribes «3 2 1»: das el postorden sin invertirlo, o has puesto las aristas al revés (B → A). El DFS termina primero las tareas del final."},
           ["¿Qué tarea termina primero el DFS que empieza en la 1?",
            "El orden topológico es el postorden INVERSO: el último en terminar va el primero.",
            "Comprueba también el sentido: «A B» es la arista A → B."])
    prueba("Llegar dos veces a una tarea no es un ciclo", "trampa", [(3, [(1, 2), (2, 3), (1, 3)])],
           "La tarea 3 se alcanza desde la 1 y desde la 2, pero no hay ningún ciclo: «1 2 3».",
           {"wa": "Escribes «Imposible»: tomas cualquier vecino ya visitado como un ciclo. Solo es ciclo si el vecino sigue en la pila del DFS (estado 1); si ya terminó (estado 2), no."},
           ["Al volver a la tarea 1, su vecino 3 ya está visitado… pero ya terminó: no está en el camino actual.",
            "Hacen falta tres estados: sin visitar, en la pila y terminado.",
            "Marca «terminado» (estado 2) al salir del DFS de cada vértice y declara ciclo solo con un vecino en estado 1."])
    prueba("El preorden no sirve", "trampa", [(3, [(1, 2), (1, 3), (3, 2)])],
           "1 antes que 2 y que 3, y 3 antes que 2: la única respuesta es «1 3 2».",
           {"wa": "Escribes «1 2 3»: guardas cada tarea al EMPEZAR su DFS (preorden). Hay que guardarla al TERMINAR (postorden) y luego invertir."},
           ["El DFS desde la 1 visita antes la 2 que la 3, pero la 3 tiene que ir antes que la 2.",
            "Mete el vértice en la lista cuando terminas su DFS, no cuando entras en él."])
    prueba("Tareas a las que no se llega desde la 1", "trampa", [(3, [(2, 1), (3, 2)])],
           "3 antes que 2 y 2 antes que 1: «3 2 1». Desde la tarea 1 no se alcanza ninguna otra.",
           {"wa": "Te faltan tareas o salen en mal orden: lanzas el DFS solo desde la tarea 1. Hay que lanzarlo desde CADA tarea no visitada."},
           ["¿Cuántas tareas escribe tu programa en este caso?",
            "Recorre v = 1…N y, si v no está visitada, lanza el DFS desde v."])
    prueba("Ciclo de dos tareas que no incluye la 1", "trampa", [(3, [(1, 2), (2, 3), (3, 2)])],
           "2 antes que 3 y 3 antes que 2: «Imposible», aunque la tarea 1 no esté en el ciclo.",
           {"wa": "Escribes un orden: no detectas el ciclo 2 → 3 → 2. Un vecino que sigue en la pila (estado 1) cierra un ciclo, sea cual sea la tarea de partida."},
           ["Sigue el DFS desde la 1: 1 → 2 → 3, y desde la 3 se ve la 2, que sigue en la pila.",
            "Cuando detectes el ciclo, recuerda escribir «Imposible» en vez del orden."])
    prueba("Ciclo de tres tareas", "trampa", [(4, [(1, 2), (2, 3), (3, 4), (4, 2)])],
           "2 → 3 → 4 → 2 es un ciclo de longitud 3: «Imposible».",
           {"wa": "Detectas los ciclos de dos tareas pero no los más largos: no basta con mirar si existen A → B y B → A. Usa el estado «en la pila» del DFS."},
           ["Un ciclo puede tener cualquier longitud.",
            "En el DFS, si un vecino está en estado 1 (en la pila), hay un ciclo, mida lo que mida."])
    prueba("Imposible aunque haya tareas libres", "trampa", [(5, [(1, 2), (3, 4), (4, 5), (5, 3)])],
           "La 1 y la 2 se pueden hacer, pero 3 → 4 → 5 → 3 es un ciclo: «Imposible», no un orden parcial.",
           {"wa": "Escribes solo parte de las tareas: si hay un ciclo, la respuesta es «Imposible» entera. Con el algoritmo de Kahn, comprueba al final si has sacado las N tareas."},
           ["Si alguna tarea no puede hacerse nunca, no existe ningún orden válido.",
            "Con Kahn: si la cola se vacía antes de haber sacado N tareas, hay ciclo."])
    prueba("Muchas dependencias sin ciclo", "trampa", [dag_unico(rng, 9, 40)],
           "Nueve tareas con todas las dependencias posibles hacia delante (36): más aristas que tareas no implica ciclo.",
           {"wa": "Hay muchas aristas a tareas ya terminadas y ninguna cierra un ciclo. ¿Deduces «Imposible» por el número de aristas o por ver un vértice ya visitado?"},
           ["Un grafo sin ciclos puede tener hasta N·(N-1)/2 aristas.",
            "Solo hay ciclo si un vecino está en la pila del DFS en ese momento."])
    casos = [dag_unico(rng, 6, 3, ciclo=True), dag_unico(rng, 5, 2), (1, []), dag_unico(rng, 7, 4, ciclo=True),
             dag_unico(rng, 4, 1), (2, [(1, 2), (2, 1)]), dag_unico(rng, 8, 6)]
    prueba("Varios casos seguidos", "trampa", casos,
           "Casos con y sin ciclo alternados: nada de un caso (marcas, «hay ciclo», la lista del orden) debe pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: algo no se reinicia entre casos (el indicador de ciclo, el vector de estados o la lista del postorden).",
            "rte": "Un vector del caso anterior con otro tamaño: créalos dentro de cada caso."},
           ["Tras un caso «Imposible», ¿tu programa vuelve a poner «no hay ciclo»?",
            "Declara el grafo, los estados, la lista y el indicador de ciclo dentro de resuelveCaso (o en un objeto nuevo por caso)."])

    # ------------------------------------------------------------------ aleatorios
    casos = [dag_unico(rng, rng.randint(1, 8), rng.randint(0, 8), ciclo=rng.random() < .3) for _ in range(120)]
    casos[0] = dag_unico(rng, 5, 2, ciclo=True)
    prueba("Casos pequeños al azar (orden único)", "aleatorio", casos,
           "120 casos de hasta 8 tareas; los que tienen solución admiten un único orden.",
           {"wa": "Algún caso falla: localiza la línea, busca el caso y dibújalo (son muy pequeños)."},
           ["El caso que falla es el de la línea que te marca el juez.",
            "Comprueba si es un ciclo que no detectas o un orden que no respeta alguna dependencia."])
    casos = [dag_unico(rng, rng.randint(50, 300), rng.randint(0, 600), ciclo=rng.random() < .3) for _ in range(30)]
    prueba("Casos medianos al azar (orden único)", "aleatorio", casos,
           "30 casos de 50 a 300 tareas, con y sin ciclos.",
           {"wa": "Algún caso falla: si es «Imposible», revisa la detección de ciclos; si no, que el orden respeta todas las dependencias."},
           ["Comprueba tu salida: para cada dependencia «A B», A debe aparecer antes que B.",
            "Un ciclo largo solo se detecta con el estado «en la pila»."])

    # ------------------------------------------------------------------ rendimiento
    prueba("10.000 tareas en cadena y 100.000 dependencias", "rendimiento", [dag_unico(rng, 10000, 90001)],
           "El caso más grande: un único orden posible y una recursión de 10.000 niveles.",
           {"tle": "Debe ser O(N + M). ¿Usas una matriz de adyacencia, buscas la siguiente tarea libre recorriendo todas cada vez (Kahn en O(N²)) o copias el grafo en cada llamada?",
            "mle": "Demasiada memoria: una matriz N × N o copiar el grafo en cada llamada recursiva no cabe. Pasa el grafo por referencia (const&).",
            "rte": "Con 10.000 niveles de recursión no debería romperse aquí; revisa que no declaras vectores grandes dentro de la función recursiva.",
            "wa": "En el caso grande el orden no es el único válido que existe: revisa la detección de ciclos y el postorden inverso."},
           ["Pasa el grafo por referencia (Digrafo const& g) a la función recursiva.",
            "Cada vértice y cada arista se deben procesar una vez: O(N + M).",
            "Con Kahn, guarda las tareas libres en una cola; no busques la siguiente recorriendo las N tareas."])
    casos = []
    for _ in range(60):
        a, b = rng.sample(range(1, 10001), 2)
        casos.append((10000, [(a, b), (b, a)]))
    prueba("60 casos de 10.000 tareas con un ciclo", "rendimiento", casos,
           "Muchos casos grandes con casi todas las tareas sueltas y un ciclo de dos: mide el coste por tarea.",
           {"tle": "Algo cuesta O(N²) por caso: una matriz N × N, Kahn buscando la tarea libre recorriendo todas, o copiar el grafo en cada llamada al DFS."},
           ["Con 10.000 tareas, O(N²) son 10⁸ operaciones por caso: demasiado con 60 casos.",
            "Usa listas de adyacencia (Digrafo) y pasa el grafo por referencia."])
    n = 10000
    cadena = [(i, i + 1) for i in range(1, n)] + [(n, 1)]
    prueba("Ciclo que pasa por las 10.000 tareas", "rendimiento", [(n, cadena)],
           "1 → 2 → … → 10.000 → 1: un ciclo enorme que se detecta en lo más profundo de la recursión.",
           {"wa": "Un ciclo muy largo también es un ciclo: «Imposible».",
            "tle": "Detectar el ciclo debe costar O(N + M).",
            "mle": "Demasiada memoria en una recursión de 10.000 niveles: ¿copias el grafo o vectores en cada llamada?"},
           ["El DFS llega a la tarea 10.000 y ve la 1, que sigue en la pila.",
            "Pasa todo por referencia en la recursión."])
    return P


VARIANTES = [
    Variante("escribe las tareas desde 0", [("cout << v + 1;", "cout << v;")], prueba=4, v="wa"),
    Variante("no invierte el postorden", [("reverse(post.begin(), post.end());   // postorden inverso = orden topologico", "")], prueba=5, v="wa"),
    Variante("aristas al revés", [("g.ponArista(a - 1, b - 1);   // a antes que b", "g.ponArista(b - 1, a - 1);")], prueba=5, v="wa"),
    Variante("cualquier visitado es un ciclo", [("if (estado[w] == 1) hayCiclo = true;", "if (estado[w] != 0) hayCiclo = true;")], prueba=6, v="wa"),
    Variante("preorden en vez de postorden",
             [("        estado[v] = 1;\n        for", "        estado[v] = 1;\n        post.push_back(v);\n        for"),
              ("        estado[v] = 2;\n        post.push_back(v);", "        estado[v] = 2;"),
              ("reverse(post.begin(), post.end());   // postorden inverso = orden topologico", "")],
             prueba=7, v="wa"),
    Variante("DFS solo desde la tarea 1",
             [("for (int v = 0; v < g.V() && !hayCiclo; ++v)\n            if (estado[v] == 0) dfs(g, v);", "dfs(g, 0);")],
             prueba=8, v="wa"),
    Variante("no detecta ciclos", [("if (estado[w] == 1) hayCiclo = true;        // w sigue en la pila: ciclo\n            else ", "")], prueba=9, v="wa"),
    Variante("solo detecta ciclos de dos tareas",
             [("if (estado[w] == 1) hayCiclo = true;", "if (estado[w] == 1 && g.hayArista(w, v)) hayCiclo = true;")], prueba=10, v="wa"),
    Variante("«hay ciclo» sin reiniciar entre casos",
             [("class OrdenTopologico {", "bool hayCiclo = false;\nclass OrdenTopologico {"),
              ("estado(g.V(), 0), hayCiclo(false) {", "estado(g.V(), 0) {"),
              ("    bool hayCiclo;\n", "")],
             prueba=13, v="wa"),
    Variante("copia el grafo en cada llamada", [("void dfs(Digrafo const& g, int v) {", "void dfs(Digrafo g, int v) {")], prueba=[16, 17], v="tle"),
    Variante("una tarea por línea", [("if (!primero) cout << ' ';", "if (!primero) cout << '\\n';")], prueba=1, v="pe"),
]
