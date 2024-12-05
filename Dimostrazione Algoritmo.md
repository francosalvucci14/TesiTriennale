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

Quando l'algoritmo risale alla radice, per i due figli della radice avremo calcolato correttamente i valori $EA$ e $T_\max$. 
A quel punto, basta chiamare la seconda fase

La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA_{sx}\leq T_{\max,dx}\land EA_{dx}\leq T_{\max,sx}$$

Se usando i valori ottenuti in fase 1 questa condizione viene verificata per ogni sottoalbero, allora posso affermare che l'albero è temporalmente connesso, altrimenti se almeno un sottoalbero non mi verifica la condizione, affermo che l'albero non è temporalmente connesso.

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
```pseudo
\begin{algorithm}
\caption{Procedura Preprocessing}
\begin{algorithmic}
\Require $L_v$ : Lista timestamp arco entrante in $v$
\Procedure{Preprocessing}{Albero $T$}
      \If{$v$ è Nullo}
	      \Return $-\infty,\infty$
      \EndIf
	      \If{$v$ è foglia}
		      \Return $L_v[1],L_v[n]$
          \EndIf
          \State $min_{sx},max_{sx}=$ Preprocessing($sx(v)$)
          \State $min_{dx},max_{dx}=$ Preprocessing($dx(v)$)
          \If{$(min_{sx}\gt max_{dx})\land (min_{dx}\gt max_{sx})$}
	          \Return $\infty,\infty$
          \EndIf
          \Comment{Questo If va messo nella parte di ottimizzazione, quando si vede che si può fare tutto insieme}
          \State $EA=\max(min_{sx},min_{dx})$
          \State $Tmax=\min(max_{sx},max_{dx})$
          \State NextEA = BinarySearch($L_v,EA$)
          \State NextTime = BinarySearch($L_v,Tmax$)
          \If{NextEA $=-1\lor$NextTime=$-1$}
	          \Return $\infty,\infty$
          \EndIf
          \State minTime = $\min(Tmax,L_v[n])$
          \Return NextTime,minTime
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```
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
```pseudo
\begin{algorithm}
\caption{Procedura Check Temporal Connectivity}
\begin{algorithmic}

\end{algorithmic}
\end{algorithm}
```
# Dimostrazione

# Ottimizzazione dell'algoritmo

# Osservazione sull'ordinamento degli archi