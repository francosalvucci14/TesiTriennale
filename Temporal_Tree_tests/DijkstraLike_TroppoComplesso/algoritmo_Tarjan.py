import heapq
from bisect import bisect_left
from collections import defaultdict

def temporal_bfs_memo(u, adj_list, memo):
    """Esegue una BFS temporale con memorizzazione (memoization)"""
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
            idx = bisect_left(timestamps, current_time)
            if idx < len(timestamps):
                next_time = timestamps[idx]
                if neighbor not in visited or next_time < visited.get(neighbor, float('inf')):
                    visited[neighbor] = next_time
                    heapq.heappush(heap, (next_time, neighbor))
        
    return set(visited.keys())  # Restituisce i nodi raggiungibili

def is_temporally_connected(adj_list):
    """Verifica se il grafo è temporaneamente connesso usando BFS temporale per ogni nodo"""
    nodes = list(adj_list.keys())
    memo = defaultdict(dict)

    all_reachable_nodes = []
    
    # Eseguiamo BFS temporale per ogni nodo
    for u in nodes:
        reachable = temporal_bfs_memo(u, adj_list, memo)
        all_reachable_nodes.append(reachable)
        print(f"Nodi raggiungibili da {u}: {reachable}")
    
    # Verifica se tutte le componenti connesse contengono tutti i nodi
    for reachable in all_reachable_nodes:
        if len(reachable) != len(nodes):
            return False  # Se una componente non contiene tutti i nodi, ritorna False
    
    return True  # Se tutte le componenti contengono tutti i nodi, ritorna True

# Esempio di grafo
adj_list = {
    0: [(1, [1, 2]), (2, [1, 2])],
    1: [(0, [1, 2]), (3, [2])],
    2: [(0, [1, 2]), (4, [3])],
    3: [(1, [2])],
    4: [(2, [3])]
}

# Test del grafo
is_connected = is_temporally_connected(adj_list)
print("Il grafo è temporalmente connesso?", is_connected)
