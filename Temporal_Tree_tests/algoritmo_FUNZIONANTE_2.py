# Dijkstra-like

import heapq

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
#print(is_temporally_connected_v3(adj_list))
print(is_temporally_connected_v3(tree3))