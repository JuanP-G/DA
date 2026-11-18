"""Vídeo EJ 02-5 · Ordenando a los pacientes en urgencias (animado)."""
from vidlib import C, W, H, font, find_line
from anim import Escena, ease, lerp, mix
from pd_comun import AZUL, NARANJA, flecha, aparece, texto, codigo, portada, cierre
from vor_comun import caja, mueve, paso_idx, tick, args_preview, etiqueta
from pq_comun import Monticulo
from pq_traza import escena_traza, escena_codigo, escena_lista

CPP = "../../2-Colas de prioridad/EJ_02-5/EJ_02-5.cpp"
TEMA = "Tema 2 · Colas de prioridad"
EV = [("I", "Alberto", 4000), ("I", "Pepe", 3000), ("A",), ("I", "Rosa", 2000), ("I", "Laura", 5000),
      ("A",), ("I", "Sara", 3000), ("A",), ("A",)]
COLS = {"Alberto": C["blue"], "Pepe": NARANJA, "Rosa": C["purple"], "Laura": C["red"], "Sara": C["green"]}


def simula():
    pq = Monticulo(lambda a, b: (-a[0], a[1]) < (-b[0], b[1]))   # (gravedad, orden)
    pasos, salida = [], []
    for i, e in enumerate(EV):
        ant = pq.copia()
        if e[0] == "I":
            pq.push(e[1], (e[2], i))
            s = f"I {e[1]} {e[2]}"
            c = "text"
        else:
            n, (g, o) = pq.pop()
            salida.append(n)
            emp = any(p[0] == g for _, p in pq.a)
            s = f"A → {n}" + ("  (empate: llegó antes)" if emp else "")
            c = "gold"
        pasos.append((ant, pq.copia(), s, c))
    return pasos, salida


PASOS, SALIDA = simula()


def etq(e, p):
    return f"{e[:4]}\n{p[0]}"


def e_portada(f):
    def dib(f):
        u = f.p(0.3, 0.6)
        f.d.rounded_rectangle((880, 260, 1040, 420), 16, fill=mix(C["bot"], (230, 236, 245), u))
        f.d.rectangle((945, 285, 975, 395), fill=mix(C["bot"], C["red"], u))
        f.d.rectangle((905, 325, 1015, 355), fill=mix(C["bot"], C["red"], u))
    portada(f, "EJ 02-5", "Pacientes en urgencias", TEMA, dib)


def e_problema(f):
    texto(f, (640, 70), "llegan pacientes (I) y el médico atiende (A)", 26, "text", aparece(f, f.c(0)), anchor="mm")
    for k, e in enumerate(EV[:6]):
        t0 = f.c(0) + 0.3 * k
        if f.t < t0:
            continue
        s = f"I {e[1]} {e[2]}" if e[0] == "I" else "A"
        caja(f, 320, 150 + k * 62, s, c=COLS.get(e[1], C["gold"]) if e[0] == "I" else "gold", u=aparece(f, t0), w=260, h=48, tam=20)
    if f.t >= f.c(1):
        etiqueta(f, (850, 280), "en cada A: el MÁS GRAVE", 26, "red", aparece(f, f.c(1)))
    if f.t >= f.c(2):
        etiqueta(f, (850, 360), "a igual gravedad: el que llegó antes", 24, "text", aparece(f, f.c(2)))


def e_idea(f):
    texto(f, (640, 90), "cola de prioridad de máximos por (gravedad, orden de llegada)", 26, "gold", aparece(f, f.c(0)), anchor="mm")
    if f.t >= f.c(1):
        etiqueta(f, (640, 260), "I → push      A → top y pop", 28, "text", aparece(f, f.c(1)), mono=True)
    if f.t >= f.c(2):
        etiqueta(f, (640, 360), "el orden de llegada es el número de evento: deshace los empates", 24, "green", aparece(f, f.c(2)))


def lateral(f, k, fr):
    texto(f, (60, 130), "atendidos:", 22, "muted", 1)
    n = sum(1 for q in range(k + (1 if fr > 0.4 else 0)) if EV[q][0] == "A")
    for q in range(n):
        caja(f, 140, 190 + q * 62, SALIDA[q], c=COLS[SALIDA[q]], w=150, h=48, tam=20)


def e_traza(f):
    escena_traza(f, PASOS, etq, colores=COLS, lateral=lateral, titulo="cola de máximos: más grave arriba")


A_L = find_line(CPP, "struct Paciente {")
B_L = find_line(CPP, "cout << \"---\\n\";")
L_CMP = find_line(CPP, "if (gravedad != o.gravedad) return gravedad < o.gravedad;")
F_L = find_line(CPP, "priority_queue<Paciente> cola;")
L_I = find_line(CPP, "cola.push({ nombre, gravedad, i });")
L_A = find_line(CPP, "cout << cola.top().nombre << '\\n';")


def e_codigo(f):
    escena_codigo(f, CPP, [(A_L, A_L + 8, {L_CMP, L_CMP + 1}, "struct Paciente"),
                           (F_L, B_L, {L_I}, "eventos"),
                           (F_L, B_L, {L_A - 1, L_A, L_A + 1}, "eventos")], size=19)


def e_detalles(f):
    escena_lista(f, [("operator<: la priority_queue de la STL es de máximos", "text"),
                     ("orden mayor = llegó después: va detrás en el empate", "text"),
                     ("una A con la sala vacía no escribe nada", "text"),
                     ("cada evento O(log n)", "gold")])


def e_cierre(f):
    cierre(f, "Pacientes en urgencias", [
        "cola de máximos de pacientes",
        "más grave primero; empate, el que llegó antes",
        "I: push · A: top y pop",
        "O(log n) por evento",
    ])


ESC = [
    Escena("Ordenando a los pacientes en urgencias. A quién atiende el médico en cada momento.", e_portada, titulo="Portada", extra=1.0),
    Escena("Van llegando pacientes con su gravedad, y de vez en cuando el médico queda libre para atender a uno. "
           "Siempre atiende al más grave. "
           "Y si hay varios igual de graves, al que lleva más tiempo esperando.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Es una cola de prioridad de máximos, ordenada por gravedad y por orden de llegada. "
           "Cada ingreso es un push, y cada atención, un top y un pop. "
           "El orden de llegada se guarda con el número de evento, y deshace los empates.",
           e_idea, titulo="La idea", extra=1.5),
    Escena("Entran Alberto, cuatro mil, y Pepe, tres mil. Se atiende a Alberto. "
           "Entran Rosa y Laura; Laura, con cinco mil, sube a la cima y es la siguiente. "
           "Entra Sara con tres mil, igual que Pepe: Pepe llegó antes, así que va primero. "
           "Y después Sara. Rosa se queda esperando.",
           e_traza, titulo="El ejemplo", extra=2.0),
    Escena("En el código, el operador menor del paciente compara por gravedad y, si empatan, el que llegó después es menor. "
           "Un ingreso hace push con el nombre, la gravedad y el número de evento. "
           "Una atención escribe la cima y la saca.",
           e_codigo, titulo="El código", extra=2.0),
    Escena("Se define el operador menor porque la priority queue es de máximos. "
           "El que llegó después tiene orden mayor y queda detrás. "
           "Si se pide atender con la sala vacía, no se escribe nada. "
           "Cada evento cuesta logaritmo de ene.",
           e_detalles, titulo="Detalles", extra=1.5),
    Escena("Resumiendo: una cola de máximos por gravedad y orden de llegada; ingresar es push, y atender, top y pop.",
           e_cierre, titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    args_preview(ESC, "preview/02-5", "../02-5_pacientes_en_urgencias.mp4", "02-5")
