# EJ 02-1 · Lo que cuesta sumar

📄 [Enunciado](<../Enunciados/prob-Lo que cuesta sumar.pdf>) · 💻 [Solución](EJ_02-1.cpp)

## Qué piden
Sumar N números con el **mínimo esfuerzo total**, sabiendo que sumar `a + b` cuesta `a + b`.

## Cómo se plantea
**Algoritmo voraz:** en cada paso se suman **los dos números más pequeños** que haya disponibles, y el resultado vuelve al montón como un número más. Es la misma idea que la construcción de los códigos de Huffman.

1. Se meten los N sumandos en una **cola de prioridad de mínimos** (`priority_queue<long long, vector<long long>, greater<long long>>`).
2. Mientras quede más de un elemento:
   - se sacan los dos menores `a` y `b`,
   - se acumula `esfuerzo += a + b`,
   - se mete `a + b` en la cola.
3. Cuando queda un único número (la suma total), `esfuerzo` es la respuesta.

## Por qué así
- **¿Por qué los dos menores?** Cada número se vuelve a pagar en todas las sumas en las que participa (directamente o dentro de un resultado parcial). Conviene que los números grandes participen en el menor número de sumas posible, es decir, que se sumen lo más tarde posible.
- **No basta con ordenar una vez** y sumar de izquierda a derecha: en `30 40 50 60` eso cuesta 370, pero `(30+40) + (50+60)` cuesta 360. Los resultados parciales hay que volver a meterlos en la cola, porque pueden ser mayores que números que aún no se han usado.
- **`long long` obligatorio:** con 100.000 sumandos de hasta 10⁶ la suma total ya llega a 10¹¹, y el esfuerzo es todavía mayor (la suma total se paga varias veces); nada de eso cabe en `int`. Por eso la cola guarda `long long` aunque los sumandos se lean como `int`.
- **Error típico:** `priority_queue<long long>` a secas es de **máximos**; sin `greater<>` se sumarían siempre los dos mayores.
- Con N = 1 el `while` no se ejecuta y se escribe 0, como pide el enunciado.

## Traza del ejemplo
```text
Caso 2: 3 1 4 2        cola = {1, 2, 3, 4}
  saca 1, 2 -> mete 3   esfuerzo = 3    cola = {3, 3, 4}
  saca 3, 3 -> mete 6   esfuerzo = 9    cola = {4, 6}
  saca 4, 6 -> mete 10  esfuerzo = 19   cola = {10}       -> 19
Caso 3: 30 40 50 60
  saca 30, 40 -> 70     esfuerzo = 70   cola = {50, 60, 70}
  saca 50, 60 -> 110    esfuerzo = 180  cola = {70, 110}
  saca 70, 110 -> 180   esfuerzo = 360  cola = {180}      -> 360
Caso 5: 5              cola = {5} (un solo elemento)     -> 0
```

## Coste
**O(N log N)** por caso: N inserciones iniciales y N − 1 iteraciones, cada una con dos `pop` y un `push` de coste logarítmico.
