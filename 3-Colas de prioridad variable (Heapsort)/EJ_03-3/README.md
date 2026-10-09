# EJ 03-3 · Multitarea

📄 [Enunciado](<../Enunciados/prob-Multitarea.pdf>) · 💻 [Solución](EJ_03-3.cpp)

## Qué piden
Con tareas únicas `[c, f)` y periódicas (que se repiten cada `p` minutos), decir si hay dos que se solapen dentro de `[0, T)`.

## Cómo se plantea
**Barrido en orden de comienzo** con una `IndexPQ<pair<int,int>>` de mínimos:

| | Qué es |
|---|---|
| **Índice** | número de tarea: `0..N-1` únicas, `N..N+M-1` periódicas |
| **Prioridad** | `(ini, fin)` de su **próxima** aparición |
| `periodo[i]` | 0 si es única, `p` si es periódica |

Se guarda `tiempoActual` = fin de la última aparición procesada. Mientras no haya conflicto, la cola no esté vacía y el `top` empiece antes de `T`:
1. Si `ini < tiempoActual` → se solapa con la anterior ⇒ **SI**.
2. Si no, `tiempoActual = fin` y:
   - tarea periódica → `update(elem, {ini + p, fin + p})`: la misma tarea pasa a su siguiente aparición;
   - tarea única → `pop`.

## Por qué así
- **Basta comparar con la anterior:** las apariciones salen ordenadas por inicio; si la actual empieza después de que acabe la anterior, también empieza después de todas las previas (que acabaron antes).
- **Por qué `update`:** una tarea periódica es *un solo elemento* que va avanzando en el tiempo. `update` cambia su prioridad y la hunde en el montículo sin sacarla y volverla a meter.
- Los intervalos son semiabiertos: `[2,8)` y `[8,10)` no chocan, por eso la condición es `<` estricto.
- Se para en cuanto el `top` empieza en `T` o después: lo que pase más tarde no cuenta (caso 3).
- Si dos apariciones empiezan a la vez, la segunda tiene `ini < tiempoActual` (toda tarea dura ≥ 1 min) ⇒ conflicto, como debe ser.
- `ini + p` llega como mucho a unos 2·10⁸: cabe en `int`.

## Traza del ejemplo
```text
Caso 1 (T=10):  (2,5) → t=5    (4,6): 4 < 5            → SI
Caso 2 (T=10):  (1,4)  t=4   update → (9,12)
                (5,7)  t=7   update → (13,15)
                (9,12) t=12  update → (17,20)
                top (13,15): 13 ≥ 10, paro             → NO
Caso 3 (T=10):  (1,5)  t=5   pop
                (6,7)  t=7   update → (16,17)
                (8,20) t=20  pop
                top (16,17): 16 ≥ 10, paro             → NO
```

## Coste
**O((N + M + K) log(N + M))**, con K el número de apariciones que empiezan antes de `T`: cada una cuesta un `pop` o `update` logarítmico (sin conflictos no se solapan, así que K ≤ T).
