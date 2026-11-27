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

#include "EnterosInf.h"
#include "Matriz.h"

/*@ <answer>

 Mejor no llevar muchas monedas

 N tipos de monedas (1..100) con valor v_i y c_i unidades (1..1.000). Pagar EXACTAMENTE el
 precio P (1..10.000) con el menor numero de monedas, o decir que no se puede.

 PLANTEAMIENTO (cambio de monedas con cantidades limitadas)

     monedas(i, j) = minimo numero de monedas para pagar j usando los tipos 1..i

     monedas(0, 0) = 0,   monedas(0, j) = +Inf  si j > 0
     monedas(i, j) = min { monedas(i-1, j - k*v_i) + k  :  0 <= k <= min(c_i, j / v_i) }

 Respuesta: monedas(N, P); si es +Inf no se puede. Para saber cuantas de cada tipo se usan se
 recorre la tabla hacia atras desde (N, P) buscando el k que dio el valor de la casilla.

 Coste: O(P * (suma de min(c_i, P/v_i))) en tiempo y O(N * P) en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int n, P;
    cin >> n;
    vector<int> v(n + 1), c(n + 1);
    for (int i = 1; i <= n; ++i) cin >> v[i];
    for (int i = 1; i <= n; ++i) cin >> c[i];
    cin >> P;

    Matriz<EntInf> monedas(n + 1, P + 1, Infinito);
    monedas[0][0] = 0;
    for (int i = 1; i <= n; ++i)
        for (int j = 0; j <= P; ++j) {
            monedas[i][j] = monedas[i - 1][j];                    // ninguna del tipo i
            for (int k = 1; k <= c[i] && k * v[i] <= j; ++k) {    // k monedas del tipo i
                EntInf con = monedas[i - 1][j - k * v[i]] + k;
                if (con < monedas[i][j]) monedas[i][j] = con;
            }
        }

    if (monedas[n][P] == Infinito) {
        cout << "NO\n";
        return;
    }
    // reconstruccion: cuantas monedas de cada tipo
    vector<int> usadas(n + 1, 0);
    int j = P;
    for (int i = n; i >= 1; --i) {
        int k = 0;
        while (monedas[i - 1][j - k * v[i]] + k != monedas[i][j]) ++k;
        usadas[i] = k;
        j -= k * v[i];
    }
    cout << "SI";
    for (int i = 1; i <= n; ++i) cout << ' ' << usadas[i];
    cout << '\n';
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
