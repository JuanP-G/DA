# EJ 10-L · Cambio exacto

📄 [Enunciado](../Enunciados/prob-Cambio%20exacto.pdf) · 💻 [Solución](EJ_10-L.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Un precio `P` (1 a 10.000 céntimos) y `N` monedas o billetes (1 a 100) de valores cualesquiera hasta 10.000; **cada pieza se puede usar una sola vez**. Hay que pagar **lo menos posible, pero al menos `P`**, y de entre todas las formas de pagar esa cantidad, la que **use menos piezas**. Se escribe la cantidad pagada y el número de piezas.

## Recurrencia (formato de examen)

Piezas de valores $v_1, \dots, v_N$. Para $0 \le i \le N$ y $s \ge 0$:

$$
\text{piezas}(i, s) = \text{mínimo de piezas, usando solo las } i \text{ primeras, que suman exactamente } s \quad (\infty \text{ si no se puede})
$$

**Casos base**

$$
\text{piezas}(0, 0) = 0 \qquad \text{piezas}(0, s) = \infty \quad (s > 0)
$$

**Recurrencia** ($1 \le i \le N$)

$$
\text{piezas}(i, s) =
\begin{cases}
\text{piezas}(i-1, s) & \text{si } v_i > s \\
\min\big(\text{piezas}(i-1, s),\ \text{piezas}(i-1, s - v_i) + 1\big) & \text{si } v_i \le s
\end{cases}
$$

**Llamada inicial / respuesta:**

$$
s^* = \min\{\, s \ge P \mid \text{piezas}(N, s) < \infty \,\} \qquad \text{se escribe } s^* \text{ y } \text{piezas}(N, s^*)
$$

**Hasta dónde mirar:** si una forma de pagar suma $S \ge P$ y a la vez es la mínima, al quitarle cualquier pieza $v$ se queda por debajo de $P$: $S - v < P$. Como $v \le 10.000$, $S < P + 10.000$. Basta con calcular las sumas $s \le P + \max_i v_i$.

**Implementación:** una sola fila (`piezas[s]`) recorrida de **mayor a menor** `s` para no usar una pieza dos veces. Coste $O(N \cdot (P + \max v))$ en tiempo y $O(P + \max v)$ en espacio.

## Cómo se plantea
Es una **mochila 0/1 de suma exacta** (como la cuerda de la cometa, [10-1](../EJ_10-1/README.md)), pero con dos objetivos encadenados: primero la **menor suma** que llegue a `P`, y para esa suma, el **menor número de piezas**.

```text
piezas[0] = 0, el resto infinito
para cada pieza v:
    para s de tope a v (de mayor a menor):
        piezas[s] = min(piezas[s], piezas[s − v] + 1)
s = P; mientras piezas[s] sea infinito: s++
escribir s y piezas[s]
```

## Traza del ejemplo 2 (`P = 100`, piezas 25 50 25 50)
```text
sumas alcanzables y mínimo de piezas
  25 → 1      50 → 1      75 → 2     100 → 2 (50+50)    ...
100 se puede pagar exactamente con 2 piezas (50 + 50) o con 3 (50 + 25 + 25)
→ 100 2
```

## Por qué así
- **Recorrer `s` hacia abajo** es lo que hace que cada pieza se use como mucho una vez: al actualizar `piezas[s]` solo se mira `piezas[s − v]`, que todavía no se ha tocado con esta pieza. Hacia arriba se obtendría la versión de monedas **ilimitadas** (como [10-2](../EJ_10-2/README.md)).
- **No hace falta una tabla de `P` por `N` en memoria:** la fila `i` solo depende de la `i − 1`.
- **El tope `P + max v`** evita calcular sumas enormes (hasta 10⁶) que nunca serán la respuesta.

## Ojo con
- Pagar **más** puede salir más barato en piezas, pero el enunciado manda **primero la cantidad** y solo después el número de piezas (ejemplo 1: se pagan 1.500 con dos piezas aunque 2.000 usaría una).
- Si no se puede pagar exactamente, la respuesta es la **menor suma mayor** que `P`: por eso se avanza `s` desde `P` hasta encontrar un valor alcanzable.
