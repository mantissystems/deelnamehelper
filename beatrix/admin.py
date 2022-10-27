from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Dataimport, User
from .models import Flexevent, Person, Topic
from .models import Room, Message,Person

# admin.site.register(UserAdmin)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

admin.site.register(Flexevent)
admin.site.register(Person)
admin.register(User)
admin.register(Dataimport)
