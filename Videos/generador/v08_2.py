"""Vídeo EJ 08-2 · ¡Nos invaden! (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview

CPP = "../../8-Algoritmos voraces/EJ_08-2/EJ_08-2.cpp"
TEMA = "Tema 8 · Algoritmos voraces"
ENE = [40, 20, 80, 30]          # ejemplo 1, sin ordenar
EQU = [35, 50, 25, 40]
ENS, EQS = sorted(ENE), sorted(EQU)


def castillo(f, x, y, v, u=1.0, estado=None, w=96):
    """Ciudad: castillo con los enemigos encima. estado: None, 'gana', 'pierde'."""
    if u <= 0:
        return
    c = mix(C["bot"], (120, 128, 150), u)
    d = f.d
    d.rectangle((x - w / 2, y - 40, x + w / 2, y + 30), fill=c)
    for k in range(4):
        xx = x - w / 2 + k * (w / 3.5)
        d.rectangle((xx, y - 56, xx + w / 7, y - 40), fill=c)
    d.rectangle((x - 12, y + 4, x + 12, y + 30), fill=mix(C["bot"], (60, 66, 84), u))
    rc = C["red"]
    if estado == "gana":
        rc = C["green"]
    caja(f, x, y - 92, v, c=rc, u=u, w=70, h=44, tam=24)


def escudo(f, x, y, v, u=1.0, gris=False):
    if u <= 0:
        return
    c = C["dim"] if gris else C["blue"]
    d = f.d
    pts = [(x - 34, y - 34), (x + 34, y - 34), (x + 34, y + 4), (x, y + 40), (x - 34, y + 4)]
    d.polygon(pts, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u))
    d.line(pts + [pts[0]], fill=mix(C["bot"], c, u), width=4)
    d.text((x, y - 4), str(v), font=font(24, True), fill=mix(C["bot"], C["dim"] if gris else C["text"], u), anchor="mm")


XC = [280, 520, 760, 1000]
YC, YE = 260, 560


def e_portada(f):
    def dib(f):
        castillo(f, 900, 330, 30, u=f.p(0.3, 0.6))
        escudo(f, 1080, 360, 35, u=f.p(0.6, 0.6))
    portada(f, "EJ 08-2", "¡Nos invaden!", TEMA, dib)


def e_problema(f):
    for k, v in enumerate(ENE):
        castillo(f, XC[k], YC, v, aparece(f, f.c(0) + 0.2 * k))
    for k, v in enumerate(EQU):
        escudo(f, XC[k], YE, v, aparece(f, f.c(1) + 0.2 * k))
    if f.t >= f.c(1):
        texto(f, (40, 110), "ciudades", 22, "red", aparece(f, f.c(0)))
        texto(f, (40, 470), "equipos", 22, "blue", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 680), "se gana si  equipo ≥ enemigos", 30, "gold", u, mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 420), "un equipo por ciudad · ¿máximo de victorias?", 26, "text", aparece(f, f.c(3)), anchor="mm")


def e_desperdicio(f):
    # mini ejemplo: ciudades 10, 30; equipos 15, 40
    izq, der = 330, 950
    texto(f, (izq, 90), "mal", 34, "red", aparece(f, f.c(1)), anchor="mm")
    texto(f, (der, 90), "bien", 34, "green", aparece(f, f.c(2)), anchor="mm")
    for base, t0, asig in [(izq, f.c(1), {0: 40, 1: 15}), (der, f.c(2), {0: 15, 1: 40})]:
        u = aparece(f, f.c(0))
        xs = [base - 130, base + 130]
        for k, v in enumerate([10, 30]):
            castillo(f, xs[k], 300, v, u)
        if f.t < t0:
            escudo(f, base - 130, 560, 15, u)
            escudo(f, base + 130, 560, 40, u)
            continue
        for k in (0, 1):
            e = asig[k]
            src = (base - 130, 560) if e == 15 else (base + 130, 560)
            p = mueve(src, (xs[k], 420), f.lin(t0, 1.0))
            escudo(f, p[0], p[1], e)
            if f.t >= t0 + 1.0:
                ok = e >= [10, 30][k]
                tick(f, xs[k] + 60, 420, ok)
        if f.t >= t0 + 1.2:
            n = sum(asig[k] >= [10, 30][k] for k in (0, 1))
            texto(f, (base, 560), f"{n} victoria" + ("s" if n > 1 else ""), 30, "green" if n == 2 else "red", aparece(f, t0 + 1.2), anchor="mm")
    if f.t >= f.c(1) + 1.2:
        texto(f, (izq, 620), "el 40 se desperdicia con el 10", 22, "muted", aparece(f, f.c(1) + 1.2), anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 680), "a cada ciudad, el equipo MÁS PEQUEÑO que la gana", 28, "gold", aparece(f, f.c(3)), anchor="mm")


def traza():
    """Pasos de la voraz sobre los vectores ordenados: (j, i, gana)."""
    pasos, i = [], 0
    for j in range(len(EQS)):
        if i >= len(ENS):
            break
        g = EQS[j] >= ENS[i]
        pasos.append((j, i, g))
        if g:
            i += 1
    return pasos


PASOS = traza()


def e_voraz(f):
    # ordenar: los elementos se recolocan
    u = f.lin(f.c(0) + 0.3, 1.5)
    for k, v in enumerate(ENE):
        x = lerp(XC[k], XC[ENS.index(v)], ease(u))
        castillo(f, x, YC, v)
    k_paso, fr = paso_idx(f, f.c(1), f.c(4), len(PASOS))
    usados = {}
    descartados = set()
    for q in range(max(0, min(k_paso + 1, len(PASOS)))):
        j, i, g = PASOS[q]
        if g:
            usados[j] = i
        else:
            descartados.add(j)
    for k, v in enumerate(EQU):
        x = lerp(XC[k], XC[EQS.index(v)], ease(u))
        j = EQS.index(v)
        if j in usados and f.t >= f.c(1):
            q = [q for q, p in enumerate(PASOS) if p[0] == j][0]
            t_q = f.c(1) + q * (f.c(4) - f.c(1)) / len(PASOS)
            p = mueve((XC[j], YE), (XC[usados[j]], YC + 110), f.lin(t_q, 0.8))
            escudo(f, p[0], p[1], v)
            if f.t >= t_q + 0.8:
                tick(f, XC[usados[j]] + 62, YC + 110, True)
        else:
            escudo(f, x, YE, v, gris=j in descartados)
            if j in descartados:
                tick(f, XC[j] + 60, YE, False)
    if f.t >= f.c(1) and k_paso < len(PASOS):
        j, i, g = PASOS[max(0, k_paso)]
        f.d.polygon([(XC[i] - 12, YC - 140), (XC[i] + 12, YC - 140), (XC[i], YC - 124)], fill=C["gold"])
        texto(f, (XC[i], YC - 160), "i", 22, "gold", 1, mono=True, anchor="mm")
        f.d.polygon([(XC[j] - 12, YE + 66), (XC[j] + 12, YE + 66), (XC[j], YE + 50)], fill=C["gold"])
        texto(f, (XC[j], YE + 86), "j", 22, "gold", 1, mono=True, anchor="mm")
        s = f"{EQS[j]} ≥ {ENS[i]}" if g else f"{EQS[j]} < {ENS[i]}: no gana a ninguna"
        texto(f, (1150, 420), s, 26, "green" if g else "red", 1, mono=True, anchor="mm")
    texto(f, (60, 90), "ordenados de menor a mayor", 22, "muted", aparece(f, f.c(0)))
    if f.t >= f.c(4):
        texto(f, (1150, 420), "3 victorias", 34, "green", aparece(f, f.c(4)), anchor="mm")


def e_porque(f):
    # intercambio: solución con 50 en la ciudad 20 y 25 en la 30 → se intercambian
    xs = [420, 860]
    for k, v in enumerate([20, 30]):
        castillo(f, xs[k], 260, v, aparece(f, f.c(0)))
    asign = [50, 25] if f.t < f.c(1) + 0.3 else [25, 50]
    u = f.lin(f.c(1) + 0.3, 1.2)
    if f.t >= f.c(0):
        pa = mueve((xs[0], 400), (xs[1], 400), u) if f.t >= f.c(1) + 0.3 else (xs[0], 400)
        pb = mueve((xs[1], 400), (xs[0], 400), u) if f.t >= f.c(1) + 0.3 else (xs[1], 400)
        escudo(f, pa[0], pa[1], 50, aparece(f, f.c(0)))
        escudo(f, pb[0], pb[1], 25, aparece(f, f.c(0)))
        if f.t < f.c(1) + 0.3:
            tick(f, xs[0] + 62, 400, True, aparece(f, f.c(0)))
            tick(f, xs[1] + 62, 400, False, aparece(f, f.c(0)))
        elif u >= 1:
            tick(f, xs[0] + 62, 400, True)
            tick(f, xs[1] + 62, 400, True)
    texto(f, (640, 520), "intercambiar nunca empeora", 30, "gold", aparece(f, f.c(2)), anchor="mm")
    texto(f, (640, 580), "siempre hay una solución óptima que hace lo mismo que la voraz", 24, "muted", aparece(f, f.c(2) + 0.4), anchor="mm")


A = find_line(CPP, "sort(enemigos.begin()")
B = find_line(CPP, "cout << victorias")
CODE = codigo(CPP, A, B, maxc=60)
L_IF = find_line(CPP, "if (equipos[j] >= enemigos[i])")
L_V = find_line(CPP, "++victorias;")


def e_codigo(f):
    hl = {A, A + 1}
    k_paso, fr = paso_idx(f, f.c(1), f.T - 3.0, len(PASOS))
    if 0 <= k_paso < len(PASOS):
        j, i, g = PASOS[k_paso]
        hl = {L_IF} if fr < 0.5 or not g else {L_IF, L_V, L_V + 1}
    elif k_paso >= len(PASOS):
        hl = {B}
    f.code(30, 90, 640, 440, CODE, hl=hl, title="voraz", size=19)
    # vectores a la derecha
    x0 = 760
    texto(f, (x0, 160), "enemigos", 20, "red", 1)
    texto(f, (x0, 320), "equipos", 20, "blue", 1)
    ii = jj = None
    if 0 <= k_paso < len(PASOS):
        jj, ii, g = PASOS[k_paso]
    vict = sum(1 for q in range(max(0, min(k_paso + (1 if fr >= 0.5 else 0), len(PASOS)))) if PASOS[q][2])
    for k in range(4):
        caja(f, x0 + 40 + k * 110, 230, ENS[k], c="gold" if k == ii else "red", w=86, borde=5 if k == ii else 3)
        caja(f, x0 + 40 + k * 110, 390, EQS[k], c="gold" if k == jj else "blue", w=86, borde=5 if k == jj else 3)
    texto(f, (x0, 480), f"victorias = {vict}", 30, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("≥ y no >: con los mismos efectivos también se gana  (40 contra 40)", "text"),
             ("un equipo que no gana a la ciudad más fácil no gana a ninguna", "text"),
             ("N ≤ 300.000:  O(N log N) por las dos ordenaciones; el recorrido es lineal", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 180 + 110 * k), s, 26, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "¡Nos invaden!", [
        "ordenar ciudades y equipos",
        "a la ciudad más fácil, el equipo más pequeño que la gana",
        "si no gana a la más fácil, se descarta",
        "intercambio: la voraz es óptima · O(N log N)",
    ])


ESC = [
    Escena("¡Nos invaden! Asignar equipos de defensa a ciudades para ganar el máximo de batallas.", e_portada, titulo="Portada", extra=1.0),
    Escena("Hay ene ciudades invadidas, cada una con sus enemigos. "
           "Y ene equipos de defensa, cada uno con sus efectivos. "
           "Un equipo gana seguro si tiene al menos tantos efectivos como el enemigo. "
           "Se manda un equipo a cada ciudad, y hay que conseguir el máximo de victorias.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Mira este caso pequeño: ciudades con diez y treinta enemigos, y equipos de quince y cuarenta. "
           "Si mandamos el de cuarenta a la ciudad de diez, gana, pero el de quince pierde contra treinta: una victoria. "
           "Si mandamos el de quince a la de diez, ganan los dos. "
           "La idea: a cada ciudad, el equipo más pequeño que la gana. Los grandes se guardan para las difíciles.",
           e_desperdicio, titulo="No desperdiciar", extra=1.5),
    Escena("Ordenamos las ciudades y los equipos de menor a mayor. "
           "Con i señalamos la ciudad más fácil sin defender, y recorremos los equipos con j. "
           "Si el equipo gana a esa ciudad, se la queda y pasamos a la siguiente ciudad. "
           "Si no gana ni a la más fácil, no gana a ninguna: se descarta. "
           "En el ejemplo, tres victorias.",
           e_voraz, titulo="La voraz", extra=1.5),
    Escena("¿Por qué es óptimo? Supón una solución que defiende la ciudad fácil con un equipo grande, y otra ciudad con uno pequeño que pierde. "
           "Si los intercambiamos, el pequeño gana la fácil y el grande gana la otra. "
           "Intercambiar nunca empeora, así que siempre hay una solución óptima que hace lo mismo que la voraz.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, primero se ordenan los dos vectores. "
           "Luego un solo bucle recorre los equipos: si el equipo jota gana a la ciudad i, se suma una victoria y se avanza i. "
           "Al final se escribe el número de victorias.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Ojo con la condición: es mayor o igual, con los mismos efectivos también se gana. "
           "Un equipo que no gana a la ciudad más fácil se manda a una que se pierde de todas formas. "
           "Y el coste es ene log ene, por las dos ordenaciones.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: se ordena todo, a la ciudad más fácil se le manda el equipo más pequeño que la gana, "
           "y los que no ganan a ninguna se descartan. El argumento de intercambio demuestra que es óptimo.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/08-2", "../08-2_nos_invaden.mp4", "08-2")
