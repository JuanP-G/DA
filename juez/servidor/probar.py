#!/usr/bin/env python3
"""Prueba el servidor con 8 envíos (correcto, incorrecto, no compila, bucle infinito, segfault,
abort, código malicioso y salida infinita). Uso:  python3 probar.py [http://127.0.0.1:8099]"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8099"
RAIZ = Path(__file__).resolve().parent.parent.parent
cfg = json.loads((RAIZ / "juez" / "juez.json").read_text(encoding="utf-8"))["04-3"]
sol = (RAIZ / cfg["solucion"]).read_bytes().decode("utf-8", "replace")
fallo = sol.replace(cfg["fallo"][0], cfg["fallo"][1])
sin_main = sol.replace("int main()", "int main2()")
casos = {
    "correcta (debe ser AC)": sol,
    "con un fallo (WA)": fallo,
    "no compila (CE)": "int main(){ x }",
    "bucle infinito (TLE)": sin_main + "\nint main(){ while(1){} }",
    "segfault (RTE)": sin_main + "\nint main(){ int*p=nullptr; return *p; }",
    "abort (RTE)": sin_main + "\n#include <cstdlib>\nint main(){ abort(); }",
    "malicioso (rechazado)": '#include <cstdlib>\nint main(){ system("cat /etc/passwd"); }',
    "salida infinita (no debe colgar)": sin_main + '\n#include <cstdio>\nint main(){ for(;;) puts("xxxxxxxxxxxxxxxx"); }',
    "memoria infinita (RTE, no debe colgar)": sin_main + "\n#include <vector>\nint main(){ std::vector<int> v; for(;;) v.push_back(1); }",
    "bomba de procesos (sin efecto)": sin_main + "\n#include <cstdlib>\nint main(){ for(;;) std::system(\"x\"); }".replace("std::system", "std::abs") ,
}
for n, c in casos.items():
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL + "/juzgar", json.dumps({"id": "04-3", "codigo": c}).encode(), {"Content-Type": "application/json"}), timeout=120)
        d = json.load(r)
    except urllib.error.HTTPError as e:
        d = {"http": e.code, **json.load(e)}
    det = [(x["n"], x["v"], x["ms"]) for x in d.get("tests", [])]
    print(f"{n:42} {d.get('veredicto') or d} {det} {d.get('log', '')[:80]!r} {time.time()-t:.1f}s")
    time.sleep(4.2)
