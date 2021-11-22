'''
File contenente le viste dell'app gbliometry
'''
from django.shortcuts import HttpResponse

def index(request):
    '''
    Pagina principale
    '''
    
    return HttpResponse("Benvenuto/a nella pagina iniziale")