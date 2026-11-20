"""Vídeo EJ Eval-1 · MasterHash (animado)."""
import heapq
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../12-Evaluacion/EJ_Eval-1/EJ_Eval-1.cpp"
TEMA = "Pruebas evaluativas"
ARI = [(2, 4), (3, 4), (4, 5), (5, 6), (6, 7), (7, 6), (1, 7)]
S, P = 1, 5
POS = {2: (250, 220), 3: (250, 440), 4: (470, 330), 5: (690, 330), 6: (910, 220), 7: (910, 440), 1: (690, 540)}


def necesarias():
    inv = {v: [a for a, b in ARI if b == v] for v in POS}
    orden, vis, pila = [], {P}, [P]
    while pila:
        v = pila.pop()
        orden.append(v)
        for w in inv[v]:
            if w not in vis:
                vis.add(w)
                pila.append(w)
    return orden


NEC = necesarias()


def kahn():
    ent = {v: sum(1 for a, b in ARI if b == v and a in NEC) for v in NEC}
    libres = [v for v in NEC if ent[v] == 0]
    heapq.heapify(libres)
    pasos = [(None, dict(ent), sorted(libres))]
    while libres:
        v = heapq.heappop(libres)
        for a, b in ARI:
            if a == v and b in NEC:
                ent[b] -= 1
                if ent[b] == 0:
                    heapq.heappush(libres, b)
        pasos.append((v, dict(ent), sorted(libres)))
    return pasos


KP = kahn()
ORDEN = [p[0] for p in KP[1:]]


def grafo(f, ns=None, es=None, under=None, u=1.0, aristas=ARI, inverso=False):
    if u <= 0:
        return
    ed = [(b, a) for a, b in aristas] if inverso else aristas
    f.dgraph(POS, ed, ns=ns or {}, es=es or {}, r=30, under=under)


def fuego(f, x, y, u=1.0):
    if u <= 0:
        return
    for k, (dx, h, c) in enumerate([(-10, 30, C["red"]), (8, 38, NARANJA), (0, 22, C["gold"])]):
        f.d.polygon([(x + dx - 10, y), (x + dx, y - h * u), (x + dx + 10, y)], fill=c)


def plato(f, x, y, u=1.0):
    if u <= 0:
        return
    f.d.ellipse((x - 40, y - 10, x + 40, y + 14), outline=mix(C["bot"], C["gold"], u), width=4)


def base_ns(extra=None):
    ns = {v: ("node", "node_t", None) for v in POS}
    ns[S] = ((90, 50, 40), "text", "red")
    ns[P] = ("gold", "node_t", None)
    if extra:
        ns.update(extra)
    return ns


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.6)
        f.d.rounded_rectangle((830, 300, 1090, 400), 30, fill=mix(C["bot"], (90, 96, 110), u))
        f.d.rectangle((800, 300, 1120, 316), fill=mix(C["bot"], (120, 126, 140), u))
        fuego(f, 960, 440, f.p(0.6, 0.6))
    portada(f, "Eval-1", "MasterHash", TEMA, dib)


def e_problema(f):
    u = aparece(f, f.c(0))
    grafo(f, ns=base_ns() if f.t >= f.c(1) else None, u=u)
    if f.t >= f.c(0):
        texto(f, (640, 80), "X → Y:  la elaboración X hace falta para la Y", 24, "text", u, anchor="mm")
    if f.t >= f.c(1):
        fuego(f, POS[S][0] + 44, POS[S][1] + 10, aparece(f, f.c(1)))
        texto(f, (POS[S][0], POS[S][1] + 56), "S: quemada", 20, "red", aparece(f, f.c(1)), anchor="mm")
        plato(f, POS[P][0], POS[P][1] + 46, aparece(f, f.c(1)))
        texto(f, (POS[P][0], POS[P][1] - 52), "P: el plato", 20, "gold", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 650), "¿se puede hacer P sin S y sin ciclos?  →  NO, o SI y un orden", 24, "gold", aparece(f, f.c(2)))


def e_paso1(f):
    inv = f.t >= f.c(1)
    k, fr = paso_idx(f, f.c(2), f.c(3), len(NEC))
    marc = NEC[:max(0, min(k + 1, len(NEC)))]
    ns = base_ns({v: ("green", "node_t", None) for v in marc if v != P})
    es = {}
    for a, b in ARI:
        if b in marc and a in marc:
            es[(b, a) if inv else (a, b)] = ("green", 4)
    grafo(f, ns=ns, es=es, inverso=inv)
    texto(f, (640, 70), "1 · ¿qué hace falta para P?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if inv:
        texto(f, (640, 120), "en el grafo INVERSO: lo alcanzable desde P", 24, "text", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 650), "necesarias: 5, 4, 2, 3   ·   el ciclo 6 ↔ 7 no importa", 24, "green", aparece(f, f.c(3)))


def e_paso2(f):
    ns = base_ns({v: ("green", "node_t", None) for v in NEC if v != P})
    grafo(f, ns=ns)
    texto(f, (640, 70), "2 · ¿necesita la quemada?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    fuego(f, POS[S][0] + 44, POS[S][1] + 10)
    if f.t >= f.c(1):
        tick(f, POS[S][0] + 60, POS[S][1] - 40, True, aparece(f, f.c(1)))
        etiqueta(f, (640, 650), "S = 1 no está entre las necesarias: seguimos", 24, "green", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 600), "si estuviera (o S = P):  NO", 24, "red", aparece(f, f.c(2)))


def e_paso3(f):
    k, fr = paso_idx(f, f.c(2), f.c(4), len(KP) - 1)
    k = max(-1, k)
    hechos = ORDEN[:max(0, min(k + (1 if fr > 0.5 else 0), len(ORDEN)))]
    st = KP[min(len(KP) - 1, max(0, k + (1 if fr > 0.5 else 0)))] if f.t >= f.c(2) else KP[0]
    ns = base_ns({v: ("green", "node_t", None) for v in NEC if v != P})
    for v in hechos:
        ns[v] = ("blue", "node_t", "gold")
    grid = {(a, b): ("dim", 2) for a, b in ARI if not (a in NEC and b in NEC)}
    under = {v: str(st[1][v]) for v in NEC} if f.t >= f.c(1) else None
    grafo(f, ns=ns, es=grid, under=under)
    texto(f, (640, 70), "3 · orden topológico de las necesarias (Kahn)", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        texto(f, (640, 115), "nº junto a cada vértice = aristas de entrada pendientes", 20, "gold", aparece(f, f.c(1)), anchor="mm")
        texto(f, (60, 590), "libres (mínimo primero):", 20, "muted", 1)
        for q, v in enumerate(st[2]):
            caja(f, 380 + q * 70, 600, v, c="gold", w=56, h=44, tam=22)
        texto(f, (60, 660), "orden:", 20, "muted", 1)
        for q, v in enumerate(hechos):
            caja(f, 190 + q * 70, 668, v, c="blue", w=56, h=44, tam=22)
    if f.t >= f.c(4):
        etiqueta(f, (900, 668), "SI 2 3 4 5", 28, "green", aparece(f, f.c(4)), mono=True)


def e_ciclo(f):
    pos = {2: (420, 300), 3: (640, 300), 4: (860, 300)}
    ar = [(2, 3), (3, 2), (3, 4)]
    ns = {2: ("green", "node_t", None), 3: ("green", "node_t", None), 4: ("gold", "node_t", None)}
    under = {2: "1", 3: "1", 4: "1"} if f.t >= f.c(1) else None
    f.dgraph(pos, ar, ns=ns, es={(2, 3): ("red", 4), (3, 2): ("red", 4)} if f.t >= f.c(1) else {}, r=30, under=under)
    texto(f, (640, 120), "¿y si las necesarias tienen un ciclo?", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 470), "nadie tiene 0 entradas: Kahn no saca a todos", 24, "red", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 540), "orden.size() < total  →  NO", 26, "red", aparece(f, f.c(2)), mono=True)


A_L = find_line(CPP, "Digrafo inv = g.inverso();")
B_L = find_line(CPP, "cout << '\\n';", A_L + 30)
CODE = codigo(CPP, A_L, B_L, maxc=90)
CODE = [(n, s) for n, s in CODE if not s.strip().startswith("//")]
L1 = (A_L, find_line(CPP, "if (!necesaria[w]) { necesaria[w] = true;"))
L2 = find_line(CPP, "if (necesaria[S]) { cout << \"NO\\n\"; return; }")
L3 = (find_line(CPP, "vector<int> entrada(N, 0);"), find_line(CPP, "if (necesaria[w] && --entrada[w] == 0) libres.push(w);"))
L4 = find_line(CPP, "if ((int)orden.size() < total)")


SECC = [("1 · necesarias (inverso desde P)", L1[0], L1[1] + 2),
        ("2 · ¿necesita S?", L2, L2),
        ("3 · Kahn con las necesarias", L3[0], L3[1] + 1),
        ("4 · ¿ciclo?  y salida", L4, B_L)]


def e_codigo(f):
    k = 0
    for q in range(4):
        if f.t >= f.c(q):
            k = q
    tit, a, b = SECC[k]
    lines = [(n, t) for n, t in codigo(CPP, a, b, maxc=90) if not t.strip().startswith("//")]
    hl = {L2} if k == 1 else ({L4} if k == 3 else set())
    f.code(40, 90, 1200, 540, lines, hl=hl, title=tit, size=19)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("S == P: el plato es lo quemado → NO (P siempre es necesaria)", "text"),
             ("P sale la última: todas las necesarias llegan a P", "text"),
             ("cola de mínimos en Kahn: sale siempre el menor disponible", "text"),
             ("O((N + A) log N): recorrido, conteo y Kahn con cola de prioridad", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "MasterHash", [
        "necesarias: alcanzables desde P en el grafo inverso",
        "si S está entre ellas: NO",
        "Kahn solo con las necesarias (cola de mínimos)",
        "si no salen todas, hay ciclo: NO",
    ])


ESC = [
    Escena("MasterHash. Saber si un plato se puede cocinar, y en qué orden.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos elaboraciones y anotaciones del tipo equis hace falta para y griega: un grafo dirigido. "
           "La elaboración ese se ha quemado, y pe es el plato que queremos. "
           "El plato se puede hacer si no necesita lo quemado y lo que necesita no tiene ciclos. Si se puede, hay que dar un orden.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Paso uno: qué hace falta para el plato. Son los vértices desde los que se llega a pe. "
           "Si damos la vuelta a todas las aristas, son los que se alcanzan desde pe. "
           "Un recorrido desde pe en el grafo inverso los marca. "
           "Aquí: cinco, cuatro, dos y tres. El ciclo entre seis y siete no nos afecta.",
           e_paso1, titulo="1 · Lo necesario", extra=1.5),
    Escena("Paso dos: ¿está lo quemado entre lo necesario? "
           "Aquí no: el uno no hace falta para el cinco. "
           "Si estuviera, o si el plato fuera lo quemado, la respuesta es no.",
           e_paso2, titulo="2 · Lo quemado", extra=1.5),
    Escena("Paso tres: un orden topológico solo de las necesarias, con el algoritmo de Kahn. "
           "Contamos cuántas aristas de entrada tiene cada una dentro del conjunto. "
           "Las que tienen cero están libres; sacamos siempre la menor, y restamos uno a sus sucesoras. "
           "Cuando una llega a cero, queda libre. "
           "Sale dos, tres, cuatro, cinco.",
           e_paso3, titulo="3 · El orden", extra=2.0),
    Escena("¿Y si hay un ciclo entre las necesarias? "
           "Entonces nunca llegan a cero entradas, y Kahn no consigue sacarlas a todas. "
           "Si el orden tiene menos elaboraciones que el total, la respuesta es no.",
           e_ciclo, titulo="Ciclos", extra=1.5),
    Escena("En el código, primero el recorrido con una pila en el inverso. "
           "Después la comprobación de lo quemado. "
           "Luego Kahn: contar entradas, meter las libres en una cola de mínimos y sacarlas. "
           "Al final, si faltan elaboraciones, hay ciclo; si no, se escribe sí y el orden.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("Si ese es igual a pe, el plato está quemado: no. "
           "Pe sale siempre la última, porque todo lo necesario llega a ella. "
           "La cola de mínimos hace que salga siempre la menor disponible. "
           "Y el coste es ene más a por logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: lo necesario se saca del grafo inverso, se descarta si incluye lo quemado, y se ordena con Kahn; si no salen todas, hay un ciclo.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/Eval-1", "../Eval-1_masterhash.mp4", "Eval-1")
