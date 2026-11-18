"""Vídeo EJ 09-4 · El telesilla (animado)."""
import math
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../9-Algoritmos voraces II/EJ_09-4/EJ_09-4.cpp"
TEMA = "Tema 9 · Algoritmos voraces II"
P = 30
PESOS = [16, 8, 20, 12, 10]
ORD = sorted(PESOS)
XP = [260 + 190 * k for k in range(5)]
YB = 620


def persona(f, x, y, p, u=1.0, c=None, gris=False):
    if u <= 0:
        return
    c = C["dim"] if gris else (c or C["blue"])
    r = 14 + p * 0.5
    f.d.ellipse((x - 14, y - 2 * r - 34, x + 14, y - 2 * r - 6), fill=mix(C["bot"], c, u))
    f.d.rounded_rectangle((x - r, y - 2 * r, x + r, y), 10, fill=mix(C["bot"], mix(C["panel"], c, 0.5), u), outline=mix(C["bot"], c, u), width=3)
    f.d.text((x, y - r), str(p), font=font(20, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def cable(f, u=1.0):
    f.d.line((0, 230, W, 110), fill=mix(C["bot"], (150, 160, 180), u), width=3)


def silla(f, x, u=1.0):
    if u <= 0:
        return
    y = 230 - x * 120 / W
    c = mix(C["bot"], (170, 180, 200), u)
    f.d.line((x, y, x, y + 70), fill=c, width=3)
    f.d.line((x - 60, y + 130, x + 60, y + 130), fill=c, width=6)
    f.d.line((x - 60, y + 70, x + 60, y + 70), fill=c, width=3)
    f.d.line((x - 60, y + 70, x - 60, y + 130), fill=c, width=3)
    f.d.line((x + 60, y + 70, x + 60, y + 130), fill=c, width=3)
    return y + 128


def e_portada(f):
    def dib(f):
        f.d.line((760, 330, 1180, 260), fill=(150, 160, 180), width=3)
        u = f.p(0.3, 0.6)
        x = 960
        f.d.line((x, 297, x, 340), fill=mix(C["bot"], (170, 180, 200), u), width=3)
        f.d.line((x - 50, 390, x + 50, 390), fill=mix(C["bot"], (170, 180, 200), u), width=6)
        f.d.polygon([(760, 520), (900, 380), (1040, 520)], fill=(230, 236, 245))
    portada(f, "EJ 09-4", "El telesilla", TEMA, dib)


def e_problema(f):
    cable(f, aparece(f, f.c(0)))
    ys = silla(f, 640, aparece(f, f.c(0)))
    if f.t >= f.c(0):
        texto(f, (640, 400), f"2 plazas · como mucho P = {P} kg", 24, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, p in enumerate(PESOS):
        persona(f, XP[k], YB, p, aparece(f, f.c(1) + 0.2 * k))
    if f.t >= f.c(2):
        etiqueta(f, (640, 470), "¿mínimo de viajes para subir a todos?", 26, "text", aparece(f, f.c(2)))


def traza():
    ev, i, j = [], 0, len(ORD) - 1
    while i <= j:
        junto = i < j and ORD[i] + ORD[j] <= P
        ev.append((i, j, junto))
        if junto:
            i += 1
        j -= 1
    return ev


EV = traza()


def e_voraz(f):
    cable(f)
    k, fr = paso_idx(f, f.c(1), f.c(4), len(EV))
    subidos = {}
    for q in range(max(0, min(k + (1 if fr > 0.4 else 0), len(EV)))):
        i, j, junto = EV[q]
        subidos[j] = q
        if junto:
            subidos[i] = q
    for q in range(max(0, min(k + (1 if fr > 0.4 else 0), len(EV)))):
        tq = f.c(1) + (q + 0.4) * (f.c(4) - f.c(1)) / len(EV)
        avance = f.lin(tq + 0.6, 6.0)
        xs = lerp(200, 1200, avance) - q * 0
        xs = min(1180, 200 + 330 * (len(EV) - 1 - q) * 0 + lerp(0, 1, avance) * 0 + 240 + 330 * (q))
        ys = silla(f, xs)
        i, j, junto = EV[q]
        quien = [j] + ([i] if junto else [])
        for m, p in enumerate(quien):
            dst = (xs + (30 if m == 0 else -30), ys)
            pos = mueve((XP[p], YB), dst, f.lin(tq, 0.8))
            persona(f, pos[0], pos[1], ORD[p], c=C["green"])
    for p in range(len(ORD)):
        if p not in subidos:
            persona(f, XP[p], YB, ORD[p])
    texto(f, (640, 330), "ordenados por peso", 22, "muted", aparece(f, f.c(0)), anchor="mm") if f.t < f.c(1) else None
    if 0 <= k < len(EV):
        i, j, junto = EV[k]
        for p, s in ((i, "i"), (j, "j")):
            if p not in subidos or fr < 0.4:
                texto(f, (XP[p], YB + 30), s, 22, "gold", 1, mono=True, anchor="mm")
        s = (f"{ORD[j]} + {ORD[i]} = {ORD[i] + ORD[j]} ≤ {P}: suben juntos" if junto else
             (f"{ORD[j]} solo" + (f" ({ORD[j]} + {ORD[i]} > {P})" if i < j else "")))
        etiqueta(f, (640, 450), s, 26, "green" if junto else NARANJA, 1)
    elif k >= len(EV):
        etiqueta(f, (640, 450), f"{len(EV)} viajes", 30, "green", aparece(f, f.c(4)))


def e_porque(f):
    texto(f, (640, 80), "el más pesado tiene que subir en algún viaje", 26, "text", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(0))
    persona(f, 500, 450, 20, u, c=C["red"])
    persona(f, 700, 450, 8, u)
    persona(f, 860, 450, 10, u)
    if f.t >= f.c(1):
        u1 = aparece(f, f.c(1))
        f.d.line((500, 480, 700, 480), fill=mix(C["bot"], C["green"], u1), width=4)
        etiqueta(f, (640, 560), "si cabe con alguien, cabe con el más ligero: que vaya con él", 24, "green", u1)
    if f.t >= f.c(2):
        etiqueta(f, (640, 630), "si no cabe ni con el más ligero, sube solo", 24, NARANJA, aparece(f, f.c(2)))


A_L = find_line(CPP, "sort(peso.begin(), peso.end());")
B_L = find_line(CPP, "cout << viajes")
CODE = codigo(CPP, A_L, B_L, maxc=80)
L_IF = find_line(CPP, "if (i < j && peso[i] + peso[j] <= P) ++i;")
L_J = find_line(CPP, "--j;")


def e_codigo(f):
    hl = {A_L}
    k, fr = paso_idx(f, f.c(1), f.T - 2.5, len(EV))
    if 0 <= k < len(EV):
        hl = {L_IF} if fr < 0.5 else {L_J, L_J + 1}
    elif k >= len(EV):
        hl = {B_L}
    f.code(20, 90, 720, 440, CODE, hl=hl, title="emparejar extremos", size=18)
    x0 = 780
    texto(f, (x0, 130), f"P = {P}", 24, "gold", 1, mono=True)
    vi = 0
    for q in range(max(0, min(k + (1 if fr >= 0.5 else 0), len(EV)))):
        vi += 1
    for p, v in enumerate(ORD):
        cur = 0 <= k < len(EV) and p in EV[k][:2]
        caja(f, x0 + 40 + p * 90, 220, v, c="gold" if cur else "blue", w=74, borde=5 if cur else 2)
    if 0 <= k < len(EV):
        i, j, _ = EV[k]
        texto(f, (x0 + 40 + i * 90, 270), "i", 22, "gold", 1, mono=True, anchor="mm")
        texto(f, (x0 + 40 + j * 90, 295 if i == j else 270), "j", 22, "gold", 1, mono=True, anchor="mm")
    texto(f, (x0, 350), f"viajes = {vi}", 28, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("mientras i <= j: si queda uno solo (i == j), también sube", "text"),
             ("i < j en el if: nadie se sienta dos veces", "text"),
             ("se diferencia del 09-3: aquí el más pesado nunca se descarta, sube solo", "text"),
             ("N ≤ 500.000:  O(N log N) por la ordenación", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "El telesilla", [
        "ordenar por peso",
        "el más pesado sube en cada viaje",
        "si cabe con el más ligero, suben juntos",
        "dos punteros · O(N log N)",
    ])


ESC = [
    Escena("El telesilla. Cuántos viajes hacen falta para subir a todos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Las sillas tienen dos plazas y soportan como mucho pe kilos; aquí, treinta. "
           "Hay una cola de esquiadores, cada uno con su peso. "
           "¿Cuántos viajes hacen falta como mínimo?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Ordenamos por peso y miramos los extremos: el más ligero, con i, y el más pesado, con jota. "
           "El más pesado sube en este viaje. "
           "Si cabe con el más ligero, suben juntos; si no, sube solo. "
           "Cada vuelta es un viaje. Aquí, tres.",
           e_voraz, titulo="Emparejar extremos", extra=2.5),
    Escena("¿Por qué? El más pesado tiene que subir en algún viaje. "
           "Si puede ir con alguien, también puede ir con el más ligero, así que lo emparejamos con él. "
           "Y si ni con el más ligero cabe, no cabe con nadie: sube solo.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, se ordenan los pesos. "
           "Mientras i sea menor o igual que jota: si caben los dos, avanza i; siempre retrocede jota y se cuenta un viaje.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("La condición del bucle es menor o igual, para que suba también el último si se queda solo. "
           "En el if, i menor que jota, para no sentar a la misma persona dos veces. "
           "A diferencia de las pilas, aquí nadie se descarta: el más pesado sube solo. "
           "Y el coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: se ordena, y en cada viaje sube el más pesado, acompañado del más ligero si caben.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/09-4", "../09-4_el_telesilla.mp4", "09-4")
