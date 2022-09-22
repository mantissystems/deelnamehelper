from django import forms 
from django.db import models
from beatrix.models import Person

class Personform(forms.Form):
  class Meta:
    model =Person
    fields=('__all__')