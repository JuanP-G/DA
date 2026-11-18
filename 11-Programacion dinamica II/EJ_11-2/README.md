# EJ 11-2 · Aibofobia

📄 Enunciado: en el juez de la asignatura (`Ej11-2`) · 💻 [Solución](EJ_11-2.cpp)

## Qué piden
Una palabra de 1 a 1.000 letras minúsculas. Hay que escribir el **mínimo número de letras que añadir** (en cualquier posición) para convertirla en un palíndromo, y **uno de esos palíndromos**. Vale cualquiera de los que tengan el mínimo.

## Cómo se plantea
Programación dinámica **sobre intervalos** de la palabra:

```text
faltan(i, j) = mínimo de letras a añadir para que s[i..j] sea un palíndromo

faltan(i, j) = 0                                          si i >= j
             = faltan(i+1, j−1)                           si s[i] == s[j]
             = 1 + min(faltan(i+1, j), faltan(i, j−1))    si no
```
Si los extremos son iguales, se emparejan entre sí. Si no, a uno de los dos se le pone una copia al otro lado: a `s[i]` (y queda `s[i+1..j]`) o a `s[j]` (y queda `s[i..j−1]`).

La tabla se rellena por **longitudes crecientes** del intervalo. Después se **reconstruye** desde `(0, n−1)`, construyendo a la vez la mitad izquierda y la derecha:
- `s[i] == s[j]`: `s[i]` a la izquierda, `s[j]` a la derecha, y a `(i+1, j−1)`;
- si conviene emparejar `s[i]`: `s[i]` en los dos lados, y a `(i+1, j)`;
- si no: `s[j]` en los dos lados, y a `(i, j−1)`;
- si queda una letra en el centro (`i == j`), va una sola vez.

## Traza de `amad`
```text
a…d distintos: faltan(1,3) "mad" = 2,  faltan(0,2) "ama" = 0  → mejor emparejar la d
izq = "d",  der = "d",  queda "ama"
a = a: izq = "da", der = "da",  queda "m" en el centro
izq + "m" + reverse(der) = "damad"                       → 1 damad
```

## Por qué así
- **Equivale a la subsecuencia palindrómica más larga:** `faltan(0, n−1) = n − LPS`. Las letras que ya forman palíndromo se quedan, y a cada una de las demás se le añade su pareja.
- **Coste:** O(n²) en tiempo y en espacio (10⁶ casillas para n = 1.000).

## Ojo con
- Hay muchas respuestas válidas: para `roda` esta solución escribe `rodador` y el enunciado `adoroda`. El juez acepta las dos.
- Si la palabra ya es un palíndromo se escribe `0` y la propia palabra.
