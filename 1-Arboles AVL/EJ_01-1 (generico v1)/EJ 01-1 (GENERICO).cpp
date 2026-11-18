
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <algorithm>
#include <climits>
#include <string>
#include <cstdlib>
using namespace std;

/*@ <answer>

 ¿Es un árbol AVL? (versión genérica, primera versión)

 Cada caso es una letra (N = enteros, P = palabras) y un árbol con paréntesis, '.' = vacío.
 Decidir si es AVL. La entrada acaba con el fichero.

 PLANTEAMIENTO
 leerAVL lee el árbol en inorden a la vez que lo comprueba: devuelve si es AVL y deja su altura.
 Para ver que es de búsqueda basta con que los valores salgan en inorden estrictamente
 crecientes: se guarda el anterior y se compara con cada valor nuevo.

 Coste: O(n) por árbol, con n el número de nodos.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

template <typename T>
bool leerAVL(int& altura, T& anterior, bool& hayAnterior);

template <typename T>
bool leerAVL(int& altura, T& anterior, bool& hayAnterior) {
	// '(' o '.'
	char c;
	cin >> c;

	if (c == '.') { // árbol vacío
		altura = 0;
		return true;
	}
	int altIzq, altDer;
	bool izqOK = leerAVL(altIzq, anterior, hayAnterior); // Leer subárbol izquierdo
	
	T valor;
	cin >> valor; // Leer el valor del nodo actual
	bool ordenOK = !hayAnterior || anterior < valor; // Comprobamos el orden
	anterior = valor;
	hayAnterior = true;

	bool derOK = leerAVL(altDer, anterior, hayAnterior); // Leer subárbol derecho
	cin >> c; // Leer el ')'

	altura = max(altIzq, altDer) + 1; // Actualizar altura
	return izqOK && derOK && ordenOK && (abs(altIzq - altDer) <= 1); // Comprobamos AVL y orden
}

bool resuelveCaso() {
    // la letra dice de qué tipo es el árbol (N números, P palabras)
    char tipo;
    cin >> tipo;
    if (!cin)  // fin de la entrada
        return false;

    int altura = 0;
    bool hayAnterior = false;
    bool ok;
    if (tipo == 'N') {
        int anterior;
        ok = leerAVL(altura, anterior, hayAnterior);
    } else {
        string anterior;
        ok = leerAVL(altura, anterior, hayAnterior);
    }
    cout << (ok ? "SI" : "NO") << '\n';
    return true;
}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   while (resuelveCaso());

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}

//ENTRADA SALIDA
/*
ENTRADA DE EJEMPLO
N
((. 1 .) 2 (. 3 (. 4 .)))
N
(. 1 ((. 2 .) 3 (. 4 .)))
P
((. raton .) cabra (. perro (. gato .)))
P
((. dos .) tres (. uno .))
N
.

SALIDA DE EJEMPLO
SI
NO
NO
SI
SI

*/
