// =====================================================================
// Acepta el Reto #311 - Ordenando a los pacientes en urgencias
// https://aceptaelreto.com/problem/statement.php?id=311
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 2-Colas de prioridad/EJ_02-5/EJ_02-5.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - el separador de cada caso es `----` (cuatro guiones)
// =====================================================================

#include <iostream>
#include <vector>
#include <queue>

using namespace std;

/*
    Casos --> 1 <= N <= 200.000  (2*10^5)
	Gravedad --> 1 <= N <= 1.000.000   (10^0)
	I (Ingreso) --> Los nombres son strings de 1 a 20 caracteres, sin espacios
	A (Atencion) --> No hay atencion si no hay pacientes
*/

struct Paciente {
    string nombre;
    int gravedad;
    int orden; // orden de llegada

	// primero por gravedad, y a igualdad, por orden de llegada
    bool operator<(const Paciente& o) const {
        if (gravedad != o.gravedad) return gravedad < o.gravedad;
        return orden > o.orden;
	}
};

bool resuelveCaso() {
    int casos;
    if(!(cin >> casos) || casos == 0) return false;
    priority_queue<Paciente> cola;

    for (int i = 0; i < casos; ++i) {
        char tipo;
		cin >> tipo;
        if (tipo == 'I') {
            string nombre;
			cin >> nombre;
			int gravedad;
            cin >> gravedad;
            cola.push({ nombre, gravedad, i });
        }
        else if (tipo == 'A') {
            if (!cola.empty()) {
                cout << cola.top().nombre << '\n';
                cola.pop();
            }
        }
    }
        
	cout << "----\n";
	return true;
}

int main()
{
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    while (resuelveCaso());
    return 0;
}
