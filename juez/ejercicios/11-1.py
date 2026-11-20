"""11-1 · El cazatesoros: juez con pruebas pensadas para cada error típico.

Es la mochila 0/1: cada cofre pesa 3·p segundos (p de bajada y 2·p de subida) y vale su oro.
El enunciado admite CUALQUIER conjunto óptimo de cofres, en cualquier orden: el comprobador
(juez/ejercicios/comprobadores/11-1.py y .js) mira que el oro sea el máximo, que los cofres existan
(sin usar ninguno dos veces), que quepan en la botella y que sumen ese oro. ALTERNATIVA da otra
solución óptima (desempata cogiendo el cofre) y el verificador comprueba que se acepta.

El solucionador es propio: tabla por filas con lista de «cogido» y se ha validado contra fuerza
bruta (todos los subconjuntos) en miles de casos pequeños.
"""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "11-Programacion dinamica II/EJ_11-1/EJ_11-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["int tiempo = 3 * prof[i];", "int tiempo = prof[i];"],
}


def resuelve(T, cofres, coge_en_empate=False):
    """(oro máximo, índices de los cofres cogidos en el orden de la entrada)."""
    fila = [0] * (T + 1)
    filas = [fila]
    for p, o in cofres:
        w = 3 * p
        if w > T:
            nueva = fila[:]
        else:
            nueva = fila[:w] + [a if a >= b + o else b + o for a, b in zip(fila[w:], fila)]
        filas.append(nueva)
        fila = nueva
    j, coge = T, []
    for i in range(len(cofres), 0, -1):
        p, o = cofres[i - 1]
        w = 3 * p
        antes = filas[i - 1]
        if w <= j and (filas[i][j] != antes[j] or (coge_en_empate and antes[j - w] + o == filas[i][j])):
            coge.append(i - 1)
            j -= w
    return fila[T], coge[::-1]


def bloque(T, cofres, coge_en_empate=False):
    oro, coge = resuelve(T, cofres, coge_en_empate)
    return f"{oro}\n{len(coge)}\n" + "".join(f"{cofres[i][0]} {cofres[i][1]}\n" for i in coge) + "---\n"


def caso_a_texto(c):
    T, cofres = c
    return f"{T}\n{len(cofres)}\n" + "".join(f"{p} {o}\n" for p, o in cofres)


def aleatorio(rng, nmax, tmax, pmax, omax=10000):
    n = rng.randint(1, nmax)
    return (rng.randint(1, tmax), [(rng.randint(1, pmax), rng.randint(1, omax)) for _ in range(n)])


EXPLICA = "Si hay varias soluciones óptimas vale cualquiera, con los cofres en cualquier orden."


def pruebas():
    rng = random.Random(1101)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append(Prueba(nombre, tipo,
                        entrada=f"{len(casos)}\n" + "".join(caso_a_texto(c) for c in casos),
                        salida="".join(bloque(*c) for c in casos), casos=len(casos),
                        comprueba=comprueba, si=si, pistas=pistas))

    # ------------------------------------------------------------------ enunciado
    prueba("Ejemplo 1 del enunciado", "enunciado", [(210, [(40, 5), (40, 1), (25, 2)])],
           "El primer ejemplo del PDF: los dos cofres de 40 m no caben juntos. " + EXPLICA,
           {"wa": "Falla el primer ejemplo: revisa el coste de cada cofre (3·p segundos), la recurrencia y el formato (oro, número de cofres, un cofre por línea y ---).",
            "pe": "Los datos están bien pero no el formato: cada cosa en su línea y «---» al final de cada caso."},
           ["Calcula a mano lo que cuesta cada cofre: bajar p y subir 2·p.",
            "Es una mochila 0/1: oro(i, j) = máximo oro con los cofres 1..i y j segundos.",
            "Escribe el oro, el número de cofres, cada cofre como «profundidad oro» y después «---»."])
    prueba("Ejemplo 2 del enunciado", "enunciado", [(200, [(25, 4), (50, 5), (40, 4), (10, 2), (70, 10)])],
           "El segundo ejemplo del PDF: coger primero el cofre más valioso que cabe no es lo mejor.",
           {"wa": "Sale 7 en vez de 8: estás eligiendo de forma voraz (el más valioso primero). Hace falta programación dinámica."},
           ["Con 200 segundos, ¿qué da coger primero el de 5 monedas? ¿Y los de 25 y 40 metros?",
            "Ninguna regla voraz (por oro, por tiempo o por oro/tiempo) sirve en la mochila 0/1: rellena la tabla oro(i, j)."])
    prueba("Ejemplo 3 del enunciado", "enunciado", [(29, [(10, 20)])],
           "El tercer ejemplo del PDF: el único cofre cuesta 30 segundos y la botella da 29. Se escribe 0, 0 y ---.",
           {"wa": "Coges el cofre: cuesta 10 de bajada y 20 de subida, 30 en total, y no cabe. Si no coges nada, escribe «0», «0» y «---»."},
           ["¿Cuánto cuesta subir un cofre que está a 10 metros?",
            "El tiempo de un cofre es p + 2·p = 3·p."])
    prueba("Ejemplo 4 del enunciado", "enunciado", [(60, [(12, 7), (10, 5), (8, 4), (10, 6)])],
           "El cuarto ejemplo del PDF: dos formas de llegar a 11 gastando justo los 60 segundos. " + EXPLICA,
           {"wa": "Las dos soluciones gastan EXACTAMENTE los 60 segundos: si sale menos de 11, un cofre que cabe justo no lo estás cogiendo (¿< en vez de ≤?)."},
           ["12 + 8 = 20 metros son 60 segundos, justo lo que da la botella.",
            "Un cofre cabe si 3·p ≤ j, con igual incluido."])

    # ------------------------------------------------------------------ trampas
    prueba("Formato: profundidad, oro y --- en cada caso", "trampa",
           [(100, [(20, 7)]), (50, [(10, 3), (60, 9)])],
           "Dos casos sencillos (un cofre en cada uno): hay que escribir el oro, el número de cofres, cada cofre como «profundidad oro» y «---» tras CADA caso.",
           {"wa": "Mira el «Por qué»: o falta la línea «---», o falta la línea con el número de cofres, o escribes los cofres como «oro profundidad» (es al revés: primero la profundidad).",
            "pe": "Los datos son correctos pero mal repartidos en líneas: el oro en una línea, el número de cofres en otra y un cofre por línea."},
           ["La salida esperada del primer caso es «7», «1», «20 7» y «---», cada una en su línea.",
            "Cada cofre se escribe como aparece en la entrada: primero la profundidad y luego el oro.",
            "No olvides escribir «---» al final de cada caso, también del último."])
    prueba("Cabe justo: 3·p igual a T", "trampa", [(30, [(10, 7)])],
           "Un cofre a 10 m con una botella de 30 segundos: cuesta exactamente 30 y se puede subir.",
           {"wa": "No coges un cofre que cabe justo: la condición es 3·p ≤ j (con igual). Revisa también que la tabla llega hasta la columna T incluida."},
           ["Bajar 10 y subir 20 son 30 segundos: los que hay.",
            "Usa ≤ al comprobar si el cofre cabe, y que el bucle de j llegue hasta T (j <= T)."])
    prueba("Subir cuesta el doble que bajar", "trampa", [(40, [(10, 9), (5, 4)])],
           "Cofres a 10 y 5 m con 40 segundos de aire: cuestan 30 y 15 segundos, no caben los dos y se sube solo el de 9 monedas.",
           {"wa": "Coges los dos cofres: estás contando p o 2·p segundos por cofre. Bajar cuesta p y subir 2·p: en total 3·p."},
           ["¿Cuánto se tarda en bajar y subir desde 10 metros? ¿Y desde 5?",
            "El peso de cada cofre en la mochila es 3·p, tanto al rellenar la tabla como al reconstruir."])
    prueba("Cada cofre se sube una sola vez", "trampa", [(60, [(10, 5)])],
           "Un único cofre de 30 segundos y 60 de aire: cabría dos veces, pero solo hay uno (respuesta 5).",
           {"wa": "Sale 10: usas el mismo cofre dos veces. En la mochila 0/1, si coges el cofre i, el resto sale de la fila i − 1: oro(i − 1, j − 3·p) + o, no oro(i, j − 3·p) + o.",
            "rte": "Algo se sale de rango al reconstruir: si tu tabla deja repetir cofres, la reconstrucción no cuadra."},
           ["Con un solo cofre, ¿cuánto oro puede haber como mucho?",
            "Si la tabla es de una fila, recórrela con j de T hacia 0; si es entera, usa la fila i − 1 al coger el cofre i."])
    prueba("Ningún cofre cabe", "trampa", [(100, [(34, 50), (500, 10000), (40, 7)])],
           "Todos los cofres cuestan más de 100 segundos: se escribe «0», «0» y «---».",
           {"wa": "Si no se coge ningún cofre hay que escribir igualmente la línea con el 0 (número de cofres) y el «---».",
            "rte": "Con cofres más hondos que la botella, j − 3·p es negativo: comprueba que cabe antes de mirar esa casilla."},
           ["¿Qué escribe tu programa cuando no cabe nada?",
            "La salida es siempre: oro, número de cofres (aunque sea 0), los cofres y «---»."])
    prueba("Cofre muchísimo más hondo que la botella", "trampa", [(1, [(500, 10000)]), (3, [(1, 4), (500, 9)])],
           "Botellas de 1 y 3 segundos con un cofre a 500 m (1.500 segundos): j − 3·p queda muy negativo.",
           {"rte": "Accedes a oro(i − 1, j − 3·p) con un índice negativo. Comprueba 3·p ≤ j ANTES de mirar esa casilla.",
            "wa": "Coges un cofre que no cabe o lees basura de fuera de la tabla: comprueba 3·p ≤ j antes de usar j − 3·p."},
           ["¿Qué vale j − 3·p con j = 1 y p = 500?",
            "Solo se puede coger el cofre si 3·p ≤ j: si no, oro(i, j) = oro(i − 1, j)."])
    prueba("Reconstrucción: descontar el tiempo del cofre cogido", "trampa", [(30, [(10, 5), (10, 6)])],
           "Dos cofres de 30 segundos y 30 de aire: solo se puede subir uno, el de 6 monedas.",
           {"wa": "Escribes los dos cofres: al reconstruir, cuando decides que el cofre i está cogido hay que pasar a (i − 1, j − 3·p_i), descontando su tiempo."},
           ["Tu oro es 6, pero ¿cuánto tiempo suman los cofres que escribes?",
            "Reconstruye desde (N, T): si oro(i, j) ≠ oro(i − 1, j), el cofre i está cogido y j baja en 3·p_i."])
    prueba("Voraz por oro/tiempo no sirve", "trampa", [(60, [(12, 40), (10, 30), (10, 30)])],
           "El cofre de 12 m es el que más oro da por segundo, pero los dos de 10 m juntos dan más (60 frente a 40).",
           {"wa": "Ordenas por oro/segundo y coges los mejores: en la mochila 0/1 eso no da el óptimo. Rellena la tabla."},
           ["Coger el de 12 m deja 24 segundos: no cabe ninguno más.",
            "Hace falta probar las dos opciones para cada cofre: cogerlo o no (programación dinámica)."])
    prueba("Cofres repetidos", "trampa", [(60, [(10, 5), (10, 5)]), (95, [(5, 1), (5, 1), (5, 1), (25, 2)])],
           "Cofres idénticos (misma profundidad y oro): si se cogen varios, se escribe cada uno en su línea.",
           {"wa": "Hay cofres iguales y hay que escribirlos todos los que se cojan: no los juntes ni te saltes los repetidos."},
           ["En el primer caso se cogen los dos cofres «10 5»: van dos líneas iguales.",
            "Marca los cofres cogidos por su posición en la entrada, no por su valor."])
    prueba("Un cofre de cada clase", "borde",
           [(1500, [(500, 10000)]), (10000, [(1, 1)]), (3, [(1, 10000), (1, 9999)])],
           "Valores extremos: un cofre a 500 m que cabe justo, el cofre más barato y dos de 1 m con un solo hueco.",
           {"wa": "Algún caso extremo falla: revisa ≤ en la condición de que cabe y que no repites cofres."},
           ["El primer cofre cuesta 1.500 segundos, justo la botella.",
            "En el último solo cabe uno de los dos cofres de 1 m (3 segundos): el de 10.000."])
    casos = [(600, [(rng.randint(1, 40), rng.randint(1, 10000)) for _ in range(12)]),
             (90, [(10, 3), (10, 4), (20, 9)]), (29, [(10, 20)]), (1, [(1, 1)]),
             (300, [(30, 8), (20, 1), (10, 2), (40, 9)]), (30, [(10, 1)])]
    prueba("Varios casos seguidos", "trampa", casos,
           "Un caso de 12 cofres con varios cogidos seguido de casos más pequeños: nada de un caso debe pasar al siguiente.",
           {"wa": "El primer caso sale bien y los siguientes no: algo no se reinicia (la tabla, las marcas de cofres cogidos o el contador).",
            "rte": "Un vector de un caso anterior con otro tamaño: créalos dentro de cada caso."},
           ["Tras un caso con muchos cofres cogidos, ¿quedan marcas en tu vector de cogidos?",
            "Declara la tabla, el vector de cogidos y el contador dentro de resuelveCaso."])

    # ------------------------------------------------------------------ aleatorios
    casos = [aleatorio(rng, 8, 300, 40, 50) for _ in range(150)]
    prueba("Casos pequeños al azar", "aleatorio", casos,
           "150 casos de hasta 8 cofres con poco oro (muchos empates entre soluciones). " + EXPLICA,
           {"wa": "Algún caso falla: localiza el caso en la entrada (son pequeños) y resuélvelo a mano."},
           ["El «Por qué» dice qué falla: el oro máximo, un cofre que no existe o que no caben.",
            "Prueba ese caso en tu ordenador y compara con todas las combinaciones de cofres."])
    casos = [aleatorio(rng, 18, 3000, 200) for _ in range(30)]
    prueba("Casos medianos al azar", "aleatorio", casos,
           "30 casos de hasta 18 cofres y 3.000 segundos.",
           {"wa": "Algún caso mediano falla: revisa la recurrencia y la reconstrucción."},
           ["Si los pequeños salen bien y estos no, revisa los tamaños de la tabla (N + 1 filas y T + 1 columnas).",
            "Comprueba que la reconstrucción empieza en (N, T)."])

    # ------------------------------------------------------------------ rendimiento
    prueba("100 cofres poco hondos y 10.000 segundos", "rendimiento",
           [(10000, [(rng.randint(1, 30), rng.randint(1, 10000)) for _ in range(100)])],
           "El caso más grande con cofres baratos: caben muchísimas combinaciones.",
           {"tle": "Pruebas todas las combinaciones (recursión sin memoria, 2¹⁰⁰): guarda los resultados en la tabla oro(i, j).",
            "mle": "La tabla debe ser (N + 1) × (T + 1) enteros: no reserves más."},
           ["¿Cuántas veces calculas el mismo oro(i, j)?",
            "Rellena la tabla de N + 1 filas y T + 1 columnas con dos bucles: O(N·T)."])
    casos = [(10000, [(rng.randint(1, 500), rng.randint(1, 10000)) for _ in range(100)]) for _ in range(25)]
    prueba("25 casos de 100 cofres y 10.000 segundos", "rendimiento", casos,
           "Muchos casos del tamaño máximo: mide el coste O(N·T) por caso.",
           {"tle": "Debe costar O(N·T) por caso. ¿Recursión sin memoria, o un map en lugar de una tabla?",
            "mle": "No hace falta más que una tabla (N + 1) × (T + 1) por caso; libérala al acabar el caso (créala dentro)."},
           ["10⁶ casillas por caso es poco; 25 casos también. Si no, algo repite trabajo.",
            "Usa vector<vector<int>> y bucles, no map ni recursión sin memoria."])
    return P


RECURSIVA = """int rec(vector<int> const& prof, vector<int> const& oro, int i, int j) {
    if (i == 0) return 0;
    int r = rec(prof, oro, i - 1, j);
    if (3 * prof[i] <= j) r = max(r, rec(prof, oro, i - 1, j - 3 * prof[i]) + oro[i]);
    return r;
}

void resuelveCaso() {"""

VARIANTES = [
    Variante("no escribe ---", [('cout << "---\\n";', "")], prueba=5, v="wa"),
    Variante("escribe oro y profundidad", [("cout << prof[i] << ' ' << oro[i] << '\\n';", "cout << oro[i] << ' ' << prof[i] << '\\n';")], prueba=5, v="wa"),
    Variante("cabe solo si sobra tiempo (<)", [("if (tiempo <= j)", "if (tiempo < j)")], prueba=6, v="wa"),
    Variante("cuenta solo la bajada (p)", [("int tiempo = 3 * prof[i];", "int tiempo = prof[i];"), ("j -= 3 * prof[i];", "j -= prof[i];")], prueba=7, v="wa"),
    Variante("subir cuesta lo mismo que bajar (2p)", [("int tiempo = 3 * prof[i];", "int tiempo = 2 * prof[i];"), ("j -= 3 * prof[i];", "j -= 2 * prof[i];")], prueba=7, v="wa"),
    Variante("repite cofres (fila i)", [("mejor[i - 1][j - tiempo] + oro[i]", "mejor[i][j - tiempo] + oro[i]")], prueba=8, v="wa"),
    Variante("sin número de cofres si es 0", [("cout << mejor[N][T] << '\\n' << numCofres << '\\n';", "cout << mejor[N][T] << '\\n'; if (numCofres) cout << numCofres << '\\n';")], prueba=9, v="wa"),
    Variante("no descuenta el tiempo al reconstruir", [("            j -= 3 * prof[i];\n", "")], prueba=11, v="wa"),
    Variante("marcas de cogidos sin reiniciar", [("vector<bool> cogido(N + 1, false);", "static vector<bool> cogido(101, false);")], prueba=15, v="wa"),
    Variante("recursión sin memoria",
             [("void resuelveCaso() {", RECURSIVA),
              ("            mejor[i][j] = mejor[i - 1][j];\n            if (tiempo <= j) mejor[i][j] = max(mejor[i][j], mejor[i - 1][j - tiempo] + oro[i]);",
               "            (void)tiempo;"),
              ("if (mejor[i][j] != mejor[i - 1][j]) {", "if (rec(prof, oro, i, j) != rec(prof, oro, i - 1, j)) {"),
              ("cout << mejor[N][T] << '\\n' << numCofres", "cout << rec(prof, oro, N, T) << '\\n' << numCofres")],
             prueba=[18, 19], v="tle"),
]


# ---------------------------------------------------------------- respuesta alternativa
def ALTERNATIVA(entrada):
    """Otra respuesta óptima: al reconstruir, en caso de empate se coge el cofre."""
    v = list(map(int, entrada.split()))
    p, out = 1, []
    for _ in range(v[0]):
        T, n = v[p], v[p + 1]
        p += 2
        cofres = [(v[p + 2 * k], v[p + 2 * k + 1]) for k in range(n)]
        p += 2 * n
        out.append(bloque(T, cofres, coge_en_empate=True))
    return "".join(out)
