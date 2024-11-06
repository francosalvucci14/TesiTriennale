from collections import deque, defaultdict
import random
def generate_chain_tree(n, K, interval):
    # Funzione per generare un albero a catena con K etichette casuali sugli archi
    tree = {}
    for i in range(n - 1):
        labels = sorted(random.sample(range(1, interval + 1), K))  # K etichette
        tree[f'N{i}'] = {f'N{i+1}': labels}
    tree[f'N{n-1}'] = {}  # L'ultimo nodo non ha archi in avanti
    return tree
def bfs_connectivity(tree, start_node):
    # Funzione che esegue la BFS per determinare la connettività temporale
    reachable_times = defaultdict(set)
    reachable_times[start_node].add(0)
    queue = deque([(start_node, 0)])

    while queue:
        node, current_time = queue.popleft()
        for neighbor, times in tree[node].items():
            valid_times = [t for t in times if t >= current_time]
            for next_time in valid_times:
                if next_time not in reachable_times[neighbor]:
                    reachable_times[neighbor].add(next_time)
                    queue.append((neighbor, next_time))
    return reachable_times

def is_temporally_connected(tree):
    # Controlliamo la connettività temporale in entrambe le direzioni
    start_node = list(tree.keys())[0]  # Prendiamo un nodo di partenza arbitrario

    # Controlliamo la connettività temporale dal nodo di partenza
    reachable_times_from_start = bfs_connectivity(tree, start_node)
    if len(reachable_times_from_start) != len(tree):
        return False

    # Creiamo l'albero invertito (per la connettività temporale in direzione inversa)
    reversed_tree = defaultdict(dict)
    for node, neighbors in tree.items():
        for neighbor, times in neighbors.items():
            reversed_tree[neighbor][node] = times

    # Controlliamo la connettività temporale in direzione inversa
    reachable_times_from_end = bfs_connectivity(reversed_tree, start_node)
    if len(reachable_times_from_end) != len(tree):
        return False

    return True

def estimate_connectivity_probability(n, K, interval, simulations=1000):
    connected_count = 0
    for _ in range(simulations):
        tree = generate_chain_tree(n, K, interval)
        print(tree)
        if is_temporally_connected(tree):
            connected_count += 1
    return connected_count / simulations

# Parametri
n = 10  # Lunghezza della catena
K = 4   # Numero di etichette per arco
interval = 15  # Intervallo delle etichette temporali
simulations = 1000  # Numero di simulazioni per stima probabilità

probability = estimate_connectivity_probability(n, K, interval, simulations)
print(f'Probabilità di connettività temporale: {probability:.2f}')

