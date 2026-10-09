# EJ 03-1 · Volando drones

📄 [Enunciado](<../Enunciados/prob-Volando drones.pdf>) · 💻 [Solución](EJ_03-1.cpp)

## Qué piden
Cada sábado se monta en cada dron la pila de 9 V y la de 1,5 V más cargadas que queden; hay que escribir las horas de vuelo totales de cada sábado mientras quede alguna pila de cada tipo.

## Cómo se plantea
**Dos colas de máximos**, una por tipo de pila: `IndexPQ<int, greater<int>>`, con **índice = número de pila** y **prioridad = horas que le quedan**. Aquí la `IndexPQ` se usa como un montículo normal (solo `push`, `top` y `pop`; nunca `update`).

Bucle de sábados, mientras ninguna cola esté vacía:
1. Para cada dron (como mucho `N`), se sacan con `top` + `pop` la mejor pila de cada caja.
2. El dron vuela `min(h9, h1)` horas; se suma al total del sábado y se resta a las dos pilas.
3. Las pilas que aún tienen carga **no vuelven a la cola todavía**: se apartan en `sobran9V` / `sobran1V`.
4. Al acabar el sábado se reinsertan las sobrantes con `push` y se escribe el total.

## Por qué así
- **Apartar las sobrantes es la clave:** si se metieran en la cola en el momento, el mismo sábado se podrían volver a usar en otro dron, y el enunciado dice que cada pila se coloca una sola vez por sábado (se cargan en el club).
- **¿Por qué no `update`?** Las pilas salen de la cola al montarse, así que se reinsertan con `push` (su posición vale 0 tras el `pop`, no hay repetidos). Una `priority_queue` normal valdría igual.
- Una pila agotada (0 horas) no se reinserta: se va al reciclaje.
- Los totales caben en `int` (el enunciado garantiza ≤ 10⁹).

## Traza del ejemplo
Caso 2: `N = 2`, 9 V = {5, 12, 7, 15}, 1,5 V = {20, 20, 2}.
```text
Sábado 1:  dron 1: 15 y 20 → vuela 15   (queda 1,5 V con 5)
           dron 2: 12 y 20 → vuela 12   (queda 1,5 V con 8)
           total 27;  reinserto 1,5 V {5, 8}
           cajas: 9 V {7, 5}   1,5 V {8, 5, 2}
Sábado 2:  dron 1:  7 y 8  → vuela 7    (queda 1,5 V con 1)
           dron 2:  5 y 5  → vuela 5
           total 12;  cajas: 9 V {}   → fin
Salida: 27 12
```

## Coste
**O((A + B) log(A + B))**: cada vuelo agota al menos una pila, así que hay como mucho A + B vuelos en total, y cada uno hace un número constante de operaciones de montículo.
