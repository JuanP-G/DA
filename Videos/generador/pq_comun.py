"""Montículo (cola de prioridad / IndexPQ) para los vídeos animados de los temas 2 y 3."""
from vidlib import C, font
from anim import mix, lerp, ease


class Monticulo:
    """Montículo binario con índices (como IndexPQ). antes(a, b) = True si a va antes que b."""

    def __init__(self, antes):
        self.antes = antes
        self.a = []          # [(elem, prio)]
        self.pos = {}

    def _sw(self, i, j):
        self.a[i], self.a[j] = self.a[j], self.a[i]
        self.pos[self.a[i][0]] = i
        self.pos[self.a[j][0]] = j

    def _flota(self, i):
        while i > 0 and self.antes(self.a[i][1], self.a[(i - 1) // 2][1]):
            self._sw(i, (i - 1) // 2)
            i = (i - 1) // 2

    def _hunde(self, i):
        n = len(self.a)
        while True:
            h = 2 * i + 1
            if h >= n:
                return
            if h + 1 < n and self.antes(self.a[h + 1][1], self.a[h][1]):
                h += 1
            if self.antes(self.a[h][1], self.a[i][1]):
                self._sw(i, h)
                i = h
            else:
                return

    def push(self, e, p):
        self.a.append((e, p))
        self.pos[e] = len(self.a) - 1
        self._flota(len(self.a) - 1)

    def update(self, e, p):
        if e not in self.pos:
            return self.push(e, p)
        i = self.pos[e]
        self.a[i] = (e, p)
        self._flota(i)
        self._hunde(self.pos[e])

    def top(self):
        return self.a[0]

    def pop(self):
        r = self.a[0]
        self._sw(0, len(self.a) - 1)
        self.a.pop()
        del self.pos[r[0]]
        if self.a:
            self._hunde(0)
        return r

    def empty(self):
        return not self.a

    def copia(self):
        return list(self.a)


def arbol(f, arr, cx, y0, ancho, etiqueta, dy=90, r=34, marca=None, u=1.0, colores=None, tam=18):
    """Dibuja el montículo como árbol. etiqueta(elem, prio) -> texto. marca = conjunto de posiciones a resaltar."""
    marca = marca or set()
    pos = []
    for i in range(len(arr)):
        nivel = (i + 1).bit_length() - 1
        k = i - (2 ** nivel - 1)
        n = 2 ** nivel
        x = cx - ancho / 2 + ancho * (k + 0.5) / n
        pos.append((x, y0 + nivel * dy))
    for i in range(1, len(arr)):
        p = (i - 1) // 2
        f.d.line((pos[p], pos[i]), fill=mix(C["bot"], C["border"], u), width=3)
    for i, (e, p) in enumerate(arr):
        x, y = pos[i]
        c = (colores or {}).get(e, C["blue"])
        if i in marca:
            f.d.ellipse((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=mix(C["bot"], C["gold"], u), width=4)
        f.d.ellipse((x - r, y - r, x + r, y + r), fill=mix(C["bot"], C["panel"], u), outline=mix(C["bot"], c, u), width=3)
        for q, line in enumerate(etiqueta(e, p).split("\n")):
            f.d.text((x, y - 9 + q * 20 if "\n" in etiqueta(e, p) else y), line, font=font(tam if q == 0 else tam - 3, True),
                     fill=mix(C["bot"], C["text"] if q == 0 else C["muted"], u), anchor="mm")
    return pos



def _posiciones(n, cx, y0, ancho, dy):
    pos = []
    for i in range(n):
        nivel = (i + 1).bit_length() - 1
        k = i - (2 ** nivel - 1)
        m = 2 ** nivel
        pos.append((cx - ancho / 2 + ancho * (k + 0.5) / m, y0 + nivel * dy))
    return pos


def arbol_anim(f, arrA, arrB, u, cx, y0, ancho, etiqueta, dy=90, r=34, marca_elem=None, colores=None, tam=18):
    """Como arbol(), pero cada nodo se desliza de su sitio en arrA a su sitio en arrB (u de 0 a 1)."""
    u = ease(max(0.0, min(1.0, u)))
    pa = _posiciones(len(arrA), cx, y0, ancho, dy)
    pb = _posiciones(len(arrB), cx, y0, ancho, dy)
    ia = {e: i for i, (e, p) in enumerate(arrA)}
    for i in range(1, len(arrB)):
        f.d.line((pb[(i - 1) // 2], pb[i]), fill=C["border"], width=3)
    for i, (e, p) in enumerate(arrB):
        x1, y1 = pb[i]
        x0, y0_ = pa[ia[e]] if e in ia else (x1, y1 + 60)
        x, y = lerp(x0, x1, u), lerp(y0_, y1, u)
        c = (colores or {}).get(e, C["blue"])
        if marca_elem is not None and e == marca_elem:
            f.d.ellipse((x - r - 7, y - r - 7, x + r + 7, y + r + 7), outline=C["gold"], width=4)
        f.d.ellipse((x - r, y - r, x + r, y + r), fill=C["panel"], outline=c, width=3)
        lines = etiqueta(e, p).split("\n")
        for q, line in enumerate(lines):
            f.d.text((x, y - 9 * (len(lines) - 1) + q * 20), line, font=font(tam if q == 0 else tam - 3, True),
                     fill=C["text"] if q == 0 else C["muted"], anchor="mm")
