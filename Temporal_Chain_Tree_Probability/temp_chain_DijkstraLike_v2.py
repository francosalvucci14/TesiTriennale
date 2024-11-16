import random
import heapq
import matplotlib.pyplot as plt
from collections import defaultdict
from bisect import bisect_left
from timeit import default_timer as timer
from datetime import timedelta

def add_labels_to_tree(tree, time_range, k):
    """Aggiunge etichette temporali casuali agli archi dell'albero."""
    labeled_tree = {}
    
    for node, neighbors in tree.items():
        labeled_tree[node] = []
        for neighbor in neighbors:
            # Controlla che k non sia maggiore del numero di elementi distinti nell'intervallo
            max_k = min(k, time_range[1] - time_range[0] + 1)
            
            # Genera max_k timestamp casuali nell'intervallo specificato
            timestamps = sorted(random.sample(range(time_range[0], time_range[1] + 1), max_k))
            
            # Aggiunge l'etichetta sia al nodo corrente che al suo vicino
            labeled_tree[node].append((neighbor, timestamps))
            
            # Aggiorna anche il vicino per mantenere simmetria nell'albero
            if neighbor in labeled_tree:
                # Cerca il nodo corrente tra i vicini del vicino e aggiorna le etichette
                for i, (nbr, _) in enumerate(labeled_tree[neighbor]):
                    if nbr == node:
                        labeled_tree[neighbor][i] = (node, timestamps)
                        break
                else:
                    labeled_tree[neighbor].append((node, timestamps))
            else:
                labeled_tree[neighbor] = [(node, timestamps)]
                
    return labeled_tree


def temporal_bfs_memo(u, adj_list, memo):
    """Esegue una BFS temporale con memorizzazione (memoization)"""
    # Coda di priorità (heap), contiene tuple (timestamp, nodo)
    heap = []
    heapq.heappush(heap, (0, u))  # Partiamo da u con il timestamp minimo

    # Inizializza il dizionario memo per u
    if u not in memo:
        memo[u] = {u: 0}
    visited = memo[u]

    while heap:
        current_time, current_node = heapq.heappop(heap)

        # Esplora i vicini di current_node
        for neighbor, timestamps in adj_list[current_node]:
            # Trova il primo timestamp >= current_time
            idx = bisect_left(timestamps, current_time)
            if idx < len(timestamps):
                next_time = timestamps[idx]
                # Se il vicino non è stato visitato o se troviamo un percorso temporale migliore
                if neighbor not in visited or next_time < visited.get(neighbor, float('inf')):
                    visited[neighbor] = next_time
                    heapq.heappush(heap, (next_time, neighbor))

    # Restituisce i nodi raggiungibili
    return set(visited.keys())

def is_temporally_connected_v5(adj_list):
    """Verifica se il grafo è temporaneamente connesso usando la memorizzazione dei percorsi."""
    nodes = list(adj_list.keys())
    memo = defaultdict(dict)  # Dato che vogliamo lanciare BFS per ogni nodo

    for u in nodes:
        reachable = temporal_bfs_memo(u, adj_list, memo)
        # Se un nodo non è raggiungibile da u, il grafo non è connesso temporalmente
        if len(reachable) != len(nodes):
            return False
    return True

def run_trial(tree, k, time_range):
    """Esegue un singolo trial per verificare la connessione temporale con un determinato K e intervallo temporale."""
    time_A = time_range[0]
    time_B = time_range[1]
    if time_A == time_B:
        return True
    
    # Genera l'albero etichettato con timestamp casuali
    labeled_tree = add_labels_to_tree(tree, time_range, k)

    # Verifica se il grafo è temporaneamente connesso
    return is_temporally_connected_v5(labeled_tree)

def calculate_probability_per_interval(tree, trials, max_k, time_ranges):
    """Calcola la probabilità di connessione temporale per ciascun intervallo temporale e valore di K."""
    interval_probabilities = {time_range: [] for time_range in time_ranges}
    
    for time_range in time_ranges:
        for k in range(1, max_k + 1):
            connected_count = 0
            
            for _ in range(trials):
                chosen_time_range = random.choice(time_ranges)
                
                if chosen_time_range == time_range:
                    if run_trial(tree, k, chosen_time_range):
                        connected_count += 1
        

            probability = connected_count / trials
            
            # Se l'intervallo è [X, X], la probabilità deve essere 1
            time_A = time_range[0]
            time_B = time_range[1]
            if time_A == time_B:
                probability = 1

            interval_probabilities[time_range].append(probability)
    
    return interval_probabilities

def generate_connectivity_graph(tree, trials, max_k, time_ranges):
    """Genera un grafico della probabilità di connessione temporale al variare di K e per ogni intervallo temporale."""
    interval_probabilities = calculate_probability_per_interval(tree, trials, max_k, time_ranges)
    
    plt.figure(figsize=(15, 10))
    
    for time_range, probabilities in interval_probabilities.items():
        k_values = list(range(1, max_k + 1))
        plt.plot(k_values, probabilities, marker='o', label=f"Intervallo {time_range}")
    
    plt.title("Probabilità di Connessione Temporale al Variare di K e dell'Intervallo Temporale")
    plt.xlabel("Quantità di Etichette per Arco (K)")
    plt.ylabel("Probabilità di Connessione Temporale")
    plt.legend(title="Intervallo Temporale")
    plt.grid(True)
    #plt.show()
    plt.savefig('temp_chain_DijkstraLike_v2.png')  # Salva il plot

def generate_random_intervals(num_intervals, min_value, max_value):
  """
  Genera un numero specificato di intervalli casuali entro un range definito.

  Args:
    num_intervals: Numero di intervalli da generare.
    min_value: Valore minimo per gli estremi degli intervalli.
    max_value: Valore massimo per gli estremi degli intervalli.

  Returns:
    Lista di tuple rappresentanti gli intervalli generati casualmente.
  """

  random_intervals = []
  for _ in range(num_intervals):
    start = random.randint(min_value, max_value)
    end = random.randint(start, max_value)
    random_intervals.append((start, end))

  return random_intervals

# Esempio di utilizzo
tree5 = {
    0: [1],
    1: [0, 2],
    2: [1]
}

tree15 = {
    0: [1],
    1: [0, 2],
    2: [1, 3],
    3: [2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [7, 9],
    9: [8, 10],
    10: [9, 11],
    11: [10, 12],
    12: [11, 13],
    13: [12, 14],
    14: [13]
}

# Parametri
trials = 10000
#max_k = random.randint(1,60)  # Range massimo di K
max_k = 150
#time_ranges = [(1, 5), (5, 10), (2, 15), (15, 40),(1,150)]

randomized_intervals = generate_random_intervals(8,1,10)

start = timer()
generate_connectivity_graph(tree5, trials, max_k, randomized_intervals)    
end = timer()
print(timedelta(seconds=end-start))