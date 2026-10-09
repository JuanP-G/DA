# EJ 04-7 · Grafo bipartito

📄 [Enunciado](<../Enunciados/prob-Grafo bipartito.pdf>) · 💻 [Solución](EJ_04-7.cpp) · 🎬 [Vídeo](../../Videos/04-7_grafo_bipartito.mp4)

## Qué piden
Si los vértices se pueden **pintar con dos colores** de forma que ninguna arista una dos vértices del mismo color.

## Cómo se plantea
La observación clave es que **el color de un vértice obliga el de sus vecinos**: si `v` es blanco, todos sus adyacentes tienen que ser negros. No hay que probar combinaciones.

1. Al primer vértice de cada componente se le da un color cualquiera.
2. Con un DFS, a cada vecino **nuevo** se le asigna el color **contrario** al del vértice desde el que se llega.
3. Si se encuentra un vecino **ya visitado** y del **mismo color**, hay conflicto y el grafo **no es bipartito**.

Hay que hacerlo **en cada componente**: el grafo puede no ser conexo, así que el DFS se lanza desde cada vértice sin visitar.

## Por qué así
- **¿Por qué es correcto?** Dentro de una componente, el color del primer vértice decide todos los demás, así que solo hay dos coloreados posibles y uno es el otro con los colores invertidos. Si el que fuerza el DFS falla, falla cualquier otro.
- **Interpretación:** el conflicto aparece justo cuando hay un **ciclo de longitud impar**, como el triángulo 0‑2‑3 del segundo ejemplo.
- Se puede **cortar** en cuanto se ve un conflicto (`if (!bipar) return;`), porque la respuesta ya es NO.
- V ≤ 100, así que la recursión no preocupa aquí.

## Traza del ejemplo (caso 2)
```text
0 → blanco
2 → negro   (vecino de 0)
3 → blanco  (vecino de 2)
la arista 0-3 une dos blancos  ⇒  NO
```

## Coste
**O(V + A)** por caso.
