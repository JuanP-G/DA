"""Vídeo EJ 02-L · Cinemáticas digitales (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-L/EJ_02-L.cpp"
TEMA = "Tema 2 · Colas de prioridad"
S = 2
ESCENAS = [(0, 50), (0, 60), (10, 5), (25, 5)]        # caso 3: (minuto de envío, duración)
COLS = {0: C["blue"], 1: NARANJA}
X0, X1, TA, TB = 160, 1180, 0, 70


def X(t):
    return X0 + (t - TA) * (X1 - X0) / (TB - TA)


def simula():
    pq = Monticulo(lambda a, b: a < b)        # (libre, estación)
    for e in range(S):
        pq.push(e, (0, e))
    pasos, info, mx = [], [], 0
    for k, (m, d) in enumerate(ESCENAS):
        ant = pq.copia()
        e, (lib, _) = pq.top()
        ini = max(lib, m)
        esp = ini - m
        mx = max(mx, esp)
        pq.update(e, (ini + d, e))
        info.append((k, m, d, e, ini, esp, mx))
        pasos.append((ant, pq.copia(), f"escena {k}: llega en {m}, estación {e} libre en {lib} → espera {esp}", "red" if esp else "text"))
    return pasos, info, mx


PASOS, INFO, MAXE = simula()


def etq(e, p):
    return f"est. {e}\n{p[0]}"


def eje(f, y=600, u=1.0):
    f.d.line((X0, y, X1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    for t in range(TA, TB + 1, 10):
        f.d.line((X(t), y - 5, X(t), y + 5), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((X(t), y + 22), str(t), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def bloque(f, k, a, b, y, c, u=1.0, h=40):
    if u <= 0:
        return
    x0, x1 = X(a), lerp(X(a), X(b), u)
    if x1 - x0 < 6:
        return
    f.d.rounded_rectangle((x0 + 1, y - h / 2, x1 - 1, y + h / 2), 8, fill=mix(C["panel"], c, 0.45), outline=c, width=3)
    f.d.text(((x0 + x1) / 2, y), f"escena {k}" if x1 - x0 > 90 else str(k), font=font(16, True), fill=C["text"], anchor="mm")


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.6)
        f.d.rounded_rectangle((830, 270, 1090, 410), 12, fill=mix(C["bot"], (20, 24, 34), u), outline=mix(C["bot"], C["blue"], u), width=4)
        f.d.polygon([(940, 300), (940, 380), (1000, 340)], fill=mix(C["bot"], C["gold"], f.p(0.6, 0.5)))
    portada(f, "EJ 02-L", "Cinemáticas digitales", TEMA, dib)


def e_problema(f):
    eje(f, u=aparece(f, f.c(0)))
    for e in range(S):
        texto(f, (X0 - 14, 250 + e * 90), f"estación {e}", 20, COLS[e], aparece(f, f.c(0)), anchor="rm")
    for k, (m, d) in enumerate(ESCENAS):
        t0 = f.c(1) + 0.3 * k
        if f.t >= t0:
            u = aparece(f, t0)
            f.d.polygon([(X(m) - 10, 470), (X(m) + 10, 470), (X(m), 488)], fill=mix(C["bot"], C["gold"], u))
            texto(f, (X(m) + (12 if k % 2 else -12), 450 - 22 * (k // 2)), f"esc. {k} ({d}')", 16, "gold", u, anchor="lm" if k % 2 else "rm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 100), "¿cuánto espera, como mucho, una escena antes de empezar?", 26, "gold", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 90), "cola de mínimos con la hora en que queda libre cada estación", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 260), "inicio = max(libre de la cima, minuto de envío)", 26, "text", aparece(f, f.c(1)), mono=True)
    if f.t >= f.c(2):
        etiqueta(f, (640, 340), "espera = inicio − minuto        la estación queda libre en inicio + duración", 22, "green", aparece(f, f.c(2)), mono=True)
    if f.t >= f.c(3):
        etiqueta(f, (640, 440), "las escenas llegan en orden: basta procesarlas según se leen", 24, "muted", aparece(f, f.c(3)))


def lateral(f, k, fr):
    n = k + (1 if fr > 0.4 else 0)
    for q in range(n):
        kk, m, d, e, ini, esp, mx = INFO[q]
        y = 460 + e * 70
        bloque(f, kk, ini, ini + d, y, COLS[e], 0.5 * 0 + 1, h=36)
        if esp:
            f.d.line((X(m), y + 26, X(ini), y + 26), fill=C["red"], width=3)
            f.d.ellipse((X(m) - 5, y + 21, X(m) + 5, y + 31), fill=C["red"])
    for e in range(S):
        texto(f, (X0 - 10, 460 + e * 70), f"est. {e}", 18, COLS[e], 1, anchor="rm")
    mxv = INFO[n - 1][6] if n else 0
    texto(f, (60, 140), f"máximo = {mxv}", 26, "red", 1, mono=True)


def e_traza(f):
    escena_traza(f, PASOS, etq, colores=COLS, lateral=lateral, cx=820, ancho=360, titulo="cola de mínimos: libre más pronto arriba")


A_L = find_line(CPP, "priority_queue<long long, vector<long long>, greater<long long>> cola;")
B_L = find_line(CPP, "cout << maxT")
L_INI = find_line(CPP, "cola.push(0);")
L_TOP = find_line(CPP, "long long libre = cola.top(); cola.pop();")


def e_codigo(f):
    escena_codigo(f, CPP, [(A_L, B_L, {L_INI}, "estaciones"), (A_L, B_L, {L_TOP, L_TOP + 1}, "estaciones"),
                           (A_L, B_L, {L_TOP + 2, L_TOP + 3}, "estaciones"), (A_L, B_L, {B_L}, "estaciones")], size=20)


def e_detalles(f):
    escena_lista(f, [("solo hace falta la hora de cada estación, no cuál es", "text"),
                     ("si una estación está libre antes de que llegue la escena, espera 0", "text"),
                     ("long long: minutos y duraciones grandes", "text"),
                     ("R escenas, cada una O(log S):  O(R log S)", "gold")])


def e_cierre(f):
    cierre(f, "Cinemáticas digitales", [
        "cola de mínimos con la hora libre de cada estación",
        "inicio = max(libre, envío); espera = inicio − envío",
        "la estación vuelve con inicio + duración",
        "se guarda la espera máxima · O(R log S)",
    ])


ESC = [
    Escena("Cinemáticas digitales. Cuánto tiene que esperar, como mucho, una escena para renderizarse.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos ese estaciones de render iguales; aquí, dos. "
           "Las escenas llegan en orden, cada una con su minuto de envío y lo que tarda. "
           "Hay que calcular el tiempo máximo que alguna escena pasa esperando antes de empezar.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Guardamos en una cola de mínimos la hora en que queda libre cada estación. "
           "Cada escena empieza en el máximo entre la hora libre de la cima y su minuto de envío. "
           "Su espera es el inicio menos el envío, y la estación queda libre cuando termine. "
           "Como llegan en orden, basta procesarlas según se leen.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Las dos primeras escenas llegan en cero y ocupan las dos estaciones, hasta cincuenta y sesenta. "
           "La tercera llega en diez, pero la primera libre es en cincuenta: espera cuarenta. "
           "La cuarta llega en veinticinco y empieza en cincuenta y cinco: espera treinta. "
           "El máximo es cuarenta.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, todas las estaciones entran libres en el cero. "
           "Para cada escena se saca la cima. "
           "Se calcula el inicio, se actualiza el máximo de la espera y la estación vuelve con su nueva hora. "
           "Al final se escribe el máximo.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("No hace falta saber qué estación es, solo su hora. "
           "Si alguna está libre antes de que llegue la escena, la espera es cero. "
           "Los tiempos van en long long. "
           "Y el coste es erre por logaritmo de ese.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de mínimos con la hora libre de cada estación; cada escena empieza en el máximo entre esa hora y su envío, y se guarda la espera mayor.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-L", "../02-L_cinematicas_digitales.mp4", "02-L")
