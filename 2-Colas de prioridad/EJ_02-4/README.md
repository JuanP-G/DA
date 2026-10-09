# EJ 02-4 · La ley D'Hondt

📄 [Enunciado](<../Enunciados/prob-La ley D'Hondt.pdf>) · 💻 [Solución](EJ_02-4.cpp)

## Qué piden
Repartir N escaños entre C candidaturas con el **método D'Hondt** y escribir los escaños de cada una en el orden de la entrada.

## Cómo se plantea
El método ya dice qué hacer: dar el siguiente escaño a la candidatura de **mayor coeficiente** `votos / (1 + escaños)`. Se necesita el máximo repetidas veces mientras los coeficientes cambian → **cola de prioridad de máximos**.

Cada elemento es una `Candidatura { votos, escanios, orden }`, y `operator<` («tiene menos prioridad que») compara por:

| Criterio | Gana (sube a la cima) |
|---|---|
| 1. coeficiente `v / (1 + e)` | el mayor |
| 2. votos | el que tiene más |
| 3. `orden` en la entrada | el que aparece antes |

1. Todas entran con 0 escaños (coeficiente = votos).
2. N veces: se saca la cima, `++escanios` y se vuelve a meter (su coeficiente ha bajado).
3. Se vacía la cola guardando cada resultado en `res[orden]` y se escribe `res` en orden de entrada.

## Por qué así
- **Sin divisiones:** `v₁/(1+e₁) < v₂/(1+e₂)` ⇔ `v₁·(1+e₂) < v₂·(1+e₁)`. Con números reales, dos coeficientes iguales podrían salir distintos por redondeo y romper el desempate.
- **`long long`** porque el producto votos · escaños puede pasar de 2³¹.
- **Cuidado con el sentido del desempate en `operator<`:** «tiene menos prioridad» es el que aparece **después**, por eso la última línea es `orden > o.orden` (y no `<`). Es el error típico.
- El campo `orden` sirve a la vez para desempatar y para recolocar la salida, ya que la cola los devuelve desordenados.
- Alternativa: recorrer las C candidaturas en cada escaño, O(N·C); la cola lo deja en O(N log C).

## Traza del ejemplo
```text
Caso 1: votos 100 226 20 80 170, N = 4
  escaño 1: coef máx 226/1 -> cand 1   (226 pasa a 226/2 = 113)
  escaño 2: coef máx 170/1 -> cand 4   (170 pasa a 85)
  escaño 3: coef máx 226/2 -> cand 1   (113 > 100; pasa a 75,3)
  escaño 4: coef máx 100/1 -> cand 0
  salida: 1 2 0 0 1
Caso 2: votos 60 28 60, N = 3
  escaño 1: 60 vs 60, mismos votos -> índice menor: cand 0 (pasa a 30)
  escaño 2: cand 2 (60)
  escaño 3: 30 vs 30 (cand 0 y 2), mismos votos -> cand 0
  salida: 2 0 1
```

## Coste
**O((C + N) log C)** por caso: C inserciones y N extracciones/reinserciones en una cola de tamaño C (más el vaciado final, O(C log C)).
