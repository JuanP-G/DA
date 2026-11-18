"""Vídeo EJ 03-3 · Multitarea (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo

CPP = "../../3-Colas de prioridad variable (Heapsort)/EJ_03-3/EJ_03-3.cpp"
TEMA = "Tema 3 · Colas de prioridad variable"
T = 10
# caso 3: únicas (1,5) y (8,20); periódica (6,7) cada 10
TAREAS = [("A", 1, 5, 0), ("B", 8, 20, 0), ("C", 6, 7, 10)]
COLS = {"A": C["blue"], "B": NARANJA, "C": C["green"], "D": C["purple"], "E": C["red"]}
X0, X1, A_, B_ = 120, 1180, 0, 22


def X(v):
    return X0 + (v - A_) * (X1 - X0) / (B_ - A_)


def simula(tareas, T):
    pq = Monticulo(lambda a, b: a < b)
    per = {}
    for n, a, b, p in tareas:
        pq.push(n, (a, b))
        per[n] = p
    t, pasos = 0, []
    while not pq.empty() and pq.top()[1][0] < T:
        n, (a, b) = pq.top()
        antes = sorted(pq.copia(), key=lambda e: e[1])
        if a < t:
            pasos.append((n, a, b, "choque", t, antes, antes))
            return pasos, True
        t_ant = t
        t = b
        if per[n]:
            pq.update(n, (a + per[n], b + per[n]))
            acc = "update"
        else:
            pq.pop()
            acc = "pop"
        pasos.append((n, a, b, acc, t_ant, antes, sorted(pq.copia(), key=lambda e: e[1])))
    pasos.append((None, None, None, "fin", t, sorted(pq.copia(), key=lambda e: e[1]), None))
    return pasos, False


PASOS, CHOQUE = simula(TAREAS, T)
PASOS1, CHOQUE1 = simula([("D", 2, 5, 0), ("E", 4, 6, 0)], T)


def eje(f, y=560, u=1.0):
    if u <= 0:
        return
    f.d.line((X0, y, X1, y), fill=mix(C["bot"], C["muted"], u), width=2)
    for v in range(A_, B_ + 1, 2):
        f.d.line((X(v), y - 5, X(v), y + 5), fill=mix(C["bot"], C["muted"], u), width=2)
        f.d.text((X(v), y + 22), str(v), font=font(16, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")
    x = X(T)
    f.d.line((x, 120, x, y), fill=mix(C["bot"], C["red"], u), width=3)
    f.d.text((x + 8, 130), f"T = {T}", font=font(20, True), fill=mix(C["bot"], C["red"], u), anchor="la")


def barra(f, n, a, b, y, u=1.0, gris=False, borde=None):
    if u <= 0:
        return
    c = C["dim"] if gris else COLS[n]
    x0, x1 = X(a), lerp(X(a), X(b), u)
    if x1 - x0 < 8:
        return
    f.d.rounded_rectangle((x0 + 2, y - 22, x1 - 2, y + 22), 9, fill=mix(C["panel"], c, 0.45), outline=borde or c, width=5 if borde else 3)
    f.d.text(((x0 + x1) / 2, y), f"{n} [{a},{b})" if x1 - x0 > 100 else n, font=font(17, True), fill=C["text"], anchor="mm")


def cola(f, x, y, elems, titulo="cola de mínimos (ini, fin)"):
    texto(f, (x, y - 34), titulo, 18, "muted", 1)
    for k, (n, (a, b)) in enumerate(elems):
        caja(f, x + 70 + k * 150, y + 6, f"{n} ({a},{b})", c="gold" if k == 0 else COLS[n], w=136, h=44, tam=19, borde=5 if k == 0 else 2)


def e_portada(f):
    def dib(f):
        for k, (x, w, c) in enumerate([(780, 120, C["blue"]), (920, 60, C["green"]), (1000, 60, C["green"]), (1080, 60, C["green"])]):
            u = f.p(0.3 + 0.15 * k, 0.5)
            f.d.rounded_rectangle((x, 320, x + w, 360), 8, fill=mix(C["bot"], mix(C["panel"], c, 0.45), u), outline=mix(C["bot"], c, u), width=3)
    portada(f, "EJ 03-3", "Multitarea", TEMA, dib)


def e_problema(f):
    eje(f, u=aparece(f, f.c(0)))
    barra(f, "A", 1, 5, 220, f.lin(f.c(0), 0.8))
    barra(f, "B", 8, 20, 300, f.lin(f.c(0) + 0.3, 0.8))
    if f.t >= f.c(1):
        for k in range(3):
            barra(f, "C", 6 + 10 * k, 7 + 10 * k, 380, f.lin(f.c(1) + 0.4 * k, 0.5))
        texto(f, (X(6), 430), "C se repite cada 10", 20, "green", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 660), "¿se solapan dos tareas dentro de [0, T)?  →  SI / NO", 26, "gold", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 80), "barrido por orden de comienzo", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (640, 170), "en la cola: la PRÓXIMA aparición de cada tarea", 26, "text", u, anchor="mm")
        cola(f, 280, 270, sorted([(n, (a, b)) for n, a, b, p in TAREAS], key=lambda e: e[1]))
    if f.t >= f.c(2):
        etiqueta(f, (640, 420), "si empieza antes de que acabe la anterior: choque", 26, "red", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 500), "periódica: update a su siguiente aparición   ·   única: pop", 24, "green", aparece(f, f.c(3)))


def e_traza(f, pasos=None, t0=None, t1=None):
    pasos = pasos or PASOS
    t0 = f.c(0) if t0 is None else t0
    t1 = f.T - 1.5 if t1 is None else t1
    eje(f)
    k, fr = paso_idx(f, t0, t1, len(pasos))
    k = max(0, min(k, len(pasos) - 1))
    hechas = pasos[:k + (1 if fr > 0.5 else 0)]
    for q, (n, a, b, acc, tant, antes, despues) in enumerate(hechas):
        if n is None:
            continue
        barra(f, n, a, b, 420, borde=C["red"] if acc == "choque" else None)
    n, a, b, acc, tant, antes, despues = pasos[k]
    cola(f, 150, 170, despues if (fr > 0.5 and despues is not None) else antes)
    tact = (b if fr > 0.5 and acc in ("update", "pop") else tant)
    x = X(tact)
    f.d.line((x, 360, x, 470), fill=C["gold"], width=3)
    texto(f, (x, 350), f"tiempoActual = {tact}", 18, "gold", 1, anchor="mm")
    if acc == "fin":
        etiqueta(f, (640, 660), f"la cima empieza en ≥ T: se para  →  NO", 26, "green", 1)
    elif acc == "choque":
        etiqueta(f, (640, 660), f"{n} empieza en {a} < tiempoActual = {tant}  →  SI", 26, "red", 1)
    else:
        s = f"{n} [{a},{b}): {a} ≥ {tant} ✓   " + ("update → siguiente aparición" if acc == "update" else "pop (es única)")
        etiqueta(f, (640, 660), s, 24, "text", 1)


def e_traza3(f):
    e_traza(f)


def e_choque(f):
    e_traza(f, PASOS1, f.c(0), f.c(2))


A_L = find_line(CPP, "int tiempoActual = 0;")
B_L = find_line(CPP, "cout << (hayConflictos ? \"SI\" : \"NO\")")
CODE = [(n, t) for n, t in codigo(CPP, A_L, B_L, maxc=96) if not t.strip().startswith("//")]
L_W = find_line(CPP, "while (!hayConflictos && !cola.empty()")
L_IF = find_line(CPP, "if (ini < tiempoActual) hayConflictos = true;")
L_UP = find_line(CPP, "cola.update(elem, { ini + periodo[elem], fin + periodo[elem] });")
L_PO = find_line(CPP, "cola.pop();", L_UP)


def e_codigo(f):
    marcas = [(f.c(0), {L_W}), (f.c(1), {L_IF}), (f.c(2), {L_UP - 1, L_UP}), (f.c(3), {L_PO - 1, L_PO}), (f.c(4), {B_L})]
    hl = set()
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(20, 90, 1240, 520, CODE, hl=hl, title="barrido con IndexPQ", size=19)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("índices: 0..N−1 las únicas, N..N+M−1 las periódicas; periodo[i] = 0 si es única", "text"),
             ("la prioridad es el par (ini, fin): pair ya se compara así", "text"),
             ("las periódicas no acaban nunca: se para cuando la cima empieza en ≥ T", "text"),
             ("cada aparición antes de T cuesta O(log(N + M))", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 24, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Multitarea", [
        "IndexPQ de mínimos con la próxima aparición de cada tarea",
        "si empieza antes de tiempoActual: hay conflicto",
        "periódica: update a la siguiente; única: pop",
        "se para cuando la cima empieza en ≥ T",
    ])


ESC = [
    Escena("Multitarea. Saber si dos tareas se solapan antes de un instante te.", e_portada, titulo="Portada", extra=1.0),
    Escena("Hay tareas únicas, que ocupan un intervalo de tiempo. "
           "Y tareas periódicas, que se repiten cada pe minutos: aquí, la ce cada diez. "
           "Hay que decir si dos tareas se solapan dentro del intervalo de cero a te.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Hacemos un barrido por orden de comienzo. "
           "En una cola de prioridad de mínimos guardamos la próxima aparición de cada tarea. "
           "Llevamos el fin de la última procesada: si la siguiente empieza antes, hay choque. "
           "Si no, una periódica pasa a su siguiente aparición con update, y una única se saca con pop.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("En el ejemplo: A, de uno a cinco, es única, así que pop. "
           "Ce empieza en seis, después de cinco: bien, y update a dieciséis. "
           "Be empieza en ocho, después de siete: bien, y pop. "
           "Ahora la cima es ce en dieciséis, que ya pasa de te: paramos. No hay conflicto.",
           e_traza3, titulo="El ejemplo", extra=2.0),
    Escena("En cambio, con una tarea de dos a cinco y otra de cuatro a seis: "
           "la segunda empieza en cuatro, antes de que acabe la primera, en cinco. Hay conflicto: sí.",
           e_choque, titulo="Un choque", extra=1.5),
    Escena("En el código, el bucle sigue mientras no haya conflicto, la cola no esté vacía y la cima empiece antes de te. "
           "Si empieza antes de tiempo actual, hay conflicto. "
           "Si es periódica, update con el inicio y el fin más el periodo. "
           "Si es única, pop. "
           "Al final se escribe sí o no.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("Las únicas tienen los índices del cero al ene menos uno, y las periódicas, los siguientes. "
           "La prioridad es el par inicio, fin. "
           "Como las periódicas nunca acaban, hay que parar al llegar a te. "
           "Y cada aparición cuesta un logaritmo.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una IndexPQ con la próxima aparición de cada tarea; las periódicas avanzan con update, las únicas salen con pop, y se para al llegar a te.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/03-3", "../03-3_multitarea.mp4", "03-3")
