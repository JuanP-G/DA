"""Vídeo EJ 12-3 · Bollos preñaos (animado)."""
import os
import re
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla
from vor_comun import caja, paso_idx, tick, args_preview, etiqueta

CPP = "../../12-Evaluacion/EJ_12-3/EJ_12-3.cpp"
TEMA = "Tema 12 · Programación dinámica III"
M = 8
TIPOS = [(18, 3, 1, 10), (7, 3, 2, 100)]      # ejemplo 2: (g, c, m, p)
COLT = [(236, 150, 64), (230, 92, 92)]


def mochila(tipos, M, en_sitio=False):
    """Mismo algoritmo que el .cpp. Devuelve las filas euros tras cada tipo."""
    euros = [0] * (M + 1)
    filas = [euros[:]]
    for g, c, m, p in tipos:
        k = g // c
        nueva = euros if en_sitio else euros[:]
        for j in range(M + 1):
            t = 1
            while t <= k and t * m <= j:
                nueva[j] = max(nueva[j], (nueva if en_sitio else euros)[j - t * m] + t * p)
                t += 1
        euros = nueva
        filas.append(euros[:])
    return filas


FIL = mochila(TIPOS, M)
assert FIL[-1][M] == 240 and mochila([(15, 5, 20, 10)], 100)[-1][100] == 30
MAL = mochila(TIPOS, M, en_sitio=True)[-1][M]          # sin copiar la fila: 400


def cand(i, j):
    """Candidatos de bollos(i, j): [(t, columna de la fila i-1, valor)]."""
    g, c, m, p = TIPOS[i - 1]
    k = g // c
    return [(t, j - t * m, FIL[i - 1][j - t * m] + t * p) for t in range(0, k + 1) if t * m <= j]


# contraejemplo del voraz (por euros por gramo de masa): masa 4, A = 3 g / 10 €, B = 2 g / 6 €
VZ_M, VZ = 4, [(100, 1, 3, 10), (100, 1, 2, 6)]


def voraz(tipos, M):
    orden = sorted(tipos, key=lambda x: -x[3] / x[2])
    res, masa = 0, M
    for g, c, m, p in orden:
        t = min(g // c, masa // m)
        res += t * p
        masa -= t * m
    return res


VZ_V, VZ_OPT = voraz(VZ, VZ_M), mochila(VZ, VZ_M)[-1][VZ_M]
assert (VZ_V, VZ_OPT) == (10, 12)

TB = Tabla(50, 140, 3, M + 1, cw=96, ch=66, lw=240,
           etiquetas=["ningún tipo", "tipo 1", "tipos 1 y 2"], tam=28)


# ------------------------------------------------------------------ dibujos
def bollo(f, x, y, s=1.0, u=1.0, col=COLT[0]):
    if u <= 0:
        return
    f.d.ellipse((x - 60 * s, y - 34 * s, x + 60 * s, y + 34 * s), fill=mix(C["bot"], (214, 160, 92), u),
                outline=mix(C["bot"], (150, 100, 50), u), width=max(2, int(4 * s)))
    for dx in (-30, 0, 30):
        f.d.ellipse((x + dx * s - 12 * s, y - 10 * s, x + dx * s + 12 * s, y + 10 * s), fill=mix(C["bot"], col, u))
    f.d.arc((x - 44 * s, y - 26 * s, x + 44 * s, y + 10 * s), 200, 340, fill=mix(C["bot"], (240, 200, 140), u),
            width=max(2, int(3 * s)))


def barra_masa(f, x0, y, gramos, trozos, u=1.0, ancho=90):
    """Barra de M gramos; trozos = [(gramos, color, texto)]."""
    if u <= 0:
        return
    f.d.rectangle((x0, y, x0 + gramos * ancho, y + 46), fill=mix(C["bot"], C["panel"], u),
                  outline=mix(C["bot"], C["border"], u), width=2)
    x = x0
    for g, col, s in trozos:
        f.d.rectangle((x + 2, y + 2, x + g * ancho - 2, y + 44), fill=mix(C["bot"], col, u))
        f.d.text((x + g * ancho / 2, y + 23), s, font=font(18, True), fill=mix(C["bot"], C["node_t"], u), anchor="mm")
        x += g * ancho
    for q in range(gramos + 1):
        f.d.text((x0 + q * ancho, y + 62), str(q), font=font(16, True), fill=mix(C["bot"], C["dim"], u), anchor="mm")


def ficha(f, x, y, i, u=1.0, k=True):
    g, c, m, p = TIPOS[i]
    if u <= 0:
        return
    f.d.rounded_rectangle((x, y, x + 520, y + 150), 16, fill=mix(C["bot"], C["panel"], u),
                          outline=mix(C["bot"], COLT[i], u), width=3)
    bollo(f, x + 80, y + 75, 0.8, u, COLT[i])
    texto(f, (x + 160, y + 22), f"tipo {i + 1}", 26, COLT[i], u, fondo=C["panel"])
    texto(f, (x + 160, y + 62), f"chorizo {g} g · {c} g por bollo", 22, "text", u, fondo=C["panel"])
    texto(f, (x + 160, y + 96), f"masa {m} g · {p} € el bollo", 22, "text", u, fondo=C["panel"])
    if k:
        texto(f, (x + 500, y + 22), f"k = {g}/{c} = {g // c}", 22, "gold", u, mono=True, anchor="ra", fondo=C["panel"])


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        bollo(f, 960, 300, 1.4, f.p(0.2, 0.6), COLT[0])
        bollo(f, 1010, 420, 1.0, f.p(0.6, 0.6), COLT[1])
    portada(f, "12-3", "Bollos preñaos", TEMA, dib)


def e_problema(f):
    texto(f, (640, 80), "Estache Bo hace bollos preñaos", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        for q in range(3):
            bollo(f, 170 + q * 150, 230, 0.9, aparece(f, f.c(1) + 0.3 * q), COLT[q % 2])
        texto(f, (560, 205), "un solo tipo de chorizo por bollo", 24, "text", u)
        texto(f, (560, 245), "receta fija: c g de chorizo, m g de masa", 24, "text", u)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (120, 360), "Entrada:  N tipos (≤ 50),  M g de masa (≤ 1.000)", 26, "text", u, mono=True)
        texto(f, (120, 410), "por tipo:  g (chorizo que hay)  c  m  p (€)", 26, "text", u, mono=True)
    if f.t >= f.c(3):
        etiqueta(f, (640, 560), "¿cuántos euros como máximo?", 32, "gold", aparece(f, f.c(3)))


def e_ejemplo(f):
    ficha(f, 80, 110, 0, aparece(f, f.c(0)), k=f.t >= f.c(1))
    ficha(f, 680, 110, 1, aparece(f, f.c(0) + 0.4), k=f.t >= f.c(1))
    if f.t >= f.c(1):
        texto(f, (640, 310), "el chorizo limita cuántos bollos:  k = g / c  (división entera)", 24, "gold",
              aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        texto(f, (240, 380), f"masa: M = {M} g", 24, "muted", aparece(f, f.c(2)))
        barra_masa(f, 280, 420, M, [], aparece(f, f.c(2)))
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        barra_masa(f, 280, 420, M, [(2, COLT[1], "100 €"), (2, COLT[1], "100 €")] +
                   [(1, COLT[0], "10")] * 4, u)
        etiqueta(f, (640, 580), "2 del tipo 2 + 4 del tipo 1  =  200 + 40  =  240 €", 26, "green", u)


def e_idea(f):
    texto(f, (640, 80), "Es una mochila… con cantidades acotadas", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    filas = [("masa", "capacidad de la mochila", "blue", 1),
             ("bollo del tipo i", "objeto: peso m_i, valor p_i", NARANJA, 1),
             ("k_i = g_i / c_i", "unidades de ese objeto", "purple", 2),
             ("chorizo", "NO es otra capacidad: cada tipo tiene el suyo", "red", 3)]
    for q, (a, b, c, fr) in enumerate(filas):
        if f.t >= f.c(fr):
            u = aparece(f, f.c(fr) + 0.4 * (q if fr == 1 else 0))
            y = 180 + 100 * q
            f.d.rounded_rectangle((120, y - 32, 480, y + 32), 14, fill=mix(C["bot"], C["panel"], u),
                                  outline=mix(C["bot"], C[c] if isinstance(c, str) else c, u), width=3)
            texto(f, (300, y), a, 26, c, u, anchor="mm", fondo=C["panel"])
            flecha(f, (500, y), (lerp(500, 560, ease(u)), y), mix(C["bot"], C["muted"], u), w=3)
            texto(f, (580, y), b, 26, "text", u, anchor="lm")
    if f.t >= f.c(4):
        etiqueta(f, (640, 620), "decidir cuántos bollos t de cada tipo:  0 ≤ t ≤ k_i  y  t·m_i ≤ masa", 24, "gold",
                 aparece(f, f.c(4)))


def e_recurrencia(f):
    texto(f, (60, 80), "bollos(i, j) = máximo de euros con los tipos 1..i y j gramos de masa", 24, "muted",
          aparece(f, f.c(0)), bold=False)
    texto(f, (60, 150), "Caso base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 195, "bollos(0, j) =", [("0", "para todo j ≥ 0")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 80, "bollos(i, j) =", [("max  bollos(i−1, j − t·m_i) + t·p_i", "")], aparece(f, f.c(2)))
    texto(f, (360, y - 6), "0 ≤ t ≤ k_i,   t·m_i ≤ j", 22, "muted", aparece(f, f.c(3)), mono=True)
    if f.t >= f.c(3):
        texto(f, (80, y + 50), "t = 0: el tipo i no se usa  ·  t ≥ 1: t bollos del tipo i", 22, NARANJA,
              aparece(f, f.c(3) + 0.8), bold=False)
    texto(f, (60, y + 120), "Respuesta:  bollos(N, M)   (puede sobrar masa)", 28, "green", aparece(f, f.c(4)), mono=True)


def valores(hasta_fila, hasta_j):
    v = {(0, j): 0 for j in range(M + 1)}
    for i in range(1, 3):
        for j in range(M + 1):
            if i < hasta_fila or (i == hasta_fila and j < hasta_j):
                v[(i, j)] = FIL[i][j]
    return v


def tabla_fila(f, i, t0, t1, fin):
    k, fr = paso_idx(f, t0, t1, M + 1)
    hasta = max(0, min(k, M + 1))
    vals = valores(i, hasta if f.t < fin else M + 1)
    marca, sombra = {}, {}
    cur = (i, k) if 0 <= k <= M and f.t < fin else None
    cs = []
    if cur:
        cs = cand(i, k)
        marca[cur] = "gold"
        for t, jj, v in cs:
            sombra[(i - 1, jj)] = AZUL if t == 0 else NARANJA
    colores = {(a, b): C["dim"] for (a, b), v in vals.items() if v == 0}
    TB.dibuja(f, vals, marca=marca, sombra=sombra, colores=colores)
    g, c, m, p = TIPOS[i - 1]
    texto(f, (60, 400), f"tipo {i}:  m = {m} g de masa,  p = {p} €,  k = {g // c} bollos como mucho", 24, COLT[i - 1], 1)
    if cur:
        u = min(1, fr * 2.5)
        for t, jj, v in cs:
            if t <= 3 or i == 2:
                TB.flecha_entre(f, (i - 1, jj), cur, AZUL if t == 0 else NARANJA, u=u)
        mejor = max(v for _, _, v in cs)
        partes = [str(FIL[i - 1][jj]) if t == 0 else f"{FIL[i - 1][jj]}+{t * p}" for t, jj, v in cs]
        s = f"bollos({i}, {k}) = max(" + ", ".join(partes) + f") = {mejor}"
        texto(f, (60, 460), s, 24 if len(s) < 70 else 21, "text", 1, mono=True)
        texto(f, (60, 510), "↓ azul: t = 0 (no usar el tipo)    ↙ naranja: t bollos, t·m columnas a la izquierda",
              20, "muted", 1, bold=False)
    return vals, colores


def e_fila1(f):
    tabla_fila(f, 1, f.c(1), f.c(3), f.c(3))
    texto(f, (640, 90), "Fila 1: solo el tipo 1", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 600), "10 · min(j, 6): a partir de 6 g se acaba el chorizo", 26, "green", aparece(f, f.c(3)))


def e_fila2(f):
    vals, colores = tabla_fila(f, 2, f.c(1), f.c(3), f.c(3))
    texto(f, (640, 90), "Fila 2: añadimos el tipo 2", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(3):
        cs = cand(2, M)
        TB.dibuja(f, vals, marca={(2, M): "green"},
                  sombra={(1, jj): (AZUL if t == 0 else NARANJA) for t, jj, _ in cs}, colores=colores)
        for t, jj, v in cs:
            TB.flecha_entre(f, (1, jj), (2, M), AZUL if t == 0 else NARANJA)
        y = 460
        for q, (t, jj, v) in enumerate(cs):
            uu = aparece(f, f.c(3) + 0.6 * q)
            s = f"t = {t}:  bollos(1, {jj}) + {t}·100 = {FIL[1][jj]} + {t * 100} = {v}"
            texto(f, (80, y + 42 * q), s, 24, "green" if v == FIL[2][M] else "text", uu, mono=True)
        if f.t >= f.c(4):
            etiqueta(f, (1000, 600), f"bollos(2, 8) = {FIL[2][M]}", 30, "green", aparece(f, f.c(4)), mono=True)


def e_solucion(f):
    texto(f, (640, 80), "¿Qué bollos son?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    u1 = aparece(f, f.c(1))
    texto(f, (100, 170), "en bollos(2, 8) ganó t = 2  →  2 bollos del tipo 2, quedan 8 − 4 = 4 g", 24, "text", u1)
    u2 = aparece(f, f.c(2))
    texto(f, (100, 220), "bollos(1, 4) = 40  →  4 bollos del tipo 1", 24, "text", u2)
    tro = []
    if f.t >= f.c(1):
        tro += [(2, COLT[1], "100 €"), (2, COLT[1], "100 €")]
    if f.t >= f.c(2):
        tro += [(1, COLT[0], "10")] * 4
    barra_masa(f, 280, 320, M, tro, aparece(f, f.c(0)))
    for q in range(6 if f.t >= f.c(2) else (2 if f.t >= f.c(1) else 0)):
        col = COLT[1] if q < 2 else COLT[0]
        bollo(f, 200 + q * 150, 500, 0.7, aparece(f, f.c(1 if q < 2 else 2) + 0.2 * q), col)
    if f.t >= f.c(3):
        etiqueta(f, (640, 640), "200 + 40 = 240 €   ·   del tipo 2 sobra 1 g de chorizo", 26, "green", aparece(f, f.c(3)))


def e_voraz(f):
    texto(f, (640, 80), "¿Y un voraz por euros por gramo de masa?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (120, 160), f"masa {VZ_M} g     A: 3 g → 10 €  (3,33 €/g)     B: 2 g → 6 €  (3 €/g)", 24, "text", u, mono=True)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (120, 250), "voraz: primero A", 24, "red", u)
        barra_masa(f, 420, 240, VZ_M, [(3, COLT[0], "A 10 €")], u, ancho=110)
        texto(f, (420 + 4 * 110 + 30, 262), f"= {VZ_V} €", 28, "red", u, anchor="lm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (120, 380), "mejor: dos B", 24, "green", u)
        barra_masa(f, 420, 370, VZ_M, [(2, COLT[1], "B 6 €"), (2, COLT[1], "B 6 €")], u, ancho=110)
        texto(f, (420 + 4 * 110 + 30, 392), f"= {VZ_OPT} €", 28, "green", u, anchor="lm")
    if f.t >= f.c(4):
        etiqueta(f, (640, 580), "la masa que sobra y el tope de chorizo estropean el voraz: hace falta la tabla", 24,
                 "gold", aparece(f, f.c(4)))


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "cout << euros[M]")
CODE = codigo(CPP, A, B + 1, maxc=80)
L_VEC = find_line(CPP, "vector<int> euros(M + 1, 0);")
L_K = find_line(CPP, "int k = g / c;")
L_COPIA = find_line(CPP, "vector<int> nueva = euros;")
L_BUC = (find_line(CPP, "for (int j = 0; j <= M; ++j)"), find_line(CPP, "nueva[j] = max(nueva[j], euros[j - t * m] + t * p);"))
L_FIN = find_line(CPP, "euros = nueva;")
NOTAS = [({L_VEC}, "euros[j]: la fila anterior, un vector de M + 1"),
         ({L_K}, "k = g / c: bollos que permite el chorizo"),
         ({L_COPIA}, "nueva empieza como copia: es t = 0"),
         (set(range(L_BUC[0], L_BUC[1] + 1)), "para cada j, probar t = 1..k mientras t·m ≤ j"),
         ({L_FIN, B}, "la nueva fila pasa a ser la anterior; al final, euros[M]")]


def e_codigo(f):
    k = 0
    for q in range(len(NOTAS)):
        if f.t >= f.c(q):
            k = q
    hl, nota = NOTAS[k]
    f.code(40, 84, 1200, 470, CODE, hl=hl, title="resuelveCaso()", size=21)
    etiqueta(f, (640, 620), nota, 26, "gold", aparece(f, f.c(k)))


def e_errores(f):
    f.box(60, 110, 1160, 500, "errores típicos")
    items = [("k = g / c es división entera: 7 g de chorizo, 3 por bollo → 2 bollos", "text"),
             (f"sin copiar la fila (mismo vector, j hacia arriba): euros[8] = {MAL} ✗ (4 del tipo 2)", "red"),
             ("o se copia la fila, o se recorre j de M hacia 0", "green"),
             ("respuesta euros[M]: «con como mucho M gramos», puede sobrar masa", "text"),
             ("cabe en int: 50 tipos × 100 bollos × 100 €  ·  coste O(M · Σ k_i)", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 86 * k), s, 23, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Bollos preñaos", [
        "mochila acotada: masa = capacidad, k_i = g_i / c_i",
        "bollos(i, j) = max sobre t de bollos(i−1, j − t·m_i) + t·p_i",
        "bollos(0, j) = 0;  respuesta bollos(N, M)",
        "un vector por fila, copiando la anterior",
    ])


ESC = [
    Escena("Bollos preñaos. Un problema de evaluación de programación dinámica: una mochila en la que cada objeto tiene unidades limitadas.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Estache Bo, un cocinero gallego, va a hacer bollos preñaos para vender. "
           "Cada bollo lleva un solo tipo de chorizo, y su receta es fija: tantos gramos de chorizo y tantos de masa. "
           "Nos dan los gramos de masa que tiene y, de cada tipo de chorizo, cuánto hay, la receta y el precio del bollo. "
           "Queremos el máximo de euros que puede ganar.",
           e_problema, titulo="Qué piden", extra=1.5),
    Escena("Vamos a seguir el segundo ejemplo, con dos tipos de chorizo. "
           "El chorizo limita cuántos bollos salen de cada tipo: con dieciocho gramos y tres por bollo, seis; con siete y tres por bollo, solo dos. "
           "La masa, ocho gramos, se la reparten todos. "
           "La mejor opción: dos bollos del tipo dos y cuatro del tipo uno, doscientos cuarenta euros.",
           e_ejemplo, titulo="El ejemplo", extra=1.5),
    Escena("Esto es una mochila. "
           "La masa es la capacidad, y cada bollo es un objeto con su peso en masa y su valor en euros. "
           "Del tipo i hay ka sub i unidades, las que permite su chorizo. "
           "Ojo: el chorizo no es una segunda capacidad, porque cada tipo tiene el suyo; solo sirve para calcular ese tope. "
           "Así que para cada tipo decidimos cuántos bollos hacer.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Definimos bollos de i, jota: el máximo de euros usando los tipos del uno al i con jota gramos de masa. "
           "Sin ningún tipo, cero euros. "
           "Con el tipo i, probamos cada cantidad te: lo mejor de la fila anterior con la masa que sobra, más te bollos por su precio. "
           "Te va de cero a ka sub i, y los bollos tienen que caber en la masa. "
           "La respuesta es bollos de ene, eme.",
           e_recurrencia, titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla. La fila cero es todo ceros. "
           "En la fila uno, con el tipo uno, cada gramo de masa da un bollo de diez euros. "
           "Pero solo hay chorizo para seis bollos. "
           "Por eso a partir de seis gramos la fila se queda en sesenta.",
           e_fila1, titulo="Fila 1", extra=2.0),
    Escena("Ahora el tipo dos: dos gramos de masa, cien euros, y como mucho dos bollos. "
           "Cada casilla mira la de arriba, y las que están dos y cuatro columnas a la izquierda. "
           "Con poca masa no da ni para un bollo y se copia la fila de arriba. "
           "En la última casilla hay tres candidatos: sesenta sin bollos del tipo dos, ciento sesenta con uno y doscientos cuarenta con dos. "
           "El máximo es doscientos cuarenta.",
           e_fila2, titulo="Fila 2", extra=2.0),
    Escena("¿Qué bollos son? Se recupera hacia atrás. "
           "En la última casilla ganó te igual a dos: dos bollos del tipo dos, que gastan cuatro gramos. "
           "Con los cuatro que quedan, la fila uno vale cuarenta: cuatro bollos del tipo uno. "
           "Doscientos más cuarenta, y sobra un gramo de chorizo del tipo dos.",
           e_solucion, titulo="La solución", extra=1.5),
    Escena("¿No bastaría con un voraz, por ejemplo el que mira los euros por gramo de masa? "
           "Mira este caso: cuatro gramos de masa, el bollo A gasta tres y vale diez, el B gasta dos y vale seis. "
           "El voraz coge primero A, que rinde más por gramo, y le sobra un gramo que no sirve para nada: diez euros. "
           "Con dos bollos B se ganan doce. "
           "La masa sobrante y el tope de chorizo estropean cualquier voraz; hace falta la tabla.",
           e_voraz, titulo="¿Un voraz?", extra=1.5),
    Escena("En el código, euros guarda la fila anterior, con eme más uno casillas. "
           "Para cada tipo se calcula ka, la división entera de ge entre ce. "
           "La fila nueva empieza como una copia de la anterior: eso es te igual a cero. "
           "Para cada jota se prueban te bollos mientras quepan y no se pase de ka. "
           "Al terminar, la nueva fila pasa a ser la anterior, y se escribe euros de eme.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Errores típicos. Ka es una división entera: siete gramos y tres por bollo dan dos bollos. "
           f"Si se actualiza el mismo vector recorriendo jota hacia arriba, se mezclan bollos ya contados, y aquí saldrían {MAL} euros: cuatro bollos del tipo dos, con chorizo para dos. "
           "La solución es copiar la fila, o recorrer jota de eme hacia abajo. "
           "La respuesta es euros de eme, porque no hace falta gastar toda la masa. "
           "Y todo cabe en un entero; el coste es eme por la suma de los ka.",
           e_errores, titulo="Errores típicos", extra=1.5),
    Escena("Resumiendo: es una mochila acotada, con la masa como capacidad y ka sub i bollos de cada tipo. "
           "Cada casilla prueba todas las cantidades posibles del tipo i. "
           "Empieza en cero y la respuesta es bollos de ene, eme. "
           "Y se implementa con un vector por fila, copiando la anterior.",
           e_cierre, titulo="Resumen", extra=1.5),
]


def voz_estimada():
    """--preview sin Kokoro ni Piper: tiempos estimados (≈ 14,5 caracteres/s) en vez de sintetizar.
    Solo cambia anim._tts en este proceso; con voz instalada no hace nada."""
    import anim
    if os.environ.get("KOKORO_MODEL") or os.environ.get("PIPER_MODEL"):
        return
    def est(texto, wav):
        t, out = 0.0, []
        for fr in [x for x in re.split(r"(?<=[.:;?!])\s+", texto.strip()) if x]:
            d = len(fr) / 14.5
            out.append((fr, t, t + d))
            t += d + 0.22
        return t, out
    anim._tts = est
    tot = sum(max(e.dmin, est(e.narracion, None)[0] + e.extra) for e in ESC)
    print(f"(sin voz: tiempos estimados, duración ≈ {tot / 60:.1f} min)")


if __name__ == "__main__":
    if "--preview" in sys.argv:
        voz_estimada()
    args_preview(ESC, "preview/12-3", "../12-3_bollos_preñaos.mp4", "12-3")
