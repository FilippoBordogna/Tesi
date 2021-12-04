# Import Librerie Esterne all'app
from django.urls import path
from django.views.generic.base import TemplateView # Vista generica TemplateView
from . import views

app_name = "gbliometrics" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('', TemplateView.as_view(template_name='home.html'), name = 'home'), # Pagina principale
    path('api/', views.api, name='api')
]
