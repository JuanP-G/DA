"""Vídeo EJ 08-1 · Agujeros en la manguera (animado)."""
import sys
from vidlib import C, W, H, font, code_lines, find_line
from anim import Escena, build, preview, ease, lerp, mix

CPP = "../../8-Algoritmos voraces/EJ_08-1/EJ_08-1.cpp"
TEMA = "Tema 8 · Algoritmos voraces"
HOLES = [3, 8, 8, 9, 20, 45, 55, 90]
L = 10
HY = 380                    # altura de la manguera

HOSE, HOSE_D, HOSE_L = (58, 168, 92), (28, 96, 52), (120, 214, 140)
PATCH, PATCH_D = (226, 182, 116), (150, 108, 58)
WATER = (120, 200, 255)


def bg_at(y):
    return mix(C["top"], C["bot"], y / H)


# ------------------------------------------------------------------ piezas
SEG = [(-1, 31), (40, 60), (86, 102)]      # tramos de la manguera que se dibujan (el resto se corta)
GAP = 60


def X(p, a=None, b=None, x0=60, x1=1180):
    """Posición en pantalla. Sin a, b: escala a trozos (tramos SEG con cortes entre ellos)."""
    if a is not None:
        return x0 + (p - a) * (x1 - x0) / (b - a)
    total = sum(s1 - s0 for s0, s1 in SEG)
    u = (x1 - x0 - GAP * (len(SEG) - 1)) / total
    x = x0
    for k, (s0, s1) in enumerate(SEG):
        if p <= s1 or k == len(SEG) - 1:
            return x + (max(p, s0) - s0) * u if p >= s0 or k == 0 else x - GAP / 2
        x += (s1 - s0) * u + GAP
    return x


def cortes():
    """Centros de los cortes entre tramos."""
    return [(X(SEG[k][1]) + X(SEG[k + 1][0])) / 2 for k in range(len(SEG) - 1)]


def suelo(f, y=HY + 170):
    f.d.rectangle((0, y, W, H), fill=(30, 52, 44))
    f.d.line((0, y, W, y), fill=(52, 86, 66), width=3)


def manguera(f, x0=30, x1=1240, y=HY, r=24, con_cortes=False):
    d = f.d
    d.rounded_rectangle((x0, y - r, x1, y + r), r, fill=HOSE, outline=HOSE_D, width=3)
    d.line((x0 + r, y - r + 8, x1 - r, y - r + 8), fill=HOSE_L, width=5)
    d.rounded_rectangle((x1 - 6, y - 15, x1 + 36, y + 15), 6, fill=(170, 176, 190), outline=(90, 96, 110), width=2)
    if con_cortes:
        for xc in cortes():
            col = bg_at(y)
            d.rectangle((xc - 10, y - r - 4, xc + 10, y + r + 4), fill=col)
            for dx in (-10, 10):
                d.line((xc + dx - 5, y - r - 6, xc + dx + 5, y + r + 6), fill=C["muted"], width=3)


def gotas(f, x, y=HY, fase=0.0, n=3, caida=150, charco=True):
    for k in range(n):
        u = ((f.t * 1.1 + fase + k / n) % 1.0)
        yy = y + 22 + u * caida
        r = 5
        f.d.ellipse((x - r, yy - r * 1.5, x + r, yy + r), fill=WATER)
    if charco:
        yc = y + 22 + caida + 6
        w = 16 + 6 * (1 + __import__("math").sin(f.t * 3 + fase)) / 2
        f.d.ellipse((x - w, yc - 5, x + w, yc + 5), fill=(70, 140, 200))


def agujero(f, x, tapado=False, fase=0.0, y=HY, doble=False):
    ys = [y - 8, y + 8] if doble else [y]
    for yy in ys:
        f.d.ellipse((x - 8, yy - 7, x + 8, yy + 7), fill=(18, 34, 26), outline=HOSE_D, width=2)
    if not tapado:
        gotas(f, x, y, fase + x * 0.013, n=4 if doble else 3)


def parche(f, xa, xb, y=HY, caida=1.0, col=PATCH, borde=PATCH_D, regla=None, discontinuo=False):
    off = lerp(-160, 0, ease(caida))
    y0, y1 = y - 33 + off, y + 33 + off
    if discontinuo:
        for xx in range(int(xa), int(xb), 14):
            f.d.line((xx, y0, min(xx + 8, xb), y0), fill=borde, width=3)
            f.d.line((xx, y1, min(xx + 8, xb), y1), fill=borde, width=3)
        f.d.line((xa, y0, xa, y1), fill=borde, width=3)
        f.d.line((xb, y0, xb, y1), fill=borde, width=3)
        return
    f.d.rounded_rectangle((xa, y0, xb, y1), 6, fill=col, outline=borde, width=3)
    for xx in range(int(xa) + 8, int(xb) - 6, 12):
        f.d.line((xx, y0 + 6, xx + 6, y0 + 6), fill=borde, width=2)
        f.d.line((xx, y1 - 6, xx + 6, y1 - 6), fill=borde, width=2)
    if regla:
        yr = y0 - 72
        f.d.line((xa, yr, xb, yr), fill=C["gold"], width=2)
        f.d.line((xa, yr - 7, xa, yr + 7), fill=C["gold"], width=2)
        f.d.line((xb, yr - 7, xb, yr + 7), fill=C["gold"], width=2)
        f.d.text(((xa + xb) / 2, yr - 6), regla, font=font(20, True), fill=C["gold"], anchor="ms")


def contador(f, n, x=1120, y=100, aparece=1.0):
    if aparece <= 0:
        return
    col = mix(C["panel"], PATCH, aparece)
    f.d.rounded_rectangle((x - 70, y - 40, x + 70, y + 40), 14, fill=C["panel"], outline=C["border"], width=2)
    f.d.rounded_rectangle((x - 58, y - 14, x - 18, y + 14), 4, fill=col, outline=PATCH_D, width=2)
    f.d.text((x + 22, y), str(n), font=font(42, True), fill=mix(C["panel"], C["text"], aparece), anchor="mm")


def flecha(f, x, y=HY - 70, col="gold"):
    c = C[col]
    bob = 6 * (1 + __import__("math").sin(f.t * 6)) / 2
    f.d.polygon([(x, y + 24 + bob), (x - 13, y + bob), (x + 13, y + bob)], fill=c)
    f.d.rectangle((x - 4, y - 22 + bob, x + 4, y + bob), fill=c)


def ejes(f, nums, y=HY - 62, resalta=()):
    vals = sorted(set(nums))
    for i, p in enumerate(vals):
        x = X(p)
        if i + 1 < len(vals) and X(vals[i + 1]) - x < 30:
            x -= 9
        elif i > 0 and x - X(vals[i - 1]) < 30:
            x += 9
        f.d.text((x, y), str(p), font=font(24, True), fill=C["gold"] if p in resalta else C["muted"], anchor="ms")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    f.text((W / 2, 200), "EJ 08-1", size=26, color="gold", bold=True, anchor="mm")
    f.text((W / 2, 260), "Agujeros en la manguera", size=58, bold=True, anchor="mm")
    f.text((W / 2, 318), TEMA, size=22, color="muted", anchor="mm")
    manguera(f, y=500)
    for k, p in enumerate([10, 26, 30, 52, 70, 88]):
        agujero(f, X(p, 0, 100), y=500, fase=k * 0.3, tapado=f.t > 1.5 + k * 0.5 and f.t > f.T - 2.5)


def e_metafora(f):
    suelo(f)
    manguera(f, con_cortes=True)
    t_ag = [f.c(0) + 0.4 + 0.35 * k for k in range(len(HOLES))]
    for k, p in enumerate(HOLES):
        if f.t >= t_ag[k]:
            tap = f.t > f.c(2) + 1.0 and p <= 9
            if k != 2:
                agujero(f, X(p), tapado=tap, fase=k * 0.27, doble=(p == 8 and f.t >= t_ag[2]))
    if f.t >= f.c(1):
        caida = f.p(f.c(2), 1.0) if f.t >= f.c(2) else 0.0
        parche(f, X(3), X(3 + L), caida=caida, regla="L")
    contador(f, "?", aparece=f.p(f.c(3), 0.5))


def e_entrada(f):
    suelo(f)
    manguera(f, con_cortes=True)
    t0 = f.c(1)
    for k, p in enumerate(HOLES):
        tk = t0 + 0.45 * k
        if f.t >= tk and k != 2:
            agujero(f, X(p), fase=k * 0.27, doble=(p == 8 and f.t >= t0 + 0.45 * 2))
    vis = [p for k, p in enumerate(HOLES) if f.t >= t0 + 0.45 * k]
    ejes(f, vis, resalta=(8,) if f.t >= f.c(-1) else ())
    if f.t >= f.c(0):
        a = f.p(f.c(0), 0.5)
        f.d.rounded_rectangle((60, 100, 230, 156), 14, fill=C["panel"], outline=mix(C["panel"], C["gold"], a), width=2)
        parche(f, 78, 78 + X(L) - X(0), y=128, caida=1.0)
        f.d.text((200, 128), "10", font=font(26, True), fill=mix(C["panel"], C["gold"], a), anchor="mm")
    if f.t >= f.c(-1):
        x = X(8)
        f.d.ellipse((x - 26, HY - 26, x + 26, HY + 26), outline=C["gold"], width=3)


def _cubiertos(parches):
    return [p for p in HOLES if any(a <= p <= a + L for a in parches)]


def e_ingenua(f):
    suelo(f)
    manguera(f, con_cortes=True)
    starts = [0, 10, 40, 50, 90]
    t_p = [f.c(1) + 0.7 * k for k in range(len(starts))]
    caidos = [a for a, tk in zip(starts, t_p) if f.t >= tk + 0.7]
    for k, p in enumerate(HOLES):
        if k == 2:
            continue
        agujero(f, X(p), tapado=p in _cubiertos(caidos), fase=k * 0.27, doble=(p == 8))
    ejes(f, HOLES, resalta=(45, 55) if f.t >= f.c(2) else ())
    for a in range(0, 101, 10):
        if any(s0 <= a <= s1 for s0, s1 in SEG):
            f.d.line((X(a), HY - 44, X(a), HY - 32), fill=C["dim"], width=2)
    n = 0
    for a, tk in zip(starts, t_p):
        if f.t >= tk:
            parche(f, X(a), X(a + L), caida=f.p(tk, 0.7), col=(196, 160, 210), borde=(120, 80, 150))
            n += 1
    contador(f, n, aparece=f.p(f.c(1), 0.4))
    if f.t >= f.c(2):
        u = f.p(f.c(2), 0.6)
        x = X(50)
        f.d.line((x, HY - 120, x, HY + 120), fill=mix(C["panel"], C["red"], u), width=4)
        f.d.text((x, HY - 130), "✂", font=font(34, True), fill=mix(C["panel"], C["red"], u), anchor="ms")


GREEDY = [3, 20, 45, 90]


def e_voraz(f):
    suelo(f)
    manguera(f, con_cortes=True)
    # momentos: aterrizaje de cada parche
    t_land = [f.c(1) + 0.4, f.c(2) + 2.2, f.c(3) + 0.6, f.c(4) + 0.4]
    t_arrow = [f.c(0) + 0.3, f.c(2) + 1.0, f.c(3), f.c(4)]
    caidos = [a for a, tk in zip(GREEDY, t_land) if f.t >= tk + 0.8]
    for k, p in enumerate(HOLES):
        if k == 2:
            continue
        agujero(f, X(p), tapado=p in _cubiertos(caidos), fase=k * 0.27, doble=(p == 8))
    ejes(f, HOLES, resalta=(55,) if f.t >= f.c(3) + 1.6 else ())
    n = 0
    for a, tk in zip(GREEDY, t_land):
        if f.t >= tk:
            parche(f, X(a), X(a + L), caida=f.p(tk, 0.8), regla=str(a + L) if f.t < tk + 2.4 else None)
            n += 1
    # flecha al primer agujero sin tapar
    cur = None
    for a, ta, tl in zip(GREEDY, t_arrow, t_land):
        if ta <= f.t < tl + 0.8:
            cur = a
    if cur is not None:
        flecha(f, X(cur), y=HY - 190)
    if f.t >= f.c(3) + 1.6 and f.t < f.c(4):
        x = X(55)
        f.d.ellipse((x - 24, HY - 24, x + 24, HY + 24), outline=C["green"], width=4)
    contador(f, n, aparece=f.p(f.c(0), 0.4))


def e_optimo(f):
    a, b = -6, 26
    Xz = lambda p: X(p, a, b)
    suelo(f)
    manguera(f)
    hz = [3, 8, 9, 20]
    tslide = f.c(1) + 0.6
    u = f.p(tslide, 1.6)
    start = lerp(-5, 3, u)
    cov = [p for p in hz if start <= p <= start + L]
    for k, p in enumerate(hz):
        agujero(f, Xz(p), tapado=(p in cov and f.t >= f.c(0) + 0.8), fase=k * 0.3, doble=(p == 8))
    for p in [3, 8, 9, 20]:
        x = Xz(p)
        f.d.text((x, HY - 62), str(p), font=font(24, True), fill=C["muted"], anchor="ms")
    if f.t >= f.c(0):
        parche(f, Xz(start), Xz(start + L), caida=f.p(f.c(0), 0.7), col=(196, 160, 210), borde=(120, 80, 150))
        # la regla: hasta dónde llega
        yr = HY - 110
        f.d.line((Xz(start + L), yr - 30, Xz(start + L), yr + 70), fill=C["gold"], width=3)
        f.d.text((Xz(start + L), yr - 36), f"{start + L:.0f}", font=font(20, True), fill=C["gold"], anchor="ms")
    if f.t >= f.c(1) and u < 1:
        f.d.text((Xz(start + L / 2), HY - 170), "→", font=font(44, True), fill=C["gold"], anchor="mm")
    if f.t >= f.c(2):
        v = f.p(f.c(2), 0.6)
        f.d.rectangle((Xz(-6), HY - 34, Xz(2.5), HY + 34), outline=mix(C["panel"], C["green"], v), width=3)
        f.d.text((Xz(-1.8), HY + 70), "nada", font=font(20, True), fill=mix(C["panel"], C["green"], v), anchor="ma")


CODE_A = find_line(CPP, "int parches = 0;")
CODE_B = find_line(CPP, "cout << parches")
CODE = code_lines(CPP, CODE_A, CODE_B + 1, maxc=60)
L_FOR = find_line(CPP, "for (int p : pos)")
L_IF = find_line(CPP, "if (p > finParche)")
L_INC = find_line(CPP, "++parches;")
L_FIN = find_line(CPP, "finParche = (long long)p + L;")
L_OUT = CODE_B

# traza: (p, ¿parche nuevo?, fin, parches)
TRAZA = []
_fin, _n = -1, 0
for _p in HOLES:
    nuevo = _p > _fin
    if nuevo:
        _n += 1
        _fin = _p + L
    TRAZA.append((_p, nuevo, _fin, _n))


def e_codigo(f):
    t0, t1 = f.c(1), f.T - 1.2
    paso = (t1 - t0) / len(TRAZA)
    k = int((f.t - t0) // paso) if f.t >= t0 else -1
    k = min(k, len(TRAZA) - 1)
    fase = ((f.t - t0) % paso) / paso if 0 <= k else 0
    hl = set()
    if k < 0:
        hl = {CODE_A, CODE_A + 1}
    else:
        p, nuevo, fin, n = TRAZA[k]
        hl = {L_FOR} if fase < 0.3 else ({L_IF} if fase < 0.55 or not nuevo else {L_INC, L_FIN})
        if f.t >= t1:
            hl = {L_OUT}
    f.code(24, 84, 640, 380, CODE, hl=hl, title="resuelveCaso()", size=24)
    # manguera pequeña a la derecha
    xa, xb, y = 700, 1250, 190
    Xs = lambda q: xa + (q + 4) * (xb - xa) / 108
    f.d.rounded_rectangle((xa - 10, y - 12, xb + 4, y + 12), 12, fill=HOSE, outline=HOSE_D, width=2)
    puestos = [tr for i, tr in enumerate(TRAZA) if tr[1] and (i < k or (i == k and fase >= 0.55))]
    for (pp, _, fin, _) in puestos:
        f.d.rounded_rectangle((Xs(pp), y - 18, Xs(pp + L), y + 18), 4, fill=PATCH, outline=PATCH_D, width=2)
    for i, q in enumerate(HOLES):
        tap = any(pp <= q <= pp + L for (pp, _, _, _) in puestos)
        xx = Xs(q) + (5 if i == 2 else -5 if i == 1 else 0)
        f.d.ellipse((xx - 5, y - 4, xx + 5, y + 4), fill=(18, 34, 26))
        if not tap:
            gotas(f, xx, y - 6, i * 0.3, n=2, caida=55, charco=False)
    if 0 <= k:
        p = TRAZA[k][0]
        xx = Xs(p)
        f.d.polygon([(xx, y - 22), (xx - 9, y - 38), (xx + 9, y - 38)], fill=C["gold"])
        f.d.text((xx, y - 44), "p", font=font(18, True, True), fill=C["gold"], anchor="ms")
    # variables
    f.box(690, 300, 566, 96)
    if k >= 0:
        p, nuevo, fin, n = TRAZA[k]
        ver = fase >= 0.55
        pv = TRAZA[k - 1] if k > 0 else (None, None, -1, 0)
        fin_v, n_v = (fin, n) if ver else (pv[2], pv[3])
    else:
        p, fin_v, n_v = "–", -1, 0
    for i, (nom, val) in enumerate((("p", p), ("finParche", fin_v), ("parches", n_v))):
        x = 712 + i * 180
        f.d.text((x, 318), nom, font=font(18, False, True), fill=C["muted"])
        f.d.text((x, 344), str(val), font=font(32, True, True), fill=C["gold"] if nom != "p" else C["text"])
    # condición en grande
    if 0 <= k and 0.3 <= fase:
        p, nuevo, fin, n = TRAZA[k]
        prev_fin = TRAZA[k - 1][2] if k > 0 else -1
        s = f"{p} > {prev_fin}"
        col = C["green"] if nuevo else C["red"]
        f.d.text((972, 480), s, font=font(40, True, True), fill=col, anchor="mm")
        f.d.text((972, 536), "parche nuevo" if nuevo else "ya tapado", font=font(24, True), fill=col, anchor="mm")


def e_detalles(f):
    # izquierda: agujeros repetidos
    f.box(40, 110, 580, 380)
    f.box(660, 110, 580, 380)
    y = 300
    for (xa, xb) in ((70, 590), (690, 1210)):
        f.d.rounded_rectangle((xa, y - 16, xb, y + 16), 16, fill=HOSE, outline=HOSE_D, width=3)
    u = f.p(f.c(0) + 1.2, 0.8)
    # dos agujeros en la misma posición
    x = 330
    for dx in (-8, 8):
        f.d.ellipse((x + dx - 7, y - 6, x + dx + 7, y + 6), fill=(18, 34, 26))
        if u < 1:
            gotas(f, x + dx, y, dx * 0.02)
    if f.t >= f.c(0) + 1.2:
        parche(f, x - 60, x + 160, y=y, caida=u)
    f.d.text((x, y - 120), "×2", font=font(30, True), fill=C["gold"], anchor="ma")
    # derecha: agujero en el borde
    v = f.p(f.c(1) + 0.8, 0.8)
    xa, xb = 760, 1100
    for q, xx in ((45, xa), (55, xb)):
        f.d.ellipse((xx - 7, y - 6, xx + 7, y + 6), fill=(18, 34, 26))
        if v < 1:
            gotas(f, xx, y, q * 0.01)
        f.d.text((xx, y + 60), str(q), font=font(22, True), fill=C["muted"], anchor="ma")
    if f.t >= f.c(1) + 0.8:
        parche(f, xa - 8, xb, y=y, caida=v, regla="45 + 10 = 55")
    if f.t >= f.c(2):
        w = f.p(f.c(2), 0.5)
        f.d.ellipse((xb - 26, y - 26, xb + 26, y + 26), outline=mix(C["panel"], C["green"], w), width=4)
        f.d.text((950, 420), "p > finParche", font=font(30, True, True), fill=mix(C["panel"], C["gold"], w), anchor="mm")
    if f.t >= f.c(3):
        w = f.p(f.c(3), 0.5)
        f.d.text((W / 2, 560), "O(N)", font=font(54, True), fill=mix(C["bot"], C["gold"], w), anchor="mm")


def e_cierre(f):
    f.text((W / 2, 90), "Agujeros en la manguera", size=40, bold=True, anchor="mm")
    items = [
        ("primer agujero sin tapar  →  parche que empieza en él", 0),
        ("p > finParche  ⇒  parche nuevo, finParche = p + L", 1),
        ("una pasada: O(N)", 2),
    ]
    for txt, k in items:
        if f.t >= f.c(k):
            u = f.p(f.c(k), 0.5)
            y = 210 + 120 * k
            x = lerp(-200, 120, u)
            f.d.rounded_rectangle((x, y - 18, x + 60, y + 18), 5, fill=PATCH, outline=PATCH_D, width=2)
            f.d.text((x + 90, y), txt, font=font(28, True), fill=mix(C["bot"], C["text"], u), anchor="lm")
    manguera(f, y=640, x0=80, x1=1200)
    for k, p in enumerate([10, 40, 70]):
        parche(f, X(p, 0, 100) - 30, X(p, 0, 100) + 70, y=640, caida=1.0)


ESC = [
    Escena("Agujeros en la manguera. Es el primer problema de algoritmos voraces: en cada paso se toma la decisión que parece mejor en ese momento, y nunca se vuelve atrás.",
           e_portada, titulo="Portada"),
    Escena("Susana tiene una manguera con agujeros por los que se escapa el agua. "
           "Para arreglarla compra parches de una longitud fija, ele. "
           "Un parche tapa todos los agujeros que quedan debajo de él, y los parches se pueden solapar. "
           "¿Cuántos parches necesita como mínimo?", e_metafora, titulo="El problema"),
    Escena("Usaremos el tercer ejemplo. Los parches miden diez. "
           "Los agujeros están en las posiciones 3, 8, 8, 9, 20, 45, 55 y 90, ya ordenados de izquierda a derecha. "
           "Fíjate en que en la posición 8 hay dos agujeros.", e_entrada, titulo="El ejemplo", extra=1.0),
    Escena("Una idea ingenua: poner los parches seguidos desde el principio de la manguera. "
           "Así, colocando solo los que tapan algún agujero, salen cinco parches. "
           "Pero mira el 45 y el 55: están a diez de distancia y caben en un solo parche, y aun así gastan dos, porque el corte cae justo entre ellos.",
           e_ingenua, titulo="Una idea que falla", extra=1.0),
    Escena("La idea voraz: mira el primer agujero que sigue sin tapar. "
           "Algún parche tiene que taparlo, y lo mejor es que empiece justo en él, porque así llega lo más lejos posible: hasta el 13. "
           "Tapa el 3, los dos 8 y el 9. El primer agujero que queda fuera es el 20, así que el segundo parche empieza en el 20. "
           "El siguiente sin tapar es el 45. Su parche llega hasta el 55, y lo tapa justo en el borde. "
           "Y el 90 necesita el cuarto. Cuatro parches, uno menos que antes.", e_voraz, titulo="La idea voraz", extra=1.2),
    Escena("¿Seguro que no se puede con menos? Toma cualquier solución. Algún parche suyo tapa el primer agujero, el 3, así que empieza en el 3 o antes. "
           "Si lo deslizamos hasta que empiece justo en el 3, sigue tapando el 3, y a la derecha tapa lo mismo que antes o más. "
           "A la izquierda del 3 no hay nada que tapar, así que no se pierde nada. "
           "Repitiendo esto parche a parche, cualquier solución se convierte en la voraz sin gastar ni un parche más.",
           e_optimo, titulo="Por qué es óptimo", extra=1.0),
    Escena("En el código no hay que ordenar nada, porque los agujeros ya vienen en orden. "
           "Recorremos las posiciones con una variable, finParche, que dice hasta dónde llega el último parche puesto. "
           "Si el agujero está más allá, ponemos un parche nuevo que empieza en él y llega hasta pe más ele. "
           "Si no, ya está tapado y no hay que hacer nada. "
           "Al terminar la pasada, el contador de parches es la respuesta.", e_codigo, titulo="El código", extra=3.0),
    Escena("Tres detalles. Si hay varios agujeros en la misma posición, el mismo parche los tapa todos y no cuentan dos veces. "
           "Un agujero justo en el borde, como el 55 con el parche que empieza en el 45, ya está tapado. "
           "Por eso la condición para poner un parche nuevo es pe estrictamente mayor que finParche. "
           "Y como se mira cada agujero una sola vez, el coste es lineal.", e_detalles, titulo="Detalles", extra=1.0),
    Escena("Resumiendo: cada parche empieza en el primer agujero que sigue sin tapar. "
           "Con una variable que guarda hasta dónde llega el último, basta mirar si el agujero queda más allá. "
           "Y todo en una sola pasada.", e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        preview(ESC, "preview/08-1", tiempos=(0.3, 0.6, "fin"))
    else:
        print(f"08-1: {build(ESC, '../08-1_agujeros_en_la_manguera.mp4'):.0f}s")
