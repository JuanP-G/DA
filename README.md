# DA · Diseño de Algoritmos (UCM)

Ejercicios del juez de **Diseño de Algoritmos** resueltos en C++, cada uno con su enunciado y, según el ejercicio, una explicación del planteamiento y un vídeo paso a paso. Además, herramientas interactivas para entender cada estructura de datos.

> 🌐 **Web con todo reunido y buscador: <https://juanp-g.github.io/DA/>** (se actualiza sola con cada cambio en `main`).

| Tema | Estructura | Ejercicios | Vídeos | Herramienta interactiva |
|---|---|:--:|:--:|---|
| [1 · Árboles AVL](#tema-1--árboles-avl) | `Set<T>` (AVL), `BinTree<T>` | 3 | — | [`tema1-avl.html`](Visualizaciones/tema1-avl.html) |
| [2 · Colas de prioridad](#tema-2--colas-de-prioridad) | `priority_queue`, montículo | 7 | — | [`tema2-cola-prioridad.html`](Visualizaciones/tema2-cola-prioridad.html) |
| [3 · Colas de prioridad variable](#tema-3--colas-de-prioridad-variable-indexpq) | `IndexPQ` | 6 | 3 | [`tema3-indexpq.html`](Visualizaciones/tema3-indexpq.html) |
| [4 · Grafos no dirigidos](#tema-4--grafos-no-dirigidos) | `Grafo` | 8 | 8 | [`tema4-grafo.html`](Visualizaciones/tema4-grafo.html) |
| [5 · Grafos dirigidos](#tema-5--grafos-dirigidos) | `Digrafo` | 6 + teoría | 5 | [`tema5-digrafo.html`](Visualizaciones/tema5-digrafo.html) |

**Más abajo:** [Visualizaciones](#visualizaciones-interactivas) · [Estructuras de datos](#estructuras-de-datos) · [Vídeos](#vídeos) · [Organización](#organización-del-repositorio) · [Añadir un ejercicio](#añadir-un-ejercicio-nuevo) · [Compilar](#compilar-y-probar) · [Web](#web-del-repositorio)

---

## Tema 1 · Árboles AVL

Carpeta [`1-Arboles AVL/`](1-Arboles%20AVL).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 01-1 | ¿Es un árbol AVL? (enteros) | [📄 PDF](1-Arboles%20AVL/Enunciados/prob-%C2%BFEs%20un%20%C3%A1rbol%20AVL_.pdf) | [💻 Solución](1-Arboles%20AVL/EJ_01-1/EJ%2001-1.cpp) · [📘 Explicación](1-Arboles%20AVL/EJ_01-1/README.md) | — | Postorden: altura, mínimo y máximo de cada subárbol |
| 01-1 | ¿Es un árbol AVL? (genérico) | [📄 PDF](1-Arboles%20AVL/Enunciados/prob-%C2%BFEs%20un%20%C3%A1rbol%20AVL_%20%281%29.pdf) | [💻 Versión 1](1-Arboles%20AVL/EJ_01-1%20%28generico%20v1%29/EJ%2001-1%20%28GENERICO%29.cpp) · [💻 Versión final](1-Arboles%20AVL/EJ_01-1%20%28generico%29/EJ%2001-1%20%28GENERICO%20BIEN%29.cpp) · [📘 Explicación](1-Arboles%20AVL/EJ_01-1%20%28generico%29/README.md) | — | Lo mismo con `template <class T>` y `BinTree<T>` |
| 01-2 | Encontrar el k-ésimo elemento en un árbol AVL | [📄 PDF](1-Arboles%20AVL/Enunciados/prob-Encontrar%20el%20k-%C3%A9simo%20elemento%20en%20un%20%C3%A1rbol%20AVL.pdf) | [💻 Solución](1-Arboles%20AVL/EJ_01-2/EJ%2001-2.cpp) · [📘 Explicación](1-Arboles%20AVL/EJ_01-2/README.md) | — | `Set` AVL con tamaño de subárbol → `kesimo` |

## Tema 2 · Colas de prioridad

Carpeta [`2-Colas de prioridad/`](2-Colas%20de%20prioridad).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 02-1 | Lo que cuesta sumar | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Lo%20que%20cuesta%20sumar.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-1/EJ_02-1.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-1/README.md) | — | Cola de mínimos: sumar siempre los dos menores |
| 02-2 | Unidad Curiosa de Monitorización | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Unidad%20Curiosa%20de%20Monitorizaci%C3%B3n.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-2/EJ_02-2.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-2/README.md) | — | Cola de mínimos de próximos envíos (instante, id) |
| 02-3 | Reina del súper | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Reina%20del%20s%C3%BAper.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-3/EJ_02-3.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-3/README.md) | — | Cola de mínimos de cajas (instante libre, nº de caja) |
| 02-4 | La ley D'Hondt | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-La%20ley%20D%27Hondt.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-4/EJ_02-4.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-4/README.md) | — | Cola de máximos de cocientes votos / (1 + escaños) |
| 02-5 | Ordenando a los pacientes en urgencias | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Ordenando%20a%20los%20pacientes%20en%20urgencias.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-5/EJ_02-5.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-5/README.md) | — | Cola de máximos (gravedad, orden de llegada) |
| 02-6 | Coleccionando cómics | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Coleccionando%20c%C3%B3mics.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-6/EJ_02-6.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-6/README.md) | — | Cola de mínimos de cimas de pila + `Pila.h` |
| 02-L | Cinemáticas digitales | [📄 PDF](2-Colas%20de%20prioridad/Enunciados/prob-Cinem%C3%A1ticas%20digitales.pdf) | [💻 Solución](2-Colas%20de%20prioridad/EJ_02-L/EJ_02-L.cpp) · [📘 Explicación](2-Colas%20de%20prioridad/EJ_02-L/README.md) | — | Cola de mínimos de estaciones de renderizado |

## Tema 3 · Colas de prioridad variable (IndexPQ)

Carpeta [`3-Colas de prioridad variable (Heapsort)/`](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29). Usan [`IndexPQ.h`](Estructuras%20de%20datos/IndexPQ.h).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 03-1 | Volando drones | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-Volando%20drones.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-1/EJ_03-1.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-1/README.md) | — | Dos colas de máximos de pilas (9V y 1,5V) |
| 03-2 | 12 points go to… | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-12%20points%20go%20to%E2%80%A6.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-2/EJ_03-2.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-2/README.md) | — | `IndexPQ` de países con `update` de puntos |
| 03-3 | Multitarea | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-Multitarea.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-3/EJ_03-3.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-3/README.md) | — | `IndexPQ` de intervalos (tareas únicas y periódicas) |
| 03-4 | Pájaros en vuelo | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-P%C3%A1jaros%20en%20vuelo.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-4/EJ_03-4.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-4/README.md) | [🎬 Vídeo](Videos/03-4_pajaros_en_vuelo.mp4) | Mediana con dos montículos (máximos · mínimos) |
| 03-5 | Tridente de temas candentes | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-Tridente%20de%20temas%20candentes.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-5/EJ_03-5.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-5/README.md) | [🎬 Vídeo](Videos/03-5_tridente_temas_candentes.mp4) | `IndexPQ` de temas (citas, último C) |
| 03-L | La batalla por las audiencias | [📄 PDF](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/Enunciados/prob-La%20batalla%20por%20las%20audiencias.pdf) | [💻 Solución](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-L/EJ_03-L.cpp) · [📘 Explicación](3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/EJ_03-L/README.md) | [🎬 Vídeo](Videos/03-L_batalla_audiencias.mp4) | `IndexPQ` de canales; el líder acumula minutos |

## Tema 4 · Grafos no dirigidos

Carpeta [`4-Grafos no dirigidos/`](4-Grafos%20no%20dirigidos). Todos usan [`Grafo.h`](Estructuras%20de%20datos/Grafo.h) y están numerados como en el juez. Los algoritmos del tema (DFS, BFS, componentes, bipartito, ciclos) están juntos en [`Grafo_algoritmos.h`](Estructuras%20de%20datos/Grafo_algoritmos.h).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 04-1 | Árboles libres | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-%C3%81rboles%20libres.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-1/EJ_04-1.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-1/README.md) | [🎬 Vídeo](Videos/04-1_arboles_libres.mp4) | DFS: conexo y A = V − 1 |
| 04-2 | Los amigos de mis amigos son mis amigos | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Los%20amigos%20de%20mis%20amigos%20son%20mis%20amigos.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-2/EJ_04-2.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-2/README.md) | [🎬 Vídeo](Videos/04-2_amigos_de_mis_amigos.mp4) | DFS: componente conexa más grande |
| 04-3 | Detección de manchas negras | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Detecci%C3%B3n%20de%20manchas%20negras.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-3/EJ_04-3.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-3/README.md) | [🎬 Vídeo](Videos/04-3_manchas_negras.mp4) | Píxel → vértice i·C + j; DFS: número de componentes y la mayor |
| 04-4 | Los números de Bacon | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Los%20n%C3%BAmeros%20de%20Bacon.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-4/EJ_04-4.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-4/README.md) | [🎬 Vídeo](Videos/04-4_numeros_de_bacon.mp4) | BFS en grafo actor–película; Bacon = dist / 2 |
| 04-5 | ¡Las noticias vuelan! | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-%C2%A1Las%20noticias%20vuelan%21.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-5/EJ_04-5.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-5/README.md) | [🎬 Vídeo](Videos/04-5_las_noticias_vuelan.mp4) | Aristas en estrella + tamaño de componentes con BFS |
| 04-6 | Un nodo muy muy lejano | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Un%20nodo%20muy%20muy%20lejano.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-6/EJ_04-6.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-6/README.md) | [🎬 Vídeo](Videos/04-6_nodo_muy_lejano.mp4) | BFS con distancias, cortado en el TTL |
| 04-7 | Grafo bipartito | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Grafo%20bipartito.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-7/EJ_04-7.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-7/README.md) | [🎬 Vídeo](Videos/04-7_grafo_bipartito.mp4) | DFS coloreando con 2 colores |
| 04-L | Peaje a la sombra | [📄 PDF](4-Grafos%20no%20dirigidos/Enunciados/prob-Peaje%20a%20la%20sombra.pdf) | [💻 Solución](4-Grafos%20no%20dirigidos/EJ_04-L/EJ_04-L.cpp) · [📘 Explicación](4-Grafos%20no%20dirigidos/EJ_04-L/README.md) | [🎬 Vídeo](Videos/04-L_peaje_a_la_sombra.mp4) | 3 BFS (Álex, Lucas, trabajo) y mínimo de dA+dL+dT |

**Qué recorrido usar**

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| ¿A qué vértices se llega? ¿Es conexo? Número y tamaño de las componentes | DFS (o BFS: el orden da igual) | 04-1, 04-2, 04-3, 04-5 |
| Una asignación que *obliga* a los vecinos (2 colores) | DFS propagando la restricción | 04-7 |
| Distancia **mínima** en número de aristas | **BFS** (un DFS puede llegar por un camino largo) | 04-4, 04-6, 04-L |
| Camino compartido por dos personas hasta un destino (forma de **Y**) | BFS desde los 3 puntos y mínimo de la suma de distancias | 04-L |
| Grupos con muchos miembros | No unir todos con todos: en estrella si solo importa la conexión, o con un vértice por grupo si importan las distancias | 04-5, 04-4 |

## Tema 5 · Grafos dirigidos

Carpeta [`5-Grafos dirigidos/`](5-Grafos%20dirigidos). Todos usan [`Digrafo.h`](Estructuras%20de%20datos/Digrafo.h); los algoritmos del tema están juntos en [`Digrafo_algoritmos.h`](Estructuras%20de%20datos/Digrafo_algoritmos.h). La fila 05-0 es la **explicación general del tema** (vídeo de 23 min con capítulos).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 05-0 | Teoría del tema (explicación general) | — | [💻 Algoritmos](Estructuras%20de%20datos/Digrafo_algoritmos.h) · [🧪 Demo](Estructuras%20de%20datos/Digrafo_demo.cpp) | [🎬 Vídeo](Videos/05-0_grafos_dirigidos_teoria.mp4) | Digrafo, DFS, BFS, calculadora (grafo implícito), autobuses de la EMT, orden topológico, ciclos y componentes fuertemente conexas (extra) |
| 05-1 | Juego de Transformación Modular | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Juego%20de%20Transformaci%C3%B3n%20Modular.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-1/EJ_05-1.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-1/README.md) | [🎬 Vídeo](Videos/05-1_transformacion_modular.mp4) | BFS en un `Digrafo` construido con x → (a·x+b) mod M |
| 05-2 | La máquina calculadora | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-La%20m%C3%A1quina%20calculadora.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-2/EJ_05-2.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-2/README.md) | [🎬 Vídeo](Videos/05-2_maquina_calculadora.mp4) | BFS en un `Digrafo` con los 10.000 números del marcador (+1, ×2, ÷3) |
| 05-3 | Ordenando tareas | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Ordenando%20tareas.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-3/EJ_05-3.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-3/README.md) | [🎬 Vídeo](Videos/05-3_ordenando_tareas.mp4) | Orden topológico: postorden inverso del DFS (+ ciclos) |
| 05-4 | Sumidero en un grafo dirigido | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Sumidero%20en%20un%20grafo%20dirigido.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-4/EJ_05-4.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-4/README.md) | — | Grados: salida 0 (`ady(v)` vacío) y entrada V − 1 (contando en las listas) |
| 05-5 | Haciendo trampas en Serpientes y Escaleras | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Haciendo%20trampas%20en%20Serpientes%20y%20Escaleras.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-5/EJ_05-5.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-5/README.md) | — | BFS: casilla v → destino(v + d), d = 1…K; serpiente/escalera = salto obligatorio |
| 05-6 | Sistema de inecuaciones | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Sistema%20de%20inecuaciones.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-6/EJ_05-6.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-6/README.md) | [🎬 Vídeo](Videos/05-6_sistema_inecuaciones.mp4) | xi < xj = arista i → j; ciclo ⇒ NO; si no, valor = posición en el orden topológico |

**Qué algoritmo usar**

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| Mínimo número de pasos / jugadas / tiradas | **BFS** (camino con menos aristas) | 05-1, 05-2, 05-5 |
| Estados con reglas de movimiento (el grafo sale de una fórmula) | Construir el `Digrafo` con `ponArista`, o grafo **implícito** con los sucesores al vuelo | 05-1, 05-2, 05-5 |
| Ordenar con precedencias («A antes que B», xi < xj) | **Orden topológico**: postorden inverso del DFS; vecino en la pila ⇒ ciclo ⇒ imposible | 05-3, 05-6 |
| Grados de los vértices (p. ej. sumidero) | Salida = `ady(v).size()`; entrada = contar en todas las listas | 05-4 |
| La entrada es «V, A y A pares» | Leer con el constructor `Digrafo g(cin, primer)` | 05-4, 05-6 |

---

## Visualizaciones interactivas

Una página HTML por estructura, en [`Visualizaciones/`](Visualizaciones). Ejecutan la misma lógica que el C++ de la asignatura, muestran el código real con la línea activa resaltada y dejan construir ejemplos propios y avanzar o retroceder paso a paso (flechas del teclado).

| Página | Estructura | Qué se puede hacer |
|---|---|---|
| [`tema1-avl.html`](Visualizaciones/tema1-avl.html) | `Set<T>` (AVL) | insertar, borrar, `borraMin`, `kesimo`; factor de equilibrio y las 4 rotaciones |
| [`tema2-cola-prioridad.html`](Visualizaciones/tema2-cola-prioridad.html) | montículo binario | `push` (flotar), `pop` (hundir), heapify en O(n), mínimos/máximos |
| [`tema3-indexpq.html`](Visualizaciones/tema3-indexpq.html) | `IndexPQ` | `push`, `update`, `pop` con la tabla `posiciones` |
| [`tema4-grafo.html`](Visualizaciones/tema4-grafo.html) | `Grafo` | construir el grafo, listas de adyacencia, DFS (componentes), BFS, bipartito |
| [`tema5-digrafo.html`](Visualizaciones/tema5-digrafo.html) | `Digrafo` | construir el digrafo, BFS, orden topológico con ciclos, `inverso()` |

Se pueden usar desde la [web](https://juanp-g.github.io/DA/#herramientas) o descargando la carpeta y abriendo `index.html`. Se generan con `python3 Visualizaciones/_fuente/gen_grafos.py && python3 Visualizaciones/_fuente/build.py`.

## Estructuras de datos

Las cabeceras de la asignatura están en [`Estructuras de datos/`](Estructuras%20de%20datos). Cada ejercicio lleva su propia copia junto al `.cpp` para compilar sin rutas extra.

| Fichero | Qué es | Se usa en |
|---|---|---|
| [`bintree.h`](Estructuras%20de%20datos/bintree.h) | Árbol binario `BinTree<T>` | 01-1 genérico, 01-2 |
| [`TreeSet_AVL_plantilla.h`](Estructuras%20de%20datos/TreeSet_AVL_plantilla.h) | Conjunto sobre árbol AVL (`Set<T>`), con `kesimo` | 01-2 |
| [`Pila.h`](Estructuras%20de%20datos/Pila.h) | Pila `Pila<T>` | 02-6 |
| [`IndexPQ.h`](Estructuras%20de%20datos/IndexPQ.h) | Cola de prioridad con índices (`push`, `update`, `top`, `pop`, `priority`) | Tema 3 |
| [`Grafo.h`](Estructuras%20de%20datos/Grafo.h) | Grafo no dirigido con listas de adyacencia (`V()`, `A()`, `ady(v)`, `ponArista`) | Tema 4 |
| [`Grafo_algoritmos.h`](Estructuras%20de%20datos/Grafo_algoritmos.h) | Algoritmos del tema 4 juntos: `CaminosDFS`, `CaminosBFS`, `ComponentesConexas`, `Bipartito`, `CicloGrafo` (extra) y `esArbolLibre` | Tema 4 |
| [`Grafo_demo.cpp`](Estructuras%20de%20datos/Grafo_demo.cpp) | Ejecuta esos algoritmos sobre un grafo de ejemplo de 13 vértices y 3 componentes | Tema 4 |
| [`Digrafo.h`](Estructuras%20de%20datos/Digrafo.h) | Grafo dirigido con la misma interfaz (+ `hayArista`, `inverso()`, constructor desde `cin`) | Tema 5 |
| [`Digrafo_algoritmos.h`](Estructuras%20de%20datos/Digrafo_algoritmos.h) | Algoritmos del tema 5 juntos: `DFSDirigido`, `BFSDirigido`, `OrdenTopologico`, `CicloDirigido` y `CFC` (componentes fuertemente conexas, extra) | Vídeo 05-0 |
| [`Digrafo_demo.cpp`](Estructuras%20de%20datos/Digrafo_demo.cpp) | Ejecuta esos algoritmos sobre los grafos de las transparencias | Vídeo 05-0 |
| [`Digrafo_implicito_calculadora.cpp`](Estructuras%20de%20datos/Digrafo_implicito_calculadora.cpp) | La máquina calculadora como **grafo implícito** (transparencias 13) | Vídeo 05-0 |

## Vídeos

Todos en [`Videos/`](Videos), con subtítulos en castellano (y capítulos el de teoría). Enlazados también en la columna «Vídeo» de cada tema.

| Vídeo | Contenido |
|---|---|
| [`05-0_grafos_dirigidos_teoria.mp4`](Videos/05-0_grafos_dirigidos_teoria.mp4) | **Teoría completa del tema 5** (23 min, 10 capítulos) |
| `03-4`, `03-5`, `03-L` | Ejercicios del tema 3 |
| `04-1` … `04-7`, `04-L` | Ejercicios del tema 4 |
| `05-1`, `05-2`, `05-3`, `05-6` | Ejercicios del tema 5 |

Se generan con los scripts de [`Videos/generador/`](Videos/generador) (diapositivas con Pillow, voz Kokoro y ffmpeg); las trazas salen del mismo algoritmo que el `.cpp` y el código en pantalla se lee del fichero real.

---

## Organización del repositorio

Las carpetas de cada tema coinciden con las carpetas de la solución de Visual Studio:

```text
.
├── 1-Arboles AVL/
├── 2-Colas de prioridad/
├── 3-Colas de prioridad variable (Heapsort)/
├── 4-Grafos no dirigidos/
├── 5-Grafos dirigidos/
│   ├── Enunciados/              PDFs del juez de este tema
│   ├── EJ_05-1/                 un proyecto de VS por ejercicio
│   │   ├── EJ_05-1.cpp
│   │   ├── Digrafo.h            copia de la cabecera que usa
│   │   └── README.md            explicación: qué piden, planteamiento, traza y coste
│   └── …
├── Estructuras de datos/        cabeceras de la asignatura (+ algoritmos de los temas 4 y 5)
├── Videos/                      vídeos explicativos
│   └── generador/               scripts que los generan
├── Visualizaciones/             herramientas interactivas (abre index.html)
├── sitio/                       generador de la web
└── herramientas/                script para recolocar los proyectos de VS tras la reorganización
```

## Añadir un ejercicio nuevo

1. En VS: clic derecho en la carpeta del tema de la solución → *Agregar → Nuevo proyecto*, con **Ubicación** `…\DA\<tema>\` (por ejemplo `…\DA\5-Grafos dirigidos\`) y nombre `EJ_0T-N`.
2. El PDF del enunciado, en `<tema>/Enunciados/`.
3. Una fila en la tabla del tema de este README (si no, la web lo añade igualmente al detectar la carpeta, pero sin título).
4. Commit y push: la web se actualiza sola.

## Compilar y probar

```bash
g++ -std=c++17 -O2 -Wall -o sol "5-Grafos dirigidos/EJ_05-6/EJ_05-6.cpp"
./sol < entrada.txt
```

Las soluciones de los temas 4 y 5 están probadas con los ejemplos de los enunciados, contra soluciones de fuerza bruta en cientos o miles de casos aleatorios y con entradas en el máximo de los límites.

> ⚠️ Los DFS recursivos pueden bajar tantos niveles como vértices haya. En el juez no da problemas, pero en Visual Studio (pila de 1 MB) un caso enorme podría desbordar la pila. Por eso el 04-5 usa un BFS iterativo; en el 04-3 el enunciado limita las manchas a 50.000 píxeles justo para que el DFS recursivo sea seguro.

## Web del repositorio

**🌐 <https://juanp-g.github.io/DA/>**

Reúne enunciados, soluciones, explicaciones, vídeos y herramientas en una web estática generada desde este repositorio con [`sitio/construir.py`](sitio/construir.py) y el workflow [`.github/workflows/web.yml`](.github/workflows/web.yml) cada vez que cambia `main`. En local:

```bash
pip install markdown
python3 sitio/construir.py                      # genera sitio/_site/
python3 -m http.server -d sitio/_site 8000
```
