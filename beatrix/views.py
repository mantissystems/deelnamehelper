from time import strftime
from urllib import request
from django.shortcuts import render
import datetime
from datetime import date
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from beatrix.models import( Flexevent,Flexlid,Note,
Person,Recurrent,)

from django.views.generic import(ListView,UpdateView,DetailView)
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import connection
from collections import namedtuple
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from beatrix.serializers import FlexeventSerializer, FlexrecurrentSerializer, PersoonSerializer, TopicSerializer ,NoteSerializer
from .models import Bericht, Flexrecurrent, Message, Room, Topic
from .forms import RecurrentForm, RoomForm,UserForm, erv_RoomForm

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('erv-home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('erv-home')
        else:
            messages.error(request, 'User name or password does not exist')

    context = {'page': page}
    return render(request, 'beatrix/erv-login_register.html', context)

def erv_loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('erv-home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('erv-home')
        else:
            messages.error(request, 'User name or password does not exist')

    context = {'page': page}
    return render(request, 'beatrix/erv-login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('erv-home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False) # commit=False : for get the user (for email lower case)
            user.username = user.username.lower()
            user.save()

            # log the user in
            login(request, user)

            return redirect('erv-home')
        else:
            messages.error(request, 'Error occurred during registration.')

    context = {'form': form}
    return render(request, 'beatrix/erv-login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) | 
        Q(description__icontains = q) 
        ) # search 
    
    topcs = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms, 
        'topics': topcs, 
        'room_count': room_count, 
        'room_messages': room_messages
        }
    return render(request, 'beatrix/home.html', context)

def erv_home(request):
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        # messages.error(request, '.U bent niet ingelogd waardoor detail-gegevens niet worden getoond')
        messages.error(request, ".U kunt via 'Login' registreren of inloggen")

        
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all() ##.filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = month # int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    usr=request.user
    users=User.objects.all()
    aangemelden=Person.objects.all().filter(id__in=users)
    flexevents = Flexevent.objects.all().filter(
        # Q(datum__range=[start, end]) & 
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) | 
        Q(event_text__icontains = q) | 
        Q(description__icontains = q) 
        ) # search 
    d=[]
    ll=[]
    sc1=[]
    sc2=[]
    sc3=[]
    for fl in flexevents:
        ll=fl.lid.all()
        ll | ll
    aangemeld=ll
    # print(ll)
    aangemeld=User.objects.all().filter(
    Q(id__in=aangemeld)
        )
    room_count = flexevents.count()
    # namen=Person.objects.all()
    rooster=Flexevent.objects.all().filter(created__range=[start, end])
    context = {
        'rooster':rooster,
        'events': flexevents[0:6],   #te saneren in 3 templates
        'rooms': flexevents[0:6],    #te saneren in 3 templates
        'deelnemers':aangemeld,    #alle deelnemers en hun skills
        'topics': topcs, 
        'room_count': room_count, #te saneren in 3 templates
        'room_messages': room_messages, #te saneren in 3 templates
        'sc1':aangemelden,
        }
    if 'beatrix' in q:
        redirect('aanmelden')            
        return render(request, 'beatrix/maand_list.html', context)

    return render(request, 'beatrix/erv-home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'beatrix/room.html', context)
    
def erv_room(request, pk):
    event = Flexevent.objects.get(id=pk)
    event_messages = event.bericht_set.all()
    deelnemers = event.lid.all()
    kandidaten=User.objects.all().exclude(id__in=deelnemers)
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        messages.error(request, '.You are not logged in')
        # print(request.user)
        context = {'event': event,
     'event_messages': event_messages, 
     'deelnemers': deelnemers,
     'kandidaten': kandidaten,
     }   
        return render(request, 'beatrix/erv-room.html', context)
    if request.method == 'POST':
        gebruiker=User.objects.get(id=request.user.id) ## request.user
        bericht = Bericht.objects.create(
        user=gebruiker,
        event=event,
        body=request.POST.get('body')
        )
        return redirect('erv-room', pk=event.id)
        # event.deelnemers.add(request.user)

    context = {'event': event,
     'event_messages': event_messages, 
     'deelnemers': deelnemers,
     'kandidaten': kandidaten,
    }
    return render(request, 'beatrix/erv-room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'beatrix/erv-profile.html', context)
def erv_userProfile(request, pk):
    user = User.objects.get(id=pk)
    events = user.flexevent_set.all()[0:5]
    room_messages = user.message_set.all()
    topics = Topic.objects.all()    
    print(user)
    topcs = Topic.objects.all() #.filter(id__in=tops)
    topics = topcs
    context = {
        'user': user, 
        'events': events, 
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'beatrix/erv-profile.html', context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('erv-home')

    context = {'form': form, 'topics': topics}
    return render(request, 'beatrix/room_form.html', context)

@login_required(login_url='login')
def erv_createRoom(request):
    form = erv_RoomForm()
    topics = Topic.objects.all()
    datums=Flexevent.objects.all() ###values_list('datum',flat=True)
    # print(datums.datum)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        tijdstip=request.POST.get('tijdstip')
        activiteit = request.POST.get('topic')
        omschrijving=request.POST.get('description')
        datum=request.POST.get('datum')
        plandatum = datum #.strftime("%m/%d/%Y")

        omschrijving=plandatum + '; ' + activiteit
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Flexevent.objects.create(
             host=request.user,
            topic=topic,
            pub_time=request.POST.get('tijdstip'),
            name = request.POST.get('topic'),
            description=omschrijving, ##request.POST.get('description'),
            datum=request.POST.get('datum'),
            event_text=topic,
            # flexhost=request.user,

        )
        return redirect('erv-home')
    context = {'form': form, 'topics': topics,'datums':datums}
    return render(request, 'beatrix/erv-flexevent_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'beatrix/room_form.html', context)

@login_required(login_url='login')
def erv_updateRoom(request, pk):
    room = Flexevent.objects.get(id=pk)
    form = erv_RoomForm(instance=room)
    hosts=User.objects.filter(person__is_host=True)
    print(hosts)
    topics = Topic.objects.all()
    # if request.user != room.host:
    #     return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.update_or_create(name=topic_name)
        room.name = request.POST.get('topic')
        h=request.POST.get('host-choice')
        # print('new-host:',h)
        try:
            id_=User.objects.get(person__user=h)
        except KeyError:
            print('key-error', h)
        host=User.objects.get(pk=h)
        room.host =host # request.POST.get('host-choice')
        room.datum = request.POST.get('datum')
        room.pub_time = request.POST.get('pub_time')
        plandatum = room.datum.format()
        if plandatum==None:
            plantdatum="onbekend"
        else:plandatum=room.datum
        omschrijving="" #plandatum +'; ' + tijdstip + '; ' + topic_name
        room.topic = topic
        room.description = topic_name +'; ' + plandatum #request.POST.get('description')
        room.save()
        return redirect('erv-home')

    context = {'form': form, 'topics': topics, 'room': room, 'hosts': hosts}
    return render(request, 'beatrix/erv-room_form.html', context)

@login_required(login_url='login')
def erv_deleteRoom(request, pk):

    room = Flexevent.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('erv-home')

    context = {'obj': room}
    return render(request, 'beatrix/erv-delete.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'beatrix/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'beatrix/delete.html', context)

@login_required(login_url='login')
def erv_deleteMessage(request, pk):

    message = Bericht.objects.get(id=pk)

    # if request.user != message.user:
    #     return HttpResponse('Geen toestemming. Het is niet uw bericht!!')

    if request.method == 'POST':
        message.delete()
        return redirect('erv-home')

    context = {'obj': message}
    return render(request, 'beatrix/erv-delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'beatrix/erv-update-user.html', {'form': form})

@login_required(login_url='login')
def erv_updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'beatrix/erv-update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'beatrix/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'beatrix/activity.html', {'room_messages': room_messages})

@login_required(login_url='login')
def erv_activityPage(request):
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        messages.error(request, '.U bent niet ingelogd waardoor gegevens niet getoond worden')
    tops=Flexevent.objects.values_list('topic', flat=True)
    # topcs = Topic.objects.all().filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    print(year,month,einde)
    usr=request.user
    users=User.objects.all()
    aangemelden=Person.objects.all().filter(id__in=users)

    flexevents = Flexevent.objects.all().filter(
        Q(datum__range=[start, end]) 
        ) # search 
    ff=Flexevent.objects.none()
    for fl in flexevents:
        ff = fl.lid.all()
        ff | ff
    deelnemers = ff
    aangemeld=deelnemers
    # skills=Person.objects.all().filter(
    #     Q(id__in=aangemeld) &
    #     Q(pos1__in=['sc1','sc2','sc3'])&
    #     Q(pos2__in=['sc1','sc2','sc3'])&
    #     Q(pos3__in=['sc1','sc2','sc3'])&
    #     Q(pos4__in=['sc1','sc2','sc3'])&
    #     Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
    #     )
    room_count = flexevents.count()
    print(room_count)
    sc1=Person.objects.all().filter(
        Q(id__in=aangemeld) &
        Q(pos1__in=['sc1'])&
        Q(pos2__in=['sc1'])&
        Q(pos3__in=['sc1'])&
        Q(pos4__in=['sc1'])&
        Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
        )
    room_count = flexevents.count()
    # rooster=Flexevent.objects.all() #.filter(datum__range=[start, end])

    context = {
        'events': flexevents,
        # 'rooms': flexevents, 
        # 'personen':skills,
        # 'topics': topcs, 
        # 'room_count': room_count, 
        'sc1':aangemelden,
        'room_messages': room_messages
        }

    return render(request, 'beatrix/erv-activity.html', context)

def erv_topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Flexevent.objects.filter(name__contains=q)[0:6] ##.values_list('topic', flat=True)
    # topcs = Topic.objects.all().filter(id__in=tops)
    # topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'beatrix/erv-topics.html', {'topics': topics})

def erv_SchemaPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Flexevent.objects.filter(name__contains=q)[0:6] ##.values_list('topic', flat=True)
    # topcs = Topic.objects.all().filter(id__in=tops)
    # topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'beatrix/erv-schema.html', {'topics': topics})

class FlexeventsView(ListView):
    queryset=Flexevent.objects.all()
    
    def get_context_data(self, **kwargs):

        sl_ = self.kwargs.get("slug")
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        beginmonth = 1 #int(date.today().strftime('%m'))
        endmonth = 12 # int(date.today().strftime('%m'))
        # if beginmonth != 12:endmonth=beginmonth+1
        print(beginmonth,endmonth)
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[endmonth]
        x=0
        start=date(year,beginmonth,1)
        end=date(year,month,einde)
        x=10
        # rooster=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        rooster=Flexevent.objects.all()[:x]
        # print(rooster)
        for r in rooster:
            aanwezig=Flexlid.objects.all().filter(flexevent_id=r.id)
            ingedeelden=aanwezig.values_list('member_id', flat=True)
            # print(len(aanwezig))
            x+=len(aanwezig)
        y=int(x/4)
            # y=8
        roostergedeeltelijk=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        context = {
        'rooster': rooster,
        'roostergedeelte': roostergedeeltelijk,
        'events': roostergedeeltelijk,
        'regels':y,
        } 
        return context


@api_view(['GET'])
def personenlijst(request):
    deelnemers=Person.objects.all()
    serializer=PersoonSerializer(deelnemers,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def aantalregels(request):
    regels=Flexrecurrent.objects.all()
    serializer=FlexrecurrentSerializer(regels,many=True)

    return Response(serializer.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

@api_view(['POST'])
def flexeventbeheer(request):
    flexevents=Flexevent.objects.all()
    serializer=FlexrecurrentSerializer(flexevents,many=True)

    return Response(serializer.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def activiteit(request,pk):
    topic=Flexevent.objects.get(id=pk)

    serializer=TopicSerializer(topic,many=False)
    # if serializer.is_valid():
    #     serializer.save()

    return Response(serializer.data)

# @api_view(['DELETE'])
# def bootWerfuit(request,pk):
#     boot=Boot.objects.get(id=pk)
#     boot.delete()
    
#     return Response('boot verwijderd uit de werf')


class DetailView(DetailView):
    model = Flexevent
    template_name = 'beatrix/erv-detail.html'
    def get_context_data(self, **kwargs):

        sl_ = self.kwargs.get("pk")
        zoeknaam=self.kwargs.get("zoeknaam")
        event=Flexevent.objects.get(id=sl_)
        aanwezig=Flexlid.objects.all().filter(flexevent_id=event.id)
        aangemeld=event.lid.all()
        # ingedeelden=aanwezig.values_list('member_id', flat=True)
        kandidaten=User.objects.all().exclude(id__in=aangemeld)
        aanwezigen=User.objects.all().filter(id__in=aangemeld)
        print(sl_,zoeknaam)
        context = {
            'event':event,
        # 'aanwezig': ingedeelden,
        'kandidaten': kandidaten,
        'aanwezig': aanwezigen,
        } 
        return context

class ResultsView(DetailView):
    model = Flexevent
    template_name = 'beatrix/erv-room.html'
    def get_context_data(self, **kwargs):
        sl_ = self.kwargs.get("pk")
        flexevent=Flexevent.objects.filter(id=sl_)
        # print(flexevent)
        context = {
        'flexevent':flexevent,
        } 
        return context

def vote(request, event_id):
    event = get_object_or_404(Flexevent, pk=event_id)
    zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else ''
    print('event: ', event,'zoeknaam: ', zoeknaam)
    where1= Q(person__pos1__icontains='sc')
    where2=Q(first_name__icontains = zoeknaam)
    where3=Q(last_name__icontains = zoeknaam)
    where4=Q(username__icontains = zoeknaam)
    where5=Q(person__name__icontains=zoeknaam) 
    where6=Q(person__pos3__icontains=zoeknaam)
    where7=Q(person__pos4__icontains=zoeknaam)
    where8=Q(person__pos5__icontains=zoeknaam)
    if zoeknaam!='': 
        print('leeg: ', zoeknaam)
        where1= Q(person__pos1__icontains='sc')
        users = User.objects.filter(where1|where2|where3|where4|where5|where6|where7|where8).exclude(is_active=False) #[0:5]
    else:
        print('event: ', event,'zoeknaam: ', zoeknaam)
        users = User.objects.filter(where1|where2|where3|where4|where5|where6|where7|where8).exclude(is_active=False) #[0:5]
    aantalregels=4
    leden = []
    afmeldingen=[]
    for af in request.POST.getlist('afmelding'):
        event.lid.remove(af)
    for l in request.POST.getlist('aanmelding'):
        print(l)
        try:
            u = User.objects.get(pk=l)
        except:
            pass
        else:
            event.lid.add(l)
    # users = User.objects.all().filter(
    #     Q(last_name__icontains = zoeknaam) | 
    #     Q(first_name__icontains = zoeknaam) |
    #     Q(username__icontains = zoeknaam) |
    #     Q(person__name__icontains=zoeknaam) 
    # )
    aangemeld=event.lid.all()
    aanwezigen=User.objects.all().filter(id__in=aangemeld)

    return render(request, 'beatrix/erv-detail.html', {
            'event': event,
            'users':users,
            'aanwezig':aanwezigen, 
            'aantalregels':aantalregels,
            'error_message': "Er is geen keuze gemaakt.",
        })
    print('vote event_id, else')
    return HttpResponseRedirect(reverse('vote', args=(event_id,)))

def directvote(request, event_id):
    event = get_object_or_404(Flexevent, pk=event_id)
    zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else 'sc'
    # print('event: ', event,'zoeknaam: ', zoeknaam)
    events=Flexevent.objects.all()
    leden = []
    afmeldingen=[]
    for af in request.POST.getlist('afmelding'):
        event.lid.remove(af)
    for l in request.POST.getlist('aanmelding'):
        event.lid.add(l)
    personen=User.objects.all()
    kandidaten = User.objects.all().filter(
        Q(last_name__icontains = zoeknaam) | 
        Q(first_name__icontains = zoeknaam) |
        Q(person__pos1__icontains=zoeknaam) |
        Q(person__pos1__icontains='sc') |
        Q(person__pos2__icontains=zoeknaam) |
        Q(person__pos3__icontains=zoeknaam) |
        Q(person__pos4__icontains=zoeknaam) |
        Q(person__pos5__icontains=zoeknaam)
        ) # search 
    aangemeld=event.lid.all()
    aanwezigen=User.objects.all().filter(id__in=aangemeld)
    roeiers=Person.objects.filter(
        Q(id__in=aanwezigen) &
        Q(pos1__icontains=zoeknaam)
        )
    return render(request, 'beatrix/erv-home.html', {
            'event': event,
            'events':events,
            'users': personen,
            'roeiers': roeiers,
            'kandidaten':kandidaten,
            'aanwezig':aanwezigen, 
            'error_message': "Er is geen keuze gemaakt.",
        })
    print('vote event_id, else')
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('directvote', args=(event_id,)))

# def vote2(request, event_id,usr):
#     event = get_object_or_404(Flexevent, pk=event_id)
#     zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else 'sc'
#     print('event: ', event,'user: ', usr)

#     # leden = []
#     # afmeldingen=[]
#     # for af in request.POST.getlist('afmelding'):
#         # event.lid.remove(af)
#     aan= request.POST.get('aanmelding')
#     if aan: redirect('erv-home')
#         # print(l)
#     event.lid.add(usr)
#     personen=User.objects.all()
#     aanmelder=User.objects.get(pk=usr)
#     print(aanmelder)
#     kandidaten = User.objects.all().filter(
#         Q(last_name__icontains = zoeknaam) | 
#         Q(first_name__icontains = zoeknaam) |
#         Q(person__pos1__icontains=zoeknaam) |
#         Q(person__pos1__icontains='sc') |
#         Q(person__pos2__icontains=zoeknaam) |
#         Q(person__pos3__icontains=zoeknaam) |
#         Q(person__pos4__icontains=zoeknaam) |
#         Q(person__pos5__icontains=zoeknaam)
#         ) # search 
#     aangemeld=event.lid.all()
#     aanwezigen=User.objects.all().filter(id__in=aangemeld)
#     roeiers=Person.objects.filter(
#         Q(id__in=aanwezigen) &
#         Q(pos1__icontains=zoeknaam)
#         )
#     # except (KeyError, Flexlid.DoesNotExist):
#         # print(len(kandidaten)) ###regel niet verwijderen ###
#     return render(request, 'beatrix/erv-home.html', {
#             'event': event,
#             'users': personen,
#             'roeiers': roeiers,
#             'kandidaten':kandidaten,
#             'aanwezig':aanwezigen, 
#             'error_message': "Er is geen keuze gemaakt.",
#         })
#     print('vote event_id, else')
#         # selected_choice.keuzes += 1
#         # selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#     return HttpResponseRedirect(reverse('vote', args=(event_id,)))

class AanmeldView(ListView):
    template_name='beatrix/erv-aanmeldview.html'
    # print('aanmelden')
    queryset=Flexevent.objects.all()
    def get_context_data(self, **kwargs):
        x=0
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        volgendemaand=month
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        x+=1
        if month <= 12 and x==0: volgendemaand=month+1
        einde=monthend[volgendemaand]
        end=date(year,month,einde)
        beginmonth = 1 #int(date.today().strftime('%m'))
        endmonth = 12 # int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[endmonth]
        # aantalregels=10
        start=date(year,beginmonth,1)
        end=date(year,endmonth,einde)
        start=date(year,beginmonth,1)
        rooster=Flexevent.objects.filter(datum__range=[start, end])
        roostergedeeltelijk=Flexevent.objects.filter(datum__range=[start, end])
        context = {
        'rooster': rooster,
        } 
        return context


def events(request):
    q1 = Flexevent.objects.all()
    print('events')
    # fp = Flexevent.objects.filter(id=1).values('flexpoule')[0:1]
    r = q1
    template_name = 'beatrix/maand_list.html'
    aanwezigen = Flexlid.objects.all() #values_list('member_id', flat=True).filter(is_present=True)
    events = Flexevent.objects.all() #.filter(flexhost='',flexhost2='')
    rowers = Person.objects.all() #.filter(is_present=True)
    hosts = Person.objects.all() #.filter(is_host=True)
    rowers = rowers | hosts  # voeg hosts en roeiers samen
    results=Flexevent.objects.all()
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    einde=monthend[month]
    start=date(year,month,1)
    end=date(year,month,einde)
    namen=Person.objects.all()
    rooster=Flexevent.objects.filter(datum__range=[start, end])
    print(month,einde,start,end,rooster)
    context={
        # 'object_list':results,
        'rooster':rooster,
        'namen':namen,
       }
    return render(request, template_name, context)

@login_required(login_url='login')
def erv_recurrentRoom(request,pk):
    form = RecurrentForm()
    topic = Topic.objects.first()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
    if form.is_valid():

            form.save()
            print(form)
            return redirect('erv-home',) # pk=user.id)

    context = {'form': form, 'topics': topic, 'room': room}
    return render(request, 'beatrix/erv-recurrent_form.html', context)

@login_required(login_url='login')
def recurrent_event(request):
    template_name = 'beatrix/event_list.html'
    print('============ recurrent ============')
    resetsequence('beatrix_flexevent')  # bestandsbeheer: zet sequence op nul; kan niet gelijktijdig
    maak_activiteiten() #flexevents; nog tijdelijk niet qctief
    events=Flexevent.objects.all()
    context={'events':events}
    return render(request, template_name, context)

def maak_rooms(tekst,gebruiker):
        eerste=Topic.objects.all().first()
        start_date = datetime.date.today()
        Flexevent.objects.all().update_or_create(
        host=gebruiker,
        topic=eerste,
        name=tekst,
        description='omschrijving',
        created=start_date,
        )
        return

def maak_activiteiten():
    start_date = datetime.date.today()
    tomorrow = start_date + datetime.timedelta(days=1)
    #hier moet het array komen met de voorkeur weekdagen; bijvoorbeeld maandag woensdag vrijdag
    #het schema alleen op de voorkeurdagen aanmaken
    #het eventuele bestaande schema op de voorkeurdagen aanpassen; dus datums manipuleren van alle regels
    # in het voorbeeld wil ik alleen op woensdag en vrijdag middag flexevents maken
    # de dagen zijn verdeeld in o en m en iederee o of m in twee blokken van 2 uur beginnend om 09 en om 13
    #0=monday
    #6=sunday
    instellingen = Recurrent.objects.all().first()
    dagnaam=datetime.datetime.now().strftime('%A')
    weekdag=datetime.datetime.now().strftime('%w')
    dagnummer=int(weekdag)
    # model._meta.get_all_field_names()     will give you all the model's field names, then you can use 
    # dvdw=Recurrent._meta.get_field('dagvandeweek') #to work your way to the verbose name, and 
    blok=getattr(instellingen, 'blok') #to get the value from the model.
    dvdw=getattr(instellingen, 'dagvandeweek')
    bool0=getattr(instellingen, 'verwijder_oude_flexevents')
    bool1=getattr(instellingen, 'verwijder_oude_onderwerpen')
    bool2=getattr(instellingen, 'resetsequence')
    trw=getattr(instellingen, 'trainingsweken')
    print(blok,dvdw,trw,bool0,bool1,bool2)
    # return
    maak_alle_users_lid=False
    verwijder_oude_flexevents=True
    verwijder_oude_onderwerpen=False
    day_delta = datetime.timedelta(days=1)
    day_delta = datetime.timedelta(days=7) 
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    einde=monthend[month]
    start=date(year,month,1)
    end=date(year,month,einde)
    trainingsweken=4 #kijk 4 weken vooruit - eigenlijk 45 trainingsweken
    user=User.objects.all().first()         ## -- de beheerder en superuser
    onderwerp='flexroeien: '
    week=[1,2,3,4,5,6,7,8] #,8,9,10,11,12,13,14]
    dagvandeweek=['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag','7----','8====''maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag','16----','17====']
    blok=[0,1,2]                              #ochtend middag
    tijdblok=[' 09:00',' 13:00',' 17:30',' 09:00',' 13:00',' 17:30',' 09:00',' 13:00',' 17:30']   # 1x ochtend 2x middag
    if verwijder_oude_flexevents: 
        Flexevent.objects.all().delete()
        resetsequence('beatrix_flexevent')  # bestandsbeheer: zet sequence op nul; kan niet gelijktijdig meet topics
    if verwijder_oude_onderwerpen: Topic.objects.all().delete()
    print('====== start ===========')
    i=1
    # for j in range(start,stop,step):
    while i<=len(week):
        for d in blok:
            for w in week: 
                try:
                    start=date(year,month,i)
                except ValueError:
                    start=date(year,month,i)
                    print(' == error == ',i,w,start)
                    continue
                # if date(year,month,i).weekday() in (2,4):     #alleen woensdagen en vrijdagen
                if date(year,month,i).weekday() in blok:     #alleen woensdagen en vrijdagen
                    print(i,w,dagvandeweek[i] + tijdblok[d])
                    topic_name = onderwerp + tijdblok[d]
                    topic, created = Topic.objects.update_or_create(name=topic_name)
                    Flexevent.objects.all().update_or_create(
                    event_text=dagvandeweek[i] + tijdblok[d],
                    name=dagvandeweek[w] + tijdblok[d],
                    description=dagvandeweek[i] + tijdblok[d] , 
                    created=date(year,month,i ),
                    pub_time=tijdblok[d],
                    datum=date(year,month,i),
                    pub_date=date(year,month,i),
                    host=user,
                    topic=topic,
            )
        i+=1
    print('====== einde ===========' + str(i))
    # if maak_alle_users_lid:
    #     events=Flexevent.objects.all()
    #     gebruikers=User.objects.all()
    #     for f in events:    # maak alle users lid van het event (voor testdoeleinden)
    #         for p in gebruikers:
    #             f.lid.add(p)

    return
@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'api/':'api-overview',    
        'api/person':'profiel en additionele roeiinformatie',    
    'topic-list/': 'topic-list',    
    'topic-detail/<str:pk>/': 'topic-detail',    
    'topic-update/<str:pk>/': 'topic-update',    
    'topic-create/':'topic-create',    
    'topic-delete/<str:pk>/':'topic-delete',    
    }
    # return JsonResponse("API BASE POINT",safe=False)
    return Response(api_urls)

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def resetsequence(*args):        
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM sqlite_sequence");
    results = namedtuplefetchall(cursor)
    tabel='beatrix_flexevent'
    sql="UPDATE sqlite_sequence SET seq =0 where name='" + tabel + "'"
    cursor.execute(sql)

@api_view(['GET'])
def topicList(request):
    topics=Topic.objects.all()
    serializer=TopicSerializer(topics,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def topicDetail(request,pk):
    topics=Topic.objects.get(id=pk)
    serializer=TopicSerializer(topics,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def topicCreate(request):
    serializer=TopicSerializer(data=request.data,many=False)
    print(serializer)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def topicUpdate(request,pk):
    topic=Topic.objects.get(id=pk)
    serializer=TopicSerializer(instance=topic, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def topicDelete(request,pk):
    topic=Topic.objects.get(id=pk)
    topic.delete()
    # serializer=TopicSerializer(instance=topic, data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    return Response('onderwerp verwijderd')    



@api_view(['POST'])
def eventCreate(request):
    #  data = request.data
#     note = Note.objects.create(
#     )
    data = request.data
    print(request)
    note = Note.objects.create(
    body=data['body'])
   
    serializer = FlexeventSerializer(note, many=False)
    return Response(serializer.data)

    # body=data['body']
    # body=getattr(data, 'body')
    user=User.objects.all().first()         ## -- de beheerder en superuser
    topic=Topic.objects.all().first()
    year=2023
    month=1
    dagvandeweek='maandag'
    tijdblok='9-12'
    i=23
    note = Flexevent.objects.create(
    event_text=dagvandeweek + tijdblok,
    name=dagvandeweek + tijdblok,
    description='dagvandeweek[i] + tijdblok[d] ', 
    pub_time=tijdblok,
    datum=date(year,month,i),
    pub_date=date(year,month,i),
    host=user,
    topic=topic,
    )
    serializer = FlexeventSerializer(note, many=False)
    return Response(serializer.data)

# def createNote(request):
#     data = request.data
#     note = Note.objects.create(
#         body=data['body']
#     )
#     serializer = NoteSerializer(note, many=False)
#     return Response(serializer.data)

@api_view(['POST'])
def eventCreate_org(request):
    data = request.data
    print(data)
    note = Flexevent.objects.create(
        # event_text=data['event_text']
    )
    serializer=FlexeventSerializer(note,many=False)

    # if serializer.is_valid():
    #     serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def eventList(request):
    events=Flexevent.objects.all()
    serializer=FlexeventSerializer(events,many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def findNote(request,find):
    print(request,find)
    notes = Flexevent.objects.all().order_by('-updated')
    if find is not None:
        notes = Flexevent.objects.filter(event_text__icontains=find).order_by('-updated')
    serializer = FlexeventSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def eventDelete(request,pk):
    event=Flexevent.objects.get(id=pk)
    event.delete()
    return Response('flexevent verwijderd')    

@api_view(['GET', 'POST'])
def getNotes(request):

    if request.method == 'GET':
        return getNotesList(request)

    if request.method == 'POST':
        return createNote(request)


@api_view(['GET', 'PUT', 'DELETE'])
def getNote(request, pk):

    if request.method == 'GET':
        return getNoteDetail(request, pk)

    if request.method == 'PUT':
        return updateNote(request, pk)

    if request.method == 'DELETE':
        return deleteNote(request, pk)
def getNotesList(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def getNoteDetail(request, pk):
    notes = Note.objects.get(id=pk)
    serializer = NoteSerializer(notes, many=False)
    return Response(serializer.data)

@csrf_exempt
def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body'],
        host='wb'
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)
@csrf_exempt
def updateNote(request, pk):
    data = request.data
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer.data

@csrf_exempt
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')