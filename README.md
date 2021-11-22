# Tesi: Produzione Scientifica

DESCRIZIONE:
Tool che gestisce diverse funzionalità tramite una interfaccia grafica tra cui:
- Gestione di un gruppo di persone in maniera persistente tramite un database (consigliato SQLite), con aggiunta tramite csv (o json) o in maniera manuale.
- Query delle raccolte bibliometriche tramite API per ottenere gli indici bibliometrici delle persone.
- Salvataggio dei risultati della ricerca per permettere il confronto (grafico) tra due stati temporali salvati, in modo da valutare l’andamento delle metriche.

MATERIALE UTILIZZATO:
- API Phyton per accedere al Database di Scopus mediante le loro API REST: https://github.com/jkitchin/scopus
- SOAP Client for querying the Web of Science database: https://github.com/enricobacis/wos (al momento inutilizzato)
- Framework Phyton Django

ATTENZIONE:
- E' necessario possedere una API Key ed eventualmente un token per poter reperire le API di Scopus.
  Nel codice non ci saranno riferimento ad API Key e Token poichè una volta scaricato il pacchetto andrà modificato il file C:\Users\<user>\.pybliometrics\config.ini
  dove al posto di <user> dovrete sostituire il vostro nome utente e aggiungere:
  [Authentication]
  APIKey = ... (Obbligatorio)
  InstToken = ... (Opzionale)
  
- E' necessario possedere una API Key anche per le API di WoS (impossibile richiederla come singolo ma solo come organizzazione es. Università).

FUNZIONALITA' IMPLEMENTATE:
- 
- 
- 
FUNZIONALITA' DA IMPLEMENTARE IN FUTURO:
- 
- 
- 

Nella cartella TEST sono presenti le prove preliminari