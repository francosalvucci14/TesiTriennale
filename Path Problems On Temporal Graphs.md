
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



# 2. Notazione dei Grafi Temporali

# 3. Definizione dei Grafi Temporali

