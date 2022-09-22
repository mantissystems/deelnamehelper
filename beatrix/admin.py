from django.contrib import admin

from beatrix.models import Flexevent, Flexlid, Person

# Register your models here.
admin.site.register(Flexevent)
admin.site.register(Flexlid)
admin.site.register(Person)