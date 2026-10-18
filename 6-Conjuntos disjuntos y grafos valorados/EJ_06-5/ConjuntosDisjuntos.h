/*
 * Implementación de estructuras de partición (o conjuntos disjuntos)
 * con unión por tamaño y compresión de caminos
 * Copyright (c) 2020  Alberto Verdejo
 * Modificado por 2023 Ignacio Fábregas
 */

#ifndef CONJUNTOSDISJUNTOS_H_
#define CONJUNTOSDISJUNTOS_H_

#include <vector>
#include <unordered_map>
#include <iostream>

class ConjuntosDisjuntos {
protected:
   int ncjtos;  // número de conjuntos disjuntos
   mutable std::vector<int> p;  // enlace al padre. El atributo es mutable incluso en métodos constantes
   std::vector<int> tam;  // tamaño de los árboles
public:
   
   // crea una estructura de partición con los elementos 0..N-1,
   // cada uno en un conjunto, partición unitaria
   ConjuntosDisjuntos(int N) : ncjtos(N), p(N), tam(N,1) {
      for (int i = 0; i < N; ++i)
          p[i] = i;
   }
   
   //  devuelve el representante del conjunto que contiene a a
   int buscar(int a) const {
      if (p.at(a) == a) // es una raíz
         return a;
      else
         return p[a] = buscar(p[a]);
   }
   
   // unir los conjuntos que contengan a y b
   void unir(int a, int b) {
      int i = buscar(a);
      int j = buscar(b);
      if (i == j) return;
      if (tam[i] > tam[j]) { // i es la raíz del árbol más grande
         tam[i] += tam[j]; p[j] = i;
      } else {
         tam[j] += tam[i]; p[i] = j;
      }
      --ncjtos;
   }

   // devuelve si a y b están en el mismo conjunto
   bool unidos(int a, int b) const {
      return buscar(a) == buscar(b);
   }
   
   // devuelve el número de elementos en el conjunto de a
   int cardinal(int a) const {
      return tam[buscar(a)];
   }
   
   // devuelve el número de conjuntos disjuntos
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
              aux[r].push_back(i);  //añadimos la x a su grupo
       }
   }

};

#endif