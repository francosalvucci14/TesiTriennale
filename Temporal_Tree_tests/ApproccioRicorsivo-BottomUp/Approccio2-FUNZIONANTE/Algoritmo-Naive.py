from timeit import default_timer as timer
from datetime import timedelta
import networkx as nx

def dfs_path_check(graph, u, target, current_time, visited):
    """DFS che verifica se esiste un percorso temporale valido da u a target."""
    if u == target:
        return True
    visited.add((u, current_time))

    for neighbor in list(graph.successors(u)) + list(graph.predecessors(u)):
        if neighbor == u:
            continue

        if neighbor in [node for node in graph.nodes if graph.in_degree(node) == 0]: #controllo se il vicino è la root
            if (neighbor, current_time) not in visited:
                if dfs_path_check(graph, neighbor, target, current_time, visited):
                    return True
            continue

        neighbor_times = graph.nodes[neighbor].get("weight", [])
        valid_timestamps = [t for t in neighbor_times if t >= current_time]
        if valid_timestamps:
            next_time = min(valid_timestamps)
            if (neighbor, next_time) not in visited:
                if dfs_path_check(graph, neighbor, target, next_time, visited):
                    return True

    return False

def is_temporally_connected_v2(graph):
    """Verifica la connessione temporale in un grafo con NetworkX."""
    n_nodes = graph.number_of_nodes()
    if n_nodes <= 1:
        return True
    roots = [node for node in graph.nodes if graph.in_degree(node) == 0]
    if len(roots) != 1:
        return False
    root = roots[0]
    nodes = list(graph.nodes)

    for u in nodes:
        for v in nodes:
            if u != v:
                if u == root:
                    start_time = float('-inf')
                else:
                    start_times = graph.nodes[u].get("weight", [])
                    if not start_times:
                        return False
                    start_time = min(start_times)
                visited = set()
                if not dfs_path_check(graph, u, v, start_time, visited):
                    return False
    return True

# Esempio di utilizzo
def create_tree_with_networkx():
    # Crea un grafo diretto
    tree = nx.DiGraph()

    # Aggiungi i nodi e i pesi degli archi entranti
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
    

    return tree

# Esempio
if __name__ == "__main__":
    start = timer()
    tree = create_tree_with_networkx()
    print(is_temporally_connected_v2(tree))
    end = timer()
    print("Tempo di esecuzione:", timedelta(seconds=end - start))
