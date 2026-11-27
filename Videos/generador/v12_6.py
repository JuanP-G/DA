"""Vídeo EJ 12-6 · Alineamiento de secuencias (animado)."""
from vidlib import C, font
from anim import Escena, mix
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-6/EJ_12-6.cpp"
S = [[2, -2, 1, 1, -1], [-2, 12, -3, -2, -1], [1, -3, 5, 0, -1], [1, -2, 0, 3, -1], [-1, -1, -1, -1, -1]]
ID = {"A": 0, "C": 1, "G": 2, "T": 3, "-": 4}
a, b = "CGGATA", "TTAG"
n, m = len(a), len(b)


def s(x, y):
    return S[ID[x]][ID[y]]


M = [[0] * (m + 1) for _ in range(n + 1)]
for j in range(1, m + 1):
    M[0][j] = M[0][j - 1] + s("-", b[j - 1])
for i in range(1, n + 1):
    M[i][0] = M[i - 1][0] + s(a[i - 1], "-")
    for j in range(1, m + 1):
        M[i][j] = max(M[i - 1][j - 1] + s(a[i - 1], b[j - 1]), M[i - 1][j] + s(a[i - 1], "-"), M[i][j - 1] + s("-", b[j - 1]))
assert M[n][m] == 2

TB = Tabla(30, 90, n + 1, m + 1, cw=82, ch=72, lw=70, cabecera=["-"] + list(b), etiquetas=["-"] + list(a), tam=28)
BASE = [(0, j) for j in range(m + 1)] + [(i, 0) for i in range(1, n + 1)]
ORDEN = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]
BASES = {"A": (110, 190, 255), "C": (240, 160, 70), "G": (112, 222, 152), "T": (196, 150, 255), "-": (110, 120, 140)}


def base(f, x, y, c, u=1.0, r=30):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - r, y - r, x + r, y + r), 10, fill=mix(C["bot"], BASES[c], u))
    f.d.text((x, y), c, font=font(int(r), True), fill=mix(C["bot"], (15, 22, 40), u), anchor="mm")


def dib(f):
    for k, (x, y) in enumerate(zip("ATGC-C-", "-TACGCA")):
        base(f, 760 + 68 * k, 460, x, f.p(0.3 + 0.15 * k, 0.4))
        base(f, 760 + 68 * k, 530, y, f.p(0.4 + 0.15 * k, 0.4))


def e_problema(f):
    texto(f, (640, 80), "alinear dos cadenas rellenando con huecos", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (x, y) in enumerate(zip("ATGC-C-", "-TACGCA")):
        base(f, 400 + 80 * k, 220, x, aparece(f, f.c(1) + 0.15 * k))
        base(f, 400 + 80 * k, 300, y, aparece(f, f.c(1) + 0.15 * k))
    if f.t >= f.c(2):
        texto(f, (640, 400), "cada columna suma S[arriba, abajo]", 30, "text", aparece(f, f.c(2)), anchor="mm")
        texto(f, (640, 450), "matriz 5 × 5 en el orden  A C G T -", 26, "muted", aparece(f, f.c(2)), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 540), "nunca dos huecos en la misma columna", 28, "muted", aparece(f, f.c(3)), anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 610), "¿cuál es la puntuación máxima?", 34, "green", aparece(f, f.c(4)), anchor="mm")


def e_tabla(f):
    nb = avance(f, 1, 2, len(BASE))
    nn = avance(f, 2, 5, len(ORDEN))
    vals = {p: M[p[0]][p[1]] for p in BASE[:nb]}
    vals.update({p: M[p[0]][p[1]] for p in ORDEN[:nn]})
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= f.c(2) else None
    marca = {cur: "gold"} if cur else {}
    if f.t >= f.c(5):
        marca = {(n, m): "green"}
    TB.dibuja(f, vals, marca=marca)
    if cur:
        i, j = cur
        x, y = a[i - 1], b[j - 1]
        ops = [(f"{x} con {y}:  {M[i-1][j-1]} + {s(x, y)}", M[i - 1][j - 1] + s(x, y)),
               (f"{x} con -:  {M[i-1][j]} + {s(x, '-')}", M[i - 1][j] + s(x, "-")),
               (f"- con {y}:  {M[i][j-1]} + {s('-', y)}", M[i][j - 1] + s("-", y))]
        panel(f, 560, 150, 690, 240, f"última columna de {a[:i]} y {b[:j]}",
              [(f"{t} = {v}", "green" if v == M[i][j] else "text") for t, v in ops])
    if f.t >= f.c(5):
        texto(f, (900, 520), f"mejor(6, 4) = {M[n][m]}", 38, "green", aparece(f, f.c(5)), mono=True, anchor="mm")


ESC = [
    Escena("Alineamiento de secuencias. La mejor forma de poner en columnas dos cadenas de material genético.",
           e_portada("12-6", "Alineamiento de secuencias", dib), titulo="Portada", extra=1.0),
    Escena("Queremos comparar dos secuencias de bases. "
           "Las colocamos en columnas, manteniendo el orden, y rellenando los huecos con guiones. "
           "Cada columna puntúa según una matriz de sustitución. "
           "Una columna no puede tener dos guiones. "
           "Buscamos la puntuación máxima.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Miremos la última columna del alineamiento. Solo hay tres posibilidades. "
           "Mejor de i, j es la puntuación máxima con las i primeras letras de una cadena y las jota primeras de la otra. "
           "Se emparejan las dos últimas letras. "
           "O la de la primera cadena va con un hueco. "
           "O el hueco va con la de la segunda. "
           "Con una cadena vacía, todo son huecos: no vale cero.",
           e_lineas([(2, 80, "mejor(i, j) = máximo alineando a[1..i] con b[1..j]", "gold", 30),
                     (3, 210, "mejor(i−1, j−1) + S[a_i, b_j]", "text", 32, True),
                     (4, 290, "mejor(i−1, j)   + S[a_i, - ]", "text", 32, True),
                     (5, 370, "mejor(i, j−1)   + S[ - , b_j]", "text", 32, True),
                     (6, 480, "casos base: mejor(0, 0) = 0 y sumas de huecos", "muted", 28),
                     (7, 560, "respuesta: mejor(n, m)", "green", 30)]), titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla con el segundo ejemplo del enunciado. "
           "Primero la fila y la columna de la cadena vacía, que acumulan huecos. "
           "Después cada casilla mira tres vecinas: la diagonal, la de arriba y la de la izquierda. "
           "Sumamos la puntuación de la columna nueva. "
           "Y nos quedamos con la mayor. "
           "La esquina da el resultado: dos.",
           e_tabla, titulo="La tabla", extra=3.0),
    Escena("La tabla puede tener un millón de casillas, pero solo hace falta la fila anterior. "
           "Guardamos una sola fila, y antes de pisar una casilla apuntamos su valor: será la diagonal de la siguiente.",
           e_lineas([(0, 150, "memoria: de O(n · m) a O(m)", "gold", 36),
                     (1, 290, "arriba   = mejor[j]        (aún es la fila i−1)", "text", 28, True),
                     (1, 350, "izquierda = mejor[j−1]     (ya es la fila i)  ", "text", 28, True),
                     (1, 410, "diagonal = el «arriba» anterior              ", "text", 28, True)]), titulo="Una sola fila", extra=2.0),
    Escena("En el código, la primera fila acumula los huecos de la segunda cadena. "
           "Para cada letra de la primera, guardamos la diagonal y actualizamos la columna cero. "
           "Cada casilla es el máximo de las tres opciones, y después la diagonal pasa a ser lo que había arriba. "
           "La última casilla es la respuesta.",
           e_codigo(CPP, "vector<int> mejor(m + 1, 0);", "cout << mejor[m]",
                    [["mejor[j] = mejor[j - 1] + S[HUECO]"], ["int diagonal = mejor[0];", "mejor[0] += S[x][HUECO];"],
                     ["mejor[j] = max({", "diagonal = arriba;"], ["cout << mejor[m]"]],
                    [("fila 0", "huecos acumulados"), ("diagonal", "mejor(i−1, j−1)"),
                     ("tres opciones", "el máximo"), ("respuesta", "puede ser negativa")], maxc=100, size=14),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: miramos la última columna, que tiene tres opciones. "
           "Los casos base son huecos acumulados. "
           "La matriz puede no ser simétrica, así que importa el orden. "
           "Y basta una fila de memoria.",
           e_cierre("Alineamiento de secuencias", [
               "tres opciones para la última columna",
               "casos base: huecos acumulados, no ceros",
               "S[letra de a][letra de b]: el orden importa",
               "O(n · m) en tiempo, O(m) en memoria"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-6", "../12-6_alineamiento_de_secuencias.mp4")
