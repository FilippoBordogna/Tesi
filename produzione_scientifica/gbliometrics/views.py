from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm # Creazione di form
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    '''
        Form di Registrazione all'applicazione
    '''
    form_class = UserCreationForm # Tipo di form
    success_url = reverse_lazy('gbliometrics:login') # Url di redirezione in caso di successo ; reverse_lazy obbligatorio nelle viste generiche. 
    template_name = 'registration/signup.html' # Nome del template specifico che sovrascrive quello di default