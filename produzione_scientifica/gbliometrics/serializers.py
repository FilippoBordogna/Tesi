from rest_framework import serializers
from .models import Affiliation, Agroup, Author

class AgroupSerializer(serializers.ModelSerializer):
    '''
        Classe che serializza la classe Agroup
    '''
    
    class Meta:
        model = Agroup
        fields = '__all__'
        
class AffiliationSerializer(serializers.ModelSerializer):
    '''
        Classe che serializza la classe Affiliation
    ''' 
    
    class Meta:
        model = Affiliation
        fields = '__all__'
        
class AuthorSerializer(serializers.ModelSerializer):
    '''
        Classe che serializza la classe Author
    ''' 
    
    class Meta:
        model = Author
        fields = '__all__'