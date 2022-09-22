from django.shortcuts import render
import datetime
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from beatrix.models import Flexevent,Flexlid,Flexrecurrent,Person
from django.views.generic import(ListView,UpdateView)

class FlexeventsView(ListView):
    template_name='beatrix/events.html'
    queryset=Flexevent.objects.all()

    def get_context_data(self, **kwargs):
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[month]
        start=date(year,month,1)
        end=date(year,month,einde)
        # namen=Person.objects.all()
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
    template_name='beatrix/personlistview.html'
    # template_name='person/aanmeldview.html'
    def get_context_data(self, **kwargs):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        # sql="select id, name,substr(name,1,1) HL from person_person GROUP BY substr(name,1,1) order by HL"
        # cursor = connection.cursor() 
        # cursor.execute(sql)
        # results = recurrent.namedtuplefetchall(cursor)
        rooster = Flexevent.objects.all()
        flexpool = Person.objects.all()           
        context={
        # 'hoofdletters':results,
        'object_list':flexpool,
        'rooster':rooster,
       }
        return context

    def get_queryset(self): # new
        # criterion2 = Q(is_host=True)
        # criterion1 = Q(is_flex=True)
        # hosts = Person.objects.all().filter(criterion2)        
        flexpool = Person.objects.all()           
        # query = self.request.GET.get('slug')
        # print(query)
        # paginate_by = 10
        # sql="select id, name,is_present,substr(name,1,1) HL from person_person GROUP BY substr(name,1,1) order by HL"
        # cursor = connection.cursor() 
        # cursor.execute(sql)
        # results = recurrent.namedtuplefetchall(cursor)
        # template_name='person/person_list.html'            
        rooster = Flexevent.objects.all()
        results=flexpool
        # template_name='beatrix/aanmeldview.html'
        return flexpool,rooster


class PersonUpdateView(UpdateView):
    template_name = 'beatrix/person_form.html'
    model = Person
    fields = ('name','email' , 'is_host', 'is_flex','keuzes',)
    # form_class = PersonForm
    success_url = reverse_lazy('beatrix:person_changelist')

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
              flexhost='Michiel',
              pub_date=datum2,
              pub_time=tijd2,
                # datum=datum2,
            # flexpoule='stedelijk', #'groep ' + str(j).zfill(2),
                )
            # print(t,datum2,tijd2)
    # ch1=Flexevent.objects.all().values_list('id',flat=True)
    # x=0
    p=Person.objects.all().first()
    f=Flexevent.objects.first()
    Flexlid.objects.all().update_or_create(
    member=p, 
    flexevent=f,
    )
    # Flexevent.objects.all().update_or_create(
    # dagnaam=dagnaam, 
    # flexhost='Michiel',
    # pub_date=date.today(),
    # pub_time='10:00',
    # # flexpoule='stedelijk',
    # )

    return
