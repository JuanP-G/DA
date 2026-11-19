#!/usr/bin/env python3
"""Servidor del juez de DA para Raspberry Pi (Linux, sin root).

Recibe  POST /juzgar  {"id": "04-3", "codigo": "..."}  y devuelve el veredicto.
Cada compilación y cada ejecución van dentro de una caja de bubblewrap (sin red, sistema en
solo lectura, sin tus archivos, procesos aislados) con límites de memoria, tiempo, tamaño y
procesos. Solo usa la biblioteca estándar de Python.

Variables de entorno (todas opcionales):
  JUEZ_RAIZ      carpeta del repo DA (por defecto, dos niveles sobre este archivo)
  JUEZ_PUERTO    puerto (8099)          JUEZ_HOST  dirección (127.0.0.1)
  JUEZ_ORIGENES  orígenes CORS permitidos, separados por comas ("*" = todos)
  JUEZ_SIN_CAJA  1 = sin bubblewrap (SOLO para probar en tu PC; no usar con código ajeno)
  JUEZ_CGROUP    0 = sin systemd-run (si cgroups no está disponible)
  JUEZ_SIMULTANEOS  ejecuciones a la vez (2)
  JUEZ_CONFIAR_CF   1 = leer la IP real de la cabecera CF-Connecting-IP (túnel de Cloudflare)
"""
import json, os, re, shutil, signal, subprocess, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = Path(os.environ.get("JUEZ_RAIZ", AQUI.parent.parent)).resolve()
PUERTO = int(os.environ.get("JUEZ_PUERTO", "8099"))
HOST = os.environ.get("JUEZ_HOST", "127.0.0.1")
ORIGENES = [o.strip() for o in os.environ.get("JUEZ_ORIGENES", "*").split(",") if o.strip()]
SIN_CAJA = os.environ.get("JUEZ_SIN_CAJA") == "1"
CGROUP = os.environ.get("JUEZ_CGROUP", "1") != "0" and not SIN_CAJA
CONFIAR_CF = os.environ.get("JUEZ_CONFIAR_CF") == "1"
BIN = "prog.exe" if os.name == "nt" else "prog"
SIMULTANEOS = int(os.environ.get("JUEZ_SIMULTANEOS", "2"))

MAX_CODIGO = 64 * 1024          # bytes
MAX_SALIDA = 2 * 1024 * 1024    # bytes que se leen del programa
MAX_COLA = 6                    # peticiones esperando antes de decir «ocupado»
ESPERA_ENTRE_ENVIOS = 4.0       # segundos entre dos envíos de la misma IP
T_COMPILAR = 25                 # s
MEM_COMPILAR = "1G"
MEM_EJECUTAR = "256M"

sem = threading.Semaphore(SIMULTANEOS)
cola = 0
cola_lock = threading.Lock()
ultimo = {}                     # ip -> instante del último envío
ultimo_lock = threading.Lock()

PROHIBIDO = [
    (re.compile(r'\b(system|popen|fork|vfork|execl|execlp|execle|execv|execvp|execve|socket|ptrace|dlopen|setuid|chroot)\s*\('), 'llamada no permitida'),
    (re.compile(r'\b__asm__\b|\basm\b|\.incbin|__builtin_(?!expect|unreachable|popcount|clz|ctz|memcpy|memset|abs)'), 'ensamblador o builtin no permitido'),
    (re.compile(r'#\s*include(_next)?\s*[<"]\s*(/|\.\./|[^>"]*\.\./)'), 'include con ruta no permitida'),
    (re.compile(r'#\s*pragma\s+(comment|GCC\s+(system_header|dependency)|include_alias)'), 'pragma no permitido'),
    (re.compile(r'__has_include|<filesystem>|<thread>|<future>|<unistd\.h>|<sys/|<signal\.h>|<csignal>|<dlfcn\.h>|<netinet|<arpa/'), 'cabecera no permitida'),
]


# Las soluciones de la asignatura traen system("pause") (solo Windows); esa llamada exacta se tolera.
PAUSA = re.compile(r'system\s*\(\s*"pause"\s*\)', re.I)


def lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def compara(esperada, obtenida):
    a, b = lineas(esperada), lineas(obtenida)
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x != y:
            return {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(a)}
    return None


def leer(p):
    b = Path(p).read_bytes()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1252", "replace")


def config():
    return json.loads((RAIZ / "juez" / "juez.json").read_text(encoding="utf-8"))


def comando_caja(carpeta, argv, mem, escribible):
    """Envuelve argv en bubblewrap (+ systemd-run para memoria y procesos)."""
    if SIN_CAJA:
        return argv
    bw = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
          "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/bin", "/bin",
          "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
          ("--bind" if escribible else "--ro-bind"), str(carpeta), "/w", "--chdir", "/w",
          "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "LC_ALL", "C.UTF-8"] + argv
    if CGROUP:
        return ["systemd-run", "--user", "--scope", "--quiet", "-p", f"MemoryMax={mem}",
                "-p", "MemorySwapMax=0", "-p", "TasksMax=48"] + bw
    return bw


def correr(cmd, entrada, limite_s, tope_salida):
    """Ejecuta cmd; devuelve (estado, codigo, stdout, stderr, ms). estado: ok | tiempo | salida"""
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, stdin=entrada, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True)
    fuera, err = [], []
    tam = [0]
    corte = [False]

    def beber(f, dest, cuenta):
        while True:
            d = f.read(65536)
            if not d:
                break
            if cuenta:
                tam[0] += len(d)
                if tam[0] > tope_salida:
                    corte[0] = True
                    matar()
                    break
            if len(b"".join(dest)) < 65536 or cuenta:
                dest.append(d)

    def matar():
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except Exception:
            try: p.kill()
            except Exception: pass

    hs = [threading.Thread(target=beber, args=(p.stdout, fuera, True), daemon=True),
          threading.Thread(target=beber, args=(p.stderr, err, False), daemon=True)]
    for h in hs: h.start()
    estado = "ok"
    try:
        p.wait(timeout=limite_s)
    except subprocess.TimeoutExpired:
        estado = "tiempo"
        matar()
        p.wait()
    for h in hs: h.join(2)
    ms = int((time.monotonic() - t0) * 1000)
    if corte[0] and estado == "ok":
        estado = "salida"
    return estado, p.returncode, b"".join(fuera), b"".join(err), ms


SENALES = {11: "falló el acceso a memoria (violación de segmento, p. ej. un puntero o índice fuera de rango)",
           6: "el programa abortó (assert, excepción sin capturar o abort())",
           8: "error aritmético (división entre cero)",
           9: "el programa se quedó sin memoria o fue detenido",
           24: "tiempo de CPU agotado"}


def limpia(t, n=1500):
    t = t.replace("/w/", "").replace("\r", "")
    return t[:n]


def juzgar(ej_id, codigo):
    cfg = config().get(ej_id)
    if not cfg:
        return {"error": "Ejercicio sin juez"}
    carpeta_tests = RAIZ / "juez" / "tests" / ej_id
    pruebas = sorted(carpeta_tests.glob("*.in"), key=lambda p: int(p.stem))
    if not pruebas:
        return {"error": "Ejercicio sin pruebas"}
    limite_ms = cfg.get("limite_ms", 3000)
    # Filtro previo (capa extra; la protección real es la caja)
    revisable = PAUSA.sub("", codigo)
    for rx, motivo in PROHIBIDO:
        m = rx.search(revisable)
        if m:
            return {"veredicto": "ce", "log": f"Rechazado antes de compilar: {motivo} («{m.group(0).strip()[:40]}»)."}
    with tempfile.TemporaryDirectory(prefix="juez-") as td:
        carp = Path(td)
        os.chmod(td, 0o755)
        for c in cfg.get("cabeceras", []):
            shutil.copy(RAIZ / c, carp / Path(c).name)
        (carp / "main.cpp").write_text(codigo, encoding="utf-8", newline="\n")
        comp = comando_caja(carp, ["prlimit", "--cpu=20", "--fsize=33554432", "--core=0", "--",
                                   "g++", "-std=c++17", "-O2", "-DDOMJUDGE", "-I/w", "-o", "/w/prog", "/w/main.cpp"] if not SIN_CAJA else
                            ["g++", "-std=c++17", "-O2", "-DDOMJUDGE", "-I" + str(carp), "-o", str(carp / BIN), str(carp / "main.cpp")],
                            MEM_COMPILAR, True)
        est, rc, out, err, _ = correr(comp, subprocess.DEVNULL, T_COMPILAR, 1 << 20)
        if est == "tiempo":
            return {"veredicto": "ce", "log": "La compilación tardó demasiado."}
        if rc != 0:
            return {"veredicto": "ce", "log": limpia((out + err).decode("utf-8", "replace"), 4000)}
        filas, global_v = [], "ac"
        for i, fin in enumerate(pruebas):
            n = int(fin.stem)
            esperada = leer(fin.with_suffix(".out"))
            cmd = comando_caja(carp, ["prlimit", f"--cpu={max(2, limite_ms // 1000 + 1)}", "--fsize=1048576",
                                      "--core=0", "--nofile=32", "--", "/w/prog"] if not SIN_CAJA else [str(carp / BIN)],
                               MEM_EJECUTAR, False)
            with open(fin, "rb") as fh:
                est, rc, out, err, ms = correr(cmd, fh, limite_ms / 1000 + 1.0, MAX_SALIDA)
            fila = {"n": n, "ms": ms}
            if est == "tiempo" or ms > limite_ms:
                fila["v"] = "tle"
            elif est == "salida":
                fila["v"] = "wa"; fila["dif"] = {"linea": 1, "esperada": "(salida razonable)", "obtenida": "(demasiada salida)", "total": 1}
            elif rc != 0:
                fila["v"] = "rte"
                s = -rc if rc < 0 else (rc - 128 if rc > 128 else 0)
                fila["detalle"] = SENALES.get(s, f"el programa terminó con código {rc}") + (": " + limpia(err.decode("utf-8", "replace"), 200).strip() if err.strip() else "")
            else:
                d = compara(esperada, out.decode("utf-8", "replace"))
                if d: fila["v"] = "wa"; fila["dif"] = d
                else: fila["v"] = "ac"
            filas.append(fila)
            if fila["v"] != "ac" and global_v == "ac":
                global_v = fila["v"]
            if fila["v"] == "tle":
                for fin2 in pruebas[i + 1:]:
                    filas.append({"n": int(fin2.stem), "v": "skip", "ms": 0})
                break
        return {"veredicto": global_v, "tests": filas}


class Manejador(BaseHTTPRequestHandler):
    server_version = "JuezDA"

    def log_message(self, fmt, *a):
        pass

    def _cors(self):
        o = self.headers.get("Origin", "")
        if "*" in ORIGENES:
            self.send_header("Access-Control-Allow-Origin", "*")
        elif o in ORIGENES:
            self.send_header("Access-Control-Allow-Origin", o)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, cod, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(cod)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path.startswith("/salud"):
            self._json(200, {"ok": True, "ejercicios": sorted(config().keys()), "caja": not SIN_CAJA})
        else:
            self._json(404, {"error": "no existe"})

    def do_POST(self):
        global cola
        if self.path != "/juzgar":
            return self._json(404, {"error": "no existe"})
        if "*" not in ORIGENES and self.headers.get("Origin", "") not in ORIGENES:
            return self._json(403, {"error": "origen no permitido"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n <= 0 or n > MAX_CODIGO + 1024:
                return self._json(413, {"error": "código demasiado grande (máx. 64 KB)"})
            datos = json.loads(self.rfile.read(n))
            ej, codigo = str(datos["id"]), str(datos["codigo"])
        except Exception:
            return self._json(400, {"error": "petición no válida"})
        if len(codigo.encode("utf-8")) > MAX_CODIGO:
            return self._json(413, {"error": "código demasiado grande (máx. 64 KB)"})
        ip = (self.headers.get("CF-Connecting-IP") if CONFIAR_CF else None) or self.client_address[0]
        ahora = time.monotonic()
        with ultimo_lock:
            if ahora - ultimo.get(ip, -99) < ESPERA_ENTRE_ENVIOS:
                return self._json(429, {"error": "Demasiado rápido: espera unos segundos entre envíos."})
            ultimo[ip] = ahora
            if len(ultimo) > 5000:
                for k in [k for k, v in ultimo.items() if ahora - v > 60]: ultimo.pop(k, None)
        with cola_lock:
            if cola >= MAX_COLA:
                return self._json(503, {"error": "El juez está ocupado. Prueba en un momento."})
            cola += 1
        try:
            with sem:
                r = juzgar(ej, codigo)
        except Exception as e:
            r = {"error": "Fallo interno del juez: " + type(e).__name__}
        finally:
            with cola_lock:
                cola -= 1
        self._json(200, r)


if __name__ == "__main__":
    if not SIN_CAJA and not shutil.which("bwrap"):
        raise SystemExit("Falta bubblewrap (bwrap). Para pruebas en local: JUEZ_SIN_CAJA=1")
    if SIN_CAJA:
        print("AVISO: sin caja. Solo para pruebas con tu propio código.")
    print(f"Juez en http://{HOST}:{PUERTO}  (raíz: {RAIZ}, ejercicios: {', '.join(config())})")
    ThreadingHTTPServer((HOST, PUERTO), Manejador).serve_forever()
