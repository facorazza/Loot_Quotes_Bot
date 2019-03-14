# Loot_Quotes_Bot

### Media dei prezzi
L'approssimazione più sostanziale di tutto il processo riguarda il calcolo della media dei prezzi degli oggetti. Essendo i prezzi una misura dipendente dal tempo e dai valori passati degli stessi, l'insieme considerato non può essere considerato un **campione**. Per ovviare a ciò utilizzeremo i valori contenuti nell'intervallo di tempo più ristretto possibile, cercando comunque di mantenere una numerosità sostanziale per ogni singolo oggetto, in modo tale da eliminare, o almeno da ridurre drasticamente, la dipendenza tra le misure passate e da rendere la distribuzione il più uniforme possibile per ogni singolo oggetto.

### Incertezza
L'incertezza delle quotazioni viene calcolata attraverso la seguente formula:
*Formula*
Il valore trovato deve essere aggiunto e sottratto al valore della quotazione, trovando, in questo modo, un intervallo di confidenza entro cui il prezzo reale può cadere.
 *Intervallo di confidenza:* ksigma
L'incertezza mostrata dal bot utilizza k=1 che indica una confidenza di circa (simbolo)il 68% che il prezzo cada nell'intervallo.
Per esempio:
Raddoppiando il valore di k la confidenza dell'intervallo sale a circa il (simbolo)95%.
Quindi, riprendendo l'esempio precedente:
È possibile aumentare k ulteriormente ma ovviamente ne consegue un aumento dell'intervallo.

### Mediana e quantili
Il bot riordina i dati per prezzo in modo crescente e ne calcola la mediana. La mediana è il valore che si trova in mezzo e che divide i prezzi in due insiemi equipartiti. Analogamente il primo e il terzo quartile dividono ulteriormente i due sottoinsiemi appena creati. Questa suddivisione permette di avere un'idea della distribuzione dei dati. Infatti è possibile constatare che il 50% dei prezzi è contenuto nell'intervallo tra il *primo* e il *terzo quartile*. Conoscendo inoltre il prezzo *minimo* si deduce che l'intervallo più piccolo contenete il 25% dei dati si trova tra il minimo e il primo quartile. Analogamente tutto ciò vale anche per l'intervallo superiore, se si conosce il *massimo* dell'insieme.