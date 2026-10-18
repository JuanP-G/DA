/*
 * Demo del tema 6: ejecuta Kruskal y Prim sobre el grafo de 6 vértices del vídeo del tema 6
 * (primer ejemplo de la herramienta interactiva). Compilar:  g++ -std=c++17 GrafoValorado_demo.cpp -o demo
 */
#include <iostream>
#include "GrafoValorado_algoritmos.h"
using namespace std;

GrafoValorado<int> grafo6() {
   GrafoValorado<int> g(6);
   int a[][3] = {{4,5,2},{0,2,3},{3,4,4},{1,3,5},{3,5,6},{2,3,7},{0,1,8},{2,4,9},{1,2,10}};
   for (auto& e : a) g.ponArista({e[0], e[1], e[2]});
   return g;
}

template <class A> void muestra(string const& t, A const& arm) {
   cout << t << " coste = " << arm.costeARM() << ", aristas:";
   for (auto const& a : arm.ARM()) cout << " " << a.uno() << "-" << a.otro(a.uno()) << "(" << a.valor() << ")";
   cout << "\n";
}

int main() {
   GrafoValorado<int> g = grafo6();
   muestra("Kruskal:", ARM_Kruskal<int>(g));
   muestra("Prim:   ", ARM_Prim<int>(g));

   GrafoValorado<int> h(4);                     // no conexo: {0,1} y {2,3}
   h.ponArista({0, 1, 3}); h.ponArista({2, 3, 5});
   cout << "grafo no conexo: Kruskal conexo = " << ARM_Kruskal<int>(h).conexo() << ", Prim conexo = " << ARM_Prim<int>(h).conexo() << "\n";
   return 0;
}
