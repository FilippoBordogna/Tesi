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
    other_info = models.TextField(max_length=200) # Annotazioni Extra
    
    REQUIRED_FIELDS = ['user', 'name']
    
    def __str__(self):
        return self.user.username+"@"+self.name # Nome elemento nella vista dell'admin
    
    class Meta:
        unique_together = ('user','name'); # La coppia di camoi deve essere univoca
    
'''
class Affiliation(models.Model):
    # IDs
    aff_id = models.PositiveBigIntegerField(unique=True);
    aff_eid = models.TextField(unique=True, max_length=20);
    # Dati
    name = models.TextField(max_length=50);
    address = models.TextField(max_length=50);
    city = models.TextField(max_length=50);
    state = models.TextField(max_length=50);
    postal_code = models.TextField(max_length=50);
    country = models.TextField(max_length=50);
    url = models.URLField();
    # Timestamps
    creation_date = models.DateTimeField('Creation date into DB');
    scopus_create_date = models.DateTimeField('Creation date provided by Scopus API');
    
    REQUIRED_FIELDS = ['name'];

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