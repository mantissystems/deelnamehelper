from django.contrib import admin

from beatrix.models import Choice, Flexevent, Flexlid, Person, Question

# Register your models here.
admin.site.register(Flexevent)
admin.site.register(Flexlid)
admin.site.register(Person)
admin.site.register(Question)
admin.site.register(Choice)