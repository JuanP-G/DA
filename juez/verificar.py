#!/usr/bin/env python3
"""Verifica el juez de uno o varios ejercicios de punta a punta, con la misma caja que en la Pi.

Uso:  PYTHONUTF8=1 python3 juez/verificar.py <id> [<id> ...]   [--rapido]

Para cada ejercicio:
  1. Genera sus pruebas (herramientas/generar_tests_juez.py).
  2. Revisa los datos: tipos, pistas, explicaciones, tamaños, ejemplos del enunciado presentes...
  3. La solución del repo debe dar AC en TODAS las pruebas (si no, o el solucionador independiente
     o la solución del repo tienen un error: hay que averiguar cuál con el enunciado).
     Su tiempo de CPU debe dejar margen para la Raspberry Pi (≈ 5 veces más lenta que este PC).
  4. El fallo de demostración no debe dar AC.
  5. Cada VARIANTE (solución con un fallo típico) debe fallar, y la guía de la web (el mismo
     diagnostico.js) debe señalar la prueba y el veredicto previstos.
Devuelve 0 si todo está bien.
"""
import importlib.util, json, os, pathlib, subprocess, sys, time

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
import generar_tests_juez as gen  # noqa: E402

FACTOR_PI = 5            # la Pi 4 tarda ~3-5 veces más que este PC
MAX_FICHERO = 2_500_000  # bytes por .in (la web en el navegador los descarga)
MAX_TOTAL = 8_000_000    # bytes por ejercicio

spec = importlib.util.spec_from_file_location("servidor", RAIZ / "juez" / "servidor" / "servidor.py")
srv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srv)
_listo = False


def preparar():
    global _listo
    if not _listo:
        srv.detectar()
        nota = srv.preparar_medidor()
        if nota:
            print("AVISO medidor:", nota)
        _listo = True


def diagnostico(meta, res):
    filas = []
    por_n = {m["n"]: m for m in meta}
    for t in res.get("tests", []):
        filas.append({"t": por_n[t["n"]], "v": t["v"], "dif": t.get("dif"), "ms": t.get("ms")})
    js = ("const d=require(process.argv[1]);let s='';process.stdin.on('data',c=>s+=c).on('end',()=>{"
          "const r=d.diagnostico(JSON.parse(s));console.log(JSON.stringify({n:r.clave&&r.clave.t.n,v:r.clave&&r.clave.v,notas:r.notas}))})")
    p = subprocess.run(["node", "-e", js, str(RAIZ / "sitio" / "juez" / "diagnostico.js")],
                       input=json.dumps(filas), capture_output=True, text=True, timeout=30)
    if p.returncode:
        raise RuntimeError("diagnostico.js falló: " + p.stderr[:300])
    return json.loads(p.stdout)


def resumen(res):
    if "tests" not in res:
        return f"{res.get('veredicto') or res.get('error')} {res.get('log', '')[:300]!r}"
    return f"{res['veredicto']} " + " ".join(f"{t['n']}:{t['v']}" for t in res["tests"])


def verificar(ej, rapido=False):
    errores, avisos = [], []
    m, meta, total = gen.generar(ej, silencio=True)
    cfg = m.CONFIG
    # ---- 2. datos
    if not (RAIZ / cfg["solucion"]).exists():
        errores.append(f"no existe la solución {cfg['solucion']}")
        return errores, avisos
    sol = (RAIZ / cfg["solucion"]).read_bytes().decode("utf-8", "replace")
    if "//@ <answer>" not in sol or "//@ </answer>" not in sol:
        errores.append("la solución no tiene las marcas //@ <answer> ... //@ </answer> (la plantilla enseñaría la solución)")
    if cfg["fallo"][0] not in sol:
        errores.append(f"CONFIG['fallo'][0] no aparece en la solución: {cfg['fallo'][0]!r}")
    for c in cfg.get("cabeceras", []):
        if not (RAIZ / c).exists():
            errores.append(f"no existe la cabecera {c}")
    tipos = [x["tipo"] for x in meta]
    if "enunciado" not in tipos:
        errores.append("falta al menos una prueba de tipo «enunciado» (los ejemplos del PDF)")
    if tipos and tipos[0] != "enunciado":
        avisos.append("la primera prueba no es un ejemplo del enunciado")
    for t in ("borde", "trampa", "rendimiento"):
        if t not in tipos:
            avisos.append(f"no hay ninguna prueba de tipo «{t}»")
    if len(meta) < 12:
        avisos.append(f"solo {len(meta)} pruebas (se buscan 15-25)")
    nombres = [x["nombre"] for x in meta]
    if len(set(nombres)) != len(nombres):
        errores.append("hay nombres de prueba repetidos")
    for x in meta:
        if len(x["pistas"]) < 2:
            avisos.append(f"prueba {x['n']} «{x['nombre']}»: solo {len(x['pistas'])} pista(s)")
        tam = (RAIZ / "juez" / "tests" / ej / f"{x['n']}.in").stat().st_size
        if tam > MAX_FICHERO:
            errores.append(f"prueba {x['n']}: {tam / 1e6:.1f} MB (máx. {MAX_FICHERO / 1e6:.1f})")
        if (RAIZ / "juez" / "tests" / ej / f"{x['n']}.out").stat().st_size == 0:
            avisos.append(f"prueba {x['n']}: salida esperada vacía")
    if total > MAX_TOTAL:
        errores.append(f"las pruebas ocupan {total / 1e6:.1f} MB (máx. {MAX_TOTAL / 1e6:.0f})")
    if errores:
        return errores, avisos
    preparar()
    lim = cfg.get("limite_ms", 3000)
    # ---- 3. solución del repo
    t0 = time.time()
    r = srv.juzgar(ej, sol)
    if r.get("veredicto") != "ac":
        errores.append("la solución del repo NO da AC: " + resumen(r))
        for t in r.get("tests", []):
            if t["v"] != "ac":
                errores.append(f"   prueba {t['n']} «{meta[t['n'] - 1]['nombre']}»: {t['v']} {json.dumps(t.get('dif') or t.get('detalle'), ensure_ascii=False)[:300]}")
    else:
        lento = max(r["tests"], key=lambda t: t["ms"])
        if lento["ms"] * FACTOR_PI > lim:
            errores.append(f"la solución tarda {lento['ms']} ms en la prueba {lento['n']}: en la Pi (×{FACTOR_PI}) pasaría del límite de {lim} ms")
        print(f"  solución: AC en {len(r['tests'])} pruebas · la más lenta {lento['ms']} ms (prueba {lento['n']}) · {time.time() - t0:.1f}s")
    if errores or rapido:
        return errores, avisos
    # ---- 4. fallo de demostración
    r = srv.juzgar(ej, sol.replace(cfg["fallo"][0], cfg["fallo"][1], 1))
    if r.get("veredicto") == "ac":
        errores.append("el fallo de demostración da AC: no se nota")
    # ---- 5. variantes
    variantes = getattr(m, "VARIANTES", [])
    if len(variantes) < 4:
        avisos.append(f"solo {len(variantes)} variantes con fallos (se buscan 6-12)")
    for var in variantes:
        codigo = sol
        falta = [a for a, _ in var["cambios"] if a not in codigo]
        if falta:
            errores.append(f"variante «{var['nombre']}»: no encuentro {falta[0]!r} en la solución")
            continue
        for a, b in var["cambios"]:
            codigo = codigo.replace(a, b)
        r = srv.juzgar(ej, codigo)
        if r.get("veredicto") == "ac":
            errores.append(f"variante «{var['nombre']}»: da AC (ninguna prueba detecta este fallo)")
            continue
        if "tests" not in r:
            errores.append(f"variante «{var['nombre']}»: {resumen(r)}")
            continue
        d = diagnostico(meta, r)
        ok = d["n"] in var["prueba"] and d["v"] == var["v"]
        marca = "ok " if ok else "MAL"
        print(f"  {marca} variante «{var['nombre']}» → guía: prueba {d['n']} {d['v']} (esperado {var['prueba']} {var['v']}) · {resumen(r)}")
        if not ok:
            errores.append(f"variante «{var['nombre']}»: la guía señala la prueba {d['n']} ({d['v']}) y se esperaba {var['prueba']} ({var['v']}). Resultados: {resumen(r)}")
    return errores, avisos


if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")] or gen.todos()
    malos = 0
    for ej in ids:
        print(f"== {ej}")
        try:
            errores, avisos = verificar(ej, "--rapido" in sys.argv)
        except Exception as e:
            import traceback; traceback.print_exc()
            errores, avisos = [f"excepción: {type(e).__name__}: {e}"], []
        for a in avisos:
            print("  aviso:", a)
        for e in errores:
            print("  ERROR:", e)
        print(f"  {'BIEN' if not errores else 'MAL'}")
        malos += bool(errores)
    sys.exit(1 if malos else 0)
