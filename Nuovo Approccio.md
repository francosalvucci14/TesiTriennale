# Algoritmo

L'algoritmo è diviso in più fasi : 
- **Preprocessing (Fase 1)**
- **Fase 2**
## Fase 1 (Preprocessing)

L'idea è quella di far partire dalla **root** una visita DFS Temporale, dove per DFS Temporale si intende una DFS che visita il nodo solo se esso rispetta la condizione di crescita temporale dei timestamps.

Se partendo dalla root con questa visita riesco a toccare tutti i nodi, allora ritorno True e procedo a fase 2, altrimenti ritorno False ed esco. 

Se ritorno False in questa fase posso concludere subito che l'albero non è temporalmente connesso, in quanto esiste almeno un nodo che sicuramente non può connettersi temporalmente alla radice.

**Quanto costa questa visita?** : La visita DFS Temporale ha un costo lineare nel numero di timestamps totali, ovvero $$O(M)$$
## Fase 2

La seconda fase prevede un'approccio diverso.

Partiamo da un qualunque sottoalber, e procedendo **bottom-up** mi calcolo l'earliest-arrival time **massimo** fino al nodo root.

Una volta fatto questo visito i nodi da root, partendo a tempo $t=EA_{max}$, e vedo se tutti i nodi sono visitabili.
Per l'altro sottoalbero il procedimento è letteralmente indentico, in quanto sfruttiamo la simmetria del problema quando parliamo di alberi binari.

Se entrambi i controlli ritornano True, posso affermare che l'albero è temporalmente connesso.
- Questo vale perchè se posso toccare tutti i nodi del sottoalbero di sx, partendo con tempo $t=EA_{dx}$, e allo stesso tempo posso tocccare tutti i nodi del sottoalbero dx partendo a tempo $t=EA_{sx}$, allora significa che tutti i nodi del sottoalbero sx possono comunicare con il sottoalbero dx, e viceversa.

Se uno solo torna False, allora posso affermare che l'albero non è temporalmente connesso.

**Quanto costa questa fase?** : La ricerca bottom-up dell'earliest-arrival time massimo impiega tempo $O(M)$ (forse??)

## Costo totale algoritmo

La fase di preprocessing dei valori costa $$O(M)$$
La fase 2 costa $$O(M),\text{ oppure }O(\log(M)\cdot\log(L))$$
questa casistica dipende da come si implementa la ricerca dell'$EA$ massimo.
Per questa fase il costo va raddoppiato, in quanto vale la simmetria del problema.

Di conseguenza il costo totale dell'algoritmo risulta essere $$O(M)+O(M)[\text{rispettivamente } O(\log(M)\cdot\log(L))]$$
# Correttezza dell'algoritmo

Per dimostrare la correttezza dell'algoritmo completo dobbiamo prima dimostrare la correttezza delle due fasi principali.

## Correttezza fase 1



## Correttezza fase 2