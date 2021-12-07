from django_registration.forms import User
from gbliometrics.models import Agroup
from django.shortcuts import render
from django.core import serializers
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AgroupSerializer

@api_view(['GET']) # Accetta solo metodo GET
def apiOverview(request):
    '''
        API che ritorna la lista di API che si possono interrogare
    '''
    
    api_urls = { # Lista delle API disponibili
        'List': '/group-list/',
        'Detail view': '/group-detail/<str:pk>/',
        'Create': '/group-create/',
        'Update': '/group-update/<str:pk>/',
        'Delete': '/group-delete/<str:pk>/',
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
        request.data['user'] = request.user.id
        request.data['last_update'] = datetime.now()
        request.data['creation'] = group.creation
        
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