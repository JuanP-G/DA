"""05-L · El Necronomicón de la informática: juez con pruebas pensadas para cada error típico.

Instrucciones 1…L (A, J N, C N); el programa empieza en la 1 y termina al llegar detrás de la última.
SIEMPRE: el final se alcanza y no hay ningún ciclo alcanzable; NUNCA: el final no se alcanza;
A VECES: se alcanza el final y también un ciclo. El solucionador es propio y usa otra técnica que la
solución del repo: BFS para la alcanzabilidad y eliminación de Kahn (sobre lo alcanzable) para los ciclos.
"""
import random
from collections import deque
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "5-Grafos dirigidos/EJ_05-L/EJ_05-L.cpp",
    "cabeceras": ["5-Grafos dirigidos/EJ_05-L/Digrafo.h"],
    "limite_ms": 3000,
    "fallo": ["if (tipo == 'C') g.ponArista(i, i + 1);", ";"],
}


def veredicto(prog):
    L = len(prog)
    suc = []
    for i, (t, n) in enumerate(prog, 1):      # vértices 1..L, L+1 = final
        if t == "A":
            suc.append([i + 1])
        elif t == "J":
            suc.append([n])
        else:
            suc.append([n, i + 1])
    suc = [None] + suc + [[]]
    alc = [False] * (L + 2)
    alc[1] = True
    cola = deque([1])
    while cola:
        v = cola.popleft()
        for w in suc[v]:
            if not alc[w]:
                alc[w] = True
                cola.append(w)
    if not alc[L + 1]:
        return "NUNCA"
    grado = [0] * (L + 2)                       # Kahn sobre el subgrafo alcanzable
    for v in range(1, L + 2):
        if alc[v]:
            for w in suc[v]:
                grado[w] += 1
    cola = deque(v for v in range(1, L + 2) if alc[v] and grado[v] == 0)
    quitados = 0
    while cola:
        v = cola.popleft()
        quitados += 1
        for w in suc[v]:
            grado[w] -= 1
            if grado[w] == 0:
                cola.append(w)
    return "SIEMPRE" if quitados == sum(alc) else "A VECES"


def lee(texto):
    """'A / J 3 / C 1' -> [('A',0), ('J',3), ('C',1)]"""
    out = []
    for p in texto.split("/"):
        p = p.split()
        out.append((p[0], int(p[1]) if len(p) > 1 else 0))
    return out


def caso_a_texto(prog):
    return f"{len(prog)}\n" + "".join(f"{t}\n" if t == "A" else f"{t} {n}\n" for t, n in prog)


def al_azar(rng, L, pa=.5, pj=.25):
    prog = []
    for _ in range(L):
        x = rng.random()
        t = "A" if x < pa else ("J" if x < pa + pj else "C")
        prog.append((t, rng.randint(1, L) if t != "A" else 0))
    return prog


def adelante(rng, L, atras=0):
    """Programa grande con saltos casi siempre hacia delante y algunos hacia atrás."""
    prog = []
    for i in range(1, L + 1):
        x = rng.random()
        if x < .5:
            prog.append(("A", 0))
        else:
            t = "J" if x < .6 else "C"
            prog.append((t, rng.randint(i, min(L, i + 50))))
    for _ in range(atras):
        i = rng.randint(2, L)
        prog[i - 1] = ("C", rng.randint(1, i))
    return prog


def pruebas():
    rng = random.Random(577)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        casos = [lee(c) if isinstance(c, str) else c for c in casos]
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(veredicto(c) + "\n" for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado", ["A / A / J 1", "A / J 4 / J 5 / C 3 / A", "A / A / C 2 / A"],
           "Los tres programas del PDF: NUNCA, SIEMPRE y A VECES.",
           {"wa": "Si falla el ejemplo, revisa lo básico: el vértice «final» (detrás de la última instrucción), las aristas de cada tipo (A: siguiente; J: solo el salto; C: el salto Y la siguiente) y las tres respuestas.",
            "pe": "La respuesta es correcta pero el formato no: una palabra por línea, y «A VECES» con un espacio.",
            "rte": "Se rompe con el ejemplo: revisa los índices (instrucciones de 1 a L, el final es el vértice L si numeras desde 0)."},
           ["Construye un grafo con L + 1 vértices: el último representa «el programa ha terminado».",
            "En el segundo programa hay un salto hacia atrás (C 3 en la 4), pero desde la 3 no se vuelve a la 4: no hay bucle.",
            "Respuestas: el final no se alcanza ⇒ NUNCA; se alcanza y hay un ciclo alcanzable ⇒ A VECES; si no, SIEMPRE."])

    # ------------------------------------------------------------------ borde
    prueba("Una sola instrucción", "borde", ["A", "J 1", "C 1"],
           "Programas de una instrucción: A termina (SIEMPRE), J 1 se repite para siempre (NUNCA) y C 1 puede hacer las dos cosas (A VECES).",
           {"wa": "Con una sola instrucción falla algún caso: «J 1» es un salto a sí misma (un lazo) y «C 1» puede repetirse o seguir hasta el final.",
            "rte": "Con L = 1 te sales de rango: el final es la posición L (si numeras desde 0) y necesitas L + 1 vértices."},
           ["Dibuja el grafo de «C 1»: una arista de la instrucción 1 a sí misma y otra al final.",
            "Un lazo (arista de un vértice a sí mismo) también es un ciclo."])
    prueba("Sin saltos", "borde", ["A / A / A / A / A", "J 2 / J 3 / J 4 / A"],
           "Programas que avanzan siempre hacia delante: SIEMPRE.",
           {"wa": "Sin saltos hacia atrás todos los caminos llegan al final: SIEMPRE. ¿Cuentas como ciclo un salto a la siguiente instrucción?"},
           ["Sigue el programa: cada instrucción lleva a una posterior.",
            "J N con N = i + 1 es como una A."])

    # ------------------------------------------------------------------ trampas
    prueba("Bucle con salida: A VECES", "trampa", ["C 3 / J 1 / A"],
           "La 1 puede seguir a la 2, que vuelve a la 1 (bucle), o saltar a la 3 y terminar: A VECES.",
           {"wa": "Si te sale NUNCA: o crees que cualquier bucle impide terminar (hay que mirar si el final se alcanza), o tu C solo salta y no sigue a la siguiente. Si te sale SIEMPRE: el C no sigue a la siguiente instrucción, y sin esa arista no ves el bucle."},
           ["Un C tiene DOS sucesores: la instrucción N y la siguiente (i + 1).",
            "NUNCA es solo cuando el final no se alcanza; si se alcanza y hay un bucle alcanzable, es A VECES."])
    prueba("Llegar dos veces a una instrucción no es un bucle", "trampa", ["C 3 / A / A"],
           "A la 3 se llega por el salto de la 1 y pasando por la 2, pero no hay ningún bucle: SIEMPRE.",
           {"wa": "Escribes A VECES: tomas cualquier instrucción ya visitada como un ciclo. Solo hay ciclo si esa instrucción sigue en la pila del DFS (en el camino actual)."},
           ["Cuando el DFS llega a la 3 por segunda vez, la 3 ya ha terminado: no está en el camino actual.",
            "Usa tres estados (sin visitar, en la pila, terminado) y declara ciclo solo con un vecino «en la pila»."])
    prueba("J no sigue a la siguiente instrucción", "trampa", ["J 3 / J 1 / A"],
           "La 1 salta a la 3 y termina; la 2 (que volvería a la 1) nunca se ejecuta: SIEMPRE.",
           {"wa": "Escribes A VECES: un salto J va SOLO a la instrucción N. Si le añades también la siguiente, la 2 se vuelve alcanzable y aparece un bucle falso."},
           ["Después de un J nunca se ejecuta la instrucción siguiente (salvo que otro salto lleve a ella).",
            "J N: una sola arista, i → N. Solo C tiene las dos."])
    prueba("Un bucle al que no se llega no cuenta", "trampa", ["J 3 / J 2 / A"],
           "La 2 salta a sí misma (un bucle), pero desde la 1 nunca se llega a ella: SIEMPRE.",
           {"wa": "Escribes A VECES: buscas ciclos en todo el grafo. Solo cuentan los ciclos alcanzables desde la instrucción 1: haz el DFS solo desde ella, no desde todos los vértices."},
           ["¿Puede la ejecución llegar alguna vez a la instrucción 2?",
            "Lanza un único DFS desde la instrucción 1 (no el bucle «para cada vértice» del orden topológico)."])
    prueba("El final está detrás de la última instrucción", "trampa", ["A / J 1"],
           "Se llega a la última instrucción (la 2), pero esta salta a la 1: nunca se pasa de ella. NUNCA.",
           {"wa": "Te sale que termina: compruebas si se alcanza la ÚLTIMA instrucción, pero el programa termina al llegar DETRÁS de ella (vértice L + 1)."},
           ["Añade un vértice extra para «terminado»: con instrucciones 0…L−1, el final es el vértice L.",
            "Al final solo se llega desde la última instrucción si es A o C (los saltos van como mucho a la L): mira si se alcanza ese vértice extra."])
    prueba("NUNCA aunque haya un salto condicional", "trampa", ["C 2 / J 1"],
           "«C 2» en la 1 salta a la 2 o sigue a la 2: da igual. Y la 2 vuelve a la 1. NUNCA.",
           {"wa": "Un salto condicional no garantiza que se pueda salir: aquí sus dos caminos van a la misma instrucción. Decide con la alcanzabilidad del final, no con el tipo de instrucciones."},
           ["Dibuja las aristas: 1 → 2 (dos veces) y 2 → 1. ¿Se alcanza el final?",
            "La respuesta solo depende de: ¿se alcanza el final? ¿hay un ciclo alcanzable?"])
    prueba("Varios casos seguidos", "trampa",
           ["C 3 / J 1 / A", "A / A / A", "J 3 / J 2 / A", "A / J 4 / J 5 / C 3 / A", "A", "A / J 1", "C 2 / A"],
           "Programas seguidos con y sin bucles: nada de un caso (estados, «hay ciclo») debe pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: algo no se reinicia entre casos (el indicador de ciclo, los estados o el grafo).",
            "rte": "Un vector del caso anterior con otro tamaño: créalos dentro de cada caso con L + 1 posiciones."},
           ["Después de un programa con bucle, ¿vuelves a poner «no hay ciclo»?",
            "Declara el grafo, los estados y los indicadores dentro de resuelveCaso o en un objeto nuevo por caso."])
    prueba("Saltos a la propia instrucción", "trampa", ["A / C 2 / A", "A / J 2 / A"],
           "«C 2» en la 2 puede repetirse o seguir (A VECES); «J 2» en la 2 se repite para siempre (NUNCA).",
           {"wa": "Un salto a la propia instrucción es un lazo, que es un ciclo: con C se puede salir (A VECES); con J no (NUNCA)."},
           ["El DFS ve que el vecino de la 2 es la propia 2, que está en la pila: ciclo.",
            "Con «J 2» la única arista de la 2 es el lazo: el final no se alcanza."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 8)) for _ in range(150)]
    prueba("Programas pequeños al azar", "aleatorio", casos,
           "150 programas de hasta 8 instrucciones.",
           {"wa": "Algún caso falla: localiza la línea, busca el programa y dibuja su grafo (son muy pequeños)."},
           ["Dibuja el grafo del programa que falla, con el vértice final.",
            "Marca lo que se alcanza desde la instrucción 1 y busca bucles solo ahí."])
    casos = [al_azar(rng, rng.randint(50, 300), pa=.6, pj=.15) for _ in range(30)] + \
            [adelante(rng, rng.randint(50, 300), atras=rng.randint(0, 3)) for _ in range(30)]
    prueba("Programas medianos al azar", "aleatorio", casos,
           "60 programas de 50 a 300 instrucciones.",
           {"wa": "Algún caso falla: revisa el vértice final, las aristas del C y que los ciclos se buscan solo en lo alcanzable."},
           ["La línea que falla es el número de caso.",
            "Comprueba los tres tipos de instrucción por separado."])

    # ------------------------------------------------------------------ rendimiento
    casos = [adelante(rng, 10000, atras=rng.randint(0, 2)) for _ in range(25)]
    prueba("25 programas de 10.000 instrucciones", "rendimiento", casos,
           "Programas del tamaño máximo, con saltos casi siempre hacia delante.",
           {"tle": "Debe costar O(L) por programa. ¿Lanzas un DFS desde cada instrucción, o reinicias los visitados para cada salto?",
            "mle": "Demasiada memoria: ¿copias el grafo en cada llamada recursiva? Pásalo por referencia (const&)."},
           ["Un único DFS desde la instrucción 1 basta para responder todo.",
            "Pasa el grafo por referencia a la función recursiva."])
    prueba("Un C hacia atrás en cada instrucción", "rendimiento", [[("C", 1)] * 10000],
           "10.000 instrucciones «C 1»: la recursión llega a 10.000 niveles y hay un bucle en cada paso. A VECES.",
           {"wa": "Con 10.000 niveles algo falla: ¿limitas la profundidad?",
            "tle": "Cada instrucción y arista se deben procesar una vez.",
            "mle": "Recursión de 10.000 niveles: no copies el grafo ni vectores en cada llamada.",
            "rte": "La recursión es profunda pero aquí cabe; revisa que no declaras arrays grandes dentro de la función recursiva."},
           ["Marca las instrucciones visitadas para no repetir trabajo.",
            "Todo lo que pases a la función recursiva, por referencia."])
    n = 10000
    prueba("Un único bucle por las 10.000 instrucciones", "rendimiento", [[("J", i + 1) for i in range(1, n)] + [("J", 1)]],
           "Cada instrucción salta a la siguiente y la última vuelve a la primera: NUNCA, descubierto en lo más profundo de la recursión.",
           {"wa": "El final no se alcanza nunca: NUNCA.",
            "tle": "Debe costar O(L).",
            "mle": "Recursión de 10.000 niveles: no copies el grafo en cada llamada."},
           ["El DFS recorre las 10.000 instrucciones y vuelve a la 1, que sigue en la pila.",
            "El vértice final no se visita: NUNCA."])
    return P


VARIANTES = [
    Variante("el C solo salta", [("if (tipo == 'C') g.ponArista(i, i + 1);   // y, si es condicional, seguir", "")], prueba=4, v="wa"),
    Variante("cualquier bucle ⇒ NUNCA",
             [("if (!p.terminaAlgunaVez()) cout << \"NUNCA\\n\";", "if (!p.terminaAlgunaVez() || p.puedeNoTerminar()) cout << \"NUNCA\\n\";")],
             prueba=4, v="wa"),
    Variante("cualquier visitado es un ciclo", [("if (estado[w] == 1) hayCiclo = true;", "if (estado[w] != 0) hayCiclo = true;")], prueba=5, v="wa"),
    Variante("J también sigue a la siguiente",
             [("if (tipo == 'C') g.ponArista(i, i + 1);   // y, si es condicional, seguir", "g.ponArista(i, i + 1);")], prueba=6, v="wa"),
    Variante("DFS desde todas las instrucciones",
             [("dfs(g, 0);                          // solo lo que se alcanza desde la instruccion 1",
               "for (int v = 0; v < g.V(); ++v) if (estado[v] == 0) dfs(g, v);")], prueba=7, v="wa"),
    Variante("el final es la última instrucción", [("alcanzaFin = (estado[g.V() - 1] != 0);", "alcanzaFin = (estado[g.V() - 2] != 0);")], prueba=8, v="wa"),
    Variante("«hay ciclo» sin reiniciar entre casos",
             [("class ProgramaOscuro {", "bool hayCiclo = false;\nclass ProgramaOscuro {"),
              ("estado(g.V(), 0), hayCiclo(false) {", "estado(g.V(), 0) {"),
              ("    bool hayCiclo;\n", "")],
             prueba=10, v="wa"),
    Variante("copia el grafo en cada llamada", [("void dfs(Digrafo const& g, int v) {", "void dfs(Digrafo g, int v) {")], prueba=[14, 15, 16], v="mle"),
    Variante("SIEMPRE sin salto de línea", [("cout << \"SIEMPRE\\n\";", "cout << \"SIEMPRE \";")], prueba=1, v="pe"),
]
