# EJ 03-4 · Pájaros en vuelo

📄 [Enunciado](<../Enunciados/prob-Pájaros en vuelo.pdf>) · 💻 [Solución](EJ_03-4.cpp) · 🎬 [Vídeo](../../Videos/03-4_pajaros_en_vuelo.mp4)

## Qué piden
A una bandada que empieza con un pájaro se le unen parejas; tras cada pareja hay que dar la **mediana** de las edades (el pájaro del centro).

## Cómo se plantea
**Mediana con dos montículos** (aquí `priority_queue`, no `IndexPQ`):

| Estructura | Contiene |
|---|---|
| `lider` | la mediana actual |
| `menores` (máximos) | los más jóvenes que `lider`; su `top` es el más viejo de ellos |
| `mayores` (mínimos) | los más viejos que `lider`; su `top` es el más joven de ellos |

Invariante: `menores.size() == mayores.size()` (el total siempre es impar).

Por cada pareja:
1. Cada pájaro va a `menores` si es más joven que `lider` y a `mayores` si no.
2. Si un lado queda con 2 más que el otro, el `lider` pasa al lado pequeño y el `top` del lado grande se convierte en el nuevo `lider`.
3. Se escribe `lider`.

## Por qué así
- Al entrar **dos** pájaros los tamaños solo pueden quedar iguales (uno a cada lado) o descompensados en 2 (los dos al mismo lado); en ese caso **un solo** traspaso reequilibra.
- **No hace falta `IndexPQ`:** nunca se cambia la prioridad de un pájaro ya metido; solo se inserta y se saca el máximo/mínimo.
- Alternativa ingenua: insertar ordenado en un vector (O(n) por pareja ⇒ O(n²)), demasiado lento con 100.000 parejas.
- Las edades son distintas, así que no hay empates con `lider`.

## Traza del ejemplo
Caso 1: empieza `30`.
```text
+10 +20 → menores {20,10}  mayores {}          dif 2 → 30 a mayores, lider = 20
          menores {10}  lider 20  mayores {30}                           → 20
+35 +25 → menores {10}  mayores {25,30,35}     dif 2 → 20 a menores, lider = 25
          menores {20,10}  lider 25  mayores {30,35}                     → 25
+5  +40 → menores {20,10,5}  mayores {30,35,40}  equilibrado             → 25
Salida: 20 25 25
```

## Coste
**O(P log P)** con P parejas: cada pareja hace un número constante de `push`/`pop` de coste logarítmico.
