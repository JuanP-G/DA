# Juez para la web de DA: estudio de viabilidad

**Recomendación: WebAssembly en el navegador (clang 8 + lld, binji/wasm-clang).** Está probado de punta a punta con el 04-3.

| Opción | Pros | Contras / riesgos | Coste |
|---|---|---|---|
| a) WASM en el navegador | El código del alumno no sale de su equipo. Sin servidor, sin abuso posible. Funciona con el hosting estático actual. | Primera descarga de unos 60 MB (queda en caché). clang 8 / C++17. Sin `shared_ptr` (atomics), excepciones solo como aborto, tiempos orientativos. | 0 € |
| b) Función serverless en Vercel | Control total del veredicto. | Vercel no trae compilador y no puede ejecutar código no fiable sin sandbox. Habría que montar un contenedor externo, con vigilancia de abuso, tiempo y memoria. | Medio / alto |
| c) API externa (Piston / Judge0) | Rápido de montar. | Envía el código de los alumnos a un tercero. Piston público está cerrado. Judge0 es de pago, con límites y CORS. | De pago |
| d) Enlace a Acepta el Reto | Veredicto oficial, 44 ejercicios ya enlazados en `herramientas/acepta_el_reto.json`. | Hay que salir de la web y no cubre todos los ejercicios. Úsalo como complemento. | 0 € |

## Resultados
- Veredictos probados: Correcto, Respuesta incorrecta (primera línea distinta), Error de compilación, Tiempo excedido y Error de ejecución.
- Barrido de 62 soluciones de la asignatura: **47 compilan**. Los 14 fallos son `shared_ptr` (atomics no disponibles en wasm32). Otro más es `EJ_01-1 (generico)/bintree.h`, que en el repo es un HTML.

## Pruebas (casos de test)
- Formato: `juez/tests/<id>/N.in` y `N.out`, más `N.txt` con el nombre. El manifiesto sale de `juez/juez.json` y `construir.py`.
- Para 04-3 hay 5 grupos: los 2 ejemplos del enunciado, bordes, 30 aleatorios pequeños, tablero y rayas, y uno grande de 400x400. Los generó un solver independiente en Python (BFS, semillas fijas). Todos coinciden con la solución del repo.
- Comparación: se ignoran espacios al final de línea y líneas vacías finales.
- Hay 21 pares reales en `Acepta el Reto/pruebas` que se pueden reutilizar.

## Decisiones pendientes
1. Alojar los binarios WASM (~60 MB) o enlazar a binji.github.io (hoy se enlazan; se cambia con `JUEZ_WASM_BASE`).
2. Cómo conseguir pruebas para los ~60 ejercicios restantes (generadores propios, los 21 pares existentes, o solo enlace a ACR).
3. Tests ocultos o visibles. Hoy son visibles.
4. Dónde encajarlo en el diseño D (pestaña «Probar»).
