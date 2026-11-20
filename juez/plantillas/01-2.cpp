
/*@ <answer>
 *
 * Nombre y Apellidos:
 *
 *@ </answer> */

#include <iostream>
#include <fstream>

using namespace std;

#include "bintree.h"  // estructuras de datos de clase

/*@ <answer>

 Encontrar el k-ésimo elemento en un árbol AVL

 Se insertan N valores en un Set (árbol AVL) y para cada consulta k se escribe el k-ésimo menor,
 o ?? si no existe. Tras cada caso, ---. La entrada acaba con un caso con N = 0.

 PLANTEAMIENTO
 Cada nodo guarda tami = tamaño de su hijo izquierdo + 1 (la posición de la raíz en su subárbol),
 mantenido en inserta y en las rotaciones (ver TreeSet_AVL_plantilla.h). kesimo(k) baja desde la raíz:
 k == tami -> la raíz; k < tami -> izquierdo con el mismo k; k > tami -> derecho con k - tami.
 Si se llega a un hueco lanza out_of_range y se escribe ??.

 Coste: O(log N) por inserción y por consulta: O((N + Q) log N) por caso.

 @ </answer> */


// ================================================================
// Escribe el código completo de tu solución aquí debajo
// ================================================================
//@ <answer>

// Conjunto con árbol AVL (TreeSet_AVL_plantilla.h, versión de clase SIN tami ni kesimo).
// Tienes que añadir a cada nodo el atributo tami (tamaño del hijo izquierdo + 1), mantenerlo
// donde haga falta y programar kesimo(k). En el juez la clase va en este mismo fichero.

/**
 * Implementación de conjuntos mediante Árboles de búsqueda AVL
 *
 * Copyright (c) 2020 Alberto Verdejo
 * Editado por 2023 Ignacio Fábregas
 */

#ifndef TREESET_AVL_H_
#define TREESET_AVL_H_

#include <algorithm>
#include <functional>
#include <stack>
#include <stdexcept>
#include <utility>
#include <iostream>
#include <iomanip>


template<class T, class Comparator = std::less<T>>
class Set {
protected:

    /*
     * Nodo que almacena internamente el elemento (de tipo T),
     * punteros al hijo izquierdo y derecho, que pueden ser nullptr si el hijo es vacío,
     * y la altura.
     */
    struct TreeNode;
    using Link = TreeNode*;

    struct TreeNode {
        T elem;       //elemento
        Link iz, dr;  //hijos izquierdo y derecho
        int altura;   //altura

        TreeNode(T const& e, Link i = nullptr, Link d = nullptr,
            int alt = 1) : elem(e), iz(i), dr(d), altura(alt) {
        }
    };

    // puntero a la raíz de la estructura jerárquica de nodos
    Link raiz;

    // número de elementos (cardinal del conjunto)
    int nelems;

    // objeto función que compara elementos (orden total estricto)
    Comparator menor;

public:

    // constructor (conjunto vacío)
    Set(Comparator c = Comparator()) : raiz(nullptr), nelems(0), menor(c) {}

    // constructor por copia
    Set(Set const& other) {
        copia(other);
    }

    // operador de asignación
    Set& operator=(Set const& that) {
        if (this != &that) {
            libera(raiz);
            copia(that);
        }
        return *this;
    }

    // destructor
    ~Set() {
        libera(raiz);
    };

    bool insert(T const& e) {
        return inserta(e, raiz);
    }

    bool empty() const {
        return raiz == nullptr;
    }

    int size() const {
        return nelems;
    }

    bool contains(T const& e) const {
        return pertenece(e, raiz);
    }

    bool erase(T const& e) {
        return borra(e, raiz);
    }

    /* Función de depuración. Recorre el árbol comprobando que la representación es coherente:
     * orden de búsqueda, el valor de altura, el equilibrio AVL
     * y el número total de nodos.
     * Devuelve true si es correcto.
     * Si no lo es, describe el error.
     * Llámalo tras cada insert/erase mientras depuras: assert(cjto.comprueba());
     * Necesita que los elementos se puedan escribir con <<.
     */
    bool comprueba(std::ostream& err = std::cerr) const {
        int alt;
        bool ok = true;
        int n = comprueba(raiz, alt, ok, err);
        if (n != nelems) {
            err << "nelems vale " << nelems << " y hay " << n << " nodos\n";
            ok = false;
        }
        return ok;
    }

protected:

    static const int TREE_INDENTATION = 4;

    void copia(Set const& other) {
        raiz = copia(other.raiz);
        nelems = other.nelems;
        menor = other.menor;
    }

    static Link copia(Link a) {
        if (a == nullptr) return nullptr;
        else return new TreeNode(a->elem, copia(a->iz), copia(a->dr), a->altura);
    }

    static void libera(Link a) {
        if (a != nullptr) {
            libera(a->iz);
            libera(a->dr);
            delete a;
        }
    }

    bool pertenece(T const& e, Link a) const {
        if (a == nullptr) {
            return false;
        }
        else if (menor(e, a->elem)) {
            return pertenece(e, a->iz);
        }
        else if (menor(a->elem, e)) {
            return pertenece(e, a->dr);
        }
        else { // e == a->elem
            return true;
        }
    }

    bool inserta(T const& e, Link& a) {
        bool crece;
        if (a == nullptr) { // se inserta el nuevo elemento e
            a = new TreeNode(e);
            ++nelems;
            crece = true;
        }
        else if (menor(e, a->elem)) {
            crece = inserta(e, a->iz);
            if (crece) reequilibraDer(a);
        }
        else if (menor(a->elem, e)) {
            crece = inserta(e, a->dr);
            if (crece) reequilibraIzq(a);
        }
        else // el elemento e ya estaba en el árbol
            crece = false;
        return crece;
    }

    int altura(Link a) {
        if (a == nullptr) return 0;
        else return a->altura;
    }

    void rotaDer(Link& r2) {
        Link r1 = r2->iz;
        r2->iz = r1->dr;
        r1->dr = r2;
        r2->altura = std::max(altura(r2->iz), altura(r2->dr)) + 1;
        r1->altura = std::max(altura(r1->iz), altura(r1->dr)) + 1;
        r2 = r1;
    }

    void rotaIzq(Link& r1) {
        Link r2 = r1->dr;
        r1->dr = r2->iz;
        r2->iz = r1;
        r1->altura = std::max(altura(r1->iz), altura(r1->dr)) + 1;
        r2->altura = std::max(altura(r2->iz), altura(r2->dr)) + 1;
        r1 = r2;
    }

    void rotaIzqDer(Link& r3) {
        rotaIzq(r3->iz);
        rotaDer(r3);
    }

    void rotaDerIzq(Link& r1) {
        rotaDer(r1->dr);
        rotaIzq(r1);
    }

    void reequilibraIzq(Link& a) {
        if (altura(a->dr) - altura(a->iz) > 1) {
            if (altura(a->dr->iz) > altura(a->dr->dr))
                rotaDerIzq(a);
            else rotaIzq(a);
        }
        else a->altura = std::max(altura(a->iz), altura(a->dr)) + 1;
    }

    void reequilibraDer(Link& a) {
        if (altura(a->iz) - altura(a->dr) > 1) {
            if (altura(a->iz->dr) > altura(a->iz->iz))
                rotaIzqDer(a);
            else rotaDer(a);
        }
        else a->altura = std::max(altura(a->iz), altura(a->dr)) + 1;
    }

    // devuelve y borra el mínimo del árbol con raíz en a
    T borraMin(Link& a) {
        if (a->iz == nullptr) {
            T min = a->elem;
            a = a->dr;
            --nelems;
            return min;
        }
        else {
            T min = borraMin(a->iz);
            reequilibraIzq(a);
            return min;
        }
    }

    bool borra(T const& e, Link& a) {
        bool decrece = false;
        if (a != nullptr) {
            if (menor(e, a->elem)) {
                decrece = borra(e, a->iz);
                if (decrece) reequilibraIzq(a);
            }
            else if (menor(a->elem, e)) {
                decrece = borra(e, a->dr);
                if (decrece) reequilibraDer(a);
            }
            else { // e == a->elem
                if (a->iz == nullptr || a->dr == nullptr) {
                    Link aux = a;
                    a = (a->iz == nullptr) ? a->dr : a->iz;
                    --nelems;
                    delete aux;
                }
                else { // tiene dos hijos
                    T min = borraMin(a->dr);
                    a->elem = min;
                    reequilibraDer(a);
                }
                decrece = true;
            }
        }
        return decrece;
    }

    /* Para depurar: devuelve el número de nodos del subárbol con raíz en a, deja su altura
     * en alt y pone ok a false si detecta alguna incoherencia
     */
    int comprueba(Link a, int& alt, bool& ok, std::ostream& err) const {
        if (a == nullptr) { alt = 0; return 0; }
        int alti, altd;
        int ni = comprueba(a->iz, alti, ok, err);
        int nd = comprueba(a->dr, altd, ok, err);
        if (a->iz != nullptr && !menor(a->iz->elem, a->elem)) {
            err << "el hijo izquierdo de " << a->elem << " no es menor\n";
            ok = false;
        }
        if (a->dr != nullptr && !menor(a->elem, a->dr->elem)) {
            err << "el hijo derecho de " << a->elem << " no es mayor\n";
            ok = false;
        }
        if (a->altura != std::max(alti, altd) + 1) {
            err << "la altura de " << a->elem << " vale " << a->altura
                << " y debería ser " << std::max(alti, altd) + 1 << "\n";
            ok = false;
        }
        if (alti - altd > 1 || altd - alti > 1) {
            err << "el nodo " << a->elem << " está desequilibrado: alturas "
                << alti << " y " << altd << "\n";
            ok = false;
        }
        alt = std::max(alti, altd) + 1;
        return ni + nd + 1;
    }

public:
    // iteradores que recorren los elementos del conjunto de menor a mayor
    class const_iterator {
    public:
        T const& operator*() const {
            if (act == nullptr)
                throw std::out_of_range("No hay elemento a consultar");
            return act->elem;
        }

        T const* operator->() const {
            return &operator*();
        }

        const_iterator& operator++() {  // ++ prefijo
            next();
            return *this;
        }

        bool operator==(const_iterator const& that) const {
            return act == that.act;
        }

        bool operator!=(const_iterator const& that) const {
            return !(this->operator==(that));
        }

    protected:
        friend class Set;

        Link act;
        std::stack<Link> ancestros;  // antecesores no visitados

        // construye el iterador al primero
        const_iterator(Link raiz) { act = first(raiz); }

        // construye el iterador al último
        const_iterator() : act(nullptr) {}

        Link first(Link ptr) {
            if (ptr == nullptr) {
                return nullptr;
            }
            else { // buscamos el nodo más a la izquierda
                while (ptr->iz != nullptr) {
                    ancestros.push(ptr);
                    ptr = ptr->iz;
                }
                return ptr;
            }
        }

        void next() {
            if (act == nullptr) {
                throw std::out_of_range("El iterador no puede avanzar");
            }
            else if (act->dr != nullptr) { // primero del hijo derecho
                act = first(act->dr);
            }
            else if (ancestros.empty()) { // hemos llegado al final
                act = nullptr;
            }
            else { // podemos retroceder
                act = ancestros.top();
                ancestros.pop();
            }
        }
    };

    const_iterator begin() const {
        return const_iterator(raiz);
    }

    const_iterator end() const {
        return const_iterator();
    }
};


#endif


bool resuelveCaso() {

    // Escribe aquí tu solución

}

//@ </answer>
//  Lo que se escriba dejado de esta línea ya no forma parte de la solución.

int main() {
   // ajustes para que cin extraiga directamente de un fichero
#ifndef DOMJUDGE
   std::ifstream in("casos.txt");
   auto cinbuf = std::cin.rdbuf(in.rdbuf());
#endif

   while (resuelveCaso());

   // para dejar todo como estaba al principio
#ifndef DOMJUDGE
   std::cin.rdbuf(cinbuf);
   system("PAUSE");
#endif
   return 0;
}
