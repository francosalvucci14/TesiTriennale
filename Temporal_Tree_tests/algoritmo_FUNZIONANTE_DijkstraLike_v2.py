import heapq
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
from bisect import bisect_left
import random

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
adj_list2 = { 
    0: [(1, [1, 2]), (2, [1, 2])], 
    1: [(0, [1, 2]), (3, [2])], 
    2: [(0, [1, 2]), (4, [2])], 
    3: [(1, [2])], 
    4: [(2, [2])] 
} 

tree_Catena = {
    0 : [(1,[1,2])],
    1 : [(0,[1,2]),(2,[1,3])],
    2 : [(1,[1,2]),(3,[1,2])],
    3 : [(2,[1,3]),(4,[2])],
    4 : [(3,[2])]
}

tree5_1 = {
    0 : [(1,[1,2]),(2,[1,2])],
    1 : [(0,[1,2]),(3,[2])],
    2 : [(0,[1,2]),(4,[2])],
    3 : [(1,[1,2])],
    4 : [(2,[2])]
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

tree12 = {
    0: [(1, [3, 12]), (2, [5, 14])],                # Radice con due figli
    1: [(0, [4, 13]), (3, [6, 10]), (4, [7, 12]), (5, [9, 15])],  # Nodo 1 con padre 0 e figli 3, 4, 5
    2: [(0, [2, 11]), (6, [1, 8]), (7, [4, 13])],   # Nodo 2 con padre 0 e figli 6, 7
    3: [(1, [5, 12])],                              # Foglia, padre 1
    4: [(1, [3, 9]), (8, [7, 14])],                 # Nodo 4 con padre 1 e figlio 8
    5: [(1, [6, 11]), (9, [2, 14]), (10, [8, 15])], # Nodo 5 con padre 1 e figli 9, 10
    6: [(2, [4, 10])],                              # Foglia, padre 2
    7: [(2, [3, 9]), (11, [6, 14])],                # Nodo 7 con padre 2 e figlio 11
    8: [(4, [5, 12])],                              # Foglia, padre 4
    9: [(5, [4, 13])],                              # Foglia, padre 5
    10: [(5, [6, 11]), (12, [7, 14])],              # Nodo 10 con padre 5 e figlio 12
    11: [(7, [5, 10])],                             # Foglia, padre 7
    12: [(10, [3, 12])]                             # Foglia, padre 10
}

tree_v2 = {
    0: [(1, [2, 6]), (2, [6])],
    1: [(0, [2, 6]), (3, [1, 2, 3, 4, 5])],
    2: [(0, [6]), (4, [6])],
    3: [(1, [1, 2, 3, 4, 5]),(5,[3]),(6,[4]),(7,[1,2,7])],
    4: [(2, [6])],
    5: [(3,[3])],
    6: [(3,[4])],
    7: [(3,[1,2,7])]
}

tree5 = {
    0 : [(1,[1,2]),(2,[1,2])],
    1 : [(0,[1,2]),(3,[2]),(4,[3])],
    2 : [(0,[1,2]),(5,[2])],
    3 : [(1,[2])],
    4 : [(1,[3])],
    5 : [(2,[2])]
}
start = timer()
print(f"Nodi dell'albero: {tree_v2.keys()}")
print(f"Albero temporalmente connesso? : {is_temporally_connected_v5(tree5)}")
end = timer()
print(f"Tempo di esecuzione per v5: {timedelta(seconds=end-start)}")
