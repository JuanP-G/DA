"""Vídeo EJ 02-4 · La ley D'Hondt (animado)."""
from fractions import Fraction
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-4/EJ_02-4.cpp"
TEMA = "Tema 2 · Colas de prioridad"
VOTOS = [100, 226, 20, 80, 170]
NE = 4
COLS = {0: C["blue"], 1: C["red"], 2: C["dim"], 3: C["purple"], 4: C["green"]}


def antes(a, b):
    # a = (votos, escaños, orden): va antes el de mayor coeficiente, luego más votos, luego orden menor
    ca, cb = Fraction(a[0], a[1] + 1), Fraction(b[0], b[1] + 1)
    if ca != cb:
        return ca > cb
    if a[0] != b[0]:
        return a[0] > b[0]
    return a[2] < b[2]


def simula():
    pq = Monticulo(antes)
    for i, v in enumerate(VOTOS):
        pq.push(i, (v, 0, i))
    pasos, esc = [], [0] * len(VOTOS)
    for k in range(NE):
        ant = pq.copia()
        i, (v, e, o) = pq.top()
        coef = v / (e + 1)
        pq.update(i, (v, e + 1, o))
        esc[i] += 1
        pasos.append((ant, pq.copia(), f"escaño {k + 1}: {v}/{e + 1} = {coef:.1f} → candidatura {i}", "text"))
    return pasos, esc


PASOS, ESC_ = simula()


def etq(e, p):
    return f"{p[0]}/{p[1] + 1}\n{p[0] / (p[1] + 1):.0f}"


def e_portada(f):
    def dib(f):
        for k, (h, c) in enumerate([(120, C["red"]), (90, C["green"]), (60, C["blue"])]):
            u = f.p(0.3 + 0.15 * k, 0.6)
            f.d.rectangle((860 + k * 80, 420 - h * u, 920 + k * 80, 420), fill=mix(C["bot"], c, u))
    portada(f, "EJ 02-4", "La ley D'Hondt", TEMA, dib)


def barras(f, u=1.0, esc=None, marca=None):
    mx = max(VOTOS)
    for i, v in enumerate(VOTOS):
        x = 220 + i * 200
        h = 300 * v / mx * u
        f.d.rectangle((x - 50, 520 - h, x + 50, 520), fill=mix(C["bot"], mix(C["panel"], COLS[i], 0.6), u), outline=mix(C["bot"], C["gold"] if marca == i else COLS[i], u), width=4 if marca == i else 2)
        texto(f, (x, 540), f"{v}", 20, "text", u, anchor="mm")
        texto(f, (x, 570), f"cand. {i}", 18, "muted", u, anchor="mm")
        if esc:
            for q in range(esc[i]):
                f.d.ellipse((x - 14, 480 - h - 40 - q * 34, x + 14, 480 - h - 12 - q * 34), fill=C["gold"])


def e_problema(f):
    barras(f, f.lin(f.c(0), 1.0))
    if f.t >= f.c(1):
        etiqueta(f, (640, 90), f"repartir {NE} escaños con el método D'Hondt", 26, "gold", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 650), "salida: escaños de cada candidatura, en el orden de la entrada", 22, "text", aparece(f, f.c(2)))


def e_regla(f):
    texto(f, (640, 80), "cada escaño, al mayor coeficiente  votos / (escaños + 1)", 28, "gold", aparece(f, f.c(0)), anchor="mm", mono=False)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        for k, (s, c) in enumerate([("226 / 1 = 226", "red"), ("ganó uno → 226 / 2 = 113", "red"), ("ganó dos → 226 / 3 = 75,3", "red")]):
            texto(f, (640, 180 + 60 * k), s, 28, c, aparece(f, f.c(1) + 0.6 * k), mono=True, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 420), "empate de coeficiente: más votos; si no, la que va antes", 24, "text", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 500), "cola de MÁXIMOS por coeficiente: la cima se lleva el escaño", 24, "green", aparece(f, f.c(3)))
    if f.t >= f.c(4):
        etiqueta(f, (640, 580), "comparar a/(e+1) con b/(f+1) sin dividir:  a·(f+1)  vs  b·(e+1)", 24, "muted", aparece(f, f.c(4)), mono=True)


def lateral(f, k, fr):
    n = k + (1 if fr > 0.4 else 0)
    esc = [0] * len(VOTOS)
    for q in range(n):
        i = PASOS[q][0][0][0]
        esc[i] += 1
    texto(f, (60, 130), "escaños", 22, "muted", 1)
    for i, v in enumerate(VOTOS):
        y = 190 + i * 70
        caja(f, 120, y, f"{v}", c=COLS[i], w=100, h=48, tam=20)
        for q in range(esc[i]):
            f.d.ellipse((190 + q * 36, y - 14, 218 + q * 36, y + 14), fill=C["gold"])


def e_traza(f):
    escena_traza(f, PASOS, etq, colores=COLS, lateral=lateral, cx=840, ancho=680, titulo="cola de máximos: votos/(esc+1)")
    if f.t >= f.T - 1.5:
        etiqueta(f, (840, 690), "salida: " + " ".join(map(str, ESC_)), 26, "green", aparece(f, f.T - 1.5), mono=True)


A_L = find_line(CPP, "struct Candidatura {")
B_L = find_line(CPP, "cout << (i > 0 ? \" \" : \"\") << res[i];")
L_CMP = find_line(CPP, "long long izq = votos * (1 + o.escanios);")
F_L = find_line(CPP, "priority_queue<Candidatura> cola;")
L_ESC = find_line(CPP, "Candidatura c = cola.top(); cola.pop();")
L_RES = find_line(CPP, "res[cola.top().orden] = cola.top().escanios;")


def e_codigo(f):
    escena_codigo(f, CPP, [(A_L, A_L + 11, {L_CMP, L_CMP + 1, L_CMP + 2}, "struct Candidatura"),
                           (A_L, A_L + 11, {L_CMP + 3, L_CMP + 4}, "struct Candidatura"),
                           (F_L, B_L, {L_ESC, L_ESC + 1, L_ESC + 2}, "reparto"),
                           (F_L, B_L, {L_RES - 1, L_RES, L_RES + 1}, "reparto")], size=19)


def e_detalles(f):
    escena_lista(f, [("multiplicar en cruz evita los decimales (y sus errores de redondeo)", "text"),
                     ("long long: votos × escaños puede pasar de 2.000 millones", "text"),
                     ("orden guarda la posición de entrada: desempate y salida", "text"),
                     ("N escaños, cada uno O(log C):  O((C + N) log C)", "gold")])


def e_cierre(f):
    cierre(f, "La ley D'Hondt", [
        "cola de máximos por votos / (escaños + 1)",
        "la cima gana un escaño y vuelve a la cola",
        "comparar en cruz, con long long",
        "desempate: más votos, luego orden de entrada",
    ])


ESC = [
    Escena("La ley de Hondt. Repartir escaños con una cola de prioridad.", e_portada, titulo="Portada", extra=1.0),
    Escena("Varias candidaturas han recibido sus votos. "
           "Hay que repartir ene escaños con el método de Hondt. "
           "Y escribir cuántos escaños se lleva cada una, en el orden de la entrada.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Cada escaño va a la candidatura con mayor coeficiente: sus votos entre los escaños que ya tiene más uno. "
           "Doscientos veintiséis empieza valiendo doscientos veintiséis; cuando gana un escaño, pasa a ciento trece; con dos, a setenta y cinco. "
           "Si dos coeficientes empatan, gana la de más votos, y si no, la que aparece antes. "
           "Con una cola de máximos por coeficiente, la cima se lleva cada escaño. "
           "Para comparar sin dividir, se multiplica en cruz.",
           e_regla, titulo="La regla", extra=1.5),
    Escena("Primer escaño: doscientos veintiséis, candidatura uno, que pasa a ciento trece. "
           "Segundo: ciento setenta, candidatura cuatro. "
           "Tercero: ciento trece, otra vez la uno. "
           "Cuarto: cien, la candidatura cero. El resultado es uno, dos, cero, cero, uno.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, el operador menor compara los coeficientes multiplicando en cruz. "
           "Si empatan, por votos y por orden. "
           "Para cada escaño se saca la cima, se le suma un escaño y vuelve a la cola. "
           "Al final se vacía la cola guardando los escaños en la posición de cada candidatura.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Multiplicar en cruz evita los decimales. "
           "Los productos van en long long. "
           "El campo orden sirve para desempatar y para escribir la salida. "
           "Y el coste es ce más ene por logaritmo de ce.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de máximos por coeficiente; la cima gana el escaño y vuelve con un escaño más.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-4", "../02-4_la_ley_dhondt.mp4", "02-4")
