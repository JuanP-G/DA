"""Comprobador de 11-L «La fiesta de graduación»: vale CUALQUIER lista común de la longitud máxima.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/11-l.js en el navegador (el verificador comprueba que coinciden).
Por cada caso se espera una línea con canciones separadas por un espacio que sea subsecuencia de las
dos listas y tenga la longitud máxima (la de la línea esperada); si no hay ninguna, una línea vacía.
"""


def _casos(entrada):
    l = entrada.replace("\r", "").split("\n")
    n = int(l[0].split()[0])
    return [(l[1 + 2 * c].split() if 1 + 2 * c < len(l) else [],
             l[2 + 2 * c].split() if 2 + 2 * c < len(l) else []) for c in range(n)]


def _subsecuencia(x, a):
    it = iter(a)
    return all(any(c == d for d in it) for c in x)


def comprobar(entrada, esperada, obtenida):
    casos = _casos(entrada)
    e = esperada.replace("\r", "").split("\n")
    o = [x.rstrip() for x in obtenida.replace("\r", "").split("\n")]
    while o and o[-1] == "":
        o.pop()
    n = len(casos)
    total, mias = n, len(o)
    formato = None
    if len(o) > n:
        return {"linea": n + 1, "esperada": None, "obtenida": o[n], "total": total, "lineas_tuyas": mias,
                "motivo": "escribes líneas de más: una por caso"}
    o += [""] * (n - len(o))
    for c, (a, b) in enumerate(casos):
        mejor = len(e[c].split())

        def fallo(motivo):
            return {"linea": c + 1, "esperada": e[c], "obtenida": o[c], "total": total,
                    "lineas_tuyas": mias, "motivo": motivo}
        x = o[c].split()
        if not _subsecuencia(x, a):
            return fallo("esa lista no es subsecuencia de la lista de la mañana (orden, repeticiones o canciones que no están)")
        if not _subsecuencia(x, b):
            return fallo("esa lista no es subsecuencia de la lista de la tarde (orden, repeticiones o canciones que no están)")
        if len(x) != mejor:
            return fallo(f"la lista común más larga tiene {mejor} canciones y escribes {len(x)}")
        if o[c] != " ".join(x) and formato is None:
            formato = fallo("la lista es correcta, pero las canciones deben ir separadas por un solo espacio")
    if formato is not None:
        formato["pe"] = True
    return formato
