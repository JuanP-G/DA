# Generador de los vídeos de los temas 4, 5, 6 y 7

Cada `v04_X.py` es el guion de un vídeo: una lista de diapositivas, cada una con su frase de narración. Las trazas de ejecución salen de **simular el mismo algoritmo del `.cpp`** (mismo orden de adyacentes que `Grafo.h`). El código que aparece en pantalla se lee del `.cpp` real, con sus números de línea.

`vidlib.py` dibuja las diapositivas (Pillow), genera la voz (Kokoro, offline; o Piper, la voz antigua) y monta el vídeo con ffmpeg: H.264 + audio AAC + pista de subtítulos en castellano.

## Voz

Desde el vídeo 05-0 se usa **Kokoro** (`pip install kokoro-onnx`), mucho más natural que la voz Piper `es-mls_10246-low` de los vídeos anteriores. Modelos: `kokoro-v1.0.onnx` y `voices-v1.0.bin` de las [releases de kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0).

```bash
export KOKORO_MODEL=/ruta/kokoro-v1.0.onnx KOKORO_VOICES=/ruta/voices-v1.0.bin
export KOKORO_VOICE=ef_dora      # o em_alex (masculina)
```

Sin `KOKORO_MODEL` se usa Piper (`PIPER_MODEL`), como antes.

## Requisitos

- Python 3 con `pillow` y `piper-tts` (`pip install pillow piper-tts`)
- `ffmpeg`
- Una voz de Piper en castellano, por ejemplo `es-mls_10246-low` ([releases de Piper](https://github.com/rhasspy/piper/releases/tag/v0.0.2), fichero `voice-es-mls_10246-low.tar.gz`)

## Uso

```bash
cd Videos/generador
export PIPER_MODEL=/ruta/a/es-mls_10246-low.onnx
python v04_1.py --preview   # solo las imágenes, en preview/ (para revisar el diseño)
python v04_1.py             # genera ../04-1_arboles_libres.mp4
```

## Vídeo de teoría del tema 5

`v05_teoria.py` genera `../05-0_grafos_dirigidos_teoria.mp4` (≈ 23 min, con capítulos y subtítulos): conceptos de grafos dirigidos, TAD `Digrafo`, DFS, BFS, la máquina calculadora (grafo implícito), el grafo de autobuses de la EMT, orden topológico, detección de ciclos y, como extra, componentes fuertemente conexas.

- El código que sale en pantalla se lee de `Estructuras de datos/Digrafo_algoritmos.h` (y `Digrafo.h`, `Digrafo_implicito_calculadora.cpp`); `Digrafo_demo.cpp` comprueba que las trazas simuladas coinciden con la ejecución real.
- `material/emt_ejemplo.cpp` es el ejemplo de `grafoEMT.zip`; `material/emt_resultado.txt` guarda lo que imprime (BFS: 6 paradas; DFS: 2.032).
- `build()` de `vidlib.py` admite ahora `chapters={índice de diapositiva: título}`.

```bash
export PIPER_MODEL=/ruta/a/es-mls_10246-low.onnx
python v05_teoria.py --preview   # solo las imágenes
python v05_teoria.py             # genera el mp4 (tarda unos minutos)
```


## Vídeo de teoría del tema 6

`v06_1.py` … `v06_5.py` generan los vídeos de los ejercicios 06-1 a 06-5 (`../06-1_petroleros_hundidos.mp4`, `../06-2_camiones_de_reparto.mp4`, `../06-3_archipielago_en_bicicleta.mp4`, `../06-4_selva_de_tarzan.mp4`, `../06-5_minas_de_trajano.mp4`): conjuntos disjuntos sobre la rejilla, DFS con filtro `valor >= ancho` y los tres Kruskal (suma, última arista, parar al unir origen y destino), con la traza de los ejemplos del README de cada ejercicio. Los tres últimos comparten las piezas de `v06e_comun.py` (simulador de Kruskal con parada, dibujo del grafo coloreado por grupos y diapositiva paso a paso).

`v06_L.py` genera `../06-L_aeropuertos.mp4` (¿Dónde construimos los aeropuertos?: Kruskal con C < A, el empate C = A y la traza de los ejemplos 1 y 3; la simulación repite el algoritmo del `.cpp`).

`v06_teoria.py` genera `../06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4` (con capítulos y subtítulos): relaciones de equivalencia dinámicas, búsqueda rápida, unión rápida, unión por tamaños y compresión de caminos, la autoevaluación 6.1 paso a paso, los ejercicios 06-1 a 06-5, `GrafoValorado.h`, la propiedad del corte, y Kruskal y Prim sobre un grafo de 6 vértices.

- Cuando se hizo el vídeo los ejercicios del tema 6 aún no tenían `.cpp`, así que las trazas salen de **simular los algoritmos en el propio guion** (los resultados coinciden con los ejemplos de los enunciados). El código que se ve en pantalla es el de `Estructuras de datos/ConjuntosDisjuntos.h` y `GrafoValorado.h`.
- Para unión por tamaños se sigue el criterio de desempate de las transparencias (en empate, la raíz de `b` cuelga de la de `a`); la cabecera hace lo contrario y el vídeo lo advierte.

```bash
export KOKORO_MODEL=/ruta/kokoro-v1.0.onnx KOKORO_VOICES=/ruta/voices-v1.0.bin KOKORO_VOICE=ef_dora
python v06_teoria.py --preview   # solo las imágenes
python v06_teoria.py             # genera el mp4 (varios minutos: sintetiza la voz de cada diapositiva)
```


## Vídeos del tema 7

- `v07_teoria.py` genera `../07-0_digrafos_valorados_caminos_minimos_teoria.mp4` (con capítulos y subtítulos): `AristaDirigida`/`DigrafoValorado`, caminos mínimos (`dist`, `ulti`, árbol), relajación, condiciones de optimalidad, **Dijkstra paso a paso** sobre el dígrafo de las transparencias (25 pasos), su código, corrección y coste O(A log V), recuperación del camino, Dijkstra con vector O(V² + A), caminos mínimos vs ARM (el triángulo) y un resumen de 07-1 … 07-3.
- `v07_1.py`, `v07_2.py` y `v07_3.py` generan los vídeos de los ejercicios (`../07-1_navegando_sin_teclado.mp4`, `../07-2_camino_al_cole.mp4`, `../07-3_rapideats.mp4`).
- `v07_4.py` … `v07_7.py` generan los de 07-4 a 07-7 (`../07-4_conferencia_de_paz.mp4`, `../07-5_mejor_camino.mp4`, `../07-6_repartiendo_paquetes.mp4`, `../07-7_ratones_laberinto.mp4`) con las piezas comunes de `v07b_comun.py` (Dijkstra con traza: varios orígenes, prioridad `(distancia, calles)`, grafo inverso y corte por tiempo).
- `v07_comun.py` contiene el simulador de Dijkstra (`traza`, con el mismo criterio que el código), el dibujo de dígrafos y la tabla `dist/ulti`, compartidos por los cuatro guiones.

```bash
export KOKORO_MODEL=/ruta/kokoro-v1.0.onnx KOKORO_VOICES=/ruta/voices-v1.0.bin KOKORO_VOICE=ef_dora
python v07_teoria.py --preview   # solo las imágenes (carpeta preview/)
python v07_teoria.py             # genera el mp4
```


## Vídeos de ejercicios del tema 5

`v05_1.py`, `v05_2.py`, `v05_3.py`, `v05_4.py` (sumidero), `v05_5.py` (serpientes y escaleras, con el BFS sobre el tablero), `v05_6.py` y `v05_L.py` (El Necronomicón: programa → digrafo y un DFS desde la instrucción 1). Las trazas salen de repetir el mismo algoritmo que el `.cpp`, y el código en pantalla se lee del fichero real.
