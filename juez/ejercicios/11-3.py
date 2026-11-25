"""11-3 · La colecta de primavera: juez con pruebas pensadas para cada error típico.

Entrada: número de casos; cada caso tiene «V C» (V vecinos 1..1.000, C cajas 0..4·V) y CUATRO
líneas de V enteros (0..1.000): lo que pagaría cada vecino por 1, 2, 3 y 4 cajas.
Salida: por caso, el beneficio máximo y una línea con las cajas (0..4) que se venden a cada vecino,
sin pasarse de C cajas. Si hay varios repartos óptimos vale cualquiera: por eso lleva comprobador
propio (comprobadores/11-3.{py,js}). ALTERNATIVA da otro reparto óptimo (en un empate, prefiere
vender más cajas) y el verificador comprueba que se acepta.
El solucionador es propio: con numpy, el mejor beneficio con exactamente j cajas como máximo para los
primeros i vecinos, y la reconstrucción desde la tabla entera. Validado contra fuerza bruta (todos los
repartos) en miles de casos pequeños.
"""
import itertools
import random
import numpy as np
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-3/EJ_11-3.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["for (int k = 0; k <= min(4, j); ++k)\n                mejor = max(mejor,", "for (int k = 0; k <= min(3, j); ++k)\n                mejor = max(mejor,"],
}


def tabla(V, C, pago):
    """pago[k][i]: lo que paga el vecino i por k cajas (pago[0] = 0). Devuelve dinero[i][j]."""
    dinero = np.zeros((V + 1, C + 1), dtype=np.int64)
    for i in range(1, V + 1):
        previa = dinero[i - 1]
        mejor = previa.copy()                                  # k = 0
        for k in range(1, 5):
            if k <= C:
                mejor[k:] = np.maximum(mejor[k:], previa[:C + 1 - k] + pago[k][i - 1])
        dinero[i] = mejor
    return dinero


def resuelve(V, C, pago, mas_cajas=False):
    """(beneficio, [cajas por vecino]); en un empate se vende menos (o más si mas_cajas)."""
    dinero = tabla(V, C, pago)
    rep = [0] * V
    j = C
    for i in range(V, 0, -1):
        orden = range(min(4, j), -1, -1) if mas_cajas else range(0, min(4, j) + 1)
        for k in orden:
            if dinero[i][j] == dinero[i - 1][j - k] + (pago[k][i - 1] if k else 0):
                rep[i - 1] = k
                j -= k
                break
    return int(dinero[V][C]), rep


def fuerza_bruta(V, C, pago):
    return max(sum(pago[c][i] if c else 0 for i, c in enumerate(rep))
               for rep in itertools.product(range(5), repeat=V) if sum(rep) <= C)


def texto(casos):
    out = [str(len(casos))]
    for V, C, pago in casos:
        out.append(f"{V} {C}")
        out += [" ".join(map(str, pago[k])) for k in range(1, 5)]
    return "\n".join(out) + "\n"


def salida(casos, mas_cajas=False):
    out = []
    for V, C, pago in casos:
        b, rep = resuelve(V, C, pago, mas_cajas)
        out.append(f"{b}\n{' '.join(map(str, rep))}\n")
    return "".join(out)


def mk(por_vecino, C):
    """Caso a partir de la lista [pago por 1, 2, 3, 4 cajas] de cada vecino."""
    V = len(por_vecino)
    pago = [[0] * V] + [[por_vecino[i][k] for i in range(V)] for k in range(4)]
    return (V, C, pago)


def alea(rng, V, C, vmax=20, ceros=0.0):
    return mk([[0 if rng.random() < ceros else rng.randint(0, vmax) for _ in range(4)] for _ in range(V)], C)


def _asegura():
    r = random.Random(5)
    for _ in range(500):
        V = r.randint(1, 5)
        caso = alea(r, V, r.randint(0, 4 * V), r.choice([3, 20]), 0.3)
        assert resuelve(*caso)[0] == fuerza_bruta(*caso), caso
        for mas in (False, True):
            b, rep = resuelve(*caso, mas_cajas=mas)
            assert sum(rep) <= caso[1] and sum(caso[2][c][i] if c else 0 for i, c in enumerate(rep)) == b


_asegura()


def voraz_marginal(V, C, pago):
    """Reparte las cajas una a una al vecino con mayor ganancia por la caja extra (un voraz que falla)."""
    c = [0] * V
    tot = 0
    for _ in range(C):
        mejor, bi = 0, -1
        for i in range(V):
            if c[i] < 4:
                g = pago[c[i] + 1][i] - (pago[c[i]][i] if c[i] else 0)
                if g > mejor:
                    mejor, bi = g, i
        if bi < 0:
            break
        c[bi] += 1
        tot += mejor
    return tot


def optimo(V, C, pago, kmax=4, al_menos_una=False):
    """Beneficio máximo con variantes (para escoger casos que distinguen los fallos típicos)."""
    dinero = [[0] * (C + 1) for _ in range(V + 1)]
    for i in range(1, V + 1):
        for j in range(C + 1):
            ks = range((1 if (al_menos_una and j > 0) else 0), min(kmax, j) + 1)
            dinero[i][j] = max((dinero[i - 1][j - k] + (pago[k][i - 1] if k else 0) for k in ks), default=0)
    return dinero[V][C]


def _casos_de_lectura(rng, cuantos):
    """Casos donde leer los pagos por vecino da otra respuesta pero un voraz, «como mucho 3 cajas» y
    «al menos una caja» acertarían: solo falla la lectura."""
    ok = []
    while len(ok) < cuantos:
        V = rng.randint(2, 4)
        caso = alea(rng, V, rng.randint(V, 3 * V), 30, 0.3)
        _, C, pago = caso
        b = resuelve(*caso)[0]
        plano = [x for k in range(1, 5) for x in pago[k][:]]            # orden de la entrada
        mal = [[0] * V] + [[0] * V for _ in range(4)]
        for i in range(V):
            for k in range(1, 5):
                mal[k][i] = plano[4 * i + k - 1]
        if (optimo(V, C, mal) != b and optimo(V, C, pago, 3) == b and optimo(V, C, pago, 4, True) == b
                and voraz_marginal(*caso) == b):
            ok.append(caso)
    return ok


def pruebas():
    rng = random.Random(1103)
    L = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        for V, C, pago in casos:
            assert 1 <= V <= 1000 and 0 <= C <= 4 * V and all(0 <= x <= 1000 for k in range(1, 5) for x in pago[k])
        L.append(Prueba(nombre, tipo, entrada=texto(casos), salida=salida(casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    VARIOS = "Vale cualquier reparto óptimo (con como mucho C cajas)."
    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado", [mk([[10, 5, 6, 7], [0, 100, 100, 100], [5, 4, 4, 4]], 5)],
           "3 vecinos y 5 cajas: 10 + 100 + 5 = 115, con 1, 2 (o 3) y 1 cajas. " + VARIOS,
           {"wa": "Falla el primer ejemplo: mira el beneficio (115) y que el reparto no pasa de 5 cajas y recauda ese valor.",
            "pe": "El beneficio va en una línea y las cajas de los vecinos en la siguiente, separadas por un espacio."},
           ["Las cuatro líneas de la entrada son por número de cajas (1, 2, 3, 4), cada una con los V vecinos: no por vecino.",
            "dinero(i, j) = máximo de dinero(i−1, j−k) + pago(i, k) para k de 0 a min(4, j).",
            "El máximo es 115: vender 1 caja al primero, 2 (o 3) al segundo y 1 al tercero."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [mk([[0, 10, 0, 0], [0, 10, 0, 0]], 2)],
           "Dos vecinos que solo pagan por dos cajas y solo hay dos: se atiende a uno (10). " + VARIOS,
           {"wa": "Con solo dos cajas únicamente se puede atender a un vecino: 10, no 20."},
           ["Cada vecino necesita 2 cajas para pagar algo.",
            "Si repartes una caja a cada uno no recaudas nada."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [mk([[100, 50, 30, 10]], 4)],
           "Un solo vecino que paga menos cuantas más cajas compra: se le vende una (100) y sobran tres. " + VARIOS,
           {"wa": "No hace falta vender todas las cajas: a este vecino la mejor opción es 1 caja (100).",
            "rte": "Revisa los límites: C puede ser mayor que lo que se vende."},
           ["Comparar 100, 50, 30 y 10: gana la primera.",
            "dinero(i, j) incluye k = 0 y el máximo se toma sobre «como mucho j cajas»."])

    # ------------------------------------------------------------------ bordes
    prueba("Ninguna caja", "borde", [alea(rng, 3, 0), alea(rng, 1, 0, 1000), alea(rng, 7, 0)],
           "C = 0: no se vende nada, beneficio 0 y todos los vecinos con 0 cajas.",
           {"wa": "Con C = 0 el beneficio es 0 y a cada vecino le corresponden 0 cajas.",
            "rte": "La tabla tiene C + 1 = 1 columna: revisa que no te sales."},
           ["¿Qué escribe tu programa cuando no hay cajas?",
            "dinero(i, 0) = 0 para todo i; no mires j − k con j = 0."])
    prueba("Un solo vecino", "borde", [mk([[0, 7, 9, 3]], 1), mk([[0, 7, 9, 3]], 2), mk([[0, 7, 9, 3]], 3), mk([[0, 7, 9, 3]], 4), mk([[5, 5, 5, 5]], 4), mk([[0, 0, 0, 0]], 3)],
           "Un vecino con distintos números de cajas: se le vende lo que más paga dentro de las cajas que hay.",
           {"wa": "Con V = 1 la respuesta es el máximo de los pagos de 0 a C cajas (no más de 4)."},
           ["Con 1 caja y pago 0 por 1 caja, el beneficio es 0.",
            "Con 3 cajas lo mejor es vender 3 (9)."])

    # ------------------------------------------------------------------ trampas
    prueba("Las líneas son por número de cajas", "trampa", _casos_de_lectura(rng, 5),
           "Cada línea de la entrada es para 1, 2, 3 o 4 cajas, con un valor por vecino: si las lees por vecino, o escribes mal el reparto, todo sale cambiado.",
           {"wa": "Revisa (a) cómo lees los pagos: son cuatro líneas, una por número de cajas (1, 2, 3, 4), cada una con los V vecinos, no cuatro números por vecino; (b) que escribes el beneficio en una línea y, en otra, las cajas de los vecinos EN SU ORDEN; (c) que al reconstruir restas las cajas elegidas.",
            "pe": "El beneficio va en una línea y las cajas de los vecinos en la siguiente, separadas por un espacio."},
           ["El pago del vecino i por k cajas es el número i de la línea k de la entrada: pago[k][i]. Bucle de fuera sobre k y de dentro sobre los vecinos.",
            "Escribe el beneficio y, en la línea siguiente, las cajas del vecino 1, del 2, ... en ese orden.",
            "Reconstruye desde (V, C): elige k para el vecino i y pasa a (i − 1, j − k)."])
    prueba("No hay que vender todas las cajas", "trampa", [mk([[100, 50, 30, 10]], 4), mk([[30, 20, 10, 5], [40, 30, 10, 5], [20, 10, 5, 5]], 12), mk([[9, 3, 1, 0], [8, 2, 0, 0]], 8)],
           "Todos pagan menos cuantas más cajas compran: conviene vender poco y que sobren muchas.",
           {"wa": "Obligas a vender todas las cajas (o al menos una a cada vecino): vender cero o pocas puede ser lo mejor. Cuenta k = 0 y el máximo «como mucho C cajas»."},
           ["En el segundo caso hay 12 cajas pero lo mejor es una a cada vecino (30 + 40 + 20).",
            "dinero(0, j) = 0 para todo j: «sobran cajas» no cuesta nada."])
    prueba("Como mucho 4 cajas por vecino", "trampa", [mk([[10, 20, 30, 40], [10, 20, 30, 40]], 8), mk([[1, 2, 3, 100]], 4), mk([[5, 10, 15, 20], [0, 0, 0, 1]], 8)],
           "El mejor reparto vende exactamente 4 cajas a cada vecino (el pago crece con el número de cajas): el bucle debe llegar hasta 4.",
           {"wa": "Un vecino compra como mucho 4 cajas: el bucle de k llega a 4 (no a 3, ni a j)."},
           ["En el primer caso hay 8 cajas y dos vecinos: 4 + 4 cajas, beneficio 80.",
            "for k de 0 a min(4, j): ni más de 4 ni más de las que quedan."])
    prueba("El voraz no sirve", "trampa", _voraces_que_fallan(rng, 4),
           "Repartir cada caja al vecino que más gana con ella (un voraz) da menos que el óptimo en estos casos.",
           {"wa": "Un voraz (dar cada caja al que más paga por ella) no es óptimo: hay vecinos que solo pagan por lotes de 3 o 4 cajas. Usa la tabla de programación dinámica."},
           ["Mira los vecinos que pagan 0 por 1 caja y mucho por 3 o 4: un voraz no los ve.",
            "dinero(i, j) = máximo sobre k de dinero(i−1, j−k) + pago(i, k): prueba TODAS las opciones."])
    prueba("Solo pagan por lotes", "trampa",
           [mk([[0, 40, 0, 0], [0, 0, 60, 0], [0, 0, 0, 90]], 5), mk([[0, 0, 0, 80], [0, 0, 0, 80], [0, 50, 0, 0]], 6), mk([[0, 0, 70, 0], [0, 0, 70, 0]], 5)],
           "Cada vecino paga solo si recibe un número concreto de cajas: encajar los lotes en las cajas disponibles es una mochila.",
           {"wa": "Hay que encajar los lotes: un vecino que solo paga por 3 cajas no aporta nada con 1 o 2. Revisa los casos k = 0..4 completos y los límites de j − k."},
           ["En el primer caso 5 cajas: 2 + 3 (40 + 60 = 100) mejor que 4 + 1 (90).",
            "La recurrencia no cambia: máximo sobre todas las k."])
    prueba("Reparto válido: no más cajas de las que hay", "trampa", [mk([[10, 10, 10, 10]] * 5, 3), mk([[7, 7, 7, 7]] * 3, 2), mk([[1, 1, 1, 1], [1, 1, 1, 1]], 1)],
           "Todos pagan lo mismo por cualquier número de cajas: hay muchísimos repartos con el mismo beneficio, pero solo valen los que no pasan de C cajas.",
           {"wa": "El reparto suma más cajas de las que hay (o no recauda lo que dices): al reconstruir hay que restar k de j en cada vecino (j −= k) y empezar en (V, C)."},
           ["Con 3 cajas y 5 vecinos que pagan 10 por cualquier cantidad: se atiende a 3 vecinos con 1 caja cada uno (30).",
            "En la reconstrucción, tras elegir k para el vecino i, pasa a (i − 1, j − k)."])
    prueba("Varios casos seguidos", "trampa", [alea(rng, 8, 20), alea(rng, 2, 5), mk([[3, 1, 0, 0]], 1), alea(rng, 4, 0), alea(rng, 6, 20)],
           "Un caso grande y luego otros pequeños: nada del anterior debe quedar en la tabla ni en el reparto.",
           {"wa": "Algo se arrastra de un caso al siguiente (la tabla o el vector de cajas): créalos dentro de resuelveCaso con el tamaño de cada caso.",
            "rte": "La tabla de un caso anterior tenía otro tamaño: créala en cada caso."},
           ["Si el primer caso sale bien y los siguientes no, mira qué vive fuera de la función.",
            "Declara la tabla y el vector de cajas dentro de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    casos = []
    for _ in range(150):
        V = rng.randint(1, 5)
        casos.append(alea(rng, V, rng.randint(0, 4 * V), rng.choice([3, 20, 1000]), rng.choice([0.0, 0.4])))
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "150 casos de hasta 5 vecinos (con muchos empates y valores a 0). " + VARIOS,
           {"wa": "Algún caso falla: es pequeño, prueba a mano los repartos posibles.",
            "pe": "Revisa el formato: beneficio en una línea y cajas en la siguiente."},
           ["Localiza el caso en la entrada y calcula el beneficio máximo a mano.",
            "El «Por qué» del veredicto dice si falla el beneficio o el reparto (suma de cajas, valor recaudado)."])
    casos = []
    for _ in range(30):
        V = rng.randint(10, 40)
        casos.append(alea(rng, V, rng.randint(0, 4 * V), rng.choice([20, 1000]), rng.choice([0.0, 0.3])))
    prueba("Casos medianos al azar", "aleatorio", casos,
           "30 casos de 10 a 40 vecinos. " + VARIOS,
           {"wa": "Los casos pequeños salen bien y estos no: revisa los tamaños de la tabla (V + 1 filas y C + 1 columnas) y la reconstrucción.",
            "tle": "Una recursión sin memoria es de 5^V: no termina. Guarda cada dinero(i, j) en una tabla."},
           ["¿Calculas el mismo dinero(i, j) muchas veces? Apúntalo en una tabla.",
            "Reconstruye desde (V, C) hacia atrás."])

    # ------------------------------------------------------------------ rendimiento
    prueba("1000 vecinos y 4000 cajas", "rendimiento", [alea(rng, 1000, 4000, 1000)],
           "El tamaño máximo: 1.000 vecinos y 4.000 cajas (4 millones de casillas).",
           {"tle": "Debe ser O(V · C · 4): una recursión sin memoria (5^V) no termina.",
            "mle": "La tabla de 1.001 × 4.001 enteros son unos 16 MB: no reserves más (y créala dentro del caso).",
            "rte": "Con tablas tan grandes no uses un array local (pila): usa Matriz o vector."},
           ["V·C = 4·10⁶ casillas con 5 opciones cada una son 2·10⁷ operaciones: muy poco.",
            "Rellena la tabla con tres bucles (i, j, k)."])
    prueba("Casos grandes con pocas cajas", "rendimiento", [alea(rng, 1000, 800, 1000), alea(rng, 1000, 2500, 1000, 0.5), alea(rng, 1000, 0, 1000)],
           "Tres casos de 1.000 vecinos: 800 cajas, 2.500 cajas con muchos pagos a 0 y ninguna caja.",
           {"tle": "Debe ser O(V · C) por caso.",
            "mle": "Crea la tabla dentro del caso para que se libere al terminar.",
            "wa": "Con pocas cajas la mayoría de vecinos se queda en 0: revisa que reconstruyes bien."},
           ["Con C = 0 el caso es trivial (todo ceros).",
            "No copies la tabla al llamar a funciones: pásala por referencia."])
    return L


def _voraces_que_fallan(rng, cuantos):
    ok = []
    while len(ok) < cuantos:
        V = rng.randint(2, 5)
        caso = alea(rng, V, rng.randint(2, 4 * V - 2), 30, 0.4)
        if voraz_marginal(*caso) < resuelve(*caso)[0]:
            ok.append(caso)
    return ok


# ------------------------------------------------------------ variantes (fallos típicos)
VORAZ = """void resuelveCaso() {
    int V0, C0; cin >> V0 >> C0;
    vector<array<int, 5>> p(V0 + 1);
    for (int i = 1; i <= V0; ++i) p[i][0] = 0;
    for (int k = 1; k <= 4; ++k) for (int i = 1; i <= V0; ++i) cin >> p[i][k];
    vector<int> c(V0 + 1, 0); long long tot = 0;
    for (int paso = 0; paso < C0; ++paso) {
        int bi = -1, bg = 0;
        for (int i = 1; i <= V0; ++i) if (c[i] < 4) { int g = p[i][c[i] + 1] - p[i][c[i]]; if (g > bg) { bg = g; bi = i; } }
        if (bi < 0) break;
        ++c[bi]; tot += bg;
    }
    cout << tot << '\\n';
    for (int i = 1; i <= V0; ++i) cout << c[i] << (i < V0 ? ' ' : '\\n');
    return;
"""

RECURSIVA = """int rec(Matriz<int> const& pg, int i, int j) {
    if (i == 0) return 0;
    int r = 0;
    for (int k = 0; k <= min(4, j); ++k) r = max(r, rec(pg, i - 1, j - k) + pg[i][k]);
    return r;
}

void resuelveCaso() {
    int V0, C0; cin >> V0 >> C0;
    Matriz<int> pg(V0 + 1, 5, 0);
    for (int k = 1; k <= 4; ++k) for (int i = 1; i <= V0; ++i) cin >> pg[i][k];
    cout << rec(pg, V0, C0) << '\\n';
    vector<int> cj(V0 + 1, 0);
    for (int i = V0, j = C0; i >= 1; --i)
        for (int k = 0; k <= min(4, j); ++k)
            if (rec(pg, i, j) == rec(pg, i - 1, j - k) + pg[i][k]) { cj[i] = k; j -= k; break; }
    for (int i = 1; i <= V0; ++i) cout << cj[i] << (i < V0 ? ' ' : '\\n');
    return;
"""

VARIANTES = [
    Variante("lee los pagos por vecino (no por número de cajas)",
             [("    for (int k = 1; k <= 4; ++k)\n        for (int i = 1; i <= V; ++i) cin >> pago[i][k];", "    for (int i = 1; i <= V; ++i)\n        for (int k = 1; k <= 4; ++k) cin >> pago[i][k];")], prueba=6, v="wa"),
    Variante("como mucho 3 cajas por vecino", [("min(4, j)", "min(3, j)")], prueba=8, v="wa"),
    Variante("a cada vecino le vende al menos una caja", [("for (int k = 0; k <= min(4, j); ++k)\n                mejor = max(mejor,", "for (int k = (j > 0); k <= min(4, j); ++k)\n                mejor = max(mejor,")], prueba=10, v="wa"),
    Variante("no resta las cajas al reconstruir", [("                j -= k;\n", "")], prueba=6, v="wa"),
    Variante("escribe solo el beneficio", [("    for (int i = 1; i <= V; ++i) cout << cajas[i] << (i < V ? ' ' : '\\n');\n", "")], prueba=6, v="wa"),
    Variante("escribe el reparto al revés", [("for (int i = 1; i <= V; ++i) cout << cajas[i] << (i < V ? ' ' : '\\n');", "for (int i = V; i >= 1; --i) cout << cajas[i] << (i > 1 ? ' ' : '\\n');")], prueba=12, v="wa"),
    Variante("voraz: cada caja al que más gana con ella", [("#include <vector>", "#include <vector>\n#include <array>"), ("void resuelveCaso() {", VORAZ)], prueba=9, v="wa"),
    Variante("recursión sin memoria (5^V)", [("void resuelveCaso() {", RECURSIVA)], prueba=[14], v="tle"),
]


def ALTERNATIVA(entrada):
    """Otro reparto óptimo: en los empates vende más cajas."""
    v = list(map(int, entrada.split()))
    p, casos = 1, []
    for _ in range(v[0]):
        V, C = v[p], v[p + 1]
        p += 2
        pago = [[0] * V]
        for k in range(1, 5):
            pago.append(v[p:p + V])
            p += V
        casos.append((V, C, pago))
    return salida(casos, mas_cajas=True)
