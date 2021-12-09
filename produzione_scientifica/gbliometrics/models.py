from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy

from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email' # email dell'utente
    REQUIRED_FIELDS = ['username'] # Campi richiesti oltre all'USERNAME_FIELD e la Password

    objects = CustomUserManager()

    def __str__(self):
        return self.username+" : "+self.email

class Agroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE); # Utente che ha creato il gruppo
    name = models.CharField(max_length=50); # Nome del gruppo
    creation = models.DateTimeField(); # Data di creazione
    last_update = models.DateTimeField(); # Ultima modifica
    other_info = models.TextField(max_length=200, null=True, blank=True) # Annotazioni Extra
    
    REQUIRED_FIELDS = ['user', 'name']
    
    def __str__(self):
        return self.user.username+"@"+self.name # Nome elemento nella vista dell'admin
    
    class Meta:
        unique_together = ('user','name'); # La coppia di camoi deve essere univoca
    

class Affiliation(models.Model):
    # IDs
    scopusId = models.PositiveBigIntegerField(unique=True); # Identificativo (uso solo questo poichè è possibile costruire l'eid come 10-s2.0-<scopusId>)
    # eid = models.TextField(unique=True, max_length=20); 
    # Dati
    name = models.CharField(max_length=50, unique=True);
    address = models.CharField(max_length=50, null=True, blank=True);
    city = models.CharField(max_length=50, null=True, blank=True);
    state = models.CharField(max_length=50, null=True, blank=True);
    postal_code = models.CharField(max_length=50, null=True, blank=True);
    country = models.CharField(max_length=50, null=True, blank=True);
    url = models.URLField(null=True, blank=True);
    # Campi di competenza della mia app (NO ELSEVIER)
    creation = models.DateTimeField();
    last_update = models.DateTimeField();
    
    REQUIRED_FIELDS = ['scopusId', 'name'];
    
    def __str__(self):
        return self.name+" ("+str(self.scopusId)+")"
    
'''
class Author(models.Model):
    # IDs
    auth_id = models.PositiveBigIntegerField(unique=True);
    auth_eid = models.TextField(unique=True, max_length=20);
    auth_orcid = models.PositiveBigIntegerField(unique=True);
    # Dati anagrafici
    name = models.TextField(max_length=50); # Nome
    surname = models.TextField(max_length=50) # Cognome
    full_name = models.TextField(max_length=100); # Nome completo (Cognome N.)
    # Timestamps
    creation_date = models.DateTimeField('Creation date into DB');
    # Associazione
    affiliation = models.ForeignKey(Affiliation, on_delete=models.RESTRICT);
    
    REQUIRED_FIELDS = ['name', 'surname', 'full_name', 'affiliation'];
'''