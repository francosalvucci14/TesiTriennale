from collections import defaultdict
import heapq

class TemporalGraph:
    def __init__(self, edges):
        # `edges` è una lista di tuple (u, v, times) dove `times` è una lista di etichette temporali
        self.graph = defaultdict(lambda: defaultdict(list))
        for u, v, times in edges:
            self.graph[u][v].extend(times)
            self.graph[v][u].extend(times)  # Poiché l'albero è non orientato
        # Ordiniamo le etichette temporali per ogni arco
        for u in self.graph:
            for v in self.graph[u]:
                self.graph[u][v].sort()

    def is_temporally_connected(self):
        nodes = list(self.graph.keys())
        for start in nodes:
            if not self.check_temporal_reachability(start):
                return False
        return True

    def check_temporal_reachability(self, start):
        # Dijkstra modificato per earliest-arrival time con etichette temporali
        earliest_arrival = {node: float('inf') for node in self.graph}
        earliest_arrival[start] = 0
        queue = [(0, start)]  # (tempo di arrivo, nodo)

        while queue:
            time, u = heapq.heappop(queue)
            if time > earliest_arrival[u]:
                continue

            for v in self.graph[u]:
                for t in self.graph[u][v]:
                    if t >= time and t < earliest_arrival[v]:
                        earliest_arrival[v] = t
                        heapq.heappush(queue, (t, v))

        # Verifica se tutti i nodi sono raggiungibili temporalmente dal nodo start
        return all(earliest_arrival[node] < float('inf') for node in self.graph)


# Esempio di utilizzo con l'albero dell'immagine
edges = [
    ('A', 'B', [1, 2]),
    ('A', 'C', [1, 3]),
    ('B', 'E', [2]),
    ('C', 'D', [3])
]

graph = TemporalGraph(edges)
print("Connettività temporalmente ordinata:", graph.is_temporally_connected())
