// Demo del tema 7: Dijkstra (con IndexPQ y con vector) sobre el digrafo de las transparencias.
//   g++ -std=c++17 DigrafoValorado_demo.cpp -o demo && ./demo
#include <iostream>
#include "DigrafoValorado_algoritmos.h"
using namespace std;

int main() {
   DigrafoValorado<int> g(8);
   int aristas[][3] = {
      {0,1,5}, {0,7,8}, {0,4,9}, {1,3,15}, {1,2,12}, {1,7,4}, {7,2,7}, {7,5,6},
      {4,7,5}, {4,5,4}, {4,6,20}, {5,2,1}, {5,6,13}, {2,3,3}, {2,6,11}, {3,6,9}
   };
   for (auto& a : aristas) g.ponArista({a[0], a[1], a[2]});

   Dijkstra<int> d(g, 0);
   DijkstraVector<int> dv(g, 0);

   cout << "v  dist  ulti   (Dijkstra con IndexPQ)    dist (con vector)\n";
   for (int v = 0; v < g.V(); ++v) {
      cout << v << "  " << d.distancia(v) << "\t";
      Camino<int> c = d.camino(v);
      if (c.empty()) cout << "-";
      else cout << c.back().desde() << "->" << c.back().hasta();
      cout << "\t\t\t\t" << dv.distancia(v) << "\n";
   }
   cout << "\nCamino 0 -> 6:";
   for (auto a : d.camino(6)) cout << "  " << a;
   cout << "\n";
}
