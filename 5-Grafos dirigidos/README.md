# Tema 5 · Grafos dirigidos

Resumen del tema (semana 5 del campus). Los ejercicios del juez están en las carpetas `EJ_05-1` … `EJ_05-6` y `EJ_05-L`; en cada una hay la solución en C++ (`EJ_05-N.cpp`) y una explicación del planteamiento. Todos usan [`Digrafo.h`](../Estructuras%20de%20datos/Digrafo.h); los algoritmos del tema están juntos en [`Digrafo_algoritmos.h`](../Estructuras%20de%20datos/Digrafo_algoritmos.h) (con su [demo](../Estructuras%20de%20datos/Digrafo_demo.cpp)), la calculadora como grafo implícito en [`Digrafo_implicito_calculadora.cpp`](../Estructuras%20de%20datos/Digrafo_implicito_calculadora.cpp), y todo se puede ver paso a paso en la [herramienta interactiva](../Visualizaciones/tema5-digrafo.html) y en el [vídeo de teoría](../Videos/05-0_grafos_dirigidos_teoria.mp4).

| Nº | Problema | Técnica |
|:--:|---|---|
| [05-1](EJ_05-1/README.md) | La máquina calculadora | **BFS** sobre un `Digrafo` con los 10.000 números del marcador (+1, ×2, ÷3) |
| [05-2](EJ_05-2/README.md) | Juego de Transformación Modular | BFS en un `Digrafo` construido con x → (a·x+b) mod M |
| [05-3](EJ_05-3/README.md) | Ordenando tareas | **Orden topológico** (postorden inverso del DFS) con detección de ciclos |
| [05-4](EJ_05-4/README.md) | Sumidero en un grafo dirigido | **Grados** de salida y de entrada |
| [05-5](EJ_05-5/README.md) | Haciendo trampas en Serpientes y Escaleras | BFS: casilla `v` → `destino[v + d]` |
| [05-6](EJ_05-6/README.md) | Sistema de inecuaciones | Ciclo ⇒ NO; si no, valores a partir del postorden |
| [05-L](EJ_05-L/README.md) | El Necronomicón de la informática | Programa = digrafo; un DFS desde la instrucción 1: ¿se alcanza el final? ¿hay un ciclo alcanzable? |

---

## 5.1 Grafos dirigidos

Un **grafo dirigido** (digrafo) tiene aristas con **sentido**: `v → w` no es lo mismo que `w → v`.

- **Grado de salida** de `v`: aristas que salen de `v`.  **Grado de entrada**: aristas que llegan a `v`.
- **Camino dirigido** de `s` a `t`: sucesión de aristas siguiendo su sentido. `t` es **alcanzable** desde `s` si existe.
- **Ciclo dirigido**: camino que vuelve a su origen. Un digrafo sin ciclos es un **DAG**.
- **Componente fuertemente conexa**: conjunto máximo de vértices donde todos se alcanzan entre sí (se puede ir y volver).

Aplicaciones: tareas con precedencias, dependencias entre módulos, estados de un juego, enlaces web, calles de sentido único…

## 5.2 El TAD `Digrafo`

| Método | Qué hace |
|---|---|
| `Digrafo(V)` | digrafo con `V` vértices y sin aristas; también `Digrafo(cin, primer)` lee «V, A y A pares» |
| `ponArista(v, w)` | añade `v → w` **solo** en la lista de `v` (en `Grafo` se añade en las dos) |
| `ady(v)` | lista de vértices **a los que sale** una arista desde `v` |
| `V()`, `A()` | número de vértices y de aristas |
| `inverso()` | mismo grafo con todas las aristas al revés |
| `hayArista(v, w)` | ¿existe `v → w`? |

### Representaciones

| Representación | Espacio | Añadir `v → w` | ¿existe `v → w`? | Recorrer adyacentes |
|---|:--:|:--:|:--:|:--:|
| matriz de adyacencia | V² | 1 | 1 | V |
| **listas de adyacentes** | V + A | 1 | grado-sal(v) | grado-sal(v) |
| lista de aristas | A | 1 | A | A |

Los algoritmos del tema se basan en recorrer los adyacentes de un vértice y los grafos reales suelen ser **dispersos** (A ≪ V²): por eso se usan **listas de adyacentes**.

## 5.3 Recorridos: DFS y BFS dirigidos

Son los mismos que en el tema 4, pero siguiendo el sentido de las aristas. Coste **O(V + A)**.

```cpp
void dfs(Digrafo const& g, int v) {      // alcanzabilidad
   visit[v] = true;
   for (int w : g.ady(v))
      if (!visit[w]) dfs(g, w);
}
```

```cpp
void bfs(Digrafo const& g) {              // camino con MENOS aristas
   queue<int> q;
   dist[s] = 0; visit[s] = true; q.push(s);
   while (!q.empty()) {
      int v = q.front(); q.pop();
      for (int w : g.ady(v))
         if (!visit[w]) { ant[w] = v; dist[w] = dist[v] + 1; visit[w] = true; q.push(w); }
   }
}
```

- `dist[v]` es el número mínimo de aristas de `s` a `v`; `ant[v]` permite **reconstruir el camino** retrocediendo desde el destino (`push_front`).
- Con BFS la primera vez que se llega a un vértice es por un camino mínimo; con DFS no.

### Grafo implícito
Si el grafo sale de una **regla** (la calculadora: de `x` se va a `x+1`, `2x` y `x/3`; el Transformación Modular: `x → (a·x+b) mod M`; las tiradas del dado), no hace falta construirlo entero: se calculan los **sucesores al vuelo** dentro del BFS. En 05-1 y 05-2 se construye el `Digrafo` con `ponArista` porque los estados son pocos (10.000); es igual de válido y más fácil de leer.

## 5.4 Orden topológico

Dada una relación «A debe hacerse antes que B» (arista `A → B`), un **orden topológico** coloca los vértices de modo que **todas las flechas van de izquierda a derecha**. Existe si y solo si el grafo es un **DAG**.

**Se obtiene con el postorden inverso de un DFS:** se añade cada vértice a una lista **al terminar** su DFS y se lee al revés (`push_front`).

```cpp
void dfs(Digrafo const& g, int v) {
   visit[v] = true;
   for (int w : g.ady(v))
      if (!visit[w]) dfs(g, w);
   _orden.push_front(v);                  // al terminar v
}
```

**Por qué funciona.** Para cualquier arista `v → w`, al hacer `dfs(v)` pasa una de estas tres cosas:

1. `dfs(w)` **ya terminó** ⇒ `w` terminó antes que `v`.
2. `dfs(w)` **aún no empezó** ⇒ `v` lo llama y `w` termina antes que `v`.
3. `dfs(w)` **empezó y no ha terminado** ⇒ `w` es un antecesor de `v`: hay un camino `w → … → v` y con `v → w` un **ciclo**. Imposible en un DAG.

En los casos 1 y 2, `w` termina antes que `v`, así que en el postorden **inverso** `w` queda **después** de `v`: la flecha va hacia la derecha.

## 5.5 Detección de ciclos

Un ciclo hace imposible un orden. Se detecta con el mismo DFS, usando la **pila de la recursión** (el camino actual): hacen falta dos marcas, `visit` («ya lo alcancé») y `apilado` («está ahora en la pila»).

Para cada vecino `w` de `v`:

| `w` está… | significa | acción |
|---|---|---|
| sin visitar | vértice nuevo | `ant[w] = v` y `dfs(w)` |
| visitado y **apilado** | `w` es antecesor de `v` | la arista `v → w` **cierra un ciclo** |
| visitado y **no apilado** | `w` ya terminó | sin ciclo por ahí |

`ant[]` permite recuperar el ciclo (`CicloDirigido::ciclo()`). Con tres estados (0 sin visitar, 1 en la pila, 2 terminado) se escribe en una sola variable `estado[]`, como en 05-3, 05-6 y 05-L. **Ojo:** ver un vértice ya visitado **no** es un ciclo (en un DAG hay muchos): solo cuenta si **sigue en la pila**.

## 5.6 Extra: componentes fuertemente conexas

Algoritmo de Kosaraju (`CFC` en `Digrafo_algoritmos.h`): se calcula el postorden inverso de un DFS sobre el grafo **inverso**, y se hace un DFS sobre el grafo original recorriendo los vértices en ese orden; **cada árbol del bosque es una componente**. Coste O(V + A). No lo pide ningún ejercicio, pero responde a «¿se puede ir y volver?».

---

## Qué técnica usar

| Lo que pide el problema | Herramienta | Ejercicios |
|---|---|---|
| Mínimo número de pasos / jugadas / tiradas | **BFS** (camino con menos aristas) | 05-1, 05-2, 05-5 |
| Estados con reglas de movimiento (el grafo sale de una fórmula) | Construir el `Digrafo` con `ponArista`, o grafo **implícito** | 05-1, 05-2, 05-5 |
| Ordenar con precedencias («A antes que B», xi < xj) | **Orden topológico**; vecino en la pila ⇒ ciclo ⇒ imposible | 05-3, 05-6 |
| Grados de los vértices (p. ej. sumidero) | Salida = `ady(v).size()`; entrada = contar en todas las listas | 05-4 |
| ¿Se puede terminar? ¿se puede no terminar nunca? | **DFS desde el inicio**: ¿se alcanza el final? ¿hay un ciclo **alcanzable**? | 05-L |
| La entrada es «V, A y A pares» | Leer con el constructor `Digrafo g(cin, primer)` | 05-4, 05-6 |

### Cómo reconocerlo en el enunciado

| El enunciado dice… | Piensa en… |
|---|---|
| «mínimo número de pasos / jugadas / pulsaciones» | BFS |
| «¿se puede llegar de A a B?» | DFS o BFS, mirar `visit[]` |
| «A debe hacerse antes que B» | arista A → B + orden topológico |
| «imposible», «dependencia circular» | ciclo dirigido: vecino en la pila |
| «siempre / nunca / a veces termina» | alcanzabilidad del final + ciclo alcanzable |
| estados con reglas de movimiento | grafo implícito + BFS |

### Errores típicos
- **Índices:** si los vértices vienen numerados desde 1, resta 1 (o usa el parámetro `primer` del constructor).
- **Recursión profunda:** el DFS recursivo llega a V niveles; en el juez no da problemas, pero en Visual Studio (pila de 1 MB) un caso enorme puede desbordar. Con V muy grande, mejor BFS o DFS iterativo.
- **DFS no da el camino más corto:** para «mínimo» usa BFS.
- **Un digrafo no es un grafo:** `ponArista(v, w)` añade **una** arista; si el grafo es no dirigido hay que añadir las dos.
