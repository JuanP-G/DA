
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

#include "EnterosInf.h"

/*@ <answer>

 La cuerda de la cometa
 
 N cordeles (1..1.000), cada uno con su longitud y su coste (1..1.000), y una longitud L
 (1..1.000). Cada cordel se usa como mucho una vez y el orden no importa. Si se puede formar
 exactamente L, escribir SI, el numero de formas, el minimo numero de cordeles y el minimo
 coste (cada pregunta por separado). Si no, NO.

 PLANTEAMIENTO (programacion dinamica: mochila 0/1 con suma exacta)
 Tres tablas sobre las longitudes j = 0..L, considerando los cordeles uno a uno:
     formas[j]  = numero de subconjuntos de los cordeles vistos que suman j
     cordeles[j]= minimo numero de cordeles para sumar j      (Infinito si no se puede)
     coste[j]   = minimo coste para sumar j                   (Infinito si no se puede)
 Las dos ultimas son EntInf (EnterosInf.h): con el infinito la suma "inf + 1" sigue siendo
 infinito, asi que no hace falta comprobar nada antes de sumar.
 Casos base: formas[0] = 1, cordeles[0] = coste[0] = 0.
 
 Al anadir el cordel (l, c), para j de L hacia abajo hasta l:
     formas[j]   += formas[j - l]
     cordeles[j]  = min(cordeles[j], cordeles[j - l] + 1)
     coste[j]     = min(coste[j],    coste[j - l] + c)
 Se recorre j DE MAYOR A MENOR para que cada cordel se use como mucho una vez (j - l todavia
 tiene el valor de antes de anadir este cordel).
 
 El enunciado garantiza que ninguna longitud se consigue de mas de 10^18 formas: long long.
 
 Coste: O(N * L) en tiempo y O(L) en espacio por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int N, L;
    cin >> N >> L;
    vector<long long> formas(L + 1, 0);
    vector<EntInf> cordeles(L + 1, Infinito), coste(L + 1, Infinito);
    formas[0] = 1; cordeles[0] = 0; coste[0] = 0;

    for (int k = 0; k < N; ++k) {
        int l, c;
        cin >> l >> c;
        for (int j = L; j >= l; --j) {
            formas[j] += formas[j - l];
            cordeles[j] = min(cordeles[j], cordeles[j - l] + 1);
            coste[j] = min(coste[j], coste[j - l] + c);
        }
    }

    if (formas[L] == 0) cout << "NO\n";
    else cout << "SI " << formas[L] << ' ' << cordeles[L] << ' ' << coste[L] << '\n';
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
