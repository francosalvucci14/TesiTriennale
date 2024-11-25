Fase 1 : Prepcrocessing
# Verifico se partendo da root, posso visitare tutti i nodi dell'albero
# (se non è possibile, l'albero non è temporalmente connesso). 
# Per farlo basta fare una visita DFS che controlla se ogni nodo rispetta la condizione di crescita incrementale dei timestamp.

Fase 2 : Calcolo foglia più profonda con peso massimo nei sottoalberi sinistro e destro
# Per trovare la foglia più profonda con peso massimo nei sottoalberi sinistro e destro,
# posso utilizzare la funzione find_deepest_leaves_in_subtrees definita in precedenza.
# Questa funzione calcola la foglia più profonda con peso massimo in un albero binario.
# Per trovare la foglia più profonda con peso massimo nei sottoalberi sinistro e destro,
# posso chiamare questa funzione sui sottoalberi sinistro e destro del nodo radice.
# La funzione restituirà i nodi delle foglie più profonde nei sottoalberi sinistro e destro,
# insieme ai relativi pesi massimi.

Fase 3 : Calcolo dell'EAmax partendo dalla fgolia più profonda fino alla radice
# Questa fase è simmetrica, ovvero vale per entrambi i sottoalberi, quindi ci concentreremo solo su un sottoalbero
# A questo punto, applico l'algoritmo per calcolare l'EA, usando la struttura dati del professore, ovvero quella che impiega tempo O(logMlogL)
# Se la funzione ritortna -inf, sia da un lato che dall'altro, allora ritorno subito False (l'albero non è temporalmente connesso)

Fase 4 : Verifica finale
# Se l'EAmax calcolato è maggiore o uguale al timestamp massimo del sottoalbero sinistro e destro, allora l'albero è temporalmente connesso. ??
# Altrimenti, l'albero non è temporalmente connesso.

# Oppure faccio cosi, parto dall'EAmax da sx, e lo uso come input per la visita DFS temporale da root, ovvero uso EAmax ad sx come t_start per la visita.
# Faccio la stessa cosa da EAmax da dx, se uno dei due ritorna false allora ritorno False e affermo che l'albero non è temporalmente connesso.
# Altrimenti, se entrambi ritornano True, allora l'albero è temporalmente connesso.


