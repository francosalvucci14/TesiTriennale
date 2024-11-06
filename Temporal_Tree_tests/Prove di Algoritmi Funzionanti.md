Da rivedere

Prova tempo $O(M)$

```python
import random
from collections import defaultdict, deque

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
```

Prova 2, algoritmo bidirezionale tempo $O(M)$

```python
def is_bidirectionally_temporally_connected(tree):
    def bfs_connectivity(tree, start_node):
        reachable_times = defaultdict(set)  # Tracciamo i tempi di arrivo per ogni nodo
        reachable_times[start_node].add(0)  # Il nodo iniziale è raggiungibile al tempo 0
        queue = deque([(start_node, 0)])  # Ogni elemento della coda è una tupla (nodo, tempo)

        while queue:
            node, current_time = queue.popleft()

            for neighbor, times in tree[node].items():
                # Troviamo tutti i tempi validi per raggiungere il nodo successivo
                valid_times = [t for t in times if t >= current_time]

                for next_time in valid_times:
                    # Se il tempo di arrivo non è già stato considerato per il vicino
                    if next_time not in reachable_times[neighbor]:
                        reachable_times[neighbor].add(next_time)
                        queue.append((neighbor, next_time))

        # Verifica che tutti i nodi siano stati raggiunti almeno a un tempo valido
        return all(len(times) > 0 for times in reachable_times.values())

    # Scegliamo un nodo di partenza casuale
    start_node = random.choice(list(tree.keys()))

    # Controlliamo la connettività nel grafo originale
    if not bfs_connectivity(tree, start_node):
        return False

    # Creiamo il grafo inverso
    reversed_tree = defaultdict(dict)
    for node, neighbors in tree.items():
        for neighbor, times in neighbors.items():
            reversed_tree[neighbor][node] = times

    # Controlliamo la connettività nel grafo inverso
    return bfs_connectivity(reversed_tree, start_node)
```

L'algoritmo parte da un nodo qualunque dell'albero, e fa partire l'algoritmo bge_connectivity, che controlla se l'albero è temporalmente connesso in direzione top-down, poi l'labero viene rigirato, e si vede se è temporalmente connesso in direzione bottom-up. se entramte sono vere l'algoritmo ritorna true altrimenti false.