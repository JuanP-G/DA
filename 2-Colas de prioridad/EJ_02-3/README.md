# EJ 02-3 · Reina del súper

📄 [Enunciado](<../Enunciados/prob-Reina del súper.pdf>) · 💻 [Solución](EJ_02-3.cpp)

## Qué piden
Con N cajas y una **fila única** de C clientes (cada uno con su tiempo de atención), decir en qué caja acabará Ismael, que va detrás del último.

## Cómo se plantea
Cada cliente va a la caja que **antes quede libre**; si varias quedan libres a la vez, a la de **número menor**. Eso es exactamente el mínimo de una cola de prioridad.

- Cola de **mínimos** de pares `(instante en que la caja queda libre, número de caja)`:
  `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>>`.
- El `pair` se compara lexicográficamente: primero por instante y, a igualdad, por número de caja. **El desempate del enunciado sale gratis.**

1. Se meten las N cajas como `(0, i)`: todas libres en el instante 0.
2. Para cada cliente: se saca la cima, se le suma su tiempo y se vuelve a meter.
3. Tras los C clientes, la cima es la caja que primero queda libre: la de Ismael. Se escribe `cola.top().second`.

## Por qué así
- **No hace falta simular el reloj** segundo a segundo: solo importa el orden en que se liberan las cajas.
- Ismael es simplemente el cliente C + 1, así que su caja es la que estaría en la cima si viniera otro cliente más.
- **Error típico:** usar `pair<int,int>` con `priority_queue` sin `greater<>` da la caja que **más tarde** queda libre y, a igualdad, la de número **mayor**.
- **Desbordamiento:** el instante máximo es 500.000 · 100 = 5·10⁷, cabe en `int`. (El comentario del código dice C ≤ 250.000, pero el enunciado da C ≤ 500.000; la conclusión no cambia.)
- La lectura termina al leer `cajas == 0`; el segundo `0` de la línea final ya no se lee, pero da igual porque se acaba el programa.

## Traza del ejemplo
```text
Caso 4: 4 cajas, clientes 5 5 3 3 3        cola = {(0,1),(0,2),(0,3),(0,4)}
  cliente 5 -> caja 1 (libre en 0) hasta 5   cola = {(0,2),(0,3),(0,4),(5,1)}
  cliente 5 -> caja 2 (libre en 0) hasta 5   cola = {(0,3),(0,4),(5,1),(5,2)}
  cliente 3 -> caja 3 (libre en 0) hasta 3   cola = {(0,4),(3,3),(5,1),(5,2)}
  cliente 3 -> caja 4 (libre en 0) hasta 3   cola = {(3,3),(3,4),(5,1),(5,2)}
  cliente 3 -> caja 3 (libre en 3) hasta 6   cola = {(3,4),(5,1),(5,2),(6,3)}
  Ismael -> cima (3,4) -> caja 4
```
Caso 1 (2 cajas, 10 5): caja 1 hasta 10, caja 2 hasta 5 → Ismael va a la **2**. En el caso 3 sobra una caja que nunca se usa → **3**.

## Coste
**O((N + C) log N)** por caso: N inserciones iniciales y, por cada cliente, un `pop` y un `push` en una cola de tamaño N.
