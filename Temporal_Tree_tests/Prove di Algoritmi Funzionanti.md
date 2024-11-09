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

# Considerazioni

- Per dire che fra due nodi u e v esiste un percorso temporale, basta vedere solo u->v e non il viceversa,perchè i tempi di attivazione sono in ordine crescente
- Oppure serve un'approccio sia top-down che bottom-up?? **da chiedere**
    - I percorsi temporali devono essere intesi come bidirezionali, quindi da U a V e da V a U, oppure solo da una direzione?
- Posso dire che un albero è temporalmente connesso se, facendo partire la BFS temporale dalla radice dell'albero, si toccano tutti i nodi??? **da chiedere**
- Se aun solo percorso da u a v non rispetta la proprietà temporale, posso affermare con certezza che l'albero non è temporalmente connesso? prob. si perchè se esiste un percorso di questo tipo, allora esisterà un nodo singolo che non si può connettere con gli altri, in teoria
- Proabile approccio DP??
- Il costo deve essere $O(M)$ con M= numero di archi, Oppure M= numero di percorsi temporali totali?
    - Con la seconda, prob. problema NP-Hard 

# Osservazioni

1. Cammino unidirezionale, perchè con grafo con etichette di attivazione i cammini sono non-strict
2. Temporalmente connesso, **bidirezionale**
3. Non basta fare BFS temporale, ma bisogna entrambe le direzioni
4. Non baste vedere se un nodo raggiunge tutti e tutti raggiungio lui per confermare l'algoritmo
5. Per ogni nodo EA arrivando da sopra o da uno dei rami, probabile
6. Verificare questo se approccio Prog. Din.
	1. il sott-alb sx è temporamente connesso
	2. il sotto-alb dx tempr connesso
	3. verificare che ogni nodo da sx raggiunga ogni ndo da dx e viceversa
7. Array ordinato di etichette per arco, poi binsearch
8. Se prendiamo $n$ = numero di nodi e $M$ = numero di archi, sappiamo che $M\gt n$, riusciamo a fare un'algoritmo in tempo $O(M\log(n))$ 
	1. Se faccio come (7), ottengo un tempo pari a $O(n^2\log(M))$ 

Altra domanda, La condizione di crescita incrementale si resetta alla radice??
Mi spiego, guardiamo questa foto

![[ProvaAlberoTemporale.png]]
immaginiamo l'arco tra A e B con $[1,2]$

Se la condizione incrementale si resetta alla radice, allora per dire che l'albero è temporalmente connesso basta vedere se le etichette rispettano le condizioni incrementali sia dall'alto che dal basso, passando per la radice quando vediamo i percorsi da sx a dx e viceversa.

- L'osservazione è che se un nodo parte al tempo es. $t=3$, non può arrivare su un'altro nodo al tempo $t=2$, il tempo deve essere sempre incrementale, quindi molto probabilmente la condizione non si va a resettare sulla radice

Se invece non si resetta, allora per essere temporalmente connesso bisogna che tutte le etichette abbiano valore massimo uguale al max tra tutte le etichette
- Prima trovi il max tra tutte le etichette con scan lineare tempo $O(M)$, dopo aver ordinato le etichette in senso crescente
- Poi BinSearch
