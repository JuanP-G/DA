/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <algorithm>
using namespace std;

/*@ <answer>

 Una gira agotadora

 N dias (1..150.000) con la recaudacion de cada uno. No se puede actuar dos dias seguidos.
 Recaudacion maxima.

 PLANTEAMIENTO (programacion dinamica en una dimension)

     gira(i) = recaudacion maxima con los i primeros dias

     gira(0) = 0,   gira(1) = r_1
     gira(i) = max( gira(i-1),            el dia i se descansa
                    gira(i-2) + r_i )     el dia i se actua (y el i-1 se descansa)

 Solo hacen falta los dos ultimos valores. Cabe en int: 75.000 * 10.000 = 7,5 * 10^8.

 Coste: O(N) en tiempo y O(1) en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int n;
    cin >> n;
    int dosAtras = 0, anterior = 0;          // gira(i-2) y gira(i-1)
    for (int i = 0; i < n; ++i) {
        int r;
        cin >> r;
        int actual = max(anterior, dosAtras + r);
        dosAtras = anterior;
        anterior = actual;
    }
    cout << anterior << '\n';
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
