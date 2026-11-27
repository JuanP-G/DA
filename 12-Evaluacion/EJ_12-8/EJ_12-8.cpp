/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

/*@ <answer>

 Volando entre pivotes

 N pivotes (2..100.000). De un pivote se puede ir a cualquiera de los K+1 siguientes (K = 0..10
 pivotes saltados como mucho). Cuantas formas hay de ir del 1 al N, modulo 1.000.000.007.

 PLANTEAMIENTO (programacion dinamica en una dimension)

     formas(i) = numero de formas de llegar al pivote i

     formas(1) = 1
     formas(i) = formas(i-1) + formas(i-2) + ... + formas(i-K-1)     (solo indices >= 1)

 La suma es una ventana de K+1 casillas: al avanzar se suma la que entra y se resta la que
 sale, siempre modulo 1.000.000.007 (al restar se suma el modulo para no quedar en negativo).

 Coste: O(N) en tiempo y en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

const int MOD = 1000000007;

void resuelveCaso() {
    int n, k;
    cin >> n >> k;
    vector<int> formas(n + 1, 0);
    formas[1] = 1;
    long long ventana = 1;                    // formas(i-K-1) + ... + formas(i-1)
    for (int i = 2; i <= n; ++i) {
        formas[i] = ventana;
        ventana = (ventana + formas[i]) % MOD;
        if (i - k - 1 >= 1)                   // el que queda fuera para el siguiente
            ventana = (ventana - formas[i - k - 1] + MOD) % MOD;
    }
    cout << formas[n] << '\n';
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
