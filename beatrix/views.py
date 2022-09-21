from django.shortcuts import render
import datetime
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from beatrix.models import Flexevent,Flexlid,Flexrecurrent,Person
from django.views.generic import(ListView)

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
    # template_name='person/personlistview.html'
    # template_name='person/aanmeldview.html'
    def get_context_data(self, **kwargs):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        # sql="select id, name,substr(name,1,1) HL from person_person GROUP BY substr(name,1,1) order by HL"
        # cursor = connection.cursor() 
        # cursor.execute(sql)
        # results = recurrent.namedtuplefetchall(cursor)
        rooster = Flexevent.objects.all()

        context={
        # 'hoofdletters':results,
        # 'object_list':results,
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
        results=flexpool
        # template_name='beatrix/aanmeldview.html'
        return results