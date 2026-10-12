// =====================================================================
// Acepta el Reto #341 - Reina del super
// https://aceptaelreto.com/problem/statement.php?id=341
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-3/EJ_02-3.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - la entrada termina al acabarse el fichero (no hay caso `0 0`)
// =====================================================================

#include <iostream>
#include <queue>
#include <vector>
#include <utility>
using namespace std;

/*
Cajas --> 1 <= N <= 250.000
Clientes --> 1 <= C <= 250.000
Tiempo de atencion --> 1 <= T <= 100
Instante maximo: 500.000 * 100 = 50.000.000 --> cabe en int
*/

bool resuelveCaso() {
    int cajas;
    if (!(cin >> cajas)) return false;
	// si no hay cajas, no hay caso que resolver
    if (cajas == 0) return false;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> cola;

    for (int i = 1; i <= cajas; ++i) {
		//genero los pares (tiempo, id) de los cajeros y los meto en la cola
        cola.push(pair<int, int>(0, i));
	}

    int clientes;
    cin >> clientes;
	//Simulo la llegada de los clientes, y voy actualizando el tiempo de cada cajero
    for (int i = 0; i < clientes; ++i) {
        int tiempo;
        cin >> tiempo;
        pair<int, int> cajero = cola.top(); cola.pop();
        cajero.first += tiempo;
        cola.push(cajero);
    }
	cout << cola.top().second << '\n'; // cajero que le tocara a Ismael (el acosador)
	return true;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}
