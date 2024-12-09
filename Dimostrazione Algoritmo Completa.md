```table-of-contents
title: 
style: nestedOrderedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
hideWhenEmpty: true # Hide TOC if no headings are found
debugInConsole: false # Print debug info in Obsidian console
```
# Algoritmo

## Versione alberi binari

L'algoritmo è diviso in due fasi
- Preprocessing
- Check finale

La **fase di preprocessing** è la fase che calcola, con approccio bottom-up, l'$EA_{\max}$ e il $T_\max$ di ogni sottoalbero fino alla radice. Ogni volta che risalgo di livello, propago le informazioni dai figli di $u$ fino a $u$ , e combino le informazioni che ho ottenuto con i valori sul nodo $u$.

Quando l'algoritmo risale alla radice, per ogni sottoalbero  avremo calcolato correttamente i valori $EA$ e $T_\max$. 

I valori $EA$ e $T_\max$ sono definiti così : 
- $EA_\max$ : $\max_{f:\text{ f è foglia}}EA$ da $f\in T_v$ fino al padre di $v$
- $T_\max$ : Istante di tempo $t$ tale che se arrivo al padre di $v$ a tempo $\leq t$ allora riesco a visitare tutto $T_v$
- $T_v$ : sottoalbero radicato nel nodo $v$
E vengono calcolati dall'algoritmo in questo modo : 
- Il valore dell'$EA$ è uguale al massimo dei minimi timestamp di ogni livello
- Il valore del $T_\max$ è uguale al minimo dei massimi timestamp di ogni livello

Una volta eseguita la fase 1, verranno ritornati due dizionari, uno per l'$EA$ e uno per il $T_\max$
Usando poi questi dizionari, passiamo in fase 2 per il check della temporal connectivity

Pseudocodice del preprocessing

```pseudo
\begin{algorithm}
\caption{Procedura Preprocessing}
\begin{algorithmic}
\Require $L_v$ : Lista timestamp arco entrante in $v$
\Require Dizionario $D_{EA}$,Dizionario $D_{Tmax}$
\Procedure{Preprocessing}{Albero $T$}
      \If{$v$ è Nullo}
	      \Return $-\infty,\infty,D_{EA}=\emptyset,D_{Tmax}=\emptyset$
      \EndIf
	      \If{$v$ è foglia}
		      \Return $L_v[1],L_v[n],D_{EA},D_{Tmax}$
          \EndIf
          \State $min_{sx},max_{sx}=$ Preprocessing($sx(v)$)
          \State $min_{dx},max_{dx}=$ Preprocessing($dx(v)$)
          \State $EA=\max(min_{sx},min_{dx})$
          \State $Tmax=\min(max_{sx},max_{dx})$
          \State NextEA = BinarySearch($L_v,EA$)
          \State NextTime = BinarySearch($L_v,Tmax$)
          \If{NextEA $=-1\lor$NextTime=$-1$}
	          \Return $\infty,\infty$
          \EndIf
          \State minTime = $\min(Tmax,L_v[n])$
          \State $D_{EA}(v)$=NextEA 
          \Comment{Aggiungo al dizionario EA la coppia (nodo v:NextEA) [chiave,valore]}
          \State $D_{Tmax}(v)$=minTime
          \Comment{Stessa cosa del dizionario EA}
          \Return NextTime,minTime,$D_{EA},D_{Tmax}$
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```

La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA_{sx}\leq T_{\max,dx}\land EA_{dx}\leq T_{\max,sx}\quad(1)$$

Se usando i valori ottenuti in fase 1 questa condizione viene verificata per ogni sottoalbero, allora posso affermare che l'albero è temporalmente connesso, altrimenti se almeno un sottoalbero non mi verifica la condizione, affermo che l'albero non è temporalmente connesso.

Pseudocodice fase 2
```pseudo
\begin{algorithm}
\caption{Procedura Check Temporal Connectivity}
\begin{algorithmic}
\Procedure{CheckTemporalConnectivity}{$D_{EA},D_{Tmax}$}
\State Controllo in modo ricorsivo la condizione di temporal connectivity per ogni sottoalbero, usando man mano i valori all'interno dei due dizionari.
\State Check = False
\ForAll{nodo $v$}
\State $EA(v),Tmax(v)=D_{EA}.get(v),D_{Tmax}.get(v)$
\If{$EA(v)\leq Tmax(v)$}
\State Check=True
\Else
\State Check=False
\State Se Check diventa False, significa che un sottoalbero non rispetta la condizione, quindi esco subito dal ciclo e ritorno Check
\Return False
\EndIf
\EndFor
\Return Check
\EndProcedure
\end{algorithmic}
\end{algorithm}
```
L'algoritmo completo sarà quindi il seguente
```pseudo
\begin{algorithm}
\caption{Algoritmo per Alberi Binari}
\begin{algorithmic}
\Require Dizionario $D_{EA}$,Dizionario $D_{Tmax}$
\Procedure{Algoritmo}{Albero $T$}

\State $D_{EA},D_{Tmax}=$Preprocessing($T$)
\State Check = CheckTemporalConnectivity($D_{EA},D_{Tmax}$)
\If{Check = $True$}
\Return Albero Temporalmente Connesso
\Else
\Return Albero Non Temporalmente Connesso
\EndIf
\EndProcedure
\end{algorithmic}
\end{algorithm}
```
## Versione alberi non binari

Mettere algoritmo in due fasi
- preprocessing
- check finale

Pseudocode qui

```pseudo
\begin{algorithm}
\caption{Algoritmo per Alberi Non Binari}
\begin{algorithmic}

\end{algorithmic}
\end{algorithm}
```
```pseudo
\begin{algorithm}
\caption{Procedura Preprocessing}
\begin{algorithmic}

\end{algorithmic}
\end{algorithm}
```
La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA\leq T_{\max},\forall EA,T_\max\quad(2)$$

Se usando i valori ottenuti in fase 1 questa condizione viene verificata per ogni sottoalbero, allora posso affermare che l'albero è temporalmente connesso, altrimenti se almeno un sottoalbero non mi verifica la condizione, affermo che l'albero non è temporalmente connesso.
```pseudo
\begin{algorithm}
\caption{Procedura Check Temporal Connectivity}
\begin{algorithmic}

\end{algorithmic}
\end{algorithm}
```
# Dimostrazione

La dimostrazione verrà fatta per alberi non binari, in quanto per gli alberi binari basta minimizzare tutto a un fattore $2$

Abbiamo che la fase 1 impiega tempo $\Theta(N\log(M))$, in quanto per ogni nodo calcola $EA$ e $T_\max$, sfruttando l'ordinamento degli archi.
Quindi per ogni nodo, le informazioni  vengono propagante verso l'alto, fino a raggiungere la radice.

Vediamo la fase 2: 
Per ogni sottoalbero, viene effettuata la seguente verifica

Consideriamo un nodo $u$ con i suoi figli : 
- $\forall\space EA(v)$ con $v$ figlio di $u$ eseguiamo le seguenti operazioni
	- Elimino dal dizionario $D_{Tmax}$ il $T_\max(v)$ corrispondente all'$EA(v)$ appena preso,e questo mi costa $\log(\Delta_u)$
	- Trovo il minimo $T_\max$ tra tutti i figli $v_i$ di $u$, mi costa $\log(\Delta_u)$
	- Eseguo il check tra $EA_v$ e $T_{\max,\text{minimo}}$ e costa $O(1)$
	- Riaggiungo il valore $T_\max(v)$ eliminato prima nel dizionario corrispondente, costo $\log(\Delta_u)$

Adesso, preso 
- $\delta_u$ = num. di figli del nodo $u$
- $\Delta_u$ = num. di valori $T_\max$ del nodo $u$
Abbiamo che il costo totale dell'algoritmo per il nodo $u$ è il seguente : 
$$\begin{align}&\delta_u\log(\Delta_u)\end{align}$$
Ora, per ogni nodo $u\in T$, il costo totale dell'algoritmo di check sarà $$\sum\limits_{i}^N\delta_i\log(\Delta_i)\implies \delta\log(\Delta)$$
e ora, dato che $\delta\leq N$ e $\Delta\leq M$, il costo diventerà $N\log(M)$
Quindi, abbiamo che l'algoritmo impiega : 
$$\begin{align}&\text{Tempo}=\underbrace{\Theta(N\log(M))}_{\text{Preprocessing}}+\underbrace{O(N\log(M))}_{\text{Check Temporal Connectivity}}=O(N\log(M))\\&\text{Spazio}=\Theta(N)\end{align}$$
## Alberi Binari

Per quanto riguarda gli alberi binari, la dimostrazione è la stessa, semplicemente il tutto viene abbassato di un fattore 2.

Infatti il costo della fase 2 sarà semplicemente $N\log(M)$, in quanto il valore $\delta$ sarà uguale a 2, $\forall\space u\in T$

Il costo totale sarà sempre 
$$\begin{align}&\text{Tempo}=\underbrace{\Theta(N\log(M))}_{\text{Preprocessing}}+\underbrace{O(N\log(M))}_{\text{Check Temporal Connectivity}}=\Theta(N\log(M))\\&\text{Spazio}=\Theta(N)\end{align}$$
# Ottimizzazione dell'algoritmo

Possiamo notare che, a meno di costanti motliplicative, le due fasi dell'algoritmo possono essere unite in un unico algoritmo, che mentre calcola i valori $EA,T_\max$ bottom-up riesce anche ad effettuare il controllo di connettività temporale fra tutti i sottoalberi relativi ad un nodo interno $u$, $\forall\space u\in T$

I due pseudocodici sono i seguenti

**Alberi Binari**

```pseudo
\begin{algorithm}
\caption{Algoritmo Completo}
\begin{algorithmic}
\Require $L_v$ : Lista timestamp arco entrante in $v$
\Procedure{DFS-EA-Tmax}{Albero $T$,nodo $v$}
      \If{$v$ è Nullo}
	      \Return $-\infty,\infty$
      \EndIf
	      \If{$v$ è foglia}
		      \Return $L_v[1],L_v[n]$
          \EndIf
          \State $min_{sx},max_{sx}=$ DFS-EA-Tmax($sx(v)$)
          \State $min_{dx},max_{dx}=$ DFS-EA-Tmax($dx(v)$)
          \If{($min_{sx}\gt max_{dx})\lor (min_{dx}\gt max_{sx})$}
	          \Return $\infty,\infty$
          \EndIf
          \State $EA=\max(min_{sx},min_{dx})$
          \State $Tmax=\min(max_{sx},max_{dx})$
          \State NextEA = BinarySearch($L_v,EA$)
          \State NextTime = BinarySearch($L_v,Tmax$)
          \If{(NextEA $=-1$)$\lor$(NextTime=$-1$)}
	          \Return $\infty,\infty$
          \EndIf
          \State minTime = $\min(Tmax,L_v[n])$
          \Return NextEA,minTime
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```

Possiamo notare che nella versione ottimizzata, per gli alberi binari non c'è bisogno di mantenere in memoria i due dizionari, di conseguenza il costo temporale rimane invariato ma il costo spaziale passa da $O(N)$ a $O(1)$

Una possibile implementazione in Python è la seguente

```python
def dfs_EA_tmax(nodo):

    if nodo is None:
        return float("-inf"),float("inf")
    if nodo.left == None and nodo.right == None:
        return nodo.weight[0],nodo.weight[-1] 
        
    min_sx,max_sx = dfs_EA_tmax(nodo.left)
    min_dx,max_dx = dfs_EA_tmax(nodo.right)

    if min_sx>max_dx and min_dx>max_sx:
        return float("inf"),float("inf")

    EA = max(min_sx,min_dx)
    t_max_visita = min(max_sx,max_dx)
    
    nextEA = binary_search(nodo.weight,EA)
    nextTimeMax = binary_search_leq(nodo.weight,t_max_visita) 
    if nextEA == -1 or nextTimeMax == -1:
        
        exit("Errore: EA o tempo max visita non trovati")
    minTime = min(t_max_visita,nextTimeMax)

    return nextEA,minTime
```

L'algoritmo completo sarà quindi 

```pseudo
    \begin{algorithm}
    \caption{Algoritmo}
    \begin{algorithmic}
      \Procedure{Alg}{Albero $T$,radice $root$}
      \State $EA_{sx},T_{max,sx}=$ DFS-EA-Tmax($T,sx(root)$)
      \State $EA_{dx},T_{max,dx}=$ DFS-EA-Tmax($T,dx(root)$)
      \If{$EA_{sx}=\infty\lor EA_{dx}=\infty$}
      \Return Albero non è temporalmente connesso
      \EndIf
      \If{$EA_{sx}\leq T_{max,dx}\land EA_{dx}\leq T_{max,sx}$}
      \Return Albero è temporalmente connesso
	    \Else
	    \Return Albero non è temporalmente connesso
      \EndIf
      \EndProcedure
      \end{algorithmic}
    \end{algorithm}
```

**Alberi Non Binari**

Per gli alberi non binari lo pseudocodice è il seguente

```pseudo
\begin{algorithm}
\caption{Algoritmo Completo}
\begin{algorithmic}
\Require $L_v$ : Lista timestamp arco entrante in $v$
\Require Dizionario $D_{Nodi}$
\Require Dizionario $D_{SottoAlberi}$
\Require Dizionario $D_{EA}$,Dizionario $D_{Tmax}$
\Procedure{DFS-EA-Tmax}{Albero $T$,nodo $v$}
      \If{$v$ è Nullo}
	      \Return $D_{Nodi}=\emptyset$
      \EndIf
	      \If{$child(v)=\emptyset$}
		      \Return $D_{Nodi}(v)=(L_v[1],L_v[n])$
          \EndIf
          \State $D_{SottoAlberi}(v)=\emptyset$
          \ForAll{figlio $u$ di $v$}
          \State $update(D_{SottoAlberi}(v)$,DFS-EA-TMax($u$)
          \State $D_{EA}(v),D_{Tmax}(v)$=$D_{SottoAlberi}(u)$
          \EndFor
          \ForAll{$EA_v\in D_{EA}(v)$}
          \State $delete(D_{Tmax}(v),T_{\max,v})$
          \State minTime = $FindMin(D_{Tmax}(v))$
          \If{$EA_v\gt minTime$}
          \Return $D_{Nodi}(v)=(\infty,\infty)$
          \EndIf
          \State $insert(D_{Tmax}(v),T_{\max,v})$
          \EndFor
          
          \State $EA=\max(D_{EA})$
          \State $Tmax=\min(D_{Tmax})$
          \State NextEA = BinarySearch($L_v,EA$)
          \State NextTime = BinarySearch($L_v,Tmax$)
          
          \State minTime = $\min(Tmax,L_v[n])$
          \State $D_{SottoAlberi}(v)=(NextEA,minTime)$
          \Return $D_{SottoAlberi}$
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```
Una possibile implementazione in Python di questo pseudocodice potrebbe essere la seguente

```python
def dfs_EA_tmax_spazioN_NonBinary(root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Caso base: foglia
    if not root.children:
        return {root.value: (root.weight[0], root.weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}

    # Calcolo ricorsivo per ogni figlio
    ea_vals = []
    t_max_vals = []

    for child in root.children:
        sottoalberi.update(dfs_EA_tmax_spazioN_NonBinary(child))
        ea, t_max = sottoalberi[child.value]
        ea_vals.append(ea)
        t_max_vals.append(t_max)

    min_tmax = min(t_max_vals)
    pos_min = t_max_vals.index(min_tmax)
    #first_ea = ea_vals[pos_min]
    for i in range(len(ea_vals)):
        if ea_vals.index(ea_vals[i]) == pos_min:
            continue
        elif ea_vals[i] > min_tmax:
            return {root.value: (float("inf"), float("inf"))}

    # Calcolo EA e Tmax per il nodo corrente
    EA = max(ea_vals)
    t_max_visita = min(t_max_vals)

    nextEA = binary_search(root.weight, EA)
    nextTimeMax = binary_search_leq(root.weight, t_max_visita)  # Binary search per trovare il predecessore
    minTime = min(t_max_visita, nextTimeMax)

    # Aggiornamento del nodo corrente nei risultati
    sottoalberi[root.value] = (nextEA, minTime)

    return sottoalberi
```

L'algoritmo completo sarà quindi il seguente

```pseudo
    \begin{algorithm}
    \caption{Algoritmo}
    \begin{algorithmic}
    \Require Dizionario $D_{EA}$, Dizionario $D_{Tmax}$
      \Procedure{Alg}{Albero $T$,radice $root$}
      \State $D_{Risultati}=$ DFS-EA-Tmax($T,root$)
      \ForAll{Figlio $u$ di $root$}
      \State $D_{EA},D_{Tmax}=D_{Risultati}(u)$
      \EndFor
      \State Check=True
      \ForAll{$EA_{v_i}\in D_{EA}(root)$}
          \State $delete(D_{Tmax}(root),T_{\max,v_i})$
          \State minTime = $FindMin(D_{Tmax}(root))$
          \If{$EA_{v_i}\gt minTime$}
          \State Check=False
          \EndIf
          \State $insert(D_{Tmax}(root),T_{\max,v_i})$
        \EndFor
      \If{Check=True}
      \Return Albero temporalmente connesso
      \Else
      \Return Albero non temporalmente connesso
      \EndIf
      \EndProcedure
      \end{algorithmic}
    \end{algorithm}
```
In questo caso, l'ottimizzazione si trova solo sulla parte del codice, perchè sia il costo temporale che spaziale rimane invariato

Costo temporale $O(N\log(M))$
# Osservazione sull'ordinamento degli archi

Fino ad ora abbiamo fatto l'assunzione che i timestamp sugli archi fossero ordinati in partenza, ma nella realtà nessuno ci conferma se è effettivamente così oppure no.

Nel caso in cui i timestamp degli archi non siano ordinati, si può effettuare una procedura di preprocessing in cui in tempo $O(M\log(M))$ si possono ordinare tutti i timestamp.

Questo vale sia per alberi binari che non binari.

Il costo totale quindi cambierà in questo modo : 

- Alberi Binari : $$O(N\log(M))+O(M\log(M))=O(M\log(M)),\quad M=\Omega(N)$$
- Alberi Non Binari $$O(N\log(M))+O(M\log(M))=O(M\log(M)),\quad M=\Omega(N)$$
