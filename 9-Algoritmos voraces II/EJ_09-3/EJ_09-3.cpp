
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

 Carreras de coches
 
 N pilas (1 <= N <= 300.000) con su voltaje (0..10^6) y un voltaje minimo V (0..2*10^6).
 Cada coche necesita dos pilas cuyos voltajes sumen al menos V. Escribir el maximo numero de
 coches que pueden funcionar a la vez.

 PLANTEAMIENTO (voraz: emparejar extremos)
 Se ordenan las pilas y se miran la mas debil (i) y la mas fuerte (j):
   - si juntas llegan a V, forman un coche: la mas debil que puede acompanar a la mas fuerte
     es la mejor pareja para ella (las mas potentes se guardan para las demas);
   - si no llegan, la mas debil no sirve con NINGUNA otra (la mas fuerte ya no basta) y se
     descarta.
 
 Coste: O(N log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, V;
    cin >> N >> V;
    vector<int> pilas(N);
    for (int& p : pilas) cin >> p;
    sort(pilas.begin(), pilas.end());

    int coches = 0;
    int i = 0, j = N - 1;
    while (i < j) {
        if (pilas[i] + pilas[j] >= V) {    // pareja valida: un coche mas
            ++coches;
            ++i; --j;
        } else {
            ++i;                           // la mas debil no sirve con nadie
        }
    }
    cout << coches << '\n';
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
