
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <queue>
#include <vector>
#include <functional>
using namespace std;

/*@ <answer>

 Pájaros en vuelo

 Una bandada empieza con un pájaro y se le unen parejas. Tras cada pareja escribir la mediana de
 las edades. La entrada acaba con un caso 0 0.

 PLANTEAMIENTO (mediana con dos montículos)
 lider = mediana; menores = cola de máximos con los más jóvenes; mayores = cola de mínimos con los
 más viejos, siempre del mismo tamaño. Cada pájaro nuevo va a su lado; si un lado queda con dos
 más, el líder pasa al lado pequeño y la cima del grande es el nuevo líder.

 Coste: O(log P) por pareja.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int primero, parejas;
    cin >> primero >> parejas;

    if (primero == 0 && parejas == 0) return false;

    priority_queue<int> menores;                             // max-heap
    priority_queue<int, vector<int>, greater<int>> mayores;  // min-heap
    int lider = primero;

    for (int i = 0; i < parejas; ++i) {
        for (int j = 0; j < 2; ++j) {
            int edad; cin >> edad;

            if (edad < lider) menores.push(edad);
            else mayores.push(edad);
        }
        if (menores.size() > mayores.size()) {
            mayores.push(lider);
            lider = menores.top(); menores.pop();
        }
        else if (mayores.size() > menores.size()) {
            menores.push(lider);
            lider = mayores.top(); mayores.pop();
        }
        cout << lider << (i + 1 < parejas ? ' ' : '\n');
    }
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
