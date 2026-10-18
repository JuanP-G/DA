# Tema 6 · Conjuntos disjuntos, grafos valorados y árboles de recubrimiento de coste mínimo

Resumen del tema (semana 6 del campus) con la respuesta al ejercicio de autoevaluación 6.1. Los ejercicios del juez están en las carpetas `EJ_06-1` … `EJ_06-5`; en cada una hay una explicación del planteamiento (sin código de la solución).

| Nº | Problema | Técnica |
|:--:|---|---|
| [06-1](EJ_06-1/README.md) | Petroleros hundidos | Conjuntos disjuntos: uniones que solo crecen, tamaño máximo con `cardinal` |
| [06-2](EJ_06-2/README.md) | Camiones de reparto | Grafo valorado + DFS/BFS que ignora las aristas que no cumplen el umbral |
| [06-3](EJ_06-3/README.md) | Recorriendo el archipiélago en bicicleta | Kruskal: **suma** del árbol de recubrimiento de coste mínimo |
| [06-4](EJ_06-4/README.md) | La selva de Tarzán | Kruskal: **última** arista aceptada (el máximo del ARM) |
| [06-5](EJ_06-5/README.md) | Las minas del emperador Trajano | Kruskal con parada: arista que conecta **dos** vértices (camino minimax) |

---

## 6.1 Conjuntos disjuntos

Una **relación de equivalencia** (reflexiva, simétrica y transitiva) reparte los elementos en **clases**: una partición en conjuntos disjuntos. Si la relación es **dinámica** (van apareciendo nuevos pares relacionados mientras se hacen preguntas) el TAD de conjuntos disjuntos permite:

| Operación | Qué hace |
|---|---|
| `ConjuntosDisjuntos(N)` | partición unitaria de 0 … N − 1 |
| `unir(a, b)` | fusiona los conjuntos de `a` y de `b` |
| `buscar(a)` | representante (raíz) del conjunto de `a` |
| `unidos(a, b)` | ¿mismo conjunto? |
| `cardinal(a)` | tamaño del conjunto de `a` |
| `num_cjtos()` | cuántos conjuntos hay |

Solo se puede **unir**, nunca separar. Por eso sirve para problemas en los que lo que pasa va juntando cosas (manchas que crecen, islas que se conectan…).

### Implementaciones y coste (M operaciones sobre N elementos)

| Implementación | Idea | Coste en el caso peor |
|---|---|---|
| Búsqueda rápida | `id[i]` = conjunto de `i`; unir reetiqueta todo un conjunto | N · M |
| Unión rápida | un árbol por conjunto, `p[i]` = padre; unir cuelga una raíz de otra | N · M (los árboles pueden ser cadenas) |
| Unión por tamaños | cuelga el árbol **pequeño** del grande ⇒ altura ≤ log N | N + M log N |
| Compresión de caminos | tras `buscar`, cada nodo visitado pasa a colgar de la raíz | N + M log N |
| **Tamaños + compresión** (`ConjuntosDisjuntos.h`) | las dos | **N + M · lg\* N** |

`lg* N` (logaritmo iterado) es el número de veces que hay que aplicar `log` hasta llegar a 1; es ≤ 5 para cualquier N que quepa en un ordenador, así que en la práctica **cada operación es constante**.

### Autoevaluación del campus

Partición unitaria de 10 elementos y estas uniones, en orden: `9-0  3-4  5-8  7-2  2-1  5-7  0-3  4-2`.

**1. Búsqueda rápida** (`unir(a, b)`: los elementos con el identificador de `a` pasan a tener el de `b`):

```text
                 id[0..9]
inicial           0  1  2  3  4  5  6  7  8  9
unir(9,0)         0  1  2  3  4  5  6  7  8  0
unir(3,4)         0  1  2  4  4  5  6  7  8  0
unir(5,8)         0  1  2  4  4  8  6  7  8  0
unir(7,2)         0  1  2  4  4  8  6  2  8  0
unir(2,1)         0  1  1  4  4  8  6  1  8  0
unir(5,7)         0  1  1  4  4  1  6  1  1  0
unir(0,3)         4  1  1  4  4  1  6  1  1  4
unir(4,2)         1  1  1  1  1  1  6  1  1  1
```
Quedan dos conjuntos: `{6}` y `{0,1,2,3,4,5,7,8,9}`.

**2. Unión rápida** (`unir(a, b)`: la raíz de `a` pasa a ser hija de la raíz de `b`):

```text
                 p[0..9]
inicial           0  1  2  3  4  5  6  7  8  9
unir(9,0)         0  1  2  3  4  5  6  7  8  0
unir(3,4)         0  1  2  4  4  5  6  7  8  0
unir(5,8)         0  1  2  4  4  8  6  7  8  0
unir(7,2)         0  1  2  4  4  8  6  2  8  0
unir(2,1)         0  1  1  4  4  8  6  2  8  0
unir(5,7)         0  1  1  4  4  8  6  2  1  0      (raíz de 5 = 8, raíz de 7 = 1)
unir(0,3)         4  1  1  4  4  8  6  2  1  0      (raíz de 0 = 0, raíz de 3 = 4)
unir(4,2)         4  1  1  4  1  8  6  2  1  0      (raíz de 4 = 4, raíz de 2 = 1)
```
Árboles finales:

```text
1                          6
├─ 2                     (solo)
│  └─ 7
├─ 4
│  ├─ 0
│  │  └─ 9
│  └─ 3
└─ 8
   └─ 5
```
La altura máxima es 3 (de 9 a 1 pasando por 0 y 4). Con otro orden de uniones podría salir una cadena de N nodos: por eso la unión rápida «a secas» tiene coste N · M en el peor caso.

**3. Unión rápida por tamaños.** Se cuelga siempre la raíz del árbol **más pequeño** de la del más grande. Cuando los dos árboles **empatan en tamaño**, hay que fijar un criterio; **las transparencias y la cabecera lo hacen al revés**:

| | Empate en tamaño |
|---|---|
| Transparencias (`tam[i] >= tam[j]`) | la raíz de `b` cuelga de la de `a` |
| `ConjuntosDisjuntos.h` (`tam[i] > tam[j]`) | la raíz de `a` cuelga de la de `b` |

Los dos son correctos (misma complejidad), solo cambian los árboles. Sin compresión de caminos, con el criterio de las **transparencias**:

```text
                 p[0..9]
inicial           0  1  2  3  4  5  6  7  8  9
unir(9,0)         9  1  2  3  4  5  6  7  8  9      0 cuelga de 9 (tamaños 1 y 1: empate → b cuelga de a)
unir(3,4)         9  1  2  3  3  5  6  7  8  9
unir(5,8)         9  1  2  3  3  5  6  7  5  9
unir(7,2)         9  1  7  3  3  5  6  7  5  9
unir(2,1)         9  7  7  3  3  5  6  7  5  9      raíz de 2 = 7 (tamaño 2) ≥ 1 → 1 cuelga de 7
unir(5,7)         9  7  7  3  3  7  6  7  5  9      raíz de 5 (tamaño 2) vs 7 (tamaño 3) → 5 cuelga de 7
unir(0,3)         9  7  7  9  3  7  6  7  5  9      raíz de 0 = 9 (tamaño 2), raíz de 3 = 3 (tamaño 2) → empate: 3 cuelga de 9
unir(4,2)         9  7  7  9  3  7  6  7  5  7      raíz de 4 = 9 (tamaño 4), raíz de 2 = 7 (tamaño 5) → 9 cuelga de 7
```
Árbol final grande (raíz 7, tamaño 9) y el `{6}` solo:

```text
7
├─ 1
├─ 2
├─ 5
│  └─ 8
└─ 9
   ├─ 0
   └─ 3
      └─ 4
```
Altura 3 (9 elementos: ≤ log₂ 9 ≈ 3,2). Con el criterio de la **cabecera** (`>`) los vectores finales salen: `p = 4 2 2 4 2 8 6 2 2 0`, con la raíz 2 y el mismo tamaño total 9.

---

## 6.2 Grafos valorados

Grafos cuyas aristas llevan un **valor** (distancia, tiempo, tarifa, anchura…). Pueden ser dirigidos o no; esta semana, **no dirigidos** (los dirigidos, la semana siguiente).

`GrafoValorado.h`:

| Clase / método | Qué es |
|---|---|
| `Arista<Valor>(v, w, valor)` | arista con dos extremos y un valor |
| `a.uno()`, `a.otro(u)` | un extremo; el otro extremo respecto de `u` |
| `a.valor()` | el valor |
| `a < b`, `a > b` | comparan **por valor** (sirven para ordenar o para una cola de prioridad) |
| `GrafoValorado<Valor>(V)` | grafo con V vértices sin aristas |
| `GrafoValorado<Valor>(cin, primer)` | lo lee: «V, A y A aristas `u v valor`»; `primer` = número del primer vértice (0 o 1) |
| `ponArista(a)` | añade la arista (se guarda **en las listas de sus dos extremos**) |
| `ady(v)` | lista de aristas incidentes en `v` (`vector<Arista>`) |
| `aristas()` | todas las aristas, **cada una una sola vez** |
| `V()`, `A()` | vértices y aristas |

Dentro, cada arista es un objeto compartido (`shared_ptr`), así que las dos listas de adyacencia apuntan a la **misma** arista.

Recorrido típico: `for (auto a : g.ady(v)) { int w = a.otro(v); … a.valor() … }`. Un DFS/BFS puede **filtrar** por valor (06-2).

---

## 6.3 Árbol de recubrimiento de coste mínimo (ARM)

Un **árbol de recubrimiento** de un grafo conexo es un subgrafo que conecta todos los vértices y no tiene ciclos. Si el grafo tiene V vértices, el árbol tiene exactamente **V − 1** aristas. Si las aristas tienen valor, el **ARM** es el de menor suma.

### Propiedad del corte
Un *corte* reparte los vértices en dos conjuntos no vacíos. **La arista de menor valor que cruza un corte cualquiera pertenece al ARM** (si hay empates, a algún ARM). Es lo que justifica Kruskal y Prim.

### Kruskal
1. Ordenar las aristas por valor creciente.
2. Partición unitaria de los vértices.
3. Para cada arista `(v, w)`: si `!unidos(v, w)` ⇒ `unir(v, w)` y se acepta; si no, cerraría un ciclo y se descarta.
4. Parar con V − 1 aristas aceptadas.

Coste: **O(V + A log A)** (ordenar domina; la partición es casi lineal). Si el grafo no es conexo se obtiene un *bosque* de recubrimiento mínimo (sale con menos de V − 1 aristas).

### Prim
1. Empezar en un vértice cualquiera: ese es el árbol.
2. Repetir: de entre las aristas que unen un vértice **del árbol** con otro **de fuera**, aceptar la de menor valor (se saca de una cola de prioridad).
3. Parar con V − 1 aristas.

Coste: **O(A log V)** con cola de prioridad. En un grafo no conexo, solo recubre la componente del vértice inicial.

| | Kruskal | Prim |
|---|---|---|
| Estructura | ordenar aristas + conjuntos disjuntos | cola de prioridad de aristas |
| Cómo crece | un bosque que se va fundiendo | un único árbol |
| Mejor cuando | pocas aristas | muchas aristas |

### Lo que más se reutiliza
- **Suma del ARM** (06-3).
- **Arista máxima del ARM** = mínima cuerda para conectar todo (06-4).
- **Camino minimax** entre dos vértices = arista máxima del camino en el ARM, y se obtiene parando Kruskal al conectarlos (06-5). Con aristas de mayor a menor se obtiene el *camino maximin* (la «anchura» de 06-2).
