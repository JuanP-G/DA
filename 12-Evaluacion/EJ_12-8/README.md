# EJ 12-8 · Volando entre pivotes

📄 [Enunciado](<../Enunciados/prob-Volando entre pivotes.pdf>) · 💻 [Solución](EJ_12-8.cpp) · 🎬 [Vídeo](<../../Videos/12-8_volando_entre_pivotes.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Una fila de $N$ pivotes (2..100.000). Desde uno se puede ir al siguiente o saltarse como mucho $K$ (0..10). ¿De **cuántas formas** se llega del primero al último? Módulo $1.000.000.007$.

## Recurrencia (formato de examen)

- $\text{formas}(i)$: número de formas de llegar al pivote $i$.

**Caso base**

$$
\text{formas}(1) = 1
$$

**Recurrencia** ($i \ge 2$)

$$
\text{formas}(i) = \sum_{d=1}^{\min(K+1,\ i-1)} \text{formas}(i-d) \pmod{10^9+7}
$$

**Llamada inicial / respuesta:** $\text{formas}(N)$. **Coste:** $O(N)$ con ventana deslizante (u $O(NK)$ sumando cada vez).

## Cómo se plantea
Se mira el **último vuelo**: venía de alguno de los $K+1$ pivotes anteriores, y cada uno aporta sus propias formas.

## Traza del ejemplo 3 (`4 2`)
```text
formas(1) = 1
formas(2) = 1                      (desde 1)
formas(3) = 1 + 1 = 2              (desde 2 y 1)
formas(4) = 2 + 1 + 1 = 4          (desde 3, 2 y 1)
```

## Por qué así
- Es Fibonacci generalizado: con $K = 1$ sale exactamente Fibonacci.
- La **ventana** evita volver a sumar los mismos términos: entra `formas(i)` y sale `formas(i−K−1)`.

## Ojo con
- Saltarse $K$ pivotes significa avanzar hasta $K+1$ posiciones.
- Al **restar** módulo hay que sumar antes el módulo para no quedar en negativo.
- La recursión sin memoria es exponencial.
