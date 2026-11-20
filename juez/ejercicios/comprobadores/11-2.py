"""Comprobador de 11-2 «Aibofobia»: vale CUALQUIER palíndromo con el mínimo de letras añadidas.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/11-2.js en el navegador (el verificador comprueba que coinciden).
Cada línea debe ser «k palíndromo»: k el mínimo, y el palíndromo, de minúsculas, con n + k letras
y que contenga la palabra como subsecuencia (se obtiene añadiendo letras, sin quitar ni cambiar).
"""
import re


def _lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def _subsecuencia(a, b):
    k = 0
    for c in b:
        if k < len(a) and a[k] == c:
            k += 1
    return k == len(a)


def _revisa(s, k_esp, linea):
    t = linea.split()
    if len(t) != 2:
        return "cada línea debe tener el número de letras añadidas y el palíndromo, separados por un espacio"
    if not re.fullmatch(r"-?[0-9]+", t[0]):
        return "la línea debe empezar por el número de letras añadidas"
    k, p = int(t[0]), t[1]
    if k != k_esp:
        return f"el mínimo de letras que hay que añadir es {k_esp} y escribes {k}"
    if not re.fullmatch(r"[a-z]+", p):
        return "el palíndromo debe estar formado solo por letras minúsculas"
    if p != p[::-1]:
        return f"«{p}» no es un palíndromo"
    if len(p) != len(s) + k:
        return f"el palíndromo debería tener {len(s)} + {k} = {len(s) + k} letras y tiene {len(p)}"
    if not _subsecuencia(s, p):
        return f"«{p}» no se obtiene añadiendo letras a «{s}» (no contiene sus letras en orden)"
    return None


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    pal = entrada.split()
    pal = pal[1:1 + int(pal[0])]
    for i, s in enumerate(pal):
        x = e[i]
        y = o[i] if i < len(o) else None
        d = {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(e), "lineas_tuyas": len(o)}
        if y is None:
            d["motivo"] = "tu salida acaba antes"
            return d
        if y == x:
            continue
        motivo = _revisa(s, int(x.split()[0]), y)
        if motivo:
            d["motivo"] = motivo
            return d
        if y != " ".join(y.split()):
            d["motivo"] = "la respuesta es válida, pero el número y el palíndromo deben ir separados por un solo espacio"
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
    # ¿Las mismas palabras con otro reparto en líneas? (p. ej. el número y el palíndromo en líneas
    # distintas): se reparten como en la salida esperada y, si así es correcta, es de presentación.
    pal = obtenida.split()
    if len(pal) == 2 * len(_lineas(esperada)):
        nuevas = [" ".join(pal[k:k + 2]) for k in range(0, len(pal), 2)]
        if _comprobar(entrada, esperada, "\n".join(nuevas) + "\n") is None:
            d = dict(d)
            d["pe"] = True
            d["motivo"] = "tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado"
    return d
