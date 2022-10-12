from django.contrib import admin
from django.urls import path,include
# from beatrix.views import events
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('beatrix.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),    
    # path('beatrix', include('beatrix.urls')),
    # path('', events, name='events'),    
]
