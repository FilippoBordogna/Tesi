# Import Librerie Esterne all'app
from django.urls import path, include
from . import views
from rest_framework import routers

app_name = "api" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('',views.apiOverview, name='api-overview'), # Lista delle API disponibili
    path('groups-list/',views.groupList, name='group-list') # Lista dei gruppi dell'utente
]