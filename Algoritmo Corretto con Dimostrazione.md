```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
debugInConsole: false # Print debug info in Obsidian console
```
# Algoritmo

L'algoritmo è diviso in più fasi : 
- **Preprocessing (Fase 1)**
- **Fase 2**
- **Fase 3**
- **Fase 4**
- **Check Finale**

## Idea dell'algoritmo

**Fase 1 : Prepcrocessing**

Verifico se partendo da root, posso visitare tutti i nodi dell'albero (se non è possibile, l'albero non è temporalmente connesso).
Per farlo basta fare una visita DFS che controlla se ogni nodo rispetta la condizione di crescita incrementale dei timestamp.
  
**Fase 2 : Calcolo foglia più profonda con timestamp minimo nei sottoalberi sinistro e destro**

Per trovare la foglia con timestamp minimo nei sottoalberi sinistro e destro,
posso utilizzare la funzione ***find_leaf_min_timestamp*** definita di seguito.
Questa funzione calcola la foglia con timestamp minimo in un albero binario.

**Fase 3 : Calcolo dell'$EA_{\min}$ partendo dalla foglia più profonda fino alla radice**

Questa fase è simmetrica, ovvero vale per entrambi i sottoalberi, quindi ci concentreremo solo su un sottoalbero.
A questo punto, applico l'algoritmo per calcolare l'EA, usando la struttura dati del professore, ovvero quella che impiega tempo $O(\log M\cdot\log L)$
Se la funzione ritorna $-\infty$, sia da un lato che dall'altro, allora ritorno subito False (l'albero non è temporalmente connesso)

**Fase 4 : Calcolo tempo massimo di visita di un sottoalbero**

Questa fase è simmetrica, come la fase 3.

Con un approccio bottom-up, possiamo calcolare il tempo massimo di visita per un sottoalbero.

Il tempo massimo è calcolato così:
1. Si parte dalla profondità massima dell'albero, si controllano tutti i timestamp degli archi di quel livello e si prende il timestamp minimo fra tutti i massimi
2. Risalendo di livello mi porto l'informazione del livello precedente, e riapplico la verifica precedente
3. Ripeto 1 e 2 fino a che non raggiungo la radice, a quel punto al nodo radice aggiungo l'informazione $t_{\max}$, che mi indentifica il tempo massimo per visitare il sottoalbero

**Check Finale**

La condizione da verificare è la seguente : 
$$EA_{\min,sx}\leq t_{\max,dx}\land EA_{\min,dx}\leq t_{\max,sx}$$
Se questa condizione viene verificata, allora possiamo affermare che l'albero è temporalmente connesso.

## Fase 1 (Preprocessing)

L'idea è quella di far partire dalla **root** una visita DFS Temporale, dove per DFS Temporale si intende una DFS che visita il nodo solo se esso rispetta la condizione di crescita temporale dei timestamps.

Se partendo dalla root con questa visita riesco a toccare tutti i nodi, allora ritorno True e procedo a fase 2, altrimenti ritorno False ed esco. 

Se ritorno False in questa fase posso concludere subito che l'albero non è temporalmente connesso, in quanto esiste almeno un nodo che sicuramente non può connettersi temporalmente alla radice.

**Quanto costa questa visita?** : La visita DFS Temporale ha un costo lineare nel numero di timestamps totali, ovvero $$O(M)$$
## Fase 2

La fase 2 prevede la ricerca delle foglie, nel sottoalbero sx e dx, che si trovano nella massima profondità che hanno timestamp minimo.

**Quanto costa questa fase?** : La ricerca di queste foglie ha un costo lineare nel numero di timestamp, e quindi impiega tempo $$O(M)$$
## Fase 3

La seconda fase prevede un'approccio diverso.

Partiamo da un qualunque sottoalbero, e procedendo **bottom-up** mi calcolo l'earliest-arrival time **minimo** fino al nodo root.

Per $EA_{\min}$ intendiamo l'earliest-arrival che parte dalla foglia più profonda con timestamp minimo, e che da li arriva fino a root

**Quanto costa questa fase?** : La ricerca bottom-up dell'earliest-arrival time minimo impiega tempo $$O(\log M\cdot\log L)$$
Con $M=\text{num. timestamps},L=\text{num. timestamps max su arco}$

## Fase 4

La quarta fase prevede l'uso di un approccio bottom-up per calcolare il tempo massimo per visitare il sottoalbero.

La spiegazione è descritta in precedenza.

Il costo di questa fase è $$O(M)$$

## Check Finale

Il check finale si occupa solo di controllare se la condizione $$EA_{\min,sx}\leq t_{\max,dx}\land EA_{\min,dx}\leq t_{\max,sx}$$
viene verificata o no.

Il costo è costante, ovvero $O(1)$
## Costo totale algoritmo

La fase di preprocessing dei valori costa $$O(M)$$
La fase 2 costa $$O(M)$$
La fase 3 costa $$O(\log M\cdot\log L)$$
Per questa fase il costo va raddoppiato, in quanto vale la simmetria del problema.

La fase 4 costa $$O(1)$$
Di conseguenza il costo totale dell'algoritmo risulta essere $$O(M)+O(M)+O(M)+O(\log M\log L)+O(1)\implies O(M)+O(\log M\log L)$$
Possiamo notare che l'algoritmo risulta essere lineare nel numero di timestamp, e anche nel caso peggiore il costo computazionale sarà $$O(M)$$
## Correttezza dell'algoritmo

La correttezza della dimostrazione e dell'algoritmo dipende dal fatto che ogni fase sia implementata in modo rigoroso e che i vincoli posti siano sufficienti per garantire la proprietà di **connessione temporale**. 
Consideriamo i punti critici 

---
### **1. Fase 1: Verifica della connettività temporale**

L'algoritmo di visita **DFS Temporale** esplora solo i nodi i cui timestamp sugli archi sono maggiori/uguali al tempo attuale di visita. Infatti alla fine della dfs avremo un'insieme di nodi definito in questo modo 
$$V(root)=\{v\in V:t_{v}\geq t_{root}\}$$
Se la visita riesce a visitare tutti i nodi partendo da root, procediamo verso la fase 2, altrimenti ritorniamo False, e affermiamo che l'albero non è temporalmente connesso.

Questo lo possiamo affermare perchè, se dalla root esiste almeno un nodo che non può essere raggiunto, allora significa che su un determinato arco i timestamp sono strettamente minori del tempo di visita attuale. 

Questo implica che sul percorso da root al nodo, ovvero $P_{root\to u}$ ,esiste un arco che va a rompere la sequenza crescente dei timestamp, e di conseguenza questo implica che root e $u$ non possono connettersi temporalmente.

---
### **2. Fase 2: Ricerca della foglia più profonda con timestamp minimo**

Questa fase si concentra sul ricercare le foglie più profonde dei rispettivi sottoalberi, tale che la foglia che viene presa è quella con timestamp minimo fra tutte le foglie in profondità massima.

Perchè cercare questo tipo di foglia? Perchè così facendo, possiamo sfruttare queste foglie per far partire il calcolo dell'$EA_{\min}$ fino al nodo root.

L'osservazione che comanda questa dimostrazione è la seguente : 

>[!info]- Osservazione chiave
>Valgono le due condizioni : 
>1. Se $\not\exists EA_{\min}\implies\not\exists EA_{\max}$
>2. Se $\not\exists EA_{\max}\implies\text{non è detto che }\not\exists EA_{\min}$

Queste due condizioni si possono dimostrare in modo logico : 
1. Se l'$EA_{\min}$ non esiste, allora significa che se parto dalla foglia più profonda con timestamp minimo non riesco a raggiungere l'altro nodo, che nel nostro caso è la root. Questo implica che anche se parto dalla foglia più profonda con timestamp massimo, non riuscirò comunque a raggiungere la root.
2. Se l'$EA_{\max}$ non esiste, significa che se parto dalla foglia più profonda con timestamp massimo non riesco a raggiungere l'altro nodo, che nel nostro caso è la root. Questo però non implica che sicuramente non esiste $EA_{\min}$ . Infatti, semplicemente possiamo avere la casistica in cui l'$EA_{\max}$ non esiste a causa di una sequenza non crescente tra due nodi, partendo dal nodo con timestamp massimo, ma avere allo stesso tempo l'$EA_{\min}$ partendo sempre da quel nodo.

---
### **3. Fase 3: Calcolo dell'EA minimo**

In questa fase ci occupiamo di calcolare l'$EA_{\min}$ partendo dalla foglia in fase 2 fino alla radice.

L'algoritmo che fa ciò si basa sulla struttura dati del paper del professore, e la dimostrazione di correttezza è spiegata li

---
### **4. Fase 4: Calcolo tempo massimo per visitare il sottoalbero**

#### **1. Correttezza dell'aggiornamento a livello locale**

Per ogni nodo NN:

- Se $N$ è una **foglia**, il tempo massimo per visitarlo è semplicemente il massimo $t_\max=\max⁡(\omega(N))$ dei suoi timestamp. Questo è corretto perché una foglia non ha figli da considerare.
- Se $N$ ha figli $L$ (sinistro) e $R$ (destro), il tempo massimo per visitare il sottoalbero dipende da:
    - Il tempo massimo $t_{\max,L}$ per visitare il sottoalbero sinistro.
    - Il tempo massimo $t_{\max,R}$​ per visitare il sottoalbero destro.
    - Per garantire che entrambi i figli siano raggiungibili, $t_\max$​ deve essere il **minimo** tra $t_{\max,L}​$ e $t_{max,R}​$, poiché il percorso verso entrambi deve essere valido temporalmente.

**Correttezza locale**: Questo approccio assicura che si selezioni sempre un tempo che permetta di visitare sia il sottoalbero sinistro che il destro.

---

#### **2. Propagazione bottom-up**

Il calcolo viene effettuato risalendo dai nodi foglia fino alla radice:

- Ogni passo garantisce che $t_\max$​ sia valido per il sottoalbero considerato.
- Poiché ogni nodo calcola $t_\max​$ in base ai figli, il risultato propagato verso la radice rappresenta il tempo massimo per visitare l'intero sottoalbero.

**Correttezza globale**: La propagazione bottom-up garantisce che ogni sottoalbero soddisfi i vincoli temporali richiesti, e il risultato finale rappresenta il tempo massimo per visitare tutto il sottoalbero.

### **5. Check finale**

Nell'ultima fase si fa un semplice controllo tra gli $EA_{\min}$ e i $t_{max}$ dei rispettivi sottoalberi

Se vale che l'$EA_{\min,sx}\gt t_{\max,dx}$, allora significa che il tempo minimo che ci vuole per risalire il sottoalbero sinistro verso la radice non combacia con il tempo massimo per visitare il sottoalbero destro, quindi significa che i nodi del sottoalbero sinistro non potranno mai visitare i nodi nel sottoalbero destro.

Ovviamente la stessa cosa vale per l'$EA_{\min,dx}$ e $t_{\max,sx}$.

### Conclusione

Seguendo tutte le fasi dell'algoritmo, andiamo a coprire tutte queste casistiche : 
1. I nodi di un sottoalbero sono temporalmente connessi fra loro (fase 1+fase3)
2. I nodi di un sottoalbero possono visitare i nodi dell'altro sottoalbero (fase 3+fase4)

E di conseguenza l'algoritmo è corretto, e ritorna correttamente True o False

## Codice dell'algoritmo

```python title="is_temporaly_connected"
from bisect import bisect_left

class Node:
    def __init__(self, value, weight=[]):
        self.value = value
        self.weight = weight
        self.left = None
        self.right = None

def build_temporal_tree(node, parent=None, tree=None):
    if tree is None:
        tree = {}

    if node is None:
        return tree

    if parent is not None:
        if node.value not in tree:
            tree[node.value] = []
        tree[node.value].append((parent.value, node.weight))

    build_temporal_tree(node.left, node, tree)
    build_temporal_tree(node.right, node, tree)

    return tree

def print_temporal_tree(tree):
    for node, edges in tree.items():
        print(f"{node}: {edges}")

def EA_min_query_function(tree, u, v, t_start):
    current_node = u
    current_time = t_start

    while current_node != v:
        neighbors = tree.get(current_node, [])
        parent = None
        times = []

        for neighbor, timestamps in neighbors:
            if neighbor == v or neighbor == neighbors[0][0]:
                parent = neighbor
                times = timestamps
                break

        if not parent or not times:
            return float("-inf")

        idx = bisect_left(times, current_time)
        if idx == len(times):
            return float("-inf")

        max_valid_time = min(times[idx:])
        current_time = max_valid_time
        current_node = parent

    return current_time

def find_node_with_max_weight(node, depth=0):
    """
    Trova la foglia più profonda con il timestamp minimo alla sua profondità.

    Args:
        node: Nodo corrente.
        depth: Profondità corrente del nodo.

    Returns:
        Una tupla (timestamp minimo, nodo corrispondente, profondità).
    """
    if node is None:
        return float("inf"), None, -1  # Nessun nodo

    # Se è una foglia, restituisci il timestamp minimo
    if node.left is None and node.right is None:
        min_timestamp = min(node.weight, default=float("inf"))
        return min_timestamp, node, depth

    # Ricorsione sui figli
    left_min, left_node, left_depth = find_node_with_max_weight(node.left, depth + 1)
    right_min, right_node, right_depth = find_node_with_max_weight(node.right, depth + 1)

    # Scegli la foglia più profonda; in caso di parità, quella con il timestamp minimo
    if left_depth > right_depth:
        return left_min, left_node, left_depth
    elif right_depth > left_depth:
        return right_min, right_node, right_depth
    else:  # Stessa profondità
        if left_min <= right_min:
            return left_min, left_node, left_depth
        else:
            return right_min, right_node, right_depth

def calculate_maximum_earliest_arrivals(tree, left_leaf, right_leaf, root, max_timestamps, EA_query_function):
    """
    Calcola il minimo Earliest Arrival (EA minimo) per i percorsi dalle foglie sinistra e destra alla radice.

    Args:
        tree: struttura dati che rappresenta l'albero temporale.
        left_leaf: nodo foglia più profondo tutto a sinistra.
        right_leaf: nodo foglia più profondo tutto a destra.
        root: nodo radice dell'albero.
        max_timestamps: tuple con i timestamp massimi per le foglie sinistra e destra.
        EA_query_function: funzione che implementa la query EA dalla struttura del paper.

    Returns:
        - Un dizionario contenente EA_sx e EA_dx se validi, oppure False se almeno uno è infinito.
    """
    # Timestamp massimo per le foglie
    max_t_sx, max_t_dx = max_timestamps

    # Calcola EA per il percorso dalla foglia sinistra alla radice
    EA_sx = EA_query_function(tree, left_leaf.value, root.value, max_t_sx)

    # Calcola EA per il percorso dalla foglia destra alla radice
    EA_dx = EA_query_function(tree, right_leaf.value, root.value, max_t_dx)

    # Controlla se uno dei risultati è infinito
    if EA_sx == float("-inf") or EA_dx == float("-inf"):
        return False  # Non c'è percorso temporalmente connesso

    # Salva le informazioni nella radice
    root_info = {
        "Min_EA_sx": EA_sx,
        "Min_EA_dx": EA_dx
    }
    return root_info

def verify_temporal_connectivity(node, current_time=float("-inf")):
    """
    Verifica se l'albero è temporalmente connesso usando una visita DFS.

    Args:
        node: Nodo corrente dell'albero.
        current_time: Timestamp corrente minimo per rispettare la connettività temporale.

    Returns:
        True se l'albero è temporalmente connesso, False altrimenti.
    """
    if node is None:
        return True  # Nodo vuoto è sempre connesso

    # Controlla se esiste un timestamp valido
    valid_timestamps = [t for t in node.weight if t >= current_time]
    if not valid_timestamps:
        return False  # Non esiste un percorso temporale valido

    # Procedi verso i figli con il timestamp minimo richiesto
    next_time = min(valid_timestamps)
    left_connected = verify_temporal_connectivity(node.left, next_time)
    right_connected = verify_temporal_connectivity(node.right, next_time)

    return left_connected and right_connected

def calculate_max_timestamp_bottom_up(node):
    """
    Calcola il timestamp massimo per visitare un intero sottoalbero usando un approccio bottom-up.

    Args:
        node: Nodo corrente.

    Returns:
        Il timestamp massimo utilizzabile per il sottoalbero.
    """
    if node is None:
        return float("inf")  # Nodo vuoto non impone restrizioni

    # Calcola ricorsivamente i timestamp massimi per i figli
    left_max = calculate_max_timestamp_bottom_up(node.left)
    right_max = calculate_max_timestamp_bottom_up(node.right)

    # Calcola il massimo utilizzabile per il nodo corrente
    node_max = max(node.weight, default=float("-inf"))

    return min(left_max, right_max, node_max)

def algoritmo(root):
    print("--------FASE 1--------")
    # Fase 1: Verifica della connettività temporale
    if not verify_temporal_connectivity(root.left):
        return "L'albero non è temporalmente connesso."

    print("\nCheck Fase 1 OK")

    # Fase 2: Trova le foglie più profonde con timestamp minimo nei sottoalberi
    min_left, left_node, _ = find_node_with_max_weight(root.left)
    min_right, right_node, _ = find_node_with_max_weight(root.right)

    print("\n--------FASE 2--------")
    print(f"\nFoglia più profonda sottoalbero sinistro: {left_node.value if left_node else None}, Timestamp: {min_left}")
    print(f"Foglia più profonda sottoalbero destro: {right_node.value if right_node else None}, Timestamp: {min_right}")

    print("\n--------FASE 3--------")
    # Fase 3: Calcolo dell'EA minimo partendo dalle foglie trovate in Fase 2
    tree = build_temporal_tree(root)
    print("\nStruttura dell'albero temporale:")
    print_temporal_tree(tree)

    EA_sx = EA_min_query_function(tree, left_node.value, root.value, min_left) if left_node else float("-inf")
    EA_dx = EA_min_query_function(tree, right_node.value, root.value, min_right) if right_node else float("-inf")

    print(f"EA minimo dal nodo sinistro: {EA_sx}")
    print(f"EA minimo dal nodo destro: {EA_dx}")

    print("\n--------FASE 4--------")
    # Fase 4: Calcolo dei timestamp massimi per entrambi i sottoalberi
    t_max_sx = calculate_max_timestamp_bottom_up(root.left)
    t_max_dx = calculate_max_timestamp_bottom_up(root.right)

    print(f"\nTimestamp massimo sottoalbero sinistro: {t_max_sx}")
    print(f"Timestamp massimo sottoalbero destro: {t_max_dx}")

    # Check finale
    if EA_sx <= t_max_dx and EA_dx <= t_max_sx:
        print("\nCheck Fase 4 OK")
        return "\nL'albero è temporalmente connesso."
    else:
        print("\nCheck Fase 4 NO")
        return "\nL'albero non è temporalmente connesso."
```

---
# Algoritmo 2

Pseudocode : 

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
def dfs_EA_tmax(root):
    if root is None:
        return float("-inf"),float("inf")
    if root.left == None and root.right == None:
        return root.weight[0],root.weight[-1] #min(root.weight), max(root.weight)

    min_sx,max_sx = dfs_EA_tmax(root.left)
    min_dx,max_dx = dfs_EA_tmax(root.right)

    if not (min_sx<=max_dx or min_dx<=max_sx):
        return float("inf"),float("inf")

    EA = max(min_sx,min_dx)
    t_max_visita = min(max_sx,max_dx)
    k = binary_search(root.weight,EA) # K = minimo timestamp >= EA
    if k == -1: 
        return float("inf"),float("inf")
    return k,min(t_max_visita,root.weight[-1])
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
