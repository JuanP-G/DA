"""Vídeo EJ 02-2 · Unidad Curiosa de Monitorización (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-2/EJ_02-2.cpp"
TEMA = "Tema 2 · Colas de prioridad"
USU = [(1234, 300), (9000, 200)]
K = 5
COLS = {1234: C["blue"], 9000: NARANJA}


def simula():
    pq = Monticulo(lambda a, b: a < b)        # prioridad (t, id)
    per = dict(USU)
    for i, p in USU:
        pq.push(i, (p, i))
    pasos, salida = [], []
    for _ in range(K):
        antes = pq.copia()
        i, (t, _) = pq.top()
        salida.append(i)
        pq.update(i, (t + per[i], i))
        s = f"t = {t}: envío a {i}" + ("  (empate: id menor)" if any(p[0] == t and e != i for e, p in antes) else "")
        pasos.append((antes, pq.copia(), s, "text", t, i))
    return pasos, salida


PASOS, SALIDA = simula()
X0, X1, TA, TB = 120, 1180, 0, 1000


def X(t):
    return X0 + (t - TA) * (X1 - X0) / (TB - TA)


def etq(e, p):
    return f"{e}\nt={p[0]}"


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.6)
        f.d.rounded_rectangle((830, 260, 1090, 400), 14, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], C["green"], u), width=3)
        for k in range(4):
            f.d.line((850, 370 - k * 25, 1070, 370 - k * 25 - (k % 2) * 20), fill=mix(C["bot"], C["green"], u), width=2)
    portada(f, "EJ 02-2", "Unidad Curiosa de Monitorización", TEMA, dib)


def eje(f, y=560, u=1.0):
    f.d.line((X0, y, X1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    for t in range(TA, TB + 1, 100):
        f.d.line((X(t), y - 5, X(t), y + 5), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((X(t), y + 22), str(t), font=font(15, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def e_problema(f):
    eje(f, u=aparece(f, f.c(0)))
    for r, (i, p) in enumerate(USU):
        u = aparece(f, f.c(0) + 0.3 * r)
        texto(f, (X0 - 10, 300 + r * 100), str(i), 22, COLS[i], u, anchor="rm")
        for k in range(1, TB // p + 1):
            if f.t >= f.c(1) + 0.15 * k:
                caja(f, X(k * p), 300 + r * 100, "✉", c=COLS[i], w=44, h=40, tam=20)
        texto(f, (X0 + 10, 250 + r * 100), f"cada {p}", 18, COLS[i], u)
    if f.t >= f.c(2):
        etiqueta(f, (640, 120), "¿a quién van los K primeros envíos?  empate: id menor", 24, "gold", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 90), "cola de mínimos por (instante del próximo envío, id)", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 260), "saca el primero  →  se le envía", 26, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 340), "t += periodo  →  vuelve a la cola", 26, "green", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 460), "solo hay n elementos en la cola, aunque K sea enorme", 24, "muted", aparece(f, f.c(3)))


def lateral(f, k, fr):
    texto(f, (80, 150), "envíos:", 22, "muted", 1)
    n = k + (1 if fr > 0.4 else 0)
    for q in range(n):
        caja(f, 130, 210 + q * 62, SALIDA[q], c=COLS[SALIDA[q]], w=110, h=48, tam=22)


def e_traza(f):
    escena_traza(f, [p[:4] for p in PASOS], etq, colores=COLS, lateral=lateral)


A_L = find_line(CPP, "struct Envio {")
B_L = find_line(CPP, "cout << \"---\\n\";")
L_CMP = find_line(CPP, "if (t != o.t) return t > o.t;")
L_PU = find_line(CPP, "cola.push({ (long long)p, id, p });")
L_TOP = find_line(CPP, "Envio e = cola.top(); cola.pop();")


def e_codigo(f):
    F = find_line(CPP, "priority_queue<Envio")
    escena_codigo(f, CPP, [(A_L, A_L + 8, {L_CMP, L_CMP + 1}, "struct Envio"),
                           (F, B_L, {L_PU}, "la cola"),
                           (F, B_L, {L_TOP, L_TOP + 1}, "la cola"),
                           (F, B_L, {L_TOP + 2, L_TOP + 3}, "la cola")], size=20)


def e_detalles(f):
    escena_lista(f, [("operator> porque la cola es de mínimos (greater<Envio>)", "text"),
                     ("el primer envío de cada usuario es en t = periodo", "text"),
                     ("long long para t: los instantes crecen con K", "text"),
                     ("K envíos, cada uno O(log n):  O(K log n)", "gold")])


def e_cierre(f):
    cierre(f, "Unidad Curiosa de Monitorización", [
        "cola de mínimos por (próximo envío, id)",
        "saca, envía, suma el periodo y vuelve a meter",
        "empate: el id menor, en el comparador",
        "O(K log n)",
    ])


ESC = [
    Escena("Unidad Curiosa de Monitorización. A quién van los primeros envíos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Hay varios usuarios, cada uno recibe un informe cada cierto periodo: aquí, uno cada trescientos y otro cada doscientos. "
           "Los envíos se van sucediendo en el tiempo. "
           "Hay que decir a quién van los ka primeros; si coinciden, va antes el identificador menor.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Usamos una cola de prioridad de mínimos, ordenada por el instante del próximo envío y, a igualdad, por el identificador. "
           "Se saca el primero y se le envía. "
           "Su instante aumenta en su periodo, y vuelve a la cola. "
           "Así la cola solo tiene un elemento por usuario, aunque ka sea enorme.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("En doscientos, el nueve mil. En trescientos, el mil doscientos treinta y cuatro. "
           "En cuatrocientos, otra vez el nueve mil. "
           "En seiscientos coinciden los dos: va primero el mil doscientos treinta y cuatro, que tiene el identificador menor. "
           "Y después el nueve mil.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, el struct Envio compara por instante y luego por identificador. "
           "Cada usuario entra con su primer envío en el instante de su periodo. "
           "En cada vuelta se saca la cima y se escribe su identificador. "
           "Se le suma el periodo y vuelve a la cola.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Se define el operador mayor porque la cola es de mínimos. "
           "El primer envío es en el instante igual al periodo. "
           "Los instantes van en long long. "
           "Y el coste es ka por logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de mínimos con el próximo envío de cada usuario; se saca, se envía, se suma el periodo y vuelve.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-2", "../02-2_unidad_curiosa_de_monitorizacion.mp4", "02-2")
