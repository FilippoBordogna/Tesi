from django.http import HttpResponse

def index(request):
    '''
        Pagina Principale
    '''
    return HttpResponse("Benvenuto/a nella pagina Iniziale della Applicazione Gbliometrics")