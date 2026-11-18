"""Escenas genéricas para los vídeos de colas de prioridad del tema 2."""
from vidlib import C, W, H, font, find_line
from anim import ease, lerp, mix
from pd_comun import aparece, texto, codigo, cierre
from vor_comun import paso_idx, etiqueta
from pq_comun import arbol, arbol_anim


def escena_traza(f, pasos, etq, colores=None, t0=None, t1=None, cx=820, ancho=640, lateral=None, titulo="montículo: arriba, el primero"):
    """
    pasos: [(antes, despues, texto, color)] con antes/despues = listas del montículo [(elem, prio)].
    lateral(f, k, fr): dibuja lo propio del problema a la izquierda.
    """
    t0 = f.c(0) if t0 is None else t0
    t1 = f.T - 1.5 if t1 is None else t1
    k, fr = paso_idx(f, t0, t1, len(pasos))
    k = max(0, min(k, len(pasos) - 1))
    antes, despues, s, c = pasos[k]
    col = colores(despues + antes) if callable(colores) else colores
    if fr < 0.4:
        arbol(f, antes, cx, 180, ancho, etq, marca={0} if antes else set(), colores=col, r=40, tam=19)
    else:
        arbol_anim(f, antes, despues, (fr - 0.4) / 0.45, cx, 180, ancho, etq, colores=col, r=40, tam=19)
    texto(f, (cx, 110), titulo, 20, "muted", 1, anchor="mm")
    etiqueta(f, (cx, 630), s, 24, c, 1, mono=True)
    if lateral:
        lateral(f, k, fr)
    return k, fr


def escena_codigo(f, cpp, secciones, size=20, maxc=92):
    """secciones: [(a, b, hl, título)], una por frase de la narración (la k-ésima empieza en f.c(k))."""
    k = 0
    for q in range(len(secciones)):
        if f.t >= f.c(q):
            k = q
    a, b, hl, titulo = secciones[k]
    lines = [(n, t) for n, t in codigo(cpp, a, b, maxc=maxc) if not t.strip().startswith("//") and t.strip()]
    f.code(40, 80, 1200, 600, lines, hl=hl, title=titulo, size=size)


def escena_lista(f, items):
    f.box(60, 120, 1160, 440)
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])
