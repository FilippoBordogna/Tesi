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
  Nel codice non ci saranno riferimento ad API Key e Token poichè una volta scaricato il pacchetto andrà modificato il file C:\Users\_user_\.pybliometrics\config.ini
  dove al posto di _user_ dovrete sostituire il vostro nome utente e aggiungere:
  [Authentication]
  APIKey = ... (Obbligatorio)
  InstToken = ... (Opzionale)
  
- E' necessario possedere una API Key anche per le API di WoS (impossibile richiederla come singolo ma solo come organizzazione es. Università).

FUNZIONALITA' IMPLEMENTATE:
- Implementazione della classe utente custom (mail come id ed username unico a differenza del modello Django di default)
- Registrazione in 2 passi (form + mail di conferma) (Simulato il flusso email tramite file per un debug più facile)
- Login, Logout
- Recupero della password (da non loggati) via email (Simulato il flusso email tramite file per un debug più facile)
- Modifica della password (da loggati)

FUNZIONALITA' DA IMPLEMENTARE PROSSIMAMENTE:
- Mappare API già testate nella cartella TEST per successive chiamate API da parte dell'app
- CRUD Tabella Authors
- CRUD Tabella Groups
- CRUD Tabella Authors_Groups
- CRUD Tabella Users_Groups
- CRUD Tabella Stats

STRUTTURA del PROGETTO:
- Nella cartella 'produzione_scientifica' è presente il progetto Django vero e proprio.
- Nella cartella 'TEST' sono presenti le prove preliminari effettuate tramite client Python.

GUIDE seguite:
- Classe User custom: 
	https://testdriven.io/blog/django-custom-user-model
- Registrazione in 2 passi (form + mail di conferma simulata tramite file):
	https://django-registration.readthedocs.io/en/3.2/activation-workflow.html
	https://django-registration.readthedocs.io/en/3.2/quickstart.html
	https://stackoverflow.com/questions/21004455/how-to-subclass-registration-form-in-django-registration	
- Pagine di Login e Logout:
	https://learndjango.com/tutorials/django-login-and-logout-tutorial
- Reset della password via email (email simulata tramite file) e modifica della password da loggatti:
	https://learndjango.com/tutorials/django-password-reset-tutorial 
