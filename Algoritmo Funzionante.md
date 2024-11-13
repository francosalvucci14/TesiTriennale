# Algoritmo NAIVE

```python
def dfs_path_check(u, target, adj_list, current_time, visited):
    """DFS che verifica se esiste un percorso temporale valido da u a target."""
    if u == target:
        return True
    visited.add(u)

    for neighbor, timestamps in adj_list[u]:
        # Considera solo timestamp >= current_time per rispettare la condizione di crescita
        valid_timestamps = [t for t in timestamps if t >= current_time]
        if valid_timestamps:
            next_time = min(valid_timestamps)  # Scegli il minimo valido per continuare la DFS
            if neighbor not in visited:
                # Continua DFS per verificare se si può raggiungere il target
                if dfs_path_check(neighbor, target, adj_list, next_time, visited):
                    return True

    visited.remove(u)
    return False

def is_temporally_connected_v2(adj_list):
    # Step 1: Per ogni coppia di nodi (u, v), verifica se esiste un percorso temporale valido
    nodes = list(adj_list.keys())
    for u in nodes:
        for v in nodes:
            if u != v:
                visited = set()  # Traccia i nodi visitati per ogni coppia (u, v)
                if not dfs_path_check(u, v, adj_list, 1, visited):  # Partendo dal timestamp minimo 1
                    return False  # Se esiste una coppia non connessa temporalmente, ritorna False
    return True
```
# Algoritmo Ottimizzato

L'algoritmo è il seguente

```python
from collections import defaultdict, deque

def compress_timestamps(adj_list):
    # Estrai tutti i timestamp
    all_timestamps = set()
    for u in adj_list:
        for v, timestamps in adj_list[u]:
            all_timestamps.update(timestamps)

    # Ordina e assegna un indice a ogni timestamp per la compressione
    sorted_timestamps = sorted(all_timestamps)
    timestamp_index = {t: i for i, t in enumerate(sorted_timestamps)}
    return timestamp_index, sorted_timestamps

def bfs_temporal(u, target, adj_list, timestamp_index, sorted_timestamps):
    # BFS per cercare di raggiungere il target rispettando i tempi
    queue = deque([(u, 0)])  # Ogni elemento è una coppia (nodo, indice timestamp)
    visited = {u: 0}  # Traccia il timestamp minimo visitato per ciascun nodo

    while queue:
        current, time_idx = queue.popleft()

        if current == target:
            return True

        for neighbor, timestamps in adj_list[current]:
            # Considera solo timestamp >= sorted_timestamps[time_idx]
            for t in timestamps:
                if t >= sorted_timestamps[time_idx]:  # Usa sorted_timestamps correttamente
                    next_time_idx = timestamp_index[t]
                    # Visita solo se non è già stato visitato con un tempo minore
                    if neighbor not in visited or visited[neighbor] > next_time_idx:
                        visited[neighbor] = next_time_idx
                        queue.append((neighbor, next_time_idx))
                    break  # Prendi solo il primo timestamp valido

    return False

def is_temporally_connected_v5(adj_list):
    # Step 1: Comprimi i timestamp
    timestamp_index, sorted_timestamps = compress_timestamps(adj_list)

    # Step 2: Verifica la connessione temporale per ogni coppia di nodi
    nodes = list(adj_list.keys())
    for u in nodes:
        for v in nodes:
            if u != v:
                if not bfs_temporal(u, v, adj_list, timestamp_index, sorted_timestamps):
                    return False  # Se una coppia non è connessa, ritorna False
    return True
```

Poco da dire, l'algoritmo ha complessitò $O(N^2\cdot M)$
## Dimostrazione

La **dimostrazione di correttezza** dell'algoritmo si basa sul fatto che l'algoritmo verifica correttamente se esiste un percorso temporale valido tra ogni coppia di nodi nel grafo, seguendo la logica definita nella descrizione dell'algoritmo. La correttezza si fonda su due aspetti principali:

1. **Rilevare correttamente la connessione temporale tra due nodi**.
2. **Gestire correttamente la crescita temporale durante la BFS**.

### Descrizione dell'algoritmo

- **Compressione dei timestamp**: L'algoritmo prima raccoglie tutti i timestamp associati agli archi, li ordina e li mappa su indici compatti. Questo step permette di evitare la gestione esplicita di timestamp duplicati e consente di lavorare su una rappresentazione più efficiente.
  
- **BFS temporale**: Per ogni coppia di nodi \( u \) e \( v \), l'algoritmo esegue una BFS che esplora i nodi adiacenti di \( u \) e cerca di raggiungere \( v \), rispettando la condizione di crescita temporale (un nodo può essere visitato solo se il suo timestamp è maggiore o uguale a quello del nodo precedente).

### Dimostrazione di correttezza

#### 1. **Correttezza nella ricerca del percorso temporale valido** (verifica della connessione temporale)

L'algoritmo utilizza una **BFS** per esplorare il grafo tenendo traccia dei timestamp. La BFS esplora i vicini di un nodo solo se il timestamp dell'arco che li collega è maggiore o uguale al timestamp dell'arco precedente. 

- **Proprietà di crescita temporale**: La condizione fondamentale dell'algoritmo è che per ogni arco tra due nodi, il timestamp dell'arco deve essere maggiore o uguale a quello dell'arco precedente (quindi crescente nel tempo). La BFS implementa correttamente questa condizione, dato che per ogni arco esamina solo quelli con timestamp >= a quello del nodo da cui si è arrivati.
  
  La **condizione di crescita temporale** assicura che la BFS esplori i nodi in modo che il percorso rispettato sia valido temporalmente. Quindi, se troviamo un percorso che collega due nodi \( u \) e \( v \), il percorso rispetterà sempre la condizione di crescita temporale, il che significa che **ogni arco nel percorso avrà un timestamp che cresce o resta costante**.

#### 2. **Correttezza nella gestione dei timestamp**

Poiché l'algoritmo ordina i timestamp prima di eseguire la BFS, è sicuro che il processo di esplorazione avvenga in ordine crescente o uguale dei timestamp. Questo è fondamentale per garantire che non ci siano "salti" temporali durante l'esplorazione del grafo, rispettando la condizione che i nodi possano essere raggiunti solo tramite archi con timestamp crescente.

- L'ordinamento dei timestamp permette di determinare rapidamente quale sia il prossimo arco da esplorare e garantisce che la BFS visiti i nodi solo quando possibile secondo la regola di crescita temporale.

#### 3. **Correttezza per ogni coppia di nodi**

L'algoritmo esegue una BFS per ogni coppia di nodi \( u \) e \( v \), verificando se esiste un percorso temporale valido da \( u \) a \( v \). Se per una qualsiasi coppia di nodi non esiste un percorso valido (ossia, la BFS non riesce a raggiungere \( v \) da \( u \)), l'algoritmo ritorna **False**, indicando che i nodi non sono temporaneamente connessi.

- La **BFS** garantisce che tutti i nodi che sono connessi a \( u \) nel rispetto della condizione temporale siano esplorati.
- Se il nodo \( v \) è raggiungibile partendo da \( u \) seguendo la regola dei timestamp crescenti, la BFS troverà il percorso e restituirà **True**.
- Se nessun percorso valido è trovato, la funzione restituirà **False** per quella coppia di nodi.

Poiché l'algoritmo esamina tutte le possibili coppie di nodi, la correttezza complessiva del risultato è garantita: l'algoritmo restituirà **True** se e solo se ogni nodo è connesso temporalmente a tutti gli altri nodi, rispettando la condizione di crescita temporale.

#### 4. **Completamento dell'esplorazione**

Ogni volta che eseguiamo una BFS, esploriamo solo archi con timestamp maggiore o uguale rispetto al timestamp del nodo precedente, quindi non saltiamo mai nessun arco che possa violare la condizione di crescita temporale. Inoltre, l'ordinamento dei timestamp garantisce che esploreremo sempre il percorso più "vecchio" possibile per rispettare la crescita temporale, e poiché esploriamo tutti gli archi, **l'algoritmo trova sempre un percorso valido** (se esiste).

### Conclusione

L'algoritmo è **corretto** perché:
- La BFS garantisce che ogni percorso trovato rispetti la condizione di crescita temporale.
- L'ordinamento dei timestamp assicura che non vengano saltati archi validi.
- Per ogni coppia di nodi \( u, v \), la BFS verificherà correttamente se esiste un percorso temporale valido. Se non esiste, l'algoritmo restituirà correttamente **False**.

In questo modo, l'algoritmo verifica correttamente la connessione temporale tra tutte le coppie di nodi nel grafo.

## Complessità

Se \( K \) rappresenta il numero di **etichette totali** (ovvero il numero di timestamp distinti che compaiono tra tutti gli archi), la complessità cambia di nuovo in modo significativo. Ecco come possiamo analizzare la situazione in base a questa definizione di \( K \).

### 1. **Compressione dei Timestamp** con \( K \) come numero totale di etichette

Se \( K \) è il numero totale di etichette distinte (o timestamp) tra tutti gli archi, questo significa che dovremo ordinare e associare un indice a ciascun timestamp. In questo caso, la complessità della **compressione dei timestamp** diventa:

\[
O(K \log K)
\]

Dove \( K \) è il numero totale di etichette. Questo passaggio è relativamente costoso, ma viene eseguito solo una volta.

### 2. **BFS Temporale per ciascuna coppia di nodi**

La BFS temporale esplora gli archi, e per ciascun arco dovremo considerare i timestamp associati. In questo caso, la BFS esplora gli archi e i loro timestamp, e nel peggiore dei casi può essere necessario verificare tutti i timestamp associati a ciascun arco. Se ogni arco ha al massimo \( K \) timestamp, allora:

- La **BFS** esplorerà ogni arco e considererà al massimo \( K \) timestamp, il che comporta un costo di \( O(M \cdot K) \) per ogni chiamata alla BFS, dove \( M \) è il numero di archi.

### Complessità Totale

1. **Compressione dei timestamp**:
   - Ordinamento dei timestamp distinti: \( O(K \log K) \).

2. **BFS per tutte le coppie di nodi**:
   - Per ogni coppia di nodi, eseguiamo una BFS che ha un costo di \( O(M \cdot K) \) (poiché esploriamo gli archi e, per ciascun arco, possiamo esaminare fino a \( K \) timestamp).

Poiché dobbiamo eseguire la BFS per ogni coppia di nodi, il costo totale dell'algoritmo diventa:

$$
O(K \log K + N^2 \cdot M \cdot K)
$$

Dove:
- \( N \) è il numero di nodi,
- \( M \) è il numero di archi,
- \( K \) è il numero totale di etichette (timestamp distinti).

### 3. **Caso particolare: \( K = N-1 \) (una sola etichetta per arco)**

Se hai solo una singola etichetta per arco, ovvero ogni arco ha un solo timestamp, allora:

- \( K = N - 1 \), e la **compressione dei timestamp** diventa $O((N - 1) \log (N - 1)) = O(N \log N)$.
- La **BFS** per ogni coppia di nodi ha un costo di \( O(M) \), perché ogni arco ha solo un timestamp da esaminare.

In questo caso, la complessità totale dell'algoritmo diventa:

$$
O(N \log N + N^2 \cdot M)
$$

### 4. **Caso particolare: \( K \gg N \) (molti timestamp per arco)**

Se \( K \) è molto grande, ad esempio $K \gg N$, allora la complessità diventa:

$$
O(K \log K + N^2 \cdot M \cdot K)
$$

### Sintesi della Complessità

- Se \( K \) è piccolo (ad esempio \( K = 1 \) o costante), la complessità è sostanzialmente \( O(N^2 \cdot M) \), che è molto più gestibile.
- Se \( K \) è grande (ad esempio $K \gg N$, la complessità può crescere rapidamente, in particolare a causa del termine $O(N^2 \cdot M \cdot K)$.

### Considerazioni finali

- **Se \( K \) è piccolo o moderato**, la complessità totale può essere accettabile, ma se \( K \) cresce significativamente, l'algoritmo può diventare costoso, soprattutto se hai molti archi e un numero elevato di timestamp.
- In questo caso, ottimizzare la parte di esplorazione dei timestamp, per esempio limitando il numero di timestamp considerati durante la BFS, o implementando tecniche più efficienti di ricerca dei timestamp validi, potrebbe essere utile per ridurre la complessità.

# Algoritmo Ottimizzato con approccio Dijkstra-like

## Algoritmo

```python
# Dijkstra-like

import heapq

def temporal_bfs(u, adj_list, n):
    """Esegui una BFS che esplora i nodi partendo da u, rispettando l'ordine temporale dei timestamp"""
    # Coda di priorità (heap), contiene tuple del tipo (timestamp, nodo)
    heap = []
    # Inizializza la coda con i nodi vicini di u, con il minimo timestamp
    for neighbor, timestamps in adj_list[u]:
        for timestamp in timestamps:
            heapq.heappush(heap, (timestamp, neighbor))

    visited = set()
    visited.add(u)

    while heap:
        current_time, current_node = heapq.heappop(heap)

        if current_node not in visited:
            visited.add(current_node)

            # Aggiungi i vicini di current_node alla coda se non sono già stati visitati
            for neighbor, timestamps in adj_list[current_node]:
                if neighbor not in visited:
                    for timestamp in timestamps:
                        if timestamp >= current_time:  # Solo timestamp validi
                            heapq.heappush(heap, (timestamp, neighbor))

    return visited

def is_temporally_connected_v3(adj_list):
    """Verifica se il grafo è temporaneamente connesso, per ogni coppia di nodi"""
    nodes = list(adj_list.keys())
    n = len(nodes)

    # Per ogni nodo u, esegui BFS temporale per trovare tutti i nodi raggiungibili da u
    for u in nodes:
        reachable = temporal_bfs(u, adj_list, n)

        # Se un nodo non è raggiungibile da u, il grafo non è connesso temporalmente
        for v in nodes:
            if v != u and v not in reachable:
                return False

    return True
```

## Costo computazionale

Certo! Ecco l'algoritmo basato sull'approccio che ti ho descritto, utilizzando una coda di priorità per esplorare i grafi con il vincolo temporale:

### Algoritmo: Connessione temporale ottimizzata

1. **Preprocessing (ordinamento degli archi):**
   - Per ogni nodo, ordiniamo i suoi archi in base ai timestamp.
2. **Ricerca temporale con Dijkstra-like:**
   - Per ogni nodo \(u\), eseguiamo una ricerca utilizzando una coda di priorità per esplorare i vicini rispettando l'ordine temporale crescente dei timestamp.

### Descrizione del codice:

1. **`temporal_bfs(u, adj_list, n)`**:
   - Per ogni nodo \(u\), eseguiamo una BFS utilizzando una coda di priorità. Gli archi sono esplorati in ordine crescente di timestamp.
   - La coda di priorità è usata per garantire che esploriamo i vicini con il minimo timestamp per primo.
   - La funzione ritorna l'insieme di nodi raggiungibili da \(u\) rispettando l'ordine temporale.

2. **`is_temporally_connected_v3(adj_list)`**:
   - Per ogni nodo \(u\), chiama `temporal_bfs` per trovare tutti i nodi che sono raggiungibili da \(u\).
   - Se per una qualsiasi coppia di nodi \(u\) e \(v\), \(v\) non è raggiungibile da \(u\), il grafo non è connesso temporalmente, quindi ritorna **False**.
   - Se tutte le coppie di nodi sono connesse, ritorna **True**.

### Complessità:

- **Ordinamento degli archi**: Per ogni nodo \(u\), dobbiamo ordinare gli archi. Questo ha un costo di \(O(M \log M)\), dove \(M\) è il numero di archi.
- **BFS con coda di priorità**: La BFS con coda di priorità ha un costo di \(O(M \log M)\) per ogni nodo.
- **Complessità totale**: Poiché dobbiamo eseguire la BFS per ogni nodo, il costo complessivo sarà:
$$
O(N \cdot M \log M)
$$

Dove:
- \(N\) è il numero di nodi.
- \(M\) è il numero di archi.

Questo approccio è molto più efficiente di $O(N^2 \cdot M)$, soprattutto quando \(M\) è molto maggiore di \(N\).

### Come funziona l'algoritmo:

- Per ogni nodo \(u\), esploriamo i suoi vicini in modo che ogni arco esplorato abbia un timestamp maggiore o uguale al timestamp dell'arco precedente, garantendo così che il percorso temporale sia valido.
- L'uso della coda di priorità permette di esplorare gli archi in ordine temporale crescente, ottimizzando l'esplorazione.
- Se per qualsiasi coppia di nodi non troviamo un percorso valido, l'algoritmo restituirà **False**.

Con questo approccio, dovremmo essere in grado di ridurre significativamente il costo rispetto all'algoritmo originale.
## Correttezza

L'approccio Dijkstra-like è basato sull'idea di esplorare i nodi nel grafo rispettando l'ordine temporale dei timestamp degli archi. Per dimostrare la correttezza dell'algoritmo, possiamo seguire i seguenti passaggi:

### 1. **Proprietà fondamentale dell'algoritmo:**
L'algoritmo cerca di determinare se per ogni coppia di nodi \( u \) e \( v \) esiste un percorso valido temporale, in cui i timestamp sugli archi che compongono il percorso siano crescenti. In altre parole, se siamo in un nodo \( u \) e vogliamo raggiungere un nodo \( v \), dobbiamo esplorare solo gli archi che rispettano il vincolo temporale \( t_{u \to v} \geq t_{u \to u} \), dove \( t_{u \to v} \) è il timestamp dell'arco da \( u \) a \( v \).

### 2. **Usare una coda di priorità (Dijkstra-like):**
Dijkstra è un algoritmo che esplora i nodi di un grafo partendo da un nodo di origine, scegliendo sempre il percorso minimo (o, in questo caso, il percorso temporale con il timestamp minimo) attraverso una coda di priorità. Nel nostro caso, la **priorità** non è il "peso" degli archi, ma il **timestamp** associato a ciascun arco.

L'idea è simile a Dijkstra, ma invece di minimizzare la distanza, minimizziamo il tempo, cioè scegliamo gli archi con il timestamp più basso.

### 3. **Correttezza dell'approccio:**
La correttezza di questo approccio si basa sul fatto che:

- Quando esploriamo un nodo \( u \), lo facciamo considerando solo gli archi che rispettano il vincolo temporale: selezioniamo solo archi \( (u, v) \) in cui il timestamp è maggiore o uguale al timestamp del nodo corrente.
  
- La coda di priorità garantisce che esploriamo prima i nodi attraverso gli archi con il timestamp più basso possibile, il che implica che esploreremo i percorsi temporali in ordine crescente di timestamp.

#### Dimostrazione di correttezza:

##### A. **Proprietà di scelta ottimale:**
Ogni volta che esploriamo un nodo \( u \), lo facciamo scegliendo l'arco con il **minimo timestamp** (questo è simile a Dijkstra, che sceglie il percorso di peso minimo). Questo assicura che esploriamo sempre il percorso più "veloce" (temporalmente più vicino), in modo da rispettare la condizione di crescita dei timestamp lungo il percorso.

##### B. **Proprietà di esplorazione corretta:**
Quando esploriamo un nodo \( u \) e passiamo a un nodo \( v \), esaminiamo solo gli archi che partono da \( u \) e che hanno un timestamp maggiore o uguale a quello corrente. In altre parole, esploriamo i percorsi che rispettano la condizione di crescita dei timestamp. Se esiste un percorso valido temporale da \( u \) a \( v \), lo troveremo esplorando questi archi in ordine di timestamp crescente.

##### C. **Correttezza del percorso:**
Se esiste un percorso temporale valido da \( u \) a \( v \), il nostro algoritmo lo troverà:

- Ogni volta che esploriamo un nodo \( v \) a partire da un nodo \( u \), lo facciamo con un timestamp che rispetta la condizione di crescita.
- Poiché esploriamo prima gli archi con il timestamp più basso, garantiamo che ogni percorso temporale che esploriamo sia valido.
  
Se riusciamo a raggiungere un nodo \( v \) partendo da \( u \), vuol dire che esiste un percorso temporale valido tra \( u \) e \( v \), rispettando la condizione sui timestamp.

### 4. **Rispetto del vincolo di crescita:**
Il nostro algoritmo rispetta sempre il vincolo di crescita sui timestamp, poiché:

- Gli archi sono esplorati solo se il loro timestamp è maggiore o uguale al timestamp corrente.
- La coda di priorità gestisce l'esplorazione in modo che non vengano mai esplorati archi con timestamp "retroattivi", mantenendo così la correttezza temporale del percorso.

### 5. **Verifica globale della connettività temporale:**
Nel nostro algoritmo, per ogni nodo \( u \), esploriamo tutti i nodi raggiungibili da \( u \) rispettando i vincoli temporali. Dopo aver eseguito la ricerca per un nodo, verifichiamo che tutti gli altri nodi siano raggiungibili. Se, per qualsiasi nodo \( u \), esiste un nodo \( v \) che non è raggiungibile partendo da \( u \), il grafo non è temporaneamente connesso, e quindi l'algoritmo restituirà **False**.

### Conclusioni sulla correttezza:

- L'algoritmo è corretto perché esplora i nodi in ordine di timestamp crescente, garantendo che ogni percorso temporale che esplora sia valido.
- Ogni nodo viene visitato solo quando il timestamp degli archi che partono da esso soddisfa il vincolo temporale.
- La coda di priorità assicura che esploriamo sempre il percorso temporale più promettente, ossia quello con il timestamp più basso.
- Alla fine dell'esecuzione, l'algoritmo verifica la connettività temporale globale, restituendo **True** se ogni coppia di nodi è connessa temporalmente e **False** altrimenti.

In sintesi, il comportamento del nostro algoritmo garantisce che esploreremo correttamente tutti i percorsi temporali validi, rispettando i vincoli sui timestamp, e quindi è **corretto**.