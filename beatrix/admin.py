from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Flexevent, Person, Topic
from .models import Room, Message,Person,Instromer

# admin.site.register(UserAdmin)
# admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

admin.site.register(Flexevent)
admin.site.register(Person)
admin.site.register(Instromer)
admin.register(User)
