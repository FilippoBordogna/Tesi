# Import Librerie Esterne all'app
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # Vista generica TemplateView

# Import Librerie Interne all'app
#from gbliometrics.views import SignUpView # Vista generica SignUpView
from gbliometrics import views
from django_registration.backends.activation.views import RegistrationView
from gbliometrics.forms import CustomRegistrationForm

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"), # Pagina di amministrazione
    path('gbliometrics/', include('gbliometrics.urls')), # Inclusione delle url nel file gbliometrics/urls.py
    path('accounts/',  include('django.contrib.auth.urls')), # Autenticazione utente: riferimento alla libreria auth
    path('accounts/register/', RegistrationView.as_view(form_class=CustomRegistrationForm), name='registration_register'), # Override della registrazione della libreria django_registration
    path('accounts/', include('django_registration.backends.activation.urls')), # Registrazione utente: riferimento alla libreria django_registration
]
