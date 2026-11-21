"""01-2 · Encontrar el k-ésimo elemento en un árbol AVL: juez con pruebas pensadas para cada error
típico (repetidos, posiciones inexistentes, tami en las rotaciones, coste logarítmico...)."""
import pathlib
import random
from _comun import Prueba, Variante

CONFIG = {
    # El ejercicio consiste en ampliar la clase Set (tami y kesimo). En el juez la clase va en el mismo
    # fichero: la solución de referencia lleva TreeSet_AVL_plantilla.h incrustada y la plantilla del
    # alumno trae la versión de clase SIN tami ni kesimo. Así no se puede incluir la cabecera resuelta.
    "solucion": "juez/soluciones/01-2.cpp",
    "plantilla": "juez/plantillas/01-2.cpp",
    "cabeceras": ["1-Arboles AVL/EJ_01-2/bintree.h"],
    "limite_ms": 3000,
    "fallo": ["cout << \"??\\n\";", "cout << \"?\\n\";"],
}

# Restricciones del enunciado: 1 ≤ N ≤ 300.000 valores entre 1 y 1.000.000 (con repetidos),
# 1 ≤ M ≤ N consultas con posiciones entre 1 y N; la entrada acaba con N = 0.
VMAX = 1_000_000


def resuelve(valores, consultas):
    """Solucionador independiente: el conjunto ordenado (sin repetidos) y su posición k-1."""
    orden = sorted(set(valores))
    return [str(orden[k - 1]) if k <= len(orden) else "??" for k in consultas]


def caso(valores, consultas):
    n = len(valores)
    assert 1 <= n <= 300000 and 1 <= len(consultas) <= n
    assert all(1 <= v <= VMAX for v in valores) and all(1 <= k <= n for k in consultas)
    return valores, consultas


def caso_azar(rng, n, vmax, m=None):
    vals = [rng.randint(1, vmax) for _ in range(n)]
    m = m if m is not None else rng.randint(1, n)
    return caso(vals, [rng.randint(1, n) for _ in range(m)])


def pruebas():
    rng = random.Random(1201)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        P.append((nombre, tipo, [caso(v, c) for v, c in casos], comprueba, si, pistas))

    # --- enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [([15, 20, 25, 30], [1, 3]), ([16, 8, 4, 4, 32], [2, 4, 5]), ([7], [1])],
           "Los tres casos del PDF, con un valor repetido y una posición que no existe.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (N, los valores, M y las posiciones), el k-ésimo o el formato (un valor o ?? por línea y --- tras cada caso).",
            "pe": "Los valores son correctos pero el formato no: cada consulta en su línea y una línea con --- al final de cada caso.",
            "rte": "El programa se rompe con el ejemplo: ¿capturas la excepción de kesimo cuando la posición no existe?"},
           ["Ejecuta el ejemplo en tu ordenador y compara línea a línea.",
            "No hay número de casos: se lee hasta encontrar N = 0.",
            "Cada consulta escribe el elemento o «??», y tras las consultas de cada caso se escribe «---»."])

    # --- bordes
    prueba("Un único valor", "borde", [([5], [1]), ([VMAX], [1]), ([1], [1])],
           "Conjuntos de un solo elemento (incluidos los valores mínimo y máximo, 1 y 1.000.000): la posición 1 es ese elemento.",
           {"wa": "Con un solo elemento, kesimo(1) debe ser la raíz: revisa el valor inicial de tami (1 en un nodo nuevo) y la comparación k == tami.",
            "rte": "Con un solo nodo accedes a un hijo vacío: revisa el caso k == tami."},
           ["En un nodo recién creado, tami vale 1 (hijo izquierdo vacío + 1).",
            "Si k == tami, la respuesta es la raíz de ese subárbol."])
    prueba("Todos los valores iguales", "borde", [([7, 7, 7, 7, 7], [1, 2, 3, 4, 5])],
           "Cinco 7: el conjunto es {7}; la posición 1 es 7 y las demás no existen (??).",
           {"wa": "Insertas los repetidos como elementos nuevos o cuentas mal el tamaño: un conjunto no tiene repetidos, {7, 7, 7, 7, 7} = {7}.",
            "rte": "Al pedir una posición que no existe accedes a un nodo vacío: lanza la excepción (o escribe ??) en vez de seguir."},
           ["¿Cuántos elementos tiene el conjunto después de insertar cinco 7?",
            "insert no hace nada si el elemento ya está: ni crea nodo ni cambia tami."])
    vals = rng.sample(range(2, VMAX), 18) + [1, VMAX]
    rng.shuffle(vals)
    prueba("Primera y última posición", "borde", [(vals, [1, 20, 1, 20])],
           "20 valores distintos (entre ellos 1 y 1.000.000): la posición 1 es el menor y la 20 el mayor.",
           {"wa": "Fallas en los extremos: k = 1 es el elemento más a la izquierda y k = tamaño el más a la derecha. Revisa la bajada por la derecha (k − tami) y el desplazamiento de 1."},
           ["La posición 1 es el mínimo; la posición «número de elementos», el máximo.",
            "Para llegar al máximo hay que bajar siempre por la derecha restando tami en cada paso."])

    # --- trampas
    prueba("Formato: ??, --- y el 0 final", "trampa", [([9, 9, 9], [3])],
           "Un caso mínimo: {9} y la posición 3 no existe. Debe salir exactamente «??» y luego «---», y nada más (el 0 final no es un caso).",
           {"wa": "Algo falla en el formato básico: escribe exactamente «??» (dos interrogaciones) si la posición no existe, una línea «---» tras CADA caso, y para cuando N sea 0 (el 0 no es un caso: no escribas otro «---»). Si escribes un 9, estás guardando los repetidos."},
           ["Mira tu salida completa: ¿termina con una sola línea «---»?",
            "La entrada acaba con N = 0: en ese momento hay que salir sin escribir nada.",
            "«if (!cin || n == 0) return false;» al principio de resuelveCaso, y cout << \"??\\n\" en el catch."])
    prueba("Las posiciones empiezan en 1", "trampa", [([40, 20, 60, 10, 30, 50, 70], [1, 2, 4, 7])],
           "La posición 1 es el menor elemento (10), no el segundo.",
           {"wa": "Cuentas las posiciones desde 0: kesimo(1) es el MENOR elemento. Con tami = tamaño del izquierdo + 1, la raíz está en la posición tami (empezando en 1)."},
           ["Con {10, 20, ..., 70}, la posición 1 debe dar 10.",
            "No restes 1 a k antes de llamar a kesimo: tami ya cuenta desde 1."])
    prueba("Repetidos: posiciones que ya no existen", "trampa", [([2, 1, 3, 3, 2, 3], [4, 3, 6, 1, 5, 2])],
           "Seis valores pero solo 3 distintos: las posiciones 4, 5 y 6 no existen (??) y la 3 es el mayor.",
           {"wa": "Guardas los repetidos (multiset, vector ordenado sin quitar duplicados...) o confundes N con el tamaño del conjunto. Hay posiciones entre 1 y N que no corresponden a ningún elemento."},
           ["El conjunto es {1, 2, 3}: ¿qué debe salir para la posición 4?",
            "Si un valor ya está en el árbol, insert no hace nada.",
            "La posición k existe solo si k ≤ número de elementos DISTINTOS."])
    prueba("Bajar por la derecha restando tami", "trampa", [([4, 2, 6, 1, 3, 5, 7], [6, 7, 5, 3, 1])],
           "Árbol perfecto 1..7: para la posición 6 hay que bajar a la derecha buscando la posición 6 − 4 = 2.",
           {"wa": "Al bajar por la derecha sigues buscando la misma k. Al pasar al hijo derecho te saltas la raíz y todo su hijo izquierdo: busca k − tami."},
           ["En la raíz (4, tami 4), la posición 6 está a la derecha. ¿Qué posición ocupa dentro del subárbol derecho?",
            "k < tami → izquierda con k; k == tami → raíz; k > tami → derecha con k − tami."])
    prueba("Repetido que baja por la izquierda", "trampa", [([4, 2, 6, 1, 3, 5, 7, 1], [4, 2, 3, 5, 7, 1, 8])],
           "Tras construir 1..7 se vuelve a insertar el 1: su búsqueda baja dos veces por la izquierda y no debe cambiar ningún tami.",
           {"wa": "Sumas 1 a tami al bajar por la izquierda aunque el valor ya estuviera: solo hay que sumarlo si de verdad se ha insertado un nodo nuevo (crece == true)."},
           ["Tras insertar el 1 repetido, ¿cuánto vale tami en la raíz? Debe seguir siendo 4.",
            "Actualiza tami DESPUÉS de saber si la inserción en el hijo izquierdo ha tenido éxito."])
    prueba("Rotaciones a la derecha", "trampa", [([5, 4, 3, 2, 1], [5, 4, 3, 2, 1])],
           "Valores decrecientes: el árbol se reequilibra con rotaciones a la derecha y tami tiene que seguir siendo correcto.",
           {"wa": "No actualizas tami en rotaDer: el nodo que baja (r2) pierde a r1 y a su hijo izquierdo, así que r2->tami -= r1->tami."},
           ["Dibuja el árbol tras insertar 5, 4, 3 y la rotación: ¿cuánto debe valer tami en el 5?",
            "En una rotación a la derecha solo cambia el tami del nodo que baja.",
            "En rotaDer(r2), con r1 = r2->iz: r2->tami -= r1->tami."])
    prueba("Rotaciones a la izquierda", "trampa", [([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])],
           "Valores crecientes: el árbol se reequilibra con rotaciones a la izquierda y tami tiene que seguir siendo correcto.",
           {"wa": "No actualizas tami en rotaIzq: el nodo que sube (r2) gana a r1 y a todo su hijo izquierdo, así que r2->tami += r1->tami."},
           ["Dibuja el árbol tras insertar 1, 2, 3 y la rotación: ¿cuánto debe valer tami en el 2?",
            "En una rotación a la izquierda solo cambia el tami del nodo que sube.",
            "En rotaIzq(r1), con r2 = r1->dr: r2->tami += r1->tami."])
    prueba("Rotaciones dobles", "trampa",
           [([3, 1, 2], [1, 2, 3]), ([1, 3, 2], [1, 2, 3]),
            ([50, 20, 80, 10, 30, 25, 27, 70, 90, 75, 72], list(range(1, 12)))],
           "Inserciones que provocan rotaciones izquierda-derecha y derecha-izquierda.",
           {"wa": "Las rotaciones dobles dejan tami mal. Si las escribes a mano, es fácil equivocarse: hazlas como composición de las dos simples (que ya actualizan tami)."},
           ["Inserta 3, 1, 2 a mano y comprueba tami en los tres nodos.",
            "rotaIzqDer(a) = rotaIzq(a->iz) y después rotaDer(a); así no hay que tocar tami aparte."])
    prueba("Consultas desordenadas y repetidas", "trampa",
           [([12, 5, 30, 5, 18, 1, 44, 30, 9, 27], [8, 1, 8, 3, 10, 2, 9, 1, 7, 4])],
           "Las consultas no vienen en orden y se repiten: cada una se responde por sí sola.",
           {"wa": "Supones que las consultas vienen ordenadas (por ejemplo, avanzando un iterador de una a otra) o cambias el árbol al consultar. Cada consulta empieza desde la raíz."},
           ["¿Qué pasa con tu programa si después de la posición 8 se pide la 1?",
            "kesimo no modifica nada: baja desde la raíz en cada consulta."])
    grande = caso_azar(rng, 2000, 5000, 50)
    prueba("Varios casos seguidos", "trampa",
           [grande, ([3, 1, 2], [1, 2, 3]), ([10], [1]), ([6, 6], [1, 2]), ([4, 8, 2, 6], [4, 1])],
           "Un caso grande seguido de otros pequeños: el conjunto de cada caso empieza vacío.",
           {"wa": "El conjunto (o un contador) se arrastra de un caso al siguiente: declara el Set dentro de resuelveCaso, no global ni static."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de resuelveCaso.",
            "Declara Set<int> arbol; dentro de la función de cada caso."])

    # --- aleatorios
    pequenos = [caso_azar(rng, n, rng.choice([3, 10, 30, 1000]))
                for n in [rng.randint(1, 15) for _ in range(250)]]
    prueba("Aleatorios pequeños", "aleatorio", pequenos,
           "250 casos pequeños al azar, muchos con valores repetidos.",
           {"wa": "Hay algún caso concreto que no tratas: busca el caso por las líneas «---» de la salida y pruébalo solo.",
            "rte": "Algún caso rompe tu programa: busca cuál con las líneas «---»."},
           ["Cuenta los «---» antes de la línea que falla para saber qué caso es.",
            "Inserta esos valores a mano, dibuja el árbol con los tami y sigue la búsqueda."])
    medianos = [caso_azar(rng, n, rng.choice([n // 2 + 1, 5 * n, VMAX]))
                for n in [rng.randint(100, 3000) for _ in range(25)]]
    prueba("Aleatorios medianos", "aleatorio", medianos,
           "25 casos de hasta 3.000 valores, con muchas rotaciones de todos los tipos.",
           {"wa": "Con muchas rotaciones algún tami acaba mal: llama a comprueba() del .h tras cada insert mientras depuras.",
            "rte": "Con árboles medianos se rompe: revisa los punteros en las rotaciones."},
           ["Usa assert(arbol.comprueba()) tras cada inserción para encontrar el primer tami incorrecto.",
            "Repasa los cuatro tipos de rotación con un dibujo."])

    # --- rendimiento
    n = 100000
    prueba("100.000 valores crecientes y 100.000 consultas", "rendimiento",
           [(list(range(1, n + 1)), [rng.randint(n // 2, n) for _ in range(n)])],
           "Insertar en orden creciente (peor caso de un árbol sin equilibrar) y consultar posiciones altas.",
           {"tle": "Tu solución es lineal por operación: o el árbol no se equilibra (insertar en orden lo convierte en una lista) o kesimo recorre los elementos en inorden. Cada operación debe costar O(log N).",
            "rte": "Recursión muy profunda: ¿el árbol se está quedando como una lista? Revisa las rotaciones.",
            "mle": "Gastas demasiada memoria: no copies el conjunto ni guardes vectores por consulta."},
           ["Con 100.000 consultas, recorrer en inorden hasta la posición k cuesta demasiado.",
            "kesimo debe bajar un solo camino desde la raíz usando tami: O(altura) = O(log N).",
            "Comprueba que insert reequilibra (rotaciones) para que la altura sea logarítmica."])
    prueba("300.000 valores al azar", "rendimiento",
           [caso_azar(rng, 300000, VMAX, 20000)],
           "El tamaño máximo del enunciado (N = 300.000) con valores repetidos al azar.",
           {"tle": "Insertar 300.000 valores tiene que costar O(N log N): revisa que la inserción no recorre el árbol entero ni copia nada.",
            "mle": "Demasiada memoria para 300.000 nodos: no guardes copias del árbol.",
            "rte": "Con 300.000 valores se rompe: revisa la memoria dinámica y los punteros."},
           ["Lee con cin >> sin hacer nada costoso por valor.",
            "Cada insert es O(log N) si el árbol está equilibrado."])

    def texto_entrada(casos):
        return "".join(f"{len(v)}\n{' '.join(map(str, v))}\n{len(c)}\n{' '.join(map(str, c))}\n"
                       for v, c in casos) + "0\n"

    return [Prueba(nombre, tipo, entrada=texto_entrada(casos),
                   salida="".join("\n".join(resuelve(v, c)) + "\n---\n" for v, c in casos),
                   casos=len(casos), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, casos, comprueba, si, pistas in P]


# ---------------------------------------------------------------- variantes
# Muchos fallos típicos están en la clase (tami en inserta, en las rotaciones, en kesimo). Como la
# solución de referencia lleva la cabecera incrustada, la variante cambia directamente ese texto.
_H = (pathlib.Path(__file__).resolve().parents[2] / "1-Arboles AVL" / "EJ_01-2" / "TreeSet_AVL_plantilla.h"
      ).read_bytes().decode("latin-1")


def con_h(*cambios):
    for a, _ in cambios:
        assert _H.count(a) == 1, a
    return list(cambios)


_MULTI_A = _H[_H.index("        else if (menor(a->elem, e)) {\n            crece = inserta(e, a->dr);"):
              _H.index("crece = false;") + len("crece = false;")]
_MULTI_B = "        else {\n            crece = inserta(e, a->dr);\n            if (crece) reequilibraIzq(a);\n        }"

LINEAL = """auto it = arbol.begin();
            for (int j = 1; j < posValor && it != arbol.end(); ++j) ++it;
            if (it == arbol.end()) throw out_of_range("no existe");
            cout << *it << '\\n';"""

VARIANTES = [
    Variante("escribe ? en vez de ??", [("cout << \"??\\n\";", "cout << \"?\\n\";")], prueba=5, v="wa"),
    Variante("no escribe --- tras cada caso", [("cout << \"---\\n\";  // separador entre casos", "")], prueba=5, v="wa"),
    Variante("trata el 0 final como un caso", [("if (!cin || nValores == 0)", "if (!cin)")], prueba=5, v="wa"),
    Variante("posiciones desde 0", [("arbol.kesimo(posValor)", "arbol.kesimo(posValor - 1)")], prueba=6, v="wa"),
    Variante("el conjunto admite repetidos", con_h((_MULTI_A, _MULTI_B)), prueba=[5, 7], v="wa"),
    Variante("baja por la derecha sin restar tami",
             con_h(("else return kesimo(k - a->tami, a->dr);", "else return kesimo(k, a->dr);")), prueba=8, v="wa"),
    Variante("suma tami aunque el valor esté repetido",
             con_h(("            crece = inserta(e, a->iz);\n            if (crece) {\n                a->tami += 1;",
                     "            crece = inserta(e, a->iz);\n            a->tami += 1;\n            if (crece) {")), prueba=9, v="wa"),
    Variante("rotaDer no actualiza tami", con_h(("r2->tami -= r1->tami;", "")), prueba=10, v="wa"),
    Variante("rotaIzq no actualiza tami", con_h(("r2->tami += r1->tami;", "")), prueba=11, v="wa"),
    Variante("Set global que no se vacía entre casos", [("    Set<int> arbol;\n", "    static Set<int> arbol;\n")], prueba=14, v="wa"),
    Variante("no reequilibra (árbol de búsqueda simple)",
             con_h(("if (altura(a->dr) - altura(a->iz) > 1) {", "if (false) {"),
                    ("if (altura(a->iz) - altura(a->dr) > 1) {", "if (false) {")), prueba=17, v="tle"),
    Variante("k-ésimo recorriendo en inorden (lineal)",
             [("cout << arbol.kesimo(posValor) << '\\n';", LINEAL)], prueba=17, v="tle"),
]
