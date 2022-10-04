from django.urls import path

from beatrix.views import( 
AanmeldView, FlexdetailView, FlexeventsView, PersonListView,PersonUpdateView, PersonenLijstMaken, 
apiOverview, bootBeheer, bootDetail, bootLijst, bootWerfuit, eventBeheer, flexEvents, home,
recurrent_event,
# events,
# maandlistview,
# personenlijst,
# event_detail,
# flexlistview,
deelname, ResultsView, vote,DetailView,IndexView, werfin
# assign,
)

# app_name = 'beatrix'
urlpatterns = [
    # path('', home, name='home'),
    path('', FlexeventsView.as_view(), name='home'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:event_id>/vote/', vote, name='vote'),  
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('events/', AanmeldView.as_view(), name='aanmelden'),
    path('recurrent/', recurrent_event, name='recurrent'),
    path('<int:pk>/', PersonUpdateView.as_view(), name='person_change'),
    path('api/person/', PersonenLijstMaken.as_view()),    
    path('api/', apiOverview,name='api-overview'),    
    path('bootlijst/', bootLijst,name='bootlijst'),    
    path('flexevents/', flexEvents,name='flexevents'),    
    path('bootdetail/<str:pk>/', bootDetail,name='bootdetail'),    
    path('bootaanmaken/', werfin,name='bootaanmaken'),    
    path('bootbeheer/<str:pk>/', bootBeheer,name='bootbeheer'),    
    path('flexeventsbeheer/<str:pk>/', eventBeheer,name='flexeventsbeheer'),    
    path('bootwerfuit/<str:pk>/', bootWerfuit,name='bootwerfuit'),    
    # path('kal/<slug:slug>/' , FlexdetailView.as_view(), name='kal'),     
    # path('collect/', Flexpoule.as_view(), name='collect'),
    # path('collecting/', flexcollect, name='collecting'),
    # path('flexcalculate/', FlexCalculateView.as_view(), name='flexcalculate'),
    # path('export/', export_team_data, name='export'),
    # path('eq/<slug:slug>/' , equipe_aanwezigheid, name='eq'), 
    # path('helptekst/', HelpTekstView.as_view(), name='helptekst'),
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/