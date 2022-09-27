from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,blank=True)
    is_flex = models.BooleanField(default=True)        #wil ingedeeld worden in flexpoule
    # is_host = models.BooleanField(default=False)        #kan flexhost zijn
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
