# EJ 10-2 · Construyendo dianas

📄 Enunciado: en el juez de la asignatura (`Ej10-2`) · 💻 [Solución](EJ_10-2.cpp)

## Qué piden
Un valor V (1..50.000) y una diana con S sectores (1..100) de puntuaciones distintas en orden creciente (1..1.000). Cada sector se puede usar **las veces que haga falta**. Hay que escribir el **mínimo número de dardos** para sumar V y las puntuaciones usadas (`4: 25 25 25 25`), o `Imposible`. Vale cualquier solución óptima. **La entrada acaba con el fichero.**

## Recurrencia (formato de examen)

Sectores numerados $1..S$ con puntuaciones $p_1 < p_2 < \dots < p_S$. Para $0 \le i \le S$ y $0 \le j \le V$:

$$
\text{dardos}(i, j) = \text{mínimo número de dardos para sumar exactamente } j \text{ usando los sectores } 1..i
$$

**Casos base**

$$
\text{dardos}(i, 0) = 0 \qquad \forall\, i \ge 0
$$

$$
\text{dardos}(0, j) = +\infty \qquad \forall\, j > 0
$$

**Recurrencia** ($1 \le i \le S$, $1 \le j \le V$)

$$
\text{dardos}(i, j) =
\begin{cases}
\text{dardos}(i-1, j) & \text{si } p_i > j \\
\min\big(\text{dardos}(i-1, j),\ \text{dardos}(i,\ j - p_i) + 1\big) & \text{si } p_i \le j
\end{cases}
$$

O **no se usa** el sector $i$ (fila $i-1$), o se tira **un dardo más** a él y se sigue en la **fila $i$**, porque se puede volver a usar.

**Llamada inicial / respuesta:** $\text{dardos}(S, V)$; si vale $+\infty$, `Imposible`.

**Reconstrucción** desde $(i, j) = (S, V)$ mientras $j > 0$: si $\text{dardos}(i, j) = \text{dardos}(i-1, j)$ se pasa a $(i-1, j)$; si no, se apunta $p_i$ y se pasa a $(i, j - p_i)$.

**Coste:** $O(S \cdot V)$ en tiempo y en espacio (la tabla entera, para reconstruir).

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

## El código, paso a paso

**1. Lectura.** No hay número de casos, así que se lee `while (cin >> V >> S)`. Las puntuaciones se guardan en `p[1..S]` (por eso `p` tiene `S + 1` posiciones), igual que en la fórmula: el sector `i` es `p[i]`.

**2. La tabla.** `dardos` tiene `S + 1` filas y `V + 1` columnas, todas a `INF` («no se puede»). La fila `i` significa «puedo usar los sectores `1..i`», así que la **fila 0** es «sin ningún sector». La columna `j` es la suma que quiero conseguir.

**3. Casos base.** `dardos[0][0] = 0` y, en cada fila, `dardos[i][0] = 0`: sumar 0 no necesita dardos. El resto de la fila 0 se queda en `INF`.

**4. Rellenar** fila a fila, de izquierda a derecha. En cada casilla `(i, j)` hay dos opciones:

```text
            j − p[i]          j
fila i−1      ·          [ no usar i ]   ← copia la de arriba: dardos[i-1][j]
fila i    [ usar i ] ─────────► (i, j)   ← la de p[i] columnas a la izquierda, + 1 dardo
```
- **No usar el sector `i`:** lo mismo que sin él, la casilla de **arriba**.
- **Usar el sector `i` una vez más:** un dardo + lo que cuesta sumar `j − p[i]`, mirando **en la misma fila `i`**, porque el sector se puede repetir.

Se queda el mínimo. El `!= INF` evita calcular `INF + 1`, que se desbordaría.

**5. Respuesta.** `dardos[S][V]`: si es `INF`, `Imposible`.

## Reconstrucción: qué dardos se han tirado

La tabla solo guarda **cuántos** dardos. Para saber **cuáles**, se recorre hacia atrás desde la casilla de la respuesta `(i, j) = (S, V)`, preguntando en cada paso **de dónde salió ese número**:

- Si `dardos[i][j] == dardos[i-1][j]`, el valor ya se conseguía sin el sector `i` → el sector `i` **no hace falta**: se sube a la fila `i − 1`.
- Si no, el valor solo pudo salir de **usar el sector `i`** → se escribe `p[i]` y se resta: se pasa a `(i, j − p[i])`, en la misma fila (se puede volver a usar).
- Se para cuando `j == 0`: ya se ha sumado todo.

## Traza del ejemplo 2 (V = 8, sectores 1 4 6)

**Tabla rellena** (∞ = no se puede):
```text
            j:   0  1  2  3  4  5  6  7  8
ninguno  (0):    0  ∞  ∞  ∞  ∞  ∞  ∞  ∞  ∞
{1}      (1):    0  1  2  3  4  5  6  7  8
{1,4}    (2):    0  1  2  3  1  2  3  4  2
{1,4,6}  (3):    0  1  2  3  1  2  1  2  2   ← respuesta: dardos[3][8] = 2
```
Por ejemplo, `dardos[2][8] = min(dardos[1][8], dardos[2][4] + 1) = min(8, 1 + 1) = 2`.

**Reconstrucción** desde `(3, 8)`:
```text
(3, 8) = 2   arriba (2, 8) = 2   iguales  → el 6 no hace falta, subo        (2, 8)
(2, 8) = 2   arriba (1, 8) = 8   distintos → se tiró un 4, resto 8 − 4      (2, 4)
(2, 4) = 1   arriba (1, 4) = 4   distintos → se tiró un 4, resto 4 − 4      (2, 0)
j = 0 → fin                                              salida:  2: 4 4
```
Con el 6 también se llega a 8 (6 + 1 + 1), pero con 3 dardos. Por eso tirar siempre al sector más alto no sirve: hace falta la tabla.

## Por qué así
- **Tabla entera para reconstruir:** con una sola fila se sabe el mínimo, pero no qué sectores lo dan.
- **Las puntuaciones salen de mayor a menor**, como en el ejemplo del enunciado.
- **Coste:** O(S·V) en tiempo y en espacio por caso (como mucho 5·10⁶ casillas).

## Ojo con
- No hay número de casos: `while (cin >> V >> S)`.
- El formato es `k:` y luego cada puntuación precedida de un espacio.
