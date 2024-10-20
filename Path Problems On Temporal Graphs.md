
```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
includeLinks: true # Make headings clickable
debugInConsole: false # Print debug info in Obsidian console
```

# Astrazione

Lo **`Shortest Path`** è un problema fondamentale sui grafi.

Il concetto di shortest path classico è insufficiente, o addirittura imperfetto nei grafi temporali, dato che le informazioni temporali determinano l'ordine delle attività lungo qualsiasi percorso.

Calcolare questi **`percorsi temporali`** è impegnativo poiché i sottopercorsi di un percorso "corto" potrebbero non essere "corti" in un grafico temporale.

![[Temporal-Static Graph.png|Figura 1]]

# 1. Introduzione

Molti grafi nel mondo reale sono **Grafi Temporali**, dove ogni vertice comunica con un'altro vertice ad un'istanza di tempo specifica.

**Esempio** : 

Assumiamo che $\text{Figura}\space1(a)$ mostri un network di trasporto aereo, allora i due nodi $a$ e $b$ indicano che esiste un volo da $a$ a $b$ nel giorno $1$ e nel giorno $2$, infatti i numeri $1$ e $2$ sugli archi rappresentano il tempo di partenza dei voli.

Ci sono vari esempi di grafi temporali nella vita reale, come:
- Chiamate tra persone
- Social Network
- etc...

Ogni grafo temporale ha la sua versione `statica`, infatti i grafi temporali sono spesso condensati in quelli che si chiamano `grafi statici`, perchè questa versione è molto più semplice da gestire.

**Esempio**

Per calcolare le Componenti Fortemente Connesse ($SCCs$) di un grafo statico abbiamo un'algoritmo lineare, mentre per calcolare quelle di un grafo temporale **NON** esiste un'algoritmo polinomiale.

>[!warning]- Osservazione
>Si può notare che alcuni percorsi nel grafo statico potrebbero non essere un percorso completo nel grafo temporale.

Per esempio, $\left< a,b,g,j\right>$ è un percorso in $\text{Figura}\space1(b)$, ma $\left< a,b,g,j\right>$ in $\text{Figura}\space1(a)$ è problematico perchè $g$ ha solo un volo per $j$ al giorno $2$ ma non lo possiamo raggiungere prima del giorno $4$.

L'esempio soora indica che un grafo statico condensato può presentare informazioni fuorvianti relative al grafo temporale originale, e quindi è essenziale mantenere le informazioni temporali nei grafi.

Esistono 4 tipi di percorsi temporali, che collettivamente si chiamano **minimun temporal paths** (percorsi temporali minimi), dato che loro danno il valore minimo per differenti misure:

1. `earliest-arrival path` : percorso che fornisce l'earliest arrival time partendo da una sorgente $x$ fino a un target $y$
2. `latest-departure path` : percorso che fornisce il latest departure time partendo da sorgente $x$ fino a un target $y$ entro un certo tempo 
3. `fastest path` : il percorso attraverso il quale si va da $x$ a $y$ con il tempo trascorso minimo
4. `shortest path` : il percorso più breve da $x$ a $y$ in termini di tempo di attraversamento complessivo necessario sull'arco

>[!warning]- Osservazione
>Notare che uno shortest path potrebbe non essere necessariamente un fastest path
>Notare anche che un fastest path potrebbe non essere un earliest-arrival path

Per calcolare questi percorsi non possiamo usare l'approccio Greedy che di norma viene usato nel calcolo dei percorsi per grafi statici, per esempio l'algoritmo di Dijkstra, perchè quelli sono basati sulla proprietà che un sottopercorso di uno shortest path è anch'esso uno shortest path, cosa non necessariamente vera quando calcoliamo uno dei 4 `minimun temporal paths`.

# 2. Notazione dei Grafi Temporali

## 2.1 Definizione di un grafo temporale

**`Notazione di un grafo temporale`**

Sia $G=(V,E)$ un grafo temporale, con $V$ denotiamo l'insieme dei nodi, e con $E$ l'insieme degli archi.

Un'arco $e \in E$ è una **quadrupla** $(u,v,t,\lambda)$, dove:
- $u,v\in V$
- $t$ è il **tempo di inizio (starting time)**
- $\lambda$ è il **tempo di traversata (traversal time)** per andare da $u \to v$ partendo al tempo $t$
- $t+\lambda$ è il **tempo di fine**

Denotiamo lo starting time di $e$ con $t(e)$ e il traversal time con $\lambda(e)$

Se gli archi non sono diretti, allora lo starting time e il traversal time di un arco sono gli stessi da $u\to v$ e da $v\to u$.

Vediamo alcuni esempi:
- **Chiamata o Sistema di Messaggistica** : ogni vertice rappresenta una persona, e un'arco $(u,v,t,\lambda)$ indica che il vertice $u$ comunica con $v$ al tempo $t$, e il tempo di connessione è $\lambda$.

- Social Network : ogni vertice rappresenta una persona, e un'arco $(u,v,t,\lambda)$ può essere un'interazione tra $u$ e $v$ al tempo $t$ che prende tempo $\lambda$.

## 2.2 Insiemi di archi temporali

Denotiamo con $\prod(u,v)$ l'insieme degli archi temporali da $u$ verso $v$, mentre il numero di questi archi temporali è $\pi(u,v)$, infatti vale $$\pi(u,v)=\left|\prod(u,v)\right|$$
Definiamo anche il **massimo** numero di archi temporali da $u$ a $v$ , $\forall u,v\in V$, come $$\pi=\text{max}\{\pi(u,v):(u,v)\in(V\times V)\}$$
Il valore di $\pi$ può essere molto grande per molti grafi temporali reali.

### 2.2.1 Uguaglianza di due archi temporali

In un grado temporale $G=(V,E)$, dati due archi temporali $e_1=(u_1,v_1,t_1,\lambda_1)\in E,e_2=(u_2,v_2,t_2,\lambda_2)\in E$ , abbiamo che 

$$e_1=e_2\iff(u_1=u_2\land v_1=v_2\land t_1=t_2\land\lambda_1=\lambda_2)$$

Se noi condensiamo archi temporali in archi statici, otteniamo il corrispondente grafo statico, definito come $G_s=(V_S,E_s)$, dove $V_s=V$ e $E_s={(u,v):(u,v,t,\lambda)\in E}$.
Come possiamo notare, la condensazione **rimuove** tutte le informazioni temporali dagli archi di $E$ e combina tutti gloi archi che hanno stessi nodi di inizio e fine in un singolo arco.

### 2.2.2 Vicinato di un nodo

Definiamo il numero di vertici di $G$ e $G_s$ come $n=|V|=|V_s|$, e il numero di archi di $G$ come $M=|E|$, mentre quelli di $G_s$ sono $m=|E_s|$ 

Definiamo l'insieme dei **vicini-uscenti (out-neighbors)** di un vertice $u$ in $G$ o $G_s$ come $$\Gamma_{\text{out}}(u,G)=\Gamma_{\text{out}}(u,G_s)=\{v:(u,v,t,\lambda)\in E\}=\{v:(u,v)\in E_s\}$$
Definiamo il **grado-uscente (out-degree)** di un vertice $u$ in $G$ come 
$$d_{\text{out}}(u,G)=\sum\limits_{v\in\Gamma_{\text{out}}(u,G)}\pi(u,v)$$
e quello di $u$ in $G_s$ come
$$d_{\text{out}}(u,G_s)=\left|\Gamma_{\text{out}}(u,G_s)\right|$$

L'insieme dei **vicini-entranti (in-neighbors)** e il **grado-entrante (in-degree)** di un vertice $u$ in $G$ o $G_s$ sono definiti in modo completamente simmetrico
$$\begin{align}&\Gamma_{\text{in}}(u,G)=\Gamma_{\text{in}}(u,G_s)=\{v:(v,u,t,\lambda)\in E\}=\{v:(v,u)\in E_s\}\\\\&d_{\text{in}}(u,G)=\sum\limits_{v\in\Gamma_{\text{in}}(u,G)}\pi(v,u)\\\\&d_{\text{in}}(u,G_s)=\left|\Gamma_{\text{int}}(u,G_s)\right|\end{align}$$
# 3. Definizione dei Grafi Temporali

# 4. Algoritmi One-Pass per calcolare gli shortest path
