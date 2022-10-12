from django.contrib import admin

# from beatrix.models import Boot, Flexevent, Person
from .models import Flexevent, Topic ##, User
from .models import Room, Message

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

admin.site.register(Flexevent)
# admin.site.register(Person)
# @admin.register(Boot)
# class PersonAdmin(admin.ModelAdmin):
#     list_filter = ('flexhost','bootnaam')
#     list_display = ('flexhost', 'bootnaam')
#     search_fields = ('flexhost','bootnaam')
