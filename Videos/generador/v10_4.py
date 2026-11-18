"""Vídeo EJ 10-4 · ¿Por dónde hay que subir? (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../10-Programacion dinamica/EJ_10-4/EJ_10-4.cpp"
TEMA = "Tema 10 · Programación dinámica"
T = [[2, 5, 8, 3], [1, 4, 2, 9], [9, 2, 8, 5], [3, 5, 2, 1]]
N = 4
VOR = [(3, 1), (2, 0), (1, 1), (0, 2)]          # camino voraz (fila, col) en índices 0
OPT = [(3, 1), (2, 2), (1, 3), (0, 2)]          # camino óptimo


def calcula(T):
    n = len(T)
    m = [row[:] for row in T]
    for i in range(1, n):
        for j in range(n):
            m[i][j] = T[i][j] + max(m[i - 1][k] for k in (j - 1, j, j + 1) if 0 <= k < n)
    return m


M = calcula(T)
ORDEN = [(i, j) for i in range(1, N) for j in range(N)]
ETQ = ["fila 1", "fila 2", "fila 3", "fila 4"]
CAB = ["col 1", "col 2", "col 3", "col 4"]
TB = Tabla(40, 150, N, N, cw=110, ch=96, lw=110, cabecera=CAB, etiquetas=ETQ, tam=34)   # tablero
TM = Tabla(660, 150, N, N, cw=110, ch=96, lw=30, cabecera=CAB, etiquetas=[""] * 4, tam=34)  # mejor


def ficha(f, tabla, i, j, u=1.0, col=None):
    x, y = tabla.centro(i, j)
    c = col or C["gold"]
    r = 34
    f.d.ellipse((x - r, y - r, x + r, y + r), outline=mix(C["panel"], c, u), width=6)


def recorrido(f, tabla, path, u, col, w=7):
    pts = [tabla.centro(i, j) for i, j in path]
    n = len(pts) - 1
    k = u * n
    for s in range(min(int(k), n)):
        flecha(f, pts[s], pts[s + 1], col, w=w, cab=16)
    if int(k) < n:
        a, b = pts[int(k)], pts[int(k) + 1]
        t = k - int(k)
        if t > 0.05:
            f.d.line((a, (lerp(a[0], b[0], t), lerp(a[1], b[1], t))), fill=col, width=w)


def tablero(f, u=1.0, sombra=None, marca=None):
    TB.dibuja(f, {(i, j): T[i][j] for i in range(N) for j in range(N)}, u=u, sombra=sombra, marca=marca)


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        tb = Tabla(830, 160, 4, 4, cw=86, ch=76, lw=0, cabecera=[""] * 4, etiquetas=[""] * 4, tam=28)
        tb.dibuja(f, {(i, j): T[i][j] for i in range(4) for j in range(4)}, u=f.p(0.2, 0.8))
        recorrido(f, tb, OPT, f.lin(1.2, 2.4), C["gold"])
    portada(f, "EJ 10-4", "¿Por dónde hay que subir?", TEMA, dib)


def e_problema(f):
    tablero(f, u=f.p(f.c(0), 0.8))
    if f.t >= f.c(1):
        # los tres movimientos desde (3,1)
        u = aparece(f, f.c(1))
        ficha(f, TB, 3, 1, u)
        a = TB.centro(3, 1)
        for dj in (-1, 0, 1):
            b = TB.centro(2, 1 + dj)
            flecha(f, (a[0] + dj * 10, a[1] - 34), (lerp(a[0], b[0], 0.75), lerp(a[1], b[1], 0.75)), mix(C["bot"], C["blue"], u), w=6, cab=16)
    if f.t >= f.c(2):
        recorrido(f, TB, OPT, f.lin(f.c(2) + 0.3, 2.4), C["gold"])
        s = sum(T[i][j] for k, (i, j) in enumerate(OPT) if f.lin(f.c(2) + 0.3, 2.4) * 3 >= k)
        texto(f, (1000, 300), "suma", 26, "muted", aparece(f, f.c(2)), anchor="mm")
        texto(f, (1000, 360), str(s), 60, "gold", aparece(f, f.c(2)), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (1000, 470), "¿máximo?  ¿desde qué columna?", 26, "text", aparece(f, f.c(3)), anchor="mm")


def e_voraz(f):
    tablero(f)
    u1 = f.lin(f.c(0) + 0.6, 2.6)
    recorrido(f, TB, VOR, u1, C["red"])
    s1 = sum(T[i][j] for k, (i, j) in enumerate(VOR) if u1 * 3 >= k)
    texto(f, (950, 250), "lo más grande encima", 26, "red", aparece(f, f.c(0)))
    texto(f, (950, 290), f"{s1}", 48, "red", aparece(f, f.c(0) + 0.6))
    if f.t >= f.c(2):
        u2 = f.lin(f.c(2) + 0.3, 2.6)
        recorrido(f, TB, OPT, u2, C["green"])
        s2 = sum(T[i][j] for k, (i, j) in enumerate(OPT) if u2 * 3 >= k)
        texto(f, (950, 420), "mejor", 26, "green", aparece(f, f.c(2)))
        texto(f, (950, 460), f"{s2}", 48, "green", aparece(f, f.c(2) + 0.3))


def e_idea(f):
    vals = {(0, j): M[0][j] for j in range(N)}
    marca, sombra = {}, {}
    if f.t >= f.c(1):
        vals[(1, 3)] = "?"
        marca[(1, 3)] = "gold"
        sombra = {(0, 2): AZUL, (0, 3): AZUL}
    if f.t >= f.c(2) + 1.5:
        vals[(1, 3)] = M[1][3]
    tablero(f)
    TM.dibuja(f, vals, u=aparece(f, f.c(0), 0.8), marca=marca, sombra=sombra)
    texto(f, (1100, 120), "mejor", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        for k in (2, 3):
            TM.flecha_entre(f, (0, k), (1, 3), AZUL, u=f.lin(f.c(1) + 0.3, 0.6))
    if f.t >= f.c(2):
        texto(f, (980, 600), "9 + max(8, 3) = 17", 34, "gold", aparece(f, f.c(2)), mono=True, anchor="mm")


def e_recurrencia(f):
    texto(f, (70, 90), "mejor(i, j) = máxima suma subiendo desde (i, j) hasta la fila 1", 24, "muted", aparece(f, f.c(0)), bold=False)
    texto(f, (70, 160), "Caso base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 90, 205, "mejor(1, j) =", [("t(1, j)", "1 ≤ j ≤ N")], aparece(f, f.c(1)))
    texto(f, (70, y + 30), "Recurrencia  (2 ≤ i ≤ N)", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 90, y + 76, "mejor(i, j) =", [("t(i, j) + max( mejor(i−1, k) )", "k ∈ {j−1, j, j+1},  1 ≤ k ≤ N")], aparece(f, f.c(2)))
    texto(f, (70, y + 40), "Respuesta", 26, "gold", aparece(f, f.c(3)))
    y = formula(f, 90, y + 86, "suma =", [("max_j mejor(N, j)", "")], aparece(f, f.c(3)))
    formula(f, 90, y + 6, "columna =", [("la menor j con mejor(N, j) = suma", "")], aparece(f, f.c(3) + 1.5))


def e_rellenar(f):
    t0, t1 = f.c(0) + 0.4, f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    k = int((f.t - t0) / paso) if f.t >= t0 else 0
    k = max(0, min(k, len(ORDEN)))
    vals = {(0, j): M[0][j] for j in range(N)}
    for (i, j) in ORDEN[:k]:
        vals[(i, j)] = M[i][j]
    marca, sombra = {}, {}
    cur = ORDEN[k] if k < len(ORDEN) and f.t >= t0 else None
    if cur:
        i, j = cur
        marca[cur] = "gold"
        for kk in (j - 1, j, j + 1):
            if 0 <= kk < N:
                sombra[(i - 1, kk)] = AZUL
    tablero(f, sombra={cur: NARANJA} if cur else None)
    TM.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (1100, 120), "mejor", 26, "gold", 1, anchor="mm")
    if cur:
        i, j = cur
        u = ((f.t - t0) % paso) / paso
        for kk in (j - 1, j, j + 1):
            if 0 <= kk < N:
                TM.flecha_entre(f, (i - 1, kk), cur, AZUL, u=min(1, u * 2.5))
    if f.t >= f.c(3):
        best = max(M[N - 1])
        col = M[N - 1].index(best)
        TM.dibuja(f, vals, marca={(N - 1, col): "green"})
        texto(f, (960, 640), f"{best}  en la columna {col + 1}", 34, "green", aparece(f, f.c(3)), anchor="mm")


def e_camino(f):
    vals = {(i, j): M[i][j] for i in range(N) for j in range(N)}
    tablero(f)
    TM.dibuja(f, vals)
    u = f.lin(f.c(1), 3.0)
    recorrido(f, TM, OPT, u, C["green"])
    recorrido(f, TB, OPT, u, C["green"])
    if f.t >= f.c(2):
        texto(f, (640, 640), "5 + 8 + 9 + 8 = 30", 34, "green", aparece(f, f.c(2)), mono=True, anchor="mm")


def e_empate(f):
    t1 = [[1] * 3 for _ in range(3)]
    m1 = calcula(t1)
    tb = Tabla(80, 170, 3, 3, cw=110, ch=96, lw=0, cabecera=["col 1", "col 2", "col 3"], etiquetas=[""] * 3, tam=34)
    tm = Tabla(560, 170, 3, 3, cw=110, ch=96, lw=0, cabecera=["col 1", "col 2", "col 3"], etiquetas=[""] * 3, tam=34)
    tb.dibuja(f, {(i, j): 1 for i in range(3) for j in range(3)})
    u = aparece(f, f.c(0) + 0.5, 1.0)
    vm = {(i, j): m1[i][j] for i in range(3) for j in range(3)}
    tm.dibuja(f, vm, u=u)
    if f.t >= f.c(1):
        tm.dibuja(f, vm, marca={(2, j): "gold" for j in range(3)})
        texto(f, (1060, 300), "3  3  3", 36, "gold", aparece(f, f.c(1)), mono=True, anchor="mm")
    if f.t >= f.c(2):
        tm.dibuja(f, vm, marca={(2, 0): "green"})
        texto(f, (1060, 380), "columna 1", 34, "green", aparece(f, f.c(2)), anchor="mm")
        texto(f, (1060, 300), "mejor[j] > mejor[col]", 22, "text", aparece(f, f.c(2) + 1), mono=True, anchor="mm")


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "cout << anterior[col]")
CODE = codigo(CPP, A, B + 1, maxc=80)
L_F1 = find_line(CPP, "for (int j = 0; j < N; ++j) cin >> anterior[j];")
L_ARR = find_line(CPP, "int mejorArriba = anterior[j];")
L_IZ = find_line(CPP, "if (j > 0) mejorArriba")
L_DE = find_line(CPP, "if (j + 1 < N) mejorArriba")
L_ACT = find_line(CPP, "actual[j] = t + mejorArriba;")
L_SWAP = find_line(CPP, "swap(anterior, actual);")
L_MAX = find_line(CPP, "if (anterior[j] > anterior[col]) col = j;")


def e_codigo(f):
    t0, t1 = f.c(1), f.c(3)
    paso = (t1 - t0) / len(ORDEN)
    k = int((f.t - t0) / paso) if f.t >= t0 else -1
    k = min(k, len(ORDEN))
    hl = {L_F1}
    ant, act = M[0][:], [None] * N
    cur = None
    if 0 <= k < len(ORDEN):
        i, j = ORDEN[k]
        cur = (i, j)
        ant = M[i - 1][:]
        act = [M[i][jj] if jj < j else None for jj in range(N)]
        u = ((f.t - t0) % paso) / paso
        hl = {L_ARR, L_IZ, L_DE} if u < 0.6 else {L_ACT}
        if j == N - 1 and u > 0.85:
            hl = {L_SWAP}
    elif k >= len(ORDEN):
        ant, act = M[N - 1][:], [None] * N
        hl = {L_MAX}
    f.code(16, 84, 770, 540, CODE, hl=hl, title="resuelveCaso()", size=15)
    x0 = 830
    for r, (nom, vec) in enumerate((("anterior", ant), ("actual", act))):
        y = 200 + r * 170
        texto(f, (x0, y - 40), nom, 24, "muted", 1, mono=True)
        for jj in range(N):
            x = x0 + jj * 102
            hl_c = cur is not None and ((r == 1 and jj == cur[1]) or (r == 0 and abs(jj - cur[1]) <= 1))
            colb = (C["gold"] if r == 1 else AZUL) if hl_c else C["border"]
            f.d.rectangle((x, y, x + 90, y + 80), fill=C["panel"], outline=colb, width=4 if hl_c else 2)
            if vec[jj] is not None:
                f.d.text((x + 45, y + 40), str(vec[jj]), font=font(32, True), fill=C["text"], anchor="mm")
    if cur:
        texto(f, (x0, 520), f"fila {cur[0] + 1}, columna {cur[1] + 1}", 26, "gold", 1)
    if k >= len(ORDEN):
        texto(f, (x0, 520), "30 2", 40, "green", aparece(f, t1), mono=True)


def e_cierre(f):
    cierre(f, "¿Por dónde hay que subir?", [
        "lo más grande de encima no sirve: hay que mirar la tabla",
        "mejor(i, j) = t(i, j) + máx de las 3 casillas de encima",
        "respuesta: máximo de la última fila, el de más a la izquierda",
        "dos filas basta:  O(N²) tiempo, O(N) memoria",
    ])


ESC = [
    Escena("¿Por dónde hay que subir? Un tablero de números, y hay que encontrar el camino hacia arriba que más suma.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos un tablero de ene por ene con un número en cada casilla. "
           "Se empieza en una casilla de la última fila y en cada paso se sube a una de las tres casillas de encima: la de arriba o una de las dos diagonales. "
           "Al llegar a la primera fila, ganamos la suma de todas las casillas por las que hemos pasado. "
           "Queremos la suma máxima, y la columna por la que hay que empezar.",
           e_problema, titulo="El problema", extra=1.2),
    Escena("¿Y si subimos siempre a la casilla más grande de las de encima? "
           "Desde el 5, la mayor es el 9, después el 4 y después el 8: veintiséis. "
           "Pero subiendo por el 8, el 9 y el 8 se llega a treinta. Elegir lo mejor en cada paso no sirve: hay que mirar más lejos.",
           e_voraz, titulo="Lo más grande no sirve", extra=1.5),
    Escena("La clave es pensar desde arriba. Llamamos mejor de i, jota a la máxima suma que se consigue empezando en esa casilla y subiendo hasta la primera fila. "
           "En la primera fila ya hemos llegado: mejor es el propio número. "
           "Para cualquier otra casilla, es su número más la mejor de las casillas de encima. Para este 9: nueve más el máximo entre 8 y 3, diecisiete.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Así queda escrito. "
           "Caso base: en la fila uno, mejor es el propio valor de la casilla. "
           "Recurrencia: el valor de la casilla más el máximo de mejor en las tres casillas de encima que existan. "
           "La respuesta es el máximo de la última fila, y si hay empate, la columna más pequeña.",
           e_recurrencia, titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla fila a fila, de arriba abajo, porque cada fila necesita la de encima. "
           "Cada casilla mira sus tres vecinas de la fila anterior y se queda con la mayor. "
           "En los bordes solo hay dos. "
           "En la última fila está la respuesta: treinta, empezando por la columna dos.",
           e_rellenar, titulo="Rellenar la tabla", extra=2.5),
    Escena("El problema no pide el camino, pero la tabla lo dice: "
           "desde el treinta se sube siempre a la casilla de encima con mayor valor en la tabla. "
           "Cinco, ocho, nueve y ocho: treinta.",
           e_camino, titulo="El camino", extra=1.5),
    Escena("En el segundo ejemplo todas las casillas valen uno. "
           "Cualquier recorrido suma tres, y las tres columnas empatan. "
           "Se pide la de más a la izquierda, así que al buscar el máximo solo se cambia de columna si el valor es estrictamente mayor.",
           e_empate, titulo="Empates", extra=1.5),
    Escena("En el código no hace falta la tabla entera: basta con dos filas, la anterior y la actual. "
           "Se lee la primera fila en anterior. Para cada fila siguiente, cada casilla mira las tres de anterior que existen, y guarda en actual su valor más la mayor. "
           "Al acabar la fila, se intercambian con swap, que no copia nada. "
           "Al final, anterior es la última fila, y se busca su máximo con mayor estricto.",
           e_codigo, titulo="El código", extra=3.0),
    Escena("Resumiendo: elegir lo más grande de encima no sirve. "
           "Cada casilla guarda su valor más el máximo de las tres de encima. "
           "La respuesta es el máximo de la última fila, el de más a la izquierda. "
           "Con dos filas, ene al cuadrado en tiempo y ene en memoria.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/10-4", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-4: {build(ESC, '../10-4_por_donde_hay_que_subir.mp4'):.0f}s")
