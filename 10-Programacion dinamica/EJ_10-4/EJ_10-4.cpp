
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

 ¿Por donde hay que subir?
 
 Tablero N x N (3 <= N <= 1.000) con numeros 1..10.000. Se empieza en una casilla de la ultima
 fila y se sube hasta la primera; en cada paso se va a una de las tres casillas de la fila de
 encima (en vertical o en diagonal) sin salirse. Escribir la suma maxima y la columna (1..N)
 de la ultima fila por la que hay que empezar (la de mas a la izquierda si hay varias).

 PLANTEAMIENTO (programacion dinamica)
     mejor(i, j) = suma maxima de un recorrido que empieza en (i, j) y sube hasta la fila 1
 
     mejor(1, j) = t(1, j)
     mejor(i, j) = t(i, j) + max( mejor(i - 1, j - 1), mejor(i - 1, j), mejor(i - 1, j + 1) )
                   (solo las columnas que existen)
 
 La respuesta es el maximo de mejor(N, j); con '>' estricto al recorrer j de izquierda a
 derecha, en caso de empate se queda la columna de mas a la izquierda.
 
 Se guarda en una Matriz (Matriz.h) y se rellena fila a fila, de arriba (fila 1) abajo.

 Coste: O(N^2) en tiempo y en espacio por caso (la suma maxima es <= 10^7: cabe en int).

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N;
    cin >> N;
    Matriz<int> mejor(N, N);
    for (int j = 0; j < N; ++j) cin >> mejor[0][j];           // fila 1
    for (int i = 1; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            int t;
            cin >> t;
            int mejorArriba = mejor[i - 1][j];
            if (j > 0) mejorArriba = max(mejorArriba, mejor[i - 1][j - 1]);
            if (j + 1 < N) mejorArriba = max(mejorArriba, mejor[i - 1][j + 1]);
            mejor[i][j] = t + mejorArriba;
        }
    }

    int col = 0;
    for (int j = 1; j < N; ++j)
        if (mejor[N - 1][j] > mejor[N - 1][col]) col = j;
    cout << mejor[N - 1][col] << ' ' << col + 1 << '\n';
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
