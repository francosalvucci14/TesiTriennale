import random
import heapq
import matplotlib.pyplot as plt

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


def temporal_bfs(u, adj_list, n):
    """Esegui una BFS che esplora i nodi partendo da u, rispettando l'ordine temporale dei timestamp"""
    heap = []
    for neighbor, timestamps in adj_list[u]:
        for timestamp in timestamps:
            heapq.heappush(heap, (timestamp, neighbor))

    visited = set()
    visited.add(u)

    while heap:
        current_time, current_node = heapq.heappop(heap)

        if current_node not in visited:
            visited.add(current_node)

            for neighbor, timestamps in adj_list[current_node]:
                if neighbor not in visited:
                    for timestamp in timestamps:
                        if timestamp >= current_time:
                            heapq.heappush(heap, (timestamp, neighbor))
    
    return visited

def is_temporally_connected_v3(adj_list):
    """Verifica se il grafo è temporaneamente connesso, per ogni coppia di nodi"""
    
    nodes = list(adj_list.keys())
    n = len(nodes)
    
    for u in nodes:
        reachable = temporal_bfs(u, adj_list, n)

        for v in nodes:
            if v != u and v not in reachable:
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
    return is_temporally_connected_v3(labeled_tree)

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
    
    plt.figure(figsize=(10, 6))
    
    for time_range, probabilities in interval_probabilities.items():
        k_values = list(range(1, max_k + 1))
        plt.plot(k_values, probabilities, marker='o', label=f"Intervallo {time_range}")
    
    plt.title("Probabilità di Connessione Temporale al Variare di K e dell'Intervallo Temporale")
    plt.xlabel("Quantità di Etichette per Arco (K)")
    plt.ylabel("Probabilità di Connessione Temporale")
    plt.legend(title="Intervallo Temporale")
    plt.grid(True)
    plt.show()

# Esempio di utilizzo
tree5 = {
    0: [1],
    1: [0, 2],
    2: [1, 3],
    3: [2, 4],
    4: [3]
}

# Parametri
trials = 500
#max_k = random.randint(1,60)  # Range massimo di K
max_k = 60
time_ranges = [(1, 5), (5, 10), (2, 15), (15, 40),(1,150)]

generate_connectivity_graph(tree5, trials, max_k, time_ranges)
