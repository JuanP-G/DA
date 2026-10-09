# EJ 04-1 · Árboles libres

📄 [Enunciado](<../Enunciados/prob-Árboles libres.pdf>) · 💻 [Solución](EJ_04-1.cpp) · 🎬 [Vídeo](../../Videos/04-1_arboles_libres.mp4)

## Qué piden
Decidir si un grafo no dirigido es **árbol libre**, es decir, **acíclico y conexo**.

## Cómo se plantea
Hay dos cosas que comprobar, pero gracias a una propiedad de los árboles solo hace falta recorrer el grafo una vez.

> En un grafo con **V** vértices, dos cualesquiera de estas tres condiciones implican la tercera:
> 1. es conexo
> 2. es acíclico
> 3. tiene exactamente **V − 1** aristas

Por tanto, *árbol libre* ⇔ **conexo y A = V − 1**. Comprobar el número de aristas es inmediato (`g.A()`), así que solo queda saber si el grafo es conexo:

- Se lanza un **DFS desde el vértice 0** y se cuentan los vértices visitados.
- Si se visitan los **V**, el grafo es conexo.

## Por qué así
- **¿Por qué no buscar ciclos directamente?** Se puede (un DFS que encuentra un vecino ya visitado que no es su padre ha encontrado un ciclo), pero hay que llevar el padre de cada vértice y además seguir comprobando la conexión. Contar aristas es más sencillo y más difícil de equivocar.
- **¿DFS o BFS?** Para saber *a qué vértices se llega* da igual el orden de visita. Se usa DFS porque es el recorrido más corto de escribir.
- `Grafo(cin)` lee exactamente el formato del enunciado: `V`, `A` y luego `A` pares de vértices desde 0.

## Traza del ejemplo
| Caso | V | A | ¿A = V−1? | DFS desde 0 visita | Resultado |
|---|---|---|---|---|---|
| 1 | 6 | 5 | sí | 0,5,2,1,3,4 → 6 | **SI** |
| 2 | 6 | 5 | sí | 0,1,2,3 → 4 (el {4,5} queda aparte) | **NO** |
| 3 | 1 | 0 | sí | 0 → 1 | **SI** |

El caso 2 es la trampa: tiene V − 1 aristas, pero hay un ciclo 0‑1‑2‑3 y por eso no llega a conectarlo todo.

## Coste
**O(V + A)** por caso: el DFS pasa una vez por cada vértice y por cada arista.

> ⚠️ El DFS recursivo puede llegar a profundidad V (hasta 10.000). En el juez no da problemas; en Visual Studio en modo Debug (pila de 1 MB) un camino tan largo podría desbordar la pila.
