"""Comprobador de 10-2 «Construyendo dianas»: vale CUALQUIER solución óptima, con las puntuaciones
en cualquier orden.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/10-2.js en el navegador (el verificador comprueba que coinciden).
"""
import re


def _lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def _casos(entrada):
    v = entrada.split()
    p, r = 0, []
    while p + 1 < len(v):
        V, S = int(v[p]), int(v[p + 1])
        r.append((V, [int(x) for x in v[p + 2:p + 2 + S]]))
        p += 2 + S
    return r


def _revisa(V, sectores, k, linea):
    """(motivo, pe) si «linea» no es una solución óptima, o None."""
    if linea.strip() == "Imposible":
        return f"escribes Imposible, pero sí se puede conseguir {V} (con {k} dardos)", False
    m = re.fullmatch(r"\s*(-?\d+)\s*:((?:\s*-?\d+)*)\s*", linea)
    if not m:
        return "la línea debe ser «número de dardos: puntuaciones» (por ejemplo «2: 4 4») o Imposible", False
    n = int(m.group(1))
    nums = [int(x) for x in m.group(2).split()]
    if n != k:
        return f"escribes {n} dardos y el mínimo es {k}", False
    if len(nums) != n:
        return f"dices {n} dardos pero escribes {len(nums)} puntuaciones", False
    ss = set(sectores)
    for x in nums:
        if x not in ss:
            return f"la puntuación {x} no es ningún sector de esta diana", False
    if sum(nums) != V:
        return f"tus puntuaciones suman {sum(nums)} y no {V}", False
    if linea != f"{n}: " + " ".join(map(str, nums)):
        return "la solución es correcta, pero el formato no: «dardos», dos puntos pegados, y cada puntuación precedida de un espacio", True
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    for i, (V, sectores) in enumerate(_casos(entrada)):
        x = e[i]
        y = o[i] if i < len(o) else None
        d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
        if y is None:
            d["motivo"] = "tu salida acaba antes"
            return d
        if y == x:
            continue
        if x == "Imposible":
            d["motivo"] = f"no se puede conseguir {V} con estas puntuaciones: la respuesta es Imposible"
            return d
        r = _revisa(V, sectores, int(x.split(":")[0]), y)
        if r:
            d["motivo"] = r[0]
            if r[1]:
                d["pe"] = True
            return d
    if len(o) > len(e):
        return {"linea": len(e) + 1, "esperada": None, "obtenida": o[len(e)], "total": len(e),
                "lineas_tuyas": len(o), "motivo": "escribes líneas de más"}
    return None


def comprobar(entrada, esperada, obtenida):
    return _comprobar(entrada, esperada, obtenida)
