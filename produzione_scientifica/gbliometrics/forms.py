from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from django_registration.forms import RegistrationForm

'''class CustomUserCreationForm(UserCreationForm): # Form di creazione utente personalizzata

    class Meta:
        model = CustomUser
        fields = ('email', 'username') # Campi da specificare oltre alla password
'''

class CustomUserChangeForm(UserChangeForm):
    '''
        Form di modifica utente personalizzata (Secondo il modello User customizzato)
    '''
    class Meta:
        model = CustomUser
        fields = ('email', 'username') # Campi da specificare oltre alla password
        
class CustomRegistrationForm(RegistrationForm):
    '''
        Form di creazione utente personalizzata (Secondo il modello User customizzato)
    '''
    class Meta:
        model = CustomUser
        fields = ('email', 'username') # Campi da specificare oltre alla password