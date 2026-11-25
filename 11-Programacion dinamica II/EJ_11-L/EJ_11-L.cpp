/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

#include "Matriz.h"

/*@ <answer>

 La fiesta de graduacion

 Dos listas de canciones (hasta 1.000 palabras cada una, con repeticiones posibles). Hay que
 encontrar la lista mas larga que sea subsecuencia de las dos (mismo orden, sin saltar
 canciones de una lista a otra, cada repeticion con su propia aparicion en cada lista).
 Escribirla; si no hay ninguna, una linea vacia.

 PLANTEAMIENTO (programacion dinamica: subsecuencia comun mas larga, LCS)

     larga(i, j) = longitud de la mayor lista comun usando a_1..a_i y b_1..b_j

     larga(i, 0) = larga(0, j) = 0
     larga(i, j) = larga(i - 1, j - 1) + 1                   si a_i = b_j
                 = max(larga(i - 1, j), larga(i, j - 1))     si no

 Respuesta: larga(n, m). Se guarda la tabla entera para reconstruir la lista: desde (n, m),
 si a_i = b_j se coge la cancion y se va a (i - 1, j - 1); si no, se va a donde este el
 maximo, (i - 1, j) o (i, j - 1). Las canciones salen de atras hacia delante, asi que se
 dan la vuelta al final.

 Lectura: cada lista ocupa una linea (puede estar vacia), asi que se lee con getline y se
 trocea con un istringstream.

 Coste: O(n * m) en tiempo y en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

vector<string> leeLista() {
    string linea;
    getline(cin, linea);
    istringstream ss(linea);
    vector<string> v;
    string palabra;
    while (ss >> palabra) v.push_back(palabra);
    return v;
}

void resuelveCaso() {
    static bool primera = true;
    if (primera) {                 // lo que queda de la linea del numero de casos
        string resto;
        getline(cin, resto);
        primera = false;
    }
    vector<string> a = leeLista(), b = leeLista();
    int n = a.size(), m = b.size();

    Matriz<int> larga(n + 1, m + 1, 0);
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j)
            if (a[i - 1] == b[j - 1]) larga[i][j] = larga[i - 1][j - 1] + 1;
            else larga[i][j] = max(larga[i - 1][j], larga[i][j - 1]);

    vector<string> lista;
    for (int i = n, j = m; i > 0 && j > 0; ) {
        if (a[i - 1] == b[j - 1]) { lista.push_back(a[i - 1]); --i; --j; }
        else if (larga[i - 1][j] >= larga[i][j - 1]) --i;
        else --j;
    }
    reverse(lista.begin(), lista.end());

    for (size_t k = 0; k < lista.size(); ++k) cout << (k ? " " : "") << lista[k];
    cout << '\n';
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
