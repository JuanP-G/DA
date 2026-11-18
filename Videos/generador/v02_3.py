"""Vídeo EJ 02-3 · Reina del súper (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-3/EJ_02-3.cpp"
TEMA = "Tema 2 · Colas de prioridad"
NC = 4
CLI = [5, 5, 3, 3, 3]
COLS = {1: C["blue"], 2: NARANJA, 3: C["green"], 4: C["purple"]}


def simula():
    pq = Monticulo(lambda a, b: a < b)        # (libre, caja)
    for c in range(1, NC + 1):
        pq.push(c, (0, c))
    pasos = []
    for t in CLI:
        antes = pq.copia()
        c, (lib, _) = pq.top()
        pq.update(c, (lib + t, c))
        pasos.append((antes, pq.copia(), f"cliente de {t}: caja {c} (libre en {lib}) hasta {lib + t}", "text"))
    c, (lib, _) = pq.top()
    pasos.append((pq.copia(), pq.copia(), f"Ismael: la cima es la caja {c}", "gold"))
    return pasos, c


PASOS, CAJA = simula()


def etq(e, p):
    return f"caja {e}\n{p[0]}"


def cajero(f, x, y, c, u=1.0, ocupado=False):
    if u <= 0:
        return
    col = COLS[c]
    f.d.rounded_rectangle((x - 50, y, x + 50, y + 50), 8, fill=mix(C["bot"], mix(C["panel"], col, 0.4), u), outline=mix(C["bot"], col, u), width=3)
    f.d.text((x, y + 25), f"caja {c}", font=font(18, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def persona(f, x, y, t, u=1.0, c=None):
    if u <= 0:
        return
    c = c or C["gold"]
    f.d.ellipse((x - 12, y - 40, x + 12, y - 16), fill=mix(C["bot"], c, u))
    f.d.rounded_rectangle((x - 18, y - 14, x + 18, y + 20), 8, fill=mix(C["bot"], mix(C["panel"], c, 0.5), u), outline=mix(C["bot"], c, u), width=2)
    f.d.text((x, y + 4), str(t), font=font(16, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def e_portada(f):
    def dib(f):
        cajero(f, 900, 300, 1, f.p(0.3, 0.5))
        cajero(f, 1030, 300, 2, f.p(0.4, 0.5))
        for k in range(3):
            persona(f, 900 + k * 60, 450, "", f.p(0.6 + 0.1 * k, 0.4))
    portada(f, "EJ 02-3", "Reina del súper", TEMA, dib)


def e_problema(f):
    for c in range(1, NC + 1):
        cajero(f, 250 + (c - 1) * 260, 140, c, aparece(f, f.c(0) + 0.15 * c))
    if f.t >= f.c(1):
        for k, t in enumerate(CLI):
            persona(f, 640 - 2 * 70 + k * 70, 420, t, aparece(f, f.c(1) + 0.15 * k))
        texto(f, (640, 480), "una sola fila; cada cliente va a la primera caja que quede libre", 22, "text", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        persona(f, 640 + 3 * 70 + 20, 420, "?", aparece(f, f.c(2)), c=C["red"])
        etiqueta(f, (640, 600), "¿en qué caja acabará Ismael, el último de la fila?", 26, "gold", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 90), "cola de mínimos por (hora en que queda libre, nº de caja)", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 260), "el siguiente cliente va a la cima", 26, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 340), "esa caja queda libre más tarde: libre + tiempo del cliente", 24, "green", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 460), "empate: la caja de número menor (el par lo compara así)", 24, "muted", aparece(f, f.c(3)))


def lateral(f, k, fr):
    texto(f, (80, 150), "fila:", 22, "muted", 1)
    hechos = k + (1 if fr > 0.4 else 0)
    for q, t in enumerate(CLI):
        persona(f, 120 + q * 60, 240, t, 1, c=C["dim"] if q < hechos else C["gold"])
    persona(f, 120 + len(CLI) * 60, 240, "I", 1, c=C["red"])


def e_traza(f):
    escena_traza(f, PASOS, etq, colores=COLS, lateral=lateral)


A_L = find_line(CPP, "priority_queue<pair<int, int>")
B_L = find_line(CPP, "cout << cola.top().second")
L_INI = find_line(CPP, "cola.push(pair<int, int>(0, i));")
L_TOP = find_line(CPP, "pair<int, int> cajero = cola.top(); cola.pop();")


def e_codigo(f):
    escena_codigo(f, CPP, [(A_L, B_L, {A_L}, "cajas"), (A_L, B_L, {L_INI}, "cajas"),
                           (A_L, B_L, {L_TOP, L_TOP + 1, L_TOP + 2}, "cajas"), (A_L, B_L, {B_L}, "cajas")], size=20)


def e_detalles(f):
    escena_lista(f, [("pair<int,int> = (libre, caja): con greater, empate → caja menor", "text"),
                     ("más cajas que clientes: alguna sigue libre en 0 y gana la menor", "text"),
                     ("no hace falta guardar a qué caja va cada cliente", "text"),
                     ("C clientes, cada uno O(log N):  O(C log N)", "gold")])


def e_cierre(f):
    cierre(f, "Reina del súper", [
        "cola de mínimos de (libre, caja)",
        "cada cliente: top, suma su tiempo, push",
        "Ismael va a la caja de la cima",
        "O(C log N)",
    ])


ESC = [
    Escena("Reina del súper. Adivinar en qué caja acabará el último de la fila.", e_portada, titulo="Portada", extra=1.0),
    Escena("Un supermercado tiene ene cajas; aquí, cuatro. "
           "Hay una sola fila, y cada cliente va a la primera caja que quede libre. Sabemos cuánto tarda cada uno. "
           "Ismael va el último. ¿En qué caja le atenderán?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Guardamos las cajas en una cola de mínimos, por la hora en que quedan libres y el número de caja. "
           "El siguiente cliente va a la caja de la cima. "
           "Esa caja queda libre más tarde: se le suma el tiempo del cliente y vuelve a la cola. "
           "Si dos cajas quedan libres a la vez, va la de número menor.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Las cuatro cajas empiezan libres. Los dos clientes de cinco van a las cajas uno y dos. "
           "Los de tres, a las cajas tres y cuatro. "
           "El último de tres va a la caja tres, que se libera en tres. "
           "Ahora la cima es la caja cuatro: ahí irá Ismael.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, una cola de mínimos de pares. "
           "Todas las cajas entran libres en el instante cero. "
           "Cada cliente saca la cima, le suma su tiempo y la vuelve a meter. "
           "Al final, la cima es la caja de Ismael.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("El par libre, caja hace que el empate lo gane la caja menor sin escribir comparador. "
           "Si hay más cajas que clientes, alguna se queda en cero. "
           "No hace falta guardar a qué caja va cada cliente. "
           "Y el coste es ce por logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de mínimos con la hora en que queda libre cada caja; cada cliente coge la cima, y Ismael, la cima del final.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-3", "../02-3_reina_del_super.mp4", "02-3")
