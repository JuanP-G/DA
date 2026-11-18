"""Vídeo EJ 03-2 · 12 points go to… (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo, arbol, arbol_anim

CPP = "../../3-Colas de prioridad variable (Heapsort)/EJ_03-2/EJ_03-2.cpp"
TEMA = "Tema 3 · Colas de prioridad variable"
EVENTOS = [("Germany", 8), ("France", 8), ("?", None), ("Spain", 12), ("?", None), ("Spain", 8),
           ("Italy", 22), ("?", None), ("Italy", -7), ("?", None)]
COLS = {"Germany": C["gold"], "France": C["blue"], "Spain": C["red"], "Italy": C["green"]}


def antes(a, b):
    return (-a[0], a[1]) < (-b[0], b[1])


def simula():
    pq, idx, est = Monticulo(antes), {}, []
    for nom, pts in EVENTOS:
        if nom == "?":
            e, (p, n) = pq.top()
            est.append((nom, pts, pq.copia(), dict(idx), f"{n} {p}", None))
        else:
            nuevo = nom not in idx
            if nuevo:
                idx[nom] = len(idx)
            act = 0 if nuevo else pq.a[pq.pos[idx[nom]]][1][0]
            pq.update(idx[nom], (act + pts, nom))
            est.append((nom, pts, pq.copia(), dict(idx), None, act))
    return est


EST = simula()


def etq(e, p):
    return f"{p[1][:3]}\n{p[0]}"


def colores(arr):
    return {e: COLS[p[1]] for e, p in arr}


def e_portada(f):
    def dib(f):
        for k, (n, c) in enumerate([("12", C["gold"]), ("10", C["blue"]), ("8", C["red"])]):
            caja(f, 860 + k * 110, 330, n, c=c, u=f.p(0.3 + 0.2 * k, 0.5), w=90, h=70, tam=32)
    portada(f, "EJ 03-2", "12 points go to…", TEMA, dib)


def e_problema(f):
    texto(f, (640, 70), "votaciones que llegan una a una", 26, "text", aparece(f, f.c(0)), anchor="mm")
    for k, (n, p) in enumerate(EVENTOS[:6]):
        t0 = f.c(0) + 0.3 * k
        if f.t < t0:
            continue
        u = aparece(f, t0)
        y = 140 + k * 62
        s = "?" if n == "?" else f"{n}  {p:+d}"
        caja(f, 300, y, s, c="gold" if n == "?" else COLS[n], u=u, w=260, h=48, tam=22)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (520, 270), "suma (o resta) puntos a un país", 22, "text", u)
        texto(f, (520, 270 + 2 * 62), "?  →  ¿quién va primero y con cuántos?", 22, "gold", u)
    if f.t >= f.c(2):
        etiqueta(f, (640, 600), "empate a puntos: el nombre menor va antes", 24, "text", aparece(f, f.c(2)))


def e_por_que(f):
    texto(f, (640, 70), "un país cambia de puntos cuando ya está en la cola", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(1))
    caja(f, 420, 260, "priority_queue", c="red", u=u, w=300, h=60, tam=24)
    texto(f, (420, 330), "no deja cambiar la prioridad", 22, "red", u, anchor="mm")
    texto(f, (420, 360), "de un elemento que ya está", 22, "red", u, anchor="mm")
    if f.t >= f.c(2):
        u2 = aparece(f, f.c(2))
        caja(f, 860, 260, "IndexPQ", c="green", u=u2, w=300, h=60, tam=24)
        texto(f, (860, 330), "update(índice, nueva prioridad)", 22, "green", u2, anchor="mm", mono=True)
        texto(f, (860, 360), "y el elemento flota o se hunde", 22, "green", u2, anchor="mm")
    if f.t >= f.c(3):
        u3 = aparece(f, f.c(3))
        texto(f, (640, 480), "índice: nº de país (unordered_map nombre → índice)", 24, "text", u3, anchor="mm")
        texto(f, (640, 530), "prioridad: (puntos, nombre)", 24, "text", u3, anchor="mm")


def e_traza(f):
    k, fr = paso_idx(f, f.c(0), f.T - 1.5, len(EST))
    k = max(0, min(k, len(EST) - 1))
    nom, pts, arr, idx, salida, act = EST[k]
    prev = EST[k - 1][2] if k > 0 else []
    if nom == "?":
        arbol(f, arr, 820, 190, 640, etq, marca={0}, colores=colores(arr), r=40, tam=20)
    else:
        arbol_anim(f, prev, arr, (fr - 0.2) / 0.5, 820, 190, 640, etq, marca_elem=idx.get(nom), colores=colores(arr), r=40, tam=20)
    # evento actual y lista de eventos
    for q, (n, p) in enumerate(EVENTOS):
        y = 110 + q * 52
        s = "?" if n == "?" else f"{n} {p:+d}"
        c = "gold" if q == k else ("dim" if q < k else "border")
        caja(f, 150, y, s, c=c, w=200, h=40, tam=18, borde=4 if q == k else 2,
             txt=None if q >= k else "dim")
    if nom == "?":
        etiqueta(f, (820, 620), f"?  →  {salida}", 30, "gold", 1, mono=True)
    else:
        s = f"{nom}: {act} {pts:+d} = {act + pts}" + ("   (nuevo)" if act == 0 and k == [i for i, e in enumerate(EVENTOS) if e[0] == nom][0] else "   update")
        etiqueta(f, (820, 620), s, 24, "text", 1, mono=True)
    texto(f, (820, 120), "montículo: arriba, el mejor", 20, "muted", 1, anchor="mm")


def e_hunde(f):
    # Italy 22 → 15: baja y Spain 20 sube
    a = EST[7][2]
    b = EST[8][2]
    ita = [e for e, p in b if p[1] == "Italy"][0]
    arbol_anim(f, a, b, f.lin(f.c(1), 1.5), 640, 200, 700, etq, marca_elem=ita, colores=colores(b), r=42, tam=20)
    texto(f, (640, 90), "Italy −7: su prioridad empeora", 28, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 560), "update la HUNDE: se cambia con su mejor hijo mientras haga falta", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 630), "si mejorara, FLOTARÍA hacia arriba · O(log n) en los dos casos", 24, "green", aparece(f, f.c(2)))


A_L = find_line(CPP, "struct Mejor {")
B_L = find_line(CPP, "pq.update(idx, { actuales + puntos, nombre });")
F_L = find_line(CPP, "for (int i = 0; i < n; ++i) {")
L_Q = find_line(CPP, "auto const& lider = pq.top().prioridad;")
L_NU = find_line(CPP, "if (it == indice.end()) {")
L_PR = find_line(CPP, "actuales = pq.priority(idx).first;")


def e_codigo(f):
    if f.t < f.c(1):
        lines = codigo(CPP, A_L, A_L + 5, maxc=90)
        f.code(40, 90, 1200, 300, lines, hl=set(range(A_L + 2, A_L + 4)), title="comparador Mejor", size=22)
        return
    lines = [(n, t) for n, t in codigo(CPP, F_L, B_L + 2, maxc=90) if not t.strip().startswith("//") and t.strip()]
    marcas = [(f.c(1), {L_Q, L_Q + 1}), (f.c(2), set(range(L_NU, L_NU + 5))), (f.c(3), {L_PR}), (f.c(4), {B_L})]
    hl = set()
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(40, 70, 1200, 620, lines, hl=hl, title="bucle de eventos", size=19)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("la prioridad lleva el nombre: así el empate se resuelve en el comparador", "text"),
             ("update inserta si el índice no estaba, y si estaba lo recoloca", "text"),
             ("priority(idx) da los puntos actuales del país", "text"),
             ("cada evento O(log n); cada ? O(1)", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "12 points go to…", [
        "IndexPQ: índice = país, prioridad = (puntos, nombre)",
        "Mejor: más puntos antes; empate, nombre menor",
        "votación: update con los puntos nuevos",
        "?: top, en O(1)",
    ])


ESC = [
    Escena("Doce puntos van para… Saber en cada momento quién va ganando.", e_portada, titulo="Portada", extra=1.0),
    Escena("Las votaciones llegan una a una. "
           "Cada una suma o resta puntos a un país, y una interrogación pregunta quién va primero y con cuántos puntos. "
           "Si dos países empatan, va antes el de nombre menor.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("La dificultad es que un país cambia de puntos cuando ya está en la cola. "
           "Una priority queue normal no deja cambiar la prioridad de algo que ya está dentro. "
           "La IndexPQ sí: update con el índice y la nueva prioridad, y el elemento flota o se hunde a su sitio. "
           "El índice es el número de cada país, que se guarda en un mapa, y la prioridad es el par puntos, nombre.",
           e_por_que, titulo="Por qué IndexPQ", extra=1.5),
    Escena("Vamos con el ejemplo. Alemania ocho, y Francia ocho: empatan, y Francia va arriba por el nombre. "
           "La pregunta responde Francia ocho. "
           "España doce sube a la cima. "
           "España suma ocho más: veinte. Italia llega con veintidós y pasa delante. "
           "Italia pierde siete, baja a quince, y España vuelve a liderar con veinte.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("Fíjate en el último cambio: Italia empeora su prioridad. "
           "Update la hunde, cambiándola con su mejor hijo mientras haga falta. "
           "Si mejorara, flotaría hacia arriba. En los dos casos, logaritmo de ene.",
           e_hunde, titulo="Flotar y hundir", extra=1.5),
    Escena("En el código, el comparador Mejor pone antes más puntos, y con empate, el nombre menor. "
           "La interrogación lee la cima. "
           "Si el país es nuevo, se le da el siguiente índice y parte de cero. "
           "Si ya estaba, priority da sus puntos actuales. "
           "Y update guarda la nueva prioridad.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("Meter el nombre dentro de la prioridad permite resolver el empate en el comparador. "
           "Update sirve tanto para insertar como para cambiar. "
           "Priority da los puntos actuales. "
           "Cada votación cuesta logaritmo de ene, y cada pregunta, constante.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una IndexPQ con el país como índice y los puntos y el nombre como prioridad; cada votación es un update, y cada pregunta, la cima.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/03-2", "../03-2_12_points_go_to.mp4", "03-2")
