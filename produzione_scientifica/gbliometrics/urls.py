# Import Librerie Esterne all'app
from django.urls import path
from . import views

app_name = "api"

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    # API DEI GRUPPI (MIA APP)
    path('groups/', views.groupApiOverview, name='groups-api-overview'), # Lista delle API dei gruppi disponibili
    path('groups/groups-list/', views.groupsList, name='groups-list'), # Lista dei gruppi dell'utente
    path('groups/group-details/<str:groupId>/', views.groupDetails, name='group-details'), # Dettagli del gruppo dell'utente
    path('groups/group-create/', views.groupCreate, name='group-create'), # Aggiunto di un gruppo a quelli dell'utente
    path('groups/group-update/<str:groupId>/', views.groupUpdate, name='group-update'), # Modifica del gruppo dell'utente
    path('groups/group-delete/<str:groupId>/', views.groupDelete, name='group-delete'), # Eliminazione del gruppo dell'utente
    path('groups/group-add-author/<str:groupId>/<str:authorScopusId>/', views.groupAddAuthor, name="group-add-author"), # Aggiunta di un Autore al gruppo
    path('groups/group-add-multiple-authors/<str:groupId>/', views.groupAddMultipleAuthors ,name="group-add-multiple-authors"), # Aggiunta di PIU' (JSON) autori al gruppo
    path('groups/group-remove-author/<str:groupId>/<str:authorId>/', views.groupRemoveAuthor, name="group-remove-author"), # Rimozione di un Autore al gruppo
    
    # API DELLE AFFILIAZIONI (ELSEVIER + MIA APP)
    path('affiliations/', views.affiliationApiOverview, name='affiliations-api-overview'), # Lista delle API dei gruppi disponibili
    path('affiliations/affiliation-details/<str:affiliationScopusId>/', views.affiliationDetails, {'refresh': False}, name='affiliation-details'), # Dettagli dell'associazione (Se possibile da DB)
    path('affiliations/affiliation-details/<str:affiliationScopusId>/refresh/', views.affiliationDetails, {'refresh': True}, name='affiliation-details-refresh'), # Dettagli dell'associazione (API Scopus)
    
    # API DEGLI AUTORI (ELSEVIER + MIA APP)
    path('authors/', views.authorApiOverview, name='authors-api-overview'), # Lista delle API dei gruppi disponibili
    path('authors/author-details/<str:authorScopusId>/', views.authorDetails, name='author-details'), # Dettagli dell'associazione (API Scopus)
    path('authors/author-details-DB/<str:authorId>/', views.authorDetailsDB, name='author-details-db'), # Dettagli dell'associazione (DB) 
    
    # API DEGLI SNAPSHOT (ELSEVIER + MIA APP)
    path('snapshots/', views.snapshotApiOverview, name='snapshots-api-overview'), # Lista delle API degli snapshot
    path('snapshots/snapshots-list/', views.snapshotsList, name='snapshots-list'), # Lista degli snapshot dell'utente
    path('snapshots/snapshot-get/<str:snapshotId>/', views.snapshotGet, name='snapshot-get'), # Lettura di uno snapshot salvato (file)
    path('snapshots/snapshot-compute/<str:groupId>/', views.snapshotCompute, name='snapshot-compute'), # Creazione del dizionario dello Snapshot del gruppo specificato dall'utente
    path('snapshots/snapshot-save/<str:title>/', views.snapshotSave, name='snapshot-save'), # Salvataggio di uno snapshot dato come contenuto della POST
    path('snapshots/snapshot-delete/<str:snapshotId>/', views.snapshotDelete, name='snapshot-delete'), # Eliminazione dello snapshot specificato dall'utente
]