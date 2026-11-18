# EJ 10-4 · ¿Por dónde hay que subir?

📄 Enunciado: en el juez de la asignatura (`Ej10-4`) · 💻 [Solución](EJ_10-4.cpp)

## Qué piden
Un tablero N × N (3 ≤ N ≤ 1.000) con números 1..10.000. Se empieza en una casilla de la **última fila** y se sube hasta la **primera**. En cada paso se va a una de las tres casillas de la fila de encima (vertical o diagonal) sin salirse. Hay que escribir la **suma máxima** y la **columna** de la última fila por la que empezar; si hay empate, la de más a la izquierda.

## Cómo se plantea
```text
mejor(i, j) = suma máxima de un recorrido que empieza en (i, j) y sube hasta la fila 1

mejor(1, j) = t(1, j)
mejor(i, j) = t(i, j) + max( mejor(i−1, j−1), mejor(i−1, j), mejor(i−1, j+1) )
              (solo las columnas que existen)
```
La respuesta es el máximo de `mejor(N, j)`. Se recorre `j` de izquierda a derecha con `>` estricto, así que en un empate se queda la columna de más a la izquierda.

Se rellena fila a fila guardando solo la fila anterior.

## Traza del ejemplo 1
```text
tablero        mejor
2 5 8 3        2  5  8  3
1 4 2 9        6 12 10 17
9 2 8 5       21 14 25 22
3 5 2 1       24 30 27 26      → 30 en la columna 2
```
Desde el 5 la casilla mayor de encima es el 9, pero subiendo por ahí solo se llega a 26: hay que mirar la tabla, no ir a lo voraz.

## Por qué así
- **Rellenar desde arriba:** `mejor(i, j)` necesita la fila `i − 1`, así que se empieza por la fila 1. La respuesta queda en la última fila, que es la que pregunta el enunciado.
- **Coste:** O(N²) en tiempo y O(N) en espacio. La suma máxima es ≤ 10⁷: cabe en `int`.

## Ojo con
- Las columnas 1 y N solo tienen dos casillas encima.
