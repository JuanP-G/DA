
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <utility>
#include <climits>
using namespace std;

#include "Pila.h"  // estructuras de datos de clase

/*@ <answer>

 Coleccionando cómics

 N pilas de cómics; cada cliente se lleva el menor identificador entre las cimas. Decir qué puesto
 de la fila hay que ocupar para llevarse el menor de toda la tienda. Acaba con el fichero.

 PLANTEAMIENTO (simulación)
 Cada pila es una Pila<int>; mientras se lee se calcula el mínimo de todo el caso. Cola de mínimos
 de pares (cima, pila): si la cima global es el buscado, ese es el puesto; si no, ese cliente se
 lleva el cómic, se desapila y, si la pila no queda vacía, entra su nueva cima.

 Coste: O(T log N) por caso, con T el total de cómics.

 Pilas           --> 1 <= N <= 100.000       (10^5)
 Comics por pila --> 1 <= K <= 100
 Identificador   --> 1 <= id <= 100.000.000  (10^8)
 Total comics    --> suma de K <= 1.000.000  (10^6)
 Puesto (salida) --> 1 <= puesto <= 1.000.000
 Todo cabe en int.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int n;
    if (!(cin >> n)) return false;

    // cola de MÍNIMOS de (identificador, nº de pila)
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;

    vector<Pila<int>> pilas(n);
    int mejor = INT_MAX;

    for (int i = 0; i < n; ++i) {
        int nComics;
        cin >> nComics;
        for (int j = 0; j < nComics; ++j) {
            int id;
            cin >> id;
            pilas[i].apila(id);              // del fondo a la cima: orden correcto
            if (id < mejor) mejor = id;
        }
        cola.push({ pilas[i].cima(), i });     // la cima de esta pila entra en juego
    }

    int puesto = 1;
    while (cola.top().first != mejor) {
        int p = cola.top().second;
        cola.pop();
        pilas[p].desapila();                 // ese cliente se lleva la cima
        if (!pilas[p].esVacia())             // si queda algo, asoma el siguiente
            cola.push({ pilas[p].cima(), p });
        ++puesto;
    }

    cout << puesto << '\n';
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
