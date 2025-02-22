from bisect import bisect_left

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}  # {neighbor_node: [temporal_labels]}

def edge_stream_representation(root):
    """Genera la rappresentazione dell'albero come una sequenza di archi temporali ordinata"""
    edges = []
    
    def dfs(node):
        for neighbor, times in node.edges.items():
            for time in times:
                edges.append((node, neighbor, time))  # (u, v, t)
            # Recursive DFS call to process children
            dfs(neighbor)
    
    dfs(root)
    
    # Ordina gli archi in base al valore delle etichette temporali
    edges.sort(key=lambda x: x[2])  # ordinamento in base al valore dell'etichetta temporale
    return edges

def check_temporal_connectivity(root):
    """Verifica se l'albero è temporalmente connesso"""
    
    # Otteniamo la rappresentazione in edge stream
    edges = edge_stream_representation(root)
    #print(edges)
    # Troviamo il massimo tra tutte le etichette temporali
    max_time = max(time for _, _, time in edges)
    
    # Caso base: Se tutte le etichette sono uguali, ritorna True
    if all(time == edges[0][2] for _, _, time in edges):
        return True
    
    # Verifica la connettività temporale tramite Binary Search
    for u, v, time in edges:
        if time >= max_time:
            return False  # Se troviamo un arco con tempo >= al massimo, ritorniamo False
    
    # Se nessun arco ha tempi >= al massimo, allora è connesso
    return True

# Creazione dei nodi dell'albero
nodeA = Node('A')
nodeB = Node('B')
nodeC = Node('C')
nodeD = Node('D')
nodeE = Node('E')

# Creazione delle etichette temporali sugli archi
# nodeA.edges = {nodeB: [1, 2], nodeC: [1, 3]}  # Arco da A a B con etichette temporali [1, 2] e A a C [1, 3]
# nodeB.edges = {nodeD: [2]}  # Arco da B a D con etichetta temporale [2]
# nodeC.edges = {nodeE: [2]}  # Arco da C a E con etichetta temporale [2]
# nodeD.edges = {}  # Nodo D senza archi
# nodeE.edges = {}  # Nodo E senza archi

# Creazione delle etichette temporali sugli archi
nodeA.edges = {nodeB: [2,6], nodeC: [6]}  # Arco da A a B con etichette temporali [1, 2] e A a C [1, 3]
nodeB.edges = {nodeD: [6]}  # Arco da B a D con etichetta temporale [2]
nodeC.edges = {nodeE: [3]}  # Arco da C a E con etichetta temporale [2]
nodeD.edges = {}  # Nodo D senza archi
nodeE.edges = {}  # Nodo E senza archi

# Verifica se l'albero è temporalmente connesso
print(check_temporal_connectivity(nodeA))  # Dovrebbe restituire True o False a seconda dell'albero
