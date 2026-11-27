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

 Megaautopista de Oriente

 N areas de descanso (1..300.000) en orden de punto kilometrico, cada una con su beneficio.
 Dos restaurantes deben estar a D kilometros o mas. Beneficio maximo y DONDE construirlos.

 PLANTEAMIENTO (programacion dinamica con reconstruccion)

     gana(i)  = beneficio maximo usando solo las i primeras areas
     antes(i) = cuantas areas estan a D km o mas por detras del area i  (x_j <= x_i - D)

     gana(0) = 0
     gana(i) = max( gana(i-1),                  no se construye en la i
                    gana(antes(i)) + b_i )      se construye en la i

 Como las posiciones estan ordenadas, antes(i) nunca retrocede: se avanza un puntero.
 Reconstruccion desde i = N: si gana(i) = gana(i-1) no hay restaurante en i; si no, si lo hay
 y se salta a antes(i).

 Coste: O(N) en tiempo y en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

bool resuelveCaso() {
    int n, d;
    cin >> n >> d;
    if (!cin)  // fin de la entrada
        return false;
    vector<int> x(n + 1), b(n + 1);
    for (int i = 1; i <= n; ++i) cin >> x[i];
    for (int i = 1; i <= n; ++i) cin >> b[i];

    vector<int> gana(n + 1, 0), antes(n + 1, 0);
    int j = 0;                                 // areas 1..j compatibles con la actual
    for (int i = 1; i <= n; ++i) {
        while (x[j + 1] <= x[i] - d) ++j;
        antes[i] = j;
        int construir = gana[j] + b[i];
        gana[i] = construir > gana[i - 1] ? construir : gana[i - 1];
    }
    cout << gana[n] << '\n';

    vector<int> elegidas;                      // de atras hacia delante
    for (int i = n; i > 0; ) {
        if (gana[i] == gana[i - 1]) --i;
        else {
            elegidas.push_back(x[i]);
            i = antes[i];
        }
    }
    for (int k = (int)elegidas.size() - 1; k >= 0; --k)
        cout << elegidas[k] << (k > 0 ? " " : "");
    cout << '\n';
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
