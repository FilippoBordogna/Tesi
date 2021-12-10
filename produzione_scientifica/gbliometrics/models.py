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
    # ATTENZIONE: Prima di eliminare una affiliazione devo eliminare la dipendenza degli autori da quella affiliazione.
    # IDs
    scopusId = models.PositiveBigIntegerField(unique=True); # Identificativo (uso solo questo poichè è possibile costruire l'eid come 10-s2.0-<scopusId>)
    # eid = models.TextField(unique=True, max_length=20); 
    # Dati
    name = models.CharField(max_length=50, unique=True); # Nome
    address = models.CharField(max_length=50, null=True, blank=True); # Indirizzo
    city = models.CharField(max_length=50, null=True, blank=True); # Città
    state = models.CharField(max_length=50, null=True, blank=True); # Provincia
    postal_code = models.CharField(max_length=50, null=True, blank=True); # Codice Postale
    country = models.CharField(max_length=50, null=True, blank=True); # Nazione
    url = models.URLField(null=True, blank=True); # Sito internet principale
    # Campi di competenza della mia app (NO ELSEVIER)
    creation = models.DateTimeField(); # Data di creazione nel mio DB
    last_update = models.DateTimeField(); # Data di ultima modifica nel mio DB
    
    REQUIRED_FIELDS = ['scopusId', 'name']; # Campi obbligatori
    
    def __str__(self):
        return self.name+" ("+str(self.scopusId)+")"
    

class Author(models.Model):
    # IDs
    scopusId = models.PositiveBigIntegerField(unique=True); # Id di Scopus: Dato questo campo con 9-s2.0-<scopusId> trovo l'eid
    # eid = models.TextField(unique=True, max_length=20);
    # Dati anagrafici
    name = models.CharField(max_length=50, null=True, blank=True); # Nome
    surname = models.CharField(max_length=50, null=True, blank=True) # Cognome
    full_name = models.CharField(max_length=100); # Nome completo (Cognome N.)
    # Chiave esterna alla classe Affiliation:
    # Prima di eliminare una affiliazione devo eliminare la dipendenza degli autori da quella affiliazione
    affiliation = models.ForeignKey(Affiliation, on_delete=models.RESTRICT); # Affiliazione a cui è affiliato
    # Timestamps
    creation = models.DateTimeField(); # Data di creazione nel mio DB
    last_update = models.DateTimeField(); # Data ultima modifica del record nel mio DB
    
    REQUIRED_FIELDS = ['scopusId', 'full_name', 'affiliation']; # Campi obbligatori
    
    def __str__(self):
        return self.full_name+" ("+str(self.scopusId)+")"
    

class Connection(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # Chiave esterna alla classe Author
    group = models.ForeignKey(Agroup, on_delete=models.CASCADE) # Chiave esterna alla classe Agroup
    