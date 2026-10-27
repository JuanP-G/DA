// =====================================================================
// Acepta el Reto #504 - Cual es el mejor camino?
// https://aceptaelreto.com/problem/statement.php?id=504
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 7-Digrafos valorados y caminos minimos/EJ_07-5/EJ_07-5.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
//  - el separador de cada caso es `----` (cuatro guiones)
// =====================================================================

#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <utility>
#include <functional>
// ---------- DigrafoValorado.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/*
 * Implementacion de grafos dirigidos valorados
 * Copyright (c) 2020  Alberto Verdejo
 * Modificado por 2023 Ignacio Fabregas
 */

#ifndef DIGRAFOVALORADO_H_
#define DIGRAFOVALORADO_H_

#include <iostream>
#include <memory>
#include <stdexcept>
#include <vector>

template <typename Valor>
class AristaDirigida {
public:
   AristaDirigida(): pimpl(nullptr) {}

   AristaDirigida(int v, int w, Valor valor): pimpl(std::make_shared<AristaDirigida_impl>(v, w, valor)) {}

   int desde() const { return pimpl->v; }

   int hasta() const { return pimpl->w; }

   Valor valor() const { return pimpl->valor; }

   void print(std::ostream & o = std::cout) const {
      o << "(" << pimpl->v << ", " << pimpl->w << ", " << pimpl->valor << ")";
   }

   bool operator<(AristaDirigida<Valor> const& b) const {
      return valor() < b.valor();
   }

   bool operator>(AristaDirigida<Valor> const& b) const {
      return b.valor() < valor();
   }

private:
   struct AristaDirigida_impl {
      int v, w;
      Valor valor;
      AristaDirigida_impl(int v, int w, Valor valor) : v(v), w(w), valor(valor) {}
   };
   std::shared_ptr<AristaDirigida_impl> pimpl;
};

template <typename Valor>
inline std::ostream& operator<<(std::ostream & o, AristaDirigida<Valor> const& ar){
   ar.print(o);
   return o;
}

template <typename Valor>
using AdysDirVal = std::vector<AristaDirigida<Valor>>;  // lista de adyacentes a  un vertice

template <typename Valor>
class DigrafoValorado {
public:

    /** Crea un grafo dirigido y valorado con V vertices */
   DigrafoValorado(int v) : _V(v), _A(0), _ady(_V) {}
   
   /**
    * Crea un grafo dirigido y valorado a partir de los datos en el flujo de entrada (si puede).
    * primer es el indice del primer vertice del grafo en el entrada.
    */
   DigrafoValorado(std::istream & flujo, int primer = 0) : _A(0) {
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
    * Anade la arista dirigida v-w al grafo.
    * @throws invalid_argument si algun vertice no existe
    */
   void ponArista(AristaDirigida<Valor> arista) {
      int v = arista.desde(), w = arista.hasta();
      if (v < 0 || v >= _V || w < 0 || w >= _V)
         throw std::invalid_argument("Vertice inexistente");
      ++_A;
      _ady[v].push_back(arista);
   }
   
   /** Comprueba si hay arista de v a w. */
   bool hayArista(int v, int w) const {
      for (auto a : _ady[v])
         if (a.hasta() == w) return true;
      return false;
   }
   
   /**
    * Devuelve la lista de adyacencia de v.
    * @throws invalid_argument si v no existe
    */
   AdysDirVal<Valor> const& ady(int v) const {
      if (v < 0 || v >= _V)
         throw std::invalid_argument("Vertice inexistente");
      return _ady[v];
   }
   
   /** Devuelve el grafo dirigido inverso. */
   DigrafoValorado<Valor> inverso() const {
      DigrafoValorado<Valor> inv(_V);
      for (auto v = 0; v < _V; ++v) {
         for (auto a : _ady[v]) {
            inv.ponArista({a.hasta(), a.desde(), a.valor()});
         }
      }
      return inv;
   }
   
   /** Muestra el grafo en el stream de salida o */
   void print(std::ostream& o = std::cout) const {
      o << _V << " vArtices, " << _A << " aristas\n";
      for (auto v = 0; v < _V; ++v) {
         o << v << ": ";
         for (auto a : _ady[v]) {
            o << a << " ";
         }
         o << "\n";
      }
   }
   
private:
   int _V;   //numero de vertices
   int _A;   //numero de aristas
   std::vector<AdysDirVal<Valor>> _ady;   // vector de listas de adyacentes
   
};

/** Para mostrar grafos por la salida estandar. */
template <typename Valor>
inline std::ostream& operator<<(std::ostream& o,const DigrafoValorado<Valor>& g){
   g.print(o);
   return o;
}


#endif /*  DIGRAFOVALORADO_H_ */
// ---------- fin de DigrafoValorado.h ----------
// ---------- IndexPQ.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/**
 * Implementacion de colas con prioridad mediante monticulos.
 * Los elementos son enteros de 0 a N-1 que tienen asociada una prioridad
 * dentro de la cola. La prioridad de un elemento puede ser modificada
 * con coste en O(log N).
 *
 * Copyright (c) 2020 Alberto Verdejo
 * Modificado por 2023 Ignacio Fabregas
 */

#ifndef INDEXPQ_H_
#define INDEXPQ_H_

#include <iostream>
#include <stdexcept>
#include <vector>


// T es el tipo de las prioridades
// Comparator dice cuando un valor de tipo T es mas prioritario que otro
template <typename T = int, typename Comparator = std::less<T>>
class IndexPQ {

public:
   // Registro para las parejas < elem, prioridad >
   struct Par {
      int elem;
      T prioridad;
   };
   
private:
   // vector que contiene los datos (pares < elem, prioridad >)
   std::vector<Par> array;      // El primer elemento esta en la posicion 1
   
   // vector que contiene las posiciones en array de los elementos
   std::vector<int> posiciones;   // un 0 indica que el elemento no esta

    /* Objeto funcion que sabe comparar elementos.
     * antes(a,b) es cierto si a es mas prioritario que b (a debe salir antes que b)
     */
   Comparator antes;
   
public:
   IndexPQ(int N, Comparator c = Comparator()) : array(1), posiciones(N, 0), antes(c) {}
   
   IndexPQ(IndexPQ<T,Comparator> const&) = default;
   
   IndexPQ<T,Comparator>& operator=(IndexPQ<T,Comparator> const&) = default;
   
   ~IndexPQ() = default;
   
   // e debe ser uno de los posibles elementos
   void push(int e, T const& p) {
      if (posiciones.at(e) != 0)
         throw std::invalid_argument("No se pueden insertar elementos repetidos.");
      else {
         array.push_back({e, p});
         posiciones[e] = size();
         flotar(size());
      }
   }

   // Actualizar la prioridad del elemento e
   void update(int e, T const& p) {
      int i = posiciones.at(e);
      if (i == 0) // el elemento e se inserta por primera vez
         push(e, p);
      else {
         array[i].prioridad = p;
         if (i != 1 && antes(array[i].prioridad, array[i/2].prioridad))
            flotar(i);
         else // puede hacer falta hundir a e
            hundir(i);
      }
   }
   
   int size() const {
      return int(array.size()) - 1;
   }
   
   bool empty() const {
      return size() == 0;
   }
   
   Par const& top() const {
      if (size() == 0)
         throw std::domain_error("No se puede consultar el primero de una cola vacia");
      else return array[1];
   }

    T const& priority(int e) const {
     if (posiciones.at(e) == 0)
         throw std::invalid_argument("No se puede consultar la prioridad de un elemento que no existe");
      else
         return array[posiciones[e]].prioridad;
   }
   
   void pop() {
      if (size() == 0) throw std::domain_error("No se puede eliminar el primero de una cola vacia.");
      else {
         posiciones[array[1].elem] = 0; // para indicar que no esta
         if (size() > 1) {
            array[1] = std::move(array.back());
            posiciones[array[1].elem] = 1;
            array.pop_back();
            hundir(1);
         } else
            array.pop_back();
      }
   }

    /* Escritura del monticulo. Metodo para depurar */
    void print(){
        std::cout << "[";
        for(int i = 1; i < array.size()-1; i++)
            std::cout << array[i] << ", ";
        std::cout << array[ array.size()-1] << "]" << std::endl;
    }

private:
   
   void flotar(int i) {
      Par parmov = std::move(array[i]);
      int hueco = i;
      while (hueco != 1 && antes(parmov.prioridad, array[hueco/2].prioridad)) {
         array[hueco] = std::move(array[hueco/2]); posiciones[array[hueco].elem] = hueco;
         hueco /= 2;
      }
      array[hueco] = std::move(parmov); posiciones[array[hueco].elem] = hueco;
   }
   
   void hundir(int i) {
      Par parmov = std::move(array[i]);
      int hueco = i;
      int hijo = 2*hueco; // hijo izquierdo, si existe
      while (hijo <= size())  {
         // cambiar al hijo derecho de i si existe y va antes que el izquierdo
         if (hijo < size() && antes(array[hijo + 1].prioridad, array[hijo].prioridad))
            ++hijo;
         // flotar el hijo si va antes que el elemento hundiendose
         if (antes(array[hijo].prioridad, parmov.prioridad)) {
            array[hueco] = std::move(array[hijo]); posiciones[array[hueco].elem] = hueco;
            hueco = hijo; hijo = 2*hueco;
         }
         else break;
      }
      array[hueco] = std::move(parmov); posiciones[array[hueco].elem] = hueco;
   }
   
};

#endif /* INDEXPQ_H_ */
// ---------- fin de IndexPQ.h ----------

using namespace std;

/*
    Cual es el mejor camino?

    Ciudad con N intersecciones (2 <= N <= 20.000) y C calles (0 <= C <= 100.000) de
    longitud 1..5.000, de doble sentido. Para cada una de K <= 10 consultas (origen y
    destino distintos) escribir la distancia minima y SI si algun camino de esa distancia
    usa ademas el MENOR NUMERO DE CALLES posible entre los dos puntos (NO si no), o
    SIN CAMINO. Tras cada caso, una linea con ---. La entrada empieza con el numero de casos.
*/

/*
    PLANTEAMIENTO
    Dos cosas distintas desde el origen:

      1. Menor numero de calles posible (sin mirar la longitud): un recorrido en anchura.
            calles[v] = menor numero de calles de origen a v
      2. Distancia minima, y entre los caminos de esa distancia, el de MENOS calles:
         Dijkstra donde la prioridad es una pareja (distancia, calles) comparada en ese orden.
            dist[v]   = distancia minima
            pasos[v]  = menos calles entre los caminos de distancia dist[v]

    Respuesta de la consulta: distancia dist[destino] y SI si pasos[destino] == calles[destino]
    (el mejor camino en distancia tambien es de los de menos calles), NO si pasos > calles.

    - Con la pareja, al sumar una calle (c, 1) el orden lexicografico se conserva, asi que
      Dijkstra sigue siendo correcto.
    - Doble sentido: dos aristas dirigidas por calle.
    - El Dijkstra se para en cuanto el destino esta en la cabeza de la cola: su (distancia, calles)
      ya es definitivo (las calles miden >= 1, asi que nada que salga despues puede mejorarlo).
    - Hasta 10 consultas con origenes distintos: se repiten los dos recorridos por consulta.

    Coste: O(K * C log N) por caso.
*/

using Par = pair<int, int>;                   // (distancia, calles)

void resuelveCaso() {
    int N, C;
    cin >> N >> C;
    DigrafoValorado<int> g(N);
    for (int i = 0; i < C; ++i) {
        int u, v, d;
        cin >> u >> v >> d;
        --u; --v;
        g.ponArista({u, v, d});
        g.ponArista({v, u, d});
    }

    const int INF = numeric_limits<int>::max();
    int K; cin >> K;
    while (K--) {
        int origen, destino;
        cin >> origen >> destino;
        --origen; --destino;

        // Dijkstra con prioridad (distancia, calles)
        vector<Par> mejor(N, {INF, INF});
        IndexPQ<Par> pq(N);
        mejor[origen] = {0, 0};
        pq.push(origen, mejor[origen]);
        while (!pq.empty() && pq.top().elem != destino) {
            int v = pq.top().elem; pq.pop();
            for (auto a : g.ady(v)) {
                int w = a.hasta();
                Par nuevo = {mejor[v].first + a.valor(), mejor[v].second + 1};
                if (nuevo < mejor[w]) {
                    mejor[w] = nuevo;
                    pq.update(w, nuevo);
                }
            }
        }

        if (mejor[destino].first == INF) {
            cout << "SIN CAMINO\n";
        }else{
            // Anchura: menor numero de calles posible, sin mirar la longitud
            vector<int> calles(N, -1);
            queue<int> cola;
            calles[origen] = 0;
            cola.push(origen);
            while (!cola.empty() && calles[destino] == -1) {
                int v = cola.front(); cola.pop();
                for (auto a : g.ady(v)) {
                    int w = a.hasta();
                    if (calles[w] == -1) { calles[w] = calles[v] + 1; cola.push(w); }
                }
            }

            cout << mejor[destino].first << (mejor[destino].second == calles[destino] ? " SI\n" : " NO\n");
        }
    }
    cout << "----\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();
    return 0;
}
