"""Vídeo EJ 11-2 · Aibofobia (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-2/EJ_11-2.cpp"
TEMA = "Tema 11 · Programación dinámica II"
S = "reconor"
n = len(S)


def calcula(s):
    m = len(s)
    F = [[0] * m for _ in range(m)]
    for d in range(1, m):
        for i in range(m - d):
            j = i + d
            F[i][j] = (F[i + 1][j - 1] if d >= 2 else 0) if s[i] == s[j] else 1 + min(F[i + 1][j], F[i][j - 1])
    return F


F = calcula(S)
ORDEN = [(i, i + d) for d in range(1, n) for i in range(n - d)]


def reconstruye():
    """Pasos: (tipo, i, j). Y las ranuras del resultado: lista de (pos, letra, añadida, paso)."""
    pasos, izq, der = [], [], []
    i, j = 0, n - 1
    while i <= j:
        q = len(pasos)
        if i == j:
            pasos.append(("centro", i, j)); izq.append((S[i], False, q)); i += 1
        elif S[i] == S[j]:
            pasos.append(("igual", i, j)); izq.append((S[i], False, q)); der.append((S[j], False, q)); i += 1; j -= 1
        elif F[i + 1][j] <= F[i][j - 1]:
            pasos.append(("izq", i, j)); izq.append((S[i], False, q)); der.append((S[i], True, q)); i += 1
        else:
            pasos.append(("der", i, j)); izq.append((S[j], True, q)); der.append((S[j], False, q)); j -= 1
    L = len(izq) + len(der)
    slots = [(k, c, a, q) for k, (c, a, q) in enumerate(izq)] + [(L - 1 - k, c, a, q) for k, (c, a, q) in enumerate(der)]
    return pasos, slots, L


PASOS, SLOTS, LRES = reconstruye()
RES = "".join(c for _, c, _, _ in sorted(SLOTS))
assert RES == RES[::-1] and len(RES) == n + F[0][n - 1]

GRIS = (30, 40, 62)
TB = Tabla(30, 92, n, n, cw=62, ch=56, lw=70, cabecera=[f"{c}" for c in S], etiquetas=[f"{c}" for c in S], tam=26)
BAJO = {(i, j): GRIS for i in range(n) for j in range(i)}


# ------------------------------------------------------------------ fichas
def ficha(f, x, y, c, u=1.0, col=None, borde=None, tam=56):
    if u <= 0:
        return
    col = col or C["text"]
    h = tam / 2
    f.d.rounded_rectangle((x - h, y - h, x + h, y + h), 8, fill=mix(C["bot"], (236, 222, 190), u),
                          outline=mix(C["bot"], borde or (150, 120, 80), u), width=4 if borde else 2)
    f.d.text((x, y + 2), c, font=font(int(tam * 0.6), True), fill=mix(C["bot"], col if col != C["text"] else (40, 30, 20), u), anchor="mm")


def fila(f, x0, y, s, sep=66, u=1.0, cols=None, bordes=None, tam=56):
    for k, c in enumerate(s):
        ficha(f, x0 + k * sep, y, c, u, col=(cols or {}).get(k), borde=(bordes or {}).get(k), tam=tam)


def espejo(f, x, y0, y1, u=1.0):
    if u <= 0:
        return
    yy = y0
    while yy < y1:
        f.d.line((x, yy, x, min(y1, yy + 12)), fill=mix(C["bot"], C["gold"], u), width=3)
        yy += 22


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        x0 = 800
        u = f.p(0.3, 0.8)
        fila(f, x0, 320, "damad", sep=72, u=u, bordes={0: NARANJA})
        espejo(f, x0 + 2 * 72, 260, 380, f.p(0.9, 0.6))
    portada(f, "EJ 11-2", "Aibofobia", TEMA, dib)


def e_problema(f):
    # "amad" -> "damad"
    x0, y = 440, 300
    sep = 80
    u_in = f.p(f.c(2), 1.0) if f.t >= f.c(2) else 0
    dx = sep * ease(u_in)
    if f.t >= f.c(0):
        fila(f, x0 + dx, y, "amad", sep=sep, u=aparece(f, f.c(0)))
    if f.t >= f.c(2):
        # la "d" nueva cae desde arriba a la izquierda
        yy = lerp(80, y, ease(f.p(f.c(2), 1.0)))
        ficha(f, x0, yy, "d", borde=NARANJA)
    if f.t >= f.c(1):
        texto(f, (640, 160), "¿palíndromo?  no" if f.t < f.c(2) + 1.2 else "¿palíndromo?  sí", 34, "red" if f.t < f.c(2) + 1.2 else "green", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2) + 1.2:
        espejo(f, x0 + 2 * sep, 230, 370, aparece(f, f.c(2) + 1.2))
        texto(f, (640, 450), "1 letra añadida", 34, "green", aparece(f, f.c(2) + 1.4), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 540), "mínimo de letras  +  un palíndromo que lo consiga", 26, "text", aparece(f, f.c(3)), anchor="mm")


def e_idea(f):
    sep = 80
    x0, y = 400, 200
    fila(f, x0, y, S, sep=sep)
    # punteros
    def puntero(k, col, u):
        if u <= 0:
            return
        x = x0 + k * sep
        f.d.polygon([(x, y + 44), (x - 12, y + 66), (x + 12, y + 66)], fill=mix(C["bot"], col, u))
    if f.t < f.c(2):
        u = aparece(f, f.c(0))
        puntero(0, C["gold"], u)
        puntero(n - 1, C["gold"], u)
        texto(f, (x0, y + 90), "i", 26, "gold", u, mono=True, anchor="mm")
        texto(f, (x0 + (n - 1) * sep, y + 90), "j", 26, "gold", u, mono=True, anchor="mm")
        if f.t >= f.c(1):
            u2 = aparece(f, f.c(1))
            a, b = x0, x0 + (n - 1) * sep
            f.d.arc((a, y - 120, b, y + 40), 200, 340, fill=mix(C["bot"], C["green"], u2), width=4)
            texto(f, (640, 70), "iguales: se emparejan  →  queda el interior", 26, "green", u2, anchor="mm")
            # el interior se ilumina
            for k in range(1, n - 1):
                xk = x0 + k * sep
                f.d.rectangle((xk - 30, y + 34, xk + 30, y + 38), fill=mix(C["bot"], C["blue"], u2))
    else:
        # e  c  o  n  o  →  e ... o   distintos
        u = aparece(f, f.c(2))
        puntero(1, C["gold"], u)
        puntero(n - 2, C["gold"], u)
        texto(f, (640, 70), "distintos (e ≠ o): a uno de los dos le ponemos pareja", 26, NARANJA, u, anchor="mm")
        # opción A: copiar 'e' al otro lado
        ya, yb = 400, 560
        if f.t >= f.c(3):
            ua = aparece(f, f.c(3))
            texto(f, (70, ya), "A", 34, "blue", ua, anchor="mm")
            fila(f, 160, ya, "econo", sep=62, u=ua, tam=48)
            ficha(f, 160 + 5 * 62, ya, "e", ua, borde=NARANJA, tam=48)
            texto(f, (560, ya), "→ queda  cono", 26, "blue", ua, anchor="lm")
            texto(f, (840, ya), "1 + faltan(i+1, j)", 26, "blue", ua, mono=True, anchor="lm")
        if f.t >= f.c(4):
            ub = aparece(f, f.c(4))
            texto(f, (70, yb), "B", 34, NARANJA, ub, anchor="mm")
            ficha(f, 160, yb, "o", ub, borde=NARANJA, tam=48)
            fila(f, 160 + 62, yb, "econo", sep=62, u=ub, tam=48)
            texto(f, (560, yb), "→ queda  econ", 26, NARANJA, ub, anchor="lm")
            texto(f, (840, yb), "1 + faltan(i, j−1)", 26, NARANJA, ub, mono=True, anchor="lm")
        if f.t >= f.c(5):
            texto(f, (640, 660), "nos quedamos con la que necesite menos", 28, "gold", aparece(f, f.c(5)), anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 80), "faltan(i, j) = mínimo de letras a añadir para que s[i..j] sea palíndromo", 24, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (60, 150), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 195, "faltan(i, j) =", [("0", "si i ≥ j   (una letra o nada)")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia  (i < j)", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 76, "faltan(i, j) =", [("faltan(i+1, j−1)", "si s[i] = s[j]"),
                                                  ("1 + min( faltan(i+1, j),  faltan(i, j−1) )", "si s[i] ≠ s[j]")],
                aparece(f, f.c(2)), size=24, colores=[C["green"], NARANJA])
    texto(f, (60, y + 40), "Respuesta:  faltan(0, n−1)", 28, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 90), "Se rellena por diagonales: intervalos cada vez más largos", 24, "text", aparece(f, f.c(4)))


def e_tabla(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    nn = int((f.t - t0) / paso) if f.t >= t0 else 0
    nn = max(0, min(nn, len(ORDEN)))
    vals = {(i, i): 0 for i in range(n)}
    for (i, j) in ORDEN[:nn]:
        vals[(i, j)] = F[i][j]
    sombra = dict(BAJO)
    marca = {}
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= t0 else None
    if f.t < t0:
        for i in range(n):
            sombra[(i, i)] = mix(C["panel"], C["green"], 0.5 * aparece(f, f.c(0)))
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw + n * TB.cw / 2, 80), "j  →", 20, "muted", 1, anchor="mm")
    texto(f, (TB.x0 + 14, TB.y0 + 40 + n * TB.ch / 2), "i", 22, "muted", 1, anchor="mm")
    # la palabra con el intervalo actual
    xw, yw = 640, 150
    for k, c in enumerate(S):
        dentro = cur and cur[0] <= k <= cur[1]
        borde = None
        if cur and k in cur:
            borde = C["green"] if S[cur[0]] == S[cur[1]] else NARANJA
        ficha(f, xw + 30 + k * 66, yw, c, 1 if (dentro or not cur) else 0.35, borde=borde)
    if cur:
        i, j = cur
        marca[cur] = "gold"
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        if S[i] == S[j]:
            if j - i >= 2:
                TB.flecha_entre(f, (i + 1, j - 1), cur, C["green"], u=u)
            s = f"{S[i]} = {S[j]}"
            texto(f, (xw + 30 + 3 * 66, 240), s, 30, "green", 1, mono=True, anchor="mm")
        else:
            TB.flecha_entre(f, (i + 1, j), cur, AZUL, u=u)
            TB.flecha_entre(f, (i, j - 1), cur, NARANJA, u=u)
            texto(f, (xw + 30 + 3 * 66, 240), f"{S[i]} ≠ {S[j]}:  1 + min", 30, NARANJA, 1, mono=True, anchor="mm")
        TB.dibuja(f, vals, marca=marca, sombra=sombra)
        if S[i] == S[j]:
            if j - i >= 2:
                TB.flecha_entre(f, (i + 1, j - 1), cur, C["green"], u=u)
        else:
            TB.flecha_entre(f, (i + 1, j), cur, AZUL, u=u)
            TB.flecha_entre(f, (i, j - 1), cur, NARANJA, u=u)
    if f.t >= t1:
        TB.dibuja(f, vals, marca={(0, n - 1): "green"}, sombra=sombra)
        texto(f, (xw + 30 + 3 * 66, 330), f"faltan(0, {n - 1}) = {F[0][n - 1]}", 34, "green", aparece(f, t1), mono=True, anchor="mm")


def e_reconstruye(f):
    vals = {(i, j): F[i][j] for i in range(n) for j in range(i, n)}
    t0 = f.c(1)
    paso = (f.c(4) - t0) / len(PASOS)
    q = int((f.t - t0) / paso) if f.t >= t0 else -1
    q = min(q, len(PASOS) - 1)
    marca = {}
    if q >= 0:
        tipo, i, j = PASOS[q]
        marca[(i, j)] = "gold"
    TB.dibuja(f, vals, marca=marca, sombra=BAJO)
    for k in range(max(0, q)):
        tipo, i, j = PASOS[k]
        dest = {"igual": (i + 1, j - 1), "izq": (i + 1, j), "der": (i, j - 1)}.get(tipo)
        if dest and dest[0] <= dest[1] or tipo == "igual" and dest:
            if dest[0] < n and dest[1] >= 0:
                TB.flecha_entre(f, (i, j), dest, C["green"] if tipo == "igual" else (AZUL if tipo == "izq" else NARANJA))
    # explicación del paso
    xw = 640
    if q >= 0:
        tipo, i, j = PASOS[q]
        s = {"igual": f"{S[i]} = {S[j]}: una a cada lado",
             "izq": f"{S[i]} ≠ {S[j]}: pareja para la {S[i]}",
             "der": f"{S[i]} ≠ {S[j]}: pareja para la {S[j]}",
             "centro": f"queda la {S[i]}: va en el centro"}[tipo]
        texto(f, (xw + 300, 200), s, 28, "green" if tipo in ("igual", "centro") else NARANJA, 1, anchor="mm")
        if tipo in ("izq", "der"):
            a, b = F[i + 1][j], F[i][j - 1]
            texto(f, (xw + 300, 250), f"faltan(i+1, j) = {a}   faltan(i, j−1) = {b}", 22, "muted", 1, mono=True, anchor="mm")
    # ranuras del resultado
    sep = 62
    x0 = 640 - (LRES - 1) * sep / 2
    y = 645
    for k in range(LRES):
        xx = x0 + k * sep
        f.d.rounded_rectangle((xx - 27, y - 27, xx + 27, y + 27), 8, outline=C["border"], width=2)
    for pos, c, añadida, qq in SLOTS:
        if f.t >= t0 + qq * paso:
            u = f.lin(t0 + qq * paso, 0.5)
            xx = x0 + pos * sep
            ficha(f, xx, lerp(y - 80, y, ease(u)), c, borde=NARANJA if añadida else None, tam=54)
    if f.t >= f.c(4):
        texto(f, (640, 565), f"{F[0][n - 1]}  {RES}", 40, "green", aparece(f, f.c(4)), mono=True, anchor="mm")
        texto(f, (640, 700), "con borde naranja: las letras añadidas", 20, "muted", aparece(f, f.c(4)), anchor="mm")


A = find_line(CPP, "Matriz<int> faltan(n")
B = find_line(CPP, "cout << faltan[0][n - 1]")
CODE = codigo(CPP, A, B, maxc=92)
L_EQ = find_line(CPP, "if (s[i] == s[j]) faltan[i][j]")
L_NE = find_line(CPP, "else faltan[i][j] = 1 + min(")
L_C = find_line(CPP, "if (i == j) { izq += s[i]; ++i; }")
L_IG = find_line(CPP, "else if (s[i] == s[j]) { izq += s[i]; der += s[j];")
L_IZ = find_line(CPP, "else if (faltan[i + 1][j] <= faltan[i][j - 1])")
L_DE = find_line(CPP, "else { izq += s[j]; der += s[j]; --j; }")
L_REV = find_line(CPP, "reverse(der.begin(), der.end());")
TBC = Tabla(900, 150, n, n, cw=44, ch=40, lw=0, cabecera=list(S), etiquetas=[""] * n, tam=18)


def e_codigo(f):
    hl = {A}
    vals = {(i, i): 0 for i in range(n)}
    marca = {}
    t0, t1 = f.c(1), f.c(2)
    izq = der = ""
    if t0 <= f.t < t1:
        paso = (t1 - t0) / len(ORDEN)
        k = min(len(ORDEN) - 1, int((f.t - t0) / paso))
        for (i, j) in ORDEN[:k]:
            vals[(i, j)] = F[i][j]
        i, j = ORDEN[k]
        marca[(i, j)] = "gold"
        hl = {L_EQ} if S[i] == S[j] else {L_NE}
    elif f.t >= t1:
        vals = {(i, j): F[i][j] for i in range(n) for j in range(i, n)}
        t2 = f.T - 4.0
        paso = (t2 - t1) / len(PASOS)
        k = min(len(PASOS) - 1, int((f.t - t1) / paso))
        tipo, i, j = PASOS[k]
        marca[(i, j)] = "gold"
        hl = {{"centro": L_C, "igual": L_IG, "izq": L_IZ, "der": L_DE}[tipo]}
        if f.t >= t2:
            hl = {L_REV, B}
        # izq / der construidos hasta el paso k (incluido)
        for qq in range(k + 1):
            tp, a, b = PASOS[qq]
            if tp == "centro":
                izq += S[a]
            elif tp == "igual":
                izq += S[a]; der += S[b]
            elif tp == "izq":
                izq += S[a]; der += S[a]
            else:
                izq += S[b]; der += S[b]
    f.code(10, 84, 866, 560, CODE, hl=hl, title="tabla y reconstrucción", size=15)
    TBC.dibuja(f, vals, marca=marca, sombra=BAJO)
    if f.t >= t1:
        texto(f, (900, 500), f"izq = \"{izq}\"", 24, "blue", 1, mono=True)
        texto(f, (900, 540), f"der = \"{der}\"", 24, NARANJA, 1, mono=True)
        if f.t >= f.T - 4.0:
            texto(f, (900, 600), f"{izq} + {der[::-1]}", 26, "green", aparece(f, f.T - 4.0), mono=True)


def e_detalles(f):
    f.box(40, 110, 580, 420, "casos")
    f.box(660, 110, 580, 420, "detalles")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        fila(f, 110, 200, "radar", sep=62, u=u, tam=48)
        texto(f, (450, 200), "→ 0", 30, "green", u, mono=True, anchor="lm", fondo=C["panel"])
        fila(f, 110, 290, "x", sep=62, u=u, tam=48)
        texto(f, (450, 290), "→ 0", 30, "green", u, mono=True, anchor="lm", fondo=C["panel"])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (80, 380), "empate: vale cualquiera", 26, "text", u, fondo=C["panel"])
        texto(f, (80, 425), "abeja → abejeba  (o ajebeja…)", 22, "muted", u, mono=True, fondo=C["panel"])
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (690, 180), "der se construye al revés:", 24, "text", u, fondo=C["panel"])
        texto(f, (690, 220), "al final  izq + reverse(der)", 24, "gold", u, mono=True, fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 320), "O(n²) tiempo y memoria", 28, "gold", u, fondo=C["panel"])
        texto(f, (690, 360), "n ≤ 1000  →  un millón de casillas", 22, "muted", u, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Aibofobia", [
        "PD sobre intervalos: faltan(i, j) para s[i..j]",
        "extremos iguales → interior;  distintos → 1 + min",
        "se rellena por diagonales, de cortos a largos",
        "reconstruir desde (0, n−1) poniendo letras a los dos lados",
    ])


ESC = [
    Escena("Aibofobia. Cuántas letras hay que añadir a una palabra para que sea un palíndromo.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos una palabra, por ejemplo, amad. "
           "No se lee igual al revés. "
           "Pero si le añadimos una de delante, queda damad, que sí es un palíndromo: una sola letra. "
           "Hay que decir el mínimo de letras que hay que añadir, en cualquier posición, y un palíndromo que lo consiga.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("La idea es mirar los dos extremos. "
           "En reconor, la primera y la última son erre: se emparejan entre sí, y solo queda arreglar lo de dentro. "
           "Ahora los extremos son e y o, distintos. Una de las dos se quedará sin pareja, así que hay que añadirle una copia. "
           "Opción A: ponemos otra e al final, y queda por arreglar cono. "
           "Opción B: ponemos otra o al principio, y queda e ce o ene. "
           "Nos quedamos con la que necesite menos letras.",
           e_idea, titulo="Mirar los extremos", extra=1.5),
    Escena("Faltan de i, j es el mínimo de letras para que el trozo de i a j sea palíndromo. "
           "Caso base: si el trozo tiene una letra o ninguna, ya es palíndromo, cero. "
           "Si los extremos son iguales, faltan del interior. Si son distintos, uno más el mínimo de quitar el extremo izquierdo o el derecho. "
           "La respuesta es faltan de cero, ene menos uno. "
           "Cada casilla usa intervalos más cortos, así que se rellena por diagonales.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("La tabla es un triángulo: solo tienen sentido las casillas con i menor o igual que j, y la diagonal son ceros. "
           "Vamos diagonal a diagonal: primero los trozos de dos letras, luego de tres, y así. "
           "Si los extremos son iguales, se copia la casilla de abajo a la izquierda; si no, uno más la menor entre la de abajo y la de la izquierda. "
           "La esquina de arriba a la derecha dice que a reconor le faltan dos letras.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Ahora construimos el palíndromo a la vez por los dos lados. "
           "Si los extremos son iguales, uno va a la izquierda y otro a la derecha. "
           "Si son distintos, se mira qué opción daba el mínimo y esa letra se pone en los dos lados: una es la original y la otra es añadida. "
           "Y si queda una letra sola, va en el centro. "
           "Sale reconocer: dos letras añadidas.",
           e_reconstruye, titulo="Construir el palíndromo", extra=2.0),
    Escena("En el código, faltan es una matriz de ene por ene, y el bucle exterior recorre la distancia de entre i y j, es decir, las diagonales. "
           "Después, con dos índices que se acercan, se van llenando dos cadenas: izq por la izquierda y der por la derecha. "
           "Al final, der se da la vuelta y se pega detrás de izq.",
           e_codigo, titulo="El código", extra=5.0),
    Escena("Si la palabra ya es palíndromo, por ejemplo radar, o tiene una sola letra, la respuesta es cero. "
           "Cuando las dos opciones empatan, vale cualquiera de los palíndromos. "
           "La cadena der se construye al revés, por eso se le da la vuelta al final. "
           "El coste es ene al cuadrado en tiempo y memoria: con mil letras, un millón de casillas, que cabe sin problema.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es programación dinámica sobre intervalos. "
           "Extremos iguales, se pasa al interior; distintos, uno más el mínimo. "
           "Se rellena por diagonales. "
           "Y el palíndromo se reconstruye desde la esquina poniendo letras a los dos lados.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-2", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-2: {build(ESC, '../11-2_aibofobia.mp4'):.0f}s")
