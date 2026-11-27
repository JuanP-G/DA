"""Comprobador de 12-10 «Megaautopista de Oriente»: vale CUALQUIER elección óptima.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/12-10.js en el navegador (el verificador comprueba que coinciden).
Por cada caso se esperan dos líneas: el beneficio y las posiciones en orden creciente.
"""


def _casos(entrada):
    d = iter(map(int, entrada.split()))
    r = []
    for n in d:
        D = next(d)
        x = [next(d) for _ in range(n)]
        b = [next(d) for _ in range(n)]
        r.append((D, dict(zip(x, b))))
    return r


def _entero(s):
    return 0 < len(s) <= 9 and all(c in "0123456789" for c in s)


def comprobar(entrada, esperada, obtenida):
    casos = _casos(entrada)
    e = esperada.replace("\r", "").split("\n")
    o = [x.rstrip() for x in obtenida.replace("\r", "").split("\n")]
    while o and o[-1] == "":
        o.pop()
    total, mias = 2 * len(casos), len(o)
    formato = None
    if mias > total:
        return {"linea": total + 1, "esperada": None, "obtenida": o[total], "total": total, "lineas_tuyas": mias,
                "motivo": "escribes líneas de más: dos por caso"}
    o += [""] * (total - len(o))
    for c, (D, b) in enumerate(casos):
        def fallo(k, motivo):
            return {"linea": k + 1, "esperada": e[k], "obtenida": o[k], "total": total,
                    "lineas_tuyas": mias, "motivo": motivo}
        i, j = 2 * c, 2 * c + 1
        v, s = o[i].split(), o[j].split()
        if v != [e[i].strip()]:
            return fallo(i, "el beneficio máximo no es ese")
        if not s or not all(_entero(t) for t in s):
            return fallo(j, "la segunda línea son los puntos kilométricos de los restaurantes")
        p = [int(t) for t in s]
        if any(q not in b for q in p):
            return fallo(j, "alguna de esas posiciones no es un área de descanso")
        if any(q - a < D for a, q in zip(p, p[1:])):
            return fallo(j, f"las posiciones deben ir de menor a mayor y separadas al menos {D} km")
        if sum(b[q] for q in p) != int(e[i]):
            return fallo(j, "esas áreas no suman el beneficio máximo")
        for k, t in ((i, v), (j, s)):
            if o[k] != " ".join(t) and formato is None:
                formato = fallo(k, "la respuesta es correcta, pero separa con un solo espacio")
    if formato is not None:
        formato["pe"] = True
    return formato
