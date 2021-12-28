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
  
<!-- E' necessario possedere una API Key anche per le API di WoS (impossibile richiederla come singolo ma solo come organizzazione es. Università). -->

## TASKS':
- [x] Implementazione della classe CustomUser (mail come id ed username unico a differenza del modello Django di default) (MODELLO)
- [x] Implementazione della classe Affiliation (MODELLO)
- [x] Implementazione della classe Author (MODELLO)
- [x] Implementazione della classe Agroup (Gruppi di autori) (MODELLO)
- [x] Implementazione della classe Snapshot (MODELLO)
- [x] CRUD Tabella Agroups (API)
- [x] CRUD Tabella Affiliations (API)
- [x] CRUD Tabella Authors (API)
- [x] CRUD Tabella Snapshot (API)
- [x] Pagina Home (FRONTEND)
- [x] Pagina di Login (FRONTEND)
- [x] Pagina di Creazione account in 2 passaggi (Immissione dei dati + conferma via Email(Simulata su file)) (FRONTEND)
- [x] Pagina di modifica della password (FRONTEND)
- [x] Pagina di reset della password in 3 passaggi (Richiesta di reset, conferma via Email(Simulata su file), Immissione dei nuovi dati) (FRONTEND)
- [x] Pagina dei Gruppi (FRONTEND)
- [x] Pagina dei dettagli dei gruppi (Lista autori nel gruppo) (FRONTEND)
- [x] Pagina dei dettagli degli autori (FRONTEND)
- [x] Pagina dei dettagli delle affiliazioni(FRONTEND)
- [x] Pagina di visualizzazione delle statistiche di un gruppo (computazione dei dati al momento) con eventuale salvataggio dello snapshot (FRONTEND)
- [x] Pagina di visualizzazione di tutti gli snapshot salvati (FRONTEND)
- [x] Pagina di visualizzazione di uno snapshot salvato in precedenza (FRONTEND)
- [ ] Pagina di confronto degli snapshot (FRONTEND)
- [ ] Pagina di ricerca degli autori (FRONTEND)
- [ ] Effettuare i controlli nelle chiamata AJAX laddove necessario (FRONTEND)
- [ ] Aggiungere la possibilità di modificare il titolo di uno snapshot salvato (API + FRONTEND)
- [ ] Aggiungere la possibilità di prendere i dati dei dettagli affiliazione anche dal DB (Aggiungi un parametro refresh) (FRONTEND)
- [ ] Migliorare la grafica (FRONTEND)
- [ ] Aggiungere alla pagina dei dettagli degli autori una sezione contenente l'elenco dei documenti scritti (FRONTEND + API)


## STRUTTURA del PROGETTO:
- Nella cartella [produzione_scientifica](produzione_scientifica) è presente il progetto Django vero e proprio suddiviso in cartelle:
 	- [Backend: Modelli e Migrazioni del DB e API](produzione_scientifica/gbliometrics)
 	- [Frontend: Templates](produzione_scientifica/frontend)
 	- [Snapshots: File su cui sono salvati gli stati temporali di un gruppo di autori](produzione_scientifica/snapshots)
 	- [Templates: Modelli HTML per la gestione degli utenti](produzione_scientifica/templates)
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
- AJAX
  - https://www.youtube.com/watch?v=hISSGMafzvU&ab_channel=DennisIvy
- BOOTSTRAP 4
  - https://www.w3schools.com/bootstrap4
  - https://www.w3schools.com/js/js_graphics_chartjs.asp
