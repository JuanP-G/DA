"""Vídeo EJ 02-6 · Coleccionando cómics (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-6/EJ_02-6.cpp"
TEMA = "Tema 2 · Colas de prioridad"
PILAS = [[5, 2, 3, 1, 20], [9, 12, 44, 13, 4, 7, 8]]     # del fondo a la cima
MEJOR = min(min(p) for p in PILAS)
COLS = {0: C["blue"], 1: NARANJA}


def simula():
    pilas = [list(p) for p in PILAS]
    pq = Monticulo(lambda a, b: a < b)
    for i, p in enumerate(pilas):
        pq.push(i, (p[-1], i))
    pasos, vendidos, puesto = [], [], 1
    while pq.top()[1][0] != MEJOR:
        ant = pq.copia()
        i, (v, _) = pq.pop()
        pilas[i].pop()
        vendidos.append((v, i))
        if pilas[i]:
            pq.push(i, (pilas[i][-1], i))
        pasos.append((ant, pq.copia(), f"puesto {puesto}: se lleva el {v} (pila {i})" + (f", asoma el {pilas[i][-1]}" if pilas[i] else ""), "text"))
        puesto += 1
    pasos.append((pq.copia(), pq.copia(), f"puesto {puesto}: la cima es el {MEJOR}, ¡el mejor!", "gold"))
    return pasos, vendidos, puesto


PASOS, VEND, PUESTO = simula()


def etq(e, p):
    return f"{p[0]}\npila {e}"


def comic(f, x, y, v, u=1.0, c=None, gris=False):
    if u <= 0:
        return
    c = C["dim"] if gris else (c or C["blue"])
    f.d.rounded_rectangle((x - 46, y - 18, x + 46, y + 18), 5, fill=mix(C["bot"], mix(C["panel"], c, 0.4), u), outline=mix(C["bot"], c, u), width=2)
    f.d.text((x, y), str(v), font=font(18, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def dibuja_pilas(f, quitados=0, u=1.0, x0=150, sep=150, base=600, marca_mejor=False):
    vend = VEND[:quitados]
    for i, p in enumerate(PILAS):
        n = len(p) - sum(1 for v, j in vend if j == i)
        for k in range(n):
            v = p[k]
            comic(f, x0 + i * sep, base - k * 40, v, u, c=C["gold"] if (marca_mejor and v == MEJOR) else COLS[i])
        texto(f, (x0 + i * sep, base + 34), f"pila {i}", 18, "muted", u, anchor="mm")


def e_portada(f):
    def dib(f):
        for k in range(4):
            comic(f, 960, 420 - k * 40, ["", "", "", ""][k], f.p(0.3 + 0.1 * k, 0.4), c=[C["blue"], NARANJA, C["green"], C["red"]][k])
    portada(f, "EJ 02-6", "Coleccionando cómics", TEMA, dib)


def e_problema(f):
    dibuja_pilas(f, 0, aparece(f, f.c(0)), x0=380, sep=260, marca_mejor=f.t >= f.c(2))
    if f.t >= f.c(1):
        etiqueta(f, (900, 200), "cada cliente se lleva la cima más pequeña", 24, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (900, 280), f"¿en qué puesto de la fila te llevas el {MEJOR}?", 26, "gold", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 90), "solo importan las CIMAS: una cola de mínimos con ellas", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 260), "se vende la cima menor: pop, desapilar", 26, "text", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (640, 340), "si a esa pila le queda algo, su nueva cima entra en la cola", 24, "green", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 440), f"se para cuando la cima de la cola es el mejor de la tienda ({MEJOR})", 24, "muted", aparece(f, f.c(3)))


def lateral(f, k, fr):
    dibuja_pilas(f, k + (1 if fr > 0.4 and k < len(VEND) else 0), x0=110, sep=170, base=560, marca_mejor=True)


def e_traza(f):
    escena_traza(f, PASOS, etq, colores=COLS, lateral=lateral, cx=880, ancho=420, titulo="cola de mínimos con las cimas")


A_L = find_line(CPP, "priority_queue<pair<int, int>")
B_L = find_line(CPP, "cout << puesto")
L_AP = find_line(CPP, "pilas[i].apila(id);")
L_PU = find_line(CPP, "cola.push({ pilas[i].cima(), i });")
L_W = find_line(CPP, "while (cola.top().first != mejor) {")
L_DE = find_line(CPP, "pilas[p].desapila();")


def e_codigo(f):
    escena_codigo(f, CPP, [(A_L, B_L, {L_AP, L_AP + 1}, "cómics"), (A_L, B_L, {L_PU}, "cómics"),
                           (A_L, B_L, {L_W, L_W + 1, L_W + 2, L_DE}, "cómics"), (A_L, B_L, {L_DE + 1, L_DE + 2, L_DE + 3}, "cómics")], size=18)


def e_detalles(f):
    escena_lista(f, [("la pila se lee del fondo a la cima: apilar en ese orden la deja bien", "text"),
                     ("el mejor se calcula al leer: el mínimo de todos los cómics", "text"),
                     ("la cola tiene como mucho N elementos (una cima por pila)", "text"),
                     ("cada venta O(log N)", "gold")])


def e_cierre(f):
    cierre(f, "Coleccionando cómics", [
        "una cola de mínimos con la cima de cada pila",
        "vender: pop y desapilar; la nueva cima entra",
        "hasta que la cima de la cola es el mejor",
        "el puesto es el número de ventas más uno",
    ])


ESC = [
    Escena("Coleccionando cómics. Qué puesto de la fila hay que coger para llevarse el mejor.", e_portada, titulo="Portada", extra=1.0),
    Escena("En la tienda hay varias pilas de cómics, cada uno con un identificador. "
           "Cada cliente de la fila se lleva el cómic con identificador más pequeño de entre las cimas. "
           "¿En qué puesto de la fila hay que ponerse para llevarse el menor de toda la tienda?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Solo importan las cimas, así que las metemos en una cola de prioridad de mínimos. "
           "Cada venta saca la cima menor y desapila ese cómic. "
           "Si a esa pila le queda algo, su nueva cima entra en la cola. "
           "Paramos cuando la cima de la cola es el mejor de la tienda.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Las cimas son ocho y veinte. Se venden el ocho, el siete y el cuatro, de la segunda pila. "
           "Después el trece, y asoma el cuarenta y cuatro. "
           "Ahora la menor es el veinte de la primera pila; al venderlo, asoma el uno. "
           "El uno queda en la cima: hay que ser el sexto.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, cada pila se llena del fondo a la cima, y se apunta el mejor. "
           "La cima de cada pila entra en la cola. "
           "Mientras la cima de la cola no sea el mejor, se vende: pop y desapilar. "
           "Si queda algo, entra la nueva cima, y el puesto avanza.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("La entrada da cada pila del fondo a la cima, así que apilar en ese orden la deja bien. "
           "El mejor se calcula mientras se lee. "
           "La cola nunca tiene más de una cima por pila. "
           "Y cada venta cuesta logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de mínimos con las cimas; se vende la menor y entra la siguiente de su pila, hasta que asoma el mejor.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-6", "../02-6_coleccionando_comics.mp4", "02-6")
