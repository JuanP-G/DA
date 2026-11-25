"""Vídeo EJ 11-L · La fiesta de graduación (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-L/EJ_11-L.cpp"
TEMA = "Tema 11 · Programación dinámica II"
MAN = ["Yesterday", "Macarena", "Mocatriz", "Buleria", "Orobroy", "Thriller"]
TAR = ["Macarena", "Buleria", "Texas", "Vagabundo", "Thriller", "Bizcochito"]
n, m = len(MAN), len(TAR)
CORTO = {s: s[:3] for s in MAN + TAR}

L = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        L[i][j] = L[i - 1][j - 1] + 1 if MAN[i - 1] == TAR[j - 1] else max(L[i - 1][j], L[i][j - 1])
ORDEN = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]


def reconstruye():
    pasos, i, j = [], n, m
    while i > 0 and j > 0:
        if MAN[i - 1] == TAR[j - 1]:
            pasos.append(("coge", i, j)); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            pasos.append(("arriba", i, j)); i -= 1
        else:
            pasos.append(("izq", i, j)); j -= 1
    return pasos


REC = reconstruye()
RES = [MAN[i - 1] for t, i, j in reversed(REC) if t == "coge"]
assert RES == ["Macarena", "Buleria", "Thriller"] and L[n][m] == 3
TB = Tabla(30, 110, n + 1, m + 1, cw=72, ch=62, lw=110, cabecera=["·"] + [CORTO[s] for s in TAR],
           etiquetas=["·"] + [CORTO[s] for s in MAN], tam=28)
VERDE = C["green"]


def ficha(f, x, y, s, u=1.0, borde=None, w=150, h=44, col=(210, 190, 235), tam=20):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), 12, fill=mix(C["bot"], col, u),
                          outline=mix(C["bot"], borde or (90, 80, 120), u), width=5 if borde else 2)
    f.d.text((x, y), s, font=font(tam, True), fill=mix(C["bot"], (30, 25, 45), u), anchor="mm")


def lista(f, x0, y, nombres, u=1.0, brillo=None, col=(210, 190, 235), sep=190, w=170, tam=19):
    for k, s in enumerate(nombres):
        ficha(f, x0 + k * sep, y, s, u, borde=(brillo or {}).get(k), w=w, col=col, tam=tam)


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        for r, y in enumerate([260, 340]):
            for k in range(4):
                ficha(f, 870 + k * 110, y, "♪", f.p(0.3 + 0.1 * (k + 4 * r), 0.4), w=90, h=60, col=(210, 190, 235) if r == 0 else (190, 220, 235), tam=30)
    portada(f, "EJ 11-L", "La fiesta de graduación", TEMA, dib)


def e_problema(f):
    xs = 130
    texto(f, (60, 110), "mañana", 28, "gold", aparece(f, f.c(0)))
    texto(f, (60, 400), "tarde", 28, AZUL, aparece(f, f.c(0)))
    lista(f, xs + 90, 190, MAN, aparece(f, f.c(0)), sep=185, w=170, tam=19)
    lista(f, xs + 90, 480, TAR, aparece(f, f.c(0)), col=(190, 220, 235), sep=185, w=170, tam=19)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        for a, b in [(1, 0), (3, 1), (5, 4)]:
            xa, xb = xs + 90 + a * 185, xs + 90 + b * 185
            f.d.line((xa, 212, xb, 458), fill=mix(C["bot"], VERDE, u), width=5)
            ficha(f, xa, 190, MAN[a], 1.0, borde=VERDE, w=170, tam=19)
            ficha(f, xb, 480, TAR[b], 1.0, borde=VERDE, w=170, tam=19)
    if f.t >= f.c(2):
        texto(f, (640, 630), "mismo orden en las dos listas, saltándose canciones", 28, "text", aparece(f, f.c(2)), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 575), "lista común más larga:  Macarena · Buleria · Thriller", 30, "green", aparece(f, f.c(3)), anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 685), "(si hay repeticiones, cada una con su propia aparición)", 22, "muted", aparece(f, f.c(4)), anchor="mm")


def e_idea(f):
    # mira solo las últimas canciones de los prefijos
    texto(f, (640, 70), "miramos las últimas canciones de los dos trozos", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    ficha(f, 400, 190, "… Thriller", aparece(f, f.c(0)), w=230, h=60, tam=26)
    ficha(f, 880, 190, "… Thriller", aparece(f, f.c(0)), w=230, h=60, tam=26, col=(190, 220, 235))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        f.d.line((400, 225, 640, 300), fill=mix(C["bot"], VERDE, u), width=5)
        f.d.line((880, 225, 640, 300), fill=mix(C["bot"], VERDE, u), width=5)
        texto(f, (640, 340), "iguales: entra en la lista  →  1 + lo de los trozos sin ellas", 28, "green", u, anchor="mm")
        texto(f, (640, 385), "larga(i−1, j−1) + 1", 28, "green", u, mono=True, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        ficha(f, 400, 520, "… Orobroy", u, w=230, h=60, tam=26)
        ficha(f, 880, 520, "… Vagabundo", u, w=230, h=60, tam=26, col=(190, 220, 235))
        texto(f, (640, 450), "distintas: una de las dos sobra", 28, NARANJA, u, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (400, 600), "quito la de la mañana", 24, NARANJA, u, anchor="mm")
        texto(f, (400, 640), "larga(i−1, j)", 26, NARANJA, u, mono=True, anchor="mm")
        texto(f, (880, 600), "quito la de la tarde", 24, AZUL, u, anchor="mm")
        texto(f, (880, 640), "larga(i, j−1)", 26, AZUL, u, mono=True, anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 695), "me quedo con la mayor", 28, "gold", aparece(f, f.c(4)), anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 70), "larga(i, j) = longitud de la lista común más larga entre las i primeras de mañana y las j primeras de tarde", 22, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (60, 140), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 185, "larga(i, 0) = larga(0, j) =", [("0", "con un trozo vacío no hay lista")], aparece(f, f.c(1)), size=24)
    texto(f, (60, y + 30), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 76, "larga(i, j) =", [("larga(i−1, j−1) + 1", "si a_i = b_j"),
                                                 ("max( larga(i−1, j), larga(i, j−1) )", "si no")],
                aparece(f, f.c(2)), size=26, colores=[VERDE, NARANJA])
    texto(f, (60, y + 36), "Respuesta:  larga(n, m)", 28, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 90), "y para escribir la lista, la tabla entera y volver desde (n, m)", 24, "text", aparece(f, f.c(4)))


def e_tabla(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    nn = max(0, min(len(ORDEN), int((f.t - t0) / paso) if f.t >= t0 else 0))
    vals = {(0, j): 0 for j in range(m + 1)}
    vals.update({(i, 0): 0 for i in range(n + 1)})
    for (i, j) in ORDEN[:nn]:
        vals[(i, j)] = L[i][j]
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= t0 else None
    marca, sombra = {}, {}
    if cur:
        i, j = cur
        marca[cur] = "gold"
        if MAN[i - 1] == TAR[j - 1]:
            sombra[(i - 1, j - 1)] = VERDE
        else:
            sombra[(i - 1, j)] = AZUL
            sombra[(i, j - 1)] = NARANJA
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw + 3.5 * TB.cw, 85), "canciones de la tarde →", 20, "muted", aparece(f, f.c(0)), anchor="mm")
    if cur:
        i, j = cur
        u = min(1, ((f.t - t0) % paso) / paso * 2.5)
        f.box(690, 110, 560, 330, "casilla actual")
        texto(f, (715, 160), f"{MAN[i - 1]}", 26, "gold", 1, fondo=C["panel"])
        texto(f, (715, 200), f"{TAR[j - 1]}", 26, AZUL, 1, fondo=C["panel"])
        if MAN[i - 1] == TAR[j - 1]:
            TB.flecha_entre(f, (i - 1, j - 1), cur, VERDE, u=u)
            texto(f, (715, 270), "¡iguales!", 30, "green", 1, fondo=C["panel"])
            texto(f, (715, 320), f"{L[i - 1][j - 1]} + 1 = {L[i][j]}", 30, "green", 1, mono=True, fondo=C["panel"])
        else:
            TB.flecha_entre(f, (i - 1, j), cur, AZUL, u=u)
            TB.flecha_entre(f, (i, j - 1), cur, NARANJA, u=u)
            texto(f, (715, 270), "distintas", 28, "muted", 1, fondo=C["panel"])
            texto(f, (715, 320), f"max({L[i - 1][j]}, {L[i][j - 1]}) = {L[i][j]}", 30, "text", 1, mono=True, fondo=C["panel"])
    if f.t >= t1:
        TB.dibuja(f, {(i, j): L[i][j] for i in range(n + 1) for j in range(m + 1)}, marca={(n, m): "green"})
        texto(f, (900, 600), f"larga({n}, {m}) = {L[n][m]}", 36, "green", aparece(f, t1), mono=True, anchor="mm")


def e_reconstruye(f):
    vals = {(i, j): L[i][j] for i in range(n + 1) for j in range(m + 1)}
    t0 = f.c(1)
    paso = (f.c(4) - t0) / len(REC)
    q = int((f.t - t0) / paso) if f.t >= t0 else -1
    q = min(q, len(REC) - 1)
    marca = {}
    if q >= 0:
        tipo, i, j = REC[q]
        marca[(i, j)] = "gold"
    TB.dibuja(f, vals, marca=marca)
    for r in range(max(0, q)):
        tipo, i, j = REC[r]
        dest = {"coge": (i - 1, j - 1), "arriba": (i - 1, j), "izq": (i, j - 1)}[tipo]
        TB.flecha_entre(f, (i, j), dest, VERDE if tipo == "coge" else (AZUL if tipo == "arriba" else NARANJA))
    if q >= 0:
        tipo, i, j = REC[q]
        txt = {"coge": f"{MAN[i - 1]} = {TAR[j - 1]}: la cojo", "arriba": "distintas: subo (arriba ≥ izquierda)",
               "izq": "distintas: voy a la izquierda"}[tipo]
        f.box(690, 110, 560, 150, "paso")
        texto(f, (715, 170), txt, 26, "green" if tipo == "coge" else NARANJA, 1, fondo=C["panel"])
    # lista que va saliendo (de atrás hacia delante)
    cogidas = [MAN[i - 1] for k, (t, i, j) in enumerate(REC) if t == "coge" and f.t >= t0 + k * paso]
    y = 330
    texto(f, (690, y - 40), "sale de atrás hacia delante:", 22, "muted", aparece(f, t0), fondo=C["bot"])
    for k, s in enumerate(cogidas):
        ficha(f, 800 + k * 0, y + 20 + 56 * k, s, 1.0, borde=VERDE, w=220, h=46, tam=22)
    if f.t >= f.c(4):
        texto(f, (900, 560), "reverse", 28, "gold", aparece(f, f.c(4)), mono=True, anchor="mm")
        texto(f, (900, 610), "Macarena Buleria Thriller", 28, "green", aparece(f, f.c(4) + 0.6), anchor="mm")


def e_lectura(f):
    f.box(40, 110, 580, 480, "cada lista, una línea")
    f.box(660, 110, 580, 480, "tras el número de casos")
    entrada = ["4", "One Respect Radio_Ga_Ga One …", "Respect One Volando_voy …", "Despacito Fiesta_pagana", "Grandola_Vila_Morena", "…"]
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        for k, s in enumerate(entrada[1:5]):
            texto(f, (70, 170 + 55 * k), s, 22, "text" if k < 2 else "muted", u, mono=True, fondo=C["panel"])
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (70, 420), "una lista puede ser VACÍA", 24, "gold", u, fondo=C["panel"])
        texto(f, (70, 465), "→  getline + istringstream, no cin >> palabra", 22, "muted", u, fondo=C["panel"], bold=False)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (690, 170), "cin >> numCasos  deja el salto de línea", 24, "text", u, fondo=C["panel"])
        texto(f, (690, 220), "el primer getline lo leería vacío", 24, NARANJA, u, fondo=C["panel"])
        texto(f, (690, 290), "static bool primera", 24, "gold", u, mono=True, fondo=C["panel"])
        texto(f, (690, 335), "se come ese salto una vez", 22, "muted", u, fondo=C["panel"], bold=False)
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 420), "sin canciones comunes:", 24, "text", u, fondo=C["panel"])
        texto(f, (690, 465), "se escribe una línea vacía", 26, "green", u, fondo=C["panel"])


La = find_line(CPP, "vector<string> leeLista()")
Lb = find_line(CPP, "cout << '\\n';")
CODE = codigo(CPP, La, Lb, maxc=72)
L_GET = find_line(CPP, "getline(cin, linea);")
L_PRI = find_line(CPP, "if (primera)")
L_MAT = find_line(CPP, "Matriz<int> larga(n + 1, m + 1, 0);")
L_IGU = find_line(CPP, "if (a[i - 1] == b[j - 1]) larga[i][j]")
L_REC = find_line(CPP, "for (int i = n, j = m; i > 0 && j > 0; ) {")
L_REV = find_line(CPP, "reverse(lista.begin(), lista.end());")


def e_codigo(f):
    hl = {L_GET}
    if f.t >= f.c(1):
        hl = {L_MAT, L_IGU}
    if f.t >= f.c(2):
        hl = {L_REC}
    if f.t >= f.c(3):
        hl = {L_REV, Lb}
    f.code(40, 80, 840, 590, CODE, hl=hl, title="LCS con reconstrucción", size=15)
    f.box(900, 80, 340, 590, "qué hace")
    notas = [("getline + istringstream", "una lista por línea", C["blue"]),
             ("tabla (n+1) × (m+1)", "iguales: diagonal + 1", NARANJA),
             ("desde (n, m) hacia atrás", "coge, sube o va a la izquierda", C["green"]),
             ("reverse y a escribir", "una línea por caso", C["gold"])]
    for k, (a, b, col) in enumerate(notas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (925, 140 + 120 * k), a, 21, col, u, fondo=C["panel"])
            texto(f, (925, 180 + 120 * k), b, 19, "muted", u, bold=False, fondo=C["panel"])


def e_detalles(f):
    f.box(40, 110, 580, 480, "cuidado con")
    f.box(660, 110, 580, 480, "coste")
    cuid = [("el orden importa", "Columbia / Bohemian al revés: solo cabe una", C["blue"]),
            ("repeticiones", "cada una usa su propia aparición en las dos listas", NARANJA),
            ("empates", "vale cualquier lista de la longitud máxima", C["green"])]
    for k, (a, b, col) in enumerate(cuid):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (70, 170 + 130 * k), a, 26, col, u, fondo=C["panel"])
            texto(f, (70, 212 + 130 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 190), "O(n · m)", 44, "gold", u, mono=True, fondo=C["panel"])
        texto(f, (690, 270), "1000 × 1000", 28, "text", u, fondo=C["panel"])
        texto(f, (690, 330), "un millón de casillas", 26, "muted", u, fondo=C["panel"])
        texto(f, (690, 390), "unos 4 MB  →  cabe", 24, "muted", u, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "La fiesta de graduación", [
        "subsecuencia común más larga (LCS) de dos listas",
        "iguales: diagonal + 1;  distintas: max(arriba, izquierda)",
        "tabla entera y volver desde (n, m) cogiendo las iguales",
        "dar la vuelta a la lista; getline para las líneas vacías",
    ])


ESC = [
    Escena("La fiesta de graduación. Una lista de reproducción con las canciones que aceptan los dos grupos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Los de mañana proponen una lista de canciones, y los de tarde, otra. "
           "La lista final solo puede tener canciones que estén en las dos, y en el mismo orden que en cada una, aunque falten algunas. "
           "Aquí, Macarena, Buleria y Thriller aparecen en las dos listas, y en ese orden. "
           "Queremos la lista más larga posible. "
           "Y si una canción se repite, cada repetición necesita una aparición distinta en cada lista.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Para resolverlo, miramos las últimas canciones de los dos trozos. "
           "Si son iguales, esa canción entra en la lista, y seguimos con lo que queda de cada lado. "
           "Si son distintas, una de las dos sobra. "
           "O quitamos la de la mañana, o quitamos la de la tarde. "
           "Nos quedamos con la opción que dé la lista más larga.",
           e_idea, titulo="Últimas canciones", extra=1.5),
    Escena("Larga de i, j es la longitud de la lista común más larga entre las i primeras canciones de mañana y las j primeras de tarde. "
           "Con un trozo vacío, cero. "
           "Si las canciones i y j son iguales, uno más larga de i menos uno, j menos uno. "
           "Si no, el máximo entre quitar una u otra. "
           "La respuesta es larga de n, m, y para escribir la lista guardamos la tabla entera.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("Esta es la tabla, con las canciones de mañana en las filas y las de tarde en las columnas. "
           "Cuando las canciones coinciden, la casilla vale la diagonal más uno. "
           "Cuando no, el máximo entre la casilla de arriba y la de la izquierda. "
           "Y en la esquina sale tres: tres canciones en común, en orden.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Para saber cuáles son, volvemos desde la esquina. "
           "Si las canciones coinciden, la cogemos y vamos a la diagonal. "
           "Si no, subimos o vamos a la izquierda, hacia el lado que tenga el mayor valor. "
           "Así las canciones salen de la última a la primera. "
           "Por eso al final damos la vuelta a la lista, y sale Macarena, Buleria, Thriller.",
           e_reconstruye, titulo="Reconstruir la lista", extra=2.0),
    Escena("Un detalle de la entrada: cada lista ocupa una línea, y puede estar vacía. "
           "Por eso se lee la línea entera con getline y se trocea con un istringstream, en vez de leer palabras sueltas. "
           "Además, después de leer el número de casos queda un salto de línea pendiente, y el primer getline lo leería vacío. "
           "Por eso, la primera vez, se descarta. "
           "Y si no hay canciones comunes, se escribe una línea vacía.",
           e_lectura, titulo="Leer las listas", extra=1.5),
    Escena("En el código, primero se leen las dos listas. "
           "Después se rellena la tabla: si las canciones coinciden, la diagonal más uno; si no, el máximo. "
           "Luego se recorre hacia atrás desde la esquina, recogiendo las canciones coincidentes. "
           "Se da la vuelta a la lista y se escribe, separada por espacios.",
           e_codigo, titulo="El código", extra=1.5),
    Escena("Tres cuidados. "
           "El orden importa: si dos canciones están al revés, solo cabe una de ellas. "
           "Las repeticiones usan cada una su propia aparición. "
           "Y si hay varias listas igual de buenas, vale cualquiera. "
           "El coste es n por m: con mil canciones por lista, un millón de casillas.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es la subsecuencia común más larga. "
           "Si las canciones coinciden, diagonal más uno; si no, el máximo de arriba e izquierda. "
           "Se vuelve desde la esquina cogiendo las coincidencias, y se da la vuelta a la lista. "
           "Y las líneas vacías se leen con getline.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-L", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-L: {build(ESC, '../11-L_la_fiesta_de_graduacion.mp4'):.0f}s")
