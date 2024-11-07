import random
import matplotlib.pyplot as plt
import numpy as np

def generate_temporal_tree_chain(n, K, time_interval):
    """
    Genera un albero a catena con `n` nodi e assegna a ciascun arco `K` etichette temporali casuali
    prese da un intervallo di valori temporali specificato.

    :param n: numero di nodi nell'albero
    :param K: quantità di etichette temporali per arco
    :param time_interval: tuple con (tempo_min, tempo_max) per l'intervallo temporale
    :return: dizionario che rappresenta l'albero temporale
    """
    tree = {}
    for i in range(n - 1):
        # Ogni nodo `i` punta al nodo successivo `i+1`
        tree[i] = {i + 1: sorted(random.sample(range(time_interval[0], time_interval[1] + 1), K))}
        tree[i + 1] = {}  # Inizializza il nodo successivo nel dizionario

    return tree

def is_temporally_connected(tree):
    """
    Verifica se l'albero è temporalmente connesso usando una BFS temporale.

    :param tree: dizionario dell'albero temporale
    :return: True se l'albero è temporalmente connesso, False altrimenti
    """
    # Inizializza la coda e il set di nodi visitati
    start_node = next(iter(tree))
    queue = [(start_node, 0)]  # (nodo, tempo corrente)
    visited = set()
    visited.add(start_node)

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

def calculate_connectivity_probability(num_trials, n, K, time_interval):
    """
    Calcola la probabilità che un albero a catena sia temporalmente connesso per una data
    quantità di etichette `K` e un intervallo temporale specifico.

    :param num_trials: numero di prove da eseguire
    :param n: numero di nodi nell'albero
    :param K: quantità di etichette temporali per arco
    :param time_interval: tuple con (tempo_min, tempo_max) per l'intervallo temporale
    :return: probabilità che l'albero sia temporalmente connesso
    """
    connected_count = 0

    for _ in range(num_trials):
        # Genera un albero temporale casuale
        tree = generate_temporal_tree_chain(n, K, time_interval)
        # Verifica la connessione temporale
        if is_temporally_connected(tree):
            connected_count += 1

    # Calcola la probabilità di connessione temporale
    return connected_count / num_trials

# Parametri
n = 10               # Numero di nodi
K = 5                # Quantità di etichette temporali per arco
time_interval = (1, n**2)  # Intervallo di valori temporali
num_trials = 1000    # Numero di simulazioni

# Calcola la probabilità di connessione temporale
probabilità = calculate_connectivity_probability(num_trials, n, K, time_interval)
print(f"Probabilità di connessione temporale: {probabilità:.2f}")
