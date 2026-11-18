
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <limits>
using namespace std;

#include "DigrafoValorado.h"  // estructuras de datos de clase
#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 Camino al cole

 Pueblo con N intersecciones (1 <= N <= 100.000) y C calles (0 <= C <= 200.000) con
 longitud 1..10.000. Las calles se pueden recorrer en AMBOS sentidos. Lucas va de la
 interseccion 1 a la N: de cuantas formas distintas puede ir recorriendo la distancia
 minima? (0 si no hay camino; el resultado es < 2^31.)

 PLANTEAMIENTO
 Dijkstra desde la interseccion 1 con un vector mas que cuenta caminos minimos:

     formas[v] = numero de caminos de longitud minima de 1 a v

 Al relajar la arista v -> w con valor c (v ya tiene dist y formas DEFINITIVAS):
   - dist[v] + c <  dist[w]  : hemos encontrado algo mas corto, TODOS los caminos
                               anteriores a w dejan de valer       formas[w] = formas[v]
   - dist[v] + c == dist[w]  : otra manera, igual de buena, de llegar a w
                                                                   formas[w] += formas[v]
   - dist[v] + c >  dist[w]  : no sirve, no se hace nada.

 Por que formas[v] ya es definitivo cuando se saca v de la cola: todos los caminos
 minimos a v llegan por un vecino u con dist[u] < dist[v] (las calles miden >= 1), y
 esos u se sacaron antes y ya sumaron su aportacion.

 - Calles de doble sentido: cada calle se anade en las dos direcciones al DigrafoValorado.
 - N = 1: la casa es el colegio, hay una unica forma (no moverse): formas[0] = 1 al inicio.
 - Sin camino: formas[N-1] se queda en 0.
 - Se usa unsigned long long: el resultado final es < 2^31, pero el numero de caminos de
   OTROS vertices puede ser enorme. Con unsigned el desbordamiento esta definido (modulo
   2^64) y no estropea la respuesta, que sigue siendo exacta porque es pequena.

 Coste: O(C log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, C;
    cin >> N >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, l;
        cin >> u >> v >> l;
        --u; --v;
        g.ponArista({u, v, l});      // calle de doble sentido: las dos aristas dirigidas
        g.ponArista({v, u, l});
    }

    const int INF = numeric_limits<int>::max();
    vector<int> dist(N, INF);
    vector<unsigned long long> formas(N, 0);
    IndexPQ<int> pq(N);

    dist[0] = 0;
    formas[0] = 1;                   // una forma de estar en casa: no moverse
    pq.push(0, 0);
    while (!pq.empty()) {
        int v = pq.top().elem; pq.pop();
        for (auto a : g.ady(v)) {
            int w = a.hasta();
            int d = dist[v] + a.valor();
            if (d < dist[w]) {
                dist[w] = d;
                formas[w] = formas[v];
                pq.update(w, d);
            } else if (d == dist[w]) {
                formas[w] += formas[v];
            }
        }
    }

    cout << formas[N - 1] << '\n';   // 0 si no se llega
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
