"""Vídeo EJ 12-1 · El carpintero Ebanisto (animado)."""
import os
import re
import sys
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, formula, codigo, portada, cierre, Tabla
from vor_comun import caja, paso_idx, tick, args_preview, etiqueta

CPP = "../../12-Evaluacion/EJ_12-1/EJ_12-1.cpp"
TEMA = "Tema 12 · Programación dinámica III"
L, MARCAS = 10, [3, 6, 8]
MADERA, MADERA_O = (196, 140, 84), (130, 86, 44)


def resuelve(L, marcas):
    """Mismo algoritmo que el .cpp: por longitud de intervalo d = j - i creciente."""
    p = [0] + marcas + [L]
    P = len(p)
    e = [[0] * P for _ in range(P)]
    mejor_k = {}
    orden = []
    for d in range(2, P):
        for i in range(P - d):
            j = i + d
            mejor, mk = -1, None
            for k in range(i + 1, j):
                v = e[i][k] + e[k][j]
                if mejor < 0 or v < mejor:
                    mejor, mk = v, k
            e[i][j] = 2 * (p[j] - p[i]) + mejor
            mejor_k[(i, j)] = mk
            orden.append((i, j))
    return p, e, mejor_k, orden


PT, E, MK, ORDEN = resuelve(L, MARCAS)
NP = len(PT)
assert E[0][NP - 1] == 40 and resuelve(20, [8, 10, 15, 17])[1][0][5] == 88


def coste_orden(L, orden):
    cortes, tot, partes = [0, L], 0, []
    for c in orden:
        a = max(x for x in cortes if x < c)
        b = min(x for x in cortes if x > c)
        tot += 2 * (b - a)
        partes.append((c, a, b, 2 * (b - a)))
        cortes.append(c)
    return tot, partes


T_IZQ, PART_IZQ = coste_orden(L, [3, 6, 8])
T_OPT, PART_OPT = coste_orden(L, [6, 3, 8])
assert (T_IZQ, T_OPT) == (42, 40)

TB = Tabla(40, 150, NP, NP, cw=104, ch=72, lw=110,
           cabecera=[f"j={j} ({PT[j]})" for j in range(NP)],
           etiquetas=[f"i={i} ({PT[i]})" for i in range(NP)], tam=28)
OSCURO = {(i, j): (0, 0, 0) for i in range(NP) for j in range(NP) if j <= i}


# ------------------------------------------------------------------ dibujos
def tablon(f, x0, y, escala, cortes, u=1.0, hueco=18, marcas=MARCAS, alto=44, nuevo=None):
    """Dibuja el tablón ya cortado por 'cortes' (los trozos se separan un poco)."""
    if u <= 0:
        return
    pts = sorted(set([0, L] + list(cortes)))
    for q in range(len(pts) - 1):
        a, b = pts[q], pts[q + 1]
        dx = q * hueco
        xa, xb = x0 + a * escala + dx, x0 + b * escala + dx
        f.d.rectangle((xa, y, xb, y + alto), fill=mix(C["bot"], MADERA, u), outline=mix(C["bot"], MADERA_O, u), width=2)
        for v in range(3):
            yy = y + 10 + v * 12
            f.d.line((xa + 6, yy, xb - 6, yy + 2), fill=mix(C["bot"], (176, 122, 70), u), width=1)
        for m in marcas:
            if a < m < b:
                xm = x0 + m * escala + dx
                for yy in range(int(y) - 8, int(y + alto + 8), 8):
                    f.d.line((xm, yy, xm, yy + 4), fill=mix(C["bot"], C["red"], u), width=3)
    for q, m in enumerate(pts):
        if m in (0, L) or m in cortes:
            pass
    return pts


def sierra(f, x, y, u=1.0):
    if u <= 0:
        return
    f.d.polygon([(x - 6, y - 70), (x + 6, y - 70), (x + 6, y - 6), (x - 6, y - 6)], fill=mix(C["bot"], (200, 210, 225), u))
    for k in range(8):
        yy = y - 70 + k * 8
        f.d.polygon([(x - 6, yy), (x - 12, yy + 4), (x - 6, yy + 8)], fill=mix(C["bot"], (200, 210, 225), u))
    f.d.rounded_rectangle((x - 16, y - 100, x + 16, y - 66), 6, fill=mix(C["bot"], (160, 60, 50), u))


def regla(f, x0, y, escala, u=1.0):
    for m in [0] + MARCAS + [L]:
        f.d.text((x0 + m * escala, y), str(m), font=font(18, True), fill=mix(C["bot"], C["muted"], u), anchor="mm")


# ------------------------------------------------------------------ escenas
def e_portada(f):
    def dib(f):
        tablon(f, 800, 330, 34, [], f.p(0.2, 0.6))
        sierra(f, 800 + 6 * 34, 330, f.p(0.7, 0.5))
    portada(f, "12-1", "El carpintero Ebanisto", TEMA, dib)


def e_problema(f):
    texto(f, (640, 80), "Cortar un tablón por todas sus marcas", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    tablon(f, 190, 200, 90, [], aparece(f, f.c(0)))
    regla(f, 190, 270, 90, aparece(f, f.c(0)))
    if f.t >= f.c(1):
        u = aparece(f, f.c(1))
        etiqueta(f, (640, 360), "cortar un trozo en dos cuesta el DOBLE de su longitud", 28, "gold", u)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (120, 450), "Entrada:  L (10..10⁶),  N marcas (1..500) en orden creciente", 26, "text", u, mono=True)
    if f.t >= f.c(3):
        etiqueta(f, (640, 570), "¿qué orden de cortes da el mínimo esfuerzo?", 30, "gold", aparece(f, f.c(3)))


def fila_orden(f, y, partes, total, t0, dt, col, titulo):
    hechos = [c for k, (c, a, b, e) in enumerate(partes) if f.t >= t0 + k * dt]
    texto(f, (60, y - 50), titulo, 24, col, aparece(f, t0 - 0.6))
    tablon(f, 180, y, 70, hechos, hueco=20)
    x = 180
    acc = []
    for k, (c, a, b, e) in enumerate(partes):
        if f.t >= t0 + k * dt:
            acc.append(f"2·{b - a}")
            sierra(f, 180 + c * 70 + 20 * sum(1 for h in hechos if h < c) - 10, y,
                   1.0 - f.p(t0 + k * dt + 0.6, 0.4)) if f.t < t0 + k * dt + 1.0 else None
    if acc:
        s = " + ".join(acc)
        fin = len(acc) == len(partes)
        texto(f, (180, y + 80), s + (f" = {total}" if fin else ""), 28, col if fin else "text", 1, mono=True, anchor="lm")


def e_ordenes(f):
    fila_orden(f, 230, PART_IZQ, T_IZQ, f.c(0) + 0.6, 1.2, "red", "orden 3, 6, 8")
    if f.t >= f.c(2):
        fila_orden(f, 450, PART_OPT, T_OPT, f.c(2) + 0.6, 1.2, "green", "orden 6, 3, 8")
    if f.t >= f.c(3):
        etiqueta(f, (640, 640), "el orden importa: 42 frente a 40", 28, "gold", aparece(f, f.c(3)))


def e_idea(f):
    texto(f, (640, 80), "La idea: el primer corte de un trozo", 32, "gold", aparece(f, f.c(0)), anchor="mm")
    x0, esc = 190, 90
    if f.t < f.c(2):
        tablon(f, x0, 220, esc, [], aparece(f, f.c(0)))
        regla(f, x0, 290, esc)
    if f.t >= f.c(1) and f.t < f.c(2):
        u = aparece(f, f.c(1))
        for q, m in enumerate(MARCAS):
            texto(f, (x0 + m * esc, 180), f"k = {m}", 22, "gold", aparece(f, f.c(1) + 0.4 * q), anchor="mm")
        etiqueta(f, (640, 380), "por la marca que sea, cortar el trozo de 0 a 10 cuesta 2·10 = 20", 26, "text", u)
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        tablon(f, x0, 220, esc, [6], hueco=60)
        regla(f, x0, 290, esc)
        texto(f, (x0 + 3 * esc, 340), "trozo (0, 6)", 24, AZUL, u, anchor="mm")
        texto(f, (x0 + 8 * esc + 60, 340), "trozo (6, 10)", 24, NARANJA, u, anchor="mm")
        etiqueta(f, (640, 430), "quedan dos trozos INDEPENDIENTES: cada uno con sus marcas", 26, "text", u)
    if f.t >= f.c(3):
        etiqueta(f, (640, 540), "esfuerzo(0, 10) = 20 + mejor(0, 6) + mejor(6, 10)  … probando cada k", 26, "gold", aparece(f, f.c(3)))


def e_recurrencia(f):
    texto(f, (60, 80), "p₀ = 0,  p₁ < … < p_N las marcas,  p_{N+1} = L", 24, "muted", aparece(f, f.c(0)), mono=True)
    texto(f, (60, 120), "esfuerzo(i, j) = mínimo para hacer todos los cortes entre p_i y p_j", 24, "muted",
          aparece(f, f.c(0)), bold=False)
    texto(f, (60, 190), "Caso base", 26, "gold", aparece(f, f.c(1)))
    y = formula(f, 80, 235, "esfuerzo(i, i+1) =", [("0", "(trozo sin marcas)")], aparece(f, f.c(1)))
    texto(f, (60, y + 30), "Recurrencia  (j − i ≥ 2)", 26, "gold", aparece(f, f.c(2)))
    y = formula(f, 80, y + 80, "esfuerzo(i, j) =", [("2·(p_j − p_i) + min  esfuerzo(i, k) + esfuerzo(k, j)", "")],
                aparece(f, f.c(2)))
    texto(f, (640, y - 4), "i < k < j", 22, "muted", aparece(f, f.c(2) + 0.6), mono=True)
    texto(f, (60, y + 60), "Respuesta:  esfuerzo(0, N+1)", 28, "green", aparece(f, f.c(3)), mono=True)
    texto(f, (60, y + 120), "como el producto de matrices encadenadas: partir un intervalo", 22, NARANJA,
          aparece(f, f.c(4)), bold=False)


def vals_hasta(n):
    v = {(i, i + 1): 0 for i in range(NP - 1)}
    for (i, j) in ORDEN[:n]:
        v[(i, j)] = E[i][j]
    return v


def e_tabla(f):
    t0, t1 = f.c(2), f.c(5)
    n_pasos = len(ORDEN)
    k, fr = paso_idx(f, t0, t1, n_pasos)
    hechos = max(0, min(k, n_pasos))
    vals = vals_hasta(hechos) if f.t >= f.c(1) else {}
    marca, sombra = {}, dict(OSCURO)
    cur = ORDEN[k] if 0 <= k < n_pasos else None
    lineas = []
    if cur:
        i, j = cur
        marca[cur] = "gold"
        ks = list(range(i + 1, j))
        q = min(len(ks) - 1, int(fr * (len(ks) + 0.6)))
        kk = ks[q]
        sombra[(i, kk)] = AZUL
        sombra[(kk, j)] = NARANJA
        lineas.append((f"({i},{j}):  2·({PT[j]} − {PT[i]}) = {2 * (PT[j] - PT[i])}", "gold"))
        for r, kr in enumerate(ks[:q + 1]):
            v = E[i][kr] + E[kr][j]
            ok = kr == MK[cur] and q == len(ks) - 1
            lineas.append((f"k={kr}: {E[i][kr]} + {E[kr][j]} = {v}" + ("  ← mín" if ok else ""), "green" if ok else "text"))
        if q == len(ks) - 1:
            lineas.append((f"→ {2 * (PT[j] - PT[i])} + {E[i][MK[cur]] + E[MK[cur]][j]} = {E[i][j]}", "green"))
    if f.t >= t1:
        marca = {(0, NP - 1): "green"}
    TB.dibuja(f, vals, marca=marca, sombra=sombra)
    d = cur[1] - cur[0] if cur else None
    texto(f, (720, 100), f"diagonal d = j − i = {d}" if d else ("d = 1: trozos sin marcas → 0" if f.c(1) <= f.t < t1 else ""),
          24, "gold", 1)
    for r, (s, c) in enumerate(lineas):
        texto(f, (720, 170 + 50 * r), s, 23, c, 1, mono=True)
    if cur:
        i, j = cur
        kk = [x for x in range(i + 1, j)][min(j - i - 2, int(fr * (j - i - 1 + 0.6)))]
        TB.flecha_entre(f, (i, kk), cur, AZUL, u=1)
        TB.flecha_entre(f, (kk, j), cur, NARANJA, u=1)
    if f.t >= t1:
        etiqueta(f, (980, 560), f"esfuerzo(0, 4) = {E[0][NP - 1]}", 32, "green", aparece(f, t1), mono=True)


def e_arbol(f):
    texto(f, (640, 70), "¿En qué orden se corta?  Se sigue el k ganador", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    nodos = []

    def rec(i, j, dep):
        if j - i < 2:
            nodos.append((i, j, dep, None))
            return
        nodos.append((i, j, dep, MK[(i, j)]))
        rec(i, MK[(i, j)], dep + 1)
        rec(MK[(i, j)], j, dep + 1)
    rec(0, NP - 1, 0)
    pos = {}
    for i, j, dep, k in nodos:
        pos[(i, j)] = (140 + (PT[i] + PT[j]) / 2 * 100, 170 + dep * 150)
    for i, j, dep, k in nodos:
        t = f.c(min(dep + 1, 3))
        if f.t < t:
            continue
        u = aparece(f, t)
        x, y = pos[(i, j)]
        if k is not None:
            for h in ((i, k), (k, j)):
                if f.t >= f.c(min(dep + 2, 3)):
                    f.d.line((x, y + 40, pos[h][0], pos[h][1] - 40), fill=C["muted"], width=3)
        leaf = k is None
        w = 150
        f.d.rounded_rectangle((x - w / 2, y - 40, x + w / 2, y + 40), 12, fill=mix(C["bot"], C["panel"], u),
                              outline=mix(C["bot"], C["dim"] if leaf else C["gold"], u), width=3)
        texto(f, (x, y - 16), f"[{PT[i]}, {PT[j]}]", 24, "text", u, anchor="mm", fondo=C["panel"])
        texto(f, (x, y + 16), "trozo final" if leaf else f"corte {PT[k]}: {2 * (PT[j] - PT[i])}", 20,
              "dim" if leaf else "gold", u, anchor="mm", fondo=C["panel"])
    if f.t >= f.c(3):
        etiqueta(f, (640, 650), f"primero el 6 (20), luego el 3 (12) y el 8 (8):  {E[0][NP - 1]}", 26, "green", aparece(f, f.c(3)))


A = find_line(CPP, "void resuelveCaso()")
B = find_line(CPP, "cout << esfuerzo[0][N + 1]")
CODE = [(n, s) for n, s in codigo(CPP, A, B + 1, maxc=90) if s.strip() not in ("", "}")]
L_P = (find_line(CPP, "vector<long long> p(N + 2);"), find_line(CPP, "p[N + 1] = L;"))
L_T = find_line(CPP, "vector<vector<long long>> esfuerzo(P, vector<long long>(P, 0));")
L_D = (find_line(CPP, "for (int d = 2; d < P; ++d)"), find_line(CPP, "int j = i + d;"))
L_K = (find_line(CPP, "long long mejor = -1;"), find_line(CPP, "esfuerzo[i][j] = 2 * (p[j] - p[i]) + mejor;"))
NOTAS = [(set(range(L_P[0], L_P[1] + 1)), "los puntos: 0, las marcas y L"),
         ({L_T}, "tabla P × P a ceros: ya vale para los trozos sin marcas"),
         (set(range(L_D[0], L_D[1] + 1)), "por diagonales: d = j − i = 2, 3, …"),
         (set(range(L_K[0], L_K[1] + 1)), "mínimo sobre k y se suma el corte 2·(p_j − p_i)"),
         ({B}, "la respuesta, esfuerzo[0][N+1]")]


def e_codigo(f):
    k = 0
    for q in range(len(NOTAS)):
        if f.t >= f.c(q):
            k = q
    hl, nota = NOTAS[k]
    f.code(40, 84, 1200, 490, CODE, hl=hl, title="resuelveCaso()", size=21)
    etiqueta(f, (640, 630), nota, 26, "gold", aparece(f, f.c(k)))


def e_errores(f):
    f.box(60, 110, 1160, 500, "errores típicos")
    items = [("el esfuerzo es el DOBLE de la longitud del trozo, no la longitud", "text"),
             ("0 y L también son puntos: sin ellos falta el primer corte", "text"),
             ("rellenar por filas o columnas sin cuidado usa casillas sin calcular: por diagonales", "red"),
             (f"ningún voraz (en orden, por la marca centrada…): 3, 6, 8 cuesta {T_IZQ}", "text"),
             ("probar los N! órdenes no termina:  O(N³) tiempo y O(N²) memoria", "gold")]
    for k, (s, c) in enumerate(items):
        if f.t >= f.c(k):
            texto(f, (100, 170 + 86 * k), s, 23, c, aparece(f, f.c(k)), fondo=C["panel"])


def e_cierre(f):
    cierre(f, "El carpintero Ebanisto", [
        "puntos 0, marcas, L;  trozo (i, j)",
        "esfuerzo(i, j) = 2·(p_j − p_i) + min_k (i, k) + (k, j)",
        "esfuerzo(i, i+1) = 0;  respuesta esfuerzo(0, N+1)",
        "tabla por diagonales:  O(N³) tiempo, O(N²) memoria",
    ])


ESC = [
    Escena("El carpintero Ebanisto. Un problema de evaluación de programación dinámica sobre intervalos.",
           e_portada, titulo="Portada", extra=1.0),
    Escena("Ebanisto tiene que cortar un tablón por varias marcas: en el primer ejemplo, un tablón de diez metros con marcas en el tres, el seis y el ocho. "
           "Cortar un trozo de madera en dos le cuesta el doble de la longitud de ese trozo. "
           "Nos dan la longitud del tablón y las marcas, en orden creciente. "
           "Hay que elegir el orden de los cortes para que el esfuerzo total sea mínimo.",
           e_problema, titulo="Qué piden", extra=1.5),
    Escena("Si corta de izquierda a derecha, primero corta el tablón entero por el tres, después el trozo de siete por el seis, y por último el de cuatro por el ocho. "
           "Veinte más catorce más ocho: cuarenta y dos. "
           "Si empieza por el seis, luego corta el trozo de seis por el tres, y el de cuatro por el ocho: veinte más doce más ocho, cuarenta. "
           "El orden importa.",
           e_ordenes, titulo="El orden importa", extra=2.0),
    Escena("La clave está en el primer corte de cada trozo. "
           "Se haga por la marca que se haga, cortar el trozo entero cuesta lo mismo: el doble de su longitud. "
           "Y después quedan dos trozos independientes, cada uno con sus propias marcas. "
           "Así que solo hay que probar cada marca ka como primer corte, y resolver lo mejor posible las dos partes.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Numeramos los puntos: el cero, las marcas, y la longitud ele al final. Esfuerzo de i, jota es lo mínimo para hacer todos los cortes entre el punto i y el jota. "
           "Si son puntos consecutivos no hay nada que cortar: cero. "
           "Si no, el primer corte cuesta dos por la longitud, más el mínimo, para cada ka entre medias, de los dos trozos que quedan. "
           "La respuesta es esfuerzo de cero, ene más uno. "
           "Es la misma forma que el producto de matrices encadenadas.",
           e_recurrencia, titulo="Recurrencia", extra=1.5),
    Escena("Cada casilla necesita intervalos más cortos, así que la tabla se rellena por diagonales. "
           "La primera diagonal son trozos sin marcas: ceros. "
           "En la segunda, cada trozo tiene una sola marca: doce, diez y ocho. "
           "En la tercera hay dos marcas para elegir: veintiséis y veintidós. "
           "Y en la última casilla probamos las tres marcas: la del seis da doce más ocho, veinte, y con el corte inicial de veinte, cuarenta.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Para saber el orden, seguimos la marca que ganó en cada casilla. "
           "En el tablón entero ganó el seis. "
           "En el trozo de cero a seis se corta por el tres, y en el de seis a diez, por el ocho. "
           "Veinte más doce más ocho: cuarenta.",
           e_arbol, titulo="El orden óptimo", extra=1.5),
    Escena("En el código, primero se forma el vector de puntos con el cero, las marcas y ele. "
           "La tabla empieza a ceros, y eso ya sirve para los trozos sin marcas. "
           "El bucle de fuera recorre las diagonales, de, que es jota menos i; el de dentro, el principio del trozo. "
           "Para cada trozo se busca el mínimo sobre ka y se le suma el corte. "
           "La respuesta queda en la esquina, esfuerzo de cero, ene más uno.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Errores típicos. El esfuerzo es el doble de la longitud, no la longitud. "
           "El cero y ele cuentan como puntos; sin ellos falta el primer corte. "
           "Si se rellena la tabla por filas de arriba abajo, se usan casillas que aún no están calculadas; por eso, por diagonales. "
           "Ningún voraz sirve: cortar en orden cuesta cuarenta y dos. "
           "Y probar todos los órdenes es factorial; con la tabla, el coste es ene al cubo.",
           e_errores, titulo="Errores típicos", extra=1.5),
    Escena("Resumiendo: los puntos son el cero, las marcas y ele, y cada subproblema es un trozo entre dos puntos. "
           "Su esfuerzo es el corte inicial más el mejor reparto en dos trozos. "
           "Los trozos sin marcas valen cero, y la respuesta es el tablón entero. "
           "Se rellena por diagonales, en ene al cubo.",
           e_cierre, titulo="Resumen", extra=1.5),
]


def voz_estimada():
    """--preview sin Kokoro ni Piper: tiempos estimados (≈ 14,5 caracteres/s) en vez de sintetizar.
    Solo cambia anim._tts en este proceso; con voz instalada no hace nada."""
    import anim
    if os.environ.get("KOKORO_MODEL") or os.environ.get("PIPER_MODEL"):
        return
    def est(texto, wav):
        t, out = 0.0, []
        for fr in [x for x in re.split(r"(?<=[.:;?!])\s+", texto.strip()) if x]:
            d = len(fr) / 14.5
            out.append((fr, t, t + d))
            t += d + 0.22
        return t, out
    anim._tts = est
    tot = sum(max(e.dmin, est(e.narracion, None)[0] + e.extra) for e in ESC)
    print(f"(sin voz: tiempos estimados, duración ≈ {tot / 60:.1f} min)")


if __name__ == "__main__":
    if "--preview" in sys.argv:
        voz_estimada()
    args_preview(ESC, "preview/12-1", "../12-1_el_carpintero_ebanisto.mp4", "12-1")
