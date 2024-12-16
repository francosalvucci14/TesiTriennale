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
- Preprocessing
- Check finale

La **fase di preprocessing** è la fase che calcola con approccio bottom-up i seguenti valori, per ogni nodo $v$ : 
- $EA_{\max}(v)=\max_{f:\text{f è foglia}}EA$ da $f\in T_v$ fino al padre di $v$ 
- $LD_\max(v)=$ Istante di tempo $t$ tale che se arrivo al padre di $v$ a tempo $\leq t$, allora posso visitare tutto $T_v$
- $D_v:$ Vettore di size $\delta_v=\text{num. figli di }v$ che contiene le coppie $(LD_\max[u],u)$, con $u\in\text{child(v)}$ ordinate in modo non crescete secondo il valore di $LD_\max[u]$

Ogni volta che salgo di livello, propago le informazioni dai figli di $u$ fino a $u$ , e combino le informazioni che ho ottenuto con i valori sul nodo $u$.

Una volta eseguita la fase 1, verranno ritornati questi $3$ vettori. 
Usando poi questi vettori, passiamo in fase 2 per il check della temporal connectivity.

Pseudocodice fase di preprocessing
```pseudo
\begin{algorithm}
\caption{Procedura Preprocessing}
\begin{algorithmic}
\Require $L_v$ : Lista di timestamp sull'arco entrante in $v$, per ogni $v$ nodo
\Require Vettore $EA_{\max}$,Vettore $LD_{\max}$, Vettore $D_v$
\Procedure{Preprocessing}{Nodo $v$}
	      \If{$v$ è foglia}
	      \State $EA_{\max}[v]=\min(L_v)$
	      \State $LD_{\max}[v]=\max(L_v)$
		      \Return $EA_{\max}[v],LD_{\max}[v],D_v$
          \EndIf
          \ForAll{figlio $u_i$ di $v$}
          \State $min_{u_i},max_{u_i}=$ Preprocessing($u_i$)
          \State $EA_{\max}[u_i]=min_{u_i}$
          \State $LD_{\max}[u_i]=max_{u_i}$
          \State $D_v[i]=(LD_{\max}[u_i],u_i)$
          \Comment{$D_v$ in pos. i = coppia $(LD_{\max}[u_i],u_i)$, per ogni figlio di $v$}
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
	          \Return $EA_{\max}[v],LD_{\max}[v],D_v$
	    \Else
		    \State $EA_{\max}[v]=$NextEA
		    \State $LD_{\max}[v]=$NextLD
          \EndIf
          
          \Return $EA_{\max}[v],LD_{\max}[v],D_v$
      \EndProcedure
\end{algorithmic}
\end{algorithm}
```

La **fase di check finale** è la fase che si occupa di vedere se l'albero rispetta la condizione di connettività temporale, ovvero 
$$EA_\max\leq T_{\max},\forall EA_\max,T_\max$$
Usando sempre l'approccio bottom-up.

Usando i valori ottenuti dalla fase 1, avrò due casistiche : 
1) Se la condizione sarà verificata sempre, allora potrò affermare che **l'albero è  temporalmente connesso**
2) Se la condizione non verrà verificata per almeno un sottoalbero, allora potrò affermare che **l'albero non è temporalmente connesso**

Lo pseudocodice della fase 2 è il seguente

```pseudo
\begin{algorithm}
\caption{Procedura Check Temporal Connectivity}
\begin{algorithmic}
\Procedure{CheckTemporalConnectivity}{$v,EA_{\max},LD_{\max},D_v$}
\If{$v$ is foglia}
\Return True
\EndIf
\ForAll{$u\in\text{child(v)}$}
\State Check = Check $\land$ CheckTemporalConnectivity($u,EA_{\max},LD_{\max},D_v$)
\EndFor
\State Check = True
\ForAll{$u\in\text{child(v)}$}
\If{$EA_{\max}[u]\gt\max_{u'\in\text{child(v)},u'\neq u}LD_{\max}[u']$}
\Return False
\EndIf
\EndFor
\If{Check = False}
\Return False
\Else 
\Return True
\EndIf
\EndProcedure
\end{algorithmic}
\end{algorithm}
```

Da mettere calcolo effettivo di $min_{u'\in\text{child(v)},u'\neq u}LD_{\max}[u']$ + algoritmo completo+ dimostrazione