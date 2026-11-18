"""Vídeo EJ 09-1 · ¡En primera línea de playa! (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta

CPP = "../../9-Algoritmos voraces II/EJ_09-1/EJ_09-1.cpp"
TEMA = "Tema 9 · Algoritmos voraces II"
ED = [(2, 10), (12, 20), (1, 4), (6, 15)]          # (W, E) como en la entrada
ORD = sorted(ED, key=lambda e: e[1])
ALT = {(1, 4): 150, (2, 10): 230, (6, 15): 190, (12, 20): 260}
COLS = {(1, 4): C["blue"], (2, 10): C["purple"], (6, 15): NARANJA, (12, 20): C["green"]}
X0, X1, A, B = 100, 1180, 0, 21
YS = 470                    # suelo (paseo marítimo)


def X(v):
    return X0 + (v - A) * (X1 - X0) / (B - A)


def edificio(f, e, u=1.0, gris=False, ok=False, dy=0):
    if u <= 0:
        return
    w, E = e
    c = C["dim"] if gris else COLS[e]
    h = ALT[e] * u
    x0, x1 = X(w), X(E)
    f.d.rectangle((x0, YS - h + dy, x1, YS + dy), fill=mix(C["bot"], mix(C["panel"], c, 0.35), 1), outline=c, width=3)
    for r in range(int(h // 40)):
        for k in range(int((x1 - x0 - 20) // 30)):
            xx, yy = x0 + 14 + k * 30, YS - h + 16 + r * 40 + dy
            f.d.rectangle((xx, yy, xx + 12, yy + 16), fill=mix(C["panel"], c, 0.6))
    if ok:
        tick(f, (x0 + x1) / 2, YS - h - 26 + dy, True)


def playa(f, u=1.0):
    f.d.rectangle((0, YS, W, YS + 70), fill=mix(C["bot"], (60, 66, 84), u))
    f.d.rectangle((0, YS + 70, W, H), fill=mix(C["bot"], (220, 190, 120), u))
    for k in range(20):
        x = k * 70 + (f.t * 15) % 70
        f.d.arc((x - 30, H - 30, x + 30, H - 10), 180, 360, fill=mix(C["bot"], (120, 190, 255), u), width=3)
    for v in range(A, B + 1):
        f.d.line((X(v), YS + 62, X(v), YS + 70), fill=mix(C["bot"], C["muted"], u), width=1)
        if v % 2 == 0:
            f.d.text((X(v), YS + 50), str(v), font=font(14, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


def pasadizo(f, x, u=1.0, c=None):
    """Pasadizo en el metro [x, x+1], bajo el paseo hacia la playa."""
    if u <= 0:
        return
    c = c or C["gold"]
    f.d.rectangle((X(x), YS, X(x + 1), YS + 70 * u), fill=mix(C["bot"], (30, 30, 36), u), outline=mix(C["bot"], c, u), width=3)


def e_portada(f):
    def dib(f):
        for k, (x, h) in enumerate([(780, 140), (880, 200), (990, 160)]):
            u = f.p(0.3 + 0.2 * k, 0.6)
            f.d.rectangle((x, 420 - h * u, x + 90, 420), fill=mix(C["bot"], (60, 80, 120), u), outline=mix(C["bot"], C["blue"], u), width=3)
        f.d.rectangle((760, 420, 1100, 460), fill=(220, 190, 120))
    portada(f, "EJ 09-1", "¡En primera línea de playa!", TEMA, dib)


def e_problema(f):
    playa(f, aparece(f, f.c(0)))
    for k, e in sorted(enumerate(ED), key=lambda ke: -ALT[ke[1]]):
        edificio(f, e, f.lin(f.c(0) + 0.3 * k, 0.8))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        pasadizo(f, 3, u)
        texto(f, (X(3.5), 130), "pasadizo de 1 m", 22, "gold", u, anchor="mm")
        flecha(f, (X(3.5), 145), (X(3.5), YS - 160), mix(C["bot"], C["gold"], u), w=3)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 80), "tiene que quedar ENTERO debajo del edificio:  W ≤ x  y  x + 1 ≤ E", 24, "text", u, mono=True, anchor="mm")
    if f.t >= f.c(3):
        etiqueta(f, (640, 620), "¿mínimo de pasadizos para que todos tengan uno?", 26, "gold", aparece(f, f.c(3)))


def traza():
    pas, x, ev = 0, None, []
    for (w, E) in ORD:
        nuevo = pas == 0 or w > x
        if nuevo:
            pas += 1
            x = E - 1
        ev.append(((w, E), nuevo, x))
    return ev


EV = traza()


def e_voraz(f):
    playa(f)
    k, fr = paso_idx(f, f.c(1), f.c(4), len(EV))
    pas = []
    for q, (e, nuevo, x) in sorted(enumerate(EV), key=lambda qe: -ALT[qe[1][0]]):
        listo = q < k or (q == k and fr > 0.4)
        edificio(f, e, ok=listo and f.t >= f.c(1))
        if listo and nuevo and f.t >= f.c(1):
            pas.append((x, q))
    for x, q in pas:
        tq = f.c(1) + (q + 0.4) * (f.c(4) - f.c(1)) / len(EV)
        pasadizo(f, x, f.lin(tq, 0.5))
    texto(f, (640, 70), "ordenados por el extremo ESTE", 26, "muted", aparece(f, f.c(0)), anchor="mm")
    if 0 <= k < len(EV):
        (w, E), nuevo, x = EV[k]
        f.d.line((X(E), 110, X(E), YS), fill=C["gold"], width=2)
        s = f"[{w}, {E}]: " + (f"pasadizo nuevo en [{E - 1}, {E}], lo más al este" if nuevo else f"{w} ≤ {x}: ya tiene")
        etiqueta(f, (640, 620), s, 26, NARANJA if nuevo else "green", 1)
    elif k >= len(EV):
        etiqueta(f, (640, 620), f"{len(set(p for p, _ in pas))} pasadizos", 32, "green", aparece(f, f.c(4)))


def e_porque(f):
    playa(f)
    e1 = (1, 4)
    edificio(f, (2, 10))
    edificio(f, e1)
    u = aparece(f, f.c(0))
    x = 1 if f.t < f.c(1) else lerp(1, 3, ease(f.lin(f.c(1), 1.2)))
    pasadizo(f, x, u, c=C["purple"])
    texto(f, (640, 80), "cualquier pasadizo del primero está en su trozo", 24, "text", u, anchor="mm")
    if f.t >= f.c(1):
        texto(f, (640, 130), "moverlo al este, hasta [E−1, E], no hace perder a nadie", 24, "gold", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        etiqueta(f, (640, 620), "y puede servir a más edificios que empiezan después", 26, "green", aparece(f, f.c(2)))


A_L = find_line(CPP, "vector<pair<int, int>> edif(N);")
B_L = find_line(CPP, "cout << pasadizos")
CODE = codigo(CPP, A_L, B_L, maxc=76)
L_IF = find_line(CPP, "if (pasadizos == 0 || W > x) {")
L_X = find_line(CPP, "x = E - 1;")
L_SO = find_line(CPP, "sort(edif.begin(), edif.end());")


def e_codigo(f):
    hl = {A_L, A_L + 1}
    if f.t >= f.c(1):
        hl = {L_SO}
    k, fr = paso_idx(f, f.c(2), f.T - 2.5, len(EV))
    if 0 <= k < len(EV):
        hl = {L_IF} if fr < 0.5 or not EV[k][1] else {L_IF, L_X - 1, L_X}
    elif k >= len(EV):
        hl = {B_L}
    f.code(20, 90, 760, 440, CODE, hl=hl, title="pinchar intervalos", size=18)
    x0 = 830
    texto(f, (x0, 110), "pares (E, W) ordenados", 18, "muted", 1)
    pas, x = 0, None
    for q, ((w, E), nuevo, xx) in enumerate(EV):
        hecho = q < k or (q == k and fr >= 0.5)
        caja(f, x0 + 90, 170 + q * 62, f"({E}, {w})", c="gold" if q == k else COLS[(w, E)], w=150, h=46, tam=22, borde=5 if q == k else 2)
        if hecho:
            if nuevo:
                pas, x = pas + 1, xx
            tick(f, x0 + 200, 170 + q * 62, True)
    texto(f, (x0, 440), f"x = {x if x is not None else -1}", 26, "gold", 1, mono=True)
    texto(f, (x0, 480), f"pasadizos = {pas}", 26, "green", 1, mono=True)


def e_detalles(f):
    f.box(60, 120, 1160, 440)
    items = [("se guarda (E, W) para que sort ordene directamente por el extremo este", "text"),
             ("basta mirar W ≤ x: como su E es mayor o igual, x + 1 ≤ E ya se cumple", "text"),
             ("pasadizos == 0: el primer edificio siempre necesita uno", "text"),
             ("N ≤ 100.000:  O(N log N) por la ordenación", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 95 * k), s, 25, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "¡En primera línea de playa!", [
        "pinchar intervalos con el mínimo de puntos",
        "ordenar por el extremo este",
        "pasadizo nuevo, lo más al este posible: [E−1, E]",
        "un edificio ya está servido si W ≤ x · O(N log N)",
    ])


ESC = [
    Escena("En primera línea de playa. Cuántos pasadizos hacen falta para que todos los edificios tengan salida al mar.", e_portada, titulo="Portada", extra=1.0),
    Escena("En el paseo marítimo hay edificios, cada uno ocupa desde su extremo oeste hasta su extremo este. "
           "Queremos excavar pasadizos de un metro de ancho hasta la playa. "
           "A un edificio le sirve un pasadizo si queda entero debajo de él. "
           "¿Cuántos pasadizos hacen falta como mínimo?",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Ordenamos los edificios por su extremo este. "
           "El que acaba antes necesita un pasadizo, y lo ponemos lo más al este posible, en su último metro. "
           "Así sirve también a todos los que empiezan antes de ese metro. "
           "Seguimos: si un edificio ya tiene el pasadizo debajo, nada; si no, otro pasadizo en su último metro. "
           "En el ejemplo bastan dos.",
           e_voraz, titulo="La voraz", extra=1.5),
    Escena("¿Por qué el último metro? Cualquier pasadizo del primer edificio está dentro de él. "
           "Si lo movemos al este, hasta el último metro, sigue sirviendo a los mismos edificios, porque todos acaban más tarde. "
           "Y puede servir a otros que empiezan después.",
           e_porque, titulo="Por qué funciona", extra=1.5),
    Escena("En el código, cada edificio se guarda como el par E, W, para que sort los ordene por el extremo este. "
           "Después se ordenan. "
           "Y se recorren: si es el primero o su W es mayor que x, se pone un pasadizo nuevo en E menos uno.",
           e_codigo, titulo="El código", extra=4.0),
    Escena("Guardar E primero ahorra escribir un comparador. "
           "Basta comprobar W menor o igual que x, porque el E de los siguientes es mayor o igual. "
           "La condición pasadizos igual a cero hace que el primero siempre tenga uno. "
           "Y el coste es ene log ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: es pinchar intervalos. Se ordenan por el extremo este y cada pasadizo nuevo se pone lo más al este posible.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/09-1", "../09-1_en_primera_linea_de_playa.mp4", "09-1")
