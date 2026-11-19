# Servidor del juez (Raspberry Pi, sin root)

Corre con un usuario normal. Necesita: `python3`, `g++`, `bwrap` (bubblewrap) y, opcionalmente,
`systemd-run --user` para limitar la memoria con cgroups.

## Instalar y probar en la Pi
    git clone -b claude/juez-da https://github.com/JuanP-G/DA.git ~/DA
    cd ~/DA/juez/servidor
    python3 servidor.py                 # en una terminal (escucha en 127.0.0.1:8099)
    python3 probar.py                   # en otra: 10 envíos de prueba

## Qué protege
- Caja de bubblewrap: sin red, `/usr` solo lectura, sin tus archivos, procesos aislados, `/tmp` vacío.
- Memoria 256 MB (1 GB al compilar), procesos máx. 48, CPU y tiempo limitados, ficheros ≤ 1 MB, salida ≤ 2 MB.
- Filtro previo de código (system, fork, exec, asm, includes con rutas...). Capa extra, no la principal.
- Cola: 2 ejecuciones a la vez, máx. 6 esperando; 1 envío cada 4 s por IP; código ≤ 64 KB.
- Sin `JUEZ_ORIGENES` acepta peticiones de cualquier web: fíjalo a tu dominio al publicarlo.

## Variables
`JUEZ_ORIGENES` (CORS, p. ej. `https://studia-one-flax.vercel.app`), `JUEZ_PUERTO`, `JUEZ_HOST`,
`JUEZ_SIMULTANEOS`, `JUEZ_CGROUP=0` (sin systemd-run), `JUEZ_CONFIAR_CF=1` (IP real tras Cloudflare),
`JUEZ_SIN_CAJA=1` (SOLO para probar en tu PC con tu propio código).

## Conectar la web
Al construir la web: `JUEZ_SERVIDOR=https://tu-url python sitio/construir.py`. Si el servidor no responde,
la página usa el compilador del navegador (WebAssembly) como respaldo.
