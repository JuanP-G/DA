# EJ 11-2 · Aibofobia

📄 Enunciado: en el juez de la asignatura (`Ej11-2`) · 💻 [Solución](EJ_11-2.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una palabra de 1 a 1.000 letras minúsculas. Hay que escribir el **mínimo número de letras que añadir** (en cualquier posición) para convertirla en un palíndromo, y **uno de esos palíndromos**. Vale cualquiera de los que tengan el mínimo.

## Recurrencia (formato de examen)

Palabra $s = s_1 s_2 \dots s_n$. Para $1 \le i, j \le n$:

$$
\text{faltan}(i, j) = \text{mínimo número de letras a añadir para que } s_i \dots s_j \text{ sea un palíndromo}
$$

**Casos base**

$$
\text{faltan}(i, j) = 0 \qquad \text{si } i \ge j \quad (\text{vacía o una sola letra})
$$

**Recurrencia** ($i < j$)

$$
\text{faltan}(i, j) =
\begin{cases}
\text{faltan}(i+1,\ j-1) & \text{si } s_i = s_j \\
1 + \min\big(\text{faltan}(i+1, j),\ \text{faltan}(i,\ j-1)\big) & \text{si } s_i \ne s_j
\end{cases}
$$

Si los extremos coinciden, se emparejan entre sí. Si no, se añade una copia de $s_i$ al final (queda $s_{i+1..j}$) o una copia de $s_j$ al principio (queda $s_{i..j-1}$).

**Llamada inicial / respuesta:** $\text{faltan}(1, n)$.

**Orden de cálculo:** $\text{faltan}(i, j)$ depende de intervalos **más cortos**, así que se rellena por longitudes $d = j - i$ crecientes ($d = 1, 2, \dots, n-1$).

**Reconstrucción** desde $(1, n)$: si $s_i = s_j$ se pone $s_i$ a la izquierda y $s_j$ a la derecha y se pasa a $(i+1, j-1)$; si $\text{faltan}(i+1, j) \le \text{faltan}(i, j-1)$ se pone $s_i$ en los dos lados y se pasa a $(i+1, j)$; si no, $s_j$ en los dos lados y a $(i, j-1)$; si $i = j$, $s_i$ va una vez en el centro.

**Coste:** $O(n^2)$ en tiempo y en espacio.

## Cómo se plantea
Programación dinámica **sobre intervalos** de la palabra:

```text
faltan(i, j) = mínimo de letras a añadir para que s[i..j] sea un palíndromo

faltan(i, j) = 0                                          si i >= j
             = faltan(i+1, j−1)                           si s[i] == s[j]
             = 1 + min(faltan(i+1, j), faltan(i, j−1))    si no
```
Si los extremos son iguales, se emparejan entre sí. Si no, a uno de los dos se le pone una copia al otro lado: a `s[i]` (y queda `s[i+1..j]`) o a `s[j]` (y queda `s[i..j−1]`).

La tabla se rellena por **longitudes crecientes** del intervalo. Después se **reconstruye** desde `(0, n−1)`, construyendo a la vez la mitad izquierda y la derecha:
- `s[i] == s[j]`: `s[i]` a la izquierda, `s[j]` a la derecha, y a `(i+1, j−1)`;
- si conviene emparejar `s[i]`: `s[i]` en los dos lados, y a `(i+1, j)`;
- si no: `s[j]` en los dos lados, y a `(i, j−1)`;
- si queda una letra en el centro (`i == j`), va una sola vez.

## Traza de `amad`
```text
a…d distintos: faltan(1,3) "mad" = 2,  faltan(0,2) "ama" = 0  → mejor emparejar la d
izq = "d",  der = "d",  queda "ama"
a = a: izq = "da", der = "da",  queda "m" en el centro
izq + "m" + reverse(der) = "damad"                       → 1 damad
```

## Por qué así
- **Equivale a la subsecuencia palindrómica más larga:** `faltan(0, n−1) = n − LPS`. Las letras que ya forman palíndromo se quedan, y a cada una de las demás se le añade su pareja.
- **Coste:** O(n²) en tiempo y en espacio (10⁶ casillas para n = 1.000).

## Ojo con
- Hay muchas respuestas válidas: para `roda` esta solución escribe `rodador` y el enunciado `adoroda`. El juez acepta las dos.
- Si la palabra ya es un palíndromo se escribe `0` y la propia palabra.
