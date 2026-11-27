# EJ 12-6 · Alineamiento de secuencias

📄 [Enunciado](<../Enunciados/prob-Alineamiento de secuencias.pdf>) · 💻 [Solución](EJ_12-6.cpp) · 🎬 [Vídeo](<../../Videos/12-6_alineamiento_de_secuencias.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Dos cadenas de `A`, `C`, `G`, `T` (hasta 1.000) y una matriz $S$ de $5 \times 5$ (orden `A C G T -`). Un alineamiento coloca las cadenas en columnas rellenando con guiones; puntúa la suma de $S$ de cada columna. Se pide el **máximo**. Cada caso trae una matriz y varios pares de cadenas.

## Recurrencia (formato de examen)

- $\text{mejor}(i, j)$: máxima puntuación alineando los $i$ primeros caracteres de $a$ con los $j$ primeros de $b$.

**Casos base**

$$
\text{mejor}(0, 0) = 0, \quad \text{mejor}(i, 0) = \text{mejor}(i-1, 0) + S[a_i, -], \quad \text{mejor}(0, j) = \text{mejor}(0, j-1) + S[-, b_j]
$$

**Recurrencia** ($i, j \ge 1$)

$$
\text{mejor}(i, j) = \max \begin{cases}
\text{mejor}(i-1, j-1) + S[a_i, b_j] \\
\text{mejor}(i-1, j) + S[a_i, -] \\
\text{mejor}(i, j-1) + S[-, b_j]
\end{cases}
$$

**Llamada inicial / respuesta:** $\text{mejor}(n, m)$.

**Coste:** $O(nm)$ en tiempo y $O(m)$ en espacio por par.

## Cómo se plantea
Se mira la **última columna** del alineamiento: o empareja las dos últimas bases, o una de ellas con un hueco. No hay más opciones (dos guiones juntos no están permitidos).

## Una sola fila
```text
diagonal = valor de mejor(i−1, j−1)   (se guarda antes de pisarlo)
arriba   = mejor[j]                    (todavía es de la fila i−1)
izquierda = mejor[j−1]                 (ya es de la fila i)
```

## Por qué así
- Se parece a la subsecuencia común más larga (11-L), pero con puntuaciones: **siempre** se suma algo, y puede ser negativo.
- Los casos base **no son cero**: alinear con la cadena vacía obliga a poner huecos.

## Ojo con
- La primera cadena indexa las **filas** de $S$ y la segunda las **columnas**: $S$ no tiene por qué ser simétrica.
- La matriz es la misma para todos los pares de un caso.
- El resultado puede ser **negativo**.
- Cabe en `int`: como mucho 2.000 columnas de 50.000.
