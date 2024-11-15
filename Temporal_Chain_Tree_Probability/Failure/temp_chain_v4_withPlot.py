import random
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}  # Dizionario che mappa i nodi vicini alle liste di etichette temporali

    def add_edge(self, neighbor, times):
        self.edges[neighbor] = times

def generate_temporal_labels_for_edges(tree, max_K, time_interval):
    """
    Assegna un numero casuale di etichette temporali a ciascun arco, 
    con etichette scelte casualmente da un intervallo definito.
    
    :param tree: dizionario che rappresenta l'albero di oggetti Node
    :param max_K: numero massimo di etichette temporali per arco
    :param time_interval: intervallo temporale come tuple (tempo_min, tempo_max)
    :return: l'albero con etichette temporali assegnate agli archi
    """
    interval_range = range(time_interval[0], time_interval[1] + 1)

    for node in tree.values():
        for neighbor in node.edges.keys():
            # Numero casuale di etichette per l'arco
            K = random.randint(1, max_K)
            
            # Genera un set di etichette casuali per l'arco, prese dall'intervallo
            times = sorted(random.sample(interval_range, min(K, len(interval_range))))
            
            # Aggiungi l'arco con le etichette temporali generate
            node.add_edge(neighbor, times)

def edge_stream_representation(root):
    """Genera la rappresentazione dell'albero come una sequenza di archi temporali ordinata"""
    edges = []

    def dfs(node):
        for neighbor, times in node.edges.items():
            for time in times:
                edges.append((node, neighbor, time))  # (u, v, t)
            # Recursive DFS call to process children
            for neighbor_node in node.edges:
                dfs(neighbor_node)

    dfs(root)
    
    # Ordina gli archi in base al valore delle etichette temporali
    edges.sort(key=lambda x: x[2])  # ordinamento in base al valore dell'etichetta temporale
    return edges

def check_temporal_connectivity(root):
    """Verifica se l'albero è temporalmente connesso"""
    
    # Otteniamo la rappresentazione in edge stream
    edges = edge_stream_representation(root)
    
    # Troviamo il massimo tra tutte le etichette temporali
    max_time = max(time for _, _, time in edges)
    
    # Caso base: Se tutte le etichette sono uguali, ritorna True
    if all(time == edges[0][2] for _, _, time in edges):
        return True
    
    # Verifica la connettività temporale tramite Binary Search
    for u, v, time in edges:
        if time >= max_time:
            return False  # Se troviamo un arco con tempo >= al massimo, ritorniamo False
    
    # Se nessun arco ha tempi >= al massimo, allora è connesso
    return True

def calculate_connectivity_probability(tree, num_trials, max_K, time_interval):
    """
    Calcola la probabilità che un albero sia temporalmente connesso per una data
    quantità di etichette `K` e un intervallo temporale specifico.
    
    :param tree: dizionario dell'albero di oggetti Node
    :param num_trials: numero di prove da eseguire
    :param max_K: massimo numero di etichette temporali per arco
    :param time_interval: tuple con (tempo_min, tempo_max) per l'intervallo temporale
    :return: probabilità che l'albero sia temporalmente connesso
    """
    connected_count = 0

    for _ in range(num_trials):
        # Aggiungi etichette temporali casuali agli archi
        generate_temporal_labels_for_edges(tree, max_K, time_interval)
        # Controlla se l'albero è temporalmente connesso
        if check_temporal_connectivity(tree[0]):
            connected_count += 1

    return connected_count / num_trials

# Definisci manualmente la struttura dell'albero con oggetti Node
nodeA = Node('A')
nodeB = Node('B')
nodeC = Node('C')
nodeD = Node('D')
nodeE = Node('E')

# Creazione delle connessioni (senza etichette temporali)
nodeA.edges = {nodeB: [], nodeC: []}
nodeB.edges = {nodeD: []}
nodeC.edges = {nodeE: []}
nodeD.edges = {}
nodeE.edges = {}

# Creazione di un dizionario con i nodi
tree = {
    0: nodeA,
    1: nodeB,
    2: nodeC,
    3: nodeD,
    4: nodeE
}

# Parametri della simulazione
n = len(tree)               # Numero di nodi nell'albero
num_trials = 500            # Numero di simulazioni per ogni configurazione
max_K = 1               # Quantità massima di etichette per arco
# Prova a variare l'intervallo temporale e il numero di etichette
time_intervals = [(1,3),(1, 100), (5, 50), (10, 100), (15, 150)]

# Risultati da raccogliere per il plot
results = {}

# Esegui la simulazione per ogni combinazione di intervallo temporale
for time_interval in time_intervals:
    probabilities = []
    prob = calculate_connectivity_probability(tree, num_trials, max_K, time_interval)
    probabilities.append(prob)
    print(probabilities)
    results[time_interval] = probabilities

# Plot dei risultati
plt.figure(figsize=(10, 6))
for time_interval, probabilities in results.items():
    plt.plot([max_K], probabilities, marker='o', label=f"Intervallo {time_interval}")

# Configura il plot
plt.title("Probabilità di Connessione Temporale al Variare dell'Intervallo Temporale")
plt.xlabel("Quantità di Etichette per Arco (K)")
plt.ylabel("Probabilità di Connessione Temporale")
plt.legend(title="Intervallo Temporale")
plt.grid(True)
plt.show()
