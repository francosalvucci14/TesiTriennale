from collections import defaultdict, deque

def compress_timestamps(adj_list):
    # Estrai tutti i timestamp
    all_timestamps = set()
    for u in adj_list:
        for v, timestamps in adj_list[u]:
            all_timestamps.update(timestamps)
    
    # Ordina e assegna un indice a ogni timestamp per la compressione
    sorted_timestamps = sorted(all_timestamps)
    timestamp_index = {t: i for i, t in enumerate(sorted_timestamps)}
    return timestamp_index, sorted_timestamps

def bfs_temporal(u, target, adj_list, timestamp_index, sorted_timestamps):
    # BFS per cercare di raggiungere il target rispettando i tempi
    queue = deque([(u, 0)])  # Ogni elemento è una coppia (nodo, indice timestamp)
    visited = {u: 0}  # Traccia il timestamp minimo visitato per ciascun nodo
    
    while queue:
        current, time_idx = queue.popleft()
        
        if current == target:
            return True
        
        for neighbor, timestamps in adj_list[current]:
            # Considera solo timestamp >= sorted_timestamps[time_idx]
            for t in timestamps:
                if t >= sorted_timestamps[time_idx]:  # Usa sorted_timestamps correttamente
                    next_time_idx = timestamp_index[t]
                    # Visita solo se non è già stato visitato con un tempo minore
                    if neighbor not in visited or visited[neighbor] > next_time_idx:
                        visited[neighbor] = next_time_idx
                        queue.append((neighbor, next_time_idx))
                    break  # Prendi solo il primo timestamp valido
                
    return False

def is_temporally_connected_v5(adj_list):
    # Step 1: Comprimi i timestamp
    timestamp_index, sorted_timestamps = compress_timestamps(adj_list)
    
    # Step 2: Verifica la connessione temporale per ogni coppia di nodi
    nodes = list(adj_list.keys())
    for u in nodes:
        for v in nodes:
            if u != v:
                if not bfs_temporal(u, v, adj_list, timestamp_index, sorted_timestamps):
                    return False  # Se una coppia non è connessa, ritorna False
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
    2: [(0, [4]), (4, [2,5,6])],
    3: [(1, [2,4])],
    4: [(2, [2,5,6])]
}
tree2 = {
    0:[(1,[1,3]),(2,[2,6])],
    1:[(0,[1,3]),(3,[3,5]),(4,[4,6])],
    2:[(0,[2,6])],
    3:[(1,[3,5])],
    4:[(1,[4,6])]
}
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
print(is_temporally_connected_v5(tree4))