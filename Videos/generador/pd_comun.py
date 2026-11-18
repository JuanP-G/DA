"""Piezas comunes de los vídeos animados de programación dinámica (temas 10 y 11)."""
import math
from vidlib import C, W, H, font, code_lines
from anim import ease, lerp, mix

AZUL = (110, 190, 255)        # flecha "no usar" / de arriba
NARANJA = (240, 160, 70)      # flecha "usar" / de la izquierda
VERDE = C["green"]


def flecha(f, a, b, col, w=4, cab=12):
    f.d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - cab * math.cos(ang - 0.45), b[1] - cab * math.sin(ang - 0.45))
    p2 = (b[0] - cab * math.cos(ang + 0.45), b[1] - cab * math.sin(ang + 0.45))
    f.d.polygon([b, p1, p2], fill=col)


def aparece(f, t0, d=0.5):
    """0..1 desde t0 (0 si aún no ha llegado)."""
    return f.p(t0, d) if f.t >= t0 else 0.0


def texto(f, xy, s, size=24, col="text", u=1.0, bold=True, mono=False, anchor="la", fondo=None):
    if u <= 0:
        return
    c = C[col] if isinstance(col, str) else col
    fondo = fondo or C["bot"]
    f.d.text(xy, s, font=font(size, bold, mono), fill=mix(fondo, c, u), anchor=anchor)


class Tabla:
    """Tabla de PD: filas con etiqueta a la izquierda, columnas con cabecera arriba."""

    def __init__(self, x0, y0, filas, cols, cw=64, ch=56, lw=130, cabecera=None, etiquetas=None, tam=24):
        self.x0, self.y0, self.filas, self.cols = x0, y0, filas, cols
        self.cw, self.ch, self.lw, self.tam = cw, ch, lw, tam
        self.cabecera = cabecera or [str(j) for j in range(cols)]
        self.etiquetas = etiquetas or [str(i) for i in range(filas)]

    def celda(self, i, j):
        x = self.x0 + self.lw + j * self.cw
        y = self.y0 + 40 + i * self.ch
        return x, y, x + self.cw, y + self.ch

    def centro(self, i, j):
        a, b, c, d = self.celda(i, j)
        return (a + c) / 2, (b + d) / 2

    def dibuja(self, f, vals, u=1.0, marca=None, sombra=None, fmt=None, colores=None):
        d = f.d
        if u <= 0:
            return
        for j in range(self.cols):
            a, _, c, _ = self.celda(0, j)
            d.text(((a + c) / 2, self.y0 + 20), self.cabecera[j], font=font(min(20, self.tam), True),
                   fill=mix(C["bot"], C["muted"], u), anchor="mm")
        for i in range(self.filas):
            _, b, _, e = self.celda(i, 0)
            d.text((self.x0 + self.lw - 12, (b + e) / 2), self.etiquetas[i], font=font(20, True),
                   fill=mix(C["bot"], C["muted"], u), anchor="rm")
            for j in range(self.cols):
                a, b, c, e = self.celda(i, j)
                fondo = C["panel"]
                if sombra and (i, j) in sombra:
                    fondo = mix(C["panel"], sombra[(i, j)], 0.38)
                d.rectangle((a, b, c, e), fill=mix(C["bot"], fondo, u), outline=mix(C["bot"], C["border"], u), width=2)
                if (i, j) in vals:
                    v = vals[(i, j)]
                    s = fmt(v) if fmt else ("∞" if v is None else str(v))
                    col = C["dim"] if v is None else C["text"]
                    if colores and (i, j) in colores:
                        col = colores[(i, j)]
                    d.text(((a + c) / 2, (b + e) / 2), s, font=font(self.tam, True), fill=col, anchor="mm")
        if marca:
            for (i, j), col in marca.items():
                a, b, c, e = self.celda(i, j)
                d.rectangle((a - 2, b - 2, c + 2, e + 2), outline=C[col] if isinstance(col, str) else col, width=5)

    def flecha_entre(self, f, de, a, col, u=1.0, dx=0, dy=0):
        if u <= 0:
            return
        x0, y0 = self.centro(*de)
        x1, y1 = self.centro(*a)
        ang = math.atan2(y1 - y0, x1 - x0)
        r = min(self.cw, self.ch) * 0.32
        p = (x0 + math.cos(ang) * r + dx, y0 + math.sin(ang) * r + dy)
        q = (x1 - math.cos(ang) * r + dx, y1 - math.sin(ang) * r + dy)
        q = (lerp(p[0], q[0], ease(u)), lerp(p[1], q[1], ease(u)))
        flecha(f, p, q, col, w=4)


def formula(f, x, y, izq, casos, u=1.0, size=26, colores=None):
    """
    izq = "dardos(i, j) ="     casos = [("expresión", "si condición"), ...]
    Dibuja la llave de casos. Devuelve la y de debajo.
    """
    if u <= 0:
        return y
    fn = font(size, True, True)
    col = mix(C["bot"], C["text"], u)
    lh = size + 16
    w_izq = f.d.textlength(izq + " ", font=fn)
    if len(casos) == 1:
        e, c = casos[0]
        f.d.text((x, y), izq + " " + e + ("   " + c if c else ""), font=fn, fill=col)
        return y + lh
    alto = lh * len(casos)
    xb = x + w_izq
    f.d.text((x, y + alto / 2 - lh / 2), izq, font=fn, fill=col)
    # llave
    bc = mix(C["bot"], C["gold"], u)
    f.d.line((xb + 10, y, xb + 4, y + 6, xb + 4, y + alto / 2 - 8, xb - 4, y + alto / 2 - 4, xb + 4, y + alto / 2,
              xb + 4, y + alto - 6, xb + 10, y + alto), fill=bc, width=3, joint="curve")
    ancho_e = max(f.d.textlength(e, font=fn) for e, _ in casos)
    for k, (e, c) in enumerate(casos):
        ce = mix(C["bot"], colores[k], u) if colores else col
        f.d.text((xb + 24, y + k * lh), e, font=fn, fill=ce)
        f.d.text((xb + 24 + ancho_e + 30, y + k * lh), c, font=font(size - 2, False, True), fill=mix(C["bot"], C["muted"], u))
    return y + alto


def codigo(cpp, ini, fin, maxc=72):
    """Líneas de código sin comentarios al final de línea y sin la sangría común."""
    raw = [(n, s.split("//")[0].rstrip() if "//" in s and not s.strip().startswith("//") else s)
           for n, s in code_lines(cpp, ini, fin, maxc=300)]
    ind = min(len(s) - len(s.lstrip()) for _, s in raw if s.strip())
    return [(n, s[ind:] if len(s[ind:]) <= maxc else s[ind:][:maxc - 1] + "…") for n, s in raw]


def portada(f, num, titulo, tema, dibujo=None):
    f.text((420, 250), num, size=26, color="gold", bold=True, anchor="mm")
    f.text((420, 312), titulo, size=50 if len(titulo) < 24 else 40, bold=True, anchor="mm")
    f.text((420, 368), tema, size=22, color="muted", anchor="mm")
    if dibujo:
        dibujo(f)


def cierre(f, titulo, items, cols=None):
    f.text((W / 2, 80), titulo, size=40, bold=True, anchor="mm")
    cols = cols or [C["blue"], NARANJA, C["purple"], C["green"]]
    for k, txt in enumerate(items):
        t0 = f.c(min(k, len(f._cues) - 1)) + 0.2 * max(0, k - len(f._cues) + 1)
        if f.t >= t0:
            u = f.p(t0, 0.5)
            y = 180 + 100 * k
            x = lerp(-200, 80, u)
            f.d.ellipse((x, y - 15, x + 30, y + 15), fill=cols[k % len(cols)])
            f.d.text((x + 52, y), txt, font=font(25, True), fill=mix(C["bot"], C["text"], u), anchor="lm")
