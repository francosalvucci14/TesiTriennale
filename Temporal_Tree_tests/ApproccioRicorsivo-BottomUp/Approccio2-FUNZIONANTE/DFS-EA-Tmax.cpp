#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <climits>
#include <cstdlib>
#include <chrono>
using namespace std::chrono;

struct Node {
    char value;
    std::vector<int> weight;
    Node* left;
    Node* right;

    Node(char val, std::vector<int> wt = {}) : value(val), weight(wt), left(nullptr), right(nullptr) {}
};

int binary_search(const std::vector<int>& arr, int target) {
    if (arr.empty()) return -1; // Verifica array vuoto
    int left = 0, right = arr.size() - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] >= target) {
            result = mid;
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return result != -1 ? arr[result] : -1;
}

int binary_search_leq(const std::vector<int>& arr, int target) {
    if (arr.empty()) return -1; // Verifica array vuoto
    int left = 0, right = arr.size() - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] <= target) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return result != -1 ? arr[result] : -1;
}

std::pair<int, int> dfs_EA_tmax_spazio1(Node* root) {
    if (!root) return {INT_MIN, INT_MAX};
    if (!root->left && !root->right) {
        if (root->weight.empty()) {
            std::cerr << "Errore: Nodo " << root->value << " ha una lista di pesi vuota!\n";
            exit(EXIT_FAILURE);
        }
        std::cout << "EA e tempo max visita per il sottoalbero radicato nel nodo " << root->value << " (foglia): (" << root->weight.front() << ", " << root->weight.back() << ")\n";
        return {root->weight.front(), root->weight.back()};
    }

    auto [min_sx, max_sx] = root->left ? dfs_EA_tmax_spazio1(root->left) : std::make_pair(INT_MIN, INT_MAX);
    auto [min_dx, max_dx] = root->right ? dfs_EA_tmax_spazio1(root->right) : std::make_pair(INT_MIN, INT_MAX);

    int EA = std::max(min_sx, min_dx);
    int t_max_visita = std::min(max_sx, max_dx);
    std::cout << "EA e tempo max visita per il sottoalbero radicato nel nodo " << root->value << " (nodo interno): (" << EA << ", " << t_max_visita << ")\n";

    int k = binary_search(root->weight, EA);
    int nextTimeMax = binary_search_leq(root->weight, t_max_visita);

    if (k == -1 || nextTimeMax == -1) {
        std::cerr << "Errore: EA o tempo max visita non trovati per il nodo " << root->value << "\n";
        exit(EXIT_FAILURE);
    }

    int minTime = std::min(t_max_visita, nextTimeMax);
    return {k, minTime};
}

std::map<char, std::pair<int, int>> dfs_EA_tmax_spazioN(Node* root) {
    if (!root) return {};

    if (!root->left && !root->right) {
        if (root->weight.empty()) {
            std::cerr << "Errore: Nodo " << root->value << " ha una lista di pesi vuota!\n";
            exit(EXIT_FAILURE);
        }
        std::cout << "EA e tempo max visita per il sottoalbero radicato nel nodo " << root->value << " (foglia): (" << root->weight.front() << ", " << root->weight.back() << ")\n";
        return {{root->value, {root->weight.front(), root->weight.back()}}};
    }

    std::map<char, std::pair<int, int>> sottoalberi;

    if (root->left) {
        auto left_result = dfs_EA_tmax_spazioN(root->left);
        sottoalberi.insert(left_result.begin(), left_result.end());
    }

    if (root->right) {
        auto right_result = dfs_EA_tmax_spazioN(root->right);
        sottoalberi.insert(right_result.begin(), right_result.end());
    }

    int ea_sx = root->left ? sottoalberi[root->left->value].first : INT_MIN;
    int t_max_sx = root->left ? sottoalberi[root->left->value].second : INT_MAX;
    int ea_dx = root->right ? sottoalberi[root->right->value].first : INT_MIN;
    int t_max_dx = root->right ? sottoalberi[root->right->value].second : INT_MAX;

    int EA = std::max(ea_sx, ea_dx);
    int t_max_visita = std::min(t_max_sx, t_max_dx);
    std::cout << "EA e tempo max visita per il sottoalbero radicato nel nodo " << root->value << " (nodo interno): (" << EA << ", " << t_max_visita << ")\n";

    int k = binary_search(root->weight, EA);
    int nextTimeMax = binary_search_leq(root->weight, t_max_visita);

    int minTime = std::min(t_max_visita, nextTimeMax);
    sottoalberi[root->value] = {k, minTime};

    return sottoalberi;
}

bool algoritmo(Node* root) {
    std::cout << "Versione con spazio O(1)\n";

    auto [ea_sx, t_max_sx] = root->left ? dfs_EA_tmax_spazio1(root->left) : std::make_pair(INT_MIN, INT_MAX);
    auto [ea_dx, t_max_dx] = root->right ? dfs_EA_tmax_spazio1(root->right) : std::make_pair(INT_MIN, INT_MAX);

    std::cout << "------------------------------------------------\n";
    std::cout << "EA e tempo max visita sx della radice " << root->value << ": (" << ea_sx << ", " << t_max_sx << ")\n";
    std::cout << "EA e tempo max visita dx della radice " << root->value << ": (" << ea_dx << ", " << t_max_dx << ")\n";

    return ea_sx <= t_max_dx && ea_dx <= t_max_sx;
}

bool algoritmo2(Node* root) {
    std::cout << "Versione con spazio O(n)\n";

    auto risultati = dfs_EA_tmax_spazioN(root);

    int ea_sx = root->left ? risultati[root->left->value].first : INT_MIN;
    int t_max_sx = root->left ? risultati[root->left->value].second : INT_MAX;
    int ea_dx = root->right ? risultati[root->right->value].first : INT_MIN;
    int t_max_dx = root->right ? risultati[root->right->value].second : INT_MAX;

    std::cout << "------------------------------------------------\n";
    std::cout << "EA e tempo max visita sx della radice " << root->value << ": (" << ea_sx << ", " << t_max_sx << ")\n";
    std::cout << "EA e tempo max visita dx della radice " << root->value << ": (" << ea_dx << ", " << t_max_dx << ")\n";

    return ea_sx <= t_max_dx && ea_dx <= t_max_sx;
}

int main() {
    // Node* root = new Node('A');
    // root->left = new Node('B', {2, 6});
    // root->right = new Node('C', {6});
    // root->left->left = new Node('D', {1, 2, 3, 4, 5,6});
    // root->right->right = new Node('E', {6});
    Node* root = new Node('A');
    root->left = new Node('B', {2, 3, 5, 8});
    root->right = new Node('C', {3, 5});
    root->left->left = new Node('D', {1, 4, 5, 6});
    root->left->right = new Node('E', {1, 5, 9});
    root->right->left = new Node('F', {1,2,5});
    root->right->right = new Node('G', {2, 5});
    root->left->left->left = new Node('H', {2, 4});
    root->right->left->right = new Node('I', {1, 11});

    auto start = high_resolution_clock::now();
    std::cout << "Albero temporalmente connesso? : " << (algoritmo(root) ? "Risposta : Albero Temporalmente Connesso" : "Fatte da Nculo") << "\n";
    std::cout << "\n";
    std::cout << "Albero temporalmente connesso? : " << (algoritmo2(root) ? "Risposta : Albero Temporalmente Connesso" : "Fatte da Nculo") << "\n";
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);

    std::cout << "Time taken by function: "
         << duration.count() << " microseconds";
    return 0;
}