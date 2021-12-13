from django.http.response import HttpResponse
from django_registration.forms import User
from pybliometrics.scopus.utils.create_config import create_config
from rest_framework.fields import JSONField # Modello User Django
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
        API che ritorna la lista di API dei gruppi che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Lista dei gruppi dell\'utente': '/group-list/',
        'Dettagli di un gruppo': '/group-detail/<str:pk>/',
        'Creazione di un gruppo': '/group-create/',
        'Modifica di un gruppo': '/group-update/<str:pk>/',
        'Eliminazione di un gruppo': '/group-delete/<str:pk>/',
        'Aggiunta di un autore': '/group-add-author/<str:groupId>/<str:authorScopusId>/',
        'Rimozione di un autore': '/group-remove-author/<str:groupId>/<str:authorId>/'
    }
     
    return Response(api_urls, status=200)

@api_view(['GET']) # Accetta solo metodo GET
def groupList(request):
    '''
        API che mostra i gruppi creati dall'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        groups = Agroup.objects.filter(user=request.user) # Gruppi appartenenti all'utente
        serializer = AgroupSerializer(groups, many=True)
        
        return Response(serializer.data, status=200) # Ritorno i dati di interesse trasformati in JSON
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['GET']) # Accetta solo metodo GET
def groupDetail(request, pk): # Necessita del parametro pk
    '''
        API che mostra i dettagli di un gruppo
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo di cui mi interessano i dettagli
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'") # Errore
        
        serializer = AgroupSerializer(group, many=False)
        
        return Response(serializer.data, status=200)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def groupCreate(request):
    '''
        API che crea un gruppo associato all'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        # I campi user, data di creazione e data di ultima modifica settati per evitare modifiche che favoriscono inconsistenza
        request.data['user'] = request.user.id
        request.data['creation'] = datetime.now()
        request.data['last_update'] = datetime.now()
        
        if(Agroup.objects.filter(user=request.user, name=request.data['name']).exists()): # Elemento con uguali campi user e name già presente
            return myError("Il gruppo che stai inserendo esiste già") # Errore

        else: # Non esiste un elemento con uguali campi user e name
            serializers = AgroupSerializer(data=request.data) # Trasformo il JSON passatomi in oggetto Agroup
            if(serializers.is_valid()): # Oggetto creato correttamente
                serializers.save(); # Salvo l'oggetto nel DB
            
            return Response(serializers.data, status=200) # Ritorno il JSON con le opportune modifiche (vedi request.data poco sopra)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def groupUpdate(request, pk):
    '''
        API che modifica un gruppo associato all'utente (Non ottimale per modifiche sugli autori appartenenti al gruppo)
    '''
    
    if(request.user.is_authenticated): # Utente loggato     
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'") # Errore
        
        # I campi user, data di creazione e data di ultima modifica settati per evitare modifiche che favoriscono inconsistenza
        request.data['id'] = group.id
        request.data['user'] = request.user.id
        request.data['last_update'] = datetime.now()
        request.data['creation'] = group.creation
        
        if(Agroup.objects.filter(user=request.user, name=request.data['name'], ).exclude(id=pk).exists()): # Elemento con uguali campi user e name già presente (con id diverso)
            return myError("E' già presente un gruppo con lo stesso nome associato al tuo utente") # Errore
        
        serializers = AgroupSerializer(instance=group, data=request.data) # Creo un istanza dell'oggetto con i campi modificati
        if(serializers.is_valid()): # Formato corretto
            serializers.save(); # Salvo le modifiche all'oggetto nel DB 
        
        return Response(serializers.data, status=200) 
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['DELETE']) # Accetta solo metodo DELETE
def groupDelete(request, pk):
    '''
        API che elimina un gruppo associato all'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato 
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo da eliminare
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'") # Errore
        
        group.delete(); # Eliminazione del campo nel DB (non necessita conferma con .save())
        
        return Response({'message':"Gruppo eliminato con successo"}, status=200)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['POST']) # Accetta solo metodo POST
def groupAddAuthor(request, groupId, authorScopusId):
    '''
        API che aggiunge ad un gruppo un autore.
        Se il gruppo non esiste o non è di tua proprietà genera un errore.
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad aggiungere un utente ad un gruppo inesistente o non di tua proprieta'") # Errore
        
        risposta = authorUpdate_Create(authorScopusId) # Creo o aggiorno i dati dell'autore
        if(risposta.status_code==500):
            return risposta
        
        author = Author.objects.get(scopusId=authorScopusId) # Autore da aggiungere
        group.authors.add(author) # Aggiungo l'autore al gruppo

        serializer = AgroupSerializer(group, many=False)
        
        return Response(serializer.data, status=200)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore

@api_view(['POST']) # Accetta solo metodo POST
def groupRemoveAuthor(request, groupId, authorId):
    '''
        API che rimuove un autore da un gruppo.
        Se il gruppo non esiste o non è di tua proprietà genera un errore.
    '''
   
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=groupId) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad aggiungere un utente ad un gruppo inesistente o non di tua proprieta'") # Errore
        
        author = Author.objects.get(id=authorId) # Autore da aggiungere
        if(group.authors.filter(id=author.id).exists()):
            group.authors.remove(author) # Aggiungo l'autore al gruppo
            serializer = AgroupSerializer(group, many=False)
            
            return Response(serializer.data, status=200)
        else:
            return myError("L'utente che stai cercando di rimuovere non è presente nel gruppo")

        
        
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
    
    # Il controllo sull'eventuale esistenza (prima della chiamata) nel DB del record da inserire lo lascio alla funzione chiamante
    serializers = AffiliationSerializer(data=dizionario) # Trasformo il JSON passatomi in oggetto Affiliation
    
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        return Response(serializers.data, status=200)
    else:
        return myError(serializers.error_messages) # Errore 
    
def affiliationUpdate(dizionario, pk):
    '''
        Funzione che dato un dizionario modifica un oggetto Affiliazione
        - Se la modifica va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    # Il controllo sull'eventuale esistenza nel DB di un record con gli stessi campi chiave la lascio alla funzione chiamante
    
    affiliation =  Affiliation.objects.get(scopusId=pk) # Affiliazione su cui effettuare le modifiche
    serializers = AffiliationSerializer(instance=affiliation, data=dizionario) # Creo un istanza dell'oggetto con i campi modificati
        
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200)
    else:    
        return myError(serializers.error_messages) # Errore
    
def affiliationUpdate_Create(id):
    '''
        Funzione che controlla la presenza nel DB della affiliazione con scopusId=id
        Se non è presente la aggiunge al DB
        Se è presente aggiorna il record
    '''
    
    esiste = Affiliation.objects.filter(scopusId=id).exists() # Presenza nel DB dell'affiliazione
    
    try:
        ar=AffiliationRetrieval(aff_id=id, refresh=True, view="STANDARD");
    except:
        return myError("Non esiste un Affiliazione con id = "+str(id))
    
    af={
                'scopusId': ar.eid.split('-')[2],
                # 'ScopusId': pk # Preferisco prenderlo da Scopus (perchè potrebbe essere cambiato per qualche motivo)
                'name': ar.affiliation_name,
                'address': ar.address,
                'city': ar.city,
                'state': ar.state,
                'postal_code': ar.postal_code,
                'country': ar.country,
                'url': ar.org_URL,
                'last_update': datetime.now(),
            }
    
    if(not esiste): # Se non esiste, creo l'oggetto Affiliazione nel DB        
        af['creation'] = datetime.now()
        risposta = affiliationCreate(af)
        
    else: # Se esiste Aggiorno
        affiliation = Affiliation.objects.get(scopusId=id)
        af['creation'] = affiliation.creation
        risposta = affiliationUpdate(af, id)
        
    return risposta
    
@api_view(['GET']) # Accetta solo metodo GET
def affiliationApiOverview(request):
    '''
        API che ritorna la lista di API delle Affiliazioni che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Dettagli affiliazione (da DB se possibile)': '/affiliation-detail/<str:pk>/',
        'Dettagli affiliazione (da Scopus)': '/affiliation-detail/<str:pk>/refresh/'
    }
     
    return Response(api_urls, status=200)

@api_view(['GET']) # Accetta solo metodo GET
def affiliationDetail(request, pk, refresh):
    '''
        API che ritorna i dettagli di una affiliazione.
        Se refresh = False restituisco i dati dal DB
            - Se l'oggetto non è presente interrogo le API di Elsevier
                - Creo l'oggetto con le informazioni ricevute
            - Ritorno i dettagli in formato JSON
        Se refresh = True prendo i dati aggiornati da Elsevier
            - Se l'oggetto non è presente nel DB lo creo
            - Se l'oggetto è presente lo aggiorno
            - Ritorno i dettagli in formato JSON
        N.B. PER IL MOMENTO QUESTA CHIAMATA E' DISPONIBILE ANCHE SE NON LOGGATI (IN FUTURO CHISSA')
    '''
    
    esiste = Affiliation.objects.filter(scopusId=pk).exists() # Se uso .get() anzichè .filter() errore
    if(esiste):
        affiliation = Affiliation.objects.get(scopusId=pk) # Oggetto Affiliation di cui mi interessano i dettagli
    
    if(not(refresh) and esiste): # Ho i dati e non devo aggiornare: Prendo i dati dal DB
        serializer = AffiliationSerializer(affiliation, many=False)
        
        return Response(serializer.data, status=200)
    else:
        response = affiliationUpdate_Create(pk) # Creo o aggiorno il record dell'affiliazione
        return response
    
####################################################################################
#################################### API AUTORI ####################################
####################################################################################

def authorCreate(dizionario):
    '''
        Funzione che dato un dizionario crea un oggetto Autore
        - Se la creazione va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    # Il controllo sull'eventuale esistenza (prima della chiamata) nel DB del record da inserire lo lascio alla funzione chiamante
    risposta = affiliationUpdate_Create(id=dizionario['affiliation-scopusId'])
    if(risposta.status_code==500):
        return risposta
    
    dizionario['affiliation'] = risposta.data["id"] # La risposta mi dà (tra le altre cose) l'id della affiliazione appena creata/aggiornata che userò come chiave esterna
    
    serializers = AuthorSerializer(data=dizionario) # Trasformo il JSON passatomi in oggetto Author
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200)
    else:
        return myError(serializers.error_messages) # Errore
    
def authorUpdate(dizionario, pk):
    '''
        API che dato un dizionario modifica un oggetto Autore
        - Se la modifica va a buon fine Restituisco i dati inseriti nel DB
        - Altrimenti restituisco un errore
    '''
    
    # Il controllo sull'eventuale esistenza nel DB di un record con gli stessi campi chiave la lascio alla funzione chiamante
    
    affiliation = Affiliation.objects.get(scopusId=dizionario['affiliation-scopusId']) 
    dizionario['affiliation'] = affiliation.id
      
    author =  Author.objects.get(scopusId=pk)
    serializers = AuthorSerializer(instance=author, data=dizionario) # Creo un istanza dell'oggetto con i campi modificati
        
    if(serializers.is_valid()): # Formato corretto
        serializers.save(); # Salvo l'oggetto nel DB
        
        return Response(serializers.data, status=200)
    else:    
        return myError(serializers.error_messages) # Errore
    
def authorUpdate_Create(id):
    '''
        Funzione che controlla la presenza nel DB dell'autore con scopusId=id
        Se non è presente la aggiunge al DB
        Se è presente aggiorna il record
        Se tutto va a buon fine restituisco anche informazioni extra non presenti nel DB
    '''
    
    esiste = Author.objects.filter(scopusId=id).exists() # Esistenza nel DB dell'autore
    ar=AuthorRetrieval(author_id=id, refresh=True, view="ENHANCED");
    au={
            'scopusId': ar.identifier,
            'name': ar.given_name,
            'surname': ar.surname,
            'full_name': ar.indexed_name,
            'affiliation-scopusId': ar.affiliation_current[0][0],
            'last_update': datetime.now()
        } # Dizionario che passerò alla funzione che crea/aggiorna l'autore
    
    if(esiste): # Devo aggiornare l'oggetto
        author = Author.objects.get(scopusId=id)  
        au['creation'] = author.creation
        risposta = authorUpdate(au, id)
    else: # Devo creare l'oggetto
        au['creation'] = datetime.now()
        risposta = authorCreate(au)
    
    if(risposta.status_code==500):
        return risposta
    else:
        # Setto i campi extra della risposta che non ho utilizzato per creare il DB
        risposta.data["document-count"] = ar.document_count
        risposta.data["cited-by-count"] = ar.cited_by_count # Citazioni ad Autori
        risposta.data["citation-count"] = ar.citation_count # Citazioni a Documenti
        risposta.data["h-index"] = ar.h_index
        risposta.data["publication-range"] = ar.publication_range
        risposta.data["subjects"] = ar.subject_areas
        risposta.data["classification"] = ar.classificationgroup
        
        #return Response(ar._json) Ritorna troppi campi che non mi servono
    
        return risposta        

@api_view(['GET']) # Accetta solo metodo GET
def authorApiOverview(request):
    '''
        API che ritorna la lista di API degli autori che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Dettagli autore (da Scopus) dato scopusId': '/author-detail/<str:pk>/'
    }
     
    return Response(api_urls, status=200)

@api_view(['GET']) # Accetta solo metodo GET
def authorDetail(request, pk):
    '''
        API che ritorna i dettagli di un autore.
        Se l'oggetto non è presente nel DB lo aggiungo.
        Se l'oggetto è presente nel DB
            - Se i dati differiscono da quelli nel DB aggiorno
            - Se i dati sono uguali non aggiorno
        In ogni caso ritornerò i dati di Scopus (+ campi del DB)
        N.B. PER IL MOMENTO QUESTA CHIAMATA E' DISPONIBILE ANCHE SE NON LOGGATI (IN FUTURO CHISSA')
    '''
    
    risposta = authorUpdate_Create(pk)   
    return risposta

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
        'Creazione dello snapshot del gruppo': '/snapshot-create/<str:groupId>/<str:title>/'
    }
     
    return Response(api_urls, status=200)

@api_view(['GET']) # Accetta solo metodo GET
def snapshotList(request):
    '''
        API che mostra gli snapshot dell'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        snapshots = Snapshot.objects.filter(user=request.user)
        serializer = SnapshotSerializer(snapshots, many=True)
        
        return Response(serializer.data, status=200) # Ritorno i dati di interesse trasformati in JSON
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def snapshotCreate(request, groupId, title):
    '''
        API che crea lo snapshot di un gruppo specificato dall'utente
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
        dati_singoli=[]
        
        for author in group.authors.all(): # Ciclo fra gli autori del gruppo
            risposta = authorUpdate_Create(author.scopusId) # Aggiorno i dati di un autore
            tot_document_count += risposta.data["document-count"] 
            tot_cited_by_count += risposta.data["cited-by-count"]
            tot_citation_count += risposta.data["citation-count"] 
            tot_h_index += risposta.data["h-index"]
            #dati_singoli.append(risposta.data)
       
        contenuto = {
                        "groupAuthors": AuthorSerializer(group.authors.all(), many=True).data,
                        "tot_document_count": tot_document_count,
                        "tot_cited_by_count": tot_cited_by_count,
                        "tot_citation_count": tot_citation_count,
                        "tot_h_index": tot_h_index,
                        "timestamp": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        #"singoli": dati_singoli
                    }
        
        
        contenuto_byte = json.dumps(contenuto, indent=2).encode('utf-8')
        file = ContentFile(contenuto_byte)
        file.name = title
        snapshot = Snapshot(user=request.user, title=title, creation=datetime.now()) # Creazione dello snapshot
        snapshot.save() # Salvataggio dello snapshot
        snapshot.informations.save(title, file) # Aggiunta allo snapshot del file
               
        return Response(contenuto, status=200)
        
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore
    
@api_view(['DELETE']) # Accetta solo metodo GET 
def snapshotDelete(request, snapshotId):
    '''
        API che elimina uno snapshot specificato dall'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato 
        try:
            snapshot = Snapshot.objects.get(user=request.user, id=snapshotId) # Gruppo da eliminare
        except Snapshot.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            return myError("Stai provando ad eliminare uno snapshot inesistente o non di tua proprieta'") # Errore
        
        snapshot.delete(); # Eliminazione del campo nel DB (non necessita conferma con .save())
        
        return Response({'message':"Snapshot eliminato con successo"}, status=200)
    else: # Utente NON loggato
        return myError("Non sei loggato") # Errore