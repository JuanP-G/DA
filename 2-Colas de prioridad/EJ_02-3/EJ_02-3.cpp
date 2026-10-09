#include <iostream>
#include <queue>
#include <vector>
#include <utility>
using namespace std;

/*
Cajas --> 1 ≤ 𝘕 ≤ 𝟤𝟧𝟢.𝟢𝟢0
Clientes --> 1 ≤ C ≤ 𝟤𝟧𝟢.𝟢𝟢0
Tiempo de atencion --> 1 ≤ T ≤ 1𝟢0
Instante maximo: 500.000 * 100 = 50.000.000 --> cabe en int
*/

bool resuelveCaso() {
    int cajas;
    cin >> cajas;
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