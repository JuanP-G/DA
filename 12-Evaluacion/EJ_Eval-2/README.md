# EJ Eval-2 · Bollos preñaos

📄 [Enunciado](<../Enunciados/prob-Bollos preñaos.pdf>) · 💻 [Solución](EJ_Eval-2.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N tipos de chorizo (1..50) y M gramos de masa de pan (1..1.000). Del tipo i hay $g_i$ gramos; cada bollo de ese tipo lleva $c_i$ gramos de chorizo y $m_i$ de masa, y se vende a $p_i$ euros (todo entre 1 y 100). Cada bollo lleva un solo tipo de chorizo. Hay que escribir el **máximo de euros** que se puede ganar.

## Recurrencias (formato de examen)

Del tipo $i$ se pueden hacer como mucho $k_i = \lfloor g_i / c_i \rfloor$ bollos. Para $0 \le i \le N$ y $0 \le j \le M$:

- $\text{bollos}(i, j)$: máximo de euros haciendo bollos de los tipos $1..i$ con $j$ gramos de masa.

**Casos base**

$$
\text{bollos}(0, j) = 0 \qquad \forall\, j \ge 0
$$

**Recurrencia** ($1 \le i \le N$, $0 \le j \le M$)

$$
\text{bollos}(i, j) = \max_{\substack{0 \le t \le k_i \\ t\, m_i \le j}} \big(\text{bollos}(i-1,\ j - t\, m_i) + t\, p_i\big)
$$

Se elige **cuántos** bollos $t$ hacer del tipo $i$: los limita el chorizo ($t \le k_i$) y la masa que queda ($t\, m_i \le j$). Con $t = 0$ el tipo no se usa.

**Llamada inicial / respuesta:** $\text{bollos}(N, M)$. No hace falta gastar toda la masa: la tabla guarda «con **como mucho** $j$ gramos».

**Implementación:** un vector por fila; la nueva se calcula a partir de una copia de la anterior. Coste $O(M \cdot \sum k_i) \le O(1.000 \cdot 5.000)$ por caso y $O(M)$ en espacio.

## Cómo se plantea
Es una **mochila con cantidades acotadas**. La masa es la capacidad, cada bollo es un objeto (peso $m_i$, valor $p_i$) y del tipo $i$ hay $k_i$ unidades. El chorizo no es otra dimensión de la mochila: cada tipo tiene el suyo, así que solo sirve para calcular $k_i$.

```text
para cada tipo (g, c, m, p):
    k = g / c                         ← bollos posibles con ese chorizo
    nueva = euros                     ← t = 0
    para j = 0..M:
        para t = 1..k mientras t·m ≤ j:
            nueva[j] = max(nueva[j], euros[j − t·m] + t·p)
    euros = nueva
respuesta: euros[M]
```

## Traza del ejemplo 2 (M = 8)
```text
tipo 1: g=18 c=3 m=1 p=10  → k = 6
        euros[j] = 10·min(j, 6)          → euros = 0 10 20 30 40 50 60 60 60
tipo 2: g=7  c=3 m=2 p=100 → k = 2
        nueva[8] = max(60, euros[6] + 100, euros[4] + 200) = max(60, 160, 240) = 240
→ 240
```
Dos bollos del tipo 2 (4 g de masa, 200 €) y cuatro del tipo 1 con la masa que queda (40 €).

## Por qué así
- **No vale un voraz** por precio ni por euros/gramo de masa: el límite de chorizo y la masa que sobra lo estropean. La tabla prueba todas las cantidades.
- **El chorizo no es una segunda capacidad:** no se comparte entre tipos, así que se convierte en el tope $k_i$.
- **Copiar la fila anterior** (o recorrer $j$ hacia abajo) evita contar bollos del mismo tipo dos veces y pasarse de $k_i$.

## Ojo con
- $k_i = g_i / c_i$ es división entera: con 7 g y 3 por bollo salen 2 bollos.
- La respuesta es $\text{bollos}(N, M)$ y no «con la masa exacta»: puede sobrar masa.
- Cabe en `int`: como mucho 50 tipos × 100 bollos × 100 €.
