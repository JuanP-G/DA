# EJ 03-5 · Tridente de temas candentes

📄 [Enunciado](<../Enunciados/prob-Tridente de temas candentes.pdf>) · 💻 [Solución](EJ_03-5.cpp) · 🎬 [Vídeo](../../Videos/03-5_tridente_temas_candentes.mp4)

## Qué piden
Procesar citas (`C tema n`) y expiraciones (`E tema n`) y, en cada `TC`, escribir los 3 temas con más citas vigentes (empate ⇒ el de `C` más reciente; los de 0 citas no salen).

## Cómo se plantea
**Una `IndexPQ<Prio, Mejor>`**:

| | Qué es |
|---|---|
| **Índice** | número del tema (`unordered_map` tema → índice y `vector nombre` índice → tema) |
| **Prioridad** | `Prio{citas, ultimoC}`: citas vigentes e instante (nº de evento) de su último `C` |
| **`Mejor`** | más citas antes; si empatan, `ultimoC` mayor antes |

Bucle de eventos (`t` = número de evento):
1. Tema nuevo → `push(idx, {0, -1})`.
2. `C` → `citas += n`, `ultimoC = t`; `E` → `citas -= n`. En ambos casos `update(idx, p)`.
3. `TC` → se hacen hasta 3 `top` + `pop` mientras el `top` tenga `citas > 0`, se escriben y **se vuelven a meter** con `push`.

## Por qué así
- **`update` es imprescindible:** las citas suben y bajan constantemente; la tabla de posiciones de la `IndexPQ` localiza el tema en O(1) y lo recoloca en O(log n).
- **Sacar y reinsertar** es la forma de ver los 3 primeros: el montículo solo garantiza el orden de la raíz, no de sus hijos.
- El desempate necesita `ultimoC` **dentro de la prioridad** (el comparador no ve índices). Una `E` no cambia `ultimoC`.
- Parar al ver `citas == 0`: si el mejor tiene 0, todos los demás también.
- Capacidad `n`: nunca hay más temas que eventos.

## Traza del ejemplo
```text
Caso 1: tras 4 eventos  quickSort(39,t3) mergeSort(40,t1) burbuja(17,t2)
TC  → pop mergeSort, quickSort, burbuja → 1 mergeSort 2 quickSort 3 burbuja; push de vuelta
C heapSort 19 → (19,t5)   C burbuja 1 → (18,t6)   E mergeSort 6 → (34,t1)
TC  → 1 quickSort(39)  2 mergeSort(34)  3 heapSort(19)       (burbuja 18 queda fuera)
Caso 2: Hulk (0,t0)  Ironman (3000,t1)  Superman (3000,t3)
TC  → 1 Superman (empate, C más reciente)  2 Ironman;  Hulk tiene 0 → se para
```

## Coste
**O(n log n)** por caso: cada `C`/`E` es un acceso hash más un `update` O(log n), y cada `TC` hace como mucho 3 `pop` y 3 `push`.
