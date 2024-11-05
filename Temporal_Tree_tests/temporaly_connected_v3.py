def is_temporally_connected(graph):
    def dfs(node, last_label):
        for neighbor, labels in graph[node].items():
            for label in labels:
                if label >= last_label:
                    if not dfs(neighbor, label):
                        return False
                else:
                    break  # Se incontriamo un'etichetta minore, interrompiamo la visita di quel ramo
        return True

    # Scegli un nodo radice qualsiasi
    root = list(graph.keys())[0]
    return dfs(root, float('-inf'))

def is_temporally_connected_dp(graph, K):
    """Verifica se un grafo con K etichette per arco è temporalmente connesso.

    Args:
        graph: Un dizionario che rappresenta il grafo.
        K: Il numero di etichette per arco.

    Returns:
        True se il grafo è temporalmente connesso, False altrimenti.
    """

    n = len(graph)
    node_to_index = {node: i for i, node in enumerate(graph)}
    dp = [[False] * (K + 1) for _ in range(n)]

    # Caso base: nodi foglia
    for node, neighbors in graph.items():
        node_index = node_to_index[node]
        if not neighbors:
            for j in range(K + 1):
                dp[node_index][j] = True

    # Calcolo dei valori di dp
    for node, neighbors in graph.items():
        node_index = node_to_index[node]
        for neighbor, labels in neighbors.items():
            neighbor_index = node_to_index[neighbor]
            for label in labels:
                for j in range(label, K + 1):
                    dp[node_index][j] |= dp[neighbor_index][j]

    # Verifica se esiste un percorso dalla radice a una foglia
    root_index = node_to_index[list(graph.keys())[0]]
    return any(dp[root_index])

# Esempio di grafo
graph = {
    'A': {'B': [1, 3, 5], 'C': [2, 4, 6]},
    'B': {'D': [3, 6, 8], 'E': [5, 7, 9]},
    'C': {'F': [4, 7, 10]},
    'D': {},
    'E': {},
    'F': {}
}

K = 10

if is_temporally_connected_dp(graph, K):
    print("Il grafo è temporalmente connesso.")
else:
    print("Il grafo non è temporalmente connesso.")

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

K = 3

print(is_temporally_connected(graph))
#print(is_temporally_connected_dp(graph, K))