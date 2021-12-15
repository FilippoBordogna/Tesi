# Import Librerie Esterne all'app
from django.urls import path, include
from django.views.generic.base import TemplateView # Vista generica TemplateView

app_name = "gbliometrics" # Namespace per evitare futuri conflitti

# URL
urlpatterns = [ # Url appartenenti all'app gbliometrics
    #path('user/', TemplateView.as_view(template_name='home.html'), name = 'home'), # Pagina principale
    path('api/', include('gbliometrics.api_urls'))
]
