
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

 El cazatesoros
 
 Una botella para T segundos bajo el agua (1..10.000) y N cofres (1..100), cada uno con su
 profundidad p (1..500) y su oro (1..10.000). Subir un cofre cuesta p segundos de bajada y
 2p de subida, y en cada inmersion se sube un solo cofre. Escribir el maximo oro, cuantos
 cofres hay que coger y cada uno (profundidad y oro como en la entrada), y despues ---.

 PLANTEAMIENTO (programacion dinamica: mochila 0/1)
 Cada cofre es un objeto de peso 3p (segundos) y valor su oro; la mochila tiene capacidad T.
 
     oro(i, j) = maximo oro con los cofres 1..i y j segundos de aire
 
     oro(0, j) = 0
     oro(i, j) = oro(i - 1, j)                                   si 3 p_i > j
               = max(oro(i - 1, j), oro(i - 1, j - 3 p_i) + o_i)  si no
 
 Se guarda la tabla entera para saber que cofres se han cogido: desde (N, T) hacia atras,
 si oro(i, j) != oro(i - 1, j) el cofre i se ha cogido y se pasa a (i - 1, j - 3 p_i).
 Los cofres se escriben en el orden de la entrada.
 
 Coste: O(N * T) en tiempo y en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int T, N;
    cin >> T >> N;
    vector<int> prof(N + 1), oro(N + 1);
    for (int i = 1; i <= N; ++i) cin >> prof[i] >> oro[i];

    Matriz<int> mejor(N + 1, T + 1, 0);
    for (int i = 1; i <= N; ++i) {
        int tiempo = 3 * prof[i];
        for (int j = 0; j <= T; ++j) {
            mejor[i][j] = mejor[i - 1][j];
            if (tiempo <= j) mejor[i][j] = max(mejor[i][j], mejor[i - 1][j - tiempo] + oro[i]);
        }
    }

    vector<bool> cogido(N + 1, false);
    int numCofres = 0;
    for (int i = N, j = T; i >= 1; --i) {
        if (mejor[i][j] != mejor[i - 1][j]) {
            cogido[i] = true;
            ++numCofres;
            j -= 3 * prof[i];
        }
    }

    cout << mejor[N][T] << '\n' << numCofres << '\n';
    for (int i = 1; i <= N; ++i)
        if (cogido[i]) cout << prof[i] << ' ' << oro[i] << '\n';
    cout << "---\n";
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
