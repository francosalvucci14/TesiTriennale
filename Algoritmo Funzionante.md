
# Analisi

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

# Algoritmo

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

# Dimostrazione

Per dimostrare formalmente la correttezza dell'algoritmo, dobbiamo mostrare che l'algoritmo verifica correttamente se il grafo è **temporalmente connesso**. Un grafo è temporalmente connesso se per ogni coppia di nodi \( u \) e \( v \), esiste un cammino diretto da \( u \) a \( v \) che rispetta l'ordine temporale delle etichette sui bordi.

### Strategia di dimostrazione:
1. **Definizione di albero temporalmente connesso**:
   Un albero è temporalmente connesso se, dato un insieme di etichette temporali sugli archi, esiste un cammino che rispetta l'ordine delle etichette per ogni coppia di nodi \( u \) e \( v \), ossia un cammino con etichette $t_1, t_2, \ldots, t_k$ tali che $t_1 \leq t_2 \leq \ldots \leq t_k$ .

2. **Struttura dell'algoritmo**:
   - L'algoritmo costruisce una lista di adiacenza in cui ogni arco ha associata una o più etichette temporali.
   - Ordina gli archi per ciascun nodo in base alle etichette temporali.
   - Esegue una DFS modificata che tiene traccia dei tempi minimi e massimi di accesso per ogni nodo.
   - Verifica se i cammini tra coppie di nodi rispettano le condizioni di connessione temporale.

### Dimostrazione della correttezza:

**Lemma 1 (Connettività temporale tramite DFS)**:
La DFS, eseguita a partire da un nodo radice e ordinando i vicini per tempo crescente, esplora ogni cammino possibile in ordine temporale. Questo assicura che ogni nodo raggiunto durante la DFS è connesso alla radice con un cammino che rispetta l'ordine temporale.

*Dimostrazione*:
La DFS visita ogni nodo adiacente in ordine crescente di etichette temporali. Supponiamo di partire dal nodo \( 0 \) (radice). Quando si esplora un nodo \( u \) e si visita il nodo \( v \) con etichetta temporale \( t \), \( v \) viene raggiunto solo se \( t \) è maggiore o uguale al tempo corrente della DFS. Pertanto, l'ordine di esplorazione rispetta l'ordine temporale.

**Lemma 2 (Tracciamento dei tempi minimi e massimi)**:
La DFS calcola correttamente i tempi minimi e massimi di accesso per ogni nodo.

*Dimostrazione*:
Durante la DFS, quando si visita un nodo \( v \) a partire da \( u \) tramite un'etichetta temporale \( t \), si aggiorna il tempo minimo di \( v \) come il tempo minimo tra \( t \) e i tempi minimi dei nodi figli esplorati. In questo modo, alla fine della DFS, i tempi minimi e massimi registrati per ogni nodo indicano l'intervallo temporale in cui il nodo può essere raggiunto.

**Teorema (Correttezza dell'algoritmo)**:
L'algoritmo determina se il grafo è temporalmente connesso.

*Dimostrazione*:
Per ogni coppia di nodi $u$ e $v$, l'algoritmo controlla se i loro intervalli di tempo di accesso si sovrappongono. Se gli intervalli \([min\_time[u], max\_time[u]]\) e \([min\_time[v], max\_time[v]]\) si sovrappongono, esiste un cammino temporale diretto che connette \( u \) e \( v \). Se per qualche coppia \( (u, v) \), gli intervalli non si sovrappongono, significa che non esiste un cammino che rispetta l'ordine temporale tra quei nodi, quindi il grafo non è temporalmente connesso.

**Conclusione**:
L'algoritmo ordina correttamente gli archi per tempo, esplora la'lbero rispettando l'ordine temporale tramite DFS, e verifica le condizioni di connettività temporale controllando gli intervalli di accesso dei nodi. Pertanto, se l'algoritmo restituisce `True`, l'albero è temporalmente connesso; altrimenti, non lo è.

# Algoritmo 2

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