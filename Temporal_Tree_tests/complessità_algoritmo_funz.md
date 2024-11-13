# Algoritmo 1

Rivediamo l'analisi del costo totale tenendo conto di M e K grandi:

    - Ordinamento degli archi globalmente:
        - Abbiamo M etichette temporali totali da ordinare, quindi l'ordinamento di tutti gli archi basato su queste etichette ha un costo di O(MlogM), dove M è il numero totale di etichette temporali (ossia la somma delle etichette di tutti gli archi).
    - Creazione della lista sorted_edges_for_node:
        - In questa fase, stiamo solo raggruppando gli archi per ciascun nodo, quindi il costo di questa operazione è O(M), poiché dobbiamo processare tutte le etichette temporali.
    - DFS (Depth-First Search):
        - La DFS esplora ogni arco e, di conseguenza, ogni etichetta temporale. Poiché ogni arco ha associato uno o più tempi, e ci sono MM etichette temporali totali, la DFS ha un costo di O(M).
    - Verifica dei percorsi temporali tra coppie di nodi:
        - La parte di verifica tra tutte le coppie di nodi (u,v) ha un costo di O(N^2), dove N è il numero di nodi nel grafo.

Complessità totale:

Poiché M è molto maggiore di N, possiamo ignorare la parte O(N^2) se M è sufficientemente grande. Il costo totale quindi diventa:
O(Mlog⁡M)+O(M)+O(N2)
O(MlogM)+O(M)+O(N2)

Nel caso peggiore, se MM cresce molto rispetto a NN, il termine dominante sarà O(Mlog⁡M)O(MlogM). Quindi la complessità finale sarà:
O(Mlog⁡M)
O(MlogM)
Caso particolare con KK etichette per arco:

Se KK è molto grande, ogni arco avrà KK etichette temporali, e quindi MM sarà proporzionale a K×EK×E, dove EE è il numero di archi. Quindi in questo caso:

    Il numero totale di etichette temporali MM cresce linearmente con KK e EE, quindi la complessità complessiva diventa:

O(K×Elog⁡(K×E))+O(K×E)
O(K×Elog(K×E))+O(K×E)

Nel caso in cui MM (che è K×EK×E) è molto grande, la complessità diventa dominata da O(Mlog⁡M)O(MlogM).
Conclusione:

    Quando M≫NM≫N (ossia, il numero di etichette temporali è molto grande rispetto al numero di nodi), la complessità dell'algoritmo sarà principalmente dominata dal termine O(Mlog⁡M)O(MlogM).
    Se KK è molto grande, ciò comporterà un aumento proporzionale di MM (dato che M=K×EM=K×E), ma la complessità totale rimarrà comunque O(Mlog⁡M)O(MlogM), dove MM è il numero totale di etichette temporali.

In sintesi, se MM cresce molto rispetto a NN, il costo dominante sarà O(Mlog⁡M)O(MlogM).

# Algoritmo 2

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

\[
O(K \log K + N^2 \cdot M \cdot K)
\]

Dove:
- \( N \) è il numero di nodi,
- \( M \) è il numero di archi,
- \( K \) è il numero totale di etichette (timestamp distinti).

### 3. **Caso particolare: \( K = N-1 \) (una sola etichetta per arco)**

Se hai solo una singola etichetta per arco, ovvero ogni arco ha un solo timestamp, allora:

- \( K = N - 1 \), e la **compressione dei timestamp** diventa \( O((N - 1) \log (N - 1)) = O(N \log N) \).
- La **BFS** per ogni coppia di nodi ha un costo di \( O(M) \), perché ogni arco ha solo un timestamp da esaminare.

In questo caso, la complessità totale dell'algoritmo diventa:

\[
O(N \log N + N^2 \cdot M)
\]

### 4. **Caso particolare: \( K \gg N \) (molti timestamp per arco)**

Se \( K \) è molto grande, ad esempio \( K \gg N \), allora la complessità diventa:

\[
O(K \log K + N^2 \cdot M \cdot K)
\]

### Sintesi della Complessità

- Se \( K \) è piccolo (ad esempio \( K = 1 \) o costante), la complessità è sostanzialmente \( O(N^2 \cdot M) \), che è molto più gestibile.
- Se \( K \) è grande (ad esempio \( K \gg N \)), la complessità può crescere rapidamente, in particolare a causa del termine \( O(N^2 \cdot M \cdot K) \).

### Considerazioni finali

- **Se \( K \) è piccolo o moderato**, la complessità totale può essere accettabile, ma se \( K \) cresce significativamente, l'algoritmo può diventare costoso, soprattutto se hai molti archi e un numero elevato di timestamp.
- In questo caso, ottimizzare la parte di esplorazione dei timestamp, per esempio limitando il numero di timestamp considerati durante la BFS, o implementando tecniche più efficienti di ricerca dei timestamp validi, potrebbe essere utile per ridurre la complessità.