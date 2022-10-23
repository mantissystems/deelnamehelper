from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Flexevent, Room,User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
    #   fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class erv_RoomForm(ModelForm):
    class Meta:
        model = Flexevent
        fields = '__all__'
        exclude = ['host', 'lid']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'email']        
        # fields = ['avatar', 'name', 'username', 'email', 'bio']        