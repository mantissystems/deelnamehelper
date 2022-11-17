from datetime import datetime
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
SCULL = [
            ('--', '--'),
            ('sc1', 'sc1'),
            ('sc2', 'sc2'),
            ('sc2a', 'sc2a'),
            ('sc3', 'sc3'),
            ('sc4', 'sc4'),
            ('b1', 'b1'),
            ('b2', 'b2'),
            ('b3', 'b3'),
            ('b4', 'b4'),
            ('st1', 'st1'),
            ('st2', 'st2'),
            ('st3', 'st3'),
]
DVDW = [
            ('--', '--'),
            ('0', 'maandag'),
            ('ma-wo', 'ma-wo'),
            ('ma-wo-vr', '0,3,4'),
]
TIJDBLOK = [
            ('--', '--'),
            ('1','09:00'),
            ('2','13:00'),
            ('3','17:30'),
]

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
    participants = models.ManyToManyField(User, related_name='participant', blank=True)
    updated = models.DateTimeField(auto_now=True) # everytime save (or updated) the field
    created = models.DateTimeField(auto_now_add=True) # first time created the field

    class Meta:
        ordering = ['-updated', '-created'] # ('-' for reverse the order)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # when room delete, delete all chiled messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)     

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=100)
    avatar=models.ImageField(null=True,default="avatar.svg")      # install Pillow is needed
    email = models.CharField(max_length=100,blank=True)
    is_flex = models.BooleanField(default=True)        #wil ingedeeld worden in flexpoule
    is_host = models.BooleanField(default=False)        #kan flexhost zijn
    keuzes = models.IntegerField(default=0) #aantal keren als host gekozen
    roeileeftijd = models.CharField(max_length=20,blank=True)
    is_lid= models.BooleanField(default=True)           #is roeiend lid;member
    in_poule = models.BooleanField(default=False)       #wil flexibel roeiern
    vaart = models.BooleanField(default=False)          #zit in ingedeelde boot op het water
    pos1 = models.CharField(max_length=18, choices=SCULL,default='sc1')  #aanbod vaardigheid om voorstel te berekenen voor wat nodig is aan in te delen boten
    pos2 = models.CharField(max_length=18, choices=SCULL,default='sc1') 
    pos3 = models.CharField(max_length=18, choices=SCULL,default='sc1') 
    pos4 = models.CharField(max_length=18, choices=SCULL,default='sc1') 
    pos5 = models.CharField(max_length=318, choices=SCULL,default='st1') 
    coach = models.CharField(max_length=18, choices=SCULL,default='st1')     
    keuzes = models.IntegerField(default=0) #aantal keren als host gekozen

    def __str__(self):
        return self.name

class Flexevent(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # host = models.ManyToManyField(User,through='Hosts')  ##, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,null=True) ##SET_NULL, null=True)
    event_text = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
    pub_date = models.CharField(max_length=35)
    datum = models.DateField(auto_now=False)
    pub_time = models.CharField(max_length=35, default='10:00')
    lid = models.ManyToManyField(User, related_name='deelnemer', blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return "%s" % (self.event_text)               
class Flexlid(models.Model):
    flexevent = models.ForeignKey(Flexevent, on_delete=models.CASCADE,null=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    is_host = models.BooleanField(default=False)

    class Meta:
        ordering = ('member',)    
    def __str__(self):
        return "%s" % (self.flexevent)        


class Bericht(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Flexevent, on_delete=models.CASCADE) # when room delete, delete all chiled messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)     

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

# python .\manage.py makemigrations
# python .\manage.py migrate
class Flexrecurrent(models.Model):
    regels = models.CharField(max_length=18,default='30')

class Recurrent(models.Model):
    name = models.CharField(max_length=18,default='FlexibelRoeien')
    start=models.CharField(max_length=18,default='30')
    end=models.CharField(max_length=18,default='30')
    trainingsweken=models.CharField(max_length=18,default='4')
    onderwerp=models.CharField(max_length=18,default='flexroeien')
    dagvandeweek = models.CharField(max_length=18, choices=DVDW,default='0') 
    blok = models.CharField(max_length=18, choices=TIJDBLOK,default='1') 
    verwijder_oude_flexevents=models.BooleanField(default=True)
    resetsequence=models.BooleanField(default=True)
    verwijder_oude_onderwerpen=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



class Instromer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
