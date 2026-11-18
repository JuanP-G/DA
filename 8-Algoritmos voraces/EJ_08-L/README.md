# EJ 08-L · Planificación de conferencias

📄 Enunciado: en el juez de la asignatura (`Ej08-L`) · 💻 [Solución](EJ_08-L.cpp)

## Qué piden
N conferencias (1 ≤ N ≤ 250.000), cada una con hora de comienzo y de fin (enteros 0..10⁹). Dos conferencias que se solapan no pueden ir en la misma sala; una que empieza **justo cuando acaba otra no se solapa** con ella. Hay que escribir el **mínimo número R de salas** y, en otra línea, la sala (1..R) de cada conferencia en el orden de la entrada. Vale **cualquier** asignación válida.

## Cómo se plantea
Voraz recorriendo las conferencias por hora de **comienzo**. Para cada una:
- si hay alguna sala libre (su última conferencia acabó como muy tarde cuando empieza esta), se **reutiliza**;
- si no, se **abre una sala nueva**.

Para saber al momento si hay alguna libre basta mirar la sala que queda libre **antes**: una cola de prioridad de mínimos con pares `(hora en que queda libre, sala)`.

```text
ordenar índices por comienzo
para cada conferencia c:
    si cola no vacía y cola.top().hora <= ini[c]:  sala[c] = esa sala, pop
    si no:                                         sala[c] = ++numSalas
    push (fin[c], sala[c])
```

**Por qué es óptimo:** solo se abre la sala `k` cuando las `k − 1` abiertas están ocupadas en el instante en que empieza la conferencia. En ese instante hay `k` conferencias a la vez, así que ninguna planificación puede usar menos de `k` salas.

## Traza del ejemplo 1
```text
[1,5)  → sala 1                    cola: (5,1)
[3,10) → 5 > 3: sala 2             cola: (5,1) (10,2)
[6,12) → 5 ≤ 6: reutiliza la 1     cola: (10,2) (12,1)
R = 2,  salas en orden de entrada: 1 2 1
```

## Por qué así
- **Ordenar índices, no las conferencias:** así se puede escribir la sala de cada una en el orden de la entrada.
- **`<=` al comparar:** acabar a las 5 y empezar a las 5 no es solape.
- **Coste:** O(N log N) por caso.

## Ojo con
- Hay muchas respuestas correctas. En el ejemplo 3 esta solución escribe `1 2 3` y el enunciado `1 3 2`: el juez acepta las dos.
