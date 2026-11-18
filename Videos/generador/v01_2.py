"""Vídeo EJ 01-2 · El k-ésimo elemento en un árbol AVL (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

H_FILE = "../../1-Arboles AVL/EJ_01-2/TreeSet_AVL_plantilla.h"
TEMA = "Tema 1 · Árboles AVL"

# árbol: 50(30(20, 40(35, ·)), 70(60, 80))
POS = {50: (640, 150), 30: (420, 260), 70: (860, 260), 20: (310, 380), 40: (530, 380), 60: (760, 380), 80: (960, 380), 35: (470, 500)}
HIJOS = {50: (30, 70), 30: (20, 40), 70: (60, 80), 40: (35, None), 20: (None, None), 60: (None, None), 80: (None, None), 35: (None, None)}


def tam(n):
    if n is None:
        return 0
    i, d = HIJOS[n]
    return 1 + tam(i) + tam(d)


TAMI = {n: tam(HIJOS[n][0]) + 1 for n in POS}


def baja(k):
    pasos, n = [], 50
    while n is not None:
        t = TAMI[n]
        if k == t:
            pasos.append((n, k, "="))
            return pasos, n
        if k < t:
            pasos.append((n, k, "<"))
            n = HIJOS[n][0]
        else:
            pasos.append((n, k, ">"))
            k -= t
            n = HIJOS[n][1]
    pasos.append((None, k, "null"))
    return pasos, None


def dibuja(f, u=1.0, tami=True, marca=None, cols=None, pos=None, etq=None):
    pos = pos or POS
    if u <= 0:
        return
    for n, (i, d) in HIJOS.items():
        for h in (i, d):
            if h is not None and h in pos and n in pos:
                f.d.line((pos[n], pos[h]), fill=mix(C["bot"], C["border"], u), width=3)
    for n, (x, y) in pos.items():
        c = (cols or {}).get(n, C["blue"])
        if marca and n in marca:
            f.d.ellipse((x - 42, y - 42, x + 42, y + 42), outline=mix(C["bot"], C["gold"], u), width=4)
        f.d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        f.d.text((x, y), str(n), font=font(22, True), fill=mix(C["bot"], C["text"], u), anchor="mm")
        if tami:
            s = (etq or TAMI).get(n)
            if s is not None:
                caja(f, x + 44, y - 30, s, c="gold", u=u, w=34, h=28, tam=16, borde=2)


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.8)
        for (x, y), s in zip([(960, 260), (880, 360), (1040, 360)], ["2", "1", "3"]):
            caja(f, x, y, s, c="blue", u=u, w=60, h=60, tam=24)
    portada(f, "EJ 01-2", "El k-ésimo en un AVL", TEMA, dib)


def e_problema(f):
    dibuja(f, aparece(f, f.c(0)), tami=False)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        orden = sorted(POS)
        for q, v in enumerate(orden):
            caja(f, 220 + q * 120, 620, v, c="green" if q == 3 else "blue", u=aparece(f, f.c(1) + 0.15 * q), w=90, h=50, tam=22)
            texto(f, (220 + q * 120, 660), f"{q + 1}º", 16, "muted", aparece(f, f.c(1) + 0.15 * q), anchor="mm")
        texto(f, (640, 560), "kesimo(4) = 40", 26, "green", aparece(f, f.c(1) + 1.5), mono=True, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 60), "en tiempo LOGARÍTMICO; si no existe, ??", 26, "gold", aparece(f, f.c(2)))


def e_tami(f):
    dibuja(f, 1, tami=f.t >= f.c(1))
    texto(f, (640, 50), "recorrer en inorden cuesta O(k): demasiado", 24, "red", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 590), "tami = tamaño del hijo izquierdo + 1  =  posición de la raíz en su subárbol", 24, "gold", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 650), "50 tiene 4 por la izquierda: es el 5º", 24, "text", aparece(f, f.c(2)))


def e_baja(f, k, t0, t1):
    pasos, res = baja(k)
    q, fr = paso_idx(f, t0, t1, len(pasos))
    q = max(0, min(q, len(pasos) - 1))
    camino = [p[0] for p in pasos[:q + 1] if p[0] is not None]
    cols = {n: C["green"] for n in camino}
    dibuja(f, 1, marca={pasos[q][0]} if pasos[q][0] is not None else None, cols=cols)
    n, kk, op = pasos[q]
    if op == "=":
        s = f"k = {kk} = tami: es el {n}"
        c = "green"
    elif op == "<":
        s = f"k = {kk} < {TAMI[n]}: a la izquierda con el mismo k"
        c = "text"
    elif op == ">":
        s = f"k = {kk} > {TAMI[n]}: a la derecha con k = {kk} − {TAMI[n]} = {kk - TAMI[n]}"
        c = NARANJA
    else:
        s = "nullptr: no existe  →  ??"
        c = "red"
    texto(f, (640, 50), f"kesimo({k})", 30, "gold", 1, mono=True, anchor="mm")
    etiqueta(f, (640, 620), s, 24, c, 1, mono=True)


def e_k4(f):
    e_baja(f, 4, f.c(0), f.T - 1)


def e_k79(f):
    if f.t < f.c(2):
        e_baja(f, 7, f.c(0), f.c(2) - 0.3)
    else:
        e_baja(f, 9, f.c(2), f.T - 1)


# rotación: 16|3 ← 8|2 ← 4|1   →   8|2 con 4|1 y 16|1
ANTES = {16: (640, 170), 8: (500, 290), 4: (380, 410)}
DESPUES = {8: (640, 170), 4: (500, 290), 16: (780, 290)}


def e_mantener(f):
    texto(f, (640, 50), "hay que mantener tami al insertar y al rotar", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    u = f.lin(f.c(2), 1.5)
    pos = {n: (lerp(ANTES[n][0], DESPUES[n][0], ease(u)), lerp(ANTES[n][1], DESPUES[n][1], ease(u))) for n in ANTES}
    hijos_a = {16: (8, None), 8: (4, None), 4: (None, None)}
    hijos_b = {8: (4, 16), 4: (None, None), 16: (None, None)}
    hij = hijos_a if u < 0.5 else hijos_b
    for n, (i, d) in hij.items():
        for h in (i, d):
            if h is not None:
                f.d.line((pos[n], pos[h]), fill=C["border"], width=3)
    etq = {16: 3, 8: 2, 4: 1} if f.t < f.c(3) else {16: 1, 8: 2, 4: 1}
    for n, (x, y) in pos.items():
        f.d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=C["panel"], outline=C["red"] if (n == 16 and f.t >= f.c(3)) else C["blue"], width=3)
        f.d.text((x, y), str(n), font=font(22, True), fill=C["text"], anchor="mm")
        caja(f, x + 44, y - 30, etq[n], c="gold", w=34, h=28, tam=16, borde=2)
    if f.t >= f.c(1):
        etiqueta(f, (640, 500), "insertar por la izquierda: tami + 1 en el camino", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 560), "rotaDer:  r2->tami −= r1->tami   (16: 3 − 2 = 1)", 24, "red", aparece(f, f.c(3)), mono=True)
    if f.t >= f.c(4):
        etiqueta(f, (640, 620), "rotaIzq:  r2->tami += r1->tami   ·   las dobles son dos simples", 24, "text", aparece(f, f.c(4)), mono=True)


A_L = find_line(H_FILE, "T const& kesimo(int k, Link a) const {")
CODE = codigo(H_FILE, A_L, A_L + 5, maxc=90)
L_IN = find_line(H_FILE, "a->tami += 1;")
L_RD = find_line(H_FILE, "r2->tami -= r1->tami;")
L_RI = find_line(H_FILE, "r2->tami += r1->tami;")


def e_codigo(f):
    if f.t < f.c(3):
        hl = {A_L + 1} if f.t < f.c(1) else ({A_L + 2} if f.t < f.c(2) else {A_L + 3, A_L + 4})
        f.code(40, 90, 1200, 280, CODE, hl=hl, title="kesimo(k, a)", size=20)
    else:
        lines = [(L_IN, codigo(H_FILE, L_IN, L_IN)[0][1]), (L_RD, codigo(H_FILE, L_RD, L_RD)[0][1]), (L_RI, codigo(H_FILE, L_RI, L_RI)[0][1])]
        f.code(40, 90, 1200, 200, lines, hl={L_IN, L_RD, L_RI}, title="los tres sitios donde se actualiza tami", size=20)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("un valor repetido no se inserta: tami no cambia y hay menos elementos", "text"),
             ("k fuera de rango (o ≤ 0) siempre acaba en nullptr: excepción y ??", "text"),
             ("en cada paso se descarta un subárbol entero", "text"),
             ("altura O(log n) en un AVL:  kesimo en O(log n)", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "El k-ésimo en un AVL", [
        "tami = tamaño del izquierdo + 1 en cada nodo",
        "k = tami: la raíz · k < tami: izquierda · k > tami: derecha con k − tami",
        "mantener tami al insertar y en las rotaciones",
        "O(log n) por consulta",
    ])


ESC = [
    Escena("El ka-ésimo elemento en un árbol AVL, en tiempo logarítmico.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos un conjunto guardado en un árbol AVL. "
           "Queremos una operación nueva, ka-ésimo, que devuelva el elemento que ocupa la posición ka si los ordenamos de menor a mayor: el cuarto es cuarenta. "
           "Tiene que costar un logaritmo, y si la posición no existe se escriben dos interrogaciones.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Recorrer el árbol en inorden y contar funcionaría, pero cuesta ka pasos. "
           "La idea es guardar en cada nodo un número más, tami: el tamaño de su hijo izquierdo más uno. Es la posición de ese nodo dentro de su subárbol. "
           "El cincuenta tiene cuatro por la izquierda, así que es el quinto.",
           e_tami, titulo="El atributo tami", extra=1.5),
    Escena("Buscamos el cuarto. En el cincuenta, cuatro es menor que cinco: está a la izquierda, y seguimos buscando el cuarto. "
           "En el treinta, cuatro es mayor que dos: está a la derecha, y allí es el segundo. "
           "En el cuarenta, dos es igual a su tami: es él.",
           e_k4, titulo="kesimo(4)", extra=1.5),
    Escena("El séptimo: siete es mayor que cinco, así que a la derecha buscando el segundo. "
           "En el setenta, dos es su tami: es el setenta. "
           "Y el noveno: a la derecha con cuatro, luego con dos, luego con uno, y se llega a un hueco vacío: no existe.",
           e_k79, titulo="kesimo(7) y kesimo(9)", extra=1.5),
    Escena("Para que esto funcione, tami tiene que estar siempre bien. "
           "Al insertar por la izquierda, se suma uno al tami de cada nodo del camino. "
           "Y en las rotaciones cambia quién es hijo izquierdo de quién. "
           "En una rotación a la derecha, el nodo que baja pierde el tami del que sube: dieciséis pasa de tres a uno. "
           "En una rotación a la izquierda, el que sube lo suma. Las dobles son dos simples.",
           e_mantener, titulo="Mantener tami", extra=2.0),
    Escena("En el código, si se llega a un nulo, se lanza out of range. "
           "Si ka es igual a tami, se devuelve el elemento. "
           "Si es menor, se sigue por la izquierda; si es mayor, por la derecha restando tami. "
           "Y estos son los tres sitios donde se actualiza tami: al insertar y en las dos rotaciones.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Un valor repetido no se inserta, así que no toca tami. "
           "Una ka fuera de rango siempre termina en un nulo y lanza la excepción. "
           "Cada paso descarta un subárbol entero. "
           "Y como la altura de un AVL es logarítmica, ka-ésimo también.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: con tami en cada nodo, se baja comparando ka con tami, y basta mantenerlo al insertar y al rotar.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/01-2", "../01-2_kesimo_en_un_avl.mp4", "01-2")
