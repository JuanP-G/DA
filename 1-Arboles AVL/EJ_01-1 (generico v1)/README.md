# EJ 01-1 · ¿Es un árbol AVL? (genérico, v1)

📄 [Enunciado](<../Enunciados/prob-¿Es un árbol AVL_ (1).pdf>) · 💻 [Solución](<EJ 01-1 (GENERICO).cpp>)

Primera versión del ejercicio genérico (árboles de enteros `N` o palabras `P`, formato `(izq raíz der)`). Da la salida correcta en el ejemplo (`SI NO NO SI SI`).

**En qué se diferencia de la versión final:**
- **No construye el árbol:** `leerAVL<T>` lee los caracteres `(`, `.` y `)` directamente de `cin` y comprueba mientras lee.
- **El orden se comprueba con el inorden:** como el formato es `(izq raíz der)`, los valores llegan en inorden; el árbol es de búsqueda si cada valor es estrictamente mayor que el anterior (`anterior`, `hayAnterior`). No necesita mínimos ni máximos.
- La altura se devuelve por referencia (vacío = 0) y el resultado como `bool`.
- Coste **O(N)** y memoria solo **O(h)** (no guarda el árbol).

Es correcta y algo más ligera, pero mezcla lectura y lógica en una sola función. La [versión final](<../EJ_01-1 (generico)/README.md>) separa ambas cosas usando `BinTree` y `read_tree`.
