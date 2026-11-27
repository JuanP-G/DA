"""Vídeo EJ 12-4 · Mejor no llevar muchas monedas (animado)."""
from vidlib import C, font
from anim import Escena, mix
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-4/EJ_12-4.cpp"
V, CANT, P = [15, 10, 5], [2, 2, 2], 20
COLS = [0, 5, 10, 15, 20]
INF = 99
F = [[0 if j == 0 else INF for j in COLS]]
for v, c in zip(V, CANT):
    ant = F[-1]
    F.append([min(ant[COLS.index(j - k * v)] + k for k in range(c + 1) if k * v <= j) for j in COLS])
assert F[-1][-1] == 2
VAL = lambda i, j: None if F[i][j] >= INF else F[i][j]
ORDEN = [(i, j) for i in range(4) for j in range(5)]
TB = Tabla(30, 130, 4, 5, cw=92, ch=82, lw=150, cabecera=[str(j) for j in COLS],
           etiquetas=["ninguna", "+ de 15", "+ de 10", "+ de 5"], tam=32)


def moneda(f, x, y, v, u=1.0, r=40, borde=False):
    if u <= 0:
        return
    f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], (226, 184, 70), u),
                outline=mix(C["bot"], C["green"] if borde else (140, 105, 30), u), width=7 if borde else 4)
    f.d.text((x, y), str(v), font=font(int(r * 0.7), True), fill=mix(C["bot"], (60, 40, 5), u), anchor="mm")


def dib(f):
    for k, v in enumerate([50, 10, 5, 1]):
        moneda(f, 960 + 80 * k, 450, v, f.p(0.3 + 0.25 * k, 0.5), r=34)


def e_problema(f):
    texto(f, (640, 80), "pagar EXACTAMENTE 20 con el menor número de monedas", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for t, v in enumerate(V):
        texto(f, (230, 200 + 110 * t), f"dos de {v}", 26, "muted", aparece(f, f.c(1)), anchor="mm")
        for k in range(2):
            moneda(f, 400 + 100 * k, 200 + 110 * t, v, aparece(f, f.c(1)))
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (880, 220), "15 + 5 = 20", 34, "green", u, mono=True, anchor="mm")
        texto(f, (880, 300), "10 + 10 = 20", 34, "green", u, mono=True, anchor="mm")
        texto(f, (880, 370), "dos monedas en ambos casos", 24, "muted", u, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 580), "salida:  SI 0 2 0   (o SI 1 0 1)", 32, "text", aparece(f, f.c(3)), mono=True, anchor="mm")


def e_tabla(f):
    n = avance(f, 1, 5, len(ORDEN))
    vals = {(i, j): VAL(i, j) for i, j in ORDEN[:n]}
    cur = ORDEN[n] if n < len(ORDEN) and f.t >= f.c(1) else None
    marca = {cur: "gold"} if cur else {}
    if f.t >= f.c(5):
        marca = {(3, 4): "green"}
    TB.dibuja(f, vals, marca=marca)
    if cur and cur[0] > 0:
        i, j = cur
        v, c, cant = V[i - 1], CANT[i - 1], COLS[j]
        filas = [(f"monedas de {v}: hay {c}", "muted")]
        for k in range(c + 1):
            if k * v <= cant:
                a = VAL(i - 1, COLS.index(cant - k * v))
                filas.append((f"k = {k}:  {'∞' if a is None else a} + {k}", "green" if a is not None and a + k == F[i][j] else "text"))
        panel(f, 660, 130, 590, 320, f"pagar {cant}", filas)
    if f.t >= f.c(5):
        texto(f, (640, 600), "monedas(3, 20) = 2", 38, "green", aparece(f, f.c(5)), mono=True, anchor="mm")


ESC = [
    Escena("Mejor no llevar muchas monedas. Pagar un precio exacto con las monedas que hay, usando las menos posibles.",
           e_portada("12-4", "Mejor no llevar muchas monedas", dib), titulo="Portada", extra=1.0),
    Escena("Mario quiere pagar exactamente veinte, con las menos monedas posibles. "
           "Tiene dos monedas de quince, dos de diez y dos de cinco. "
           "Puede usar una de quince y una de cinco, o las dos de diez. "
           "Se escribe cuántas monedas de cada tipo usa, en el orden de la entrada.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Monedas de i, j es el mínimo número de monedas para pagar j usando los i primeros tipos. "
           "Sin monedas, pagar cero cuesta cero, y cualquier otra cantidad es imposible: infinito. "
           "Del tipo i decidimos cuántas usar: ninguna, una, dos, hasta las que haya. "
           "Cada opción cuesta esas ka monedas, más lo mejor para el resto sin ese tipo. "
           "Nos quedamos con el mínimo.",
           e_lineas([(0, 90, "monedas(i, j) = mínimo para pagar j con los tipos 1..i", "gold", 30),
                     (1, 200, "monedas(0, 0) = 0        monedas(0, j) = ∞", "text", 30, True),
                     (2, 310, "para cada k de 0 a c[i]  (si k · v[i] ≤ j)", "muted", 28),
                     (3, 390, "monedas(i − 1, j − k · v[i]) + k", "text", 34, True),
                     (4, 490, "monedas(i, j) = el mínimo de todas", "green", 32),
                     (4, 570, "respuesta: monedas(N, P)", "muted", 26)]), titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla con el ejemplo. "
           "En la primera fila no hay monedas: solo se puede pagar el cero. "
           "Cada fila añade un tipo, y siempre mira la fila de arriba, nunca la propia. "
           "Si mirara la misma fila, estaríamos suponiendo monedas ilimitadas. "
           "Para cada casilla se prueban todas las cantidades de la moneda nueva. "
           "La última casilla dice que veinte se paga con dos monedas.",
           e_tabla, titulo="La tabla", extra=3.0),
    Escena("Para saber qué monedas son, recorremos la tabla hacia atrás desde la última casilla. "
           "Con el cinco: usando cero, el valor de arriba ya es dos, así que no hace falta. "
           "Con el diez: usando dos, quedan cero, y cero más dos es dos. "
           "Con el quince ya no queda nada que pagar. "
           "Resultado: cero, dos, cero.",
           e_lineas([(0, 90, "reconstrucción: de (3, 20) hacia arriba", "gold", 32),
                     (1, 220, "moneda de 5:   k = 0,  se sigue en 20", "text", 30, True),
                     (2, 300, "moneda de 10:  k = 2,  se sigue en  0", "text", 30, True),
                     (3, 380, "moneda de 15:  k = 0", "text", 30, True),
                     (4, 500, "SI 0 2 0", "green", 48, True)]), titulo="Reconstrucción", extra=1.5),
    Escena("Un voraz que coja siempre la moneda mayor no sirve. "
           "Con una moneda de quince y dos de diez, para pagar veinte cogería la de quince, y faltarían cinco que no tiene. "
           "La tabla encuentra las dos de diez.",
           e_lineas([(0, 110, "¿y coger siempre la mayor?", "gold", 34),
                     (1, 260, "monedas: 15, 10, 10      precio: 20", "text", 30, True),
                     (1, 340, "voraz: 15 y faltan 5  →  NO", "muted", 30, True),
                     (2, 460, "tabla: 10 + 10  →  SI", "green", 36, True)]), titulo="¿Por qué no voraz?", extra=1.5),
    Escena("En el código, la matriz usa enteros con infinito, para que sumar no desborde. "
           "El bucle de ka empieza copiando la opción de no usar el tipo, y prueba el resto mientras haya monedas y quepan. "
           "Si la casilla final es infinito, escribimos NO. "
           "Si no, se reconstruye buscando la ka que dio cada valor.",
           e_codigo(CPP, "Matriz<EntInf> monedas", "j -= k * v[i];",
                    [["monedas[0][0] = 0;"], ["monedas[i][j] = monedas[i - 1][j];", "for (int k = 1; k <= c[i]"],
                     ["if (monedas[n][P] == Infinito)"], ["while (monedas[i - 1][j - k * v[i]]"]],
                    [("EntInf", "infinito + k sigue siendo infinito"), ("bucle de k", "k ≤ c[i]  y  k·v[i] ≤ j"),
                     ("NO", "la casilla final es infinito"), ("reconstrucción", "la k que dio el valor")]),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: es el problema del cambio, pero con cantidades limitadas. "
           "Para cada tipo se decide cuántas monedas usar. "
           "Siempre mirando la fila anterior. "
           "Y la tabla entera permite reconstruir la solución.",
           e_cierre("Mejor no llevar muchas monedas", [
               "cambio de monedas con cantidades limitadas",
               "k de 0 a min(c[i], j / v[i])",
               "monedas(i, j) = min( monedas(i−1, j − k·v[i]) + k )",
               "reconstrucción desde (N, P)"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-4", "../12-4_mejor_no_llevar_muchas_monedas.mp4")
