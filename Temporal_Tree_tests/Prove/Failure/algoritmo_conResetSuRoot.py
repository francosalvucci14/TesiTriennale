from collections import defaultdict, deque
import math

class Node:
    def __init__(self, label):
        self.label = label
        self.edges = {}

    def add_edge(self, neighbor, times):
        self.edges[neighbor] = times

def calculate_earliest_arrival_from_root(root):
    """Calcola l'EA di ciascun nodo partendo dalla radice verso le foglie."""
    ea_times = defaultdict(lambda: math.inf)
    ea_times[root] = 0  # Tempo di arrivo della radice è 0
    queue = deque([(root, 0)])  # (nodo, tempo)

    while queue:
        current, current_time = queue.popleft()
        
        for neighbor, times in current.edges.items():
            min_time = min(times)
            # Aggiorna solo se il nuovo tempo è più basso
            if ea_times[neighbor] > min_time and min_time >= current_time:
                ea_times[neighbor] = min_time
                queue.append((neighbor, min_time))

    return ea_times

def calculate_earliest_arrival_from_leaf_to_root(leaf):
    """Calcola l'EA risalendo da una foglia verso la radice."""
    ea_times = defaultdict(lambda: -math.inf)  # Inizializziamo con -inf
    ea_times[leaf] = 0  # Il tempo di arrivo della foglia è 0

    # Usando una coda per fare una visita in ampiezza (BFS)
    queue = deque([leaf])
    visited = set()

    while queue:
        current = queue.popleft()
        visited.add(current)

        for neighbor, times in current.edges.items():
            # Calcoliamo il tempo minimo tra gli archi per il vicino
            min_time = min(times)
            # Il nuovo tempo per il vicino deve essere maggiore o uguale a quello del nodo corrente
            new_time = max(min_time, ea_times[current])

            if ea_times[neighbor] < new_time:
                ea_times[neighbor] = new_time
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return ea_times


def is_temporally_connected(root):
    # Calcola EA dai sottoalberi sinistro e destro rispetto alla radice
    left_subtree, right_subtree = list(root.edges.keys())
    left_ea_times = calculate_earliest_arrival_from_root(left_subtree)
    right_ea_times = calculate_earliest_arrival_from_root(right_subtree)

    # Calcola EA risalendo verso la radice
    left_to_root_ea = calculate_earliest_arrival_from_leaf_to_root(left_subtree)
    right_to_root_ea = calculate_earliest_arrival_from_leaf_to_root(right_subtree)

    # Verifica connessione temporale tra sottoalberi
    for u in left_ea_times:
        for v in right_ea_times:
            if left_ea_times[u] > right_to_root_ea[v] or right_ea_times[v] > left_to_root_ea[u]:
                return False
    return True

# Esempio di albero
nodeA = Node('A')
nodeB = Node('B')
nodeC = Node('C')
nodeD = Node('D')
nodeE = Node('E')

nodeA.add_edge(nodeB, [1, 2])
nodeA.add_edge(nodeC, [1, 3])
nodeB.add_edge(nodeD, [2])
nodeC.add_edge(nodeE, [2])

print(is_temporally_connected(nodeA))  # Output atteso: True o False a seconda dell'albero
print(calculate_earliest_arrival_from_leaf_to_root(nodeA))
