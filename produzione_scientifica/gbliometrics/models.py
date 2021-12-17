from datetime import datetime
from enum import unique
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy

from .managers import CustomUserManager
from django.conf import settings
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email' # email dell'utente
    REQUIRED_FIELDS = ['username'] # Campi richiesti oltre all'USERNAME_FIELD e la Password

    objects = CustomUserManager()

    def __str__(self):
        return self.username+" : "+self.email
  

class Affiliation(models.Model):
    # ATTENZIONE: Prima di eliminare una affiliazione devo eliminare la dipendenza degli autori da quella affiliazione.
    # IDs
    scopusId = models.PositiveBigIntegerField(unique=True) # Identificativo (uso solo questo poichè è possibile costruire l'eid come 10-s2.0-<scopusId>)
    # eid = models.TextField(unique=True, max_length=20)
    # Dati
    name = models.CharField(max_length=50, unique=True) # Nome
    address = models.CharField(max_length=50, null=True, blank=True) # Indirizzo
    city = models.CharField(max_length=50, null=True, blank=True) # Città
    state = models.CharField(max_length=50, null=True, blank=True) # Provincia
    postal_code = models.CharField(max_length=50, null=True, blank=True) # Codice Postale
    country = models.CharField(max_length=50, null=True, blank=True) # Nazione
    url = models.URLField(null=True, blank=True) # Sito internet principale
    # Campi di competenza della mia app (NO ELSEVIER)
    creation = models.DateTimeField() # Data di creazione nel mio DB
    last_update = models.DateTimeField() # Data di ultima modifica nel mio DB
    
    REQUIRED_FIELDS = ['scopusId', 'name'] # Campi obbligatori
    
    def __str__(self):
        return self.name+" ("+str(self.scopusId)+")"
    

class Author(models.Model):
    # IDs
    scopusId = models.PositiveBigIntegerField(unique=True) # Id di Scopus: Dato questo campo con 9-s2.0-<scopusId> trovo l'eid
    # eid = models.TextField(unique=True, max_length=20)
    # Dati anagrafici
    name = models.CharField(max_length=50, null=True, blank=True) # Nome
    surname = models.CharField(max_length=50, null=True, blank=True) # Cognome
    full_name = models.CharField(max_length=100) # Nome completo (Cognome N.)
    # Chiave esterna alla classe Affiliation:
    # Prima di eliminare una affiliazione devo eliminare la dipendenza degli autori da quella affiliazione
    affiliation = models.ForeignKey(Affiliation, on_delete=models.RESTRICT) # Affiliazione a cui è affiliato
    # Timestamps
    creation = models.DateTimeField() # Data di creazione nel mio DB
    last_update = models.DateTimeField() # Data ultima modifica del record nel mio DB
    
    REQUIRED_FIELDS = ['scopusId', 'full_name', 'affiliation'] # Campi obbligatori
    
    def __str__(self):
        return self.full_name+" ("+str(self.scopusId)+")"
    

class Agroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) # Utente che ha creato il gruppo
    name = models.CharField(max_length=50) # Nome del gruppo
    authors = models.ManyToManyField(Author, null=True, blank=True) # Autori appartenenti al gruppo
    other_info = models.TextField(max_length=200, null=True, blank=True) # Annotazioni Extra
    creation = models.DateTimeField() # Data di creazione
    last_update = models.DateTimeField() # Ultima modifica
    
    
    REQUIRED_FIELDS = ['user', 'name']
    
    def __str__(self):
        return self.user.username+"@"+self.name # Nome elemento nella vista dell'admin
    
    class Meta:
        unique_together = ('user','name') # La coppia di camoi deve essere univoca
        
class Snapshot(models.Model):
    def user_directory_path(instance, title): # Funzione che crea il percorso ed il nome del file json
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_"+title+".json"
        return 'snapshots/user_{0}/{1}'.format(instance.user.id, filename)
    
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) # Utente proprietario
    title = models.CharField(max_length=50) # Titolo dello Snapshot  
    creation = models.DateTimeField(default=datetime.now()) # Data di creazione
    informations = models.FileField(upload_to=user_directory_path) # File contenente i dati
    
    def __str__(self):
        #return self.creation.strftime("%Y-%m-%d_%H-%M-%S@")+self.user.username+"@"+self.title # Nome elemento nella vista dell'admin
        return self.informations.path

# Operazioni post Evento
@receiver(models.signals.post_delete, sender=Snapshot)
def delete_file(sender, instance, *args, **kwargs):
    '''
        Quando viene eliminato uno Snapshot elimina il file contente lo Snapshot eliminato
    '''

    if (instance.informations): # campo non null
        path = instance.informations.path # Percorso del file
        if(os.path.isfile(path)): # Il percorso porta ad un file
            os.remove(path) # Elimino il file