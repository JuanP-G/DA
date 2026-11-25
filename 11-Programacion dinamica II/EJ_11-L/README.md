# EJ 11-L · La fiesta de graduación

📄 [Enunciado](../Enunciados/prob-La%20fiesta%20de%20graduaci%C3%B3n.pdf) · 💻 [Solución](EJ_11-L.cpp)

🧩 Plantilla: [**número de casos**](../../Plantillas/1.NumeroCasos.cpp) — la entrada empieza con el número de casos y `void resuelveCaso()` resuelve uno.

## Qué piden
Dos listas de canciones (la de mañana y la de tarde), de hasta 1.000 títulos cada una, **con repeticiones posibles**. La lista final solo puede tener canciones de **las dos**, en el **mismo orden** en que salen en cada una (se pueden saltar canciones), y cada repetición debe corresponder a una aparición distinta en cada lista. Hay que escribir la **más larga** (o una línea vacía si no hay ninguna).

## Recurrencia (formato de examen) · subsecuencia común más larga

Listas $a_1 \dots a_n$ y $b_1 \dots b_m$. Para $0 \le i \le n$, $0 \le j \le m$:

$$
\text{larga}(i, j) = \text{longitud de la mayor lista común usando } a_1..a_i \text{ y } b_1..b_j
$$

**Casos base**

$$
\text{larga}(i, 0) = 0 \qquad \text{larga}(0, j) = 0
$$

**Recurrencia** ($i, j \ge 1$)

$$
\text{larga}(i, j) =
\begin{cases}
\text{larga}(i-1, j-1) + 1 & \text{si } a_i = b_j \\
\max\big(\text{larga}(i-1, j),\ \text{larga}(i, j-1)\big) & \text{si } a_i \ne b_j
\end{cases}
$$

**Llamada inicial / respuesta:** $\text{larga}(n, m)$.

**Reconstrucción** desde $(n, m)$: si $a_i = b_j$, la canción $a_i$ está en la lista y se pasa a $(i-1, j-1)$; si no, se pasa al vecino con mayor valor, $(i-1, j)$ si $\text{larga}(i-1, j) \ge \text{larga}(i, j-1)$, y a $(i, j-1)$ en otro caso. Las canciones salen **de la última a la primera**, así que se dan la vuelta al escribir.

**Coste:** $O(n \cdot m)$ en tiempo y en espacio (un millón de casillas como mucho).

## Cómo se plantea
Es la clásica **subsecuencia común más larga (LCS)**, con palabras en vez de letras.

```text
larga[i][j] = a[i] == b[j] ? larga[i−1][j−1] + 1
                            : max(larga[i−1][j], larga[i][j−1])
```
La tabla se guarda **entera** para poder reconstruir la lista, que se va construyendo desde el final.

Cada línea de entrada es una lista con las palabras separadas por espacios, así que se lee con `getline` y se trocea con un `istringstream` (una lista **puede estar vacía**, por eso no basta con `cin >> palabra`).

## Traza del ejemplo 1
```text
mañana: One Respect Radio_Ga_Ga One Volando_voy Caruso
tarde:  Respect One Volando_voy Ne_me_quitte_pas Radio_Ga_Ga

en común y en orden: Respect · One · Volando_voy      (la One de mañana es la segunda)
Radio_Ga_Ga también está en las dos, pero en la tarde va al final: no cabe con las demás
→ Respect One Volando_voy
```

## Por qué así
- **Repeticiones:** la LCS ya las trata bien. Cada coincidencia `a_i = b_j` **gasta** una posición de cada lista y se pasa a `(i−1, j−1)`, así que una canción repetida en la lista final necesita una aparición distinta en cada lista original.
- **Condición (2) del enunciado** es exactamente «subsecuencia» de las dos listas, y la **(1)** («solo canciones de ambas») la cumple por construcción.

## Ojo con
- Si no hay canciones comunes hay que escribir una **línea vacía** (aquí sale sola: la lista queda vacía y solo se escribe `\n`).
- Hay varias soluciones igual de largas (ejemplo 4: `Columbia` o `Bohemian_Rhapsody`); el juez acepta cualquiera.
- Tras leer el número de casos con `cin >>` queda en la entrada el **salto de línea** de esa primera línea: antes de leer la primera lista con `getline` hay que consumirlo (la variable `primera`).
