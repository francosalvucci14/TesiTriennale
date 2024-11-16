import heapq
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
from bisect import bisect_left

# def temporal_bfs_optimized(u, adj_list):
#     """Esegue una BFS temporale partendo da u rispettando l'ordine temporale, con complessità O(M log M)"""
#     heap = []
#     visited = {u: 0}  # Dizionario con il nodo e il minimo timestamp raggiunto
    
#     # Inizializza la coda con il minimo timestamp per ogni vicino
#     for neighbor, timestamps in adj_list[u]:
#         min_timestamp = min(timestamps)
#         heapq.heappush(heap, (min_timestamp, neighbor))

#     while heap:
#         current_time, current_node = heapq.heappop(heap)

#         # Se il nodo non è mai stato visitato o se troviamo un timestamp minore
#         if current_node not in visited or current_time < visited[current_node]:
#             visited[current_node] = current_time

#             # Aggiungi i vicini di current_node con il prossimo timestamp valido
#             for neighbor, timestamps in adj_list[current_node]:
#                 if neighbor not in visited or current_time < visited[neighbor]:
#                     # Trova il primo timestamp >= current_time
#                     idx = bisect_left(timestamps, current_time)
#                     if idx < len(timestamps):
#                         next_time = timestamps[idx]
#                         heapq.heappush(heap, (next_time, neighbor))

#     return visited.keys()

# def is_temporally_connected_v4(adj_list):
#     """Verifica se il grafo è temporaneamente connesso con un costo O(M log M)"""
#     nodes = list(adj_list.keys())
    
#     # Per ogni nodo u, esegui BFS temporale per trovare tutti i nodi raggiungibili da u
#     for u in nodes:
#         reachable = temporal_bfs_optimized(u, adj_list)

#         # Verifica se esiste un nodo non raggiungibile
#         if len(reachable) != len(nodes):
#             return False
    
#     return True

def temporal_bfs_memo(u, adj_list, memo):
    """Esegue una BFS temporale con memorizzazione (memoization)"""
    # Coda di priorità (heap), contiene tuple (timestamp, nodo)
    heap = []
    heapq.heappush(heap, (0, u))  # Partiamo da u con il timestamp minimo

    # Inizializza il dizionario memo per u
    if u not in memo:
        memo[u] = {u: 0}
    visited = memo[u]

    while heap:
        current_time, current_node = heapq.heappop(heap)

        # Esplora i vicini di current_node
        for neighbor, timestamps in adj_list[current_node]:
            # Trova il primo timestamp >= current_time
            idx = bisect_left(timestamps, current_time)
            if idx < len(timestamps):
                next_time = timestamps[idx]
                # Se il vicino non è stato visitato o se troviamo un percorso temporale migliore
                if neighbor not in visited or next_time < visited.get(neighbor, float('inf')):
                    visited[neighbor] = next_time
                    heapq.heappush(heap, (next_time, neighbor))

    
    # Restituisce i nodi raggiungibili
    return set(visited.keys())

def is_temporally_connected_v5(adj_list):
    """Verifica se il grafo è temporaneamente connesso usando la memorizzazione dei percorsi."""
    nodes = list(adj_list.keys())
    memo = defaultdict(dict)  # Dato che vogliamo lanciare BFS per ogni nodo

    for u in nodes:
        reachable = temporal_bfs_memo(u, adj_list, memo)
        print(f"Nodi visitabili da {u}: {reachable}")
        # Se un nodo non è raggiungibile da u, il grafo non è connesso temporalmente
        if len(reachable) != len(nodes):
            return False
    return True


adj_list = { 
    0: [(1, [1, 2]), (2, [1, 3])], 
    1: [(0, [1, 2]), (3, [2])], 
    2: [(0, [1, 3]), (4, [3])], 
    3: [(1, [2])], 
    4: [(2, [3])] 
} 

tree5 = {
    0 : [(1,[1,2])],
    1 : [(0,[1,2]),(2,[1,2])],
    2 : [(1,[1,2]),(3,[1,2])],
    3 : [(2,[1,2]),(4,[2])],
    4 : [(3,[2])]
}
tree3 = {
    0:[(1,[2,6]),(2,[6])],
    1:[(0,[2,6]),(3,[1,2,3,4,5,6])],
    2:[(0,[6]),(4,[6])],
    3:[(1,[1,2,3,4,5,6])],
    4:[(2,[6])]
}

tree4 = {
    0:[(1,[2]),(2,[5,7])],
    1:[(0,[2]),(3,[5])],
    2:[(0,[5,7]),(4,[8,9]),(5,[8,8])],
    3:[(1,[5])],
    4:[(2,[8,9])],
    5:[(2,[8,8])]
}

start = timer()
print(f"Albero temporalmente connesso? : {is_temporally_connected_v5(tree3)}")
end = timer()
print(f"Tempo di esecuzione per v5: {timedelta(seconds=end-start)}")