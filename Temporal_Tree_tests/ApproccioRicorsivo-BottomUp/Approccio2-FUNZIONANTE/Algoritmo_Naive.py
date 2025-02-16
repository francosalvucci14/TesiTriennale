from timeit import default_timer as timer
from datetime import timedelta
import networkx as nx

# def dfs_path_check(graph, u, target, current_time, visited):
#     """DFS che verifica se esiste un percorso temporale valido da u a target."""
#     if u == target:
#         return True
#     visited.add((u, current_time))

#     for neighbor in list(graph.successors(u)) + list(graph.predecessors(u)):
#         if neighbor == u:
#             continue

#         if neighbor in [node for node in graph.nodes if graph.in_degree(node) == 0]: #controllo se il vicino è la root
#             if (neighbor, current_time) not in visited:
#                 if dfs_path_check(graph, neighbor, target, current_time, visited):
#                     return True
#             continue

#         neighbor_times = graph.nodes[neighbor].get("timestamp", [])
#         valid_timestamps = [t for t in neighbor_times if t >= current_time]
#         if valid_timestamps:
#             next_time = min(valid_timestamps)
#             if (neighbor, next_time) not in visited:
#                 if dfs_path_check(graph, neighbor, target, next_time, visited):
#                     return True

#     return False

# def is_temporally_connected_v2(graph):
#     """Verifica la connessione temporale in un grafo con NetworkX."""
#     n_nodes = graph.number_of_nodes()
#     if n_nodes <= 1:
#         return True
#     roots = [node for node in graph.nodes if graph.in_degree(node) == 0]
#     if len(roots) != 1:
#         return False
#     root = roots[0]
#     nodes = list(graph.nodes)

#     for u in nodes:
#         for v in nodes:
#             if u != v:
#                 if u == root:
#                     start_time = float('-inf')
#                 else:
#                     start_times = graph.nodes[u].get("timestamp", [])
#                     if not start_times:
#                         return False
#                     start_time = min(start_times)
#                 visited = set()
#                 if not dfs_path_check(graph, u, v, start_time, visited):
#                     return False
#     return True

def dfs_path_check(graph, u, target, current_time, visited):
    """
    DFS che verifica se esiste un percorso temporale valido da u a target in un grafo non diretto.
    """
    if u == target:
        return True
    visited.add((u, current_time))

    for neighbor in graph.neighbors(u):  # Usa neighbors per grafi non diretti
        if neighbor == u:
            continue

        # Controlla se il vicino è la radice (senza timestamp)
        if graph.nodes[neighbor].get("weight") is None:
            if (neighbor, current_time) not in visited:
                if dfs_path_check(graph, neighbor, target, current_time, visited):
                    return True
            continue

        # Controlla i timestamp del vicino
        neighbor_times = graph.nodes[neighbor].get("weight", [])
        valid_timestamps = [t for t in neighbor_times if t >= current_time]
        if valid_timestamps:
            next_time = min(valid_timestamps)
            if (neighbor, next_time) not in visited:
                if dfs_path_check(graph, neighbor, target, next_time, visited):
                    return True

    return False


def is_temporally_connected_v2(graph):
    """
    Verifica la connessione temporale in un grafo non diretto con NetworkX.
    """
    n_nodes = graph.number_of_nodes()
    if n_nodes <= 1:
        return True

    # Identifica la radice (nodo senza timestamp)
    roots = [node for node in graph.nodes if graph.nodes[node].get("weight") is None]
    if len(roots) != 1:
        return False  # Deve esserci esattamente una radice
    root = roots[0]

    nodes = list(graph.nodes)

    for u in nodes:
        for v in nodes:
            if u != v:
                # Determina il timestamp iniziale
                if u == root:
                    start_time = float('-inf')  # La radice può iniziare senza vincoli temporali
                else:
                    start_times = graph.nodes[u].get("weight", [])
                    if not start_times:
                        return False  # Nessun timestamp disponibile per un nodo non radice
                    start_time = min(start_times)

                visited = set()
                if not dfs_path_check(graph, u, v, start_time, visited):
                    return False
    return True


# def is_temporally_connected(graph):
#     """
#     Determina se un albero temporale rappresentato come grafo NetworkX è temporalmente connesso.
    
#     Args:
#     - graph: un grafo orientato NetworkX (DiGraph) con nodi che hanno un attributo 'timestamp'.

#     Returns:
#     - True se il grafo è temporalmente connesso, False altrimenti.
#     """
#     nodes = list(graph.nodes)
    
#     # Controlla la connessione temporale per ogni coppia di nodi
#     for u in nodes:
#         for v in nodes:
#             if u != v:
#                 if not temporal_path_exists(graph, u, v):
#                     return False
#     return True

# def temporal_path_exists(graph, start, target):
#     """
#     Verifica se esiste un cammino temporale tra due nodi in un grafo NetworkX.

#     Args:
#     - graph: un grafo NetworkX (DiGraph) con nodi che hanno un attributo 'timestamp'.
#     - start: nodo iniziale.
#     - target: nodo finale.

#     Returns:
#     - True se esiste un cammino temporale, False altrimenti.
#     """
#     visited = set()
#     queue = [(start, float('-inf'))]  # Nodo iniziale e timestamp minimo

#     while queue:
#         current, last_time = queue.pop(0)
#         if current == target:
#             return True
        
#         # Ottieni il timestamp del nodo corrente
#         current_timestamps = graph.nodes[current].get('timestamp', [])
        
#         for neighbor in graph.successors(current):  # Usa successors() per grafi orientati
#             # Ottieni il timestamp del nodo vicino
#             neighbor_timestamps = graph.nodes[neighbor].get('timestamp', [])
            
#             if not neighbor_timestamps:
#                 # Se il nodo vicino non ha timestamp, lo consideriamo valido
#                 if neighbor not in visited:
#                     visited.add(neighbor)
#                     queue.append((neighbor, last_time))
#             else:
#                 # Verifica se esiste un timestamp valido per il nodo vicino
#                 if any(t >= last_time for t in neighbor_timestamps) and neighbor not in visited:
#                     visited.add(neighbor)
#                     # Usa il prossimo timestamp valido per il nodo vicino
#                     next_time = min(t for t in neighbor_timestamps if t >= last_time)
#                     queue.append((neighbor, next_time))

#     return False

def is_temporally_connected(graph):
    """
    Determina se un albero temporale rappresentato come grafo NetworkX è temporalmente connesso.
    
    Args:
    - graph: un grafo orientato NetworkX (DiGraph) con archi che hanno un attributo 'timestamp'.

    Returns:
    - True se il grafo è temporalmente connesso, False altrimenti.
    """
    nodes = list(graph.nodes)
    
    # Controlla la connessione temporale per ogni coppia di nodi
    for u in nodes:
        for v in nodes:
            if u != v:
                if not temporal_path_exists(graph, u, v):
                    return False
    return True

def temporal_path_exists(graph, start, target):
    """
    Verifica se esiste un cammino temporale tra due nodi in un grafo NetworkX.

    Args:
    - graph: un grafo NetworkX (Graph) con nodi e timestamp come liste.
    - start: nodo iniziale.
    - target: nodo finale.

    Returns:
    - True se esiste un cammino temporale, False altrimenti.
    """
    visited = set()
    queue = [(start, float('-inf'))]  # Nodo iniziale e timestamp minimo

    while queue:
        current, last_time = queue.pop(0)
        if current == target:
            return True
        
        for neighbor in graph.neighbors(current):  # Usa neighbors() per grafi non diretti
            # Ottieni la lista di timestamp del nodo vicino
            timestamps = graph.nodes[neighbor].get('weight', None)
            
            # Caso speciale per la radice o nodi senza timestamp
            if timestamps is None:
                # Qualsiasi arco è valido se il nodo vicino non è visitato
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, last_time))
            else:
                # Verifica i timestamp per nodi con liste di timestamp valide
                if any(t >= last_time for t in timestamps) and neighbor not in visited:
                    visited.add(neighbor)
                    # Usa il timestamp minimo valido come prossimo timestamp
                    next_time = min(t for t in timestamps if t >= last_time)
                    queue.append((neighbor, next_time))
                
    return False

# Esempio di utilizzo
def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.Graph()
    

    ## Aggiungi i nodi e i pesi degli archi entranti
    tree.add_node("A", weight=None)  # Radice senza arco entrante
    tree.add_node("B", weight=[2, 6])
    tree.add_node("C", weight=[6])
    tree.add_node("D", weight=[1, 2, 3, 4, 5,6])
    tree.add_node("E", weight=[6])
    tree.add_node("F", weight=[1, 6])

    # Aggiungi gli archi (parent -> child)
    tree.add_edges_from([
        ("A", "B"),
        ("A", "C"),
        ("A", "F"),
        ("B", "D"),
        ("C", "E")
    ])

    # tree.add_node("A", timestamp=None)  # Radice senza arco entrante
    # tree.add_node("B", timestamp=[1, 2, 3, 4, 5, 6])
    # tree.add_node("C", timestamp=[1,9])
    # tree.add_node("D", timestamp=[2,6])
    # tree.add_node("E", timestamp=[1, 2, 3, 4, 5, 6])
    # tree.add_node("F", timestamp=[2, 6])
    # tree.add_node("G", timestamp=[1,4])
    # tree.add_node("H", timestamp=[10])
    # tree.add_node("I", timestamp=[1])
    # tree.add_node("J", timestamp=[1])
    # tree.add_node("K", timestamp=[1])
    # tree.add_node("L", timestamp=[1])
    # tree.add_node("M", timestamp=[1])
    # tree.add_node("N", timestamp=[1])
    # tree.add_node("O", timestamp=[1])
    # tree.add_node("P", timestamp=[1])

    # # Aggiungi gli archi (parent -> child)
    # tree.add_edges_from([
    #     ("A", "B"),
    #     ("A", "C"),
    #     ("A", "D"),
    #     ("B", "E"),
    #     ("B", "F"),
    #     ("C", "G"),
    #     ("C", "H"),
    #     ("C", "I"),
    #     ("D", "J"),
    #     ("F", "K"),
    #     ("H", "L"),
    #     ("H", "M"),
    #     ("K", "O"),
    #     ("O", "P"),
    #     ("J", "N")
    # ])
    return tree

# Esempio
if __name__ == "__main__":
    start = timer()
    tree = create_tree_with_networkx()
    print(is_temporally_connected(tree))
    print(is_temporally_connected_v2(tree))
    end = timer()
    print("Tempo di esecuzione:", timedelta(seconds=end - start))
