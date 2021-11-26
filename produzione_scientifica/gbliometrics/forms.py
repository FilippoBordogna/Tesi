from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm): # Form di creazione utente personalizzata

    class Meta:
        model = CustomUser
        fields = ('email', 'username') # Campi da specificare oltre alla password

class CustomUserChangeForm(UserChangeForm): # Form di modifica utente personalizzata

    class Meta:
        model = CustomUser
        fields = ('email', 'username') # Campi da specificare oltre alla password