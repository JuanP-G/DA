# EJ 04-3 · Detección de manchas negras

📄 [Enunciado](<../Enunciados/prob-Detección de manchas negras.pdf>) · 💻 [Solución](EJ_04-3.cpp) · 🎬 [Vídeo](../../Videos/04-3_manchas_negras.mp4)

## Qué piden
En un bitmap de píxeles blancos (`-`) y negros (`#`): **cuántas manchas negras** hay y **cuántos píxeles tiene la mayor**. Dos píxeles negros están en la misma mancha si se puede ir de uno a otro pasando solo por negros y moviéndose **en horizontal o vertical**.

## Cómo se plantea
Aunque el enunciado no lo dice, es un problema de grafos:

1. **Cada píxel es un vértice.** Para usar `Grafo` (vértices `0..V-1`) se numeran fila por fila:
   ```text
   píxel (i, j)  →  vértice  i·C + j          (y V = F·C)
   ```
2. **Dos píxeles negros vecinos** (arriba, abajo, izquierda o derecha) se unen con una arista.
3. Entonces **una mancha es una componente conexa** de píxeles negros.
4. La respuesta es el **número de componentes** (solo de píxeles negros) y el **tamaño de la mayor**.

Es el mismo esquema que el [EJ 04-2](../EJ_04-2/README.md) (un DFS por componente que devuelve su tamaño), pero además se cuentan las componentes.

### Poner cada arista una sola vez
Desde cada píxel negro solo se mira el de su **derecha** y el de **abajo**:
```text
          .
     .  [v] → v+1        (derecha:  mismo i, j+1  →  v + 1)
         ↓
        v+C              (abajo:    i+1, mismo j  →  v + C)
```
La arista con el de la izquierda y el de arriba ya la puso ese otro píxel. Si se miraran los cuatro vecinos, cada arista aparecería dos veces (el resultado sería el mismo, pero con el doble de trabajo).

## Por qué así
- **Las diagonales no cuentan.** En el primer ejemplo, dos manchas se tocan por una esquina (fila 2, columna 4 y fila 3, columna 5) y aun así son dos manchas. Por eso no se ponen aristas en diagonal.
- **Los píxeles blancos** quedan como vértices sin aristas. El bucle del constructor solo lanza el DFS desde píxeles **negros**, así que nunca cuentan como mancha.
- **¿DFS recursivo?** Sí: el enunciado garantiza que ninguna mancha pasa de 50.000 píxeles, y esa es justo la profundidad máxima de la recursión.
- **¿Hace falta el grafo?** Se podría recorrer la matriz directamente, mirando los vecinos sobre la marcha. Pero con `Grafo` el problema queda exactamente igual que el de componentes conexas del tema y se reutiliza el mismo DFS. Con F·C = 10⁶ el grafo ocupa unos 46 MB, sin problema.

## Traza (caso 2)
```text
#-#-#-###-        columnas 0, 2 y 4: tres manchas de 4 píxeles
#-#-#-#-#-        columnas 6 y 8: la fila de arriba (columna 7) las une
#-#-#-#-#-        → una mancha de 4 + 4 + 1 = 9
#-#-#-#-#-
                  ⇒  4 manchas, la mayor de 9   →   "4 9"
```

## Coste
**O(F·C)** por caso: cada píxel tiene como mucho 2 aristas "propias" (derecha y abajo) y el DFS pasa una vez por cada vértice y arista.
