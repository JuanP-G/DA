/*
 * Árboles de recubrimiento de coste mínimo (ARM) del tema 6, reunidos en un solo fichero
 * para estudiar y para usar en el juez:
 *
 *   ARM_Kruskal   ordena las aristas y usa ConjuntosDisjuntos para descartar ciclos   O(A log A)
 *   ARM_Prim      crece un árbol desde el vértice 0 con una cola de prioridad          O(A log A)
 *
 * Los dos devuelven el mismo coste (si hay varios ARM, pueden devolver árboles distintos).
 * Si el grafo no es conexo no existe ARM: conexo() es false y no se debe leer el coste.
 * Los usa GrafoValorado_demo.cpp, que los ejecuta sobre el grafo de la herramienta interactiva.
 */

#ifndef GRAFOVALORADO_ALGORITMOS_H_
#define GRAFOVALORADO_ALGORITMOS_H_

#include <algorithm>
#include <queue>
#include <vector>
#include "GrafoValorado.h"
#include "ConjuntosDisjuntos.h"

// ---------------------------------------------------------------------------
template <typename Valor>
class ARM_Kruskal {
public:
   ARM_Kruskal(GrafoValorado<Valor> const& g) : coste(0), V(g.V()) {
      std::vector<Arista<Valor>> aristas = g.aristas();
      std::sort(aristas.begin(), aristas.end());          // por valor creciente
      ConjuntosDisjuntos cjtos(g.V());
      for (auto const& a : aristas) {
         int v = a.uno(), w = a.otro(v);
         if (!cjtos.unidos(v, w)) {                       // no cierra ciclo: se acepta
            cjtos.unir(v, w);
            _ARM.push_back(a);
            coste += a.valor();
            if (_ARM.size() == (size_t)g.V() - 1) break;  // ya hay V - 1 aristas
         }
      }
   }
   bool conexo() const { return V == 0 || _ARM.size() == (size_t)V - 1; }
   Valor costeARM() const { return coste; }
   std::vector<Arista<Valor>> const& ARM() const { return _ARM; }
private:
   std::vector<Arista<Valor>> _ARM;
   Valor coste;
   int V;
};

// ---------------------------------------------------------------------------
template <typename Valor>
class ARM_Prim {
public:
   ARM_Prim(GrafoValorado<Valor> const& g) : visit(g.V(), false), coste(0), V(g.V()) {
      if (V == 0) return;
      visitar(g, 0);                                      // el árbol empieza en el vértice 0
      while (!pq.empty() && _ARM.size() < (size_t)V - 1) {
         auto a = pq.top(); pq.pop();                     // la arista más barata que sale del árbol
         int v = a.uno(), w = a.otro(v);
         if (visit[v] && visit[w]) continue;              // las dos puntas ya están dentro: sobra
         _ARM.push_back(a);
         coste += a.valor();
         if (!visit[v]) visitar(g, v);
         if (!visit[w]) visitar(g, w);
      }
   }
   bool conexo() const { return V == 0 || _ARM.size() == (size_t)V - 1; }
   Valor costeARM() const { return coste; }
   std::vector<Arista<Valor>> const& ARM() const { return _ARM; }
private:
   std::vector<Arista<Valor>> _ARM;
   std::priority_queue<Arista<Valor>, std::vector<Arista<Valor>>, std::greater<Arista<Valor>>> pq;
   std::vector<bool> visit;
   Valor coste;
   int V;

   // mete v en el árbol y las aristas que salen de v en la cola
   void visitar(GrafoValorado<Valor> const& g, int v) {
      visit[v] = true;
      for (auto const& a : g.ady(v))
         if (!visit[a.otro(v)]) pq.push(a);
   }
};

#endif
