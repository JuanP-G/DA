
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <string>
using namespace std;

#include "bintree.h"  // estructuras de datos de clase

/*@ <answer>

 ¿Es un árbol AVL? (versión genérica)

 Cada caso es una letra (N = enteros, P = palabras) y un árbol en el formato de bintree.h.
 Decidir si es AVL. La entrada acaba con el fichero.

 PLANTEAMIENTO
 Se lee el árbol con read_tree<T> y se recorre en postorden: analizar devuelve, para cada
 subárbol, si es AVL, su altura y su mínimo y máximo. Un nodo es AVL si sus hijos lo son, la
 diferencia de alturas es <= 1 y todo el izquierdo es menor y todo el derecho mayor que él.
 Con plantillas (template) sirve igual para int y para string.

 Coste: O(n) por árbol, con n el número de nodos.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

// Información que necesito de cada subárbol para poder decidir sobre el nodo padre.
template <class T>
struct Info {
    bool esAVL;
    int altura;    // -1 si el subárbol está vacío
    T minimo;      // solo tiene sentido si altura != -1
    T maximo;      // idem
};

// Recorrido en postorden: primero los dos hijos y después el nodo, porque
// para decidir sobre un nodo necesito tener ya resueltos sus subárboles.
template <class T>
Info<T> analizar(const BinTree<T>& arbol) {
    if (arbol.empty()) return { true, -1, T(), T() };

    Info<T> izq = analizar(arbol.left());
    Info<T> der = analizar(arbol.right());
    T elem = arbol.root();

    bool hayIzq = (izq.altura != -1);
    bool hayDer = (der.altura != -1);

    Info<T> actual;

    // La altura de un nodo es la del hijo más alto, más uno.
    actual.altura = 1 + max(izq.altura, der.altura);

    // El menor valor del subárbol está en el izquierdo, o es el propio
	// nodo si no hay hijo izquierdo y viceversa para el máximo.
    actual.minimo = hayIzq ? izq.minimo : elem;
    actual.maximo = hayDer ? der.maximo : elem;

	actual.esAVL = izq.esAVL && der.esAVL             // comprobamos que sus hijos son AVL
        && abs(izq.altura - der.altura) <= 1  // factor de equilibrio
        && (!hayIzq || izq.maximo < elem)     // todo el izq es menor
        && (!hayDer || elem < der.minimo);    // todo el der es mayor

    return actual;
}

// Lee un árbol del tipo pedido y escribe la respuesta.
template <class T>
void resuelveArbol() {
    BinTree<T> arbol = read_tree<T>(cin);
    cout << (analizar(arbol).esAVL ? "SI" : "NO") << '\n';
}

bool resuelveCaso() {
    // la letra dice de qué tipo es el árbol de la línea siguiente
    char tipo;
    cin >> tipo;
    if (!cin)  // fin de la entrada
        return false;
    if (tipo == 'N') resuelveArbol<int>();
    else resuelveArbol<string>();
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
