# EJ 10-3 · Esquivando las obras en los cruces

📄 Enunciado: en el juez de la asignatura (`Ej10-3`) · 💻 [Solución](EJ_10-3.cpp)

## Qué piden
Una ciudad de N calles este-oeste y M calles norte-sur (1 ≤ N, M ≤ 50). Cada cruce es `.` (libre) o `X` (obras). Hay que contar los **caminos más cortos** de la esquina noroeste a la sureste que **no pasan por obras** (siempre < 10⁹).

## Recurrencia (formato de examen)

Cruces $(i, j)$ con $0 \le i < N$ (calle este-oeste) y $0 \le j < M$ (calle norte-sur):

$$
\text{caminos}(i, j) = \text{número de caminos mínimos de } (0, 0) \text{ a } (i, j) \text{ que no pasan por obras}
$$

**Casos base**

$$
\text{caminos}(0, 0) = 1
$$

$$
\text{caminos}(i, j) = 0 \qquad \text{si } i < 0 \text{ o } j < 0 \ (\text{fuera de la ciudad})
$$

**Recurrencia** ($(i, j) \ne (0, 0)$)

$$
\text{caminos}(i, j) =
\begin{cases}
0 & \text{si } (i, j) \text{ tiene obras} \\
\text{caminos}(i-1, j) + \text{caminos}(i, j-1) & \text{en otro caso}
\end{cases}
$$

A un cruce solo se llega **desde el norte** $(i-1, j)$ o **desde el oeste** $(i, j-1)$: un camino mínimo nunca retrocede.

**Llamada inicial / respuesta:** $\text{caminos}(N-1, M-1)$.

**Implementación:** por filas con un solo vector ($\text{caminos}[j]$ guarda la fila de arriba hasta que se sobrescribe). Coste $O(N \cdot M)$ en tiempo y $O(M)$ en espacio.

## Cómo se plantea
Un camino de longitud mínima **solo avanza hacia el sur o hacia el este**. Por eso a un cruce `(i, j)` solo se llega desde el de arriba o desde el de la izquierda:

```text
caminos(0, 0) = 1
caminos(i, j) = 0                                    si (i, j) tiene obras
              = caminos(i−1, j) + caminos(i, j−1)    si no   (fuera de la ciudad vale 0)
```

Se rellena fila a fila con **un solo vector**: `caminos[j]` aún tiene el valor de la fila de arriba y `caminos[j−1]` ya tiene el de la izquierda en la fila actual.

## Traza del ejemplo 1
```text
.....        1 1 1 1 1
.X...        1 0 1 2 3
..X.X   →    1 1 0 2 0
.....        1 2 2 4 4      → 4
```

## Por qué así
- **Por qué solo sur y este:** un camino de `(N−1) + (M−1)` manzanas no puede permitirse ni un paso hacia el norte ni hacia el oeste.
- **Coste:** O(N·M) en tiempo y O(M) en espacio.

## Ojo con
- En el ejemplo 2 sí hay un camino que esquiva las obras, pero es más largo de lo imprescindible: no cuenta, y la respuesta es 0.
