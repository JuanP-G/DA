"""Vídeo de teoría · Tema 1 · Árboles AVL (animado)."""
from vidlib import C, W, H, font
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

TEMA = "Tema 1 · Árboles AVL"


def nodo(f, x, y, s, u=1.0, c=None, r=30, alt=None, marca=False):
    if u <= 0:
        return
    c = c or C["blue"]
    if marca:
        f.d.ellipse((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=mix(C["bot"], C["gold"], u), width=4)
    f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
    f.d.text((x, y), str(s), font=font(22, True), fill=mix(C["bot"], C["text"], u), anchor="mm")
    if alt is not None:
        f.d.text((x + r + 6, y - r + 4), f"h{alt}", font=font(16, True), fill=mix(C["bot"], C["gold"], u), anchor="lm")


def arbol(f, pos, aristas, u=1.0, cols=None, alts=None, marca=None):
    for a, b in aristas:
        if a in pos and b in pos:
            f.d.line((pos[a], pos[b]), fill=mix(C["bot"], C["border"], u), width=3)
    for k, (x, y) in pos.items():
        nodo(f, x, y, k, u, (cols or {}).get(k), alt=(alts or {}).get(k), marca=marca and k in marca)


def interp(pa, pb, u):
    u = ease(max(0.0, min(1.0, u)))
    return {k: (lerp(pa[k][0], pb[k][0], u), lerp(pa[k][1], pb[k][1], u)) for k in pb}


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.8)
        arbol(f, {2: (960, 260), 1: (880, 360), 3: (1040, 360)}, [(2, 1), (2, 3)], u)
    portada(f, "Teoría", "Árboles AVL", TEMA, dib)


ABB = {50: (640, 150), 30: (430, 260), 70: (850, 260), 20: (320, 370), 40: (540, 370), 60: (740, 370), 80: (960, 370)}
ABB_A = [(50, 30), (50, 70), (30, 20), (30, 40), (70, 60), (70, 80)]


def e_abb(f):
    arbol(f, ABB, ABB_A, aparece(f, f.c(0)))
    texto(f, (640, 60), "árbol binario de búsqueda: izquierda < raíz < derecha", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        # buscar 60: 50 → 70 → 60
        camino = [50, 70, 60]
        k = min(2, int((f.t - f.c(1)) / 0.9))
        for q in range(k + 1):
            x, y = ABB[camino[q]]
            nodo(f, x, y, camino[q], c=C["green"], marca=q == k)
        etiqueta(f, (640, 500), "buscar 60:  60 > 50 → derecha,  60 < 70 → izquierda,  ¡ahí está!", 24, "text", 1)
    if f.t >= f.c(2):
        etiqueta(f, (640, 570), "cada comparación baja un nivel: coste = altura del árbol", 24, "green", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 640), "inorden (izq, raíz, der) los da ordenados: 20 30 40 50 60 70 80", 22, "muted", aparece(f, f.c(3)))


def e_degenerado(f):
    texto(f, (640, 60), "insertar 1, 2, 3, 4, 5 en orden en un ABB normal", 26, "red", aparece(f, f.c(0)), anchor="mm")
    n = min(5, int((f.t - f.c(0)) / 0.7) + 1) if f.t >= f.c(0) else 0
    pos = {k: (360 + (k - 1) * 140, 130 + (k - 1) * 95) for k in range(1, n + 1)}
    arbol(f, pos, [(k, k + 1) for k in range(1, 5)])
    if f.t >= f.c(1):
        etiqueta(f, (400, 580), "es una lista: buscar cuesta O(n)", 26, "red", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (400, 650), "hace falta mantener el árbol EQUILIBRADO", 26, "gold", aparece(f, f.c(2)))


def e_avl(f):
    pos = {30: (640, 160), 20: (480, 280), 40: (800, 280), 10: (400, 400), 25: (560, 400), 50: (880, 400)}
    ar = [(30, 20), (30, 40), (20, 10), (20, 25), (40, 50)]
    alts = {30: 3, 20: 2, 40: 2, 10: 1, 25: 1, 50: 1} if f.t >= f.c(1) else None
    arbol(f, pos, ar, aparece(f, f.c(0)), alts=alts)
    texto(f, (640, 60), "AVL: en cada nodo, |altura izq − altura der| ≤ 1", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 520), "cada nodo guarda su altura (vacío = 0)", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 590), "así la altura es O(log n): buscar, insertar y borrar en O(log n)", 24, "green", aparece(f, f.c(2)))


# rotación simple a la derecha: 30 ← 20 ← 10   →   20 con 10 y 30
RD_A = {30: (640, 160), 20: (520, 280), 10: (400, 400)}
RD_B = {20: (640, 160), 10: (520, 280), 30: (760, 280)}
# rotación simple a la izquierda: 10 → 20 → 30
RI_A = {10: (640, 160), 20: (760, 280), 30: (880, 400)}
RI_B = {20: (640, 160), 10: (520, 280), 30: (760, 280)}


def e_simples(f):
    if f.t < f.c(2):
        u = f.lin(f.c(1), 1.5)
        pos = interp(RD_A, RD_B, u)
        ar = [(30, 20), (20, 10)] if u < 0.5 else [(20, 10), (20, 30)]
        arbol(f, pos, ar, cols={30: C["red"]} if u < 1 else {20: C["green"]})
        texto(f, (640, 60), "desequilibrio por la izquierda-izquierda  →  rotación a la DERECHA", 26, "gold", 1, anchor="mm")
        if u < 1:
            etiqueta(f, (640, 520), "en el 30: altura izq 2, der 0", 24, "red", 1)
        else:
            etiqueta(f, (640, 520), "el 20 sube, el 30 baja a su derecha", 24, "green", 1)
    else:
        u = f.lin(f.c(2) + 0.6, 1.5)
        pos = interp(RI_A, RI_B, u)
        ar = [(10, 20), (20, 30)] if u < 0.5 else [(20, 10), (20, 30)]
        arbol(f, pos, ar, cols={10: C["red"]} if u < 1 else {20: C["green"]})
        texto(f, (640, 60), "derecha-derecha  →  rotación a la IZQUIERDA (el simétrico)", 26, "gold", 1, anchor="mm")
        if f.t >= f.c(3):
            etiqueta(f, (640, 560), "se recalcula la altura de los dos nodos que se mueven: O(1)", 24, "text", aparece(f, f.c(3)))


# doble: 30 ← 10 → 20  (izquierda-derecha)
D_A = {30: (640, 160), 10: (520, 280), 20: (640, 400)}
D_M = {30: (640, 160), 20: (520, 280), 10: (400, 400)}
D_B = {20: (640, 160), 10: (520, 280), 30: (760, 280)}


def e_dobles(f):
    texto(f, (640, 60), "izquierda-derecha: una rotación no basta", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    u1 = f.lin(f.c(1), 1.3)
    u2 = f.lin(f.c(2), 1.3)
    if u2 <= 0:
        pos = interp(D_A, D_M, u1)
        ar = [(30, 10), (10, 20)] if u1 < 0.5 else [(30, 20), (20, 10)]
    else:
        pos = interp(D_M, D_B, u2)
        ar = [(30, 20), (20, 10)] if u2 < 0.5 else [(20, 10), (20, 30)]
    arbol(f, pos, ar, cols={20: C["green"]} if u2 >= 1 else None)
    if f.t >= f.c(1):
        etiqueta(f, (640, 520), "1 · rotación a la izquierda en el hijo (10)", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 580), "2 · rotación a la derecha en la raíz (30)", 24, "text", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 650), "derecha-izquierda: lo simétrico  ·  rotaIzqDer y rotaDerIzq", 22, "green", aparece(f, f.c(3)))


def e_insertar(f):
    pasos = ["1 · se baja como en un ABB y se inserta como hoja", "2 · al volver de la recursión, se recalculan las alturas",
             "3 · el primer nodo desequilibrado se arregla con una rotación", "4 · con eso el árbol vuelve a ser AVL: O(log n)"]
    texto(f, (640, 60), "Insertar en un AVL", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, s in enumerate(pasos):
        if f.t >= f.c(k + 1 if k < 3 else 4):
            etiqueta(f, (640, 170 + 90 * k), s, 26, "text" if k < 3 else "green", aparece(f, f.c(k + 1 if k < 3 else 4)))
    if f.t >= f.c(4):
        etiqueta(f, (640, 600), "borrar es parecido, pero puede necesitar rotaciones en varios niveles", 22, "muted", aparece(f, f.c(4) + 0.5))


def e_set(f):
    f.box(60, 110, 560, 460, "TreeSet_AVL_plantilla.h  ·  Set<T>")
    ops = [("insert(e)", "O(log n)"), ("contains(e)", "O(log n)"), ("erase(e)", "O(log n)"), ("size(), empty()", "O(1)"), ("recorrido en orden", "O(n)")]
    for k, (o, c) in enumerate(ops):
        if f.t >= f.c(min(k, 1)):
            texto(f, (100, 180 + 70 * k), o, 26, "text", aparece(f, f.c(min(k, 1))), mono=True, fondo=C["panel"])
            texto(f, (440, 180 + 70 * k), c, 24, "gold", aparece(f, f.c(min(k, 1))), mono=True, fondo=C["panel"])
    f.box(660, 110, 560, 460, "en los ejercicios")
    if f.t >= f.c(2):
        texto(f, (700, 180), "01-1 · comprobar si es AVL:", 24, "blue", aparece(f, f.c(2)), fondo=C["panel"])
        texto(f, (700, 220), "recursión que devuelve altura,", 22, "text", aparece(f, f.c(2)), fondo=C["panel"])
        texto(f, (700, 252), "mínimo y máximo", 22, "text", aparece(f, f.c(2)), fondo=C["panel"])
    if f.t >= f.c(3):
        texto(f, (700, 340), "01-2 · k-ésimo:", 24, "blue", aparece(f, f.c(3)), fondo=C["panel"])
        texto(f, (700, 380), "un atributo más (tami) que hay", 22, "text", aparece(f, f.c(3)), fondo=C["panel"])
        texto(f, (700, 412), "que mantener al insertar y rotar", 22, "text", aparece(f, f.c(3)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Árboles AVL", [
        "ABB: izquierda < raíz < derecha; coste = altura",
        "AVL: alturas de los hijos difieren como mucho en 1",
        "rotaciones simples (II, DD) y dobles (ID, DI)",
        "insert, contains y erase en O(log n)",
    ])


ESC = [
    Escena("Árboles AVL: árboles de búsqueda que se mantienen equilibrados solos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Un árbol binario de búsqueda guarda, en cada nodo, los menores a la izquierda y los mayores a la derecha. "
           "Para buscar el sesenta: es mayor que cincuenta, a la derecha; menor que setenta, a la izquierda; y ahí está. "
           "Cada comparación baja un nivel, así que el coste es la altura del árbol. "
           "Y recorrido en inorden, da los elementos ordenados.",
           e_abb, titulo="Árboles de búsqueda", extra=1.5),
    Escena("El problema: si insertamos uno, dos, tres, cuatro y cinco en orden, cada uno va a la derecha del anterior. "
           "El árbol se convierte en una lista, y buscar cuesta ene. "
           "Hace falta mantenerlo equilibrado.",
           e_degenerado, titulo="El árbol degenerado", extra=1.5),
    Escena("Un árbol AVL exige que, en cada nodo, las alturas de los dos hijos se diferencien como mucho en uno. "
           "Cada nodo guarda su altura; el árbol vacío tiene altura cero. "
           "Con esa condición, la altura es logarítmica, y buscar, insertar y borrar cuestan logaritmo de ene.",
           e_avl, titulo="La condición AVL", extra=1.5),
    Escena("Cuando una inserción rompe el equilibrio, se arregla con rotaciones. "
           "Si el exceso está en el hijo izquierdo del hijo izquierdo, una rotación a la derecha: el veinte sube y el treinta baja a su derecha. "
           "Si está en la derecha de la derecha, la rotación simétrica, a la izquierda. "
           "Solo cambian unos pocos punteros y dos alturas: tiempo constante.",
           e_simples, titulo="Rotaciones simples", extra=2.0),
    Escena("Si el exceso está en el hijo derecho del hijo izquierdo, una rotación no basta. "
           "Primero se rota a la izquierda en el hijo. "
           "Y luego a la derecha en la raíz. "
           "El caso derecha izquierda es el simétrico. Son las rotaciones dobles.",
           e_dobles, titulo="Rotaciones dobles", extra=2.0),
    Escena("Insertar en un AVL tiene cuatro pasos. "
           "Se baja como en un árbol de búsqueda y se inserta como hoja. "
           "Al volver de la recursión se recalculan las alturas. "
           "El primer nodo desequilibrado se arregla con una rotación. "
           "Y con eso vuelve a ser AVL, en tiempo logarítmico. Borrar es parecido, pero puede necesitar rotar en varios niveles.",
           e_insertar, titulo="Insertar", extra=1.5),
    Escena("En el curso usamos el Set de la plantilla, implementado con un AVL. "
           "Insert, contains y erase cuestan logaritmo de ene; size y empty, constante. "
           "En el ejercicio uno uno se comprueba si un árbol es AVL con una recursión que devuelve altura, mínimo y máximo. "
           "Y en el uno dos se añade un atributo nuevo, tami, para encontrar el ka-ésimo, que hay que mantener al insertar y al rotar.",
           e_set, titulo="En el curso", extra=2.0),
    Escena("Resumiendo: un árbol de búsqueda cuesta lo que su altura; el AVL la mantiene logarítmica exigiendo equilibrio en cada nodo y arreglándolo con rotaciones simples y dobles.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/01-0", "../01-0_arboles_avl_teoria.mp4", "01-0")
