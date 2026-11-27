"""Vídeo EJ 12-9 · Una gira agotadora (animado)."""
from vidlib import C, font
from anim import Escena, mix
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-9/EJ_12-9.cpp"
R = [1, 8, 1, 1, 8, 3]
n = len(R)
G = []
for i, r in enumerate(R):
    G.append(max(G[i - 1] if i >= 1 else 0, (G[i - 2] if i >= 2 else 0) + r))
assert G == [1, 8, 8, 9, 16, 16]
TB = Tabla(100, 150, 2, n, cw=130, ch=90, lw=190, cabecera=[f"día {i + 1}" for i in range(n)],
           etiquetas=["recauda", "gira(i)"], tam=36)


def dia(f, x, y, num, v, u=1.0, actua=False):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - 60, y - 60, x + 60, y + 60), 14, fill=mix(C["bot"], (150, 60, 90) if actua else (34, 48, 84), u),
                          outline=mix(C["bot"], C["gold"] if actua else C["border"], u), width=5 if actua else 2)
    f.d.text((x, y - 34), f"día {num}", font=font(18), fill=mix(C["bot"], C["muted"], u), anchor="mm")
    f.d.text((x, y + 12), str(v), font=font(40, True), fill=mix(C["bot"], C["text"], u), anchor="mm")


def dib(f):
    for k, v in enumerate([10, 1, 10]):
        dia(f, 840 + 140 * k, 310, k + 1, v, f.p(0.3 + 0.25 * k, 0.5), actua=k != 1 and f.t > 1.4)


def e_problema(f):
    texto(f, (640, 80), "elegir los días de función: nunca dos seguidos", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    elegidos = {1, 4} if f.t >= f.c(2) else set()
    if f.t >= f.c(1) and f.t < f.c(2):
        elegidos = {0, 2, 4}
    for k, v in enumerate(R):
        dia(f, 215 + 170 * k, 260, k + 1, v, aparece(f, f.c(0)), actua=k in elegidos)
    if f.t >= f.c(1) and f.t < f.c(2):
        texto(f, (640, 430), "días 1, 3 y 5:  1 + 1 + 8 = 10", 34, "muted", aparece(f, f.c(1)), mono=True, anchor="mm")
        texto(f, (640, 490), "días 2, 4 y 6:  8 + 1 + 3 = 12", 34, "muted", aparece(f, f.c(1)), mono=True, anchor="mm")
    if f.t >= f.c(2):
        texto(f, (640, 460), "días 2 y 5:  8 + 8 = 16", 40, "green", aparece(f, f.c(2)), mono=True, anchor="mm")
    if f.t >= f.c(3):
        texto(f, (640, 560), "y se descansa dos días seguidos", 28, "text", aparece(f, f.c(3)), anchor="mm")


def e_tabla(f):
    nn = avance(f, 1, 4, n)
    vals = {(0, i): R[i] for i in range(n)}
    vals.update({(1, i): G[i] for i in range(nn)})
    cur = nn if nn < n and f.t >= f.c(1) else None
    marca = {(1, cur): "gold"} if cur is not None else {}
    if cur is not None:
        no = G[cur - 1] if cur >= 1 else 0
        antes = G[cur - 2] if cur >= 2 else 0
        si = antes + R[cur]
        panel(f, 190, 420, 900, 170, f"día {cur + 1}",
              [(f"descanso:  gira(i−1) = {no}", "green" if no == G[cur] else "text"),
               (f"actúo:     gira(i−2) + {R[cur]} = {antes} + {R[cur]} = {si}", "green" if si == G[cur] else "text")])
    if f.t >= f.c(4):
        marca = {(1, n - 1): "green"}
        texto(f, (640, 510), "gira(6) = 16", 40, "green", aparece(f, f.c(4)), mono=True, anchor="mm")
    TB.dibuja(f, vals, marca=marca)


ESC = [
    Escena("Una gira agotadora. Elegir qué días actuar para recaudar lo máximo sin actuar dos días seguidos.",
           e_portada("12-9", "Una gira agotadora", dib), titulo="Portada", extra=1.0),
    Escena("Conocemos lo que se recaudaría cada día, pero los actores necesitan descansar al menos un día entre funciones. "
           "Actuar un día sí y otro no recauda como mucho doce. "
           "Lo mejor es actuar los días dos y cinco: dieciséis. "
           "Y eso obliga a descansar dos días seguidos.",
           e_problema, titulo="El problema", extra=2.0),
    Escena("Pensemos en el último día. Solo hay dos opciones. "
           "Gira de i es la recaudación máxima con los i primeros días. "
           "Si ese día descansan, vale lo mismo que con un día menos. "
           "Si actúan, el anterior se descansa, y sumamos la recaudación a lo de dos días antes. "
           "Nos quedamos con el mayor.",
           e_lineas([(0, 90, "¿actúan el último día o no?", "gold", 34),
                     (2, 200, "gira(0) = 0        gira(1) = r1", "text", 32, True),
                     (3, 320, "descansan:  gira(i−1)", "text", 34, True),
                     (4, 400, "actúan:     gira(i−2) + r_i", "text", 34, True),
                     (5, 510, "gira(i) = el máximo de las dos", "green", 34),
                     (5, 590, "respuesta: gira(N)", "muted", 28)]), titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla con el cuarto ejemplo. "
           "Cada día comparamos descansar con actuar. "
           "Actuar suma lo de hoy a lo que teníamos dos días atrás. "
           "Descansar conserva el valor anterior. "
           "Al final, dieciséis.",
           e_tabla, titulo="La tabla", extra=2.5),
    Escena("Cada valor solo depende de los dos anteriores. "
           "Así que no hace falta guardar la tabla: bastan dos variables, y la memoria es constante.",
           e_lineas([(0, 170, "gira(i) solo mira gira(i−1) y gira(i−2)", "gold", 34),
                     (1, 320, "dosAtras = anterior", "text", 34, True),
                     (1, 390, "anterior = actual", "text", 34, True),
                     (1, 510, "memoria O(1)", "green", 38)]), titulo="Memoria", extra=1.5),
    Escena("En el código empezamos con las dos variables a cero. "
           "Para cada día leemos la recaudación y calculamos el máximo. "
           "Después desplazamos las dos variables. "
           "La última es la respuesta.",
           e_codigo(CPP, "int dosAtras = 0, anterior = 0;", "cout << anterior",
                    [["int dosAtras = 0, anterior = 0;"], ["int actual = max(anterior, dosAtras + r);"],
                     ["dosAtras = anterior;", "anterior = actual;"], ["cout << anterior"]],
                    [("dos variables", "gira(i−2) y gira(i−1)"), ("máximo", "descansar o actuar"),
                     ("desplazar", "en este orden"), ("coste", "O(N) por caso")], size=18),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: en el último día se descansa o se actúa. "
           "Si se actúa, se salta al de dos días antes. "
           "Alternar o coger el día más caro no es óptimo. "
           "Tiempo lineal y memoria constante.",
           e_cierre("Una gira agotadora", [
               "dos opciones: descansar o actuar",
               "gira(i) = max(gira(i−1), gira(i−2) + r_i)",
               "ni alternar ni voraz: no son óptimos",
               "O(N) en tiempo, O(1) en memoria"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-9", "../12-9_una_gira_agotadora.mp4")
