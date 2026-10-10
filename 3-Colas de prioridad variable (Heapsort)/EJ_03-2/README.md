# EJ 03-2 · 12 points go to…

📄 [Enunciado](<../Enunciados/prob-12 points go to….pdf>) · 💻 [Solución](EJ_03-2.cpp)

## Qué piden
Procesar sumas y restas de puntos a países y, en cada `?`, decir qué país va primero y con cuántos puntos (empate ⇒ nombre menor).

## Cómo se plantea
**Una `IndexPQ<Par, Mejor>`** donde:

| | Qué es |
|---|---|
| **Índice** | número asignado al país la primera vez que aparece (`unordered_map<string,int> indice`) |
| **Prioridad** | `pair<int,string>` = (puntos actuales, nombre) |
| **`Mejor`** | más puntos antes; si empatan, nombre menor antes |

Bucle de eventos:
1. `?` → `pq.top().prioridad` da directamente nombre y puntos del líder.
2. `nombre x` → si el país es nuevo se le da el siguiente índice y parte de 0; si no, se leen sus puntos con `pq.priority(idx)`. Después `pq.update(idx, {actuales + x, nombre})`.

`update` inserta si el elemento no estaba (posición 0) y, si estaba, cambia su prioridad y lo **flota o hunde** según haya subido o bajado.

## Por qué así
- **Hace falta `update`:** la puntuación de un país cambia muchas veces, y puede **bajar**. Con una `priority_queue` no se puede modificar un elemento; habría que meter copias y descartar las obsoletas al consultar.
- **El nombre va dentro de la prioridad** porque el comparador de la `IndexPQ` solo ve prioridades, no índices; sin él no se podría desempatar por nombre.
- La tabla `posiciones` de la `IndexPQ` (índice → posición en el montículo) es lo que permite encontrar al país en O(1) y recolocarlo en O(log n).
- Se crea con capacidad `n` (eventos): nunca hay más países que eventos.
- Puntos: como mucho 100 · 500.000 = 5·10⁷ en valor absoluto, cabe en `int`.

## Traza del ejemplo
Caso 2:
```text
Germany 8   → idx 0, (8, Germany)          top: Germany 8
France 8    → idx 1, (8, France)           top: France 8   (empate, nombre menor)
?           → France 8
Spain 12    → idx 2, (12, Spain)           top: Spain 12
?           → Spain 12
Spain 8     → update(2, (20, Spain))
Italy 22    → idx 3, (22, Italy)           top: Italy 22
?           → Italy 22
Italy -7    → update(3, (15, Italy))  hunde top: Spain 20
?           → Spain 20
```

## Coste
**O(N log N)** por caso: cada evento es una búsqueda en la tabla hash más un `update` en O(log N), y cada `?` es O(1).
