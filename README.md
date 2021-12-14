# Tesi: Produzione Scientifica

## DESCRIZIONE:
Tool che gestisce diverse funzionalità tramite una interfaccia grafica tra cui:
- Gestione di un gruppo di persone in maniera persistente tramite un database (consigliato SQLite), con aggiunta tramite csv (o json) o in maniera manuale.
- Query delle raccolte bibliometriche tramite API per ottenere gli indici bibliometrici delle persone.
- Salvataggio dei risultati della ricerca per permettere il confronto (grafico) tra due stati temporali salvati, in modo da valutare l’andamento delle metriche.

## MATERIALE UTILIZZATO:
- [API Phyton per accedere al Database di Scopus mediante le loro API REST](https://github.com/jkitchin/scopus)
- [SOAP Client for querying the Web of Science database](https://github.com/enricobacis/wos) (al momento inutilizzato)
- [Framework Phyton Django](https://www.djangoproject.com)
	- [Django Registration](https://django-registration.readthedocs.io/en/3.2/index.html)
	- [Django Rest Framework](https://www.django-rest-framework.org) 

## ATTENZIONE:
E' necessario possedere una API Key ed eventualmente un token per poter reperire le API di Scopus.
  
Nel codice non ci saranno riferimento ad API Key e Token poichè una volta scaricato il pacchetto andrà modificato il file (C:\Users\<user>\\.pybliometrics\config.ini)
dove al posto di user dovrete sostituire il vostro nome utente e aggiungere:
```
[Authentication]
APIKey = ... (Obbligatorio)
InstToken = ... (Opzionale)
```
  
E' necessario possedere una API Key anche per le API di WoS (impossibile richiederla come singolo ma solo come organizzazione es. Università).

## FUNZIONALITA':
- [x] Implementazione della classe utente custom (mail come id ed username unico a differenza del modello Django di default)
- [x] Registrazione in 2 passi (form + mail di conferma) (Simulato il flusso email tramite file per un debug più facile)
- [x] Login, Logout
- [x] Recupero della password (da non loggati) via email (Simulato il flusso email tramite file per un debug più facile)
- [x] Modifica della password (da loggati)
- [x] CRUD Tabella Agroups (API)
- [x] CRUD Tabella Affiliations (API)
- [x] CRUD Tabella Authors (API)
- [x] CRUD Tabella Snapshot (API)
- [ ] Aggiornamento dello stile del front-end

## STRUTTURA del PROGETTO:
- Nella cartella [produzione_scientifica](produzione_scientifica) è presente il progetto Django vero e proprio suddiviso in
 - [produzione_scientifica/gbliometrics](Backend)
 - [produzione_scientifica/frontend](Frontend)
 - [produzione_scientifica/sent_emails](Cartella contente le simulazioni di email per creare account o recuperare password)
 - [produzione_scientifica/snapshots](Snapshots: File su cui sono salvati gli stati temporali di un gruppo di autori)
 - [produzione_scientifica/templates](Templates)
- Nella cartella [TEST](TEST) sono presenti le prove preliminari effettuate tramite client Python.

## GUIDE seguite:
- Classe User custom: 
  - https://testdriven.io/blog/django-custom-user-model
- Registrazione in 2 passi (form + mail di conferma simulata tramite file):
  - https://django-registration.readthedocs.io/en/3.2/activation-workflow.html
  - https://django-registration.readthedocs.io/en/3.2/quickstart.html
  - https://stackoverflow.com/questions/21004455/how-to-subclass-registration-form-in-django-registration	
- Pagine di Login e Logout:
  - https://learndjango.com/tutorials/django-login-and-logout-tutorial
- Reset della password via email (email simulata tramite file) e modifica della password da loggatti:
  - https://learndjango.com/tutorials/django-password-reset-tutorial
- API Rest
  - https://www.django-rest-framework.org/tutorial/quickstart
  - https://www.youtube.com/watch?v=TmsD8QExZ84&ab_channel=DennisIvy
