# EJ 06-L · ¿Dónde construimos los aeropuertos?

📄 [Enunciado](<../Enunciados/prob-¿Dónde construimos los aeropuertos_.pdf>) · 💻 [Solución](EJ_06-L.cpp)

## Qué piden
N localidades y M carreteras posibles de doble sentido (puede haber varias entre el mismo par), cada una con su coste. Un aeropuerto cuesta A. Cada localidad debe **tener un aeropuerto o poder llegar por carretera a otra que lo tenga**. Hay que dar el **coste mínimo** y el **número de aeropuertos**; si varias soluciones empatan en coste, la que tenga **más aeropuertos**.

## Cómo se plantea
Localidades = vértices, carreteras = aristas. Una solución es un conjunto de carreteras que parte las localidades en **grupos conexos**, con **un aeropuerto por grupo**:

```text
coste = (suma de las carreteras construidas) + A · (número de grupos)
```

Unir dos grupos con una carretera de coste `C` ahorra un aeropuerto (`A`), así que **compensa solo si `C < A`**. Es un **Kruskal** con una condición extra:

1. Ordenar las carreteras por coste creciente.
2. `ConjuntosDisjuntos cd(N)`: al principio cada localidad es un grupo.
3. Para cada carretera en ese orden:
   - si `C ≥ A` ⇒ **parar** (esta y las siguientes ya no compensan);
   - si `u` y `v` están en grupos distintos ⇒ construirla: `cd.unir(u, v)` y sumar `C`;
   - si ya están unidos ⇒ cerraría un ciclo: se descarta.
4. Aeropuertos = `cd.num_cjtos()` (uno por grupo). Coste total = carreteras + `aeropuertos · A`.

## Por qué así
- **Empate `C == A`:** la carretera cuesta lo mismo que el aeropuerto que ahorra, y el enunciado pide **más aeropuertos** ⇒ no se construye. Por eso la condición es estricta (`C < A`). En el ejemplo 3, la carretera 2–3 cuesta 50 = A: construirla da 120 con 1 aeropuerto, no construirla da 120 con 2 ⇒ se prefieren los 2.
- **Con `C < A` el ahorro es real,** así que el número de aeropuertos de una solución óptima queda determinado (los grupos que forman las carreteras más baratas que `A`).
- **Carreteras repetidas entre el mismo par:** Kruskal se queda con la más barata y descarta las demás como ciclo.
- **N = 1:** un grupo y un aeropuerto: `A 1`.
- **Se puede parar** en cuanto una carretera cuesta `A` o más: están ordenadas.
- **Localidades desde 1:** se resta 1 al leer cada carretera. Como la primera línea del caso trae tres números (`N M A`), no sirve el constructor `GrafoValorado(cin, 1)`: se crea `GrafoValorado<int> g(N)` y se añaden las aristas con `ponArista`.
- **`long long`:** el coste puede acercarse a 2 · 10⁹ (10.000 aeropuertos de 100.000 más carreteras), al límite de un `int`.

## Traza de los ejemplos
```text
Ejemplo 1 (N=4, A=100):  carreteras ordenadas  1-2 (10)  4-3 (20)  2-3 (30)  4-1 (40)
  1-2 (10)  grupos distintos, 10 < 100  → se construye   total 10   {1,2} {3} {4}
  4-3 (20)  grupos distintos, 20 < 100  → se construye   total 30   {1,2} {3,4}
  2-3 (30)  grupos distintos, 30 < 100  → se construye   total 60   {1,2,3,4}
  4-1 (40)  ya unidos → se descarta
  1 grupo ⇒ 1 aeropuerto:  60 + 100 = 160            →  160 1

Ejemplo 2 (N=5, A=1000):  1-2 (20)  3-2 (30)  4-5 (10)  →  tres carreteras
  grupos {1,2,3} y {4,5}  ⇒ 2 aeropuertos:  60 + 2000   →  2060 2

Ejemplo 3 (N=3, A=50):   1-2 (20)  2-3 (50)  1-3 (80)
  1-2 (20) < 50 → se construye;  2-3 (50) ≥ 50 → parar
  grupos {1,2} y {3} ⇒ 2 aeropuertos:  20 + 100 = 120  →  120 2
```

## Coste
Ordenar: O(M log M). Kruskal con la partición: O(N + M · lg\* N). En total **O(N + M log M)** por caso.

## Ojo con
- Condición **estricta** `C < A` (con `≤` el tercer ejemplo daría `120 1`).
- Cada caso crea su propia partición.
- La suma de N y de M de todos los casos llega a 500.000: leer con `ios::sync_with_stdio(false)`.
