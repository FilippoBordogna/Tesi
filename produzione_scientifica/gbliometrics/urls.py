# Import Librerie Esterne all'app
from django.urls import path
from . import views

app_name = "api"

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    # API DEI GRUPPI (MIA APP)
    path('groups/', views.groupApiOverview, name='group-api-overview'), # Lista delle API dei gruppi disponibili
    path('groups/group-list/', views.groupList, name='group-list'), # Lista dei gruppi dell'utente
    path('groups/group-detail/<str:groupId>/', views.groupDetail, name='group-detail'), # Dettagli del gruppo dell'utente
    path('groups/group-create/', views.groupCreate, name='group-create'), # Aggiunto di un gruppo a quelli dell'utente
    path('groups/group-update/<str:groupId>/', views.groupUpdate, name='group-update'), # Modifica del gruppo dell'utente
    path('groups/group-delete/<str:groupId>/', views.groupDelete, name='group-delete'), # Eliminazione del gruppo dell'utente
    path('groups/group-add-author/<str:groupId>/<str:authorScopusId>/', views.groupAddAuthor, name="group-add-author"), # Aggiunta di un Autore al gruppo
    path('groups/group-remove-author/<str:groupId>/<str:authorId>/', views.groupRemoveAuthor, name="group-remove-author"), # Rimozione di un Autore al gruppo
    
    # API DELLE AFFILIAZIONI (ELSEVIER + MIA APP)
    path('affiliations/', views.affiliationApiOverview, name='affiliationapi-overview'), # Lista delle API dei gruppi disponibili
    path('affiliations/affiliation-detail/<str:affiliationScopusId>/', views.affiliationDetail, {'refresh': False}, name='affiliation-detail'), # Dettagli dell'associazione (Se possibile da DB)
    path('affiliations/affiliation-detail/<str:affiliationScopusId>/refresh/', views.affiliationDetail, {'refresh': True}, name='affiliation-detail-refresh'), # Dettagli dell'associazione (API Scopus)
    
    # API DEGLI AUTORI (ELSEVIER + MIA APP)
    path('authors/', views.authorApiOverview, name='author-overview'), # Lista delle API dei gruppi disponibili
    path('authors/author-detail/<str:auhtorScopusId>/', views.authorDetail, name='author-detail'), # Dettagli dell'associazione (API Scopus)
    path('authors/author-detail-DB/<str:authorId>/', views.authorDetailDB, name='author-detail-db'), # Dettagli dell'associazione (DB) 
    
    # API DEGLI SNAPSHOT (ELSEVIER + MIA APP)
    path('snapshots/', views.snapshotApiOverview, name='snapshot-api-overview'), # Lista delle API degli snapshot
    path('snapshots/snapshot-list/', views.snapshotList, name='snapshot-list'), # Lista degli snapshot dell'utente
    path('snapshots/snapshot-compute/<str:groupId>/', views.snapshotCompute, name='snapshot-compute'), # Creazione del dizionario dello Snapshot del gruppo specificato dall'utente
    path('snapshots/snapshot-save/<str:title>/', views.snapshotSave, name='snapshot-save'), # Salvataggio di uno snapshot dato come contenuto della POST
    path('snapshots/snapshot-delete/<str:snapshotId>/', views.snapshotDelete, name='snapshot-delete'), # Eliminazione dello snapshot specificato dall'utente
]