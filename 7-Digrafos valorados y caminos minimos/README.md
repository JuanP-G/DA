# Tema 7 · Dígrafos valorados y caminos de coste mínimo

Resumen del tema (semana 7 del campus) con la respuesta a las dos reflexiones: «Caminos mínimos vs ARM» y «Dijkstra con vector». Los ejercicios del juez están en las carpetas `EJ_07-1` … `EJ_07-3`; en cada una hay la solución en C++ (`EJ_07-N.cpp`) y una explicación del planteamiento. El código de Dijkstra de las transparencias está en [`DigrafoValorado_algoritmos.h`](../Estructuras%20de%20datos/DigrafoValorado_algoritmos.h) (con su [demo](../Estructuras%20de%20datos/DigrafoValorado_demo.cpp)) y se puede ver paso a paso en la [herramienta interactiva](../Visualizaciones/tema7-dijkstra.html).

| Nº | Problema | Técnica |
|:--:|---|---|
| [07-1](EJ_07-1/README.md) | Navegando sin teclado | Dijkstra con **dos tipos de coste** (carga de la página + enlace): la carga se suma a la arista que entra |
| [07-2](EJ_07-2/README.md) | Camino al cole | Dijkstra que **cuenta** cuántos caminos mínimos hay (grafo no dirigido) |
| [07-3](EJ_07-3/README.md) | RapidEats con ruta | Dijkstra directo + **reconstruir el camino** con `ulti[]` |

---

## 7.1 Dígrafos valorados

Un **dígrafo valorado** es un grafo dirigido en el que cada arista lleva un valor (peso, coste, distancia, tiempo…). En [`DigrafoValorado.h`](../Estructuras%20de%20datos/DigrafoValorado.h):

| Clase / método | Qué hace |
|---|---|
| `AristaDirigida<Valor>(v, w, valor)` | arista de `v` a `w`; `desde()`, `hasta()`, `valor()`, y `<` / `>` por valor |
| `DigrafoValorado<Valor>(V)` | dígrafo sin aristas; también `DigrafoValorado(cin, primer)` lee «V, A y A aristas» |
| `ponArista(a)` | añade la arista (solo en la lista de `v`; **una** copia) |
| `ady(v)` | lista de aristas que **salen** de `v` |
| `V()`, `A()` | número de vértices y de aristas |
| `inverso()` | mismo grafo con todas las aristas al revés |
| `hayArista(v, w)` | ¿existe `v → w`? |

Diferencias con `GrafoValorado` (tema 6): allí la arista es un par `uno / otro` y se guarda en **las dos** listas; aquí tiene **sentido** y se guarda solo en la de `desde()`. **Para un grafo no dirigido** se llama dos veces a `ponArista` (`v → w` y `w → v`), como hacen 07-2 y 07-3.

## 7.2 Caminos de coste mínimo

Dado un dígrafo valorado y un origen `s`, hallar el camino más barato de `s` a cada vértice. Todos los caminos mínimos desde `s` forman un **árbol de caminos mínimos**, que se guarda con dos vectores:

- `dist[v]` — longitud del camino más corto conocido de `s` a `v` (∞ si no hay).
- `ulti[v]` — **última arista** de ese camino (con ella se reconstruye hacia atrás).

### Relajación de aristas
Si la arista `v → w` mejora el camino conocido hasta `w`, se actualizan los dos vectores:

```cpp
void relajar(AristaDirigida<Valor> a) {
    int v = a.desde(), w = a.hasta();
    if (dist[w] > dist[v] + a.valor()) {
        dist[w] = dist[v] + a.valor();
        ulti[w] = a;
    }
}
```

### Condiciones de optimalidad
`dist[]` contiene las distancias mínimas desde `s` si y solo si:

1. `dist[s] = 0`,
2. para todo `v`, `dist[v]` es la longitud de **algún** camino de `s` a `v`,
3. para toda arista `v → w`: `dist[w] ≤ dist[v] + valor` (ninguna arista se puede relajar más).

### Algoritmo de Dijkstra
Funciona si **todos los valores son ≥ 0**. Considera los vértices en **orden creciente de distancia** desde el origen: mete el origen en una cola de prioridad con prioridad 0 y, mientras haya cola, saca el vértice `v` de menor `dist` (ya definitiva) y **relaja todas las aristas que salen de él** (`pq.update(w, dist[w])` mete a `w` si no estaba o le cambia la prioridad). Es la `IndexPQ` del tema 3.

```cpp
Dijkstra(DigrafoValorado<Valor> const& g, int orig)
      : origen(orig), dist(g.V(), INF), ulti(g.V()), pq(g.V()) {
   dist[origen] = 0;
   pq.push(origen, 0);
   while (!pq.empty()) {
      int v = pq.top().elem; pq.pop();
      for (auto a : g.ady(v)) relajar(a);
   }
}
```

**Corrección.** Cada arista `v → w` se relaja **exactamente una vez** (al sacar `v`) y deja `dist[w] ≤ dist[v] + valor`. Esa desigualdad se mantiene hasta el final porque `dist[w]` no puede aumentar y `dist[v]` ya no cambia (es definitiva: con valores ≥ 0 nada que salga después de `v` de la cola puede ser más corto). Se cumplen las condiciones de optimalidad.

**Con valores negativos falla:** un vértice ya «tratado» podría mejorar después. Para eso están Bellman-Ford (otro tema).

**Coste: O(A log V)**, con espacio adicional O(V).

| Operación | Veces | Coste |
|---|:--:|:--:|
| inicializar los vectores | 1 | V |
| construir la cola de prioridad | 1 | V |
| `pop` | V | log V |
| `update` | ≤ A | log V |

### Reconstruir un camino
Con `ulti[]` se retrocede desde el destino hasta el origen (`07-3`):

```cpp
Camino<Valor> camino(int v) const {
    Camino<Valor> cam;
    for (int u = v; u != origen; u = ulti[u].desde())
        cam.push_front(ulti[u]);          // se mete por delante: queda de origen a v
    return cam;
}
```

### Variantes de los ejercicios
- **07-1 — dos tipos de coste.** El coste de un vértice (carga de una página) se carga en la arista que **entra** en él: `coste(v → w) = enlace + carga[w]`, y `dist[origen] = carga[origen]`. El grafo resultante tiene un único tipo de coste.
- **07-2 — contar caminos mínimos.** Segundo vector `formas[]`: si se mejora `dist[w]` → `formas[w] = formas[v]`; si se empata → `formas[w] += formas[v]`.
- **07-3 — dar el camino.** Dijkstra normal y, al final, retroceder por `ulti[]`.

---

## Reflexiones del campus

### ¿Es el árbol de caminos mínimos un árbol de recubrimiento de coste mínimo?
**No, en general.** Son dos árboles que responden a preguntas distintas:

| | Árbol de caminos mínimos (Dijkstra) | Árbol de recubrimiento de coste mínimo (Kruskal, Prim) |
|---|---|---|
| Grafo | dirigido o no | no dirigido |
| Qué minimiza | la distancia **desde el origen a cada vértice** | la **suma** de los valores de las aristas del árbol |
| ¿Depende del origen? | **sí** (cambia con `s`) | no |

**Contraejemplo.** Triángulo no dirigido con 0-1 (2), 1-2 (2) y 0-2 (3), origen 0:

```text
        1
      2/ \2           ARM:  0-1 y 1-2         coste total 4
      /   \                 pero el camino 0→2 cuesta 4 (hay uno de 3)
     0-----2
        3             Árbol de caminos mínimos desde 0:  0-1 (2) y 0-2 (3)   coste total 5
```
- El ARM no sirve como árbol de caminos mínimos: llegar a 2 por él cuesta 4, pero el camino directo cuesta 3.
- El árbol de caminos mínimos no sirve como ARM: pesa 5 en vez de 4.

Pueden **coincidir** (por ejemplo si el grafo ya es un árbol, o en casos especiales), pero no hay por qué. Otro error típico: sumar una constante a todas las aristas no cambia el ARM (el orden de las aristas es el mismo), pero **sí** puede cambiar los caminos mínimos (pasar por más aristas penaliza más).

### Dijkstra con un vector en lugar de la cola de prioridad
La cola de prioridad solo se usa para obtener «el vértice no tratado de menor `dist`». Se puede sustituir por un vector `dist[]` más un `tratado[]`: en cada paso se **recorre** el vector para encontrar el mínimo entre los no tratados (`O(V)`), se marca y se relajan sus aristas (sin `update`: basta asignar).

| Versión | Coste |
|---|:--:|
| Con `IndexPQ` (montículo) | **O(A log V)** |
| Con vector | **O(V² + A)** = O(V²) |

- En un grafo **disperso** (A ≈ V) gana el montículo: V log V frente a V².
- En un grafo **denso** (A ≈ V²) gana el vector: V² frente a V² log V. Además es más simple y con menos constantes.

Está implementado como `DijkstraVector` en [`DigrafoValorado_algoritmos.h`](../Estructuras%20de%20datos/DigrafoValorado_algoritmos.h), y la herramienta interactiva permite ejecutarlo y comparar cuántos recorridos del vector hace.

---

## Qué técnica usar

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| Camino de **menor coste total** con costes ≥ 0 | **Dijkstra** (`IndexPQ`) | 07-1, 07-2, 07-3 |
| Coste en los **vértices** además de en las aristas | Sumar el coste del vértice a la arista que entra (y el del origen a `dist[origen]`) | 07-1 |
| **Cuántos** caminos mínimos hay | Dijkstra + vector `formas[]` (sustituir si mejora, sumar si empata) | 07-2 |
| Escribir **el camino** | `ulti[]` y retroceder desde el destino | 07-3 |
| Grafo **no dirigido** | Añadir cada arista en los dos sentidos al `DigrafoValorado` | 07-2, 07-3 |
| Mínimo número de aristas (sin valores) | BFS (tema 4/5), no Dijkstra | — |
