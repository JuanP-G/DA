#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>

#include "bintree.h"

using namespace std;

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
void resolverCaso() {
    BinTree<T> arbol = read_tree<T>(cin);
    cout << (analizar(arbol).esAVL ? "SI" : "NO") << '\n';
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // No hay número de casos: se lee hasta agotar la entrada. La letra
    // dice de qué tipo es el árbol de la línea siguiente.
    char tipo;
    while (cin >> tipo) {
        if (tipo == 'N') {
            resolverCaso<int>();
        }
        else {
            resolverCaso<string>();
        }
    }

    return 0;
}