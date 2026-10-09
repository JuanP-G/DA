# EJ 04-2 · Los amigos de mis amigos son mis amigos

📄 [Enunciado](<../Enunciados/prob-Los amigos de mis amigos son mis amigos.pdf>) · 💻 [Solución](EJ_04-2.cpp) · 🎬 [Vídeo](../../Videos/04-2_amigos_de_mis_amigos.mp4)

## Qué piden
Cuántas personas tiene el **grupo de amigos más grande**, sabiendo que la amistad es transitiva.

## Cómo se plantea
1. **Modelo:** cada persona es un vértice y cada amistad una arista.
2. Por el refrán, A y C son amigos si hay una cadena A–B–…–C. Eso es justo que haya un **camino** entre ellos.
3. Por tanto, un grupo de amigos es una **componente conexa** del grafo.
4. La respuesta es el **tamaño de la componente conexa más grande**.

Algoritmo:
- Se recorren los vértices y, para cada uno **no visitado**, se lanza un DFS.
- Ese DFS visita su componente entera y **devuelve cuántos vértices ha visitado**.
- Se guarda el máximo.

```text
dfs(v):  visit[v] = true; tam = 1
         para cada w adyacente a v no visitado: tam += dfs(w)
         devolver tam
```

Este es el ejemplo clásico de teoría (`MaximaCompConexa`).

## Por qué así
- **Lanzar un DFS por cada vértice no visitado** es la forma de recorrer *todas* las componentes, no solo la del vértice 0.
- Con el vector `visit` compartido, cada vértice se visita una sola vez en total, aunque haya muchas componentes.
- **Parejas repetidas** (`2 3` y `3 2`): `Grafo` guarda la arista repetida, pero no importa, porque el DFS no vuelve a entrar en un vértice ya visitado.
- **Personas sin amigos** forman su propia componente de tamaño 1. Salen solas del bucle, sin ningún caso especial.
- Las personas van de 1 a N y `Grafo(cin, 1)` les resta 1 al leerlas.

## Traza del ejemplo (caso 2)
Componentes: {1,2,3,4,5,6} y {7,8,9,10} → tamaños 6 y 4 → **6**.

## Coste
**O(N + M)** por caso.

> ⚠️ El DFS recursivo puede llegar a profundidad N (hasta 20.000). En el juez no da problemas; en Visual Studio en modo Debug (pila de 1 MB) podría desbordar la pila.
