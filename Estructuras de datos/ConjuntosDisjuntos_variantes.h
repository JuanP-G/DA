/*
 * Las tres primeras implementaciones de la estructura de partición del tema 6
 * (transparencias de A. Verdejo), antes de llegar a la que se usa en el juez
 * (ConjuntosDisjuntos.h: unión por tamaños + compresión de caminos).
 *
 *   BusquedaRapida     vector id[]: buscar O(1), unir O(N)
 *   UnionRapida        un árbol por conjunto: unir y buscar O(altura), que puede ser N
 *   UnionPorTamanos    árboles que cuelgan el pequeño del grande: altura <= log N
 *
 * Las tres tienen la misma interfaz que ConjuntosDisjuntos (buscar, unir, unidos, num_cjtos)
 * y las usa ConjuntosDisjuntos_demo.cpp para comprobar la autoevaluación 6.1.
 */

#ifndef CONJUNTOSDISJUNTOS_VARIANTES_H_
#define CONJUNTOSDISJUNTOS_VARIANTES_H_

#include <vector>

// ---------------------------------------------------------------------------
class BusquedaRapida {
public:
   BusquedaRapida(int N) : ncjtos(N), id(N) {
      for (int i = 0; i < N; ++i) id[i] = i;
   }
   // identificador del conjunto de a: un solo acceso al vector
   int buscar(int a) const { return id.at(a); }

   // los elementos del conjunto de a pasan a tener el identificador del conjunto de b
   void unir(int a, int b) {
      int ia = buscar(a), ib = buscar(b);
      if (ia == ib) return;
      for (int k = 0; k < (int)id.size(); ++k)
         if (id[k] == ia) id[k] = ib;
      --ncjtos;
   }
   bool unidos(int a, int b) const { return buscar(a) == buscar(b); }
   int num_cjtos() const { return ncjtos; }
   std::vector<int> const& vector_id() const { return id; }
private:
   int ncjtos;
   std::vector<int> id;     // id[a] = identificador del conjunto de a
};

// ---------------------------------------------------------------------------
class UnionRapida {
public:
   UnionRapida(int N) : ncjtos(N), p(N) {
      for (int i = 0; i < N; ++i) p[i] = i;
   }
   // sube por los enlaces al padre hasta la raíz
   int buscar(int a) const {
      while (p.at(a) != a) a = p[a];
      return a;
   }
   // la raíz de a pasa a ser hija de la raíz de b
   void unir(int a, int b) {
      int i = buscar(a), j = buscar(b);
      if (i == j) return;
      p[i] = j;
      --ncjtos;
   }
   bool unidos(int a, int b) const { return buscar(a) == buscar(b); }
   int num_cjtos() const { return ncjtos; }
   std::vector<int> const& vector_p() const { return p; }
private:
   int ncjtos;
   std::vector<int> p;      // p[a] = padre de a (una raíz es su propio padre)
};

// ---------------------------------------------------------------------------
class UnionPorTamanos {
public:
   UnionPorTamanos(int N) : ncjtos(N), p(N), tam(N, 1) {
      for (int i = 0; i < N; ++i) p[i] = i;
   }
   int buscar(int a) const {
      while (p.at(a) != a) a = p[a];
      return a;
   }
   // la raíz del árbol más pequeño cuelga de la del más grande (en empate, la de a de la de b)
   void unir(int a, int b) {
      int i = buscar(a), j = buscar(b);
      if (i == j) return;
      if (tam[i] > tam[j]) { tam[i] += tam[j]; p[j] = i; }
      else                 { tam[j] += tam[i]; p[i] = j; }
      --ncjtos;
   }
   bool unidos(int a, int b) const { return buscar(a) == buscar(b); }
   int cardinal(int a) const { return tam[buscar(a)]; }
   int num_cjtos() const { return ncjtos; }
   std::vector<int> const& vector_p() const { return p; }
   std::vector<int> const& vector_tam() const { return tam; }
private:
   int ncjtos;
   std::vector<int> p;      // enlace al padre
   std::vector<int> tam;    // tam[r] = tamaño del árbol de raíz r (solo vale en las raíces)
};

#endif
