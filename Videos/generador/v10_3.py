"""Vídeo EJ 10-3 · Esquivando las obras en los cruces (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre

CPP = "../../10-Programacion dinamica/EJ_10-3/EJ_10-3.cpp"
TEMA = "Tema 10 · Programación dinámica"
G1 = [".....", ".X...", "..X.X", "....."]
G2 = [".X...", "...X.", "XXX.."]
CAM = [(255, 206, 92), (112, 222, 152), (196, 150, 255), (240, 160, 70)]


def tabla(g):
    N, M = len(g), len(g[0])
    c = [[0] * M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            if g[i][j] == "X":
                c[i][j] = 0
            elif i == 0 and j == 0:
                c[i][j] = 1
            else:
                c[i][j] = (c[i - 1][j] if i else 0) + (c[i][j - 1] if j else 0)
    return c


T1, T2 = tabla(G1), tabla(G2)


def caminos_lista(g):
    N, M = len(g), len(g[0])
    res = []

    def go(i, j, path):
        if g[i][j] == "X":
            return
        if (i, j) == (N - 1, M - 1):
            res.append(path)
            return
        if i + 1 < N:
            go(i + 1, j, path + "S")
        if j + 1 < M:
            go(i, j + 1, path + "E")
    go(0, 0, "")
    return res


PATHS = caminos_lista(G1)


# ------------------------------------------------------------------ dibujo de la ciudad
class Ciudad:
    def __init__(self, g, x0, y0, paso):
        self.g, self.x0, self.y0, self.paso = g, x0, y0, paso
        self.N, self.M = len(g), len(g[0])

    def pos(self, i, j):
        return self.x0 + j * self.paso, self.y0 + i * self.paso

    def dibuja(self, f, u=1.0, vals=None, actual=None, persona=True, estacion=True, conos=True):
        d = f.d
        P = self.paso
        # manzanas
        for i in range(self.N - 1):
            for j in range(self.M - 1):
                x, y = self.pos(i, j)
                d.rounded_rectangle((x + 12, y + 12, x + P - 12, y + P - 12), 10, fill=mix(C["bot"], (44, 62, 92), u))
        # calles
        for i in range(self.N):
            a, b = self.pos(i, 0), self.pos(i, self.M - 1)
            d.line((a, b), fill=mix(C["bot"], (120, 132, 156), u), width=6)
        for j in range(self.M):
            a, b = self.pos(0, j), self.pos(self.N - 1, j)
            d.line((a, b), fill=mix(C["bot"], (120, 132, 156), u), width=6)
        for i in range(self.N):
            for j in range(self.M):
                x, y = self.pos(i, j)
                if self.g[i][j] == "X" and conos:
                    cono(f, x, y, u)
                elif vals is not None and (i, j) in vals:
                    v = vals[(i, j)]
                    r = 22
                    col = C["gold"] if (i, j) == actual else (C["panel"])
                    d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], col, u), outline=mix(C["bot"], C["gold"], u), width=2)
                    d.text((x, y), str(v), font=font(22, True), fill=C["node_t"] if (i, j) == actual else C["text"], anchor="mm")
                else:
                    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=mix(C["bot"], (200, 208, 222), u))
        if persona:
            x, y = self.pos(0, 0)
            muñeco(f, x - 44, y - 30, u)
        if estacion:
            x, y = self.pos(self.N - 1, self.M - 1)
            tren(f, x + 30, y + 10, u)

    def camino(self, f, path, col, u=1.0, w=8, off=0):
        x, y = self.pos(0, 0)
        pts = [(x + off, y + off)]
        i = j = 0
        for s in path:
            if s == "S":
                i += 1
            else:
                j += 1
            x, y = self.pos(i, j)
            pts.append((x + off, y + off))
        n = len(pts) - 1
        k = u * n
        for s in range(int(k)):
            f.d.line((pts[s], pts[s + 1]), fill=col, width=w)
        if int(k) < n:
            a, b = pts[int(k)], pts[int(k) + 1]
            t = k - int(k)
            f.d.line((a, (lerp(a[0], b[0], t), lerp(a[1], b[1], t))), fill=col, width=w)


def cono(f, x, y, u=1.0):
    c1 = mix(C["bot"], (255, 140, 40), u)
    f.d.polygon([(x, y - 24), (x - 17, y + 16), (x + 17, y + 16)], fill=c1)
    f.d.line((x - 10, y, x + 10, y), fill=mix(C["bot"], (255, 255, 255), u), width=4)
    f.d.rectangle((x - 22, y + 14, x + 22, y + 20), fill=mix(C["bot"], (200, 100, 30), u))


def muñeco(f, x, y, u=1.0):
    c = mix(C["bot"], C["blue"], u)
    f.d.ellipse((x - 9, y - 30, x + 9, y - 12), fill=c)
    f.d.line((x, y - 12, x, y + 10), fill=c, width=5)
    f.d.line((x - 10, y - 4, x + 10, y - 4), fill=c, width=4)
    f.d.line((x, y + 10, x - 8, y + 26), fill=c, width=4)
    f.d.line((x, y + 10, x + 8, y + 26), fill=c, width=4)


def tren(f, x, y, u=1.0):
    c = mix(C["bot"], C["red"], u)
    f.d.rounded_rectangle((x - 4, y - 26, x + 52, y + 4), 8, fill=c)
    f.d.rectangle((x + 6, y - 20, x + 20, y - 8), fill=mix(C["bot"], (220, 235, 255), u))
    f.d.rectangle((x + 28, y - 20, x + 42, y - 8), fill=mix(C["bot"], (220, 235, 255), u))
    for xx in (x + 8, x + 40):
        f.d.ellipse((xx - 6, y, xx + 6, y + 12), fill=mix(C["bot"], (40, 40, 50), u))


CI = Ciudad(G1, 300, 170, 150)


def valores_hasta(T, g, k):
    N, M = len(g), len(g[0])
    vals = {}
    for n in range(min(k, N * M)):
        i, j = divmod(n, M)
        if g[i][j] != "X":
            vals[(i, j)] = T[i][j]
    return vals


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        c = Ciudad(["....", ".X..", "...."], 880, 230, 120)
        c.dibuja(f, u=f.p(0.2, 0.8))
        c.camino(f, "EESSE", C["gold"], u=f.lin(1.2, 2.5), w=7)
    portada(f, "EJ 10-3", "Esquivando las obras", TEMA, dib)


def e_problema(f):
    CI.dibuja(f, u=f.p(f.c(0), 0.8), conos=f.t >= f.c(1), persona=f.t >= f.c(1) - 0.1, estacion=f.t >= f.c(1) - 0.1)
    if f.t >= f.c(2):
        texto(f, (W / 2, 660), "¿cuántos caminos?", 34, "gold", aparece(f, f.c(2)), anchor="mm")


def e_sur_este(f):
    CI.dibuja(f)
    u = f.lin(f.c(0) + 0.4, 2.4)
    CI.camino(f, "SSSEEEE", C["green"], u=u)
    if f.t >= f.c(1):
        v = aparece(f, f.c(1))
        texto(f, (1060, 250), "↓ S × 3", 30, "green", v)
        texto(f, (1060, 300), "→ E × 4", 30, "green", v)
    if f.t >= f.c(2):
        # un rodeo hacia el norte
        CI.camino(f, "EESN", C["red"], u=f.lin(f.c(2) + 0.2, 1.6), w=6, off=10)
        texto(f, (1060, 420), "↑ más largo", 30, "red", aparece(f, f.c(2) + 1.6))


def e_idea(f):
    vals = {}
    CI.dibuja(f, vals={(1, 3): "?", (0, 3): T1[0][3], (1, 2): T1[1][2]} if f.t >= f.c(1) else {(1, 3): "?"}, actual=(1, 3))
    a = CI.pos(0, 3)
    b = CI.pos(1, 3)
    c = CI.pos(1, 2)
    if f.t >= f.c(0):
        u = f.lin(f.c(0) + 0.3, 0.8)
        flecha(f, (a[0], a[1] + 26), (a[0], lerp(a[1] + 26, b[1] - 26, ease(u))), AZUL, w=6, cab=16)
        flecha(f, (c[0] + 26, c[1]), (lerp(c[0] + 26, b[0] - 26, ease(u)), c[1]), NARANJA, w=6, cab=16)
    if f.t >= f.c(1) + 1.5:
        texto(f, (1060, 220), "1 + 1 = 2", 34, "gold", aparece(f, f.c(1) + 1.5), mono=True)
    if f.t >= f.c(2):
        x, y = CI.pos(2, 2)
        f.d.ellipse((x - 34, y - 34, x + 34, y + 34), outline=C["red"], width=4)
        texto(f, (1060, 420), "obras → 0", 34, "red", aparece(f, f.c(2)))


def e_recurrencia(f):
    texto(f, (70, 90), "caminos(i, j) = nº de caminos mínimos de (0, 0) a (i, j) sin pasar por obras", 24, "muted",
          aparece(f, f.c(0)), bold=False)
    texto(f, (70, 170), "Casos base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 90, 215, "caminos(0, 0) =", [("1", "")], aparece(f, f.c(1)))
    y = formula(f, 90, y + 4, "caminos(i, j) =", [("0", "si i < 0 o j < 0  (fuera)")], aparece(f, f.c(1) + 1.2))
    texto(f, (70, y + 40), "Recurrencia", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 90, y + 90, "caminos(i, j) =", [("0", "si (i, j) tiene obras"),
                                                   ("caminos(i−1, j) + caminos(i, j−1)", "si no")],
                aparece(f, f.c(2)), colores=[C["red"], C["text"]])
    texto(f, (70, y + 50), "Respuesta:  caminos(N−1, M−1)", 28, "green", aparece(f, f.c(3)), mono=True)


def e_ola(f):
    t0, t1 = f.c(0) + 0.6, f.T - 2.5
    total = CI.N * CI.M
    k = int((f.t - t0) / ((t1 - t0) / total)) if f.t >= t0 else 0
    k = max(0, min(total, k))
    vals = valores_hasta(T1, G1, k)
    act = divmod(k, CI.M) if k < total else None
    if act and G1[act[0]][act[1]] == "X":
        act = None
    CI.dibuja(f, vals=vals, actual=act)
    if act:
        i, j = act
        b = CI.pos(i, j)
        if i > 0 and G1[i - 1][j] != "X":
            a = CI.pos(i - 1, j)
            flecha(f, (a[0], a[1] + 24), (b[0], b[1] - 24), AZUL, w=5)
        if j > 0 and G1[i][j - 1] != "X":
            c = CI.pos(i, j - 1)
            flecha(f, (c[0] + 24, c[1]), (b[0] - 24, b[1]), NARANJA, w=5)
    if k >= total:
        x, y = CI.pos(CI.N - 1, CI.M - 1)
        f.d.ellipse((x - 32, y - 32, x + 32, y + 32), outline=C["green"], width=5)


def e_cuatro(f):
    vals = {(i, j): T1[i][j] for i in range(4) for j in range(5) if G1[i][j] != "X"}
    CI.dibuja(f, vals=vals)
    offs = [-12, -4, 4, 12]
    for k, p in enumerate(PATHS):
        t0 = f.c(min(k + 1, 4)) if k < 3 else f.c(4)
        t0 = f.c(0) + 0.8 + k * ((f.T - f.c(0) - 3) / 4)
        if f.t >= t0:
            CI.camino(f, p, CAM[k], u=f.lin(t0, 1.8), w=6, off=offs[k])
            texto(f, (1080, 200 + 60 * k), p, 28, CAM[k], aparece(f, t0 + 1.8), mono=True)


CI2 = Ciudad(G2, 300, 200, 150)


def e_ejemplo2(f):
    t0, t1 = f.c(1), f.c(3)
    total = CI2.N * CI2.M
    k = int((f.t - t0) / ((t1 - t0) / total)) if f.t >= t0 else 0
    k = max(0, min(total, k))
    vals = valores_hasta(T2, G2, k)
    CI2.dibuja(f, vals=vals, actual=divmod(k, CI2.M) if k < total and G2[k // CI2.M][k % CI2.M] != "X" else None)
    if f.t >= f.c(2) and f.t < f.c(3) + 99:
        CI2.camino(f, "SEESEEN"[:0], C["red"], 0)
    if f.t >= f.c(3):
        x, y = CI2.pos(CI2.N - 1, CI2.M - 1)
        f.d.ellipse((x - 32, y - 32, x + 32, y + 32), outline=C["red"], width=5)
        texto(f, (W / 2, 660), "0 caminos", 34, "red", aparece(f, f.c(3)), anchor="mm")


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "cout << caminos[N - 1][M - 1]")
CODE = codigo(CPP, A, B + 1)
L_INI = find_line(CPP, "caminos[0][0] = 1;")
L_X = find_line(CPP, "if (mapa[i][j] == 'X') caminos[i][j] = 0;")
L_SUMA = find_line(CPP, "if (j > 0) caminos[i][j] += caminos[i][j - 1];")
L_OUT = B


def e_codigo(f):
    f.code(20, 84, 720, 470, CODE, hl={L_INI}, title="resuelveCaso()", size=19)
    t0, t1 = f.c(1), f.T - 2.0
    total = 4 * 5
    k = int((f.t - t0) / ((t1 - t0) / total)) if f.t >= t0 else -1
    k = min(k, total)
    # vector caminos[j] tras procesar k casillas (por filas)
    vec = [1, 0, 0, 0, 0]
    fila_act = 0
    for n in range(max(0, k)):
        i, j = divmod(n, 5)
        fila_act = i
        if G1[i][j] == "X":
            vec[j] = 0
        elif j > 0:
            vec[j] += vec[j - 1]
    hl = {L_INI}
    cur = None
    if 0 <= k < total:
        i, j = divmod(k, 5)
        cur = (i, j)
        hl = {L_X} if G1[i][j] == "X" else ({L_SUMA} if j > 0 else {L_X})
    elif k >= total:
        hl = {L_OUT}
    f.code(20, 84, 720, 470, CODE, hl=hl, title="resuelveCaso()", size=19)
    # mini ciudad
    mc = Ciudad(G1, 820, 130, 70)
    mc.dibuja(f, persona=False, estacion=False)
    if cur:
        x, y = mc.pos(*cur)
        f.d.ellipse((x - 14, y - 14, x + 14, y + 14), outline=C["gold"], width=4)
    # vector
    x0, y0 = 830, 470
    texto(f, (x0, y0 - 34), "caminos[j]", 22, "muted", 1, mono=True)
    for j in range(5):
        x = x0 + j * 80
        hl_c = cur and cur[1] == j
        f.d.rectangle((x, y0, x + 70, y0 + 60), fill=C["panel"], outline=C["gold"] if hl_c else C["border"], width=4 if hl_c else 2)
        f.d.text((x + 35, y0 + 30), str(vec[j]), font=font(28, True), fill=C["text"], anchor="mm")
        f.d.text((x + 35, y0 + 78), str(j), font=font(18, True), fill=C["dim"], anchor="mm")
    if cur and cur[1] > 0 and G1[cur[0]][cur[1]] != "X":
        a = (x0 + (cur[1] - 1) * 80 + 35, y0 - 6)
        b = (x0 + cur[1] * 80 + 35, y0 - 6)
        flecha(f, (a[0] + 10, a[1]), (b[0] - 10, b[1]), NARANJA, w=4)


def e_detalles(f):
    f.box(40, 110, 580, 360, "solo un vector")
    f.box(660, 110, 580, 360, "coste")
    if f.t >= f.c(0):
        u = aparece(f, f.c(0))
        texto(f, (330, 230), "arriba = caminos[j]", 28, "blue", u, mono=True, anchor="mm", fondo=C["panel"])
        texto(f, (330, 290), "izquierda = caminos[j−1]", 28, NARANJA, u, mono=True, anchor="mm", fondo=C["panel"])
        texto(f, (330, 380), "O(M) memoria", 30, "gold", aparece(f, f.c(0) + 2), anchor="mm", fondo=C["panel"])
    if f.t >= f.c(1):
        texto(f, (950, 260), "O(N · M)", 54, "gold", aparece(f, f.c(1)), anchor="mm", fondo=C["panel"])
        texto(f, (950, 340), "≤ 50 × 50 cruces", 26, "muted", aparece(f, f.c(1) + 0.5), anchor="mm", fondo=C["panel"])
    if f.t >= f.c(2):
        texto(f, (W / 2, 560), "resultado < 10⁹  →  cabe en int", 30, "text", aparece(f, f.c(2)), anchor="mm")


def e_cierre(f):
    cierre(f, "Esquivando las obras en los cruces", [
        "camino mínimo = solo sur y este",
        "caminos(i, j) = arriba + izquierda;  obras → 0",
        "caminos(0, 0) = 1;  respuesta en (N−1, M−1)",
        "un vector por filas:  O(N·M) tiempo, O(M) memoria",
    ])


ESC = [
    Escena("Esquivando las obras en los cruces. Un problema clásico de programación dinámica: contar caminos en una cuadrícula.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Cuadracity es una ciudad de calles en cuadrícula. "
           "Estás en la esquina noroeste, quieres llegar a la estación de tren, en la esquina sureste, y hay obras en algunos cruces. "
           "¿De cuántas formas puedes llegar sin caminar más de lo imprescindible y sin pasar por ninguna obra?",
           e_problema, titulo="El problema", extra=1.2),
    Escena("No caminar de más significa no retroceder nunca: solo se baja hacia el sur o se avanza hacia el este. "
           "En esta ciudad son tres manzanas hacia el sur y cuatro hacia el este, en cualquier orden. "
           "Un solo paso hacia el norte o hacia el oeste ya alarga el camino, y ese no cuenta.",
           e_sur_este, titulo="Solo sur y este", extra=1.2),
    Escena("Por eso, a un cruce solo se puede llegar desde el de arriba o desde el de la izquierda. "
           "Los caminos que llegan a él son los que llegan al de arriba más los que llegan al de la izquierda: aquí, uno más uno, dos. "
           "Y si el cruce tiene obras, no puede llegar ningún camino: vale cero.",
           e_idea, titulo="La idea", extra=1.2),
    Escena("Así queda escrito, como se pide en el examen. "
           "Casos base: a la esquina de salida se llega de una forma, y fuera de la ciudad, de ninguna. "
           "Recurrencia: cero si el cruce tiene obras, y si no, la suma del de arriba y el de la izquierda. "
           "La respuesta es el valor de la estación, en la esquina ene menos uno, eme menos uno.",
           e_recurrencia, titulo="Recurrencia", extra=1.5),
    Escena("Ahora rellenamos la ciudad fila a fila, de izquierda a derecha. "
           "En la primera calle hay un uno en cada cruce: solo se llega yendo recto hacia el este. "
           "Las obras ponen un cero, y ese cero corta los caminos que pasarían por ellas. "
           "Al llegar a la estación tenemos la respuesta: cuatro caminos.",
           e_ola, titulo="La ola de números", extra=3.0),
    Escena("Y estos son los cuatro: tres al sur y cuatro al este en distinto orden, sin pisar ninguna obra.",
           e_cuatro, titulo="Los cuatro caminos", dmin=11, extra=3.0),
    Escena("En el segundo ejemplo las obras cortan todos los caminos cortos. "
           "La primera calle está cortada en el segundo cruce, la segunda en el cuarto, y la tercera empieza con tres obras seguidas. "
           "Hay un rodeo que la alcanza, volviendo hacia el norte, pero es más largo, y no cuenta. "
           "Los números lo muestran solos: a la estación llegan cero caminos.",
           e_ejemplo2, titulo="Ejemplo 2", extra=1.5),
    Escena("En el código, los caminos se guardan en una matriz de ene por eme, de la cabecera Matriz, que se rellena por filas. "
           "Si el cruce tiene obras se pone a cero. Si no, se le suma el de arriba y el de la izquierda, cuando existen. "
           "Al terminar, la última casilla es la respuesta.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("Detalles: la memoria es ene por eme, que con cincuenta por cincuenta como mucho no importa. "
           "El tiempo es ene por eme, y con cincuenta por cincuenta como mucho, es instantáneo. "
           "Y el enunciado garantiza que el resultado cabe en un entero.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: un camino mínimo solo va al sur o al este. "
           "Cada cruce suma lo que llega de arriba y de la izquierda, y las obras valen cero. "
           "Se empieza con un uno en la salida y la respuesta queda en la estación. "
           "Todo en una matriz, en ene por eme.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/10-3", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"10-3: {build(ESC, '../10-3_esquivando_las_obras.mp4'):.0f}s")
