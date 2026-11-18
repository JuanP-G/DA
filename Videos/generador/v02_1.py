"""Vídeo EJ 02-1 · Lo que cuesta sumar (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo, arbol, arbol_anim

CPP = "../../2-Colas de prioridad/EJ_02-1/EJ_02-1.cpp"
TEMA = "Tema 2 · Colas de prioridad"
NUMS = [3, 1, 4, 2]


def simula(nums):
    pq = Monticulo(lambda a, b: a < b)
    for k, v in enumerate(nums):
        pq.push(k, v)
    nid, esf, pasos = len(nums), 0, []
    while len(pq.a) > 1:
        antes = pq.copia()
        a = pq.pop()
        b = pq.pop()
        esf += a[1] + b[1]
        pq.push(nid, a[1] + b[1])
        nid += 1
        pasos.append((a[1], b[1], esf, antes, pq.copia()))
    return pasos


PASOS = simula(NUMS)


def bloque(f, x, y, v, u=1.0, c=None, esc=12):
    if u <= 0:
        return
    c = c or C["blue"]
    w = 40 + v * esc
    f.d.rounded_rectangle((x - w / 2, y - 28, x + w / 2, y + 28), 10, fill=mix(C["bot"], mix(C["panel"], c, 0.45), u), outline=mix(C["bot"], c, u), width=3)
    f.d.text((x, y), str(v), font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def e_portada(f):
    def dib(f):
        bloque(f, 880, 300, 3, f.p(0.3, 0.5))
        texto(f, (960, 300), "+", 34, "gold", f.p(0.5, 0.5), anchor="mm")
        bloque(f, 1040, 300, 4, f.p(0.6, 0.5))
    portada(f, "EJ 02-1", "Lo que cuesta sumar", TEMA, dib)


def e_problema(f):
    for k, v in enumerate(NUMS):
        bloque(f, 300 + k * 220, 220, v, aparece(f, f.c(0) + 0.2 * k))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        bloque(f, 470, 400, 3, u, c=C["green"])
        texto(f, (560, 400), "+", 34, "gold", u, anchor="mm")
        bloque(f, 640, 400, 4, u, c=C["green"])
        texto(f, (760, 400), "cuesta 7", 28, "gold", u, anchor="lm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 580), "sumarlos todos con el MÍNIMO esfuerzo total", 28, "text", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 70), "un número sumado pronto se vuelve a pagar en cada suma siguiente", 24, "text", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (330, 150), "en orden: 30 + 40 + 50 + 60", 24, "red", u, anchor="mm")
        for k, (s, v) in enumerate([("30+40", 70), ("70+50", 120), ("120+60", 180)]):
            texto(f, (330, 210 + k * 50), f"{s} = {v}", 24, "text", aparece(f, f.c(1) + 0.4 * k), mono=True, anchor="mm")
        texto(f, (330, 380), "total 370", 28, "red", aparece(f, f.c(1) + 1.4), anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (950, 150), "siempre los dos más pequeños", 24, "green", u, anchor="mm")
        for k, (s, v) in enumerate([("30+40", 70), ("50+60", 110), ("70+110", 180)]):
            texto(f, (950, 210 + k * 50), f"{s} = {v}", 24, "text", aparece(f, f.c(2) + 0.4 * k), mono=True, anchor="mm")
        texto(f, (950, 380), "total 360", 28, "green", aparece(f, f.c(2) + 1.4), anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 560), "cola de MÍNIMOS: saca dos, suma, mete el resultado", 26, "gold", aparece(f, f.c(3)))


def etq(e, p):
    return str(p)


def e_traza(f):
    k, fr = paso_idx(f, f.c(0), f.T - 2, len(PASOS))
    k = max(0, min(k, len(PASOS) - 1))
    a, b, esf, antes, despues = PASOS[k]
    if fr < 0.45:
        arbol(f, antes, 640, 170, 560, etq, marca={0}, r=38, tam=22)
    else:
        arbol_anim(f, antes, despues, (fr - 0.45) / 0.4, 640, 170, 560, etq, r=38, tam=22)
    etiqueta(f, (640, 520), f"saca {a} y {b}  →  mete {a + b}", 28, "text", 1, mono=True)
    prev = PASOS[k - 1][2] if k > 0 else 0
    etiqueta(f, (640, 600), f"esfuerzo = {prev} + {a + b} = {esf}", 28, "green", 1 if fr > 0.3 else 0.001, mono=True)
    texto(f, (640, 90), "cola de mínimos (montículo)", 22, "muted", 1, anchor="mm")
    if f.t >= f.T - 2:
        etiqueta(f, (640, 670), "queda un solo número: el esfuerzo es 19", 26, "gold", aparece(f, f.T - 2))


A_L = find_line(CPP, "priority_queue<long long, vector<long long>, greater<long long>> cola;")
B_L = find_line(CPP, "cout << esfuerzo")
CODE = [(n, t) for n, t in codigo(CPP, A_L, B_L, maxc=88)]
L_W = find_line(CPP, "while (cola.size() > 1) {")


def e_codigo(f):
    marcas = [(f.c(0), {A_L}), (f.c(1), {L_W, L_W + 1, L_W + 2}), (f.c(2), {L_W + 3, L_W + 4}), (f.c(3), {B_L})]
    hl = set()
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(40, 100, 1200, 460, CODE, hl=hl, title="cola de mínimos", size=21)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("long long: las sumas parciales crecen mucho", "text"),
             ("con un solo número el esfuerzo es 0 (el bucle no entra)", "text"),
             ("es la misma idea que el código de Huffman", "text"),
             ("N − 1 sumas, cada una O(log N):  O(N log N)", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Lo que cuesta sumar", [
        "sumar a + b cuesta a + b",
        "los pequeños primero: se pagan más veces",
        "cola de mínimos: saca dos, mete la suma",
        "O(N log N), con long long",
    ])


ESC = [
    Escena("Lo que cuesta sumar. Sumar muchos números con el menor esfuerzo posible.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos ene números. "
           "Sumar dos números cuesta lo que vale su suma: tres más cuatro cuesta siete. "
           "Hay que sumarlos todos con el mínimo esfuerzo total.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Cada resultado parcial se vuelve a sumar después, así que se paga otra vez. "
           "Si sumamos en orden treinta, cuarenta, cincuenta y sesenta, cuesta trescientos setenta. "
           "Si sumamos siempre los dos más pequeños, cuesta trescientos sesenta. "
           "Para tener siempre a mano los dos más pequeños, una cola de prioridad de mínimos.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Con tres, uno, cuatro y dos: sacamos uno y dos, sumamos tres, y lo metemos. "
           "Sacamos tres y tres, seis. "
           "Y cuatro y seis, diez. "
           "El esfuerzo total es diecinueve.",
           e_traza, titulo="El ejemplo", extra=2.5),
    Escena("En el código, una priority queue de mínimos con greater. "
           "Mientras quede más de un número, se sacan los dos de arriba. "
           "Su suma se añade al esfuerzo y se vuelve a meter en la cola. "
           "Al final se escribe el esfuerzo.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Se usa long long, porque las sumas crecen deprisa. "
           "Con un solo número el esfuerzo es cero. "
           "Es la misma idea que el código de Huffman. "
           "Y el coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: con una cola de mínimos, se suman siempre los dos más pequeños y el resultado vuelve a la cola.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-1", "../02-1_lo_que_cuesta_sumar.mp4", "02-1")
