from django.http.response import JsonResponse
from django_registration.forms import User
from pybliometrics import scopus
from gbliometrics.models import Agroup, Affiliation
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AgroupSerializer, AffiliationSerializer

from pybliometrics.scopus import AffiliationRetrieval

@api_view(['GET']) # Accetta solo metodo GET
def groupApiOverview(request):
    '''
        API che ritorna la lista di API dei gruppi che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Lista': '/group-list/',
        'Dettagli': '/group-detail/<str:pk>/',
        'Creazione': '/group-create/',
        'Modifica': '/group-update/<str:pk>/',
        'Elimina': '/group-delete/<str:pk>/',
    }
     
    return Response(api_urls)

@api_view(['GET']) # Accetta solo metodo GET
def groupList(request):
    '''
        API che mostra i gruppi creati dall'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        groups = Agroup.objects.filter(user=request.user) # Gruppi appartenenti all'utente
        serializer = AgroupSerializer(groups, many=True)
        
        return Response(serializer.data) # Ritorno i dati di interesse trasformati in JSON
    
    else: # Utente NON loggato
        message = "Non sei loggato";
        
        return Response({'status':'false', 'message':message}, status=500) # Errore

@api_view(['GET']) # Accetta solo metodo GET
def groupDetail(request, pk): # Necessita del parametro pk
    '''
        API che mostra i dettagli di un gruppo
    '''
    
    if(request.user.is_authenticated): # Utente loggato
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo di cui mi interessano i dettagli
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            message = "Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'";
            
            return Response({'status':'false', 'message':message}, status=500) # Errore
        
        serializer = AgroupSerializer(group, many=False)
        
        return Response(serializer.data)
    
    else: # Utente NON loggato
        message = "Non sei loggato";

        return Response({'status':'false', 'message':message}, status=500) # Errore
    
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
            message = "Il gruppo che stai inserendo esiste già";
            
            return Response({'status':'false', 'message':message}, status=500) # Errore
        
        else: # Non esiste un elemento con uguali campi user e name
            serializers = AgroupSerializer(data=request.data) # Trasformo il JSON passatomi in oggetto Agroup
            if(serializers.is_valid()): # Oggetto creato correttamente
                serializers.save(); # Salvo l'oggetto nel DB
            
            return Response(serializers.data) # Ritorno il JSON con le opportune modifiche (vedi request.data poco sopra)
    
    else: # Utente NON loggato
        message = "Non sei loggato";
        
        return Response({'status':'false', 'message':message}, status=500) # Errore
    
@api_view(['POST']) # Accetta solo metodo POST
def groupUpdate(request, pk): # Necessita del parametro pk
    '''
        API che modifica un gruppo associato all'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato     
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo su cui effettuare le modifiche
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            message = "Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'";
            
            return Response({'status':'false', 'message':message}, status=500) # Errore
        
        # I campi user, data di creazione e data di ultima modifica settati per evitare modifiche che favoriscono inconsistenza
        request.data['id'] = group.id
        request.data['user'] = request.user.id
        request.data['last_update'] = datetime.now()
        request.data['creation'] = group.creation
        
        if(Agroup.objects.filter(user=request.user, name=request.data['name'], ).exclude(id=pk).exists()): # Elemento con uguali campi user e name già presente (con id diverso)
            message = "E' già presente un gruppo con lo stesso nome associato al tuo utente";
            
            return Response({'status':'false', 'message':message}, status=500) # Errore
        
        serializers = AgroupSerializer(instance=group, data=request.data) # Creo un istanza dell'oggetto con i campi modificati
        
        if(serializers.is_valid()): # Oggetto modificato correttamente
            serializers.save(); # Salvo le modifiche all'oggetto nel DB 
        
        return Response(serializers.data) 
    
    else: # Utente NON loggato
        message = "Non sei loggato";
        
        return Response({'status':'false', 'message':message}, status=500) # Errore
    
@api_view(['DELETE']) # Accetta solo metodo DELETE
def groupDelete(request, pk):
    '''
        API che elimina un gruppo associato all'utente
    '''
    
    if(request.user.is_authenticated): # Utente loggato 
        try:
            group = Agroup.objects.get(user=request.user, id=pk) # Gruppo da eliminare
        except Agroup.DoesNotExist: # Gruppo inesistente o non di proprietà dell'utente
            message = "Stai provando ad accedere ad informazioni su un gruppo inesistente o non di tua proprieta'";
            
            return Response({'status':'false', 'message':message}, status=500) # Errore
        
        group.delete(); # Eliminazione del campo nel DB (non necessita conferma con .save())
        
        return Response({'message':"Gruppo eliminato con successo"})
    
    else: # Utente NON loggato
        message = "Non sei loggato";
        
        return Response({'status':'false', 'message':message}, status=500) # Errore
    

## API AFFILIAZIONI ##
@api_view(['GET']) # Accetta solo metodo GET
def affiliationApiOverview(request):
    '''
        API che ritorna la lista di API delle Affiliazioni che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'Dettagli affiliazione (da DB se possibile)': '/affiliation-detail/<str:pk>/',
        'Dettagli affiliazione (da Elsevier)': '/affiliation-detail/<str:pk>/refresh/'
    }
     
    return Response(api_urls)

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
    
    affiliation = Affiliation.objects.get(scopusId=pk)
    esiste = Affiliation.objects.filter(scopusId=pk).exists() # Se uso .get() anzichè .filter() errore
    
    if(not(refresh) and esiste): # Ho i dati e non devo aggiornare: Prendo i dati dal DB
        serializer = AffiliationSerializer(affiliation, many=False) # many = True è incorretto siccome prendo 1 solo oggetto ma mi permette di usare il .filter() sopra
        
        return Response(serializer.data)
        #return Response("Prova")
    
    else: # Non ho i dati o li devo aggiornare: Prendo i dati da Elsevier
        ar=AffiliationRetrieval(aff_id=pk, refresh=True, view="STANDARD");
        
        af={
            'scopusId': ar.eid.split('-')[2],
            'name': ar.affiliation_name,
            'address': ar.address,
            'city': ar.city,
            'state': ar.state,
            'postal_code': ar.postal_code,
            'country': ar.country,
            'url': ar.org_URL,
        }
        
        af['last_update'] = datetime.now() # Aggiungo la data di modifica
        
        if(not esiste): # Devo creare l'oggetto
            af['creation'] = datetime.now() # Aggiungo la data di creazione 
            
            serializers = AffiliationSerializer(data=af) # Trasformo il JSON passatomi in oggetto Affiliation
            if(serializers.is_valid()): # Oggetto creato correttamente
                serializers.save(); # Salvo l'oggetto nel DB
       
        else: # Devo aggiornare l'oggetto
            af['creation'] = affiliation.creation # Mantengo la data di creazione: Per restituire il campo nella risposta (Per il DB operazione inutile)
            serializers = AffiliationSerializer(instance=affiliation, data=af) # Creo un istanza dell'oggetto con i campi modificati
        
        if(serializers.is_valid()): # Oggetto modificato correttamente
            serializers.save(); # Salvo le modifiche all'oggetto nel DB 
        
        return Response(serializers.data) # Ritorno il JSON con le opportune modifiche (vedi last_update e creation)
        