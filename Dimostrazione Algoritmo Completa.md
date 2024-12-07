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
Quindi per ogni nodo, le informazioni corrette vengono propagante pagando $\log(M)$

Vediamo la fase 2: 
Per ogni sottoalbero, viene effettuata la seguente verifica

Consideriamo un nodo $u$ con i suoi figli : 
- $\forall\space EA(v)$ con $v$ figlio di $u$ eseguiamo le seguenti operazioni
	- Elimino dal dizionario $D_{Tmax}$ il $T_\max(v)$ corrispondente all'$EA(v)$ appena preso, mi costa $\log(\Delta_u)$
	- Trovo il minimo $T_\max$ tra tutti i figli $v_i$ di $u$, mi costa $\log(\Delta_u)$
	- Eseguo il check tra $EA_v$ e $T_{\max,\text{minimo}}$ e costa $O(1)$
	- Riaggiungo il valore $T_\max(v)$ eliminato prima nel dizionario corrispondente, costo $\log(\Delta_u)$

Adesso, preso 
- $\delta_u$ = num. di figli del nodo $u$
- $\Delta_u$ = num. di valori $T_\max$ del nodo $u$
Abbiamo che il costo totale dell'algoritmo per il nodo $u$ è il seguente : 
$$\begin{align}&\delta_u\log(\Delta_u)\end{align}$$
Ora, per ogni nodo $u\in T$, il costo totale dell'algoritmo di check sarà $$N\sum\limits_{i}^N\delta_i\log(\Delta_i)\implies N\delta\log(\Delta)$$
e ora, dato che $\delta\leq N$ e $\Delta\leq M$, il costo diventerà $N^2\log(M)$
Quindi, abbiamo che l'algoritmo impiega : 
$$\begin{align}&\text{Tempo}=\underbrace{\Theta(N\log(M))}_{\text{Preprocessing}}+\underbrace{O(N^2\log(M))}_{\text{Check Temporal Connectivity}}=O(N^2\log(M))\\&\text{Spazio}=\Theta(N)\end{align}$$
## Alberi Binari

Per quanto riguarda gli alberi binari, la dimostrazione è la stessa, semplicemente il tutto viene abbassato di un fattore 2.

Infatti il costo della fase 2 sarà semplicemente $N\log(M)$, in quanto il valore $\delta$ sarà uguale a 2, $\forall\space u\in T$

Il costo totale sarà sempre 
$$\begin{align}&\text{Tempo}=\underbrace{\Theta(N\log(M))}_{\text{Preprocessing}}+\underbrace{O(N\log(M))}_{\text{Check Temporal Connectivity}}=\Theta(N\log(M))\\&\text{Spazio}=\Theta(N)\end{align}$$
# Ottimizzazione dell'algoritmo

Possiamo notare che, a meno di costanti motliplicative, le due fasi dell'algoritmo possono essere unite in un unico algoritmo, che mentre calcola i valori $EA,T_\max$ bottom-up riesce anche ad effettuare il controllo di connettività temporale fra i sottoalberi realtivi ad un nodo padre $u$
# Osservazione sull'ordinamento degli archi