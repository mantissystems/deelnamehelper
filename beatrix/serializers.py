from rest_framework import serializers
from .models import Flexevent, Person,Boot

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email')

class BootSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boot
        # fields = ('id', 'bootnaam', 'beschikbaar')
        fields='__all__'

class FlexeventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'