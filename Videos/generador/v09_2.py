"""Vídeo EJ 09-2 · El alienígena infiltrado (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../9-Algoritmos voraces II/EJ_09-2/EJ_09-2.cpp"
TEMA = "Tema 9 · Algoritmos voraces II"
CI, FI = 1, 10
TR = [(0, 5), (2, 8), (5, 10), (7, 11)]
COLS = [C["blue"], C["purple"], NARANJA, C["green"]]
X0, X1, A, B = 140, 1180, 0, 12
YT = 520


def X(v):
    return X0 + (v - A) * (X1 - X0) / (B - A)


def eje(f, u=1.0):
    if u <= 0:
        return
    f.d.line((X0, YT, X1, YT), fill=mix(C["bot"], C["muted"], u), width=2)
    for v in range(A, B + 1):
        f.d.line((X(v), YT - 5, X(v), YT + 5), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((X(v), YT + 22), str(v), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def objetivo(f, c, fi, cubierto=None, u=1.0, y=440):
    if u <= 0:
        return
    f.d.rounded_rectangle((X(c), y - 22, X(fi), y + 22), 10, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], C["gold"], u), width=3)
    if cubierto is not None and cubierto > c:
        f.d.rounded_rectangle((X(c), y - 22, X(min(cubierto, fi)), y + 22), 10, fill=mix(C["panel"], C["green"], 0.55))
    f.d.text((X(c) - 12, y), "[C, F)", font=font(18, True), fill=mix(C["bot"], C["gold"], u), anchor="rm")


def trabajo(f, k, a, b, y, u=1.0, gris=False, sel=False, cand=False):
    if u <= 0:
        return
    c = C["dim"] if gris else COLS[k]
    x0, x1 = X(a), lerp(X(a), X(b), u)
    if x1 - x0 < 8:
        return
    f.d.rounded_rectangle((x0 + 2, y - 20, x1 - 2, y + 20), 9, fill=mix(C["panel"], c, 0.45 if not gris else 0.15),
                          outline=C["gold"] if sel else c, width=5 if sel else 3)
    if u >= 1:
        f.d.text(((x0 + x1) / 2, y), f"[{a}, {b})", font=font(18, True), fill=C["text"], anchor="mm")
    if cand:
        f.d.text((x0 - 10, y), "≤", font=font(20, True), fill=C["gold"], anchor="rm")


YR = [140, 205, 270, 335]


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.8)
        x, y = 960, 330
        f.d.ellipse((x - 60, y - 70, x + 60, y + 50), fill=mix(C["bot"], (90, 200, 120), u))
        f.d.ellipse((x - 38, y - 30, x - 8, y), fill=mix(C["bot"], (10, 20, 10), u))
        f.d.ellipse((x + 8, y - 30, x + 38, y), fill=mix(C["bot"], (10, 20, 10), u))
    portada(f, "EJ 09-2", "El alienígena infiltrado", TEMA, dib)


def e_problema(f):
    eje(f, aparece(f, f.c(0)))
    objetivo(f, CI, FI, u=aparece(f, f.c(0)))
    for k, (a, b) in enumerate(TR):
        trabajo(f, k, a, b, YR[k], f.lin(f.c(1) + 0.3 * k, 0.8))
    if f.t >= f.c(2):
        texto(f, (640, 70), "en cada instante de [C, F), al menos un trabajo en marcha", 26, "text", aparece(f, f.c(2)), anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 640), "mínimo de trabajos, o Imposible", 28, "gold", aparece(f, f.c(3)))


def traza():
    ev, cub, i, orden = [], CI, 0, sorted(range(len(TR)), key=lambda k: TR[k])
    while cub < FI:
        cand, lejos, mejor = [], cub, None
        while i < len(orden) and TR[orden[i]][0] <= cub:
            cand.append(orden[i])
            if TR[orden[i]][1] > lejos:
                lejos, mejor = TR[orden[i]][1], orden[i]
            i += 1
        ev.append((cub, cand, mejor, lejos))
        if lejos == cub:
            break
        cub = lejos
    return ev


EV = traza()


def e_voraz(f):
    eje(f)
    k, fr = paso_idx(f, f.c(1), f.c(4), len(EV))
    cub = CI
    elegidos, vistos = set(), set()
    for q in range(max(0, min(k + (1 if fr > 0.6 else 0), len(EV)))):
        cub = EV[q][3]
        elegidos.add(EV[q][2])
    for q in range(max(0, min(k + 1, len(EV)))):
        vistos |= set(EV[q][1])
    objetivo(f, CI, FI, cubierto=cub)
    cand = set(EV[k][1]) if 0 <= k < len(EV) else set()
    for j, (a, b) in enumerate(TR):
        trabajo(f, j, a, b, YR[j], gris=j in vistos and j not in elegidos and j not in cand,
                sel=j in elegidos or (0 <= k < len(EV) and j == EV[k][2] and fr > 0.3), cand=j in cand)
    x = X(cub)
    f.d.line((x, 110, x, YT), fill=C["gold"], width=3)
    texto(f, (x + 8, 100), f"cubierto = {cub}", 20, "gold", 1)
    if 0 <= k < len(EV):
        c0, cs, m, lejos = EV[k]
        etiqueta(f, (640, 640), f"empiezan ≤ {c0}: " + ", ".join(f"[{TR[j][0]},{TR[j][1]})" for j in cs) + f"  →  el que llega más lejos: {lejos}", 22, "text", 1)
    elif k >= len(EV):
        etiqueta(f, (640, 640), f"{len(EV)} trabajos", 30, "green", aparece(f, f.c(4)))
    texto(f, (640, 60), "ordenados por comienzo", 22, "muted", aparece(f, f.c(0)), anchor="mm")


def e_imposible(f):
    eje(f)
    objetivo(f, 0, 3, cubierto=1 if f.t >= f.c(1) else 0)
    trabajo(f, 0, 0, 1, YR[1])
    trabajo(f, 1, 2, 3, YR[2])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        f.d.rectangle((X(1), 418, X(2), 462), fill=mix(C["bot"], C["red"], u))
        texto(f, (X(1.5), 380), "hueco", 22, "red", u, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 640), "nadie empieza ≤ 1 y pasa de 1:  Imposible", 26, "red", aparece(f, f.c(2)))


def e_porque(f):
    eje(f)
    objetivo(f, CI, FI, cubierto=5)
    trabajo(f, 1, 2, 8, YR[1], sel=False)
    trabajo(f, 2, 5, 10, YR[2], sel=True)
    u = aparece(f, f.c(0))
    texto(f, (640, 70), "de los que no dejan hueco, el que llega más lejos", 26, "gold", u, anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        f.d.rectangle((X(8), 180, X(10), 300), outline=mix(C["bot"], C["green"], u), width=3)
        texto(f, (X(9), 160), "lo que se gana", 20, "green", u, anchor="mm")
        etiqueta(f, (640, 640), "cambiar el de cualquier solución por este no deja huecos y cubre igual o más", 22, "text", u)


A_L = find_line(CPP, "sort(trab.begin(), trab.end());")
B_L = find_line(CPP, "else cout << \"Imposible")
CODE = codigo(CPP, A_L, B_L, maxc=84)
L_W = find_line(CPP, "while (i < N && trab[i].first <= cubierto) {")
L_HU = find_line(CPP, "if (masLejos == cubierto) { posible = false; break; }")
L_CU = find_line(CPP, "cubierto = masLejos;")


def e_codigo(f):
    hl = {A_L}
    k, fr = paso_idx(f, f.c(1), f.T - 2.5, len(EV))
    if 0 <= k < len(EV):
        hl = [{L_W, L_W + 1, L_W + 2}, {L_HU}, {L_CU, L_CU + 1}][min(2, int(fr * 3))]
    elif k >= len(EV):
        hl = {B_L - 1}
    f.code(10, 90, 830, 520, CODE, hl=hl, title="cubrir un intervalo", size=17)
    x0 = 880
    cub, us = CI, 0
    for q in range(max(0, min(k + (1 if fr > 0.66 else 0), len(EV)))):
        cub, us = EV[q][3], us + 1
    texto(f, (x0, 140), f"[C, F) = [{CI}, {FI})", 24, "gold", 1, mono=True)
    for j, (a, b) in enumerate(sorted(TR)):
        cand = 0 <= k < len(EV) and TR.index((a, b)) in EV[k][1]
        caja(f, x0 + 70, 220 + j * 56, f"[{a}, {b})", c="gold" if cand else "blue", w=120, h=44, tam=20, borde=5 if cand else 2)
    texto(f, (x0, 470), f"cubierto = {cub}", 24, "green", 1, mono=True)
    texto(f, (x0, 510), f"usados = {us}", 24, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("los intervalos son semiabiertos: [0,5) y [5,10) no dejan hueco", "text"),
             ("i nunca retrocede: cada trabajo se mira una sola vez", "text"),
             ("puede haber N = 0 trabajos: Imposible (salvo que C = F)", "text"),
             ("O(N log N) por la ordenación; el bucle es lineal", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "El alienígena infiltrado", [
        "cubrir [C, F) con el mínimo de intervalos",
        "ordenar por comienzo; cubierto empieza en C",
        "de los que empiezan ≤ cubierto, el que llega más lejos",
        "si nadie pasa de cubierto: Imposible · O(N log N)",
    ])


ESC = [
    Escena("El alienígena infiltrado. Cubrir un intervalo de tiempo con el mínimo número de trabajos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos un intervalo de tiempo, de ce a efe, que hay que vigilar. "
           "Y ene trabajos, cada uno con su comienzo y su fin. "
           "En cada instante del intervalo tiene que haber al menos un trabajo en marcha. "
           "Hay que decir cuántos trabajos hacen falta como mínimo, o que es imposible.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Ordenamos los trabajos por su comienzo, y llevamos hasta dónde está cubierto, que al principio es ce. "
           "Entre los trabajos que empiezan antes de lo cubierto, que son los que no dejan hueco, elegimos el que acaba más tarde. "
           "Lo cubierto avanza hasta su fin, y repetimos. "
           "Al llegar a efe, hemos usado dos trabajos.",
           e_voraz, titulo="La voraz", extra=1.5),
    Escena("¿Y si ningún trabajo pasa de lo cubierto? "
           "Aquí uno acaba en uno y el siguiente empieza en dos: el instante uno no lo cubre nadie. "
           "Entonces es imposible.",
           e_imposible, titulo="Imposible", extra=1.5),
    Escena("¿Por qué el que llega más lejos? "
           "Cualquier solución tiene que usar un trabajo que empiece antes de lo cubierto; cambiarlo por el que llega más lejos no deja huecos y cubre lo mismo o más.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, se ordenan los trabajos. "
           "Mientras lo cubierto no llegue a efe: un bucle interno avanza i por los que empiezan antes de lo cubierto y guarda el fin más lejano; "
           "si no pasa de lo cubierto, es imposible; si pasa, lo cubierto avanza y se cuenta un trabajo.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Los intervalos son semiabiertos: uno que acaba en cinco y otro que empieza en cinco no dejan hueco. "
           "El índice i nunca retrocede, así que cada trabajo se mira una vez. "
           "Puede no haber ningún trabajo. "
           "Y el coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: se ordena por comienzo y, desde lo cubierto, se elige siempre el que llega más lejos sin dejar hueco. Si ninguno avanza, es imposible.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/09-2", "../09-2_el_alienigena_infiltrado.mp4", "09-2")
