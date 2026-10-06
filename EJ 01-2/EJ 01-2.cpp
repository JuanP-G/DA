#include <iostream>
#include "bintree.h"
#include "TreeSet_AVL_plantilla.h"

using namespace std;



int main(){

	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);

	int nValores;

	//Mientras siga habiendo casos 
	while (cin >> nValores && nValores != 0)	{

		//entrada de los valores del arbol
		Set<int> arbol;
		for (int i = 0; i < nValores; ++i) {
			int valor;
			cin >> valor;
			//Agregar valor al arbol
			arbol.insert(valor);
		}

		//numero de numeros que queremos consultar
		int nConsultas;
		cin >> nConsultas;

		//Consulta de los numeros que queremos consultar
		for (int i = 0; i < nConsultas; ++i) {
			int	posValor;
			cin >> posValor;
			try {
				cout << arbol.kesimo(posValor) << '\n';
			}
			catch (out_of_range&) {
				cout << "??\n";
			}
		}
		cout << "---\n"; //Separador entre casos
	}
}