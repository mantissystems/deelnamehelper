from django.db import models
from django.contrib.auth.models import User

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

class Flexevent(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    event_text = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=35)
    pub_time = models.CharField(max_length=35)
    dagnaam = models.CharField(max_length=35, default='10:00')
    flexhost = models.CharField(max_length=135, default='-')
    lid = models.ManyToManyField(Person,through='Flexlid')  ##, on_delete=models.SET_NULL, null=True)
    # flexhost2 = models.CharField(max_length=135, default='-')
    # flexpoule = models.CharField(max_length=135, default='groep')
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

# python .\manage.py makemigrations
# python .\manage.py migrate