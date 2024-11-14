import random
import heapq
import matplotlib.pyplot as plt

def print_tree(tree):
    # Definisci la mappatura dei nodi in caratteri
    node_to_char = {i: chr(ord('A') + i) for i in range(len(tree))}
    
    for node, edges in tree.items():
        node_char = node_to_char[node]  # Ottieni il carattere associato al nodo
        for neighbor, timestamps in edges:
            neighbor_char = node_to_char[neighbor]  # Ottieni il carattere del vicino
            print(f"Nodo {node_char} -> Vicino {neighbor_char} con tempi {timestamps}")

def add_labels_to_tree(tree, time_range, k):
    """Aggiunge etichette temporali casuali a ciascun arco di un albero, garantendo che siano uguali per entrambi i nodi dell'arco."""
    labeled_tree = {node: [] for node in tree}
    added_edges = set()

    for node, neighbors in tree.items():
        for neighbor in neighbors:
            # Evita di duplicare l'etichetta per la coppia (node, neighbor)
            if (neighbor, node) not in added_edges:
                # Genera fino a K etichette temporali casuali nell'intervallo specificato
                timestamps = sorted(random.randint(time_range[0], time_range[1]) for _ in range(random.randint(1, k)))
                # Aggiungi le etichette sia per (node -> neighbor) che per (neighbor -> node)
                labeled_tree[node].append((neighbor, timestamps))
                labeled_tree[neighbor].append((node, timestamps))
                added_edges.add((node, neighbor))
    print("TREE-------------------")
    print_tree(labeled_tree)
    return labeled_tree

def temporal_bfs(u, adj_list, n):
    """Esegui una BFS temporale partendo dal nodo u."""
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
    """Verifica se il grafo è temporaneamente connesso."""
    nodes = list(adj_list.keys())
    for u in nodes:
        reachable = temporal_bfs(u, adj_list, len(nodes))
        for v in nodes:
            if v != u and v not in reachable:
                return False
    return True

def run_trial(tree, k, time_range):
    """Esegue un singolo trial per verificare la connessione temporale con un determinato K e intervallo temporale."""
    # Genera l'albero etichettato con timestamp casuali
    labeled_tree = add_labels_to_tree(tree, time_range, k)
    
    # Verifica se il grafo è temporaneamente connesso
    return is_temporally_connected_v3(labeled_tree)

def calculate_probability_per_interval(tree, trials, max_k, time_ranges):
    """Calcola la probabilità di connessione temporale per ciascun intervallo temporale e valore di K."""
    interval_probabilities = {time_range: [] for time_range in time_ranges}
    # Per ogni intervallo temporale
    for time_range in time_ranges:
        for k in range(1, max_k + 1):
            connected_count = 0
            
            for _ in range(trials):
                # A ogni trial, scegli un intervallo casualmente, ma considera solo i risultati per l'intervallo corrente
                chosen_time_range = random.choice(time_ranges)
                
                if chosen_time_range == time_range:
                    if run_trial(tree, k, chosen_time_range):
                        print("TRUE\n")
                        connected_count += 1
            
            # Calcola la probabilità per l'intervallo corrente e K corrente
            probability = connected_count / trials
            interval_probabilities[time_range].append(probability)
    
    return interval_probabilities

def generate_connectivity_graph(tree, trials, max_k, time_ranges):
    """Genera un grafico della probabilità di connessione temporale al variare di K e per ogni intervallo temporale."""
    interval_probabilities = calculate_probability_per_interval(tree, trials, max_k, time_ranges)
    
    plt.figure(figsize=(10, 6))
    
    # Grafico per ogni intervallo temporale
    for time_range, probabilities in interval_probabilities.items():
        k_values = list(range(1, max_k + 1))
        plt.plot(k_values, probabilities, marker='o', label=f"Intervallo {time_range}")
    
    # Configurazione del grafico
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
trials = 1000
max_k = 5  # Range massimo di K
time_ranges = [(1,1),(1, 5), (5, 10), (2, 15), (15, 40)]  # Lista di intervalli possibili
generate_connectivity_graph(tree5, trials, max_k, time_ranges)
