from collections import defaultdict

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [False] * (2 * n)

    def update(self, start, end, val, node=1, left=0, right=None):
        if right is None:
            right = self.n - 1
        if start > right or end < left:
            return
        if start <= left and end >= right:
            self.tree[node] = val
            return
        mid = (left + right) // 2
        self.update(start, end, val, 2 * node, left, mid)
        self.update(start, end, val, 2 * node + 1, mid + 1, right)
        self.tree[node] = self.tree[2 * node] or self.tree[2 * node + 1]

    def query(self, start, end, node=1, left=0, right=None):
        if right is None:
            right = self.n - 1
        if start > right or end < left:
            return False
        if start <= left and end >= right:
            return self.tree[node]
        mid = (left + right) // 2
        return self.query(start, end, 2 * node, left, mid) or self.query(start, end, 2 * node + 1, mid + 1, right)

def dfs_up(adj_list, min_times, max_times, node, parent, current_time):
    min_time = current_time
    max_time = current_time

    for neighbor, time in sorted(adj_list[node], key=lambda x: x[1]):
        if neighbor != parent:
            min_child, max_child = dfs_up(adj_list, min_times, max_times, neighbor, node, time)
            min_time = min(min_time, min_child)
            max_time = max(max_time, max_child)

    min_times[node] = min_time
    max_times[node] = max_time
    return min_time, max_time

def is_temporally_connected_optimized(n, edges):
    # Crea la lista di adiacenza
    adj_list = defaultdict(list)
    for u, v, times in edges:
        for t in times:
            adj_list[u].append((v, t))
            adj_list[v].append((u, t))

    # Calcola i tempi minimi e massimi per ogni nodo
    min_times = [float('inf')] * n
    max_times = [-float('inf')] * n
    dfs_up(adj_list, min_times, max_times, 0, -1, float('-inf'))

    # Trova il massimo tempo
    max_time = max(max(t for _, _, times in edges) for _, _, _ in edges)

    # Costruisci l'albero segmentato
    segment_tree = SegmentTree(max_time + 1)

    # Inserisci gli intervalli nell'albero segmentato
    for node, (min_time, max_time) in enumerate(zip(min_times, max_times)):
        segment_tree.update(min_time, max_time, True, 1, 0, max_time)

    # Verifica la connessione temporale
    for u in range(n):
        for v in range(u + 1, n):
            if segment_tree.query(min_times[v], max_times[v], 1, 0, max_time):
                return False

    return True

tree = [
    (0, 1, [2,6]), 
    (0, 2, [6]),    
    (1, 3, [1,2,3,4,5,6]),
    (2,4,[6])          
]
n2 = 5
print(is_temporally_connected_optimized(n2, tree))  # True