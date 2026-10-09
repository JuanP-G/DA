# EJ 04-5 · ¡Las noticias vuelan!

📄 [Enunciado](<../Enunciados/prob-¡Las noticias vuelan!.pdf>) · 💻 [Solución](EJ_04-5.cpp) · 🎬 [Vídeo](../../Videos/04-5_las_noticias_vuelan.mp4)

## Qué piden
Para **cada** usuario, a cuántos usuarios llegaría una noticia que empezara en él.

## Cómo se plantea
1. **Modelo:** cada usuario es un vértice. Dos usuarios están unidos si comparten algún grupo.
2. La noticia se extiende hasta que no queda ningún amigo sin enterarse, así que llega exactamente a la **componente conexa** del usuario que la empieza.
3. Respuesta de *i* = **tamaño de la componente conexa de *i***.

Hasta aquí es casi el EJ 04-2. Hay dos diferencias que lo hacen más difícil.

### 1. Construir el grafo sin explotar
Unir todos los pares de un grupo de *k* usuarios da *k(k−1)/2* aristas: con un grupo de 100.000 son 5.000 millones.

**Truco:** aquí solo importa **quién está conectado con quién, no la distancia**. Basta con unir a todos los miembros del grupo **con el primero** (una *estrella*). Son *k − 1* aristas y el grupo sigue en una sola componente.

```text
grupo {2,5,4}:   2 ─ 5
                 2 ─ 4        (no hace falta 5 ─ 4)
```
(En el EJ 04-4 esto **no** servía, porque allí sí importan las distancias. Por eso allí las películas son vértices.)

### 2. Responder a todos sin repetir trabajo
Hacer un recorrido **por usuario** sería cuadrático. Se hace **un recorrido por componente**:
- `comp[v]` = número de componente de `v`.
- `tam[c]` = tamaño de la componente `c`.
- La respuesta de `v` es `tam[comp[v]]`.

### 3. BFS iterativo en vez de DFS recursivo
Una componente puede tener 100.000 vértices, y un DFS recursivo bajaría 100.000 niveles, con riesgo de **desbordar la pila**. Para *contar* una componente da igual el orden, así que se usa un **BFS con cola**, que no tiene ese problema.

## Detalles
- Los **grupos vacíos** o de **un solo usuario** no ponen ninguna arista.
- Un usuario que **no está en ningún grupo** forma su propia componente de tamaño 1.
- La salida va **en una línea**, separada por espacios.

## Traza (caso 1)
```text
grupos {2,5,4} {} {1,2} {1} {6,7}
componentes: {1,2,4,5} → 4    {3} → 1    {6,7} → 2
salida:      4 4 1 4 4 2 2
```

## Coste
**O(N + Σ tamaños de grupo)** por caso, lineal en el tamaño de la entrada.
