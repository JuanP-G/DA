"""01-1-2 · ¿Es un árbol AVL? (genérico: enteros «N» o palabras «P», árbol con paréntesis y «.» =
vacío, hasta fin de fichero): juez con pruebas pensadas para cada error típico."""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "1-Arboles AVL/EJ_01-1 (generico)/EJ 01-1 (GENERICO BIEN).cpp",
    "cabeceras": ["1-Arboles AVL/EJ_01-1 (generico)/bintree.h"],
    "limite_ms": 3000,
    "fallo": ["&& (!hayDer || elem < der.minimo);", "&& (!hayDer || !(der.minimo < elem));"],
}


# ---------------------------------------------------------------- árboles
class Arbol:
    """Árbol binario en vectores: val[i], L[i], R[i] (-1 = vacío). Sin recursión para los grandes."""

    def __init__(self):
        self.val, self.L, self.R, self.raiz = [], [], [], -1

    def nodo(self, l, v, r):
        self.val.append(v); self.L.append(l); self.R.append(r)
        return len(self.val) - 1


def desde_parentesis(s, tipo):
    """«((. 1 .) 2 (. 3 .))» → Arbol (solo para árboles pequeños escritos a mano)."""
    conv = int if tipo == "N" else str
    toks = s.replace("(", " ( ").replace(")", " ) ").split()
    a, pos = Arbol(), 0

    def rec():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == ".":
            return -1
        assert t == "("
        l = rec()
        v = conv(toks[pos]); pos += 1
        r = rec()
        assert toks[pos] == ")"; pos += 1
        return a.nodo(l, v, r)

    a.raiz = rec()
    assert pos == len(toks)
    return a


def parentesis(a):
    """Formato de la entrada: «.» o «(izq raíz der)», como lo escribe BinTree."""
    out, pila = [], [("t", a.raiz)]
    while pila:
        k, x = pila.pop()
        if k == "s":
            out.append(x)
        elif x == -1:
            out.append(".")
        else:
            out.append("(")
            pila += [("s", ")"), ("t", a.R[x]), ("s", " "), ("s", str(a.val[x])), ("s", " "), ("t", a.L[x])]
    return "".join(out)


def es_avl(a):
    """Solucionador independiente: de búsqueda si el inorden es estrictamente creciente (con el
    orden de int o de string según el tipo), y equilibrado si en cada nodo las alturas de los hijos
    difieren como mucho en 1."""
    if a.raiz == -1:
        return True
    prev, hay, pila, x = None, False, [], a.raiz
    while pila or x != -1:
        while x != -1:
            pila.append(x); x = a.L[x]
        x = pila.pop()
        if hay and not (prev < a.val[x]):
            return False
        prev, hay = a.val[x], True
        x = a.R[x]
    orden, pila = [], [a.raiz]
    while pila:
        x = pila.pop(); orden.append(x)
        for h in (a.L[x], a.R[x]):
            if h != -1:
                pila.append(h)
    alt = [0] * len(a.val)
    for x in reversed(orden):
        hi = alt[a.L[x]] if a.L[x] != -1 else 0
        hd = alt[a.R[x]] if a.R[x] != -1 else 0
        if abs(hi - hd) > 1:
            return False
        alt[x] = 1 + max(hi, hd)
    return True


# ---------------------------------------------------------------- generadores
def forma_avl(a, h, rng, p_lleno=0.5, p_roto=0.0):
    if h <= 0:
        return -1
    if h == 1:
        return a.nodo(-1, 0, -1)
    if rng.random() < p_roto and h >= 3:
        hi, hd = rng.choice([(h - 1, h - 3), (h - 3, h - 1)])
    elif rng.random() < p_lleno:
        hi, hd = h - 1, h - 1
    else:
        hi, hd = rng.choice([(h - 1, h - 2), (h - 2, h - 1)])
    l = forma_avl(a, hi, rng, p_lleno, p_roto)
    r = forma_avl(a, hd, rng, p_lleno, p_roto)
    return a.nodo(l, 0, r)


def forma_azar(a, n, rng):
    if n == 0:
        return -1
    k = rng.randrange(n)
    l = forma_azar(a, k, rng)
    r = forma_azar(a, n - 1 - k, rng)
    return a.nodo(l, 0, r)


def forma_fibonacci(a, h):
    if h <= 0:
        return -1
    if h == 1:
        return a.nodo(-1, 0, -1)
    l = forma_fibonacci(a, h - 1)
    r = forma_fibonacci(a, h - 2)
    return a.nodo(l, 0, r)


def inorden_nodos(a):
    res, pila, x = [], [], a.raiz
    while pila or x != -1:
        while x != -1:
            pila.append(x); x = a.L[x]
        x = pila.pop(); res.append(x); x = a.R[x]
    return res


def pon_valores(a, valores):
    """Pone los valores (ya ordenados) en inorden: queda un árbol de búsqueda."""
    ino = inorden_nodos(a)
    assert len(valores) == len(ino)
    for x, v in zip(ino, valores):
        a.val[x] = v
    return a


def enteros(rng, n, lo=-60, hi=60):
    return sorted(rng.sample(range(lo, hi), n))


def palabras(rng, n, letras="abcdez", largo=(1, 4)):
    vistas = set()
    while len(vistas) < n:
        vistas.add("".join(rng.choice(letras) for _ in range(rng.randint(*largo))))
    return sorted(vistas)


def perturba(a, rng):
    ino = inorden_nodos(a)
    if len(ino) < 2:
        return a
    t = rng.random()
    if t < 0.5:
        i, j = rng.sample(range(len(ino)), 2)
        a.val[ino[i]], a.val[ino[j]] = a.val[ino[j]], a.val[ino[i]]
    else:
        i = rng.randrange(len(ino) - 1)
        if rng.random() < 0.5:
            a.val[ino[i]] = a.val[ino[i + 1]]
        else:
            a.val[ino[i + 1]] = a.val[ino[i]]
    return a


def caso_pequeno(rng):
    a = Arbol()
    if rng.random() < 0.45:
        a.raiz = forma_avl(a, rng.randint(0, 4), rng, 0.4, 0.15)
    else:
        a.raiz = forma_azar(a, rng.randint(0, 9), rng)
    tipo = rng.choice("NP")
    n = len(a.val)
    pon_valores(a, enteros(rng, n) if tipo == "N" else palabras(rng, n))
    if rng.random() < 0.35:
        perturba(a, rng)
    return tipo, a


def lista_derecha(n):
    a = Arbol()
    sig = -1
    for v in range(n, 0, -1):
        sig = a.nodo(-1, v, sig)
    a.raiz = sig
    return a


def avl_grande(rng, n, valores):
    """AVL de n nodos obtenido insertando claves al azar (con rotaciones) en un AVL propio."""
    a = Arbol()
    alt = []

    def h(x):
        return alt[x] if x != -1 else 0

    def act(x):
        alt[x] = 1 + max(h(a.L[x]), h(a.R[x]))

    def rot_der(x):
        y = a.L[x]; a.L[x] = a.R[y]; a.R[y] = x; act(x); act(y); return y

    def rot_izq(x):
        y = a.R[x]; a.R[x] = a.L[y]; a.L[y] = x; act(x); act(y); return y

    def inserta(x, v):
        if x == -1:
            alt.append(1)
            return a.nodo(-1, v, -1)
        if v < a.val[x]:
            a.L[x] = inserta(a.L[x], v)
        else:
            a.R[x] = inserta(a.R[x], v)
        act(x)
        if h(a.L[x]) - h(a.R[x]) > 1:
            if h(a.R[a.L[x]]) > h(a.L[a.L[x]]):
                a.L[x] = rot_izq(a.L[x])
            return rot_der(x)
        if h(a.R[x]) - h(a.L[x]) > 1:
            if h(a.L[a.R[x]]) > h(a.R[a.R[x]]):
                a.R[x] = rot_der(a.R[x])
            return rot_izq(x)
        return x

    for v in rng.sample(range(10 * n), n):
        a.raiz = inserta(a.raiz, v)
    return pon_valores(a, valores)


# ---------------------------------------------------------------- pruebas
def pruebas():
    rng = random.Random(1112)
    P = []

    def prueba(nombre, tipo, casos, comprueba, si, pistas):
        cs = [(t, x if isinstance(x, Arbol) else desde_parentesis(x, t)) for t, x in casos]
        P.append((nombre, tipo, cs, comprueba, si, pistas))

    # --- enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           [("N", "((. 1 .) 2 (. 3 (. 4 .)))"), ("N", "(. 1 ((. 2 .) 3 (. 4 .)))"),
            ("P", "((. raton .) cabra (. perro (. gato .)))"), ("P", "((. dos .) tres (. uno .))"), ("N", ".")],
           "Los cinco casos del PDF: árboles de enteros y de palabras, y el árbol vacío.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura (letra y árbol con paréntesis), las dos condiciones del AVL o el formato SI/NO.",
            "pe": "Los SI/NO son correctos pero el formato no: escribe cada respuesta en su propia línea, sin espacios ni texto extra.",
            "rte": "El programa se rompe con el ejemplo: revisa la lectura del árbol (read_tree de bintree.h ya entiende este formato) y el final de la entrada."},
           ["Ejecuta el ejemplo en tu ordenador y compara línea a línea.",
            "Cada caso son dos líneas: la letra (N o P) y el árbol. No hay número de casos: se lee hasta que falle la lectura de la letra.",
            "Lee el árbol con read_tree<int> o read_tree<string> según la letra y escribe «SI» o «NO» (sin tilde) en una línea."])

    # --- bordes
    prueba("Árboles vacíos", "borde", [("N", "."), ("P", ".")],
           "El árbol vacío «.», de enteros y de palabras: es AVL (SI).",
           {"wa": "El árbol vacío es AVL: no tiene ningún nodo que incumpla nada.",
            "rte": "Con el árbol vacío accedes a la raíz (root()) de un árbol que no tiene."},
           ["¿Qué hace tu función si el árbol está vacío (empty())?",
            "El caso base debe devolver «es AVL» sin mirar root(), left() ni right()."])
    prueba("Un solo nodo", "borde", [("N", "(. 7 .)"), ("P", "(. hola .)")],
           "Un árbol con solo la raíz, de enteros y de palabras: es AVL.",
           {"wa": "Una hoja siempre es AVL. Si dices NO, los hijos vacíos estorban en las comparaciones de orden: no compares con el mínimo/máximo de un hijo que no existe.",
            "rte": "Con una hoja accedes a la raíz de un hijo vacío."},
           ["Sigue tu código a mano con «(. 7 .)».",
            "Guarda si cada hijo existe (por ejemplo, altura ≠ −1) y solo compara con él si existe."])
    prueba("Dos nodos", "borde", [("N", "((. 3 .) 8 .)"), ("P", "(. ana (. pepe .))")],
           "Raíz con un solo hijo (izquierdo o derecho): alturas 1 y 0, sigue siendo AVL.",
           {"wa": "Con un solo hijo la diferencia de alturas es 1, que SÍ está permitida, y el hijo vacío no debe estorbar al comparar."},
           ["La condición es |altIzq − altDer| ≤ 1: una diferencia de 1 vale.",
            "Comprueba también que el hijo que falta no rompe la comparación de orden."])

    # --- trampas
    prueba("Los enteros se comparan como números", "trampa", [("N", "((. 9 .) 10 (. 100 .))")],
           "Con N, 9 < 10 < 100 aunque como texto «9» > «10»: es AVL.",
           {"wa": "Estás leyendo los árboles N como palabras (string): como texto «9» va después de «10». Con N hay que usar int.",
            "rte": "Algo falla al leer los enteros: con N el árbol es de int."},
           ["Compara «9» y «10» como texto y como números: ¿dan lo mismo?",
            "Según la letra, llama a read_tree<int> (N) o a read_tree<string> (P)."])
    prueba("Las palabras se comparan como texto", "trampa", [("P", "((. 10 .) 9 (. 90 .))")],
           "Con P los valores son palabras: «10» < «9» < «90» en orden alfabético, así que es AVL.",
           {"wa": "Estás leyendo los árboles P como enteros. Con P los valores son cadenas y se comparan alfabéticamente: «10» < «9».",
            "rte": "Lees las palabras como números y la lectura falla al encontrar letras."},
           ["Una palabra puede estar formada por dígitos, pero sigue siendo una palabra.",
            "Con la letra P usa string (read_tree<string>), aunque el valor parezca un número."])
    prueba("Números negativos y cero", "trampa", [("N", "((. -7 .) -3 (. 0 .))")],
           "Los enteros pueden ser negativos o cero: (-7) -3 (0) es AVL.",
           {"wa": "El valor por defecto de un hijo vacío (T() = 0, o un centinela como -1) se cuela en las comparaciones: «0 < -7» es falso. No compares con el máximo/mínimo de un hijo vacío."},
           ["Sigue tu código con la hoja -7: ¿con qué la comparas si no tiene hijos?",
            "Ningún número sirve como centinela si los enteros pueden ser cualquiera: usa un booleano «hay hijo izquierdo/derecho»."])
    prueba("Extremos de int", "trampa", [("N", "((. -2147483648 .) 0 (. 2147483647 .))")],
           "Valores INT_MIN y INT_MAX en el árbol: es AVL.",
           {"wa": "Usas INT_MIN / INT_MAX como mínimo y máximo del árbol vacío: con un nodo que vale INT_MAX sin hijo derecho, «INT_MAX < INT_MAX» es falso. Usa un booleano «hay hijo».",
            "rte": "Algún cálculo con los valores se desborda: no hace falta sumar ni restar valores, solo compararlos."},
           ["¿Qué devuelve tu árbol vacío como mínimo? ¿Puede coincidir con un valor real?",
            "Marca el vacío con altura −1 (o un booleano) y compara solo con hijos que existan."])
    prueba("Palabras que son prefijo de otras", "trampa",
           [("P", "((. ga .) gato (. gatos .))"), ("P", "(. gatos (. gato .))")],
           "«ga» < «gato» < «gatos»: el orden alfabético de string. El segundo árbol no es de búsqueda.",
           {"wa": "Comparas las palabras de forma distinta al orden de string (por longitud, solo la primera letra...). Usa el operador < de string."},
           ["Un prefijo va siempre antes: «gato» < «gatos».",
            "No inventes tu propio orden: el < de std::string es el alfabético que pide el enunciado."])
    prueba("Lista hacia la derecha", "trampa", [("N", "(. 1 (. 2 (. 3 .)))")],
           "Tres nodos en fila hacia la derecha: es de búsqueda pero NO es AVL (alturas 0 y 2 en la raíz).",
           {"wa": "Comparas las alturas sin valor absoluto: «altIzq − altDer ≤ 1» da −2 ≤ 1 y deja pasar los árboles cargados a la derecha. O solo compruebas el orden."},
           ["La raíz tiene alturas 0 (izquierda) y 2 (derecha).",
            "¿Qué pasa con tu comparación si altIzq − altDer es negativo?",
            "La condición es abs(altIzq − altDer) ≤ 1, en cada nodo."])
    prueba("Lista hacia la izquierda y en zigzag", "trampa",
           [("N", "(((. 1 .) 2 .) 3 .)"), ("P", "((. a (. b .)) c .)"), ("P", "(. a ((. b .) c .))")],
           "Otras listas de tres nodos: hacia la izquierda y en zigzag. Ninguna es AVL.",
           {"wa": "Solo compruebas el orden, o la diferencia de alturas solo en un sentido."},
           ["Calcula a mano las alturas de los dos hijos de la raíz en cada árbol.",
            "Usa abs(altIzq − altDer) ≤ 1 y que la altura sea 1 + max(altIzq, altDer)."])
    prueba("Diferencia de alturas exactamente 1", "trampa", [("P", "(((. a .) b .) c (. d .))")],
           "La raíz tiene alturas 2 y 1 (diferencia justo 1): SÍ es AVL.",
           {"wa": "Te equivocas en el límite: una diferencia de alturas de 1 está permitida. Revisa si usas < 1 en vez de ≤ 1."},
           ["La raíz y el nodo «b» tienen diferencia 1: el árbol es AVL.",
            "La condición es |altIzq − altDer| ≤ 1 (menor o IGUAL)."])
    prueba("Diferencia de alturas 2 sin ser una lista", "trampa",
           [("N", "(((. 1 .) 2 (. 3 .)) 4 .)"), ("P", "(. a ((. b .) c (. d .)))")],
           "Árboles con ramas cuya raíz tiene alturas 2 y 0: NO son AVL.",
           {"wa": "Con diferencia 2 debe salir NO. Revisa el valor absoluto, el límite (≤ 1) y que la altura del vacío sea coherente (−1 u 0)."},
           ["El primer árbol: el hijo izquierdo tiene altura 2 y el derecho está vacío.",
            "Revisa cómo calculas la altura: vacío = −1 (o 0), y cada nodo 1 + max(hijos)."])
    prueba("Desequilibrio en un nodo interior", "trampa", [("P", "((((. a .) b .) c .) d ((. e .) f (. g .)))")],
           "La raíz está equilibrada pero el nodo «c» no (alturas 2 y 0): el árbol NO es AVL.",
           {"wa": "Solo miras el equilibrio de la raíz, o no usas el resultado de los hijos: un nodo es AVL solo si sus DOS subárboles también lo son."},
           ["El nodo «c» tiene un hijo izquierdo de altura 2 y ninguno derecho.",
            "La condición AVL es para todo subárbol, no solo para la raíz.",
            "esAVL = izq.esAVL && der.esAVL && equilibrado && ordenado."])
    prueba("Nieto que rompe el orden por la izquierda", "trampa", [("P", "((. b (. z .)) m (. x .))")],
           "«z» es mayor que su padre «b» (bien) pero está a la izquierda de la raíz «m» (mal): NO es de búsqueda.",
           {"wa": "Comparas cada nodo solo con sus hijos directos, o calculas mal el máximo del subárbol izquierdo. Todo el subárbol izquierdo tiene que ser menor que la raíz: compara con su MÁXIMO."},
           ["¿Qué palabras hay a la izquierda de «m»?",
            "No basta hijo izquierdo < raíz < hijo derecho: hay que mirar todo el subárbol.",
            "Devuelve el mínimo y el máximo de cada subárbol: el máximo es el del hijo DERECHO si existe, si no la raíz."])
    prueba("Nieto que rompe el orden por la derecha", "trampa", [("N", "((. 5 .) 10 ((. 7 .) 20 .))")],
           "El 7 es menor que su padre 20 (bien) pero está a la derecha de la raíz 10 (mal): NO es de búsqueda.",
           {"wa": "Comparas solo con los hijos directos, o calculas mal el mínimo del subárbol derecho: es el del hijo IZQUIERDO si existe, si no la raíz."},
           ["¿Qué valores hay a la derecha del 10?",
            "Comprueba raíz < mínimo de todo el subárbol derecho."])
    prueba("Valor repetido en el subárbol izquierdo", "trampa", [("P", "((. ana (. luis .)) luis (. pepe .))")],
           "«luis» aparece dos veces, una a la izquierda de la raíz «luis»: el orden es ESTRICTO, NO es AVL.",
           {"wa": "Usas ≤ (o !(raíz < máximo)) al comparar con el subárbol izquierdo. La raíz debe ser ESTRICTAMENTE mayor que todo su hijo izquierdo: izq.maximo < raíz."},
           ["Hay dos «luis» en el árbol.",
            "La comparación con el izquierdo debe ser estricta: izq.maximo < elem."])
    prueba("Valor repetido en el subárbol derecho", "trampa", [("N", "((. 3 .) 5 ((. 5 .) 8 .))")],
           "Un 5 a la derecha de la raíz 5: tampoco vale, NO es AVL.",
           {"wa": "Usas ≤ al comparar con el subárbol derecho. La raíz debe ser ESTRICTAMENTE menor que todo su hijo derecho: elem < der.minimo."},
           ["Hay dos 5 en el árbol.",
            "La comparación con el derecho debe ser estricta: elem < der.minimo."])
    prueba("Altura, no número de nodos", "trampa",
           [("N", "((((. 1 .) 2 (. 3 .)) 4 ((. 5 .) 6 (. 7 .))) 8 (. 9 (. 10 .)))")],
           "Hijos con alturas 3 y 2 pero con 7 y 2 nodos: es AVL. Lo que se compara son ALTURAS.",
           {"wa": "Estás comparando el número de nodos de los hijos (o sumando alturas) en lugar de sus alturas. La altura es 1 + el MÁXIMO de las de los hijos."},
           ["El hijo izquierdo tiene 7 nodos y altura 3; el derecho, 2 nodos y altura 2.",
            "altura = 1 + max(izq.altura, der.altura)."])
    fib = []
    for t, h in (("N", 5), ("P", 6)):
        a = Arbol(); a.raiz = forma_fibonacci(a, h)
        n = len(a.val)
        fib.append((t, pon_valores(a, list(range(1, n + 1)) if t == "N" else palabras(rng, n, "abcdefghij", (2, 4)))))
    prueba("Hojas a profundidades muy distintas", "trampa", fib,
           "Árboles de Fibonacci (los AVL más desequilibrados posibles): hay hojas a profundidades muy distintas y son AVL.",
           {"wa": "Usas un criterio global (comparar la rama más corta con la más larga, o la profundidad de las hojas). La condición AVL es LOCAL: en cada nodo, la altura de sus dos hijos."},
           ["Dibuja el primer árbol: la rama más corta y la más larga difieren en más de 1, pero cada nodo está equilibrado.",
            "Compara, en cada nodo, la altura de su hijo izquierdo con la de su derecho."])
    grande = Arbol()
    li = forma_avl(grande, 7, rng, 1.0)
    ld = forma_avl(grande, 5, rng, 1.0)
    grande.raiz = grande.nodo(li, 0, ld)
    pon_valores(grande, list(range(1000, 1000 + 7 * len(grande.val), 7)))
    prueba("Varios casos seguidos", "trampa",
           [("N", grande), ("P", "(. hola .)"), ("N", "((. 1 .) 2 (. 3 .))"), ("P", "((. b .) c .)"),
            ("N", "."), ("N", "(. 4 (. 9 .))")],
           "Un árbol grande que no es AVL seguido de varios pequeños (de los dos tipos) que sí lo son: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: un booleano global que no vuelves a poner a true, el «último valor» del inorden, o la letra del caso anterior.",
            "rte": "Lo que queda de un caso estropea la lectura del siguiente."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de la función de cada caso.",
            "Que la recursión devuelva sus resultados (un struct) en vez de usar variables globales."])

    # --- aleatorios
    prueba("Aleatorios pequeños", "aleatorio", [caso_pequeno(rng) for _ in range(300)],
           "300 árboles pequeños al azar, de enteros (con negativos) y de palabras.",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; busca ese árbol en la entrada y dibújalo.",
            "rte": "Algún árbol rompe tu programa: busca el caso por el número de línea."},
           ["Cuenta la línea que falla: es el número de caso. Copia ese caso y pruébalo solo.",
            "Dibuja el árbol y calcula, de abajo arriba, altura, mínimo y máximo de cada nodo."])

    # --- rendimiento
    n1 = 110000
    v1, x = [], -500000
    for _ in range(n1):
        v1.append(x); x += rng.randint(1, 9)
    prueba("AVL grande de enteros (110.000 nodos)", "rendimiento", [("N", avl_grande(rng, n1, v1))],
           "Un árbol AVL enorme de enteros: hay que recorrerlo una sola vez.",
           {"tle": "Tu solución no es lineal: recalculas alturas, mínimos o máximos recorriendo subárboles una y otra vez. Haz que cada llamada devuelva todo lo necesario.",
            "mle": "Gastas demasiada memoria: no copies el árbol ni vectores en cada llamada.",
            "rte": "Con un árbol grande se rompe: revisa la recursión."},
           ["Una sola recursión en postorden que devuelva (es AVL, altura, mínimo, máximo) basta: O(n).",
            "No llames a una función «altura» aparte desde cada nodo."])
    n2 = 90000
    prueba("AVL grande de palabras (90.000 nodos)", "rendimiento",
           [("P", avl_grande(rng, n2, palabras(rng, n2, "abcdefghijklmnopqrstuvwxyz", (5, 8))))],
           "Un árbol AVL enorme de palabras.",
           {"tle": "Con palabras cada comparación cuesta más: no compares ni copies strings de más (pásalos por referencia constante) y recorre el árbol una sola vez.",
            "mle": "Copias demasiadas cadenas: devuelve o pasa los strings por referencia."},
           ["Pasa los árboles y los strings por const&.",
            "Un único recorrido en postorden: O(n) comparaciones."])
    prueba("Lista degenerada de 100.000 nodos", "rendimiento", [("N", lista_derecha(100000))],
           "Un árbol que es una lista hacia la derecha: recursión muy profunda y peor caso de las soluciones cuadráticas.",
           {"tle": "Tu solución es cuadrática en árboles profundos: en cada nodo vuelves a recorrer el subárbol entero (para la altura, el mínimo o el máximo). Calcula todo en un solo recorrido.",
            "rte": "La recursión es muy profunda (100.000 llamadas). El juez da pila de sobra; revisa que no declaras arrays grandes en la función recursiva.",
            "mle": "Cada llamada recursiva gasta demasiada memoria: no copies estructuras al pasarlas como parámetro."},
           ["En una lista, si calculas la altura aparte en cada nodo el coste es n².",
            "Devuelve la altura (y el mínimo y el máximo) desde la propia recursión en lugar de recalcularla."])

    return [Prueba(nombre, tipo,
                   entrada="".join(f"{t}\n{parentesis(a)}\n" for t, a in cs),
                   salida="".join(("SI" if es_avl(a) else "NO") + "\n" for t, a in cs),
                   casos=len(cs), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, cs, comprueba, si, pistas in P]


# ---------------------------------------------------------------- variantes
LENTA = """template <class T>
int alturaLenta(const BinTree<T>& a) {
    return a.empty() ? -1 : 1 + max(alturaLenta(a.left()), alturaLenta(a.right()));
}

template <class T>
Info<T> analizar(const BinTree<T>& arbol) {"""

VARIANTES = [
    Variante("diferencia de alturas con < en vez de ≤",
             [("abs(izq.altura - der.altura) <= 1", "abs(izq.altura - der.altura) < 1")], prueba=12, v="wa"),
    Variante("diferencia de alturas sin valor absoluto",
             [("abs(izq.altura - der.altura) <= 1", "izq.altura - der.altura <= 1")], prueba=10, v="wa"),
    Variante("no usa el resultado de los hijos",
             [("actual.esAVL = izq.esAVL && der.esAVL", "actual.esAVL = true")], prueba=14, v="wa"),
    Variante("compara solo con los hijos directos",
             [("actual.minimo = hayIzq ? izq.minimo : elem;", "actual.minimo = elem;"),
              ("actual.maximo = hayDer ? der.maximo : elem;", "actual.maximo = elem;")], prueba=[15, 16], v="wa"),
    Variante("≤ con el subárbol izquierdo",
             [("(!hayIzq || izq.maximo < elem)", "(!hayIzq || !(elem < izq.maximo))")], prueba=17, v="wa"),
    Variante("≤ con el subárbol derecho",
             [("(!hayDer || elem < der.minimo)", "(!hayDer || !(der.minimo < elem))")], prueba=18, v="wa"),
    Variante("lee los enteros como palabras",
             [("if (tipo == 'N') resuelveArbol<int>();", "if (tipo == 'N') resuelveArbol<string>();")], prueba=5, v="wa"),
    Variante("lee las palabras como enteros",
             [("else resuelveArbol<string>();", "else resuelveArbol<int>();")], prueba=6, v="wa"),
    Variante("compara con el hijo izquierdo vacío (T() = 0)",
             [("(!hayIzq || izq.maximo < elem)", "(izq.maximo < elem)")], prueba=7, v="wa"),
    Variante("cuenta nodos en vez de altura",
             [("actual.altura = 1 + max(izq.altura, der.altura);", "actual.altura = izq.altura + der.altura + 2;")], prueba=19, v="wa"),
    Variante("altura recalculada en cada nodo (cuadrático)",
             [("template <class T>\nInfo<T> analizar(const BinTree<T>& arbol) {", LENTA),
              ("    Info<T> actual;\n", "    int hiL = alturaLenta(arbol.left()), hdL = alturaLenta(arbol.right());\n    Info<T> actual;\n"),
              ("abs(izq.altura - der.altura) <= 1", "abs(hiL - hdL) <= 1")], prueba=25, v="tle"),
    Variante("todas las respuestas en una línea",
             [("cout << (analizar(arbol).esAVL ? \"SI\" : \"NO\") << '\\n';", "cout << (analizar(arbol).esAVL ? \"SI\" : \"NO\") << ' ';")],
             prueba=1, v="pe"),
]
