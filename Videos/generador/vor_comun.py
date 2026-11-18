"""Piezas comunes de los vídeos animados de voraces (temas 8, 9 y 12) y de los temas 1-3."""
import sys
from vidlib import C, W, H, font
from anim import ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto


def col(c):
    return C[c] if isinstance(c, str) else c


def caja(f, x, y, s, c="blue", u=1.0, w=70, h=56, tam=26, relleno=None, gris=False, borde=4, txt=None):
    """Caja redondeada con un número/texto centrado en (x, y)."""
    if u <= 0:
        return
    c = C["dim"] if gris else col(c)
    rel = relleno if relleno is not None else C["panel"]
    f.d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), 10, fill=mix(C["bot"], rel, u),
                          outline=mix(C["bot"], c, u), width=borde)
    f.d.text((x, y), str(s), font=font(tam, True), fill=mix(C["bot"], col(txt) if txt else (C["dim"] if gris else C["text"]), u),
             anchor="mm")


def mueve(a, b, u):
    u = ease(max(0.0, min(1.0, u)))
    return lerp(a[0], b[0], u), lerp(a[1], b[1], u)


def paso_idx(f, t0, t1, n):
    """Índice del paso actual al repartir [t0, t1) en n pasos (-1 antes, n después) y fracción dentro del paso."""
    if f.t < t0:
        return -1, 0.0
    if f.t >= t1:
        return n, 1.0
    x = (f.t - t0) / (t1 - t0) * n
    return int(x), x - int(x)


def tick(f, x, y, ok=True, u=1.0, r=16):
    if u <= 0:
        return
    c = mix(C["bot"], C["green"] if ok else C["red"], u)
    if ok:
        f.d.line((x - r, y, x - r / 3, y + r * 0.7, x + r, y - r * 0.8), fill=c, width=5, joint="curve")
    else:
        f.d.line((x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8), fill=c, width=5)
        f.d.line((x - r * 0.8, y + r * 0.8, x + r * 0.8, y - r * 0.8), fill=c, width=5)


def barra_tiempo(f, x0, x1, y, a, b, marcas=(), u=1.0, etiq=None):
    """Eje horizontal de a a b con marcas [(valor, texto)]."""
    if u <= 0:
        return
    f.d.line((x0, y, x1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    for v, s in marcas:
        x = x0 + (v - a) * (x1 - x0) / (b - a)
        f.d.line((x, y - 6, x, y + 6), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((x, y + 20), s, font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def args_preview(ESC, carpeta, salida, nombre):
    from anim import build, preview
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, carpeta, tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"{nombre}: {build(ESC, salida):.0f}s")


def etiqueta(f, xy, s, size=24, c="text", u=1.0, mono=False, pad=12):
    """Texto centrado sobre una pastilla oscura (para que se lea sobre cualquier fondo)."""
    if u <= 0:
        return
    fn = font(size, True, mono)
    w = f.d.textlength(s, font=fn)
    x, y = xy
    f.d.rounded_rectangle((x - w / 2 - pad, y - size / 2 - pad, x + w / 2 + pad, y + size / 2 + pad), 12,
                          fill=mix(C["bot"], C["panel"], u))
    f.d.text((x, y), s, font=fn, fill=mix(C["panel"], col(c), u), anchor="mm")
