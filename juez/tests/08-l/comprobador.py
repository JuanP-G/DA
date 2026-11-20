"""Comprobador de 08-l «Planificación de conferencias»: vale CUALQUIER asignación de salas válida
con el mínimo número de salas.

Cada caso ocupa dos líneas: el número de salas R (debe coincidir con el de la salida esperada, que
es el mínimo) y la sala de cada conferencia (N enteros entre 1 y R, sin dos conferencias que se
solapen en la misma sala; una que empieza justo cuando acaba otra no se solapa con ella).

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/08-l.js en el navegador (el verificador comprueba que coinciden).
"""
import re

_NUM = re.compile(r"^-?\d+$")


def _lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def _casos(entrada):
    v = entrada.split()
    p = 0

    def sig():
        nonlocal p
        p += 1
        return int(v[p - 1])
    for _ in range(sig()):
        n = sig()
        yield [(sig(), sig()) for _ in range(n)]


def _revisa_salas(confs, R, linea):
    """Motivo por el que «linea» no es una asignación válida con R salas, o None."""
    t = linea.split()
    if not all(_NUM.match(x) for x in t):
        return "la línea debería tener solo números de sala"
    n = len(confs)
    if len(t) != n:
        return f"hay {n} conferencias y escribes {len(t)} números de sala"
    t = [int(x) for x in t]
    for i, s in enumerate(t):
        if not 1 <= s <= R:
            return f"la conferencia {i + 1} va a la sala {s}, que no existe (con {R} salas van de 1 a {R})"
    orden = sorted(range(n), key=lambda i: (t[i], confs[i][0], confs[i][1], i))
    for a, b in zip(orden, orden[1:]):
        if t[a] == t[b] and confs[b][0] < confs[a][1]:
            x, y = sorted((a, b))
            return (f"las conferencias {x + 1} ({confs[x][0]}-{confs[x][1]}) y {y + 1} "
                    f"({confs[y][0]}-{confs[y][1]}) se solapan y las pones las dos en la sala {t[a]}")
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    for k, confs in enumerate(_casos(entrada)):
        for j in (2 * k, 2 * k + 1):
            x = e[j]
            y = o[j] if j < len(o) else None
            d = {"linea": j + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
            if y is None:
                d["motivo"] = "tu salida acaba antes"
                return d
            if y == x:
                continue
            if j == 2 * k:
                t = y.split()
                if t == [x]:
                    d["motivo"] = "el número de salas es correcto, pero sobran espacios en la línea"
                    d["pe"] = True
                elif len(t) != 1 or not _NUM.match(t[0]):
                    d["motivo"] = "esta línea debería tener solo el número mínimo de salas"
                elif int(t[0]) > int(x):
                    d["motivo"] = f"usas {int(t[0])} salas y basta con {x}"
                else:
                    d["motivo"] = f"con {int(t[0])} salas no caben: hay un momento con {x} conferencias a la vez"
                return d
            motivo = _revisa_salas(confs, int(e[2 * k]), y)
            if motivo:
                d["motivo"] = motivo
                return d
            if y != " ".join(y.split()):
                d["motivo"] = "la asignación es válida, pero los números deben ir separados por un solo espacio"
                d["pe"] = True
                return d
    if len(o) > len(e):
        return {"linea": len(e) + 1, "esperada": None, "obtenida": o[len(e)], "total": len(e),
                "lineas_tuyas": len(o), "motivo": "escribes líneas de más"}
    return None


def comprobar(entrada, esperada, obtenida):
    d = _comprobar(entrada, esperada, obtenida)
    if d is None or d.get("pe"):
        return d
    # ¿Los mismos datos con otro reparto en líneas? Se reparten tus palabras como en la salida
    # esperada y, si así es correcta, es un error de presentación.
    cuentas = [len(l.split()) for l in _lineas(esperada)]
    pal = obtenida.split()
    if len(pal) == sum(cuentas):
        nuevas, k = [], 0
        for c in cuentas:
            nuevas.append(" ".join(pal[k:k + c]))
            k += c
        if _comprobar(entrada, esperada, "\n".join(nuevas) + "\n") is None:
            d = dict(d)
            d["pe"] = True
            d["motivo"] = "tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado"
    return d
