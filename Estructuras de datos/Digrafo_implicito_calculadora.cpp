/*
 * Tema 5 · La máquina calculadora: BFS sobre un grafo IMPLÍCITO (transparencias 13).
 * Los vértices son los números 0..9999; los adyacentes de v se calculan al vuelo con
 * las tres operaciones, sin construir ningún Digrafo. Compilar:  g++ -std=c++17 este.cpp
 * Entrada: pares "origen destino". Salida: mínimo de pulsaciones.
 */
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

const int MAX = 10000;
const int INF = 1000000000; // ∞

int adyacente(int v, int i) {
   switch (i) {
      case 0: return (v + 1) % MAX; // + 1
      case 1: return (v * 2) % MAX; // * 2
      case 2: return v / 3;         // / 3
   }
   return v;
}

int bfs(int origen, int destino) {
   if (origen == destino) return 0;
   vector<int> distancia(MAX, INF);
   distancia[origen] = 0;
   queue<int> cola; cola.push(origen);
   while (!cola.empty()) {
      int v = cola.front(); cola.pop();
      for (int i = 0; i < 3; ++i) {
         int w = adyacente(v, i);
         if (distancia[w] == INF) {
            distancia[w] = distancia[v] + 1;
            if (w == destino) return distancia[w];
            else cola.push(w);
         }
      }
   }
   return -1; // no se llega nunca (con +1 siempre se llega)
}

bool resuelveCaso() {
   int origen, destino;
   cin >> origen >> destino;
   if (!cin) return false;
   cout << bfs(origen, destino) << "\n";
   return true;
}

int main() {
   while (resuelveCaso());
   return 0;
}
