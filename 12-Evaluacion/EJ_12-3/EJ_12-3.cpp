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

 Bollos preñaos

 N tipos de chorizo (1..50) y M gramos de masa (1..1.000). Del tipo i hay g_i gramos; cada
 bollo lleva c_i gramos de ese chorizo y m_i de masa y se vende a p_i euros (todo 1..100).
 Maximo de euros.

 PLANTEAMIENTO (programacion dinamica: mochila con cantidades acotadas)
 Del tipo i se pueden hacer como mucho k_i = g_i / c_i bollos (division entera): el chorizo
 limita cuantos, la masa es la capacidad compartida de la mochila.
     bollos(i, j) = maximo de euros con los tipos 1..i y j gramos de masa
     bollos(0, j) = 0
     bollos(i, j) = max { bollos(i-1, j - t*m_i) + t*p_i  :  0 <= t <= k_i,  t*m_i <= j }
 La respuesta es bollos(N, M) (no hace falta gastar toda la masa).
 Con un vector por fila (se copia la anterior antes de rellenar la nueva).

 Coste: O(M * suma de k_i) <= O(1.000 * 5.000) por caso; espacio O(M).

 @ </answer> */

// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, M;
    cin >> N >> M;
    vector<int> euros(M + 1, 0);                 // fila i-1: euros[j] con j gramos de masa
    for (int i = 0; i < N; ++i) {
        int g, c, m, p;
        cin >> g >> c >> m >> p;
        int k = g / c;                           // bollos de este tipo como mucho
        vector<int> nueva = euros;               // t = 0: no hacer ningun bollo de este tipo
        for (int j = 0; j <= M; ++j)
            for (int t = 1; t <= k && t * m <= j; ++t)
                nueva[j] = max(nueva[j], euros[j - t * m] + t * p);
        euros = nueva;
    }
    cout << euros[M] << '\n';
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
