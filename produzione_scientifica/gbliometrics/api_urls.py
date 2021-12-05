# Import Librerie Esterne all'app
from django.urls import path, include
from . import views

app_name = "api" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('',views.prova, name='prova') # Prova API
]