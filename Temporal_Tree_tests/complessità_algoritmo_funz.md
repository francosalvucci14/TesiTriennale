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
