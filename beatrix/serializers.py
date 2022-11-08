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
        model = Flexevent
        fields='__all__'                
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']        