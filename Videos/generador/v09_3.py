"""Vídeo EJ 09-3 · Carreras de coches (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../9-Algoritmos voraces II/EJ_09-3/EJ_09-3.cpp"
TEMA = "Tema 9 · Algoritmos voraces II"
V = 20
PILAS = [12, 3, 15, 8, 10]
ORD = sorted(PILAS)
XP = [240 + 200 * k for k in range(5)]
YB = 600


def pila(f, x, y, v, u=1.0, c=None, gris=False, esc=12):
    """Pila vertical con su voltaje; (x, y) = base."""
    if u <= 0:
        return
    c = C["dim"] if gris else (c or C["green"])
    h = 40 + v * esc
    f.d.rounded_rectangle((x - 28, y - h, x + 28, y), 8, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
    f.d.rectangle((x - 12, y - h - 10, x + 12, y - h), fill=mix(C["bot"], c, u))
    lv = min(1.0, v / 16)
    f.d.rectangle((x - 20, y - 8 - (h - 16) * lv, x + 20, y - 8), fill=mix(C["bot"], mix(C["panel"], c, 0.6), u))
    f.d.text((x, y - h / 2), str(v), font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def coche(f, x, y, u=1.0, ok=True):
    if u <= 0:
        return
    c = mix(C["bot"], C["red"] if ok else C["dim"], u)
    f.d.rounded_rectangle((x - 70, y - 20, x + 70, y + 14), 12, fill=c)
    f.d.polygon([(x - 36, y - 20), (x - 18, y - 44), (x + 24, y - 44), (x + 44, y - 20)], fill=c)
    for dx in (-40, 40):
        f.d.ellipse((x + dx - 15, y + 2, x + dx + 15, y + 32), fill=mix(C["bot"], (30, 30, 36), u))


def e_portada(f):
    def dib(f):
        coche(f, 950, 330, f.p(0.3, 0.6))
        pila(f, 880, 470, 8, f.p(0.6, 0.5), esc=6)
        pila(f, 1020, 470, 12, f.p(0.8, 0.5), esc=6)
    portada(f, "EJ 09-3", "Carreras de coches", TEMA, dib)


def e_problema(f):
    for k, v in enumerate(PILAS):
        pila(f, XP[k], YB, v, aparece(f, f.c(0) + 0.2 * k))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        coche(f, 640, 150, u)
        texto(f, (640, 210), f"cada coche: 2 pilas que sumen ≥ V = {V}", 26, "gold", u, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 660), "¿cuántos coches a la vez, como máximo?", 26, "text", aparece(f, f.c(2)))


def e_malo(f):
    # juntar las dos más fuertes: 15 + 12, y quedan 3, 8, 10
    xs = [240, 440, 640, 840, 1040]
    for k, v in enumerate(ORD):
        if f.t >= f.c(1) and v in (12, 15):
            continue
        pila(f, xs[k], YB, v)
    texto(f, (640, 70), "¿juntar las dos más potentes?", 30, "red", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = f.lin(f.c(1), 1.0)
        for k, v in ((3, 12), (4, 15)):
            p = mueve((xs[k], YB), (560 + (k - 3) * 140, 380), u)
            pila(f, p[0], p[1], v, esc=8)
        coche(f, 630, 160, aparece(f, f.c(1) + 0.8))
        texto(f, (720, 160), "15 + 12 = 27", 26, "green", aparece(f, f.c(1) + 0.8), anchor="lm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 660), "las que quedan no llegan: 8 + 10 = 18 < 20  →  1 coche", 26, "red", aparece(f, f.c(2)))


def traza():
    ev, i, j = [], 0, len(ORD) - 1
    while i < j:
        ok = ORD[i] + ORD[j] >= V
        ev.append((i, j, ok))
        if ok:
            i, j = i + 1, j - 1
        else:
            i += 1
    return ev


EV = traza()
NC = sum(e[2] for e in EV)


def e_voraz(f):
    k, fr = paso_idx(f, f.c(1), f.c(4), len(EV))
    estado = {}
    coches = []
    for q in range(max(0, min(k + (1 if fr > 0.5 else 0), len(EV)))):
        i, j, ok = EV[q]
        if ok:
            estado[i] = estado[j] = ("coche", len(coches))
            coches.append((i, j, q))
        else:
            estado[i] = ("fuera", None)
    for c_, (i, j, q) in enumerate(coches):
        xc = 360 + 380 * c_
        coche(f, xc, 140)
    for p in range(len(ORD)):
        st = estado.get(p)
        if st and st[0] == "coche":
            c_ = st[1]
            i, j, q = coches[c_]
            tq = f.c(1) + (q + 0.5) * (f.c(4) - f.c(1)) / len(EV)
            dst = (360 + 380 * c_ + (-50 if p == i else 50), 400)
            pos = mueve((XP[p], YB), dst, f.lin(tq, 0.8))
            pila(f, pos[0], pos[1], ORD[p], esc=8)
        else:
            pila(f, XP[p], YB, ORD[p], gris=st is not None)
            if st:
                tick(f, XP[p], YB + 30, False)
    texto(f, (640, 60), "ordenadas: la más débil y la más fuerte", 22, "muted", aparece(f, f.c(0)), anchor="mm")
    if 0 <= k < len(EV):
        i, j, ok = EV[k]
        for p, s in ((i, "i"), (j, "j")):
            f.d.polygon([(XP[p] - 12, YB + 40), (XP[p] + 12, YB + 40), (XP[p], YB + 24)], fill=C["gold"])
            texto(f, (XP[p], YB + 56), s, 20, "gold", 1, mono=True, anchor="mm")
        s = f"{ORD[i]} + {ORD[j]} = {ORD[i] + ORD[j]} " + ("≥ 20: coche" if ok else "< 20: la débil no sirve con nadie")
        etiqueta(f, (640, 692), s, 24, "green" if ok else "red", 1)
    elif k >= len(EV):
        etiqueta(f, (640, 692), f"{NC} coches", 30, "green", aparece(f, f.c(4)))


def e_porque(f):
    texto(f, (640, 80), "la más débil que acompaña bien a la más fuerte es su mejor pareja", 24, "gold", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(0))
    pila(f, 400, 520, 8, u)
    pila(f, 560, 520, 15, u)
    pila(f, 800, 520, 10, u)
    pila(f, 960, 520, 12, u)
    if f.t >= f.c(1):
        u1 = aparece(f, f.c(1))
        f.d.line((400, 200, 560, 200), fill=mix(C["bot"], C["green"], u1), width=4)
        f.d.line((800, 200, 960, 200), fill=mix(C["bot"], C["green"], u1), width=4)
        texto(f, (480, 180), "23", 22, "green", u1, anchor="mm")
        texto(f, (880, 180), "22", 22, "green", u1, anchor="mm")
        etiqueta(f, (640, 640), "las potentes quedan para las demás", 26, "text", u1)
    if f.t >= f.c(2):
        etiqueta(f, (640, 580), "si ni con la más fuerte llega, no llega con ninguna", 24, "red", aparece(f, f.c(2)))


A_L = find_line(CPP, "sort(pilas.begin(), pilas.end());")
B_L = find_line(CPP, "cout << coches")
CODE = codigo(CPP, A_L, B_L, maxc=80)
L_IF = find_line(CPP, "if (pilas[i] + pilas[j] >= V) {")
L_EL = find_line(CPP, "++i;                           // la mas debil")


def e_codigo(f):
    hl = {A_L}
    k, fr = paso_idx(f, f.c(1), f.T - 2.5, len(EV))
    if 0 <= k < len(EV):
        ok = EV[k][2]
        hl = {L_IF} if fr < 0.5 else ({L_IF + 1, L_IF + 2} if ok else {L_EL - 1, L_EL})
    elif k >= len(EV):
        hl = {B_L}
    f.code(20, 90, 720, 440, CODE, hl=hl, title="emparejar extremos", size=18)
    x0 = 780
    texto(f, (x0, 130), f"V = {V}", 24, "gold", 1, mono=True)
    nc = 0
    for q in range(max(0, min(k + (1 if fr >= 0.5 else 0), len(EV)))):
        nc += EV[q][2]
    for p, v in enumerate(ORD):
        cur = 0 <= k < len(EV) and p in EV[k][:2]
        caja(f, x0 + 40 + p * 90, 220, v, c="gold" if cur else "green", w=74, borde=5 if cur else 2)
    if 0 <= k < len(EV):
        i, j, ok = EV[k]
        texto(f, (x0 + 40 + i * 90, 270), "i", 22, "gold", 1, mono=True, anchor="mm")
        texto(f, (x0 + 40 + j * 90, 270), "j", 22, "gold", 1, mono=True, anchor="mm")
    texto(f, (x0, 340), f"coches = {nc}", 28, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("mientras i < j: hacen falta dos pilas distintas", "text"),
             ("≥ V: sumar justo V también vale", "text"),
             ("N ≤ 300.000:  O(N log N) por la ordenación; los punteros, lineal", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 180 + 110 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Carreras de coches", [
        "ordenar las pilas",
        "más débil + más fuerte ≥ V: coche",
        "si no llegan, la más débil se descarta",
        "dos punteros que se acercan · O(N log N)",
    ])


ESC = [
    Escena("Carreras de coches. Cuántos coches pueden correr a la vez con las pilas que tenemos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos pilas, cada una con su voltaje. "
           "Cada coche necesita dos pilas cuyos voltajes sumen al menos uve; aquí, veinte. "
           "¿Cuántos coches pueden funcionar a la vez como máximo?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("¿Y si juntamos las dos más potentes? "
           "Quince más doce, un coche. "
           "Pero las que quedan, ocho y diez, suman dieciocho: no llegan. Solo un coche, y se podían dos.",
           e_malo, titulo="Lo que no funciona", extra=1.5),
    Escena("Ordenamos las pilas y miramos los extremos: la más débil, con i, y la más fuerte, con jota. "
           "Si juntas llegan a veinte, forman un coche y las dos se retiran. "
           "Si no llegan, la más débil no sirve ni con la más fuerte, así que no sirve con ninguna: se descarta. "
           "Así salen dos coches.",
           e_voraz, titulo="Emparejar extremos", extra=1.5),
    Escena("¿Por qué? A la más fuerte le damos la más débil que la acompaña bien. "
           "Así las potentes quedan para ayudar a las demás. "
           "Y una pila que no llega ni con la más fuerte no llega con ninguna.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, se ordenan las pilas. "
           "Mientras i sea menor que jota: si suman al menos uve, un coche más y se acercan los dos punteros; si no, solo avanza i.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("La condición es i menor que jota, porque hacen falta dos pilas distintas. "
           "Sumar exactamente uve también vale. "
           "Y el coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: se ordenan las pilas y se emparejan la más débil y la más fuerte; si no llegan, la débil se descarta.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/09-3", "../09-3_carreras_de_coches.mp4", "09-3")
