```table-of-contents
title: 
style: nestedOrderedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
hideWhenEmpty: true # Hide TOC if no headings are found
debugInConsole: false # Print debug info in Obsidian console
```
# Preliminari

Assumiamo che tutti i timestamp degli archi siano ordinati in senso crescente.
Tutti gli algoritmi che seguiranno sfruttano questa assunzione.
Se i timestamp sugli archi non sono ordinati, possiamo ovviare al problema ordinandoli usando l'algoritmo MergeSort, vedi [Capitolo 4](#^cc0759)
# Algoritmo

L'algoritmo è diviso in due fasi
- Preprocessing dei vettori $EA_\max,LD_\max$
- Check finale

La **fase di preprocessing** è la fase che calcola con approccio bottom-up i seguenti valori, per ogni nodo $v$ : 
- $EA_{\max}(v)=\max_{f:\text{f è foglia}}EA$ da $f\in T_v$ fino al padre di $v$ 
- $LD_\max(v)=$ Istante di tempo $t$ tale che se arrivo al padre di $v$ a tempo $\leq t$, allora posso visitare tutto $T_v$

Ogni volta che salgo di livello, propago le informazioni dai figli di $u$ fino a $u$ , e combino le informazioni che ho ottenuto con i valori sul nodo $u$.

Una volta eseguita la fase 1, verranno ritornati questi $2$ vettori che poi useremo nella fase di check per determinare se l'albero è temporalmente connesso oppure no.

Lo pseudocodice della fase di preprocessing è il seguente

```pseudo
\begin{algorithm}
\caption{Procedura Preprocessing}
\begin{algorithmic}
\Require $L_v$ : Lista di timestamp sull'arco entrante in $v$, per ogni $v$ nodo
\Require Vettore $EA_{\max}$,Vettore $LD_{\max}$
\Procedure{Preprocessing}{Nodo $v$}
	      \If{$v$ è foglia}
	      \State $EA_{\max}[v]=\min(L_v)$
	      \State $LD_{\max}[v]=\max(L_v)$
		      \Return $EA_{\max}[v],LD_{\max}[v]$
          \EndIf
          \ForAll{figlio $u_i$ di $v$}
          \State $min_{u_i},max_{u_i}=$ Preprocessing($u_i$)
          \State $EA_{\max}[u_i]=min_{u_i}$
          \State $LD_{\max}[u_i]=max_{u_i}$
          
          \EndFor
          
          \State $EA=\max_{u\in\text{child(v)}}EA_{\max}[u_i]$
          \Comment{$\forall$ figlio di $v$}
          \State $LD=\min_{u\in\text{child(v)}}LD_{\max}[u_i]$
          \Comment{$\forall$ figlio di $v$}
          \State NextEA = Successor($L_v,EA$)
          \Comment{NextEA = Successore di EA}
          \State NextLD = Predecessor($L_v,LD$)
          \Comment{NextTime = Predecessore di LD}
          \If{NextEA $=-1\space\lor\space$NextTime=$-1$}
		        \State $EA_{\max}[v]=\infty$
		        \State $LD_{\max}[v]=\infty$
	          
	    \Else
		    \State $EA_{\max}[v]=$NextEA
		    \State $LD_{\max}[v]=$NextLD
		    
          \EndIf
          \Return $EA_{\max}[v],LD_{\max}[v]$
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```

Le query di `Successore` e `Predecessore` vengono implementate usando l'idea della ricerca binaria, che possiamo usare avendo assunto che i timestamp sugli archi sono tutti ordinati.

La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA_\max\leq LD_{\max},\forall EA_\max,LD_\max$$
Usando sempre l'approccio bottom-up.

Mentre controlla queste condizioni, l'algoritmo calcola anche un vettore $D_v$ definito così:
- $D_v:$ Vettore di size $\delta_v=\text{num. figli di }v$ che contiene le coppie $(EA_\max[u],LD_\max[u])$ $\forall\space u\in\text{child(v)}$ 

Con questo vettore poi faremo tutti i check necessari per determinare se il ogni sottoalbero si può connettere temporalmente con gli altri

Usando i valori ottenuti dalla fase 1, avremo due casistiche : 
1) Se la condizione sarà verificata sempre, allora potrò affermare che **l'albero è  temporalmente connesso**
2) Se la condizione non verrà verificata per almeno un sottoalbero, allora potrò affermare che **l'albero non è temporalmente connesso**

Codice fase 2 con calcolo di $D_v$

```pseudo
\begin{algorithm}
\caption{Procedura Check Temporal Connectivity}
\begin{algorithmic}
\Input Vettori $EA_{\max},LD_{\max}$
\Procedure{CheckTemporalConnectivity}{$v,EA_{\max},LD_{\max}$}

\State $D_v=$ vettore vuoto
\If{$v$ is foglia}
\Return True
\EndIf

\ForAll{$u\in\text{child(v)}$}
\If{Not CheckTemporalConnectivity($u,EA_{\max},LD_{\max}$)}
\Return False
\EndIf 
\If{$EA_{\max}[u] = \infty\space\lor\space LD_{\max}[u]=\infty$}
\Return False
\Else
\State Appendo al vettore $D_v$ la coppia $\langle EA_{\max}[u],LD_{\max}[u]\rangle$
\EndIf

\EndFor

\State Ordino il vettore $D_v$ in modo crescente rispetto ai valori $LD_{\max}$ al suo interno

\Comment{Step 1}
\If{$D_{v}[1][1]\leq D_v[2][2]$}
\Comment{Step 2}
\State Vado avanti
\EndIf

\For{$i$=2 to $\delta_u$}
\Comment{Step 3}
\If{$D_{v}[i][1]\gt D_{v}[1][2]$}
\Return False

\EndIf
\EndFor

\Return True

\EndProcedure
\end{algorithmic}
\end{algorithm}
```

Dopo aver definito le due procedure in modo separato, diamo lo pseudociodice dell'algoritmo completo, che sarà il seguente :

```pseudo
\begin{algorithm}
\caption{Algoritmo Completo}
\begin{algorithmic}
\Procedure{Algoritmo}{Albero $T$}
\State $EA_{\max} $ vettore vuoto
\State $LD_{\max} $ vettore vuoto
\State $EA_{\max},LD_{\max}$ = Preprocessing(Radice $v$)
\State check = CheckTemporalConnectivity($EA_{\max},LD_{\max}$)
\If{check = False}
\Return False
\Else
\Return True
\EndIf

\EndProcedure
\end{algorithmic}
\end{algorithm}
```
## Dimostrazione 

La dimostrazione di correttezza verrà effettuata sulla procedura di `CheckTemporalConnectivity`

L'algoritmo di check funziona nel modo seguente.

Vengono definite due casistiche : 
- quando il nodo $v$ è foglia
- quando il nodo $v$ è nodo interno

Quando il nodo $v$ è una foglia, semplicemente l'algoritmo ritorna `True`, dato che una foglia è sempre temporalmente connessa con se stessa.

Quando il nodo $v$ è nodo interno l'algoritmo opera in questo modo : 
- Crea il vettore $D_v$ e appende a questo vettore la coppia $(EA_\max[u],LD_\max[u])$, per ogni $u\in\text{child(v)}$, se i valori di $EA_\max$ e $LD_\max$ sono diversi da $\infty$
	- In caso contrario, significa che da quel determinato nodo non posso proseguire con il check, e di conseguenza devo ritornare `False`
- Ordina questo vettore in modo crescente rispetto ai valori $LD_\max$ presenti al suo interno
	- All'interno del vettore $D_v$ avremo tutte le informazioni che si servono per vedere se i sottoalberi radicati nei figli di $v$ sono fra loro temporalmente connessi.
- Esegue effettivamente il check tra i sottoalberi relativi ai figli di $v$
- Ritorna il check per quel sottoalbero, se il check diventerà `False` anche solo una volta, l'algoritmo ritornerà `False` e si potrà affermare che l'albero totale $T$ non è temporalmente connesso; altrimenti, se nessun sottoalbero darà `False`, si potrà affermare che l'albero completo $T$ è temporalmente connesso.

Vediamo come funziona il check effettivo tra i sottoalberi di un nodo $v$

La fase di check dei sottoalberi opera in $3$ fasi : 
1) Ordina il vettore $D_v$ in modo crescente rispetto ai valori $LD_\max$ presenti al suo interno, in modo tale da avere il minimo $LD$, tra tutti i figli di $v$, nella prima posizione del vettore $D_v$
2) Controllo se l'$EA$ in posizione $1$ è minore/uguale al secondo $LD$ (ovvero l'$LD$ in posizione $2$). In questo modo evitiamo di confrontare fra loro $EA$ e $LD$ relativi allo stesso figlio $u$ di $v$. Se questa condizione è vera, allora proseguiamo in fase $3$, altrimeni ritorno subito `False` ed esco dall'algoritmo.
3) Partendo dalla seconda posizione del vettore $D_v$ fino al $\delta_u$, controllo se l'$i$-esimo $EA$ è minore/uguale al $LD$ minimo (ovvero quello in prima posizione.). Se la condizione sarà sempre verificata, allora ritorno `True`, altrimenti se un solo valore non mi verifica la condizione, ritorno `False`

In modo ricorsivo risalgo l'albero verso la radice, propagando il check verso l'alto. 
Se alla fine check sarà uguale a `True` allora ritorno che l'Albero è temporalmente connesso, altrimenti ritorno che l'Albero non è temporalmente connesso.

Quanto costa l'intero algoritmo?

- **Fase (1)** : Dato che il vettore $D_v$ ha size $\delta_v=\text{num. figli di v}$, l'ordinamento di tale vettore mi costerà $$\delta_v\log(\delta_v)$$
- **Fase (2)** : Check tra il primo $EA$ e il secondo $LD$ costa costante $O(1)$
- **Fase (3)** : Check per ogni $EA_i$ , con $i=2,\dots,\delta_u$ . Costo lineare nel num. di figli di $v$, ovvero $O(\delta_v)$

Quindi in totale il costo per il nodo $v$ sarà $\delta_v\log(\delta_v)$.

Ora, dato che un nodo potrà avere al più $\Delta$ figli, con $\Delta=\text{grado massimo dell'albero}$, possiamo affermare che $\delta_v\log(\delta_v)$ sarà sempre $\leq\delta_v\log(\Delta)$. 

Di conseguenza, per ogni nodo $v\in T$, il costo complessivo dell'algoritmo di check sarà $$\sum\limits_v\delta_i\log(\Delta)\implies\log(\Delta)\sum\limits_v\delta_i\implies\Delta\log(\Delta)$$
Adesso, dato che $\Delta\leq N-1$,  l'algoritmo di check della temporal connectivity costerà $$O(N\log(N))$$
Di conseguenza, l'algoritmo completo compreso di preprocessing dei valori e check temporal connectivity costerà
$$O(N\log(M))+O(N\log(N))\implies O(N\log(M)),\quad M=\Omega(N)$$
# Unificazione delle procedure

Possiamo notare che le due procedure possono essere unite in un unica procedura, ovvero una procedura che mentre calcola i valori $EA$ e $LD$ esegue anche il check temporale tra i sottoalberi.

Nel caso degli alberi binari il costo della procedura di check sarà sovrastato dal costo del calcolo dei valori $EA$ e $LD$, in quanto il costo della fase di check risulterà essere costante. Di conseguenza il costo della procedura unificata sarà semplicemente uguale al costo della fase di preprocessing, quindi $O(N\log(M))$. 

Nel caso degli alberi non binari, per ogni nodo $v$ verrà eseguito il check su tutti i suoi figli. Ogni nodo $v$ ha $\delta_v$ figli, che al più saranno $\Delta=\text{grado massimo dell'albero }T$. 

Per un singolo nodo $v$ pago $$O(\underbrace{\delta_v}_\text{check}+\underbrace{\delta_v\log(\delta_v)}_\text{ordinamento}+\underbrace{\log(M)}_\text{query di succ. e predec.})\implies O(\delta_v\log(\delta_v)+\log(M))$$

Per ogni nodo $v\in T$, il costo totale dell'algoritmo sarà : 
$$O(N[\underbrace{\log(M)}_{\text{costo per succ. e pred.}}+\underbrace{\Delta\log(\Delta)}_{\text{check su sottoalberi}}])=O(N\log(M)+N^2\log(N))=O(N^2\log(N))$$

Possiamo notare quindi un'ottimizzazione sia nella scrittura del codice sia nel costo computazionale.

Lo pseudocodice della procedura unificata sarà il seguente : 

```pseudo
\begin{algorithm}
\caption{Algoritmo Unificato}
\begin{algorithmic}
\Require $L_v$ : Lista di timestamp sull'arco entrante in $v$, per ogni $v$ nodo
\INput Vettore $EA_{\max}$,Vettore $LD_{\max}$
\Procedure{Visita-DFS}{Nodo $v$,$EA_{\max},LD_{\max}$}
\State $D_v=$ vettore vuoto
	      \If{$v$ è foglia}
	      \State $EA_{\max}[v]=\min(L_v)$
	      \State $LD_{\max}[v]=\max(L_v)$
	      \State Check = True
		      \Return $EA_{\max}[v],LD_{\max}[v]$,Check
          \EndIf
          \ForAll{figlio $u_i$ di $v$}
          \State $min_{u_i},max_{u_i},$Check = Visita-DFS($u_i$)
          \State $EA_{\max}[u_i]=min_{u_i}$
          \State $LD_{\max}[u_i]=max_{u_i}$
          \State Appendo al vettore $D_v$ la tripla $\langle EA_{\max}[u],LD_{\max}[u],Check\rangle$
          
          \EndFor
          \If{lenght($D_v$)$\gt1$}
          \State Ordino il vettore $D_v$ in modo crescente rispetto ai valori $LD_{\max}$ al suo interno
          \Comment{Step 1}
\If{Not ($D_{v}[1][1]\leq D_v[2][2]$)}
\Comment{Step 2}
\Return $EA_{\max}[u],LD_{\max}[u]$,False
\EndIf

\For{$i$=2 to $\delta_u$}
\Comment{Step 3}
\If{$D_{v}[i][1]\gt D_{v}[1][2]$}
\Return $EA_{\max}[u],LD_{\max}[u]$,False

\EndIf
\EndFor
          \EndIf
          \State $EA=\max_{u\in\text{child(v)}}EA_{\max}[u_i]$
          \Comment{$\forall$ figlio di $v$}
          \State $LD=\min_{u\in\text{child(v)}}LD_{\max}[u_i]$
          \Comment{$\forall$ figlio di $v$}
          \State NextEA = Successor($L_v,EA$)
          \Comment{NextEA = Successore di EA}
          \State NextLD = Predecessor($L_v,LD$)
          \Comment{NextTime = Predecessore di LD}
          \If{NextEA $=-1\space\lor\space$NextTime=$-1$}
		        \State $EA_{\max}[v]=\infty$
		        \State $LD_{\max}[v]=\infty$
	          
	    \Else
		    \State $EA_{\max}[v]=$NextEA
		    \State $LD_{\max}[v]=$NextLD
		    
          \EndIf
          \Return $EA_{\max}[v],LD_{\max}[v]$,Check
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```
L'algoritmo che richiamerà questa funzione sarà il seguente

```pseudo
\begin{algorithm}
\caption{Algoritmo Completo}
\begin{algorithmic}
\Procedure{Algoritmo}{Albero $T$}
\State $EA_{\max} $ vettore vuoto
\State $LD_{\max} $ vettore vuoto
\State Check = False
\State $EA_{\max},LD_{\max}$,Check = Visita-DFS(Radice $v$)
\If{check = False}
\Return False
\Else
\Return True
\EndIf

\EndProcedure
\end{algorithmic}
\end{algorithm}
```

# Ordinamento dei timestamp sugli archi

^cc0759

Fin'ora abbiamo fatto l'assunzione che i timestamp sugli archi fossero effettivamente ordinati in senso crescente, ma non è detto che sia sempre così.

Infatti, se i timestamp non fossero ordinati noi non potremmo effettuare query di successore e precedessore in tempo $\log(M)$, ma saremmo costretti a farlo in tempo $O(M)$, cosa che ci andrà a rallentare il tempo di esecuzione in modo esponenziale; infatti si passerebbe da $N\log(M)$ a $N\cdot M$ 

Per ovviare a questo problema, possiamo definire un'algoritmo che con una visita controlla se i timestamp sono ordinati.

Se la risposta è si si continua in modo normale con gli algoritmi precedenti, altrimenti si ordinano i timestamp.

L'algoritmo per vedere se i timestamp sono ordinati può essere fatto in tempo $O(M)$, usando una semplice visita `DFS`, mentre l'ordinamento effettivo dei timestamp impiegherà tempo $M\log(M)$ sfruttando il `MergeSort`.

Per quanto riguarda i costi, avremo che : 
1) Per la versione non unificata, il costo sarà $$O(N\log(M)+O(M)+O(M\log(M)))\implies O(M\log(M))$$
2) Per la versione unificata, il costo sarà $$O(N^2\log(M)+O(M)+O(M\log(M)))\implies O(N^2\log(M))$$
Come si può notare, abbiamo che per la versione non unificata il costo sarà sovrastato dall'ordinamento dei timestamp; mentre nella versione unificata, il costo rimarrà invariato.
# Appendice dei codici

**Possibile implementazione algoritmo separato**

Preprocessing

```python
def preprocess(tree, node, EA_max, LD_max):
    """
    Procedura di preprocessing per calcolare EA_max e LD_max per ogni nodo.

    tree: grafo orientato rappresentante l'albero
    node: nodo corrente
    EA_max: dizionario per salvare i valori di EA_max
    LD_max: dizionario per salvare i valori di LD_max
    """
    children = list(tree.successors(node))
    weights = tree.nodes[node].get("weight", [])

    # Caso base: foglia
    if not children:
        EA_max[node] = min(weights)
        LD_max[node] = max(weights)
        return EA_max[node], LD_max[node]

    # Variabili temporanee per raccogliere i valori dai figli
    ea_values = []
    ld_values = []

    for child in children:
        ea_child, ld_child = preprocess(tree, child, EA_max, LD_max)
        ea_values.append(ea_child)
        ld_values.append(ld_child)

    # Calcolo di EA e LD per il nodo corrente
    EA = max(ea_values)
    LD = min(ld_values)

    # Trova il successore e predecessore in base ai pesi
    if weights:
        NextEA = binary_search(weights, EA)
        NextLD = binary_search_leq(weights, LD)
        if NextEA == -1 or NextLD == -1:
            EA_max[node] = float('inf')
            LD_max[node] = float('inf')
        else:

            EA_max[node] = NextEA
            LD_max[node] = NextLD
    else:
        EA_max[node] = -1
        LD_max[node] = -1

    return EA_max[node], LD_max[node]

```

Fase di check 

```python
def check_temporal_connectivity(tree, node, EA_max, LD_max):
    """
    Procedura per controllare la connettività temporale di un albero.

    tree: grafo orientato rappresentante l'albero
    node: nodo corrente
    EA_max: dizionario contenente i valori di EA_max
    LD_max: dizionario contenente i valori di LD_max
    """
    children = list(tree.successors(node))

    # Caso base: foglia
    if not children:
        return True

    intervals = []

    for child in children:
        if not check_temporal_connectivity(tree, child, EA_max, LD_max):
            return False
        if not (EA_max[child] == float("inf") or LD_max[child] == float("inf")):
            intervals.append((EA_max[child], LD_max[child]))
        else:
            return False

    # Ordina gli intervalli per LD_max
    intervals.sort(key=lambda x: x[1])

    if len(intervals) > 1:
		if not (intervals[0][0] <= intervals[1][1]):
			return False
		# Controllo di consistenza
		for i in range(1, len(intervals)):
			if intervals[i][0] > intervals[0][1]:
				return False
	elif len(intervals) == 1:
		return True

	return True
```

Algoritmo

```python
def algoritmo(T):
    """
    Algoritmo per la verifica della connettività temporale di un albero.

    T: grafo orientato rappresentante l'albero
    """
    EA_max = {}
    LD_max = {}
    preprocess(T, "A", EA_max, LD_max)
    check = check_temporal_connectivity(T, "A", EA_max, LD_max)
    
    if check:
        return "L'albero è temporalmente connesso"
    else:
        return "L'albero non è temporalmente connesso"
```

**Possibile implementazione algoritmo unificato**

Visita

```python
def DFS_Totale(tree, root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Ottieni i figli del nodo corrente
    children = list(tree.successors(root))
    weight = tree.nodes[root]["weight"]

    # Caso base: foglia
    if not children:
        return {root: (weight[0], weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}
    ea_tmax = []

    # Calcolo ricorsivo per ogni figlio
    for child in children:
        sottoalberi.update(DFS_Totale(tree, child))
        ea, t_max = sottoalberi[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])

    # Step 2 e 3: Controlli di consistenza
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            return {root: (float("inf"), float("inf"))}

        for i in range(1, len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                return {root: (float("inf"), float("inf"))}

    # Calcola EA e Tmax per il nodo corrente
    EA = max(ea_tmax, key=lambda x: x[0])[0]
    t_max_visita = min(ea_tmax, key=lambda x: x[1])[1]
    if not weight:
        k, nextTimeMax = 0, 0
        sottoalberi[root] = (k, nextTimeMax)
        return sottoalberi
    k = binary_search(weight, EA)
    nextTimeMax = binary_search_leq(weight, t_max_visita)

    if nextTimeMax == -1 and root != "A":
        return {root: (float("inf"), float("inf"))}

    # Aggiorna i risultati
    sottoalberi[root] = (k, nextTimeMax)
    return sottoalberi
```

Algoritmo completo

```python
def algoritmo3_networkx(tree):
    # Trova la radice (nodo senza archi entranti)
    root = [n for n, d in tree.in_degree() if d == 0][0]

    risultati = DFS_Totale(tree, root)

    # Ottieni i risultati per i figli della radice
    figli = list(tree.successors(root))
    if not figli:
        return False

    ea_tmax = []
    if risultati[root][0] == float("inf") or risultati[root][1] == float("inf"):
        return False

    for child in figli:
        ea, t_max = risultati[child]
        ea_tmax.append((ea, t_max))

    # Step 1: Ordina per Tmax
    ea_tmax.sort(key=lambda x: x[1])

    # Step 2 e 3: Controlli di consistenza
    if len(ea_tmax) > 1:
        if not (ea_tmax[0][0] <= ea_tmax[1][1]):
            return False

        for i in range(1, len(ea_tmax)):
            if ea_tmax[i][0] > ea_tmax[0][1]:
                return False
    elif len(ea_tmax) == 1:
        return True
    return True
```

