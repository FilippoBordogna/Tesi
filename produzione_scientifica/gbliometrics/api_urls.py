# Import Librerie Esterne all'app
from django.urls import path
from . import views
from rest_framework import routers

app_name = "api" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    path('',views.apiOverview, name='api-overview'), # Lista delle API disponibili
    path('groups-list/',views.groupList, name='group-list'), # Lista dei gruppi dell'utente
    path('group-detail/<str:pk>/',views.groupDetail, name='group-detail'), # Dettagli del gruppo dell'utente
    path('group-create/',views.groupCreate, name='group-create'), # Aggiunto di un gruppo a quelli dell'utente
    path('group-update/<str:pk>/',views.groupUpdate, name='group-update'), # Modifica del gruppo dell'utente
    path('group-delete/<str:pk>/',views.groupDelete, name='group-delete'), # Eliminazione del gruppo dell'utente
]