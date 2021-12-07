from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomRegistrationForm
from .models import Agroup, CustomUser

class GroupInline(admin.StackedInline): # Oggetto Inline che verrà aggiunto
    model = Agroup
    extra = 0
    fieldsets = ( # Campi di visualizzazione
        ('Dati', {'fields': ('name', 'id', 'other_info')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )

class CustomUserAdmin(UserAdmin):
    add_form = CustomRegistrationForm # Form custom per creare un utente
    form = CustomUserChangeForm # Form custom per modificare i dati di un utente
    model = CustomUser # Modello User custom
    list_display = ('id', 'email', 'is_staff', 'username', 'is_active', 'last_login',) # Campi da mostrare nella pagina principale
    list_filter = ('email', 'is_staff', 'username', 'is_active', 'last_login',) # Campi su cui filtrare
    fieldsets = ( # Campi di modifica
        ('Dati d\'accesso', {'fields': ('email', 'password', 'username', 'last_login')}),
        ('Permessi', {'fields': ('is_staff', 'is_active')}),
    )
    inlines = [GroupInline] # Aggiungo il modulo ChoiceInline dichiarato sopra
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username') # Campi di ricerca
    ordering = ('email','username') # Campi di ordinamento
  
class CustomAgroup(admin.ModelAdmin):
    model = Agroup
    list_display = ('id', 'user', 'name', 'creation', 'last_update')
    list_filter = ('user', 'name', 'creation', 'last_update')
    fieldsets = ( # Campi di modifica
        ('Dati', {'fields': ('user', 'name', 'other_info')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('user','name', 'creation', 'last_update', 'other_info')}
        ),
    )
    search_fields = ('user','name', 'creation', 'last_update') # Campi di ricerca
    ordering = ('user','name', 'creation', 'last_update') # Campi di ordinamento

admin.site.register(CustomUser, CustomUserAdmin) # Aggiungo la visualizzazione degli utenti Custom
admin.site.register(Agroup, CustomAgroup) # Aggiungo la visualizzazione dei gruppi