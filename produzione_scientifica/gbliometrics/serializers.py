from rest_framework import serializers
from .models import Agroup

class AgroupSerializer(serializers.ModelSerializer):
    '''
        Classe che serializza la classe Agroup
    '''
    class Meta:
        model = Agroup
        fields = '__all__'