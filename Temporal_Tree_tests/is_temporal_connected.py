from collections import defaultdict
#Funzionante, da vedere correttezza
def is_temporally_connected_v2(tree):
    # Inizializzazione dell'insieme dei nodi visitati
    visited = set()
    
    # Lista di nodi che rimangono da visitare (tutti inizialmente)
    all_nodes = set(tree.keys())
    
    # Ripeti la BFS temporale per ogni nodo non ancora visitato
    for start_node in all_nodes:
        if start_node in visited:
            continue
        
        # Coda per la BFS temporale
        queue = [(start_node, 0)]
        local_visited = set()
        
        # Esegui la BFS per verificare raggiungibilità temporale
        while queue:
            node, t_curr = queue.pop(0)
            if node in visited:
                continue
            
            visited.add(node)
            local_visited.add(node)
            
            # Esplora i successori di `node`
            for neighbor, times in tree[node].items():
                # Trova i tempi validi (>= t_curr)
                valid_times = [t for t in times if t >= t_curr]
                if valid_times:
                    min_valid_time = min(valid_times)
                    if neighbor not in visited:
                        queue.append((neighbor, min_valid_time))
        
        # Alla fine della BFS, verifica che tutti i nodi esplorati
        # siano stati visitati
        if local_visited != all_nodes:
            return False  # Non tutti i nodi sono connessi temporalmente
    
    # Se tutti i nodi sono stati visitati senza problemi
    return True

def is_temporally_connected_v2_timelimit(tree):
    visited = set()  # Insieme dei nodi visitati
    all_nodes = set(tree.keys())  # Tutti i nodi dell'albero

    # Ripeti la BFS temporale per ogni nodo non ancora visitato
    for start_node in all_nodes:
        if start_node in visited:
            continue
        
        # Coda per la BFS temporale
        queue = [(start_node, 0)]
        
        # Esegui la BFS per verificare raggiungibilità temporale
        while queue:
            node, t_curr = queue.pop(0)
            if node in visited:
                continue
            
            visited.add(node)
            
            # Esplora i successori di `node`
            for neighbor, times in tree[node].items():
                # Usa un approccio iterativo su `times` per trovare il primo tempo valido
                for t in sorted(times):
                    if t >= t_curr:
                        # Aggiungi il vicino alla coda con il primo tempo valido trovato
                        if neighbor not in visited:
                            queue.append((neighbor, t))
                        break  # Esci dopo aver trovato il primo tempo valido
        
    # Se tutti i nodi sono stati visitati senza problemi
    return len(visited) == len(all_nodes)

# Questo visita ogni arco una sola volta, riducendo la complessità a O(M)
def is_temporally_connected_v3_timelimit(tree):
    visited_nodes = set()
    visited_edges = set()  # Insieme degli archi visitati

    def dfs(node, time):
        visited_nodes.add(node)
        for neighbor, times in tree[node].items():
            for t in times:
                edge = (node, neighbor, t)
                if edge not in visited_edges and t >= time:
                    visited_edges.add(edge)
                    dfs(neighbor, t)

    # Inizia la BFS da un nodo arbitrario
    start_node = next(iter(tree))
    dfs(start_node, 0)

    return len(visited_nodes) == len(tree)

tree_connected = {
    "A": {"B": [1, 3, 5], "C": [2, 4, 6], "D": [3, 5, 7]},
    "B": {"E": [4, 6, 8], "F": [5, 7, 9]},
    "C": {"G": [5, 8, 10], "H": [6, 9, 11]},
    "D": {"I": [7, 10, 12], "J": [8, 11, 13]},
    "E": {"K": [9, 12, 14], "L": [10, 13, 15]},
    "F": {"M": [11, 14, 16], "N": [12, 15, 17]},
    "G": {"O": [13, 16, 18], "P": [14, 17, 19]},
    "H": {"Q": [15, 18, 20], "R": [16, 19, 21]},
    "I": {},
    "J": {},
    "K": {},
    "L": {},
    "M": {},
    "N": {},
    "O": {},
    "P": {},
    "Q": {},
    "R": {},
}

tree_not_connected = {
    "A": {"B": [1, 2, 5], "C": [3, 6, 10], "D": [4, 7]},
    "B": {"E": [8, 10], "F": [12]},
    "C": {"G": [7, 8, 15], "H": [10, 11]},
    "D": {"I": [5, 9], "J": [11, 12]},
    "E": {"K": [13, 14], "L": [15]},  # Problema: tempo di attivazione molto elevato
    "F": {
        "M": [9, 10],
        "N": [16],
    },  # Problema: tempo di attivazione non crescente per M
    "G": {"O": [10, 12, 13], "P": [18]},  # Problema: connessione temporale interrotta
    "H": {"Q": [14], "R": [17]},
    "I": {},
    "J": {},
    "K": {},
    "L": {},
    "M": {},
    "N": {},
    "O": {},
    "P": {},
    "Q": {},
    "R": {},
}

tree_temporally_connected = {
    "A": {"B": [1, 2, 3], "C": [2, 4]},
    "B": {"D": [3, 5], "E": [4, 6]},
    "C": {"F": [5, 7]},
    "D": {},
    "E": {},
    "F": {},
}
albero1 = {
    'A': {'B': [2, 3], 'C': [4]},
    'B': {'D': [5], 'E': [6]},
    'C': {'F': [7]},
    'D': {},
    'E': {},
    'F': {}
}

#print(is_temporally_connected(tree_temporally_connected, "B"))
print(is_temporally_connected_v2(albero1))
print(is_temporally_connected_v2_timelimit(albero1))
print(is_temporally_connected_v3_timelimit(albero1))