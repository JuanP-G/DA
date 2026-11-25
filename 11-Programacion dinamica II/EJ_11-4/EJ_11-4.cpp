/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

#include "EnterosInf.h"
#include "Matriz.h"

/*@ <answer>

 Seis grados de separacion

 Una red de P personas (1..500) y R relaciones (0..10.000) entre pares de nombres. El grado
 de separacion de dos personas es el minimo numero de relaciones que las unen; el de la red,
 el maximo de todos los pares. Si algun par no esta conectado, se escribe DESCONECTADA.

 PLANTEAMIENTO (programacion dinamica: algoritmo de Floyd-Warshall)

     dist(k, i, j) = minimo de relaciones entre i y j pasando como intermedias solo por
                     las personas 1..k

     dist(0, i, j) = 1          si i y j se conocen
                   = 0          si i = j
                   = infinito   si no
     dist(k, i, j) = min(dist(k - 1, i, j), dist(k - 1, i, k) + dist(k - 1, k, j))

 Como dist(k, ., .) solo necesita dist(k - 1, ., .), se usa UNA matriz que se va mejorando
 con k = 1..P (el paso k no cambia ni la fila ni la columna k).

 Respuesta: el maximo de la matriz final; si hay algun infinito (alguien sin relaciones, o
 dos grupos sin camino entre ellos), DESCONECTADA. Con P = 1 no hay pares y el grado es 0.

 La matriz es una Matriz<EntInf> (Matriz.h y EnterosInf.h): inf + 1 sigue siendo infinito.

 Los nombres se pasan a numeros 0..P-1 con un unordered_map segun van apareciendo.

 Coste: O(P^3) en tiempo y O(P^2) en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int P, R;
    cin >> P >> R;
    Matriz<EntInf> dist(P, P, Infinito);
    for (int i = 0; i < P; ++i) dist[i][i] = 0;

    unordered_map<string, int> numero;
    auto id = [&](const string& nombre) {
        auto it = numero.find(nombre);
        if (it != numero.end()) return it->second;
        int nuevo = numero.size();
        numero[nombre] = nuevo;
        return nuevo;
    };
    for (int r = 0; r < R; ++r) {
        string a, b;
        cin >> a >> b;
        int x = id(a), y = id(b);
        dist[x][y] = dist[y][x] = 1;
    }

    // quien no sale en ninguna relacion se queda con distancia infinita a todos los demas

    for (int k = 0; k < P; ++k)
        for (int i = 0; i < P; ++i) {
            EntInf dik = dist[i][k];
            if (dik == Infinito) continue;
            for (int j = 0; j < P; ++j)
                if (dik + dist[k][j] < dist[i][j]) dist[i][j] = dik + dist[k][j];
        }

    EntInf grado = 0;
    for (int i = 0; i < P; ++i)
        for (int j = 0; j < P; ++j)
            if (dist[i][j] > grado) grado = dist[i][j];

    if (grado == Infinito) cout << "DESCONECTADA\n";
    else cout << grado << '\n';
}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   int numCasos;
   std::cin >> numCasos;
   for (int i = 0; i < numCasos; ++i)
      resuelveCaso();

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
