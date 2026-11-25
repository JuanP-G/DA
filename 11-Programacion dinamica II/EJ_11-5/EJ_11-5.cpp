/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

#include "Matriz.h"

/*@ <answer>

 Las vacas pensantes

 Una hilera de N cubos (1..1.000) con cantidades distintas de comida. Dos vacas se alternan;
 en cada turno se elige uno de los DOS EXTREMOS, se come y se retira. Empieza nuestra vaca;
 Devoradora siempre coge el extremo MAYOR. Cuanto puede comer nuestra vaca como maximo?

 PLANTEAMIENTO (programacion dinamica sobre intervalos)

     come(i, j) = maximo que come nuestra vaca con los cubos i..j cuando le toca a ELLA

     come(i, j) = 0                                                 si i > j
     come(i, j) = max( a_i + despues(i + 1, j),  a_j + despues(i, j - 1) )

 donde despues(l, r) es lo que come nuestra vaca con l..r cuando acaba de elegir ella y
 ahora le toca a Devoradora, que SE SABE lo que hara (coge el extremo mayor):

     despues(l, r) = 0                        si l > r
                   = come(l + 1, r)           si a_l > a_r    (Devoradora se come a_l)
                   = come(l, r - 1)           si a_l < a_r    (Devoradora se come a_r)

 Como las cantidades son distintas, nunca hay empate. Respuesta: come(1, N).

 Cada intervalo depende de otros mas cortos, asi que se rellena por longitudes crecientes.

 Coste: O(N^2) en tiempo y en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int n;
    cin >> n;
    vector<int> a(n + 2);
    for (int i = 1; i <= n; ++i) cin >> a[i];

    // come[i][j], con come[i][j] = 0 si i > j (se deja una fila y columna de sobra)
    Matriz<int> come(n + 3, n + 3, 0);
    auto despues = [&](int l, int r) {
        if (l > r) return 0;
        return a[l] > a[r] ? come[l + 1][r] : come[l][r - 1];
    };
    for (int largo = 1; largo <= n; ++largo)
        for (int i = 1; i + largo - 1 <= n; ++i) {
            int j = i + largo - 1;
            come[i][j] = max(a[i] + despues(i + 1, j), a[j] + despues(i, j - 1));
        }

    cout << come[1][n] << '\n';
}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   int numCasos;
   std::cin >> numCasos;
   for (int i = 0; i < numCasos; ++i)
      resuelveCaso();

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
