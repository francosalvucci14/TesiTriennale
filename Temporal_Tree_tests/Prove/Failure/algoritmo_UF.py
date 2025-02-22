def is_temporally_connected(n, edges):
    # Espande gli archi con etichette temporali multiple in una lista di tuple (u, v, t)
    expanded_edges = []
    for (u, v, times) in edges:
        for t in times:
            expanded_edges.append((u, v, t))
    
    # Ordina gli archi per etichetta temporale
    expanded_edges.sort(key=lambda x: x[2])
    
    # Inizializza il union-find
    uf = UnionFind(n)
    
    for (u, v, t) in expanded_edges:
        uf.union(u, v)  # Unione dell'arco nell'albero temporale
        if uf.is_connected():  # Verifica se è tutto connesso
            return True
    
    return False  # Non è temporalmente connesso

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n  # Numero di componenti connessi
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            # Union by rank
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            self.components -= 1  # Riduci il numero di componenti connessi
    
    def is_connected(self):
        return self.components == 1


n = 4  # Numero di nodi
edges = [
    (0, 1, [1, 2]),  # L'arco tra 0 e 1 è disponibile ai tempi 1, 3 e 5
    (0, 2, [1,2]),     # L'arco tra 1 e 2 è disponibile ai tempi 2 e 4
    (1, 3, [2]),     # L'arco tra 2 e 3 è disponibile ai tempi 1 e 4
    (2, 4, [2])       # L'arco tra 3 e 4 è disponibile solo al tempo          # L'arco tra 0 e 4 è disponibile solo al tempo 5
]

# Chiamata alla funzione per verificare la connessione temporale
result = is_temporally_connected(n, edges)
print(result)
