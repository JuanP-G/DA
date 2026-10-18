/*
 * Caminos de coste mínimo del tema 7 (transparencias de A. Verdejo), en un solo fichero
 * para estudiar y para usar en el juez:
 *
 *   Dijkstra         con IndexPQ (la cola de prioridad variable del tema 3)   O(A log V)
 *   DijkstraVector   sin cola: se busca el mínimo con un bucle                 O(V^2 + A)
 *
 * Los dos calculan, desde un origen, la distancia mínima a todos los vértices (dist[]) y la
 * última arista de cada camino mínimo (ulti[]). Exigen aristas con valor >= 0.
 * Los usa DigrafoValorado_demo.cpp, que los ejecuta sobre el grafo de las transparencias.
 *
 * Para grafos NO dirigidos basta añadir cada arista en los dos sentidos
 * (ponArista({v, w, c}) y ponArista({w, v, c})).
 */

#ifndef DIGRAFOVALORADO_ALGORITMOS_H_
#define DIGRAFOVALORADO_ALGORITMOS_H_

#include <deque>
#include <limits>
#include <vector>
#include "DigrafoValorado.h"
#include "IndexPQ.h"

template <typename Valor>
using Camino = std::deque<AristaDirigida<Valor>>;

// ---------------------------------------------------------------------------
template <typename Valor>
class Dijkstra {
public:
   Dijkstra(DigrafoValorado<Valor> const& g, int orig)
      : origen(orig), dist(g.V(), INF), ulti(g.V()), pq(g.V()) {
      dist[origen] = 0;
      pq.push(origen, 0);
      while (!pq.empty()) {
         int v = pq.top().elem; pq.pop();      // el más cercano que queda: su dist ya es definitiva
         for (auto a : g.ady(v))
            relajar(a);
      }
   }

   bool hayCamino(int v) const { return dist[v] != INF; }
   Valor distancia(int v) const { return dist[v]; }

   // Camino mínimo origen -> v (vacío si v == origen; se debe comprobar hayCamino(v) antes).
   Camino<Valor> camino(int v) const {
      Camino<Valor> cam;
      // recuperamos el camino retrocediendo desde v con ulti[]
      for (int u = v; u != origen; u = ulti[u].desde())
         cam.push_front(ulti[u]);
      return cam;
   }

private:
   const Valor INF = std::numeric_limits<Valor>::max();
   int origen;
   std::vector<Valor> dist;
   std::vector<AristaDirigida<Valor>> ulti;
   IndexPQ<Valor> pq;

   void relajar(AristaDirigida<Valor> a) {
      int v = a.desde(), w = a.hasta();
      if (dist[w] > dist[v] + a.valor()) {
         dist[w] = dist[v] + a.valor(); ulti[w] = a;
         pq.update(w, dist[w]);                // push si w no estaba en la cola
      }
   }
};

// ---------------------------------------------------------------------------
// Reflexión del campus: Dijkstra con un vector en lugar de la cola de prioridad.
// Cada vez se busca el vértice no tratado de menor dist[] recorriendo el vector (O(V)),
// así que el coste es V * V + A. Mejor que A log V cuando el grafo es denso (A ~ V^2).
template <typename Valor>
class DijkstraVector {
public:
   DijkstraVector(DigrafoValorado<Valor> const& g, int orig)
      : origen(orig), dist(g.V(), INF), ulti(g.V()) {
      std::vector<bool> tratado(g.V(), false);
      dist[origen] = 0;
      for (int paso = 0; paso < g.V(); ++paso) {
         int v = -1;
         for (int u = 0; u < g.V(); ++u)       // mínimo entre los no tratados con dist finita
            if (!tratado[u] && dist[u] != INF && (v == -1 || dist[u] < dist[v])) v = u;
         if (v == -1) break;                   // el resto no es alcanzable
         tratado[v] = true;
         for (auto a : g.ady(v)) {
            int w = a.hasta();
            if (dist[w] > dist[v] + a.valor()) { dist[w] = dist[v] + a.valor(); ulti[w] = a; }
         }
      }
   }

   bool hayCamino(int v) const { return dist[v] != INF; }
   Valor distancia(int v) const { return dist[v]; }
   Camino<Valor> camino(int v) const {
      Camino<Valor> cam;
      for (int u = v; u != origen; u = ulti[u].desde()) cam.push_front(ulti[u]);
      return cam;
   }

private:
   const Valor INF = std::numeric_limits<Valor>::max();
   int origen;
   std::vector<Valor> dist;
   std::vector<AristaDirigida<Valor>> ulti;
};

#endif /* DIGRAFOVALORADO_ALGORITMOS_H_ */
