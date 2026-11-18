"""Vídeo EJ 01-1 · ¿Es un árbol AVL? (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../1-Arboles AVL/EJ_01-1/EJ 01-1.cpp"
TEMA = "Tema 1 · Árboles AVL"


def arbol(f, nodos, aristas, u=1.0, cols=None, info=None, r=32, marca=None):
    """nodos: {id: (texto, x, y)}; aristas: [(a, b)]; info: {id: texto debajo}."""
    if u <= 0:
        return
    for a, b in aristas:
        f.d.line((nodos[a][1], nodos[a][2], nodos[b][1], nodos[b][2]), fill=mix(C["bot"], C["border"], u), width=3)
    for k, (s, x, y) in nodos.items():
        c = (cols or {}).get(k, C["blue"])
        if marca and k in marca:
            f.d.ellipse((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=mix(C["bot"], C["gold"], u), width=4)
        f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        f.d.text((x, y), str(s), font=font(22, True), fill=mix(C["bot"], C["text"], u), anchor="mm")
        if info and k in info:
            for q, line in enumerate(info[k].split("\n")):
                f.d.text((x + r + 8, y - 12 + q * 20), line, font=font(18, True), fill=mix(C["bot"], C["gold"], u), anchor="lm")


# caso 1: 2 1 -1 -1 3 -1 4 -1 -1
N1 = {"2": (2, 640, 170), "1": (1, 460, 300), "3": (3, 820, 300), "4": (4, 960, 430)}
A1 = [("2", "1"), ("2", "3"), ("3", "4")]
# caso 2: 1 -1 3 2 -1 -1 4 -1 -1
N2 = {"1": (1, 640, 170), "3": (3, 820, 300), "2": (2, 700, 430), "4": (4, 940, 430)}
A2 = [("1", "3"), ("3", "2"), ("3", "4")]
# nieto que rompe el orden: 5, izq 2 con hijo derecho 7
N3 = {"5": (5, 640, 190), "2": (2, 480, 320), "7": (7, 600, 450)}
A3 = [("5", "2"), ("2", "7")]

# postorden del caso 1: (nodo, texto)
POST = [("1", "alt 1\n[1, 1]"), ("4", "alt 1\n[4, 4]"), ("3", "alt 2\n[3, 4]"), ("2", "alt 3\n[1, 4]")]


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.8)
        nod = {"a": ("", 960, 260), "b": ("", 880, 360), "c": ("", 1040, 360)}
        arbol(f, nod, [("a", "b"), ("a", "c")], u, r=26)
    portada(f, "EJ 01-1", "¿Es un árbol AVL?", TEMA, dib)


def e_problema(f):
    arbol(f, N1, A1, aparece(f, f.c(0)))
    if f.t >= f.c(1):
        etiqueta(f, (640, 560), "1 · de búsqueda: a la izquierda menores, a la derecha mayores", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 620), "2 · en cada nodo, las alturas de los hijos difieren como mucho en 1", 24, "text", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        texto(f, (640, 70), "entrada en preorden, -1 = vacío:   2 1 -1 -1 3 -1 4 -1 -1", 24, "gold", aparece(f, f.c(3)), mono=True, anchor="mm")


def e_fallos(f):
    if f.t < f.c(2):
        arbol(f, N2, A2, aparece(f, f.c(0)), cols={"1": C["red"]} if f.t >= f.c(1) else None)
        if f.t >= f.c(1):
            etiqueta(f, (640, 580), "en el 1: altura izquierda 0, derecha 2  →  NO es AVL", 24, "red", aparece(f, f.c(1)))
    else:
        arbol(f, N3, A3, aparece(f, f.c(2)), cols={"7": C["red"]} if f.t >= f.c(3) else None)
        if f.t >= f.c(2):
            texto(f, (640, 70), "¿basta con comparar cada nodo con sus hijos?", 26, "gold", aparece(f, f.c(2)), anchor="mm")
        if f.t >= f.c(3):
            etiqueta(f, (640, 580), "7 > 2 está bien con su padre, pero está a la izquierda del 5", 24, "red", aparece(f, f.c(3)))
            etiqueta(f, (640, 640), "hay que comparar con el MÁXIMO del subárbol izquierdo y el MÍNIMO del derecho", 22, "text", aparece(f, f.c(3) + 0.5))


def e_postorden(f):
    k, fr = paso_idx(f, f.c(1), f.c(3), len(POST))
    info = {n: s for n, s in POST[:max(0, min(k + 1, len(POST)))]}
    marca = {POST[k][0]} if 0 <= k < len(POST) else None
    cols = {n: C["green"] for n in info}
    arbol(f, N1, A1, 1, cols=cols, info=info, marca=marca)
    texto(f, (640, 70), "cada subárbol devuelve: ¿es AVL?, su altura, su mínimo y su máximo", 24, "gold", aparece(f, f.c(0)), anchor="mm")
    if 0 <= k < len(POST):
        n = POST[k][0]
        s = {"1": "hoja: altura 1, min = max = 1",
             "4": "hoja: altura 1, min = max = 4",
             "3": "alturas 0 y 1 ✓   3 < min der = 4 ✓",
             "2": "alturas 1 y 2 ✓   max izq = 1 < 2 < min der = 3 ✓"}[n]
        etiqueta(f, (640, 580), s, 24, "text", 1, mono=True)
    elif k >= len(POST):
        etiqueta(f, (640, 580), "SI", 34, "green", aparece(f, f.c(3)))
    if f.t >= f.c(2):
        texto(f, (640, 650), "primero los hijos, luego el nodo: postorden", 22, "muted", aparece(f, f.c(2)), anchor="mm")


A_L = find_line(CPP, "bool leerAVL(int& altura, int& minimo, int& maximo) {")
B_L = find_line(CPP, "return izqOK && derOK")
CODE = [(n, t) for n, t in codigo(CPP, A_L, B_L + 1, maxc=100) if not t.strip().startswith("//") and t.strip()]
L_VA = find_line(CPP, "if (valor == -1) {")
L_RE = find_line(CPP, "bool izqOK = leerAVL(")
L_AL = find_line(CPP, "altura = max(altIzq, altDer) + 1;")


def e_codigo(f):
    marcas = [(f.c(0), {A_L}), (f.c(1), set(range(L_VA, L_VA + 5))), (f.c(2), {L_RE, L_RE + 1}),
              (f.c(3), {L_AL, L_AL + 1, L_AL + 2}), (f.c(4), {B_L})]
    hl = set()
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(20, 70, 1240, 620, CODE, hl=hl, title="leerAVL: se lee y se comprueba a la vez", size=18)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("no se construye el árbol: preorden = raíz, izquierdo, derecho", "text"),
             ("vacío: altura 0, mínimo INT_MAX, máximo INT_MIN (las comparaciones salen solas)", "text"),
             ("se lee siempre el árbol entero, aunque ya falle, para no descolocar la entrada", "text"),
             ("versión genérica: read_tree<T> y un struct Info<T>; vale para int y string", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 23, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "¿Es un árbol AVL?", [
        "AVL = de búsqueda + equilibrado en altura",
        "recursión en postorden: altura, mínimo y máximo",
        "max izq < raíz < min der  y  |altIzq − altDer| ≤ 1",
        "O(n): cada nodo se mira una vez",
    ])


ESC = [
    Escena("¿Es un árbol AVL? Comprobarlo recorriendo el árbol una sola vez.", e_portada, titulo="Portada", extra=1.0),
    Escena("Nos dan un árbol binario de enteros, y hay que decir si es AVL. "
           "Primero, tiene que ser de búsqueda: en cada nodo, todo lo de la izquierda es menor y todo lo de la derecha, mayor. "
           "Segundo, en cada nodo las alturas de los dos hijos se diferencian como mucho en uno. "
           "El árbol llega en preorden, con menos uno para el árbol vacío.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Este no lo es: "
           "en la raíz, el hijo izquierdo tiene altura cero y el derecho, dos. "
           "¿Y basta con comparar cada nodo con sus hijos? "
           "No: aquí el siete es mayor que su padre, el dos, pero está a la izquierda del cinco. Hay que comparar con el máximo y el mínimo de cada subárbol.",
           e_fallos, titulo="Dos maneras de fallar", extra=1.5),
    Escena("Por eso cada subárbol devuelve cuatro cosas: si es AVL, su altura, su mínimo y su máximo. "
           "Las hojas uno y cuatro tienen altura uno. El tres tiene alturas cero y uno, y es menor que el mínimo de su derecha. "
           "Para decidir sobre un nodo, primero hay que resolver sus hijos: es un postorden. "
           "En la raíz todo cuadra: sí es AVL.",
           e_postorden, titulo="De abajo arriba", extra=1.5),
    Escena("En el código, leerAVL devuelve si es AVL y deja la altura, el mínimo y el máximo en parámetros por referencia. "
           "Si lee menos uno, es vacío: altura cero y centinelas. "
           "Si no, se llama dos veces, para el izquierdo y para el derecho. "
           "Calcula su altura, su mínimo y su máximo. "
           "Y es AVL si lo son los dos hijos, las alturas casi coinciden y el valor queda entre el máximo izquierdo y el mínimo derecho.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("No hace falta construir el árbol, porque el preorden permite leerlo y comprobarlo a la vez. "
           "Los centinelas del vacío hacen que las comparaciones salgan sin casos especiales. "
           "Siempre se lee el árbol entero, para que el siguiente caso empiece bien. "
           "Y la versión genérica hace lo mismo con read tree y un struct Info, y sirve para enteros y palabras.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: un AVL es de búsqueda y equilibrado; se comprueba en postorden propagando altura, mínimo y máximo.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/01-1", "../01-1_es_un_arbol_avl.mp4", "01-1")
