from collections import deque,defaultdict
import random
def transform_tree_to_graph(tree):
    """
    Trasforma un albero in un grafo non diretto.
    Ogni arco dell'albero viene duplicato nella direzione opposta.
    """
    graph = {}
    
    # Per ogni nodo nell'albero
    for node, neighbors in tree.items():
        if node not in graph:
            graph[node] = {}
        
        # Aggiungi i nodi vicini (e i tempi di attivazione)
        for neighbor, times in neighbors.items():
            if neighbor not in graph:
                graph[neighbor] = {}
            graph[node][neighbor] = times
            
            # Aggiungi l'arco anche nella direzione opposta
            graph[neighbor][node] = times
    
    return graph


# def is_temporally_connected(graph):
#     """
#     Verifica se un grafo è temporalmente connesso.
#     Parte da un nodo casuale e applica la BFS su un grafo non diretto.
#     """
#     # Scegli un nodo casuale come punto di partenza
#     start_node = random.choice(list(graph.keys()))
#     queue = [(start_node, 0)]  # (nodo, tempo corrente)
#     visited = set()
#     visited.add(start_node)

#     while queue:
#         node, t_curr = queue.pop(0)

#         # Esplora tutti i nodi successori di `node`
#         for neighbor, times in graph[node].items():
#             valid_times = [t for t in times if t >= t_curr]
#             valid_times_rev = [t for t in times if t <= t_curr]
#             if valid_times or valid_times_rev:
#                 min_valid_time = min(valid_times)  # Ottieni il primo tempo valido
#                 if neighbor not in visited:
#                     visited.add(neighbor)
#                     queue.append((neighbor, min_valid_time))
#             else:
#                 return False

#     # Se tutti i nodi sono stati visitati, il grafo è temporalmente connesso
#     return len(visited) == len(graph)


def bfs_check(graph, start, direction="forward"):
    """
    Esegue una BFS su un grafo non diretto con un controllo temporale.
    La direzione indica se i tempi devono essere crescenti ("forward") o decrescenti ("reverse").
    """
    queue = deque([(start, 0 if direction == "forward" else float('inf'))])
    times = defaultdict(lambda: float('inf') if direction == "forward" else float('-inf'))
    times[start] = 0 if direction == "forward" else float('inf')
    visited = set([start])

    while queue:
        node, t_curr = queue.popleft()
        for neighbor, edge_times in graph[node].items():
            if direction == "forward":
                valid_times = [t for t in edge_times if t >= t_curr]
                if valid_times:
                    min_valid_time = min(valid_times)
                    if min_valid_time < times[neighbor]:  # Condizione di aggiornamento per evitare cicli
                        times[neighbor] = min_valid_time
                        queue.append((neighbor, min_valid_time))
                        visited.add(neighbor)
            else:
                valid_times = [t for t in edge_times if t <= t_curr]
                if valid_times:
                    max_valid_time = max(valid_times)
                    if max_valid_time > times[neighbor]:
                        times[neighbor] = max_valid_time
                        queue.append((neighbor, max_valid_time))
                        visited.add(neighbor)

    return visited, times

def is_temporally_connected_bidirectional(graph):
    """
    Verifica se il grafo è temporalmente connesso bidirezionalmente per ogni coppia (u, v).
    """
    all_nodes = list(graph.keys())
    start_node = random.choice(all_nodes)
    if start_node == all_nodes[0]:
        # BFS in avanti per percorsi temporali crescenti da start_node a ogni altro nodo
        visited_forward, times_forward = bfs_check(graph, start_node, "forward")
        print(f"Nodi visitati a partire dal nodo {start_node}, {visited_forward}")
        if len(visited_forward) != len(graph):
            return False
    elif graph.get(start_node) == {}:
        # BFS inversa per percorsi temporali decrescenti da ogni altro nodo a start_node
        visited_reverse, times_reverse = bfs_check(graph, start_node, "reverse")
        print(f"Nodi visitati a partire dal nodo {start_node}, {visited_reverse}")
        if len(visited_reverse) != len(graph):
            return False
    else:
        visited_forward, times_forward = bfs_check(graph, start_node, "forward")
        visited_reverse, times_reverse = bfs_check(graph, start_node, "reverse")
        print(f"Nodi visitati a partire dal nodo {start_node}, {visited_reverse} e {visited_forward}")
        if len(visited_forward) != len(graph) or len(visited_reverse) != len(graph):
            return False  # Se non tutti i nodi sono raggiunti in entrambi i sensi, non è temporalmente connesso
    
    return True

# Test
albero1 = {
    'A': {'B': [1, 2], 'C': [3, 4]},
    'B': {'D': [1, 3]},
    'C': {'E': [2, 4]},
    'D': set(),
    'E': set()
}

albero2 = {
    'A': {'B': [1, 2], 'C': [2, 3]},
    'B': {'D': [1, 3]},
    'C': {'E': [4, 5]},
    'D': {},
    'E': {}
}   

albero3 = {
    'A': {'B': [1, 2], 'C': [3, 4]},
    'B': {'D': [1, 3]},
    'C': {'E': [2, 4]},
    'D': {'F': [1,1]},
    'E': {},
    'F': {}
}

albero = {
    'A' : {'B': [2,4], 'C': [1]},
    'B' : {'D': [5]},
    'C' : {'E': [2,3]},
    'D' : {},
    'E' : {}
}
grafo = transform_tree_to_graph(albero)

# Verifica se il grafo è temporalmente connesso
result = is_temporally_connected_bidirectional(albero)
print(result)  # Dovrebbe restituire True

