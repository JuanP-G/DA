# EJ 06-1 · Petroleros hundidos

📄 [Enunciado](<../Enunciados/prob-Petroleros hundidos.pdf>) · 💻 [Solución](EJ_06-1.cpp)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#288 · Petroleros hundidos](https://aceptaelreto.com/problem/statement.php?id=288) — *casi el mismo problema*. Mismo problema, pero allí no hay número de casos (se lee hasta el final del fichero) y, según el ejemplo de la página, el mar va como espacio en blanco en vez de `-`: lee cada fila con `getline` y comprueba que la longitud es C.

📥 **Versión lista para enviar** (un solo fichero, con las cabeceras dentro y el formato de entrada/salida de allí): [`ACR-288_petroleros_hundidos.cpp`](<../../Acepta el Reto/ACR-288_petroleros_hundidos.cpp>)
<!-- acr:fin -->

## Qué piden
Una rejilla de F × C celdas (`-` mar, `#` petróleo). Dos celdas de petróleo son de la **misma mancha** si se llega de una a otra pasando solo por petróleo, moviéndose en **8 direcciones**. Después van apareciendo N celdas nuevas de petróleo, una a una. Hay que escribir el **tamaño de la mancha más grande** al principio y tras cada celda nueva.

```text
Salida del ejemplo 1:  10 10 12 16     (inicial + 3 celdas nuevas)
Salida del ejemplo 2:   0  1  1  3     (rejilla vacía + 3 celdas nuevas)
```

## Cómo se plantea
Es el problema de las manchas negras del tema 4 (04-3), pero con la imagen **cambiando**. La clave es fijarse en *cómo* cambia:

> Las celdas solo **se añaden**, nunca se quitan ⇒ las manchas solo pueden **crecer o fundirse**, jamás partirse.

Eso es justo lo que hacen los **conjuntos disjuntos**: una partición que solo sabe **unir** conjuntos.

**Modelo**

| Idea | En el problema |
|---|---|
| Elemento | cada celda `(i, j)` → número `i·C + j` (0 … F·C − 1) |
| Conjunto | una mancha |
| `unir(a, b)` | dos celdas de petróleo vecinas (8 direcciones) |
| `cardinal(a)` | tamaño de la mancha de `a` |

**Algoritmo**

1. Crear `ConjuntosDisjuntos cd(F·C)` y un `mayor = 0`.
2. **Imagen inicial:** para cada celda `#`, unirla con sus vecinas (de las 8) que sean `#` y actualizar `mayor = max(mayor, cd.cardinal(celda))`. Escribir `mayor`.
3. **Cada celda nueva `(f, c)`** (pasar a base 0: `f−1`, `c−1`):
   - marcarla como petróleo,
   - unirla con sus vecinas que ya sean petróleo,
   - `mayor = max(mayor, cd.cardinal(celda))`,
   - escribir `mayor`.

El máximo **no hace falta recalcularlo** recorriendo todos los conjuntos: como solo hay uniones, la única mancha que puede haber cambiado es la de la celda nueva, y el tamaño máximo nunca baja. Basta compararlo con el cardinal de la mancha de la celda nueva.

## Por qué así
- **8 vecinos:** recorrer `di, dj ∈ {−1, 0, 1}` salvo `(0, 0)` y comprobar que `(i+di, j+dj)` está dentro de la rejilla **y es petróleo**. Unir con una celda de mar rompería el resultado.
- **Se puede unir con vecinas «hacia atrás» y «hacia delante»:** al procesar la imagen inicial, cuando llegas a una celda las vecinas posteriores pueden no estar unidas aún, pero cuando se procesen ellas se unirán con esta. Con cualquiera de los dos criterios (mirar los 8 o solo 4 ya vistos) el resultado final es el mismo.
- **La representación `i·C + j`** es la del 04-3: no hace falta construir un grafo, la rejilla *es* el grafo.
- **Lectura:** cada fila es una cadena sin espacios (`cin >> fila`). La salida son números separados por **un espacio** y sin espacio final.
- **Entrada en el límite:** F·C llega a 4.000.000 de celdas en total y N a 400.000 ⇒ el vector de la partición y la rejilla tienen que crearse **por caso** (no reservar 10⁶ fijos por cada caso) y conviene `ios::sync_with_stdio(false)`.
- Si una celda nueva ya fuera petróleo (el enunciado dice que no pasa), bastaría con repetir el máximo: `unir` con una celda de su propia mancha no cambia nada.

## Traza del ejemplo 2 (rejilla 3 × 4 vacía)
Celda `(f, c)` → número `(f−1)·4 + (c−1)`.

```text
Inicial               mayor = 0                         → 0
(2,2)  nº 5            sin vecinas negras: mancha {5}    → 1
(3,4)  nº 11           vecinas: 6, 7, 10 (todas limpias) → 1   (otra mancha {11})
(2,3)  nº 6            vecinas negras: 5 (izq.) y 11 (diagonal abajo-dcha.)
                       unir(6,5) y unir(6,11) → {5, 6, 11}
                       cardinal = 3                      → 3
```

## Las preguntas del campus
**¿Se podría usar la solución del tema 4 en cada imagen?** Sí, pero repitiendo un DFS/BFS de toda la rejilla después de cada celda nueva.

**¿Qué coste tendría?** Una imagen cuesta O(F·C); hay N + 1 imágenes ⇒ **O((N + 1) · F · C)**. Con F·C = 10⁶ y N = 10⁵ serían ~10¹¹ operaciones: no pasa.

**¿Se puede mejorar con conjuntos disjuntos?** Sí, como arriba: la imagen inicial se procesa una vez y cada celda nueva solo mira sus 8 vecinas.

**¿Qué coste tiene?**

| Parte | Coste |
|---|---|
| Crear la partición | O(F·C) |
| Imagen inicial: ≤ 8 `unir` por celda | O(F·C · lg\* (F·C)) |
| Cada celda nueva: ≤ 8 `unir` + 1 `cardinal` | O(lg\* (F·C)) |
| **Total** | **O(F·C + N)** (con la `lg*` prácticamente constante) |

`ConjuntosDisjuntos.h` usa unión por tamaños y compresión de caminos, que es lo que da ese coste casi lineal.

## Ojo con
- Fila/columna del enunciado van de 1 a F / 1 a C; la partición, de 0.
- Salida con **N + 1** números por caso, aunque N = 0.
- No olvides actualizar `mayor` también en la imagen inicial (la rejilla puede venir con petróleo).
