
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>

using namespace std;

#include "bintree.h"  // estructuras de datos de clase
#include "TreeSet_AVL_plantilla.h"  // estructuras de datos de clase

/*@ <answer>

 Encontrar el k-ésimo elemento en un árbol AVL

 Se insertan N valores en un Set (árbol AVL) y para cada consulta k se escribe el k-ésimo menor,
 o ?? si no existe. Tras cada caso, ---. La entrada acaba con un caso con N = 0.

 PLANTEAMIENTO
 Cada nodo guarda tami = tamaño de su hijo izquierdo + 1 (la posición de la raíz en su subárbol),
 mantenido en inserta y en las rotaciones (ver TreeSet_AVL_plantilla.h). kesimo(k) baja desde la raíz:
 k == tami -> la raíz; k < tami -> izquierdo con el mismo k; k > tami -> derecho con k - tami.
 Si se llega a un hueco lanza out_of_range y se escribe ??.

 Coste: O(log N) por inserción y por consulta: O((N + Q) log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int nValores;
    cin >> nValores;
    if (!cin || nValores == 0)  // caso especial: 0 marca el final
        return false;

    // entrada de los valores del arbol
    Set<int> arbol;
    for (int i = 0; i < nValores; ++i) {
        int valor;
        cin >> valor;
        arbol.insert(valor);
    }

    // consultas
    int nConsultas;
    cin >> nConsultas;
    for (int i = 0; i < nConsultas; ++i) {
        int posValor;
        cin >> posValor;
        try {
            cout << arbol.kesimo(posValor) << '\n';
        }
        catch (out_of_range&) {
            cout << "??\n";
        }
    }
    cout << "---\n";  // separador entre casos
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
