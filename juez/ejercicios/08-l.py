"""08-l · Planificación de conferencias: juez con pruebas pensadas para cada error típico.

El enunciado admite cualquier asignación de salas válida con el mínimo número de salas y el juez la
acepta: juez/ejercicios/comprobadores/08-l.py (servidor) y 08-l.js (navegador) comprueban que el
número de salas es el mínimo y que no hay dos conferencias solapadas en la misma sala. ALTERNATIVA da
otra asignación (salas renumeradas al revés) y el verificador comprueba que también se acepta.
El solucionador (por hora de comienzo, reutilizando la sala que queda libre antes) se ha validado
contra el máximo número de conferencias simultáneas y contra fuerza bruta (todas las asignaciones)
en miles de casos pequeños.
"""
import heapq
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "8-Algoritmos voraces/EJ_08-L/EJ_08-L.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["if (!salas.empty() && salas.top().first <= ini[c]) {", "if (!salas.empty() && salas.top().first < ini[c]) {"],
}


def planifica(confs):
    n = len(confs)
    orden = sorted(range(n), key=lambda i: (confs[i][0], i))
    libres, sala, r = [], [0] * n, 0
    for c in orden:
        if libres and libres[0][0] <= confs[c][0]:
            _, s = heapq.heappop(libres)
        else:
            r += 1
            s = r
        sala[c] = s
        heapq.heappush(libres, (confs[c][1], s))
    return r, sala


def salida(confs):
    r, sala = planifica(confs)
    return f"{r}\n" + " ".join(map(str, sala)) + "\n"


def caso_a_texto(confs):
    return f"{len(confs)}\n" + "".join(f"{a} {b}\n" for a, b in confs)


def al_azar(rng, n, tope, durmax):
    out = []
    for _ in range(n):
        a = rng.randint(0, tope - 1)
        out.append((a, min(tope, a + rng.randint(1, durmax))))
    return out


EXPLICA = " Vale cualquier asignación válida con el mínimo número de salas."


def pruebas():
    rng = random.Random(808)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(salida(c) for c in casos), casos=len(casos),
                        comprueba=comprueba + EXPLICA, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [[(1, 5), (3, 10), (6, 12)], [(5, 10), (1, 5)], [(1, 5), (2, 6), (3, 7)]],
           "Los tres casos del PDF.",
           {"wa": "Si falla hasta el ejemplo, revisa la idea: recorrer las conferencias por hora de COMIENZO y reutilizar una sala que ya esté libre o abrir una nueva. El «Por qué» te dice qué línea está mal.",
            "pe": "Las salas son correctas pero el formato no: por cada caso, una línea con R y otra con las N salas separadas por un espacio."},
           ["Sigue a mano el primer caso: la de 6 a 12 puede ir a la sala de la de 1 a 5.",
            "Escribe dos líneas por caso: el número de salas y luego la sala de cada conferencia EN EL ORDEN DE LA ENTRADA.",
            "Guarda en una cola de prioridad de mínimos (hora en que queda libre, sala) y mira solo la que queda libre antes."])

    # ------------------------------------------------------------------ borde
    prueba("Una sola conferencia", "borde", [[(0, 1000000000)]],
           "N = 1 con los tiempos extremos (0 y 10⁹): una sala.",
           {"wa": "Con una conferencia basta una sala: «1» y luego «1».",
            "rte": "Con N = 1 algo se sale de rango: revisa la cola de prioridad vacía (no hagas top() sin comprobar empty())."},
           ["¿Qué escribe tu programa con una única conferencia?",
            "Comprueba que la cola no está vacía antes de mirar su cima."])
    prueba("Todas a la vez", "borde", [[(10, 20), (10, 20), (10, 20), (10, 20)]],
           "Cuatro conferencias idénticas: hacen falta 4 salas, una para cada una.",
           {"wa": "Conferencias idénticas se solapan entre sí: cada una necesita su sala. ¿Reutilizas una sala que todavía está ocupada?"},
           ["Una sala solo se puede reutilizar si su última conferencia acabó como muy tarde cuando empieza la nueva.",
            "Compara la hora en que queda libre con la hora de COMIENZO de la conferencia."])

    # ------------------------------------------------------------------ trampas
    prueba("Una empieza justo cuando acaba otra", "trampa", [[(1, 5), (5, 10), (10, 15)]],
           "Tres conferencias encadenadas (1-5, 5-10, 10-15): no se solapan y cabe todo en una sala.",
           {"wa": "Usas más salas de la cuenta: tratas como solapadas dos conferencias que se tocan. Una que empieza justo cuando acaba otra puede ir en la misma sala: la condición es libre ≤ comienzo, no <."},
           ["Relee el enunciado: «Una conferencia que empieza justo cuando termina otra no se solapa con ella».",
            "Reutiliza la sala si queda libre en un instante ≤ que el comienzo de la nueva."])
    prueba("Conferencias desordenadas", "trampa", [[(9, 12), (6, 9), (2, 6)]],
           "Tres conferencias encadenadas dadas al revés (9-12, 6-9, 2-6): caben todas en una sala.",
           {"wa": "Usas más salas: recorres las conferencias en el orden de la entrada. Hay que recorrerlas por hora de comienzo."},
           ["Si colocas primero la de 9 a 12, ¿puede ir después la de 6 a 9 en la misma sala?",
            "Ordena (los índices de) las conferencias por hora de comienzo antes de repartir salas."])
    prueba("Hay que mirar la sala que queda libre antes", "trampa", [[(1, 2), (1, 10), (3, 4)]],
           "Al llegar la de 3 a 4, la sala de 1-2 está libre aunque la de 1-10 no: bastan 2 salas.",
           {"wa": "Abres una sala nueva aunque hay una libre: miras solo la que queda libre MÁS TARDE (cola de máximos) o una sala cualquiera. Hay que mirar la que queda libre antes."},
           ["¿Qué sala está libre a las 3?",
            "La cola de prioridad debe ser de MÍNIMOS: priority_queue<…, vector<…>, greater<…>>."])
    prueba("Las salas se escriben en el orden de la entrada", "trampa", [[(10, 20), (1, 5), (3, 15)]],
           "Con 2 salas: 1-5 y 10-20 juntas y 3-15 en la otra. La línea de salas debe seguir el orden de la entrada.",
           {"wa": "El número de salas está bien, pero la asignación pone juntas dos conferencias que se solapan: escribes las salas en el orden ORDENADO, no en el de la entrada."},
           ["La i-ésima sala que escribes es la de la i-ésima conferencia de la entrada.",
            "Ordena un vector de índices, guarda sala[c] para cada índice y al final escribe sala[0], sala[1], …"])
    prueba("Ordenar por hora de fin no sirve", "trampa", [[(3, 9), (0, 4), (6, 7), (0, 3)]],
           "0-3 con 3-9 en una sala y 0-4 con 6-7 en otra: bastan 2. Recorriendo por hora de fin salen 3.",
           {"wa": "Usas 3 salas: recorres las conferencias por hora de FIN. Para este problema el orden correcto es por hora de COMIENZO."},
           ["Prueba a mano recorriendo por fin: 0-3, 0-4, 6-7 y… ¿dónde va la 3-9?",
            "Ordena por hora de comienzo: así, cuando abres una sala nueva, todas las abiertas están ocupadas en ese instante."])
    prueba("Muchos solapes no implican muchas salas", "trampa", [[(1, 10), (1, 2), (3, 4), (5, 6), (7, 8)]],
           "La de 1 a 10 se solapa con otras cuatro, pero esas cuatro caben en una sala: bastan 2.",
           {"wa": "El mínimo de salas es el máximo de conferencias que coinciden EN UN MISMO INSTANTE, no el número de conferencias con las que se solapa una."},
           ["¿En algún momento hay tres conferencias a la vez?",
            "Reparte con el voraz por comienzo: el número de salas que abre es el mínimo."])
    prueba("Una sala libre sirve una sola vez", "trampa", [[(1, 2), (3, 10), (4, 6)]],
           "La sala de 1-2 la reutiliza la de 3-10; la de 4-6 necesita otra sala (2).",
           {"wa": "Das la misma sala a dos conferencias que se solapan: cuando reutilizas una sala, hay que sacarla de la cola (pop) antes de volver a meterla con su nueva hora."},
           ["Tras dar la sala 1 a la conferencia de 3 a 10, ¿cuándo vuelve a quedar libre?",
            "Al reutilizar: pop() de la cima y push() con (fin de la nueva conferencia, sala)."])
    prueba("Varios casos seguidos", "trampa",
           [[(1, 5), (2, 6), (3, 7)], [(0, 1)], [(1, 5), (5, 10)], [(4, 8), (1, 3), (2, 9)]],
           "Casos con distinto número de salas seguidos: nada del caso anterior (salas abiertas, cola) debe quedar.",
           {"wa": "El primer caso sale bien y los siguientes no: el contador de salas o la cola de prioridad no se reinician en cada caso."},
           ["Si en el segundo caso escribes «4» o más, el contador viene del caso anterior.",
            "Declara la cola, el contador de salas y el vector de salas dentro de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    casos = [al_azar(rng, rng.randint(1, 8), rng.choice([10, 20]), rng.randint(1, 8)) for _ in range(200)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "200 casos de hasta 8 conferencias con muchos extremos que se tocan.",
           {"wa": "Algún caso falla: el «Por qué» dice qué conferencias se solapan o cuántas salas sobran; busca el caso y dibújalo."},
           ["La línea mala te dice el caso: cada caso ocupa dos líneas.",
            "Revisa el orden (por comienzo), la comparación ≤ y que la cola es de mínimos."])
    casos = [al_azar(rng, rng.randint(100, 2000), rng.choice([1000, 10 ** 6, 10 ** 9]), rng.choice([10, 1000, 10 ** 8])) for _ in range(20)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "20 casos de 100 a 2.000 conferencias con tiempos hasta 10⁹.",
           {"wa": "Algún caso mediano falla: suele ser la cola de prioridad (de mínimos, con pop al reutilizar) o el orden de salida."},
           ["Comprueba que escribes las salas en el orden de la entrada.",
            "Comprueba que la cola guarda (hora en que queda libre, sala)."])

    # ------------------------------------------------------------------ rendimiento
    n = 150000
    prueba("150.000 conferencias que coinciden todas", "rendimiento", [[(i, 2 * n - i) for i in range(n)]],
           "Conferencias anidadas que coinciden todas en un instante: hacen falta 150.000 salas.",
           {"tle": "Algo cuesta O(N·R): ¿buscas una sala libre recorriendo todas las salas abiertas? Con una cola de prioridad cada paso es O(log N).",
            "mle": "Gastas demasiada memoria: con 150.000 salas, guarda solo una entrada por sala en la cola."},
           ["Con 150.000 salas, recorrerlas todas por cada conferencia son ~10¹⁰ pasos.",
            "Solo necesitas saber cuál queda libre antes: una cola de prioridad de mínimos.",
            "Ordena una vez (O(N log N)) y usa la cola: O(N log N) en total."])
    prueba("100.000 conferencias al azar", "rendimiento", [al_azar(rng, 100000, 10 ** 6, 3000)],
           "Un caso grande al azar.",
           {"tle": "Debe ser O(N log N): ordenar y una cola de prioridad.",
            "wa": "En el caso grande falla la asignación: revisa el pop al reutilizar y el orden de salida."},
           ["Ordena índices por comienzo con sort.",
            "Cola de prioridad de mínimos con (libre, sala)."])
    return P


VARIANTES = [
    Variante("extremos que se tocan se solapan (<)", [("salas.top().first <= ini[c]", "salas.top().first < ini[c]")], prueba=4, v="wa"),
    Variante("no ordena las conferencias", [("sort(orden.begin(), orden.end(), [&](int a, int b) { return ini[a] < ini[b]; });", "")], prueba=5, v="wa"),
    Variante("escribe las salas en el orden ordenado", [("cout << sala[i] << (i + 1 < N ? ' ' : '\\n');", "cout << sala[orden[i]] << (i + 1 < N ? ' ' : '\\n');")], prueba=7, v="wa"),
    Variante("ordena por hora de fin", [("return ini[a] < ini[b];", "return fin[a] < fin[b];")], prueba=8, v="wa"),
    Variante("cola de máximos", [("priority_queue<Libre, vector<Libre>, greater<Libre>> salas;", "priority_queue<Libre> salas;")], prueba=6, v="wa"),
    Variante("no saca la sala al reutilizarla", [("            salas.pop();\n", "")], prueba=10, v="wa"),
    Variante("contador de salas sin reiniciar", [("int numSalas = 0;", "static int numSalas = 0;")], prueba=11, v="wa"),
    Variante("busca una sala libre entre todas (O(N·R))",
             [("""    using Libre = pair<int, int>;      // (hora en que la sala queda libre, sala)
    priority_queue<Libre, vector<Libre>, greater<Libre>> salas;
    vector<int> sala(N);
    int numSalas = 0;
    for (int c : orden) {
        if (!salas.empty() && salas.top().first <= ini[c]) {
            sala[c] = salas.top().second;      // reutilizar la que queda libre antes
            salas.pop();
        } else {
            sala[c] = ++numSalas;              // todas ocupadas: sala nueva
        }
        salas.push({fin[c], sala[c]});
    }""", """    vector<int> libre, sala(N);
    for (int c : orden) {
        int s = -1;
        for (int k = 0; k < (int)libre.size(); ++k)
            if (libre[k] <= ini[c]) { s = k; break; }
        if (s < 0) { libre.push_back(0); s = (int)libre.size() - 1; }
        libre[s] = fin[c];
        sala[c] = s + 1;
    }
    int numSalas = (int)libre.size();""")], prueba=14, v="tle"),
    Variante("una sala por línea", [("cout << sala[i] << (i + 1 < N ? ' ' : '\\n');", "cout << sala[i] << '\\n';")], prueba=1, v="pe"),
]


# ---------------------------------------------------------------- respuesta alternativa
def ALTERNATIVA(entrada):
    """Otra respuesta correcta: la misma planificación con las salas numeradas al revés
    (la sala s pasa a ser la R + 1 - s). El verificador comprueba que el juez la acepta."""
    v = list(map(int, entrada.split()))
    p, out = 1, []
    for _ in range(v[0]):
        n = v[p]
        p += 1
        confs = [(v[p + 2 * i], v[p + 2 * i + 1]) for i in range(n)]
        p += 2 * n
        r, sala = planifica(confs)
        out.append(str(r))
        out.append(" ".join(str(r + 1 - s) for s in sala))
    return "\n".join(out) + "\n"
