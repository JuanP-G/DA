# EJ 02-5 · Ordenando a los pacientes en urgencias

📄 [Enunciado](<../Enunciados/prob-Ordenando a los pacientes en urgencias.pdf>) · 💻 [Solución](EJ_02-5.cpp)

## Qué piden
Procesar ingresos (`I nombre gravedad`) y atenciones (`A`); en cada `A` escribir el paciente **más grave** y, a igualdad, **el que más tiempo lleva esperando**.

## Cómo se plantea
Es el uso de libro de una cola de prioridad: inserciones y extracciones del máximo intercaladas.

- **Cola de máximos** (`priority_queue<Paciente>`, que usa `operator<`).
- Cada `Paciente` guarda `nombre`, `gravedad` y `orden` (el número de evento en que llegó, `i`).
- `operator<` («tiene menos prioridad que»):
  1. si las gravedades difieren, tiene menos prioridad el de **menor gravedad**;
  2. si empatan, tiene menos prioridad el que **llegó después**: `orden > o.orden`.

Bucle principal, para cada uno de los n eventos:
- `I` → `push({nombre, gravedad, i})`.
- `A` → escribir `top().nombre` y `pop()`.

Al acabar el caso, `---`.

## Por qué así
- **El orden de llegada hay que guardarlo explícitamente:** `priority_queue` no es estable, así que sin `orden` dos pacientes con la misma gravedad podrían salir en cualquier orden.
- **Error típico:** escribir `orden < o.orden` en el desempate; eso daría prioridad al que llegó **más tarde** (una pila en lugar de una cola entre empatados).
- Basta con usar el índice del evento `i` como marca de llegada: es creciente, aunque no consecutivo.
- La gravedad 0 es válida (caso 3: Ana entra con 0 y nadie la atiende; solo se escribe `---`).
- Los pacientes que quedan sin atender al final del caso se descartan: la cola es local a `resuelveCaso`.
- El `if (!cola.empty())` es solo una protección: el enunciado garantiza que no hay `A` sin pacientes.

## Traza del ejemplo
```text
Caso 2 (cola mostrada como nombre/gravedad, cima a la izquierda)
  I Alberto 4000   {Alberto/4000}
  I Pepe 3000      {Alberto/4000, Pepe/3000}
  A -> Alberto     {Pepe/3000}
  I Rosa 2000      {Pepe/3000, Rosa/2000}
  I Laura 5000     {Laura/5000, Pepe/3000, Rosa/2000}
  A -> Laura       {Pepe/3000, Rosa/2000}
  I Sara 3000      {Pepe/3000 (orden 1), Sara/3000 (orden 6), Rosa/2000}
  A -> Pepe        empate a 3000: Pepe llegó antes
  A -> Sara        {Rosa/2000}  (Rosa se queda sin atender)
  ---
```

## Coste
**O(n log n)** por caso: cada evento hace a lo sumo un `push` o un `pop`, de coste logarítmico en el tamaño de la cola.
