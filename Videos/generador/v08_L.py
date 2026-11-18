"""Vídeo EJ 08-L · Planificación de conferencias (animado)."""
import heapq
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview

CPP = "../../8-Algoritmos voraces/EJ_08-L/EJ_08-L.cpp"
TEMA = "Tema 8 · Algoritmos voraces"
CONF = [("a", 0, 4), ("b", 1, 3), ("c", 3, 7), ("d", 4, 6), ("e", 5, 9)]      # orden de entrada
ENTRADA = [CONF[k] for k in (2, 0, 4, 1, 3)]                                   # como se leen: c a e b d
COLS = {"a": C["blue"], "b": NARANJA, "c": C["purple"], "d": C["green"], "e": C["red"]}
X0, X1, TA, TB = 200, 1180, 0, 10


def X(t):
    return X0 + (t - TA) * (X1 - X0) / (TB - TA)


def simula():
    pq, sala, n, pasos = [], {}, 0, []
    for nm, a, b in sorted(CONF, key=lambda c: c[1]):
        cola_antes = sorted(pq)
        if pq and pq[0][0] <= a:
            libre, s = heapq.heappop(pq)
            sala[nm] = s
            tipo = "reusa"
        else:
            n += 1
            sala[nm] = n
            tipo = "nueva"
        heapq.heappush(pq, (b, sala[nm]))
        pasos.append((nm, a, b, tipo, sala[nm], cola_antes, sorted(pq)))
    return pasos, sala, n


PASOS, SALA, R = simula()
YL = {1: 200, 2: 290, 3: 380}


def charla(f, nm, a, b, y, u=1.0, h=50, c=None):
    if u <= 0:
        return
    c = c or COLS[nm]
    x0, x1 = X(a), lerp(X(a), X(b), u)
    if x1 - x0 < 8:
        return
    f.d.rounded_rectangle((x0 + 2, y - h / 2, x1 - 2, y + h / 2), 10, fill=mix(C["panel"], c, 0.45), outline=c, width=3)
    if u >= 1:
        f.d.text(((x0 + x1) / 2, y), nm, font=font(22, True), fill=C["text"], anchor="mm")


def eje(f, y=470, u=1.0):
    if u <= 0:
        return
    f.d.line((X0, y, X1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    for t in range(TA, TB + 1):
        f.d.line((X(t), y - 5, X(t), y + 5), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((X(t), y + 20), str(t), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def carriles(f, n, u=1.0):
    for s in range(1, n + 1):
        y = YL[s]
        f.d.rounded_rectangle((X0 - 10, y - 34, X1 + 10, y + 34), 12, outline=mix(C["bot"], C["border"], u), width=2)
        texto(f, (X0 - 24, y), f"sala {s}", 20, "muted", u, anchor="rm")


def cola(f, x, y, elems, u=1.0, titulo=True):
    if titulo:
        texto(f, (x, y - 40), "cola de mínimos (libre, sala)", 18, "muted", u)
    if not elems:
        texto(f, (x, y), "vacía", 20, "dim", u)
    for k, (t, s) in enumerate(elems):
        caja(f, x + 60 + k * 120, y + 10, f"({t}, {s})", c="gold" if k == 0 else "blue", u=u, w=104, h=44, tam=20, borde=5 if k == 0 else 2)


def e_portada(f):
    def dib(f):
        for k, (nm, a, b) in enumerate(CONF[:3]):
            u = f.p(0.3 + 0.2 * k, 0.6)
            y = 280 + 60 * k
            x0 = 760 + a * 40
            f.d.rounded_rectangle((x0, y, x0 + (b - a) * 40, y + 44), 8, fill=mix(C["bot"], mix(C["panel"], COLS[nm], 0.45), u), outline=mix(C["bot"], COLS[nm], u), width=3)
    portada(f, "EJ 08-L", "Planificación de conferencias", TEMA, dib)


def e_problema(f):
    eje(f, u=aparece(f, f.c(0)))
    for k, (nm, a, b) in enumerate(CONF):
        charla(f, nm, a, b, 110 + 70 * k, f.lin(f.c(0) + 0.3 * k, 0.8))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        x = X(3)
        f.d.line((x, 90, x, 450), fill=mix(C["bot"], C["green"], u), width=3)
        texto(f, (x + 10, 530), "b acaba en 3 y c empieza en 3: no se solapan", 22, "green", u)
    if f.t >= f.c(2):
        texto(f, (640, 620), "mínimo de salas  +  la sala de cada una (en el orden de la entrada)", 24, "gold", aparece(f, f.c(2)), anchor="mm")


def e_voraz(f):
    eje(f)
    k, fr = paso_idx(f, f.c(1), f.c(5), len(PASOS))
    n_salas = max([p[4] for p in PASOS[:max(0, min(k + 1, len(PASOS)))]] + [0])
    carriles(f, n_salas)
    for q, (nm, a, b, tipo, s, antes, despues) in enumerate(PASOS):
        if q < k or (q == k and f.t >= f.c(1)):
            u = 1.0 if q < k else min(1, fr * 2)
            p = mueve((X((a + b) / 2), 110), (X((a + b) / 2), YL[s]), u)
            charla(f, nm, a, b, p[1])
    texto(f, (640, 70), "por hora de comienzo", 24, "muted", aparece(f, f.c(0)), anchor="mm")
    if 0 <= k < len(PASOS):
        nm, a, b, tipo, s, antes, despues = PASOS[k]
        x = X(a)
        f.d.line((x, 150, x, 460), fill=C["gold"], width=2)
        cola(f, 160, 590, antes if fr < 0.5 else despues)
        s_txt = f"{nm} empieza en {a}: " + (f"la sala {s} está libre desde {antes[0][0]}" if tipo == "reusa" else
                                             ("no hay salas" if not antes else f"la primera libre es a las {antes[0][0]} > {a}: sala nueva"))
        texto(f, (640, 660), s_txt, 24, "green" if tipo == "reusa" else NARANJA, 1, anchor="mm")
    elif k >= len(PASOS):
        cola(f, 160, 590, PASOS[-1][6])
        texto(f, (640, 660), f"R = {R} salas", 32, "green", aparece(f, f.c(5)), anchor="mm")


def e_porque(f):
    eje(f)
    carriles(f, R)
    for nm, a, b, tipo, s, _, _ in PASOS:
        charla(f, nm, a, b, YL[s])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        x = X(5)
        f.d.line((x, 150, x, 460), fill=mix(C["bot"], C["red"], u), width=4)
        for s in (1, 2, 3):
            f.d.ellipse((x - 9, YL[s] - 9, x + 9, YL[s] + 9), fill=mix(C["bot"], C["red"], u))
        texto(f, (x + 14, 140), "en t = 5 hay 3 a la vez", 22, "red", u)
    if f.t >= f.c(2):
        texto(f, (640, 590), "se abre la sala k solo si hay k conferencias a la vez", 26, "gold", aparece(f, f.c(2)), anchor="mm")
        texto(f, (640, 640), "ninguna planificación puede usar menos", 24, "muted", aparece(f, f.c(2) + 0.4), anchor="mm")


def e_orden(f):
    texto(f, (640, 80), "la salida va en el orden de la ENTRADA", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(0))
    for k, (nm, a, b) in enumerate(ENTRADA):
        caja(f, 300 + k * 170, 200, nm, c=COLS[nm], u=u, w=90, h=60, tam=28)
        texto(f, (300 + k * 170, 250), str(k), 18, "muted", u, anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (100, 330), "orden", 22, "muted", u)
        orden = sorted(range(5), key=lambda k: ENTRADA[k][1])
        for q, k in enumerate(orden):
            p = mueve((300 + k * 170, 360), (300 + q * 170, 360), f.lin(f.c(1) + 0.4, 1.2))
            caja(f, p[0], p[1], str(k), c="muted", w=70, h=50, tam=24)
        texto(f, (640, 430), "se ordenan los ÍNDICES por comienzo", 24, "text", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (100, 520), "sala", 22, "muted", u)
        for k, (nm, a, b) in enumerate(ENTRADA):
            caja(f, 300 + k * 170, 530, SALA[nm], c="green", u=u, w=70, h=50, tam=24)
        texto(f, (640, 620), "salida:  " + " ".join(str(SALA[nm]) for nm, _, _ in ENTRADA), 28, "green", u, mono=True, anchor="mm")


A = find_line(CPP, "vector<int> orden(N);")
B = find_line(CPP, "for (int i = 0; i < N; ++i) cout << sala[i]")
CODE = codigo(CPP, A, B, maxc=80)
L_IF = find_line(CPP, "if (!salas.empty() && salas.top().first <= ini[c]) {")
L_NU = find_line(CPP, "sala[c] = ++numSalas;")
L_PU = find_line(CPP, "salas.push({fin[c], sala[c]});")
L_SO = find_line(CPP, "sort(orden.begin(), orden.end()")


def e_codigo(f):
    hl = {L_SO}
    k, fr = paso_idx(f, f.c(1), f.T - 2.5, len(PASOS))
    if 0 <= k < len(PASOS):
        tipo = PASOS[k][3]
        hl = ({L_IF, L_IF + 1, L_IF + 2} if tipo == "reusa" else {L_NU - 1, L_NU}) if fr < 0.6 else {L_PU}
    elif k >= len(PASOS):
        hl = {B - 1, B}
    f.code(10, 90, 800, 520, CODE, hl=hl, title="salas", size=16)
    x0 = 850
    if 0 <= k < len(PASOS):
        nm, a, b, tipo, s, antes, despues = PASOS[k]
        texto(f, (x0, 130), f"conferencia {nm} = [{a}, {b})", 22, "text", 1, mono=True)
        texto(f, (x0, 175), f"→ sala {s}" + (" (reutilizada)" if tipo == "reusa" else " (nueva)"), 22, "green" if tipo == "reusa" else NARANJA, 1)
        cola_l = antes if fr < 0.6 else despues
        texto(f, (x0, 250), "cola:", 20, "muted", 1)
        for q, (t, ss) in enumerate(cola_l):
            caja(f, x0 + 60, 300 + q * 56, f"({t}, {ss})", c="gold" if q == 0 else "blue", w=104, h=44, tam=20, borde=5 if q == 0 else 2)
    elif k >= len(PASOS):
        texto(f, (x0, 160), f"numSalas = {R}", 26, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("<= al comparar: acabar a las 5 y empezar a las 5 no es solaparse", "text"),
             ("vale cualquier asignación válida (el juez acepta 1 2 3 y 1 3 2)", "text"),
             ("N ≤ 250.000:  O(N log N), por la ordenación y la cola", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 180 + 110 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Planificación de conferencias", [
        "recorrer las conferencias por hora de comienzo",
        "reutilizar la sala que queda libre antes (cola de mínimos)",
        "si ninguna está libre, sala nueva",
        "k salas ⇔ k conferencias a la vez · O(N log N)",
    ])


ESC = [
    Escena("Planificación de conferencias. Cuántas salas hacen falta como mínimo.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos conferencias, cada una con su hora de comienzo y de fin. "
           "Dos que se solapan no pueden ir en la misma sala; pero si una empieza justo cuando acaba otra, no se solapan. "
           "Hay que decir el mínimo de salas y en qué sala va cada conferencia.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Recorremos las conferencias por orden de comienzo. "
           "La primera abre la sala uno. "
           "Para cada nueva, miramos la sala que queda libre antes, que es la cima de una cola de prioridad de mínimos. "
           "Si ya está libre cuando empieza la conferencia, se reutiliza. Si no, ninguna lo está, y se abre una sala nueva. "
           "Al final, tres salas.",
           e_voraz, titulo="La voraz", extra=2.5),
    Escena("¿Por qué tres es el mínimo? "
           "Mira el instante cinco: hay tres conferencias a la vez. "
           "La voraz solo abre la sala ka cuando las otras ka menos uno están ocupadas, es decir, cuando hay ka conferencias a la vez. Nadie puede hacerlo con menos.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("La salida tiene que ir en el orden de la entrada. "
           "Por eso no se ordenan las conferencias, sino un vector de índices, por hora de comienzo. "
           "Así cada sala se guarda en la posición de su conferencia y se escriben en el orden original.",
           e_orden, titulo="El orden de salida", extra=1.5),
    Escena("En el código, se ordenan los índices por comienzo. "
           "Para cada conferencia: si la cola no está vacía y su cima ya está libre, se reutiliza esa sala y se saca; si no, sala nueva. "
           "En los dos casos se mete en la cola el fin de la conferencia con su sala.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Se compara con menor o igual, porque acabar y empezar a la misma hora no es solaparse. "
           "Hay muchas asignaciones correctas, y el juez acepta cualquiera. "
           "El coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: por hora de comienzo, se reutiliza la sala que queda libre antes o se abre una nueva. "
           "Se abren tantas salas como conferencias coinciden a la vez como mucho, que es el mínimo posible.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/08-L", "../08-L_planificacion_de_conferencias.mp4", "08-L")
