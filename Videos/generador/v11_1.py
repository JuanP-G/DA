"""Vídeo EJ 11-1 · El cazatesoros (animado)."""
import math
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-1/EJ_11-1.cpp"
TEMA = "Tema 11 · Programación dinámica II"
T = 200
COF = [(25, 4), (50, 5), (40, 4), (10, 2), (70, 10)]     # ejemplo 2: (profundidad, oro)
COLS = list(range(0, 196, 15))                            # todos los tiempos son múltiplos de 15
N = len(COF)


def tabla():
    o = [[0] * len(COLS) for _ in range(N + 1)]
    for i in range(1, N + 1):
        p, g = COF[i - 1]
        w = 3 * p
        for k, j in enumerate(COLS):
            o[i][k] = o[i - 1][k]
            if w <= j:
                o[i][k] = max(o[i][k], o[i - 1][COLS.index(j - w)] + g)
    return o


O = tabla()
ORDEN = [(i, k) for i in range(1, N + 1) for k in range(len(COLS))]


def reconstruye():
    pasos, k = [], len(COLS) - 1
    for i in range(N, 0, -1):
        if O[i][k] != O[i - 1][k]:
            pasos.append(("coge", i, k))
            k -= 3 * COF[i - 1][0] // 15
        else:
            pasos.append(("no", i, k))
    return pasos


REC = reconstruye()
ETQ = ["ninguno"] + [f"{p} m · {g}" for p, g in COF]
TB = Tabla(30, 150, N + 1, len(COLS), cw=62, ch=58, lw=130, cabecera=[str(j) for j in COLS], etiquetas=ETQ, tam=24)

# ------------------------------------------------------------------ mar
SUP = 170               # y de la superficie
ESC_P = 6.0             # píxeles por metro


def mar(f, u=1.0, x0=0, x1=W):
    f.d.rectangle((x0, SUP, x1, H), fill=mix(C["bot"], (16, 60, 110), u))
    for k in range(int((x1 - x0) / 40) + 1):
        x = x0 + k * 40 + (f.t * 20) % 40
        f.d.arc((x - 20, SUP - 8, x + 20, SUP + 8), 0, 180, fill=mix(C["bot"], (120, 190, 255), u), width=2)
    f.d.rectangle((x0, H - 40, x1, H), fill=mix(C["bot"], (120, 100, 70), u))


def barco(f, x, u=1.0):
    c = mix(C["bot"], (170, 110, 60), u)
    f.d.polygon([(x - 70, SUP - 26), (x + 70, SUP - 26), (x + 50, SUP + 6), (x - 50, SUP + 6)], fill=c)
    f.d.line((x, SUP - 26, x, SUP - 100), fill=c, width=4)
    f.d.polygon([(x + 4, SUP - 96), (x + 50, SUP - 50), (x + 4, SUP - 46)], fill=mix(C["bot"], (235, 235, 240), u))


def cofre(f, x, y, oro, u=1.0, abierto=False, sel=False):
    if u <= 0:
        return
    c = mix(C["bot"], (150, 95, 45), u)
    b = mix(C["bot"], (255, 206, 92), u)
    f.d.rounded_rectangle((x - 26, y - 16, x + 26, y + 16), 4, fill=c, outline=b if sel else mix(C["bot"], (90, 55, 25), u), width=3)
    f.d.rectangle((x - 26, y - 4, x + 26, y), fill=mix(C["bot"], (90, 55, 25), u))
    f.d.text((x, y + 34), f"{oro}", font=font(20, True), fill=b, anchor="mm")


def buzo(f, x, y, u=1.0):
    c = mix(C["bot"], (255, 206, 92), u)
    f.d.ellipse((x - 12, y - 30, x + 12, y - 6), fill=mix(C["bot"], (200, 220, 240), u), outline=c, width=3)
    f.d.rounded_rectangle((x - 10, y - 6, x + 10, y + 26), 6, fill=c)
    f.d.rectangle((x + 10, y - 2, x + 16, y + 18), fill=mix(C["bot"], (150, 160, 175), u))
    for k in range(3):
        by = y - 40 - ((f.t * 60 + k * 25) % 70)
        f.d.ellipse((x + 6 - k * 3, by - 4, x + 14 - k * 3, by + 4), outline=mix(C["bot"], (180, 220, 255), u), width=2)


def botella(f, x, y, usado, total=T, u=1.0, h=300):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - 30, y, x + 30, y + h), 14, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], (170, 180, 200), u), width=3)
    f.d.rectangle((x - 10, y - 18, x + 10, y), fill=mix(C["bot"], (170, 180, 200), u))
    lleno = max(0.0, 1 - usado / total)
    f.d.rounded_rectangle((x - 22, y + 8 + (h - 16) * (1 - lleno), x + 22, y + h - 8), 10, fill=mix(C["bot"], (90, 200, 255), u))
    f.d.text((x, y + h + 26), f"{max(0, total - usado):.0f} s", font=font(22, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


XS = [300, 450, 600, 750, 900]


def pos_cofre(k):
    return XS[k], SUP + COF[k][0] * ESC_P


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        f.d.rectangle((760, 300, 1240, 640), fill=(16, 60, 110))
        cofre(f, 1000, 560, "", u=f.p(0.3, 0.8))
        buzo(f, 900, 430 + 20 * math.sin(f.t), u=f.p(0.5, 0.8))
    portada(f, "EJ 11-1", "El cazatesoros", TEMA, dib)


def e_problema(f):
    mar(f, aparece(f, f.c(0), 0.8))
    barco(f, 140, aparece(f, f.c(0), 0.8))
    for k, (p, g) in enumerate(COF):
        x, y = pos_cofre(k)
        cofre(f, x, y, g, aparece(f, f.c(1) + 0.3 * k))
        if f.t >= f.c(1) + 0.3 * k:
            f.d.text((x, y - 30), f"{p} m", font=font(18, True), fill=C["muted"], anchor="mm")
    botella(f, 1150, 260, 0, u=aparece(f, f.c(2)))
    if f.t >= f.c(3):
        # el buzo baja al cofre de 40 m y sube
        x, y = pos_cofre(2)
        u = f.lin(f.c(3) + 0.3, 3.0)
        if u < 1 / 3:
            yy = lerp(SUP, y, u * 3)
        else:
            yy = lerp(y, SUP, (u - 1 / 3) * 1.5)
        buzo(f, x - 40, yy)
        texto(f, (x + 60, y - 120), "bajar 40 s", 22, "blue", aparece(f, f.c(3) + 0.3))
        texto(f, (x + 60, y - 90), "subir 80 s", 22, "blue", aparece(f, f.c(3) + 1.3))
        texto(f, (x + 60, y - 50), "= 3 · p", 26, "gold", aparece(f, f.c(3) + 2.5), mono=True)


def e_voraz(f):
    mar(f)
    barco(f, 140)
    usado = 0
    elegidos = []
    t0 = f.c(1)
    if f.t >= f.c(0):
        x, y = pos_cofre(4)
        if f.t < f.c(1):
            f.d.line((x - 30, y - 30, x + 30, y + 30), fill=C["red"], width=5)
            f.d.line((x - 30, y + 30, x + 30, y - 30), fill=C["red"], width=5)
    plan = [(1, f.c(1) + 0.3), (3, f.c(1) + 2.0)]
    if f.t >= f.c(3):
        plan = [(0, f.c(3) + 0.3), (2, f.c(3) + 1.8)]
    for k, (p, g) in enumerate(COF):
        x, y = pos_cofre(k)
        sel = any(kk == k and f.t >= tk for kk, tk in plan)
        cofre(f, x, y, g, sel=sel)
        f.d.text((x, y - 30), f"{3 * p} s", font=font(18, True), fill=C["muted"], anchor="mm")
    for kk, tk in plan:
        if f.t >= tk:
            usado += 3 * COF[kk][0] * min(1, f.lin(tk, 1.0))
    botella(f, 1150, 260, usado)
    oro = sum(COF[kk][1] for kk, tk in plan if f.t >= tk + 1.0)
    col = "red" if f.t < f.c(3) else "green"
    if f.t >= f.c(1):
        texto(f, (1050, 640), f"oro = {oro}", 34, col, aparece(f, f.c(1)), anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 80), "oro(i, j) = máximo oro con los cofres 1..i y j segundos de aire;  cofre i: profundidad p_i, oro o_i", 22, "muted",
          aparece(f, f.c(0)), bold=False)
    texto(f, (60, 150), "Caso base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 195, "oro(0, j) =", [("0", "∀ j ≥ 0")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 76, "oro(i, j) =", [("oro(i−1, j)", "si 3·p_i > j"),
                                               ("max( oro(i−1, j),  oro(i−1, j − 3·p_i) + o_i )", "si 3·p_i ≤ j")],
                aparece(f, f.c(2)), size=24)
    texto(f, (60, y + 40), "Respuesta:  oro(N, T)", 28, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 90), "Reconstrucción:  oro(i, j) ≠ oro(i−1, j)  ⇒  se coge el cofre i,  j ← j − 3·p_i", 24, "text",
          aparece(f, f.c(4)), mono=True)


def e_tabla(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    n = int((f.t - t0) / paso) if f.t >= t0 else 0
    n = max(0, min(n, len(ORDEN)))
    vals = {(0, k): 0 for k in range(len(COLS))}
    for (i, k) in ORDEN[:n]:
        vals[(i, k)] = O[i][k]
    marca, sombra = {}, {}
    cur = ORDEN[n] if n < len(ORDEN) and f.t >= t0 else None
    if cur:
        i, k = cur
        w = 3 * COF[i - 1][0] // 15
        marca[cur] = "gold"
        sombra[(i - 1, k)] = AZUL
        if k - w >= 0:
            sombra[(i - 1, k - w)] = NARANJA
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw, 132), "segundos de aire (de 15 en 15)", 20, "muted", 1)
    if cur:
        i, k = cur
        w = 3 * COF[i - 1][0] // 15
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        TB.flecha_entre(f, (i - 1, k), cur, AZUL, u=u)
        if k - w >= 0:
            TB.flecha_entre(f, (i - 1, k - w), cur, NARANJA, u=u)
    if f.t >= f.c(3):
        TB.dibuja(f, vals, marca={(N, len(COLS) - 1): "green"})
        texto(f, (640, 560), "oro(5, 200) = oro(5, 195) = 8", 32, "green", aparece(f, f.c(3)), mono=True, anchor="mm")


def e_reconstruye(f):
    vals = {(i, k): O[i][k] for i in range(N + 1) for k in range(len(COLS))}
    t0 = f.c(1)
    paso = (f.T - 2.5 - t0) / len(REC)
    n = int((f.t - t0) / paso) if f.t >= t0 else -1
    n = min(n, len(REC))
    marca, sombra = {}, {}
    cogidos = []
    for q in range(max(0, n)):
        if REC[q][0] == "coge":
            cogidos.append((REC[q][1], t0 + q * paso))
    if 0 <= n < len(REC):
        tipo, i, k = REC[n]
        marca[(i, k)] = "gold"
        sombra[(i - 1, k)] = AZUL
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    # flechas del recorrido hecho
    for q in range(max(0, min(n, len(REC)))):
        tipo, i, k = REC[q]
        if tipo == "no":
            TB.flecha_entre(f, (i, k), (i - 1, k), AZUL)
        else:
            w = 3 * COF[i - 1][0] // 15
            TB.flecha_entre(f, (i, k), (i - 1, k - w), NARANJA)
    if 0 <= n < len(REC):
        tipo, i, k = REC[n]
        a, b = O[i][k], O[i - 1][k]
        s = f"{a} = {b}: el cofre {i} no" if a == b else f"{a} ≠ {b}: se coge el cofre {i}"
        texto(f, (640, 560), s, 30, "blue" if a == b else NARANJA, 1, mono=True, anchor="mm")
    elif n >= len(REC):
        texto(f, (640, 560), "8 de oro:  25 m (4)  y  40 m (4)", 32, "green", aparece(f, t0 + len(REC) * paso), anchor="mm")
    for k, (i, tc) in enumerate(cogidos):
        u = f.lin(tc + 0.2, 1.2)
        x = 560 + 160 * k
        y = lerp(720, 640, ease(u))
        cofre(f, x, y, COF[i - 1][1], sel=True)


A = find_line(CPP, "vector<vector<int>> mejor(N + 1")
B = find_line(CPP, "j -= 3 * prof[i];")
CODE = codigo(CPP, A, B + 3, maxc=92)
L_TAB = A
L_CP = find_line(CPP, "mejor[i][j] = mejor[i - 1][j];")
L_MAX = find_line(CPP, "if (tiempo <= j) mejor[i][j] = max(")
L_NE = find_line(CPP, "if (mejor[i][j] != mejor[i - 1][j]) {")
L_CG = find_line(CPP, "cogido[i] = true;")
TBC = Tabla(886, 140, N + 1, len(COLS), cw=25, ch=36, lw=0, cabecera=[""] * len(COLS), etiquetas=[""] * (N + 1), tam=14)


def e_codigo(f):
    hl = {L_TAB}
    vals = {(0, k): 0 for k in range(len(COLS))}
    marca = {}
    t0, t1 = f.c(1), f.c(3)
    if f.t >= t0 and f.t < t1:
        paso = (t1 - t0) / len(ORDEN)
        n = min(len(ORDEN) - 1, int((f.t - t0) / paso))
        for (i, k) in ORDEN[:n]:
            vals[(i, k)] = O[i][k]
        cur = ORDEN[n]
        marca[cur] = "gold"
        hl = {L_CP} if ((f.t - t0) % paso) / paso < 0.5 else {L_MAX}
    elif f.t >= t1:
        vals = {(i, k): O[i][k] for i in range(N + 1) for k in range(len(COLS))}
        paso = (f.T - 2 - t1) / len(REC)
        n = max(0, min(len(REC) - 1, int((f.t - t1) / paso)))
        tipo, i, k = REC[n]
        marca[(i, k)] = "gold"
        hl = {L_NE} if tipo == "no" else {L_NE, L_CG, B}
    f.code(10, 84, 866, 540, CODE, hl=hl, title="tabla y reconstrucción", size=15)
    TBC.dibuja(f, vals, marca=marca)


def e_detalles(f):
    f.box(40, 110, 580, 400, "salida")
    f.box(660, 110, 580, 400, "detalles")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        for k, s in enumerate(["8", "2", "25 4", "40 4", "---"]):
            texto(f, (90, 170 + 52 * k), s, 30, "text" if k < 4 else "gold", u, mono=True, fondo=C["panel"])
        texto(f, (330, 260), "← oro", 22, "muted", u, fondo=C["panel"])
        texto(f, (330, 312), "← cofres", 22, "muted", u, fondo=C["panel"])
        texto(f, (330, 390), "← orden de entrada", 22, "muted", u, fondo=C["panel"])
    if f.t >= f.c(1):
        texto(f, (690, 180), "nada cabe:  0  0  ---", 26, "text", aparece(f, f.c(1)), mono=True, fondo=C["panel"])
    if f.t >= f.c(2):
        texto(f, (690, 260), "varias óptimas: vale cualquiera", 24, "text", aparece(f, f.c(2)), fondo=C["panel"])
    if f.t >= f.c(3):
        texto(f, (690, 360), "O(N · T) tiempo y memoria", 28, "gold", aparece(f, f.c(3)), fondo=C["panel"])
        texto(f, (690, 400), "(la tabla entera, para reconstruir)", 20, "muted", aparece(f, f.c(3)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "El cazatesoros", [
        "mochila 0/1: peso 3·p (segundos), valor el oro, capacidad T",
        "oro(i, j) = max( no coger,  coger: oro(i−1, j − 3p) + o )",
        "reconstruir: distinto de arriba ⇒ se cogió ese cofre",
        "O(N · T), con la tabla entera",
    ])


ESC = [
    Escena("El cazatesoros. Una mochila cero uno, y esta vez además hay que decir qué cofres se cogen.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Marcos ha encontrado un barco hundido rodeado de cofres de oro, cada uno a una profundidad. "
           "Sabe cuánto oro tiene cada uno. "
           "Pero solo tiene una botella de aire, que le deja estar bajo el agua te segundos. "
           "En cada inmersión sube un cofre: bajar a pe metros cuesta pe segundos y subir cuesta el doble. En total, tres pe.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("¿Y si cogemos primero los cofres con más oro? "
           "El de diez monedas está a setenta metros: necesita doscientos diez segundos y no cabe. "
           "El siguiente es el de cinco, que gasta ciento cincuenta, y después solo cabe el de dos: siete monedas. "
           "Pero cogiendo los de veinticinco y cuarenta metros se gastan ciento noventa y cinco segundos y se consiguen ocho. "
           "Elegir lo más valioso primero no sirve.",
           e_voraz, titulo="Lo más valioso no sirve", extra=1.5),
    Escena("Es una mochila cero uno: cada cofre pesa tres pe segundos y vale su oro, y la capacidad es te. "
           "Caso base: sin ningún cofre, cero monedas. "
           "Recurrencia: o no se coge el cofre i, y queda lo de la fila de arriba; o se coge, si cabe, y se suma su oro a lo que se consigue con el aire que queda. "
           "La respuesta es oro de ene, te. "
           "Y para saber qué cofres: si una casilla es distinta de la de arriba, ese cofre se ha cogido.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("Como todos los tiempos son múltiplos de quince, dibujamos las columnas de quince en quince. "
           "Cada casilla mira la de arriba, no coger, y la de arriba tantas columnas atrás como cuesta el cofre, coger. "
           "La última casilla, que vale lo mismo para ciento noventa y cinco que para doscientos segundos, dice ocho.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Ahora, qué cofres. Empezamos en la última casilla y subimos. "
           "Si vale lo mismo que la de arriba, ese cofre no hacía falta. "
           "Si es distinta, se cogió: lo apuntamos y restamos sus segundos. "
           "Así salen los cofres de cuarenta y de veinticinco metros, con cuatro monedas cada uno.",
           e_reconstruye, titulo="Qué cofres", extra=2.0),
    Escena("En el código, la tabla tiene ene más uno filas y te más uno columnas, y empieza a cero. "
           "El doble bucle copia la casilla de arriba y, si el cofre cabe, prueba a cogerlo. "
           "Después, un bucle de ene hacia uno: si la casilla es distinta de la de arriba, marca el cofre como cogido y resta su tiempo.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("La salida: el oro, el número de cofres y cada cofre con su profundidad y su oro, en el orden de la entrada, y tres guiones. "
           "Si no cabe ningún cofre, cero, cero y los guiones. "
           "Si hay varias soluciones óptimas, como en el cuarto ejemplo, vale cualquiera. "
           "El coste es ene por te, en tiempo y en memoria, porque para reconstruir hace falta la tabla entera.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es una mochila cero uno con peso tres pe y valor el oro. "
           "Cada casilla elige entre no coger el cofre y cogerlo. "
           "Para saber cuáles, se sube desde la última casilla: si cambia, se cogió. "
           "Todo en ene por te.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-1", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-1: {build(ESC, '../11-1_el_cazatesoros.mp4'):.0f}s")
