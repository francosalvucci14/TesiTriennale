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
Se i timestamp sugli archi non sono ordinati, possiamo ovviare al problema ordinandoli usando l'algoritmo MergeSort, vedi [Capitolo 5](#^33fd38)
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
\State $D_v=$ vettore vuoto
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
          \If{NextEA $=-1\lor$NextTime=$-1$}
		        \State $EA_{\max}[v]=\infty$
		        \State $LD_{\max}[v]=\infty$
	          \Return $EA_{\max}[v],LD_{\max}[v]$
	    \Else
		    \State $EA_{\max}[v]=$NextEA
		    \State $LD_{\max}[v]=$NextLD
		    \Return $EA_{\max}[v],LD_{\max}[v]$
          \EndIf
          
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```

Le query di `Successore` e `Predecessore` vengono implementate usando l'idea della ricerca binaria, che posso usare perchè ho assunto che i timestamp sugli archi sono ordinati.

La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA_\max\leq LD_{\max},\forall EA_\max,LD_\max$$
Usando sempre l'approccio bottom-up.

Mentre controlla queste condizioni, calcola anche un vettore $D_v$ definito così:
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
\Require Vettori $EA_{\max},LD_{\max}$
\Procedure{CheckTemporalConnectivity}{$v,EA_{\max},LD_{\max}$}

\State $D_v=$ vettore vuoto
\If{$v$ is foglia}
\Return True
\EndIf

\ForAll{$u\in\text{child(v)}$}
\State check = CheckTemporalConnectivity($u,EA_{\max},LD_{\max}$)
\If{check = False}
\Return False
\EndIf
\State Appendo al vettore $D_v$ la coppia $\langle EA_{\max}[u],LD_{\max}[u]\rangle$
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

A questo punto, l'algoritmo completo sarà il seguente

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
- Crea il vettore $D_v$, e appende a questo vettore la coppia $(EA_\max[u],LD_\max[u])$, per ogni $u\in\text{child(v)}$
- Ordina questo vettore in modo crescente rispetto ai valori $LD_\max$ presenti al suo interno
	- All'interno del vettore $D_v$ quando $v$ è nodo interno, avremo tutte le informazioni di $EA$ e $LD$ relative ad ogni figlio di $v$, e di conseguenza possiamo usare queste informazioni per vedere se quei sottoalberi sono fra loro temporalmente connessi.
- Esegue effettivamente il check tra i sottoalberi relativi ai figli di $v$
- Ritorna il check per quel sottoalbero, se check diventerà `False` anche solo una volta, l'algoritmo ritornerà `False` e si potrà affermare che l'albero totale $T$ non è temporalmente connesso; altrimenti, se nessun sottoalbero darà `False`, si potrà affermare che l'albero completo $T$ è temporalmente connesso.

Vediamo come funziona il check effettivo tra i sottoalberi di un nodo $v$

Questo pezzo dell'algoritmo opera in $3$ fasi : 
1) Ordina il vettore $D_V$ in modo crescente rispetto ai valori $LD_\max$ presenti al suo interno, in modo tale da avere il minimo $LD$, tra tutti i figli di $v$, nella prima posizione del vettore $D_v$
2) Controllo se il primo $EA$ che trovo, ovvero l'$EA$ relativo al $LD$ minimo fra tutti i figli (quindi l'$EA$ in posizione $1$), è minore/uguale al secondo $LD$ (ovvero il $LD$ minimo levando il primo). In questo modo evitiamo di confrontare fra loro $EA$ e $LD$ relativi allo stesso figlio $u$ di $v$. Se questa condizione è vera, allora proseguiamo tranquillamente, altrimeni ritorno subito `False`
3) Partendo dalla seconda posizione del vettore $D_v$ fino al $\delta_u$, controllo se l'$i$-esimo $EA$ è minore/uguale al $LD$ minimo (quello in prima posizione.). Se la condizione sarà sempre verificata, allora ritorno `True`, altrimenti se un solo valore non mi verifica la condizione, ritorno `False`
4) In modo ricorsivo propago il valore del check, e se alla fine check sarà uguale a `True` allora ritorno che l'Albero è temporalmente connesso, altrimenti ritorno che l'Albero non è temporalmente connesso.

Quanto costa l'intero algoritmo?

- **Fase (1)** : Dato che il vettore $D_v$ ha size $\delta_v=\text{num. figli di v}$, l'ordinamento di tale vettore mi costerà $$\delta_v\log(\delta_v)$$
- **Fase (2)** : Costo costante $O(1)$
- **Fase (3)** : Costo lineare nel numero di figli di $v$, ovvero $O(\delta_v)$

Quindi in totale il costo per il nodo $v$ sarà $\delta_v\log(\delta_v)$, che sarà sempre minore/uguale di $\delta_v\log(\Delta)$ con $\Delta=\text{grado massimo dell'albero}$

Di conseguenza, per ogni nodo $v\in T$, il costo sarà $$\sum\limits_v\delta_i\log(\Delta)\implies\log(\Delta)\sum\limits_v\delta_i\implies\Delta\log(\Delta)$$
Ora, dato che il grado massimo dell'albero sarà al più $N-1$, l'algoritmo di check della temporal connectivity sarà $$N\log(N)$$

