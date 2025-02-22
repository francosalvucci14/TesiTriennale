from collections import deque
import heapq
import random
def is_temporally_connected(tree):
    """
    Verifica se un albero dato è temporalmente connesso.
    
    Args:
    tree (dict): Albero temporale rappresentato come un dizionario. 
                 La chiave è il nodo e il valore è un dizionario dei nodi vicini con le etichette temporali.
    
    Returns:
    bool: True se l'albero è temporalmente connesso, False altrimenti.
    """
    # Inizializzazione dei tempi di visita per ogni nodo
    time_visited = {node: float('inf') for node in tree}
    time_visited[next(iter(tree))] = -1  # Partiamo dal primo nodo a -1

    # Coda per BFS
    queue = deque([next(iter(tree))])  # Partiamo dal primo nodo (radice)
    
    # Propagazione dei tempi di visita utilizzando una BFS
    while queue:
        node = queue.popleft()

        # Esploriamo i vicini del nodo
        for neighbor, labels in tree[node].items():
            # Troviamo tutte le etichette temporali che sono valide per attraversare l'arco
            valid_labels = [label for label in labels if label > time_visited[node]]

            # Se esistono etichette valide, aggiorniamo il tempo del vicino
            for label in valid_labels:
                # Se il nuovo tempo di visita è più basso, aggiorniamo e aggiungiamo il vicino nella coda
                if label < time_visited[neighbor]:
                    time_visited[neighbor] = label
                    queue.append(neighbor)

    # Verifica se tutti i nodi sono stati visitati
    return all(time_visited[node] != float('inf') for node in tree)

def is_temporally_connected_1(tree):
    # tree: dizionario in cui ogni nodo ha come valore un dizionario di archi
    # root: nodo radice dell'albero
    # Esempio di `tree`: {u: {v: [t1, t2, ...], ...}, ...}

    # Inizializzazione della coda e del set di visitati
    start_node = next(iter(tree))
    queue = [(start_node, 0)]  # (nodo, tempo corrente)
    visited = set()
    visited.add(start_node)

    # BFS temporale
    while queue:
        node, t_curr = queue.pop(0)

        # Esplora tutti i nodi successori di `node`
        for neighbor, times in tree[node].items():
            # Filtra i tempi di attivazione validi (>= t_curr)
            valid_times = [t for t in times if t >= t_curr]
            if valid_times:
                min_valid_time = min(valid_times)  # Ottieni il primo tempo valido
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, min_valid_time))

    # Se tutti i nodi sono stati visitati, l'albero è temporalmente connesso
    return len(visited) == len(tree)

def is_temporally_connected_2(tree):
    """
    Verifica se un albero dato è temporalmente connesso, con complessità O(M).
    
    Args:
    tree (dict): Albero temporale rappresentato come un dizionario. 
                 La chiave è il nodo e il valore è un dizionario dei nodi vicini con le etichette temporali.
    
    Returns:
    bool: True se l'albero è temporalmente connesso, False altrimenti.
    """
    # Inizializzazione dei tempi di visita per ogni nodo
    time_visited = {node: float('inf') for node in tree}
    time_visited[next(iter(tree))] = -1  # Partiamo dal primo nodo a -1

    # Coda per BFS
    queue = deque([next(iter(tree))])  # Partiamo dal primo nodo (radice)
    
    # Propagazione dei tempi di visita utilizzando una BFS
    while queue:
        node = queue.popleft()

        # Esploriamo i vicini del nodo
        for neighbor, labels in tree[node].items():
            # Troviamo la minima etichetta temporale che è valida per attraversare l'arco
            min_label = min(labels)  # La transizione temporale più rapida (minima etichetta valida)
            
            # Se il tempo minimo dell'arco è maggiore del tempo di visita del nodo corrente, possiamo attraversarlo
            if min_label > time_visited[node]:
                if min_label < time_visited[neighbor]:
                    time_visited[neighbor] = min_label
                    queue.append(neighbor)

    # Verifica se tutti i nodi sono stati visitati
    return all(time_visited[node] != float('inf') for node in tree)

def is_temporally_connected_h(tree):
    """
    Verifica se un albero dato è temporalmente connesso, con complessità O(M log K).
    
    Args:
    tree (dict): Albero temporale rappresentato come un dizionario. 
                 La chiave è il nodo e il valore è un dizionario dei nodi vicini con le etichette temporali.
    
    Returns:
    bool: True se l'albero è temporalmente connesso, False altrimenti.
    """
    # Inizializzazione dei tempi di visita per ogni nodo
    time_visited = {node: float('inf') for node in tree}
    time_visited[next(iter(tree))] = -1  # Partiamo dal primo nodo a -1

    # Coda per BFS
    queue = deque([next(iter(tree))])  # Partiamo dal primo nodo (radice)
    
    # Propagazione dei tempi di visita utilizzando una BFS
    while queue:
        node = queue.popleft()

        # Esploriamo i vicini del nodo
        for neighbor, labels in tree[node].items():
            # Usa un heap per trovare la minima etichetta temporale
            heapq.heapify(labels)  # Trasforma la lista delle etichette in un heap
            min_label = heapq.heappop(labels)  # Estrae il minimo elemento
            
            # Se il tempo minimo dell'arco è maggiore del tempo di visita del nodo corrente, possiamo attraversarlo
            if min_label > time_visited[node]:
                if min_label < time_visited[neighbor]:
                    time_visited[neighbor] = min_label
                    queue.append(neighbor)

    # Verifica se tutti i nodi sono stati visitati
    return all(time_visited[node] != float('inf') for node in tree)

def is_temporally_connected_r(tree):
    # tree: dizionario in cui ogni nodo ha come valore un dizionario di archi
    # Esempio di `tree`: {u: {v: [t1, t2, ...], ...}, ...}

    # Se l'albero è vuoto, consideriamolo temporalmente connesso
    if not tree:
        return True

    # Scegli un nodo casuale
    root = random.choice(list(tree.keys()))

    # Inizializzazione della coda e del set di visitati
    queue = [(root, 0)]  # (nodo, tempo corrente)
    visited = set()
    visited.add(root)

    # BFS temporale
    while queue:
        node, t_curr = queue.pop(0)

        # Esplora tutti i nodi successori di `node` (considerando la bidirezionalità)
        for neighbor, times in tree[node].items():
            # Filtra i tempi di attivazione validi (>= t_curr)
            valid_times = [t for t in times if t >= t_curr]
            if valid_times:
                min_valid_time = min(valid_times)  # Ottieni il primo tempo valido
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, min_valid_time))

                # Consideriamo anche il movimento in senso opposto (bidirezionale)
                # Se l'arco è bidirezionale, aggiungi anche il nodo precedente
                for reverse_neighbor, reverse_times in tree[neighbor].items():
                    valid_reverse_times = [t for t in reverse_times if t >= t_curr]
                    if valid_reverse_times:
                        min_reverse_valid_time = min(valid_reverse_times)
                        if reverse_neighbor not in visited:
                            visited.add(reverse_neighbor)
                            queue.append((reverse_neighbor, min_reverse_valid_time))

    # Se tutti i nodi sono stati visitati, l'albero è temporalmente connesso
    return len(visited) == len(tree)

# Test con alcuni alberi temporali

albero1 = {
    'A': {'B': [1, 2], 'C': [3, 4]},
    'B': {'D': [1, 3]},
    'C': {'E': [2, 4]},
    'D': {},
    'E': {}
}

albero2 = {
    'A': {'B': [1, 2], 'C': [2, 3]},
    'B': {'D': [1, 3]},
    'C': {'E': [4, 5]},
    'D': {},
    'E': {}
}

albero3 = {
    'A': {'B': [1, 2], 'C': [3, 4, 6]},
    'B': {'D': [1, 3]},
    'C': {'E': [5, 6]},
    'D': {},
    'E': {}
}

albero4 = {
    'A': {'B': [1, 2], 'C': [2, 3]},
    'B': {'D': [1, 4]},
    'C': {'E': [3, 5]},
    'D': {},
    'E': {}
}

albero5 = {
    'A': {'B': [1, 3], 'C': [2, 4]},
    'B': {'D': [1, 4]},
    'C': {'E': [5, 6]},
    'D': {},
    'E': {}
}

albero = {
    'A' : {'B': [1,2], 'C': [4], 'D' : {5,6}},
    'D' : {'E' : [7], 'F' : [6,7]},
    'F' : {'G' : [8]},
    'G' : {'H' : [8,9,10]},
    'B' : {},
    'C' : {},
    'E' : {},
    'H' : {}
}
# Esegui i test
print(is_temporally_connected_1(albero))  # Dovrebbe restituire True
