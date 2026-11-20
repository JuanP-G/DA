# EJ 08-4 · Maratón de cine de terror

📄 [Enunciado](<../Enunciados/prob-Maratón de cine de terror.pdf>) · 💻 [Solución](EJ_08-4.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
N películas (1 ≤ N ≤ 500.000), cada una con el día D (1..100.000), la hora de comienzo `HH:MM` y la duración en minutos (1..1.000.000). Entre película y película hacen falta **10 minutos libres**. Hay que escribir el **máximo número de películas** que se pueden ver enteras.

## Cómo se plantea
Es el problema clásico de **selección de actividades**. Cada película es un intervalo en minutos absolutos:

```text
inicio = (D·24 + HH)·60 + MM          fin = inicio + duración
se puede ver después de otra si  inicio >= finAnterior + 10
```

Voraz: se ordenan por hora de **fin** y se coge cada película compatible con la última elegida. La que acaba antes deja más tiempo libre para las demás.

## Traza del ejemplo 2
```text
10:30–12:00   12:00–13:10   16:00–17:50     (ordenadas por fin)
10:30–12:00  ✓  libre desde 12:10
12:00–13:10  ✗  empieza a las 12:00 < 12:10
16:00–17:50  ✓                                   → 2
```
En el ejemplo 3, la de las 23:30 del día 1 acaba a la 1:00 del día 2 y la siguiente empieza a la 1:10: justo 10 minutos, se pueden ver las dos.

## Por qué así
- **Minutos absolutos:** así las películas que cruzan la medianoche no son un caso especial.
- **Intercambio:** en una solución óptima se puede cambiar su primera película por la que acaba antes de todas sin solapar con las demás. Repitiendo, la voraz es óptima.
- **Coste:** O(N log N) por caso.

## Ojo con
- Leer la hora con un `char` para saltar los dos puntos: `cin >> h >> c >> m`.
- `long long`: 100.000 días son 1,44·10⁸ minutos, más la duración. Cabe en `int`, pero así no hay dudas.
