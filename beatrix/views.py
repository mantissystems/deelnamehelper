from urllib import request
from django.shortcuts import render
import datetime
from datetime import date
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from beatrix.models import( Flexevent,Flexlid,
Person,)

# from .models import Room,Topic,Message
# # from beatrix.forms import MyUserCreationForm, UserForm,RoomForm,Personform
from django.views.generic import(ListView,UpdateView,DetailView)
# from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.serializers import Serializer
# from rest_framework import generics
# from beatrix.serializers import FlexeventSerializer, PersoonSerializer,BootSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from beatrix.serializers import FlexrecurrentSerializer, PersoonSerializer 
from .models import Bericht, Flexrecurrent, Message, Room, Topic,Choice
from .forms import RoomForm,UserForm, erv_RoomForm

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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all().filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = 12 # int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    usr=request.user
    users=User.objects.all()
    gebruikers=Person.objects.all()
    aangemelden=Flexlid.objects.all() ##filter(member_id__in=gebruikers)
    ingedeelden=Flexevent.objects.filter(deelnemers__id__in=users)
    flexevents = Flexevent.objects.all().filter(
        Q(created__range=[start, end]) & 
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) | 
        Q(event_text__icontains = q) | 
        Q(description__icontains = q) 
        ) # search 
    d=[]
    ff=Flexlid.objects.none()
    for fl in flexevents:
        d = fl.deelnemers.all()
        ff=Flexlid.objects.all().filter(flexevent=fl)
        ff | ff
        d | d
    deelnemers = d
    aangemeld=ff
    aangemeldelijst=aangemelden.values_list('member_id',flat=True)
    skills=Person.objects.all().filter(
        Q(id__in=aangemeldelijst) &
        Q(pos1__in=['sc1','sc2','sc3'])&
        Q(pos2__in=['sc1','sc2','sc3'])&
        Q(pos3__in=['sc1','sc2','sc3'])&
        Q(pos4__in=['sc1','sc2','sc3'])&
        Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
        )
    room_count = flexevents.count()
    namen=Person.objects.all()
    rooster=Flexevent.objects.all().filter(created__range=[start, end])
    # rooster=Flexevent.objects.all() #filter(pub_date__range=[(2021,1,1),(2023,12,12)])
    print(month,einde,start,end,'count=' ,ff.count(),skills.count())
    # context={
    #     # 'object_list':results,
    #    }
    context = {
        'rooster':rooster,
        'namen':namen,
        'events': flexevents,
        'rooms': flexevents, 
        'deelnemers':skills,
        'topics': tops, 
        'room_count': room_count, 
        'room_messages': room_messages
        }
    if 'beatrix' in q:
        redirect('aanmelden')            
        return render(request, 'beatrix/maand_list.html', context)
        print(q)
        # if request.method == 'GET':
        # q1 = Flexevent.objects.all()
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
    deelnemers = event.deelnemers.all()
    aanwezig=Flexlid.objects.all().filter(flexevent_id=event.id)
    ingedeelden=aanwezig.values_list('member_id', flat=True)
    kandidaten=User.objects.all() #.exclude(id__in=ingedeelden)[:5]
    gebruikers=Person.objects.all()
    # aangemelden=Flexlid.objects.filter(member_id__in=gebruikers)
    aangemelden=Flexlid.objects.all().filter(
        Q(member_id__in=gebruikers) &
        Q(flexevent_id=event.id)
        )
    print(aangemelden)
    if request.method == 'POST':
        bericht = Bericht.objects.create(
            user=request.user,
            event=event,
            body=request.POST.get('body')
        )
        event.deelnemers.add(request.user)
        return redirect('erv-room', pk=event.id)

    context = {'event': event,
     'event_messages': event_messages, 
     'deelnemers': aangemelden,
    #  'kandidaten': kandidaten,
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
    events = user.flexevent_set.all()
    room_messages = user.message_set.all()
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all().filter(id__in=tops)
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
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Flexevent.objects.create(
             host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            event_text=topic,
            flexhost=request.user,

        )
        return redirect('erv-home')

    context = {'form': form, 'topics': topics}
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
    topics = Topic.objects.all()
    event = Flexevent.objects.get(id=pk)
    event_messages = event.bericht_set.all()
    deelnemers = event.deelnemers.all()
    ingedeelden=deelnemers.values_list('id', flat=True)
    deelnemers = event.deelnemers.all()
    kandidaten=User.objects.all().exclude(id__in=ingedeelden)[0:10]
    users=User.objects.all()
    ing=Flexevent.objects.filter(deelnemers__id__in=users)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')
    verwijder=Flexevent.objects.none()
    flexevnt = get_object_or_404(Flexevent, pk=pk)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
#  als id in deelnemers, dan verwijderen
        for l in request.POST.getlist('aanmelding'):
            verwijder=Flexevent.objects.filter(deelnemers__id__in=l)
            event.deelnemers.add(l)
            v=deelnemers.filter(id__in=l)
            # print(verwijder)
            if v:
                print('verwijder', v)
        for l in request.POST.getlist('aanmelding'):
            verwijder=Flexevent.objects.filter(deelnemers__id__in=l)
            event.deelnemers.add(l)
# 
    context = {'form': form, 
    'topics': topics,
     'room': room,
     'event': room,  # tbv erv-detail.html
     'kandidaten': kandidaten,
     }
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

    if request.user != message.user:
        return HttpResponse('U mag hier niet komen!!')

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

    return render(request, 'beatrix/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'beatrix/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'beatrix/activity.html', {'room_messages': room_messages})

def erv_activityPage(request):
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all().filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = 12 # int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    usr=request.user
    users=User.objects.all()
    ingedeelden=Flexevent.objects.filter(deelnemers__id__in=users)
    flexevents = Flexevent.objects.all().filter(
        Q(pub_date__range=[start, end]) 
        # Q(topic__name__icontains = q) | 
        # Q(name__icontains = q) | 
        # Q(event_text__icontains = q) | 
        # Q(description__icontains = q) 
         ) # search 
    for fl in flexevents:
        d = fl.deelnemers.all()
        d | d
        deelnemers = d
    skills=Person.objects.all().values_list('pos1','pos2','pos3','pos4','pos5').filter(
        Q(id__in=deelnemers) &
        Q(pos1__in=['sc1','sc2','sc3'])&
        Q(pos2__in=['sc1','sc2','sc3'])&
        Q(pos3__in=['sc1','sc2','sc3'])&
        Q(pos4__in=['sc1','sc2','sc3'])&
        Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
        )

    room_count = flexevents.count()
    # sessions = Session.objects.filter(expire_date__gte=date.today())
    # uid_list = []
    context = {
        'events': flexevents,
        'rooms': flexevents, 
        'personen':skills,
        'topics': topcs, 
        'room_count': room_count, 
        'room_messages': room_messages
        }

    return render(request, 'beatrix/erv-activity.html', context)

def erv_topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Flexevent.objects.filter(description__contains=q) ##.values_list('topic', flat=True)
    # topcs = Topic.objects.all().filter(id__in=tops)
    # topics = topcs ##Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'beatrix/erv-topics.html', {'topics': topics})

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

# @api_view(['GET'])
# def bootDetail(request,pk):
#     boot=Boot.objects.get(id=pk)
#     serializer=BootSerializer(boot,many=False)

#     return Response(serializer.data)

# @api_view(['POST'])
# def werfin(request):
#     serializer=BootSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['POST'])
# def bootBeheer(request,pk):
#     boot=Boot.objects.get(id=pk)
#     serializer=BootSerializer(instance=boot,data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# def bootWerfuit(request,pk):
#     boot=Boot.objects.get(id=pk)
#     boot.delete()
    
#     return Response('boot verwijderd uit de werf')

# class IndexView(ListView):
#     template_name = 'beatrix/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""  
#         return Question.objects.order_by('-pub_date')[:5]


# class DetailView(DetailView):
#     model = Flexevent
#     template_name = 'beatrix/detail.html'


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
    print(event)
    leden = []
    afmeldingen=[]
    hosts=[]
    for h in request.POST.getlist('hoofdhost'):
        hosts.append(h)
    for af in request.POST.getlist('afmelding'):
        afmeldingen.append(af)
    for l in request.POST.getlist('aanmelding'):
        leden.append(l)
    aantalregels=30
    if len(hosts)>0:
        hh=Person.objects.all().filter(id__in=hosts)[:1]
        uu=User.objects.all().filter(id__in=hosts)[:1]
        # Flexevent.objects.all().filter(id=event_id).update(flexhost=h[0].name)
        Flexlid.objects.all().filter(flexevent_id=event_id,member_id=hh[0].id).update(is_host=1)
    for l in leden:
        try:
            uu=User.objects.get(id=l)
            event.deelnemers.add(uu)
        except (KeyError, User.DoesNotExist):
            print('vote deelnemer add, except')
        Flexlid.objects.all().update_or_create(
            member_id=l,
            flexevent_id=event_id,
        )        
    for af in afmeldingen:
        p = Person.objects.get(id=af)
        if p:
            m = Flexlid.objects.filter(flexevent_id=event_id,
                                       member_id=p,)
            print(m)
            if m[0].is_host==True:
                Flexevent.objects.all().filter(id=event_id).update(flexhost='')
            m.delete()

        pp=Person.objects.get(id=p.id)
        pp.keuzes-=1
        pp.save()
    aanwezig=Flexlid.objects.all().filter(flexevent_id=event_id)
    ishost=Flexlid.objects.all().filter(flexevent_id=event_id,is_host=True)
    ingedeelden=aanwezig.values_list('member_id', flat=True)
    zijnhost=ishost.values_list('member_id', flat=True)
    kandidaten=Person.objects.all().exclude(id__in=ingedeelden)[:5]
    kandidaten=Person.objects.all()
    aanwezigen=Person.objects.all().filter(id__in=ingedeelden)
    hosts=Person.objects.all().filter(id__in=zijnhost) #.update(is_host=True)
    question = get_object_or_404(Flexevent, pk=event_id)
    try:
        # selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice = question.lid.get(pk=request.POST['aanmelding'])
        print('vote event_id, try')
    except (KeyError, Choice.DoesNotExist):
        print('vote choice, except')
        # Redisplay the form.
        # print(len(aanwezig)) #regel niet verwijderen
        # print(len(kandidaten)) #regel niet verwijderen
        return render(request, 'beatrix/erv-detail.html', {
            'event': event,
            'kandidaten':kandidaten[0:5],
            'aanwezig':aanwezigen, 
            'hosts':hosts, 
            # 'boten':boten, 
            'aantal':kandidaten.count(), 
            'aantalregels':aantalregels,
            'error_message': "Er is geen keuze gemaakt.",
        })
        # onderstaande 4 regels zijn uitgesterd omdat ze te maken hebben met de poll choices, die niet meer actief zijn
    else:
        print('vote event_id, else')
        selected_choice.keuzes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('vote', args=(event_id,)))



class AanmeldView(ListView):
    template_name='beatrix/erv-aanmeldview.html'
    print('aanmelden')
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
        x=100
        aantalregels=10
        start=date(year,beginmonth,1)
        end=date(year,endmonth,einde)
        start=date(year,beginmonth,1)
        rooster=Flexevent.objects.filter(created__range=[start, end])
        roostergedeeltelijk=Flexevent.objects.filter(created__range=[start, end])[:x]
        context = {
        'rooster': roostergedeeltelijk,
        'aantalregels':aantalregels,
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
    # hosts = Person.objects.all().filter(is_host=True, is_present=True)
    rowers = rowers | hosts  # voeg hosts en roeiers samen
    results=Flexevent.objects.all()
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    einde=monthend[month]
    start=date(year,month,1)
    end=date(year,month,einde)
    namen=Person.objects.all()
    rooster=Flexevent.objects.filter(created__range=[start, end])
    # rooster=Flexevent.objects.all() #filter(pub_date__range=[(2021,1,1),(2023,12,12)])
    print(month,einde,start,end,rooster)
    context={
        # 'object_list':results,
        'rooster':rooster,
        'namen':namen,
       }
    return render(request, template_name, context)

# class PersonListView (ListView):
#     model=Person
#     queryset = Person.objects.all()           
#     # template_name='beatrix/personlistview.html'
#     template_name='person/aanmeldview.html'
# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = Personform(request.POST)
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = Personform()

#     return render(request, 'person_form.html', {'form': form})

# def deelname(request, event_id):
#     print('deelname')
#     event = get_object_or_404(Flexevent, pk=event_id)
#     selected_event = Flexevent.objects.all().filter(id=event_id)
#     leden = []
#     afmeldingen=[]
#     for l in request.POST.getlist('aanmelding'):
#         leden.append(l)
#     print(leden)
#     for af in request.POST.getlist('host'):
#         afmeldingen.append(af)        
#     print(afmeldingen)
#     aanwezig=Person.objects.all().filter(id__in=leden)
#     for l in leden:
#         Flexlid.objects.all().update_or_create(
#             member_id=l,
#             taak_id=event_id,
#         )
#         p=Person.objects.get(id=l)
#         p.keuzes+=1
#         p.is_flex=True
#         p.save()
#     for af in afmeldingen:
#         p = Person.objects.get(id=af)
#         if p:
#             m = Flexlid.objects.filter(taak=event.id,
#                                        member_id=p,)
#             m.delete()
#         pp=Person.objects.get(id=p.id)
#         pp.keuzes-=1
#         pp.save()
#     return HttpResponseRedirect(reverse('beatrix:kal', args=(event_id,)))


def recurrent_event(request):
    template_name = 'beatrix/flexevent_list.html'
    maak_activiteiten() #flexevents; houd tijdelijk niet qctief
    # Topic.objects.all().delete()
    # Room.objects.all().delete()
    # Message.objects.all().delete()
    # tops=[]
    # tops.append('flexmaandag')
    # tops.append('flexdinsdag')
    # tops.append('flexwoensdag')
    # tops.append('flexdonderdag')
    # tops.append('flexvrijdag')
    gebruiker=User.objects.all().first()
    # for t in tops:
    #     Topic.objects.all().update_or_create(
    #         name=t,
    #     )
    #     maak_rooms(t,gebruiker)
    return render(request, template_name, {})

def maak_rooms(tekst,gebruiker):
        # gebruiker=User.objects.all().first()
        eerste=Topic.objects.all().first()
        start_date = datetime.date.today()
        Flexevent.objects.all().update_or_create(
        host=gebruiker,
        topic=eerste,
        name=tekst,
        description='omschrijving',
        # updated=start_date,
        created=start_date,
        )
        room = Flexevent.objects.all().first()
        # room_messages = room.message_set.all()
        participants = room.deelnemers.all()
        room.deelnemers.add(gebruiker)
        message = Bericht.objects.create(
            user=gebruiker,
            event=room,
            body=tekst
        )
        return

def maak_activiteiten():
    start_date = datetime.date.today()
    tomorrow = start_date + datetime.timedelta(days=1)
    dagnaam=datetime.datetime.now().strftime('%A')
    weekdag=datetime.datetime.now().strftime('%w')
    dagnummer=int(weekdag)
    # boten=Boot.objects.values_list('bootnaam',flat=True)
    day_delta = datetime.timedelta(days=1)
    for d in range(7):
        tomorrow = start_date + datetime.timedelta(days=d)
    weekdag=int(start_date.strftime('%w'))
    Flexevent.objects.all().delete()
    taak=[]
    taak.append('training');dn=5
    trainingsweken=8 #45
    for j in range(trainingsweken):
        day_delta = datetime.timedelta(days=7) 
        datum2=start_date + j * day_delta   
        weekdag=datum2.strftime('%w')
        dagnaam='training_' + str(j)
        week=datum2.strftime('%W')
        personen=Person.objects.values_list('name',flat=True)
        qs2 = Person.objects.none()
        for pp in personen:
            dd = pp.split(' ')
            if len(dd[0]) > 100:
                created = User.objects.update_or_create(
                username=dd[0],
                first_name=dd[0],
                last_name=dd,),
                password='mantis123'

        user=User.objects.all().first()
        topc=Topic.objects.create(name='gegenereerd'+ str(j))
        for t in range(1,7,1):
            tijd2="20:30"
            Flexevent.objects.all().update_or_create(
            event_text='training_' + str(j),
            description=dagnaam, 
            flexhost='Te bepalen',
            created=datum2,
            pub_time=tijd2,
            host=user,
            topic=topc,
                )
        fl=Flexevent.objects.values_list('id',flat=True)
        for f in fl:
            p=Person.objects.all().first()
        f=Flexevent.objects.first()
        Flexlid.objects.all().update_or_create(
        member=p, 
        flexevent=f,
    )

    return
@api_view(['GET'])
def apiOverview(request):
    api_urls={
    'api/':'api-overview',    
    'api/person':'api/person',    
    'bootlijst/':'bootlijst',    
    'flexevents/':'flexevents',    
    'flexeventsbeheer/':'flexeventsbeheer',    
    'bootdetail/<str:pk>/':'bootdetail',    
    'bootaanmaken/':'bootaanmaken',    
    'bootbeheer/<str:pk>/':'bootbeheer',    
    'bootwerfuit/<str:pk>/':'bootwerfuit',    


    }
    # return JsonResponse("API BASE POINT",safe=False)
    return Response(api_urls)