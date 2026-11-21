# EJ Eval-3 · Cine romántico a raudales

📄 [Enunciado](<../Enunciados/prob-Cine romántico a raudales.pdf>) · 💻 [Solución](EJ_Eval-3.cpp) · 🎬 [Vídeo](<../../Videos/Eval-3_cine_romantico.mp4>)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N películas (1..300.000), cada una con su día D (1..100.000), hora de comienzo `HH:MM` y duración (1..1.000.000 minutos). Entre una película y la siguiente hacen falta **10 minutos libres**, y las películas se ven enteras. Hay que escribir el **máximo de minutos** que se puede estar viendo películas. Es la versión con pesos del 08-4 (*Maratón de cine de terror*): allí se maximizaba el número de películas, aquí el tiempo.

## Recurrencias (formato de examen)

Cada película es un intervalo en minutos absolutos: $\text{ini}_i = (D_i - 1) \cdot 1440 + 60\,HH_i + MM_i$ y $\text{fin}_i = \text{ini}_i + \text{dur}_i$. Se ordenan por $\text{ini}$ (películas $0..N-1$) y se define

- $\text{sig}(i)$: la primera película $k$ con $\text{ini}_k \ge \text{fin}_i + 10$ (o $N$ si no hay).
- $\text{minutos}(i)$: máximo de minutos viendo películas elegidas entre la $i$ y las siguientes.

**Caso base**

$$
\text{minutos}(N) = 0
$$

**Recurrencia** ($0 \le i < N$)

$$
\text{minutos}(i) = \max\big(\text{minutos}(i+1),\ \ \text{dur}_i + \text{minutos}(\text{sig}(i))\big)
$$

O **no se ve** la película $i$ y se sigue con la siguiente, o **se ve** y la próxima que se puede ver es $\text{sig}(i)$.

**Llamada inicial / respuesta:** $\text{minutos}(0)$.

**Implementación:** se rellena de $N-1$ hacia $0$ y $\text{sig}(i)$ se calcula con búsqueda binaria (`lower_bound`) en los inicios ordenados. Coste $O(N \log N)$ por caso y $O(N)$ en espacio.

## Cómo se plantea
```text
pasar cada película a minutos absolutos: ini = (D−1)·1440 + HH·60 + MM,  fin = ini + dur
ordenar por ini
minutos[N] = 0
para i = N−1 .. 0:
    sig = lower_bound(inicios, fin_i + 10)
    minutos[i] = max(minutos[i+1], dur_i + minutos[sig])
respuesta: minutos[0]
```

## Traza del ejemplo 2
```text
ordenadas: A = [660, 750) 90 min    B = [660, 840) 180 min    C = [765, 825) 60 min
minutos[3] = 0
minutos[2] (C): max(0, 60 + 0)                       = 60
minutos[1] (B): sig = 3 → max(60, 180 + 0)           = 180
minutos[0] (A): sig = 2 (765 ≥ 750 + 10) → max(180, 90 + 60) = 180
→ 180
```
Ver A y C da 150 minutos, pero compensa más la película larga sola.

## Por qué así
- **No vale el voraz del 08-4** (la que antes termina): ese maximiza el número de películas, no los minutos.
- **Ordenar por inicio** permite que todas las películas compatibles con la $i$ estén después de $\text{sig}(i)$, y la búsqueda binaria lo encuentra en $O(\log N)$.
- **Minutos absolutos:** así las películas de días distintos (o que pasan de medianoche) se comparan sin casos especiales.

## Ojo con
- Hacen falta **10 minutos libres**: una que empieza justo cuando acaba otra **no** se puede ver (ejemplo 1). La condición es $\text{ini} \ge \text{fin} + 10$.
- El total cabe en `int`: las películas vistas no se solapan, así que como mucho suman los 100.000 días más la última película (≈ 1,45·10⁸ minutos). Los minutos absolutos se guardan en `long long` por comodidad.
- Las películas no vienen ordenadas, y los días cuentan: no basta con la hora.
- Recorrer todas las siguientes para buscar $\text{sig}(i)$ es $O(N^2)$: con N = 300.000 no da tiempo.
