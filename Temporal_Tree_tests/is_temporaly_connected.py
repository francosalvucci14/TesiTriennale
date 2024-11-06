import random
from collections import defaultdict, deque

# Algoritmo 1, parte da nodo root e visita tutti i nodi con tempo maggiore o uguale a quello corrente
def is_temporally_connected_1(tree, root):
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

# Algoritmo 2 partendo da nodo scelto casualmente

def is_temporally_connected_2(tree):
    # Seleziona un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))
    queue = deque([(start_node, 0)])  # Coda per BFS temporale, inizialmente al tempo 0
    visited = set()

    # Esegui la BFS temporale
    while queue:
        node, t_curr = queue.popleft()
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

# Algoritmo 3

def is_temporally_connected_3(tree):
    # Seleziona un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))

    # Crea un dizionario per tenere traccia dei nodi visitati
    visited = set()
    queue = deque([(start_node, 0)])  # Coda per BFS temporale, inizialmente al tempo 0

    # Esegui la BFS temporale
    while queue:
        node, t_curr = queue.popleft()
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

# Algoritmo 4
def is_temporally_connected_4(tree):
    # Seleziona un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))

    # Crea una coda per BFS e un set per i nodi visitati
    queue = deque([(start_node, 0)])  # Nodo e tempo iniziale
    visited = set()
    times = {node: float('inf') for node in tree}  # Inizializza i tempi a infinito
    times[start_node] = 0  # Imposta il tempo di partenza a 0

    # Esegui la BFS temporale
    while queue:
        node, t_curr = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        # Esplora i successori di `node`
        for neighbor, activation_times in tree[node].items():
            # Trova il tempo minimo valido (>= t_curr)
            valid_times = [t for t in activation_times if t >= t_curr]
            if valid_times:
                next_time = min(valid_times)
                # Aggiorna il tempo di attivazione se è migliore
                if next_time < times[neighbor]:
                    times[neighbor] = next_time
                    queue.append((neighbor, next_time))

    # Controllo finale: se tutti i nodi sono stati visitati
    return len(visited) == len(tree)

# Algoritmo 5, approccio top-down e bottom-up
def is_temporally_connected_5(tree):
    # Seleziona un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))
    
    # Funzione per esplorazione top-down
    def top_down(node, current_time, visited):
        if node in visited:
            return
        visited.add(node)

        # Esplora i successori
        for neighbor, activation_times in tree[node].items():
            valid_times = [t for t in activation_times if t >= current_time]
            if valid_times:
                next_time = min(valid_times)
                top_down(neighbor, next_time, visited)

    # Funzione per esplorazione bottom-up
    def bottom_up(node, reachable_times):
        for neighbor in tree[node]:
            bottom_up(neighbor, reachable_times)
            # Aggiungi i tempi di attivazione dal vicino
            reachable_times.update(reachable_times[neighbor])

    visited = set()
    # Top-down per visitare tutti i nodi
    top_down(start_node, 0, visited)

    if len(visited) < len(tree):
        return False  # Se non tutti i nodi sono visitati, non è connesso

    # Bottom-up per verificare la connessione temporale
    reachable_times = {node: set() for node in tree}
    bottom_up(start_node, reachable_times)

    # Controlla se ogni nodo può raggiungere ogni altro nodo
    for node in tree:
        if not reachable_times[node]:
            return False  # Se un nodo non ha tempi validi, non è connesso

    return True

# Algoritmo 6, con DP

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