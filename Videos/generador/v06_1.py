"""Vídeo EJ 06-1 · Petroleros hundidos (conjuntos disjuntos sobre una rejilla que solo crece)."""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, W
from v06_teoria import limpia, tabla, sim_petroleros, manchas, EJ1
from v06e_comun import TEMA, pinta_preview

CPP = "../../6-Conjuntos disjuntos y grafos valorados/EJ_06-1/EJ_06-1.cpp"
NOMBRE = "Petroleros hundidos"
COR = "EJ 06-1"
A0 = find_line(CPP, "class Manchas")
A1 = find_line(CPP, "int masGrande() const")
CLASE = limpia(code_lines(CPP, A0, A1, maxc=76))
R0 = find_line(CPP, "void resuelveCaso()")
RES = limpia(code_lines(CPP, R0, find_line(CPP, "cout << '\\n';"), maxc=76))
L_CEL = find_line(CPP, "int celda = i * C + j;")
L_PET = find_line(CPP, "petroleo[celda] = true;")
L_VEC = find_line(CPP, "for (int di = -1")
L_FUE = find_line(CPP, "if (a < 0 || a >= F")
L_UNI = find_line(CPP, "cd.unir(celda, a * C + b);")
L_MAX = find_line(CPP, "mayor = max(mayor, cd.cardinal(celda));")
L_INI = find_line(CPP, "if (fila[j] == '#') m.anade(i, j);")
L_NUE = find_line(CPP, "m.anade(f - 1, c - 1);")


def main(preview=False):
    segs = [(portada(NOMBRE, COR, TEMA),
             "Petroleros hundidos. Una rejilla en la que solo aparecen manchas nuevas: es exactamente el caso de los conjuntos disjuntos, que solo saben unir.", 0)]

    segs.append((ideas("El problema", [
        "Rejilla de F × C celdas (hasta 1.000 × 1.000): «-» es mar y «#» es petróleo.",
        "Dos celdas de petróleo son de la misma mancha si se llega de una a otra por petróleo, en 8 direcciones.",
        "Después van apareciendo N celdas nuevas (hasta 100.000), una a una.",
        ("Salida: el tamaño de la mancha mayor al principio y tras cada celda nueva.", "gold"),
    ]), "Tenemos una rejilla con mar y petróleo. Dos celdas de petróleo son de la misma mancha si se puede ir de una a otra pasando solo por petróleo, moviéndonos en ocho direcciones. "
        "Después van apareciendo celdas nuevas de petróleo, una a una, y hay que escribir el tamaño de la mancha más grande al principio y tras cada celda nueva.", 0))

    s = Slide("Las manchas solo crecen o se funden", TEMA)
    s.box(40, 100, 1200, 150, "idea")
    s.text((70, 150), "las celdas solo se AÑADEN, nunca se quitan", size=32, mono=True, color="gold")
    s.text((70, 205), "⇒ una mancha nunca se parte: solo crece o se funde con otra.", size=24, color="muted")
    s.bullets(60, 290, 1160, [
        "Repetir un DFS de toda la rejilla tras cada celda cuesta O((N + 1) · F · C): ~10¹¹, no pasa.",
        ("Una partición que solo sabe UNIR es justo lo que hace falta: conjuntos disjuntos.", "gold"),
        "La rejilla es el grafo: no se construye ninguna lista de adyacencia.",
    ], size=23, gap=16)
    segs.append((s, "La clave es fijarse en cómo cambia la imagen: las celdas solo se añaden, nunca se quitan, así que una mancha nunca se parte, solo crece o se funde con otra. "
                    "Repetir un recorrido de toda la rejilla tras cada celda nueva costaría del orden de diez elevado a once operaciones, demasiado. "
                    "Una partición que solo sabe unir es justo lo que hace falta: los conjuntos disjuntos. Y la rejilla es el grafo, no hace falta construir listas de adyacencia.", 0))

    s = Slide("El modelo", TEMA)
    tabla(s, 70, 130, ["Idea", "En el problema"], [
        ["Elemento", "cada celda (i, j)  →  número  i·C + j"],
        ["Conjunto", "una mancha"],
        ["unir(a, b)", "dos celdas de petróleo vecinas (8 direcciones)"],
        ["cardinal(a)", "tamaño de la mancha de a"],
    ], [300, 820], rh=56, size=24)
    s.bullets(70, 410, W - 140, [
        "anade(i, j): marca la celda, la une con sus vecinas de petróleo y  mayor = max(mayor, cardinal(celda)).",
        ("Solo ha podido cambiar la mancha de la celda nueva, y el máximo nunca baja: no hace falta recorrer los conjuntos.", "gold"),
        "La imagen inicial se procesa con la misma operación, celda a celda.",
    ], size=22, gap=14)
    segs.append((s, "Cada celda es un elemento, con el número i por C más j. Un conjunto es una mancha. Unir es juntar dos celdas de petróleo vecinas, y el cardinal es el tamaño de la mancha. "
                    "La operación añade marca la celda, la une con sus vecinas de petróleo, y actualiza el máximo con el cardinal de su mancha. Solo ha podido cambiar la mancha de la celda nueva, y el máximo nunca baja. "
                    "La imagen inicial se procesa con esa misma operación, celda a celda.", 0))

    s = Slide("El código: anade", "EJ_06-1.cpp")
    s.code(24, 84, 800, 520, CLASE, hl={L_CEL, L_PET, L_VEC, L_FUE, L_UNI, L_MAX}, title="class Manchas", size=15)
    s.box(844, 84, 412, 520, "qué hace")
    s.bullets(864, 130, 372, ["celda = i·C + j y se marca como petróleo.",
                              "Doble bucle di, dj ∈ {−1, 0, 1}: los 8 vecinos.",
                              "Se salta (0, 0) y lo que cae fuera de la rejilla.",
                              ("Solo se une con las que YA son petróleo.", "gold"),
                              "mayor = max(mayor, cardinal(celda))."], size=19, gap=14)
    segs.append((s, "La clase Manchas guarda un conjunto disjunto con una celda por elemento. En añade, se marca la celda y se recorren los ocho vecinos con dos bucles, saltando la propia celda y las que caen fuera de la rejilla. "
                    "Solo se une con los vecinos que ya son petróleo, porque unir con mar rompería el resultado. Y al final se actualiza el máximo con el cardinal de la mancha de la celda.", 0))

    s = Slide("El código: resuelveCaso", "EJ_06-1.cpp")
    s.code(24, 84, 800, 440, RES, hl={L_INI, L_NUE}, title="resuelveCaso()", size=15)
    s.box(844, 84, 412, 440, "qué hace")
    s.bullets(864, 130, 372, ["Cada fila se lee como una cadena (sin espacios).",
                              "Cada «#» de la imagen inicial: m.anade(i, j).",
                              "Se escribe masGrande(): la salida inicial.",
                              "Cada celda nueva (en base 1 → restar 1): anade y se escribe de nuevo."], size=19, gap=14)
    s.bullets(60, 545, 1160, [("Salida: N + 1 números separados por un espacio, sin espacio al final.", "gold")], size=21, gap=10)
    segs.append((s, "Leemos cada fila como una cadena y, por cada almohadilla, llamamos a añade. Escribimos el máximo inicial. Después, por cada celda nueva, restamos uno a fila y columna, la añadimos y escribimos el máximo. "
                    "La salida son N más uno números separados por un espacio.", 0))

    # ---------------- ejemplo 1 (8x8)
    fills, mayor = manchas(EJ1)
    s = Slide("Ejemplo 1 · imagen inicial", COR)
    s.grid(80, 110, EJ1, 62, fills=fills)
    s.box(640, 110, 600, 340, "manchas")
    s.bullets(660, 160, 560, ["Cada color es un conjunto distinto.", ("La mayor tiene 10 celdas (amarilla).", "gold"), "Salida inicial: 10"], size=22, gap=16)
    segs.append((s, "En el primer ejemplo la imagen inicial tiene varias manchas, cada una de un color. La mayor tiene diez celdas, así que empezamos escribiendo diez.", 0))
    nuevas = [(6, 8), (2, 5), (6, 5)]
    bm2 = [list(r) for r in EJ1]
    for (f, c) in nuevas:
        bm2[f - 1][c - 1] = "#"
    bm2 = ["".join(r) for r in bm2]
    fills2, _ = manchas(bm2)
    s = Slide("Ejemplo 1 · tras añadir (6,8), (2,5) y (6,5)", COR)
    s.grid(80, 110, bm2, 62, fills=fills2, rings=[(f - 1, c - 1) for f, c in nuevas])
    s.box(640, 110, 600, 340, "salida")
    s.text((670, 170), "10   10   12   16", size=44, color="gold", bold=True)
    s.bullets(660, 250, 560, ["Las celdas nuevas llevan marco rojo.", "Las dos primeras no cambian el máximo.", "La tercera funde varias manchas de golpe: 16."], size=21, gap=14)
    segs.append((s, "Añadimos las tres celdas nuevas. Las dos primeras no cambian el máximo, pero la tercera funde varias manchas de golpe y el máximo pasa a dieciséis. La salida es diez, diez, doce, dieciséis.", 0))

    # ---------------- ejemplo 2 (3x4), paso a paso
    pasos, res = sim_petroleros()
    textos = ["Segundo ejemplo: una rejilla de tres por cuatro, sin petróleo. El máximo vale cero.",
              "Aparece la celda dos, dos, el número cinco. No tiene vecinas de petróleo: mancha de una celda. Máximo uno.",
              "Después la tres, cuatro, el número once. No toca a la anterior: otra mancha de una celda. El máximo sigue en uno.",
              "Y por último la dos, tres, el número seis. Toca al cinco en horizontal y al once en diagonal: hacemos unir con las dos y las tres celdas quedan en una mancha. El cardinal es tres: máximo tres."]
    for k, (negros, ids, mayor_k) in enumerate(res):
        s = Slide("Ejemplo 2 · rejilla 3 × 4 vacía", f"paso {k} de 3" if k else "inicio")
        bm = ["".join("#" if (i, j) in negros else "-" for j in range(4)) for i in range(3)]
        fl, _ = manchas(bm)
        rings = [(pasos[k - 1][0] - 1, pasos[k - 1][1] - 1)] if k else []
        s.grid(90, 120, bm, 88, fills=fl, rings=rings, labels={(i, j): i * 4 + j for i in range(3) for j in range(4)}, lsize=17, esquina=True)
        s.box(520, 110, 720, 300, "estado")
        s.text((550, 150), f"mayor = {mayor_k}", size=40, color="gold", bold=True)
        if k:
            f, c = pasos[k - 1]
            s.text((550, 220), f"celda nueva ({f},{c})  →  número {(f - 1) * 4 + c - 1}", size=24)
            vec = [(i, j) for i in range(3) for j in range(4) if (i, j) in negros and (i, j) != (f - 1, c - 1)
                   and abs(i - (f - 1)) <= 1 and abs(j - (c - 1)) <= 1]
            s.text((550, 270), "vecinas de petróleo: " + (", ".join(str(i * 4 + j) for i, j in vec) if vec else "ninguna"), size=22, color="muted")
            if vec:
                s.text((550, 320), "unir con " + " y ".join(str(i * 4 + j) for i, j in vec), size=22, color="gold")
        s.caption("Salida acumulada: " + " ".join(str(r[2]) for r in res[:k + 1]), y=600)
        segs.append((s, textos[k], 0))

    segs.append((ideas("Detalles y coste", [
        "8 vecinos: di, dj ∈ {−1, 0, 1} menos (0, 0), comprobando límites y que sean petróleo.",
        "Fila y columna del enunciado van de 1; la partición, de 0.",
        "Se escriben N + 1 números por caso, aunque N = 0.",
        "La partición y la rejilla se crean por caso (F·C llega a 10⁶).",
        ("Coste: O(F·C + N), con la lg* de la partición prácticamente constante.", "gold"),
    ]), "Algunos detalles. Los ocho vecinos se recorren con dos bucles, comprobando que están dentro y que son petróleo. Las filas y columnas del enunciado empiezan en uno. "
        "Se escriben N más uno números por caso, incluso si N es cero. La partición se crea por caso. Y el coste es F por C más N, porque la lg estrella es casi constante.", 0))

    segs.append((cierre(NOMBRE, [
        "Las celdas solo se añaden: las manchas crecen o se funden, nunca se parten.",
        "Elemento = celda i·C + j; conjunto = mancha; unir = vecinas de petróleo.",
        "anade(i, j): marcar, unir con las 8 vecinas de petróleo y  mayor = max(mayor, cardinal(celda)).",
        "La imagen inicial usa la misma operación.",
        "O(F·C + N) en lugar de O((N + 1) · F · C).",
    ]), "Resumiendo: conjuntos disjuntos sobre la rejilla. Cada celda nueva se une con sus vecinas de petróleo y el máximo se actualiza con su cardinal. El coste es casi lineal.", 0))

    if preview:
        pinta_preview(segs, "06-1")
    else:
        print(f"06-1: {build(segs, '../06-1_petroleros_hundidos.mp4'):.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
