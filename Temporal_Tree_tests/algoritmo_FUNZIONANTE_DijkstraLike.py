# Dijkstra-like

import heapq

def print_tree(tree):
    # Definisci la mappatura dei nodi in caratteri
    node_to_char = {i: chr(ord('A') + i) for i in range(len(tree))}
    
    for node, edges in tree.items():
        node_char = node_to_char[node]  # Ottieni il carattere associato al nodo
        for neighbor, timestamps in edges:
            neighbor_char = node_to_char[neighbor]  # Ottieni il carattere del vicino
            print(f"Nodo {node_char} -> Vicino {neighbor_char} con tempi {timestamps}")

# def all_labels_equal(adj_list):
#     """Controlla se tutte le etichette temporali degli archi sono uguali"""
#     first_label = None
    
#     for node, edges in adj_list.items():
#         for _, timestamps in edges:
#             if not timestamps:
#                 continue
#             if first_label is None:
#                 first_label = timestamps[0]
#             # Verifica se tutte le etichette sono uguali al primo timestamp trovato
#             if any(label != first_label for label in timestamps):
#                 return False
#     return True

def temporal_bfs(u, adj_list, n):
    """Esegui una BFS che esplora i nodi partendo da u, rispettando l'ordine temporale dei timestamp"""
    # Coda di priorità (heap), contiene tuple del tipo (timestamp, nodo)
    heap = []
    # Inizializza la coda con i nodi vicini di u, con il minimo timestamp
    for neighbor, timestamps in adj_list[u]:
        for timestamp in timestamps:
            heapq.heappush(heap, (timestamp, neighbor))

    visited = set()
    visited.add(u)

    while heap:
        current_time, current_node = heapq.heappop(heap)

        if current_node not in visited:
            visited.add(current_node)

            # Aggiungi i vicini di current_node alla coda se non sono già stati visitati
            for neighbor, timestamps in adj_list[current_node]:
                if neighbor not in visited:
                    for timestamp in timestamps:
                        if timestamp >= current_time:  # Solo timestamp validi
                            heapq.heappush(heap, (timestamp, neighbor))
    
    return visited

def is_temporally_connected_v3(adj_list):
    # Se tutte le etichette sono uguali, ritorna True
    # if all_labels_equal(adj_list):
    #     return True
    """Verifica se il grafo è temporaneamente connesso, per ogni coppia di nodi"""
    nodes = list(adj_list.keys())
    n = len(nodes)
    
    # Per ogni nodo u, esegui BFS temporale per trovare tutti i nodi raggiungibili da u
    for u in nodes:
        reachable = temporal_bfs(u, adj_list, n)

        # Se un nodo non è raggiungibile da u, il grafo non è connesso temporalmente
        for v in nodes:
            if v != u and v not in reachable:
                return False
    
    return True

tree3 = {
    0:[(1,[2,6]),(2,[6])],
    1:[(0,[2,6]),(3,[1,2,3,4,5,6])],
    2:[(0,[6]),(4,[6])],
    3:[(1,[1,2,3,4,5,6])],
    4:[(2,[6])]
}

tree4 = {
    0:[(1,[2,3]),(2,[4])],
    1:[(0,[2,3]),(3,[5]),(4,[6])],
    2:[(0,[4]),(5,[7])],
    3:[(1,[5])],
    4:[(1,[6])],
    5:[(2,[7])]
}
adj_list = { 
    0: [(1, [1, 2]), (2, [1, 2])], 
    1: [(0, [1, 2]), (3, [2])], 
    2: [(0, [1, 2]), (4, [2])], 
    3: [(1, [2])], 
    4: [(2, [2])] 
} 
adj_list2 = { 
    0: [(1, [1]), (2, [1])], 
    1: [(0, [1]), (3, [1])], 
    2: [(0, [1]), (4, [1])], 
    3: [(1, [1])], 
    4: [(2, [1])] 
} 
tree5 = {
    0 : [(1,[1,2])],
    1 : [(0,[1,2]),(2,[1,2])],
    2 : [(1,[1,2]),(3,[1,2])],
    3 : [(2,[1,2]),(4,[2])],
    4 : [(3,[2])]
}
#print(is_temporally_connected_v3(adj_list))
print_tree(adj_list2)
print(f"Albero temporalmente connesso? : {is_temporally_connected_v3(adj_list2)}")