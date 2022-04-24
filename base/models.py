from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

BLOOD = (
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B+'),
    ('AB+','AB+'),
    ('AB-','AB-'),
    ('O+','O+'),
    ('O-','O-'),
)

GENDER = (
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)

FREQUENCY = (
    ('Weekly','Weekly'),
    ('Monthly','Monthly'),
    ('Yearly','Yearly'),
    ('Once in a Year','Once in a Year'),
    ('Once in a Lifetime','Once in a Lifetime')
)

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")
    blood = models.CharField(max_length=20,choices=BLOOD,null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=20,choices=GENDER,null=True)
    height = models.FloatField(null=True)
    cellphone = models.BigIntegerField(null=True)
    address = models.CharField(max_length=255,null=True)
    occupation = models.CharField(max_length=255,null=True)
    blood_given = models.BooleanField(null=True)
    frequency = models.CharField(max_length=255,choices=FREQUENCY,null=True,help_text="How frequently you donate blood?")
    smoke = models.BooleanField(null=True)
    report = models.FileField(upload_to='documents',null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    name = models.CharField(max_length=200)
    cause = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]
