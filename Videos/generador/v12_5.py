"""Vídeo EJ 12-5 · Bizcocho con frutas (animado)."""
from vidlib import C, font
from anim import Escena, mix, ease, lerp
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-5/EJ_12-5.cpp"
B = [0, 1, 2, 0, 0, 2, 1, 2]
n = len(B)
NOMBRE = {0: "—", 1: "N", 2: "L"}
FRUTA = {1: (240, 140, 40), 2: (245, 220, 60)}


def igual(a, b):
    return int(B[a] != 0 and B[a] == B[b])


D = {}


def dias(i, largo):
    return 0 if largo == 0 else D[(largo, i)]


def opciones(i, largo):
    j = i + largo - 1
    return [("dos izquierda", dias(i + 2, largo - 2), igual(i, i + 1)),
            ("dos derecha", dias(i, largo - 2), igual(j - 1, j)),
            ("uno de cada", dias(i + 1, largo - 2), igual(i, j))]


ORDEN = [(largo, i) for largo in range(2, n + 1, 2) for i in range(n - largo + 1)]
for largo, i in ORDEN:
    D[(largo, i)] = max(a + b for _, a, b in opciones(i, largo))
assert D[(n, 0)] == 2

TB = Tabla(20, 150, 4, 7, cw=70, ch=80, lw=110, cabecera=[str(i + 1) for i in range(7)],
           etiquetas=[f"largo {k}" for k in (2, 4, 6, 8)], tam=30)
FUERA = {(r, i): (30, 40, 62) for r, largo in enumerate((2, 4, 6, 8)) for i in range(7) if i > n - largo}


def trozo(f, x, y, v, u=1.0, borde=None, w=86, h=104):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), 12, fill=mix(C["bot"], (196, 140, 80), u),
                          outline=mix(C["bot"], borde or (120, 78, 40), u), width=7 if borde else 3)
    if v:
        f.d.ellipse((x - 24, y - h / 2 + 8, x + 24, y - h / 2 + 56), fill=mix(C["bot"], FRUTA[v], u))
    f.d.text((x, y + h / 4), str(v), font=font(30, True), fill=mix(C["bot"], (45, 25, 8), u), anchor="mm")


def dib(f):
    for k, v in enumerate([1, 2, 0, 1]):
        trozo(f, 790 + 100 * k, 310, v, f.p(0.3 + 0.2 * k, 0.5))


JUGADAS = [(0, 7), (1, 6), (2, 5), (3, 4)]


def e_problema(f):
    texto(f, (640, 80), "cada día, dos trozos... pero solo por los extremos", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    xs = [220 + 120 * k for k in range(n)]
    quitados = {}
    for d, par in enumerate(JUGADAS):
        t = f.c(2) + 1.8 * d
        if f.t >= t:
            for idx in par:
                quitados[idx] = (d, f.lin(t, 0.8))
    for k, v in enumerate(B):
        if k in quitados:
            d, u = quitados[k]
            lado = JUGADAS[d].index(k)
            x = lerp(xs[k], 230 + 270 * d + 90 * lado, ease(u))
            y = lerp(250, 460, ease(u))
            trozo(f, x, y, v, 1, w=lerp(86, 66, u), h=lerp(104, 80, u))
        else:
            trozo(f, xs[k], 250, v, aparece(f, f.c(0)))
    for d, (a, b) in enumerate(JUGADAS):
        if a in quitados and quitados[a][1] >= 1:
            ok = igual(a, b)
            texto(f, (275 + 270 * d, 540), f"día {d + 1}  {'✓' if ok else '✗'}", 28, "green" if ok else "muted", 1, anchor="mm")
    texto(f, (640, 140), "1 = naranja    2 = limón    0 = sin fruta", 24, "muted", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 620), "máximo de días con la misma fruta: 2", 34, "green", aparece(f, f.c(3)), anchor="mm")


def e_tabla(f):
    nn = avance(f, 1, 4, len(ORDEN))
    vals = {((largo // 2) - 1, i): D[(largo, i)] for largo, i in ORDEN[:nn]}
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= f.c(1) else None
    marca = {(cur[0] // 2 - 1, cur[1]): "gold"} if cur else {}
    if f.t >= f.c(4):
        marca = {(3, 0): "green"}
    for k, v in enumerate(B):
        hl = "gold" if cur and cur[1] <= k < cur[1] + cur[0] else None
        trozo(f, 100 + 66 * k, 90, v, aparece(f, f.c(0)), borde=C[hl] if hl else None, w=58, h=70)
    TB.dibuja(f, vals, marca=marca, sombra=FUERA)
    if cur:
        largo, i = cur
        filas = []
        for nombre, a, b in opciones(i, largo):
            filas.append((f"{nombre:14} {a} + {b} = {a + b}", "green" if a + b == D[cur] else "text"))
        panel(f, 650, 190, 600, 240, f"trozos {i + 1}..{i + largo}", filas)
    if f.t >= f.c(4):
        texto(f, (640, 640), "dias(1, 8) = 2", 38, "green", aparece(f, f.c(4)), mono=True, anchor="mm")


ESC = [
    Escena("Bizcocho con frutas. Cuántos días podemos coincidir en el sabor cortando solo por los extremos.",
           e_portada("12-5", "Bizcocho con frutas", dib), titulo="Portada", extra=1.0),
    Escena("Hay un bizcocho en fila, y cada día cortamos dos trozos: los dos de un lado, o uno de cada lado. "
           "Un día es bueno si los dos trozos tienen la misma fruta: naranja con naranja, o limón con limón. "
           "En este ejemplo: el primer día no coincide, el segundo toca naranja, el tercero limón, y el último no tiene fruta. "
           "Lo máximo son dos días.",
           e_problema, titulo="El problema", extra=2.0),
    Escena("Después de cada día queda un trozo contiguo. Así que basta saber dónde empieza y dónde acaba. "
           "Días de i, j es el máximo de días buenos con los trozos de i a j. "
           "Si no quedan trozos, cero. "
           "Hay tres jugadas: dos por la izquierda, dos por la derecha, o uno de cada lado. "
           "Cada una suma uno si los dos trozos cortados tienen la misma fruta. "
           "Nos quedamos con la mejor.",
           e_lineas([(1, 80, "dias(i, j) = máximo de días buenos con los trozos i..j", "gold", 30),
                     (3, 180, "dias(i, j) = 0   si no quedan trozos", "text", 30, True),
                     (4, 300, "dias(i+2, j)   + igual(i, i+1)", "text", 32, True),
                     (4, 370, "dias(i, j−2)   + igual(j−1, j)", "text", 32, True),
                     (4, 440, "dias(i+1, j−1) + igual(i, j)  ", "text", 32, True),
                     (5, 530, "igual = 1 si tienen la misma fruta (y no es 0)", "muted", 26),
                     (6, 600, "dias(i, j) = máximo de las tres", "green", 32)]), titulo="Recurrencia", extra=1.5),
    Escena("La tabla se rellena por longitudes pares: primero los bizcochos de dos trozos. "
           "Cada fila usa solo la fila de arriba, que son bizcochos dos trozos más cortos. "
           "En cada casilla comparamos las tres jugadas. "
           "Y nos quedamos con la mayor. "
           "La última casilla, el bizcocho entero, vale dos.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Dos trozos del mismo lado son vecinos, y nunca tienen la misma fruta. "
           "Aun así hay que considerar esas jugadas: no dan puntos, pero cambian lo que queda en los extremos. "
           "Y un voraz que coja la pareja en cuanto la ve puede estropear dos parejas posteriores.",
           e_lineas([(0, 150, "mismo lado  →  nunca puntúa", "muted", 34),
                     (1, 280, "pero coloca otras frutas en los extremos", "gold", 34),
                     (2, 430, "coger la primera pareja que se ve no es óptimo", "text", 30),
                     (2, 500, "hay que comparar las tres jugadas", "green", 30)]), titulo="Ojo", extra=1.5),
    Escena("En el código, igual comprueba que haya fruta y que sea la misma. "
           "La matriz tiene filas y columnas de sobra para los intervalos vacíos. "
           "El largo avanza de dos en dos, y cada casilla es el máximo de las tres jugadas. "
           "Se escribe días de uno, ene.",
           e_codigo(CPP, "auto igual", "cout << dias[1][n]",
                    [["auto igual"], ["Matriz<int> dias"], ["for (int largo = 2", "dias[i][j] = max("], ["cout << dias[1][n]"]],
                    [("igual(a, b)", "los ceros no cuentan"), ("huecos", "intervalo vacío = 0"),
                     ("largo += 2", "siempre quedan pares"), ("respuesta", "dias[1][n]")], maxc=100, size=14),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: programación dinámica sobre intervalos. "
           "Tres jugadas posibles cada día. "
           "Dos ceros no puntúan. "
           "Y el coste es ene al cuadrado.",
           e_cierre("Bizcocho con frutas", [
               "estado: el trozo contiguo i..j que queda",
               "tres jugadas: izquierda, derecha, uno de cada",
               "dos ceros no son un día bueno",
               "O(N²) en tiempo y espacio"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-5", "../12-5_bizcocho_con_frutas.mp4")
