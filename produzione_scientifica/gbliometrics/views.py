# Import Librerie Esterne all'app
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

# Import Librerie Interne all'app
from .forms import CustomUserCreationForm # Form di creazione utente personalizzata

class SignUpView(generic.CreateView):
    '''
        Form di Registrazione all'applicazione
    '''
    form_class = CustomUserCreationForm # Tipo di form
    success_url = reverse_lazy('gbliometrics:login') # Url di redirezione in caso di successo ; reverse_lazy obbligatorio nelle viste generiche. 
    template_name = 'registration/signup.html' # Nome del template specifico che sovrascrive quello di default