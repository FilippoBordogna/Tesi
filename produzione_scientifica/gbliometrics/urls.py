# Import Librerie Esterne all'app
from django.urls import path, include
from django.views.generic.base import TemplateView # Vista generica TemplateView

# Import Librerie Interne all'app
from . import views # Viste
from .views import SignUpView # Vista generica SignUpView

app_name = "gbliometrics" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('', TemplateView.as_view(template_name='home.html'), name = 'home'), # Pagina principale
    path('accounts/',  include('django.contrib.auth.urls')), # Autenticazione utente: riferimento alla libreria auth
    path('signup/', SignUpView.as_view(), name='signup') # Registrazione utente: riferimento all view SignUpView (views.py)
]
