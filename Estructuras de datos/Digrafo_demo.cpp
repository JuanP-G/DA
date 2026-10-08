/*
 * Demo del tema 5: ejecuta los algoritmos de Digrafo_algoritmos.h sobre los grafos
 * de las transparencias. Compilar:  g++ -std=c++17 Digrafo_demo.cpp -o demo
 */
#include <iostream>
#include "Digrafo_algoritmos.h"
using namespace std;

// Digrafo de 13 vértices de las transparencias 12 y 15 (aristas en este orden)
Digrafo digrafo13() {
   Digrafo g(13);
   int a[][2] = {{4,2},{2,3},{3,2},{6,0},{0,1},{2,0},{11,12},{12,9},{9,10},{9,11},{7,9},
                 {10,12},{11,4},{4,3},{3,5},{6,8},{8,6},{5,4},{0,5},{6,4},{6,9},{7,6}};
   for (auto& e : a) g.ponArista(e[0], e[1]);
   return g;
}

// DAG de 7 vértices de las transparencias 14
Digrafo dag7() {
   Digrafo g(7);
   int a[][2] = {{0,1},{0,2},{0,5},{6,0},{6,4},{5,2},{3,2},{3,5},{3,4},{3,6},{1,4}};
   for (auto& e : a) g.ponArista(e[0], e[1]);
   return g;
}

void muestra(string const& t, Camino const& c) {
   cout << t;
   for (int x : c) cout << " " << x;
   cout << "\n";
}

int main() {
   Digrafo g = digrafo13();

   DFSDirigido dfs(g, 2);
   cout << "alcanzables desde 2:";
   for (int v = 0; v < g.V(); ++v) if (dfs.alcanzable(v)) cout << " " << v;
   cout << "\n";

   BFSDirigido bfs(g, 7);
   cout << "distancias desde 7:";
   for (int v = 0; v < g.V(); ++v) cout << " " << v << ":" << bfs.distancia(v);
   cout << "\n";
   muestra("camino 7 -> 3:", bfs.camino(3));

   CicloDirigido cd(g);
   cout << "hay ciclo: " << cd.hayCiclo() << "\n";
   muestra("ciclo:", cd.ciclo());

   Digrafo d = dag7();
   OrdenTopologico ot(d);
   muestra("orden topologico del DAG:", ot.orden());
   cout << "hay ciclo en el DAG: " << CicloDirigido(d).hayCiclo() << "\n";

   CFC cfc(g);
   cout << "componentes fuertemente conexas: " << cfc.numComponentes() << "\n";
   for (int v = 0; v < g.V(); ++v) cout << " " << v << "->c" << cfc.componente(v);
   cout << "\n";
   return 0;
}
