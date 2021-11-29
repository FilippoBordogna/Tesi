# Import Librerie Esterne all'app
from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic.base import TemplateView # Vista generica TemplateView

# Import Librerie Interne all'app
from gbliometrics.views import SignUpView # Vista generica SignUpView
from gbliometrics import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"), # Pagina di amministrazione
    path('gbliometrics/', include('gbliometrics.urls')), # Inclusione delle url nel file gbliometrics/urls.py
    path('accounts/',  include('django.contrib.auth.urls')), # Autenticazione utente: riferimento alla libreria auth
    path('accounts/signup/', SignUpView.as_view(), name='signup') # Registrazione utente: riferimento all view SignUpView (views.py)
]
