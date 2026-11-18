# Grafos no dirigidos (tema 4) · resumen

🎬 Vídeo: [`04-0_grafos_no_dirigidos_teoria.mp4`](../Videos/04-0_grafos_no_dirigidos_teoria.mp4)

## Conceptos
- **Grafo**: vértices unidos por aristas sin dirección. Dos vértices unidos son **adyacentes**; el **grado** es el número de adyacentes.
- **Camino**: secuencia de vértices unidos por aristas. **Ciclo**: camino que vuelve al principio.
- **Componente conexa**: grupo máximo de vértices conectados entre sí. **Conexo**: una sola componente. **Árbol libre**: conexo y sin ciclos (`A = V − 1`).

## Representación
| | Memoria | En el curso |
|---|---|---|
| matriz de adyacencia | `V²` | no |
| **listas de adyacencia** | `V + A` | [`Grafo.h`](../Estructuras%20de%20datos/Grafo.h): `Grafo g(V)`, `g.ponArista(v, w)`, `g.ady(v)` |

## Recorridos
- **DFS** (profundidad, recursivo): marca `v` y, para cada adyacente `w` sin visitar, `ant[w] = v` y `dfs(w)`. Visita todo lo alcanzable; las aristas usadas forman un árbol.
- **BFS** (anchura, con cola): visita por capas, de más cerca a más lejos; `dist[w] = dist[v] + 1` da la **distancia mínima en número de aristas**.

Los dos cuestan **`O(V + A)`**. Están en [`Grafo_algoritmos.h`](../Estructuras%20de%20datos/Grafo_algoritmos.h): `CaminosDFS`, `CaminosBFS`, `ComponentesConexas`, `Bipartito`, `CicloGrafo`.

## Lo que sale de un recorrido
| Problema | Cómo | Ejercicios |
|---|---|---|
| Componentes conexas | un DFS (o BFS) desde cada vértice sin visitar | [04-1](EJ_04-1/README.md), [04-2](EJ_04-2/README.md), [04-3](EJ_04-3/README.md), [04-5](EJ_04-5/README.md) |
| Bipartito | colorear con 2 colores; falla si una arista une dos iguales | [04-7](EJ_04-7/README.md) |
| Ciclos / árbol libre | una arista hacia un visitado que no es el padre; o bien: conexo con `A = V − 1` | [04-1](EJ_04-1/README.md) |
| Distancias mínimas | BFS | [04-4](EJ_04-4/README.md), [04-6](EJ_04-6/README.md), [04-L](EJ_04-L/README.md) |

## Grafos implícitos
No hace falta construir el grafo si los vecinos se pueden calcular: en una imagen, cada píxel negro es un vértice (número `i·columnas + j`) y sus vecinos son los de arriba, abajo, izquierda y derecha; las manchas son las componentes conexas ([04-3](EJ_04-3/README.md)).
