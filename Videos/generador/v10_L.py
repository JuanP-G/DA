"""Vídeo EJ 10-L · Cambio exacto (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../10-Programacion dinamica/EJ_10-L/EJ_10-L.cpp"
TEMA = "Tema 10 · Programación dinámica"
PRECIO = 100
MON = [25, 50, 25, 50]
PASO = 25
COLS = list(range(0, 151, PASO))          # sumas 0, 25, ..., 150 (= P + máx)
INF = None


def filas():
    f = [[0] + [INF] * (len(COLS) - 1)]
    for v in MON:
        prev = f[-1]
        nueva = prev[:]
        for k in range(len(COLS) - 1, -1, -1):          # de mayor a menor
            s = COLS[k]
            if s >= v and prev[COLS.index(s - v)] is not INF:
                c = prev[COLS.index(s - v)] + 1
                if nueva[k] is INF or c < nueva[k]:
                    nueva[k] = c
        f.append(nueva)
    return f


P = filas()
ETQ = ["ninguna"] + [f"{v}" for v in MON]
TB = Tabla(40, 150, len(P), len(COLS), cw=100, ch=70, lw=120, cabecera=[str(s) for s in COLS], etiquetas=ETQ, tam=28)
ORDEN = [(i, k) for i in range(1, len(P)) for k in range(len(COLS) - 1, -1, -1)]


def moneda(f, x, y, v, r=40, u=1.0, borde=None, col=(205, 170, 70)):
    if u <= 0:
        return
    f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], col, u), outline=mix(C["bot"], borde or (140, 110, 40), u),
                width=5 if borde else 3)
    f.d.text((x, y), str(v), font=font(int(r * 0.62), True), fill=mix(C["bot"], (50, 35, 10), u), anchor="mm")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        for k, v in enumerate([500, 1000, 2000]):
            u = f.p(0.3 + 0.3 * k, 0.6)
            moneda(f, 760 + k * 120, 320 - 30 * (k % 2), v, r=48, u=u, col=(205, 170, 70) if v < 2000 else (150, 200, 150))
    portada(f, "EJ 10-L", "Cambio exacto", TEMA, dib)


def e_problema(f):
    # recta de sumas posibles del primer ejemplo
    x0, x1, y = 90, 1190, 400
    f.d.line((x0, y, x1, y), fill=C["border"], width=4)
    esc = (x1 - x0) / 3600
    for v in [0, 500, 1000, 1500, 2000, 2500, 3000, 3500]:
        x = x0 + v * esc
        f.d.line((x, y - 10, x, y + 10), fill=C["muted"], width=3)
        f.d.text((x, y + 34), str(v), font=font(20, True), fill=C["muted"], anchor="mm")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        for k, v in enumerate([500, 1000, 2000]):
            moneda(f, 400 + k * 150, 200, v, r=44, u=u, col=(205, 170, 70) if v < 2000 else (150, 200, 150))
        texto(f, (90, 120), "precio  1400", 34, "gold", u)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        for v in [500, 1000, 1500, 2000, 2500, 3000, 3500]:
            x = x0 + v * esc
            f.d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=mix(C["bot"], C["blue"], u))
        px = x0 + 1400 * esc
        f.d.line((px, y - 90, px, y + 12), fill=mix(C["bot"], C["red"], u), width=5)
        f.d.text((px, y - 110), "precio", font=font(24, True), fill=mix(C["bot"], C["red"], u), anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        x = x0 + 1500 * esc
        f.d.ellipse((x - 19, y - 19, x + 19, y + 19), outline=mix(C["bot"], C["green"], u), width=6)
        texto(f, (x, y + 90), "1500 con 2 piezas  (500 + 1000)", 28, "green", u, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        x = x0 + 2000 * esc
        texto(f, (x + 40, y + 150), "2000 con 1 pieza: más caro", 26, "red", u, anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 600), "1º  pagar lo menos posible (≥ precio)      2º  con las menos piezas", 28, "text", aparece(f, f.c(4)), anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 70), "piezas(i, s) = mínimo de piezas, usando las i primeras, que suman EXACTAMENTE s", 24, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (60, 130), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 175, "piezas(0, s) =", [("0", "si s = 0"), ("∞", "si s > 0   (sin piezas no se suma nada)")], aparece(f, f.c(1)), size=24, colores=[C["green"], C["red"]])
    texto(f, (60, y + 24), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 66, "piezas(i, s) =", [("piezas(i−1, s)", "no usar la pieza i"),
                                                   ("piezas(i−1, s−vᵢ) + 1", "usarla  (si vᵢ ≤ s)")],
                aparece(f, f.c(2)), size=24, colores=[AZUL, NARANJA])
    texto(f, (80, y + 12), "→ se queda con el menor de los dos:  min", 24, "text", aparece(f, f.c(2)))
    texto(f, (60, y + 80), "Respuesta:  la MENOR  s ≥ precio  con piezas(N, s) finito", 28, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 135), "(y ese valor es el número de piezas)", 24, "muted", aparece(f, f.c(3)))


def e_tabla(f):
    t0, t1 = f.c(1), f.c(4)
    paso = (t1 - t0) / len(ORDEN)
    nn = max(0, min(len(ORDEN), int((f.t - t0) / paso) if f.t >= t0 else 0))
    vals = {(0, k): P[0][k] for k in range(len(COLS))}
    for (i, k) in ORDEN[:nn]:
        vals[(i, k)] = P[i][k]
    # lo que aún no se ha recorrido en la fila actual conserva el valor de arriba
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= t0 else None
    if cur:
        i, k = cur
        for kk in range(0, k + 1):
            vals[(i, kk)] = P[i - 1][kk]
    marca, sombra = {}, {}
    if cur:
        i, k = cur
        marca[cur] = "gold"
        v = MON[i - 1]
        sombra[(i - 1, k)] = AZUL
        if COLS[k] >= v:
            sombra[(i - 1, k - v // PASO)] = NARANJA
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw + 3.5 * TB.cw, 105), "suma que se paga →", 22, "muted", aparece(f, f.c(0)), anchor="mm")
    if cur:
        i, k = cur
        v = MON[i - 1]
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        TB.flecha_entre(f, (i - 1, k), (i, k), AZUL, u=u)
        if COLS[k] >= v:
            TB.flecha_entre(f, (i - 1, k - v // PASO), (i, k), NARANJA, u=u)
        moneda(f, 1150, 250, v, r=44, u=1.0)
        texto(f, (1150, 330), "moneda actual", 20, "muted", 1, anchor="mm")
        texto(f, (1150, 400), "de derecha a izquierda", 20, "muted", 1, anchor="mm")
    if f.t >= t1:
        texto(f, (640, 620), "menor suma ≥ 100 con valor finito:  100  con  2 piezas", 32, "green", aparece(f, t1), anchor="mm")
        TB.dibuja(f, {(i, k): P[i][k] for i in range(len(P)) for k in range(len(COLS))}, marca={(len(P) - 1, 4): "green"})


def e_limite(f):
    # por qué basta llegar a precio + máximo
    y = 330
    x0, esc = 100, 0.9
    px = x0 + 700 * esc * 0.9
    f.d.line((x0, y + 70, 1200, y + 70), fill=C["border"], width=3)
    # barra de piezas que suman S > P
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        xs = x0
        piezas = [260, 190, 170, 120]
        cols = [(205, 170, 70), (150, 200, 150), (150, 170, 230), (230, 140, 120)]
        for k, v in enumerate(piezas):
            a = xs; b = xs + v * 1.0 * u
            f.d.rectangle((a, y - 30, b, y + 30), fill=mix(C["bot"], cols[k], u), outline=C["bot"], width=3)
            f.d.text(((a + b) / 2, y), str(v), font=font(22, True), fill=mix(C["bot"], (40, 30, 10), u), anchor="mm")
            xs = b
        f.d.line((x0 + 650, y - 80, x0 + 650, y + 80), fill=mix(C["bot"], C["red"], u), width=5)
        f.d.text((x0 + 650, y - 100), "precio", font=font(24, True), fill=mix(C["bot"], C["red"], u), anchor="mm")
        texto(f, (x0 + 740, y), "S", 34, "gold", u, anchor="lm")
    if f.t >= f.c(1):
        u = f.p(f.c(1), 0.9)
        # quitamos la última pieza: sigue por encima del precio → no era la mínima
        a = x0 + 740 - 120 * (1 - 0) * 1.0
        f.d.rectangle((x0 + 740 - 120, y - 30 - 60 * u, x0 + 740, y + 30 - 60 * u), outline=mix(C["bot"], C["red"], u), width=4)
        texto(f, (640, 190), "si quitando una pieza se sigue llegando al precio, S no era la mínima", 26, "red", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 480), "así que  S − v < precio  para toda pieza v", 30, "text", u, anchor="mm")
        texto(f, (640, 540), "S < precio + v ≤ precio + valor máximo", 30, "gold", aparece(f, f.c(3)), anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 625), "basta calcular las sumas hasta  P + máx  (≤ 20.000)", 30, "green", aparece(f, f.c(4)), anchor="mm")


def e_orden(f):
    # por qué la fila se recorre de mayor a menor
    f.box(40, 110, 570, 450, "de menor a mayor  ✗")
    f.box(670, 110, 570, 450, "de mayor a menor  ✓")
    cols = [0, 50, 100]
    for lado, (x0, ok) in enumerate([(100, False), (730, True)]):
        for k, s in enumerate(cols):
            x = x0 + k * 150
            f.d.rectangle((x, 280, x + 130, 340), fill=C["panel2"] if "panel2" in C else C["bot"], outline=C["border"], width=2)
            f.d.text((x + 65, 262), str(s), font=font(20, True), fill=C["muted"], anchor="mm")
    moneda(f, 310, 190, 50, r=34)
    moneda(f, 940, 190, 50, r=34)
    # una sola moneda de 50, fila inicial: 0 -> 0 piezas
    def celda(x0, k, txt, col):
        x = x0 + k * 150
        f.d.text((x + 65, 310), txt, font=font(30, True), fill=col, anchor="mm")
    for x0 in (100, 730):
        celda(x0, 0, "0", C["text"]); celda(x0, 1, "∞", C["dim"]); celda(x0, 2, "∞", C["dim"])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        # izquierda: 50 se rellena y luego 100 se rellena con la MISMA moneda
        celda(100, 1, "1", mix(C["bot"], C["green"], u))
        if f.t >= f.c(2):
            u2 = aparece(f, f.c(2))
            celda(100, 2, "2", mix(C["bot"], C["red"], u2))
            texto(f, (325, 420), "¡usa la moneda dos veces!", 26, "red", u2, anchor="mm", fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        celda(730, 2, "∞", C["dim"])
        texto(f, (955, 420), "100 mira el 50 de antes de la moneda:  ∞", 22, "green", u, anchor="mm", fondo=C["panel"])
        celda(730, 1, "1", mix(C["bot"], C["green"], u))
    if f.t >= f.c(4):
        texto(f, (640, 640), "una sola fila:  s de mayor a menor  →  cada pieza, una vez", 30, "gold", aparece(f, f.c(4)), anchor="mm")


A = find_line(CPP, "int tope = precio + maximo;")
B = find_line(CPP, "cout << s <<")
CODE = codigo(CPP, A, B, maxc=80)
L_TOPE = A
L_INI = find_line(CPP, "vector<EntInf> piezas")
L_FOR = find_line(CPP, "for (int v : valor)")
L_MIN = find_line(CPP, "piezas[s] = min(")
L_RES = find_line(CPP, "int s = precio;")
L_WH = find_line(CPP, "while (piezas[s] == Infinito)")
L_OUT = B


def e_codigo(f):
    hl = {L_INI}
    if f.t >= f.c(1):
        hl = {L_FOR, L_MIN}
    if f.t >= f.c(2):
        hl = {L_RES, L_WH}
    if f.t >= f.c(3):
        hl = {L_OUT}
    f.code(40, 90, 800, 560, CODE, hl=hl, title="una fila de EntInf", size=17)
    f.box(880, 90, 360, 560, "qué hace")
    notas = [("EntInf  =  entero con ∞", "inf + 1  sigue siendo  ∞", C["blue"]),
             ("s de tope a v", "cada pieza, una vez", NARANJA),
             ("while  piezas[s] = ∞", "sube hasta una suma posible", C["green"]),
             ("escribe  s  y  piezas[s]", "pagado  y  nº de piezas", C["gold"])]
    for k, (a, b, col) in enumerate(notas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (910, 150 + 120 * k), a, 24, col, u, fondo=C["panel"])
            texto(f, (910, 190 + 120 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Cambio exacto", [
        "mochila 0/1 de suma exacta: piezas(s) = mínimo de piezas",
        "una fila de EntInf recorrida de mayor a menor",
        "hasta  precio + valor máximo  basta",
        "la menor suma ≥ precio con valor finito",
    ])


ESC = [
    Escena("Cambio exacto. Pagar lo mínimo posible, con las menos monedas y billetes.", e_portada, titulo="Portada", extra=1.0),
    Escena("Queremos pagar un producto de mil cuatrocientos céntimos, con una moneda de quinientos, una de mil y un billete de dos mil. "
           "Cada pieza solo se puede usar una vez. "
           "Estas son todas las cantidades que podemos pagar. "
           "La menor que llega al precio es mil quinientos, con dos piezas. "
           "Pagar con el billete de dos mil usa una sola, pero cuesta más. "
           "Primero importa pagar lo menos posible, y solo después, usar las menos piezas.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Es una mochila de las de siempre, pero con suma exacta. "
           "Piezas de i, s es el mínimo de piezas, usando las i primeras, que suman exactamente s. "
           "Sin piezas, sumar cero cuesta cero piezas, y cualquier otra cantidad es imposible: infinito. "
           "Con la pieza i, o no la usamos, o la usamos y miramos s menos su valor, con una pieza más. Nos quedamos con el mínimo. "
           "La respuesta es la menor suma que llega al precio y que no sea infinito.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("Probamos con cien céntimos y cuatro monedas: veinticinco, cincuenta, veinticinco y cincuenta. "
           "Al principio, solo la suma cero es posible, con cero piezas. "
           "Vamos pieza a pieza, y en cada una recorremos las sumas de derecha a izquierda. "
           "Cada casilla compara la de arriba, no usar la pieza, con la de arriba desplazada su valor, más una pieza. "
           "Al final, la primera suma que llega a cien está a cien céntimos con dos piezas: las dos de cincuenta.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Pero, hasta dónde hay que calcular? "
           "Imagina que S es la mínima suma que llega al precio. "
           "Si pudiéramos quitar una pieza y seguir llegando, S no sería la mínima. "
           "Así que al quitar cualquiera, nos quedamos por debajo del precio: S menos v es menor que el precio. "
           "Es decir, S es menor que el precio más el valor máximo, que son como mucho veinte mil. "
           "Basta calcular las sumas hasta el precio más el valor máximo.",
           e_limite, titulo="Hasta dónde calcular", extra=1.5),
    Escena("Y por qué de derecha a izquierda? "
           "Si recorriéramos de izquierda a derecha, la casilla cincuenta se rellenaría con la moneda de cincuenta. "
           "Y después la casilla cien miraría la cincuenta ya actualizada, y usaría la misma moneda dos veces. "
           "De derecha a izquierda, cada casilla mira solo valores de antes de esa moneda. "
           "Así cada pieza se usa una vez, y nos basta una sola fila.",
           e_orden, titulo="Una fila, de mayor a menor", extra=1.5),
    Escena("En el código, el vector de piezas es de enteros con infinito, el tipo EntInf. "
           "Por cada valor, un bucle de s desde el tope hasta el valor, tomando el mínimo. "
           "Después se sube desde el precio hasta encontrar una suma que no sea infinito. "
           "Y se escribe esa suma y su número de piezas.",
           e_codigo, titulo="El código", extra=1.5),
    Escena("Resumiendo: mochila cero uno de suma exacta, con el mínimo de piezas. "
           "Una sola fila de enteros con infinito, recorrida de mayor a menor. "
           "Basta llegar hasta el precio más el valor máximo. "
           "Y la respuesta es la primera suma que llega al precio y no es infinito.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/10-L", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-L: {build(ESC, '../10-L_cambio_exacto.mp4'):.0f}s")
