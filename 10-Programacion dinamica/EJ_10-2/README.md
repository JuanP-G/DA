# EJ 10-2 · Construyendo dianas

📄 Enunciado: en el juez de la asignatura (`Ej10-2`) · 💻 [Solución](EJ_10-2.cpp)

## Qué piden
Un valor V (1..50.000) y una diana con S sectores (1..100) de puntuaciones distintas en orden creciente (1..1.000). Cada sector se puede usar **las veces que haga falta**. Hay que escribir el **mínimo número de dardos** para sumar V y las puntuaciones usadas (`4: 25 25 25 25`), o `Imposible`. Vale cualquier solución óptima. **La entrada acaba con el fichero.**

## Cómo se plantea
Es el **problema del cambio** con monedas ilimitadas:

```text
dardos(i, j) = mínimo nº de dardos para sumar j con los sectores 1..i

dardos(0, 0) = 0          dardos(0, j) = INF   (j > 0)
dardos(i, j) = dardos(i−1, j)                                si p_i > j
             = min(dardos(i−1, j), dardos(i, j − p_i) + 1)   si p_i ≤ j
```
En la segunda opción se queda en la **fila i** porque el sector i se puede volver a usar.

**Reconstrucción** desde `(S, V)` hacia atrás:
- si `dardos(i, j) == dardos(i−1, j)`, el sector i no hace falta: se sube a la fila `i − 1`;
- si no, se ha usado el sector i: se escribe y se pasa a `(i, j − p_i)`.

## Traza del ejemplo 2 (V = 8, sectores 1 4 6)
```text
j:          0 1 2 3 4 5 6 7 8
con {1}:    0 1 2 3 4 5 6 7 8
con {1,4}:  0 1 2 3 1 2 3 4 2
con {1,4,6}:0 1 2 3 1 2 1 2 2
(3,8): 2 == fila anterior → no usa el 6
(2,8): 2 ≠ 8 → usa el 4 → (2,4): 1 ≠ 4 → usa el 4 → j = 0       → 2: 4 4
```
Con el 6 también hay soluciones (6 + 1 + 1), pero necesitan 3 dardos.

## Por qué así
- **Tabla entera para reconstruir:** con una sola fila se sabe el mínimo, pero no qué sectores lo dan.
- **Las puntuaciones salen de mayor a menor**, como en el ejemplo del enunciado.
- **Coste:** O(S·V) en tiempo y en espacio por caso (como mucho 5·10⁶ casillas).

## Ojo con
- No hay número de casos: `while (cin >> V >> S)`.
- El formato es `k:` y luego cada puntuación precedida de un espacio.
