
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

 Agujeros en la manguera
 
 N agujeros (1 <= N <= 100.000) en posiciones 1..10^9 dadas en orden no decreciente (puede
 haber varios en la misma posicion) y parches de longitud L (1..1.000). Un parche tapa los
 agujeros separados como mucho L entre si. Escribir el minimo numero de parches.

 PLANTEAMIENTO (voraz)
 El agujero mas a la izquierda que siga sin tapar tiene que quedar dentro de algun parche.
 Lo mejor es empezar el parche justo en el: asi llega lo mas lejos posible (hasta p + L) y
 tapa todos los agujeros de [p, p + L]. Se repite con el primer agujero que quede fuera.
 
 Por que es optimo: cualquier solucion tiene un parche que tapa el primer agujero p; ese
 parche no llega mas alla de p + L, asi que el nuestro tapa al menos lo mismo que el suyo
 (a la derecha de p no hay nada sin tapar que el pudiera tapar y el nuestro no).
 
 Coste: O(N) por caso (las posiciones ya vienen ordenadas).

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, L;
    cin >> N >> L;
    vector<int> pos(N);
    for (int& p : pos) cin >> p;

    int parches = 0;
    long long finParche = -1;          // hasta donde llega el ultimo parche puesto
    for (int p : pos) {
        if (p > finParche) {           // agujero sin tapar: parche nuevo que empieza en el
            ++parches;
            finParche = (long long)p + L;
        }
    }
    cout << parches << '\n';
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
