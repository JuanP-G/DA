// =====================================================================
// Acepta el Reto #505 - Volando drones
// https://aceptaelreto.com/problem/statement.php?id=505
//
// Version lista para enviar: un solo fichero, con las cabeceras dentro.
// Generada por herramientas/para_acepta.py a partir de 3-Colas de prioridad variable (Heapsort)/EJ_03-1/EJ_03-1.cpp
// (no la edites a mano: se vuelve a generar).
// =====================================================================

#include <iostream>
#include <vector>
#include <functional> //greater
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
drones	--> 1 <= N <= 100.000 (10^5)
pila 9V/1.5V --> 1 <= pila <= 200.000 (2*10^5)
*/

bool resolverCaso(){
	int drones;
	if (!(cin >> drones)) return false;

	int pila9V, pila1V; 
	cin >> pila9V >> pila1V; // no se usan, solo para leer la entrada


	//creo la cola maximos de las pilas de 9V
	IndexPQ<int, greater<int>> cola9V(pila9V); //greater<int> para que sea maximos
	for(int i = 0; i < pila9V; ++i) {
		int horas;
		cin >> horas;
		cola9V.push(i, horas);
	}

	//creo la cola maximos de las pilas de 1.5V
	IndexPQ<int, greater<int>> cola1V(pila1V); //greater<int> para que sea maximos
	for(int i = 0; i < pila1V; ++i) {
		int horas;
		cin >> horas;
		cola1V.push(i, horas);
	}

	//Si no hay drones no puedo volar, devolvemos 0
	if(drones <= 0) {
		cout << "0\n";
		return true;
	}

	//puedo volar el finde si tengo al menos 1 pila de cada tipo y al menos 1 drone
	//2 pilas por drone, 1 de cada tipo
	bool primero = true;
	while (!cola1V.empty() && !cola9V.empty()) {
		int horasFinde = 0;
		vector<pair<int, int>> sobran9V, sobran1V; //para guardar las pilas usadas y devolverlas a la cola

		//cogemos un drone y le metemos 1 pila de cada tipo hasta quedarnos sin drones o pilas
		int contador = 0;
		while (contador < drones && !cola9V.empty() && !cola1V.empty()) {
			//auto = IndexPQ<int, greater<int>>::Par
			auto p9 = cola9V.top();   cola9V.pop();
			auto p1 = cola1V.top();   cola1V.pop();
			// p9.elem, p9.prioridad, p1.elem, p1.prioridad

			int tiempo = min(p9.prioridad, p1.prioridad); //tiempo que puedo volar ese drone
			horasFinde += tiempo;
			p9.prioridad -= tiempo; //restamos el tiempo volado a la pila de 9V
			p1.prioridad -= tiempo; //restamos el tiempo volado a la pila de 1.5V
			if (p9.prioridad > 0) sobran9V.push_back({ p9.elem, p9.prioridad }); //si sobra tiempo de la pila de 9V la guardamos para devolverla a la cola
			if (p1.prioridad > 0) sobran1V.push_back({ p1.elem, p1.prioridad }); //si sobra tiempo de la pila de 1.5V la guardamos para devolverla a la cola

			++contador;
		}
		
		for (auto& s : sobran9V) cola9V.push(s.first, s.second); //devolvemos las pilas de 9V sobrantes a la cola
		for (auto& s : sobran1V) cola1V.push(s.first, s.second); //devolvemos las pilas de 1.5V sobrantes a la cola

		if (!primero) cout << ' '; //si no es el primer caso, ponemos un espacio
		cout << horasFinde; //devolvemos las horas voladas ese finde
		primero = false;
	}
	cout << '\n';
	return true;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	while (resolverCaso());
	return 0;
}
