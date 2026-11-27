"""Vídeo EJ 12-10 · Megaautopista de Oriente (animado)."""
from vidlib import C, font
from anim import Escena, mix
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-10/EJ_12-10.cpp"
X, BEN, D = [10, 20, 30, 40, 55], [20, 40, 20, 30, 25], 15
n = len(X)
antes, gana = [0], [0]
for i in range(n):
    antes.append(sum(1 for q in X if q <= X[i] - D))
    gana.append(max(gana[-1], gana[antes[-1]] + BEN[i]))
assert gana[-1] == 95 and antes[1:] == [0, 0, 1, 2, 4]
ELEGIDAS = []
i = n
while i > 0:
    if gana[i] == gana[i - 1]:
        i -= 1
    else:
        ELEGIDAS.append(i - 1)
        i = antes[i]
assert sorted(X[k] for k in ELEGIDAS) == [20, 40, 55]

TB = Tabla(60, 330, 3, n, cw=150, ch=76, lw=190, cabecera=[f"área {i + 1}" for i in range(n)],
           etiquetas=["beneficio", "antes(i)", "gana(i)"], tam=32)


def px(km):
    return 100 + (km - 5) * 1080 / 55


def carretera(f, y, u=1.0, sel=(), marcar=None, benef=True):
    if u <= 0:
        return
    f.d.rectangle((60, y - 14, 1220, y + 14), fill=mix(C["bot"], (60, 66, 82), u))
    for x in range(80, 1210, 60):
        f.d.line((x, y, x + 30, y), fill=mix(C["bot"], (220, 220, 220), u), width=3)
    for k, (km, b) in enumerate(zip(X, BEN)):
        x = px(km)
        col = (200, 80, 80) if k in sel else (70, 100, 150)
        f.d.rounded_rectangle((x - 36, y - 80, x + 36, y - 30), 8, fill=mix(C["bot"], col, u),
                              outline=mix(C["bot"], C["gold"] if k == marcar else col, u), width=5)
        if benef:
            f.d.text((x, y - 55), str(b), font=font(26, True), fill=mix(C["bot"], C["text"], u), anchor="mm")
        f.d.text((x, y + 40), f"km {km}", font=font(20), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def dib(f):
    f.d.rectangle((760, 330, 1240, 356), fill=(60, 66, 82))
    for k in range(3):
        if f.t > 0.4 + 0.3 * k:
            x = 820 + 170 * k
            f.d.rounded_rectangle((x - 40, 260, x + 40, 318), 8, fill=(200, 80, 80))
            f.d.polygon([(x - 50, 262), (x, 230), (x + 50, 262)], fill=(230, 180, 80))


def e_problema(f):
    texto(f, (640, 80), "dónde construir restaurantes: separados al menos D = 15 km", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    sel = ()
    if f.t >= f.c(2):
        sel = tuple(ELEGIDAS)
    carretera(f, 300, aparece(f, f.c(1)), sel=sel)
    if f.t >= f.c(2):
        texto(f, (640, 450), "40 + 30 + 25 = 95", 40, "green", aparece(f, f.c(2)), mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 540), "salida:  95", 30, "text", aparece(f, f.c(3)), mono=True, anchor="mm")
        texto(f, (640, 590), "         20 40 55", 30, "text", aparece(f, f.c(3)), mono=True, anchor="mm")


def e_tabla(f):
    nn = avance(f, 1, 4, n)
    cur = nn if nn < n and f.t >= f.c(1) else None
    carretera(f, 190, aparece(f, f.c(0)), marcar=cur)
    vals = {(0, k): BEN[k] for k in range(n)}
    vals.update({(1, k): antes[k + 1] for k in range(nn + (cur is not None))})
    vals.update({(2, k): gana[k + 1] for k in range(nn)})
    marca = {(2, cur): "gold"} if cur is not None else {}
    if cur is not None:
        i = cur + 1
        no, si = gana[i - 1], gana[antes[i]] + BEN[cur]
        texto(f, (640, 640), f"max( {no} ,  gana({antes[i]}) + {BEN[cur]} = {si} ) = {gana[i]}", 30, "text", 1, mono=True, anchor="mm")
    if f.t >= f.c(4):
        marca = {(2, n - 1): "green"}
        texto(f, (640, 640), f"gana(5) = {gana[n]}", 38, "green", aparece(f, f.c(4)), mono=True, anchor="mm")
    TB.dibuja(f, vals, marca=marca)


def e_recons(f):
    texto(f, (640, 60), "reconstrucción: de la última área hacia atrás", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    pasos = [4, 3, 1]                       # índices de las áreas elegidas, en el orden en que salen
    sel = tuple(p for k, p in enumerate(pasos) if f.t >= f.c(k + 1))
    carretera(f, 200, 1.0, sel=sel)
    TB.dibuja(f, {**{(0, k): BEN[k] for k in range(n)}, **{(1, k): antes[k + 1] for k in range(n)},
                  **{(2, k): gana[k + 1] for k in range(n)}}, marca={(2, p): "green" for p in sel})
    frases = ["95 ≠ 70: restaurante en el km 55, saltar a antes = 4",
              "70 ≠ 40: restaurante en el km 40, saltar a antes = 2",
              "40 ≠ 20: restaurante en el km 20, antes = 0: fin"]
    for k, s in enumerate(frases):
        if f.t >= f.c(k + 1) and (k == 2 or f.t < f.c(k + 2)):
            texto(f, (640, 640), s, 28, "text", 1, anchor="mm")


ESC = [
    Escena("Megaautopista de Oriente. Dónde construir restaurantes para ganar lo máximo respetando una distancia mínima.",
           e_portada("12-10", "Megaautopista de Oriente", dib), titulo="Portada", extra=1.0),
    Escena("Dos restaurantes de la empresa no pueden estar a menos de quince kilómetros. "
           "Cada área de descanso tiene su punto kilométrico y su beneficio. "
           "Lo mejor aquí es construir en los kilómetros veinte, cuarenta y cincuenta y cinco. "
           "Hay que escribir el beneficio y también las posiciones.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("En la última área hay dos opciones: construir o no. "
           "Gana de i es el máximo beneficio usando las i primeras áreas. "
           "Antes de i es cuántas áreas quedan a quince kilómetros o más por detrás. "
           "Si no construimos, vale gana de i menos uno. "
           "Si construimos, su beneficio más lo mejor de las áreas compatibles.",
           e_lineas([(0, 90, "¿construir en el área i o no?", "gold", 34),
                     (1, 200, "gana(i)  = máximo con las áreas 1..i", "muted", 28),
                     (2, 260, "antes(i) = áreas con x ≤ x_i − D", "muted", 28),
                     (3, 370, "no:  gana(i−1)", "text", 34, True),
                     (4, 450, "sí:  gana(antes(i)) + b_i", "text", 34, True),
                     (4, 570, "gana(i) = el máximo;  gana(0) = 0", "green", 30)]), titulo="Recurrencia", extra=1.5),
    Escena("Calculamos área por área. "
           "Como las posiciones están ordenadas, antes de i nunca retrocede: basta avanzar un puntero. "
           "Cada casilla compara no construir con construir. "
           "Y saltar a las áreas compatibles. "
           "El máximo beneficio es noventa y cinco.",
           e_tabla, titulo="La tabla", extra=3.0),
    Escena("Para saber dónde construir recorremos la tabla hacia atrás. "
           "El último valor cambió, así que hay restaurante en el kilómetro cincuenta y cinco. "
           "Saltamos a las compatibles: otro en el cuarenta. "
           "Y otro en el veinte, y ya no quedan áreas.",
           e_recons, titulo="Reconstrucción", extra=2.0),
    Escena("En el código, el puntero jota cuenta las áreas compatibles. "
           "Cada gana es el máximo entre no construir y construir. "
           "La reconstrucción guarda las posiciones de atrás hacia delante. "
           "Por eso se escriben al revés.",
           e_codigo(CPP, "vector<int> gana(n + 1, 0)", "elegidas[k] << (k > 0",
                    [["while (x[j + 1] <= x[i] - d) ++j;"], ["int construir = gana[j] + b[i];", "gana[i] = construir >"],
                     ["elegidas.push_back(x[i]);", "i = antes[i];"], ["for (int k = (int)elegidas.size() - 1"]],
                    [("puntero j", "nunca retrocede: O(N)"), ("máximo", "construir o no"),
                     ("hacia atrás", "sin recursión"), ("al revés", "orden creciente")], size=14),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: construir o no en cada área. "
           "Si construimos, saltamos a las compatibles. "
           "A exactamente D kilómetros sí se puede. "
           "Y la reconstrucción recorre la tabla hacia atrás.",
           e_cierre("Megaautopista de Oriente", [
               "gana(i) = max(gana(i−1), gana(antes(i)) + b_i)",
               "antes(i) con un puntero: O(N)",
               "a exactamente D km sí es válido",
               "reconstrucción hacia atrás"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-10", "../12-10_megaautopista_de_oriente.mp4")
