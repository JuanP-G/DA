#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include "IndexPQ.h"

using namespace std;

struct Prio {
    int citas;     // citas vigentes del tema
    int ultimoC;   // instante (numero de evento) de su ultimo C
};

struct Mejor {
    bool operator()(Prio const& a, Prio const& b) const {
        if (a.citas != b.citas) return a.citas > b.citas;  // mas citas va antes
        return a.ultimoC > b.ultimoC;                      // empate: el mas reciente
    }
};

bool resolverCaso() {
    int n;
    if (!(cin >> n)) return false;

    IndexPQ<Prio, Mejor> pq(n);
    unordered_map<string, int> indice;   // tema -> indice
    vector<string> nombre;               // indice -> tema

    for (int t = 0; t < n; ++t) {
        string tipo;
        cin >> tipo;
        if (tipo == "TC") {
            vector<IndexPQ<Prio, Mejor>::Par> podio;
            while (podio.size() < 3 && !pq.empty()
                && pq.top().prioridad.citas > 0) {
                podio.push_back(pq.top());
                pq.pop();
            }
            for (int k = 0; k < (int)podio.size(); ++k)
                cout << k + 1 << ' ' << nombre[podio[k].elem] << '\n';
            for (auto const& p : podio) pq.push(p.elem, p.prioridad);
        }
        else {
            string tema; int m;
            cin >> tema >> m;
            int idx;
            auto it = indice.find(tema);
            if (it == indice.end()) {            // tema nuevo
                idx = nombre.size();
                indice[tema] = idx;
                nombre.push_back(tema);
                pq.push(idx, { 0, -1 });
            }
            else idx = it->second;
            Prio p = pq.priority(idx);
            if (tipo == "C") { p.citas += m; p.ultimoC = t; }
            else p.citas -= m;
            pq.update(idx, p);
        }
    }
    cout << "---\n";
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    while (resolverCaso());
    return 0;
}