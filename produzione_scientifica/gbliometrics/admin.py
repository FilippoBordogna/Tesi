from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomRegistrationForm
from .models import Affiliation, Agroup, Author, Connection, CustomUser

# MODELLI INLINE

class GroupInline(admin.StackedInline): # Oggetto Inline che verrà aggiunto
    model = Agroup
    extra = 0
    fieldsets = ( # Campi di visualizzazione
        ('Dati', {'fields': ('id', 'name', 'other_info')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )
    
class AuthorInline(admin.StackedInline): # Oggetto Inline che verrà aggiunto
    model = Author
    extra = 0
    fieldsets = ( # Campi di visualizzazione
        ('Dati', {'fields': ('scopusId', 'orcid', 'full_name')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )

# MODELLI CUSTOM

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
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username') # Campi di ricerca
    ordering = ('email','username') # Campi di ordinamento
    
    inlines = [GroupInline] # Aggiungo il modulo GroupInline dichiarato sopra
  
class CustomAgroup(admin.ModelAdmin):
    model = Agroup
    list_display = ('id', 'user', 'name', 'creation', 'last_update') # Campi da mostrare nella pagina principale
    list_filter = ('user', 'name', 'creation', 'last_update') # Campi su cui filtrare
    fieldsets = ( # Campi di modifica di un gruppo
        ('Dati', {'fields': ('user', 'name', 'other_info')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )
    add_fieldsets = ( # Campi dell'aggiunta di un gruppo
        (None, {
            'classes': ('wide',),
            'fields': ('user','name', 'creation', 'last_update', 'other_info')}
        ),
    )
    search_fields = ('id', 'name', 'creation', 'last_update',) # Campi di ricerca
    ordering = ('id', 'name', 'creation', 'last_update') # Campi di ordinamento
    
class CustomAffiliation(admin.ModelAdmin):
    model = Affiliation
    list_display = ('id', 'scopusId', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'url', 'creation', 'last_update') # Campi da mostrare nella pagina principale
    list_filter = ('scopusId', 'name','address', 'city', 'state', 'postal_code', 'country', 'creation', 'last_update') # Campi su cui filtrare
    fieldsets = ( # Campi di modifica di un utente
        ('Dati', {'fields': ('scopusId', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'url')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('scopusId', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'url', 'creation', 'last_update')}
        ),
    )
    search_fields = ('scopusId', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'url', 'creation', 'last_update') # Campi di ricerca
    ordering = ('scopusId', 'name', 'address', 'city', 'state', 'postal_code', 'country', 'url', 'creation', 'last_update') # Campi di ordinamento
    
    inlines = [AuthorInline] # Aggiungo il modulo AuthorInline dichiarato sopra
    
class CustomAuhtor(admin.ModelAdmin):
    model = Author
    list_display = ('id', 'scopusId', 'full_name', 'affiliation', 'creation', 'last_update') # Campi da mostrare nella pagina principale
    list_filter = ('scopusId', 'name', 'surname', 'full_name', 'affiliation', 'creation', 'last_update') # Campi su cui filtrare
    fieldsets = ( # Campi di modifica di un utente
        ('Identificativi', {'fields': ('scopusId', 'affiliation')}),
        ('Dati Anagrafici', {'fields': ('name', 'surname', 'full_name')}),
        ('Timestamps', {'fields': ('creation', 'last_update')}),
    )
    add_fieldsets = ( # Campi dell'aggiunta di un utente
        (None, {
            'classes': ('wide',),
            'fields': ('scopusId', 'name', 'surname', 'full_name', 'affiliation', 'creation', 'last_update')}
        ),
    )
    search_fields = ('scopusId', 'name', 'surname', 'full_name', 'creation', 'last_update') # Campi di ricerca
    ordering = ('scopusId', 'name', 'surname', 'full_name', 'affiliation', 'creation', 'last_update') # Campi di ordinamento
    
admin.site.register(CustomUser, CustomUserAdmin) # Aggiungo la visualizzazione degli Utenti Custom
admin.site.register(Agroup, CustomAgroup) # Aggiungo la visualizzazione dei Gruppi
admin.site.register(Affiliation, CustomAffiliation) # Aggiungo la visualizzazione delle Affiliazioni
admin.site.register(Author, CustomAuhtor) # Aggiungo la visualizzazione degli Autori
admin.site.register(Connection) # Aggiungo la visualizzazione delle Connessioni