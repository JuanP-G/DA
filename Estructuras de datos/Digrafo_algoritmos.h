/*
 * Algoritmos básicos sobre grafos dirigidos del tema 5 (transparencias de A. Verdejo),
 * reunidos en un solo fichero para estudiar y para usar en el juez:
 *
 *   DFSDirigido      alcanzabilidad                      O(V + A)
 *   BFSDirigido      camino más corto (menos aristas)    O(V + A)
 *   OrdenTopologico  postorden inverso (el grafo debe ser un DAG)
 *   CicloDirigido    detecta un ciclo y lo devuelve
 *   CFC              componentes fuertemente conexas (Kosaraju, usa inverso())   [extra]
 *
 * Los usa Digrafo_demo.cpp, que ejecuta cada uno sobre los grafos de las transparencias.
 */

#ifndef DIGRAFO_ALGORITMOS_H_
#define DIGRAFO_ALGORITMOS_H_

#include <deque>
#include <queue>
#include <stdexcept>
#include <vector>
#include "Digrafo.h"

using Camino = std::deque<int>;

// ---------------------------------------------------------------------------
class DFSDirigido {
public:
   DFSDirigido(Digrafo const& g, int s) : visit(g.V(), false) {
      dfs(g, s);
   }
   bool alcanzable(int v) const {
      return visit[v];
   }
private:
   std::vector<bool> visit; // visit[v] = ¿hay camino dirigido de s a v?
   void dfs(Digrafo const& g, int v) {
      visit[v] = true;
      for (int w : g.ady(v))
         if (!visit[w]) dfs(g, w);
   }
};

// ---------------------------------------------------------------------------
class BFSDirigido {
public:
   BFSDirigido(Digrafo const& g, int s) : visit(g.V(), false),
                                          ant(g.V()), dist(g.V()), s(s) {
      bfs(g);
   }
   bool hayCamino(int v) const {
      return visit[v];
   }
   int distancia(int v) const {
      return dist[v];
   }
   Camino camino(int v) const {
      if (!hayCamino(v)) throw std::domain_error("No existe camino");
      Camino cam;
      for (int x = v; x != s; x = ant[x])
         cam.push_front(x);
      cam.push_front(s);
      return cam;
   }
private:
   std::vector<bool> visit; // visit[v] = ¿hay camino de s a v?
   std::vector<int> ant;    // ant[v]   = último vértice antes de llegar a v
   std::vector<int> dist;   // dist[v]  = aristas en el camino s->v más corto
   int s;
   void bfs(Digrafo const& g) {
      std::queue<int> q;
      dist[s] = 0; visit[s] = true;
      q.push(s);
      while (!q.empty()) {
         int v = q.front(); q.pop();
         for (int w : g.ady(v)) {
            if (!visit[w]) {
               ant[w] = v; dist[w] = dist[v] + 1; visit[w] = true;
               q.push(w);
            }
         }
      }
   }
};

// ---------------------------------------------------------------------------
class OrdenTopologico {
public:
   // g es DAG
   OrdenTopologico(Digrafo const& g) : visit(g.V(), false) {
      for (int v = 0; v < g.V(); ++v)
         if (!visit[v])
            dfs(g, v);
   }
   // devuelve la ordenación topológica
   std::deque<int> const& orden() const {
      return _orden;
   }
private:
   std::vector<bool> visit;
   std::deque<int> _orden; // ordenación topológica
   void dfs(Digrafo const& g, int v) {
      visit[v] = true;
      for (int w : g.ady(v))
         if (!visit[w])
            dfs(g, w);
      _orden.push_front(v);
   }
};

// ---------------------------------------------------------------------------
class CicloDirigido {
public:
   CicloDirigido(Digrafo const& g) : visit(g.V(), false), ant(g.V()),
                                     apilado(g.V(), false), hayciclo(false) {
      for (int v = 0; v < g.V(); ++v)
         if (!visit[v])
            dfs(g, v);
   }
   bool hayCiclo() const { return hayciclo; }
   Camino const& ciclo() const { return _ciclo; }
private:
   std::vector<bool> visit;   // visit[v] = ¿se ha alcanzado a v en el dfs?
   std::vector<int> ant;      // ant[v] = vértice anterior en el camino a v
   std::vector<bool> apilado; // apilado[v] = ¿está el vértice v en la pila?
   Camino _ciclo;             // ciclo dirigido (vacío si no existe)
   bool hayciclo;
   void dfs(Digrafo const& g, int v) {
      apilado[v] = true;
      visit[v] = true;
      for (int w : g.ady(v)) {
         if (hayciclo) // si hemos encontrado un ciclo terminamos
            return;
         if (!visit[w]) { // encontrado un nuevo vértice, seguimos
            ant[w] = v; dfs(g, w);
         } else if (apilado[w]) { // hemos detectado un ciclo
            // se recupera retrocediendo
            hayciclo = true;
            for (int x = v; x != w; x = ant[x])
               _ciclo.push_front(x);
            _ciclo.push_front(w); _ciclo.push_front(v);
         }
      }
      apilado[v] = false;
   }
};

// ---------------------------------------------------------------------------
// EXTRA: componentes fuertemente conexas (algoritmo de Kosaraju)
//   1) postorden inverso de un DFS sobre el grafo INVERSO
//   2) DFS sobre el grafo original siguiendo ese orden: cada árbol es una componente
class CFC {
public:
   CFC(Digrafo const& g) : visit(g.V(), false), _comp(g.V(), -1), _num(0) {
      OrdenTopologico ord(g.inverso());   // aquí solo importa el orden, no que sea DAG
      for (int v : ord.orden()) {
         if (!visit[v]) {
            dfs(g, v);
            ++_num;
         }
      }
   }
   int numComponentes() const { return _num; }
   int componente(int v) const { return _comp[v]; }
   bool fuertementeConectados(int v, int w) const { return _comp[v] == _comp[w]; }
private:
   std::vector<bool> visit;
   std::vector<int> _comp;  // _comp[v] = número de la componente de v
   int _num;
   void dfs(Digrafo const& g, int v) {
      visit[v] = true;
      _comp[v] = _num;
      for (int w : g.ady(v))
         if (!visit[w]) dfs(g, w);
   }
};

#endif /* DIGRAFO_ALGORITMOS_H_ */
