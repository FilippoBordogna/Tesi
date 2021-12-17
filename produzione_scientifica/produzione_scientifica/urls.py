# Import Librerie Esterne all'app
from django.contrib import admin
from django.urls import path, include

# Import Librerie Interne all'app
from django_registration.backends.activation.views import RegistrationView
from gbliometrics.forms import CustomRegistrationForm

urlpatterns = [
    path('', include('frontend.urls')), # Inclusione delle url presenti nel file frontend/urls.py (frontend)
    path('admin/', admin.site.urls, name="admin"), # Pagina di amministrazione
    path('api/', include('gbliometrics.urls')), # Inclusione delle url presenti nel file gbliometrics/urls.py (backend: API)
    path('accounts/',  include('django.contrib.auth.urls')), # Autenticazione utente: riferimento alla libreria auth
    path('accounts/register/', RegistrationView.as_view(form_class=CustomRegistrationForm), name='registration_register'), # Override della registrazione della libreria django_registration
    path('accounts/', include('django_registration.backends.activation.urls')), # Registrazione utente: riferimento alla libreria django_registration
]
