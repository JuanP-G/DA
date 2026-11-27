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

 Bizcocho con frutas

 N trozos en fila (N par, 2..1.000); cada uno lleva 0 (nada), 1 (naranja) o 2 (limon). Cada dia
 se cortan dos trozos SOLO por los extremos: los dos por la izquierda, los dos por la derecha o
 uno de cada lado. Maximo numero de dias en que los dos trozos tienen la misma fruta.

 PLANTEAMIENTO (programacion dinamica sobre intervalos)

     dias(i, j) = maximo de dias buenos con los trozos i..j (siempre un numero par de trozos)

     dias(i, j) = 0                                          si no quedan trozos (i > j)
     dias(i, j) = max( dias(i+2, j)   + igual(i, i+1),       los dos por la izquierda
                       dias(i, j-2)   + igual(j-1, j),       los dos por la derecha
                       dias(i+1, j-1) + igual(i, j) )        uno de cada lado

 igual(a, b) = 1 si los trozos a y b tienen la misma fruta y no es 0; si no, 0.
 Se rellena por longitudes pares crecientes. Respuesta: dias(1, N).

 Coste: O(N^2) en tiempo y en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int n;
    cin >> n;
    if (!cin)  // fin de la entrada
        return false;
    vector<int> f(n + 1);
    for (int i = 1; i <= n; ++i) cin >> f[i];

    auto igual = [&](int a, int b) { return f[a] != 0 && f[a] == f[b] ? 1 : 0; };

    // dias[i][j] = 0 si i > j (se dejan filas y columnas de sobra)
    Matriz<int> dias(n + 3, n + 3, 0);
    for (int largo = 2; largo <= n; largo += 2)
        for (int i = 1; i + largo - 1 <= n; ++i) {
            int j = i + largo - 1;
            int izquierda = dias[i + 2][j] + igual(i, i + 1);
            int derecha = dias[i][j - 2] + igual(j - 1, j);
            int unoYuno = dias[i + 1][j - 1] + igual(i, j);
            dias[i][j] = max({ izquierda, derecha, unoYuno });
        }

    cout << dias[1][n] << '\n';
    return true;
}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   while (resuelveCaso());

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
