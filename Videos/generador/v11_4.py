"""Vídeo EJ 11-4 · Seis grados de separación (animado)."""
import math
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-4/EJ_11-4.cpp"
TEMA = "Tema 11 · Programación dinámica II"
NOM = ["Marta", "Mario", "Roberto", "Raquel"]
ARISTAS = [(0, 1), (1, 2), (2, 3), (1, 3)]
n = 4
INF = None


def inicial():
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for a, b in ARISTAS:
        d[a][b] = d[b][a] = 1
    return d


def suma(a, b):
    return INF if a is INF or b is INF else a + b


def menor(a, b):
    if a is INF:
        return b
    if b is INF:
        return a
    return min(a, b)


SNAP = [inicial()]
CAMBIOS = [[]]
for k in range(n):
    d = [r[:] for r in SNAP[-1]]
    ch = []
    for i in range(n):
        for j in range(n):
            nv = menor(d[i][j], suma(SNAP[-1][i][k], SNAP[-1][k][j]))
            if nv != d[i][j]:
                d[i][j] = nv
                ch.append((i, j))
    SNAP.append(d)
    CAMBIOS.append(ch)
FIN = SNAP[-1]
assert max(max(r) for r in FIN) == 2

POS = {0: (150, 440), 1: (330, 330), 2: (500, 440), 3: (500, 220)}
TB = Tabla(640, 150, n, n, cw=110, ch=84, lw=140, cabecera=NOM, etiquetas=NOM, tam=32)
COL_NODO = [(150, 190, 230), (240, 170, 90), (150, 200, 150), (200, 150, 220)]


def red(f, x0, y0, pos, aristas, u=1.0, brillo=None, rotulos=True, ar=None, r=34, escala=1.0):
    """Dibuja el grafo de conocidos. brillo: nodos resaltados {nodo: color}. ar: aristas resaltadas {(a,b): color}."""
    if u <= 0:
        return
    ar = ar or {}
    brillo = brillo or {}
    for a, b in aristas:
        col = ar.get((a, b)) or ar.get((b, a))
        pa, pb = pos[a], pos[b]
        f.d.line((x0 + pa[0] * escala, y0 + pa[1] * escala, x0 + pb[0] * escala, y0 + pb[1] * escala),
                 fill=mix(C["bot"], col or C["border"], u), width=7 if col else 4)
    for i, (x, y) in pos.items():
        x, y = x0 + x * escala, y0 + y * escala
        col = brillo.get(i)
        f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], COL_NODO[i % 4], u),
                    outline=mix(C["bot"], col or (30, 40, 60), u), width=7 if col else 3)
        if rotulos:
            f.d.text((x, y), NOM[i][0], font=font(26, True), fill=mix(C["bot"], (30, 30, 40), u), anchor="mm")
            f.d.text((x, y + r + 20), NOM[i], font=font(20, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        pos = {0: (0, 90), 1: (110, 0), 2: (220, 90), 3: (110, 190), 4: (330, 0), 5: (330, 190)}
        ar = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (2, 4), (2, 5)]
        for k in range(len(pos)):
            pass
        red(f, 780, 200, {i: p for i, p in pos.items()}, ar, u=f.p(0.3, 0.8), rotulos=False, r=26)
    portada(f, "EJ 11-4", "Seis grados de separación", TEMA, dib)


def e_problema(f):
    u = aparece(f, f.c(0))
    red(f, 60, 40, POS, ARISTAS, u, escala=1.0)
    ar, br = {}, {}
    if f.t >= f.c(2):
        ar = {(0, 1): C["gold"], (1, 2): C["gold"]}
        br = {0: C["gold"], 2: C["gold"]}
        red(f, 60, 40, POS, ARISTAS, 1.0, brillo=br, ar=ar)
        texto(f, (700, 300), "Marta → Roberto:  2 relaciones", 30, "gold", aparece(f, f.c(2)), anchor="lm")
    if f.t >= f.c(1):
        texto(f, (700, 150), "grado entre dos personas:", 28, "text", aparece(f, f.c(1)), anchor="lm")
        texto(f, (700, 195), "el menor nº de relaciones que las une", 24, "muted", aparece(f, f.c(1)), anchor="lm", bold=False)
    if f.t >= f.c(3):
        u3 = aparece(f, f.c(3))
        texto(f, (700, 400), "grado de la red:", 28, "text", u3, anchor="lm")
        texto(f, (700, 450), "el MAYOR de todos los pares", 30, "green", u3, anchor="lm")
    if f.t >= f.c(4):
        u4 = aparece(f, f.c(4))
        texto(f, (700, 540), "si alguien no se alcanza:", 28, "red", u4, anchor="lm")
        texto(f, (700, 585), "DESCONECTADA", 36, "red", u4, anchor="lm")


def e_idea(f):
    # i ... k ... j
    pos = {0: (160, 330), 1: (640, 330), 2: (1120, 330)}
    nombres = ["i", "k", "j"]
    for q, (x, y) in pos.items():
        u = aparece(f, f.c(0))
        if u > 0:
            f.d.ellipse((x - 40, y - 40, x + 40, y + 40), fill=mix(C["bot"], COL_NODO[q], u), outline=mix(C["bot"], C["gold"] if q == 1 else (30, 40, 60), u), width=6 if q == 1 else 3)
            f.d.text((x, y), nombres[q], font=font(34, True, True), fill=mix(C["bot"], (30, 30, 40), u), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        f.d.arc((160, 150, 1120, 330 + 120), 200, 340, fill=mix(C["bot"], AZUL, u), width=6)
        texto(f, (640, 105), "dist(i, j)  hoy", 30, AZUL, u, mono=True, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        flecha(f, (200, 336), (600 - 0, 336), NARANJA, w=7, cab=18) if u > 0.5 else None
        texto(f, (400, 400), "dist(i, k)", 28, NARANJA, u, mono=True, anchor="mm")
        if u > 0.5:
            flecha(f, (680, 336), (1080, 336), NARANJA, w=7, cab=18)
        texto(f, (880, 400), "dist(k, j)", 28, NARANJA, u, mono=True, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (640, 520), "dist(i, j) = min( dist(i, j),  dist(i, k) + dist(k, j) )", 32, "gold", u, mono=True, anchor="mm")
        texto(f, (640, 580), "¿me conviene pasar por k?", 26, "muted", u, anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 70), "dist(i, j) tras permitir pasar por las personas 0..k", 24, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (60, 140), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 185, "dist(i, j) =", [("0", "si i = j"), ("1", "si se conocen"), ("∞", "si no")],
                aparece(f, f.c(1)), size=24, colores=[C["green"], C["gold"], C["red"]])
    texto(f, (60, y + 30), "Para k = 0, 1, ..., P−1", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 76, "dist(i, j) =", [("min( dist(i, j),  dist(i, k) + dist(k, j) )", "")], aparece(f, f.c(2)), size=26)
    texto(f, (60, y + 36), "Respuesta:  el máximo de la matriz  (o  ∞  →  DESCONECTADA)", 26, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 90), "una sola matriz,  O(P³)", 24, "muted", aparece(f, f.c(4)))


def e_floyd(f):
    t0, t1 = f.c(1), f.c(5)
    fase = (t1 - t0) / n
    k = -1 if f.t < t0 else min(n - 1, int((f.t - t0) / fase))
    snap = SNAP[0] if k < 0 else SNAP[k + 1] if ((f.t - t0) % fase) / fase > 0.5 else SNAP[k]
    vals = {(i, j): snap[i][j] for i in range(n) for j in range(n)}
    sombra, marca = {}, {}
    brillo, ar = {}, {}
    if k >= 0:
        brillo = {k: C["gold"]}
        for q in range(n):
            sombra[(k, q)] = AZUL
            sombra[(q, k)] = AZUL
        if ((f.t - t0) % fase) / fase > 0.5:
            for (i, j) in CAMBIOS[k + 1]:
                marca[(i, j)] = "green"
    red(f, 10, 40, POS, ARISTAS, 1.0, brillo=brillo, ar=ar, escala=0.85)
    TB.dibuja(f, vals, marca=marca, sombra=sombra, fmt=lambda v: "∞" if v is None else str(v))
    if k >= 0:
        texto(f, (640 + 70 + 2 * 110, 110), f"pasando por {NOM[k]}", 30, "gold", 1, anchor="mm")
        if CAMBIOS[k + 1] and ((f.t - t0) % fase) / fase > 0.5:
            texto(f, (900, 580), f"{len(CAMBIOS[k + 1])} casillas mejoran:  1 + 1 = 2", 28, "green", 1, anchor="mm")
        elif not CAMBIOS[k + 1] and ((f.t - t0) % fase) / fase > 0.5:
            texto(f, (900, 580), "ninguna mejora", 28, "muted", 1, anchor="mm")
    if f.t >= t1:
        mx = TB
        texto(f, (640, 660), "máximo de la matriz = 2  →  grado de separación 2", 34, "green", aparece(f, t1), anchor="mm")


def e_desconexa(f):
    # ejemplo 3: Lucia, Pablo, Elena, Jorge  +  una persona que no sale en ninguna relación (P = 5)
    nombres = ["Lucia", "Pablo", "Elena", "Jorge", "?"]
    pos = {0: (200, 260), 1: (360, 130), 2: (360, 390), 3: (80, 130), 4: (40, 430)}
    ar = [(0, 1), (1, 2), (2, 0), (0, 3)]
    for a, b in ar:
        u = aparece(f, f.c(0))
        if u > 0:
            f.d.line((pos[a][0] + 100, pos[a][1] + 50, pos[b][0] + 100, pos[b][1] + 50), fill=mix(C["bot"], C["border"], u), width=4)
    for i, (x, y) in pos.items():
        u = aparece(f, f.c(0)) if i < 4 else aparece(f, f.c(1))
        if u > 0:
            col = (150, 190, 230) if i < 4 else (90, 90, 110)
            f.d.ellipse((x + 100 - 32, y + 50 - 32, x + 100 + 32, y + 50 + 32), fill=mix(C["bot"], col, u),
                        outline=mix(C["bot"], C["red"] if i == 4 else (30, 40, 60), u), width=5 if i == 4 else 3)
            f.d.text((x + 100, y + 50), nombres[i][0], font=font(26, True), fill=mix(C["bot"], (30, 30, 40), u), anchor="mm")
            f.d.text((x + 100, y + 50 + 52), nombres[i] if i < 4 else "(sin relaciones)", font=font(20, True),
                     fill=mix(C["bot"], C["muted"], u), anchor="mm")
    if f.t >= f.c(1):
        texto(f, (700, 140), "P = 5 pero solo salen 4 nombres", 28, "text", aparece(f, f.c(1)), anchor="lm")
        texto(f, (700, 190), "la quinta persona no tiene relaciones", 24, "muted", aparece(f, f.c(1)), anchor="lm", bold=False)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (700, 300), "su fila y su columna: ∞", 28, "red", u, anchor="lm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (700, 400), "⇒  DESCONECTADA", 44, "red", u, anchor="lm")
    if f.t >= f.c(4):
        u = aparece(f, f.c(4))
        texto(f, (640, 600), "no hace falta buscar componentes:  basta comprobar si queda algún ∞", 26, "text", u, anchor="mm")


A = find_line(CPP, "Matriz<EntInf> dist(P, P, Infinito);")
B = find_line(CPP, "else cout << grado")
CODE = codigo(CPP, A, B, maxc=76)
L_ID = find_line(CPP, "auto id = [&](const string& nombre)")
L_REL = find_line(CPP, "dist[x][y] = dist[y][x] = 1;")
L_FK = find_line(CPP, "for (int k = 0; k < P; ++k)")
L_MIN = find_line(CPP, "if (dik + dist[k][j] < dist[i][j])")
L_MAX = find_line(CPP, "if (dist[i][j] > grado) grado = dist[i][j];")
L_DES = find_line(CPP, "if (grado == Infinito)")


def e_codigo(f):
    hl = {A, L_ID}
    if f.t >= f.c(1):
        hl = {L_REL}
    if f.t >= f.c(2):
        hl = {L_FK, L_MIN}
    if f.t >= f.c(3):
        hl = {L_MAX, L_DES}
    f.code(40, 80, 840, 580, CODE, hl=hl, title="Floyd-Warshall sobre Matriz<EntInf>", size=15)
    f.box(900, 80, 340, 580, "qué hace")
    notas = [("nombres → 0..P−1", "mapa: según aparecen", C["blue"]),
             ("relación = 1 (ida y vuelta)", "si no, ∞ (EntInf)", NARANJA),
             ("k fuera, i y j dentro", "inf + 1 sigue siendo ∞", C["green"]),
             ("máximo de la matriz", "∞  →  DESCONECTADA", C["gold"])]
    for k, (a, b, col) in enumerate(notas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (925, 140 + 120 * k), a, 21, col, u, fondo=C["panel"])
            texto(f, (925, 180 + 120 * k), b, 19, "muted", u, bold=False, fondo=C["panel"])


def e_detalles(f):
    f.box(40, 110, 580, 480, "cuidado con")
    f.box(660, 110, 580, 480, "coste")
    cuid = [("el orden de los bucles", "k SIEMPRE por fuera; si no, faltan caminos", C["blue"]),
            ("P = 1", "no hay pares: grado 0, no DESCONECTADA", NARANJA),
            ("hasta 10.000 relaciones", "los nombres se repiten: mapa nombre → número", C["green"])]
    for k, (a, b, col) in enumerate(cuid):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (70, 170 + 130 * k), a, 26, col, u, fondo=C["panel"])
            texto(f, (70, 212 + 130 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 190), "O(P³)", 44, "gold", u, mono=True, fondo=C["panel"])
        texto(f, (690, 270), "P ≤ 500", 28, "text", u, fondo=C["panel"])
        texto(f, (690, 330), "125 millones de pasos", 26, "muted", u, fondo=C["panel"])
        texto(f, (690, 390), "una matriz de 250.000 casillas", 24, "muted", u, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Seis grados de separación", [
        "distancias entre todos los pares: Floyd-Warshall",
        "dist(i, j) = min( dist(i, j), dist(i, k) + dist(k, j) )",
        "k fuera del todo; una sola matriz con EntInf",
        "el máximo de la matriz;  si queda ∞, DESCONECTADA",
    ])


ESC = [
    Escena("Seis grados de separación. Cuánto tardas en llegar de cualquiera a cualquiera a través de conocidos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos una red de personas con relaciones directas. "
           "El grado entre dos personas es el menor número de relaciones que hay que cruzar para unirlas. "
           "Marta conoce solo a Mario, así que para llegar a Roberto necesita dos relaciones. "
           "El grado de la red es el mayor de todos los pares: aquí, dos. "
           "Y si hay alguien al que no se llega nunca, la red está desconectada.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Queremos las distancias entre todos los pares a la vez. "
           "Fíjate en dos personas, i y j, y en una tercera, k. "
           "Hoy sabemos una distancia entre i y j, que puede ser infinita. "
           "Pero tal vez sea más corto ir de i a k, y de k a j. "
           "Si es así, nos quedamos con el mínimo. Esa es la idea de Floyd y Warshall.",
           e_idea, titulo="Pasar por k", extra=1.5),
    Escena("Al principio, la distancia de uno mismo es cero, si se conocen es uno, y si no, infinito. "
           "Después, para cada persona k, una detrás de otra, actualizamos todos los pares: "
           "el mínimo entre la distancia actual y la que pasa por k. "
           "La respuesta es el máximo de la matriz, o infinito si algún par no se alcanza. "
           "Es una sola matriz y cuesta P al cubo.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("Esta es la matriz de distancias. "
           "Con Marta como intermedia, no mejora nada: nadie pasa por ella. "
           "Con Mario, sí: Marta ya puede llegar a Roberto y a Raquel pasando por él, uno más uno, dos. "
           "Con Roberto y con Raquel no hay nada que mejorar. "
           "El máximo de la matriz es dos: ese es el grado de separación.",
           e_floyd, titulo="La matriz", extra=2.5),
    Escena("Un caso especial. Aquí hay cinco personas, pero solo aparecen cuatro nombres en las relaciones. "
           "La quinta persona no tiene ninguna relación. "
           "Su fila y su columna se quedan en infinito. "
           "Así que la red está desconectada. "
           "No hace falta buscar componentes: basta mirar si queda algún infinito en la matriz.",
           e_desconexa, titulo="Redes desconectadas", extra=1.5),
    Escena("En el código, la matriz es de enteros con infinito, EntInf, y los nombres se pasan a números con un mapa según van apareciendo. "
           "Cada relación pone un uno en los dos sentidos. "
           "Después, el bucle de k va por fuera, y dentro i y j. Como infinito más uno sigue siendo infinito, no hay que tratar casos aparte. "
           "Por último se busca el máximo y, si es infinito, se escribe desconectada.",
           e_codigo, titulo="El código", extra=1.5),
    Escena("Tres cuidados. "
           "El bucle de k siempre va el primero, por fuera. "
           "Con una sola persona no hay pares, y el grado es cero. "
           "Los nombres pueden repetirse en muchas relaciones, por eso el mapa. "
           "El coste es P al cubo: con quinientas personas, ciento veinticinco millones de pasos, que se hacen en una fracción de segundo.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: Floyd y Warshall calculan todas las distancias con una sola matriz. "
           "Se permite pasar por k, uno tras otro, tomando el mínimo. "
           "El grado de la red es el máximo de la matriz. "
           "Y si queda algún infinito, está desconectada.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-4", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-4: {build(ESC, '../11-4_seis_grados_de_separacion.mp4'):.0f}s")
