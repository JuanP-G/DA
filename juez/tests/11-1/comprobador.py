"""Comprobador de 11-1 «El cazatesoros»: vale CUALQUIER conjunto óptimo de cofres, en cualquier orden.

comprobar(entrada, esperada, obtenida) -> None si la salida es correcta, o un dict con la primera
línea mala: {linea, esperada, obtenida, total, lineas_tuyas, motivo[, pe]}. Lo mismo hace
comprobadores/11-1.js en el navegador (el verificador comprueba que coinciden).
Por cada caso se espera: el oro máximo, el número K de cofres, K líneas «profundidad oro» con
cofres de la entrada (cada uno como mucho tantas veces como aparece) que quepan en la botella
(3·p segundos cada uno) y sumen ese oro, y una línea «---».
"""
import re

_ENTERO = re.compile(r"-?[0-9]+")


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
        T, n = sig(), sig()
        yield T, [(sig(), sig()) for _ in range(n)]


def _numeros(linea, cuantos):
    t = linea.split()
    if len(t) != cuantos or not all(_ENTERO.fullmatch(x) for x in t):
        return None
    return [int(x) for x in t]


def _comprobar(entrada, esperada, obtenida):
    e, o = _lineas(esperada), _lineas(obtenida)
    ie = io = 0
    formato = None

    def fallo(motivo, esp):
        return {"linea": io + 1, "esperada": esp, "obtenida": o[io] if io < len(o) else None,
                "total": len(e), "lineas_tuyas": len(o), "motivo": motivo}

    for T, cofres in _casos(entrada):
        oro = int(e[ie])
        k_esp = int(e[ie + 1])
        sep = ie + k_esp + 2
        # 1. oro máximo
        if io >= len(o):
            return fallo("tu salida acaba antes", e[ie])
        x = _numeros(o[io], 1)
        if x is None:
            return fallo("en esta línea va el oro máximo (un solo número)", e[ie])
        if x[0] != oro:
            return fallo(f"el oro máximo es {oro} y escribes {x[0]}", e[ie])
        if o[io] != str(x[0]) and formato is None:
            formato = fallo("el oro es correcto, pero la línea debe tener solo el número", e[ie])
        io += 1
        # 2. número de cofres
        if io >= len(o):
            return fallo("tu salida acaba antes: falta la línea con el número de cofres", e[ie + 1])
        x = _numeros(o[io], 1)
        if x is None:
            return fallo("en esta línea va el número de cofres que hay que recoger (un solo número)", e[ie + 1])
        k = x[0]
        if k < 0 or k > len(cofres):
            return fallo(f"escribes {k} cofres y en la entrada hay {len(cofres)}", e[ie + 1])
        io += 1
        # 3. los cofres
        quedan = {}
        for c in cofres:
            quedan[c] = quedan.get(c, 0) + 1
        tiempo = suma = 0
        for _ in range(k):
            esp = e[ie + 2] if k_esp else e[sep]
            if io >= len(o):
                return fallo(f"tu salida acaba antes: dices que hay {k} cofres y faltan líneas de cofres", esp)
            x = _numeros(o[io], 2)
            if x is None:
                return fallo(f"dices que hay {k} cofres, así que aquí va un cofre como «profundidad oro»", esp)
            c = (x[0], x[1])
            if c not in quedan:
                return fallo(f"no hay ningún cofre «{x[0]} {x[1]}» en la entrada (primero va la profundidad y luego el oro)", esp)
            if quedan[c] == 0:
                return fallo(f"el cofre «{x[0]} {x[1]}» aparece más veces de las que está en la entrada (cada cofre se sube una sola vez)", esp)
            if o[io] != f"{x[0]} {x[1]}" and formato is None:
                formato = fallo("el cofre es correcto, pero la profundidad y el oro deben ir separados por un solo espacio", esp)
            quedan[c] -= 1
            tiempo += 3 * x[0]
            suma += x[1]
            io += 1
        if tiempo > T:
            io -= 1 if k else 0
            return fallo(f"los cofres que escribes necesitan {tiempo} segundos (3·p cada uno) y la botella da {T}", e[sep - 1])
        if suma != oro:
            io -= 1 if k else 0
            return fallo(f"los cofres que escribes suman {suma} monedas y no {oro}", e[sep - 1])
        # 4. separador
        if io >= len(o):
            return fallo("tu salida acaba antes: falta la línea «---» del final del caso", "---")
        if o[io] != "---":
            if o[io].strip() == "---" and formato is None:
                formato = fallo("la línea debe ser exactamente «---»", "---")
            elif o[io].strip() != "---":
                return fallo("después de los cofres de cada caso va una línea con «---»", "---")
        io += 1
        ie = sep + 1
    if io < len(o):
        return fallo("escribes líneas de más", None)
    if formato is not None:
        formato["pe"] = True
    return formato


def comprobar(entrada, esperada, obtenida):
    d = _comprobar(entrada, esperada, obtenida)
    if d is None or d.get("pe"):
        return d
    if obtenida.split() == esperada.split():
        d = dict(d)
        d["pe"] = True
        d["motivo"] = "tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado"
    return d
