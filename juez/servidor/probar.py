#!/usr/bin/env python3
"""Prueba el servidor del juez de punta a punta. Uso:

    python3 probar.py [http://127.0.0.1:8099] [--rapido] [--carga]

Envía casos con el veredicto que deben dar (correcto, incorrecto, no compila, bucle infinito,
segfault, abort, memoria, salida infinita, código malicioso, bomba de procesos, llenar /tmp,
leer archivos de la Pi...), comprueba que el servidor sigue vivo tras cada uno y, al final,
que una conexión lenta no lo bloquea. --carga lanza envíos a la vez (pon JUEZ_ESPERA=0 en el
servidor para probarlo desde una sola IP). Devuelve código 1 si algo no da lo esperado.
"""
import json, socket, sys, threading, time, urllib.request, urllib.error
from pathlib import Path
from urllib.parse import urlparse

args = [a for a in sys.argv[1:] if not a.startswith("--")]
URL = (args[0] if args else "http://127.0.0.1:8099").rstrip("/")
RAPIDO = "--rapido" in sys.argv
RAIZ = Path(__file__).resolve().parent.parent.parent
cfg = json.loads((RAIZ / "juez" / "juez.json").read_text(encoding="utf-8"))["04-3"]
sol = (RAIZ / cfg["solucion"]).read_bytes().decode("utf-8", "replace")
fallo = sol.replace(cfg["fallo"][0], cfg["fallo"][1])
sin_main = sol.replace("int main()", "int main2()")
CAT = "#define CAT(a,b) a##b\n"            # para saltarse el filtro de texto: la caja debe aguantar

# (nombre, código, veredictos aceptables)
casos = [
    ("correcta", sol, {"ac"}),
    ("con un fallo", fallo, {"wa"}),
    ("no compila", "int main(){ x }", {"ce"}),
    ("bucle infinito", sin_main + "\nint main(){ for(volatile int i=0;;i++){} }", {"tle"}),
    ("dormir (tiempo de reloj)", sin_main + '\nextern "C" unsigned sleep(unsigned);\nint main(){ sleep(30); }', {"tle"}),
    ("segfault", sin_main + "\nint main(){ volatile int*p=nullptr; return *p; }", {"rte"}),
    ("abort", sin_main + "\n#include <cstdlib>\nint main(){ abort(); }", {"rte"}),
    ("recursión profunda correcta", sin_main + '\n#include <cstdio>\nint f(int n){ volatile char b[64]; b[0]=n; return n? f(n-1)+b[0]:0; }\nint main(){ f(300000); return 0; }', {"wa"}),
    ("memoria infinita", sin_main + "\n#include <vector>\nint main(){ std::vector<int> v; for(;;) v.push_back(1); }", {"mle"}),
    ("memoria tocada 3 GB", sin_main + "\n#include <cstring>\nint main(){ for(int i=0;i<3072;i++){ char*p=new char[1<<20]; memset(p,1,1<<20);} }", {"mle"}),
    ("salida infinita", sin_main + '\n#include <cstdio>\nint main(){ for(;;) puts("xxxxxxxxxxxxxxxx"); }', {"ole"}),
    ("malicioso (system)", '#include <cstdlib>\nint main(){ system("cat /etc/passwd"); }', {"ce"}),
    ("bomba de procesos (sin filtro)", sin_main + CAT + 'extern "C" int CAT(fo,rk)();\nint main(){ for(;;) CAT(fo,rk)(); }', {"tle", "rte", "wa"}),
    ("llenar /tmp", sin_main + '#include <cstdio>\n#include <string>\nint main(){ static char b[1<<20]; for(int i=0;i<4000;i++){ FILE*f=fopen(("/tmp/"+std::to_string(i)).c_str(),"w"); if(!f) return 3; fwrite(b,1,sizeof b,f); fclose(f);} }', {"rte"}),
    ("escribir en /w", sin_main + '#include <cstdio>\nint main(){ FILE*f=fopen("/w/x","w"); return f?0:4; }', {"rte"}),
    ("leer /etc/passwd", sin_main + '#include <cstdio>\nint main(){ FILE*f=fopen("/etc/passwd","r"); if(f){ char b[200]; while(fgets(b,200,f)) fputs(b,stdout);} return f?0:5; }', {"rte"}),
    ("leer el home", sin_main + '#include <cstdio>\nint main(){ return fopen("/home","r")?0:6; }', {"rte"}),
    ("formato distinto (PE)", sol.replace("<< ' ' <<", "<< '\\n' <<"), {"pe"}),
    ("crear procesos (seccomp)", sin_main + CAT + '#include <cstdio>\nextern "C" int CAT(fo,rk)();\nint main(){ return CAT(fo,rk)() < 0 ? 7 : 0; }', {"rte"}),
    ("cabecera prohibida", '#include <unistd.h>\nint main(){}', {"ce"}),
    ("plantilla explosiva (compilación)", "template<int N> struct F{ enum { v = F<N-1>::v + F<N-2>::v }; };\ntemplate<> struct F<1>{ enum { v = 1 }; };\ntemplate<> struct F<0>{ enum { v = 0 }; };\nint main(){ return F<200000>::v; }", {"ce"}),
]
if RAPIDO:
    casos = [c for c in casos if c[0] in ("correcta", "con un fallo", "no compila", "bucle infinito", "memoria infinita")]


def pedir(cuerpo, timeout=180):
    req = urllib.request.Request(URL + "/juzgar", json.dumps(cuerpo).encode(), {"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=timeout))
    except urllib.error.HTTPError as e:
        return {"http": e.code, **json.load(e)}


def salud():
    try:
        return json.load(urllib.request.urlopen(URL + "/salud", timeout=10))
    except urllib.error.HTTPError as e:
        return json.load(e)
    except Exception as e:
        return {"ok": False, "error": str(e)}


s = salud()
print("salud:", json.dumps({k: s.get(k) for k in ("ok", "limites", "autoprueba")}, ensure_ascii=False))
espera = 0.2 if "--carga" in sys.argv else 4.2
malos = 0
for n, c, esperado in casos:
    t = time.time()
    d = pedir({"id": "04-3", "codigo": c})
    if d.get("http") == 429:
        time.sleep(4.2); d = pedir({"id": "04-3", "codigo": c})
    v = d.get("veredicto")
    det = [(x["n"], x["v"], x["ms"]) for x in d.get("tests", [])][:3]
    vivo = salud().get("ok")
    bien = v in esperado and vivo
    malos += not bien
    extra = d.get("log", "") or next((x.get("detalle", "") for x in d.get("tests", []) if x.get("detalle")), "") or d.get("error", "")
    print(f"{'OK ' if bien else 'MAL'} {n:34} {v!s:4} {det} {extra[:70]!r} {time.time()-t:.1f}s{'' if vivo else '  ¡SERVIDOR NO RESPONDE!'}")
    time.sleep(espera)

# Conexión lenta: abre el socket y no termina la petición. El juez debe seguir atendiendo.
u = urlparse(URL)
lentos = []
for _ in range(5):
    k = socket.create_connection((u.hostname, u.port or 80), timeout=5)
    k.sendall(b"POST /juzgar HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\nContent-Length: 5000\r\n\r\n{")
    lentos.append(k)
t = time.time(); ok = salud().get("ok")
print(f"{'OK ' if ok else 'MAL'} {'conexiones lentas no bloquean':34} {time.time()-t:.2f}s")
malos += not ok
for k in lentos: k.close()

if "--carga" in sys.argv:
    res = []
    def uno(i):
        res.append(pedir({"id": "04-3", "codigo": sol if i % 2 == 0 else fallo}, timeout=300))
    hs = [threading.Thread(target=uno, args=(i,)) for i in range(12)]
    t = time.time()
    for h in hs: h.start()
    for h in hs: h.join()
    cuenta = {}
    for r in res:
        k = r.get("veredicto") or f"http {r.get('http')}"
        cuenta[k] = cuenta.get(k, 0) + 1
    ok = all(r.get("veredicto") in ("ac", "wa") or r.get("http") in (429, 503) for r in res) and salud().get("ok")
    print(f"{'OK ' if ok else 'MAL'} {'12 envíos a la vez':34} {cuenta} {time.time()-t:.1f}s")
    malos += not ok

print("\nTodo bien." if not malos else f"\n{malos} prueba(s) no dieron lo esperado.")
sys.exit(1 if malos else 0)
