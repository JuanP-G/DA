"""Vídeo EJ 11-5 · Las vacas pensantes (animado)."""
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, build, preview, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla

CPP = "../../11-Programacion dinamica II/EJ_11-5/EJ_11-5.cpp"
TEMA = "Tema 11 · Programación dinámica II"
A = [8, 7, 1, 4]
n = len(A)


def despues(F, l, r):
    if l > r:
        return 0
    return F[l + 1][r] if A[l] > A[r] else F[l][r - 1]


F = [[0] * (n + 1) for _ in range(n + 2)]
for largo in range(1, n + 1):
    for i in range(n - largo + 1):
        j = i + largo - 1
        F[i][j] = max(A[i] + despues(F, i + 1, j), A[j] + despues(F, i, j - 1))
assert F[0][n - 1] == 12
ORDEN = [(i, i + d) for d in range(n) for i in range(n - d)]
GRIS = (30, 40, 62)
BAJO = {(i, j): GRIS for i in range(n) for j in range(i)}
TB = Tabla(40, 110, n, n, cw=96, ch=80, lw=100, cabecera=[f"{k}" for k in A], etiquetas=[f"{k}" for k in A], tam=32)
MIA = (240, 170, 90)
SUYA = (200, 120, 150)


def cubo(f, x, y, v, u=1.0, borde=None, w=84, h=90, gris=False):
    if u <= 0:
        return
    col = (110, 110, 120) if gris else (190, 150, 95)
    f.d.polygon([(x - w / 2 - 6, y - h / 2), (x + w / 2 + 6, y - h / 2), (x + w / 2 - 8, y + h / 2), (x - w / 2 + 8, y + h / 2)],
                fill=mix(C["bot"], col, u), outline=mix(C["bot"], borde or (110, 80, 50), u), width=6 if borde else 3)
    f.d.text((x, y + 4), str(v), font=font(32, True), fill=mix(C["bot"], (40, 28, 12), u), anchor="mm")


def vaca(f, x, y, col, u=1.0, etiqueta=""):
    """Cabeza de vaca sencilla."""
    if u <= 0:
        return
    c = mix(C["bot"], col, u)
    f.d.ellipse((x - 46, y - 40, x + 46, y + 46), fill=c)
    f.d.ellipse((x - 62, y - 36, x - 30, y - 8), fill=c)
    f.d.ellipse((x + 30, y - 36, x + 62, y - 8), fill=c)
    f.d.ellipse((x - 30, y + 8, x + 30, y + 48), fill=mix(C["bot"], (235, 200, 190), u))
    f.d.ellipse((x - 26, y - 14, x - 14, y - 2), fill=mix(C["bot"], (30, 30, 40), u))
    f.d.ellipse((x + 14, y - 14, x + 26, y - 2), fill=mix(C["bot"], (30, 30, 40), u))
    f.d.ellipse((x - 14, y + 22, x - 6, y + 32), fill=mix(C["bot"], (90, 60, 60), u))
    f.d.ellipse((x + 6, y + 22, x + 14, y + 32), fill=mix(C["bot"], (90, 60, 60), u))
    if etiqueta:
        f.d.text((x, y + 80), etiqueta, font=font(22, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        for k, v in enumerate([8, 7, 1, 4]):
            cubo(f, 780 + k * 100, 340, v, f.p(0.3 + 0.2 * k, 0.5), w=70, h=76)
        vaca(f, 780, 220, MIA, f.p(0.9, 0.6))
        vaca(f, 1080, 220, SUYA, f.p(1.1, 0.6))
    portada(f, "EJ 11-5", "Las vacas pensantes", TEMA, dib)


# turnos del ejemplo: (quien, índice del cubo)
TURNOS = [("yo", 0), ("ella", 1), ("yo", 3), ("ella", 2)]


def e_problema(f):
    xs = [330 + k * 190 for k in range(n)]
    y = 330
    vaca(f, 150, 150, MIA, aparece(f, f.c(0)), "yo (empiezo)")
    vaca(f, 1130, 150, SUYA, aparece(f, f.c(0)), "Devoradora")
    comidos = {}
    for q, (quien, idx) in enumerate(TURNOS):
        t = f.c(2) + 1.3 * q if f.t >= f.c(2) else 1e9
        if f.t >= t:
            comidos[idx] = (quien, f.lin(t, 0.9))
    for k in range(n):
        v = A[k]
        if k in comidos:
            quien, u = comidos[k]
            pila = [i2 for (q2, i2) in TURNOS if q2 == quien]
            dest = (150 if quien == "yo" else 1130, 340 + 70 * pila.index(k))
            x = lerp(xs[k], dest[0], ease(u)); yy = lerp(y, dest[1], ease(u))
            cubo(f, x, yy, v, 1.0, borde=MIA if quien == "yo" else SUYA, w=84 * (1 - 0.3 * u), h=90 * (1 - 0.3 * u))
        else:
            cubo(f, xs[k], y, v, aparece(f, f.c(1)))
    mias = sum(A[idx] for (q, idx) in [t for t in TURNOS if t[0] == "yo"] if idx in comidos and comidos[idx][1] >= 1)
    suyas = sum(A[idx] for (q, idx) in [t for t in TURNOS if t[0] == "ella"] if idx in comidos and comidos[idx][1] >= 1)
    if f.t >= f.c(2):
        texto(f, (150, 250), f"{mias}", 44, "gold", 1, mono=True, anchor="mm")
        texto(f, (1130, 250), f"{suyas}", 44, "muted", 1, mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 90), "ella siempre coge el extremo MAYOR", 30, SUYA, aparece(f, f.c(3)), anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 560), "¿cuánto puedo comer como máximo?  →  12", 34, "green", aparece(f, f.c(4)), anchor="mm")


def e_idea(f):
    texto(f, (640, 70), "yo elijo: izquierda o derecha", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    # fila (a b ... y z)
    xs = [260 + k * 150 for k in range(6)]
    for k, v in enumerate(["a", "…", "…", "…", "…", "z"]):
        cubo(f, xs[k], 230, v, aparece(f, f.c(0)), w=70, h=76, borde=MIA if k in (0, 5) and f.t >= f.c(1) else None)
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (xs[0], 310), "a", 26, MIA, u, anchor="mm", mono=True)
        texto(f, (xs[5], 310), "z", 26, MIA, u, anchor="mm", mono=True)
        texto(f, (640, 345), "mis dos opciones", 22, "muted", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 430), "Devoradora NO decide: coge el mayor de los dos extremos que queden", 28, SUYA, u, anchor="mm")
        texto(f, (640, 475), "su respuesta está decidida de antemano", 24, "muted", u, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (640, 560), "no hay que adivinar su jugada:  solo yo maximizo", 30, "green", u, anchor="mm")
    if f.t >= f.c(4):
        u = aparece(f, f.c(4))
        texto(f, (640, 620), "(sin minimax: ella no es una rival óptima)", 24, "muted", u, anchor="mm")


def e_recurrencia(f):
    texto(f, (60, 60), "come(i, j) = lo máximo que como yo con los cubos i..j, y me toca", 24, "muted", aparece(f, f.c(0)), bold=False)
    y = formula(f, 80, 110, "come(i, j) =", [("0", "si i > j   (no hay cubos)")], aparece(f, f.c(1)), size=24)
    texto(f, (60, y + 18), "Si cojo el de la izquierda  →  Devoradora responde", 24, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 58, "come(i, j) =", [("max( a[i] + después(i+1, j),", ""), ("      a[j] + después(i, j−1) )", "")],
                aparece(f, f.c(2)), size=26, colores=[NARANJA, AZUL])
    texto(f, (60, y + 28), "después(l, r)  =  lo que como yo cuando mueve ella", 24, "gold", aparece(f, f.c(3)))
    y = formula(f, 80, y + 70, "después(l, r) =", [("come(l+1, r)", "si a[l] > a[r]   (ella coge a[l])"),
                                                   ("come(l, r−1)", "si no   (ella coge a[r])")],
                aparece(f, f.c(3)), size=24, colores=[SUYA, SUYA])
    texto(f, (60, y + 28), "Respuesta:  come(1, N)", 28, "green", aparece(f, f.c(4)), mono=True)


def e_tabla(f):
    t0, t1 = f.c(1), f.c(4)
    paso = (t1 - t0) / len(ORDEN)
    nn = max(0, min(len(ORDEN), int((f.t - t0) / paso) if f.t >= t0 else 0))
    vals = {}
    for (i, j) in ORDEN[:nn]:
        vals[(i, j)] = F[i][j]
    cur = ORDEN[nn] if nn < len(ORDEN) and f.t >= t0 else None
    sombra = dict(BAJO)
    marca = {}
    if cur:
        i, j = cur
        marca[cur] = "gold"
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    texto(f, (TB.x0 + TB.lw + 2 * TB.cw, 80), "j  →", 20, "muted", aparece(f, f.c(0)), anchor="mm")
    if cur:
        i, j = cur
        f.box(560, 100, 690, 400, f"come({i + 1}, {j + 1})   cubos {A[i:j + 1]}")
        if i == j:
            texto(f, (590, 190), f"un solo cubo: me lo como  →  {A[i]}", 28, "green", 1, fondo=C["panel"])
        else:
            for q, (lado, idx, resto, col) in enumerate([("izquierda", i, (i + 1, j), NARANJA), ("derecha", j, (i, j - 1), AZUL)]):
                yy = 160 + 160 * q
                l, r = resto
                if l > r:
                    resp, val = "—", 0
                elif A[l] > A[r]:
                    resp, val = f"ella coge {A[l]}", F[l + 1][r] if l + 1 <= r else 0
                else:
                    resp, val = f"ella coge {A[r]}", F[l][r - 1] if l <= r - 1 else 0
                tot = A[idx] + val
                texto(f, (590, yy), f"cojo {A[idx]} ({lado})", 26, col, 1, fondo=C["panel"])
                texto(f, (590, yy + 42), f"{resp}   →   me quedo con {val} más", 22, "muted", 1, bold=False, fondo=C["panel"])
                texto(f, (590, yy + 82), f"{A[idx]} + {val} = {tot}", 28, "green" if tot == F[i][j] else "text", 1, mono=True, fondo=C["panel"])
    if f.t >= t1:
        TB.dibuja(f, {(i, j): F[i][j] for (i, j) in ORDEN}, marca={(0, n - 1): "green"}, sombra=sombra)
        texto(f, (640, 640), f"come(1, 4) = {F[0][n - 1]}", 36, "green", aparece(f, t1), mono=True, anchor="mm")


def e_porque(f):
    # ejemplo 2 4 15 5: voraz vs óptimo vs minimax
    ej = [2, 4, 15, 5]
    for k, v in enumerate(ej):
        cubo(f, 340 + k * 200, 190, v, aparece(f, f.c(0)))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (640, 330), "si cojo el mayor (el 5): ella coge el 15  →  5 + 4 = 9", 28, "muted", u, anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 400), "pero si cojo el 2, quedan 4 · 15 · 5…", 26, "text", u, anchor="mm")
        texto(f, (640, 450), "ella coge el 5 (mayor extremo) y me deja el 15", 26, SUYA, aparece(f, f.c(2) + 0.8), anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (640, 540), "2 + 15 = 17", 46, "green", u, mono=True, anchor="mm")
    if f.t >= f.c(4):
        texto(f, (640, 610), "sacrificar el mayor hoy puede dar más mañana", 26, "text", aparece(f, f.c(4)), anchor="mm")


La = find_line(CPP, "Matriz<int> come(n + 3, n + 3, 0);")
Lb = find_line(CPP, "cout << come[1][n]")
CODE = codigo(CPP, La, Lb, maxc=76)
L_DES = find_line(CPP, "auto despues = [&](int l, int r)")
L_RET = find_line(CPP, "return a[l] > a[r] ? come[l + 1][r] : come[l][r - 1];")
L_LAR = find_line(CPP, "for (int largo = 1; largo <= n; ++largo)")
L_MAX = find_line(CPP, "come[i][j] = max(")
L_OUT = Lb


def e_codigo(f):
    hl = {La}
    if f.t >= f.c(1):
        hl = {L_DES, L_RET}
    if f.t >= f.c(2):
        hl = {L_LAR, L_MAX}
    if f.t >= f.c(3):
        hl = {L_OUT}
    f.code(40, 90, 800, 560, CODE, hl=hl, title="tabla por longitudes", size=17)
    f.box(880, 90, 360, 560, "qué hace")
    notas = [("Matriz con hueco", "come[i][j] = 0 si i > j", C["blue"]),
             ("después(l, r)", "la respuesta de Devoradora", SUYA),
             ("largo de 1 a n", "intervalos cortos antes que largos", C["green"]),
             ("come[1][n]", "una sola línea por caso", C["gold"])]
    for k, (a, b, col) in enumerate(notas):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (910, 150 + 120 * k), a, 24, col, u, fondo=C["panel"])
            texto(f, (910, 190 + 120 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])


def e_detalles(f):
    f.box(40, 110, 580, 480, "cuidado con")
    f.box(660, 110, 580, 480, "coste")
    cuid = [("cantidades distintas", "por eso su elección nunca tiene empate", C["blue"]),
            ("el último cubo", "con un solo cubo, me lo como yo o ella según toque", NARANJA),
            ("no es un minimax", "ella juega siempre igual: solo maximizo yo", C["green"])]
    for k, (a, b, col) in enumerate(cuid):
        if f.t >= f.c(k):
            u = aparece(f, f.c(k))
            texto(f, (70, 170 + 130 * k), a, 26, col, u, fondo=C["panel"])
            texto(f, (70, 212 + 130 * k), b, 20, "muted", u, bold=False, fondo=C["panel"])
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (690, 190), "O(N²)", 44, "gold", u, mono=True, fondo=C["panel"])
        texto(f, (690, 270), "N ≤ 1000", 28, "text", u, fondo=C["panel"])
        texto(f, (690, 330), "medio millón de intervalos", 26, "muted", u, fondo=C["panel"])
        texto(f, (690, 390), "cada uno en O(1)", 24, "muted", u, fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Las vacas pensantes", [
        "PD sobre intervalos: come(i, j) con los cubos i..j",
        "yo elijo extremo; Devoradora responde con el mayor",
        "come(i, j) = max(a[i] + después(i+1, j), a[j] + después(i, j−1))",
        "se rellena de intervalos cortos a largos",
    ])


ESC = [
    Escena("Las vacas pensantes. Comer lo máximo contra una vaca que siempre coge el cubo mayor.", e_portada, titulo="Portada", extra=1.0),
    Escena("Hay una hilera de cubos con comida. Dos vacas se turnan, y cada una coge uno de los dos extremos. "
           "Yo empiezo, y mi compañera Devoradora sigue siempre la misma regla: coge el extremo que tenga más comida. "
           "En este ejemplo, cojo el ocho, ella el siete, yo el cuatro, y a ella le queda el uno. "
           "Ella siempre elige el extremo mayor. "
           "¿Cuánto puedo comer como máximo? Doce.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("En mi turno elijo entre dos cosas: el cubo de la izquierda o el de la derecha. "
           "Pero después, mi rival no decide nada. "
           "Su respuesta es siempre la misma: el mayor de los dos extremos. "
           "Así que no hay que adivinar su jugada. Solo yo maximizo. "
           "No es un juego de minimax, porque Devoradora no es una rival que juegue lo mejor posible.",
           e_idea, titulo="Mis dos opciones", extra=1.5),
    Escena("Come de i, j es lo máximo que como yo con los cubos de i a j, cuando me toca. "
           "Sin cubos, cero. "
           "Si cojo el de la izquierda, me llevo a de i, y luego mueve Devoradora. "
           "Después de l, r es lo que me queda cuando ella mueve: si a de l es mayor, ella se lo come y yo sigo con l más uno, r. Si no, se come el derecho. "
           "La respuesta es come de uno, ene.",
           e_recurrencia, titulo="Recurrencia", extra=2.0),
    Escena("La tabla se rellena de intervalos cortos a largos, porque cada casilla depende de intervalos más pequeños. "
           "Con un solo cubo, me lo como. "
           "Para más cubos, probamos las dos opciones: cojo el de la izquierda o el de la derecha, miramos qué responde ella, y sumamos lo que me queda. "
           "Me quedo con la mayor. "
           "La esquina dice que puedo comer doce.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Con dos, cuatro, quince y cinco, coger siempre el mayor no es lo mejor. "
           "Si cojo el cinco, ella se lleva el quince y yo me quedo con nueve. "
           "Pero si cojo el dos, ella coge el cinco, que es el mayor de los extremos, y me deja el quince. "
           "Dos más quince, diecisiete. "
           "A veces conviene sacrificar lo mejor hoy para conseguir más después.",
           e_porque, titulo="¿Por qué no voraz?", extra=1.5),
    Escena("En el código, la matriz come tiene una fila y una columna de sobra, para que valga cero cuando i es mayor que j. "
           "Después es una función que mira quién es mayor, a de l o a de r, y devuelve la casilla que corresponda. "
           "El bucle va de largo uno a n, y cada casilla es el máximo de las dos opciones. "
           "Se escribe come de uno, n.",
           e_codigo, titulo="El código", extra=1.5),
    Escena("Tres detalles. Las cantidades son distintas, así que Devoradora nunca duda entre dos extremos. "
           "No hay minimax: ella juega siempre igual y solo yo maximizo. "
           "El coste es ene al cuadrado: con mil cubos, medio millón de intervalos, cada uno en tiempo constante.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: programación dinámica sobre intervalos. "
           "Yo elijo un extremo, y Devoradora responde con el mayor. "
           "Come de i, j es el máximo de las dos opciones, sumando lo que me queda después de su respuesta. "
           "Y se rellena de intervalos cortos a largos.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        solo = {int(x) for x in sys.argv[sys.argv.index("--solo") + 1].split(",")} if "--solo" in sys.argv else None
        preview(ESC, "preview/11-5", tiempos=(0.5, "fin"), solo=solo)
    else:
        print(f"11-5: {build(ESC, '../11-5_las_vacas_pensantes.mp4'):.0f}s")
