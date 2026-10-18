// =====================================================================
// Acepta el Reto #646 - Camiones de reparto
// https://aceptaelreto.com/problem/statement.php?id=646
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 6-Conjuntos disjuntos y grafos valorados/EJ_06-2/EJ_06-2.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
// =====================================================================

#include <iostream>
#include <vector>
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

using namespace std;

/*
    Camiones de reparto

    V intersecciones (2 <= V <= 10.000) y E calles de doble sentido (0 <= E <= 100.000),
    cada una con la anchura MAXIMA que puede tener un camion para pasar por ella.
    K <= 10 consultas (origen, destino, anchura del camion): SI/NO segun pueda ir.
*/

/*
    PLANTEAMIENTO
    Grafo valorado NO dirigido: intersecciones = vertices, calles = aristas,
    anchura maxima = valor de la arista.

    Cada consulta es una pregunta de alcanzabilidad CON FILTRO:
        hay un camino origen --> destino que use solo aristas con valor >= anchura?

    Un recorrido (DFS) desde el origen que IGNORA las aristas demasiado estrechas lo
    responde. La comparacion es >= : un camion de anchura 15 cabe justo por una calle
    de anchura maxima 15 (el fragmento de las transparencias usa <, que es otra cosa).

    Se repite para cada consulta (el filtro cambia con la anchura), con un vector
    de visitados nuevo cada vez.

    Coste: O(K * (V + E)). La recursion baja como mucho V = 10.000 niveles.
*/

class Alcanzables {
public:
    // vertices alcanzables desde origen usando solo aristas con valor >= ancho
    Alcanzables(GrafoValorado<int> const& g, int origen, int ancho)
        : visitado(g.V(), false), ancho(ancho) {
        dfs(g, origen);
    }

    bool alcanzable(int v) const { return visitado[v]; }

private:
    vector<bool> visitado;
    int ancho;

    void dfs(GrafoValorado<int> const& g, int v) {
        visitado[v] = true;
        for (auto a : g.ady(v)) {
            int w = a.otro(v);
            if (a.valor() >= ancho && !visitado[w]) dfs(g, w);
        }
    }
};

void resuelveCaso() {
    GrafoValorado<int> g(cin, 1);   // V, E y E calles; intersecciones numeradas desde 1

    int k; cin >> k;
    while (k--) {
        int origen, destino, ancho;
        cin >> origen >> destino >> ancho;
        Alcanzables a(g, origen - 1, ancho);
        cout << (a.alcanzable(destino - 1) ? "SI" : "NO") << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();

    return 0;
}
