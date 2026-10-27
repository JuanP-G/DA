"""Vídeo EJ 06-5 · Las minas del emperador Trajano (Kruskal hasta unir origen y destino: minimax)."""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line
from v06_teoria import limpia, wgraph
from v06e_comun import TEMA, sim, dibuja, slide_paso, slide_final, narra, pinta_preview

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-5/EJ_06-5.cpp"
NOMBRE = "Las minas del emperador Trajano"
COR = "EJ 06-5"
I0 = find_line(CPP, "void resuelveCaso()")
L_SORT = find_line(CPP, "sort(galerias.begin()")
L_BRK = find_line(CPP, "if (cd.unidos(origen, destino)) break;")
L_UNI = find_line(CPP, "if (!cd.unidos(u, v))")
L_UNIR = find_line(CPP, "cd.unir(u, v);")
L_AG = find_line(CPP, "aguante = a.valor();")
L_FIN = find_line(CPP, "if (cd.unidos(origen, destino)) cout", L_BRK + 1)
CODE = limpia(code_lines(CPP, I0, L_FIN + 1, maxc=72))

EJ1 = dict(n=4, org=1, dst=4, E=[(1, 2, 2), (2, 4, 5), (1, 3, 6), (4, 1, 10)],
           pos={1: (760, 210), 2: (1040, 210), 3: (760, 440), 4: (1040, 440)})


def trazas(ej, nombre_ej, titulo):
    pasos, fin = sim(ej, "par")
    segs = []
    for i in range(len(pasos)):
        s = slide_paso(titulo, COR, ej, "par", pasos, i, nombre_ej, "galerías")
        st = pasos[i]
        a, b, c = ej["E"][st["k"]]
        if st["d"] == "une":
            cap = f"{a}–{b} ({c} s): se une. Aguante = {c}."
        elif st["d"] == "ciclo":
            cap = f"{a} y {b} ya están unidas: se descarta."
        else:
            cap = f"{ej['org']} y {ej['dst']} ya están unidos: se para."
        s.caption(cap, y=626)
        segs.append((s, narra(ej, "par", pasos, i, "La galería entre las cámaras"), 0))
    return segs, pasos, fin


def main(preview=False):
    segs = [(portada(NOMBRE, COR, TEMA),
             "Las minas del emperador Trajano. Es un Kruskal que se detiene en cuanto el origen y el destino quedan unidos: un camino de cuello de botella.", 0)]

    segs.append((ideas("El problema", [
        "N cámaras y M galerías de doble sentido; cada una tarda cierto tiempo en recorrerse.",
        "Palencia Jones va de la cámara origen a la cámara destino y descansa en cada cámara.",
        "Solo cuenta lo que aguanta la respiración en UNA galería: la más larga del camino.",
        ("Salida: el menor máximo posible, o «IMPOSIBLE».", "gold"),
    ]), "Hay cámaras y galerías que se recorren en los dos sentidos, cada una con su tiempo. Palencia Jones va del origen al destino, y descansa en cada cámara, "
        "así que solo cuenta cuánto aguanta la respiración en una galería, la más larga del camino. Hay que dar el menor máximo posible, o imposible.", 0))

    s = Slide("No es la suma: es el máximo", TEMA)
    s.box(40, 100, 560, 360, "ejemplo 1: de 1 a 4")
    pos = {1: (120, 200), 2: (320, 200), 3: (120, 400), 4: (520, 400)}
    wgraph(s, {1: (110, 190), 2: (310, 190), 4: (500, 390), 3: (110, 390)}, EJ1["E"], r=24, lsize=22)
    s.box(620, 100, 620, 360, "dos caminos")
    s.text((650, 150), "1 → 4 directo:", size=22, color="muted")
    s.text((650, 185), "máximo 10", size=28, mono=True)
    s.text((650, 250), "1 → 2 → 4  (2 y 5):", size=22, color="muted")
    s.text((650, 285), "suma 7, máximo 5", size=28, mono=True, color="gold")
    s.text((650, 350), "respuesta: 5", size=34, bold=True, color="gold")
    s.bullets(60, 490, 1160, [
        "No es Dijkstra: no se minimiza la suma, sino la galería más larga (minimax).",
        ("Con límite T se pueden usar las galerías de tiempo ≤ T: el menor T que conecta origen y destino sale de Kruskal.", "gold"),
    ], size=22, gap=12)
    segs.append((s, "Atención: no se minimiza la suma, sino la galería más larga. En el ejemplo, ir directo de la uno a la cuatro cuesta diez. El rodeo por la dos suma siete, pero su galería más larga es cinco, y esa es la respuesta. "
                    "No es un problema de caminos mínimos. Con un límite T podemos usar las galerías de tiempo menor o igual que T, y el menor T que conecta origen y destino lo da Kruskal.", 0))

    s = Slide("El código", "EJ_06-5.cpp")
    s.code(24, 84, 800, 520, CODE, hl={L_SORT, L_BRK, L_UNI, L_UNIR, L_AG, L_FIN}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["Se lee el grafo y después origen y destino (−1).",
                              "sort: galerías por tiempo creciente.",
                              "unidos(origen, destino) ⇒ break.",
                              "!unidos ⇒ unir y  aguante = valor.",
                              "Al final: aguante o IMPOSIBLE.",
                              "origen == destino: ya están unidos ⇒ 0."], size=19, gap=14)
    segs.append((s, "En el código se lee el grafo, y después el origen y el destino, restándoles uno. Se ordenan las galerías por tiempo. En cada vuelta, si origen y destino ya están unidos, salimos. "
                    "Si los extremos de la galería no están unidos, los unimos y guardamos su valor en aguante. Al final, si origen y destino están unidos escribimos aguante, y si no, imposible. "
                    "Si origen y destino son la misma cámara, ya están unidos y el aguante sigue valiendo cero.", 0))

    t1, p1, f1 = trazas(EJ1, "ejemplo 1 · de la cámara 1 a la 4", "Ejemplo 1: Kruskal hasta unir 1 y 4")
    segs += t1
    segs.append((slide_final("Ejemplo 1: resultado", COR, EJ1, "par", p1, f1, "ejemplo 1 · de la cámara 1 a la 4",
                             "La galería de 5 s es la más larga del mejor camino: respuesta 5.", "5", "aguante = 5"),
                 "Origen y destino quedan unidos al aceptar la galería de cinco segundos: esa es la respuesta. Las galerías de seis y de diez no se llegan a mirar.", 0))

    segs.append((ideas("Casos y coste", [
        "origen == destino: ya están unidos desde el principio ⇒ 0.",
        "Nunca se unen (por ejemplo M = 0 con N = 2): «IMPOSIBLE», en mayúsculas.",
        "Se escribe el tiempo de UNA galería (un máximo), no la suma del camino.",
        "La partición se crea por caso, con tamaño N.",
        ("Coste: O(N + M log M); en el peor caso se miran todas las galerías.", "gold"),
    ]), "Los casos especiales. Si origen y destino son el mismo, ya están unidos y la respuesta es cero. Si nunca se unen, imposible, en mayúsculas. "
        "Se escribe el tiempo de una galería, no la suma. Y el coste lo domina la ordenación.", 0))

    segs.append((cierre(NOMBRE, [
        "Camino de cuello de botella: minimizar la galería más larga, no la suma.",
        "Kruskal hasta unidos(origen, destino).",
        "Respuesta: el valor de la última arista aceptada.",
        "origen == destino ⇒ 0; nunca se unen ⇒ «IMPOSIBLE».",
        "O(N + M log M).",
    ]), "Resumiendo: el menor máximo se encuentra con Kruskal, parando en cuanto origen y destino quedan unidos. La respuesta es la última galería aceptada.", 0))

    if preview:
        pinta_preview(segs, "06-5")
    else:
        print(f"06-5: {build(segs, '../06-5_minas_de_trajano.mp4'):.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
