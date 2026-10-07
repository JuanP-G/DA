# EJ 04-4 · Los números de Bacon

📄 [Enunciado](<../Ejercicios juez/4-Grafos no dirigidos/prob-Los números de Bacon.pdf>) · 💻 [Solución](EJ_04-4.cpp) · 🎬 [Vídeo](../Videos/04-4_numeros_de_bacon.mp4)

## Qué piden
Para varios actores, la **cadena más corta de películas** que los une con Kevin Bacon, o `INF` si no la hay.

## Cómo se plantea
Es un **camino mínimo sin pesos**, así que se resuelve con **BFS**. El BFS visita los vértices por capas de distancia, así que la primera vez que llega a uno lo hace por el camino más corto (un DFS podría llegar antes por un camino largo). Hay tres detalles que hacen el ejercicio más interesante que un BFS normal:

### 1. Los vértices tienen nombre
`Grafo` trabaja con números `0..V-1`, así que se usa un `unordered_map<string,int>`: cada nombre nuevo recibe el siguiente número.

### 2. Cómo poner las aristas (la clave del ejercicio)
Lo directo sería unir **cada par** de actores de una película. Pero una película de *k* actores da *k(k−1)/2* aristas: con 100.000 actores son unos 5.000 millones.

**Truco:** las **películas también son vértices**.
```text
actor ── película ── actor
```
Una película de *k* actores son solo *k* aristas. A cambio, pasar de un actor a otro cuesta **2 aristas**, así que:

> **número de Bacon = distancia / 2**

### 3. Hay que saber V antes de crear el grafo
`Grafo(V)` necesita el número de vértices, pero no se sabe cuántos actores hay hasta leer todas las películas. Por eso:
1. Se leen todas las películas y se guarda el reparto de cada una (ya en números).
2. Se crea `Grafo g(actores + peliculas)`. Los vértices `0..actores-1` son actores y `actores + p` es la película `p`.
3. Se ponen las aristas actor–película.

Después se hace **un único BFS desde KevinBacon**. Así cada consulta es solo mirar `dist[actor]`, en lugar de un BFS por consulta (con 100.000 consultas sería demasiado lento).

## Por qué así
- Si **KevinBacon no aparece** en ninguna película, todos los números son `INF` (segundo caso del ejemplo).
- Si un actor no es alcanzable desde Bacon (`dist == -1`), su número es `INF`.
- El BFS da la distancia **mínima**: Dustin Hoffman está a 1 por *Sleepers*, aunque también se llegue a él en 2 pasos por *Rain Man*.

## Traza (caso 1)
```text
KevinBacon (0) ─ Sleepers ─ DustinHoffman      dist 2 → 1
KevinBacon ─ AlgunosHombresBuenos ─ JackNicholson ─ MejorImposible ─ HelenHunt
                                                                    dist 4 → 2
HelenHunt ─ LoQueLaNocheEsconde ─ AnaDeArmas                        dist 6 → 3
JohnDoe: no hay camino                                              → INF
```

## Coste
**O(V + A)** para el BFS, con V ≤ actores + películas ≈ 105.000 y A = suma de los tamaños de los repartos. Cada consulta cuesta O(1) de media (búsqueda en el `unordered_map`).
