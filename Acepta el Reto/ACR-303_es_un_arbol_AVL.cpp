// =====================================================================
// Acepta el Reto #303 - Es un arbol AVL?
// https://aceptaelreto.com/problem/statement.php?id=303
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 1-Arboles AVL/EJ_01-1/EJ 01-1.cpp
// (no la edites a mano: se vuelve a generar).
// =====================================================================

/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>
#include <algorithm>
#include <climits>
#include <cstdlib>
using namespace std;

/*@ <answer>

 Es un arbol AVL?

 Arbol binario de enteros en preorden (-1 = vacio). Decidir si es AVL: de busqueda
 (estricto) y con alturas de los hijos que difieren como mucho en 1 en todo nodo.

 PLANTEAMIENTO
 No se construye el arbol: leerAVL(altura, minimo, maximo) lee un subarbol y lo comprueba a
 la vez. Como viene en preorden, se lee la raiz y se llama dos veces (izquierdo y derecho).
 Devuelve si es AVL y deja por referencia su altura, su minimo y su maximo
 (vacio: altura 0, minimo INT_MAX, maximo INT_MIN). Un nodo es AVL si:
   - los dos hijos lo son,
   - |altIzq - altDer| <= 1,
   - maxIzq < valor < minDer.

 Coste: O(n) por arbol, con n el numero de nodos (cada nodo se lee una vez).

 @ </answer> */


// ================================================================
// Escribe el codigo completo de tu solucion aqui debajo
// ================================================================
//@ <answer>

bool leerAVL(int& altura, int& min, int& max);

bool leerAVL(int& altura, int& minimo, int& maximo) {
	int valor;
	cin >> valor;

	if (valor == -1) { // arbol vacio
		altura = 0;
		minimo = INT_MAX; // centinela para el minimo
		maximo = INT_MIN; // centinela para el maximo
		return true;
	}

	// Leer subarbol izquierdo y derecho
	int altIzq, minIzq, maxIzq;
	int altDer, minDer, maxDer;

	bool izqOK = leerAVL(altIzq, minIzq, maxIzq); // Leer subarbol izquierdo
	bool derOK = leerAVL(altDer, minDer, maxDer); // Leer subarbol derecho

	altura = max(altIzq, altDer) + 1; // Actualizar altura
	minimo = min(minIzq, valor); // Actualizar minimo
	maximo = max(maxDer, valor); // Actualizar maximo

	// Comprobamos tanto la propiedad de AVL como la propiedad de arbol binario de busqueda
	return izqOK && derOK && (abs(altIzq - altDer) <= 1) && (maxIzq < valor) && (valor < minDer);
}

void resuelveCaso() {
    int altura = 0, minimo = 0, maximo = 0;
    cout << (leerAVL(altura, minimo, maximo) ? "SI" : "NO") << '\n';
}

//@ </answer>
//  Lo que se escriba dejado de esta linea ya no forma parte de la solucion.

int main() {
    int casos; cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}

//ENTRADA SALIDA
/*
ENTRADA DE EJEMPLO 
3
2 1 -1 -1 3 -1 4 -1 -1
1 -1 3 2 -1 -1 4 -1 -1
4 1 -1 -1 3 -1 2 -1 -1

SALIDA DE EJEMPLO
SI
NO
NO
*/

//VERSION OPTIMIZADA
/*
#include <iostream>
#include <algorithm>
#include <cmath>

using namespace std;

struct Info {
    bool is_avl;
    int height;
    int min_val;
    int max_val;
};

Info checkAVL() {
    int val;
    cin >> val;

    if (val == -1) {
        return {true, 0, 0, 0};
    }

    Info left = checkAVL();
    Info right = checkAVL();

    bool ok = left.is_avl && right.is_avl;

    // Propiedad de equilibrio de alturas
    if (abs(left.height - right.height) > 1) {
        ok = false;
    }

    // Propiedad de Arbol Binario de Busqueda (claves estrictamente menores/mayores)
    if (left.height > 0 && left.max_val >= val) {
        ok = false;
    }
    if (right.height > 0 && right.min_val <= val) {
        ok = false;
    }

    int h = 1 + max(left.height, right.height);
    int min_v = (left.height > 0) ? left.min_val : val;
    int max_v = (right.height > 0) ? right.max_val : val;

    return {ok, h, min_v, max_v};
}

int main() {
    // Optimizacion de E/S estandar en C++
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int t;
    if (cin >> t) {
        while (t--) {
            Info res = checkAVL();
            if (res.is_avl) {
                cout << "SI\n";
            } else {
                cout << "NO\n";
            }
        }
    }
    return 0;
}
*/
