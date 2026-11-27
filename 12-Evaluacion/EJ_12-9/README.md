# EJ 12-9 · Una gira agotadora

📄 [Enunciado](<../Enunciados/prob-Una gira agotadora.pdf>) · 💻 [Solución](EJ_12-9.cpp) · 🎬 [Vídeo](<../../Videos/12-9_una_gira_agotadora.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
La recaudación de $N$ días (hasta 150.000). **No se puede actuar dos días seguidos**. Máxima recaudación.

## Recurrencia (formato de examen)

- $\text{gira}(i)$: máxima recaudación con los días $1..i$.

**Casos base**

$$
\text{gira}(0) = 0, \qquad \text{gira}(1) = r_1
$$

**Recurrencia** ($i \ge 2$)

$$
\text{gira}(i) = \max\big(\text{gira}(i-1),\ \ \text{gira}(i-2) + r_i\big)
$$

**Llamada inicial / respuesta:** $\text{gira}(N)$. **Coste:** $O(N)$ en tiempo y $O(1)$ en espacio.

## Cómo se plantea
Sobre el último día solo hay dos opciones: se **descansa** (vale lo de $i-1$) o se **actúa**, y entonces el anterior se descansa (vale lo de $i-2$ más $r_i$).

## Traza del ejemplo 4 (`1 8 1 1 8 3`)
```text
día:    1   2   3   4   5   6
r:      1   8   1   1   8   3
gira:   1   8   8   9  16  16
→ 16 (días 2 y 5)
```

## Por qué así
- **Alternar** días pares o impares no basta: aquí daría 12 y lo óptimo es 16, descansando dos días seguidos.
- **Voraz** (coger el mayor y tachar sus vecinos) también falla: con `10 1 10 10 1` o `4 5 4` se pierde dinero.

## Ojo con
- Solo hacen falta los dos últimos valores.
- La recursión directa es exponencial; con 150.000 días, ni siquiera conviene recursión.
- Cabe en `int` (como mucho 75.000 actuaciones de 10.000).
