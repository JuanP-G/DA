# EJ 12-7 · Oposiciones a notaría

📄 [Enunciado](<../Enunciados/prob-Oposiciones a notaría.pdf>) · 💻 [Solución](EJ_12-7.cpp) · 🎬 [Vídeo](<../../Videos/12-7_oposiciones_a_notaria.mp4>)

🧩 Plantilla: [**centinela**](../../Plantillas/2.Centinela.cpp) — la entrada acaba con un caso de 0 documentos y `bool resuelveCaso()` devuelve `false` al leerlo.

## Qué piden
`n` documentos (2..200) con $p_i$ páginas (hasta 1.000) que hay que fusionar **de dos en dos y sin cambiar el orden**. Cada fusión tarda tantos segundos como páginas tiene el resultado. Se pide el **tiempo total mínimo**.

## Recurrencia (formato de examen)

- $\text{tiempo}(i, j)$: mínimo tiempo para juntar los documentos $i..j$ en uno.
- $\text{paginas}(i..j) = s_j - s_{i-1}$, con $s$ las sumas acumuladas.

**Caso base**

$$
\text{tiempo}(i, i) = 0
$$

**Recurrencia** ($i < j$)

$$
\text{tiempo}(i, j) = \min_{i \le k < j} \big(\text{tiempo}(i, k) + \text{tiempo}(k+1, j)\big) + \text{paginas}(i..j)
$$

**Llamada inicial / respuesta:** $\text{tiempo}(1, n)$. Se rellena por longitudes crecientes. **Coste:** $O(n^3)$ en tiempo y $O(n^2)$ en espacio.

## Cómo se plantea
Es el esquema de la **multiplicación encadenada de matrices**: se elige cuál es la **última** fusión. La última une un bloque $i..k$ con otro $k+1..j$ y cuesta siempre lo mismo (todas las páginas), sea cual sea $k$.

## Traza del ejemplo 3 (`6 5 4 3`)
```text
longitud 2:  (6,5) = 11   (5,4) = 9    (4,3) = 7
longitud 3:  (6..4) = min(0+9, 11+0) + 15 = 24
             (5..3) = min(0+7, 9+0) + 12  = 19
longitud 4:  min(0+19, 11+7, 24+0) + 18   = 36     ← (6 5) (4 3)
```

## Por qué así
- **No es Huffman:** unir siempre los dos más cortos exige poder cambiar el orden, y aquí solo se unen **vecinos**.
- **No basta unir el par vecino más corto** (voraz): no siempre es óptimo.

## Ojo con
- El tiempo de una fusión incluye **todas** las páginas del resultado.
- La entrada termina con un `0` que no se procesa.
- Cabe en `int`.
