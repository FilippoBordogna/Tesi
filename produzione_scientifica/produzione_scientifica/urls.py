# Import Librerie Esterne all'app
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"), # Pagina di amministrazione
    path('gbliometrics/', include('gbliometrics.urls')), # Inclusione delle url nel file gbliometrics/urls.py
]
