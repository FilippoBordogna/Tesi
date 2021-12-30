from django.urls import path
from django.views.generic.base import TemplateView # Vista generica TemplateView

app_name = "frontend" # Namespace per evitare futuri conflitti

urlpatterns = [
    # HOMEPAGE
    path('', TemplateView.as_view(template_name='home.html'), name="home"), # Pagina principale
    
    # GRUPPI
    path('groups/groups-list', TemplateView.as_view(template_name='groups-list.html'), name='groups-list'), # Pagina di gestione dei gruppi
    path('groups/authors-list/<str:groupId>/', TemplateView.as_view(template_name='authors-list.html'), name='authors-list'), # Pagina di gestione degli autori
    path('groups/group-authors-add/',TemplateView.as_view(template_name="group-authors-add.html"), name="group-authors-add"), # Pagina di aggiunta autori ad un gruppo
    
    # AUTORI
    path('authors/author-details/<str:auhtorScopusId>/', TemplateView.as_view(template_name='author-details.html'), name='author-details'), # Pagine di visualizzazione dei dettagli di un autore
    
    # AFFILIAZIONI
    path('affiliations/affiliation-details/<str:affiliationScopusId>/', TemplateView.as_view(template_name='affiliation-details.html'), name='affiliation-details'), # Pagina di visualizzazione dei dettagli di una affiliazione
    
    # SNAPSHOTS
    path('snapshots/snapshot-compute/<str:groupId>/', TemplateView.as_view(template_name='snapshot-compute.html'), name="snapshot-compute"), # Pagina che computa lo snapshot di un gruppo al momento presente
    path('snapshots/snapshots-list', TemplateView.as_view(template_name='snapshots-list.html'), name="snapshots-list"), # Pagina di visualizzazione degli snapshot salvati (con possibilità di confrontarli a 2 a 2)
    path('snapshots/snapshot-get/<str:snapshotId>/', TemplateView.as_view(template_name='snapshot-get.html'), name="snapshot-get"), # Pagina che mostra uno snapshot salvato
    path('snapshots/snapshots-compare/<str:snapshotId1>/<str:snapshotId2>/', TemplateView.as_view(template_name='snapshots-compare.html'), name="snapshots-compare"), # Pagina che mostra uno snapshot salvato
]
