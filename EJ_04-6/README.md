# EJ 04-6 · Un nodo muy muy lejano

📄 [Enunciado](<../Ejercicios juez/4-Grafos no dirigidos/prob-Un nodo muy muy lejano.pdf>) · 💻 [Solución](EJ_04-6.cpp) · 🎬 [Vídeo](../Videos/04-6_nodo_muy_lejano.mp4)

## Qué piden
Dado un nodo origen y un TTL, cuántos nodos **no** recibe el mensaje.

## Cómo se plantea
Lo importante es traducir la historia del TTL a algo de grafos. Cada salto de un nodo a su vecino gasta 1 de TTL, así que:

> **w recibe el mensaje ⇔ distancia(origen, w) ≤ TTL**

(distancia = número mínimo de aristas). En el ejemplo, desde 6 con TTL 2 llegan los nodos a 1 o 2 aristas de distancia.

Distancias mínimas en un grafo **sin pesos** se calculan con **BFS** (recorrido en anchura):

1. `dist[origen] = 0` y se mete el origen en una cola.
2. Se saca `v`. Si `dist[v] == TTL`, el mensaje no sigue desde ahí. Si no, cada vecino no visitado `w` recibe `dist[w] = dist[v] + 1` y entra en la cola.
3. Respuesta = **N − alcanzados**.

## Por qué así
- **¿Por qué BFS y no DFS?** El BFS visita los vértices **por orden de distancia**, así que la primera vez que llega a un vértice lo hace por el camino más corto. Un DFS puede llegar primero por un camino largo: diría que un nodo está a distancia 5 cuando hay un atajo de 2, y lo daría por inalcanzable.
- **Cortar en `dist[v] == TTL`** evita recorrer el resto del grafo inútilmente.
- **TTL = 0:** solo se cuenta el propio origen (la consulta `1 0` del ejemplo da 6 de 7).
- Hay **varias consultas sobre el mismo grafo**: el grafo se lee una vez y se hace un BFS nuevo por consulta (como mucho 10).

## Traza del ejemplo (consulta `4 2`)
```text
dist 0: 4
dist 1: 1, 5, 6
dist 2: 2, 7      ← aquí el TTL se acaba
no llega: 3       ⇒  1
```

## Coste
**O(N + C)** por consulta, y como mucho 10 consultas por red.
