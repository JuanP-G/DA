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

/*@ <answer>

 Cambio exacto

 Un precio P (1..10.000 centimos) y N monedas o billetes (1..100), cada uno de valor
 hasta 10.000, cada uno UNA sola vez. Hay que pagar lo menos posible (al menos P) y,
 entre todas las formas de pagar esa cantidad, usar el menor numero de piezas.
 Escribir la cantidad pagada y las piezas usadas.

 PLANTEAMIENTO (programacion dinamica: mochila 0/1 de suma exacta)

     piezas(i, s) = minimo de piezas, usando solo las i primeras, que suman exactamente s
                    (infinito si no se puede)

     piezas(0, 0) = 0,   piezas(0, s) = infinito si s > 0
     piezas(i, s) = piezas(i - 1, s)                                   si v_i > s
                  = min(piezas(i - 1, s), piezas(i - 1, s - v_i) + 1)  si no

 Respuesta: la MENOR s >= P con piezas(N, s) finito, y ese valor.

 Hasta donde hay que llegar: si una forma de pagar suma S >= P y no es la minima, se le
 puede quitar una pieza y seguir pagando >= P. Por tanto la cantidad minima S cumple que,
 quitando cualquiera de sus piezas, se queda por debajo de P: S - v < P, y como v <= 10.000,
 S < P + 10.000. Basta con calcular las sumas hasta P + maxValor.

 Se guarda una sola fila y se recorre s de mayor a menor, para no usar dos veces la misma
 pieza (la 0/1).

 Coste: O(N * (P + maxValor)) en tiempo y O(P + maxValor) en espacio.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

void resuelveCaso() {
    int precio, n;
    cin >> precio >> n;
    vector<int> valor(n);
    int maximo = 0;
    for (int& v : valor) { cin >> v; maximo = max(maximo, v); }

    const int INF = 1000000000;
    int tope = precio + maximo;
    vector<int> piezas(tope + 1, INF);
    piezas[0] = 0;
    for (int v : valor)
        for (int s = tope; s >= v; --s)
            if (piezas[s - v] != INF) piezas[s] = min(piezas[s], piezas[s - v] + 1);

    int s = precio;
    while (piezas[s] == INF) ++s;
    cout << s << ' ' << piezas[s] << '\n';
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
