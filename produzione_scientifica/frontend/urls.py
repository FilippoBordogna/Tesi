from django.urls import path
from django.views.generic.base import TemplateView # Vista generica TemplateView

app_name = "frontend" # Namespace per evitare futuri conflitti

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name = 'home'), # Pagina principale
]
