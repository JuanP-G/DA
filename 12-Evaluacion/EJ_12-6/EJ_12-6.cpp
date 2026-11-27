/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

/*@ <answer>

 Alineamiento de secuencias

 Dos cadenas de bases A, C, G, T (hasta 1.000) y una matriz de sustitucion 5x5 (orden A C G T -).
 Puntuacion maxima de un alineamiento: cada columna empareja base-base, base-hueco o hueco-base.

 PLANTEAMIENTO (programacion dinamica sobre dos prefijos)

     mejor(i, j) = puntuacion maxima alineando los i primeros de a con los j primeros de b

     mejor(0, 0) = 0
     mejor(i, 0) = mejor(i-1, 0) + S[a_i][-]
     mejor(0, j) = mejor(0, j-1) + S[-][b_j]
     mejor(i, j) = max( mejor(i-1, j-1) + S[a_i][b_j],      ultima columna: a_i con b_j
                        mejor(i-1, j)   + S[a_i][-],        ultima columna: a_i con hueco
                        mejor(i, j-1)   + S[-][b_j] )       ultima columna: hueco con b_j

 Solo se necesita la fila anterior: se guarda una fila y la diagonal en una variable.
 Cabe en int: como mucho 2.000 columnas de 50.000 = 10^8.

 Coste: O(n * m) en tiempo y O(m) en espacio por par.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

const int HUECO = 4;

int indice(char c) {
    switch (c) {
    case 'A': return 0;
    case 'C': return 1;
    case 'G': return 2;
    default: return 3;   // 'T'
    }
}

void resuelvePar(const int S[5][5]) {
    string a, b;
    cin >> a >> b;
    int n = a.size(), m = b.size();

    vector<int> mejor(m + 1, 0);
    for (int j = 1; j <= m; ++j)
        mejor[j] = mejor[j - 1] + S[HUECO][indice(b[j - 1])];

    for (int i = 1; i <= n; ++i) {
        int x = indice(a[i - 1]);
        int diagonal = mejor[0];             // mejor(i-1, 0)
        mejor[0] += S[x][HUECO];
        for (int j = 1; j <= m; ++j) {
            int y = indice(b[j - 1]);
            int arriba = mejor[j];           // mejor(i-1, j)
            mejor[j] = max({ diagonal + S[x][y], arriba + S[x][HUECO], mejor[j - 1] + S[HUECO][y] });
            diagonal = arriba;
        }
    }
    cout << mejor[m] << '\n';
}

void resuelveCaso() {
    int S[5][5];
    for (int f = 0; f < 5; ++f)
        for (int c = 0; c < 5; ++c) cin >> S[f][c];
    int pares;
    cin >> pares;
    for (int p = 0; p < pares; ++p)
        resuelvePar(S);
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
