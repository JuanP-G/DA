#include <iostream>
#include <algorithm>
#include <climits>
#include <string>
#include <cstdlib>

using namespace std;

template <typename T>
bool leerAVL(int& altura, T& anterior, bool& hayAnterior);

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	// Leemos el tipo de datos (N para números, P para palabras)
	char tipo;
	while (cin >> tipo) {
		int altura = 0;
		bool hayAnterior = false;
		bool ok;

		if(tipo == 'N') {
			int anterior;
			ok = leerAVL(altura, anterior, hayAnterior); // T es int
		} else { //if (tipo == 'P')
			string anterior;
			ok = leerAVL(altura, anterior, hayAnterior); // T es string
		}

		cout << (ok ? "SI" : "NO") << endl;
	}
}

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