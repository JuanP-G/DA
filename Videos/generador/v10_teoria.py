"""Vídeo de teoría · Programación dinámica (temas 10 y 11), animado."""
import sys
from vidlib import C, W, H, font
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, portada, cierre, Tabla

TEMA = "Temas 10 y 11 · Programación dinámica"
MORADO = C["purple"]


# ------------------------------------------------------------------ árbol de fib(5)
def arbol(n, prof=0, nodos=None, aristas=None, padre=None, cont=None):
    if nodos is None:
        nodos, aristas, cont = [], [], [0]
    yo = len(nodos)
    nodos.append([n, prof, 0.0])
    if padre is not None:
        aristas.append((padre, yo))
    if n >= 2:
        arbol(n - 1, prof + 1, nodos, aristas, yo, cont)
        nodos[yo][2] = cont[0]
        cont[0] += 1
        arbol(n - 2, prof + 1, nodos, aristas, yo, cont)
    else:
        nodos[yo][2] = cont[0]
        cont[0] += 1
    return nodos, aristas


NOD, ARI = arbol(5)
NX = max(x for _, _, x in NOD)
POS = [(90 + x * (1100 / NX), 130 + p * 105) for _, p, x in NOD]
COLF = {5: C["text"], 4: C["blue"], 3: NARANJA, 2: MORADO, 1: C["green"], 0: C["muted"]}
# orden de visita (preorden = orden de llamada)
ORD = list(range(len(NOD)))


def nodo(f, k, u=1.0, gris=False, r=28):
    if u <= 0:
        return
    x, y = POS[k]
    v = NOD[k][0]
    c = C["dim"] if gris else COLF[v]
    f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=4)
    f.d.text((x, y), f"f{v}", font=font(20, True), fill=mix(C["bot"], c, u), anchor="mm")


def e_portada(f):
    def dib(f):
        T = Tabla(780, 250, 3, 5, cw=70, ch=60, lw=0, cabecera=[""] * 5, etiquetas=[""] * 3, tam=24)
        u = f.p(0.3, 1.2)
        k = int(u * 15)
        vals = {(i, j): (i + 1) * (j + 1) for i in range(3) for j in range(5) if i * 5 + j < k}
        T.dibuja(f, vals)
    portada(f, "Teoría", "Programación dinámica", TEMA, dib)


def e_fib(f):
    texto(f, (640, 50), "fib(n) = fib(n−1) + fib(n−2)", 30, "text", aparece(f, f.c(0)), mono=True, anchor="mm")
    t0, t1 = f.c(1), f.c(2)
    k = int((f.t - t0) / (t1 - t0) * len(NOD)) if f.t >= t0 else 0
    k = max(0, min(k, len(NOD)))
    for (a, b) in ARI:
        if b < k:
            f.d.line((POS[a], POS[b]), fill=C["border"], width=3)
    rep = f.t >= f.c(2)
    for q in range(k):
        v = NOD[q][0]
        gris = rep and v not in (3, 2)
        nodo(f, q, 1, gris=gris)
        if rep and v in (3, 2):
            x, y = POS[q]
            u = aparece(f, f.c(2) + (0.6 if v == 2 else 0))
            f.d.ellipse((x - 36, y - 36, x + 36, y + 36), outline=mix(C["bot"], COLF[v], u), width=3)
    if rep:
        texto(f, (1100, 670), "f3 ×2   f2 ×3", 28, NARANJA, aparece(f, f.c(2)), mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (300, 670), "fib(n): ¡exponencial!", 28, "red", aparece(f, f.c(3)), anchor="mm")


def e_memo(f):
    # vector fib rellenado de izquierda a derecha
    vals = [0, 1, 1, 2, 3, 5, 8, 13]
    T = Tabla(240, 220, 1, 8, cw=96, ch=80, lw=0, cabecera=[f"fib({i})" for i in range(8)], etiquetas=[""], tam=32)
    t0, t1 = f.c(1), f.c(2)
    k = int((f.t - t0) / (t1 - t0) * 8) if f.t >= t0 else 0
    k = max(0, min(k, 8))
    v = {(0, j): vals[j] for j in range(k)}
    marca = {(0, k): "gold"} if 2 <= k < 8 else {}
    T.dibuja(f, v, marca=marca)
    if 2 <= k < 8:
        u = ((f.t - t0) / (t1 - t0) * 8) % 1
        T.flecha_entre(f, (0, k - 1), (0, k), AZUL, u=min(1, u * 2), dy=-26)
        T.flecha_entre(f, (0, k - 2), (0, k), NARANJA, u=min(1, u * 2), dy=26)
    texto(f, (640, 120), "cada subproblema se calcula UNA vez y se apunta", 28, "green", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(2):
        texto(f, (640, 420), "exponencial  →  O(n)", 40, "gold", aparece(f, f.c(2)), mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 520), "eso es la programación dinámica:", 26, "text", aparece(f, f.c(3)), anchor="mm")
        texto(f, (640, 565), "recursión  +  tabla con los resultados", 30, "text", aparece(f, f.c(3) + 0.3), anchor="mm")


def e_ingredientes(f):
    f.box(60, 140, 540, 440, "1 · subproblemas repetidos")
    f.box(680, 140, 540, 440, "2 · principio de optimalidad")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        # mini árbol con nodos repetidos
        pts = [(330, 240), (230, 340), (430, 340), (180, 440), (280, 440), (380, 440), (480, 440)]
        lab = ["f4", "f3", "f2", "f2", "f1", "f1", "f0"]
        for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
            f.d.line((pts[a], pts[b]), fill=mix(C["panel"], C["border"], u), width=3)
        for k, (x, y) in enumerate(pts):
            c = MORADO if lab[k] == "f2" else C["muted"]
            f.d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=C["panel"], outline=mix(C["panel"], c, u), width=4)
            f.d.text((x, y), lab[k], font=font(18, True), fill=mix(C["panel"], c, u), anchor="mm")
        texto(f, (330, 530), "los mismos cálculos, muchas veces", 22, "muted", u, anchor="mm", fondo=C["panel"])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        # camino óptimo A -> B pasando por M: el trozo A -> M también es óptimo
        A, M, B = (760, 450), (950, 280), (1140, 420)
        f.d.line((A, (850, 330), M), fill=mix(C["panel"], C["green"], u), width=6, joint="curve")
        f.d.line((M, (1060, 300), B), fill=mix(C["panel"], C["green"], u), width=6, joint="curve")
        f.d.line((A, (880, 520), (1000, 480), M), fill=mix(C["panel"], C["dim"], u), width=3)
        for p, s in [(A, "A"), (M, "M"), (B, "B")]:
            f.d.ellipse((p[0] - 18, p[1] - 18, p[0] + 18, p[1] + 18), fill=mix(C["panel"], C["gold"], u))
            f.d.text(p, s, font=font(18, True), fill=C["node_t"], anchor="mm")
        texto(f, (950, 530), "si A→B es óptimo, A→M también", 22, "muted", u, anchor="mm", fondo=C["panel"])
    if f.t >= f.c(2):
        texto(f, (640, 640), "con los dos  →  programación dinámica", 30, "gold", aparece(f, f.c(2)), anchor="mm")


PASOS = [("1", "Definición", "decir con palabras\nqué calcula la\nfunción y qué es\ncada parámetro", C["blue"]),
         ("2", "Recurrencia", "casos base y\ncasos recursivos,\ncada uno con\nsu condición", NARANJA),
         ("3", "Tabla", "orden de relleno:\ncada casilla\ndespués de las\nque necesita", MORADO),
         ("4", "Respuesta", "qué casilla es\nla respuesta y,\nsi lo piden,\nreconstruir", C["green"])]


def e_receta(f):
    for k, (num, tit, desc, col) in enumerate(PASOS):
        t0 = f.c(min(k + 1, 4))
        if f.t < t0:
            continue
        u = aparece(f, t0)
        x = 40 + k * 305
        y = lerp(200, 150, ease(u))
        f.d.rounded_rectangle((x, y, x + 285, y + 330), 18, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], col, u), width=4)
        f.d.ellipse((x + 20, y + 20, x + 80, y + 80), fill=mix(C["bot"], col, u))
        f.d.text((x + 50, y + 50), num, font=font(32, True), fill=C["node_t"], anchor="mm")
        f.d.text((x + 96, y + 50), tit, font=font(26, True), fill=mix(C["bot"], C["text"], u), anchor="lm")
        for q, line in enumerate(desc.split("\n")):
            f.d.text((x + 22, y + 120 + q * 40), line, font=font(24), fill=mix(C["bot"], C["muted"], u))
        if k < 3:
            flecha(f, (x + 287, y + 165), (x + 304, y + 165), mix(C["bot"], C["muted"], u), w=3, cab=8)
    texto(f, (640, 80), "La receta", 34, "gold", aparece(f, f.c(0)), anchor="mm")


def e_dos_formas(f):
    f.box(40, 110, 580, 480, "descendente: recursión + memoria")
    f.box(660, 110, 580, 480, "ascendente: rellenar la tabla")
    # descendente: llamadas que bajan, con caché
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        ys = [190, 270, 350, 430, 510]
        for k, y in enumerate(ys):
            x = 120 + k * 50
            f.d.text((x, y), f"fib({5 - k})", font=font(22, True, True), fill=mix(C["panel"], C["text"], u), anchor="lm")
            if k < 4:
                flecha(f, (x + 20, y + 18), (x + 60, y + 52), mix(C["panel"], C["muted"], u), w=2, cab=8)
        texto(f, (420, 300), "¿ya está\n apuntado?", 24, "gold", u, fondo=C["panel"])
        texto(f, (420, 400), "sí → se usa\nno → se calcula", 22, "muted", u, fondo=C["panel"])
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        T = Tabla(700, 200, 4, 6, cw=80, ch=60, lw=0, cabecera=[""] * 6, etiquetas=[""] * 4, tam=22)
        k = int(f.lin(f.c(2), max(0.5, f.c(3) - f.c(2))) * 24)
        vals = {(i, j): "·" for i in range(4) for j in range(6) if i * 6 + j < k}
        T.dibuja(f, vals, u=u, marca={(k // 6, k % 6): "gold"} if k < 24 else None)
        texto(f, (950, 530), "fila a fila, sin recursión", 22, "muted", u, anchor="mm", fondo=C["panel"])
    if f.t >= f.c(3):
        texto(f, (640, 650), "en el curso: ascendente, con bucles", 28, "gold", aparece(f, f.c(3)), anchor="mm")


def e_memoria(f):
    texto(f, (640, 70), "Si cada fila solo usa la de arriba, basta un vector", 28, "text", aparece(f, f.c(0)), anchor="mm")
    # mochila 0/1: usa la fila de arriba → recorrer j de derecha a izquierda
    sep = 70
    for blk, (y, tit, col, dirr) in enumerate([(220, "0/1 (cada objeto una vez)  →  de derecha a izquierda", NARANJA, -1),
                                               (470, "ilimitados (monedas)  →  de izquierda a derecha", C["blue"], 1)]):
        t0 = f.c(1 + blk)
        if f.t < t0:
            continue
        u = aparece(f, t0)
        texto(f, (120, y - 120), tit, 24, col, u)
        for j in range(11):
            x = 120 + j * sep
            f.d.rectangle((x, y - 30, x + sep - 6, y + 30), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], C["border"], u), width=2)
            f.d.text((x + sep / 2 - 3, y + 48), str(j), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")
        # recorrido
        p = f.lin(t0 + 0.5, 3.5)
        jj = int(p * 8) + 3
        jj = min(jj, 10)
        j = jj if dirr == 1 else 13 - jj
        x = 120 + j * sep
        f.d.rectangle((x - 2, y - 32, x + sep - 4, y + 32), outline=C["gold"], width=4)
        xa = 120 + (j - 3) * sep
        a = (xa + sep / 2, y - 32)
        b = (x + sep / 2 - 3, y - 32)
        f.d.arc((a[0], y - 75, b[0], y + 5), 200, 340, fill=col, width=4)
        texto(f, (xa + sep / 2 - 3, y), "nuevo" if dirr == 1 else "viejo", 16, col, 1, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 650), "pero para reconstruir hace falta la tabla entera", 28, "gold", aparece(f, f.c(3)), anchor="mm")


def e_reconstruir(f):
    T = Tabla(120, 140, 4, 6, cw=80, ch=64, lw=60, cabecera=[str(j) for j in range(6)], etiquetas=["0", "1", "2", "3"], tam=24)
    vals = {(0, j): 0 for j in range(6)}
    M = [[0] * 6, [0, 0, 3, 3, 3, 3], [0, 0, 3, 4, 4, 7], [0, 0, 3, 4, 5, 7]]
    vals = {(i, j): M[i][j] for i in range(4) for j in range(6)}
    camino = [((3, 5), (2, 5), "no"), ((2, 5), (1, 2), "sí"), ((1, 2), (0, 0), "sí")]
    t0 = f.c(1)
    k = int((f.t - t0) / 1.6) if f.t >= t0 else -1
    marca = {}
    if 0 <= k < len(camino):
        marca[camino[k][0]] = "gold"
    elif k >= len(camino):
        marca[(0, 0)] = "green"
    T.dibuja(f, vals, marca=marca)
    for q in range(min(max(0, k), len(camino))):
        a, b, s = camino[q]
        T.flecha_entre(f, a, b, AZUL if s == "no" else NARANJA)
    texto(f, (760, 200), "desde la casilla de la respuesta,", 24, "text", aparece(f, f.c(0)))
    texto(f, (760, 236), "se deshacen las decisiones:", 24, "text", aparece(f, f.c(0)))
    if f.t >= f.c(1):
        texto(f, (760, 320), "igual que arriba → no se usó", 24, AZUL, aparece(f, f.c(1)))
        texto(f, (760, 360), "distinta → se usó, y se salta", 24, NARANJA, aparece(f, f.c(1)))
    if f.t >= f.c(2):
        texto(f, (760, 460), "ejemplos: 10-2 (dardos), 11-1 (cofres),", 22, "muted", aparece(f, f.c(2)))
        texto(f, (760, 492), "11-2 (el palíndromo)", 22, "muted", aparece(f, f.c(2)))


PATRONES = [("Mochila 0/1", "10-1 · 11-1", "fila i−1", NARANJA),
            ("Monedas ilimitadas", "10-2", "misma fila", C["blue"]),
            ("Cuadrícula", "10-3 · 10-4", "arriba / izquierda", MORADO),
            ("Intervalos", "11-2", "por diagonales", C["green"])]


def mini(f, k, x, y, u):
    """Dibujito de la forma de la tabla de cada patrón."""
    cw = 30
    col = PATRONES[k][3]
    filas = 4
    for i in range(filas):
        for j in range(5):
            if k == 3 and j < i:
                continue
            f.d.rectangle((x + j * cw, y + i * cw, x + j * cw + cw - 3, y + i * cw + cw - 3), fill=mix(C["panel"], C["border"], u))
    ci, cj = 2, 3
    cx, cy = x + cj * cw + cw / 2, y + ci * cw + cw / 2
    deps = {0: [(1, 3), (1, 1)], 1: [(1, 3), (2, 1)], 2: [(1, 3), (2, 2)], 3: [(3, 3), (2, 2)]}[k]
    if k == 3:
        ci, cj = 2, 3
        deps = [(3, 3), (2, 2), (3, 2)]
    for (i, j) in deps:
        if k == 3 and (i, j) == (3, 2):
            continue
        a = (x + j * cw + cw / 2, y + i * cw + cw / 2)
        flecha(f, a, (cx + (a[0] - cx) * 0.25, cy + (a[1] - cy) * 0.25), mix(C["panel"], col, u), w=3, cab=7)
    f.d.rectangle((x + cj * cw - 1, y + ci * cw - 1, x + cj * cw + cw - 2, y + ci * cw + cw - 2), outline=mix(C["panel"], C["gold"], u), width=3)


def e_patrones(f):
    texto(f, (640, 60), "Los cuatro patrones del curso", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (tit, ej, dep, col) in enumerate(PATRONES):
        t0 = f.c(k + 1)
        if f.t < t0:
            continue
        u = aparece(f, t0)
        x = 40 + (k % 2) * 610
        y = 110 + (k // 2) * 280
        f.d.rounded_rectangle((x, y, x + 590, y + 260), 16, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], col, u), width=3)
        f.d.text((x + 24, y + 36), tit, font=font(28, True), fill=mix(C["bot"], col, u), anchor="lm")
        f.d.text((x + 24, y + 80), ej, font=font(20, True), fill=mix(C["bot"], C["muted"], u), anchor="lm")
        f.d.text((x + 24, y + 130), "depende de:", font=font(20), fill=mix(C["bot"], C["muted"], u), anchor="lm")
        f.d.text((x + 24, y + 164), dep, font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="lm")
        mini(f, k, x + 400, y + 70, u)


def e_examen(f):
    texto(f, (60, 60), "En el examen", 32, "gold", aparece(f, f.c(0)))
    texto(f, (60, 120), "1 · Definición:  mochila(i, j) = máximo valor con los objetos 1..i sin pasar del peso j", 22, "text",
          aparece(f, f.c(1)), bold=False)
    texto(f, (60, 175), "2 · Casos base:", 22, "text", aparece(f, f.c(2)))
    y = formula(f, 100, 215, "mochila(0, j) =", [("0", "0 ≤ j ≤ M")], aparece(f, f.c(2)), size=22)
    texto(f, (60, y + 16), "3 · Recurrencia (con TODAS las condiciones):", 22, "text", aparece(f, f.c(3)))
    y = formula(f, 100, y + 56, "mochila(i, j) =", [("mochila(i−1, j)", "si p_i > j"),
                                                     ("max( mochila(i−1, j),  mochila(i−1, j−p_i) + v_i )", "si p_i ≤ j")],
                aparece(f, f.c(3)), size=22)
    texto(f, (60, y + 24), "4 · Llamada inicial:  mochila(N, M)", 22, "text", aparece(f, f.c(4)), mono=True)
    texto(f, (60, y + 70), "5 · Coste:  O(N·M) en tiempo;  memoria O(N·M), u O(M) con un vector", 22, "text", aparece(f, f.c(5)), mono=True)
    if f.t >= f.c(6):
        texto(f, (640, 670), "cuenta casi más que el código", 28, NARANJA, aparece(f, f.c(6)), anchor="mm")


def e_cierre(f):
    cierre(f, "Programación dinámica", [
        "subproblemas repetidos + principio de optimalidad",
        "definición, recurrencia, orden de la tabla, respuesta",
        "un vector si basta la fila de arriba (¡el sentido importa!)",
        "la tabla entera si hay que reconstruir",
    ])


ESC = [
    Escena("Programación dinámica: cómo resolver problemas recursivos sin repetir el mismo cálculo una y otra vez.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Empecemos por algo conocido: fibonacci. Cada número es la suma de los dos anteriores. "
           "Si lo programamos con recursión tal cual, fib de cinco llama a fib de cuatro y a fib de tres, y cada una vuelve a llamar a otras dos. "
           "Fíjate: fib de tres se calcula dos veces, y fib de dos, tres veces. "
           "El árbol crece de forma exponencial.",
           e_fib, titulo="Fibonacci recursivo", extra=1.5),
    Escena("La solución es apuntar cada resultado la primera vez que se calcula. "
           "Con un vector, cada casilla se rellena a partir de las dos anteriores, de izquierda a derecha. "
           "De exponencial pasamos a lineal. "
           "Esa es la idea de la programación dinámica: una recursión, más una tabla donde se guardan los resultados.",
           e_memo, titulo="Apuntar resultados", extra=1.5),
    Escena("Funciona cuando hay subproblemas repetidos, como en fibonacci. "
           "Y, en optimización, cuando se cumple el principio de optimalidad: una solución óptima está hecha de soluciones óptimas de sus subproblemas. "
           "Con las dos cosas, la programación dinámica es el camino.",
           e_ingredientes, titulo="Cuándo se puede", extra=1.5),
    Escena("Para resolver cualquier problema, seguimos siempre la misma receta. "
           "Primero, decir con palabras qué calcula la función y qué significan sus parámetros. "
           "Segundo, la recurrencia: los casos base y los recursivos, cada uno con su condición. "
           "Tercero, en qué orden se rellena la tabla, para que cada casilla se calcule después de las que necesita. "
           "Y cuarto, qué casilla es la respuesta y, si lo piden, cómo reconstruir la solución.",
           e_receta, titulo="La receta", extra=1.5),
    Escena("Hay dos formas de programarlo. "
           "Descendente: la recursión de siempre, pero antes de calcular algo se mira si ya está apuntado. "
           "Ascendente: se rellena la tabla con bucles, desde los casos base hacia la respuesta, sin recursión. "
           "En el curso usamos la ascendente.",
           e_dos_formas, titulo="Descendente y ascendente", extra=1.5),
    Escena("Muchas veces cada fila solo necesita la de arriba, y entonces basta con un vector. "
           "Pero el sentido del recorrido importa. En una mochila cero uno, donde cada objeto se usa una vez, hay que ir de derecha a izquierda, para leer valores todavía de la fila anterior. "
           "Con objetos ilimitados, como las monedas, se va de izquierda a derecha, porque queremos el valor ya actualizado. "
           "Eso sí: si hay que reconstruir la solución, hace falta la tabla entera.",
           e_memoria, titulo="Ahorrar memoria", extra=2.0),
    Escena("Reconstruir es deshacer el camino. "
           "Desde la casilla de la respuesta, si vale lo mismo que la de arriba, ese objeto no se usó; si es distinta, se usó, y se salta hacia atrás su peso. "
           "Así se reconstruyen los dardos, los cofres o el palíndromo de los ejercicios.",
           e_reconstruir, titulo="Reconstruir", extra=2.0),
    Escena("En el curso salen cuatro patrones. "
           "La mochila cero uno, que mira la fila de arriba: la cometa y el cazatesoros. "
           "Las monedas ilimitadas, que miran su misma fila: las dianas. "
           "La cuadrícula, donde cada casilla depende de sus vecinas de arriba o de la izquierda: las obras y el tablero. "
           "Y los intervalos, que se rellenan por diagonales: el palíndromo.",
           e_patrones, titulo="Los patrones", extra=2.0),
    Escena("En el examen, la recurrencia cuenta tanto como el código, y se escribe así. "
           "Una definición con palabras. "
           "Los casos base. "
           "La recurrencia con todas sus condiciones. "
           "La llamada inicial que da la respuesta. "
           "Y el coste en tiempo y en memoria. "
           "Cada problema del repositorio tiene la suya escrita en este formato.",
           e_examen, titulo="Formato de examen", extra=2.0),
    Escena("Resumiendo: programación dinámica cuando hay subproblemas repetidos y principio de optimalidad. "
           "Siempre la misma receta: definición, recurrencia, orden de la tabla y respuesta. "
           "Un vector si basta la fila de arriba, con cuidado con el sentido. "
           "Y la tabla entera si hay que reconstruir.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/10-0", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-0: {build(ESC, '../10-0_programacion_dinamica_teoria.mp4'):.0f}s")
