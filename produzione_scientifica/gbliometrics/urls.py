"""produzione_scientifica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# IMPORT
from django.urls import path, include
from django.views.generic.base import TemplateView # Vista generica TemplateView

from . import views # Viste
from .views import SignUpView # Vista generica SignUpView

app_name = "gbliometrics" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('', TemplateView.as_view(template_name='home.html'), name = 'home'), # Pagina principale
    path('accounts/',  include('django.contrib.auth.urls')), # Autenticazione utente: riferimento alla libreria auth
    path('accounts/signup/', SignUpView.as_view(), name='signup') # Registrazione utente: riferimento all view SignUpView
]
