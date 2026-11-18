
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <limits>
#include <utility>
#include <functional>
using namespace std;

#include "DigrafoValorado.h"  // estructuras de datos de clase
#include "IndexPQ.h"  // estructuras de datos de clase

/*@ <answer>

 Cual es el mejor camino?

 Ciudad con N intersecciones (2 <= N <= 20.000) y C calles (0 <= C <= 100.000) de
 longitud 1..5.000, de doble sentido. Para cada una de K <= 10 consultas (origen y
 destino distintos) escribir la distancia minima y SI si algun camino de esa distancia
 usa ademas el MENOR NUMERO DE CALLES posible entre los dos puntos (NO si no), o
 SIN CAMINO. Tras cada caso, una linea con ---. La entrada empieza con el numero de casos.

 PLANTEAMIENTO
 Dos cosas distintas desde el origen:

   1. Menor numero de calles posible (sin mirar la longitud): un recorrido en anchura.
         calles[v] = menor numero de calles de origen a v
   2. Distancia minima, y entre los caminos de esa distancia, el de MENOS calles:
      Dijkstra donde la prioridad es una pareja (distancia, calles) comparada en ese orden.
         dist[v]   = distancia minima
         pasos[v]  = menos calles entre los caminos de distancia dist[v]

 Respuesta de la consulta: distancia dist[destino] y SI si pasos[destino] == calles[destino]
 (el mejor camino en distancia tambien es de los de menos calles), NO si pasos > calles.

 - Con la pareja, al sumar una calle (c, 1) el orden lexicografico se conserva, asi que
   Dijkstra sigue siendo correcto.
 - Doble sentido: dos aristas dirigidas por calle.
 - El Dijkstra se para en cuanto el destino esta en la cabeza de la cola: su (distancia, calles)
   ya es definitivo (las calles miden >= 1, asi que nada que salga despues puede mejorarlo).
 - Hasta 10 consultas con origenes distintos: se repiten los dos recorridos por consulta.

 Coste: O(K * C log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

using Par = pair<int, int>;                   // (distancia, calles)

void resuelveCaso() {
    int N, C;
    cin >> N >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, d;
        cin >> u >> v >> d;
        --u; --v;
        g.ponArista({u, v, d});
        g.ponArista({v, u, d});
    }

    const int INF = numeric_limits<int>::max();
    int K; cin >> K;
    while (K--) {
        int origen, destino;
        cin >> origen >> destino;
        --origen; --destino;

        // Dijkstra con prioridad (distancia, calles)
        vector<Par> mejor(N, {INF, INF});
        IndexPQ<Par> pq(N);
        mejor[origen] = {0, 0};
        pq.push(origen, mejor[origen]);
        while (!pq.empty() && pq.top().elem != destino) {
            int v = pq.top().elem; pq.pop();
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                Par nuevo = {mejor[v].first + a.valor(), mejor[v].second + 1};
                if (nuevo < mejor[w]) {
                    mejor[w] = nuevo;
                    pq.update(w, nuevo);
                }
            }
        }

        if (mejor[destino].first == INF) {
            cout << "SIN CAMINO\n";
        }else{
            // Anchura: menor numero de calles posible, sin mirar la longitud
            vector<int> calles(N, -1);
            queue<int> cola;
            calles[origen] = 0;
            cola.push(origen);
            while (!cola.empty() && calles[destino] == -1) {
                int v = cola.front(); cola.pop();
                for (auto a : g.ady(v)) {
                    int w = a.hasta();
                    if (calles[w] == -1) { calles[w] = calles[v] + 1; cola.push(w); }
                }
            }

            cout << mejor[destino].first << (mejor[destino].second == calles[destino] ? " SI\n" : " NO\n");
        }
    }
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
