"""Vídeo EJ 08-3 · Comienza la temporada (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview

CPP = "../../8-Algoritmos voraces/EJ_08-3/EJ_08-3.cpp"
TEMA = "Tema 8 · Algoritmos voraces"
JUG = [3, 3, 4, 5, 5]
EQ = [3, 4, 4, 6, 7]
TALLAS = [3, 4, 5, 6, 7]
XT = {t: 240 + 190 * k for k, t in enumerate(TALLAS)}
YJ, YE = 300, 540          # base de las pilas


def camiseta(f, x, y, t, u=1.0, c=None, gris=False):
    if u <= 0:
        return
    c = C["dim"] if gris else (c or C["blue"])
    pts = [(x - 16, y - 24), (x - 34, y - 12), (x - 26, y + 2), (x - 18, y - 4), (x - 18, y + 24),
           (x + 18, y + 24), (x + 18, y - 4), (x + 26, y + 2), (x + 34, y - 12), (x + 16, y - 24), (x + 6, y - 18), (x - 6, y - 18)]
    f.d.polygon(pts, fill=mix(C["bot"], mix(C["panel"], c, 0.35), u), outline=mix(C["bot"], c, u))
    f.d.text((x, y + 4), str(t), font=font(18, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def jugador(f, x, y, t, u=1.0, c=None):
    if u <= 0:
        return
    c = c or C["gold"]
    f.d.ellipse((x - 14, y - 44, x + 14, y - 16), fill=mix(C["bot"], c, u))
    f.d.rounded_rectangle((x - 20, y - 12, x + 20, y + 24), 8, fill=mix(C["bot"], mix(C["panel"], c, 0.5), u), outline=mix(C["bot"], c, u), width=2)
    f.d.text((x, y + 6), str(t), font=font(16, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def simula():
    """Eventos por jugador, en orden: (talla, k-ésimo de su talla, 'suya'|'mas'|'compra', índice de la camiseta usada)."""
    quedan = {t: [k for k, e in enumerate(EQ) if e == t] for t in range(1, 10)}
    ev = []
    for t in TALLAS:
        js = [k for k, j in enumerate(JUG) if j == t]
        for q, jk in enumerate(js):
            if quedan[t]:
                ev.append((t, jk, q, "suya", quedan[t].pop(0)))
            elif quedan[t + 1]:
                ev.append((t, jk, q, "mas", quedan[t + 1].pop(0)))
            else:
                ev.append((t, jk, q, "compra", None))
    return ev


EV = simula()
COMPRAR = sum(1 for e in EV if e[3] == "compra")


def pos_j(jk):
    t = JUG[jk]
    q = [k for k, j in enumerate(JUG) if j == t].index(jk)
    return XT[t] + (q - 0.5 * (JUG.count(t) - 1)) * 54, YJ


def pos_e(ek):
    t = EQ[ek]
    q = [k for k, e in enumerate(EQ) if e == t].index(ek)
    return XT[t] + (q - 0.5 * (EQ.count(t) - 1)) * 76, YE


def ejes(f, u=1.0):
    for t in TALLAS:
        texto(f, (XT[t], 640), f"talla {t}", 22, "muted", u, anchor="mm")
        f.d.line((XT[t] - 80, 610, XT[t] + 80, 610), fill=mix(C["bot"], C["border"], u), width=2)


def e_portada(f):
    def dib(f):
        camiseta(f, 900, 320, 12, u=f.p(0.3, 0.5))
        camiseta(f, 1000, 320, 13, u=f.p(0.5, 0.5))
        jugador(f, 1100, 340, 12, u=f.p(0.7, 0.5))
    portada(f, "EJ 08-3", "Comienza la temporada", TEMA, dib)


def e_problema(f):
    u0 = aparece(f, f.c(0))
    for k in range(len(JUG)):
        x, y = pos_j(k)
        jugador(f, x, y, JUG[k], u0)
    u1 = aparece(f, f.c(1))
    for k in range(len(EQ)):
        x, y = pos_e(k)
        camiseta(f, x, y, EQ[k], u1)
    ejes(f, u1)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        # jugador de talla 3 prueba la de 3 (ok), la de 4 (ok) y una de 2 no existe → dibujo de regla
        texto(f, (640, 90), "su talla  o  una más", 30, "green", u, anchor="mm")
        texto(f, (640, 135), "(más pequeña no sirve)", 22, "red", u, anchor="mm")
        x1, _ = pos_j(0)
        flecha(f, (x1, YJ + 30), (pos_e(0)[0], YE - 34), mix(C["bot"], C["green"], u), w=3)
        flecha(f, (x1 + 10, YJ + 30), (pos_e(1)[0] - 20, YE - 34), mix(C["bot"], C["green"], u), w=3)
    if f.t >= f.c(3):
        texto(f, (640, 690), "¿cuántas equipaciones hay que comprar, como mínimo?", 26, "gold", aparece(f, f.c(3)), anchor="mm")


def e_voraz(f):
    ejes(f)
    k, fr = paso_idx(f, f.c(1), f.c(4), len(EV))
    usadas = {}
    hechos = EV[:max(0, min(k, len(EV)))]
    for q, ev in enumerate(EV):
        if ev[4] is not None:
            usadas[ev[4]] = q
    for ek in range(len(EQ)):
        q = usadas.get(ek)
        x, y = pos_e(ek)
        if q is not None and q <= k and f.t >= f.c(1):
            u = 1.0 if q < k else fr * 2
            jx, jy = pos_j(EV[q][1])
            p = mueve((x, y), (jx, jy + 62), u)
            camiseta(f, p[0], p[1], EQ[ek], c=C["green"] if EV[q][3] == "suya" else NARANJA)
        else:
            camiseta(f, x, y, EQ[ek], gris=f.t >= f.c(4))
    for jk in range(len(JUG)):
        x, y = pos_j(jk)
        ev = [e for e in EV if e[1] == jk][0]
        q = EV.index(ev)
        c = None
        if f.t >= f.c(1) and q < k or (q == k and fr > 0.5):
            c = {"suya": C["green"], "mas": NARANJA, "compra": C["red"]}[ev[3]]
        jugador(f, x, y, JUG[jk], c=c)
        if c == C["red"]:
            caja(f, x, y - 78, "+1 €", c="red", w=70, h=36, tam=18)
    if 0 <= k < len(EV):
        t = EV[k][0]
        f.d.rectangle((XT[t] - 88, 180, XT[t] + 88, 600), outline=C["gold"], width=3)
        s = {"suya": "de su talla", "mas": f"de la talla {t + 1}", "compra": "no queda ninguna: comprar"}[EV[k][3]]
        texto(f, (640, 90), f"talla {t}: {s}", 28, {"suya": "green", "mas": NARANJA, "compra": "red"}[EV[k][3]], 1, anchor="mm")
    elif k < 0:
        texto(f, (640, 90), "de la talla más pequeña a la más grande", 26, "text", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 90), f"comprar = {COMPRAR}", 34, "red", aparece(f, f.c(4)), mono=True, anchor="mm")


def e_porque(f):
    # una camiseta de talla 4: ¿para el de talla 3 o para el de talla 4?
    xa, xb, xc = 380, 640, 900
    u = aparece(f, f.c(0))
    jugador(f, xa, 280, 3, u)
    jugador(f, xb, 280, 4, u)
    camiseta(f, xb, 500, 4, u)
    camiseta(f, xc, 500, 5, u, gris=f.t < f.c(2))
    texto(f, (xa, 200), "solo le sirven 3 y 4", 20, "muted", u, anchor="mm")
    texto(f, (xb, 200), "le sirven 4 y 5", 20, "muted", u, anchor="mm")
    if f.t >= f.c(1):
        p = mueve((xb, 500), (xa, 345), f.lin(f.c(1), 1.0))
        camiseta(f, p[0], p[1], 4, c=NARANJA)
    if f.t >= f.c(2):
        p = mueve((xc, 500), (xb, 345), f.lin(f.c(2), 1.0))
        camiseta(f, p[0], p[1], 5, c=C["green"])
    if f.t >= f.c(3):
        texto(f, (640, 640), "dársela al pequeño nunca empeora", 30, "gold", aparece(f, f.c(3)), anchor="mm")


A = find_line(CPP, "vector<int> jugadores(MAX_TALLA + 2")
B = find_line(CPP, "cout << comprar")
CODE = codigo(CPP, A, B, maxc=72)
L_SU = find_line(CPP, "int deSuTalla =")
L_MA = find_line(CPP, "int deUnaMas =")
L_CO = find_line(CPP, "comprar += faltan;")
L_CU = find_line(CPP, "for (int i = 0; i < N; ++i) { int t; cin >> t; ++jugadores[t]; }")


def e_codigo(f):
    t0, t1 = f.c(1), f.T - 3
    k, fr = paso_idx(f, t0, t1, len(TALLAS))
    hl = {L_CU, L_CU + 1}
    if 0 <= k < len(TALLAS):
        hl = [{L_SU, L_SU + 1}, {L_MA, L_MA + 1, L_MA + 2}, {L_CO}][min(2, int(fr * 3))]
    elif k >= len(TALLAS):
        hl = {B}
    f.code(20, 90, 760, 470, CODE, hl=hl, title="contar y recorrer tallas", size=17)
    # vectores de cuentas
    x0 = 830
    jug = {t: JUG.count(t) for t in range(2, 9)}
    eq = {t: EQ.count(t) for t in range(2, 9)}
    comprar = 0
    for q in range(max(0, min(k + (1 if fr > 0.66 else 0), len(TALLAS)))):
        t = TALLAS[q]
        falt = jug[t]
        s = min(falt, eq[t]); eq[t] -= s; falt -= s
        m = min(falt, eq[t + 1]); eq[t + 1] -= m; falt -= m
        comprar += falt
    texto(f, (x0, 130), "talla", 18, "muted", 1)
    texto(f, (x0, 200), "jug.", 18, "gold", 1)
    texto(f, (x0, 270), "equip.", 18, "blue", 1)
    for q, t in enumerate(TALLAS):
        x = x0 + 100 + q * 64
        texto(f, (x, 140), str(t), 20, "muted", 1, anchor="mm")
        cur = 0 <= k < len(TALLAS) and TALLAS[k] == t
        caja(f, x, 210, jug[t], c="gold", w=54, h=46, tam=22, borde=5 if cur else 2)
        caja(f, x, 280, eq[t], c="blue", w=54, h=46, tam=22, borde=5 if cur else 2)
    texto(f, (x0, 360), f"comprar = {comprar}", 30, "red", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("solo hay 100 tallas: se cuentan en vez de ordenar  →  O(N + M + 100)", "gold"),
             ("el vector tiene hueco para la talla 101 (vale 0): los de talla 100 la miran", "text"),
             ("una equipación más pequeña no sirve a nadie de una talla mayor", "text")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 180 + 110 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Comienza la temporada", [
        "contar jugadores y equipaciones por talla",
        "tallas de menor a mayor: primero la suya",
        "si falta, la de una talla más; si no, comprar",
        "O(N + M + 100) por caso",
    ])


ESC = [
    Escena("Comienza la temporada. Cuántas equipaciones hay que comprar para que jueguen todos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Hay jugadores, cada uno con su talla. "
           "Y hay equipaciones, también con su talla. "
           "Un jugador puede usar una equipación de su talla o de una talla más; las pequeñas no le valen. "
           "Hay que decir el mínimo de equipaciones que comprar.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Vamos de la talla más pequeña a la más grande. "
           "Los jugadores de cada talla usan primero las equipaciones de su talla, que ya no quiere nadie más pequeño. "
           "Si faltan, cogen las de una talla más. "
           "Y los que se quedan sin nada son equipaciones que hay que comprar. "
           "En este ejemplo, hay que comprar una.",
           e_voraz, titulo="La voraz", extra=1.5),
    Escena("¿Por qué darle la camiseta de una talla más al pequeño? "
           "El de talla tres solo puede usar tallas tres o cuatro, así que se la damos a él. "
           "El de talla cuatro todavía puede usar una de cinco. "
           "Dársela al pequeño nunca empeora.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, como solo hay cien tallas, se cuentan jugadores y equipaciones de cada talla en dos vectores. "
           "Después, para cada talla: se usan las de su talla, luego las de la siguiente, que se descuentan, y lo que falte se suma a comprar.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Contar en vez de ordenar deja el coste en ene más eme más cien. "
           "El vector tiene una casilla más, la talla ciento uno, que vale cero, para que los de talla cien no se salgan. "
           "Y recuerda: una equipación más pequeña no le sirve a nadie de talla mayor.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: se cuenta por tallas, se recorren de menor a mayor usando primero la propia talla y después la siguiente, "
           "y lo que falta se compra.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/08-3", "../08-3_comienza_la_temporada.mp4", "08-3")
