# DA · Ejercicios del juez

> 🌐 **Web con todo reunido** (ejercicios, PDFs, soluciones, vídeos y herramientas interactivas): **<https://juanp-g.github.io/DA/>**

## Índice

- [Tema 1 · Árboles AVL](#tema-1--árboles-avl)
- [Tema 2 · Colas de prioridad](#tema-2--colas-de-prioridad)
- [Tema 3 · Colas de prioridad variable (IndexPQ)](#tema-3--colas-de-prioridad-variable-indexpq)
- [Tema 4 · Grafos no dirigidos](#tema-4--grafos-no-dirigidos)
- [Tema 5 · Grafos dirigidos](#tema-5--grafos-dirigidos)
- [Visualizaciones interactivas](#visualizaciones-interactivas)
- [Estructuras de datos](#estructuras-de-datos)
- [Organización del repositorio](#organización-del-repositorio)
- [Compilar y probar](#compilar-y-probar)

## Tema 1 · Árboles AVL

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 01-1 | ¿Es un árbol AVL? (enteros) | [📄 PDF](Ejercicios%20juez/1-Arboles%20AVL/prob-%C2%BFEs%20un%20%C3%A1rbol%20AVL_.pdf) | [💻 Solución](DA/EJ%2001-1.cpp) | — | Postorden: altura, mínimo y máximo de cada subárbol |
| 01-1 | ¿Es un árbol AVL? (genérico) | [📄 PDF](Ejercicios%20juez/1-Arboles%20AVL/prob-%C2%BFEs%20un%20%C3%A1rbol%20AVL_%20%281%29.pdf) | [💻 Versión 1](EJ%2001-1%20%28GENERICO%29/EJ%2001-1%20%28GENERICO%29.cpp) · [💻 Versión final](J%2001-1%20%28GENERICO%29%20-%20NICE/EJ%2001-1%20%28GENERICO%20BIEN%29.cpp) | — | Lo mismo con `template <class T>` y `BinTree<T>` |
| 01-2 | Encontrar el k-ésimo elemento en un árbol AVL | [📄 PDF](Ejercicios%20juez/1-Arboles%20AVL/prob-Encontrar%20el%20k-%C3%A9simo%20elemento%20en%20un%20%C3%A1rbol%20AVL.pdf) | [💻 Solución](EJ%2001-2/EJ%2001-2.cpp) | — | `Set` AVL con tamaño de subárbol → `kesimo` |

## Tema 2 · Colas de prioridad

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 02-1 | Lo que cuesta sumar | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Lo%20que%20cuesta%20sumar.pdf) | [💻 Solución](EJ_02-1/EJ_02-1.cpp) | — | Cola de mínimos: sumar siempre los dos menores |
| 02-2 | Unidad Curiosa de Monitorización | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Unidad%20Curiosa%20de%20Monitorizaci%C3%B3n.pdf) | [💻 Solución](EJ_02-2/EJ_02-2.cpp) | — | Cola de mínimos de próximos envíos (instante, id) |
| 02-3 | Reina del súper | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Reina%20del%20s%C3%BAper.pdf) | [💻 Solución](EJ_02-3/EJ_02-3.cpp) | — | Cola de mínimos de cajas (instante libre, nº de caja) |
| 02-4 | La ley D'Hondt | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-La%20ley%20D%27Hondt.pdf) | [💻 Solución](EJ_02-4/EJ_02-4.cpp) | — | Cola de máximos de cocientes votos / (1 + escaños) |
| 02-5 | Ordenando a los pacientes en urgencias | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Ordenando%20a%20los%20pacientes%20en%20urgencias.pdf) | [💻 Solución](EJ_02-5/EJ_02-5.cpp) | — | Cola de máximos (gravedad, orden de llegada) |
| 02-6 | Coleccionando cómics | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Coleccionando%20c%C3%B3mics.pdf) | [💻 Solución](EJ_02-6/EJ_02-6.cpp) | — | Cola de mínimos de cimas de pila + `Pila.h` |
| 02-L | Cinemáticas digitales | [📄 PDF](Ejercicios%20juez/2-Colas%20de%20prioridad/prob-Cinem%C3%A1ticas%20digitales.pdf) | [💻 Solución](EJ_02-L/EJ_02-L.cpp) | — | Cola de mínimos de estaciones de renderizado |

## Tema 3 · Colas de prioridad variable (IndexPQ)

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 03-1 | Volando drones | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-Volando%20drones.pdf) | [💻 Solución](EJ_03-1/EJ_03-1.cpp) | — | Dos colas de máximos de pilas (9V y 1,5V) |
| 03-2 | 12 points go to… | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-12%20points%20go%20to%E2%80%A6.pdf) | [💻 Solución](EJ_03-2/EJ_03-2.cpp) | — | `IndexPQ` de países con `update` de puntos |
| 03-3 | Multitarea | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-Multitarea.pdf) | [💻 Solución](EJ_03-3/EJ_03-3.cpp) | — | `IndexPQ` de intervalos (tareas únicas y periódicas) |
| 03-4 | Pájaros en vuelo | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-P%C3%A1jaros%20en%20vuelo.pdf) | [💻 Solución](EJ_03-4/EJ_03-4.cpp) | [🎬 Vídeo](Videos/03-4_pajaros_en_vuelo.mp4) | Mediana con dos montículos (máximos · mínimos) |
| 03-5 | Tridente de temas candentes | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-Tridente%20de%20temas%20candentes.pdf) | [💻 Solución](EJ_03-5/EJ_03-5.cpp) | [🎬 Vídeo](Videos/03-5_tridente_temas_candentes.mp4) | `IndexPQ` de temas (citas, último C) |
| 03-L | La batalla por las audiencias | [📄 PDF](Ejercicios%20juez/3-Colas%20de%20prioridad%20variable%20%28Heapsort%29/prob-La%20batalla%20por%20las%20audiencias.pdf) | [💻 Solución](EJ_03-L/EJ_03-L.cpp) | [🎬 Vídeo](Videos/03-L_batalla_audiencias.mp4) | `IndexPQ` de canales; el líder acumula minutos |

## Tema 4 · Grafos no dirigidos

Todos usan [`Grafo.h`](Estructuras%20de%20datos/Grafo.h). Están numerados como en el juez.

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 04-1 | Árboles libres | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-%C3%81rboles%20libres.pdf) | [💻 Solución](EJ_04-1/EJ_04-1.cpp) · [📘 Explicación](EJ_04-1/README.md) | [🎬 Vídeo](Videos/04-1_arboles_libres.mp4) | DFS: conexo y A = V − 1 |
| 04-2 | Los amigos de mis amigos son mis amigos | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Los%20amigos%20de%20mis%20amigos%20son%20mis%20amigos.pdf) | [💻 Solución](EJ_04-2/EJ_04-2.cpp) · [📘 Explicación](EJ_04-2/README.md) | [🎬 Vídeo](Videos/04-2_amigos_de_mis_amigos.mp4) | DFS: componente conexa más grande |
| 04-3 | Detección de manchas negras | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Detecci%C3%B3n%20de%20manchas%20negras.pdf) | [💻 Solución](EJ_04-3/EJ_04-3.cpp) · [📘 Explicación](EJ_04-3/README.md) | [🎬 Vídeo](Videos/04-3_manchas_negras.mp4) | Píxel → vértice i·C + j; DFS: número de componentes y la mayor |
| 04-4 | Los números de Bacon | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Los%20n%C3%BAmeros%20de%20Bacon.pdf) | [💻 Solución](EJ_04-4/EJ_04-4.cpp) · [📘 Explicación](EJ_04-4/README.md) | [🎬 Vídeo](Videos/04-4_numeros_de_bacon.mp4) | BFS en grafo actor–película; Bacon = dist / 2 |
| 04-5 | ¡Las noticias vuelan! | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-%C2%A1Las%20noticias%20vuelan%21.pdf) | [💻 Solución](EJ_04-5/EJ_04-5.cpp) · [📘 Explicación](EJ_04-5/README.md) | [🎬 Vídeo](Videos/04-5_las_noticias_vuelan.mp4) | Aristas en estrella + tamaño de componentes con BFS |
| 04-6 | Un nodo muy muy lejano | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Un%20nodo%20muy%20muy%20lejano.pdf) | [💻 Solución](EJ_04-6/EJ_04-6.cpp) · [📘 Explicación](EJ_04-6/README.md) | [🎬 Vídeo](Videos/04-6_nodo_muy_lejano.mp4) | BFS con distancias, cortado en el TTL |
| 04-7 | Grafo bipartito | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Grafo%20bipartito.pdf) | [💻 Solución](EJ_04-7/EJ_04-7.cpp) · [📘 Explicación](EJ_04-7/README.md) | [🎬 Vídeo](Videos/04-7_grafo_bipartito.mp4) | DFS coloreando con 2 colores |
| 04-L | Peaje a la sombra | [📄 PDF](Ejercicios%20juez/4-Grafos%20no%20dirigidos/prob-Peaje%20a%20la%20sombra.pdf) | [💻 Solución](EJ_04-L/EJ_04-L.cpp) · [📘 Explicación](EJ_04-L/README.md) | [🎬 Vídeo](Videos/04-L_peaje_a_la_sombra.mp4) | 3 BFS (Álex, Lucas, trabajo) y mínimo de dA+dL+dT |

**Cómo elegir el recorrido en este tema**

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| ¿A qué vértices se llega? ¿Es conexo? Número y tamaño de las componentes | DFS (o BFS: el orden da igual) | 04-1, 04-2, 04-3, 04-5 |
| Una asignación que *obliga* a los vecinos (2 colores) | DFS propagando la restricción | 04-7 |
| Distancia **mínima** en número de aristas | **BFS** (un DFS puede llegar por un camino largo) | 04-4, 04-6, 04-L, 05-1, 05-2, 05-5 |
| Grafo **dirigido** cuyas aristas salen de una fórmula | Construir el `Digrafo` con `ponArista` y hacer BFS | 05-1, 05-2 |
| Ordenar con precedencias («A antes que B», xi < xj) | **Orden topológico**: postorden inverso del DFS; ciclo ⇒ imposible | 05-3, 05-6 |
| Grados de los vértices (p. ej. sumidero) | Salida = `ady(v).size()`; entrada = contar en todas las listas | 05-4 |
| Camino compartido por dos personas hasta un destino (forma de **Y**) | BFS desde los 3 puntos y mínimo de la suma de distancias | 04-L |
| Grupos con muchos miembros | No unir todos con todos: en estrella si solo importa la conexión, o con un vértice por grupo si importan las distancias | 04-5, 04-4 |

## Tema 5 · Grafos dirigidos

| Nº | Problema | Enunciado | Solución | Vídeo | Idea |
|:--:|---|:--:|---|:--:|---|
| 05-1 | Juego de Transformación Modular | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-Juego%20de%20Transformaci%C3%B3n%20Modular.pdf) | [💻 Solución](EJ_05-1/EJ_05-1.cpp) · [📘 Explicación](EJ_05-1/README.md) | [🎬 Vídeo](Videos/05-1_transformacion_modular.mp4) | BFS en un `Digrafo` construido con x → (a·x+b) mod M |
| 05-2 | La máquina calculadora | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-La%20m%C3%A1quina%20calculadora.pdf) | [💻 Solución](EJ_05-2/EJ_05-2.cpp) · [📘 Explicación](EJ_05-2/README.md) | [🎬 Vídeo](Videos/05-2_maquina_calculadora.mp4) | BFS en un `Digrafo` con los 10.000 números del marcador (+1, ×2, ÷3) |
| 05-3 | Ordenando tareas | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-Ordenando%20tareas.pdf) | [💻 Solución](EJ_05-3/EJ_05-3.cpp) · [📘 Explicación](EJ_05-3/README.md) | [🎬 Vídeo](Videos/05-3_ordenando_tareas.mp4) | Orden topológico: postorden inverso del DFS (+ ciclos) |
| 05-4 | Sumidero en un grafo dirigido | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-Sumidero%20en%20un%20grafo%20dirigido.pdf) | [💻 Solución](EJ_05-4/EJ_05-4.cpp) · [📘 Explicación](EJ_05-4/README.md) | — | Grados: salida 0 (`ady(v)` vacío) y entrada V − 1 (contando en las listas) |
| 05-5 | Haciendo trampas en Serpientes y Escaleras | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-Haciendo%20trampas%20en%20Serpientes%20y%20Escaleras.pdf) | [💻 Solución](EJ_05-5/EJ_05-5.cpp) · [📘 Explicación](EJ_05-5/README.md) | — | BFS: casilla v → destino(v + d), d = 1…K; serpiente/escalera = salto obligatorio |
| 05-6 | Sistema de inecuaciones | [📄 PDF](Ejercicios%20juez/5-Grafos%20dirigidos/prob-Sistema%20de%20inecuaciones.pdf) | [💻 Solución](EJ_05-6/EJ_05-6.cpp) · [📘 Explicación](EJ_05-6/README.md) | [🎬 Vídeo](Videos/05-6_sistema_inecuaciones.mp4) | xi < xj = arista i → j; ciclo ⇒ NO; si no, valor = posición en el orden topológico |

## Visualizaciones interactivas

Una página HTML por estructura de datos, en [`Visualizaciones/`](Visualizaciones). Ejecutan la misma lógica que el C++ de `Estructuras de datos/`, muestran el código real con la línea activa resaltada y dejan construir ejemplos propios, avanzar y retroceder paso a paso (flechas del teclado) y cambiar la velocidad.

| Página | Estructura | Qué se puede hacer |
|---|---|---|
| [`tema1-avl.html`](Visualizaciones/tema1-avl.html) | `Set<T>` (AVL) | insertar, borrar, `borraMin`, `kesimo`; factor de equilibrio y las 4 rotaciones |
| [`tema2-cola-prioridad.html`](Visualizaciones/tema2-cola-prioridad.html) | montículo binario | `push` (flotar), `pop` (hundir), heapify en O(n), mínimos/máximos |
| [`tema3-indexpq.html`](Visualizaciones/tema3-indexpq.html) | `IndexPQ` | `push`, `update`, `pop` con la tabla `posiciones` |
| [`tema4-grafo.html`](Visualizaciones/tema4-grafo.html) | `Grafo` | construir el grafo, listas de adyacencia, DFS (componentes), BFS, bipartito |
| [`tema5-digrafo.html`](Visualizaciones/tema5-digrafo.html) | `Digrafo` | construir el digrafo, BFS, orden topológico con ciclos, `inverso()` |

GitHub no ejecuta HTML dentro del repositorio: descarga el repositorio (o solo la carpeta `Visualizaciones`) y abre `index.html` con doble clic. Las páginas se generan con `python3 Visualizaciones/_fuente/gen_grafos.py && python3 Visualizaciones/_fuente/build.py`; en `_fuente/` están los fragmentos, el CSS/JS compartido y el generador (el código C++ de las páginas de grafos se lee de los `.h` y `.cpp` reales).

## Estructuras de datos

Las cabeceras que da la asignatura están juntas en [`Estructuras de datos/`](Estructuras%20de%20datos). Cada ejercicio lleva también su propia copia junto al `.cpp`, para compilar sin rutas extra.

| Fichero | Qué es | Se usa en |
|---|---|---|
| [`Grafo.h`](Estructuras%20de%20datos/Grafo.h) | Grafo no dirigido con listas de adyacencia (`V()`, `A()`, `ady(v)`, `ponArista`) | Tema 4 |
| [`Digrafo.h`](Estructuras%20de%20datos/Digrafo.h) | Grafo dirigido con la misma interfaz (+ `hayArista`, `inverso()`) | Tema 5 (05-1 … 05-6) |
| [`IndexPQ.h`](Estructuras%20de%20datos/IndexPQ.h) | Cola de prioridad con índices (`push`, `update`, `top`, `pop`, `priority`) | Tema 3 |
| [`TreeSet_AVL_plantilla.h`](Estructuras%20de%20datos/TreeSet_AVL_plantilla.h) | Conjunto sobre árbol AVL (`Set<T>`), con `kesimo` | 01-2 |
| [`bintree.h`](Estructuras%20de%20datos/bintree.h) | Árbol binario `BinTree<T>` | 01-1 genérico, 01-2 |
| [`Pila.h`](Estructuras%20de%20datos/Pila.h) | Pila `Pila<T>` | 02-6 |

## Organización del repositorio

```text
.
├── EJ_0T-N/                 solución de cada ejercicio (T = tema, N = número del juez)
│   ├── EJ_0T-N.cpp
│   ├── <estructura>.h       copia de la cabecera que usa (si usa alguna)
│   └── README.md            explicación del planteamiento (tema 4)
├── Ejercicios juez/         enunciados en PDF, por tema
├── Estructuras de datos/    cabeceras que da la asignatura
├── Visualizaciones/         páginas interactivas de cada estructura (abre index.html)
│   └── _fuente/             fragmentos, CSS/JS compartido y scripts que las generan
└── Videos/                  vídeos explicativos
    └── generador/           scripts que generan los vídeos
```

## Compilar y probar

```bash
g++ -std=c++17 -O2 -Wall -o sol EJ_04-1/EJ_04-1.cpp
./sol < entrada.txt
```

Las soluciones del tema 4 están probadas con los ejemplos de los enunciados, contra soluciones de fuerza bruta en miles de casos aleatorios y con entradas en el máximo de los límites.

> ⚠️ Los DFS recursivos del tema 4 pueden bajar tantos niveles como vértices haya. En el juez no da problemas, pero en Visual Studio (pila de 1 MB) un caso enorme podría desbordar la pila. Por eso el 04-5 usa un BFS iterativo. En el 04-3 el enunciado limita las manchas a 50.000 píxeles justo para que el DFS recursivo sea seguro.

## Web del repositorio

**🌐 Dirección: <https://juanp-g.github.io/DA/>**

Todo lo anterior (enunciados, soluciones, explicaciones, vídeos y herramientas interactivas) se reúne en una web estática que se genera sola desde este repositorio con [`sitio/construir.py`](sitio/construir.py) y el workflow [`.github/workflows/web.yml`](.github/workflows/web.yml), cada vez que cambia `main`. Para verla en local:

```bash
pip install markdown
python3 sitio/construir.py      # genera sitio/_site/
python3 -m http.server -d sitio/_site 8000
```

Para publicarla en GitHub Pages: *Settings → Pages → Source: GitHub Actions*. (En repositorios privados Pages requiere un plan de pago, y la web publicada es pública. Sin Pages, cada ejecución del workflow deja la web como artefacto descargable `web-DA`.) Un ejercicio nuevo aparece en la web al añadir su fila en las tablas de este README o, como mínimo, su carpeta `EJ_0T-N/` con el `.cpp`.
