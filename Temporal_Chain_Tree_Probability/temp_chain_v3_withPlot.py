import random
import matplotlib.pyplot as plt
import numpy as np

def generate_temporal_tree_labels(tree, max_K, time_interval):
    """
    Assegna etichette temporali casuali agli archi di un albero passato come input.
    
    :param tree: dizionario che rappresenta l'albero
    :param K: quantità di etichette temporali per arco
    :param time_interval: tuple con (tempo_min, tempo_max) per l'intervallo temporale
    :return: dizionario dell'albero con etichette temporali assegnate agli archi
    """
    # # Calcola la lunghezza dell'intervallo temporale
    # interval_range = range(time_interval[0], time_interval[1] + 1)
    # max_labels = min(K, len(interval_range))  # Assicura che non superi la lunghezza dell'intervallo

    # labeled_tree = {}
    # for node, neighbors in tree.items():
    #     labeled_tree[node] = {}
    #     for neighbor in neighbors:
    #         # Genera un massimo di `max_labels` etichette casuali nell'intervallo specificato
    #         labeled_tree[node][neighbor] = sorted(random.sample(interval_range, max_labels))

    # return labeled_tree
    # Calcola la lunghezza dell'intervallo temporale
    interval_range = range(time_interval[0], time_interval[1] + 1)

    labeled_tree = {}
    for node, neighbors in tree.items():
        labeled_tree[node] = {}
        for neighbor in neighbors:
            # Genera un numero casuale di etichette tra 1 e `max_K`
            K = random.randint(1, max_K)
            # Seleziona `K` etichette casuali nell'intervallo specificato
            labeled_tree[node][neighbor] = sorted(random.sample(interval_range, min(K, len(interval_range))))

    return labeled_tree

def is_temporally_connected(tree):
    """
    Verifica se l'albero è temporalmente connesso usando una BFS temporale.
    
    :param tree: dizionario dell'albero temporale
    :return: True se l'albero è temporalmente connesso, False altrimenti
    """
    start_node = next(iter(tree))
    queue = [(start_node, 0)]  # (nodo, tempo corrente)
    visited = set()
    visited.add(start_node)

    while queue:
        node, t_curr = queue.pop(0)
        
        for neighbor, times in tree[node].items():
            valid_times = [t for t in times if t >= t_curr]
            if valid_times:
                min_valid_time = min(valid_times)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, min_valid_time))

    return len(visited) == len(tree)

def calculate_connectivity_probability(tree, num_trials, K, time_interval):
    """
    Calcola la probabilità che un albero sia temporalmente connesso per una data
    quantità di etichette `K` e un intervallo temporale specifico.
    
    :param tree: dizionario dell'albero
    :param num_trials: numero di prove da eseguire
    :param K: quantità di etichette temporali per arco
    :param time_interval: tuple con (tempo_min, tempo_max) per l'intervallo temporale
    :return: probabilità che l'albero sia temporalmente connesso
    """
    connected_count = 0

    for _ in range(num_trials):
        labeled_tree = generate_temporal_tree_labels(tree, K, time_interval)
        if is_temporally_connected(labeled_tree):
            connected_count += 1

    return connected_count / num_trials

# Definisci manualmente la struttura dell'albero a catena
tree = {
    0: [1],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [7],
    7: [8],
    8: [9],
    9:[]
}

# Parametri della simulazione
n = len(tree)               # Numero di nodi nell'albero a catena
num_trials = 500            # Numero di simulazioni per ogni configurazione
K_values = range(1, 10)     # Diverse quantità di etichette per arco
time_intervals = [(1, 5), (5, 10), (2, 15), (15, 40)]  # Diversi intervalli temporali

# Risultati da raccogliere per il plot
results = {}

# Esegui la simulazione per ogni combinazione di K e intervallo temporale
for time_interval in time_intervals:
    probabilities = []
    for K in K_values:
        prob = calculate_connectivity_probability(tree, num_trials, K, time_interval)
        probabilities.append(prob)
    results[time_interval] = probabilities

# Plot dei risultati
plt.figure(figsize=(10, 6))
for time_interval, probabilities in results.items():
    plt.plot(K_values, probabilities, marker='o', label=f"Intervallo {time_interval}")

# Configura il plot
plt.title("Probabilità di Connessione Temporale al Variare di K e dell'Intervallo Temporale")
plt.xlabel("Quantità di Etichette per Arco (K)")
plt.ylabel("Probabilità di Connessione Temporale")
plt.legend(title="Intervallo Temporale")
plt.grid(True)
plt.show()
