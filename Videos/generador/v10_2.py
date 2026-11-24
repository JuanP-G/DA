"""Vídeo EJ 10-2 · Construyendo dianas (animado)."""
import math
import sys
from vidlib import C, W, H, font, code_lines, find_line
from anim import Escena, build, preview, ease, lerp, mix

CPP = "../../10-Programacion dinamica/EJ_10-2/EJ_10-2.cpp"
TEMA = "Tema 10 · Programación dinámica"
P = [1, 4, 6]                      # sectores del ejemplo 2
V = 8
INF = None
SECT_COL = {1: (86, 156, 230), 4: (236, 150, 64), 6: (178, 120, 220), 8: (86, 156, 230), 12: (236, 150, 64)}
NOMBRES = ["ninguno", "{1}", "{1,4}", "{1,4,6}"]


def tabla_dp(P, V):
    S = len(P)
    d = [[INF] * (V + 1) for _ in range(S + 1)]
    d[0][0] = 0
    orden = []                     # orden en que se rellenan (i, j) con i >= 1, j >= 1
    for i in range(1, S + 1):
        d[i][0] = 0
        for j in range(1, V + 1):
            d[i][j] = d[i - 1][j]
            p = P[i - 1]
            if p <= j and d[i][j - p] is not INF:
                c = d[i][j - p] + 1
                if d[i][j] is INF or c < d[i][j]:
                    d[i][j] = c
            orden.append((i, j))
    return d, orden


D, ORDEN = tabla_dp(P, V)


def reconstruye(P, V, d):
    pasos, i, j = [], len(P), V
    while j > 0:
        if d[i][j] == d[i - 1][j]:
            pasos.append(("sube", i, j))
            i -= 1
        else:
            pasos.append(("dardo", i, j))
            j -= P[i - 1]
    pasos.append(("fin", i, j))
    return pasos


REC = reconstruye(P, V, D)


# ------------------------------------------------------------------ piezas
def flecha_linea(f, a, b, col, w=4, cab=12):
    d = f.d
    d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - cab * math.cos(ang - 0.45), b[1] - cab * math.sin(ang - 0.45))
    p2 = (b[0] - cab * math.cos(ang + 0.45), b[1] - cab * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=col)


def diana(f, cx, cy, R, sectores, resalta=None, aparece=1.0):
    if aparece <= 0:
        return
    R = R * ease(aparece)
    n = len(sectores)
    f.d.ellipse((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), fill=(26, 30, 38), outline=(70, 76, 90), width=3)
    for k, s in enumerate(sectores):
        a0 = -90 + 360 * k / n
        a1 = a0 + 360 / n
        base = SECT_COL.get(s, C["blue"])
        col = mix(base, (20, 20, 26), 0.35)
        if resalta == s:
            col = mix(base, (255, 255, 255), 0.25)
        f.d.pieslice((cx - R, cy - R, cx + R, cy + R), a0, a1, fill=col, outline=(16, 18, 24), width=3)
        am = math.radians((a0 + a1) / 2)
        f.d.text((cx + math.cos(am) * R * 0.62, cy + math.sin(am) * R * 0.62), str(s), font=font(int(30 * R / 130 + 4), True),
                 fill=(255, 255, 255), anchor="mm")
    f.d.ellipse((cx - R * 0.12, cy - R * 0.12, cx + R * 0.12, cy + R * 0.12), fill=(200, 60, 60), outline=(16, 18, 24), width=2)


def punto_sector(cx, cy, R, sectores, s, k=0):
    n = len(sectores)
    idx = sectores.index(s)
    a = math.radians(-90 + 360 * (idx + 0.5) / n + (k * 9 - 9))
    r = R * (0.42 + 0.16 * (k % 2))
    return cx + math.cos(a) * r, cy + math.sin(a) * r


def dardo(f, x, y, u):
    """Dardo que vuela desde la derecha y se clava en (x, y); u = progreso 0..1."""
    if u <= 0:
        return
    u = ease(u)
    sx, sy = W + 60, y - 220
    px, py = lerp(sx, x, u), lerp(sy, y, u) - math.sin(u * math.pi) * 60
    ang = math.atan2(y - sy, x - sx)
    L = 54
    tx, ty = px - math.cos(ang) * L, py - math.sin(ang) * L
    f.d.line((tx, ty, px, py), fill=(230, 232, 240), width=5)
    f.d.polygon([(px, py), (px - math.cos(ang - 0.3) * 12, py - math.sin(ang - 0.3) * 12),
                 (px - math.cos(ang + 0.3) * 12, py - math.sin(ang + 0.3) * 12)], fill=(200, 205, 215))
    for s in (-1, 1):
        f.d.polygon([(tx, ty), (tx + math.cos(ang) * 14, ty + math.sin(ang) * 14),
                     (tx - math.cos(ang + s * 1.2) * 12, ty - math.sin(ang + s * 1.2) * 12)], fill=C["red"])


def barra_suma(f, x, y, w, dardos_vals, V, progreso, h=34):
    """Barra de 0 a V que se llena con los dardos ya clavados (progreso[k] = 0..1 de cada uno)."""
    f.d.rounded_rectangle((x, y, x + w, y + h), 8, fill=C["panel"], outline=C["border"], width=2)
    acc = 0.0
    for v, u in zip(dardos_vals, progreso):
        if u <= 0:
            break
        a = x + w * acc / V
        acc += v * ease(u)
        b = x + w * acc / V
        f.d.rounded_rectangle((a + 2, y + 3, max(a + 4, b - 2), y + h - 3), 6, fill=SECT_COL.get(v, C["blue"]))
        if u >= 1:
            f.d.text(((a + b) / 2, y + h / 2), str(v), font=font(20, True), fill=(255, 255, 255), anchor="mm")
    f.d.text((x + w + 14, y + h / 2), f"= {sum(v for v, u in zip(dardos_vals, progreso) if u >= 1)}", font=font(24, True),
             fill=C["text"], anchor="lm")


class Tabla:
    def __init__(self, x0, y0, cw=78, ch=62, lw=150, V=V, S=len(P), nombres=NOMBRES):
        self.x0, self.y0, self.cw, self.ch, self.lw, self.V, self.S, self.nombres = x0, y0, cw, ch, lw, V, S, nombres

    def celda(self, i, j):
        x = self.x0 + self.lw + j * self.cw
        y = self.y0 + 46 + i * self.ch
        return x, y, x + self.cw, y + self.ch

    def centro(self, i, j):
        x0, y0, x1, y1 = self.celda(i, j)
        return (x0 + x1) / 2, (y0 + y1) / 2

    def dibuja(self, f, vals, cab=1.0, filas=1.0, marca=None, sombra=None, tam=26):
        d = f.d
        for j in range(self.V + 1):
            x0, _, x1, _ = self.celda(0, j)
            d.text(((x0 + x1) / 2, self.y0 + 22), str(j), font=font(22, True), fill=mix(C["bot"], C["muted"], cab), anchor="mm")
        for i in range(self.S + 1):
            u = max(0.0, min(1.0, filas * (self.S + 1) - i))
            if u <= 0:
                continue
            _, y0, _, y1 = self.celda(i, 0)
            d.text((self.x0 + self.lw - 14, (y0 + y1) / 2), self.nombres[i], font=font(22, True),
                   fill=mix(C["bot"], C["muted"], u), anchor="rm")
            for j in range(self.V + 1):
                x0, yy0, x1, yy1 = self.celda(i, j)
                fondo = C["panel"]
                if sombra and (i, j) in sombra:
                    fondo = mix(C["panel"], sombra[(i, j)], 0.35)
                d.rectangle((x0, yy0, x1, yy1), fill=mix(C["bot"], fondo, u), outline=mix(C["bot"], C["border"], u), width=2)
                v = vals.get((i, j), "")
                if v != "":
                    txt = "∞" if v is INF else str(v)
                    d.text(((x0 + x1) / 2, (yy0 + yy1) / 2), txt, font=font(tam, True),
                           fill=C["dim"] if v is INF else C["text"], anchor="mm")
        if marca:
            for (i, j), col in marca.items():
                x0, y0, x1, y1 = self.celda(i, j)
                d.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), outline=C[col] if isinstance(col, str) else col, width=5)

    def flecha_arriba(self, f, i, j, u=1.0, col=None):
        col = col or (110, 190, 255)
        x0, y0, x1, y1 = self.celda(i, j)
        xa = x0 + self.cw * 0.22
        a = (xa, y0 - self.ch * 0.55)
        b = (xa, lerp(a[1], y0 + self.ch * 0.25, ease(u)))
        if u > 0:
            flecha_linea(f, a, b, col, w=4)

    def flecha_izq(self, f, i, j, p, u=1.0, col=None):
        col = col or (240, 160, 70)
        if j - p < 0:
            return
        xa, ya = self.centro(i, j - p)
        xb, yb = self.centro(i, j)
        y = ya + self.ch * 0.30
        if u > 0:
            flecha_linea(f, (xa, y), (lerp(xa, xb - 16, ease(u)), y), col, w=4)
            if u >= 1:
                f.d.text(((xa + xb) / 2, y - 4), "+1", font=font(18, True), fill=col, anchor="ms")


def valores(hasta=None, base=True):
    """Valores visibles de la tabla: casos base y las casillas de ORDEN hasta 'hasta' (excluida)."""
    vals = {}
    if base:
        for i in range(len(P) + 1):
            vals[(i, 0)] = 0
        for j in range(1, V + 1):
            vals[(0, j)] = INF
    n = len(ORDEN) if hasta is None else hasta
    for (i, j) in ORDEN[:n]:
        vals[(i, j)] = D[i][j]
    return vals


# ------------------------------------------------------------------ escenas
def e_portada(f):
    f.text((420, 250), "EJ 10-2", size=26, color="gold", bold=True, anchor="mm")
    f.text((420, 312), "Construyendo dianas", size=54, bold=True, anchor="mm")
    f.text((420, 368), TEMA, size=22, color="muted", anchor="mm")
    diana(f, 1000, 360, 170, [10, 15, 20, 25, 30], aparece=f.p(0.2, 0.8))
    for k, (s, t0) in enumerate(((25, 1.2), (25, 1.9), (25, 2.6), (25, 3.3))):
        x, y = punto_sector(1000, 360, 170, [10, 15, 20, 25, 30], s, k)
        dardo(f, x, y, f.lin(t0, 0.6))


def e_problema(f):
    cx, cy, R = 900, 330, 160
    diana(f, cx, cy, R, P, aparece=f.p(f.c(0), 0.8),
          resalta=4 if f.c(3) <= f.t else None)
    if f.t >= f.c(1):
        u = f.p(f.c(1), 0.5)
        f.d.rounded_rectangle((90, 150, 330, 270), 18, fill=C["panel"], outline=mix(C["panel"], C["gold"], u), width=3)
        f.d.text((210, 186), "objetivo", font=font(22, True), fill=mix(C["panel"], C["muted"], u), anchor="mm")
        f.d.text((210, 236), str(V), font=font(56, True), fill=mix(C["panel"], C["gold"], u), anchor="mm")
    if f.t >= f.c(2):
        u = f.p(f.c(2), 0.5)
        f.d.text((210, 330), "↻  se puede repetir", font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="mm")
    t3 = f.c(3) + 0.8
    prog = [f.lin(t3, 0.7), f.lin(t3 + 1.0, 0.7)]
    for k, u in enumerate(prog):
        x, y = punto_sector(cx, cy, R, P, 4, k)
        dardo(f, x, y, u)
    if f.t >= f.c(3):
        barra_suma(f, 90, 560, 900, [4, 4], V, prog)


def e_voraz(f):
    # arriba: al más alto (6, 1, 1). abajo: 4, 4
    diana(f, 1110, 330, 120, P)
    t0 = f.c(0) + 0.6
    pa = [f.lin(t0, 0.6), f.lin(f.c(1) + 0.3, 0.6), f.lin(f.c(1) + 1.2, 0.6)]
    for k, (s, u) in enumerate(zip([6, 1, 1], pa)):
        x, y = punto_sector(1110, 330, 120, P, s, k)
        dardo(f, x, y, u if f.t < f.c(2) else 0)
    f.d.text((90, 180), "al más alto", font=font(26, True), fill=C["muted"])
    barra_suma(f, 90, 220, 760, [6, 1, 1], V, pa)
    n1 = sum(1 for u in pa if u >= 1)
    f.d.text((960, 237), "", font=font(20, True))
    if f.t >= f.c(1) + 2.0:
        u = f.p(f.c(1) + 2.0, 0.5)
        f.d.text((90, 290), f"{n1} dardos", font=font(34, True), fill=mix(C["bot"], C["red"], u))
    if f.t >= f.c(2):
        pb = [f.lin(f.c(2) + 0.3, 0.6), f.lin(f.c(2) + 1.0, 0.6)]
        for k, u in enumerate(pb):
            x, y = punto_sector(1110, 330, 120, P, 4, k)
            dardo(f, x, y, u)
        f.d.text((90, 420), "4 + 4", font=font(26, True), fill=C["muted"])
        barra_suma(f, 90, 460, 760, [4, 4], V, pb)
        if f.t >= f.c(2) + 1.8:
            u = f.p(f.c(2) + 1.8, 0.5)
            f.d.text((90, 530), "2 dardos", font=font(34, True), fill=mix(C["bot"], C["green"], u))
    if f.t >= f.c(3):
        u = f.p(f.c(3), 0.6)
        f.d.text((W / 2, 650), "hay que probarlo todo, en orden  →  tabla", font=font(30, True),
                 fill=mix(C["bot"], C["gold"], u), anchor="mm")


TB = Tabla(60, 150)


def e_tabla(f):
    TB.dibuja(f, {}, cab=0, filas=f.p(f.c(0), 2.0) if f.t >= f.c(0) else 0)
    if f.t >= f.c(1):
        TB.dibuja(f, {}, cab=f.p(f.c(1), 0.8), filas=1.0)
    vals = {}
    if f.t >= f.c(3):
        n = int(min(1.0, (f.t - f.c(3)) / 1.6) * (len(P) + 1) + 0.999)
        for i in range(n):
            vals[(i, 0)] = 0
    if f.t >= f.c(4):
        n = int(min(1.0, (f.t - f.c(4)) / 2.0) * V + 0.999)
        for j in range(1, n + 1):
            vals[(0, j)] = INF
    marca = {}
    if f.c(2) <= f.t < f.c(3):
        marca[(2, 8)] = "gold"
        x, y = TB.centro(2, 8)
        f.d.text((x, y), "?", font=font(30, True), fill=C["gold"], anchor="mm")
    if vals or marca:
        TB.dibuja(f, vals, marca=marca)
    diana(f, 1110, 330, 110, P)
    if f.c(2) <= f.t < f.c(3):
        f.d.text((640, 520), "dardos(2, 8) = mínimo de dardos para sumar 8 con {1, 4}", font=font(24, True, True),
                 fill=C["gold"], anchor="mm")


def e_opciones(f):
    i, j, p = 2, 8, 4
    vals = valores(hasta=ORDEN.index((i, j)))
    marca = {(i, j): "gold"}
    sombra = {}
    if f.t >= f.c(1):
        sombra[(i - 1, j)] = (110, 190, 255)
    if f.t >= f.c(2):
        sombra[(i, j - p)] = (240, 160, 70)
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    TB.flecha_arriba(f, i, j, f.p(f.c(1), 0.6) if f.t >= f.c(1) else 0)
    TB.flecha_izq(f, i, j, p, f.p(f.c(2), 0.8) if f.t >= f.c(2) else 0)
    diana(f, 1110, 300, 100, P, resalta=4 if f.t >= f.c(2) else None)
    y = 520
    if f.t >= f.c(1):
        u = f.p(f.c(1), 0.5)
        f.d.text((150, y), "no usar 4:", font=font(26, True), fill=mix(C["bot"], (110, 190, 255), u))
        if f.t >= f.c(4):
            f.d.text((330, y), "8", font=font(30, True, True), fill=C["text"])
    if f.t >= f.c(2):
        u = f.p(f.c(2), 0.5)
        f.d.text((150, y + 50), "usar 4:", font=font(26, True), fill=mix(C["bot"], (240, 160, 70), u))
        if f.t >= f.c(4):
            f.d.text((330, y + 50), "1 + 1 = 2", font=font(30, True, True), fill=C["text"])
    if f.t >= f.c(3):
        u = f.p(f.c(3), 0.5)
        f.d.text((620, y + 25), "→  el menor", font=font(28, True), fill=mix(C["bot"], C["gold"], u))
    if f.t >= f.c(4) + 2.5:
        x, yy = TB.centro(i, j)
        f.d.text((x, yy), "2", font=font(28, True), fill=C["gold"], anchor="mm")


def e_rellenar(f):
    t0, t1 = f.c(0) + 0.5, f.T - 3.0
    paso = (t1 - t0) / len(ORDEN)
    k = int((f.t - t0) / paso) if f.t >= t0 else 0
    k = max(0, min(k, len(ORDEN)))
    vals = valores(hasta=k)
    marca = {}
    if k < len(ORDEN) and f.t >= t0:
        i, j = ORDEN[k]
        marca[(i, j)] = "gold"
        u = ((f.t - t0) % paso) / paso
        TB.dibuja(f, vals, marca=marca)
        TB.flecha_arriba(f, i, j, min(1, u * 2))
        TB.flecha_izq(f, i, j, P[i - 1], min(1, u * 2))
    else:
        if k >= len(ORDEN):
            marca[(len(P), V)] = "green"
        TB.dibuja(f, vals, marca=marca)
    diana(f, 1110, 330, 110, P, resalta=P[ORDEN[k][0] - 1] if k < len(ORDEN) and f.t >= t0 else None)
    if k >= len(ORDEN):
        u = f.p(t1, 0.6)
        f.d.text((640, 540), "dardos(3, 8) = 2", font=font(36, True, True), fill=mix(C["bot"], C["green"], u), anchor="mm")


TBR = Tabla(40, 150, cw=70, ch=58, lw=130)


def e_reconstruye(f):
    vals = valores()
    cues = [f.c(2), f.c(3), f.c(5), f.c(6)]
    pos = (len(P), V)
    hechos = 0
    for k, t in enumerate(cues[:len(REC)]):
        if f.t >= t:
            hechos = k + 1
    marca, sombra = {}, {}
    dardos_tirados = []
    i, j = len(P), V
    for k in range(min(hechos, len(REC))):
        tipo, ii, jj = REC[k]
        if tipo == "sube":
            i -= 1
        elif tipo == "dardo":
            dardos_tirados.append((P[ii - 1], cues[k]))
            j -= P[ii - 1]
    if f.t >= f.c(1) and hechos < len(REC):
        tipo, ii, jj = REC[hechos] if hechos < len(REC) else REC[-1]
        marca[(i, j)] = "gold"
        if f.t >= f.c(1) and tipo != "fin":
            sombra[(i - 1, j)] = (110, 190, 255)
    elif hechos >= len(REC) - 1:
        marca[(i, j)] = "green"
    TBR.dibuja(f, vals, marca=marca, sombra=sombra, tam=24)
    # comparación en curso
    if f.t >= f.c(1) and hechos < len(REC) - 1:
        tipo = REC[hechos][0]
        a, b = D[i][j], D[i - 1][j]
        txt = f"{a} = {b}" if a == b else f"{a} ≠ {b}"
        f.d.text((420, 520), txt, font=font(40, True, True), fill=C["blue"] if a == b else (240, 160, 70), anchor="mm")
        f.d.text((420, 568), "sube: no hace falta" if a == b else "se tiró este sector", font=font(22, True), fill=C["muted"], anchor="mm")
    # recorrido hecho: flechas
    ii, jj = len(P), V
    for k in range(min(hechos, len(REC) - 1)):
        tipo = REC[k][0]
        if tipo == "sube":
            a = TBR.centro(ii, jj)
            b = TBR.centro(ii - 1, jj)
            flecha_linea(f, (a[0] + 18, a[1] - 14), (b[0] + 18, b[1] + 14), (110, 190, 255), w=4)
            ii -= 1
        else:
            a = TBR.centro(ii, jj)
            b = TBR.centro(ii, jj - P[ii - 1])
            flecha_linea(f, (a[0] - 18, a[1] + 16), (b[0] + 18, b[1] + 16), (240, 160, 70), w=4)
            jj -= P[ii - 1]
    cx, cy, R = 1110, 300, 110
    diana(f, cx, cy, R, P)
    for k, (s, t) in enumerate(dardos_tirados):
        x, y = punto_sector(cx, cy, R, P, s, k)
        dardo(f, x, y, f.lin(t + 0.3, 0.6))
    if f.t >= f.c(-1):
        u = f.p(f.c(-1), 0.6)
        f.d.text((1110, 500), "2: 4 4", font=font(44, True, True), fill=mix(C["bot"], C["green"], u), anchor="mm")


C0 = find_line(CPP, "Matriz<EntInf> dardos(S + 1")
C1 = find_line(CPP, "cout << '\\n';", find_line(CPP, "while (j > 0)"))
_raw = [(n, s.split("//")[0].rstrip() if "//" in s and not s.strip().startswith("//") else s) for n, s in code_lines(CPP, C0, C1, maxc=300)]
_ind = min(len(s) - len(s.lstrip()) for _, s in _raw if s.strip())
CODE = [(n, (s[_ind:] if len(s[_ind:]) <= 72 else s[_ind:][:71] + "…")) for n, s in _raw]
L_TAB = C0
L_BASE = find_line(CPP, "dardos[0][0] = 0;")
L_FOR_I = find_line(CPP, "for (int i = 1; i <= S; ++i) {")
L_COL0 = find_line(CPP, "dardos[i][0] = 0;")
L_COPY = find_line(CPP, "dardos[i][j] = dardos[i - 1][j];")
L_IF = find_line(CPP, "if (p[i] <= j)")
L_MIN = find_line(CPP, "dardos[i][j] = min(dardos[i][j], dardos[i][j - p[i]] + 1);")
L_WHILE = find_line(CPP, "while (j > 0)")
L_SUBE = find_line(CPP, "if (dardos[i][j] == dardos[i - 1][j]) --i;")
L_USA = find_line(CPP, "else { cout << ' ' << p[i]; j -= p[i]; }")

TBC = Tabla(770, 120, cw=44, ch=46, lw=86, nombres=["–", "{1}", "{1,4}", "{1,4,6}"])


def e_codigo(f):
    fase_rec = f.t >= f.c(4)
    hl = {L_TAB}
    if f.t >= f.c(1):
        hl = {L_BASE, L_COL0}
    vals = {}
    marca = {}
    if f.c(2) <= f.t < f.c(4):
        t0, t1 = f.c(2), f.c(4) - 0.3
        paso = (t1 - t0) / len(ORDEN)
        k = min(len(ORDEN) - 1, int((f.t - t0) / paso))
        u = ((f.t - t0) % paso) / paso
        vals = valores(hasta=k)
        i, j = ORDEN[k]
        marca[(i, j)] = "gold"
        hl = {L_COPY} if u < 0.5 else ({L_IF, L_MIN} if P[i - 1] <= j else {L_IF})
    elif f.t >= f.c(1) and not fase_rec:
        vals = valores(hasta=0)
    if fase_rec:
        vals = valores()
        t0, t1 = f.c(4) + 0.5, f.T - 1.5
        paso = (t1 - t0) / len(REC)
        k = max(0, min(len(REC) - 1, int((f.t - t0) / paso)))
        i, j = len(P), V
        for q in range(k):
            tipo, ii, jj = REC[q]
            if tipo == "sube":
                i -= 1
            elif tipo == "dardo":
                j -= P[ii - 1]
        tipo = REC[k][0]
        marca[(i, j)] = "green" if tipo == "fin" else "gold"
        hl = {L_WHILE} if tipo == "fin" else ({L_SUBE} if tipo == "sube" else {L_USA})
    f.code(20, 84, 730, 540, CODE, hl=hl, title="tabla y reconstrucción", size=16)
    TBC.dibuja(f, vals, marca=marca, tam=20)
    if fase_rec:
        f.d.text((1010, 420), "i, j = " + f"{i}, {j}", font=font(30, True, True), fill=C["gold"], anchor="mm")


def e_detalles(f):
    # Imposible: 25 con 8 y 12
    f.box(40, 100, 600, 300, "25 con {8, 12}")
    alcanzables = sorted({8 * a + 12 * b for a in range(4) for b in range(3)} - {0})
    u = f.p(f.c(0) + 0.5, 1.5)
    xs = lambda v: 70 + v * 20
    f.d.line((70, 280, xs(28), 280), fill=C["dim"], width=3)
    for v in alcanzables:
        if v <= 28 and u * 28 >= v:
            f.d.ellipse((xs(v) - 8, 272, xs(v) + 8, 288), fill=C["green"])
            f.d.text((xs(v), 300), str(v), font=font(18, True), fill=C["muted"], anchor="ma")
    f.d.text((xs(25), 230), "25 ✗", font=font(26, True), fill=C["red"] if u >= 0.9 else C["bot"], anchor="mm")
    f.d.line((xs(25), 250, xs(25), 290), fill=C["red"] if u >= 0.9 else C["bot"], width=3)
    if f.t >= f.c(0) + 2.0:
        f.d.text((340, 360), "Imposible", font=font(34, True), fill=C["red"], anchor="mm")
    # INF + 1
    f.box(660, 100, 580, 300, "∞ + 1")
    if f.t >= f.c(1):
        v = f.p(f.c(1), 0.6)
        f.d.text((950, 200), "∞ + 1", font=font(34, True, True), fill=mix(C["panel"], C["text"], v), anchor="mm")
        f.d.text((950, 260), "→  sigue siendo ∞", font=font(28, True), fill=mix(C["panel"], C["green"], v), anchor="mm")
        f.d.text((950, 330), "EntInf lo controla", font=font(26, True, True), fill=mix(C["panel"], C["gold"], v), anchor="mm")
    if f.t >= f.c(2):
        v = f.p(f.c(2), 0.6)
        f.d.text((340, 470), "while (cin >> V >> S)", font=font(28, True, True), fill=mix(C["bot"], C["text"], v), anchor="mm")
    if f.t >= f.c(3):
        v = f.p(f.c(3), 0.6)
        f.d.text((950, 470), "O(S · V)", font=font(48, True), fill=mix(C["bot"], C["gold"], v), anchor="mm")


def e_cierre(f):
    f.text((W / 2, 80), "Construyendo dianas", size=40, bold=True, anchor="mm")
    items = [
        "dardos(i, j) = mín. dardos para sumar j con los sectores 1..i",
        "no usar i  (arriba)   o   usar i otra vez  (misma fila, j − p[i]) + 1",
        "reconstruir: igual que arriba → sube;  distinto → dardo p[i]",
        "O(S · V)",
    ]
    for k, txt in enumerate(items):
        if f.t >= f.c(min(k, 3)):
            u = f.p(f.c(min(k, 3)) + 0.2 * k, 0.5)
            y = 190 + 105 * k
            x = lerp(-200, 90, u)
            col = list(SECT_COL.values())[k % 3]
            f.d.ellipse((x, y - 16, x + 32, y + 16), fill=col)
            f.d.text((x + 56, y), txt, font=font(26, True), fill=mix(C["bot"], C["text"], u), anchor="lm")


ESC = [
    Escena("Construyendo dianas. Un problema de programación dinámica: el problema del cambio de monedas, pero tirando dardos.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos una diana dividida en sectores, cada uno con su puntuación: aquí, 1, 4 y 6. "
           "Queremos sumar exactamente una cantidad, por ejemplo 8, tirando el menor número de dardos posible. "
           "Cada sector se puede repetir todas las veces que haga falta. "
           "Aquí bastan dos dardos al 4.", e_problema, titulo="El problema", extra=1.5),
    Escena("¿Y si tiramos siempre al sector más alto que quepa? Primero el 6. "
           "Quedan 2, así que un 1 y otro 1: tres dardos. "
           "Pero dos cuatros suman 8 con solo dos. "
           "Elegir lo más grande no sirve: hay que probar todas las combinaciones de forma ordenada, y para eso está la tabla.",
           e_voraz, titulo="Lo más grande no sirve", extra=1.0),
    Escena("Cada fila dice qué sectores podemos usar: la fila cero ninguno, la uno solo el 1, la dos el 1 y el 4, y la tres todos. "
           "Cada columna es la suma que queremos conseguir, de 0 a 8. "
           "En cada casilla guardamos el mínimo número de dardos: por ejemplo, esta es sumar 8 usando el 1 y el 4. "
           "Sumar cero no necesita ningún dardo, así que la primera columna es todo ceros. "
           "Y sin ningún sector no se puede sumar nada más: la fila cero es infinito.", e_tabla, titulo="La tabla", extra=1.2),
    Escena("Para rellenar una casilla hay dos opciones. "
           "No usar el sector de esa fila: entonces vale lo mismo que la casilla de arriba. "
           "O tirar un dardo más a ese sector: uno, más lo que cuesta la suma que queda, que está p columnas a la izquierda y en la misma fila, porque el sector se puede repetir. "
           "Nos quedamos con la menor. "
           "Para el 4 y la suma 8: arriba hay un 8, y a la izquierda, en la columna 4, hay un 1, más un dardo, 2. Gana el 2.",
           e_opciones, titulo="Las dos opciones", extra=1.5),
    Escena("Así se rellena toda la tabla, fila a fila y de izquierda a derecha. "
           "Con solo el 1, cada suma necesita tantos dardos como vale. "
           "Al añadir el 4, a partir de la columna 4 se empieza a ahorrar. "
           "Y con el 6, la suma 6 sale de un solo dardo. "
           "La respuesta está en la última casilla: dos dardos.", e_rellenar, titulo="Rellenar la tabla", extra=4.0),
    Escena("Ya sabemos cuántos dardos, pero no cuáles. "
           "Para saberlo, volvemos hacia atrás desde la respuesta, preguntando de dónde salió cada número. "
           "En la fila del 6, la suma 8 vale 2, igual que la de arriba: el 6 no hacía falta, así que subimos. "
           "En la fila del 4 vale 2, pero arriba hay un 8. "
           "Este 2 solo pudo salir de tirar un 4: lo apuntamos y nos movemos 4 columnas a la izquierda. "
           "En la columna 4 vale 1 y arriba hay un 4: otro dardo al 4, y llegamos a la columna 0. "
           "Hemos terminado: dos dardos, un 4 y otro 4.", e_reconstruye, titulo="Reconstruir los dardos", extra=1.5),
    Escena("En el código, la tabla es una matriz, de la cabecera Matriz, de enteros con infinito, con ese más uno filas por la fila de ningún sector, y todo empieza a infinito. "
           "La casilla de suma cero vale cero en todas las filas. "
           "El doble bucle rellena fila a fila: primero copia la de arriba, y si el sector cabe, prueba con un dardo más. "
           "Por eso las puntuaciones se guardan desde la posición 1: el sector de la fila i es p de i. "
           "Para reconstruir, un bucle mientras quede suma: si la casilla es igual que la de arriba, sube; si no, escribe el sector y resta su puntuación.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Detalles. Si la última casilla sigue en infinito, como en el tercer ejemplo, donde con 8 y 12 no se puede sumar 25, se escribe imposible. "
           "Los dardos son enteros con infinito, de la cabecera EnterosInf: infinito más uno sigue siendo infinito, y no se desborda. "
           "No hay número de casos: se lee hasta el final del fichero. "
           "Y el coste es S por V, en tiempo y en memoria.", e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: la tabla guarda el mínimo de dardos para cada suma con cada grupo de sectores. "
           "Cada casilla elige entre no usar el sector, mirando arriba, o usarlo otra vez, mirando a la izquierda en su fila. "
           "Para saber qué dardos, se vuelve hacia atrás: igual que arriba, se sube; distinto, se tiró ese sector. "
           "Todo en S por V.", e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = None
        if "--solo" in sys.argv:
            solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")}
        preview(ESC, "preview/10-2", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-2: {build(ESC, '../10-2_construyendo_dianas.mp4'):.0f}s")
