"""Vídeo EJ 12-2 · Cine romántico a raudales (animado)."""
import bisect
import os
import re
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre
from vor_comun import caja, paso_idx, tick, args_preview, etiqueta

CPP = "../../12-Evaluacion/EJ_12-2/EJ_12-2.cpp"
TEMA = "Tema 12 · Programación dinámica III"
EJ1 = [(1, "11:00", 90), (1, "12:30", 90), (1, "12:45", 60)]
EJ2 = [(1, "11:00", 90), (1, "12:45", 60), (1, "11:00", 180)]
EJ3 = [(2, "12:00", 80), (1, "20:00", 80)]
COLP = [(236, 150, 64), (196, 150, 255), (110, 190, 255)]
ROSA = (255, 130, 170)


def minuto(d, hhmm):
    hh, mm = map(int, hhmm.split(":"))
    return (d - 1) * 1440 + hh * 60 + mm


def resuelve(pelis):
    """Mismo algoritmo que el .cpp: ordenar por inicio, sig con lower_bound, de N-1 a 0."""
    p = sorted(((minuto(d, h), minuto(d, h) + dur) for d, h, dur in pelis), key=lambda x: x[0])
    ini = [a for a, _ in p]
    N = len(p)
    mins = [0] * (N + 1)
    sig = [N] * N
    for i in range(N - 1, -1, -1):
        sig[i] = bisect.bisect_left(ini, p[i][1] + 10)
        mins[i] = max(mins[i + 1], (p[i][1] - p[i][0]) + mins[sig[i]])
    return p, sig, mins


def voraz(pelis):
    """El voraz del 08-4: ordenar por fin y coger la que antes acaba si cabe (10 min de margen)."""
    p = sorted(((minuto(d, h), minuto(d, h) + dur) for d, h, dur in pelis), key=lambda x: x[1])
    fin, n, tot, elegidas = -10 ** 9, 0, 0, []
    for a, b in p:
        if a >= fin + 10:
            n, tot, fin = n + 1, tot + b - a, b
            elegidas.append((a, b))
    return n, tot, elegidas


P1, S1, M1 = resuelve(EJ1)
P2, S2, M2 = resuelve(EJ2)
P3, S3, M3 = resuelve(EJ3)
assert (M1[0], M2[0], M3[0]) == (150, 180, 160)
VN, VT, VEL = voraz(EJ2)
assert (VN, VT) == (2, 150)


def hhmm(m):
    m %= 1440
    return f"{m // 60}:{m % 60:02}"


# ------------------------------------------------------------------ línea de tiempo
class Cartelera:
    def __init__(self, pelis, x0=170, x1=1200, y0=170, dy=78, a=600, b=900):
        self.p, self.x0, self.x1, self.y0, self.dy, self.a, self.b = pelis, x0, x1, y0, dy, a, b

    def x(self, m):
        return self.x0 + (m - self.a) * (self.x1 - self.x0) / (self.b - self.a)

    def eje(self, f, u=1.0):
        y = self.y0 + self.dy * len(self.p) + 4
        f.d.line((self.x0, y, self.x1, y), fill=mix(C["bot"], C["muted"], u), width=2)
        for m in range(self.a, self.b + 1, 60):
            f.d.line((self.x(m), y - 6, self.x(m), y + 6), fill=mix(C["bot"], C["muted"], u), width=2)
            f.d.text((self.x(m), y + 22), hhmm(m), font=font(17, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")
            f.d.line((self.x(m), self.y0 - 10, self.x(m), y - 8), fill=mix(C["bot"], (52, 84, 128), u), width=1)

    def peli(self, f, k, nombre, u=1.0, estado=None, margen=False):
        """estado: None, 'si', 'no'."""
        if u <= 0:
            return
        a, b = self.p[k]
        y = self.y0 + self.dy * k
        col = COLP[k % len(COLP)]
        if estado == "no":
            col = mix(C["bot"], col, 0.35)
        x1 = lerp(self.x(a), self.x(b), ease(u))
        f.d.rounded_rectangle((self.x(a), y, max(self.x(a) + 4, x1), y + 48), 10, fill=mix(C["bot"], col, u))
        if margen:
            f.d.rectangle((self.x(b), y + 6, self.x(b + 10), y + 42), fill=mix(C["bot"], (70, 80, 100), u))
            f.d.text((self.x(b + 5), y - 10), "10'", font=font(15, True), fill=C["muted"], anchor="mm")
        f.d.text((self.x(a) - 12, y + 24), nombre, font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="rm")
        if u > 0.6:
            f.d.text((self.x(a) + 12, y + 24), f"{hhmm(a)} · {b - a}'", font=font(19, True),
                     fill=C["node_t"], anchor="lm")
        if estado:
            tick(f, max(self.x(a) + 4, x1) + 26, y + 24, estado == "si", u)


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        u = f.p(0.2, 0.6)
        f.d.rounded_rectangle((820, 230, 1120, 420), 12, fill=mix(C["bot"], (20, 20, 30), u),
                              outline=mix(C["bot"], (180, 40, 60), u), width=8)
        v = f.p(0.7, 0.6)
        x, y, r = 970, 315, 34
        f.d.ellipse((x - r - 30, y - r, x - 30 + r, y + r), fill=mix((20, 20, 30), ROSA, v))
        f.d.ellipse((x + 30 - r, y - r, x + 30 + r, y + r), fill=mix((20, 20, 30), ROSA, v))
        f.d.polygon([(x - 62, y + 12), (x + 62, y + 12), (x, y + 80)], fill=mix((20, 20, 30), ROSA, v))
    portada(f, "12-2", "Cine romántico a raudales", TEMA, dib)


def e_problema(f):
    texto(f, (640, 80), "Maratón de cine romántico", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (120, 170), "Cada película:  día D,  hora HH:MM,  duración en minutos", 26, "text", u, mono=True)
        texto(f, (120, 220), "N ≤ 300.000 películas", 24, "muted", u, mono=True)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (120, 300), "• se ven enteras", 26, "text", u)
        texto(f, (120, 345), "• 10 minutos libres entre una y la siguiente", 26, "text", u)
    if f.t >= f.c(3):
        etiqueta(f, (640, 470), "objetivo: el máximo de MINUTOS viendo películas", 30, "gold", aparece(f, f.c(3)))
    if f.t >= f.c(4):
        etiqueta(f, (640, 570), "08-4 (terror): máximo NÚMERO de películas  →  aquí, con pesos", 24, ROSA, aparece(f, f.c(4)))


def e_ejemplo1(f):
    cb = Cartelera(P1)
    cb.eje(f, aparece(f, f.c(0)))
    nombres = "ABC"
    est = [None, None, None]
    if f.t >= f.c(1):
        est[1] = "no"
    if f.t >= f.c(2):
        est[0], est[2] = "si", "si"
    for k in range(3):
        cb.peli(f, k, nombres[k], f.p(f.c(0) + 0.3 * k, 0.8), est[k], margen=(k == 0 and f.t >= f.c(1)))
    texto(f, (640, 90), "Ejemplo 1", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 520), "A acaba a las 12:30 y B empieza a las 12:30: faltan los 10 minutos", 24, "red", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 600), f"A + C = 90 + 60 = {M1[0]} minutos", 28, "green", aparece(f, f.c(2)))


def e_voraz(f):
    cb = Cartelera(P2)
    cb.eje(f)
    nombres = "ABC"
    texto(f, (640, 90), "Ejemplo 2 · ¿sirve el voraz del 08-4?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    est = [None] * 3
    vz = f.t >= f.c(1) and f.t < f.c(3)
    if vz:
        est = ["si", "no", "si"]
    if f.t >= f.c(3):
        est = ["no", "si", "no"]
    for k in range(3):
        cb.peli(f, k, nombres[k], 1.0, est[k] if (vz or f.t >= f.c(3)) else None)
    if f.t >= f.c(1):
        etiqueta(f, (640, 520), f"voraz (la que antes acaba): A y C → {VN} películas, {VT} minutos", 24,
                 "red" if f.t >= f.c(2) else "text", aparece(f, f.c(1)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 600), f"mejor: solo B → {M2[0]} minutos", 28, "green", aparece(f, f.c(3)))


def e_preparar(f):
    texto(f, (640, 80), "Preparar los datos", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        texto(f, (100, 150), "minutos absolutos:  ini = (D − 1)·1440 + HH·60 + MM,   fin = ini + dur", 24, "text", u, mono=True)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (100, 220), "ejemplo 3:", 24, "muted", u)
        texto(f, (120, 262), f"día 2 12:00 → {minuto(2, '12:00')}      día 1 20:00 → {minuto(1, '20:00')}", 24, "text", u, mono=True)
        texto(f, (120, 304), f"ordenadas por inicio: [{P3[0][0]}, {P3[0][1]})  [{P3[1][0]}, {P3[1][1]})  →  {M3[0]} minutos",
              24, "text", aparece(f, f.c(1) + 1.5), mono=True)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (100, 390), "sig(i) = primera película con  ini ≥ fin_i + 10", 26, "gold", u, mono=True)
        ini = [a for a, _ in P1]
        for k, a in enumerate(ini):
            caja(f, 260 + 130 * k, 480, a, c=COLP[k], w=110, h=52, tam=24, u=u)
            texto(f, (260 + 130 * k, 522), "ABC"[k], 20, "muted", u, anchor="mm")
        texto(f, (100, 470), "inicios", 22, "muted", u)
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (680, 470), f"A acaba en {P1[0][1]}: lower_bound({P1[0][1] + 10}) → C", 24, "text", u, mono=True)
        x = 260 + 130 * S1[0]
        f.d.rectangle((x - 60, 450, x + 60, 510), outline=C["gold"], width=4)
        texto(f, (680, 520), "búsqueda binaria: O(log N)", 22, "gold", u)


def e_recurrencia(f):
    texto(f, (60, 80), "minutos(i) = máximo de minutos eligiendo entre la película i y las siguientes", 24, "muted",
          aparece(f, f.c(0)), bold=False)
    texto(f, (60, 160), "Caso base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 205, "minutos(N) =", [("0", "")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia  (0 ≤ i < N)", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 80, "minutos(i) = max", [("minutos(i + 1)", "no ver la i"),
                                                     ("dur_i + minutos(sig(i))", "ver la i")],
                aparece(f, f.c(2)), colores=[AZUL, NARANJA])
    texto(f, (60, y + 60), "Respuesta:  minutos(0)", 28, "green", aparece(f, f.c(4)), mono=True)


def traza(f, P, S, Mn, t0, t1, fin_t, titulo, est_final):
    N = len(P)
    cb = Cartelera(P, y0=150, dy=70)
    cb.eje(f)
    # un paso por frase: la frase q + 1 explica la película N - 1 - q
    k, fr = -1, 0.0
    for q in range(N):
        if f.t >= f.c(q + 1):
            k, fr = q, min(1.0, (f.t - f.c(q + 1)) / 1.2)
    if f.t >= t1:
        k = N
    i = N - 1 - k if 0 <= k < N else None
    hechos = set(range(N - 1 - min(k, N) + 1, N + 1)) if k >= 0 else {N}
    if f.t >= fin_t:
        hechos, i = set(range(N + 1)), None
    for q in range(N):
        e = None
        if f.t >= fin_t:
            e = est_final[q]
        cb.peli(f, q, "ABC"[q], 1.0, e, margen=(q == i))
    texto(f, (640, 90), titulo, 28, "gold", 1, anchor="mm")
    # vector minutos
    x0, y0, cw = 330, 470, 130
    texto(f, (x0 - 20, y0 + 30), "minutos", 24, "muted", 1, mono=True, anchor="rm")
    for q in range(N + 1):
        x = x0 + q * cw
        hl = q == i
        f.d.rectangle((x, y0, x + cw - 14, y0 + 60), fill=C["panel"], outline=C["gold"] if hl else C["border"], width=4 if hl else 2)
        if q in hechos and q != i:
            f.d.text((x + (cw - 14) / 2, y0 + 30), str(Mn[q]), font=font(28, True), fill=C["text"], anchor="mm")
        f.d.text((x + (cw - 14) / 2, y0 + 78), str(q) + ("" if q == N else f" ({'ABC'[q]})"), font=font(17, True), fill=C["dim"], anchor="mm")
    if i is not None:
        u = fr
        cx = lambda q: x0 + q * cw + (cw - 14) / 2
        flecha(f, (cx(i + 1) - 30, y0 + 30), (lerp(cx(i + 1) - 30, cx(i) + 34, ease(u)), y0 + 30), AZUL, w=4)
        s = S[i]
        ya = y0 - 22
        f.d.line((cx(s), y0 - 2, cx(s), ya), fill=NARANJA, width=4)
        f.d.line((cx(s), ya, cx(i) + 10, ya), fill=NARANJA, width=4)
        flecha(f, (cx(i) + 10, ya), (cx(i) + 10, y0 - 4), NARANJA, w=4)
        a, b = P[i]
        no, si = Mn[i + 1], (b - a) + Mn[s]
        txt = f"minutos[{i}] = max({no}, {b - a} + minutos[{s}]) = max({no}, {si}) = {Mn[i]}"
        texto(f, (640, 600), txt, 24, "text", 1, mono=True, anchor="mm")
        texto(f, (640, 640), f"sig({i}) = {s}:  primera con ini ≥ {b} + 10", 20, NARANJA, 1, anchor="mm")
    elif f.t >= fin_t:
        etiqueta(f, (640, 620), f"minutos[0] = {Mn[0]}", 30, "green", aparece(f, fin_t), mono=True)


def e_traza1(f):
    traza(f, P1, S1, M1, f.c(1), f.c(4), f.c(4), "Traza del ejemplo 1 (de N − 1 hacia 0)", ["si", "no", "si"])


def e_traza2(f):
    traza(f, P2, S2, M2, f.c(1), f.c(4), f.c(4), "Traza del ejemplo 2", ["no", "si", "no"])


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "cout << minutos[0]")
_FUERA = ("int N;", "cin >> N;", "long long d, dur;", "int hh, mm;", "char dos;")
CODE = [(n, s) for n, s in codigo(CPP, A, B + 1, maxc=96) if s.strip() and s.strip() not in _FUERA]
L_LEE = (find_line(CPP, "p[i].ini = (d - 1) * 1440 + hh * 60 + mm;"), find_line(CPP, "p[i].fin = p[i].ini + dur;"))
L_SORT = (find_line(CPP, "sort(p.begin(), p.end());"), find_line(CPP, "for (int i = 0; i < N; ++i) inicios[i] = p[i].ini;"))
L_SIG = find_line(CPP, "int sig = lower_bound(")
L_MAX = find_line(CPP, "minutos[i] = max(minutos[i + 1]")
NOTAS = [(set(range(L_LEE[0], L_LEE[1] + 1)), "cada película pasa a minutos absolutos [ini, fin)"),
         (set(range(L_SORT[0], L_SORT[1] + 1)), "ordenar por inicio y guardar los inicios aparte"),
         ({L_SIG}, "sig con lower_bound sobre los inicios, buscando fin + 10"),
         ({L_MAX}, "no verla, o verla y saltar a sig"),
         ({B}, "la respuesta es minutos[0], en long long")]


def e_codigo(f):
    k = 0
    for q in range(len(NOTAS)):
        if f.t >= f.c(q):
            k = q
    hl, nota = NOTAS[k]
    f.code(20, 80, 1240, 500, CODE, hl=hl, title="resuelveCaso()", size=20)
    etiqueta(f, (640, 635), nota, 26, "gold", aparece(f, f.c(k)))


def e_errores(f):
    f.box(60, 110, 1160, 500, "errores típicos")
    items = [("10 minutos libres: la condición es  ini ≥ fin + 10  (ejemplo 1)", "text"),
             ("el total pasa de 2³¹: 300.000 películas de hasta 10⁶ minutos → long long", "red"),
             ("no vienen ordenadas y los días cuentan: minutos absolutos", "text"),
             ("buscar sig recorriendo todas es O(N²): con 300.000 no da tiempo", "text"),
             ("con lower_bound: O(N log N) tiempo y O(N) memoria", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 86 * k), s, 24, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Cine romántico a raudales", [
        "intervalos con pesos: el voraz del 08-4 ya no vale",
        "minutos absolutos y ordenar por inicio",
        "minutos(i) = max(minutos(i+1), dur_i + minutos(sig(i)))",
        "sig con búsqueda binaria: O(N log N), long long",
    ], cols=[ROSA, NARANJA, C["blue"], C["green"]])


ESC = [
    Escena("Cine romántico a raudales. Un problema de evaluación de programación dinámica sobre intervalos, con búsqueda binaria.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Dinamique Cinema quiere aprovechar un maratón de cine romántico. "
           "De cada película sabemos el día, la hora de comienzo y la duración en minutos, y puede haber hasta trescientas mil. "
           "Las películas se ven enteras, y entre una y la siguiente necesita diez minutos libres. "
           "Su objetivo es estar viendo películas el máximo de minutos. "
           "Es el problema del maratón de terror del tema ocho, pero allí se contaban películas y aquí se cuentan minutos.",
           e_problema, titulo="Qué piden", extra=1.5),
    Escena("En el primer ejemplo hay tres películas, A, B y C. "
           "A acaba a las doce y media, justo cuando empieza B: sin los diez minutos de descanso no se pueden ver las dos. "
           "Lo mejor es A y luego C, que empieza a menos cuarto: noventa más sesenta, ciento cincuenta minutos.",
           e_ejemplo1, titulo="Ejemplo 1", extra=1.5),
    Escena("¿Vale el voraz del tema ocho, coger siempre la que antes termina? Veamos el segundo ejemplo. "
           "El voraz elige A, que acaba primero, y luego C: dos películas, ciento cincuenta minutos. "
           "Es el máximo número de películas, pero no de minutos. "
           "La película B sola dura ciento ochenta, y solapa con las otras dos. Hace falta programación dinámica.",
           e_voraz, titulo="¿Un voraz?", extra=1.5),
    Escena("Primero preparamos los datos: cada película pasa a minutos absolutos, contando los días, y su fin es el inicio más la duración. "
           "Así, en el tercer ejemplo la película del día dos va después de la del día uno, aunque aparezca antes; se ordenan por inicio. "
           "Para cada película llamamos sig a la primera que empieza al menos diez minutos después de su fin. "
           "Como los inicios están ordenados, se encuentra con búsqueda binaria.",
           e_preparar, titulo="Preparar los datos", extra=1.5),
    Escena("Definimos minutos de i: lo máximo que se puede ver eligiendo entre la película i y las siguientes. "
           "Si no quedan películas, cero. "
           "Para la película i hay dos opciones: no verla, y seguir con la i más uno; "
           "o verla, sumar su duración, y saltar a sig de i, la primera compatible. "
           "La respuesta es minutos de cero.",
           e_recurrencia, titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos el vector de atrás hacia delante en el primer ejemplo. "
           "La película C es la última: verla da sesenta. "
           "Para B, sig es tres, porque nada empieza después: noventa frente a sesenta, noventa. "
           "Para A, sig es C, la de las doce cuarenta y cinco: ver A y seguir desde C da noventa más sesenta, ciento cincuenta. "
           "Ese es el resultado.",
           e_traza1, titulo="Traza del ejemplo 1", extra=2.0),
    Escena("En el segundo ejemplo, ordenadas por inicio, A y B empiezan a las once y C a las doce cuarenta y cinco. "
           "C da sesenta. "
           "B, de ciento ochenta, no deja ver nada más: ciento ochenta. "
           "A más C dan ciento cincuenta, menos que los ciento ochenta de seguir desde B. "
           "Resultado: ciento ochenta, solo la película larga.",
           e_traza2, titulo="Traza del ejemplo 2", extra=2.0),
    Escena("En el código, cada película se lee y se pasa a minutos absolutos. "
           "Se ordenan por inicio y se guardan los inicios en un vector aparte. "
           "Para cada i, de atrás hacia delante, lower bound busca la primera que empieza en fin más diez. "
           "Y minutos de i es el máximo entre no verla y verla. "
           "Al final se escribe minutos de cero.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Errores típicos. Los diez minutos: la condición es inicio mayor o igual que fin más diez, como muestra el primer ejemplo. "
           "El total puede pasar de dos elevado a treinta y uno, así que hace falta long long. "
           "Las películas no vienen ordenadas y los días cuentan. "
           "Buscar sig recorriendo todas las siguientes es cuadrático, y con trescientas mil no da tiempo. "
           "Con búsqueda binaria el coste es ene por logaritmo de ene.",
           e_errores, titulo="Errores típicos", extra=1.5),
    Escena("Resumiendo: son intervalos con pesos, y el voraz del tema ocho ya no sirve. "
           "Se pasan a minutos absolutos y se ordenan por inicio. "
           "Cada película se ve o no se ve, y si se ve se salta a la siguiente compatible. "
           "Esa siguiente se busca con búsqueda binaria, y el resultado va en long long.",
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
    args_preview(ESC, "preview/12-2", "../12-2_cine_romantico_a_raudales.mp4", "12-2")
