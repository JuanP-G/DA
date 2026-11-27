# EJ 12-10 · Megaautopista de Oriente

📄 [Enunciado](<../Enunciados/prob-Megaautopista de Oriente.pdf>) · 💻 [Solución](EJ_12-10.cpp) · 🎬 [Vídeo](<../../Videos/12-10_megaautopista_de_oriente.mp4>)

🧩 Plantilla: [**casos ilimitados**](../../Plantillas/3.CasosIlimitados.cpp) — se lee hasta el fin de la entrada y `bool resuelveCaso()` devuelve `false` cuando `!cin`.

## Qué piden
$N$ áreas (hasta 300.000) en posiciones crecientes $x_i$ con beneficio $b_i$. Dos restaurantes de la empresa deben estar a **$D$ km o más**. Máximo beneficio y **las posiciones** donde construir (vale cualquier solución óptima).

## Recurrencia (formato de examen)

- $\text{gana}(i)$: máximo beneficio usando solo las áreas $1..i$.
- $\text{antes}(i)$: número de áreas con $x_j \le x_i - D$ (las compatibles con la $i$).

**Caso base**

$$
\text{gana}(0) = 0
$$

**Recurrencia** ($i \ge 1$)

$$
\text{gana}(i) = \max\big(\text{gana}(i-1),\ \ \text{gana}(\text{antes}(i)) + b_i\big)
$$

**Llamada inicial / respuesta:** $\text{gana}(N)$.

**Reconstrucción:** desde $i = N$, si $\text{gana}(i) = \text{gana}(i-1)$ se pasa a $i-1$; si no, hay restaurante en $x_i$ y se salta a $\text{antes}(i)$.

**Coste:** $O(N)$ en tiempo y espacio: $\text{antes}(i)$ nunca retrocede.

## Cómo se plantea
Es la «gira agotadora» (12-9) cuando la separación depende de **kilómetros** y no de posiciones consecutivas: en lugar de `i − 2` se salta a `antes(i)`.

## Traza del ejemplo 3 (D = 15, posiciones 10 20 30, beneficios 20 40 20)
```text
i:       1    2    3
antes:   0    0    1
gana:   20   40   40
```
$\text{gana}(3) = \max(40,\ 20 + 20)$: empate. Con la condición «igual → no construir» se reconstruye `20`; el enunciado muestra `10 30`. **Las dos son correctas.**

## Por qué así
- Buscar `antes(i)` retrocediendo cada vez desde `i` puede ser $O(N^2)$; el puntero (o una búsqueda binaria) lo evita.
- Con $x_j = x_i - D$ las dos áreas **sí** son compatibles: «no a menos de D».

## Ojo con
- La reconstrucción sale de atrás hacia delante: se escribe al revés.
- Con 300.000 áreas, **no** reconstruyas con recursión profunda.
- Se lee hasta el fin de la entrada.
