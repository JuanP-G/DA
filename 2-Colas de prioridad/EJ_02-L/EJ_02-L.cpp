#include <iostream>
#include <vector>
#include <queue>

using namespace std;

//escenas de renderizado --> 𝟣 <= 𝘙 <= 𝟤.𝟢𝟢𝟢.𝟢𝟢0
//estaciones de renderizado--> 𝟣 <= 𝘛 <= 𝟣𝟢𝟢.𝟢𝟢0
bool resuelveCaso() {
	int escenas, estaciones;
	if (!(cin >> escenas >> estaciones)) return false;

	// cola de minimos de instantes de liberacion de estaciones
    priority_queue<long long, vector<long long>, greater<long long>> cola;
    for (int i = 0; i < estaciones; ++i)
        cola.push(0);        // todas libres en el instante 0

    long long maxT = 0;

    for (int i = 0; i < escenas; ++i) {
        long long minuto, tiempo;
		cin >> minuto >> tiempo;

		//cogemos la estacion que se liberara antes
        long long libre = cola.top(); cola.pop();
		// queremos entrar en el instante minuto, pero la estacion puede estar ocupada hasta libre
        long long inicio = max(libre, minuto);
		// ponemos el tiempo maximo de espera
		maxT = max(maxT, inicio - minuto);
		//volvemos a meter en la cola el instante en que se liberara la estacion
        cola.push(inicio + tiempo);
    }
    
    //sacammos el tiempo maximo de espera
	cout << maxT << '\n';
    return true;
}

int main()
{
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}