from rest_framework import serializers
from .models import Flexevent, Person

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email')

class FlexeventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'