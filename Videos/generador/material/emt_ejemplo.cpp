/**
 * Experimentos con el grafo de paradas de los autobuses urbanos de Madrid.
 */

#include <iostream>
#include <fstream>
#include <iomanip>
#include <limits>
#include <vector>
#include <queue>
#include <unordered_map>

#include "Digrafo.h"

using namespace std;

const char* PARADAS_PATH = "paradas.txt";
const char* LINEAS_PATH = "líneas.txt";

/**
 * Lee el archivo de paradas para encontrar el número máximo de parada.
 */
int leeParadaMaxima() {
	ifstream archivo(PARADAS_PATH);

	if (archivo.is_open()) {
		// Sabemos que están ordenadas, así que basta con el índice de la última
		int parada;
		archivo >> parada;

		while (archivo) {
			// Ignora el resto de la línea
			archivo.ignore(numeric_limits<streamsize>::max(), '\n');
			archivo >> parada;
		}

		return parada;
	}

	return -1;  // devuelve -1 para indicar error
}

/**
 * Lee la tabla de número de parada a su nombre.
 */
vector<string> leeNombresParada(int maximaParada) {
	ifstream archivo(PARADAS_PATH);
	vector<string> nombres(maximaParada);

	if (archivo.is_open()) {
		int parada;
		string nombre;

		while (true) {
			archivo >> parada;         // Número de parada
			archivo.ignore();          // Se come un espacio
			getline(archivo, nombre);  // Nombre de la parada

			if (!archivo) break;
			nombres[parada - 1] = nombre;
		}
	}

	return nombres;
}


/**
 * Lee el grafo de paradas de la EMT con las paradas como vértices y
 * una arista entre dos paradas si hay una línea de autobús que las
 * conecta directamente.
 */
Digrafo leeGrafoEMT() {
	// Número máximo de parada
	int maximaParada = leeParadaMaxima();

	// Digrafo que vamos a construir
	Digrafo	bus(maximaParada);

	ifstream archivo(LINEAS_PATH);

	if (archivo.is_open()) {
		string nombreLinea;      // Nombre de la línea
		int numParadasLinea[2];  // Número de paradas de ida y de vuelta

		archivo >> nombreLinea >> numParadasLinea[0] >> numParadasLinea[1];

		while (archivo) {
			// Añade las aristas por cada tramo de bus
			for (int i = 0; i < 2; ++i) {
				int anterior, parada, metros;
				archivo >> anterior >> metros;

				for (int k = 1; k < numParadasLinea[i]; ++k) {
					archivo >> parada >> metros;
					bus.ponArista(anterior - 1, parada - 1);
					anterior = parada;
				}
			}

			archivo >> nombreLinea >> numParadasLinea[0] >> numParadasLinea[1];
		}
	}

	return bus;
}

/**
 * Añade vértices en ambas direcciones entre las paradas de idéntico nombre,
 * pues suelen ser paradas enfrentadas a ambos lados de una calle.
 */
void ponGemelas(Digrafo& g) {
	ifstream archivo (PARADAS_PATH);
	unordered_map<string, int> paradas;

	if (archivo.is_open()) {
		while (true) {
			int numero; string nombre;
			archivo >> numero;
			archivo.ignore();
			getline(archivo, nombre);

			if (!archivo)
				break;

			auto it = paradas.find(nombre);

			if (it != paradas.end()) {
				g.ponArista(it->second, numero - 1);
				g.ponArista(numero - 1, it->second);
			}
			else {
				paradas[nombre] = numero - 1;
			}
		}
	}
}

using Camino = deque<int>;

/**
 * Clase para la BFS de las diapositivas (modificada para terminar al encontrar el destino).
 */
class CaminoMasCorto {
	public:
	CaminoMasCorto(Digrafo const& g, int s, int d) : visit(g.V(), false), ant(g.V()), dist(g.V()), s(s), d(d) {
		bfs(g);
	}

	// ¿hay camino del origen a v?
	bool hayCamino(int v) const {
		return visit[v];
	}

	// número de aristas entre s y v
	int distancia(int v) const {
		return dist[v];
	}

	// devuelve el camino más corto desde el origen a v (si existe)
	Camino camino(int v) const {
		if (!hayCamino(v)) throw std::domain_error("No existe camino");
		Camino cam;
		for (int x = v; x != s; x = ant[x])
			cam.push_front(x);
			cam.push_front(s);
		return cam;
	}
private:
	std::vector<bool> visit; // visit[v] = ¿hay camino de s a v?
	std::vector<int> ant;    // ant[v] = último vértice antes de llegar a v
	std::vector<int> dist;   // dist[v] = aristas en el camino s-v más corto
	int s, d;

	void bfs(Digrafo const& g) {
		std::queue<int> q;
		dist[s] = 0; visit[s] = true;
		q.push(s);
		while (!q.empty()) {
			int v = q.front(); q.pop();
			for (int w : g.ady(v)) {
				if (!visit[w]) {
					ant[w] = v; dist[w] = dist[v] + 1; visit[w] = true;
					if (w == d)
						return;
					q.push(w);
				}
			}
		}
	}
};

/**
 * Clase para la DFS de las diapositivas (modificada para terminar al encontrar el destino).
 */
class CaminosDFS {
	private:
	std::vector<bool> visit; // visit[v] = ¿hay camino de s a v?
	std::vector<int> ant;// ant[v] = último vértice antes de llegar a v
	int s, d; // vértice origen y destino
	bool encontrado = false;

	void dfs(Digrafo const& G, int v) {
		visit[v] = true;

		if (v == d) {
			encontrado = true;
			return;
		}

		for (int w : G.ady(v)) {
			if (!visit[w] && !encontrado) {
				ant[w] = v;
				dfs(G, w);
			}
		}
	}

public:
	CaminosDFS(Digrafo const& g, int s, int d) : visit(g.V(), false), ant(g.V()), s(s), d(d) {
		dfs(g, s);
	}

	// ¿hay camino del origen a v?
	bool hayCamino(int v) const {
		return visit[v];
	}

	// para representar caminos
	// devuelve un camino desde el origen a v (debe existir)
	Camino camino(int v) const {
		if (!hayCamino(v))
			throw std::domain_error("No existe camino");
		Camino cam;
		// recuperamos el camino retrocediendo
		for (int x = v; x != s; x = ant[x])
			cam.push_front(x);
		cam.push_front(s);
		return cam;
	}
};

/**
 * Muestra las paradas de un camino.
 */
void muestraCamino(const Camino& camino, const vector<string>& nombres) {
	for (int paso : camino) {
		cout << setw(5) << paso + 1 << " " << nombres[paso] << "\n";
	}
}

int main() {
	constexpr int INFORMATICA = 3863;
	constexpr int MATEMATICAS = 1693;

	Digrafo bus = leeGrafoEMT();
	vector<string> nombres = leeNombresParada(bus.V());

	ponGemelas(bus);

	// (1) Camino con menor número de paradas
	CaminoMasCorto cmc(bus, INFORMATICA - 1, MATEMATICAS - 1);
	cout << cmc.distancia(MATEMATICAS - 1) << "\n";

	muestraCamino(cmc.camino(MATEMATICAS - 1), nombres);

	// (2) Camino que encuentra la búsqueda en profundidad
/*	CaminosDFS cdfs(bus, INFORMATICA - 1, MATEMATICAS - 1);
	Camino camino = cdfs.camino(MATEMATICAS - 1);
	cout << camino.size() << "\n";

	muestraCamino(camino, nombres);
	cout << "---\n";
*/

	return 0;
}
