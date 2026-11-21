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

/*@ <answer>

 El carpintero Ebanisto

 Un tablon de longitud L (10..10^6) con N marcas (1..500) en orden creciente. Cortar un
 trozo en dos cuesta el doble de su longitud. Minimo esfuerzo para hacer todos los cortes.

 PLANTEAMIENTO (programacion dinamica sobre intervalos)
 Puntos p_0 = 0, p_1..p_N = las marcas, p_{N+1} = L.
     esfuerzo(i, j) = minimo esfuerzo para hacer todos los cortes entre p_i y p_j
     esfuerzo(i, i+1) = 0                                   (trozo sin marcas)
     esfuerzo(i, j) = 2*(p_j - p_i) + min { esfuerzo(i, k) + esfuerzo(k, j) : i < k < j }
 El primer corte del trozo (i, j) cuesta 2*(p_j - p_i) sea cual sea la marca k elegida; luego
 cada mitad se corta por separado. Respuesta: esfuerzo(0, N+1).
 Se rellena por longitud de intervalo creciente (j - i = 2, 3, ..., N+1).
 Cota: cada marca esta en como mucho N trozos cortados, 2 * L * N <= 10^9: cabe en long long
 de sobra (y casi en int).

 Coste: O(N^3) en tiempo y O(N^2) en espacio por caso.

 @ </answer> */

// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int L, N;
    cin >> L >> N;
    vector<long long> p(N + 2);
    p[0] = 0;
    for (int i = 1; i <= N; ++i) cin >> p[i];
    p[N + 1] = L;

    int P = N + 2;
    vector<vector<long long>> esfuerzo(P, vector<long long>(P, 0));
    for (int d = 2; d < P; ++d) {                // d = j - i
        for (int i = 0; i + d < P; ++i) {
            int j = i + d;
            long long mejor = -1;
            for (int k = i + 1; k < j; ++k) {
                long long e = esfuerzo[i][k] + esfuerzo[k][j];
                if (mejor < 0 || e < mejor) mejor = e;
            }
            esfuerzo[i][j] = 2 * (p[j] - p[i]) + mejor;
        }
    }
    cout << esfuerzo[0][N + 1] << '\n';
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
