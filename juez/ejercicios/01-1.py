"""01-1 · ¿Es un árbol AVL? (enteros, en preorden con -1 = vacío): juez con pruebas pensadas para
cada error típico."""
import random
from _comun import Prueba, Variante

CONFIG = {
    "solucion": "1-Arboles AVL/EJ_01-1/EJ 01-1.cpp",
    "cabeceras": [],
    "limite_ms": 3000,
    "fallo": ["(abs(altIzq - altDer) <= 1)", "(abs(altIzq - altDer) < 1)"],
}


# ---------------------------------------------------------------- árboles
class Arbol:
    """Árbol binario en vectores: val[i], L[i], R[i] (-1 = vacío). Sin recursión para los grandes."""

    def __init__(self):
        self.val, self.L, self.R, self.raiz = [], [], [], -1

    def nodo(self, l, v, r):
        self.val.append(v); self.L.append(l); self.R.append(r)
        return len(self.val) - 1


def desde_parentesis(s):
    """«((. 1 .) 2 (. 3 .))» → Arbol (solo para los árboles pequeños escritos a mano)."""
    toks = s.replace("(", " ( ").replace(")", " ) ").split()
    a, pos = Arbol(), 0

    def rec():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == ".":
            return -1
        assert t == "("
        l = rec()
        v = int(toks[pos]); pos += 1
        r = rec()
        assert toks[pos] == ")"; pos += 1
        return a.nodo(l, v, r)

    a.raiz = rec()
    assert pos == len(toks)
    return a


def preorden(a):
    """Formato de la entrada: raíz, hijo izquierdo, hijo derecho; -1 = vacío."""
    out, pila = [], [a.raiz]
    while pila:
        x = pila.pop()
        if x == -1:
            out.append("-1")
        else:
            out.append(str(a.val[x]))
            pila.append(a.R[x]); pila.append(a.L[x])
    return " ".join(out)


def es_avl(a):
    """Solucionador independiente: de búsqueda si el inorden es estrictamente creciente, y
    equilibrado si en cada nodo las alturas de los hijos difieren como mucho en 1."""
    if a.raiz == -1:
        return True
    prev, pila, x = None, [], a.raiz
    while pila or x != -1:
        while x != -1:
            pila.append(x); x = a.L[x]
        x = pila.pop()
        if prev is not None and not (prev < a.val[x]):
            return False
        prev = a.val[x]; x = a.R[x]
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


# ---------------------------------------------------------------- generadores de formas
def forma_avl(a, h, rng, p_lleno=0.5, p_roto=0.0):
    """Forma AVL de altura h (a veces, con probabilidad p_roto, un nodo desequilibrado)."""
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
    """Árbol binario cualquiera de n nodos."""
    if n == 0:
        return -1
    k = rng.randrange(n)
    l = forma_azar(a, k, rng)
    r = forma_azar(a, n - 1 - k, rng)
    return a.nodo(l, 0, r)


def forma_fibonacci(a, h):
    """El AVL con menos nodos para su altura: sus hojas están a profundidades muy distintas."""
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


def numera(a, rng, inicio=1, salto=(1, 1)):
    """Pone valores crecientes en inorden (árbol de búsqueda) con saltos al azar."""
    v = inicio
    for x in inorden_nodos(a):
        a.val[x] = v
        v += rng.randint(*salto)
    return a


def lista_derecha(n, inicio=1):
    a = Arbol()
    sig = -1
    for v in range(inicio + n - 1, inicio - 1, -1):
        sig = a.nodo(-1, v, sig)
    a.raiz = sig
    return a


def perturba(a, rng):
    """Rompe (o no) el orden: intercambia dos valores o copia el de un vecino en inorden."""
    ino = inorden_nodos(a)
    if len(ino) < 2:
        return a
    t = rng.random()
    if t < 0.4:
        i, j = rng.sample(range(len(ino)), 2)
        a.val[ino[i]], a.val[ino[j]] = a.val[ino[j]], a.val[ino[i]]
    elif t < 0.8:
        i = rng.randrange(len(ino) - 1)
        if rng.random() < 0.5:
            a.val[ino[i]] = a.val[ino[i + 1]]
        else:
            a.val[ino[i + 1]] = a.val[ino[i]]
    else:
        x = rng.choice(ino)
        a.val[x] = rng.randint(0, 99)
    return a


def caso_pequeno(rng):
    a = Arbol()
    t = rng.random()
    if t < 0.4:
        a.raiz = forma_avl(a, rng.randint(0, 4), rng, 0.4, 0.15)
    else:
        a.raiz = forma_azar(a, rng.randint(0, 9), rng)
    numera(a, rng, rng.randint(0, 5), (1, 6))
    if rng.random() < 0.35:
        perturba(a, rng)
    return a


def caso_mediano(rng):
    a = Arbol()
    a.raiz = forma_avl(a, rng.randint(5, 7), rng, 0.4, rng.choice([0, 0, 0.02, 0.05]))
    numera(a, rng, rng.randint(1, 20), (1, 9))
    if rng.random() < 0.4:
        perturba(a, rng)
    return a


def avl_grande(rng, n):
    """AVL de n nodos obtenido insertando valores al azar (con rotaciones) en un AVL propio."""
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
    return numera(a, rng, rng.randint(1, 9), (1, 7))


def mas_hondo(a):
    """Nodo hoja a mayor profundidad."""
    mejor, prof_mejor, pila = a.raiz, 0, [(a.raiz, 0)]
    while pila:
        x, p = pila.pop()
        if a.L[x] == -1 and a.R[x] == -1 and p > prof_mejor:
            mejor, prof_mejor = x, p
        for h in (a.L[x], a.R[x]):
            if h != -1:
                pila.append((h, p + 1))
    return mejor


# ---------------------------------------------------------------- pruebas
def pruebas():
    rng = random.Random(1101)
    P = []
    A = desde_parentesis

    def prueba(nombre, tipo, arboles, comprueba, si, pistas):
        P.append((nombre, tipo, [x if isinstance(x, Arbol) else A(x) for x in arboles], comprueba, si, pistas))

    # --- enunciado
    prueba("Ejemplo del enunciado", "enunciado",
           ["((. 1 .) 2 (. 3 (. 4 .)))", "(. 1 ((. 2 .) 3 (. 4 .)))", "((. 1 .) 4 (. 3 (. 2 .)))"],
           "Los tres árboles del PDF: uno AVL, uno desequilibrado y uno que no es de búsqueda.",
           {"wa": "Si falla hasta el ejemplo, el fallo es de base: la lectura en preorden (raíz, izquierdo, derecho, con -1 como vacío), las dos condiciones del AVL o el formato SI/NO.",
            "pe": "Los SI/NO son correctos pero el formato no: escribe cada respuesta en su propia línea, sin espacios ni texto extra.",
            "rte": "El programa se rompe con el ejemplo: revisa la recursión de lectura (cada -1 es un árbol vacío y corta la recursión)."},
           ["Ejecuta el ejemplo en tu ordenador y compara línea a línea.",
            "Cada caso es una línea con el árbol en preorden: se lee la raíz y después, recursivamente, el hijo izquierdo y el derecho. Un -1 es un árbol vacío.",
            "Escribe exactamente «SI» o «NO» (sin tilde) seguido de un salto de línea por caso."])

    # --- bordes
    prueba("Árbol vacío", "borde", ["."],
           "Un caso que es solo «-1»: el árbol vacío es AVL (SI).",
           {"wa": "El árbol vacío es AVL: no tiene ningún nodo que incumpla nada. Tu programa responde NO o escribe algo raro.",
            "rte": "Con el árbol vacío tu programa accede a la raíz de un árbol que no existe."},
           ["¿Qué hace tu programa si lo primero que lee es -1?",
            "El caso base de la recursión (leer -1) debe devolver «es AVL» con altura 0."])
    prueba("Un solo nodo", "borde", ["(. 7 .)", "(. 123456 .)"],
           "Un árbol con solo la raíz («7 -1 -1»): es AVL.",
           {"wa": "Una hoja siempre es AVL. Si dices NO, falla el caso base o las comparaciones con los hijos vacíos (sus «mínimo» y «máximo» no deben estorbar).",
            "rte": "Con una hoja accedes a un hijo que no existe."},
           ["Sigue tu código a mano con «7 -1 -1»: ¿qué altura, mínimo y máximo devuelve cada hijo vacío?",
            "Un hijo vacío no debe impedir nada: su máximo tiene que ser menor que cualquier valor y su mínimo mayor que cualquier valor (o compruébalo aparte con «si hay hijo...»)."])
    prueba("Dos nodos", "borde", ["((. 3 .) 8 .)", "(. 3 (. 8 .))"],
           "Raíz con un solo hijo (izquierdo o derecho): alturas 1 y 0, sigue siendo AVL.",
           {"wa": "Con un solo hijo la diferencia de alturas es 1, que SÍ está permitida. Revisa si usas < 1 en vez de ≤ 1, o si no tratas bien el hijo vacío."},
           ["La condición es |altIzq − altDer| ≤ 1: una diferencia de 1 vale.",
            "Comprueba también que el hijo que falta no rompe la comparación de orden."])
    prueba("Valor 0 en el árbol", "borde",
           ["(. 0 .)", "((. 0 .) 1 .)", "(. 0 (. 1 .))", "((. 0 .) 2 (. 3 .))"],
           "Los valores son enteros no negativos: el 0 es un valor válido.",
           {"wa": "Usas 0 (o algo parecido) como «máximo» del árbol vacío: con un nodo que vale 0 sin hijo izquierdo, «0 < 0» es falso y respondes NO. El centinela tiene que ser menor que cualquier valor posible (por ejemplo INT_MIN o -1)."},
           ["Prueba «0 -1 -1» a mano: debe salir SI.",
            "¿Qué devuelve como máximo tu árbol vacío? Tiene que ser estrictamente menor que 0.",
            "Usa INT_MIN como máximo del vacío y INT_MAX como mínimo, o guarda un booleano «hay hijo» y no compares si no lo hay."])
    prueba("Valores grandes (hasta mil millones)", "borde",
           ["(. 1000000000 .)", "((. 1 .) 500000000 (. 1000000000 .))",
            "((. 999999998 .) 999999999 (. 1000000000 .))", "((. 1000000000 .) 999999999 .)"],
           "Valores muy grandes (caben en int): el «mínimo» del árbol vacío no puede ser un número pequeño.",
           {"wa": "Usas como mínimo del árbol vacío un número fijo (100000, 1000000...) y aquí hay valores mayores. Usa INT_MAX o compruébalo con un booleano «hay hijo».",
            "rte": "Algún cálculo con valores grandes se sale de rango: no hace falta sumar ni restar valores, solo compararlos."},
           ["Prueba «1000000000 -1 -1» a mano.",
            "El mínimo del árbol vacío debe ser mayor que cualquier valor posible: INT_MAX (de <climits>)."])

    # --- trampas
    prueba("Lista hacia la derecha", "trampa", ["(. 1 (. 2 (. 3 .)))"],
           "Tres nodos en fila hacia la derecha («1 -1 2 -1 3 -1 -1»): es de búsqueda pero NO es AVL (alturas 0 y 2 en la raíz).",
           {"wa": "Comparas las alturas sin valor absoluto: «altIzq − altDer ≤ 1» da −2 ≤ 1, que es cierto, y dejas pasar los árboles cargados a la derecha. O solo compruebas el orden y no el equilibrio."},
           ["La raíz tiene alturas 0 (izquierda) y 2 (derecha).",
            "¿Qué pasa con tu comparación si altIzq − altDer es negativo?",
            "La condición es abs(altIzq − altDer) ≤ 1, en cada nodo."])
    prueba("Lista hacia la izquierda y en zigzag", "trampa",
           ["(((. 1 .) 2 .) 3 .)", "((. 1 (. 2 .)) 3 .)", "(. 1 ((. 2 .) 3 .))"],
           "Otras listas de tres nodos: hacia la izquierda y en zigzag. Ninguna es AVL.",
           {"wa": "Solo compruebas el orden, o la diferencia de alturas solo en un sentido. Las listas en zigzag también tienen alturas 2 y 0 en la raíz."},
           ["Calcula a mano las alturas de los dos hijos de la raíz en cada árbol.",
            "Usa abs(altIzq − altDer) ≤ 1 y que la altura sea 1 + max(altIzq, altDer)."])
    prueba("Diferencia de alturas exactamente 1", "trampa", ["(((. 1 .) 2 .) 3 (. 4 .))"],
           "La raíz tiene alturas 2 y 1 (diferencia justo 1): SÍ es AVL.",
           {"wa": "Te equivocas en el límite: una diferencia de alturas de 1 está permitida. Revisa si usas < 1 en vez de ≤ 1 (o «≥ 1» en vez de «> 1» para decir que no lo es)."},
           ["«3 2 1 -1 -1 -1 4 -1 -1» es AVL: diferencia 1 en la raíz y en el nodo 2.",
            "La condición es |altIzq − altDer| ≤ 1 (menor o IGUAL)."])
    prueba("Diferencia de alturas 2 sin ser una lista", "trampa",
           ["(((. 1 .) 2 (. 3 .)) 4 .)", "(. 1 ((. 2 .) 3 (. 4 .)))"],
           "Árboles con ramas cuya raíz tiene alturas 2 y 0: NO son AVL.",
           {"wa": "Con diferencia 2 debe salir NO. Si dices SI, revisa el valor absoluto, el límite (≤ 1) y que la altura del vacío sea 0 (o −1 de forma coherente)."},
           ["El primer árbol: el hijo izquierdo tiene altura 2 y el derecho está vacío.",
            "Revisa cómo calculas la altura: vacío = 0, hoja = 1, nodo = 1 + max(hijos)."])
    prueba("Desequilibrio en un nodo interior", "trampa",
           ["((((. 1 .) 2 .) 3 .) 4 ((. 5 .) 6 (. 7 .)))"],
           "La raíz está equilibrada (alturas 3 y 2) pero el nodo 3 no (alturas 2 y 0): el árbol NO es AVL.",
           {"wa": "Solo miras el equilibrio de la raíz, o no combinas el resultado de los hijos: un nodo es AVL solo si sus DOS subárboles también lo son."},
           ["El nodo 3 tiene alturas 2 y 0.",
            "La condición AVL es para todo subárbol, no solo para la raíz.",
            "Devuelve «es AVL» = izqOK && derOK && equilibrado && ordenado."])
    prueba("Nieto que rompe el orden por la izquierda", "trampa", ["((. 5 (. 15 .)) 10 (. 20 .))"],
           "El 15 es mayor que su padre 5 (bien) pero está a la izquierda de la raíz 10 (mal): NO es de búsqueda.",
           {"wa": "Comparas cada nodo solo con sus hijos directos, o calculas mal el máximo del subárbol izquierdo. Todo el subárbol izquierdo tiene que ser menor que la raíz: compara con su MÁXIMO, que está en su rama derecha."},
           ["En «10 5 -1 15 -1 -1 20 -1 -1», ¿qué valores hay a la izquierda del 10?",
            "No basta hijo izquierdo < raíz < hijo derecho: hay que mirar todo el subárbol.",
            "Haz que la recursión devuelva también el mínimo y el máximo de cada subárbol, y comprueba maxIzq < raíz < minDer. Al volver: maximo = max(maxDer, valor)."])
    prueba("Nieto que rompe el orden por la derecha", "trampa", ["((. 5 .) 10 ((. 7 .) 20 .))"],
           "El 7 es menor que su padre 20 (bien) pero está a la derecha de la raíz 10 (mal): NO es de búsqueda.",
           {"wa": "Comparas solo con los hijos directos, o calculas mal el mínimo del subárbol derecho. El mínimo de un subárbol está en su rama IZQUIERDA (o es la raíz si no tiene)."},
           ["En «10 5 -1 -1 20 7 -1 -1 -1», ¿qué valores hay a la derecha del 10?",
            "Comprueba raíz < mínimo de todo el subárbol derecho.",
            "Al volver de la recursión: minimo = min(minIzq, valor)."])
    prueba("Valor repetido en el subárbol izquierdo", "trampa", ["((. 3 (. 5 .)) 5 (. 8 .))"],
           "Un 5 a la izquierda de la raíz 5: el orden es ESTRICTO, así que NO es AVL.",
           {"wa": "Usas ≤ al comparar con el subárbol izquierdo. El enunciado pide que la raíz sea ESTRICTAMENTE mayor que todo su hijo izquierdo: maxIzq < valor."},
           ["En «5 3 -1 5 -1 -1 8 -1 -1» hay dos 5.",
            "Cambia el ≤ por < en la comparación con el máximo del izquierdo."])
    prueba("Valor repetido en el subárbol derecho", "trampa", ["((. 3 .) 5 ((. 5 .) 8 .))"],
           "Un 5 a la derecha de la raíz 5: tampoco vale, NO es AVL.",
           {"wa": "Usas ≤ al comparar con el subárbol derecho. La raíz tiene que ser ESTRICTAMENTE menor que todo su hijo derecho: valor < minDer."},
           ["En «5 3 -1 -1 8 5 -1 -1 -1» hay dos 5.",
            "Cambia el ≤ por < en la comparación con el mínimo del derecho."])
    prueba("Altura, no número de nodos", "trampa",
           ["((((. 1 .) 2 (. 3 .)) 4 ((. 5 .) 6 (. 7 .))) 8 (. 9 (. 10 .)))"],
           "Hijos con alturas 3 y 2 pero con 7 y 2 nodos: es AVL. Lo que se compara son ALTURAS.",
           {"wa": "Estás comparando el número de nodos de los hijos (o sumando las alturas) en lugar de sus alturas. La altura es 1 + el MÁXIMO de las de los hijos."},
           ["El hijo izquierdo tiene 7 nodos y altura 3; el derecho, 2 nodos y altura 2.",
            "altura = 1 + max(altIzq, altDer), no altIzq + altDer + 1."])
    fib = []
    for h in (5, 6):
        a = Arbol(); a.raiz = forma_fibonacci(a, h); fib.append(numera(a, rng, 1, (1, 1)))
    prueba("Hojas a profundidades muy distintas", "trampa", fib,
           "Árboles de Fibonacci (los AVL más desequilibrados posibles): hay hojas a profundidad 2 y a profundidad 5, y son AVL.",
           {"wa": "Usas un criterio global (por ejemplo, que todas las hojas estén a profundidades que difieren en 1, o comparar la rama más corta con la más larga). La condición AVL es LOCAL: en cada nodo, la altura de sus dos hijos."},
           ["Dibuja el primer árbol: la rama más corta tiene 3 nodos y la más larga 5, pero cada nodo está equilibrado.",
            "No compares profundidades de hojas: compara, en cada nodo, la altura de su hijo izquierdo con la de su derecho."])
    prueba("Un NO pronto no te ahorra leer el árbol", "trampa",
           ["((((. 10 .) 20 .) 30 .) 100 (((. 101 .) 102 (. 103 .)) 104 ((. 105 .) 106 (. 107 .))))",
            "(. 1 (. 2 (. 3 .)))", "(((. 1 .) 2 .) 3 .)"],
           "En el primer árbol el fallo está en el hijo izquierdo; aun así hay que leer el derecho entero para que el siguiente caso empiece donde debe.",
           {"wa": "En cuanto sabes que el izquierdo no es AVL dejas de leer (return temprano o «izqOK && leer(...)»). El resto del árbol se queda en la entrada y se lee como si fuera el caso siguiente.",
            "rte": "Te has desincronizado con la entrada: lo que queda del árbol anterior se lee como otro caso."},
           ["El primer caso es NO, pero ¿qué lee tu programa como segundo caso?",
            "Cuidado con el cortocircuito de && : «izqOK && leerAVL(...)» no llega a leer el derecho si izqOK es falso.",
            "Lee SIEMPRE los dos hijos (dos llamadas guardadas en variables) y combina los resultados después."])
    grande = Arbol()
    li = forma_avl(grande, 7, rng, 1.0)
    ld = forma_avl(grande, 5, rng, 1.0)
    grande.raiz = grande.nodo(li, 0, ld)
    numera(grande, rng, 1000, (20, 40))
    prueba("Varios casos seguidos", "trampa",
           [grande, "(. 1 .)", "((. 1 .) 2 (. 3 .))", "((. 2 .) 5 .)", ".", "(. 4 (. 9 .))"],
           "Un árbol grande que no es AVL seguido de varios pequeños que sí lo son: nada del caso anterior debe quedar.",
           {"wa": "Algo se arrastra de un caso al siguiente: un booleano «esAVL» global que no vuelves a poner a true, el «último valor» del inorden o un vector de nodos que no se vacía."},
           ["Si el primer caso sale bien y los siguientes no, mira qué variables viven fuera de la función de cada caso.",
            "Declara (o reinicia) todo lo que uses dentro de resuelveCaso, o mejor, que la recursión devuelva sus resultados en vez de usar variables globales."])

    # --- aleatorios
    prueba("Aleatorios pequeños", "aleatorio", [caso_pequeno(rng) for _ in range(300)],
           "300 árboles pequeños al azar (AVL, casi AVL y árboles cualesquiera).",
           {"wa": "Hay algún caso concreto que no tratas: la línea que falla es el número de caso; busca ese árbol en la entrada y dibújalo."},
           ["Cuenta la línea que falla: es el número de caso. Copia ese árbol y pruébalo solo.",
            "Dibuja el árbol y calcula a mano, de abajo arriba, altura, mínimo y máximo de cada nodo."])
    prueba("Aleatorios medianos", "aleatorio", [caso_mediano(rng) for _ in range(60)],
           "60 árboles de 20 a 120 nodos, casi todos AVL con algún fallo escondido.",
           {"wa": "Algún fallo escondido en lo hondo del árbol (un valor repetido, dos valores cambiados o un nodo desequilibrado) se te escapa.",
            "rte": "Con árboles algo más grandes se rompe: revisa la recursión."},
           ["Busca el caso que falla y localiza el nodo donde está el problema.",
            "Las tres comprobaciones deben hacerse en TODOS los nodos: hijos AVL, |altIzq − altDer| ≤ 1 y maxIzq < valor < minDer."])

    # --- rendimiento
    big = avl_grande(rng, 110000)
    prueba("AVL grande (más de 100.000 nodos)", "rendimiento", [big],
           "Un árbol AVL enorme: hay que recorrerlo una sola vez.",
           {"tle": "Tu solución no es lineal: recalculas alturas, mínimos o máximos recorriendo subárboles una y otra vez. Haz que cada llamada devuelva todo lo necesario.",
            "mle": "Gastas demasiada memoria: no hace falta guardar el árbol (se puede comprobar mientras se lee) y nunca copies estructuras en cada llamada.",
            "wa": "Con un árbol grande la respuesta cambia: ¿usas algún tipo pequeño (short, char) o un tamaño fijo de array?"},
           ["Una sola recursión en postorden que devuelva (es AVL, altura, mínimo, máximo) basta: O(n).",
            "No llames a una función «altura» aparte desde cada nodo."])
    hondos = []
    for tipo in ("orden", "equilibrio", "bien"):
        a = avl_grande(rng, 38000)
        x = mas_hondo(a)
        if tipo == "equilibrio":
            # cuelga una lista de dos nodos de la hoja más honda: ese subárbol ya no es AVL
            c2 = a.nodo(-1, 0, -1)
            c1 = a.nodo(-1, 0, c2)
            a.R[x] = c1
            numera(a, rng, 3, (1, 7))
        elif tipo == "orden":
            ino = inorden_nodos(a)
            i = ino.index(x)
            a.val[x] = a.val[ino[i + 1]] if i + 1 < len(ino) else a.val[ino[i - 1]]
        hondos.append(a)
    prueba("Grandes con un único fallo en lo más hondo", "rendimiento", hondos,
           "Tres árboles grandes: uno con un repetido en la hoja más honda, otro con un desequilibrio allí y otro AVL.",
           {"wa": "El fallo está en la hoja más profunda: revisa que comparas con el mínimo/máximo de TODO el subárbol y que miras el equilibrio en todos los nodos.",
            "tle": "Tu solución recorre los subárboles varias veces: debe ser O(n)."},
           ["Prueba con un árbol pequeño que tenga un valor repetido en una hoja profunda.",
            "Cada nodo se procesa una vez, al volver de las llamadas de sus dos hijos."])
    prueba("Lista degenerada de 120.000 nodos", "rendimiento", [lista_derecha(120000)],
           "Un árbol que es una lista hacia la derecha: recursión muy profunda y peor caso de las soluciones cuadráticas.",
           {"tle": "Tu solución es cuadrática en árboles profundos: en cada nodo vuelves a recorrer el subárbol entero (para la altura, el mínimo o el máximo). Calcula todo en un solo recorrido.",
            "rte": "La recursión es muy profunda (120.000 llamadas). El juez da pila de sobra; revisa que no declaras arrays grandes dentro de la función recursiva.",
            "mle": "Cada llamada recursiva gasta demasiada memoria: no copies vectores ni árboles al pasarlos como parámetro."},
           ["En una lista, la altura del subárbol de cada nodo es enorme: si la calculas aparte en cada nodo, el coste es n².",
            "Devuelve la altura (y el mínimo y el máximo) desde la propia recursión en lugar de recalcularla.",
            "Pasa por referencia lo que tenga que salir de la función (altura, mínimo, máximo) o devuelve un struct."])

    return [Prueba(nombre, tipo,
                   entrada=f"{len(arbs)}\n" + "".join(preorden(a) + "\n" for a in arbs),
                   salida="".join(("SI" if es_avl(a) else "NO") + "\n" for a in arbs),
                   casos=len(arbs), comprueba=comprueba, si=si, pistas=pistas)
            for nombre, tipo, arbs, comprueba, si, pistas in P]


# ---------------------------------------------------------------- variantes
CUADRATICA = r'''#include <vector>
struct NodoV { int v, iz, dr; };
vector<NodoV> nodosV;
int leeV() {
    int v; cin >> v;
    if (v == -1) return -1;
    int id = nodosV.size();
    nodosV.push_back({v, -1, -1});
    int a = leeV(); int b = leeV();
    nodosV[id].iz = a; nodosV[id].dr = b;
    return id;
}
int alturaV(int t) { return t == -1 ? 0 : 1 + max(alturaV(nodosV[t].iz), alturaV(nodosV[t].dr)); }
int maxV(int t) { return t == -1 ? INT_MIN : max(nodosV[t].v, max(maxV(nodosV[t].iz), maxV(nodosV[t].dr))); }
int minV(int t) { return t == -1 ? INT_MAX : min(nodosV[t].v, min(minV(nodosV[t].iz), minV(nodosV[t].dr))); }
bool avlV(int t) {
    if (t == -1) return true;
    bool a = avlV(nodosV[t].iz), b = avlV(nodosV[t].dr);
    int hi = alturaV(nodosV[t].iz), hd = alturaV(nodosV[t].dr);
    int mi = maxV(nodosV[t].iz), md = minV(nodosV[t].dr);
    return a && b && abs(hi - hd) <= 1 && mi < nodosV[t].v && nodosV[t].v < md;
}
void resuelveCaso() {
    nodosV.clear();
    int r = leeV();
    cout << (avlV(r) ? "SI" : "NO") << '\n';
}'''

VARIANTES = [
    Variante("diferencia de alturas con < en vez de ≤",
             [("(abs(altIzq - altDer) <= 1)", "(abs(altIzq - altDer) < 1)")], prueba=9, v="wa"),
    Variante("diferencia de alturas sin valor absoluto",
             [("(abs(altIzq - altDer) <= 1)", "(altIzq - altDer <= 1)")], prueba=7, v="wa"),
    Variante("no combina el resultado de los hijos",
             [("return izqOK && derOK && (abs", "return (abs")], prueba=11, v="wa"),
    Variante("compara solo con los hijos directos",
             [("minimo = min(minIzq, valor);", "minimo = valor;"),
              ("maximo = max(maxDer, valor);", "maximo = valor;")], prueba=[12, 13], v="wa"),
    Variante("≤ con el subárbol izquierdo (admite repetidos)",
             [("(maxIzq < valor)", "(maxIzq <= valor)")], prueba=14, v="wa"),
    Variante("≤ con el subárbol derecho (admite repetidos)",
             [("(valor < minDer)", "(valor <= minDer)")], prueba=15, v="wa"),
    Variante("centinela 0 como máximo del vacío",
             [("maximo = INT_MIN;", "maximo = 0;")], prueba=5, v="wa"),
    Variante("cuenta nodos en vez de altura",
             [("altura = max(altIzq, altDer) + 1;", "altura = altIzq + altDer + 1;")], prueba=16, v="wa"),
    Variante("deja de leer el derecho si el izquierdo ya falla",
             [("bool derOK = leerAVL(altDer, minDer, maxDer);", "bool derOK = izqOK && leerAVL(altDer, minDer, maxDer);")],
             prueba=18, v="wa"),
    Variante("booleano global que no se reinicia",
             [("bool leerAVL(int& altura, int& min, int& max);", "bool leerAVL(int& altura, int& min, int& max);\nbool todoOK = true;"),
              ("return izqOK && derOK && (abs(altIzq - altDer) <= 1) && (maxIzq < valor) && (valor < minDer);",
               "if (!(izqOK && derOK && (abs(altIzq - altDer) <= 1) && (maxIzq < valor) && (valor < minDer))) todoOK = false;\n\treturn todoOK;")],
             prueba=19, v="wa"),
    Variante("alturas y extremos recalculados en cada nodo (cuadrático)",
             [("void resuelveCaso() {\n    int altura = 0, minimo = 0, maximo = 0;\n    cout << (leerAVL(altura, minimo, maximo) ? \"SI\" : \"NO\") << '\\n';\n}", CUADRATICA)],
             prueba=24, v="tle"),
    Variante("todas las respuestas en una línea",
             [("cout << (leerAVL(altura, minimo, maximo) ? \"SI\" : \"NO\") << '\\n';", "cout << (leerAVL(altura, minimo, maximo) ? \"SI\" : \"NO\") << ' ';")],
             prueba=1, v="pe"),
]
