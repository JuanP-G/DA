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

 La colecta de primavera

 V vecinos (1..1.000) y C cajas (0..4V). Para cada vecino se sabe cuanto pagaria por 1, 2,
 3 o 4 cajas (0 si no compra). Hay que repartir como mucho C cajas, como mucho 4 a cada
 vecino, para recaudar lo maximo. Escribir el beneficio y las cajas de cada vecino.

 PLANTEAMIENTO (programacion dinamica: mochila con grupos, un grupo por vecino)

     dinero(i, j) = maximo que se recauda con los vecinos 1..i y como mucho j cajas

     dinero(0, j) = 0
     dinero(i, j) = max   dinero(i - 1, j - k) + pago(i, k)       0 <= k <= min(4, j)
                  k

 con pago(i, 0) = 0. Respuesta: dinero(V, C).

 Se guarda la tabla entera para reconstruir el reparto: desde (V, C) hacia atras, para cada
 vecino i se busca el k que da dinero(i, j) (cualquiera sirve) y se pasa a (i - 1, j - k).

 Coste: O(V * C * 4) en tiempo y O(V * C) en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int V, C;
    cin >> V >> C;
    vector<vector<int>> pago(V + 1, vector<int>(5, 0));
    for (int k = 1; k <= 4; ++k)
        for (int i = 1; i <= V; ++i) cin >> pago[i][k];

    vector<vector<int>> dinero(V + 1, vector<int>(C + 1, 0));
    for (int i = 1; i <= V; ++i)
        for (int j = 0; j <= C; ++j) {
            int mejor = 0;
            for (int k = 0; k <= min(4, j); ++k)
                mejor = max(mejor, dinero[i - 1][j - k] + pago[i][k]);
            dinero[i][j] = mejor;
        }

    vector<int> cajas(V + 1, 0);
    for (int i = V, j = C; i >= 1; --i) {
        for (int k = 0; k <= min(4, j); ++k)
            if (dinero[i][j] == dinero[i - 1][j - k] + pago[i][k]) {
                cajas[i] = k;
                j -= k;
                break;
            }
    }

    cout << dinero[V][C] << '\n';
    for (int i = 1; i <= V; ++i) cout << cajas[i] << (i < V ? ' ' : '\n');
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
