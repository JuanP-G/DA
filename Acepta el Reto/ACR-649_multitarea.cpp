// =====================================================================
// Acepta el Reto #649 - Multitarea
// https://aceptaelreto.com/problem/statement.php?id=649
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 3-Colas de prioridad variable (Heapsort)/EJ_03-3/EJ_03-3.cpp
// (no la edites a mano: se vuelve a generar).
//
// Cambios respecto a la version de la asignatura:
//  - no hay numero de casos: se lee hasta el final del fichero
//  - los instantes llegan hasta 10^9: `long long`
// =====================================================================

#include <iostream>
// ---------- IndexPQ.h (copiado aqui porque Acepta el Reto solo admite un fichero) ----------
/**
 * Implementacion de colas con prioridad mediante monticulos.
 * Los elementos son enteros de 0 a N-1 que tienen asociada una prioridad
 * dentro de la cola. La prioridad de un elemento puede ser modificada
 * con coste en O(log N).
 *
 * Copyright (c) 2020 Alberto Verdejo
 * Modificado por 2023 Ignacio Fabregas
 */

#ifndef INDEXPQ_H_
#define INDEXPQ_H_

#include <iostream>
#include <stdexcept>
#include <vector>


 // T es el tipo de las prioridades
 // Comparator dice cuando un valor de tipo T es mas prioritario que otro
template <typename T = int, typename Comparator = std::less<T>>
class IndexPQ {

public:
    // Registro para las parejas < elem, prioridad >
    struct Par {
        int elem;
        T prioridad;
    };

private:
    // vector que contiene los datos (pares < elem, prioridad >)
    std::vector<Par> array;      // El primer elemento esta en la posicion 1

    // vector que contiene las posiciones en array de los elementos
    std::vector<int> posiciones;   // un 0 indica que el elemento no esta

    /* Objeto funcion que sabe comparar elementos.
     * antes(a,b) es cierto si a es mas prioritario que b (a debe salir antes que b)
     */
    Comparator antes;

public:
    IndexPQ(int N, Comparator c = Comparator()) : array(1), posiciones(N, 0), antes(c) {}

    IndexPQ(IndexPQ<T, Comparator> const&) = default;

    IndexPQ<T, Comparator>& operator=(IndexPQ<T, Comparator> const&) = default;

    ~IndexPQ() = default;

    // e debe ser uno de los posibles elementos
    void push(int e, T const& p) {
        if (posiciones.at(e) != 0)
            throw std::invalid_argument("No se pueden insertar elementos repetidos.");
        else {
            array.push_back({ e, p });
            posiciones[e] = size();
            flotar(size());
        }
    }

    // Actualizar la prioridad del elemento e
    void update(int e, T const& p) {
        int i = posiciones.at(e);
        if (i == 0) // el elemento e se inserta por primera vez
            push(e, p);
        else {
            array[i].prioridad = p;
            if (i != 1 && antes(array[i].prioridad, array[i / 2].prioridad))
                flotar(i);
            else // puede hacer falta hundir a e
                hundir(i);
        }
    }

    int size() const {
        return int(array.size()) - 1;
    }

    bool empty() const {
        return size() == 0;
    }

    Par const& top() const {
        if (size() == 0)
            throw std::domain_error("No se puede consultar el primero de una cola vacia");
        else return array[1];
    }

    T const& priority(int e) const {
        if (posiciones.at(e) == 0)
            throw std::invalid_argument("No se puede consultar la prioridad de un elemento que no existe");
        else
            return array[posiciones[e]].prioridad;
    }

    void pop() {
        if (size() == 0) throw std::domain_error("No se puede eliminar el primero de una cola vacia.");
        else {
            posiciones[array[1].elem] = 0; // para indicar que no esta
            if (size() > 1) {
                array[1] = std::move(array.back());
                posiciones[array[1].elem] = 1;
                array.pop_back();
                hundir(1);
            }
            else
                array.pop_back();
        }
    }

    /* Escritura del monticulo. Metodo para depurar */
    void print() {
        std::cout << "[";
        for (int i = 1; i < array.size() - 1; i++)
            std::cout << array[i] << ", ";
        std::cout << array[array.size() - 1] << "]" << std::endl;
    }

private:

    void flotar(int i) {
        Par parmov = std::move(array[i]);
        int hueco = i;
        while (hueco != 1 && antes(parmov.prioridad, array[hueco / 2].prioridad)) {
            array[hueco] = std::move(array[hueco / 2]); posiciones[array[hueco].elem] = hueco;
            hueco /= 2;
        }
        array[hueco] = std::move(parmov); posiciones[array[hueco].elem] = hueco;
    }

    void hundir(int i) {
        Par parmov = std::move(array[i]);
        int hueco = i;
        int hijo = 2 * hueco; // hijo izquierdo, si existe
        while (hijo <= size()) {
            // cambiar al hijo derecho de i si existe y va antes que el izquierdo
            if (hijo < size() && antes(array[hijo + 1].prioridad, array[hijo].prioridad))
                ++hijo;
            // flotar el hijo si va antes que el elemento hundiendose
            if (antes(array[hijo].prioridad, parmov.prioridad)) {
                array[hueco] = std::move(array[hijo]); posiciones[array[hueco].elem] = hueco;
                hueco = hijo; hijo = 2 * hueco;
            }
            else break;
        }
        array[hueco] = std::move(parmov); posiciones[array[hueco].elem] = hueco;
    }

};

#endif /* INDEXPQ_H_ */
// ---------- fin de IndexPQ.h ----------

using namespace std;

/*
	N --> tareas unicas
	M --> tareasperiodicas
	T --> minutos donde saber si hay conflictos
*/
void resuelveCaso() {
	int N, M, T;
	cin >> N >> M >> T;

	IndexPQ<pair<long long, long long>> cola(N + M);   // prioridad = (ini, fin)
	vector<long long> periodo(N + M, 0);        // 0 --> tarea unica
	// 1..N --> Tareas unicas
	for (int i = 0; i < N; i++) {
		long long ini, fin;
		cin >> ini >> fin;
		cola.push(i, { ini, fin });
	}

	// n..M+N --> Tareas periodicas
	for (int i = N; i < N + M; i++) {
		long long ini, fin, p;
		cin >> ini >> fin >> p;
		cola.push(i, { ini, fin });
		periodo[i] = p;
	}

	long long tiempoActual = 0;
	bool hayConflictos = false;
	while (!hayConflictos && !cola.empty() && cola.top().prioridad.first < T) {
		auto tarea = cola.top();
		int elem = tarea.elem;
		long long ini = tarea.prioridad.first;
		long long fin = tarea.prioridad.second;

		if (ini < tiempoActual) hayConflictos = true;
		else {
			tiempoActual = fin;
			if (periodo[elem] != 0)
				cola.update(elem, { ini + periodo[elem], fin + periodo[elem] });
			else
				cola.pop();
		}
	}

	cout << (hayConflictos ? "SI" : "NO") << "\n";
}

int main() {

	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	while (cin >> ws && cin.peek() != EOF) resuelveCaso();

	return 0;
}
