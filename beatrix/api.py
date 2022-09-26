from person.models import Person
from rest_framework import viewsets,permissions
from .serializers import PersoonSerializer

class PersoonViewSet(viewsets.ModelViewSet):
  queryset= Person.objects.all()
  permission_classes=[permissions.AllowAny]
  serializer_class=PersoonSerializer