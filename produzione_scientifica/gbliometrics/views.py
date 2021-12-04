'''
# Import Librerie Esterne all'app
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

# Import Librerie Interne all'app
from .forms import CustomUserCreationForm # Form di creazione utente personalizzata

class SignUpView(generic.CreateView):
    
    #    Form di Registrazione all'applicazione
    
    form_class = CustomUserCreationForm # Tipo di form
    success_url = reverse_lazy('gbliometrics:login') # Url di redirezione in caso di successo ; reverse_lazy obbligatorio nelle viste generiche. 
    template_name = 'registration/signup.html' # Nome del template specifico che sovrascrive quello di default
'''

from django.http.response import JsonResponse
import pandas as pd
from datetime import datetime
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus.utils import config

def api(request):
    ar=AuthorRetrieval(author_id="6603694127", refresh=False, view="ENHANCED");
    return JsonResponse(ar._json);