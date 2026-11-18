"""Vídeo EJ 09-L · Necesitamos agua (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../9-Algoritmos voraces II/EJ_09-L/EJ_09-L.cpp"
TEMA = "Tema 9 · Algoritmos voraces II"
# ejemplo 2 del enunciado: pueblos 2..5
DN = {2: 15, 3: 20, 4: 5, 5: 20}
DS = {2: 105, 3: 100, 4: 100, 5: 100}
PUE = [2, 3, 4, 5]
PN, PS = (640, 120), (640, 640)
POS = {2: (330, 330), 3: (520, 300), 4: (760, 300), 5: (950, 330)}
DIF = {v: DN[v] - DS[v] for v in PUE}
ORDD = sorted(PUE, key=lambda v: DIF[v])
K = len(PUE) // 2
BASE = sum(DS.values())
TOTAL = BASE + sum(DIF[v] for v in ORDD[:K])


def isla(f, u=1.0):
    f.d.ellipse((140, 70, 1140, 700), fill=mix(C["bot"], (60, 110, 70), u), outline=mix(C["bot"], (220, 200, 140), u), width=6)


def planta(f, xy, s, c, u=1.0):
    if u <= 0:
        return
    x, y = xy
    f.d.rounded_rectangle((x - 50, y - 30, x + 50, y + 30), 10, fill=mix(C["bot"], c, u))
    f.d.text((x, y), s, font=font(22, True), fill=mix(C["bot"], C["node_t"], u), anchor="mm")


def pueblo(f, v, u=1.0, c=None):
    if u <= 0:
        return
    x, y = POS[v]
    c = c or C["node"]
    f.d.polygon([(x - 30, y), (x, y - 26), (x + 30, y)], fill=mix(C["bot"], C["red"], u))
    f.d.rectangle((x - 24, y, x + 24, y + 34), fill=mix(C["bot"], c, u))
    f.d.text((x, y + 17), str(v), font=font(20, True), fill=mix(C["bot"], C["node_t"], u), anchor="mm")


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.8)
        f.d.ellipse((780, 220, 1160, 460), fill=mix(C["bot"], (60, 110, 70), u))
        for k in range(3):
            y = 300 + 30 * k
            f.d.ellipse((930, y, 960, y + 40), fill=mix(C["bot"], (120, 200, 255), f.p(0.6 + 0.2 * k, 0.5)))
    portada(f, "EJ 09-L", "Necesitamos agua", TEMA, dib)


def e_problema(f):
    isla(f, aparece(f, f.c(0)))
    planta(f, PN, "Norte", C["blue"], aparece(f, f.c(0)))
    planta(f, PS, "Sur", NARANJA, aparece(f, f.c(0)))
    for k, v in enumerate(PUE):
        pueblo(f, v, aparece(f, f.c(1) + 0.2 * k))
    if f.t >= f.c(2):
        # un camión sale del norte, va al pueblo 4 y vuelve
        u = f.lin(f.c(2), 3.0)
        a, b = PN, POS[4]
        p = mueve(a, b, u * 2) if u < 0.5 else mueve(b, a, (u - 0.5) * 2)
        f.d.rounded_rectangle((p[0] - 20, p[1] - 12, p[0] + 20, p[1] + 12), 5, fill=C["blue"])
        texto(f, (900, 180), "ida y vuelta: 2 · distancia", 22, "gold", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 520), "la MITAD de los pueblos desde cada planta", 26, "gold", aparece(f, f.c(3)))


def e_dijkstra(f):
    isla(f)
    planta(f, PN, "Norte", C["blue"])
    planta(f, PS, "Sur", NARANJA)
    for v in PUE:
        pueblo(f, v)
    # ondas de Dijkstra
    for t0, src, col, D, dy in ((f.c(0), PN, C["blue"], DN, -50), (f.c(1), PS, NARANJA, DS, 70)):
        if f.t < t0:
            continue
        r = f.lin(t0, 2.0) * 700
        if r < 700:
            f.d.ellipse((src[0] - r, src[1] - r, src[0] + r, src[1] + r), outline=col, width=3)
        for v in PUE:
            dist = ((POS[v][0] - src[0]) ** 2 + (POS[v][1] - src[1]) ** 2) ** 0.5
            if r >= dist or r >= 700:
                x, y = POS[v]
                caja(f, x, y + dy, D[v], c=col, w=60, h=34, tam=18)
    if f.t >= f.c(2):
        etiqueta(f, (640, 470), "dN[v] y dS[v]: dos Dijkstra, uno desde cada planta", 24, "text", aparece(f, f.c(2)))


def tabla(f, u=1.0, hasta=4, marcar=0):
    x0, y0 = 250, 170
    cab = ["pueblo", "dN", "dS", "dN − dS"]
    for j, s in enumerate(cab):
        texto(f, (x0 + j * 200, y0), s, 22, "muted", u, anchor="mm")
    for i, v in enumerate(PUE):
        y = y0 + 60 + i * 56
        for j, val in enumerate([v, DN[v], DS[v], DIF[v]]):
            if j == 3 and i >= hasta:
                continue
            c = "text" if j < 3 else ("green" if v in ORDD[:marcar] else "gold")
            texto(f, (x0 + j * 200, y), str(val), 26, c, u, anchor="mm", mono=True)


def e_reparto(f):
    tabla(f, 1, hasta=4 if f.t >= f.c(1) else 0, marcar=K if f.t >= f.c(3) else 0)
    texto(f, (640, 70), "todos al sur:  Σ dS = 405", 30, NARANJA, aparece(f, f.c(0)), mono=True, anchor="mm")
    if f.t >= f.c(1):
        texto(f, (1040, 420), "pasar v al norte", 20, "muted", aparece(f, f.c(1)), anchor="mm")
        texto(f, (1040, 448), "cambia dN − dS", 20, "muted", aparece(f, f.c(1)), anchor="mm")
    # barras ordenadas
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        for k, v in enumerate(ORDD):
            x = 300 + k * 180
            h = -DIF[v] * 1.1
            c = C["green"] if (k < K and f.t >= f.c(3)) else C["muted"]
            f.d.rectangle((x - 40, 500, x + 40, 500 + h * u), fill=mix(C["bot"], c, u))
            texto(f, (x, 515 + h), f"{DIF[v]} ({v})", 20, "text", u, anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (1090, 560), f"405 − 185 = {TOTAL}", 26, "green", aparece(f, f.c(3)), mono=True)
    if f.t >= f.c(4):
        etiqueta(f, (1090, 640), f"respuesta = 2 · {TOTAL} = {2 * TOTAL}", 26, "gold", aparece(f, f.c(4)), mono=True)


def e_porque(f):
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        isla(f, u * 0.6)
        planta(f, PN, "Norte", C["blue"], u)
        planta(f, PS, "Sur", NARANJA, u)
        for v in PUE:
            pueblo(f, v, u, c=C["blue"] if v in ORDD[:K] else NARANJA)
        etiqueta(f, (640, 470), "los cuatro están más cerca del norte, pero solo caben dos", 24, "text", u)
    etiqueta(f, (640, 210), "coste = Σ dS  +  Σ (dN − dS) de los que van al norte", 26, "text", aparece(f, f.c(0)), mono=True)
    if f.t >= f.c(1):
        etiqueta(f, (640, 270), "Σ dS es fijo  →  elegir las (N−2)/2 diferencias más pequeñas", 24, "gold", aparece(f, f.c(1)))


A_L = find_line(CPP, "vector<long long> dN = dijkstra(g, 0)")
B_L = find_line(CPP, "cout << 2 * total")
CODE = codigo(CPP, A_L, B_L, maxc=80)
L_FOR = A_L + 3
L_SO = find_line(CPP, "sort(dif.begin(), dif.end());")
L_SU = find_line(CPP, "for (int k = 0; k < (N - 2) / 2; ++k)")


def e_codigo(f):
    marcas = [(f.c(0), {A_L}), (f.c(1), {L_FOR, L_FOR + 1, L_FOR + 2}), (f.c(2), {L_SO}), (f.c(3), {L_SU}), (f.c(4), {B_L})]
    hl = {A_L}
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(20, 100, 900, 380, CODE, hl=hl, title="reparto voraz", size=18)
    f.box(940, 100, 300, 380, "dijkstra(g, origen)")
    for k, s in enumerate(["el de siempre,", "con IndexPQ", "y long long"]):
        texto(f, (960, 160 + 40 * k), s, 22, "text", 1, fondo=C["panel"])


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("se trabaja con distancias y se multiplica por 2 al final (ida y vuelta)", "text"),
             ("long long: hasta 200.000 pueblos con distancias grandes", "text"),
             ("los pueblos son 2..N−1; el 1 y el N son las plantas", "text"),
             ("O((N + M) log N) por los Dijkstra, más O(N log N) por la ordenación", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Necesitamos agua", [
        "Dijkstra desde el norte y desde el sur",
        "empezar con todos al sur: Σ dS",
        "pasar al norte las (N−2)/2 de menor dN − dS",
        "respuesta: 2 · total",
    ])


ESC = [
    Escena("Necesitamos agua. Repartir los pueblos entre dos desalinizadoras con el menor coste.", e_portada, titulo="Portada", extra=1.0),
    Escena("En una isla hay dos plantas desalinizadoras: una al norte y otra al sur. "
           "Y hay pueblos, conectados por carreteras con su coste. "
           "A cada pueblo le llega un camión desde una planta, que va y vuelve. "
           "La mitad de los pueblos se sirven desde el norte y la otra mitad desde el sur.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Primero, hace falta saber lo que cuesta llegar a cada pueblo desde el norte: un Dijkstra desde la planta norte. "
           "Y otro desde la planta sur. "
           "Ya tenemos de ene y de ese para cada pueblo.",
           e_dijkstra, titulo="Dos Dijkstra", extra=1.5),
    Escena("Imagina que todos los pueblos van al sur: cuatrocientos cinco. "
           "Pasar un pueblo al norte cambia el coste en su de ene menos de ese. "
           "Ordenamos esas diferencias. "
           "Como hay que pasar exactamente la mitad, pasamos las más pequeñas: menos noventa y cinco y menos noventa, y queda doscientos veinte. "
           "Por la ida y la vuelta, la respuesta es cuatrocientos cuarenta.",
           e_reparto, titulo="El reparto voraz", extra=2.0),
    Escena("¿Por qué? El coste total es la suma de todos los de ese, más las diferencias de los que van al norte. "
           "La primera parte no cambia, así que basta elegir las diferencias más pequeñas. "
           "Fíjate: los cuatro pueblos están más cerca del norte, pero el norte solo tiene camiones para dos.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, dos llamadas a dijkstra. "
           "Un bucle suma los de ese y guarda las diferencias. "
           "Se ordenan. "
           "Se suman las ene menos dos entre dos primeras. "
           "Y se escribe el doble.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Todo se calcula con distancias y se multiplica por dos al final. "
           "Se usa long long, porque las sumas crecen mucho. "
           "Los pueblos son del dos al ene menos uno. "
           "Y el coste lo marcan los dos Dijkstra.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: dos Dijkstra, todos al sur, y se pasan al norte los pueblos con menor diferencia. La respuesta es el doble del total.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/09-L", "../09-L_necesitamos_agua.mp4", "09-L")
