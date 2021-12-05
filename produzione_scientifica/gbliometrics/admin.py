from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomRegistrationForm
from .models import Authors_Group, CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomRegistrationForm # Form custom per creare un utente
    form = CustomUserChangeForm # Form custom per modificare i dati di un utente
    model = CustomUser # Modello User custom
    list_display = ('email', 'is_staff', 'username', 'is_active', 'last_login',) # Campi da mostrare nella pagina principale
    list_filter = ('email', 'is_staff', 'username', 'is_active', 'last_login',) # Campi su cui filtrare
    fieldsets = ( # Campi di visualizzazione
        ('Dati d\'accesso', {'fields': ('email', 'password', 'username', 'last_login')}),
        ('Permessi', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username') # Campi di ricerca
    ordering = ('email','username') # Campi di ordinamento

admin.site.register(CustomUser, CustomUserAdmin) # Aggiungo la visualizzazione degli utenti Custom
admin.site.register(Authors_Group) # Aggiungo la visualizzazione dei gruppi