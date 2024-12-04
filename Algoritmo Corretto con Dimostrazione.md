```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
debugInConsole: false # Print debug info in Obsidian console
```

---
# Algoritmo 

Due versioni : 
- una che usa spazio costante ma paga $O(N\log(M))$ per ogni sottoalbero
- una che usa spazio $O(N)$ ma paga $O(N\log(M))$ sempre, quindi fa una passata per tutto il sottoalbero

Pseudocode versione 1: 

````pseudo
    \begin{algorithm}
    \caption{Is Temporaly Connected}
    \begin{algorithmic}
      \Procedure{DFS-EA-Tmax}{$v$}
      \If{$v$ è Nullo}
	      \Return $-\infty,\infty$
      \EndIf
	      \If{$v$ è foglia}
		      \Return $L_v[1],L_v[n]$
          \EndIf
          \State $min_{sx},max_{sx}=$ DFS-EA-Tmax($sx(v)$)
          \State $min_{dx},max_{dx}=$ DFS-EA-Tmax($dx(v)$)
          \If{not ($min_{sx}\leq max_{dx}\lor min_{dx}\leq max_{sx}$)}
	          \Return $\infty,\infty$
          \EndIf
          \State $EA=\max(min_{sx},min_{dx})$
          \State $Tmax=\min(max_{sx},max_{dx})$
          \State NextTime = BinarySearch($L_v,EA$)
          \If{NextTime $=-1$}
	          \Return $\infty,\infty$
          \EndIf
          \Return NextTime,$\min(Tmax,L_v[n])$
      \EndProcedure
      \end{algorithmic}
    \end{algorithm}
````

**Variabili** : 
- $L_v$ : lista di timestamp associati all'arco entrante in $v$
- $min,max$ sia $sx,dx$ sono rispettivamente il timestamp minimo e massimo per il sottoalbero radicato nel nodo
	- Se il nodo è foglia, questi valori saranno semplicemente il tempo minimo e massimo dell'arco entrante nel nodo
	- Se il nodo è interno, questi valori indicano i tempi minimi e massimi per il sottoalbero radicato nel nodo
- I valori min e max servono per calcolare l'$EA_\max$ e $T_\max$, valori che poi verrano propagati dal basso verso l'alto. In questo modo, una volta arrivati alla radice dell'albero originale, avremo i valori per quanto riguarda l'$EA_\max$ dal basso verso l'alto, e per quanto riguarda il $T_\max$, ovvero il tempo massimo di visita del sottoalbero
	- Questi valori vengono calcolati per ogni possibile sottoalbero, in quanto la propagazione parte dal basso verso l'alto
- La condizione espressa nella riga dell'IF ci assicura che i nodi di un sottoalbero sono temporalmente connessi fra loro, questo sempre per ogni sottoalbero fino a risalire la radice
- Il valore $NextTime$ indica il prossimo timestamp da prendere per continuare la propagazione dell'$EA_\max$, se tale valore non esiste, ovvero se ci troviamo a guardare un'arco tale che $\forall t\in L_v,t<EA_\max$, allora ritorniamo $\infty$, e di conseguenza affermiamo che non è possibile trovare un'$EA$ bottom-up, che implica che risalendo l'albero, un nodo del livello $i-esimo$ non si potrà connettere con gli altri nodi del livello $(i-1)-esimo$ e cosi via

Questa procedura viene poi applicata all'algoritmo di partenza, ovvero l'algoritmo

```pseudo
    \begin{algorithm}
    \caption{Algoritmo}
    \begin{algorithmic}
      \Procedure{Alg}{$root$}
      \State $EA_{sx},T_{max,sx}=$ DFS-EA-Tmax($sx(root)$)
      \State $EA_{dx},T_{max,dx}=$ DFS-EA-Tmax($dx(root)$)
      \If{$EA_{sx}=\infty\lor EA_{dx}=\infty$}
      \Return False
      \EndIf
      \If{$EA_{sx}\leq T_{max,dx}\land EA_{dx}\leq T_{max,sx}$}
      \Return True
	    \Else
	    \Return False
      \EndIf
      \EndProcedure
      \end{algorithmic}
    \end{algorithm}
```
Versione python

```python
def algoritmo(root):

    ea_sx,t_max_sx = dfs_EA_tmax(root.left)
    ea_dx,t_max_dx = dfs_EA_tmax(root.right)
    print("------------------------------------------------")
    print(f"EA e tempo max visita sx della radice {root.value} : {ea_sx,t_max_sx}")
    print(f"EA e tempo max visita dx della radice {root.value} : {ea_dx,t_max_dx}")

    if ea_sx == float("inf") or ea_dx == float("inf"):
        return False

    # Ogni controllo del caso per alberi non binari
    if ea_sx <= t_max_dx and ea_dx <= t_max_sx:
        return True
    else:
        return False
```

Codice Python

```python title="Algoritmo 2"
def dfs_EA_tmax_spazio1(root):

    if root is None:
        return float("-inf"),float("inf")
    if root.left == None and root.right == None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia) : {root.weight[0],root.weight[-1]}")
        return root.weight[0],root.weight[-1] 
        
    min_sx,max_sx = dfs_EA_tmax_spazio1(root.left)

    min_dx,max_dx = dfs_EA_tmax_spazio1(root.right)

    if min_sx>max_dx and min_dx>max_sx:
        return float("inf"),float("inf")

    EA = max(min_sx,min_dx)
    t_max_visita = min(max_sx,max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno) : {EA,t_max_visita}")
    k = binary_search(root.weight,EA)
    nextTimeMax = binary_search_leq(root.weight,t_max_visita) 
    if k == -1 or nextTimeMax == -1:
        
        exit("Errore: EA o tempo max visita non trovati")
    minTime = min(t_max_visita,nextTimeMax)

    return k,minTime
```

Versione con spazio $O(N)$

```python title="Versione spazio lineare"
def dfs_EA_tmax_spazioN(root):
    # Caso base: nodo nullo
    if root is None:
        return {}

    # Caso base: foglia
    if root.left is None and root.right is None:
        print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (foglia): {root.weight[0], root.weight[-1]}")
        return {root.value: (root.weight[0], root.weight[-1])}

    # Variabili per raccogliere i valori EA e Tmax per ogni sottoalbero
    sottoalberi = {}

    # Calcolo ricorsivo per il sottoalbero sinistro
    if root.left is not None:
        sottoalberi.update(dfs_EA_tmax_spazioN(root.left))

    # Calcolo ricorsivo per il sottoalbero destro
    if root.right is not None:
        sottoalberi.update(dfs_EA_tmax_spazioN(root.right))

    # Estrai i valori di EA e Tmax dai figli
    ea_sx, t_max_sx = sottoalberi[root.left.value] if root.left else (float("-inf"), float("inf"))
    ea_dx, t_max_dx = sottoalberi[root.right.value] if root.right else (float("-inf"), float("inf"))

    # Controllo di consistenza tra i sottoalberi
    if ea_sx > t_max_dx and ea_dx > t_max_sx:
        return {root.value: (float("inf"), float("inf"))}

    # Calcolo EA e Tmax per il nodo corrente
    EA = max(ea_sx, ea_dx)
    t_max_visita = min(t_max_sx, t_max_dx)
    print(f"EA e tempo max visita per il sottoalbero radicato nel nodo {root.value} (nodo interno): {EA, t_max_visita}")

    k = binary_search(root.weight,EA)
    nextTimeMax = binary_search_leq(root.weight,t_max_visita) #binary search per trovare il predecessore, quindi il primo tempo t <= t_max_visita

    minTime = min(t_max_visita,nextTimeMax)
    # Aggiornamento del nodo corrente nei risultati
    sottoalberi[root.value] = (k, minTime)

    return sottoalberi
```
## Analisi e Dimostrazione di Correttezza dell'Algoritmo dfs_EA_tmax

L'algoritmo è progettato per trovare, in un albero binario, il massimo **Earliest-Arrival Time (EA)** possibile per un percorso che visiti tutti i nodi, e il corrispondente tempo di visita massimo, in modo tale da poter determinare se l'albero in input è **temporalmente connesso** oppure no.

**Funzionamento di base:**

1. **Caso base:** Se il nodo è una foglia, l'EA è il peso minimo dell'arco entrante e il tempo di visita massimo è il peso massimo dell'arco entrante.
2. **Caso ricorsivo:**
    - Si calcolano ricorsivamente l'EA massimo e il tempo di visita massimo per i sottoalberi sinistro e destro.
    - Si verifica se i due sottoalberi sono compatibili temporalmente (cioè se esiste un ordine di visita che rispetta i vincoli temporali).
    - Si calcola l'EA massimo del nodo corrente come il massimo tra gli EA massimi dei sottoalberi.
    - Si calcola il tempo di visita massimo del nodo corrente considerando il minimo tra il tempo di visita massimo dei sottoalberi e il peso massimo dell'arco entrante nel nodo corrente.

**Ipotesi induttiva:** Assumiamo che l'algoritmo funzioni correttamente per tutti i sottoalberi di un nodo.

**Passo base:** Per le foglie, l'algoritmo calcola correttamente l'EA e il tempo di visita massimo, in quanto non ci sono sottoalberi.

**Passo induttivo:** Consideriamo un nodo interno. Per ipotesi induttiva, i valori di EA massimo e tempo di visita massimo calcolati per i sottoalberi sinistro e destro sono corretti.

- **Verifica di compatibilità:** La condizione `if not (min_sx<=max_dx or min_dx<=max_sx)` assicura che i due sottoalberi siano compatibili temporalmente. Se questa condizione non fosse verificata, non esisterebbe un ordine di visita valido per l'intero sottoalbero.
- **Calcolo dell'EA massimo:** Il massimo EA del nodo corrente è correttamente calcolato come il massimo dei minimi timestamo di tutti gli archi di un sottoalbero.
- **Calcolo del tempo di visita massimo:** Il tempo di visita massimo è calcolato considerando il minimo tra i massimi di tutti i timestamp di un sottoalbero. Questo è corretto perché il tempo di visita massimo è limitato sia dal tempo necessario per visitare tutti i nodi del sottoalbero e sia dal tempo necessario per raggiungere il nodo stesso.

**Conclusione:** L'algoritmo calcola correttamente l'EA massimo e il tempo di visita massimo per ogni nodo dell'albero, e quindi per l'intero albero.

## Costo computazionale

Analizziamo l'equazione di ricorrenza dell'algoritmo, che è la seguente $$T(N)=2T\left(\frac{N}{2}\right)+\log(M)$$
Applicando lo strotolamento, abbiamo che 
$$\begin{align}T(N)=&2T\left(\frac{N}{2}\right)+\log(M)\\&2\left(2T\left(\frac{N}{2}\right)+\log(M)\right)+\log(M)\\&\vdots\\&2^iT\left(\frac{N}{2^i}\right)+\sum\limits_{j=0}^{i-1}2^i\log(M)\end{align}$$
A questo punto, $\frac{N}{2^i}=1\iff i=\log_2(N)$
Così facendo, l'equazione diventa 
$$\begin{align}&2^{\log_2(N)}+\sum\limits_{j=0}^{\log_2(N)-1}2^i\log(M)\\&=\\&N+N\log M\implies T(N)=\Theta(N\log(M))\end{align}$$
