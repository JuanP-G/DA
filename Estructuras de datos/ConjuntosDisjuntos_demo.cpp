/*
 * Demo del tema 6: ejecuta la autoevaluación 6.1 (unir 9-0, 3-4, 5-8, 7-2, 2-1, 5-7, 0-3, 4-2 sobre
 * 10 elementos) con las cuatro implementaciones y escribe el vector resultante.
 * Compilar:  g++ -std=c++17 ConjuntosDisjuntos_demo.cpp -o demo
 */
#include <iostream>
#include "ConjuntosDisjuntos_variantes.h"
#include "ConjuntosDisjuntos.h"
using namespace std;

int pares[][2] = {{9,0},{3,4},{5,8},{7,2},{2,1},{5,7},{0,3},{4,2}};

template <class V> void escribe(string const& t, V const& v) {
   cout << t;
   for (int x : v) cout << " " << x;
   cout << "\n";
}

int main() {
   BusquedaRapida qf(10);
   for (auto& e : pares) qf.unir(e[0], e[1]);
   escribe("busqueda rapida   id =", qf.vector_id());
   cout << "  conjuntos: " << qf.num_cjtos() << "\n";

   UnionRapida qu(10);
   for (auto& e : pares) qu.unir(e[0], e[1]);
   escribe("union rapida       p =", qu.vector_p());

   UnionPorTamanos sz(10);
   for (auto& e : pares) sz.unir(e[0], e[1]);
   escribe("por tamanos        p =", sz.vector_p());
   escribe("                 tam =", sz.vector_tam());

   // la de ConjuntosDisjuntos.h (con compresión) no expone p: se comprueba con buscar/cardinal
   ConjuntosDisjuntos cd(10);
   for (auto& e : pares) cd.unir(e[0], e[1]);
   cout << "con compresion: conjuntos = " << cd.num_cjtos() << ", cardinal(0) = " << cd.cardinal(0) << ", buscar(0) = " << cd.buscar(0) << "\n";
   return 0;
}
