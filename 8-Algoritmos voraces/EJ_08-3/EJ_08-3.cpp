#include <iostream>
#include <vector>

using namespace std;

/*
    Comienza la temporada

    N jugadores con su talla y M equipaciones con su talla (1 <= N, M <= 100.000, tallas 1..100).
    Un jugador puede usar una equipacion de su talla o de UNA talla mas. Escribir el minimo
    numero de equipaciones que hay que comprar para que jueguen todos.
*/

/*
    PLANTEAMIENTO (voraz)
    Solo hay 100 tallas, asi que se cuenta cuantos jugadores y cuantas equipaciones hay de cada
    talla. Se recorren las tallas de menor a mayor; los jugadores de talla t:
      1. usan primero las equipaciones de talla t (nadie mas puede usarlas: a los de talla t - 1
         ya se les ha atendido);
      2. si faltan, usan las de talla t + 1, que se descuentan para los jugadores de talla t + 1;
      3. los que sigan sin equipacion hay que comprarlas.

    Por que es optimo: una equipacion de talla t + 1 la pueden usar los de talla t o los de
    t + 1. Si la usa un jugador de talla t, el de talla t + 1 que se queda sin ella todavia puede
    usar una de talla t + 2; el de talla t, en cambio, no tiene otra opcion. Darsela al de talla t
    nunca empeora.

    Coste: O(N + M + 100) por caso.
*/

const int MAX_TALLA = 100;

void resuelveCaso() {
    int N, M;
    cin >> N >> M;
    vector<int> jugadores(MAX_TALLA + 2, 0), equipaciones(MAX_TALLA + 2, 0);
    for (int i = 0; i < N; ++i) { int t; cin >> t; ++jugadores[t]; }
    for (int i = 0; i < M; ++i) { int t; cin >> t; ++equipaciones[t]; }

    int comprar = 0;
    for (int t = 1; t <= MAX_TALLA; ++t) {
        int faltan = jugadores[t];
        int deSuTalla = min(faltan, equipaciones[t]);
        faltan -= deSuTalla;
        int deUnaMas = min(faltan, equipaciones[t + 1]);
        equipaciones[t + 1] -= deUnaMas;
        faltan -= deUnaMas;
        comprar += faltan;
    }
    cout << comprar << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int casos;
    cin >> casos;
    while (casos--) resuelveCaso();
    return 0;
}
