"""Vídeo EJ 10-1 · La cuerda de la cometa (animado)."""
import math
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../10-Programacion dinamica/EJ_10-1/EJ_10-1.cpp"
TEMA = "Tema 10 · Programación dinámica"
L = 10
CORD = [(10, 50), (5, 10), (5, 10)]          # ejemplo 4: (longitud, coste)
COLC = [(236, 150, 64), (86, 156, 230), (178, 120, 220)]
INF = None


def tablas(cords, L):
    n = len(cords)
    fo = [[0] * (L + 1) for _ in range(n + 1)]
    co = [[INF] * (L + 1) for _ in range(n + 1)]
    cs = [[INF] * (L + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        fo[i][0], co[i][0], cs[i][0] = 1, 0, 0
    for i in range(1, n + 1):
        l, c = cords[i - 1]
        for j in range(1, L + 1):
            fo[i][j], co[i][j], cs[i][j] = fo[i - 1][j], co[i - 1][j], cs[i - 1][j]
            if l <= j and fo[i - 1][j - l] > 0:
                fo[i][j] += fo[i - 1][j - l]
                a = co[i - 1][j - l] + 1
                b = cs[i - 1][j - l] + c
                co[i][j] = a if co[i][j] is INF else min(co[i][j], a)
                cs[i][j] = b if cs[i][j] is INF else min(cs[i][j], b)
    return fo, co, cs


FO, CO, CS = tablas(CORD, L)
ORDEN = [(i, j) for i in range(1, 4) for j in range(1, L + 1)]
ETQ = ["ninguno", "{10}", "{10, 5}", "{10, 5, 5}"]
TF = Tabla(40, 170, 4, L + 1, cw=72, ch=64, lw=150, etiquetas=ETQ, tam=26)


def cordel(f, x, y, l, col, escala=40, u=1.0, etq=None):
    if u <= 0:
        return
    w = l * escala * ease(u)
    pts = []
    for k in range(int(w // 6) + 2):
        xx = x + min(w, k * 6)
        pts.append((xx, y + 3 * math.sin(k * 1.3)))
    f.d.line(pts, fill=col, width=7, joint="curve")
    if etq and u >= 1:
        f.d.text((x + w / 2, y - 16), etq, font=font(20, True), fill=col, anchor="ms")


def cometa(f, x, y, s=1.0, u=1.0):
    if u <= 0:
        return
    c1, c2 = mix(C["bot"], (255, 110, 90), u), mix(C["bot"], (255, 206, 92), u)
    pts = [(x, y - 70 * s), (x + 50 * s, y), (x, y + 90 * s), (x - 50 * s, y)]
    f.d.polygon(pts, fill=c1)
    f.d.polygon([pts[0], pts[1], (x, y)], fill=c2)
    f.d.polygon([pts[2], pts[3], (x, y)], fill=c2)
    f.d.line((x, y - 70 * s, x, y + 90 * s), fill=(60, 30, 30), width=2)
    for k in range(3):
        bx = x - 10 + k * 8
        f.d.polygon([(bx, y + 110 * s + k * 26), (bx + 10, y + 100 * s + k * 26), (bx + 10, y + 120 * s + k * 26)], fill=c2)


def regla(f, x, y, L, escala=40, u=1.0):
    if u <= 0:
        return
    col = mix(C["bot"], C["muted"], u)
    f.d.line((x, y, x + L * escala, y), fill=col, width=2)
    for k in range(L + 1):
        h = 12 if k % 5 == 0 else 6
        f.d.line((x + k * escala, y - h, x + k * escala, y + h), fill=col, width=2)
        if k % 5 == 0:
            f.d.text((x + k * escala, y + 26), str(k), font=font(18, True), fill=col, anchor="mm")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        cometa(f, 1000, 230, 1.2, f.p(0.2, 0.8))
        f.d.line((1000, 340, 1000 - 220, 640), fill=(220, 220, 230), width=2)
    portada(f, "EJ 10-1", "La cuerda de la cometa", TEMA, dib)


def e_problema(f):
    cometa(f, 1080, 200, 1.0, aparece(f, f.c(0), 0.8))
    # cordeles sobre la mesa
    for k, (l, c) in enumerate(CORD):
        cordel(f, 80, 200 + 70 * k, l, COLC[k], escala=40, u=aparece(f, f.c(1) + 0.3 * k, 0.8), etq=f"{l}  ·  {c} €")
    if f.t >= f.c(2):
        regla(f, 80, 470, L, u=aparece(f, f.c(2)))
        texto(f, (80 + L * 40 + 30, 470), f"L = {L}", 28, "gold", aparece(f, f.c(2)), anchor="lm")
    qs = [("∑", "¿cuántas formas?"), ("#", "¿mínimo de cordeles?"), ("€", "¿mínimo coste?")]
    for k, (ic, q) in enumerate(qs):
        t0 = f.c(3) + 0.8 * k
        if f.t >= t0:
            u = aparece(f, t0)
            x = 140 + 380 * k
            f.d.ellipse((x - 34, 560, x + 34, 628), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], C["gold"], u), width=3)
            f.d.text((x, 594), ic, font=font(32, True), fill=mix(C["bot"], C["gold"], u), anchor="mm")
            f.d.text((x + 50, 594), q, font=font(22, True), fill=mix(C["bot"], C["text"], u), anchor="lm")


def e_ejemplo(f):
    regla(f, 380, 560, L, escala=50)
    texto(f, (80, 140), "forma 1", 24, "muted", aparece(f, f.c(0)))
    cordel(f, 380, 200, 10, COLC[0], escala=50, u=aparece(f, f.c(0) + 0.3, 0.9), etq="10 · 50 €")
    texto(f, (80, 290), "forma 2", 24, "muted", aparece(f, f.c(1)))
    cordel(f, 380, 350, 5, COLC[1], escala=50, u=aparece(f, f.c(1) + 0.3, 0.7), etq="5 · 10 €")
    cordel(f, 630, 350, 5, COLC[2], escala=50, u=aparece(f, f.c(1) + 1.0, 0.7), etq="5 · 10 €")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (940, 160), "formas = 2", 30, "text", u, mono=True)
        texto(f, (940, 220), "cordeles = 1", 30, "text", aparece(f, f.c(2) + 0.8), mono=True)
        texto(f, (940, 280), "coste = 20", 30, "text", aparece(f, f.c(2) + 1.6), mono=True)
    if f.t >= f.c(3):
        texto(f, (940, 380), "SI 2 1 20", 36, "green", aparece(f, f.c(3)), mono=True)
        texto(f, (940, 440), "cada pregunta, por separado", 22, "muted", aparece(f, f.c(3) + 0.5))


def e_recurrencia(f):
    texto(f, (60, 76), "con los cordeles 1..i y la longitud j:", 24, "muted", aparece(f, f.c(0)), bold=False)
    y = formula(f, 70, 120, "formas(i, j) =", [("formas(i−1, j)", "si l_i > j"),
                                               ("formas(i−1, j) + formas(i−1, j − l_i)", "si l_i ≤ j")],
                aparece(f, f.c(1)), size=24)
    y = formula(f, 70, y + 26, "cordeles(i, j) =", [("cordeles(i−1, j)", "si l_i > j"),
                                                   ("min( cordeles(i−1, j), cordeles(i−1, j − l_i) + 1 )", "si l_i ≤ j")],
                aparece(f, f.c(2)), size=22)
    y = formula(f, 70, y + 26, "coste(i, j) =", [("coste(i−1, j)", "si l_i > j"),
                                                ("min( coste(i−1, j), coste(i−1, j − l_i) + c_i )", "si l_i ≤ j")],
                aparece(f, f.c(2) + 1.0), size=22)
    texto(f, (60, y + 28), "Base:  formas(i, 0) = 1,  cordeles(i, 0) = coste(i, 0) = 0;   fila 0 con j > 0:  0  y  ∞", 22, "gold",
          aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 76), "Respuesta:  formas(N, L) = 0 → NO;   si no  SI formas cordeles coste", 22, "green",
          aparece(f, f.c(4)), mono=True)


def e_tabla(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    k = int((f.t - t0) / paso) if f.t >= t0 else 0
    k = max(0, min(k, len(ORDEN)))
    vals = {(0, j): FO[0][j] for j in range(L + 1)}
    for i in range(1, 4):
        vals[(i, 0)] = 1
    for (i, j) in ORDEN[:k]:
        vals[(i, j)] = FO[i][j]
    marca, sombra = {}, {}
    cur = ORDEN[k] if k < len(ORDEN) and f.t >= t0 else None
    if cur:
        i, j = cur
        l = CORD[i - 1][0]
        marca[cur] = "gold"
        sombra[(i - 1, j)] = AZUL
        if j - l >= 0:
            sombra[(i - 1, j - l)] = NARANJA
    colores = {(i, j): C["dim"] for (i, j), v in vals.items() if v == 0}
    TF.dibuja(f, vals, marca=marca, sombra=sombra, colores=colores)
    if cur:
        i, j = cur
        l = CORD[i - 1][0]
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        TF.flecha_entre(f, (i - 1, j), cur, AZUL, u=u)
        if j - l >= 0:
            TF.flecha_entre(f, (i - 1, j - l), cur, NARANJA, u=u)
        texto(f, (640, 560), f"cordel de {l}:  no usarlo ↓   o usarlo ↘ (fila de arriba, {l} columnas antes)", 22, "text", 1, anchor="mm")
    if f.t >= f.c(3):
        TF.dibuja(f, vals, marca={(3, L): "green"}, colores=colores)
        texto(f, (640, 580), "formas(3, 10) = 2", 34, "green", aparece(f, f.c(3)), mono=True, anchor="mm")


def e_diferencia(f):
    # izquierda: dianas (misma fila) — derecha: cometa (fila de arriba)
    for k, (tit, misma, col) in enumerate((("dianas · se repite", True, C["blue"]), ("cometa · una vez", False, NARANJA))):
        x0 = 90 + k * 600
        u = aparece(f, f.c(k), 0.6)
        texto(f, (x0, 150), tit, 28, col, u)
        tb = Tabla(x0, 200, 2, 4, cw=100, ch=86, lw=0, cabecera=["", "j − p", "", "j"], etiquetas=["", ""], tam=26)
        tb.dibuja(f, {}, u=u, marca={(1, 3): "gold"} if u > 0 else None)
        if u > 0:
            de = (1, 1) if misma else (0, 1)
            tb.flecha_entre(f, de, (1, 3), col, u=f.lin(f.c(k) + 0.4, 0.8))
            tb.flecha_entre(f, (0, 3), (1, 3), AZUL, u=f.lin(f.c(k) + 0.4, 0.8))
            texto(f, (x0, 430), "misma fila i" if misma else "fila i − 1", 26, "text", aparece(f, f.c(k) + 1.0), mono=True)
    if f.t >= f.c(2):
        texto(f, (W / 2, 560), "cada cordel solo se puede usar una vez", 30, "gold", aparece(f, f.c(2)), anchor="mm")


def e_vector(f):
    # vector formas con los cordeles 10 y 5 ya metidos; ahora se añade el segundo 5
    base = FO[2][:]
    ok = FO[3][:]
    x0, y0, cw = 120, 180, 92
    def vec(y, vals, hl=None, cols=None, titulo=""):
        texto(f, (x0, y - 40), titulo, 24, "muted", 1)
        for j in range(L + 1):
            x = x0 + j * cw
            ccol = C["gold"] if hl == j else C["border"]
            f.d.rectangle((x, y, x + cw - 8, y + 70), fill=C["panel"], outline=ccol, width=4 if hl == j else 2)
            v = vals[j]
            col = (cols or {}).get(j, C["text"] if v else C["dim"])
            f.d.text((x + (cw - 8) / 2, y + 35), str(v), font=font(28, True), fill=col, anchor="mm")
            f.d.text((x + (cw - 8) / 2, y + 88), str(j), font=font(16, True), fill=C["dim"], anchor="mm")
    # mal: de izquierda a derecha
    if f.t >= f.c(1):
        mal = base[:]
        prog = f.lin(f.c(1) + 0.3, 3.0)
        js = list(range(5, L + 1))
        n = int(prog * len(js))
        for j in js[:n]:
            mal[j] += mal[j - 5]
        cols = {}
        if n > len(js) - 1:
            cols[10] = C["red"]
        vec(y0, mal, hl=js[n] if n < len(js) else None, cols=cols, titulo="izquierda → derecha  (mal)")
        if n >= len(js):
            texto(f, (x0 + 11 * cw + 10, y0 + 35), "✗", 40, "red", 1, anchor="lm")
            texto(f, (x0, y0 + 120), "formas[10] usa formas[5] ya actualizado: el mismo 5 dos veces", 22, "red", aparece(f, f.c(1) + 3.4))
    if f.t >= f.c(2):
        bien = base[:]
        prog = f.lin(f.c(2) + 0.3, 3.0)
        js = list(range(L, 4, -1))
        n = int(prog * len(js))
        for j in js[:n]:
            bien[j] += bien[j - 5]
        vec(y0 + 230, bien, hl=js[n] if n < len(js) else None, titulo="derecha → izquierda  (bien)")
        if n >= len(js):
            texto(f, (x0 + 11 * cw + 10, y0 + 265), "✓", 40, "green", 1, anchor="lm")
    if f.t >= f.c(0) and f.t < f.c(1):
        vec(y0, base, titulo="formas con {10, 5}; añadimos el otro 5")


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "else cout << \"SI \"")
CODE = codigo(CPP, A, B + 1, maxc=78)
L_INI = find_line(CPP, "formas[0] = 1; cordeles[0] = 0; coste[0] = 0;")
L_FORJ = find_line(CPP, "for (int j = L; j >= l; --j) {")
L_UPD = [find_line(CPP, "formas[j] += formas[j - l];"), find_line(CPP, "cordeles[j] = min(cordeles[j], cordeles[j - l] + 1);"),
         find_line(CPP, "coste[j] = min(coste[j], coste[j - l] + c);")]
L_OUT = B


def e_codigo(f):
    # pasos: (cordel k, j) con j de L a l
    pasos = [(k, j) for k, (l, c) in enumerate(CORD) for j in range(L, l - 1, -1)]
    t0, t1 = f.c(1), f.T - 3.0
    paso = (t1 - t0) / len(pasos)
    n = int((f.t - t0) / paso) if f.t >= t0 else -1
    n = min(n, len(pasos))
    fo = [1] + [0] * L
    co = [0] + [None] * L
    cs = [0] + [None] * L
    for (k, j) in pasos[:max(0, n)]:
        l, c = CORD[k]
        if fo[j - l] == 0:
            continue
        fo[j] += fo[j - l]
        co[j] = co[j - l] + 1 if co[j] is None else min(co[j], co[j - l] + 1)
        cs[j] = cs[j - l] + c if cs[j] is None else min(cs[j], cs[j - l] + c)
    hl, cur = {L_INI}, None
    if 0 <= n < len(pasos):
        k, j = pasos[n]
        cur = (k, j)
        l = CORD[k][0]
        hl = set(L_UPD)
    elif n >= len(pasos):
        hl = {L_OUT}
    f.code(16, 84, 700, 520, CODE, hl=hl, title="resuelveCaso()", size=15)
    x0, cw = 740, 48
    for r, (nom, vec) in enumerate((("formas", fo), ("cordeles", co), ("coste", cs))):
        y = 150 + r * 150
        texto(f, (x0, y - 34), nom, 22, "muted", 1, mono=True)
        for j in range(L + 1):
            x = x0 + j * cw
            hlc = cur is not None and j == cur[1]
            hlo = cur is not None and j == cur[1] - CORD[cur[0]][0]
            colb = C["gold"] if hlc else (NARANJA if hlo else C["border"])
            f.d.rectangle((x, y, x + cw - 4, y + 56), fill=C["panel"], outline=colb, width=3 if (hlc or hlo) else 1)
            v = vec[j]
            s = "∞" if v is None else str(v)
            f.d.text((x + (cw - 4) / 2, y + 28), s, font=font(20, True), fill=C["dim"] if v in (None, 0) and r == 0 or v is None else C["text"], anchor="mm")
    if cur:
        l, c = CORD[cur[0]]
        texto(f, (x0, 590), f"cordel {cur[0] + 1}: longitud {l}, coste {c}   ·   j = {cur[1]}", 22, "gold", 1)
    elif n >= len(pasos):
        texto(f, (x0, 590), "SI 2 1 20", 34, "green", aparece(f, t1), mono=True)


def e_detalles(f):
    f.box(40, 110, 580, 400, "cordeles iguales, distintos")
    f.box(660, 110, 580, 400, "detalles")
    if f.t >= f.c(0):
        for k, (a, b) in enumerate(((0, 1), (0, 2), (1, 2))):
            y = 190 + 90 * k
            u = aparece(f, f.c(0) + 0.5 + 0.6 * k)
            for q in range(3):
                col = COLC[q] if q in (a, b) else (60, 70, 90)
                cordel(f, 90 + q * 150, y, 3, col, escala=40, u=u if q in (a, b) else min(u, 1))
        texto(f, (330, 470), "3 formas de hacer 2", 26, "gold", aparece(f, f.c(0) + 2.5), anchor="mm", fondo=C["panel"])
    if f.t >= f.c(1):
        texto(f, (690, 180), "long long", 30, "text", aparece(f, f.c(1)), mono=True, fondo=C["panel"])
        texto(f, (690, 222), "hasta 10¹⁸ formas", 22, "muted", aparece(f, f.c(1)), fondo=C["panel"])
    if f.t >= f.c(2):
        texto(f, (690, 300), "formas[j−l] == 0 → continue", 26, "text", aparece(f, f.c(2)), mono=True, fondo=C["panel"])
        texto(f, (690, 342), "así nunca se calcula ∞ + 1", 22, "muted", aparece(f, f.c(2)), fondo=C["panel"])
    if f.t >= f.c(3):
        texto(f, (690, 420), "O(N · L) tiempo,  O(L) memoria", 26, "gold", aparece(f, f.c(3)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "La cuerda de la cometa", [
        "mochila 0/1 de suma exacta: cada cordel, como mucho una vez",
        "usar el cordel i mira la fila i − 1, l_i columnas a la izquierda",
        "formas suma;  cordeles y coste se quedan con el mínimo",
        "un vector recorrido de L hacia abajo:  O(N·L)",
    ])


ESC = [
    Escena("La cuerda de la cometa. Un problema de programación dinámica con tres preguntas sobre la misma tabla.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Tres amigos quieren hacerle una cometa a un niño, pero no tienen tijeras. "
           "Tienen cordeles de distintas longitudes, cada uno con su precio, y hay que unir algunos para que sumen exactamente la longitud ele. "
           "Cada cordel se puede usar una sola vez. "
           "Y cada uno pregunta algo distinto: cuántas formas hay de hacerlo, cuál es el mínimo número de cordeles, y cuál es el mínimo coste.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("En el cuarto ejemplo hay que formar una cuerda de diez con un cordel de diez, que cuesta cincuenta, y dos de cinco, que cuestan diez cada uno. "
           "Hay dos formas: el de diez solo, o los dos de cinco. "
           "La de menos cordeles es la del cordel de diez, pero la más barata es la de los dos de cinco, que cuesta veinte. "
           "Cada pregunta se responde por separado: sí, dos, uno, veinte.",
           e_ejemplo, titulo="El ejemplo", extra=1.5),
    Escena("Las tres funciones miran lo mismo: los cordeles del uno al i, y la longitud jota. "
           "Para el cordel i hay dos opciones: no usarlo, y queda lo de la fila de arriba con la misma longitud, o usarlo, y queda formar jota menos su longitud con los anteriores. "
           "Formas suma las dos opciones; cordeles y coste se quedan con la menor, sumando un cordel o su precio. "
           "Casos base: la longitud cero se forma de una manera, sin cordeles y sin coste; y sin ningún cordel, ninguna otra longitud. "
           "La respuesta está en la casilla ene, ele: si no hay ninguna forma, no.",
           e_recurrencia, titulo="Recurrencias", extra=2.0),
    Escena("Rellenamos la tabla de formas fila a fila. "
           "Cada casilla suma la de arriba, que es no usar el cordel, y la de arriba desplazada tantas columnas como mide el cordel, que es usarlo. "
           "Al añadir el primer cinco aparece una forma de hacer cinco; con el segundo, dos formas de hacer cinco y dos de hacer diez. "
           "La respuesta: dos formas.",
           e_tabla, titulo="La tabla de formas", extra=2.5),
    Escena("Compáralo con el problema de las dianas. Allí un sector se podía repetir, así que la opción de usarlo miraba en la misma fila. "
           "Aquí cada cordel se usa una sola vez, así que mira en la fila de arriba. "
           "Esa es toda la diferencia entre poder repetir y no poder.",
           e_diferencia, titulo="Repetir o no", extra=1.5),
    Escena("En el código basta un vector por función, pero hay que recorrerlo en el orden correcto. "
           "Si lo recorremos de izquierda a derecha, al llegar a diez ya hemos actualizado la casilla cinco con este mismo cordel, y lo estaríamos usando dos veces. "
           "De derecha a izquierda, la casilla de la que tiramos todavía tiene el valor de la fila anterior, y cada cordel cuenta una sola vez.",
           e_vector, titulo="Por qué al revés", extra=2.0),
    Escena("El código inicializa la casilla cero: una forma, cero cordeles, coste cero. El resto empieza en cero formas e infinito. "
           "Para cada cordel, recorre jota desde ele hasta su longitud, hacia abajo. "
           "Suma las formas y actualiza los dos mínimos, que son enteros con infinito, de la cabecera EnterosInf: si jota menos ele no se puede formar, siguen en infinito. "
           "Al final escribe no, o sí con las tres respuestas.",
           e_codigo, titulo="El código", extra=3.0),
    Escena("Detalles. Dos cordeles de la misma longitud son distintos: en el tercer ejemplo, tres cordeles de uno dan tres formas de hacer dos. "
           "El número de formas puede ser enorme, hasta diez elevado a dieciocho: long long. "
           "Con los enteros con infinito, sumar uno a infinito sigue siendo infinito, así que no hay que comprobar nada antes de sumar. "
           "Y el coste es ene por ele en tiempo, y ele en memoria.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es una mochila cero uno de suma exacta. "
           "Usar el cordel i mira la fila de arriba, tantas columnas atrás como mide. "
           "Formas suma, cordeles y coste toman el mínimo. "
           "Con un vector recorrido de derecha a izquierda, ene por ele.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/10-1", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-1: {build(ESC, '../10-1_la_cuerda_de_la_cometa.mp4'):.0f}s")
