"""Vídeo EJ 08-4 · Maratón de cine de terror (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview

CPP = "../../8-Algoritmos voraces/EJ_08-4/EJ_08-4.cpp"
TEMA = "Tema 8 · Algoritmos voraces"


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def txt(m):
    return f"{m // 60:02}:{m % 60:02}"


# ejemplo propio (un día)
PELIS = [("A", "10:00", "14:00"), ("B", "10:30", "11:30"), ("C", "11:45", "13:00"), ("D", "13:00", "14:30"), ("E", "14:00", "15:00")]
P = [(n, hm(a), hm(b)) for n, a, b in PELIS]
T0, T1 = hm("09:30"), hm("15:30")
X0, X1 = 140, 1220


def X(m, a=T0, b=T1):
    return X0 + (m - a) * (X1 - X0) / (b - a)


COLS = {"A": C["purple"], "B": C["blue"], "C": NARANJA, "D": C["red"], "E": C["green"]}


def eje(f, a=T0, b=T1, y=600, u=1.0, paso=60):
    if u <= 0:
        return
    f.d.line((X0, y, X1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    m = a - a % paso + (paso if a % paso else 0)
    while m <= b:
        x = X(m, a, b)
        f.d.line((x, y - 6, x, y + 6), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((x, y + 22), txt(m % 1440), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")
        m += paso


def peli(f, n, a, b, y, u=1.0, c=None, gris=False, ab=(T0, T1), h=40, etiq=True):
    if u <= 0:
        return
    c = C["dim"] if gris else (c or COLS.get(n, C["blue"]))
    x0, x1 = X(a, *ab), X(b, *ab)
    x1 = lerp(x0, x1, u)
    f.d.rounded_rectangle((x0, y - h / 2, x1, y + h / 2), 8, fill=mix(C["bot"], mix(C["panel"], c, 0.45), 1),
                          outline=c, width=3)
    for k in range(int((x1 - x0) // 22)):       # agujeros de película
        xx = x0 + 8 + k * 22
        f.d.rectangle((xx, y - h / 2 + 4, xx + 8, y - h / 2 + 9), fill=mix(C["panel"], c, 0.7))
        f.d.rectangle((xx, y + h / 2 - 9, xx + 8, y + h / 2 - 4), fill=mix(C["panel"], c, 0.7))
    if etiq and u >= 1:
        f.d.text(((x0 + x1) / 2, y), n, font=font(20, True), fill=C["text"], anchor="mm")


def descanso(f, m, y, u=1.0, ab=(T0, T1), h=40):
    if u <= 0:
        return
    x0, x1 = X(m, *ab), X(m + 10, *ab)
    f.d.rectangle((x0, y - h / 2, x1, y + h / 2), fill=mix(C["bot"], (90, 70, 40), u))
    f.d.text(((x0 + x1) / 2, y - h / 2 - 12), "10'", font=font(14, True), fill=mix(C["bot"], C["gold"], u), anchor="mm")


YS = {n: 150 + 80 * k for k, (n, _, _) in enumerate(P)}


def e_portada(f):
    def dib(f):
        for k in range(3):
            u = f.p(0.3 + 0.2 * k, 0.6)
            x = 780 + k * 150
            f.d.rounded_rectangle((x, 280, x + 130, 380), 8, fill=mix(C["bot"], (40, 20, 30), u), outline=mix(C["bot"], C["red"], u), width=3)
            f.d.text((x + 65, 330), ["👻", "🔪", "🧟"][k] if False else ["I", "II", "III"][k], font=font(30, True), fill=mix(C["bot"], C["red"], u), anchor="mm")
    portada(f, "EJ 08-4", "Maratón de cine de terror", TEMA, dib)


def e_problema(f):
    eje(f, u=aparece(f, f.c(0)))
    for k, (n, a, b) in enumerate(P):
        peli(f, n, a, b, YS[n], f.lin(f.c(0) + 0.3 * k, 0.8))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        # B y luego C: hueco de 15 min ≥ 10
        descanso(f, hm("11:30"), YS["C"] - 0, u)
        texto(f, (X(hm("11:40")), YS["C"] + 40), "≥ 10 min libres entre dos", 20, "gold", u)
    if f.t >= f.c(2):
        texto(f, (640, 80), "¿cuántas películas enteras, como máximo?", 28, "text", aparece(f, f.c(2)), anchor="mm")


def selecciona(lista):
    libre, el = -10, []
    for n, a, b in lista:
        ok = a >= libre
        el.append((n, a, b, ok))
        if ok:
            libre = b + 10
    return el


def e_malas(f):
    # 1) la que empieza antes   2) la más corta
    eje(f, u=1)
    if f.t < f.c(2):
        u = aparece(f, f.c(0))
        texto(f, (640, 80), "¿la que empieza antes?", 30, "red", u, anchor="mm")
        orden = sorted(P, key=lambda p: p[1])
        sel = selecciona(orden)
        k, fr = paso_idx(f, f.c(0) + 0.5, f.c(1), len(sel))
        for q, (n, a, b, ok) in enumerate(sel):
            g = q < k and not ok
            peli(f, n, a, b, YS[n], gris=g)
            if q < k:
                tick(f, X1 + 30, YS[n], ok)
        if f.t >= f.c(1):
            texto(f, (640, 660), "1 película: la A lo tapa todo", 26, "red", aparece(f, f.c(1)), anchor="mm")
    else:
        u = aparece(f, f.c(2))
        texto(f, (640, 80), "¿la más corta?", 30, "red", u, anchor="mm")
        Q = [("L1", hm("09:40"), hm("12:00")), ("corta", hm("11:55"), hm("12:30")), ("L2", hm("12:20"), hm("15:00"))]
        ys = [220, 320, 420]
        for k, (n, a, b) in enumerate(Q):
            c = C["purple"] if n != "corta" else C["blue"]
            gris = f.t >= f.c(3) and n != "corta"
            peli(f, n, a, b, ys[k], u, c=c, gris=gris)
        if f.t >= f.c(3):
            tick(f, X1 + 30, ys[1], True)
            texto(f, (640, 560), "la corta choca con las dos largas:  1  en vez de  2", 26, "red", aparece(f, f.c(3)), anchor="mm")


ORD = sorted(P, key=lambda p: p[2])
SEL = selecciona(ORD)


def e_voraz(f):
    eje(f)
    texto(f, (640, 70), "la que ACABA antes", 32, "green", aparece(f, f.c(0)), anchor="mm")
    # se reordenan por fin: cada fila sube a su sitio
    u = f.lin(f.c(0) + 0.5, 1.2)
    k, fr = paso_idx(f, f.c(2), f.c(4), len(SEL))
    libre = None
    for q, (n, a, b, ok) in enumerate(SEL):
        y = lerp(YS[n], 150 + 80 * q, ease(u))
        gris = q < k and not ok
        peli(f, n, a, b, y, gris=gris)
        if q < k:
            tick(f, X1 + 30, y, ok)
            if ok:
                libre = b + 10
                descanso(f, b, y)
    if libre is not None and f.t < f.c(4) + 10:
        x = X(libre)
        f.d.line((x, 110, x, 580), fill=C["gold"], width=3)
        texto(f, (x + 8 if x < 1000 else x - 8, 112), f"libre desde {txt(libre)}", 18, "gold", 1, anchor="la" if x < 1000 else "ra")
    if 0 <= k < len(SEL):
        n, a, b, ok = SEL[k]
        s = f"{n} empieza {txt(a)}" + ("  ✓" if ok else f" < libre: no")
        texto(f, (640, 660), s, 24, "green" if ok else "red", 1, anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 660), f"{sum(s[3] for s in SEL)} películas: B, C y E", 30, "green", aparece(f, f.c(4)), anchor="mm")


def e_porque(f):
    # intercambio: la primera del óptimo se cambia por la que acaba antes
    a1, b1 = hm("10:00"), hm("12:00")
    a2, b2 = hm("10:30"), hm("11:20")
    y1, y2 = 260, 360
    eje(f)
    u = aparece(f, f.c(0))
    peli(f, "1ª del óptimo", a1, b1, y1, u, c=C["purple"])
    peli(f, "resto del óptimo", hm("12:30"), hm("15:00"), y1, u, c=C["purple"])
    if f.t >= f.c(1):
        peli(f, "acaba antes", a2, b2, y2, aparece(f, f.c(1)), c=C["green"])
        x = X(b1)
        f.d.line((x, 200, x, 420), fill=C["gold"], width=2)
        f.d.line((X(b2), 200, X(b2), 420), fill=C["green"], width=2)
    if f.t >= f.c(2):
        texto(f, (640, 500), "cambiar una por otra no choca con el resto", 28, "gold", aparece(f, f.c(2)), anchor="mm")
        texto(f, (640, 550), "y deja aún más tiempo libre", 24, "muted", aparece(f, f.c(2) + 0.4), anchor="mm")


def e_minutos(f):
    texto(f, (640, 80), "minutos absolutos:  inicio = (D·24 + HH)·60 + MM", 28, "gold", aparece(f, f.c(0)), mono=True, anchor="mm")
    a, b = hm("22:00"), hm("26:00")
    ab = (a, b)
    eje(f, a, b, u=aparece(f, f.c(1)))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        x = X(hm("24:00"), *ab)
        f.d.line((x, 200, x, 590), fill=mix(C["bot"], C["muted"], u), width=2)
        texto(f, (x - 10, 210), "día 1", 20, "muted", u, anchor="rm")
        texto(f, (x + 10, 210), "día 2", 20, "muted", u, anchor="lm")
        peli(f, "23:30 + 90'", hm("23:30"), hm("25:00"), 330, f.lin(f.c(1), 1.0), c=C["purple"], ab=ab)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        descanso(f, hm("25:00"), 430, u, ab=ab)
        peli(f, "01:10", hm("25:10"), hm("25:50"), 430, f.lin(f.c(2), 1.0), c=C["green"], ab=ab)
        texto(f, (640, 530), "justo 10 minutos: se ven las dos", 26, "green", aparece(f, f.c(2) + 0.8), anchor="mm")


A = find_line(CPP, "for (Peli& p : pelis) {")
B = find_line(CPP, "cout << vistas")
CODE = codigo(CPP, A, B, maxc=84)
L_IN = find_line(CPP, "p.inicio = (dia * 24 + hh) * 60 + mm;")
L_SO = find_line(CPP, "sort(pelis.begin()")
L_IF = find_line(CPP, "if (p.inicio >= libreDesde) {")
L_LI = find_line(CPP, "libreDesde = p.fin + DESCANSO;")


def e_codigo(f):
    hl = {L_IN, L_IN + 1}
    if f.t >= f.c(1):
        hl = {L_SO}
    k, fr = paso_idx(f, f.c(2), f.T - 2.5, len(SEL))
    if 0 <= k < len(SEL):
        hl = {L_IF} if fr < 0.5 or not SEL[k][3] else {L_IF, L_LI - 1, L_LI}
    elif k >= len(SEL):
        hl = {B}
    f.code(10, 90, 830, 520, CODE, hl=hl, title="selección de actividades", size=15)
    x0, y0 = 880, 140
    texto(f, (x0, y0 - 40), "ordenadas por fin", 18, "muted", 1)
    libre = -10
    vistas = 0
    for q, (n, a, b, ok) in enumerate(SEL):
        y = y0 + q * 64
        hecho = q < k or (q == k and fr >= 0.5)
        c = (C["green"] if ok else C["dim"]) if hecho else COLS[n]
        caja(f, x0 + 30, y + 10, n, c=c, w=50, h=44, tam=22, borde=5 if q == k else 3)
        texto(f, (x0 + 70, y), f"{txt(a)}–{txt(b)}", 20, "text", 1, mono=True)
        if hecho and ok:
            libre, vistas = b + 10, vistas + 1
    texto(f, (x0, 470), f"libreDesde = {txt(libre) if libre >= 0 else '−10'}", 22, "gold", 1, mono=True)
    texto(f, (x0, 510), f"vistas = {vistas}", 26, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("la hora se lee con un char para saltar los dos puntos:  cin >> hh >> c >> mm", "text"),
             ("long long: 100.000 días ≈ 1,44·10⁸ minutos, más la duración", "text"),
             ("libreDesde empieza en −10: la primera siempre se puede ver", "text"),
             ("N ≤ 500.000:  O(N log N) por la ordenación", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Maratón de cine de terror", [
        "cada película: intervalo en minutos absolutos",
        "ordenar por hora de FIN",
        "coger cada una que empiece ≥ fin anterior + 10",
        "intercambio: la voraz es óptima · O(N log N)",
    ])


ESC = [
    Escena("Maratón de cine de terror. Ver el máximo número de películas enteras.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos la programación: cada película empieza a una hora y dura un tiempo. "
           "Entre una película y la siguiente hacen falta diez minutos libres, para salir de una sala y entrar en otra. "
           "¿Cuántas películas enteras se pueden ver como mucho?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("¿Y si cogemos siempre la que empieza antes? "
           "Aquí la primera es la A, que dura cuatro horas y lo tapa todo: solo una película. "
           "¿Y la más corta? "
           "Esta corta choca con las dos largas, que juntas sí se podían ver. Tampoco sirve.",
           e_malas, titulo="Lo que no funciona", extra=1.5),
    Escena("La buena es coger la que acaba antes. "
           "Ordenamos las películas por su hora de fin. "
           "Cogemos la primera, y apuntamos desde cuándo estamos libres: su fin más diez minutos. "
           "Cada película que empiece después de esa hora se coge; las demás se saltan. "
           "Salen tres: B, C y E.",
           e_voraz, titulo="La que acaba antes", extra=1.5),
    Escena("¿Por qué? Toma una solución óptima y su primera película. "
           "La que acaba antes de todas termina como muy tarde a la vez. "
           "Así que se pueden cambiar sin chocar con el resto, y queda incluso más tiempo libre. Repitiendo, la voraz es óptima.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("Hay películas que cruzan la medianoche. Para no tratarlas aparte, todo se pasa a minutos desde el principio. "
           "Una que empieza el día uno a las once y media y dura noventa minutos acaba a la una del día dos. "
           "Si la siguiente empieza a la una y diez, hay justo diez minutos: se pueden ver las dos.",
           e_minutos, titulo="La medianoche", extra=1.5),
    Escena("En el código, cada película se lee y se pasa a minutos absolutos. "
           "Se ordenan por la hora de fin. "
           "Y se recorren: si empieza después de libre desde, se ve, y libre desde pasa a ser su fin más diez.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Para leer la hora se usa un char que se come los dos puntos. "
           "Los minutos se guardan en long long para ir sobrados. "
           "Libre desde empieza en menos diez, para que la primera película siempre se pueda ver. "
           "Y el coste es ene log ene, por la ordenación.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es la selección de actividades. Se ordena por hora de fin y se coge cada película compatible con la última elegida.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/08-4", "../08-4_maraton_de_cine_de_terror.mp4", "08-4")
