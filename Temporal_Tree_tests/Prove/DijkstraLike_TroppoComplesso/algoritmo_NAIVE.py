# Revisione dell'algoritmo per verifica indipendente della raggiungibilità temporale tra ogni coppia di nodi 
 
def dfs_path_check(u, target, adj_list, current_time, visited): 
    """DFS che verifica se esiste un percorso temporale valido da u a target.""" 
    if u == target: 
        return True 
    visited.add(u) 
 
    for neighbor, timestamps in adj_list[u]: 
        # Considera solo timestamp >= current_time per rispettare la condizione di crescita 
        valid_timestamps = [t for t in timestamps if t >= current_time] 
        if valid_timestamps: 
            next_time = min(valid_timestamps)  # Scegli il minimo valido per continuare la DFS 
            if neighbor not in visited: 
                # Continua DFS per verificare se si può raggiungere il target 
                if dfs_path_check(neighbor, target, adj_list, next_time, visited): 
                    return True 
 
    visited.remove(u) 
    return False 
 
def is_temporally_connected_v2(adj_list): 
    # Step 1: Per ogni coppia di nodi (u, v), verifica se esiste un percorso temporale valido 
    nodes = list(adj_list.keys()) 
    for u in nodes: 
        for v in nodes: 
            if u != v: 
                visited = set()  # Traccia i nodi visitati per ogni coppia (u, v) 
                if not dfs_path_check(u, v, adj_list, 1, visited):  # Partendo dal timestamp minimo 1 
                    return False  # Se esiste una coppia non connessa temporalmente, ritorna False 
    return True 
 
 
# Lista di adiacenza dell'albero 
adj_list = { 
    0: [(1, [1, 2]), (2, [1, 3])], 
    1: [(0, [1, 2]), (3, [2])], 
    2: [(0, [1, 3]), (4, [2])], 
    3: [(1, [2])], 
    4: [(2, [2])] 
} 

tree = {
    0: [(1, [1, 3,4]), (2, [4])],
    1: [(0, [1, 3,4]), (3, [2,4])],
    2: [(0, [4]), (4, [2])],
    3: [(1, [2,4])],
    4: [(2, [2])]
}
print(is_temporally_connected_v2(tree))
    