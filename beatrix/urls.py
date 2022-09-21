from django.urls import path

from beatrix.views import( 
PersonListView,PersonUpdateView,
    # recurrent_event,events,
# maandlistview,
# personenlijst,
# event_detail,
# flexlistview,
# deelname,
# assign,
)

app_name = 'beatrix'
urlpatterns = [
    # path('', events, name='events'),
    # # path('events', events, name='events'),
    path('aanmelden', PersonListView.as_view(), name='aanmelden'),
    path('<int:pk>/', PersonUpdateView.as_view(), name='person_change'),
    # path('recurrent/', recurrent_event, name='recurrent'),
    # path('kal/<slug:slug>/' , maandlistview, name='kal'),     
    # path('<int:event_id>/event_detail/', event_detail, name='event_detail'),
    # path('rooster/', flexlistview, name='rooster'),
    # # path('deelnemen/', deelname, name='deelnemen'),
    # path('<int:event_id>/deelnemen/', deelname, name='deelnemen'),  
    # path('<int:event_id>/host/', assign, name='assign'),  
    # path('api/person/', PersonenLijstMaken.as_view()),
    # path('<int:event_id>/host/', assign, name='assign'),    
    # path('<int:event_id>/deelname/', deelname, name='deelname'),    
    # path('hoofdhost/', hoofdhost, name='hoofdhost'),
    # path('collect/', Flexpoule.as_view(), name='collect'),
    # path('collecting/', flexcollect, name='collecting'),
    # path('events/', events, name='events'),
    # path('<int:id>/activiteit/', detail, name='activiteit'),
    # path('flexcalculate/', FlexCalculateView.as_view(), name='flexcalculate'),
    # path('evenement_detail', event_detail, name='evenement_detail'), 
    # path('export/', export_team_data, name='export'),
    # path('eq/<slug:slug>/' , equipe_aanwezigheid, name='eq'), 
    # path('helptekst/', HelpTekstView.as_view(), name='helptekst'),
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/