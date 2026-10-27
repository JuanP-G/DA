"""Vídeo EJ 06-3 · Recorriendo el archipiélago en bicicleta (Kruskal: suma del ARM)."""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line
from v06_teoria import limpia
from v06e_comun import TEMA, sim, dibuja, slide_paso, slide_final, narra, pinta_preview

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-3/EJ_06-3.cpp"
NOMBRE = "Recorriendo el archipiélago en bicicleta"
COR = "EJ 06-3"
I0 = find_line(CPP, "void resuelveCaso()")
L_SORT = find_line(CPP, "sort(puentes.begin()")
L_BRK = find_line(CPP, "if (elegidos == g.V() - 1) break;")
L_UNI = find_line(CPP, "if (!cd.unidos(u, v))")
L_UNIR = find_line(CPP, "cd.unir(u, v);")
L_COS = find_line(CPP, "coste += p.valor();")
L_FIN = find_line(CPP, "if (elegidos == g.V() - 1) cout", L_BRK + 1)
CODE = limpia(code_lines(CPP, I0, L_FIN + 1, maxc=72))

EJ1 = dict(n=4, E=[(1, 2, 5), (1, 3, 10), (1, 4, 8), (2, 4, 7), (3, 4, 2)],
           pos={1: (760, 210), 2: (1040, 210), 3: (760, 440), 4: (1040, 440)})
EJ2 = dict(n=4, E=[(1, 2, 3), (2, 4, 5), (4, 1, 8)],
           pos={1: (760, 210), 2: (1040, 210), 3: (760, 440), 4: (1040, 440)})


def trazas(ej, nombre_ej, titulo):
    pasos, fin = sim(ej, "sum")
    segs = []
    for i in range(len(pasos)):
        s = slide_paso(titulo, COR, ej, "sum", pasos, i, nombre_ej, "puentes")
        st = pasos[i]
        a, b, c = ej["E"][st["k"]]
        if st["d"] == "une":
            cap = f"{a}–{b} ({c}): conjuntos distintos, se construye. Total {st['tot']}."
        elif st["d"] == "ciclo":
            cap = f"{a} y {b} ya están unidas: cerraría un ciclo, se descarta."
        else:
            cap = f"Ya hay {st['el']} = I − 1 puentes: se para."
        s.caption(cap, y=626)
        segs.append((s, narra(ej, "sum", pasos, i, "El puente entre las islas"), 0))
    return segs, pasos, fin


def main(preview=False):
    segs = [(portada(NOMBRE, COR, TEMA),
             "Recorriendo el archipiélago en bicicleta. Es el primer problema de árbol de recubrimiento de coste mínimo: Kruskal con un conjunto disjunto, sumando lo que cuestan los puentes elegidos.", 0)]

    segs.append((ideas("El problema", [
        "I islas (hasta 10.000) y P puentes presupuestados (hasta 100.000), cada uno con su coste.",
        "Hay que elegir puentes para poder ir de cualquier isla a cualquier otra.",
        ("Coste total mínimo; si no se puede: «No hay puentes suficientes».", "gold"),
        "Varios casos de prueba; con una sola isla la respuesta es 0.",
    ]), "Tenemos islas y puentes presupuestados, cada uno con su coste. Hay que elegir puentes para poder ir de cualquier isla a cualquier otra con coste total mínimo. "
        "Si no hay puentes suficientes, se escribe un mensaje. Con una sola isla no hace falta ninguno, y la respuesta es cero.", 0))

    s = Slide("Árbol de recubrimiento de coste mínimo", TEMA)
    s.box(40, 100, 1200, 150, "idea")
    s.text((70, 150), "islas = vértices   ·   puentes = aristas   ·   coste = valor", size=30, mono=True, color="gold")
    s.text((70, 200), "Queremos conectar todo con V − 1 aristas y suma mínima: un ARM.", size=22, color="muted")
    s.bullets(60, 290, 1160, [
        "Kruskal: ordenar las aristas por valor creciente.",
        "Conjuntos disjuntos: al principio cada isla está sola.",
        "Si los dos extremos ya están unidos, cerraría un ciclo: se descarta. Si no, se construye: unir y sumar.",
        ("Con I − 1 puentes elegidos hemos terminado. Si se acaban y faltan, el grafo no es conexo.", "gold"),
    ], size=23, gap=16)
    segs.append((s, "Las islas son vértices, los puentes aristas y el coste es el valor: buscamos un árbol de recubrimiento de coste mínimo. Kruskal ordena las aristas de menor a mayor, "
                    "y usa un conjunto disjunto, que al principio tiene cada isla sola. Si los dos extremos de un puente ya están unidos, se descarta porque cerraría un ciclo. Si no, se construye: se unen y se suma su coste. "
                    "Cuando llevamos una arista menos que vértices, hemos terminado. Y si se acaban los puentes antes, el grafo no es conexo.", 0))

    s = Slide("El código", "EJ_06-3.cpp")
    s.code(24, 84, 800, 520, CODE, hl={L_SORT, L_BRK, L_UNI, L_UNIR, L_COS, L_FIN}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["GrafoValorado(cin, 1): lee I, P y los puentes desde 1.",
                              "sort: operator< de Arista compara el valor.",
                              "Si ya hay I − 1: break.",
                              "!unidos ⇒ unir, sumar y contar.",
                              "Al final, ¿I − 1 elegidos? Coste o mensaje.",
                              "long long: la suma llega a 10¹⁰."], size=19, gap=14)
    segs.append((s, "En el código leemos el grafo, que numera las islas desde uno, y ordenamos las aristas, porque el operador menor de Arista compara los valores. "
                    "Recorremos los puentes: si ya llevamos una arista menos que islas, salimos. Si los extremos no están unidos, los unimos, sumamos el coste y contamos. "
                    "Al final, si se han elegido I menos uno puentes, escribimos el coste, y si no, el mensaje. La suma puede ser grande, así que va en un long long.", 0))

    t1, p1, f1 = trazas(EJ1, "ejemplo 1 · 4 islas, 5 puentes", "Ejemplo 1: Kruskal paso a paso")
    segs += t1
    segs.append((slide_final("Ejemplo 1: resultado", COR, EJ1, "sum", p1, f1, "ejemplo 1 · 4 islas, 5 puentes",
                             "Tres puentes unen las cuatro islas: coste 2 + 5 + 7 = 14.", "14", "2 + 5 + 7 = 14"),
                 "Con tres puentes quedan las cuatro islas en un solo conjunto. El coste es dos más cinco más siete: catorce.", 0))

    t2, p2, f2 = trazas(EJ2, "ejemplo 2 · la isla 3 queda aislada", "Ejemplo 2: no se puede")
    segs += t2
    segs.append((slide_final("Ejemplo 2: resultado", COR, EJ2, "sum", p2, f2, "ejemplo 2 · la isla 3 queda aislada",
                             "Solo 2 puentes elegidos < 3: la isla 3 queda aislada.", "No hay puentes suficientes", "elegidos = 2  <  I − 1 = 3"),
                 "El tercer puente cierra un ciclo y se descarta. Solo hemos elegido dos puentes, menos que tres: la isla tres queda aislada y el mensaje es: no hay puentes suficientes.", 0))

    segs.append((ideas("Detalles y coste", [
        "I = 1: no se elige nada, elegidos = 0 = I − 1 ⇒ coste 0.",
        "Cada caso crea su propia partición de tamaño I.",
        "El mensaje es exacto: «No hay puentes suficientes».",
        "Puentes repetidos entre el mismo par: el más barato gana y el otro es un ciclo.",
        ("Coste: ordenar O(P log P) + partición O(I + P lg* I)  ⇒  O(I + P log P).", "gold"),
    ]), "Algunos detalles. Con una sola isla no se elige nada y el coste es cero. Cada caso crea su propia partición. El mensaje tiene que ser exacto. "
        "Si hay puentes repetidos entre el mismo par, gana el más barato. Y el coste lo domina la ordenación.", 0))

    segs.append((cierre(NOMBRE, [
        "Islas = vértices, puentes = aristas con coste: árbol de recubrimiento de coste mínimo.",
        "Kruskal: ordenar, y por cada puente  !unidos(u, v) ⇒ unir + sumar.",
        "Parar al llegar a I − 1 puentes elegidos.",
        "Si no se llega a I − 1: «No hay puentes suficientes».",
        "O(I + P log P), con el coste en long long.",
    ]), "Resumiendo: un árbol de recubrimiento de coste mínimo con Kruskal. Ordenamos, unimos lo que no esté unido y sumamos. Paramos al elegir una arista menos que islas, "
        "y si no llegamos, escribimos el mensaje.", 0))

    if preview:
        pinta_preview(segs, "06-3")
    else:
        print(f"06-3: {build(segs, '../06-3_archipielago_en_bicicleta.mp4'):.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
