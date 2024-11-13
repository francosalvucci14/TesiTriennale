from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n  # Tiene traccia della dimensione di ogni componente

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            # Union by rank
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
                self.size[root_u] += self.size[root_v]
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
                self.size[root_v] += self.size[root_u]
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
                self.size[root_u] += self.size[root_v]

    def max_component_size(self):
        # Restituisce la dimensione della componente connessa più grande
        return max(self.size[self.find(i)] for i in range(len(self.parent)))

class OptimizedTemporalTree:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.edges = []  # Lista di archi con intervalli temporali

    def add_edge(self, u, v, times):
        for time in times:
            self.edges.append((time, u, v))  # Aggiungi l'arco con l'intervallo di attivazione

    def is_temporally_connected(self):
        # Step 1: Verifica se tutti gli archi hanno le stesse etichette
        all_same_label = True
        first_label = None
        for time, u, v in self.edges:
            if first_label is None:
                first_label = time
            if time != first_label:
                all_same_label = False
                break

        # Se tutte le etichette sono uguali, ritorna True
        if all_same_label:
            return True
        
        # Step 2: Organizza gli archi per etichetta temporale
        edge_dict = defaultdict(list)
        for time, u, v in self.edges:
            edge_dict[time].append((u, v))

        # Step 3: Ordina gli archi per tempo
        timestamps = sorted(edge_dict.keys())

        # Step 4: Applicare la logica di unione con le condizioni che hai specificato
        uf = UnionFind(self.num_nodes)
        
        for i in range(1, len(timestamps)):
            prev_timestamp = timestamps[i-1]
            curr_timestamp = timestamps[i]
            
            # Unisci gli archi che appartengono agli stessi intervalli temporali
            for u, v in edge_dict[prev_timestamp]:
                uf.union(u, v)
                
            # Propagazione degli archi che soddisfano le condizioni di unione
            if curr_timestamp >= prev_timestamp:
                for u, v in edge_dict[prev_timestamp]:
                    for u2, v2 in edge_dict[curr_timestamp]:
                        if u == u2 or v == v2:
                            uf.union(u, v)

            # Verifica se l'albero è temporalmente connesso
            if uf.max_component_size() == self.num_nodes:
                return True

        # Se nessun timestamp genera una componente connessa, restituiamo False
        return False
    
class OptimizedTemporalTree2:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.edges = []  # Lista di archi con intervalli temporali

    def add_edge(self, u, v, times):
        for time in times:
            self.edges.append((time, u, v))  # Aggiungi l'arco con l'intervallo di attivazione

    def is_temporally_connected(self):
        # Step 1: Organizza gli archi per etichetta temporale
        edge_dict = defaultdict(list)
        for time, u, v in self.edges:
            edge_dict[time].append((u, v))

        # Step 2: Ordina gli archi per tempo
        timestamps = sorted(edge_dict.keys())

        # Step 3: Verifica la copertura di archi per ciascun timestamp
        for i in range(1, len(timestamps)):
            prev_timestamp = timestamps[i-1]
            curr_timestamp = timestamps[i]

            # Crea un set di archi attivi per il timestamp precedente
            prev_edges = set(edge_dict[prev_timestamp])
            # Crea un set di archi attivi per il timestamp corrente
            curr_edges = set(edge_dict[curr_timestamp])

            # Verifica se tutti gli archi sono coperti (ogni arco deve essere attivo almeno in un timestamp)
            all_edges = prev_edges.union(curr_edges)

            # Se la copertura totale degli archi corrisponde a tutti gli archi dell'albero, ritorna True
            if len(all_edges) == len(self.edges):
                return True

        # Se nessuna combinazione di timestamp copre tutti gli archi, ritorna False
        return False

class OptimizedTemporalTree3:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.edges = []  # Lista di archi con intervalli temporali

    def add_edge(self, u, v, times):
        for time in times:
            self.edges.append((time, u, v))  # Aggiungi l'arco con l'intervallo di attivazione

    def is_temporally_connected(self):
        # Step 1: Organizza gli archi per etichetta temporale
        edge_dict = defaultdict(list)
        for time, u, v in self.edges:
            edge_dict[time].append((u, v))

        # Step 2: Ordina gli archi per tempo
        timestamps = sorted(edge_dict.keys())

        # Step 3: Verifica la connettività per ogni timestamp
        for t in timestamps:
            # Crea un grafo per il timestamp t
            graph = defaultdict(list)
            for u, v in edge_dict[t]:
                graph[u].append(v)
                graph[v].append(u)

            # Step 4: Verifica la connettività del grafo per il timestamp t
            visited = [False] * self.num_nodes
            self.dfs(0, visited, graph)  # Partiamo dal nodo 0 per fare DFS

            # Se tutti i nodi sono visitati, significa che il grafo è connesso
            if all(visited):
                return True

        return False

    def dfs(self, node, visited, graph):
        # DFS per visitare tutti i nodi raggiungibili
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, graph)

# Costruzione dell'albero con i dati forniti e verifica con il nuovo criterio
tree = OptimizedTemporalTree3(5)
# tree.add_edge(0, 1, [1, 3])   
# tree.add_edge(0, 2, [2,6])   
# tree.add_edge(1, 3, [3,5])      
# tree.add_edge(1, 4, [4,6])    
# 
tree.add_edge(0,1,[1,3,4])
tree.add_edge(0,2,[4])
tree.add_edge(1,3,[2,4])
tree.add_edge(1,4,[2,5,6])

# Verifica se esiste almeno un timestamp per cui l'albero è temporalmente connesso
result = tree.is_temporally_connected()
print(f"Albero temporalmente connesso? : {result}")  # Dovrebbe stampare True
