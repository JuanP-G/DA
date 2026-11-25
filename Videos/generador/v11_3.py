"""Vídeo EJ 11-3 · La colecta de primavera (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-3/EJ_11-3.cpp"
TEMA = "Tema 11 · Programación dinámica II"
PAGO = [[10, 5, 6, 7], [0, 100, 100, 100], [5, 4, 4, 4]]      # lo que paga cada vecino por 1, 2, 3 y 4 cajas
V, CJ = len(PAGO), 5


def p(i, k):
    return 0 if k == 0 else PAGO[i - 1][k - 1]


D = [[0] * (CJ + 1) for _ in range(V + 1)]
for i in range(1, V + 1):
    for j in range(CJ + 1):
        D[i][j] = max(D[i - 1][j - k] + p(i, k) for k in range(min(4, j) + 1))
ORDEN = [(i, j) for i in range(1, V + 1) for j in range(CJ + 1)]


def reconstruye():
    pasos, j = [], CJ
    for i in range(V, 0, -1):
        for k in range(min(4, j) + 1):
            if D[i][j] == D[i - 1][j - k] + p(i, k):
                pasos.append((i, j, k))
                j -= k
                break
    return pasos


REC = reconstruye()
REPARTO = {i: k for i, j, k in REC}
assert D[V][CJ] == 115
TB = Tabla(30, 130, V + 1, CJ + 1, cw=84, ch=76, lw=140, cabecera=[str(j) for j in range(CJ + 1)],
           etiquetas=["nadie"] + [f"vecino {i}" for i in range(1, V + 1)], tam=30)
COLK = [AZUL, NARANJA, C["purple"], C["green"], C["gold"]]


def caja(f, x, y, u=1.0, s=44, borde=None):
    if u <= 0:
        return
    f.d.rectangle((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=mix(C["bot"], (190, 150, 95), u),
                  outline=mix(C["bot"], borde or (120, 90, 50), u), width=3)
    f.d.line((x - s / 2, y - s / 6, x + s / 2, y - s / 6), fill=mix(C["bot"], (120, 90, 50), u), width=3)


def casa(f, x, y, u=1.0, col=(150, 170, 230)):
    if u <= 0:
        return
    c = mix(C["bot"], col, u)
    f.d.rectangle((x - 40, y - 20, x + 40, y + 36), fill=c)
    f.d.polygon([(x - 52, y - 20), (x, y - 62), (x + 52, y - 20)], fill=mix(C["bot"], (200, 110, 100), u))
    f.d.rectangle((x - 9, y + 6, x + 9, y + 36), fill=mix(C["bot"], (60, 50, 40), u))


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        for k in range(5):
            u = f.p(0.3 + 0.15 * k, 0.5)
            caja(f, 780 + (k % 3) * 56, 340 - (k // 3) * 56, u)
        casa(f, 1010, 330, f.p(0.9, 0.6))
    portada(f, "EJ 11-3", "La colecta de primavera", TEMA, dib)


def e_problema(f):
    xs = [250, 640, 1030]
    for i in range(V):
        u = aparece(f, f.c(0) + 0.3 * i)
        casa(f, xs[i], 190, u)
        texto(f, (xs[i], 270), f"vecino {i + 1}", 24, "muted", u, anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        for i in range(V):
            for k in range(4):
                x = xs[i] - 105 + k * 70
                f.d.rectangle((x - 30, 295, x + 30, 345), outline=mix(C["bot"], C["border"], u), width=2)
                f.d.text((x, 340 - 40 + 5), str(PAGO[i][k]), font=font(24, True), fill=mix(C["bot"], C["gold"], u), anchor="mm")
                f.d.text((x, 360), f"{k + 1}", font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")
        texto(f, (640, 395), "lo que paga cada vecino por 1, 2, 3 o 4 cajas", 22, "muted", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        for k in range(5):
            caja(f, 520 + k * 60, 520, u)
        texto(f, (640, 565), "5 cajas para repartir", 24, "text", u, anchor="mm")
    if f.t >= f.c(3):
        u = f.p(f.c(3), 1.0)
        reparto = [1, 2, 1]
        for i in range(V):
            for k in range(reparto[i]):
                yy = lerp(480, 230 - 0, ease(u)) if False else lerp(480, 440 - 0, 0)
        for i, kk in enumerate(reparto):
            texto(f, (xs[i], 440), f"{kk} caja{'s' if kk > 1 else ''}", 30, "green", u, anchor="mm")
        texto(f, (640, 625), "10 + 100 + 5 = 115", 40, "green", aparece(f, f.c(3) + 0.8), mono=True, anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 685), "máximo dinero  +  cuántas cajas para cada vecino", 22, "text", aparece(f, f.c(4)), anchor="mm")


def e_idea(f):
    # cada vecino es un "grupo": se elige UNA opción (0..4 cajas)
    texto(f, (640, 70), "cada vecino: elegir UNA opción", 34, "gold", aparece(f, f.c(0)), anchor="mm")
    for k in range(5):
        if f.t >= f.c(1) + 0.25 * k:
            u = aparece(f, f.c(1) + 0.25 * k, 0.4)
            x = 280 + k * 180
            f.d.rounded_rectangle((x - 70, 150, x + 70, 330), 14, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], COLK[k], u), width=4)
            for q in range(k):
                caja(f, x - 40 + (q % 3) * 40 if q < 3 else x - 20 + (q - 3) * 40, 200 + (0 if q < 3 else 40), u, s=30)
            texto(f, (x, 285), f"{k} caja{'s' if k != 1 else ''}", 22, "text", u, anchor="mm")
            texto(f, (x, 355), f"+ pago(i, {k})", 20, COLK[k], u, mono=True, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 470), "como una mochila donde cada «objeto» se puede coger de 5 formas", 26, "text", u, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (640, 540), "dinero(i, j) = mejor dinero con los vecinos 1..i y j cajas", 26, "gold", u, anchor="mm")
        texto(f, (640, 590), "«como mucho j»: puede sobrar alguna caja", 22, "muted", u, anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 70), "dinero(i, j) = máximo dinero con los vecinos 1..i y como mucho j cajas", 24, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (60, 140), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 185, "dinero(0, j) =", [("0", "sin vecinos no se gana nada")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 76, "dinero(i, j) =", [("max   dinero(i−1, j−k) + pago(i, k)", "k = 0..min(4, j)")],
                aparece(f, f.c(2)), size=24)
    texto(f, (80, y + 20), "vecino i se queda k cajas: le quedan j − k a los anteriores", 24, "text", aparece(f, f.c(3)))
    texto(f, (60, y + 90), "Respuesta:  dinero(V, C)", 28, "green", aparece(f, f.c(4)), mono=True)
    texto(f, (60, y + 145), "pago(i, 0) = 0", 24, "muted", aparece(f, f.c(4)), mono=True)


def e_tabla(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    nn = max(0, min(len(ORDEN), int((f.t - t0) / paso) if f.t >= t0 else 0))
    vals = {(0, j): 0 for j in range(CJ + 1)}
    for (i, j) in ORDEN[:nn]:
        vals[(i, j)] = D[i][j]
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= t0 else None
    marca, sombra = {}, {}
    if cur:
        i, j = cur
        marca[cur] = "gold"
        for k in range(min(4, j) + 1):
            sombra[(i - 1, j - k)] = COLK[k]
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw + 3 * TB.cw, 100), "cajas disponibles →", 22, "muted", aparece(f, f.c(0)), anchor="mm")
    if cur:
        i, j = cur
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        for k in range(min(4, j) + 1):
            TB.flecha_entre(f, (i - 1, j - k), cur, COLK[k], u=u, dx=0, dy=(k - 2) * 3)
        # candidatos
        f.box(720, 120, 520, 330, f"vecino {i}, {j} cajas")
        mejor = D[i][j]
        for k in range(min(4, j) + 1):
            tot = D[i - 1][j - k] + p(i, k)
            esb = tot == mejor
            texto(f, (750, 175 + 55 * k), f"k = {k}:  {D[i - 1][j - k]} + {p(i, k)} = {tot}", 26,
                  "green" if esb else COLK[k], 1, mono=True, fondo=C["panel"])
            if esb:
                f.d.rectangle((742, 168 + 55 * k, 742 + 470, 198 + 55 * k), outline=C["green"], width=2)
        texto(f, (980, 485), f"dinero({i}, {j}) = {mejor}", 30, "gold", 1, mono=True, anchor="mm")
    if f.t >= t1:
        TB.dibuja(f, {(i, j): D[i][j] for i in range(V + 1) for j in range(CJ + 1)}, marca={(V, CJ): "green"})
        texto(f, (640, 640), f"dinero(3, 5) = {D[V][CJ]}", 36, "green", aparece(f, t1), mono=True, anchor="mm")


def e_reconstruye(f):
    vals = {(i, j): D[i][j] for i in range(V + 1) for j in range(CJ + 1)}
    t0 = f.c(1)
    paso = (f.c(4) - t0) / len(REC)
    q = int((f.t - t0) / paso) if f.t >= t0 else -1
    q = min(q, len(REC) - 1)
    marca = {}
    if q >= 0:
        i, j, k = REC[q]
        marca[(i, j)] = "gold"
    TB.dibuja(f, vals, marca=marca)
    for r in range(max(0, q)):
        i, j, k = REC[r]
        TB.flecha_entre(f, (i, j), (i - 1, j - k), COLK[k])
    if q >= 0:
        i, j, k = REC[q]
        f.box(720, 120, 520, 220, f"vecino {i}")
        texto(f, (750, 180), f"dinero({i}, {j}) = {D[i][j]}", 26, "text", 1, mono=True, fondo=C["panel"])
        texto(f, (750, 225), f"{D[i - 1][j - k]} + {p(i, k)}  → k = {k}", 26, "green", 1, mono=True, fondo=C["panel"])
        texto(f, (750, 275), f"ahora a ({i - 1}, {j - k})", 24, "muted", 1, mono=True, fondo=C["panel"])
    # reparto
    for i in range(1, V + 1):
        for r in range(len(REC)):
            if REC[r][0] == i and f.t >= t0 + r * paso:
                u = f.lin(t0 + r * paso, 0.5)
                texto(f, (260 + (i - 1) * 190, 580), f"{REPARTO[i]} caja{'s' if REPARTO[i] != 1 else ''}", 30, "green", u, anchor="mm")
                caja(f, 260 + (i - 1) * 190, 520, u)
    if f.t >= f.c(4):
        texto(f, (640, 670), "desde (V, C) hacia atrás: la k que explica el valor de la casilla", 26, "text", aparece(f, f.c(4)), anchor="mm")


A = find_line(CPP, "Matriz<int> dinero(V + 1, C + 1, 0);")
B = find_line(CPP, "for (int i = 1; i <= V; ++i) cout << cajas[i]")
CODE = codigo(CPP, A, B, maxc=70)
L_MAX = find_line(CPP, "mejor = max(mejor,")
L_K = find_line(CPP, "for (int k = 0; k <= min(4, j); ++k)")
L_REC = find_line(CPP, "if (dinero[i][j] == dinero[i - 1][j - k] + pago[i][k])")
L_J = find_line(CPP, "j -= k;")
L_OUT = find_line(CPP, "cout << dinero[V][C]")


def e_codigo(f):
    hl = {A}
    if f.t >= f.c(1):
        hl = {L_K, L_MAX}
    if f.t >= f.c(2):
        hl = {L_REC, L_J}
    if f.t >= f.c(3):
        hl = {L_OUT, B}
    f.code(40, 90, 800, 560, CODE, hl=hl, title="tabla completa y reconstrucción", size=16)
    f.box(880, 90, 360, 560, "qué hace")
    notas = [("Matriz<int>  (V+1) × (C+1)", "una fila por vecino", C["blue"]),
             ("k de 0 a min(4, j)", "todas las formas de repartir", NARANJA),
             ("¿vale lo mismo?  →  k", "restar k cajas y subir", C["green"]),
             ("beneficio y cajas", "dos líneas por caso", C["gold"])]
    for k, (a, b, col) in enumerate(notas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (910, 150 + 120 * k), a, 22, col, u, fondo=C["panel"])
            texto(f, (910, 190 + 120 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])


def e_detalles(f):
    f.box(40, 110, 580, 480, "cuidado con")
    f.box(660, 110, 580, 480, "coste")
    cuid = [("entrada por filas de cajas", "4 líneas: 1, 2, 3 y 4 cajas; cada una con V vecinos", C["blue"]),
            ("no hace falta vender todas", "k = 0 vale y «como mucho j» deja sobrar", NARANJA),
            ("empates: vale cualquier reparto", "el juez lo comprueba solo", C["green"])]
    for k, (a, b, col) in enumerate(cuid):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (70, 170 + 130 * k), a, 26, col, u, fondo=C["panel"])
            texto(f, (70, 212 + 130 * k), b, 21, "muted", u, bold=False, fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 190), "O(V · C · 5)", 40, "gold", u, mono=True, fondo=C["panel"])
        texto(f, (690, 260), "V ≤ 1000,  C ≤ 4000", 26, "text", u, fondo=C["panel"])
        texto(f, (690, 320), "4 millones de casillas", 24, "muted", u, fondo=C["panel"])
        texto(f, (690, 380), "unos 16 MB  →  cabe", 24, "muted", u, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "La colecta de primavera", [
        "cada vecino es un grupo con 5 opciones (0..4 cajas)",
        "dinero(i, j) = max sobre k de dinero(i−1, j−k) + pago(i, k)",
        "tabla entera para poder reconstruir",
        "volver desde (V, C): la k que explica cada casilla",
    ])


ESC = [
    Escena("La colecta de primavera. Repartir cajas entre vecinos para ganar lo máximo.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos varios vecinos, y cada uno paga una cantidad distinta según cuántas cajas le vendamos: una, dos, tres o cuatro. "
           "Aquí tenemos la tabla de lo que pagaría cada uno. "
           "Y tenemos cinco cajas para repartir. "
           "Lo mejor es dar una caja al primero, dos al segundo y una al tercero: diez más cien más cinco, ciento quince. "
           "Hay que decir el dinero máximo y cuántas cajas lleva cada vecino.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Cada vecino es como un objeto de una mochila, pero con una diferencia: en vez de cogerlo o no, hay que elegir una opción entre cinco. "
           "Cero cajas, una, dos, tres o cuatro, y cada opción tiene su pago. "
           "Es una mochila con grupos: de cada grupo se elige una sola opción. "
           "Llamamos dinero de i, j al mejor dinero con los vecinos del uno al i y como mucho j cajas.",
           e_idea, titulo="Una opción por vecino", extra=1.5),
    Escena("Dinero de i, j es el máximo dinero con los vecinos del uno al i y como mucho j cajas. "
           "Sin vecinos no se gana nada. "
           "Para el vecino i probamos todas sus opciones, k de cero a cuatro, sin pasarnos de j. "
           "Si se queda k cajas, le quedan j menos k a los anteriores. "
           "La respuesta está en la esquina: dinero de V, C.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("La tabla tiene una fila por vecino y una columna por número de cajas. "
           "Para cada casilla miramos hasta cinco casillas de la fila de arriba, una por cada opción k, y sumamos lo que paga el vecino. "
           "Nos quedamos con la mejor, resaltada en verde. "
           "En la esquina de abajo a la derecha sale ciento quince.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Para saber cuántas cajas lleva cada uno, volvemos desde la esquina. "
           "En el último vecino buscamos la k que explica el valor de la casilla, es decir, la que cumple dinero de arriba más pago igual a la casilla. "
           "Esa es su cantidad de cajas. "
           "Restamos esas cajas, subimos de fila y repetimos hasta llegar arriba. "
           "Por eso necesitamos la tabla entera.",
           e_reconstruye, titulo="Reconstruir el reparto", extra=2.0),
    Escena("En el código, dinero es una matriz de V más uno filas por C más uno columnas. "
           "Para cada casilla, un bucle de k de cero a mínimo de cuatro y j, toma el máximo. "
           "Después, desde la esquina, se busca la k que cumple la igualdad, se guarda en cajas y se resta de j. "
           "Se escribe el beneficio y, en otra línea, las cajas de cada vecino.",
           e_codigo, titulo="El código", extra=1.5),
    Escena("Dos cosas de la entrada. Los pagos vienen en cuatro líneas, una por cada número de cajas, y no una por vecino. "
           "No hace falta vender todas las cajas: puede ser mejor que sobren. "
           "Y si hay varios repartos que ganan lo mismo, vale cualquiera. "
           "El coste es V por C por cinco: cuatro millones de casillas como mucho, que caben sin problema.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es una mochila con grupos. "
           "Cada vecino tiene cinco opciones, y dinero de i, j es el máximo sobre k. "
           "Guardamos la tabla entera. "
           "Y para el reparto, volvemos desde la esquina buscando la k que explica cada casilla.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-3", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-3: {build(ESC, '../11-3_la_colecta_de_primavera.mp4'):.0f}s")
