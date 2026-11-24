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
    python3 probar.py                   # 22 envíos de prueba + conexiones lentas

Registro de envíos y autopruebas: `journalctl -u juez-da -f`.
Salud desde fuera: `curl http://127.0.0.1:8099/salud/sistema` (temperatura, estrangulamiento, carga,
memoria, disco, límites activos y última autoprueba).

## Qué protege (código malicioso)
Las capas, de fuera a dentro; cada una funciona aunque fallen las demás:
- **seccomp** (dentro de la caja, lo instala el medidor justo antes de ejecutar): el programa del
  alumno no puede crear procesos ni hilos, ni usar ptrace, montar, módulos, eBPF, io_uring, red,
  enviar señales a otros... Lo que ningún ejercicio necesita. Se compila en la propia Pi.
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

## Entrada, salida y cabeceras
- La entrada llega por la entrada estándar (`cin`) y además se crean los ficheros `casos.txt`, `datos.txt`,
  `entrada.txt`, `input.txt` e `in.txt` con los mismos datos, así que vale leer con `cin` o abriendo el
  fichero. Se compila con `-DDOMJUDGE`, como en el juez de la asignatura.
- La salida se compara por palabras: da igual el número de espacios, que falte o sobre algún salto de
  línea o que haya líneas vacías. Solo cuenta que las palabras y su orden coincidan. No hay «error de
  presentación».
- Todas las cabeceras de `Estructuras de datos/*.h` (incluida `EnterosInf.h`) están disponibles en todos
  los ejercicios. Las que traiga un ejercicio en su `config.json` mandan sobre las comunes.

## Veredictos
| Sigla | Nombre | Cuándo |
|---|---|---|
| AC | Correcto | Pasa todas las pruebas. |
| WA | Respuesta incorrecta | Termina pero escribe otra cosa. |
| CE | Error de compilación | No compila, o usa algo prohibido (system, fork, cabeceras del sistema...). |
| TLE | Tiempo excedido | Pasa del límite de CPU, o se queda parado (tope de reloj). |
| MLE | Memoria excedida | Pasa de 256 MB. |
| RTE | Error de ejecución | Se rompe: fuera de rango, división entre cero, excepción, intento bloqueado por seccomp... |
| OLE | Salida excesiva | Escribe más de 2 MB. |

El veredicto global es el de la primera prueba que falla; tras un TLE no se ejecutan las demás.

## Pruebas con guía y pistas
Cada ejercicio tiene muchas pruebas pequeñas y cada una busca **un error típico**. Se generan con
`herramientas/generar_tests_juez.py` (la salida esperada la calcula un solucionador independiente en
Python) y se describen en `juez/tests/<id>/pruebas.json`:

    {"n": 9, "nombre": "Final de una fila y principio de la siguiente",
     "tipo": "trampa",                     // enunciado | borde | trampa | aleatorio | rendimiento
     "casos": 2,
     "comprueba": "qué mira esta prueba",
     "si": {"wa": "qué suele significar fallarla", "rte": "..."},
     "pistas": ["pista suave", "pista más directa"]}

La web elige la prueba que mejor explica el fallo (antes las trampas y los bordes, las que fallan en
su primer caso y las que tienen explicación para ese veredicto), detecta patrones (solo falla el
formato, estado que no se reinicia entre casos, solo fallan las grandes...) y ofrece «Dame una pista»:
las pistas de esa prueba de menos a más y, al final, su entrada y la salida esperada (si es pequeña).

Hoy lo tienen los 44 ejercicios de los temas 1–7 (15–25 pruebas cada uno y 7–12 soluciones con
fallos típicos que demuestran que cada error cae en la prueba pensada para él). Para añadir otro ejercicio: su generador en
`generar_tests_juez.py`, su entrada en `juez/juez.json` y volver a construir la web.

## Ejercicios con varias respuestas válidas
05-3, 05-6 y 07-3 aceptan cualquier orden topológico, asignación o camino mínimo correcto. Llevan un
comprobador propio en `juez/ejercicios/comprobadores/<id>.py` (servidor) y `<id>.js` (navegador),
que se copian a `juez/tests/<id>/`. El verificador comprueba que las dos versiones dicen lo mismo en
cientos de salidas y que se acepta una respuesta alternativa (función `ALTERNATIVA` del módulo).

## Plantilla del alumno
Sale de la solución: se vacía la zona `//@ <answer> … //@ </answer>` y el comentario con el
PLANTEAMIENTO se reduce al título (lo dan las pistas). Un ejercicio puede traer su propia plantilla
(`"plantilla"` en CONFIG): 01-2 da la clase `Set` sin `tami` ni `kesimo`, que es lo que se pide.

## En la web
Cada ejercicio con juez tiene la pestaña «Probar» (el juez se carga al abrirla). La página suelta
`juez/<id>.html` sigue existiendo.

## Verificar
`PYTHONUTF8=1 python3 juez/verificar.py [ids]`: genera las pruebas, revisa sus datos, exige AC de la
solución con margen para la Pi, que la demo falle, que cada variante caiga en su prueba según la guía
de la web (diagnostico.js) y, si hay comprobador, que Python y JavaScript coincidan.

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
