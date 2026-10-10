/*
 * Demo del tema 4: ejecuta los algoritmos de Grafo_algoritmos.h sobre un grafo
 * de ejemplo. Compilar:  g++ -std=c++17 Grafo_demo.cpp -o demo
 */
#include <iostream>
#include "Grafo_algoritmos.h"
using namespace std;

// Grafo de 13 vértices y 3 componentes:  {0..6}, {7, 8}, {9..12}
Grafo grafo13() {
   Grafo g(13);
   int a[][2] = {{0,5},{4,3},{0,1},{9,12},{6,4},{5,4},{0,2},{11,12},{9,10},{0,6},{7,8},{9,11},{5,3}};
   for (auto& e : a) g.ponArista(e[0], e[1]);
   return g;
}

void muestra(string const& t, Camino const& c) {
   cout << t;
   for (int x : c) cout << " " << x;
   cout << "\n";
}

int main() {
   Grafo g = grafo13();

   CaminosDFS dfs(g, 0);
   muestra("un camino 0 -> 3 (DFS):", dfs.camino(3));
   cout << "se llega de 0 a 9: " << dfs.hayCamino(9) << "\n";

   CaminosBFS bfs(g, 0);
   muestra("camino mas corto 0 -> 3 (BFS):", bfs.camino(3));
   cout << "distancias desde 0:";
   for (int v = 0; v <= 6; ++v) cout << " " << v << ":" << bfs.distancia(v);
   cout << "\n";

   ComponentesConexas cc(g);
   cout << "componentes: " << cc.numComponentes() << ", la mayor tiene " << cc.maxima() << " vertices\n";
   cout << "tamano de la componente de 8: " << cc.tamano(8) << "\n";

   cout << "bipartito: " << Bipartito(g).esBipartito() << "\n";     // 9-11-12 es un triangulo
   cout << "hay ciclo: " << CicloGrafo(g).hayCiclo() << "\n";

   Grafo arbol(4);                                                   // 0-1, 1-2, 1-3
   arbol.ponArista(0, 1); arbol.ponArista(1, 2); arbol.ponArista(1, 3);
   cout << "el de 4 vertices es arbol libre: " << esArbolLibre(arbol)
        << ", bipartito: " << Bipartito(arbol).esBipartito()
        << ", ciclo: " << CicloGrafo(arbol).hayCiclo() << "\n";
   cout << "el de 13 vertices es arbol libre: " << esArbolLibre(g) << "\n";
   return 0;
}
