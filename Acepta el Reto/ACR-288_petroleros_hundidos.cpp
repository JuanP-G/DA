// =====================================================================
// Acepta el Reto #288 - Petroleros hundidos
// https://aceptaelreto.com/problem/statement.php?id=288
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 6-Conjuntos disjuntos y grafos valorados/EJ_06-1/EJ_06-1.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero (el mar va como espacio en blanco: la solucion solo mira donde hay `#`)
//  - el mar va como espacios en blanco, asi que cada fila se lee entera con `getline`
//  - las filas llevan espacios: no sirve `cin >> fila`
//  - una fila puede venir recortada
// =====================================================================

#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <algorithm>
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
    Petroleros hundidos

    Rejilla F x C (1 <= F, C <= 1.000), '-' mar y '#' petroleo
    Dos celdas negras son de la misma mancha si se llega de una a otra por celdas
    negras moviendose en 8 direcciones.
    Despues aparecen N (<= 100.000) celdas nuevas de petroleo, una a una.
    Salida: tamano de la mancha mas grande al principio y tras cada celda nueva.
*/

/*
    PLANTEAMIENTO
    Las celdas solo se anaden, nunca se quitan: las manchas solo pueden crecer o
    fundirse, jamas partirse. Eso es exactamente lo que sabe hacer una particion
    de CONJUNTOS DISJUNTOS (solo sabe unir).

        elemento    = celda (i, j)  -->  numero i*C + j
        conjunto    = mancha
        unir(a, b)  = dos celdas negras vecinas (8 direcciones)
        cardinal(a) = tamano de la mancha de a

    anade(i, j): marca la celda como petroleo, la une con sus vecinas que ya sean
    petroleo y compara el tamano de SU mancha con el maximo. Como solo hay uniones,
    la unica mancha que puede haber cambiado es la de la celda nueva y el maximo
    nunca baja: no hace falta recorrer todos los conjuntos.

    La imagen inicial se procesa con la misma operacion: celda negra a celda negra.
    Al llegar a una celda, las vecinas posteriores aun no estan marcadas, pero
    cuando se procesen ellas se uniran con esta: el resultado final es el mismo.

    La rejilla es el grafo: no se construye ninguna lista de adyacencia.

    Coste: O(F*C + N) con la lg* de la particion practicamente constante.
*/

class Manchas {
public:
    Manchas(int filas, int columnas)
        : F(filas), C(columnas), petroleo(filas * columnas, false), cd(filas * columnas), mayor(0) {}

    // marca como petroleo la celda (i, j) (base 0) y actualiza la mancha mas grande
    void anade(int i, int j) {
        int celda = i * C + j;
        petroleo[celda] = true;

        for (int di = -1; di <= 1; ++di)
            for (int dj = -1; dj <= 1; ++dj) {
				//Si es la misma celda, no hace falta unirla consigo misma
                if (di == 0 && dj == 0) continue;
				//Si la celda vecina esta fuera de los limites, no hace falta unirla
                int a = i + di, b = j + dj;
                if (a < 0 || a >= F || b < 0 || b >= C) continue;
				//Si la celda vecina es petroleo, unirla con la celda actual
                if (petroleo[a * C + b]) cd.unir(celda, a * C + b);
            }
        mayor = max(mayor, cd.cardinal(celda));
    }

    int masGrande() const { return mayor; }

private:
    int F, C;
    vector<bool> petroleo;
    ConjuntosDisjuntos cd;
    int mayor;
};

void resuelveCaso() {
    int F, C;
    cin >> F >> C;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    Manchas m(F, C);
    string fila;
    for (int i = 0; i < F; ++i) {
        getline(cin, fila);
        for (int j = 0; j < C && j < (int)fila.size(); ++j)
            if (fila[j] == '#') m.anade(i, j);
    }

    cout << m.masGrande();
    int n; cin >> n;
    while (n--) {
        int f, c; cin >> f >> c;
        m.anade(f - 1, c - 1);
        cout << ' ' << m.masGrande();
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> ws && cin.peek() != EOF) resuelveCaso();

    return 0;
}
