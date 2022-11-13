from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Flexevent, Person, Topic
from .models import Room, Message,Person,Instromer

# admin.site.register(UserAdmin)
# admin.site.register(Room)
# admin.site.register(Person)
admin.site.register(Topic)
admin.site.register(Message)
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('pos1','in_poule')
    list_display = ('name','pos1', 'is_host','is_flex')
    search_fields = ('name','email','pos1')
admin.site.register(Flexevent)
admin.site.register(Instromer)
admin.register(User)
