from collections import defaultdict
import random

# Creiamo un albero temporale con 150 nodi e 25 etichette su ogni arco
def generate_large_temporally_connected_tree(n):
    tree = defaultdict(dict)
    max_k = 25  # Numero massimo di etichette per arco

    # Costruiamo l'albero binario quasi completo con connessioni temporali casuali
    for i in range(1, n//2 + 1):
        # Aggiungi figlio sinistro
        left_child = 2 * i
        if left_child <= n:
            # Genera fino a 25 etichette temporali casuali per l'arco
            tree[i][left_child] = sorted(random.sample(range(1, 1001), random.randint(1, max_k)))
        
        # Aggiungi figlio destro
        right_child = 2 * i + 1
        if right_child <= n:
            # Genera fino a 25 etichette temporali casuali per l'arco
            tree[i][right_child] = sorted(random.sample(range(1, 1001), random.randint(1, max_k)))
    
    return tree

def is_temporally_connected_v3(tree):
    # Inizializzazione della coda e dei nodi visitati
    start_node = next(iter(tree))  # Prende un nodo qualsiasi come punto di partenza
    queue = [(start_node, 0)]
    visited = set()

    # BFS temporale
    while queue:
        node, t_curr = queue.pop(0)
        if node in visited:
            continue

        visited.add(node)

        # Esplora i successori di `node`
        for neighbor, times in tree[node].items():
            # Trova i tempi validi (>= t_curr)
            valid_times = [t for t in times if t >= t_curr]
            if valid_times:
                min_valid_time = min(valid_times)
                if neighbor not in visited:
                    queue.append((neighbor, min_valid_time))

    # Controllo finale: se tutti i nodi sono stati visitati
    return len(visited) == len(tree)


tree_temporally_connected = {
    "A": {"B": [1, 2, 3], "C": [2, 4]},
    "B": {"D": [3, 5], "E": [4, 6]},
    "C": {"F": [5, 7]},
    "D": {},
    "E": {},
    "F": {},
}

tree_not_connected = {
    'A': {'B': [1, 2, 5], 'C': [3, 6, 10], 'D': [4, 7]},
    'B': {'E': [8, 10], 'F': [12]},
    'C': {'G': [7, 8, 15], 'H': [10, 11]},
    'D': {'I': [5, 9], 'J': [11, 12]},
    'E': {'K': [13, 14], 'L': [15]},  
    'F': {'M': [9, 10], 'N': [16]},   # Problema: tempo di attivazione non crescente per M
    'G': {'O': [10, 12, 13], 'P': [18]}, 
    'H': {'Q': [14], 'R': [17]},
    'I': {}, 'J': {}, 'K': {}, 'L': {}, 'M': {}, 'N': {}, 'O': {}, 'P': {}, 'Q': {}, 'R': {}
}


# for i in range(20):
#     # Genera l'albero con 150 nodi
#     tree_example_large = generate_large_temporally_connected_tree(150)
#     print("----TEST----",i)
#     print("Test con v1:")
#     print(is_temporally_connected_gemini(tree_example_large,1)) 
#     print("Test con v2:")
#     print(is_temporally_connected_v2(tree_example_large)) 
for i in range(20):
    tree_example_large = generate_large_temporally_connected_tree(150)
    print("----TEST----",i)
    print(is_temporally_connected_v3(tree_example_large)) 
print("--------")
#print(is_temporally_connected_v2(tree_temporally_connected))
print(is_temporally_connected_v3(tree_temporally_connected))
#print(is_temporally_connected(tree_temporally_connected))
