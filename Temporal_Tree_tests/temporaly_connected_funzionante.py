import random
from collections import defaultdict, deque

def is_temporally_connected(tree, root):
    # tree: dizionario in cui ogni nodo ha come valore un dizionario di archi
    # root: nodo radice dell'albero
    # Esempio di `tree`: {u: {v: [t1, t2, ...], ...}, ...}

    # Inizializzazione della coda e del set di visitati
    queue = [(root, 0)]  # (nodo, tempo corrente)
    visited = set()
    visited.add(root)

    # BFS temporale
    while queue:
        node, t_curr = queue.pop(0)

        # Esplora tutti i nodi successori di `node`
        for neighbor, times in tree[node].items():
            # Filtra i tempi di attivazione validi (>= t_curr)
            valid_times = [t for t in times if t >= t_curr]
            if valid_times:
                min_valid_time = min(valid_times)  # Ottieni il primo tempo valido
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, min_valid_time))

    # Se tutti i nodi sono stati visitati, l'albero è temporalmente connesso
    return len(visited) == len(tree)


def is_bidirectionally_temporally_connected(tree):
    def bfs_connectivity(tree, start_node):
        reachable_times = defaultdict(set)  # Tracciamo i tempi di arrivo per ogni nodo
        reachable_times[start_node].add(0)  # Il nodo iniziale è raggiungibile al tempo 0
        queue = deque([(start_node, 0)])  # Ogni elemento della coda è una tupla (nodo, tempo)

        while queue:
            node, current_time = queue.popleft()

            for neighbor, times in tree[node].items():
                # Troviamo tutti i tempi validi per raggiungere il nodo successivo
                valid_times = [t for t in times if t >= current_time]
                
                for next_time in valid_times:
                    # Se il tempo di arrivo non è già stato considerato per il vicino
                    if next_time not in reachable_times[neighbor]:
                        reachable_times[neighbor].add(next_time)
                        queue.append((neighbor, next_time))

        # Verifica che tutti i nodi siano stati raggiunti almeno a un tempo valido
        return all(len(times) > 0 for times in reachable_times.values())

    # Scegliamo un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))

    # Controlliamo la connettività nel grafo originale
    if not bfs_connectivity(tree, start_node):
        return False

    # Creiamo il grafo inverso
    reversed_tree = defaultdict(dict)
    for node, neighbors in tree.items():
        for neighbor, times in neighbors.items():
            reversed_tree[neighbor][node] = times

    # Controlliamo la connettività nel grafo inverso
    return bfs_connectivity(reversed_tree, start_node)

tree_connected = {
    "A": {"B": [1, 3, 5], "C": [2, 4, 6], "D": [3, 5, 7]},
    "B": {"E": [4, 6, 8], "F": [5, 7, 9]},
    "C": {"G": [5, 8, 10], "H": [6, 9, 11]},
    "D": {"I": [7, 10, 12], "J": [8, 11, 13]},
    "E": {"K": [9, 12, 14], "L": [10, 13, 15]},
    "F": {"M": [11, 14, 16], "N": [12, 15, 17]},
    "G": {"O": [13, 16, 18], "P": [14, 17, 19]},
    "H": {"Q": [15, 18, 20], "R": [16, 19, 21]},
    "I": {},
    "J": {},
    "K": {},
    "L": {},
    "M": {},
    "N": {},
    "O": {},
    "P": {},
    "Q": {},
    "R": {},
}

tree_not_connected = {
    "A": {"B": [1, 2, 5], "C": [3, 6, 10], "D": [4, 7]},
    "B": {"E": [8, 10], "F": [12]},
    "C": {"G": [7, 8, 15], "H": [10, 11]},
    "D": {"I": [5, 9], "J": [11, 12]},
    "E": {"K": [13, 14], "L": [15]},  # Problema: tempo di attivazione molto elevato
    "F": {
        "M": [9, 10],
        "N": [16],
    },  # Problema: tempo di attivazione non crescente per M
    "G": {"O": [10, 12, 13], "P": [18]},  # Problema: connessione temporale interrotta
    "H": {"Q": [14], "R": [17]},
    "I": {},
    "J": {},
    "K": {},
    "L": {},
    "M": {},
    "N": {},
    "O": {},
    "P": {},
    "Q": {},
    "R": {},
}

graph = {
    'A': {'B': [1, 3, 5], 'C': [2, 4, 6]},
    'B': {'A': [1, 3, 5], 'D': [3, 6, 8], 'E': [5, 7, 9]},
    'C': {'A': [2, 4, 6], 'F': [4, 7, 10]},
    'D': {'B': [3, 6, 8]},
    'E': {'B': [5, 7, 9]},
    'F': {'C': [4, 7, 10]}
}

albero1 = {
    'A': {'B': [2, 3], 'C': [4]},
    'B': {'D': [5], 'E': [6]},
    'C': {'F': [7]},
    'D': {},
    'E': {},
    'F': {}
}

albero3 = {
    'A': {'B': [1,2], 'C': [3,4,6]},
    'B': {'D': [1,3]},
    'C': {'E': [5,6]},
    'D': {},
    'E': {}
}


is_connected = is_temporally_connected(tree_not_connected,'A')
print("L'albero è temporalmente connesso:", is_connected)

is_bidirectionally_connected = is_bidirectionally_temporally_connected(tree_not_connected)
print("L'albero è bidirezionalmente temporalmente connesso:", is_bidirectionally_connected)