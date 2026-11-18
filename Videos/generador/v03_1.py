"""Vídeo EJ 03-1 · Volando drones (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo

CPP = "../../3-Colas de prioridad variable (Heapsort)/EJ_03-1/EJ_03-1.cpp"
TEMA = "Tema 3 · Colas de prioridad variable"
N = 2
P9 = [5, 12, 7, 15]
P1 = [20, 20, 2]


def simula():
    """Lista de sábados: [(cajas9 antes, cajas1 antes, [(h9, h1, vuela)], total, cajas9 después, cajas1 después)]."""
    c9 = sorted(P9, reverse=True)
    c1 = sorted(P1, reverse=True)
    sab = []
    while c9 and c1:
        a9, a1 = list(c9), list(c1)
        vuelos, s9, s1 = [], [], []
        for _ in range(N):
            if not c9 or not c1:
                break
            h9, h1 = c9.pop(0), c1.pop(0)
            t = min(h9, h1)
            vuelos.append((h9, h1, t))
            if h9 - t > 0:
                s9.append(h9 - t)
            if h1 - t > 0:
                s1.append(h1 - t)
        c9 = sorted(c9 + s9, reverse=True)
        c1 = sorted(c1 + s1, reverse=True)
        sab.append((a9, a1, vuelos, sum(v[2] for v in vuelos), list(c9), list(c1), s9, s1))
    return sab


SAB = simula()


def pila(f, x, y, h, maxh=20, u=1.0, c=None, tipo="9V", w=58, alto=120, gris=False):
    if u <= 0:
        return
    c = C["dim"] if gris else (c or (C["red"] if tipo == "9V" else C["green"]))
    f.d.rounded_rectangle((x - w / 2, y - alto, x + w / 2, y), 8, fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
    lv = max(0.0, min(1.0, h / maxh))
    if lv > 0:
        f.d.rectangle((x - w / 2 + 6, y - 6 - (alto - 12) * lv, x + w / 2 - 6, y - 6), fill=mix(C["bot"], mix(C["panel"], c, 0.6), u))
    f.d.text((x, y - alto / 2), f"{h}h", font=font(20, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def dron(f, x, y, u=1.0, giro=0.0):
    if u <= 0:
        return
    c = mix(C["bot"], (200, 210, 225), u)
    f.d.rounded_rectangle((x - 40, y - 14, x + 40, y + 14), 8, fill=c)
    for dx in (-60, 60):
        f.d.line((x + dx * 0.6, y, x + dx, y - 18), fill=c, width=4)
        a = 22 + 10 * abs((giro * 8) % 2 - 1)
        f.d.line((x + dx - a, y - 22, x + dx + a, y - 22), fill=c, width=4)


def caja_pilas(f, x0, y, alturas, tipo, u=1.0, titulo=True, marca_top=False):
    if titulo:
        texto(f, (x0, y - 160), "caja de 9 V" if tipo == "9V" else "caja de 1,5 V", 22, "red" if tipo == "9V" else "green", u)
    for k, h in enumerate(alturas):
        pila(f, x0 + 30 + k * 76, y, h, u=u, tipo=tipo)
    if marca_top and alturas:
        f.d.rectangle((x0 - 4, y - 128, x0 + 64, y + 6), outline=C["gold"], width=3)


def e_portada(f):
    def dib(f):
        dron(f, 960, 300 + 10 * (f.t % 1), f.p(0.3, 0.6), giro=f.t)
        pila(f, 920, 470, 15, u=f.p(0.6, 0.5), alto=90)
        pila(f, 1000, 470, 20, u=f.p(0.8, 0.5), tipo="1V", alto=90)
    portada(f, "EJ 03-1", "Volando drones", TEMA, dib)


def e_problema(f):
    u = aparece(f, f.c(0))
    caja_pilas(f, 80, 600, P9, "9V", u)
    caja_pilas(f, 760, 600, P1, "1V", aparece(f, f.c(0) + 0.4))
    if f.t >= f.c(1):
        u1 = aparece(f, f.c(1))
        for k in range(N):
            dron(f, 480 + k * 320, 150, u1, giro=f.t)
        texto(f, (640, 230), f"{N} drones · cada uno: una pila de cada tipo", 24, "gold", u1, anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 320), "cada sábado: las dos pilas MÁS cargadas; vuela min(h9, h1)", 24, "text", aparece(f, f.c(2)))
    if f.t >= f.c(3):
        etiqueta(f, (640, 380), "horas totales de cada sábado, mientras queden pilas de los dos tipos", 22, "muted", aparece(f, f.c(3)))


def e_sabado(f, s, t0, t1, mostrar_codigo=False):
    a9, a1, vuelos, total, d9, d1, s9, s1 = SAB[s]
    k, fr = paso_idx(f, t0, t1, len(vuelos) + 1)
    # cajas: van perdiendo las de arriba
    usados = min(len(vuelos), max(0, k + (1 if fr > 0.2 else 0))) if f.t >= t0 else 0
    if k > len(vuelos) - 1 and f.t >= t0 and k >= len(vuelos):
        caja_pilas(f, 80, 600, d9, "9V")
        caja_pilas(f, 760, 600, d1, "1V")
    else:
        caja_pilas(f, 80, 600, a9[usados:], "9V", marca_top=True)
        caja_pilas(f, 760, 600, a1[usados:], "1V", marca_top=True)
    horas = 0
    for q, (h9, h1, t) in enumerate(vuelos):
        xd = 400 + q * 480
        dron(f, xd, 130, giro=f.t)
        if q < usados:
            tq = t0 + (q + 0.2) * (t1 - t0) / (len(vuelos) + 1)
            u = f.lin(tq, 1.0)
            left = mix(C["bot"], C["text"], 1)
            r9, r1 = (h9 - t, h1 - t) if u >= 1 else (h9, h1)
            pila(f, xd - 40, 280, r9, tipo="9V", alto=90, gris=r9 == 0)
            pila(f, xd + 40, 280, r1, tipo="1V", alto=90, gris=r1 == 0)
            if u >= 1:
                texto(f, (xd, 320), f"vuela {t} h", 24, "gold", 1, anchor="mm")
                horas += t
    texto(f, (640, 380), f"sábado {s + 1}:  {horas} h", 30, "green", 1 if f.t >= t0 else 0, anchor="mm")
    if k >= len(vuelos) and f.t >= t0 and s < len(SAB) - 1:
        if s9 or s1:
            etiqueta(f, (640, 690), "las que aún tienen carga vuelven a su caja al acabar el sábado", 22, "text", 1)


def e_sab1(f):
    e_sabado(f, 0, f.c(1), f.c(3))
    texto(f, (640, 40), "las cajas son colas de MÁXIMOS: arriba, la más cargada", 22, "muted", aparece(f, f.c(0)), anchor="mm")


def e_sab2(f):
    e_sabado(f, 1, f.c(0), f.c(2))
    if f.t >= f.c(2):
        etiqueta(f, (640, 690), "la caja de 9 V se ha vaciado: fin.   Salida:  27 12", 26, "gold", aparece(f, f.c(2)), mono=False)


def e_aparte(f):
    texto(f, (640, 70), "¿por qué apartar las sobrantes hasta el final del sábado?", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    u = aparece(f, f.c(1))
    dron(f, 380, 200, u, giro=f.t)
    dron(f, 900, 200, u, giro=f.t)
    pila(f, 340, 360, 0, tipo="9V", alto=90, u=u, gris=True)
    pila(f, 420, 360, 5, tipo="1V", alto=90, u=u)
    if f.t >= f.c(1):
        p = mueve((420, 360), (940, 360), f.lin(f.c(1) + 0.4, 1.0))
        pila(f, p[0], p[1], 5, tipo="1V", alto=90, c=C["red"] if f.t >= f.c(1) + 1.4 else None)
        if f.t >= f.c(1) + 1.4:
            tick(f, 940, 420, False)
            etiqueta(f, (640, 520), "una pila no puede ir en dos drones el mismo sábado", 24, "red", 1)
    if f.t >= f.c(2):
        etiqueta(f, (640, 600), "se guardan en sobran9V / sobran1V y se reinsertan con push al final", 22, "text", aparece(f, f.c(2)))


A_L = find_line(CPP, "while (!cola1V.empty() && !cola9V.empty()) {")
B_L = find_line(CPP, "primero = false;")
CODE = [(n, t) for n, t in codigo(CPP, A_L, B_L + 1, maxc=88) if not t.strip().startswith("//")]
L_TOP = find_line(CPP, "auto p9 = cola9V.top();")
L_MIN = find_line(CPP, "int tiempo = min(p9.prioridad, p1.prioridad);")
L_SOB = find_line(CPP, "if (p9.prioridad > 0) sobran9V.push_back")
L_RE = find_line(CPP, "for (auto& s : sobran9V) cola9V.push")
L_OUT = find_line(CPP, "cout << horasFinde;")


def e_codigo(f):
    marcas = [(f.c(0), {A_L}), (f.c(1), {L_TOP, L_TOP + 1}), (f.c(2), {L_MIN, L_MIN + 1}),
              (f.c(3), {L_SOB, L_SOB + 1}), (f.c(4), {L_RE, L_RE + 1, L_OUT})]
    hl = {A_L}
    for t, h in marcas:
        if f.t >= t:
            hl = h
    f.code(20, 70, 1240, 620, CODE, hl=hl, title="un sábado por vuelta", size=16)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("IndexPQ de máximos: índice = nº de pila, prioridad = horas que le quedan", "text"),
             ("aquí se usa como un montículo normal: push, top y pop (nunca update)", "text"),
             ("puede haber 0 drones: se escribe 0", "text"),
             ("cada pila entra y sale O(log n) veces por sábado", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 24, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "Volando drones", [
        "dos colas de máximos, una por tipo de pila",
        "cada dron: top + pop de cada caja, vuela el mínimo",
        "las sobrantes se apartan y vuelven al final del sábado",
        "se escribe el total de cada sábado",
    ])


ESC = [
    Escena("Volando drones. Cuántas horas se vuela cada sábado con las pilas que tenemos.", e_portada, titulo="Portada", extra=1.0),
    Escena("Tenemos una caja de pilas de nueve voltios y otra de uno coma cinco, cada pila con las horas de carga que le quedan. "
           "Y ene drones; aquí, dos. Cada uno necesita una pila de cada tipo. "
           "Cada sábado, a cada dron se le ponen las dos pilas más cargadas, y vuela hasta que se agota una de ellas: el mínimo de las dos. "
           "Hay que escribir las horas de vuelo de cada sábado, mientras quede alguna pila de cada tipo.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Cada caja es una cola de prioridad de máximos: arriba está la pila más cargada. "
           "El primer dron coge quince y veinte, y vuela quince horas. El segundo, doce y veinte, y vuela doce. "
           "La pila de nueve voltios se gasta, y a las de uno coma cinco les quedan cinco y ocho horas. "
           "Sábado uno: veintisiete horas.",
           e_sab1, titulo="Sábado 1", extra=2.0),
    Escena("Al acabar el sábado, las sobrantes vuelven a su caja. "
           "Sábado dos: siete con ocho, siete horas; y cinco con cinco, cinco horas. Doce en total. "
           "Ya no quedan pilas de nueve voltios, así que se acaba: veintisiete y doce.",
           e_sab2, titulo="Sábado 2", extra=2.0),
    Escena("¿Por qué no se devuelve la pila a la caja en cuanto el dron aterriza? "
           "Porque entonces otro dron podría cogerla ese mismo sábado, y una pila no puede ir en dos drones a la vez. "
           "Se apartan en dos vectores y se reinsertan al final del sábado.",
           e_aparte, titulo="Apartar las sobrantes", extra=1.5),
    Escena("En el código, un bucle por sábado, mientras las dos colas tengan pilas. "
           "Para cada dron, top y pop de cada cola. "
           "Vuela el mínimo, que se suma y se resta a las dos pilas. "
           "Las que siguen con carga se apartan. "
           "Al final se reinsertan con push y se escribe el total.",
           e_codigo, titulo="El código", extra=2.5),
    Escena("Se usa una IndexPQ de máximos, con el número de pila como índice y las horas como prioridad. "
           "Pero aquí funciona como un montículo normal: solo push, top y pop. "
           "Si hay cero drones, se escribe cero. "
           "Y cada operación cuesta logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: dos colas de máximos; cada dron saca la mejor pila de cada una y vuela el mínimo; las sobrantes vuelven al final del sábado.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/03-1", "../03-1_volando_drones.mp4", "03-1")
