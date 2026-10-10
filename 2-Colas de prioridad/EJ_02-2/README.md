# EJ 02-2 · Unidad Curiosa de Monitorización

📄 [Enunciado](<../Enunciados/prob-Unidad Curiosa de Monitorización.pdf>) · 💻 [Solución](EJ_02-2.cpp)

## Qué piden
Dados varios usuarios con su `Periodo`, decir a quién van los **K primeros envíos**; si coinciden en el tiempo, va antes el de **identificador menor**.

## Cómo se plantea
Es una **simulación por eventos**: solo interesa cuál es el **próximo** envío, y eso es justo lo que da una cola de prioridad de mínimos.

Cada elemento de la cola es un `Envio`:

| Campo | Significado |
|---|---|
| `t` | instante del próximo envío a ese usuario |
| `id` | identificador del usuario |
| `periodo` | cada cuánto le toca |

El orden es **(t, id)**: primero el instante más temprano y, a igualdad, el id menor. Se define `operator>` y se usa `priority_queue<Envio, vector<Envio>, greater<Envio>>`, que pone arriba al «menor».

1. Cada usuario entra con `t = periodo` (su primer envío).
2. Se repite K veces: se saca la cima, se escribe su `id`, se hace `t += periodo` y se vuelve a meter.
3. Al final, `---`.

## Por qué así
- **Solo hay un evento pendiente por usuario** en la cola: el tamaño es siempre n, no crece con K.
- **El desempate por id va en el comparador.** Si solo se comparara `t`, la `priority_queue` no garantiza ningún orden entre empatados (no es estable) y la salida podría salir cambiada.
- **Error típico:** escribir `operator<` y usar `priority_queue<Envio>` sin más da una cola de **máximos**, que daría primero los envíos más lejanos. Con `greater<Envio>` hay que definir `operator>`.
- `top()` devuelve una referencia constante: hay que **copiar, `pop()`, modificar y `push()`**; no se puede cambiar el elemento dentro de la cola.
- `t` es `long long` por seguridad, aunque 10⁵ · 5.000 = 5·10⁸ cabría en `int`.

## Traza del ejemplo
```text
Caso 1: (1234, 300), (9000, 200), K = 5      cola = {(200,9000), (300,1234)}
  envío 1: saca (200,9000) -> mete (400,9000)   cola = {(300,1234), (400,9000)}
  envío 2: saca (300,1234) -> mete (600,1234)   cola = {(400,9000), (600,1234)}
  envío 3: saca (400,9000) -> mete (600,9000)   cola = {(600,1234), (600,9000)}
  envío 4: saca (600,1234) -> empate en t=600, gana el id menor
                            -> mete (900,1234)   cola = {(600,9000), (900,1234)}
  envío 5: saca (600,9000)
salida: 9000 1234 9000 1234 9000 ---
```
En el caso 2 el 1111 (periodo 100) se lleva los 9 envíos: el 9999 no recibe nada hasta t = 1000.

## Coste
**O((n + K) log n)** por caso: n inserciones iniciales y K extracciones/reinserciones en una cola que siempre tiene n elementos.
