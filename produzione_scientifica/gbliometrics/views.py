from django.http.response import HttpResponseBadRequest, JsonResponse
from gbliometrics.models import Agroup
from django.shortcuts import render
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AgroupSerializer

@api_view(['GET']) # Accetta solo metodo GET
def apiOverview(request):
    '''
        API che ritorna la lista di API che si possono interrogare
    '''
    api_urls = {
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
    groups = Agroup.objects.filter(user=request.user)
    serializer = AgroupSerializer(groups, many=True)
    return Response(serializer.data);