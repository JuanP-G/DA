# EJ 03-L · La batalla por las audiencias

📄 [Enunciado](<../Enunciados/prob-La batalla por las audiencias.pdf>) · 💻 [Solución](EJ_03-L.cpp) · 🎬 [Vídeo](../../Videos/03-L_batalla_audiencias.mp4)

## Qué piden
Dadas las audiencias iniciales de C canales y una serie de actualizaciones por minuto, decir cuántos minutos ha sido líder cada canal en la franja `[0, D)`, ordenados de más a menos (empate ⇒ canal menor).

## Cómo se plantea
**Una `IndexPQ<Canales, greater<Canales>>` de máximos**:

| | Qué es |
|---|---|
| **Índice** | número de canal (`1..C`; se crea con tamaño `C + 1` y el 0 no se usa) |
| **Prioridad** | `Canales{audiencia, canal}` |
| `tiempos[c-1]` | minutos que lleva liderando el canal `c` (reutiliza el struct: el campo `audiencia` guarda minutos) |

Bucle de actualizaciones, con `tiempoAnterior` = minuto de la anterior:
1. El líder actual (`pq.top()`) lo ha sido desde `tiempoAnterior` hasta el minuto `m` de esta actualización: se le suman `m − tiempoAnterior` minutos.
2. Se aplican los cambios con `pq.update(canal, {audiencia, canal})`.
3. `tiempoAnterior = m`.

Al terminar, el líder suma el último tramo `D − tiempoAnterior`. Después se ordena `tiempos` y se escriben los que tengan > 0 minutos.

## Por qué así
- **Hace falta `update`:** en cada minuto cambian canales arbitrarios, y su audiencia puede **bajar** (el líder puede dejar de serlo sin que nadie lo supere, caso 2).
- Solo importa quién lidera **entre** actualizaciones, así que se cuenta por tramos y no minuto a minuto (D llega a 10⁹).
- Desempatar por canal en la cola no es necesario (el enunciado garantiza que no hay empate en el máximo), pero no estorba; sí hace falta en la ordenación final.
- Los minutos caben en `int` (≤ D ≤ 10⁹).

## Traza del ejemplo
Caso 1 (D = 120, audiencias 9000 / 1000 / 15000):
```text
min  líder en el tramo   suma            cambios                   nuevo líder
 15  canal 3             c3 += 15        c1=13000 c3=8000          1
 30  canal 1             c1 += 15        c3=11000                  1
 45  canal 1             c1 += 15        c1=9000  c2=3500          3
 60  canal 3             c3 += 15        c1=14000                  1
100  canal 1             c1 += 40        c1=13000 c2=5000 c3=10000 1
fin  canal 1             c1 += 20
Total: c1 = 90, c3 = 30  →  "1 90" / "3 30"
```

## Coste
**O((C + U) log C + C log C)**, con U el número total de pares canal-audiencia: cada carga o `update` es O(log C) y la ordenación final O(C log C).
