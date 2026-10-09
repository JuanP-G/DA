#include <iostream>
#include <algorithm>
#include <climits>
#include <cstdlib>

using namespace std;

bool leerAVL(int& altura, int& min, int& max);

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int casos;
	cin >> casos;
	
	for (int i = 0; i < casos; ++i) {
		int altura = 0, minimo = 0, maximo = 0;
		cout << (leerAVL(altura, minimo, maximo) ? "SI" : "NO") << endl;

	}
}

bool leerAVL(int& altura, int& minimo, int& maximo) {
	int valor;
	cin >> valor;

	if (valor == -1) { // árbol vacío
		altura = 0;
		minimo = INT_MAX; // centinela para el mínimo
		maximo = INT_MIN; // centinela para el máximo
		return true;
	}

	// Leer subárbol izquierdo y derecho
	int altIzq, minIzq, maxIzq;
	int altDer, minDer, maxDer;

	bool izqOK = leerAVL(altIzq, minIzq, maxIzq); // Leer subárbol izquierdo
	bool derOK = leerAVL(altDer, minDer, maxDer); // Leer subárbol derecho

	altura = max(altIzq, altDer) + 1; // Actualizar altura
	minimo = min(minIzq, valor); // Actualizar mínimo
	maximo = max(maxDer, valor); // Actualizar máximo

	// Comprobamos tanto la propiedad de AVL como la propiedad de árbol binario de búsqueda
	return izqOK && derOK && (abs(altIzq - altDer) <= 1) && (maxIzq < valor) && (valor < minDer);
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

    // Propiedad de Árbol Binario de Búsqueda (claves estrictamente menores/mayores)
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
    // Optimización de E/S estándar en C++
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