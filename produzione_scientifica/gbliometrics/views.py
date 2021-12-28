from django.http.response import HttpResponse
from django_registration.forms import User
from pybliometrics.scopus.utils.create_config import create_config
from rest_framework.fields import JSONField, NullBooleanField # Modello User Django
from gbliometrics.models import Agroup, Affiliation, Author, Snapshot # Modelli DB
from datetime import datetime # Libreria Temporale

from rest_framework.decorators import api_view # Decoratore che permette di specificare i metodi HTTP accettati
from rest_framework.response import Response # Risposta JSON
from .serializers import AgroupSerializer, AffiliationSerializer, AuthorSerializer, SnapshotSerializer # Serializzatori (Object->JSON)

from pybliometrics.scopus import AffiliationRetrieval # Ricerca affiliazioni dato l'id
from pybliometrics.scopus import AuthorRetrieval # Ricerca autore dato l'id

from django.core.files.base import ContentFile

import json

def myError(message):
    '''
        Funzione che restituisce una risposta formattata come errore
    '''
    return Response({'status':'false', 'message':message}, status=500) # Errore

####################################################################################
#################################### API GRUPPI ####################################
####################################################################################

@api_view(['GET']) # Accetta solo metodo GET
def groupApiOverview(request):
    '''
        API che ritorna la lista di API dei gruppi che si possono interrogare.
    '''
    
    api_urls = { # Lista delle API disponibili
        'Lista dei gruppi dell\'utente': '/group-list/',
        'Dettagli di un gruppo': '/group-detail/<str:groupId>/',
        'Creazione di un gruppo': '/group-create/',
        'Modifica di un gruppo': '/group-update/<str:groupId>/',
        'Eliminazione di un gruppo': '/group-delete/<str:groupId>/',
        'Aggiunta di un autore': '/group-add-author/<str:groupId>/<str:authorScopusId>/',
        'Rimozione di un autore': '/group-remove-author/<str:groupId>/<str:authorId>/'
    }
     
    return Response(api_urls, status=200) # Successo

@api_view(['GET']) # Accetta solo metodo GET
def groupList(request):
    '''
        API che mostra i gruppi creati dall'utente.
        Se l'utente non è loggato lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        groups = Agroup.objects.filter(user=request.user).order_by('-last_update') # Gruppi appartenenti all'utente
        serializer = AgroupSerializer(groups, many=True) # Conversione Agroup->Dizionario
        return Response(serializer.data, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['GET']) # Accetta solo metodo GET
def groupDetail(request, groupId):
    '''
        API che mostra i dettagli di un gruppo specificato dall'utente.
        Se l'utente non è loggato lancio un errore.
        Se il gruppo specificato non è di proprietà dell'utente o non esiste lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo di cui mi interessano i dettagli
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'") # Errore
        
        serializer = AgroupSerializer(group, many=False) # Conversione Agroup->Dizionario
        
        return Response(serializer.data, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def groupCreate(request):
    '''
        API che crea un gruppo associato all'utente.
        Se l'utente non è loggato lancio un errore.
        Non è possibile aggiungere gli autori al gruppo da qui. (Usare group-add-author).
        Se esiste già un gruppo di proprietà dell'utente con lo stesso nome lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        # Sovrascrivo i campi user, data di creazione e data di ultima modifica settati per evitare modifiche che favoriscono inconsistenza
        request.data['user'] = request.user.id
        request.data['creation'] = datetime.now()
        request.data['last_update'] = datetime.now()
        request.data['authors'] = []
        
        if(Agroup.objects.filter(user=request.user, name=request.data['name']).exists()): # Elemento con uguali campi user e name già presente
            return myError("E' già presente un gruppo associato al tuo utente con lo stesso nome") # Errore

        else: # Non esiste un elemento con uguali campi user e name
            serializers = AgroupSerializer(data=request.data) # Conversione JSON->Agroup
            if(serializers.is_valid()): # Oggetto creato correttamente
                serializers.save(); # Salvo l'oggetto nel DB
                      
                return Response(serializers.data, status=200) # Successo
            else:
                return myError(serializers.error_messages)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def groupUpdate(request, groupId):
    '''
        API che modifica un gruppo associato all'utente (Non ottimale per modifiche sugli autori appartenenti al gruppo).
        Se l'utente non è loggato lancio un errore.
        Se il gruppo specificato non è di proprietà dell'utente o non esiste lancio un errore.
        Non è possibile modificare gli autori al gruppo da qui. (Usare group-add-author).
        Se esiste già un gruppo di proprietà dell'utente con lo stesso nome specificato come modifica lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato     
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando modificare i dati di un gruppo inesistente o non di tua proprieta'") # Errore
        
        # Sovrascrivo i campi id, user, data di creazione e data di ultima modifica per evitare modifiche che favoriscono inconsistenza
        request.data['id'] = group.id
        request.data['user'] = request.user.id
        request.data['last_update'] = datetime.now()
        request.data['creation'] = group.creation
        request.data['authors'] = group.authors.all()
        
        if(Agroup.objects.filter(user=request.user, name=request.data['name'], ).exclude(id=groupId).exists()): # Elemento con uguali campi user e name già presente (con id diverso)
            return myError("E' già presente un gruppo associato al tuo utente con lo stesso nome") # Errore
        
        serializers = AgroupSerializer(instance=group, data=request.data) # Apporto all'istanza dell'oggetto Agroup le modifiche specificate
        if(serializers.is_valid()): # Formato corretto
            serializers.save(); # Salvo le modifiche all'oggetto nel DB
            
            return Response(serializers.data, status=200) # Successo
        else:
           return myError(serializers.errors) # Errore
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['DELETE']) # Accetta solo metodo DELETE
def groupDelete(request, groupId):
    '''
        API che elimina un gruppo associato all'utente.
        Se l'utente non è loggato lancio un errore.
        Se il gruppo specificato non è di proprietà dell'utente o non esiste lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato 
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo da eliminare
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad eliminare un gruppo inesistente o non di tua proprieta'") # Errore
        
        group.delete(); # Eliminazione del campo nel DB (non necessita conferma con .save())
        
        return Response({'message':"Gruppo eliminato con successo"}, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['POST']) # Accetta solo metodo POST
def groupAddAuthor(request, groupId, authorScopusId):
    '''
        API che aggiunge ad un gruppo un autore.
        Se l'utente non è loggato lancio un errore.
        Se il gruppo non esiste o non è di tua proprietà lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad aggiungere un autore ad un gruppo inesistente o non di tua proprieta'") # Errore
        
        risposta = authorUpdate_Create(authorScopusId) # Creo o aggiorno i dati dell'autore
        if(risposta.status_code==500): # Errore nel processo di creazione / aggiornamento
            return risposta # Errore
        
        author = Author.objects.get(scopusId=authorScopusId) # Autore da aggiungere
        group.authors.add(author) # Aggiungo l'autore al gruppo

        serializer = AgroupSerializer(group, many=False) # Conversione Agroup->Dizionario
        
        return Response(serializer.data, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['POST']) # Accetta solo metodo POST
def groupRemoveAuthor(request, groupId, authorId):
    '''
        API che rimuove un autore da un gruppo.
        Se il gruppo non esiste o non è di tua proprietà lancio un errore.
        Se l'autore non è presente lancio un errore.
    '''
   
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad aggiungere un utente ad un gruppo inesistente o non di tua proprieta'") # Errore
        
        
        if(group.authors.filter(id=authorId).exists()): # L'autore esiste
            author = Author.objects.get(id=authorId) # Autore da eliminare
            group.authors.remove(author) # Rimuovo l'autore dal gruppo
            serializer = AgroupSerializer(group, many=False) # Conversione Agroup->Dizionario
            
            return Response(serializer.data, status=200) # Successo
        else:
            return myError("L'utente che stai cercando di rimuovere non è presente nel gruppo") # Errore        
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore 
    

####################################################################################
################################# API AFFILIAZIONI #################################
####################################################################################

def affiliationCreate(dizionario):
    '''
        Funzione che dato un dizionario crea un oggetto Affiliazione
        - Se la creazione va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    serializers = AffiliationSerializer(data=dizionario) # Conversione JSON->Affiliation
    
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        return Response(serializers.data, status=200) # Successo
    else:
        return myError(serializers.error_messages) # Errore 
    
def affiliationUpdate(dizionario, affiliationId):
    '''
        Funzione che dato un dizionario modifica un oggetto Affiliazione
        - Se la modifica va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    affiliation =  Affiliation.objects.get(scopusId=affiliationId) # Affiliazione su cui effettuare le modifiche
    serializers = AffiliationSerializer(instance=affiliation, data=dizionario) # Apporto all'istanza dell'oggetto Affiliation le modifiche specificate
        
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200) # Successo
    else:    
        return myError(serializers.error_messages) # Errore
    
def affiliationUpdate_Create(id):
    '''
        Funzione che controlla la presenza nel DB della affiliazione con scopusId=id:
        - Se non è presente la aggiunge al DB.
        - Se è presente aggiorna il record.
        Se non esiste l'affiliazione lancio un errore.
    '''
    
    esiste = Affiliation.objects.filter(scopusId=id).exists() # Presenza nel DB dell'affiliazione
    
    try:
        ar=AffiliationRetrieval(aff_id=id, refresh=True, view="STANDARD") # API di Elsevier-Scopus per ricevere informazioni sull'affiliazione
    except:
        return myError("Non esiste un Affiliazione con id = "+str(id)) # Errore
    
    af={ # Dizionario contenete i dati per creare / modificare l'oggetto Affiliation
                'scopusId': ar.eid.split('-')[2],
                'name': ar.affiliation_name,
                'address': ar.address,
                'city': ar.city,
                'state': ar.state,
                'postal_code': ar.postal_code,
                'country': ar.country,
                'url': ar.org_URL,
                'document_count': ar.document_count,
                'author_count': ar.author_count,
                'last_update': datetime.now(),
            }
    
    if(not esiste): # Se non esiste, creo l'oggetto Affiliazione nel DB        
        af['creation'] = datetime.now()
        risposta = affiliationCreate(af) # Creo l'affiliazione
        
    else: # Se esiste Aggiorno
        affiliation = Affiliation.objects.get(scopusId=id)
        af['creation'] = affiliation.creation
        risposta = affiliationUpdate(af, id) # Aggiorno i dati dell'affiliazione
        
    return risposta # Errore o Successo
    
@api_view(['GET']) # Accetta solo metodo GET
def affiliationApiOverview(request):
    '''
        API che ritorna la lista di API delle Affiliazioni che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Dettagli affiliazione (da DB se possibile)': '/affiliation-detail/<str:affiliationScopusId>/',
        'Dettagli affiliazione (da Scopus con conseguente aggiornamento del DB)': '/affiliation-detail/<str:affiliationScopusId>/refresh/'
    }
     
    return Response(api_urls, status=200) # Successo

@api_view(['GET']) # Accetta solo metodo GET
def affiliationDetail(request, affiliationScopusId, refresh):
    '''
        API che ritorna i dettagli di una affiliazione.
        Se refresh = False cerco di restituire i dati presenti nel DB
            - Se l'oggetto non è presente interrogo le API di Elsevier
                - Creo l'oggetto con le informazioni ricevute
        Se refresh = True prendo i dati aggiornati da Elsevier
            - Se l'oggetto non è presente nel DB lo creo
            - Se l'oggetto è presente lo aggiorno
        Ritorno i dettagli in formato JSON
        N.B. PER IL MOMENTO QUESTA CHIAMATA E' DISPONIBILE ANCHE SE NON LOGGATI (IN FUTURO CHISSA')
    '''
    
    esiste = Affiliation.objects.filter(scopusId=affiliationScopusId).exists() # Se uso .get() anzichè .filter() errore
    
    if(not(refresh) and esiste): # Ho i dati e non devo aggiornare: Prendo i dati dal DB
        affiliation = Affiliation.objects.get(scopusId=affiliationScopusId) # Affiliazione di cui ci interessano le informazioni
        serializer = AffiliationSerializer(affiliation, many=False) # Conversione Affiliation->Dizionario
        
        return Response(serializer.data, status=200) # Successo
    else: # Non ho i dati oppure li devo aggiornare
        response = affiliationUpdate_Create(affiliationScopusId) # Creo o aggiorno il record dell'affiliazione
        return response # Errore o Successo
    
####################################################################################
#################################### API AUTORI ####################################
####################################################################################

def authorCreate(dizionario):
    '''
        Funzione che dato un dizionario crea un oggetto Autore
        - Se la creazione va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    risposta = affiliationUpdate_Create(id=dizionario['affiliation_scopusId']) # Creo o aggiorno l'associazione a cui appartiene l'autore
    if(risposta.status_code==500): # Errore nel processo di creazione / aggiornamento
        return risposta # Errore
    
    dizionario['affiliation'] = risposta.data["id"] # Aggiorno la chiave esterna che collega un autore all'associazione di appartenenza
    
    serializers = AuthorSerializer(data=dizionario) # Conversione JSON->Author
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200) # Successo
    else:
        return myError(serializers.error_messages) # Errore
    
def authorUpdate(dizionario, auhtorId):
    '''
        API che dato un dizionario modifica un oggetto Autore
        - Se la modifica va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    risposta = affiliationUpdate_Create(id=dizionario['affiliation_scopusId']) # Creo o aggiorno l'associazione a cui appartiene l'autore
    if(risposta.status_code==500): # Errore nel processo di creazione / aggiornamento
        return risposta # Errore
    
    dizionario['affiliation'] = risposta.data["id"] # Aggiorno la chiave esterna che collega un autore all'associazione di appartenenza
    
    author =  Author.objects.get(scopusId=auhtorId) # Autore da modificare (Che esiste)
    serializers = AuthorSerializer(instance=author, data=dizionario) # Apporto all'istanza dell'oggetto Author le modifiche specificate
        
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200) # Successo
    else:    
        return myError(serializers.error_messages) # Errore
    
def authorUpdate_Create(id):
    '''
        Funzione che controlla la presenza nel DB dell'autore con scopusId=id
        - Se non è presente la aggiunge al DB
        - Se è presente aggiorna il record
        Se tutto va a buon fine restituisco anche informazioni extra non presenti nel DB.
    '''
    
    esiste = Author.objects.filter(scopusId=id).exists() # Esistenza nel DB dell'autore
    ar=AuthorRetrieval(author_id=id, refresh=True, view="ENHANCED") # API di Elsevier-Scopus per ricevere informazioni sull'autore
    au={ # Dizionario contenente i dati per creare / aggiornare l'autore
            'scopusId': ar.identifier,
            'name': ar.given_name,
            'surname': ar.surname,
            'full_name': ar.indexed_name,
            'affiliation_scopusId': ar.affiliation_current[0][0], # id Scopus dell'affiliazione (mi serve per linkare un autore all'affiliazione di appartenenza)
            'last_update': datetime.now()
        }
    
    if(esiste): # Devo aggiornare l'oggetto
        author = Author.objects.get(scopusId=id) # Autore da modificare
        au['creation'] = author.creation
        risposta = authorUpdate(au, id) # Modifica dell'autore
    else: # Devo creare l'oggetto
        au['creation'] = datetime.now()
        risposta = authorCreate(au) # Creazione dell'autore
    
    if(risposta.status_code==500): # Errori nel processo di creazione / aggiornamento dell'autore
        return risposta # Errore
    else:
        # Setto i campi extra della risposta che non ho utilizzato per creare il DB
        risposta.data["affiliation_name"] = ar.affiliation_current[0][5] # nome dell'affiliazione
        risposta.data["affiliation_scopusId"] = ar.affiliation_current[0][0]
        risposta.data["document_count"] = ar.document_count
        risposta.data["cited_by_count"] = ar.cited_by_count # Citazioni ad Autori
        risposta.data["citation_count"] = ar.citation_count # Citazioni a Documenti
        risposta.data["h_index"] = ar.h_index
        risposta.data["publication_range"] = ar.publication_range
        risposta.data["subjects"] = ar.subject_areas
        risposta.data["classification"] = ar.classificationgroup
        
        #return Response(ar._json) Ritorna troppi campi che non mi servono
    
        return risposta # Successo   

@api_view(['GET']) # Accetta solo metodo GET
def authorApiOverview(request):
    '''
        API che ritorna la lista di API degli autori che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Dettagli autore (da Scopus) dato scopusId': '/author-detail/<str:auhtorScopusId>/',
        'Dettagli autore (da DB) dato authorId': '/authors/author-detail-DB/<str:authorId>/'
    }
     
    return Response(api_urls, status=200) # Successo

@api_view(['GET']) # Accetta solo metodo GET
def authorDetail(request, auhtorScopusId):
    '''
        API che ritorna i dettagli di un autore.
        Se l'oggetto non è presente nel DB lo aggiungo.
        Se l'oggetto è presente nel DB aggiorno i dati
        In ogni caso ritornerò i dati di Scopus (di cui i campi del DB sono un sottoinsieme)
        N.B. PER IL MOMENTO QUESTA CHIAMATA E' DISPONIBILE ANCHE SE NON LOGGATI (IN FUTURO CHISSA')
    '''
    
    risposta = authorUpdate_Create(auhtorScopusId) # Creo / Aggiorno un autore
    return risposta # Errore o Successo

@api_view(['GET']) # Accetta solo metodo GET
def authorDetailDB(request, authorId):
    '''
        API che ritorna i dettagli presi dal DB di un autore.
        Se l'oggetto non è presente nel DB lancio un errore.
        N.B. PER IL MOMENTO QUESTA CHIAMATA E' DISPONIBILE ANCHE SE NON LOGGATI (IN FUTURO CHISSA')
    '''

    try:
        author = Author.objects.get(id=authorId) # Autore di cui ci interessano i dettagli
    except Author.DoesNotExist:
        return myError("Non esiste un autore con id = "+authorId) # Errore
    
    serializer = AuthorSerializer(author, many=False) # Conversione Snapshot->Dizionario
        
    return Response(serializer.data, status=200) # Successo

####################################################################################
################################### API SNAPSHOT ###################################
####################################################################################

@api_view(['GET']) # Accetta solo metodo GET
def snapshotApiOverview(request):
    '''
        API che ritorna la lista di API degli snapshots che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Lista degli snapshot dell\'utente': '/snapshot-list/',
        'Lettura di uno snapshot salvato': '/snapshot-get/<str:snapshotId>/',
        'Creazione dello snapshot del gruppo': '/snapshot-get/<str:groupId>/',
        'Salvataggio di uno snapshot': 'snapshot-save/<str:title>/',
        'Eliminazione di uno snapshot salvato': 'snapshot-delete/<str:snapshotId>/'
    }
     
    return Response(api_urls, status=200) # Successo

@api_view(['GET']) # Accetta solo metodo GET
def snapshotList(request):
    '''
        API che mostra gli snapshot dell'utente.
        Se l'utente non è loggato lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        snapshots = Snapshot.objects.filter(user=request.user) # Snapshots da mostrare
        serializer = SnapshotSerializer(snapshots, many=True) # Conversione Snapshot->Dizionario
        
        return Response(serializer.data, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['GET']) # Accetta solo metodo GET
def snapshotGet(request, snapshotId):
    if(request.user.is_authenticated): # Utente loggato
        try:
            snapshot = Snapshot.objects.get(id=snapshotId, user=request.user) # Snapshot di cui effettuare la lettura
        except Snapshot.DoesNotExist: # Snapshot inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su uno snapshot inesistente o non di tua proprieta'") # Errore
        
        file = json.load(snapshot.informations) # Lettura del file JSON
        return Response(file, status=200)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
 
@api_view(['GET']) # Accetta solo metodo GET
def snapshotCompute(request, groupId):
    '''
        API che crea e restituisce il dizionario contenente lo snapshot di un gruppo specificato dall'utente.
        Se l'utente non è loggato lancio un errore.
        Se il gruppo specificato non è di proprietà dell'utente o non esiste lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo di cui mi interessano i dettagli
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'") # Errore

        # Contatori globali
        tot_document_count = 0 # Numero di documenti prodotti dagli autori del gruppo
        tot_cited_by_count = 0 # Numero di citazioni agli autori del gruppo
        tot_citation_count = 0 # Numero di citazioni a documenti prodotti dagli autori del gruppo
        tot_h_index = 0 # Indice di produttività degli autori del gruppo
        # dati_singoli=[]
        
        for author in group.authors.all(): # Ciclo fra gli autori del gruppo
            risposta = authorUpdate_Create(author.scopusId) # Aggiorno i dati di un autore
            tot_document_count += risposta.data["document_count"] 
            tot_cited_by_count += risposta.data["cited_by_count"]
            tot_citation_count += risposta.data["citation_count"] 
            tot_h_index += risposta.data["h_index"]
            # dati_singoli.append(risposta.data)
       
        contenuto = { # Dizionario che diventerà il contenuto del file .json
                        "groupId": group.id,
                        "groupName": group.name,
                        "groupAuthors": AuthorSerializer(group.authors.all(), many=True).data,
                        "tot_document_count": tot_document_count,
                        "tot_cited_by_count": tot_cited_by_count,
                        "tot_citation_count": tot_citation_count,
                        "tot_h_index": tot_h_index,
                        "timestamp": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        # "singoli": dati_singoli
                    }
        return Response(contenuto, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST 
def snapshotSave(request, title):
    '''
        API che salva su file uno snapshot per operazioni di confronto future.
        Se l'utente non è loggato lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        contenuto_byte = json.dumps(request.data, indent=2).encode('utf-8') # Conversione Dizionario->Binario
        file = ContentFile(contenuto_byte) # Creazione del file
        file.name = title # Titolo del file
        snapshot = Snapshot(user=request.user, title=title, creation=datetime.now()) # Creazione dello snapshot
        snapshot.save() # Salvataggio dello snapshot
        snapshot.informations.save(title, file) # Aggiunta del file .json allo snapshot
        return Response({'message':"Snapshot salvato con successo", 'id': snapshot.id}, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['DELETE']) # Accetta solo metodo DELETE 
def snapshotDelete(request, snapshotId):
    '''
        API che elimina lo snapshot specificato dall'utente.
        Se l'utente non è loggato lancio un errore.
        Se lo snapshot specificato non è di proprietà dell'utente o non esiste lancio un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato 
        try:
            snapshot = Snapshot.objects.get(user=request.user, id=snapshotId) # Gruppo da eliminare
        except Snapshot.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad eliminare uno snapshot inesistente o non di tua proprieta'") # Errore
        
        snapshot.delete(); # Eliminazione del campo nel DB (non necessita conferma con .save())
        
        return Response({'message':"Snapshot eliminato con successo"}, status=200) # Successo
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore