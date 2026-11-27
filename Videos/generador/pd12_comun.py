"""Escenas comunes de los vídeos 12-4 … 12-10 (programación dinámica III)."""
import sys

from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview
from pd_comun import aparece, texto, codigo, portada, cierre

TEMA = "Tema 12 · Programación dinámica III"


def e_portada(num, titulo, dib):
    def dibuja(f):
        portada(f, f"EJ {num}", titulo, TEMA, dib)
    return dibuja


def lineas(f, filas):
    """filas = [(frase, y, texto, color, tamaño[, mono])]: cada línea aparece cuando empieza su frase."""
    for fila in filas:
        k, y, s, col, tam = fila[:5]
        mono = len(fila) > 5 and fila[5]
        if f.t >= f.c(k):
            texto(f, (640, y), s, tam, col, aparece(f, f.c(k)), mono=mono, anchor="mm")


def e_lineas(filas):
    return lambda f: lineas(f, filas)


def avance(f, k0, k1, total):
    """Cuántas casillas hay ya rellenas si se reparten entre las frases k0 y k1."""
    t0, t1 = f.c(k0), f.c(k1)
    if f.t < t0:
        return 0
    if f.t >= t1:
        return total
    return int((f.t - t0) / (t1 - t0) * total)


def panel(f, x, y, w, h, titulo, filas):
    """Panel lateral con líneas (texto, color)."""
    f.box(x, y, w, h, titulo)
    for k, (s, col) in enumerate(filas):
        texto(f, (x + 28, y + 70 + 42 * k), s, 23, col, 1, mono=True, bold=False, fondo=C["panel"])


def e_codigo(cpp, primera, ultima, resaltados, notas, maxc=74, size=16):
    """primera/ultima/resaltados son textos que se buscan en el .cpp; resaltados = una lista por frase."""
    a = find_line(cpp, primera)
    b = find_line(cpp, ultima, a)
    code = codigo(cpp, a, b, maxc=maxc)
    hls = [{find_line(cpp, s, a) for s in grupo} for grupo in resaltados]

    def dibuja(f):
        hl = set()
        for k, g in enumerate(hls):
            if f.t >= f.c(k):
                hl = g
        alto = min(600, 60 + (size + 7) * len(code))
        f.code(30, 70, 850, alto, code, hl=hl, title="solución", size=size)
        f.box(900, 70, 350, 600, "qué hace")
        cols = [C["blue"], (240, 160, 70), C["green"], C["gold"]]
        for k, (x, y) in enumerate(notas):
            if f.t >= f.c(k):
                u = aparece(f, f.c(k))
                texto(f, (925, 140 + 125 * k), x, 22, cols[k % 4], u, fondo=C["panel"])
                texto(f, (925, 178 + 125 * k), y, 18, "muted", u, bold=False, fondo=C["panel"])
    return dibuja


def e_cierre(titulo, items):
    return lambda f: cierre(f, titulo, items)


def principal(escenas, num, salida):
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(escenas, f"preview/{num}", tiempos=("fin",), solo=solo)
    else:
        print(f"{num}: {build(escenas, salida):.0f}s")
