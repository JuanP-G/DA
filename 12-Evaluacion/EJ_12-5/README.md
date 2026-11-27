# EJ 12-5 · Bizcocho con frutas

📄 [Enunciado](<../Enunciados/prob-Bizcocho con frutas.pdf>) · 💻 [Solución](EJ_12-5.cpp) · 🎬 [Vídeo](<../../Videos/12-5_bizcocho_con_frutas.mp4>)

🧩 Plantilla: [**casos ilimitados**](../../Plantillas/3.CasosIlimitados.cpp) — se lee hasta el fin de la entrada y `bool resuelveCaso()` devuelve `false` cuando `!cin`.

## Qué piden
Un bizcocho de $N$ trozos (par, hasta 1.000), cada uno con 0 (sin fruta), 1 (naranja) o 2 (limón). Cada día se cortan **dos trozos por los extremos**: los dos del mismo lado o uno de cada. Máximo de días en que los dos trozos tienen **la misma fruta**.

## Recurrencia (formato de examen)

- $\text{dias}(i, j)$: máximo de días buenos con los trozos $i..j$ ($j - i + 1$ siempre par).
- $\text{igual}(a, b) = 1$ si $f_a = f_b \ne 0$ y $0$ en otro caso.

**Caso base**

$$
\text{dias}(i, j) = 0 \qquad (i > j)
$$

**Recurrencia** ($i < j$)

$$
\text{dias}(i, j) = \max \begin{cases}
\text{dias}(i+2, j) + \text{igual}(i, i+1) & \text{dos por la izquierda} \\
\text{dias}(i, j-2) + \text{igual}(j-1, j) & \text{dos por la derecha} \\
\text{dias}(i+1, j-1) + \text{igual}(i, j) & \text{uno de cada lado}
\end{cases}
$$

**Llamada inicial / respuesta:** $\text{dias}(1, N)$. Se rellena por longitudes pares crecientes. **Coste:** $O(N^2)$ en tiempo y espacio.

## Cómo se plantea
Tras cada día queda un trozo de bizcocho **contiguo**, así que basta con saber dónde empieza y dónde acaba.

## Traza del ejemplo 2 (`0 1 2 0 0 2 1 2`)
```text
día 1: izquierda 0 y derecha 2        → distintos, queda 1 2 0 0 2 1
día 2: izquierda 1 y derecha 1        → naranja ✔, queda 2 0 0 2
día 3: izquierda 2 y derecha 2        → limón ✔,   queda 0 0
día 4: 0 y 0                          → sin fruta, no cuenta
→ 2
```

## Por qué así
- **No es voraz:** coger una pareja buena ahora puede romper dos parejas más tarde.
- El enunciado dice que no hay frutas consecutivas iguales (así que dos del mismo lado nunca puntúan), pero la recurrencia considera las **tres** jugadas porque hacen falta para **cambiar qué queda en los extremos**.

## Ojo con
- Dos ceros **no** cuentan: no tienen fruta.
- No olvides las jugadas del mismo lado aunque no den puntos.
- La entrada no dice cuántos casos hay: se lee hasta el final.
