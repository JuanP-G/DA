"""Vídeo EJ 06-4 · La selva de Tarzan (Kruskal: valor de la última arista aceptada)."""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line
from v06_teoria import limpia
from v06e_comun import TEMA, sim, dibuja, slide_paso, slide_final, narra, pinta_preview

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-4/EJ_06-4.cpp"
NOMBRE = "La selva de Tarzan"
COR = "EJ 06-4"
I0 = find_line(CPP, "bool resuelveCaso()")
L_EOF = find_line(CPP, "if (!cin) return false;")
L_SORT = find_line(CPP, "sort(saltos.begin()")
L_BRK = find_line(CPP, "if (cd.num_cjtos() == 1) break;")
L_UNI = find_line(CPP, "if (!cd.unidos(u, v))")
L_UNIR = find_line(CPP, "cd.unir(u, v);")
L_ULT = find_line(CPP, "ultima = s.valor();")
L_FIN = find_line(CPP, "if (cd.num_cjtos() == 1) cout", L_BRK + 1)
CODE = limpia(code_lines(CPP, I0, L_FIN + 2, maxc=72))

EJ1 = dict(n=4, E=[(1, 2, 5), (3, 1, 7), (2, 4, 8), (2, 3, 10)],
           pos={1: (760, 210), 2: (1040, 210), 3: (760, 440), 4: (1040, 440)})
EJ3 = dict(n=4, E=[(1, 2, 3), (4, 3, 6)],
           pos={1: (760, 210), 2: (1040, 210), 3: (760, 440), 4: (1040, 440)})


def trazas(ej, nombre_ej, titulo):
    pasos, fin = sim(ej, "ult")
    segs = []
    for i in range(len(pasos)):
        s = slide_paso(titulo, COR, ej, "ult", pasos, i, nombre_ej, "saltos")
        st = pasos[i]
        a, b, c = ej["E"][st["k"]]
        if st["d"] == "une":
            cap = f"{a}–{b} (cuerda {c}): árboles en conjuntos distintos, se une. Última = {c}."
        elif st["d"] == "ciclo":
            cap = f"{a} y {b} ya están conectados: se descarta."
        else:
            cap = "Un solo conjunto: ya se puede ir de cualquier árbol a cualquier otro."
        s.caption(cap, y=626)
        segs.append((s, narra(ej, "ult", pasos, i, "El salto entre los árboles"), 0))
    return segs, pasos, fin


def main(preview=False):
    segs = [(portada(NOMBRE, COR, TEMA),
             "La selva de Tarzan. Otro Kruskal, pero esta vez no sumamos: la respuesta es el valor de la última arista que se acepta.", 0)]

    segs.append((ideas("El problema", [
        "N árboles y M saltos posibles; cada salto exige una cuerda de al menos cierta longitud.",
        "Tarzan lleva una sola cuerda y quiere poder ir de cualquier árbol a cualquier otro.",
        ("Longitud mínima de la cuerda, o «Imposible».", "gold"),
        "La entrada es una secuencia de selvas, hasta el final del fichero.",
    ]), "Tarzan tiene una selva con árboles y saltos posibles entre ellos, y cada salto exige una cuerda de al menos cierta longitud. Lleva una sola cuerda, "
        "y quiere poder ir de cualquier árbol a cualquier otro. Hay que dar la longitud mínima de la cuerda, o imposible. Las selvas llegan una detrás de otra hasta el final del fichero.", 0))

    s = Slide("Con una cuerda de longitud L…", TEMA)
    s.box(40, 100, 1200, 150, "idea")
    s.text((70, 150), "con cuerda L se pueden hacer todos los saltos de valor ≤ L", size=30, mono=True, color="gold")
    s.text((70, 200), "Buscamos la menor L para la que esos saltos conecten todos los árboles.", size=22, color="muted")
    s.bullets(60, 290, 1160, [
        "Kruskal mete las aristas de menor a mayor: al meter una de valor L ya están todas las más cortas.",
        ("La respuesta es el valor de la ÚLTIMA arista aceptada: la más pesada de un ARM.", "gold"),
        "Diferencia con 06-3: no se suman los costes, se guarda el valor de la última.",
        "Si al terminar quedan varios conjuntos: «Imposible». Con N = 1 ya hay uno solo: 0.",
    ], size=23, gap=16)
    segs.append((s, "Con una cuerda de longitud L se pueden hacer todos los saltos de valor menor o igual que L. Buscamos la menor L para la que esos saltos conecten todos los árboles. "
                    "Eso es justo lo que hace Kruskal: mete las aristas de menor a mayor, así que cuando mete una de valor L ya están todas las más cortas. "
                    "La respuesta es el valor de la última arista aceptada, la más pesada de un árbol de recubrimiento mínimo. A diferencia del ejercicio anterior, no se suman: se guarda la última. "
                    "Si al terminar quedan varios conjuntos, es imposible.", 0))

    s = Slide("El código", "EJ_06-4.cpp")
    s.code(24, 84, 800, 520, CODE, hl={L_EOF, L_SORT, L_BRK, L_UNI, L_UNIR, L_ULT, L_FIN}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["Devuelve bool: false al llegar al final de la entrada.",
                              "sort: saltos por longitud creciente.",
                              "num_cjtos() == 1 ⇒ break.",
                              "!unidos ⇒ unir y  ultima = valor.",
                              "Un solo conjunto: ultima. Si no: Imposible.",
                              "N = 1: no se acepta nada y ya hay un conjunto: 0."], size=19, gap=14)
    segs.append((s, "El código lee el grafo y si la lectura falla devuelve falso, porque llegamos al final de la entrada. Ordenamos los saltos por longitud, y recorremos: si ya queda un solo conjunto, salimos. "
                    "Si los extremos no están unidos, los unimos y guardamos su valor en última. Al final, si hay un solo conjunto escribimos última, y si no, imposible. "
                    "Con un solo árbol no se acepta ninguna arista y ya hay un conjunto, así que sale cero.", 0))

    t1, p1, f1 = trazas(EJ1, "ejemplo 1 · 4 árboles, 4 saltos", "Ejemplo 1: Kruskal paso a paso")
    segs += t1
    segs.append((slide_final("Ejemplo 1: resultado", COR, EJ1, "ult", p1, f1, "ejemplo 1 · 4 árboles, 4 saltos",
                             "El salto de 10 nunca hace falta: la cuerda mínima es 8.", "8", "última = 8"),
                 "La última arista aceptada vale ocho, y el salto de diez no hace falta. Una cuerda de longitud ocho basta para ir a cualquier árbol.", 0))

    t3, p3, f3 = trazas(EJ3, "un caso imposible · dos grupos separados", "Si no se conecta todo")
    segs += t3
    segs.append((slide_final("Caso imposible", COR, EJ3, "ult", p3, f3, "un caso imposible · dos grupos separados",
                             "Quedan dos conjuntos: ninguna cuerda sirve.", "Imposible", "conjuntos = 2  ≠  1"),
                 "Se acaban los saltos y quedan dos conjuntos, uno y dos por un lado y tres y cuatro por otro. Ninguna cuerda sirve: imposible.", 0))

    segs.append((ideas("Detalles y coste", [
        "No sumar: se escribe una longitud, no un coste total.",
        "Distinguir «un solo árbol» (0) de «no se puede» (Imposible) con num_cjtos(), no con si hubo aristas.",
        "Es «Imposible», distinto del «IMPOSIBLE» del 06-5.",
        "Varias selvas hasta EOF: la partición se crea en cada una.",
        ("Coste: O(N + M log M).", "gold"),
    ]), "Detalles importantes. No hay que sumar: se escribe una longitud. Para distinguir un solo árbol de un caso imposible se mira el número de conjuntos, no si hubo aristas. "
        "La palabra es imposible con mayúscula inicial, distinta de la del problema siguiente. Y el coste es el de ordenar.", 0))

    segs.append((cierre(NOMBRE, [
        "Cuerda mínima = valor de la última arista aceptada por Kruskal.",
        "Se para en cuanto num_cjtos() == 1.",
        "Si quedan varios conjuntos: «Imposible». Con N = 1: 0.",
        "No se suma: se guarda  ultima = s.valor().",
        "O(N + M log M).",
    ]), "Resumiendo: la cuerda mínima es el valor de la última arista que acepta Kruskal. Paramos cuando queda un solo conjunto, y si al final hay varios, es imposible.", 0))

    if preview:
        pinta_preview(segs, "06-4")
    else:
        print(f"06-4: {build(segs, '../06-4_selva_de_tarzan.mp4'):.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
