// =====================================================================
// Acepta el Reto #645 - Recorriendo el archipielago en bicicleta
// https://aceptaelreto.com/problem/statement.php?id=645
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 6-Conjuntos disjuntos y grafos valorados/EJ_06-3/EJ_06-3.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
// =====================================================================

#include <iostream>
#include <vector>
#include <algorithm>
// ---------- GrafoValorado.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/*
 * Implementacion de grafos no dirigidos valorados
 * Copyright (c) 2020  Alberto Verdejo
 * Modificado por 2023 Ignacio Fabregas
 */

#ifndef GRAFOVALORADO_H_
#define GRAFOVALORADO_H_

#include <iostream>
#include <memory>
#include <stdexcept>
#include <vector>


template <typename Valor>
class Arista {
public:
   Arista() : pimpl(nullptr) {}
   Arista(int v, int w, Valor valor) : pimpl(std::make_shared<Arista_impl>(v, w, valor)) {}
   
   int uno() const { return pimpl->v; }

   int otro(int u) const { return (u == pimpl->v) ? pimpl->w : pimpl->v; }

   Valor valor() const { return pimpl->valor; }

   //Metodo para depurar
   void print(std::ostream & o = std::cout) const {
      o << "(" << pimpl->v << ", " << pimpl->w << ", " << pimpl->valor << ")";
   }
   
   bool operator<(Arista<Valor> const& b) const {
      return valor() < b.valor();
   }

   bool operator>(Arista<Valor> const& b) const {
      return b.valor() < valor();
   }

private:
   struct Arista_impl {
      int v, w;
      Valor valor;
      Arista_impl(int v, int w, Valor valor) : v(v), w(w), valor(valor) {}
   };
   
   std::shared_ptr<Arista_impl> pimpl; // puntero a la arista "de verdad"
};

template <typename Valor>
inline std::ostream& operator<<(std::ostream & o, Arista<Valor> const& ar) {
   ar.print(o);
   return o;
}

template <typename Valor>
using AdysVal = std::vector<Arista<Valor>>;  // lista de adyacentes a un vertice

template <typename Valor>
class GrafoValorado {
public:
   
   /** Crea un grafo valorado con V vertices, sin aristas. */
   GrafoValorado(int V) : _V(V), _A(0), _ady(_V) { }
   
   /**
    * Crea un grafo valorado a partir de los datos en el flujo de entrada (si puede).
    * primer es el indice del primer vertice del grafo en el entrada.
    */
   GrafoValorado(std::istream & flujo, int primer = 0) : _A(0) {
      flujo >> _V;
      if (!flujo) return;
      _ady.resize(_V);
      int E, v, w;
      Valor c;
      flujo >> E;
      while (E--) {
         flujo >> v >> w >> c;
         ponArista({v - primer, w - primer, c});
      }
   }

   /** Devuelve el numero de vertices del grafo. */
   int V() const { return _V; }
   
   /** Devuelve el numero de aristas del grafo. */
   int A() const { return _A; }
   
   /**
    * Anade una arista al grafo.
    * @throws invalid_argument si algun vertice no existe
    */
   void ponArista(Arista<Valor> arista) {
      int v = arista.uno(), w = arista.otro(v);
      if (v < 0 || v >= _V || w < 0 || w >= _V)
         throw std::invalid_argument("Vertice inexistente");
      ++_A;
      _ady[v].push_back(arista);
      _ady[w].push_back(arista);
   }
   
   /**
    * Devuelve la lista de adyacentes de v.
    * @throws invalid_argument si v no existe
    */
   AdysVal<Valor> const& ady(int v) const {
      if (v < 0 || v >= _V)
         throw std::invalid_argument("Vertice inexistente");
      return _ady[v];
   }
   
   /** Devuelve las aristas del grafo. */
   std::vector<Arista<Valor>> aristas() const {
      std::vector<Arista<Valor>> ars;
      for (int v = 0; v < V(); ++v)
         for (auto arista : ady(v))
            if (v < arista.otro(v))
               ars.push_back(arista);
      return ars;
   }
   
   /**  Muestra el grafo en el stream de salida o */
   void print(std::ostream& o = std::cout) const {
      o << _V << " vertices, " << _A << " aristas\n";
      for (auto v = 0; v < _V; ++v) {
         o << v << ": ";
         for (auto const& w : _ady[v]) {
            o << w << " ";
         }
         o << "\n";
      }
   }
   
private:
   int _V;   //numero de vertices
   int _A;   //numero de aristas
   std::vector<AdysVal<Valor>> _ady;   //vector de listas de adyacentes
};

/** ara mostrar grafos por la salida estandar. */
template <typename Valor>
inline std::ostream& operator<<(std::ostream & o, GrafoValorado<Valor> const& g) {
   g.print(o);
   return o;
}

#endif /* GRAFOVALORADO_H_ */
// ---------- fin de GrafoValorado.h ----------
// ---------- ConjuntosDisjuntos.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/*
 * Implementacion de estructuras de particion (o conjuntos disjuntos)
 * con union por tamano y compresion de caminos
 * Copyright (c) 2020  Alberto Verdejo
 * Modificado por 2023 Ignacio Fabregas
 */

#ifndef CONJUNTOSDISJUNTOS_H_
#define CONJUNTOSDISJUNTOS_H_

#include <vector>
#include <unordered_map>
#include <iostream>

class ConjuntosDisjuntos {
protected:
   int ncjtos;  // numero de conjuntos disjuntos
   mutable std::vector<int> p;  // enlace al padre. El atributo es mutable incluso en metodos constantes
   std::vector<int> tam;  // tamano de los arboles
public:
   
   // crea una estructura de particion con los elementos 0..N-1,
   // cada uno en un conjunto, particion unitaria
   ConjuntosDisjuntos(int N) : ncjtos(N), p(N), tam(N,1) {
      for (int i = 0; i < N; ++i)
          p[i] = i;
   }
   
   //  devuelve el representante del conjunto que contiene a a
   int buscar(int a) const {
      if (p.at(a) == a) // es una raiz
         return a;
      else
         return p[a] = buscar(p[a]);
   }
   
   // unir los conjuntos que contengan a y b
   void unir(int a, int b) {
      int i = buscar(a);
      int j = buscar(b);
      if (i == j) return;
      if (tam[i] > tam[j]) { // i es la raiz del arbol mas grande
         tam[i] += tam[j]; p[j] = i;
      } else {
         tam[j] += tam[i]; p[i] = j;
      }
      --ncjtos;
   }

   // devuelve si a y b estan en el mismo conjunto
   bool unidos(int a, int b) const {
      return buscar(a) == buscar(b);
   }
   
   // devuelve el numero de elementos en el conjunto de a
   int cardinal(int a) const {
      return tam[buscar(a)];
   }
   
   // devuelve el numero de conjuntos disjuntos
   int num_cjtos() const { return ncjtos; }

   // escritura para depurar
   void print(){
       std::unordered_map<int,std::vector<int>> aux;
       clases(aux);
       bool primero = true;
       for(auto& x : aux){
           std::cout << (primero ? "" : ", ");
           primero = false;
           std::cout << "{";
           std::cout << x.first;
           for(auto& y : x.second)
               std::cout << ", " << y;
           std::cout << "}";
       }
       std::cout << "\n";
   }

private:
    // Para mostrar las clases de equivalencia
    // aux es un diccionario con representante -> elementos en su clase
    void clases(std::unordered_map<int,std::vector<int>>& aux){
       for(int i = 0; i < p.size(); ++i){
           int r = buscar(p[i]); // representante
           if(aux.count(r) == 0)
              aux[r] = {};
          if(r != i)
              aux[r].push_back(i);  //anadimos la x a su grupo
       }
   }

};

#endif
// ---------- fin de ConjuntosDisjuntos.h ----------

using namespace std;

/*
    Recorriendo el archipielago en bicicleta

    I islas (1 <= I <= 10.000) y P puentes presupuestados (0 <= P <= 100.000),
    cada uno une dos islas y tiene un coste (1..100.000).
    Elegir puentes para poder ir de cualquier isla a cualquier otra con coste
    total MINIMO. Si no hay puentes suficientes: "No hay puentes suficientes".
*/

/*
    PLANTEAMIENTO
    Arbol de recubrimiento de coste minimo (ARM) de un grafo valorado:
    islas = vertices, puentes = aristas, coste = valor.
    Un ARM conecta todos los vertices con V - 1 aristas y suma minima.

    Algoritmo de KRUSKAL:
      1. Ordenar los puentes por coste creciente.
      2. Particion de las islas: al principio cada una esta sola.
      3. Para cada puente en ese orden:
            si sus dos islas YA estan unidas  --> cerraria un ciclo: se descarta
            si no                             --> se construye: unir y sumar coste.
      4. Si se han elegido I - 1 puentes, la suma es la respuesta;
         si no, el grafo no es conexo --> "No hay puentes suficientes".

    Por que funciona (propiedad del corte): el puente mas barato que cruza de un
    grupo de islas al resto pertenece a algun ARM. Cuando Kruskal llega a un puente
    que une dos conjuntos distintos, es el mas barato que sale de uno de ellos.

    Con I = 1 no hace falta ningun puente: 0.

    Coste: ordenar O(P log P) + particion O(I + P lg* I) --> O(I + P log P).
*/

void resuelveCaso() {
    GrafoValorado<int> g(cin, 1);   // I, P y P puentes; islas numeradas desde 1

    vector<Arista<int>> puentes = g.aristas();
    sort(puentes.begin(), puentes.end());   // por coste creciente (operator< de Arista)

    ConjuntosDisjuntos cd(g.V());
    long long coste = 0;
    int elegidos = 0;
    for (auto const& p : puentes) {
        if (elegidos == g.V() - 1) break;
        int u = p.uno(), v = p.otro(u);
        if (!cd.unidos(u, v)) {
            cd.unir(u, v);
            coste += p.valor();
            ++elegidos;
        }
    }

    if (elegidos == g.V() - 1) cout << coste << '\n';
    else cout << "No hay puentes suficientes\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();

    return 0;
}
