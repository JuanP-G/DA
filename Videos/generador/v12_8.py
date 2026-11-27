"""Vídeo EJ 12-8 · Volando entre pivotes (animado)."""
from vidlib import C, font
from anim import Escena, mix
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-8/EJ_12-8.cpp"
N, K = 7, 2
F = [1]
for i in range(1, N):
    F.append(sum(F[max(0, i - K - 1):i]))
assert F == [1, 1, 2, 4, 7, 13, 24]
TB = Tabla(60, 420, 1, N, cw=120, ch=90, lw=140, cabecera=[str(i + 1) for i in range(N)], etiquetas=["formas"], tam=36)


def pivote(f, x, y, num, u=1.0, borde=None):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - 16, y - 40, x + 16, y + 50), 14, fill=mix(C["bot"], (120, 132, 160), u),
                          outline=mix(C["bot"], borde or (70, 80, 110), u), width=5 if borde else 2)
    f.d.text((x, y + 75), str(num), font=font(22, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def arco(f, x0, x1, y, col, u=1.0):
    if u <= 0:
        return
    alto = 25 + (x1 - x0) * 0.2
    f.d.arc((x0, y - alto, x1, y + alto), 180, 180 + 180 * u, fill=col, width=5)


def dib(f):
    for k in range(4):
        pivote(f, 810 + 120 * k, 340, k + 1, f.p(0.3 + 0.2 * k, 0.4))
    arco(f, 810, 1050, 300, C["gold"], f.p(1.2, 0.8))


CAMINOS = [[1, 2, 3, 4], [1, 2, 4], [1, 3, 4], [1, 4]]


def e_problema(f):
    texto(f, (640, 80), "4 pivotes, se pueden saltar hasta 2", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    xs = [340 + 200 * k for k in range(4)]
    for k, x in enumerate(xs):
        pivote(f, x, 340, k + 1, aparece(f, f.c(0)))
    q = -1
    for k in range(4):
        if f.t >= f.c(1) + 1.6 * k:
            q = k
    if q >= 0:
        cam = CAMINOS[q]
        for p, s in zip(cam, cam[1:]):
            arco(f, xs[p - 1], xs[s - 1], 300, C["gold"], f.p(f.c(1) + 1.6 * q, 0.8))
        texto(f, (640, 520), "  →  ".join(map(str, cam)), 34, "text", 1, mono=True, anchor="mm")
        texto(f, (640, 580), f"forma {q + 1}", 26, "muted", 1, anchor="mm")
    if f.t >= f.c(2):
        texto(f, (640, 640), "4 formas  (el resultado, módulo 1.000.000.007)", 30, "green", aparece(f, f.c(2)), anchor="mm")


def e_tabla(f):
    texto(f, (640, 60), f"N = {N}, K = {K}: cada pivote suma los 3 anteriores", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    nn = avance(f, 1, 4, N)
    cur = nn if nn < N and f.t >= f.c(1) else None
    xs = [60 + 140 + 120 * k + 60 for k in range(N)]
    for k, x in enumerate(xs):
        pivote(f, x, 270, k + 1, aparece(f, f.c(0)), borde=C["gold"] if k == cur else None)
    vals = {(0, i): F[i] for i in range(nn)}
    marca = {(0, cur): "gold"} if cur is not None else {}
    if cur is not None:
        for p in range(max(0, cur - K - 1), cur):
            arco(f, xs[p], xs[cur], 230, C["blue"])
            marca[(0, p)] = "blue"
        sumandos = " + ".join(str(F[p]) for p in range(max(0, cur - K - 1), cur))
        texto(f, (640, 620), f"formas({cur + 1}) = {sumandos or '1 (el primero)'}" + (f" = {F[cur]}" if cur else ""), 32,
              "text", 1, mono=True, anchor="mm")
    if f.t >= f.c(4):
        marca = {(0, N - 1): "green"}
        texto(f, (640, 620), f"formas(7) = {F[-1]}", 38, "green", aparece(f, f.c(4)), mono=True, anchor="mm")
    TB.dibuja(f, vals, marca=marca)


ESC = [
    Escena("Volando entre pivotes. De cuántas formas se puede llegar del primer pivote al último.",
           e_portada("12-8", "Volando entre pivotes", dib), titulo="Portada", extra=1.0),
    Escena("Hay cuatro pivotes en fila, y el padre puede saltarse como mucho dos. "
           "Puede pasar por todos, saltarse el tercero, saltarse el segundo, o volar directamente del primero al último. "
           "En total, cuatro formas.",
           e_problema, titulo="El problema", extra=2.5),
    Escena("Pensemos en el último vuelo. Venía de alguno de los pivotes anteriores, como mucho ka más uno atrás. "
           "Formas de i es el número de formas de llegar al pivote i. "
           "Al primero se llega de una sola forma: ya está allí. "
           "Y a cualquier otro, sumando las formas de los ka más uno anteriores que existan.",
           e_lineas([(0, 90, "¿desde dónde llega el último vuelo?", "gold", 32),
                     (2, 210, "formas(i) = maneras de llegar al pivote i", "muted", 28),
                     (3, 310, "formas(1) = 1", "text", 34, True),
                     (4, 420, "formas(i) = formas(i−1) + … + formas(i−K−1)", "text", 32, True),
                     (4, 490, "(solo índices ≥ 1)   módulo 1.000.000.007", "muted", 26),
                     (4, 580, "respuesta: formas(N)", "green", 30)]), titulo="Recurrencia", extra=1.5),
    Escena("Con siete pivotes y pudiendo saltar dos, cada casilla suma las tres anteriores. "
           "Al principio hay menos de tres, y se suman las que haya. "
           "Después la ventana se desliza. "
           "Entra un valor nuevo y sale el más antiguo. "
           "Al séptimo se llega de veinticuatro formas.",
           e_tabla, titulo="La tabla", extra=2.0),
    Escena("No hace falta volver a sumar cada vez: se mantiene la suma de la ventana. "
           "Se suma el que entra y se resta el que sale. "
           "Al restar con módulo, hay que sumar antes el módulo para que no quede negativo.",
           e_lineas([(0, 140, "ventana deslizante", "gold", 38),
                     (1, 280, "ventana += formas[i]", "text", 32, True),
                     (1, 350, "ventana −= formas[i − K − 1]", "text", 32, True),
                     (2, 480, "(ventana − sale + MOD) % MOD", "green", 32, True)]), titulo="La ventana", extra=1.5),
    Escena("En el código, la tabla empieza con un uno en el primer pivote. "
           "Cada casilla es la suma de la ventana. "
           "Luego se añade la casilla nueva, y se quita la que queda fuera. "
           "El coste es lineal.",
           e_codigo(CPP, "vector<int> formas(n + 1, 0);", "cout << formas[n]",
                    [["formas[1] = 1;"], ["formas[i] = ventana;"], ["ventana = (ventana + formas[i]) % MOD;", "if (i - k - 1 >= 1)", "ventana = (ventana - formas[i - k - 1]"],
                     ["cout << formas[n]"]],
                    [("caso base", "formas[1] = 1"), ("casilla", "la suma de la ventana"),
                     ("deslizar", "entra uno, sale otro"), ("coste", "O(N) por caso")], size=16),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: contar formas es sumar los casos según el último paso. "
           "Se miran los ka más uno pivotes anteriores. "
           "Con módulo en cada operación. "
           "Y con ventana deslizante el coste es lineal.",
           e_cierre("Volando entre pivotes", [
               "mirar el último vuelo",
               "sumar los K+1 anteriores (no K)",
               "módulo en cada suma y resta",
               "O(N) con ventana deslizante"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-8", "../12-8_volando_entre_pivotes.mp4")
