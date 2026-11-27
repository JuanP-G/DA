"""Vídeo EJ 12-7 · Oposiciones a notaría (animado)."""
from vidlib import C, font
from anim import Escena, mix, ease, lerp
from pd_comun import Tabla, aparece, texto
from pd12_comun import e_portada, e_lineas, e_codigo, e_cierre, panel, avance, principal

CPP = "../../12-Evaluacion/EJ_12-7/EJ_12-7.cpp"
A = [6, 5, 4, 3]
n = len(A)
T = [[0] * n for _ in range(n)]
ORDEN = [(i, i + d) for d in range(n) for i in range(n - d)]
for i, j in ORDEN:
    if i < j:
        T[i][j] = min(T[i][k] + T[k + 1][j] for k in range(i, j)) + sum(A[i:j + 1])
assert T[0][n - 1] == 36
TB = Tabla(30, 150, n, n, cw=100, ch=90, lw=70, cabecera=[str(x) for x in A], etiquetas=[str(x) for x in A], tam=34)
BAJO = {(i, j): (30, 40, 62) for i in range(n) for j in range(i)}


def doc(f, x, y, v, u=1.0, borde=None, w=100):
    if u <= 0:
        return
    f.d.rounded_rectangle((x - w / 2, y - 60, x + w / 2, y + 60), 8, fill=mix(C["bot"], (232, 236, 244), u),
                          outline=mix(C["bot"], borde or (120, 130, 160), u), width=6 if borde else 3)
    f.d.text((x, y - 8), str(v), font=font(36, True), fill=mix(C["bot"], (20, 30, 55), u), anchor="mm")
    f.d.text((x, y + 34), "págs.", font=font(18), fill=mix(C["bot"], (90, 100, 130), u), anchor="mm")


def dib(f):
    for k, v in enumerate(A):
        doc(f, 800 + 115 * k, 310, v, f.p(0.3 + 0.2 * k, 0.5))


def e_problema(f):
    texto(f, (640, 80), "unir PDFs de dos en dos, sin cambiar el orden", 30, "gold", aparece(f, f.c(0)), anchor="mm")
    for k, v in enumerate(A):
        doc(f, 370 + 180 * k, 220, v, aparece(f, f.c(0)))
    if f.t >= f.c(1):
        texto(f, (640, 330), "cada unión tarda tantos segundos como páginas resultan", 28, "text", aparece(f, f.c(1)), anchor="mm")
    if f.t >= f.c(2):
        u = aparece(f, f.c(2))
        texto(f, (640, 420), "6+5 = 11     4+3 = 7     11+7 = 18", 32, "text", u, mono=True, anchor="mm")
        texto(f, (640, 480), "total: 11 + 7 + 18 = 36", 36, "green", u, mono=True, anchor="mm")
    if f.t >= f.c(3):
        u = aparece(f, f.c(3))
        texto(f, (640, 570), "de izquierda a derecha: 11 + 15 + 18 = 44", 30, "muted", u, mono=True, anchor="mm")


def e_tabla(f):
    resto = [p for p in ORDEN if p[0] < p[1]]
    nb = n if f.t >= f.c(1) else 0
    nn = avance(f, 2, 5, len(resto))
    vals = {(i, i): 0 for i in range(nb)}
    vals.update({p: T[p[0]][p[1]] for p in resto[:nn]})
    cur = resto[nn] if nn < len(resto) and f.t >= f.c(2) else None
    marca = {cur: "gold"} if cur else {}
    if f.t >= f.c(5):
        marca = {(0, n - 1): "green"}
    TB.dibuja(f, vals, marca=marca, sombra=BAJO)
    if cur:
        i, j = cur
        pags = sum(A[i:j + 1])
        filas = []
        for k in range(i, j):
            v = T[i][k] + T[k + 1][j] + pags
            izq, der = " ".join(map(str, A[i:k + 1])), " ".join(map(str, A[k + 1:j + 1]))
            filas.append((f"({izq}) ({der}):  {T[i][k]}+{T[k+1][j]}+{pags} = {v}", "green" if v == T[i][j] else "text"))
        panel(f, 560, 150, 690, 250, f"juntar {' '.join(map(str, A[i:j + 1]))}", filas)
    if f.t >= f.c(5):
        texto(f, (900, 520), "tiempo(1, 4) = 36", 38, "green", aparece(f, f.c(5)), mono=True, anchor="mm")


ESC = [
    Escena("Oposiciones a notaría. Fusionar muchos documentos en uno, en el menor tiempo posible y sin desordenarlos.",
           e_portada("12-7", "Oposiciones a notaría", dib), titulo="Portada", extra=1.0),
    Escena("Hay que unir varios documentos de dos en dos, manteniendo el orden. "
           "Cada unión tarda un segundo por página del resultado. "
           "Con seis, cinco, cuatro y tres páginas, lo mejor es unir las dos parejas y después los dos bloques: treinta y seis. "
           "Unirlos de izquierda a derecha costaría cuarenta y cuatro.",
           e_problema, titulo="El problema", extra=1.5),
    Escena("Pensemos en la última unión. Junta un bloque del principio con un bloque del final. "
           "Tiempo de i, j es el mínimo para juntar los documentos de i a j. "
           "Un solo documento no cuesta nada. "
           "Si el corte está en ka, se resuelve cada mitad por separado. "
           "La última unión cuesta todas las páginas, sea cual sea el corte. "
           "Probamos todos los cortes y nos quedamos con el mínimo.",
           e_lineas([(1, 90, "la última unión: (i..k) con (k+1..j)", "gold", 32),
                     (2, 190, "tiempo(i, i) = 0", "text", 32, True),
                     (3, 300, "tiempo(i, k) + tiempo(k+1, j)", "text", 34, True),
                     (5, 380, "+ páginas(i..j)", "text", 34, True),
                     (6, 490, "mínimo para i ≤ k < j", "green", 32),
                     (6, 570, "como la multiplicación encadenada de matrices", "muted", 26)]), titulo="Recurrencia", extra=1.5),
    Escena("Rellenamos la tabla con el ejemplo. "
           "La diagonal vale cero. "
           "Después los bloques de dos documentos, que cuestan su suma. "
           "Luego los de tres, probando los dos cortes. "
           "Y por último el documento completo. "
           "El mínimo es treinta y seis.",
           e_tabla, titulo="La tabla", extra=3.0),
    Escena("No sirve el algoritmo de Huffman, que une los dos más pequeños, porque aquí solo se pueden unir vecinos. "
           "Tampoco basta con unir siempre la pareja vecina más corta. "
           "Con tres, dos, dos y tres, ese voraz tarda veintiuno, y lo óptimo son veinte.",
           e_lineas([(0, 130, "Huffman no: solo se unen vecinos", "gold", 34),
                     (1, 240, "¿la pareja vecina más corta?  tampoco", "text", 30),
                     (2, 360, "3 2 2 3    voraz: 4 + 7 + 10 = 21", "muted", 30, True),
                     (2, 440, "(3 2) (2 3):  5 + 5 + 10 = 20", "green", 30, True)]), titulo="¿Por qué no voraz?", extra=1.5),
    Escena("En el código guardamos sumas acumuladas para saber las páginas de cualquier bloque al instante. "
           "La tabla se recorre por longitudes crecientes. "
           "Para cada bloque probamos todos los cortes. "
           "Y sumamos las páginas del bloque.",
           e_codigo(CPP, "vector<int> suma(n + 1, 0);", "cout << tiempo[1][n]",
                    [["suma[i] = suma[i - 1] + p;"], ["for (int largo = 2"], ["for (int k = i + 1; k < j; ++k)", "mejor = min("],
                     ["tiempo[i][j] = mejor + suma[j] - suma[i - 1];"]],
                    [("sumas", "páginas(i..j) en O(1)"), ("longitudes", "cortos antes que largos"),
                     ("cortes", "k de i a j−1"), ("coste final", "O(n³), n ≤ 200")], size=15),
           titulo="El código", extra=1.5),
    Escena("Resumiendo: programación dinámica sobre intervalos. "
           "Se elige cuál es la última unión. "
           "Esa unión cuesta siempre todas las páginas del bloque. "
           "Y el coste es ene al cubo.",
           e_cierre("Oposiciones a notaría", [
               "estado: el bloque de documentos i..j",
               "elegir la última unión (el corte k)",
               "tiempo(i, k) + tiempo(k+1, j) + páginas(i..j)",
               "O(n³) en tiempo, O(n²) en memoria"]), titulo="Resumen", extra=1.5),
]

if __name__ == "__main__":
    principal(ESC, "12-7", "../12-7_oposiciones_a_notaria.mp4")
