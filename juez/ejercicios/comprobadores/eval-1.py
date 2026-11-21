"""Comprobador de eval-1 «MasterHash»: vale CUALQUIER orden válido de las elaboraciones necesarias.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/eval-1.js en el navegador (el verificador comprueba que coinciden).
Si la respuesta es SI, la línea debe ser «SI» seguido de exactamente las elaboraciones de la
salida esperada (las necesarias para el plato), cada una una vez, respetando todas las anotaciones
entre ellas y con el plato P al final.
"""
import re


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
        n, a, s, pl = sig(), sig(), sig(), sig()
        yield n, s, pl, [(sig(), sig()) for _ in range(a)]


def _revisa(esperada, linea, P, aris):
    t = linea.split()
    if not t:
        return "la línea está vacía: hay que escribir SI (y el orden) o NO"
    if t[0] == "NO" and len(t) == 1:
        return "escribes NO, pero el plato sí se puede hacer"
    if t[0] != "SI":
        return "la línea debe empezar por SI (en mayúsculas y sin tilde) o ser NO"
    if not all(re.fullmatch(r"-?[0-9]+", x) for x in t[1:]):
        return "después de SI solo van números de elaboración"
    nums = [int(x) for x in t[1:]]
    nec = set(int(x) for x in esperada.split()[1:])
    pos = {}
    for i, x in enumerate(nums):
        if x not in nec:
            return f"la elaboración {x} no hace falta para el plato {P}"
        if x in pos:
            return f"la elaboración {x} aparece dos veces"
        pos[x] = i
    if len(nums) < len(nec):
        falta = min(nec - set(nums))
        return f"falta la elaboración {falta}, que también hace falta para el plato {P}"
    if nums[-1] != P:
        return f"el plato {P} debe ser el último"
    for x, y in aris:
        if x in pos and y in pos and pos[x] > pos[y]:
            return f"la elaboración {x} hace falta para la {y}, y en tu orden va después"
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    for i, (n, S, P, aris) in enumerate(_casos(entrada)):
        x = e[i]
        y = o[i] if i < len(o) else None
        d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
        if y is None:
            d["motivo"] = "tu salida acaba antes"
            return d
        if y == x:
            continue
        if x == "NO":
            d["motivo"] = "el plato no se puede hacer: la respuesta es NO"
            return d
        motivo = _revisa(x, y, P, aris)
        if motivo:
            d["motivo"] = motivo
            return d
        if y != " ".join(y.split()):
            d["motivo"] = "el orden es válido, pero SI y los números deben ir separados por un solo espacio"
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
    # ¿Las mismas palabras con otro reparto en líneas? Se reparten como en la salida esperada y,
    # si así es correcta, es un error de presentación.
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
