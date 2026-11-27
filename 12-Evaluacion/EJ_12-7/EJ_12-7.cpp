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

 Oposiciones a notaria

 n documentos (2..200) de p_i paginas (hasta 1.000), en orden. Se fusionan de dos en dos
 documentos CONTIGUOS y cada fusion cuesta las paginas del resultado. Minimo tiempo total.

 PLANTEAMIENTO (programacion dinamica sobre intervalos, como la multiplicacion de matrices)

     tiempo(i, j) = minimo tiempo para fusionar en uno los documentos i..j

     tiempo(i, i) = 0
     tiempo(i, j) = min { tiempo(i, k) + tiempo(k+1, j)  :  i <= k < j }  +  paginas(i..j)

 La ULTIMA fusion une el bloque i..k con el bloque k+1..j y siempre cuesta paginas(i..j),
 que se obtiene con sumas acumuladas. Se rellena por longitudes crecientes.
 Cabe en int: 200 * 1.000 paginas, cada una movida como mucho 199 veces.

 Coste: O(n^3) en tiempo y O(n^2) en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int n;
    cin >> n;
    if (!cin || n == 0)  // caso sin documentos: fin
        return false;
    vector<int> suma(n + 1, 0);              // suma[i] = paginas de los documentos 1..i
    for (int i = 1; i <= n; ++i) {
        int p;
        cin >> p;
        suma[i] = suma[i - 1] + p;
    }

    Matriz<int> tiempo(n + 1, n + 1, 0);
    for (int largo = 2; largo <= n; ++largo)
        for (int i = 1; i + largo - 1 <= n; ++i) {
            int j = i + largo - 1;
            int mejor = tiempo[i][i] + tiempo[i + 1][j];
            for (int k = i + 1; k < j; ++k)
                mejor = min(mejor, tiempo[i][k] + tiempo[k + 1][j]);
            tiempo[i][j] = mejor + suma[j] - suma[i - 1];
        }

    cout << tiempo[1][n] << '\n';
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
