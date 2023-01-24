from django.urls import path
from . import views
from beatrix.views import( 
AanmeldView,
FlexeventsView,
ResultsView,
activiteit,
activityPage,
apiOverview, 
createRoom, deleteMessage, deleteRoom,
directvote,
erv_SchemaPage,
erv_activityPage,
erv_createRoom,
erv_deleteMessage,
erv_deleteRoom,
erv_home,
erv_loginPage,
erv_room,
erv_topicsPage,
erv_updateRoom,
erv_updateUser,
erv_userProfile,
events,
flexeventbeheer, 
home,
loginPage, logoutUser,
personenlijst,
recurrent_event,
registerPage, room, 
topicsPage, updateRoom, updateUser, userProfile,
vote, 
erv_recurrentRoom,
DetailView,
aantalregels,
# vote2,
)

urlpatterns = [
    path('', erv_home, name='erv-home'),
    path('beatrix', erv_home, name='erv-home'),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('topics/', topicsPage, name="topics"),
    path('update-user/', updateUser, name="update-user"),
    path('register/', registerPage, name="register"),    
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', deleteMessage, name='delete-message'),
    path('activity/', activityPage, name="activity"),

    path('erv-create-flex/', erv_createRoom, name='erv-create-flex'),
    path('erv-update-flex/<str:pk>/', erv_updateRoom, name='erv-update-flex'),
    path('erv_activity/', erv_home, name="erv-activity"),
    path('erv-room/<str:pk>/', erv_room, name='erv-room'),    
    path('erv-topics/', erv_topicsPage, name="erv-topics"),
    path('erv-delete-room/<str:pk>/', erv_deleteRoom, name='erv-delete-room'),
    path('erv-profile/<str:pk>/', erv_userProfile, name='erv-user-profile'),
    path('erv-update-room/<str:pk>/', erv_updateRoom, name='erv-update-room'),
    path('erv-delete-message/<str:pk>/', erv_deleteMessage, name='erv-delete-message'),
    path('erv-login/', erv_loginPage, name="erv-login"),
    path('erv-logout/', logoutUser, name="erv-logout"),
    path('erv-register/', registerPage, name="erv-register"),    
    path('erv-update-user/', erv_updateUser, name="erv-update-user"),

    path('recurrent/', recurrent_event, name='recurrent'),
    path('erv-recurrency/<str:pk>', erv_recurrentRoom, name='erv-recurrency'),
    path('<int:event_id>/aanmelden/',vote, name='vote'),  
    path('<int:event_id>/directaanmelden/',directvote, name='directvote'),  
    # path('<str:event_id>/<str:usr>/aanmelden/',vote2, name='vote2'),  
    path('flexevents/', erv_SchemaPage, name="aanmelden"),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('api/person/', personenlijst,name='api-person'),    
    path('api/', apiOverview,name='api-overview'),    
    path('api/aantalregels/', aantalregels,name='api-aantalregels'),    
    path('flexevent/<str:pk>/', activiteit,name='flexevent'),    
    path('flexeventbeheer', flexeventbeheer,name='flexeventbeheer'),    
    path('topic-list/', views.topicList,name='topic-list'),    
    path('event-create/', views.eventCreate,name='event-create'),    
    path('event-list/', views.eventList,name='event-list'),    
    path('event-list/<str:pk>/delete/', views.eventDelete, name="event-delete"),
    path('event-list/<str:pk>/', views.getNote, name="event"),
    path('notes/<str:pk>/', views.getNote, name="note"),
    path('event-list/<str:find>/find/', views.findNote, name="find-note"),
    path('notes/', views.getNotes, name="notes"),
    path('notes/create/', views.createNote, name="create-note"),
    path('notes/<str:pk>/update/', views.updateNote, name="update-note"),
    path('notes/<str:pk>/delete/', views.deleteNote, name="delete-note"),
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/