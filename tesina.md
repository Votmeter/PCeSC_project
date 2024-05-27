Progetto Pervasive Computing e Cloud

Regole generali:
    • Dovete creare un progetto su GitHub dove caricare il vostro codice. Ogni partecipante del gruppo di lavoro deve effettuare i commit delle sue parti di codice.
    • Al momento dell’esame Il progetto deve essere in esecuzione sul cloud
    • L’esame consisterà in una presentazione dell’idea sviluppata, supportata da 5-10 slides. E una discussione sul codice creato.
Argomento:
Ci sono numerosi articoli scientifici che analizzano il tracciamento di animali selvatici (wildlife monitoring).
Ad esempio: https://www.nature.com/articles/srep17061
Dove analizzano con GPS le traiettorie di uccelli migratori.
Come scritto nell'articolo il dataset dello studio è disponibile qui:
https://datarepository.movebank.org/entities/datapackage/808c8032-8e24-4ec8-b0b7-91b39d46cb3a
La tesina consiste nel creare un’applicazione web per replicare/modificare i risultati dello studio scientifico
    1. Salvare i dati presenti in un database cloud (firestore o bigquery). Occorre salvare i dati csv, anche manualmente su Cloud Storage, quindi scrivere un’applicazione che legga i dati da Cloud Storage e li salvi sul database (tutti insieme, non occorre simulare l’arrivo dei dati)
    2. Create un applicazione web che ricrei i grafici presenti nell’articolo scientifico, in particolare i grafici di figure 2,4,5 (per la figura 5 deve essere possibile scegliere l’id di un uccello e monitorare la sua traiettoria)
    3. Creare una versione della figura 5 “animata”, l’applicazione cioè ridisegna/ricarica la pagina ad intervalli regolati per visualizzare una sorta di animazione della traiettoria
    4. Il sito ha una sezione disponibile solo agli utenti loggati che permette di modificare i dati nel database. Dovete creare un’interfaccia che consenta di modificare i dati facilmente. Specialmente per quanto riguarda la modifica/inserimento di una nuova traiettoria. Ad esempio posso disegnare una nuova traiettoria con un tool tipo: https://geojson.io/ e importare la nuova traiettoria nel sito (tramite copia e incolla). (l’ideale – facoltativo – sarebbe di importare una traiettoria esistente in un tool tipo geojson.io, modificarla ed inserirla nel sito modificata.
    5. Ovviamente i grafici del punto 2-3 devono cambiare in base alle modifiche fatte