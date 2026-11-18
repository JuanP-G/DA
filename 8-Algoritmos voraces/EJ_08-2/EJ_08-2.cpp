
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

 ¡Nos invaden!
 
 N ciudades invadidas (1 <= N <= 300.000) con sus efectivos enemigos y N equipos de defensa
 con sus efectivos. Un equipo por ciudad; la victoria esta garantizada si el equipo tiene al
 menos tantos efectivos como el enemigo. Escribir el maximo numero de victorias garantizadas.

 PLANTEAMIENTO (voraz)
 Se ordenan las ciudades y los equipos de menor a mayor. Para la ciudad mas facil (la de menos
 enemigos) se usa el equipo MAS PEQUENO que la gane: un equipo mas grande se desperdiciaria
 ahi y podria hacer falta en una ciudad mas dificil. Los equipos que no ganan a esa ciudad
 tampoco ganaran a ninguna de las siguientes, asi que se descartan.
 
 Con los dos vectores ordenados basta un recorrido con dos indices:
     si equipo[j] >= enemigo[i]: victoria, se pasa a la siguiente ciudad y al siguiente equipo
     si no: el equipo j no sirve para nada, se pasa al siguiente equipo
 
 Coste: O(N log N) por caso (la ordenacion).

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N;
    cin >> N;
    vector<int> enemigos(N), equipos(N);
    for (int& e : enemigos) cin >> e;
    for (int& d : equipos) cin >> d;
    sort(enemigos.begin(), enemigos.end());
    sort(equipos.begin(), equipos.end());

    int victorias = 0, i = 0;          // i = ciudad mas facil aun sin defender
    for (int j = 0; j < N && i < N; ++j) {
        if (equipos[j] >= enemigos[i]) {
            ++victorias;
            ++i;
        }
    }
    cout << victorias << '\n';
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
