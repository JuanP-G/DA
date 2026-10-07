"""Vídeo EJ 04-3 · Detección de manchas negras"""
import sys
from vidlib import Slide, portada, ideas, cierre, build, code_lines, find_line, C

CPP = "../../EJ_04-3/EJ_04-3.cpp"
NOMBRE = "Detección de manchas negras"

B1 = ["-#-#---#", "-###---#", "----####", "-#------", "-#-#----", "-###-##-", "###--##-", "--#-----"]
B2 = ["#-#-#-###-", "#-#-#-#-#-", "#-#-#-#-#-", "#-#-#-#-#-"]
MCOL = ["blue", "purple", "green", "gold", "red"]

L_NEW = find_line(CPP, "if (negro[v] && !visit[v])")
L_NUM = find_line(CPP, "++num;")
L_TAM = find_line(CPP, "int tam = dfs(g, v);")
L_MAX = find_line(CPP, "maxim = max(maxim, tam);")
L_DFS = find_line(CPP, "int dfs(")
L_REC = find_line(CPP, "if (!visit[w]) tam += dfs(g, w);")
L_RET = find_line(CPP, "return tam;")
L_V = find_line(CPP, "int v = i * C + j;")
L_DER = find_line(CPP, "g.ponArista(v, v + 1);")
L_ABA = find_line(CPP, "g.ponArista(v, v + C);")
CODE_CLASE = code_lines(CPP, find_line(CPP, "Manchas(Grafo const& g"), find_line(CPP, "};", L_DFS),
                        skip=[(find_line(CPP, "int numero() const") - 1, find_line(CPP, "// devuelve cuantos pixeles"))])
CODE_LEER = code_lines(CPP, find_line(CPP, "vector<string> bitmap(F);"), find_line(CPP, "Manchas m(g, negro);") - 1, maxc=64)


def aristas(b):
    F, Cc = len(b), len(b[0])
    E = []
    for i in range(F):
        for j in range(Cc):
            if b[i][j] != "#":
                continue
            if j + 1 < Cc and b[i][j + 1] == "#":
                E.append(((i, j), (i, j + 1)))
            if i + 1 < F and b[i + 1][j] == "#":
                E.append(((i, j), (i + 1, j)))
    return E


def manchas(b):
    """Simula Manchas: mismo orden de vértices y de adyacentes que Grafo. Devuelve [(inicio, [orden de visita])]."""
    F, Cc = len(b), len(b[0])
    ady = {}
    for a, c in aristas(b):
        ady.setdefault(a, []).append(c)
        ady.setdefault(c, []).append(a)
    visit, res = set(), []
    for i in range(F):
        for j in range(Cc):
            if b[i][j] == "#" and (i, j) not in visit:
                orden = []

                def dfs(p):
                    visit.add(p)
                    orden.append(p)
                    for q in ady.get(p, []):
                        if q not in visit:
                            dfs(q)
                dfs((i, j))
                res.append(((i, j), orden))
    return res


M1, M2 = manchas(B1), manchas(B2)


def slide_mancha(k, hechas, actual, orden, mostrar_orden, num, maxim, hl, cap):
    s = Slide("Ejecución · Caso 1", f"mancha {k} de {len(M1)}")
    s.code(24, 84, 610, 520, CODE_CLASE, hl=hl, title="class Manchas", size=16)
    fills, labels = {}, {}
    for c, (_, ords) in enumerate(hechas):
        for p in ords:
            fills[p] = MCOL[c]
    if mostrar_orden:
        for n, p in enumerate(orden, 1):
            fills[p] = MCOL[len(hechas)]
            labels[p] = n
    s.box(652, 84, 604, 360, "bitmap 8 × 8")
    s.grid(812, 112, B1, 38, fills=fills, labels=labels, rings=[actual] if actual else [], lsize=15)
    s.box(652, 460, 604, 144, "estado")
    s.text((672, 506), "num", size=18, color="muted", bold=True)
    s.pill(735, 498, str(num), fill="gold")
    s.text((830, 506), "maxim", size=18, color="muted", bold=True)
    s.pill(910, 498, str(maxim), fill="gold")
    x = 672
    for c, (_, ords) in enumerate(hechas):
        x = s.pill(x, 552, f"mancha {c + 1}: {len(ords)}", fill=MCOL[c], size=15) + 8
    s.caption(cap, y=628)
    return s


def main(preview=False):
    segs = [(portada(NOMBRE, "EJ 04-3"),
             "Detección de manchas negras. Vemos cómo se plantea, por qué funciona y cómo se ejecuta paso a paso.", 0)]

    s = Slide("El problema")
    s.box(60, 90, 400, 400, "caso 1")
    s.grid(100, 130, B1, 40, rings=[(1, 3), (2, 4)])
    s.bullets(500, 110, 720, [
        "Bitmap de píxeles blancos (-) y negros (#).",
        "Dos negros están en la misma mancha si se pasa de uno a otro solo por negros, en horizontal o vertical.",
        "Piden: cuántas manchas hay y cuántos píxeles tiene la mayor.",
        ("Las diagonales NO cuentan: los dos píxeles marcados se tocan por una esquina y son de manchas distintas.", "gold"),
    ], size=22)
    s.caption("Caso 1: 4 manchas, la mayor de 10 píxeles  →  \"4 10\"", y=540)
    segs.append((s, "Tenemos un bitmap de píxeles blancos y negros. Dos píxeles negros están en la misma mancha si podemos ir de uno a otro "
                    "pasando solo por píxeles negros y moviéndonos en horizontal o en vertical. Nos piden cuántas manchas hay y el tamaño de la mayor.", 0))
    segs.append((s, "Ojo con las diagonales: los dos píxeles marcados en rojo se tocan solo por una esquina, así que pertenecen a manchas distintas. "
                    "En este caso hay cuatro manchas y la mayor tiene diez píxeles.", 0))

    s = Slide("Cómo se plantea: es un grafo")
    labels = {(i, j): i * 8 + j for i in range(8) for j in range(8)}
    s.box(60, 90, 400, 420, "vértice = i·C + j")
    s.grid(100, 130, B1, 40, labels=labels, links=aristas(B1), lsize=11, esquina=True)
    s.bullets(500, 110, 720, [
        "Cada píxel es un vértice. Grafo numera de 0 a V-1, así que el píxel (i, j) es el vértice i·C + j (fila por fila).",
        "Dos píxeles NEGROS vecinos (arriba, abajo, izquierda, derecha) se unen con una arista.",
        ("Una mancha es una COMPONENTE CONEXA de píxeles negros.", "gold"),
        "Respuesta: número de componentes de negros y tamaño de la mayor.",
    ], size=22)
    segs.append((s, "Aunque no lo parezca, es un problema de grafos. Cada píxel es un vértice, y como el grafo numera sus vértices de cero a uve menos uno, "
                    "el píxel de la fila i y la columna jota es el vértice i por ce más jota: se numeran fila por fila.", 0))
    segs.append((s, "Dos píxeles negros vecinos se unen con una arista; son las líneas amarillas. Entonces una mancha es exactamente una componente conexa "
                    "de píxeles negros, y la respuesta es cuántas componentes hay y el tamaño de la mayor.", 0))

    s = Slide("Cada arista, una sola vez")
    mini = ["###", "###", "###"]
    s.box(60, 90, 420, 420, "vecinos del píxel v")
    s.grid(150, 150, mini, 80, fills={(1, 1): "gold", (0, 1): "muted", (1, 0): "muted", (1, 2): "green", (2, 1): "green"},
           labels={(0, 1): "v-C", (1, 0): "v-1", (1, 1): "v", (1, 2): "v+1", (2, 1): "v+C"}, lsize=20)
    s.text((270, 420), "verde: aristas que pone v", size=18, color="green", anchor="mm")
    s.text((270, 450), "gris: las puso el otro píxel", size=18, color="muted", anchor="mm")
    s.bullets(520, 110, 700, [
        "Derecha: misma fila, columna + 1  →  vértice v + 1.",
        "Abajo: fila + 1, misma columna  →  vértice v + C.",
        "Desde cada negro solo miro DERECHA y ABAJO.",
        "La arista con el de la izquierda y el de arriba ya la puso ese otro píxel cuando le tocó a él.",
        ("Si mirase los 4 vecinos, cada arista saldría dos veces.", "muted"),
    ], size=22)
    segs.append((s, "Para poner las aristas, desde cada píxel negro miramos solo el de su derecha, que es el vértice uve más uno, y el de abajo, "
                    "que es uve más ce. La arista con el de la izquierda y con el de arriba ya la puso ese otro píxel cuando le tocó. "
                    "Si miráramos los cuatro vecinos, cada arista aparecería dos veces.", 0))

    s = Slide("El código · construir el grafo", "EJ_04-3.cpp")
    s.code(24, 84, 1232, 470, CODE_LEER, hl={L_V, L_DER, L_ABA}, title="resuelveCaso", size=17)
    s.caption("Los píxeles blancos se quedan como vértices sueltos; negro[v] dice cuáles son negros", y=585)
    segs.append((s, "En el código, leemos el bitmap como un vector de strings y creamos un grafo con efe por ce vértices. Para cada píxel negro calculamos su número, "
                    "lo marcamos en el vector negro, y ponemos la arista con el de la derecha y con el de abajo si también son negros. "
                    "Los blancos se quedan como vértices sin aristas.", 0))

    segs.append((ideas("El recorrido", [
        "Igual que en el EJ 04-2: un dfs por componente que devuelve su tamaño.",
        "Pero solo se lanza desde píxeles NEGROS sin visitar (los blancos no son mancha).",
        "Cada vez que se lanza: una mancha más (num++), y maxim = max(maxim, tam).",
        "¿dfs recursivo? Sí: ninguna mancha pasa de 50.000 píxeles, así que la recursión baja como mucho 50.000 niveles.",
    ]), "El recorrido es el mismo que en el ejercicio dos: un D F S por componente que devuelve cuántos vértices visita. La diferencia es que solo lo "
        "lanzamos desde píxeles negros que aún no están en ninguna mancha, y cada vez que lo lanzamos contamos una mancha más. "
        "El enunciado garantiza que ninguna mancha pasa de cincuenta mil píxeles, que es justo la profundidad máxima de la recursión.", 0))

    num = maxim = 0
    hechas = []
    for k, (ini, orden) in enumerate(M1, 1):
        v = ini[0] * 8 + ini[1]
        segs.append((slide_mancha(k, hechas, ini, orden, False, num, maxim, {L_NEW, L_NUM},
                                  f"El píxel ({ini[0]}, {ini[1]}) = vértice {v} es negro y no está visitado: mancha nueva"),
                     f"Recorriendo los vértices en orden, el {v} es el primer píxel negro sin visitar: empieza la mancha número {k}.", 0))
        num += 1
        maxim = max(maxim, len(orden))
        segs.append((slide_mancha(k, hechas, None, orden, True, num, maxim, {L_REC, L_RET, L_TAM, L_MAX},
                                  f"El dfs visita {len(orden)} píxeles (los números son el orden de visita) → maxim = {maxim}"),
                     f"El D F S recorre toda la mancha. Los números son el orden en que visita los píxeles: en total {len(orden)}. "
                     f"El máximo pasa a ser {maxim}.", 0))
        hechas.append((ini, orden))
    s = slide_mancha(len(M1), hechas, None, [], False, num, maxim, set(), f"4 manchas, la mayor de {maxim}  →  se escribe \"4 10\"")
    segs.append((s, "Ya no quedan píxeles negros sin visitar. Hay cuatro manchas y la mayor tiene diez píxeles: la salida es cuatro diez.", 0))

    s = Slide("Caso 2")
    fills = {p: MCOL[c] for c, (_, o) in enumerate(M2) for p in o}
    s.grid(240, 120, B2, 80, fills=fills)
    s.caption("Columnas 0, 2 y 4: tres manchas de 4.   Columnas 6 y 8, unidas por arriba: una de 9.", y=480)
    s.caption("Una mancha no tiene por qué ser un rectángulo  →  \"4 9\"", y=525)
    segs.append((s, "En el segundo caso, las tres primeras columnas negras son tres manchas de cuatro píxeles. Las dos de la derecha están unidas por la fila de arriba "
                    "y forman una sola mancha de nueve: la respuesta es cuatro nueve.", 0))

    segs.append((cierre(NOMBRE, [
        "Píxel (i, j) → vértice i·C + j; aristas entre negros vecinos en horizontal o vertical.",
        "Solo derecha y abajo, para no repetir aristas.",
        "Mancha = componente conexa de negros: un dfs por cada negro no visitado.",
        "Respuesta: número de dfs lanzados y el mayor tamaño devuelto.",
        "Coste: O(F·C) por caso.",
    ]), "Resumiendo: cada píxel es un vértice, unimos los negros vecinos en horizontal y vertical mirando solo a la derecha y abajo, "
        "y cada mancha es una componente conexa. Contamos los D F S que lanzamos y nos quedamos con el mayor tamaño. El coste es lineal en el número de píxeles.", 0))

    if preview:
        import os
        os.makedirs("preview", exist_ok=True)
        for i, (sl, _, _) in enumerate(segs):
            sl.img.save(f"preview/04-3_{i:02}.png")
        print(len(segs), "diapositivas")
    else:
        t = build(segs, "../04-3_manchas_negras.mp4")
        print(f"04-3: {t:.0f}s")


if __name__ == "__main__":
    main("--preview" in sys.argv)
