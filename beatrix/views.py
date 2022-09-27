from django.shortcuts import render
import datetime
from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from beatrix.models import Flexevent,Flexlid,Flexrecurrent,Person,Question,Choice
from beatrix.forms import Personform
from django.views.generic import(ListView,UpdateView,DetailView)
from django.http import HttpResponse
from rest_framework.serializers import Serializer
from rest_framework import generics
from beatrix.serializers import PersoonSerializer

class PersonenLijstMaken(generics.ListCreateAPIView):
    queryset=Person.objects.all()
    serializer_class=PersoonSerializer

class FlexeventsView(ListView):
    template_name='beatrix/events.html'
    # template_name='beatrix/maand_list.html'
    queryset=Flexevent.objects.all()

    def get_context_data(self, **kwargs):
        sl_ = self.kwargs.get("slug")
        # mnd_ = self.kwargs.get("mnd")
        print(sl_)

        template_name='beatrix/maand_list.html'
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[month]
        x=0
        start=date(year,month,1)
        end=date(year,month,einde)
        x=10
        rooster=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        for r in rooster:
            aanwezig=Flexlid.objects.all().filter(flexevent_id=r.id)
            ingedeelden=aanwezig.values_list('member_id', flat=True)
            print(len(aanwezig))
            x+=len(aanwezig)
            # print(x)
        y=int(x/4)
            # y=8
        roostergedeelte=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        context = {
        'rooster': rooster,
        'roostergedeelte': roostergedeelte,
        'regels':y,
        } 
        return context


class IndexView(ListView):
    template_name = 'beatrix/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""  
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(DetailView):
    model = Flexevent
    template_name = 'beatrix/detail.html'


class ResultsView(DetailView):
    model = Flexevent
    template_name = 'beatrix/results.html'
    def get_context_data(self, **kwargs):
        sl_ = self.kwargs.get("pk")
        flexevent=Flexevent.objects.filter(id=sl_)
        print(flexevent)
        context = {
        'flexevent':flexevent,
        } 
        return context

def vote(request, event_id):
    event = get_object_or_404(Flexevent, pk=event_id)
    leden = []
    afmeldingen=[]
    hosts=[]
    for h in request.POST.getlist('hoofdhost'):
        hosts.append(h)
    for af in request.POST.getlist('afmelding'):
        afmeldingen.append(af)
    for l in request.POST.getlist('aanmelding'):
        leden.append(l)
    if len(hosts)>0:
        h=Person.objects.all().filter(id__in=hosts)[:1]
        Flexevent.objects.all().filter(id=event_id).update(flexhost=h[0].name)
        Flexlid.objects.all().filter(flexevent_id=event_id,member_id=h[0].id).update(is_host=1)
        # f=Flexlid.objects.filter(flexevent_id=9,member_id=2)
        # print('hosts',event_id,h[0].id,f)

    for l in leden:
        Flexlid.objects.all().update_or_create(
            member_id=l,
            flexevent_id=event_id,
        )        
    for af in afmeldingen:
        p = Person.objects.get(id=af)
        if p:
            m = Flexlid.objects.filter(flexevent_id=event_id,
                                       member_id=p,)
            m.delete()
        pp=Person.objects.get(id=p.id)
        pp.keuzes-=1
        pp.save()
    aanwezig=Flexlid.objects.all().filter(flexevent_id=event_id)
    host=Flexlid.objects.all().filter(flexevent_id=event_id,is_host=True)
    ingedeelden=aanwezig.values_list('member_id', flat=True)
    # persons = list(Person.objects.all())
    kandidaten=Person.objects.all().exclude(id__in=ingedeelden)
    aanwezigen=Person.objects.all().filter(id__in=ingedeelden)
    hosts=Person.objects.all().filter(id__in=host)
    question = get_object_or_404(Flexevent, pk=event_id)
    try:
        # selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice = question.lid.get(pk=request.POST['aanmelding'])
        # kk = question.choice_set.get(pk=request.POST['choice'])
        print('vote event_id, try')
    except (KeyError, Choice.DoesNotExist):
        print('vote choice, except')
        # Redisplay the form.
        print(len(aanwezig))
        print(len(kandidaten))
        return render(request, 'beatrix/detail.html', {
            'question': event,
            'kandidaten':kandidaten,
            'aanwezig':aanwezigen|hosts,  # kun je dicts typeren en in template typering weergeven?
            'error_message': "You didn't select a choice.",
        })
        # onderstaande 4 regels zijn uitgesterd omdat ze te maken hebben met de poll choices, die niet meer actief zijn
    # else:
    #     print('vote event_id, else')
    #     selected_choice.keuzes += 1
    #     selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('flex:vote', args=(event_id,)))

class FlexdetailView(ListView):
    template_name='beatrix/event_detail.html'
    # template_name='beatrix/maand_list.html'
    queryset=Flexevent.objects.all()

    def get_context_data(self, **kwargs):
        sl_ = self.kwargs.get("slug")
        # mnd_ = self.kwargs.get("mnd")
        print('flexdetailview:', sl_)
        flexevent=Flexevent.objects.get(id=sl_)
        # template_name='beatrix/maand_list.html'
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[month]
        start=date(year,month,1)
        end=date(year,month,einde)
        rooster=Flexevent.objects.filter(pub_date__range=[start, end])
        reedsingedeeld=Flexlid.objects.all()
        ri=[]
        for f in reedsingedeeld:
            ri.append(f)
        print(len(reedsingedeeld))
        ri=len(reedsingedeeld)
        reedsingedeeld=reedsingedeeld.values_list('member_id', flat=True)
        # kandidaten=Person.objects.all().exclude(id__in=reedsingedeeld)
        kandidaten=Person.objects.all()[0:ri]

        context = {
        'rooster': rooster,
        'flexevent':flexevent,
        'deelnemers':kandidaten
        } 
        return context

class AanmeldView(ListView):
    template_name='beatrix/aanmeldview.html'
    # template_name='beatrix/maand_list.html'
    queryset=Flexevent.objects.all()

    def get_context_data(self, **kwargs):
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[month]
        start=date(year,month,1)
        end=date(year,month,einde)
        rooster=Flexevent.objects.filter(pub_date__range=[start, end])
        # rooster=Flexevent.objects.all()
        context = {
        'rooster': rooster,
        } 
        return context


def events(request):
    q1 = Flexevent.objects.all()
    # print(request)
    # fp = Flexevent.objects.filter(id=1).values('flexpoule')[0:1]
    r = q1
    template_name = 'beatrix/events.html'
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
    rooster=Flexevent.objects.filter(pub_date__range=[start, end])
    # rooster=Flexevent.objects.all() #filter(pub_date__range=[(2021,1,1),(2023,12,12)])
    print(month,einde,start,end,rooster)
    context={
        # 'object_list':results,
        'rooster':rooster,
        'namen':namen,
       }
    return render(request, template_name, context)

class PersonListView (ListView):
    model=Person
    queryset = Person.objects.all()           
    # template_name='beatrix/personlistview.html'
    template_name='person/aanmeldview.html'
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Personform(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Personform()

    return render(request, 'person_form.html', {'form': form})

def deelname(request, event_id):
    print('deelname')
    event = get_object_or_404(Flexevent, pk=event_id)
    selected_event = Flexevent.objects.all().filter(id=event_id)
    leden = []
    afmeldingen=[]
    for l in request.POST.getlist('aanmelding'):
        leden.append(l)
    print(leden)
    for af in request.POST.getlist('host'):
        afmeldingen.append(af)        
    print(afmeldingen)
    aanwezig=Person.objects.all().filter(id__in=leden)
    for l in leden:
        Flexlid.objects.all().update_or_create(
            member_id=l,
            taak_id=event_id,
        )
        p=Person.objects.get(id=l)
        p.keuzes+=1
        p.is_flex=True
        p.save()
    for af in afmeldingen:
        p = Person.objects.get(id=af)
        if p:
            m = Flexlid.objects.filter(taak=event.id,
                                       member_id=p,)
            m.delete()
        pp=Person.objects.get(id=p.id)
        pp.keuzes-=1
        pp.save()
    return HttpResponseRedirect(reverse('beatrix:kal', args=(event_id,)))


class PersonUpdateView(UpdateView):
    template_name = 'beatrix/person_form.html'
    model = Person
    fields = ('name','email' , 'is_host', 'keuzes',)
    form_class = Personform
    success_url = reverse_lazy('beatrix:person_changelist')
    def get_context_data(self, **kwargs):
        print (**kwargs)
        context={
       }
        return context

def recurrent_event(request):
    template_name = 'beatrix/event_list.html'
    maak_activiteiten()
    return render(request, template_name, {})

def maak_activiteiten():
    start_date = datetime.date.today()
    tomorrow = start_date + datetime.timedelta(days=1)
    dagnaam=datetime.datetime.now().strftime('%A')
    weekdag=datetime.datetime.now().strftime('%w')
    dagnummer=int(weekdag)
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
        dagnaam=datum2.strftime('%A')
        week=datum2.strftime('%W'),
        for t in range(1,7,1):
            tijd2="20:30"
            Flexevent.objects.all().update_or_create(
                event_text='training_' + str(j),
              dagnaam=dagnaam, 
              flexhost='Te bepalen',
              pub_date=datum2,
              pub_time=tijd2,
                )
    p=Person.objects.all().first()
    f=Flexevent.objects.first()
    Flexlid.objects.all().update_or_create(
    member=p, 
    flexevent=f,
    )

    return