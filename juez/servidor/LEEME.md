# Servidor del juez (Raspberry Pi, sin root)

Corre con un usuario normal. Necesita: `python3` (3.9+), `g++`, `bwrap` (bubblewrap) y `prlimit`
(util-linux). `systemd-run --user` es opcional: si funciona y el cgroup de memoria está activo, se usa;
si no, el juez lo detecta solo y limita con `prlimit`.

## Instalar o actualizar en la Pi
    git clone -b claude/juez-da https://github.com/JuanP-G/DA.git ~/DA   # la primera vez
    cd ~/DA && git pull                                                  # para actualizar
    cd ~/DA/juez/servidor
    python3 servidor.py --diagnostico   # qué límites funcionan en esta Pi + autoprueba
    sh instalar.sh                      # servicio systemd (arranca solo, se reinicia si cae o se cuelga)
    python3 probar.py                   # 19 envíos de prueba + conexiones lentas

Registro de envíos y autopruebas: `journalctl -u juez-da -f`.
Salud desde fuera: `curl http://127.0.0.1:8099/salud/sistema` (temperatura, estrangulamiento, carga,
memoria, disco, límites activos y última autoprueba).

## Qué protege
- Caja de bubblewrap: sin red, `/usr` solo lectura, sin tus archivos, procesos aislados. Al ejecutar,
  todo el sistema de ficheros es de solo lectura (no se puede llenar la RAM escribiendo en `/tmp`).
- Memoria 256 MB por programa (1 GB al compilar). Con cgroup de memoria, `MemoryMax`; sin él,
  `prlimit --as`. La pila puede crecer hasta esos 256 MB (como DOMjudge): la recursión profunda no falla.
- Procesos: `TasksMax=48` con cgroups o `prlimit --nproc` sin ellos (`JUEZ_NPROC`, 256).
- Tiempo: cuenta el de CPU del programa, medido dentro de la caja (no el arranque ni la carga de la Pi).
  Además hay tope de reloj (2 × límite + 1 s) para programas que se quedan dormidos.
- Ficheros ≤ 1 MB, salida ≤ 2 MB, código ≤ 64 KB, filtro previo de código (capa extra).
- Cola: 2 ejecuciones a la vez, máx. 6 esperando; 1 envío cada 4 s por IP; máx. 48 conexiones y
  20 s para recibir cada petición.
- Autoprueba al arrancar y cada 10 min (compilar, ejecutar, recursión profunda, bucle infinito y
  límite de memoria). Si falla, `/juzgar` responde 503 y la web usa el compilador del navegador.
- Servicio systemd: `Restart=always`, watchdog (si deja de responder, se reinicia), y topes para todo
  el juez (`MemoryMax=2500M`, `TasksMax=600`, `OOMScoreAdjust=500`).
- Sin `JUEZ_ORIGENES` acepta peticiones de cualquier web; el servicio lo fija a StudIA.

## Raspberry Pi OS: activar el cgroup de memoria (recomendado)
Viene desactivado. Sin él, el límite de memoria por programa es `prlimit --as` (funciona, pero
`MemoryMax` del servicio no actúa). Para activarlo, añade al final de la única línea de
`/boot/firmware/cmdline.txt` (en Bullseye, `/boot/cmdline.txt`):

    cgroup_enable=memory cgroup_memory=1

y reinicia. `python3 servidor.py --diagnostico` dirá «cgroup memory en el núcleo: True».

## Variables
`JUEZ_ORIGENES` (CORS, p. ej. `https://studia-one-flax.vercel.app`), `JUEZ_PUERTO`, `JUEZ_HOST`,
`JUEZ_SIMULTANEOS`, `JUEZ_ESPERA` (s entre envíos por IP), `JUEZ_NPROC`, `JUEZ_TMP`,
`JUEZ_CGROUP` (`auto`, `1` exigir systemd-run, `0` no usarlo), `JUEZ_CONFIAR_CF=1` (IP real tras el
túnel de Cloudflare; solo se cree si la conexión viene de la propia Pi),
`JUEZ_SIN_CAJA=1` (SOLO para probar en tu PC con tu propio código: sin límites).

## Conectar la web
Al construir la web: `JUEZ_SERVIDOR=https://tu-url python sitio/construir.py`. Si el servidor no
responde en 150 s, está ocupado o en mantenimiento, la página usa el compilador del navegador
(WebAssembly) como respaldo.

## Si algo va mal
- Todo da «No compila» con `Failed to connect to bus`: versión antigua del servidor; actualiza.
- `/salud` da 503: lee `autoprueba.detalle` (o `journalctl -u juez-da -n 50`).
- Tiempos raros o «Tiempo excedido» de más: mira `estrangulada` en `/salud/sistema`; la Pi 4 baja
  la velocidad por calor (pon disipador/ventilador) o por fuente floja (usa la oficial de 3 A).
