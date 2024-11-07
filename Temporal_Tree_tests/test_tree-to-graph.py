import pprint as pp

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


def bfs(graph, start_node):
    """
    Esegui una BFS su un grafo, partendo da un nodo casuale.
    """
    visited = set()  # Set per tenere traccia dei nodi visitati
    queue = [start_node]  # Coda per la BFS
    visited.add(start_node)
    
    while queue:
        current_node = queue.pop(0)
        print(f"Visito il nodo {current_node}")
        
        # Aggiungi i vicini non visitati alla coda
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return visited

# Esempio di albero
albero3 = {
    'A': {'B': [1, 2], 'C': [3, 4]},
    'B': {'D': [1, 3]},
    'C': {'E': [2, 4]},
    'D': {'F': [1,1]},
    'E': {},
    'F': {}
}

# Trasformazione dell'albero in un grafo non diretto
grafo = transform_tree_to_graph(albero3)
print("GRAFO")
pp.pprint(grafo)
print("ALBERO")
pp.pprint(albero3)

# Scegli un nodo casuale e esegui la BFS
#start_node = random.choice(list(grafo.keys()))
start_node='B'
print(f"Parto dal nodo {start_node}")

# Esegui la BFS
visited_nodes = bfs(grafo, start_node)
