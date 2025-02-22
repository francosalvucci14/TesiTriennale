from bisect import bisect_left

def dfs_path_check(u, target, adj_list, current_time, visited, memo):
    """DFS che verifica se esiste un percorso temporale valido da u a target."""
    if u == target:
        return True
    if (u, target, current_time) in memo:
        return memo[(u, target, current_time)]
    
    visited.add(u)
    
    for neighbor, timestamps in adj_list[u]:
        # Trova il primo timestamp >= current_time usando ricerca binaria
        idx = bisect_left(timestamps, current_time)
        if idx < len(timestamps):  # Se esiste un timestamp valido
            next_time = timestamps[idx]
            if neighbor not in visited:
                # Continua DFS per verificare se si può raggiungere il target
                if dfs_path_check(neighbor, target, adj_list, next_time, visited, memo):
                    memo[(u, target, current_time)] = True
                    visited.remove(u)
                    return True
    
    visited.remove(u)
    memo[(u, target, current_time)] = False
    return False

def is_temporally_connected_v2(adj_list):
    # Step 1: Ordina i timestamp per ogni arco
    for node in adj_list:
        for neighbor, timestamps in adj_list[node]:
            timestamps.sort()

    # Step 2: Per ogni coppia di nodi (u, v), verifica se esiste un percorso temporale valido
    nodes = list(adj_list.keys())
    memo = {}  # Memoization per evitare ricalcoli ridondanti
    for u in nodes:
        for v in nodes:
            if u != v:
                visited = set()  # Traccia i nodi visitati per ogni coppia (u, v)
                if not dfs_path_check(u, v, adj_list, 1, visited, memo):  # Partendo dal timestamp minimo 1
                    return False  # Se esiste una coppia non connessa temporalmente, ritorna False
    return True
 
# Lista di adiacenza dell'albero 
adj_list = { 
    0: [(1, [1, 2]), (2, [1, 2])], 
    1: [(0, [1, 2]), (3, [2])], 
    2: [(0, [1, 2]), (4, [2])], 
    3: [(1, [2])], 
    4: [(2, [2])] 
} 
# Verifica della connessione temporale con il nuovo algoritmo ottimizzato 
temporally_connected_optimized = is_temporally_connected_v2(adj_list) 
print(temporally_connected_optimized)
