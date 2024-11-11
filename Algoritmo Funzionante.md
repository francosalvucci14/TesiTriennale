
Rivediamo l'analisi del costo totale tenendo conto di M e K grandi:

- **Ordinamento degli archi globalmente**:
	- Abbiamo $M$ etichette temporali totali da ordinare, quindi l'ordinamento di tutti gli archi basato su queste etichette ha un costo di $O(M\log M)$, dove $M$ è il numero totale di etichette temporali (ossia la somma delle etichette di tutti gli archi).
- **Creazione della lista sorted_edges_for_node**:
    - In questa fase, stiamo solo raggruppando gli archi per ciascun nodo, quindi il costo di questa operazione è $O(M)$, poiché dobbiamo processare tutte le etichette temporali.
- **DFS (Depth-First Search)**:
    - La DFS esplora ogni arco e, di conseguenza, ogni etichetta temporale. Poiché ogni arco ha associato uno o più tempi, e ci sono $M$ etichette temporali totali, la DFS ha un costo di $O(M)$.
- **Verifica dei percorsi temporali tra coppie di nodi**:
    - La parte di verifica tra tutte le coppie di nodi $(u,v)$ ha un costo di $O(N^2)$, dove $N$ è il numero di nodi nel grafo.

Complessità totale:

Poiché $M$ è molto maggiore di $N$, possiamo ignorare la parte $O(N^2)$ se $M$ è sufficientemente grande. Il costo totale quindi diventa:
$$O(M\log M)+O(M)+O(N^2)$$

Nel caso peggiore, se $M$ cresce molto rispetto a $N$, il termine dominante sarà $O(M\log M)$. Quindi la complessità finale sarà: $O(M\log M)$

Conclusione:

Quando $M\gt\gt N$(ossia, il numero di etichette temporali è molto grande rispetto al numero di nodi), la complessità dell'algoritmo sarà principalmente dominata dal termine $O(M\log M).$

**Algoritmo**

```python
from collections import defaultdict

def is_temporally_connected_opt(n, edges):
    # Creazione della lista di adiacenza con archi e tempi
    adj_list = defaultdict(list)

    # Aggiungi gli archi alla lista di adiacenza
    for u, v, times in edges:
        for t in times:
            adj_list[u].append((v, t))
            adj_list[v].append((u, t))

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
print(f"L'albero è temporalmente connesso? : {is_temporally_connected_opt(n2, tree2)}")
```

