#!/usr/bin/env python3
"""Servidor del juez de DA para Raspberry Pi (Linux, sin root).

Recibe  POST /juzgar  {"id": "04-3", "codigo": "..."}  y devuelve el veredicto.
Cada compilación y cada ejecución van dentro de una caja de bubblewrap (sin red, sistema en
solo lectura, sin tus archivos, procesos aislados) con límites de memoria, tiempo, tamaño y
procesos. Solo usa la biblioteca estándar de Python (3.9 o más nuevo).

Fiabilidad:
  - Al arrancar comprueba qué límites funcionan de verdad en esta máquina (cgroups de systemd o,
    si no, límites del núcleo con prlimit) y hace una autoprueba completa: compilar, ejecutar,
    comparar y verificar que el límite de memoria se aplica. La repite cada 10 minutos.
    Si falla, /juzgar responde 503 y la web usa el compilador del navegador.
  - El tiempo que cuenta es el de CPU del programa (no el de reloj), así el arranque de la caja
    o una Pi cargada no dan «Tiempo excedido» falsos.
  - Conexiones con tiempo máximo y número máximo (un cliente lento no bloquea el juez).
  - Registro de cada envío (sin el código) en la salida estándar: journalctl -u juez-da.
  - Watchdog de systemd (Type=notify): si el servidor se cuelga, systemd lo reinicia.

Diagnóstico de la máquina:  python3 servidor.py --diagnostico

Variables de entorno (todas opcionales):
  JUEZ_RAIZ      carpeta del repo DA (por defecto, dos niveles sobre este archivo)
  JUEZ_PUERTO    puerto (8099)          JUEZ_HOST  dirección (127.0.0.1)
  JUEZ_ORIGENES  orígenes CORS permitidos, separados por comas ("*" = todos)
  JUEZ_SIN_CAJA  1 = sin bubblewrap (SOLO para probar en tu PC; no usar con código ajeno)
  JUEZ_CGROUP    auto (por defecto) | 1 = exigir systemd-run --user | 0 = no usarlo
  JUEZ_SIMULTANEOS  ejecuciones a la vez (2)
  JUEZ_ESPERA    segundos entre dos envíos de la misma IP (4)
  JUEZ_NPROC     tope de procesos del usuario cuando no hay cgroups (256)
  JUEZ_TMP       carpeta para los ficheros temporales (por defecto, la del sistema)
  JUEZ_CONFIAR_CF   1 = leer la IP real de CF-Connecting-IP (solo si la conexión viene de
                    127.0.0.1, es decir, del túnel de Cloudflare en la propia Pi)
"""
import hashlib, json, os, re, shutil, signal, socket, subprocess, sys, tempfile, threading, time, traceback
import urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = Path(os.environ.get("JUEZ_RAIZ", AQUI.parent.parent)).resolve()
PUERTO = int(os.environ.get("JUEZ_PUERTO", "8099"))
HOST = os.environ.get("JUEZ_HOST", "127.0.0.1")
ORIGENES = [o.strip() for o in os.environ.get("JUEZ_ORIGENES", "*").split(",") if o.strip()]
SIN_CAJA = os.environ.get("JUEZ_SIN_CAJA") == "1"
MODO_CGROUP = os.environ.get("JUEZ_CGROUP", "auto").strip().lower()
CONFIAR_CF = os.environ.get("JUEZ_CONFIAR_CF") == "1"
BIN = "prog.exe" if os.name == "nt" else "prog"
SIMULTANEOS = max(1, int(os.environ.get("JUEZ_SIMULTANEOS", "2")))
ESPERA_ENTRE_ENVIOS = float(os.environ.get("JUEZ_ESPERA", "4"))
NPROC = int(os.environ.get("JUEZ_NPROC", "256"))
TMP = os.environ.get("JUEZ_TMP") or tempfile.gettempdir()

MAX_CODIGO = 64 * 1024          # bytes
MAX_SALIDA = 2 * 1024 * 1024    # bytes que se leen del programa
MAX_COLA = 6                    # peticiones esperando antes de decir «ocupado»
MAX_CONEXIONES = 48             # conexiones HTTP abiertas a la vez
T_SOCKET = 20                   # s: tiempo máximo para recibir la petición
T_COMPILAR = 25                 # s
MEM_COMPILAR = 1024 << 20       # bytes
MEM_EJECUTAR = 256 << 20        # bytes (también es el tamaño máximo de pila, como DOMjudge)
T_AUTOPRUEBA = 600              # s entre autopruebas

# Medidor: lanza el programa dentro de la caja, espera a que termine y escribe su tiempo de CPU,
# su estado de salida y su memoria máxima en un descriptor aparte. Hace falta porque bubblewrap
# sale sin recoger a su hijo y el tiempo de CPU del programa no llega hasta aquí.
MEDIDOR_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/audit.h>

/* seccomp: el programa del alumno no puede crear procesos ni hilos, ni usar llamadas que solo
   sirven para escaparse o atacar al núcleo. Se compila en la propia máquina, así los números
   de llamada son los de su arquitectura. */
#if defined(__x86_64__)
#define ARCH AUDIT_ARCH_X86_64
#elif defined(__aarch64__)
#define ARCH AUDIT_ARCH_AARCH64
#elif defined(__arm__)
#define ARCH AUDIT_ARCH_ARM
#elif defined(__i386__)
#define ARCH AUDIT_ARCH_I386
#endif

#define NIEGA(n) BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, (n), 0, 1), BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | EPERM)

static int seccomp_alumno(void) {
#ifndef ARCH
    return 0;
#else
    struct sock_filter f[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, ARCH, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),      /* otra ABI (int 0x80, etc.) */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
#if defined(__x86_64__)
        BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, 0x40000000, 0, 1),     /* ABI x32 */
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
#endif
#ifdef __NR_fork
        NIEGA(__NR_fork),
#endif
#ifdef __NR_vfork
        NIEGA(__NR_vfork),
#endif
        NIEGA(__NR_clone),
#ifdef __NR_clone3
        NIEGA(__NR_clone3),
#endif
        NIEGA(__NR_execveat), NIEGA(__NR_ptrace), NIEGA(__NR_process_vm_readv), NIEGA(__NR_process_vm_writev),
        NIEGA(__NR_mount), NIEGA(__NR_umount2), NIEGA(__NR_pivot_root), NIEGA(__NR_chroot),
        NIEGA(__NR_unshare), NIEGA(__NR_setns), NIEGA(__NR_keyctl), NIEGA(__NR_add_key), NIEGA(__NR_request_key),
        NIEGA(__NR_bpf), NIEGA(__NR_userfaultfd), NIEGA(__NR_perf_event_open), NIEGA(__NR_personality),
        NIEGA(__NR_kexec_load), NIEGA(__NR_init_module), NIEGA(__NR_finit_module), NIEGA(__NR_delete_module),
        NIEGA(__NR_socket), NIEGA(__NR_socketpair), NIEGA(__NR_connect), NIEGA(__NR_kill), NIEGA(__NR_tkill),
#ifdef __NR_io_uring_setup
        NIEGA(__NR_io_uring_setup), NIEGA(__NR_io_uring_enter), NIEGA(__NR_io_uring_register),
#endif
#ifdef __NR_open_by_handle_at
        NIEGA(__NR_open_by_handle_at),
#endif
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = { (unsigned short)(sizeof f / sizeof f[0]), f };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) return -1;
    return prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
#endif
}

int main(int argc, char **argv) {
    if (argc == 2 && argv[1][0] == '?') {               /* el servidor pregunta si hay seccomp */
#ifdef ARCH
        puts("seccomp");
#endif
        return 0;
    }
    if (argc < 3) return 120;
    int fd = atoi(argv[1]);
    fcntl(fd, F_SETFD, FD_CLOEXEC);          /* el programa no hereda el descriptor */
    pid_t p = fork();
    if (p < 0) return 121;
    if (p == 0) {
        if (seccomp_alumno()) _exit(124);    /* sin filtro no se ejecuta nada */
        execv(argv[2], argv + 2);
        _exit(122);
    }
    int st = 0; struct rusage ru;
    while (wait4(p, &st, 0, &ru) < 0 && errno == EINTR) {}
    long ms = ru.ru_utime.tv_sec * 1000L + ru.ru_utime.tv_usec / 1000
            + ru.ru_stime.tv_sec * 1000L + ru.ru_stime.tv_usec / 1000;
    dprintf(fd, "%ld %d %ld\n", ms, st, ru.ru_maxrss);
    if (WIFEXITED(st)) return WEXITSTATUS(st);
    if (WIFSIGNALED(st)) return 128 + WTERMSIG(st);
    return 123;
}
"""
MEDIDOR = None                  # carpeta con el medidor compilado (se monta en /m dentro de la caja)


def preparar_medidor():
    global MEDIDOR
    if SIN_CAJA:
        return None
    d = Path(tempfile.mkdtemp(prefix="medidor-", dir=TMP))
    os.chmod(d, 0o755)
    (d / "medidor.c").write_text(MEDIDOR_C)
    r = subprocess.run(["gcc" if shutil.which("gcc") else "g++", "-O2", "-x", "c", "-o", str(d / "medidor"), str(d / "medidor.c")],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    if r.returncode != 0:
        shutil.rmtree(d, ignore_errors=True)
        return "no se pudo compilar el medidor: " + r.stdout.decode("utf-8", "replace")[:200]
    os.chmod(d / "medidor", 0o755)
    r = subprocess.run([str(d / "medidor"), "?"], stdout=subprocess.PIPE, timeout=10)
    CAJA["seccomp"] = b"seccomp" in r.stdout
    import atexit
    atexit.register(shutil.rmtree, d, True)
    MEDIDOR = d
    return None


sem = threading.Semaphore(SIMULTANEOS)
cola = 0
cola_lock = threading.Lock()
ultimo = {}                     # ip -> instante del último envío
ultimo_lock = threading.Lock()
conexiones = threading.BoundedSemaphore(MAX_CONEXIONES)

# Lo que funciona en esta máquina (lo rellena detectar()) y el resultado de la última autoprueba.
CAJA = {"scope": False, "mem_cgroup": False, "pids_cgroup": False, "seccomp": False, "detalle": ""}
ESTADO = {"ok": False, "cuando": 0, "detalle": "sin autoprueba todavía"}
estado_lock = threading.Lock()

PROHIBIDO = [
    (re.compile(r'\b(system|popen|fork|vfork|execl|execlp|execle|execv|execvp|execve|socket|ptrace|dlopen|setuid|chroot|syscall)\s*\('), 'llamada no permitida'),
    (re.compile(r'\b__asm__\b|\basm\b|\.incbin|__builtin_(?!expect|unreachable|popcount|clz|ctz|memcpy|memset|abs)'), 'ensamblador o builtin no permitido'),
    (re.compile(r'#\s*include(_next)?\s*[<"]\s*(/|\.\./|[^>"]*\.\./)'), 'include con ruta no permitida'),
    (re.compile(r'#\s*pragma\s+(comment|GCC\s+(system_header|dependency)|include_alias)'), 'pragma no permitido'),
    (re.compile(r'__has_include|<filesystem>|<thread>|<future>|<unistd\.h>|<sys/|<signal\.h>|<csignal>|<dlfcn\.h>|<netinet|<arpa/'), 'cabecera no permitida'),
]

# Las soluciones de la asignatura traen system("pause") (solo Windows); esa llamada exacta se tolera.
PAUSA = re.compile(r'system\s*\(\s*"pause"\s*\)', re.I)


def log(*a):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)


def lineas(t):
    l = [x.rstrip() for x in t.replace("\r", "").split("\n")]
    while l and l[-1] == "":
        l.pop()
    return l


def compara(esperada, obtenida):
    """None si coinciden. Se comparan las palabras (separadas por espacios, tabuladores o saltos de
    línea): da igual cuántos espacios haya, si falta un salto de línea o sobran líneas vacías.
    Si no coinciden, devuelve la primera línea que difiere para enseñarla."""
    if esperada.split() == obtenida.split():
        return None
    a, b = lineas(esperada), lineas(obtenida)
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x != y:
            return {"linea": i + 1, "esperada": x, "obtenida": y, "total": len(a), "lineas_tuyas": len(b)}
    return {"linea": 1, "esperada": None, "obtenida": None, "total": len(a), "lineas_tuyas": len(b)}


# Nombres de fichero con los que los alumnos suelen leer la entrada (plantillas de la asignatura:
# casos.txt). Se crean con los mismos datos que llegan por la entrada estándar, así que vale tanto
# leer con cin como abrir el fichero.
FICHEROS_ENTRADA = ("casos.txt", "datos.txt", "entrada.txt", "input.txt", "in.txt")


def cabeceras_comunes():
    """Cabeceras de la asignatura («Estructuras de datos/*.h»): están disponibles en todos los
    ejercicios, con el mismo nombre que usan los alumnos en #include."""
    d = RAIZ / "Estructuras de datos"
    return sorted(d.glob("*.h")) if d.is_dir() else []


def leer(p):
    b = Path(p).read_bytes()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1252", "replace")


def config():
    """juez/juez.json (antigua) + juez/tests/<id>/config.json (una por ejercicio)."""
    cfg = {}
    p = RAIZ / "juez" / "juez.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    for c in sorted((RAIZ / "juez" / "tests").glob("*/config.json")):
        cfg[c.parent.name] = json.loads(c.read_text(encoding="utf-8"))
    return cfg


# ---------------------------------------------------------------- caja (bubblewrap + límites)

def montajes_sistema():
    """Monta /usr y reproduce /lib, /lib64, /bin... tal como estén en esta máquina (usr fusionado
    o no; aarch64, armhf o x86_64). Si falta el cargador dinámico, nada arranca dentro de la caja."""
    m = ["--ro-bind", "/usr", "/usr"]
    for d in ("lib", "lib64", "lib32", "bin", "sbin"):
        p = Path("/" + d)
        if p.is_symlink():
            m += ["--symlink", os.readlink(p).lstrip("/"), "/" + d]
        elif p.is_dir():
            m += ["--ro-bind", "/" + d, "/" + d]
    # g++ no necesita nada más de /etc; el cargador usa sus rutas por defecto sin ld.so.cache.
    # Pero /usr/bin/g++ puede ser un enlace a /etc/alternatives (update-alternatives, Ubuntu...).
    if Path("/etc/alternatives").is_dir():
        m += ["--ro-bind", "/etc/alternatives", "/etc/alternatives"]
    return m


def comando_caja(carpeta, argv, mem, escribible, cpu_s, procs, fd_medida=None):
    """Envuelve argv con prlimit + bubblewrap (+ systemd-run si hay cgroups que funcionen).
    Con fd_medida, el programa va bajo el medidor, que escribe en ese descriptor."""
    if SIN_CAJA:
        return argv
    # CPU: al pasar el límite blando llega SIGXCPU (= tiempo excedido); el duro es la red de seguridad.
    lim = ["prlimit", f"--cpu={cpu_s}:{cpu_s + 1}", "--core=0", f"--stack={mem}"]
    if escribible:
        lim += ["--fsize=33554432"]
    else:
        lim += ["--fsize=1048576", "--nofile=32"]
    if not CAJA["mem_cgroup"]:
        # Sin cgroup de memoria (habitual en Raspberry Pi OS: viene desactivado en el núcleo),
        # el único tope es el espacio de direcciones. Sin esto, un programa se come toda la RAM.
        lim += [f"--as={mem + (64 << 20)}"]
    if not CAJA["pids_cgroup"]:
        lim += [f"--nproc={NPROC}"]
    bw = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session"] + montajes_sistema() + [
          "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
          ("--bind" if escribible else "--ro-bind"), str(carpeta), "/w", "--chdir", "/w",
          "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "LC_ALL", "C.UTF-8"]
    if not escribible:
        # Al ejecutar no hace falta escribir en ningún sitio: así no se puede llenar la RAM con
        # ficheros en /tmp o /dev/shm (tmpfs) aunque no haya cgroup de memoria.
        bw += ["--remount-ro", "/tmp", "--remount-ro", "/dev"]
    if fd_medida is not None and MEDIDOR:
        bw += ["--ro-bind", str(MEDIDOR), "/m"]
        argv = ["/m/medidor", str(fd_medida)] + argv
    if not escribible:
        bw += ["--remount-ro", "/"]
    cmd = bw + ["--"] + lim + ["--"] + argv
    if CAJA["scope"]:
        props = ["-p", "TasksMax=%d" % procs]
        if CAJA["mem_cgroup"]:
            props += ["-p", f"MemoryMax={mem}", "-p", "MemorySwapMax=0"]
        return ["systemd-run", "--user", "--scope", "--quiet", "--collect"] + props + cmd
    return cmd


def correr(cmd, entrada, limite_s, tope_salida, fd_medida=None):
    """Ejecuta cmd. Devuelve (estado, código, stdout, stderr, ms_cpu, ms_reloj, medida).
    estado: ok | tiempo | salida. medida: (ms_cpu, estado_wait, maxrss_kb) del medidor o None."""
    t0 = time.monotonic()
    try:
        p = subprocess.Popen(cmd, stdin=entrada, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True, pass_fds=(fd_medida[1],) if fd_medida else ())
    finally:
        if fd_medida:
            os.close(fd_medida[1])
    fuera, err = [], []
    tam = [0, 0]
    corte = [False]

    def matar():
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except Exception:
            try: p.kill()
            except Exception: pass

    def beber(f, dest, i, tope):
        while True:
            d = f.read(65536)
            if not d:
                break
            tam[i] += len(d)
            if i == 0 and tam[0] > tope:
                corte[0] = True
                matar()
                break
            if i == 0 or tam[1] <= 65536:
                dest.append(d)

    hs = [threading.Thread(target=beber, args=(p.stdout, fuera, 0, tope_salida), daemon=True),
          threading.Thread(target=beber, args=(p.stderr, err, 1, 0), daemon=True)]
    for h in hs: h.start()
    estado = "ok"
    fin = t0 + limite_s
    while True:
        pid, st, ru = os.wait4(p.pid, os.WNOHANG)
        if pid:
            break
        if time.monotonic() > fin:
            estado = "tiempo"
            matar()
            pid, st, ru = os.wait4(p.pid, 0)
            break
        time.sleep(0.005)
    p.returncode = os.waitstatus_to_exitcode(st)
    for h in hs: h.join(2)
    for f in (p.stdout, p.stderr):
        try: f.close()
        except Exception: pass
    ms_reloj = int((time.monotonic() - t0) * 1000)
    ms_cpu = int((ru.ru_utime + ru.ru_stime) * 1000)
    if corte[0] and estado == "ok":
        estado = "salida"
    medida = None
    if fd_medida:
        try:
            os.set_blocking(fd_medida[0], False)
            m = os.read(fd_medida[0], 200).split()
            medida = (int(m[0]), int(m[1]), int(m[2]))
        except Exception:
            pass
        finally:
            os.close(fd_medida[0])
    return estado, p.returncode, b"".join(fuera), b"".join(err), ms_cpu, ms_reloj, medida


SENALES = {11: "falló el acceso a memoria (violación de segmento, p. ej. un puntero o índice fuera de rango)",
           6: "el programa abortó (assert, excepción sin capturar o abort())",
           8: "error aritmético (división entre cero)",
           9: "el programa se quedó sin memoria o fue detenido",
           7: "error de bus (acceso a memoria no válido)"}


def senal(rc):
    return -rc if rc < 0 else (rc - 128 if rc > 128 else 0)


def limpia(t, n=1500):
    t = t.replace("/w/", "").replace("\r", "")
    return t[:n]


def compilar(carp):
    """Compila /w/main.cpp. Devuelve None si va bien o el veredicto «ce»."""
    argv = (["g++", "-std=c++17", "-O2", "-pipe", "-DDOMJUDGE", "-I/w", "-o", "/w/prog", "/w/main.cpp"] if not SIN_CAJA else
            ["g++", "-std=c++17", "-O2", "-pipe", "-DDOMJUDGE", "-I" + str(carp), "-o", str(carp / BIN), str(carp / "main.cpp")])
    comp = comando_caja(carp, argv, MEM_COMPILAR, True, 20, 48)
    est, rc, out, err, _, _, _ = correr(comp, subprocess.DEVNULL, T_COMPILAR, 1 << 20)
    if est == "tiempo" or senal(rc) == 24:
        return {"veredicto": "ce", "log": "La compilación tardó demasiado."}
    if rc != 0:
        texto = (out + err).decode("utf-8", "replace")
        if senal(rc) == 9 or "virtual memory exhausted" in texto or "out of memory" in texto.lower():
            texto = "El compilador se quedó sin memoria (límite 1 GB).\n" + texto
        return {"veredicto": "ce", "log": limpia(texto, 4000)}
    return None


def ejecutar(carp, entrada, limite_ms):
    """Ejecuta el programa ya compilado con una entrada. Devuelve (fila, salida)."""
    cpu = max(2, -(-limite_ms // 1000) + 1)          # tope duro de CPU (s), por encima del límite
    argv = ["/w/prog"] if not SIN_CAJA else ["env", "-C", str(carp), str(carp / BIN)]   # en la caja el directorio ya es /w
    fdm = os.pipe() if (MEDIDOR and not SIN_CAJA) else None
    cmd = comando_caja(carp, argv, MEM_EJECUTAR, False, cpu, 16, fdm[1] if fdm else None)
    est, rc, out, err, ms, pared, medida = correr(cmd, entrada, 2 * limite_ms / 1000 + 1.0, MAX_SALIDA, fdm)
    if medida:                                        # lo que midió el medidor dentro de la caja
        ms = medida[0]
        rc = os.waitstatus_to_exitcode(medida[1])
        fila = {"ms": ms, "kb": medida[2]}
    else:
        # Sin medidor (o lo cortamos antes de que informara): tiempo de reloj, que incluye el
        # arranque de la caja. El rusage de bubblewrap no sirve: no recoge a su hijo.
        ms = pared
        fila = {"ms": ms}
    s = senal(rc)
    texto_err = err.decode("utf-8", "replace")
    if est == "tiempo" or ms > limite_ms or s == 24 or (s == 9 and not CAJA["mem_cgroup"] and ms >= limite_ms):
        fila["v"] = "tle"
        fila["ms"] = max(ms, limite_ms + 1) if est == "tiempo" else ms
    elif est == "salida":
        fila["v"] = "ole"
        fila["detalle"] = f"escribió más de {MAX_SALIDA >> 20} MB (¿un bucle que no termina de escribir?)"
    elif "bad_alloc" in texto_err or (s == 9 and CAJA["mem_cgroup"]) or (rc != 0 and fila.get("kb", 0) > (MEM_EJECUTAR >> 10) * 0.9):
        fila["v"] = "mle"
        fila["detalle"] = f"pasó del límite de memoria de {MEM_EJECUTAR >> 20} MB"
    elif rc != 0:
        fila["v"] = "rte"
        if rc == 124 or (rc != 0 and "Operation not permitted" in texto_err):
            base = "el programa intentó algo que el juez no permite (crear procesos, red...)"
        else:
            base = SENALES.get(s, f"el programa terminó con código {rc}")
        fila["detalle"] = base + (": " + limpia(texto_err, 200).strip() if texto_err.strip() else "")
    return fila, out


def filtro(codigo):
    revisable = PAUSA.sub("", codigo)
    for rx, motivo in PROHIBIDO:
        m = rx.search(revisable)
        if m:
            return {"veredicto": "ce", "log": f"Rechazado antes de compilar: {motivo} («{m.group(0).strip()[:40]}»)."}
    return None


_comprobadores = {}


def comprobador(ej_id):
    """Comprobador propio del ejercicio (juez/tests/<id>/comprobador.py), para los que admiten
    varias respuestas correctas. Se recarga si cambia el fichero."""
    p = RAIZ / "juez" / "tests" / ej_id / "comprobador.py"
    clave = (str(p), p.stat().st_mtime)
    if _comprobadores.get(ej_id, (None,))[0] != clave:
        ns = {}
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
        _comprobadores[ej_id] = (clave, ns["comprobar"])
    return _comprobadores[ej_id][1]


def juzgar(ej_id, codigo):
    cfg = config().get(ej_id)
    if not cfg:
        return {"error": "Ejercicio sin juez"}
    carpeta_tests = RAIZ / "juez" / "tests" / ej_id
    pruebas = sorted((p for p in carpeta_tests.glob("*.in") if p.stem.isdigit()), key=lambda p: int(p.stem))
    if not pruebas:
        return {"error": "Ejercicio sin pruebas"}
    limite_ms = cfg.get("limite_ms", 3000)
    rechazo = filtro(codigo)                         # capa extra; la protección real es la caja
    if rechazo:
        return rechazo
    with tempfile.TemporaryDirectory(prefix="juez-", dir=TMP) as td:
        carp = Path(td)
        os.chmod(td, 0o755)
        for h in cabeceras_comunes():
            shutil.copy(h, carp / h.name)
        for c in cfg.get("cabeceras", []):              # las propias del ejercicio mandan sobre las comunes
            shutil.copy(RAIZ / c, carp / Path(c).name)
        (carp / "main.cpp").write_text(codigo, encoding="utf-8", newline="\n")
        ce = compilar(carp)
        if ce:
            return ce
        filas, global_v = [], "ac"
        for i, fin in enumerate(pruebas):
            datos = fin.read_bytes()
            for nombre in FICHEROS_ENTRADA:
                (carp / nombre).write_bytes(datos)
            with open(fin, "rb") as fh:
                fila, out = ejecutar(carp, fh, limite_ms)
            fila["n"] = int(fin.stem)
            if "v" not in fila:
                esperada, obtenida = leer(fin.with_suffix(".out")), out.decode("utf-8", "replace")
                if cfg.get("comprobador"):
                    try:
                        d = comprobador(ej_id)(leer(fin), esperada, obtenida)
                    except Exception as e:              # salida tan rara que el comprobador no la entiende
                        d = {"linea": 1, "esperada": None, "obtenida": None, "total": 0,
                             "motivo": f"no se entiende la salida ({type(e).__name__})"}
                else:
                    d = compara(esperada, obtenida)
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


# ---------------------------------------------------------------- detección y autoprueba

def _ejecuta(cmd, t=15):
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=t)
        return r.returncode, r.stdout.decode("utf-8", "replace").strip()
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def detectar():
    """Decide qué mecanismos de límite usar según lo que funcione DE VERDAD en esta máquina."""
    notas = []
    CAJA.update(scope=False, mem_cgroup=False, pids_cgroup=False)
    if SIN_CAJA:
        CAJA["detalle"] = "sin caja"
        return
    for prog in ("bwrap", "prlimit", "g++"):
        if not shutil.which(prog):
            notas.append(f"falta {prog}")
    if MODO_CGROUP != "0" and shutil.which("systemd-run"):
        # Dentro de un scope con MemoryMax y TasksMax: ¿se ven memory.max y pids.max aplicados?
        sonda = ("c=/sys/fs/cgroup$(grep '^0::' /proc/self/cgroup | cut -d: -f3); "
                 "echo mem=$(cat $c/memory.max 2>/dev/null) pids=$(cat $c/pids.max 2>/dev/null)")
        rc, out = _ejecuta(["systemd-run", "--user", "--scope", "--quiet", "--collect",
                            "-p", "MemoryMax=64M", "-p", "TasksMax=7", "sh", "-c", sonda])
        if rc == 0 and "mem=" in out:
            CAJA["scope"] = True
            CAJA["mem_cgroup"] = "mem=67108864" in out
            CAJA["pids_cgroup"] = "pids=7" in out
            if not CAJA["mem_cgroup"]:
                notas.append("systemd-run funciona pero el cgroup de memoria no (en Raspberry Pi OS: "
                             "añade «cgroup_enable=memory cgroup_memory=1» a /boot/firmware/cmdline.txt); "
                             "se usa prlimit --as")
        else:
            notas.append("systemd-run --user no disponible (" + out.splitlines()[-1][:80] + "); se usa prlimit"
                         if out else "systemd-run --user no disponible; se usa prlimit")
            if MODO_CGROUP == "1":
                notas.append("JUEZ_CGROUP=1 exige systemd-run --user: la autoprueba fallará")
    CAJA["detalle"] = "; ".join(notas) or "todo disponible"


AUTO_SUMA = '#include <iostream>\nint main(){ long long a,b; std::cin>>a>>b; std::cout<<a+b<<"\\n"; }\n'
AUTO_MEMORIA = ('#include <vector>\n#include <cstdio>\nint main(){ std::vector<char*> v; '
                'for(int i=0;i<2048;i++){ char*p=new char[1<<20]; for(int j=0;j<(1<<20);j+=4096) p[j]=1; '
                'v.push_back(p);} std::printf("SIN LIMITE\\n"); }\n')
AUTO_PROCESOS = ('#include <cstdio>\nextern "C" int fork();\n'
                 'int main(){ int r = fork(); if (r == 0) return 0; std::printf(r < 0 ? "bloqueado\\n" : "PERMITIDO\\n"); }\n')
AUTO_BUCLE = 'int main(){ for(volatile unsigned long i=0;;i++){} }\n'
AUTO_PILA = ('#include <cstdio>\nint f(int n){ volatile char b[64]; b[0]=(char)n; return n? f(n-1)+b[0] : 0; }\n'
             'int main(){ std::printf("%d\\n", f(300000) != 12345); }\n')


def autoprueba():
    """Compila y ejecuta tres programas por la misma vía que los envíos reales.
    Devuelve (ok, detalle)."""
    fallos = []
    try:
        libre = shutil.disk_usage(TMP).free
        if libre < 200 << 20:
            fallos.append(f"poco disco libre en {TMP}: {libre >> 20} MB")
        with tempfile.TemporaryDirectory(prefix="juez-auto-", dir=TMP) as td:
            carp = Path(td)
            os.chmod(td, 0o755)
            for nombre, codigo, entrada, esperado in (("suma", AUTO_SUMA, b"2 40\n", "42"),
                                                      ("pila", AUTO_PILA, b"", "1"),
                                                      ("memoria", AUTO_MEMORIA, b"", None),
                                                      ("bucle", AUTO_BUCLE, b"", "TLE"),
                                                      ("procesos", AUTO_PROCESOS, b"", "bloqueado")):
                if (SIN_CAJA and nombre in ("pila", "memoria")) or (nombre == "procesos" and not CAJA["seccomp"]):
                    continue                     # sin caja no hay límites que comprobar
                (carp / "main.cpp").write_text(codigo, encoding="utf-8")
                ce = compilar(carp)
                if ce:
                    fallos.append(f"{nombre}: no compila: {ce['log'][:300]}")
                    break
                with tempfile.TemporaryFile() as fh:
                    fh.write(entrada); fh.seek(0)
                    fila, out = ejecutar(carp, fh, 1000 if nombre == "bucle" else 3000)
                salida = out.decode("utf-8", "replace").strip()
                if esperado == "TLE":
                    if fila.get("v") != "tle":
                        fallos.append(f"bucle: un bucle infinito no dio «tiempo excedido»: {fila}")
                elif esperado is not None:
                    if fila.get("v") or salida != esperado:
                        fallos.append(f"{nombre}: esperaba {esperado!r} y obtuvo {salida[:60]!r} {fila}")
                elif "SIN LIMITE" in salida or not fila.get("v"):
                    fallos.append("memoria: un programa pudo reservar 2 GB; el límite de memoria NO se aplica")
    except Exception as e:
        fallos.append(f"excepción {type(e).__name__}: {e}")
    return (not fallos), ("; ".join(fallos) or "ok")


def autoprueba_y_guarda(motivo):
    with sem:
        t = time.monotonic()
        ok, det = autoprueba()
    with estado_lock:
        cambio = ok != ESTADO["ok"]
        ESTADO.update(ok=ok, cuando=int(time.time()), detalle=det, segundos=round(time.monotonic() - t, 1))
    if cambio or not ok:
        log(f"autoprueba ({motivo}): {'OK' if ok else 'FALLO'} · {det}")
    return ok


def bucle_autoprueba():
    while True:
        time.sleep(T_AUTOPRUEBA if ESTADO["ok"] else 60)
        try:
            autoprueba_y_guarda("periódica")
        except Exception:
            traceback.print_exc()


def limpiar_restos():
    """Borra carpetas juez-* y medidor-* que quedaran de un apagado brusco."""
    ahora = time.time()
    for p in list(Path(TMP).glob("juez-*")) + list(Path(TMP).glob("medidor-*")):
        try:
            if p.is_dir() and ahora - p.stat().st_mtime > 600:
                shutil.rmtree(p, ignore_errors=True)
        except Exception:
            pass


def sistema():
    """Datos de salud de la Pi: temperatura, estrangulamiento, carga, memoria y disco."""
    d = {}
    try:
        d["temp_c"] = round(int(Path("/sys/class/thermal/thermal_zone0/temp").read_text()) / 1000, 1)
    except Exception:
        pass
    if shutil.which("vcgencmd"):
        rc, out = _ejecuta(["vcgencmd", "get_throttled"], 3)
        if rc == 0 and "=" in out:
            v = int(out.split("=")[1], 16)
            d["estrangulada"] = {"ahora": bool(v & 0x4), "subtension_ahora": bool(v & 0x1),
                                 "desde_arranque": bool(v & 0x40000), "subtension_desde_arranque": bool(v & 0x10000),
                                 "crudo": out.split("=")[1]}
    try:
        d["carga"] = [round(x, 2) for x in os.getloadavg()]
    except Exception:
        pass
    try:
        mi = dict(l.split(":", 1) for l in Path("/proc/meminfo").read_text().splitlines())
        d["mem_libre_mb"] = int(mi["MemAvailable"].split()[0]) >> 10
        d["swap_libre_mb"] = int(mi["SwapFree"].split()[0]) >> 10
    except Exception:
        pass
    try:
        d["disco_libre_mb"] = shutil.disk_usage(TMP).free >> 20
    except Exception:
        pass
    return d


# ---------------------------------------------------------------- HTTP

def ip_de(h):
    par = h.client_address[0]
    if CONFIAR_CF and par in ("127.0.0.1", "::1", "::ffff:127.0.0.1"):
        return h.headers.get("CF-Connecting-IP") or par
    return par


class Manejador(BaseHTTPRequestHandler):
    server_version = "JuezDA"
    sys_version = ""
    timeout = T_SOCKET                 # un cliente que no termina de enviar no bloquea un hilo para siempre

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
        self.send_header("Access-Control-Max-Age", "600")

    def _json(self, cod, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        try:
            self.send_response(cod)
            self._cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(b)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            pass                       # el alumno cerró la pestaña: no es un fallo del juez

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path.startswith("/salud"):
            with estado_lock:
                auto = dict(ESTADO)
            try:
                ejs = sorted(config().keys())
            except Exception as e:
                ejs, auto["ok"] = [], False
                auto["detalle"] = f"juez.json ilegible: {e}"
            cuerpo = {"ok": auto["ok"], "ejercicios": ejs, "caja": not SIN_CAJA,
                      "limites": {k: CAJA[k] for k in ("scope", "mem_cgroup", "pids_cgroup", "seccomp", "detalle")},
                      "autoprueba": auto, "cola": cola, "simultaneos": SIMULTANEOS}
            if "/salud/sistema" in self.path or "sistema=1" in self.path:
                cuerpo["sistema"] = sistema()
            self._json(200 if auto["ok"] else 503, cuerpo)
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
            if n <= 0 or n > MAX_CODIGO * 2 + 1024:
                return self._json(413, {"error": "código demasiado grande (máx. 64 KB)"})
            datos = json.loads(self.rfile.read(n))
            ej, codigo = str(datos["id"]), str(datos["codigo"])
        except socket.timeout:
            return
        except Exception:
            return self._json(400, {"error": "petición no válida"})
        if len(codigo.encode("utf-8")) > MAX_CODIGO:
            return self._json(413, {"error": "código demasiado grande (máx. 64 KB)"})
        if not ESTADO["ok"]:
            return self._json(503, {"error": "El juez está en mantenimiento.", "mantenimiento": True})
        ip = ip_de(self)
        ahora = time.monotonic()
        with ultimo_lock:
            if ahora - ultimo.get(ip, -99) < ESPERA_ENTRE_ENVIOS:
                return self._json(429, {"error": "Demasiado rápido: espera unos segundos entre envíos."})
            if len(ultimo) > 5000:
                for k in [k for k, v in ultimo.items() if ahora - v > 60]: ultimo.pop(k, None)
        with cola_lock:
            if cola >= MAX_COLA:
                return self._json(503, {"error": "El juez está ocupado. Prueba en un momento.", "ocupado": True})
            cola += 1
            en_cola = cola
        with ultimo_lock:
            ultimo[ip] = ahora
        t = time.monotonic()
        espera = 0.0
        try:
            with sem:
                espera = time.monotonic() - t
                r = juzgar(ej, codigo)
        except Exception as e:
            traceback.print_exc()
            r = {"error": "Fallo interno del juez: " + type(e).__name__}
        finally:
            with cola_lock:
                cola -= 1
        quien = hashlib.sha256(ip.encode()).hexdigest()[:8]
        log(f"{quien} {ej} {r.get('veredicto') or 'error:' + str(r.get('error'))[:40]} "
            f"cola={en_cola} espera={espera:.1f}s total={time.monotonic() - t:.1f}s")
        self._json(200, r)


class Servidor(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 64
    allow_reuse_address = True

    def process_request(self, request, client_address):
        if not conexiones.acquire(blocking=False):
            self.shutdown_request(request)              # demasiadas conexiones: se cierra sin más
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            conexiones.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            conexiones.release()


# ---------------------------------------------------------------- systemd (notify + watchdog)

NOTIFY_SOCKET = os.environ.pop("NOTIFY_SOCKET", None)   # que no lo hereden g++, systemd-run, etc.


def sd_notify(msg):
    dest = NOTIFY_SOCKET
    if not dest:
        return
    if dest.startswith("@"):
        dest = "\0" + dest[1:]
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
            s.connect(dest)
            s.sendall(msg.encode())
    except Exception:
        pass


def bucle_watchdog():
    """Solo avisa a systemd si el servidor HTTP responde de verdad; si se cuelga, systemd lo reinicia."""
    us = int(os.environ.get("WATCHDOG_USEC", "0"))
    if not us:
        return
    paso = max(1.0, us / 1e6 / 3)
    url = f"http://{'127.0.0.1' if HOST in ('0.0.0.0', '') else ('[::1]' if HOST == '::' else HOST)}:{PUERTO}/salud"
    while True:
        try:
            urllib.request.urlopen(url, timeout=5).read()
            sd_notify("WATCHDOG=1")
        except urllib.error.HTTPError:
            sd_notify("WATCHDOG=1")                     # 503 en mantenimiento: pero responde
        except Exception:
            pass
        time.sleep(paso)


def diagnostico():
    print(f"Python {sys.version.split()[0]} · raíz {RAIZ} · temporales en {TMP}")
    for prog in ("bwrap", "prlimit", "g++", "systemd-run", "vcgencmd"):
        print(f"  {prog:12} {shutil.which(prog) or 'NO ENCONTRADO'}")
    try:
        cg = Path("/proc/cgroups").read_text()
        mem = [l for l in cg.splitlines() if l.startswith("memory")]
        print("  cgroup memory en el núcleo:", mem[0].split()[-1] == "1" if mem else "no existe")
    except Exception:
        pass
    print("  línea del núcleo:", Path("/proc/cmdline").read_text().strip()[:200])
    detectar()
    nota = preparar_medidor()
    if nota:
        CAJA["detalle"] += f"; medidor: {nota}"
    print("Límites:", json.dumps({k: CAJA[k] for k in ("scope", "mem_cgroup", "pids_cgroup", "seccomp", "detalle")}, ensure_ascii=False))
    t = time.monotonic()
    ok, det = autoprueba()
    print(f"Autoprueba: {'OK' if ok else 'FALLO'} ({time.monotonic() - t:.1f}s) · {det}")
    print("Sistema:", json.dumps(sistema(), ensure_ascii=False))
    try:
        print("Ejercicios:", ", ".join(config()))
    except Exception as e:
        print("juez.json ilegible:", e); ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    if "--diagnostico" in sys.argv:
        raise SystemExit(diagnostico())
    if not SIN_CAJA and not shutil.which("bwrap"):
        raise SystemExit("Falta bubblewrap (bwrap). Para pruebas en local: JUEZ_SIN_CAJA=1")
    if SIN_CAJA:
        log("AVISO: sin caja. Solo para pruebas con tu propio código.")
    srv = Servidor((HOST, PUERTO), Manejador)    # primero el puerto: si ya hay otro juez, se para aquí
    limpiar_restos()
    detectar()
    nota = preparar_medidor()
    if nota:
        CAJA["detalle"] += f"; medidor: {nota} (se usa el tiempo de reloj)"
    log(f"límites: scope={CAJA['scope']} mem_cgroup={CAJA['mem_cgroup']} pids_cgroup={CAJA['pids_cgroup']} seccomp={CAJA['seccomp']} · {CAJA['detalle']}")
    autoprueba_y_guarda("arranque")
    if not ESTADO["ok"]:
        log("AVISO: la autoprueba falla; /juzgar responderá 503 (la web usará el navegador) hasta que se arregle.")
    threading.Thread(target=bucle_autoprueba, daemon=True).start()
    threading.Thread(target=bucle_watchdog, daemon=True).start()
    signal.signal(signal.SIGTERM, lambda *a: (sd_notify("STOPPING=1"), threading.Thread(target=srv.shutdown).start()))
    log(f"Juez en http://{HOST}:{PUERTO}  (raíz: {RAIZ}, ejercicios: {', '.join(config())})")
    sd_notify("READY=1")
    srv.serve_forever()
