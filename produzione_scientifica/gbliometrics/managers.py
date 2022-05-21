# Import Librerie Esterne all'app
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy

class CustomUserManager(BaseUserManager):
    """
        Manager del modello utente custom dove l'email è l'id di autenticazione anzichè l'username (comunque unico)
    """
    def create_user(self, email, password, **extra_fields): # L'username è sottinteso
        """
            Crea e salva un utente di cui sono dati email, username (sottinteso) e password
        """
        if not email:
            raise ValueError(ugettext_lazy('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields): # L'username è sottinteso
        """
            Creo e salvo un superutente (admin) di cui sono dati email, username (sottinteso) e password
        """
        # Permessi da ADMIN a TRUE altrimenti lancio ERRORE
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)