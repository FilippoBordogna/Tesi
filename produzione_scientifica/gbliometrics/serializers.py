from rest_framework import serializers
from .models import Affiliation, Agroup

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