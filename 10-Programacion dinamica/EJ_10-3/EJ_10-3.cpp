
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

#include "Matriz.h"

/*@ <answer>

 Esquivando las obras en los cruces
 
 Ciudad de N calles este-oeste y M calles norte-sur (1 <= N, M <= 50); cada cruce es '.'
 (libre) o 'X' (obras). Contar los caminos MAS CORTOS de la esquina noroeste (0, 0) a la
 sureste (N - 1, M - 1) que no pasan por obras (el resultado es siempre < 10^9).

 PLANTEAMIENTO (programacion dinamica: contar caminos en una cuadricula)
 Un camino de longitud minima solo avanza hacia el sur o hacia el este, asi que a un cruce
 (i, j) solo se llega desde el de arriba (i - 1, j) o desde el de la izquierda (i, j - 1):
 
     caminos(0, 0) = 1
     caminos(i, j) = 0                                      si (i, j) tiene obras
                   = caminos(i - 1, j) + caminos(i, j - 1)  si no (fuera de la ciudad vale 0)
 
 Se guarda en una Matriz (Matriz.h) y se rellena por filas, de arriba abajo y de izquierda a
 derecha, asi que cuando se llega a (i, j) ya estan calculados el de arriba y el de la izquierda.

 Coste: O(N * M) en tiempo y en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, M;
    cin >> N >> M;
    vector<string> mapa(N);
    for (int i = 0; i < N; ++i) cin >> mapa[i];

    Matriz<long long> caminos(N, M, 0);
    caminos[0][0] = 1;                    // la esquina noroeste nunca tiene obras
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            if (mapa[i][j] == 'X') caminos[i][j] = 0;
            else {
                if (i > 0) caminos[i][j] += caminos[i - 1][j];   // desde arriba
                if (j > 0) caminos[i][j] += caminos[i][j - 1];   // desde la izquierda
            }
        }
    }
    cout << caminos[N - 1][M - 1] << '\n';
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
