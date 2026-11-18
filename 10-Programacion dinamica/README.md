# Programación dinámica (temas 10 y 11) · resumen

🎬 Vídeo: [`10-0_programacion_dinamica_teoria.mp4`](../Videos/10-0_programacion_dinamica_teoria.mp4)

## Cuándo se usa
- **Subproblemas repetidos**: la recursión directa calcula lo mismo muchas veces (fibonacci: `fib(3)` dos veces y `fib(2)` tres en `fib(5)`; coste exponencial).
- **Principio de optimalidad** (en problemas de optimización): una solución óptima está formada por soluciones óptimas de sus subproblemas.

Con las dos cosas, se apunta cada resultado en una tabla la primera vez que se calcula y la recursión pasa a costar lo que cuesta rellenar la tabla.

## La receta
1. **Definición**: decir con palabras qué calcula la función y qué es cada parámetro.
2. **Recurrencia**: casos base y casos recursivos, cada uno con su condición.
3. **Tabla**: orden de relleno, de forma que cada casilla se calcule después de las que necesita.
4. **Respuesta**: qué casilla es la solución y, si lo piden, cómo reconstruirla.

Se puede programar **descendente** (recursión + memoria: antes de calcular se mira si ya está apuntado) o **ascendente** (bucles desde los casos base). En el curso se usa la ascendente.

## Ahorro de memoria
Si cada fila solo usa la de arriba, basta un vector, pero el **sentido** importa:
- **0/1** (cada objeto una vez): `j` de **derecha a izquierda**, para leer valores todavía de la fila anterior.
- **Ilimitados** (monedas): `j` de **izquierda a derecha**, para leer el valor ya actualizado.

Para **reconstruir** la solución hace falta la tabla entera: desde la casilla de la respuesta, si vale lo mismo que la de arriba ese objeto no se usó; si es distinta, se usó y se salta su peso.

## Patrones de los ejercicios
| Patrón | Depende de | Ejercicios |
|---|---|---|
| Mochila 0/1 | fila `i − 1` | [10-1](EJ_10-1/README.md), [11-1](../11-Programacion%20dinamica%20II/EJ_11-1/README.md) |
| Monedas ilimitadas | misma fila | [10-2](EJ_10-2/README.md) |
| Cuadrícula | arriba / izquierda (o las tres de encima) | [10-3](EJ_10-3/README.md), [10-4](EJ_10-4/README.md) |
| Intervalos | intervalos más cortos (por diagonales) | [11-2](../11-Programacion%20dinamica%20II/EJ_11-2/README.md) |

## Formato de examen
1. Definición: `mochila(i, j)` = máximo valor con los objetos `1..i` sin pasar del peso `j`.
2. Casos base: `mochila(0, j) = 0` para `0 ≤ j ≤ M`.
3. Recurrencia con todas las condiciones:

$$
mochila(i, j) = \begin{cases} mochila(i-1, j) & \text{si } p_i > j \\ \max\big(mochila(i-1, j),\ mochila(i-1, j-p_i) + v_i\big) & \text{si } p_i \le j \end{cases}
$$

4. Llamada inicial: `mochila(N, M)`.
5. Coste: `O(N·M)` en tiempo; memoria `O(N·M)`, u `O(M)` con un vector si no hay que reconstruir.

Cada ejercicio de los temas 10 y 11 tiene su recurrencia escrita así en su README.
