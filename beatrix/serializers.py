from rest_framework import serializers
from .models import Flexevent, Flexrecurrent, Person, Topic,Note
from rest_framework.serializers import ModelSerializer

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name','user','pos1')
        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields='__all__'                

class FlexeventSerializer(serializers.ModelSerializer):
    # topic=TopicSerializer(read_only=True,many=True)
    class Meta:
        model = Flexevent
        fields='__all__'

class FlexrecurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexrecurrent
        fields='__all__'        


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'