"""Vídeo de teoría · Tema 3 · Colas de prioridad variable (IndexPQ), animado."""
from vidlib import C, W, H, font
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo, arbol, arbol_anim

TEMA = "Tema 3 · Colas de prioridad variable"
PRIO = {0: 7, 1: 3, 2: 9, 3: 5, 4: 8}
COLS = {0: C["blue"], 1: NARANJA, 2: C["purple"], 3: C["green"], 4: C["red"]}


def etq(e, p):
    return f"e{e}\n{p}"


def construye():
    m = Monticulo(lambda a, b: a < b)
    for e in range(5):
        m.push(e, PRIO[e])
    return m


def tablas(f, arr, y=500, marca=None, u=1.0):
    """array (pares desde la posición 1) y posiciones[e]."""
    texto(f, (60, y - 10), "array", 20, "muted", u)
    for i, (e, p) in enumerate(arr):
        x = 250 + i * 110
        caja(f, x, y, f"e{e}:{p}", c=COLS[e], u=u, w=96, h=48, tam=19, borde=4 if marca and e in marca else 2)
        texto(f, (x, y + 38), str(i + 1), 15, "muted", u, anchor="mm")
    texto(f, (60, y + 80), "posiciones", 20, "muted", u)
    pos = {e: i + 1 for i, (e, p) in enumerate(arr)}
    for e in range(5):
        x = 250 + e * 110
        caja(f, x, y + 90, pos.get(e, 0), c=COLS[e], u=u, w=70, h=44, tam=20, borde=4 if marca and e in marca else 2)
        texto(f, (x, y + 126), f"e{e}", 15, "muted", u, anchor="mm")


def e_portada(f):
    def dib(f):
        m = construye()
        arbol(f, m.copia()[:3], 960, 270, 220, etq, u=f.p(0.3, 0.8), r=30, colores=COLS)
    portada(f, "Teoría", "IndexPQ", TEMA, dib)


def e_problema(f):
    texto(f, (640, 70), "a veces la prioridad de algo cambia cuando YA está en la cola", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (640, 160), "votos de Eurovisión (03-2) · distancias de Dijkstra (tema 7)", 24, "text", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        caja(f, 380, 300, "priority_queue", c="red", u=u, w=300, h=60, tam=24)
        texto(f, (380, 360), "no sabe dónde está cada elemento", 22, "red", u, anchor="mm")
        texto(f, (380, 390), "ni puede cambiarlo de sitio", 22, "red", u, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        caja(f, 900, 300, "meter repetidos", c="gold", u=u, w=300, h=60, tam=24)
        texto(f, (900, 360), "funciona, pero la cola crece", 22, "muted", u, anchor="mm")
        texto(f, (900, 390), "y hay que saltarse los viejos", 22, "muted", u, anchor="mm")
    if f.t >= f.c(4):
        etiqueta(f, (640, 520), "IndexPQ: update(elemento, nueva prioridad) en O(log n)", 26, "green", aparece(f, f.c(4)), mono=True)


def e_idea(f):
    m = construye()
    arr = m.copia()
    arbol(f, arr, 640, 120, 600, etq, u=aparece(f, f.c(0)), r=36, colores=COLS)
    if f.t >= f.c(0):
        texto(f, (60, 90), "elementos: 0 … N−1", 24, "gold", aparece(f, f.c(0)))
    if f.t >= f.c(1):
        tablas(f, arr, 460, u=aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (900, 380), "posiciones[e] = dónde está e en el array (0 = no está)", 22, "gold", aparece(f, f.c(2)))


def e_update(f):
    m = construye()
    a = m.copia()
    m.update(4, 2)
    b = m.copia()
    texto(f, (640, 50), "update(e4, 2): su prioridad mejora de 8 a 2", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t < f.c(2):
        arr = [(e, (2 if e == 4 and f.t >= f.c(1) else p)) for e, p in a]
        arbol(f, arr, 640, 120, 600, etq, r=36, colores=COLS, marca={i for i, (e, p) in enumerate(arr) if e == 4})
        tablas(f, arr, 460, marca={4})
        if f.t >= f.c(1):
            etiqueta(f, (950, 380), "posiciones[4] = 5: lo encuentra en O(1)", 22, "text", 1)
    else:
        a2 = [(e, (2 if e == 4 else p)) for e, p in a]
        u = f.lin(f.c(2), 2.0)
        arbol_anim(f, a2, b, u, 640, 120, 600, etq, r=36, colores=COLS, marca_elem=4)
        tablas(f, b if u >= 1 else a2, 460, marca={4, 1})
        etiqueta(f, (950, 380), "flota; cada intercambio actualiza posiciones", 22, "green", 1)
    if f.t >= f.c(3):
        etiqueta(f, (640, 680), "si empeora, se hunde · O(log n)", 22, "text", aparece(f, f.c(3)))


def e_ops(f):
    f.box(60, 100, 1160, 500, "IndexPQ<T, Comparator> pq(N);")
    ops = [("pq.push(e, p)", "meter e (error si ya está)", "O(log n)"),
           ("pq.update(e, p)", "cambiar la prioridad; si no está, lo mete", "O(log n)"),
           ("pq.top()", "Par { elem, prioridad } del primero", "O(1)"),
           ("pq.pop()", "sacar el primero", "O(log n)"),
           ("pq.priority(e)", "prioridad actual de e", "O(1)"),
           ("pq.empty(), pq.size()", "", "O(1)")]
    for k, (o, d, c) in enumerate(ops):
        t0 = f.c(min(k, 3))
        if f.t >= t0:
            u = aparece(f, t0 + 0.2 * (k % 2))
            y = 160 + 70 * k
            texto(f, (100, y), o, 24, "blue", u, mono=True, fondo=C["panel"])
            texto(f, (480, y), d, 22, "text", u, fondo=C["panel"])
            texto(f, (1060, y), c, 22, "gold", u, mono=True, fondo=C["panel"])
    if f.t >= f.c(4):
        etiqueta(f, (640, 650), "update sirve para todo: insertar la primera vez y cambiar después", 22, "green", aparece(f, f.c(4)))


def e_comparador(f):
    texto(f, (640, 70), "El comparador decide quién va antes", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    lineas = [("IndexPQ<int> pq(N);", "mínimos (less por defecto)", "text"),
              ("IndexPQ<int, greater<int>> pq(N);", "máximos (03-1: pilas más cargadas)", "text"),
              ("IndexPQ<pair<int,int>> pq(N);", "(ini, fin): desempata solo (03-3)", "text"),
              ("IndexPQ<Par, Mejor> pq(N);", "un struct con operator(): (puntos, nombre) en 03-2", "gold")]
    for k, (c, d, col) in enumerate(lineas):
        if f.t >= f.c(min(k + 1, 3)):
            u = aparece(f, f.c(min(k + 1, 3)) + 0.3 * max(0, k - 2))
            texto(f, (120, 170 + 110 * k), c, 24, "blue", u, mono=True)
            texto(f, (120, 210 + 110 * k), d, 22, col, u)
    if f.t >= f.c(4):
        etiqueta(f, (640, 650), "antes(a, b) es cierto si a debe salir antes que b", 22, "text", aparece(f, f.c(4)), mono=True)


def e_usos(f):
    items = [("Prioridades que cambian", "03-2 · 03-5 · 03-L: votos, citas, minutos", C["blue"]),
             ("La próxima aparición", "03-3 · tareas periódicas con update", C["green"]),
             ("Como montículo normal", "03-1 (pilas) · 03-4 (mediana, dos montículos)", NARANJA),
             ("Más adelante", "Prim (tema 6) y Dijkstra (tema 7)", C["purple"])]
    texto(f, (640, 50), "Cuándo usarla", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (t, d, c) in enumerate(items):
        if f.t < f.c(k + 1):
            continue
        u = aparece(f, f.c(k + 1))
        x = 40 + (k % 2) * 610
        y = 110 + (k // 2) * 250
        f.d.rounded_rectangle((x, y, x + 590, y + 220), 16, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        f.d.text((x + 24, y + 50), t, font=font(28, True), fill=mix(C["bot"], c, u), anchor="lm")
        f.d.text((x + 24, y + 130), d, font=font(23), fill=mix(C["bot"], C["text"], u), anchor="lm")


def e_cierre(f):
    cierre(f, "IndexPQ", [
        "elementos 0 … N−1 con una prioridad cada uno",
        "array (montículo) + posiciones (dónde está cada uno)",
        "update: flota o se hunde en O(log n)",
        "el comparador decide quién va antes",
    ])


ESC = [
    Escena("Colas de prioridad variable: la IndexPQ, una cola en la que se puede cambiar la prioridad de un elemento.", e_portada, titulo="Portada", extra=1.0),
    Escena("A veces la prioridad de un elemento cambia cuando ya está en la cola. "
           "Pasa con los votos de Eurovisión, y pasará con las distancias de Dijkstra. "
           "La priority queue de la librería no sabe dónde está cada elemento, así que no puede moverlo. "
           "Se puede meter otra copia con la nueva prioridad, pero la cola crece y hay que saltarse las viejas. "
           "La IndexPQ lo resuelve con una operación nueva: update, en tiempo logarítmico.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("En una IndexPQ los elementos son enteros, de cero a ene menos uno, y cada uno tiene su prioridad. "
           "Por dentro hay un montículo guardado en un vector de pares elemento y prioridad, empezando en la posición uno. "
           "Y un segundo vector, posiciones, dice en qué posición del montículo está cada elemento; cero si no está.",
           e_idea, titulo="Cómo es por dentro", extra=1.5),
    Escena("Hagamos update del elemento cuatro, que pasa de ocho a dos. "
           "Gracias a posiciones, sabemos al instante que está en la posición cinco, y cambiamos su prioridad. "
           "Como ha mejorado, flota hacia arriba; en cada intercambio se actualizan también las posiciones. "
           "Si hubiera empeorado, se hundiría. En los dos casos, logaritmo de ene.",
           e_update, titulo="update", extra=2.0),
    Escena("Las operaciones son: push, que mete un elemento nuevo, "
           "update, que cambia su prioridad o lo mete si no estaba, "
           "top, que devuelve el par elemento y prioridad del primero, y pop, que lo saca. "
           "Priority da la prioridad actual de un elemento, y empty y size, lo de siempre. "
           "En la práctica, update sirve para todo.",
           e_ops, titulo="Operaciones", extra=1.5),
    Escena("Como en la priority queue, un comparador decide quién va antes. "
           "Por defecto es less, y la cola es de mínimos. "
           "Con greater, de máximos, como en las pilas de los drones. "
           "Con pares se desempata solo, y con un struct propio se puede ordenar por puntos y nombre, como en Eurovisión. "
           "La regla es: antes de a, b, es cierto si a tiene que salir antes que b.",
           e_comparador, titulo="El comparador", extra=1.5),
    Escena("¿Cuándo usarla? "
           "Cuando las prioridades cambian, como los votos. "
           "Cuando cada elemento tiene una próxima aparición, como las tareas periódicas. "
           "Muchas veces, simplemente como un montículo con nombre para cada elemento. "
           "Y será la pieza clave de Prim y de Dijkstra.",
           e_usos, titulo="Cuándo usarla", extra=1.5),
    Escena("Resumiendo: la IndexPQ guarda un montículo y la posición de cada elemento, y así puede cambiar una prioridad y recolocarla en tiempo logarítmico.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/03-0", "../03-0_indexpq_teoria.mp4", "03-0")
