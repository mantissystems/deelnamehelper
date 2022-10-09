from django.urls import path

from beatrix.views import( 
# AanmeldView, FlexdetailView, 
FlexeventsView,
#  PersonListView, PersonenLijstMaken, 
activityPage, 
# apiOverview, bootBeheer, bootDetail, bootLijst, bootWerfuit, 
createRoom, deleteMessage, deleteRoom,
erv_topicsPage, 
# eventBeheer, flexEvents, 
home,
home_erv, loginPage, logoutUser,
recurrent_event,
# deelname, ResultsView, 
registerPage, room, 
topicsPage, updateRoom, updateUser, userProfile, 
# vote,
# DetailView,IndexView, werfin
# assign,
)

# app_name = 'beatrix'
urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('topics/', topicsPage, name="topics"),
    path('update-user/', updateUser, name="update-user"),
    path('register/', registerPage, name="register"),    
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    path('room/<str:pk>/', room, name='room'),    
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', deleteMessage, name='delete-message'),
    path('activity/', activityPage, name="activity"),
    path('beatrix', home_erv, name='home-erv'),
    path('topics-erv/', erv_topicsPage, name="topics-erv"),

    # path('beatrix', FlexeventsView.as_view(), name='home-erv'),
    # path('<int:pk>/', DetailView.as_view(), name='detail'),
    # path('<int:event_id>/vote/', vote, name='vote'),  
    # path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    # path('events/', AanmeldView.as_view(), name='aanmelden'),
    path('recurrent/', recurrent_event, name='recurrent'),
    # path('api/person/', PersonenLijstMaken.as_view()),    
    # path('api/', apiOverview,name='api-overview'),    
    # path('bootlijst/', bootLijst,name='bootlijst'),    
    # path('flexevents/', flexEvents,name='flexevents'),    
    # path('bootdetail/<str:pk>/', bootDetail,name='bootdetail'),    
    # path('bootaanmaken/', werfin,name='bootaanmaken'),    
    # path('bootbeheer/<str:pk>/', bootBeheer,name='bootbeheer'),    
    # path('flexeventsbeheer/<str:pk>/', eventBeheer,name='flexeventsbeheer'),    
    # path('bootwerfuit/<str:pk>/', bootWerfuit,name='bootwerfuit'),    
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/