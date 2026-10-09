/*
 * Algoritmos básicos sobre grafos NO dirigidos del tema 4, reunidos en un solo
 * fichero para estudiar y para usar en el juez (mismo estilo que Digrafo_algoritmos.h):
 *
 *   CaminosDFS           ¿hay camino de s a v? y uno cualquiera (DFS)         O(V + A)
 *   CaminosBFS           camino más corto (menos aristas) y distancias        O(V + A)
 *   ComponentesConexas   número de componentes, la de cada vértice y su tamaño O(V + A)
 *   Bipartito            ¿se puede colorear con 2 colores? (DFS coloreando)    O(V + A)
 *   CicloGrafo           ¿hay algún ciclo? (vecino visitado que no es el padre) O(V + A)
 *
 *   esArbolLibre(g)      conexo y A = V - 1  (ver EJ 04-1)
 *
 * Los usa Grafo_demo.cpp, que los ejecuta sobre un grafo de ejemplo.
 */

#ifndef GRAFO_ALGORITMOS_H_
#define GRAFO_ALGORITMOS_H_

#include <deque>
#include <queue>
#include <stdexcept>
#include <vector>
#include "Grafo.h"

using Camino = std::deque<int>;

// ---------------------------------------------------------------------------
// Caminos desde s con un DFS: dice a qué vértices se llega y da UN camino
// (no necesariamente el más corto).
class CaminosDFS {
public:
   CaminosDFS(Grafo const& g, int s) : visit(g.V(), false), ant(g.V()), s(s) {
      dfs(g, s);
   }
   bool hayCamino(int v) const { return visit[v]; }
   Camino camino(int v) const {
      if (!hayCamino(v)) throw std::domain_error("No existe camino");
      Camino cam;
      for (int x = v; x != s; x = ant[x])
         cam.push_front(x);
      cam.push_front(s);
      return cam;
   }
private:
   std::vector<bool> visit;   // visit[v] = ¿hay camino de s a v?
   std::vector<int> ant;      // ant[v] = último vértice antes de llegar a v
   int s;
   void dfs(Grafo const& g, int v) {
      visit[v] = true;
      for (int w : g.ady(v)) {
         if (!visit[w]) {
            ant[w] = v;
            dfs(g, w);
         }
      }
   }
};

// ---------------------------------------------------------------------------
// Caminos más cortos desde s con un BFS: dist[v] = número mínimo de aristas.
class CaminosBFS {
public:
   CaminosBFS(Grafo const& g, int s) : visit(g.V(), false), ant(g.V()), dist(g.V()), s(s) {
      bfs(g);
   }
   bool hayCamino(int v) const { return visit[v]; }
   int distancia(int v) const { return dist[v]; }
   Camino camino(int v) const {
      if (!hayCamino(v)) throw std::domain_error("No existe camino");
      Camino cam;
      for (int x = v; x != s; x = ant[x])
         cam.push_front(x);
      cam.push_front(s);
      return cam;
   }
private:
   std::vector<bool> visit;   // visit[v] = ¿hay camino de s a v?
   std::vector<int> ant;      // ant[v] = último vértice antes de llegar a v
   std::vector<int> dist;     // dist[v] = aristas del camino más corto s -> v
   int s;
   void bfs(Grafo const& g) {
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
// Componentes conexas: un DFS desde cada vértice sin visitar (ver EJ 04-2, 04-3, 04-5).
class ComponentesConexas {
public:
   ComponentesConexas(Grafo const& g) : comp(g.V(), -1) {
      for (int v = 0; v < g.V(); ++v) {
         if (comp[v] == -1) {
            tams.push_back(0);
            dfs(g, v, (int)tams.size() - 1);
         }
      }
   }
   int numComponentes() const { return (int)tams.size(); }
   int componente(int v) const { return comp[v]; }          // 0 .. numComponentes()-1
   int tamano(int v) const { return tams[comp[v]]; }        // tamaño de la componente de v
   bool conectados(int v, int w) const { return comp[v] == comp[w]; }
   int maxima() const {                                      // tamaño de la mayor
      int m = 0;
      for (int t : tams) if (t > m) m = t;
      return m;
   }
private:
   std::vector<int> comp;   // comp[v] = número de la componente de v (-1 = sin visitar)
   std::vector<int> tams;   // tams[c] = número de vértices de la componente c
   void dfs(Grafo const& g, int v, int c) {
      comp[v] = c;
      ++tams[c];
      for (int w : g.ady(v))
         if (comp[w] == -1) dfs(g, w, c);
   }
};

// ---------------------------------------------------------------------------
// Bipartito: colorear con un DFS; cada vecino recibe el color contrario.
// Si un vecino ya tiene el MISMO color, no es bipartito (ver EJ 04-7).
class Bipartito {
public:
   Bipartito(Grafo const& g) : color(g.V(), -1), bipar(true) {
      for (int v = 0; v < g.V() && bipar; ++v)
         if (color[v] == -1) dfs(g, v, 0);
   }
   bool esBipartito() const { return bipar; }
   int colorDe(int v) const { return color[v]; }             // 0 ó 1 (si es bipartito)
private:
   std::vector<int> color;  // -1 = sin colorear, 0 / 1 = las dos partes
   bool bipar;
   void dfs(Grafo const& g, int v, int c) {
      color[v] = c;
      for (int w : g.ady(v)) {
         if (!bipar) return;
         if (color[w] == -1) dfs(g, w, 1 - c);
         else if (color[w] == c) bipar = false;               // arista entre dos del mismo color
      }
   }
};

// ---------------------------------------------------------------------------
// EXTRA: ¿tiene ciclos un grafo no dirigido? En un DFS, ver un vecino ya
// visitado que NO es el padre (el vértice desde el que llegamos) cierra un ciclo.
// (Con aristas repetidas entre dos vértices también habría ciclo; aquí se
//  asume grafo simple, como en los ejercicios.)
class CicloGrafo {
public:
   CicloGrafo(Grafo const& g) : visit(g.V(), false), hayciclo(false) {
      for (int v = 0; v < g.V() && !hayciclo; ++v)
         if (!visit[v]) dfs(g, v, -1);
   }
   bool hayCiclo() const { return hayciclo; }
private:
   std::vector<bool> visit;
   bool hayciclo;
   void dfs(Grafo const& g, int v, int padre) {
      visit[v] = true;
      for (int w : g.ady(v)) {
         if (hayciclo) return;
         if (!visit[w]) dfs(g, w, v);
         else if (w != padre) hayciclo = true;
      }
   }
};

// ---------------------------------------------------------------------------
// Árbol libre: conexo y sin ciclos  <=>  conexo y A = V - 1  (ver EJ 04-1).
inline bool esArbolLibre(Grafo const& g) {
   return g.A() == g.V() - 1 && ComponentesConexas(g).numComponentes() == 1;
}

#endif /* GRAFO_ALGORITMOS_H_ */
