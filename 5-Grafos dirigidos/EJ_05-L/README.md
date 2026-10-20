# EJ 05-L · El Necronomicón de la informática

📄 [Enunciado](<../Enunciados/prob-El Necronomicón de la informática.pdf>) · 💻 [Solución](EJ_05-L.cpp)

## Qué piden
Un «programa oscuro» tiene L instrucciones de tres tipos: `A` (pasa a la siguiente), `J N` (salta a la N) y `C N` (salta a la N **o** sigue; no se puede predecir). Empieza en la 1 y termina al llegar detrás de la última. Hay que decir si **SIEMPRE** termina, **NUNCA** termina o **A VECES** sí y a veces no.

## Cómo se plantea
Un `Digrafo` con **L + 1 vértices**: la instrucción `i` es el vértice `i − 1`, y el vértice `L` es «el programa ha terminado». Cada ejecución posible es un camino desde el 0:

| instrucción | aristas |
|---|---|
| `A` | `i − 1 → i` |
| `J N` | `i − 1 → N − 1` |
| `C N` | las **dos**: `i − 1 → i` y `i − 1 → N − 1` |

Todos los vértices tienen sucesores salvo el final, así que un camino solo acaba al llegar a `L`; si no, sigue para siempre. **Un único DFS desde el vértice 0** responde a todo:

| respuesta | condición |
|---|---|
| **NUNCA** | el vértice `L` **no** se alcanza desde el 0 |
| **SIEMPRE** | no hay **ningún ciclo alcanzable** desde el 0 (y `L` sí se alcanza) |
| **A VECES** | `L` se alcanza **y** hay un ciclo alcanzable |

El ciclo se detecta como siempre: durante el DFS, un vecino que **sigue en la pila** (estado 1) cierra un ciclo.

## Por qué así
- **Sin ciclos, todo camino es finito:** como solo el vértice final no tiene sucesores, todos acaban en `L`; si `L` es alcanzable, la respuesta es SIEMPRE.
- **Con un ciclo alcanzable** se puede dar vueltas para siempre (nunca termina esa ejecución) y, si además se llega a `L`, otras ejecuciones sí terminan ⇒ A VECES.
- **Un salto hacia atrás no es un ciclo** si no se puede volver a él: en el ejemplo 2, `C 3` en la instrucción 4 salta a la 3, pero desde la 3 solo se va a la 5.
- **Los ciclos que no se alcanzan desde la instrucción 1 no cuentan:** por eso el DFS parte solo del vértice 0 (no de todos, como en la detección general de ciclos).
- `C N` con `N = i + 1` crea una arista repetida; no molesta.
- La recursión llega como mucho a 10.000 niveles (L máximo): no hay problema de pila.

## Traza de los ejemplos
```text
Ejemplo 1:  1:A  2:A  3:J 1        aristas 0→1  1→2  2→0     vértice final: 3
            DFS desde 0: 0→1→2→0 (0 sigue en la pila: ciclo). El 3 no se alcanza  ⇒  NUNCA

Ejemplo 2:  1:A  2:J 4  3:J 5  4:C 3  5:A      0→1  1→3  2→4  3→4  3→2  4→5
            DFS desde 0: 0→1→3→4→5 (final) y 3→2→4 (ya terminado). Sin ciclos  ⇒  SIEMPRE

Ejemplo 3:  1:A  2:A  3:C 2  4:A              0→1  1→2  2→1  2→3  3→4
            DFS desde 0: 0→1→2→1 (1 sigue en la pila: ciclo) y 2→3→4 (final)  ⇒  A VECES
```

## Coste
**O(L)** por caso: cada instrucción aporta como mucho 2 aristas y el DFS visita cada vértice una vez.
