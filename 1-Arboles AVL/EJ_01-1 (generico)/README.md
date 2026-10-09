# EJ 01-1 · ¿Es un árbol AVL? (genérico)

📄 [Enunciado](<../Enunciados/prob-¿Es un árbol AVL_ (1).pdf>) · 💻 [Solución](<EJ 01-1 (GENERICO BIEN).cpp>)

## Qué piden
Lo mismo que en [EJ 01-1](<../EJ_01-1/README.md>), pero el árbol puede ser de enteros (`N`) o de palabras (`P`) y viene en formato `(izq raíz der)`, con `.` como vacío. Se lee hasta fin de entrada.

## Cómo se plantea
1. `main` lee la letra y llama a `resolverCaso<int>()` o `resolverCaso<string>()`.
2. `resolverCaso<T>` construye el árbol con `read_tree<T>(cin)` (de `bintree.h`, que ya entiende ese formato) y escribe `SI`/`NO`.
3. `analizar(arbol)` recorre el `BinTree<T>` en **postorden** y devuelve un `Info<T>`:

| Campo | Vacío | Nodo `elem` |
|---|---|---|
| `altura` | −1 | `1 + max(izq.altura, der.altura)` |
| `minimo` | sin sentido | `izq.minimo` si hay izquierdo, si no `elem` |
| `maximo` | sin sentido | `der.maximo` si hay derecho, si no `elem` |
| `esAVL` | `true` | hijos AVL, `|izq.altura − der.altura| ≤ 1`, `izq.maximo < elem < der.minimo` |

`hayIzq`/`hayDer` (altura ≠ −1) indican si `minimo`/`maximo` del hijo son válidos.

## Por qué así
- **Plantilla en `T`:** el mismo `analizar` sirve para `int` y `string`; solo exige `operator<`.
- **Sin centinelas:** en `string` no hay un «menor que todo» cómodo (y en `int` `INT_MAX` puede ser un valor real), así que el vacío se marca con altura −1 y las comparaciones se protegen con `!hayIzq ||` / `!hayDer ||`.
- **Altura −1 para el vacío:** así una hoja tiene altura 0; la diferencia de alturas es la misma que con el convenio 0/1.
- **Árbol vacío (`.`)** → `esAVL = true` → `SI`, como pide el último caso.

**Frente a la [v1](<../EJ_01-1 (generico v1)/README.md>):**
- La v1 no construye el árbol: lo comprueba mientras lo lee, y el orden lo verifica viendo que el **inorden es estrictamente creciente** (guarda el último valor leído en `anterior`). Usa menos memoria, pero mezcla lectura y lógica y arrastra tres parámetros por referencia.
- La final **separa lectura y análisis** (`read_tree` + `analizar`), reutiliza el `BinTree` de la asignatura y devuelve un `struct` en vez de parámetros de salida: más fácil de leer, probar y reutilizar en otros ejercicios sobre `BinTree`.
- También cambia `endl` por `'\n'` (no vacía el búfer en cada línea).

## Traza del ejemplo
```text
1) ((. 1 .) 2 (. 3 (. 4 .)))   N
   1: alt 0 · 4: alt 0 · 3: alt 1, 3 < 4 · 2: alturas 0/1, 1 < 2 < 3   → SI
2) (. 1 ((. 2 .) 3 (. 4 .)))   N
   3: alt 1 ok · 1: alturas −1/1 → diferencia 2                       → NO
3) ((. raton .) cabra (. perro (. gato .)))   P
   perro: hijo derecho gato, pero "perro" < "gato" es falso            → NO
4) ((. dos .) tres (. uno .))   P
   "dos" < "tres" < "uno" (orden alfabético), alturas 0/0              → SI
5) .   N   vacío                                                       → SI
```

## Coste
**O(N)** por caso: `read_tree` y `analizar` visitan cada nodo una vez (con `string`, multiplicado por el coste de comparar palabras). Memoria **O(N)** para el árbol, más **O(h)** de pila.
