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
| [6 · Conjuntos disjuntos y grafos valorados](#tema-6--conjuntos-disjuntos-y-grafos-valorados) | `ConjuntosDisjuntos`, `GrafoValorado` | 5 + teoría | 1 | [`tema6-kruskal.html`](Visualizaciones/tema6-kruskal.html) |
| [7 · Dígrafos valorados y caminos mínimos](#tema-7--dígrafos-valorados-y-caminos-mínimos) | `DigrafoValorado`, Dijkstra | 3 + teoría | 4 | [`tema7-dijkstra.html`](Visualizaciones/tema7-dijkstra.html) |

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
| 05-1 | La máquina calculadora | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-La%20m%C3%A1quina%20calculadora.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-1/EJ_05-1.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-1/README.md) | [🎬 Vídeo](Videos/05-1_maquina_calculadora.mp4) | BFS en un `Digrafo` con los 10.000 números del marcador (+1, ×2, ÷3) |
| 05-2 | Juego de Transformación Modular | [📄 PDF](5-Grafos%20dirigidos/Enunciados/prob-Juego%20de%20Transformaci%C3%B3n%20Modular.pdf) | [💻 Solución](5-Grafos%20dirigidos/EJ_05-2/EJ_05-2.cpp) · [📘 Explicación](5-Grafos%20dirigidos/EJ_05-2/README.md) | [🎬 Vídeo](Videos/05-2_transformacion_modular.mp4) | BFS en un `Digrafo` construido con x → (a·x+b) mod M |
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

## Tema 6 · Conjuntos disjuntos y grafos valorados

Carpeta [`6-Conjuntos disjuntos y grafos valorados/`](6-Conjuntos%20disjuntos%20y%20grafos%20valorados). Usan [`ConjuntosDisjuntos.h`](Estructuras%20de%20datos/ConjuntosDisjuntos.h) y [`GrafoValorado.h`](Estructuras%20de%20datos/GrafoValorado.h). La fila 06-0 es el **resumen del tema** (con la respuesta a la autoevaluación 6.1).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 06-0 | Teoría del tema (explicación general) | — | [📘 Explicación del tema (resumen y autoevaluación)](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/README.md) | [🎬 Vídeo](Videos/06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4) | Conjuntos disjuntos (búsqueda rápida, unión rápida, por tamaños, compresión), grafos valorados, propiedad del corte, Kruskal y Prim |
| 06-1 | Petroleros hundidos | [📄 PDF](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/Enunciados/prob-Petroleros%20hundidos.pdf) | [💻 Solución](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-1/EJ_06-1.cpp) · [📘 Explicación](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-1/README.md) | — | Conjuntos disjuntos sobre las celdas (8 vecinos): `unir` al añadir petróleo y `cardinal` para el máximo |
| 06-2 | Camiones de reparto | [📄 PDF](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/Enunciados/prob-Camiones%20de%20reparto.pdf) | [💻 Solución](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-2/EJ_06-2.cpp) · [📘 Explicación](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-2/README.md) | — | `GrafoValorado` + DFS por consulta que solo cruza aristas con valor ≥ anchura |
| 06-3 | Recorriendo el archipiélago en bicicleta | [📄 PDF](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/Enunciados/prob-Recorriendo%20el%20archipi%C3%A9lago%20en%20bicicleta.pdf) | [💻 Solución](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-3/EJ_06-3.cpp) · [📘 Explicación](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-3/README.md) | — | Kruskal: suma del árbol de recubrimiento de coste mínimo (o «No hay puentes suficientes») |
| 06-4 | La selva de Tarzán | [📄 PDF](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/Enunciados/prob-La%20selva%20de%20Tarz%C3%A1n.pdf) | [💻 Solución](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-4/EJ_06-4.cpp) · [📘 Explicación](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-4/README.md) | — | Kruskal: la última arista aceptada (máximo del ARM) es la cuerda mínima |
| 06-5 | Las minas del emperador Trajano | [📄 PDF](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/Enunciados/prob-Las%20minas%20del%20emperador%20Trajano.pdf) | [💻 Solución](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-5/EJ_06-5.cpp) · [📘 Explicación](6-Conjuntos%20disjuntos%20y%20grafos%20valorados/EJ_06-5/README.md) | — | Kruskal hasta que `origen` y `destino` quedan unidos: esa arista es el camino minimax |

**Qué técnica usar**

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| Una relación que solo se va **juntando** y hay que saber tamaños de grupos o si dos están juntos | **Conjuntos disjuntos** (`unir`, `unidos`, `cardinal`) | 06-1 |
| Alcanzabilidad solo por aristas que cumplen una condición | DFS/BFS que **filtra** por `a.valor()` | 06-2 |
| Conectarlo todo al menor coste total | **Kruskal** (ordenar aristas + conjuntos disjuntos para evitar ciclos) o Prim; suma de valores | 06-3 |
| El mayor «salto» mínimo necesario para conectar todo | Kruskal: valor de la **última** arista aceptada | 06-4 |
| Mejor camino entre **dos** vértices cuando cuenta la arista más mala (no la suma) | Kruskal con parada en cuanto `origen` y `destino` están unidos | 06-5 |

---

## Tema 7 · Dígrafos valorados y caminos mínimos

Carpeta [`7-Digrafos valorados y caminos minimos/`](7-Digrafos%20valorados%20y%20caminos%20minimos). Usan [`DigrafoValorado.h`](Estructuras%20de%20datos/DigrafoValorado.h) e [`IndexPQ.h`](Estructuras%20de%20datos/IndexPQ.h); el Dijkstra de las transparencias (y la variante con vector) está en [`DigrafoValorado_algoritmos.h`](Estructuras%20de%20datos/DigrafoValorado_algoritmos.h). La fila 07-0 es el **resumen del tema** (con la respuesta a las reflexiones «Caminos mínimos vs ARM» y «Dijkstra con vector»).

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 07-0 | Teoría del tema (explicación general) | — | [📘 Explicación del tema (resumen y reflexiones)](7-Digrafos%20valorados%20y%20caminos%20minimos/README.md) · [💻 Algoritmos](Estructuras%20de%20datos/DigrafoValorado_algoritmos.h) · [🧪 Demo](Estructuras%20de%20datos/DigrafoValorado_demo.cpp) | [🎬 Vídeo](Videos/07-0_digrafos_valorados_caminos_minimos_teoria.mp4) | Dígrafos valorados, relajación, condiciones de optimalidad, Dijkstra (con montículo y con vector), ARM vs caminos mínimos |
| 07-1 | Navegando sin teclado | [📄 PDF](7-Digrafos%20valorados%20y%20caminos%20minimos/Enunciados/prob-Navegando%20sin%20teclado.pdf) | [💻 Solución](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-1/EJ_07-1.cpp) · [📘 Explicación](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-1/README.md) | [🎬 Vídeo](Videos/07-1_navegando_sin_teclado.mp4) | Dijkstra con coste en vértices y aristas: la carga de la página se suma a la arista que entra |
| 07-2 | Camino al cole | [📄 PDF](7-Digrafos%20valorados%20y%20caminos%20minimos/Enunciados/prob-Camino%20al%20cole.pdf) | [💻 Solución](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-2/EJ_07-2.cpp) · [📘 Explicación](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-2/README.md) | [🎬 Vídeo](Videos/07-2_camino_al_cole.mp4) | Dijkstra que cuenta caminos mínimos: sustituir si mejora, sumar si empata |
| 07-3 | RapidEats con ruta | [📄 PDF](7-Digrafos%20valorados%20y%20caminos%20minimos/Enunciados/prob-RapidEats.pdf) | [💻 Solución](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-3/EJ_07-3.cpp) · [📘 Explicación](7-Digrafos%20valorados%20y%20caminos%20minimos/EJ_07-3/README.md) | [🎬 Vídeo](Videos/07-3_rapideats.mp4) | Dijkstra por pedido y reconstrucción de la ruta retrocediendo por `ulti[]` |

**Qué técnica usar**

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| Camino de **menor coste total** con costes ≥ 0 | **Dijkstra** con `IndexPQ` (O(A log V)) | 07-1, 07-2, 07-3 |
| Coste también en los **vértices** (cargas, esperas) | Sumar el coste del vértice a la arista que **entra** en él y el del origen a `dist[origen]` | 07-1 |
| **Cuántos** caminos mínimos hay | Dijkstra + `formas[]`: sustituir al mejorar, sumar al empatar | 07-2 |
| Escribir **el camino** | `ulti[]`: retroceder desde el destino | 07-3 |
| Grafo **no dirigido** | Añadir cada arista en los dos sentidos al `DigrafoValorado` | 07-2, 07-3 |

---

<!-- acr-seccion:inicio -->
## Probar sin el juez: Acepta el Reto

Muchos enunciados de la asignatura salen de [Acepta el Reto](https://aceptaelreto.com), que es público y no hace falta tener acceso al juez de la UCM: puedes enviar ahí tu solución y comprobar si es correcta sin mirar la mía. Cuatro cosas que conviene saber antes:

- **Mismo problema** no siempre significa misma entrada: la versión de la asignatura puede empezar con el número de casos, mientras que en Acepta el Reto algunos terminan con una línea especial (por ejemplo `0 0 0 0`). Mira la sección *Entrada* y adapta el bucle de lectura.
- **Casi el mismo problema** cambia algún límite o el formato; la idea de la solución sirve igual.
- **Código para enviar**: Acepta el Reto solo admite un fichero `.cpp`, así que en [`Acepta el Reto/`](<Acepta el Reto>) hay una versión de cada solución con las cabeceras (`Grafo.h`, `Digrafo.h`, `IndexPQ.h`…) copiadas dentro y la lectura de la entrada adaptada. Se generan con `python3 herramientas/para_acepta.py`, no se editan a mano.
- **Relacionado** es otro problema que practica la misma técnica.
- Los enlaces se han comprobado a mano comparando enunciados; si encuentras alguno mal, avisa o corrígelo en `herramientas/acepta_el_reto.json`.

| Nº | Ejercicio | Acepta el Reto | Relación | Código para enviar | A tener en cuenta |
|:--:|---|---|---|---|---|
| 01-1 | ¿Es un árbol AVL? (enteros) | [#303](https://aceptaelreto.com/problem/statement.php?id=303) | mismo problema | [📥 ACR-303](<Acepta el Reto/ACR-303_es_un_arbol_AVL.cpp>) | Mismo enunciado: el árbol llega en preorden y -1 es el árbol vacío. |
| 01-1 | ¿Es un árbol AVL? (genérico) | [#303](https://aceptaelreto.com/problem/statement.php?id=303) | casi el mismo problema | — | Mismo problema, pero en Acepta el Reto solo hay enteros y el árbol viene en preorden (aquí llega con paréntesis y puede ser de palabras). Sirve para probar la lógica del AVL cambiando la lectura. |
| 02-1 | Lo que cuesta sumar | [#289](https://aceptaelreto.com/problem/statement.php?id=289) | mismo problema | [📥 ACR-289](<Acepta el Reto/ACR-289_lo_que_cuesta_sumar.cpp>) | Mismo enunciado. |
| 02-2 | Unidad Curiosa de Monitorización | [#351](https://aceptaelreto.com/problem/statement.php?id=351) | casi el mismo problema | [📥 ACR-351](<Acepta el Reto/ACR-351_unidad_curiosa_de_monitorizacion.cpp>) | Misma historia, pero allí los límites son menores (hasta 2.500 usuarios y 10.000 envíos; aquí 25.000 y 100.000) y el separador de cada caso es `----` (cuatro guiones). |
| 02-3 | Reina del súper | [#341](https://aceptaelreto.com/problem/statement.php?id=341) | casi el mismo problema | [📥 ACR-341](<Acepta el Reto/ACR-341_reina_del_super.cpp>) | Misma historia, pero allí hay como mucho 5 cajas y 1.000 clientes (aquí hasta 250.000 y 500.000), así que tu solución con cola de prioridad también pasa. Allí no hay caso final `0 0`: la entrada acaba con el fichero. |
| 02-5 | Ordenando a los pacientes en urgencias | [#311](https://aceptaelreto.com/problem/statement.php?id=311) | mismo problema | [📥 ACR-311](<Acepta el Reto/ACR-311_pacientes_en_urgencias.cpp>) | Mismo enunciado, pero el separador de cada caso es `----` (cuatro guiones). |
| 03-1 | Volando drones | [#505](https://aceptaelreto.com/problem/statement.php?id=505) | mismo problema | [📥 ACR-505](<Acepta el Reto/ACR-505_volando_drones.cpp>) | Mismo problema; los ejemplos del enunciado son algo distintos. |
| 03-3 | Multitarea | [#649](https://aceptaelreto.com/problem/statement.php?id=649) | casi el mismo problema | [📥 ACR-649](<Acepta el Reto/ACR-649_multitarea.cpp>) | Mismo problema; allí los instantes llegan hasta 10^9 (aquí 10^8) y no hay número de casos: se lee hasta el final del fichero. |
| 03-4 | Pájaros en vuelo | [#271](https://aceptaelreto.com/problem/statement.php?id=271) | mismo problema | [📥 ACR-271](<Acepta el Reto/ACR-271_pajaros_en_vuelo.cpp>) | Mismo enunciado (la entrada termina con «0 0»). |
| 04-1 | Árboles libres | [#307](https://aceptaelreto.com/problem/statement.php?id=307) | mismo problema | [📥 ACR-307](<Acepta el Reto/ACR-307_arboles_libres.cpp>) | Mismo enunciado, pero allí no hay número de casos: se lee hasta el final del fichero. |
| 04-2 | Los amigos de mis amigos son mis amigos | [#352](https://aceptaelreto.com/problem/statement.php?id=352) | mismo problema | [📥 ACR-352](<Acepta el Reto/ACR-352_amigos_de_mis_amigos.cpp>) | Mismo enunciado: la primera línea es el número de casos. |
| 04-3 | Ovejas negras | [#412](https://aceptaelreto.com/problem/statement.php?id=412) | problema relacionado | — | No es el mismo problema, pero practica la misma técnica: recorrer una cuadrícula de píxeles por sus componentes conexas. |
| 04-7 | Grafo bipartito | [#279](https://aceptaelreto.com/problem/statement.php?id=279) | mismo problema | [📥 ACR-279](<Acepta el Reto/ACR-279_grafo_bipartito.cpp>) | Mismo enunciado, pero allí no hay número de casos: se lee hasta el final del fichero. |
| 05-1 | La máquina calculadora | [#319](https://aceptaelreto.com/problem/statement.php?id=319) | mismo problema | [📥 ACR-319](<Acepta el Reto/ACR-319_maquina_calculadora.cpp>) | Mismo enunciado, pero allí no hay número de casos: se lee hasta el final del fichero. |
| 05-2 | La máquina calculadora | [#319](https://aceptaelreto.com/problem/statement.php?id=319) | problema relacionado | — | No es el mismo problema, pero es el caso particular de la transformación modular: BFS sobre estados con 3 operaciones y módulo 10.000. |
| 05-3 | Despegando pósits | [#654](https://aceptaelreto.com/problem/statement.php?id=654) | problema relacionado | — | No es el mismo problema, pero es un orden topológico por capas (con detección de ciclos: «IMPOSIBLE»). |
| 05-5 | Haciendo trampas en Serpientes y Escaleras | [#253](https://aceptaelreto.com/problem/statement.php?id=253) | mismo problema | [📥 ACR-253](<Acepta el Reto/ACR-253_serpientes_y_escaleras.cpp>) | Mismo enunciado, pero allí la entrada termina con la línea «0 0 0 0» en vez de empezar con el número de casos. |
| 06-1 | Petroleros hundidos | [#288](https://aceptaelreto.com/problem/statement.php?id=288) | casi el mismo problema | [📥 ACR-288](<Acepta el Reto/ACR-288_petroleros_hundidos.cpp>) | Mismo problema, pero allí no hay número de casos (se lee hasta el final del fichero) y, según el ejemplo de la página, el mar va como espacio en blanco en vez de `-`: lee cada fila con `getline` y comprueba que la longitud es C. |
| 06-2 | Camiones de reparto | [#646](https://aceptaelreto.com/problem/statement.php?id=646) | mismo problema | [📥 ACR-646](<Acepta el Reto/ACR-646_camiones_de_reparto.cpp>) | Mismo enunciado, pero allí no hay número de casos: se lee hasta el final del fichero. |
| 06-3 | Recorriendo el archipiélago en bicicleta | [#645](https://aceptaelreto.com/problem/statement.php?id=645) | casi el mismo problema | [📥 ACR-645](<Acepta el Reto/ACR-645_archipielago_en_bicicleta.cpp>) | Misma historia, pero allí los límites son menores (hasta 1.000 islas y 10.000 puentes; aquí 10.000 y 100.000) y no hay número de casos: se lee hasta el final del fichero. |
| 07-1 | Navegando sin teclado | [#318](https://aceptaelreto.com/problem/statement.php?id=318) | casi el mismo problema | [📥 ACR-318](<Acepta el Reto/ACR-318_navegando_sin_teclado.cpp>) | Misma historia, pero allí los límites son menores (hasta 1.000 páginas; aquí 3.000 páginas y 30.000 enlaces) y no hay número de casos: se lee hasta el final del fichero. |
| 07-2 | Camino al cole | [#358](https://aceptaelreto.com/problem/statement.php?id=358) | casi el mismo problema | [📥 ACR-358](<Acepta el Reto/ACR-358_camino_al_cole.cpp>) | Misma historia, pero allí los límites son distintos (hasta 10.000 intersecciones y 100.000 calles de hasta 100.000 de longitud; aquí 100.000, 200.000 y 10.000) y no hay número de casos: se lee hasta el final del fichero. |
| 07-3 | RapidEats | [#813](https://aceptaelreto.com/problem/statement.php?id=813) | casi el mismo problema | [📥 ACR-813](<Acepta el Reto/ACR-813_rapideats.cpp>) | Allí solo se pide el **tiempo mínimo** de cada pedido (sin la ruta: `30` en vez de `30: 1 -> 3`) y no hay número de casos (se lee hasta el final del fichero); el resto es igual. |

**Sin equivalente que haya encontrado:** 01-2, 02-4, 02-6, 02-L, 03-2, 03-5, 03-L, 04-4, 04-5, 04-6, 04-L, 05-4, 05-6, 06-4, 06-5. Son enunciados propios de la asignatura (o no aparecen en el buscador de Acepta el Reto).

Para añadir o corregir un enlace: edita `herramientas/acepta_el_reto.json` y ejecuta `python3 herramientas/enlaces_acepta.py`.
<!-- acr-seccion:fin -->

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
| [`tema6-kruskal.html`](Visualizaciones/tema6-kruskal.html) | `ConjuntosDisjuntos`, `GrafoValorado` | laboratorio de las 4 implementaciones de conjuntos disjuntos (autoevaluación 6.1, peor caso), manchas de petróleo (06-1), Kruskal y Prim sobre tu grafo |
| [`tema7-dijkstra.html`](Visualizaciones/tema7-dijkstra.html) | `DigrafoValorado`, Dijkstra | relajación de aristas, Dijkstra con cola de prioridad y con vector, camino por `ulti[]`, contar caminos (07-2) y coste en vértices (07-1) sobre tu grafo |

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
| [`ConjuntosDisjuntos.h`](Estructuras%20de%20datos/ConjuntosDisjuntos.h) | Partición en conjuntos disjuntos con unión por tamaños y compresión de caminos (`unir`, `buscar`, `unidos`, `cardinal`, `num_cjtos`) | Tema 6 |
| [`GrafoValorado.h`](Estructuras%20de%20datos/GrafoValorado.h) | Grafo no dirigido valorado: `Arista<Valor>` (`uno`, `otro`, `valor`) y `GrafoValorado<Valor>` (`ady`, `aristas`, `ponArista`) | Tema 6 |
| [`ConjuntosDisjuntos_variantes.h`](Estructuras%20de%20datos/ConjuntosDisjuntos_variantes.h) · [`_demo.cpp`](Estructuras%20de%20datos/ConjuntosDisjuntos_demo.cpp) | Las cuatro versiones de las transparencias (búsqueda rápida, unión rápida, por tamaños, con compresión) con contador de accesos | Tema 6 |
| [`GrafoValorado_algoritmos.h`](Estructuras%20de%20datos/GrafoValorado_algoritmos.h) · [`_demo.cpp`](Estructuras%20de%20datos/GrafoValorado_demo.cpp) | `ARM_Kruskal` y `ARM_Prim` de las transparencias | Tema 6 |
| [`DigrafoValorado.h`](Estructuras%20de%20datos/DigrafoValorado.h) | Digrafo valorado: `AristaDirigida<Valor>` (`desde`, `hasta`, `valor`) y `DigrafoValorado<Valor>` (`ady`, `ponArista`, `inverso`) | Tema 7 |
| [`DigrafoValorado_algoritmos.h`](Estructuras%20de%20datos/DigrafoValorado_algoritmos.h) · [`_demo.cpp`](Estructuras%20de%20datos/DigrafoValorado_demo.cpp) | `Dijkstra` (con `IndexPQ`) y `DijkstraVector` (O(V²)) de las transparencias | Tema 7 |
| [`Digrafo.h`](Estructuras%20de%20datos/Digrafo.h) | Grafo dirigido con la misma interfaz (+ `hayArista`, `inverso()`, constructor desde `cin`) | Tema 5 |
| [`Digrafo_algoritmos.h`](Estructuras%20de%20datos/Digrafo_algoritmos.h) | Algoritmos del tema 5 juntos: `DFSDirigido`, `BFSDirigido`, `OrdenTopologico`, `CicloDirigido` y `CFC` (componentes fuertemente conexas, extra) | Vídeo 05-0 |
| [`Digrafo_demo.cpp`](Estructuras%20de%20datos/Digrafo_demo.cpp) | Ejecuta esos algoritmos sobre los grafos de las transparencias | Vídeo 05-0 |
| [`Digrafo_implicito_calculadora.cpp`](Estructuras%20de%20datos/Digrafo_implicito_calculadora.cpp) | La máquina calculadora como **grafo implícito** (transparencias 13) | Vídeo 05-0 |

## Vídeos

Todos en [`Videos/`](Videos), con subtítulos en castellano (y capítulos el de teoría). Enlazados también en la columna «Vídeo» de cada tema.

| Vídeo | Contenido |
|---|---|
| [`05-0_grafos_dirigidos_teoria.mp4`](Videos/05-0_grafos_dirigidos_teoria.mp4) | **Teoría completa del tema 5** (23 min, 10 capítulos) |
| [`06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4`](Videos/06-0_conjuntos_disjuntos_grafos_valorados_teoria.mp4) | **Teoría completa del tema 6**: conjuntos disjuntos, grafos valorados, Kruskal y Prim, y cómo se aplican a 06-1 … 06-5 (con capítulos) |
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
├── 6-Conjuntos disjuntos y grafos valorados/   ejercicios (código + explicación) y resumen del tema
├── 7-Digrafos valorados y caminos minimos/    ejercicios (código + explicación) y resumen del tema
├── Acepta el Reto/              versiones de las soluciones listas para enviar a aceptaelreto.com (un solo fichero)
├── Estructuras de datos/        cabeceras de la asignatura (+ algoritmos de los temas 4 a 7)
├── Videos/                      vídeos explicativos
│   └── generador/               scripts que los generan
├── Visualizaciones/             herramientas interactivas (abre index.html)
├── sitio/                       generador de la web
└── herramientas/                recolocar proyectos de VS, enlaces y generador de «Acepta el Reto/»
```

## Añadir un ejercicio nuevo

1. En VS: clic derecho en la carpeta del tema de la solución → *Agregar → Nuevo proyecto*, con **Ubicación** `…\DA\<tema>\` (por ejemplo `…\DA\5-Grafos dirigidos\`) y nombre `EJ_0T-N`.
2. El PDF del enunciado, en `<tema>/Enunciados/`.
3. Una fila en la tabla del tema de este README (si no, la web lo añade igualmente al detectar la carpeta, pero sin título).
4. Si el problema también está en Acepta el Reto: añade su fila a `herramientas/acepta_el_reto.json` (y, si quieres la versión lista para enviar, una entrada en `herramientas/para_acepta.py`) y ejecuta `python3 herramientas/enlaces_acepta.py` y `python3 herramientas/para_acepta.py --probar`.
5. Commit y push: la web se actualiza sola.

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
