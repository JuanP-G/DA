# EJ 06-3 · Recorriendo el archipiélago en bicicleta

📄 [Enunciado](<../Enunciados/prob-Recorriendo el archipiélago en bicicleta.pdf>) · 💻 Solución en código: *pendiente* (esta carpeta solo trae la explicación, `GrafoValorado.h` y `ConjuntosDisjuntos.h`)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#645 · Recorriendo el archipiélago en bicicleta](https://aceptaelreto.com/problem/statement.php?id=645) — *casi el mismo problema*. Misma historia, pero allí los límites son menores (hasta 1.000 islas y 10.000 puentes; aquí 10.000 y 100.000) y no hay número de casos: se lee hasta el final del fichero.
<!-- acr:fin -->

## Qué piden
I islas y P puentes presupuestados (cada uno une dos islas y tiene un coste). Hay que elegir puentes de modo que se pueda ir de cualquier isla a cualquier otra y el **coste total de construcción sea mínimo**. Si no hay puentes suficientes para conectarlo todo: `No hay puentes suficientes`.

## Cómo se plantea
Es el **árbol de recubrimiento de coste mínimo** (ARM) de un grafo valorado: islas = vértices, puentes = aristas, coste = valor.

> Un ARM conecta todos los vértices con **V − 1 aristas** (sin ciclos) y con la suma de valores mínima.

El enunciado lo recuerda en las notas: lo que se minimiza es el **coste de construir**, no lo largo de cada trayecto.

**Algoritmo de Kruskal**

1. Ordenar todos los puentes por coste **creciente**.
2. Crear una partición `ConjuntosDisjuntos cd(I)`: al principio cada isla está sola.
3. Para cada puente `(u, v, coste)` en ese orden:
   - si `u` y `v` ya están en el mismo conjunto (`cd.unidos(u, v)`) ⇒ el puente cerraría un **ciclo**: se descarta;
   - si no ⇒ se construye: `cd.unir(u, v)`, `total += coste`, `elegidos++`.
   - Se puede parar al llegar a `elegidos == I − 1`.
4. Si `elegidos == I − 1` ⇒ escribir `total`. Si no ⇒ `No hay puentes suficientes`.

(Equivalente, y sin contar: `cd.num_cjtos() == 1` al final.)

## Por qué funciona
**Propiedad del corte:** dado cualquier reparto de las islas en dos grupos, el puente más barato que cruza de un grupo a otro pertenece a algún ARM. Kruskal, al llegar a cada puente en orden de coste, está justo en esa situación: si el puente une dos conjuntos distintos, es el más barato que sale de uno de ellos (los más baratos ya se han considerado) ⇒ es seguro cogerlo. Si une dos islas ya conectadas, cogerlo solo añadiría coste.

## Por qué así
- **Conjuntos disjuntos = detector de ciclos** en O(lg\* I): comprobar «¿ya están conectadas?» sin recorrer el grafo cada vez. Es para lo que se inventó la estructura en este tema.
- **Ordenar las aristas:** `g.aristas()` de `GrafoValorado.h` devuelve cada arista **una sola vez** (si guardas las dos copias, funciona igual, pero duplicas el trabajo). `Arista` ya trae `operator<` y `operator>`, así que sirve `std::sort` o una `priority_queue` con `greater`.
- **Caso I = 1:** no hace falta ningún puente ⇒ `0` (aunque P = 0). El bucle no hace nada y `elegidos == I − 1 == 0`: sale solo.
- **El coste total** puede llegar a unos 10⁹ (≈ 10.000 puentes de 100.000): cabe en `int`, pero usa `long long` y no hay que pensarlo.
- **Lectura:** `GrafoValorado<int> g(cin, 1)` lee «I, P y P puentes» de golpe (islas desde 1).
- **Alternativa:** el algoritmo de **Prim** (crecer un árbol desde una isla eligiendo siempre el puente más barato que sale de él, con una cola de prioridad) también da el ARM, en O(P log I). Para este problema Kruskal es más corto.

## Traza del ejemplo 1 (4 islas, 5 puentes)
```text
Ordenados por coste:  3-4 (2)   1-2 (5)   2-4 (7)   1-4 (8)   1-3 (10)

3-4 (2)    conjuntos distintos → se construye      total = 2    {3,4} {1} {2}
1-2 (5)    conjuntos distintos → se construye      total = 7    {3,4} {1,2}
2-4 (7)    conjuntos distintos → se construye      total = 14   {1,2,3,4}   ← ya hay 3 = I−1 puentes
1-4 (8)    (ya no se mira; habría cerrado un ciclo)
```
Resultado: **14**.

Ejemplo 2 (4 islas, puentes 1-2, 2-4, 4-1): se cogen `1-2 (3)` y `2-4 (5)`; `4-1 (8)` cierra el ciclo 1-2-4 y se descarta ⇒ solo 2 puentes elegidos < 3 ⇒ `No hay puentes suficientes` (la isla 3 queda aislada).

Ejemplo 3 (I = 1, P = 0): `0`.

## Coste
Ordenar: O(P log P). Kruskal con la partición: O(I + P · lg\* I). En total **O(I + P log P)**.

## Ojo con
- Cada caso crea **su propia** partición de tamaño I (no reutilizar la del caso anterior).
- Mensaje exacto: `No hay puentes suficientes`.
