
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

/*@ <answer>

 Aibofobia
 
 Una palabra de 1 a 1.000 letras minusculas. Escribir el minimo numero de letras que hay que
 anadir (en cualquier posicion) para convertirla en un palindromo, y uno de esos palindromos.

 PLANTEAMIENTO (programacion dinamica sobre intervalos)
     faltan(i, j) = minimo de letras a anadir para que s[i..j] sea un palindromo
 
     faltan(i, j) = 0                                        si i >= j
                  = faltan(i + 1, j - 1)                     si s[i] == s[j]
                  = 1 + min(faltan(i + 1, j), faltan(i, j - 1))  si no
 Si los extremos son iguales, se emparejan entre si. Si no, a uno de los dos se le anade una
 copia al otro lado: a s[i] (y queda s[i+1..j]) o a s[j] (y queda s[i..j-1]).
 
 La tabla se rellena por longitudes de intervalo crecientes. Despues se reconstruye el
 palindromo desde (0, n - 1), construyendo a la vez la mitad izquierda y la derecha:
   - s[i] == s[j]: se pone s[i] a la izquierda y s[j] a la derecha, y se pasa a (i+1, j-1);
   - si conviene emparejar s[i]: se pone s[i] en los dos lados y se pasa a (i+1, j);
   - si no, se pone s[j] en los dos lados y se pasa a (i, j-1).
 Si queda una letra en el centro (i == j) va una sola vez.
 
 Coste: O(n^2) en tiempo y en espacio por palabra.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    string s;
    cin >> s;
    int n = s.size();
    vector<vector<int>> faltan(n, vector<int>(n, 0));
    for (int d = 1; d < n; ++d) {              // d = j - i
        for (int i = 0; i + d < n; ++i) {
            int j = i + d;
            if (s[i] == s[j]) faltan[i][j] = (d >= 2) ? faltan[i + 1][j - 1] : 0;
            else faltan[i][j] = 1 + min(faltan[i + 1][j], faltan[i][j - 1]);
        }
    }

    string izq, der;                           // der se construye al reves
    int i = 0, j = n - 1;
    while (i <= j) {
        if (i == j) { izq += s[i]; ++i; }
        else if (s[i] == s[j]) { izq += s[i]; der += s[j]; ++i; --j; }
        else if (faltan[i + 1][j] <= faltan[i][j - 1]) { izq += s[i]; der += s[i]; ++i; }
        else { izq += s[j]; der += s[j]; --j; }
    }
    reverse(der.begin(), der.end());
    cout << faltan[0][n - 1] << ' ' << izq + der << '\n';
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
