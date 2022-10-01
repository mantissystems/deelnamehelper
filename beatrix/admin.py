from django.contrib import admin

from beatrix.models import Boot, Flexevent, Person
admin.site.register(Flexevent)
admin.site.register(Person)
# admin.site.register(Boot)
@admin.register(Boot)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('flexhost','bootnaam')
    list_display = ('flexhost', 'bootnaam')
    search_fields = ('flexhost','bootnaam')
# admin.site.register(Flexlid)
# admin.site.register(Question)