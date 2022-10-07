from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


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
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,blank=True)
    is_flex = models.BooleanField(default=True)        #wil ingedeeld worden in flexpoule
    is_host = models.BooleanField(default=False)        #kan flexhost zijn
    keuzes = models.IntegerField(default=0) #aantal keren als host gekozen
    def __str__(self):
        return self.name

class Flexrecurrent(models.Model):
    freq = models.CharField(max_length=18, default='4')
    rule = models.CharField(max_length=18, default='w')
    pref = models.CharField(max_length=18, default='1')
    occ = models.CharField(max_length=18, default='w')
    recurr = models.CharField(max_length=18, default='w')
    coll = models.CharField(max_length=35, default='w')
    entrydate = models.CharField(max_length=35)
    startdate = models.CharField(max_length=35)
    datum = models.DateField(auto_now=False)
    plan_qty=models.DecimalField(max_digits=17,decimal_places=2,default=0)
    flex_name = models.CharField(max_length=35, default='flexpoule')

   
class Flexevent(models.Model):
    id = models.AutoField(primary_key=True)
    event_text = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=35)
    pub_time = models.CharField(max_length=35)
    dagnaam = models.CharField(max_length=35, default='10:00')
    flexhost = models.CharField(max_length=135, default='-')
    # flexhost2 = models.CharField(max_length=135, default='-')
    # flexpoule = models.CharField(max_length=135, default='groep')
    lid = models.ManyToManyField(Person,through='Flexlid')  ##, on_delete=models.SET_NULL, null=True)
    # datum = models.DateField(auto_now=False)

    def __str__(self):
        return "%s" % (self.event_text)               
class Flexlid(models.Model):
    flexevent = models.ForeignKey(Flexevent, on_delete=models.CASCADE,null=True)
    member = models.ForeignKey(Person, on_delete=models.CASCADE,null=True)
    is_host = models.BooleanField(default=False)

    class Meta:
        ordering = ('member',)    
    def __str__(self):
        return "%s" % (self.flexevent)    


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Deelnemer(models.Model):
    question = models.ForeignKey(Flexevent, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Boot(models.Model):
    bootnaam = models.CharField(max_length=35, default='0')
    flexhost = models.CharField(max_length=135, default='-')
    # prio = models.IntegerField(default=0)
    # seats = models.IntegerField(default=0)
    # boottype = models.ForeignKey(Boottype, on_delete=models.CASCADE)
    # stuur = models.CharField(max_length=35, default='st1')
    # slag = models.CharField(max_length=35, default='sc1')
    # twee = models.CharField(max_length=35, default='sc1')
    # drie = models.CharField(max_length=35, default='sc1')
    # boeg = models.CharField(max_length=35, default='sc1')
    beschikbaar = models.BooleanField(default=True,null=True)
    # indevaart = models.BooleanField(default=True,null=True)
    indeling = models.TextField(blank=True)
    def __str__(self):
        return "%s" % (self.bootnaam)    

