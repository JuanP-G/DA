# EJ 01-1 · ¿Es un árbol AVL? (genérico, v1)

📄 [Enunciado](<../Enunciados/prob-¿Es un árbol AVL_ (1).pdf>) · 💻 [Solución](<EJ 01-1 (GENERICO).cpp>)

<!-- acr:inicio -->
🔗 **Pruébalo en Acepta el Reto** (sin necesidad del juez de la asignatura): [#303 · ¿Es un árbol AVL?](https://aceptaelreto.com/problem/statement.php?id=303) — *casi el mismo problema*. Mismo problema, pero en Acepta el Reto solo hay enteros y el árbol viene en preorden (aquí llega con paréntesis y puede ser de palabras). Sirve para probar la lógica del AVL cambiando la lectura.
<!-- acr:fin -->

Primera versión del ejercicio genérico (árboles de enteros `N` o palabras `P`, formato `(izq raíz der)`). Da la salida correcta en el ejemplo (`SI NO NO SI SI`).

**En qué se diferencia de la versión final:**
- **No construye el árbol:** `leerAVL<T>` lee los caracteres `(`, `.` y `)` directamente de `cin` y comprueba mientras lee.
- **El orden se comprueba con el inorden:** como el formato es `(izq raíz der)`, los valores llegan en inorden; el árbol es de búsqueda si cada valor es estrictamente mayor que el anterior (`anterior`, `hayAnterior`). No necesita mínimos ni máximos.
- La altura se devuelve por referencia (vacío = 0) y el resultado como `bool`.
- Coste **O(N)** y memoria solo **O(h)** (no guarda el árbol).

Es correcta y algo más ligera, pero mezcla lectura y lógica en una sola función. La [versión final](<../EJ_01-1 (generico)/README.md>) separa ambas cosas usando `BinTree` y `read_tree`.
