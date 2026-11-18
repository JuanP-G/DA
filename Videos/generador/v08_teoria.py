"""Vídeo de teoría · Algoritmos voraces (temas 8 y 9), animado."""
from vidlib import C, W, H, font
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

TEMA = "Temas 8 y 9 · Algoritmos voraces"
MORADO = C["purple"]


def moneda(f, x, y, v, u=1.0, c=None, r=34):
    if u <= 0:
        return
    c = c or C["gold"]
    f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], mix(C["panel"], c, 0.5), u), outline=mix(C["bot"], c, u), width=4)
    f.d.text((x, y), str(v), font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def e_portada(f):
    def dib(f):
        for k, v in enumerate([2, 1, 1]):
            moneda(f, 860 + k * 90, 320, v, f.p(0.3 + 0.2 * k, 0.5))
    portada(f, "Teoría", "Algoritmos voraces", TEMA, dib)


def e_idea(f):
    texto(f, (640, 70), "en cada paso, la opción que mejor parece AHORA", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    # devolver 0,80 € con monedas de 50, 20, 10
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (640, 140), "devolver 80 céntimos", 26, "text", u, anchor="mm")
        for k, v in enumerate([50, 20, 10]):
            moneda(f, 400 + k * 240, 260, v, u)
        sel = [50, 20, 10]
        for q, v in enumerate(sel):
            t0 = f.c(2) + q * 0.9
            if f.t >= t0:
                src = (400 + [50, 20, 10].index(v) * 240, 260)
                p = mueve(src, (520 + q * 120, 450), f.lin(t0, 0.7))
                moneda(f, p[0], p[1], v, c=C["green"])
        if f.t >= f.c(2) + 2.8:
            etiqueta(f, (640, 560), "la más grande que cabe, y no se vuelve atrás", 26, "green", aparece(f, f.c(2) + 2.8))
    if f.t >= f.c(3):
        etiqueta(f, (640, 640), "rápido y sencillo… pero no siempre acierta", 26, "red", aparece(f, f.c(3)))


def e_falla(f):
    texto(f, (640, 70), "monedas de 1, 3 y 4 · devolver 6", 30, "text", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        texto(f, (340, 180), "voraz", 30, "red", u, anchor="mm")
        for q, v in enumerate([4, 1, 1]):
            moneda(f, 220 + q * 120, 300, v, aparece(f, f.c(1) + 0.5 * q), c=C["red"])
        texto(f, (340, 400), "3 monedas", 26, "red", aparece(f, f.c(1) + 1.5), anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (940, 180), "óptimo", 30, "green", u, anchor="mm")
        for q, v in enumerate([3, 3]):
            moneda(f, 880 + q * 120, 300, v, aparece(f, f.c(2) + 0.5 * q), c=C["green"])
        texto(f, (940, 400), "2 monedas", 26, "green", aparece(f, f.c(2) + 1.0), anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 560), "un voraz hay que DEMOSTRARLO", 30, "gold", aparece(f, f.c(3)))
        etiqueta(f, (640, 640), "y antes, buscar contraejemplos pequeños", 24, "text", aparece(f, f.c(3) + 0.4))


def e_receta(f):
    pasos = [("1", "Criterio", "¿qué se coge\nprimero? casi\nsiempre: ordenar", C["blue"]),
             ("2", "Probar", "probar casos\npequeños para\ndescartar ideas", C["red"]),
             ("3", "Demostrar", "intercambio:\nel óptimo puede\nhacer lo mismo", MORADO),
             ("4", "Programar", "sort + un bucle\nO(N log N)", C["green"])]
    texto(f, (640, 70), "La receta", 34, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (num, tit, desc, col) in enumerate(pasos):
        t0 = f.c(min(k + 1, 4))
        if f.t < t0:
            continue
        u = aparece(f, t0)
        x = 40 + k * 305
        y = lerp(200, 150, ease(u))
        f.d.rounded_rectangle((x, y, x + 285, y + 330), 18, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], col, u), width=4)
        f.d.ellipse((x + 20, y + 20, x + 80, y + 80), fill=mix(C["bot"], col, u))
        f.d.text((x + 50, y + 50), num, font=font(32, True), fill=C["node_t"], anchor="mm")
        f.d.text((x + 94, y + 50), tit, font=font(24, True), fill=mix(C["bot"], C["text"], u), anchor="lm")
        for q, line in enumerate(desc.split("\n")):
            f.d.text((x + 22, y + 120 + q * 40), line, font=font(24), fill=mix(C["bot"], C["muted"], u))


def e_intercambio(f):
    texto(f, (640, 70), "Demostración por intercambio", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    # fila "óptimo" y fila "voraz"; se cambia la primera diferencia
    vor = ["A", "B", "C", "D"]
    opt = ["A", "X", "C", "Y"]
    u = aparece(f, f.c(1))
    texto(f, (180, 230), "voraz", 24, "green", u, anchor="rm")
    texto(f, (180, 350), "óptimo", 24, MORADO, u, anchor="rm")
    for k in range(4):
        caja(f, 260 + k * 140, 230, vor[k], c="green", u=u, w=100, h=70, tam=30)
        v = opt[k]
        if k == 1 and f.t >= f.c(2):
            v = "B"
        if k == 3 and f.t >= f.c(3):
            v = "D"
        caja(f, 260 + k * 140, 350, v, c=MORADO if v == opt[k] else C["green"], u=u, w=100, h=70, tam=30)
    if f.t >= f.c(2):
        u2 = aparece(f, f.c(2))
        f.d.rectangle((260 + 140 - 60, 190, 260 + 140 + 60, 395), outline=mix(C["bot"], C["gold"], u2), width=4)
        texto(f, (900, 300), "cambiar X por B:", 24, "text", u2)
        texto(f, (900, 340), "sigue siendo válida", 24, "text", u2)
        texto(f, (900, 380), "y no es peor", 24, "text", u2)
    if f.t >= f.c(3):
        etiqueta(f, (640, 560), "repitiendo, el óptimo se convierte en la voraz sin empeorar", 26, "green", aparece(f, f.c(3)))
    if f.t >= f.c(4):
        etiqueta(f, (640, 640), "⇒ la voraz es óptima", 30, "gold", aparece(f, f.c(4)))


PATR = [("Selección de actividades", "ordenar por FIN, coger lo compatible", "08-4", C["blue"]),
        ("Pinchar / cubrir puntos", "el parche o pasadizo lo más a la derecha", "08-1 · 09-1", NARANJA),
        ("Cubrir un intervalo", "de lo que no deja hueco, lo que llega más lejos", "09-2", MORADO),
        ("Emparejar extremos", "el más débil con el más fuerte, dos punteros", "08-2 · 09-3 · 09-4", C["green"]),
        ("Con cola de prioridad", "reutilizar lo que queda libre antes", "08-L", C["red"]),
        ("Voraz + otra técnica", "contar por tallas; Dijkstra y ordenar diferencias", "08-3 · 09-L", C["gold"])]


def e_patrones(f):
    texto(f, (640, 50), "Los patrones del curso", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, (tit, desc, ej, col) in enumerate(PATR):
        t0 = f.c(min(k + 1, 6))
        if f.t < t0:
            continue
        u = aparece(f, t0)
        x = 40 + (k % 2) * 610
        y = 100 + (k // 2) * 195
        f.d.rounded_rectangle((x, y, x + 590, y + 175), 16, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], col, u), width=3)
        f.d.text((x + 24, y + 36), tit, font=font(26, True), fill=mix(C["bot"], col, u), anchor="lm")
        f.d.text((x + 24, y + 90), desc, font=font(21), fill=mix(C["bot"], C["text"], u), anchor="lm")
        f.d.text((x + 24, y + 138), ej, font=font(20, True), fill=mix(C["bot"], C["muted"], u), anchor="lm")


def e_grafos(f):
    texto(f, (640, 70), "Ya conocías algoritmos voraces", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    items = [("Kruskal", "la arista más barata que no cierra ciclo", "tema 6", C["blue"]),
             ("Prim", "la arista más barata que sale del árbol", "tema 6", C["green"]),
             ("Dijkstra", "el vértice más cercano aún sin fijar", "tema 7", NARANJA)]
    for k, (n, d, t, col) in enumerate(items):
        if f.t < f.c(k + 1):
            continue
        u = aparece(f, f.c(k + 1))
        y = 180 + k * 130
        caja(f, 220, y, n, c=col, u=u, w=220, h=80, tam=28)
        texto(f, (360, y - 12), d, 26, "text", u)
        texto(f, (360, y + 24), t, 20, "muted", u)
    if f.t >= f.c(4):
        etiqueta(f, (640, 620), "en todos: una elección local que nunca se deshace, y una demostración", 24, "text", aparece(f, f.c(4)))


def e_vs_pd(f):
    f.box(60, 120, 560, 420, "voraz")
    f.box(660, 120, 560, 420, "programación dinámica")
    a = [("una sola elección por paso", "text"), ("nunca vuelve atrás", "text"), ("O(N log N) típico", "text"), ("necesita demostración", "gold")]
    b = [("prueba todas las opciones", "text"), ("guarda subproblemas", "text"), ("tabla: O(N·M) típico", "text"), ("correcta por la recurrencia", "gold")]
    for k in range(4):
        if f.t >= f.c(min(k, 3)):
            u = aparece(f, f.c(min(k, 3)))
            texto(f, (100, 190 + 80 * k), a[k][0], 26, a[k][1], u, fondo=C["panel"])
            texto(f, (700, 190 + 80 * k), b[k][0], 26, b[k][1], u, fondo=C["panel"])
    if f.t >= f.c(4):
        etiqueta(f, (640, 620), "monedas 1, 3, 4: la voraz falla, la dinámica (10-2) acierta", 24, "text", aparece(f, f.c(4)))


def e_cierre(f):
    cierre(f, "Algoritmos voraces", [
        "elegir lo mejor ahora y no volver atrás",
        "probar contraejemplos antes de fiarse",
        "demostrar con un argumento de intercambio",
        "casi siempre: ordenar + un bucle, O(N log N)",
    ])


ESC = [
    Escena("Algoritmos voraces: elegir lo que mejor parece en cada momento, y no volver atrás nunca.", e_portada, titulo="Portada", extra=1.0),
    Escena("Un algoritmo voraz construye la solución paso a paso, y en cada paso coge la opción que mejor parece ahora. "
           "Por ejemplo, devolver ochenta céntimos con monedas de cincuenta, veinte y diez. "
           "Cogemos siempre la moneda más grande que cabe: cincuenta, veinte y diez. "
           "Es rápido y sencillo, pero no siempre acierta.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Con monedas de uno, tres y cuatro, y seis céntimos que devolver: "
           "la voraz coge un cuatro y dos unos, tres monedas. "
           "Pero dos de tres son solo dos monedas. "
           "Por eso un voraz hay que demostrarlo, y antes conviene buscar contraejemplos pequeños.",
           e_falla, titulo="Cuándo falla", extra=1.5),
    Escena("La receta tiene cuatro pasos. "
           "Primero, el criterio: qué se coge antes, casi siempre ordenando por algo. "
           "Segundo, probar contraejemplos pequeños para descartar las ideas que fallan. "
           "Tercero, demostrarlo, normalmente con un argumento de intercambio. "
           "Y cuarto, programarlo: suele ser ordenar y un bucle.",
           e_receta, titulo="La receta", extra=1.5),
    Escena("La demostración por intercambio funciona así. "
           "Comparamos la solución voraz con una óptima cualquiera. "
           "En la primera diferencia, cambiamos lo que tiene el óptimo por lo que eligió la voraz: si sigue siendo válida y no es peor, bien. "
           "Repitiendo, el óptimo se convierte en la voraz sin empeorar. "
           "Así que la voraz también es óptima.",
           e_intercambio, titulo="Demostrar", extra=1.5),
    Escena("En el curso salen unos pocos patrones. "
           "La selección de actividades: ordenar por la hora de fin y coger lo compatible, como en la maratón de cine. "
           "Pinchar puntos o intervalos, poniendo cada parche o pasadizo lo más a la derecha posible. "
           "Cubrir un intervalo, eligiendo lo que llega más lejos sin dejar hueco. "
           "Emparejar extremos con dos punteros: invasiones, coches y telesilla. "
           "Usar una cola de prioridad, como en las salas de conferencias; y combinar el voraz con otra técnica: contar por tallas en las equipaciones, o Dijkstra en el agua.",
           e_patrones, titulo="Los patrones", extra=2.0),
    Escena("Y ya conocías algoritmos voraces de los temas de grafos. "
           "Kruskal coge siempre la arista más barata que no cierra un ciclo. "
           "Prim, la arista más barata que sale del árbol. "
           "Y Dijkstra fija siempre el vértice más cercano. "
           "Todos hacen una elección local que nunca se deshace, y cada uno tiene su demostración.",
           e_grafos, titulo="Voraces que ya conoces", extra=1.5),
    Escena("Frente a la programación dinámica, un voraz hace una sola elección por paso, "
           "no vuelve atrás, "
           "y suele costar ene log ene. "
           "Pero necesita demostración; la dinámica prueba todas las opciones y es correcta por la recurrencia. "
           "Con monedas de uno, tres y cuatro, la voraz falla y la dinámica de las dianas acierta.",
           e_vs_pd, titulo="Voraz frente a dinámica", extra=1.5),
    Escena("Resumiendo: elegir lo mejor ahora y no volver atrás; probar contraejemplos; demostrar con un intercambio; y programarlo, casi siempre, ordenando y con un bucle.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/08-0", "../08-0_algoritmos_voraces_teoria.mp4", "08-0")
