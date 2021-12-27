from django.urls import path
from django.views.generic.base import TemplateView # Vista generica TemplateView

app_name = "frontend" # Namespace per evitare futuri conflitti

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name="home"), # Pagina principale
    path('groups/', TemplateView.as_view(template_name='groups.html'), name='group-list'), # Pagina di gestione dei gruppi
    path('groups/authors/<str:groupId>/', TemplateView.as_view(template_name='authors.html'), name='author-list'), # Pagina di gestione degli autori
    path('author-detail/<str:auhtorScopusId>/', TemplateView.as_view(template_name='author-detail.html'), name='author-detail'), # Pagine di visualizzazione dei dettagli di un autore
    path('affiliation-detail/<str:affiliationScopusId>/', TemplateView.as_view(template_name='affiliation-detail.html'), name='affiliation-detail'), # Pagina di visualizzazione dei dettagli di una affiliazione
    path('snapshot/<str:groupId>/', TemplateView.as_view(template_name='snapshot.html'), name="snapshot")
]
