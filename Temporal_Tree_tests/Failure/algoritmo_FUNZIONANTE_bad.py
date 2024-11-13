from collections import defaultdict

def print_tree_structure(tree):

    # Creazione della lista di adiacenza con archi e tempi
    adj_list = defaultdict(list)
    for u, v, times in tree:
        adj_list[u].append((v, times))
        adj_list[v].append((u, times))
    print("ALBERO")
    # Stampa della struttura dell'albero
    for node in sorted(adj_list.keys()):
        print(f"Nodo {node} ->", end=" ")
        for neighbor, times in adj_list[node]:
            print(f"Vicino {neighbor} con tempi {times}", end="; ")
        print()  # Nuova riga per il prossimo nodo

# def is_temporally_connected(n, edges):
#     # Creazione della lista di adiacenza con archi e tempi
#     adj_list = defaultdict(list)
#     for u, v, times in edges:
#         for t in times:
#             adj_list[u].append((v, t))
#             adj_list[v].append((u, t))

#     # DFS per registrare i tempi di accesso
#     def dfs_up(node, parent, current_time):
#         min_time = current_time
#         max_time = current_time

#         for neighbor, time in sorted(adj_list[node], key=lambda x: x[1]):
#             if neighbor != parent:
#                 min_child, max_child = dfs_up(neighbor, node, time)
#                 min_time = min(min_time, min_child)
#                 max_time = max(max_time, max_child)

#         min_times[node] = min_time
#         max_times[node] = max_time
#         return min_time, max_time

#     # Inizializza le strutture dati
#     min_times = [float('inf')] * n
#     max_times = [-float('inf')] * n

#     # Esegui la DFS verso l'alto dalla radice (nodo 0)
#     dfs_up(0, -1, float('-inf'))

#     # Verifica dei percorsi tra coppie di nodi
#     for u in range(n):
#         for v in range(u + 1, n):
#             if not (max_times[u] >= min_times[v] and max_times[v] >= min_times[u]):
#                 return False

#     return True

def is_temporally_connected_opt(n, edges):
    
    max_times = set()
    
    for u, v, times in edges:
        # Trova il massimo per ogni arco
        max_times.add(max(times))
    
    # Se tutti i massimi sono uguali, ritorna True
    if len(max_times) == 1:
        return True
    
    # Creazione della lista di adiacenza con archi e tempi
    adj_list = defaultdict(list)
    
    # Aggiungi gli archi alla lista di adiacenza
    for u, v, times in edges:
        for t in times:
            adj_list[u].append((v, t))
            adj_list[v].append((u, t))
    print(adj_list)
    # Ordinamento globale degli archi per tempo
    all_edges = []
    for u in adj_list:
        for v, t in adj_list[u]:
            if u < v:  # Evita duplicati (ogni arco è bidirezionale)
                all_edges.append((t, u, v))
    
    # Ordina gli archi in base al tempo
    all_edges.sort()

    # Creazione della lista di archi ordinati per ciascun nodo
    sorted_edges_for_node = defaultdict(list)
    for t, u, v in all_edges:
        sorted_edges_for_node[u].append((t, v))
        sorted_edges_for_node[v].append((t, u))

    # DFS per registrare i tempi di accesso
    def dfs_up(node, parent, current_time):
        min_time = current_time
        max_time = current_time

        # Esplora gli archi ordinati per tempo per il nodo corrente
        for time, neighbor in sorted_edges_for_node[node]:
            if neighbor != parent:
                min_child, max_child = dfs_up(neighbor, node, time)
                min_time = min(min_time, min_child)
                max_time = max(max_time, max_child)

        min_times[node] = min_time
        max_times[node] = max_time
        return min_time, max_time

    # Inizializza le strutture dati
    min_times = [float('inf')] * n
    max_times = [-float('inf')] * n

    # Esegui la DFS verso l'alto dalla radice (nodo 0)
    dfs_up(0, -1, float('-inf'))
    #dfs_up(4, -1, float('-inf'))
    print(max_times,min_times)
    # Verifica dei percorsi tra coppie di nodi
    for u in range(n):
        for v in range(u + 1, n):
            if not (max_times[u] >= min_times[v] and max_times[v] >= min_times[u]):
                return False

    return True

n = 5  # Numero di nodi
edges = [
    (0, 1, [1,3]), 
    (0, 2, [2,6]),    
    (1, 3, [3,5]),
    (1,4,[4,6])          
]
tree3 = [
    (0, 1, [2,6]), 
    (0, 2, [6]),    
    (1, 3, [1,2,3,4,5,6]),
    (2,4,[6])          
]
tree = [
    (0,1,[1]),
    (1,2,[4,5]),
    (2,3,[3]),
    (3,4,[6])
]
n2 = 6
tree2 = [
    (0,1,[2]),
    (0,2,[4]),
    (1,3,[5]),
    (1,4,[3]),
    (2,5,[7])
]

tree4 = [
    (0,1,[1,3]),
    (0,2,[2,4]),
    (1,3,[3]),
    (2,4,[4])
]
tree5 = [
    (0,1,[1,3,4]),
    (0,2,[4]),
    (1,3,[2,4]),
    (2,4,[2,5,6])
]
tree6 = [
    (0,1,[1,2]),
    (0,2,[1,3]),
    (1,3,[2]),
    (2,4,[2])
]
print_tree_structure(tree5)
#print(f"L'albero è temporalmente connesso? : {is_temporally_connected(5, tree4)}") 
print(f"L'albero è temporalmente connesso? : {is_temporally_connected_opt(5, tree5)}")  

# Funziona per alberi normali, poi bisogna aggiustarlo per alberi a catena

# Approccio rivisitato

# Per verificare la connessione temporale in tempo O(Mlog⁡N), possiamo seguire questi passi:

#     DFS per registrare i tempi di accesso: Esegui una DFS per registrare i tempi minimi e massimi per ciascun nodo durante il percorso verso la radice.
#     Verifica delle connessioni tra sottoalberi: Per ogni coppia di nodi appartenenti a sottoalberi diversi, verifica che esista un journey temporale crescente risalendo alla radice e poi scendendo.

# Algoritmo dettagliato

# L'idea è di eseguire due DFS:

#     Una DFS verso l'alto per registrare i tempi minimi e massimi per ogni nodo rispetto alla radice.
#     Una DFS verso il basso per tracciare i tempi in cui è possibile scendere dalla radice ai nodi.

# Dopo aver raccolto queste informazioni, possiamo verificare se è possibile avere un percorso temporale crescente tra ogni coppia di nodi.