from rest_framework import serializers
from .models import Flexevent, Flexrecurrent, Person, Topic

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name','user','pos1')

class FlexeventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'
class FlexrecurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexrecurrent
        fields='__all__'        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields='__all__'                
