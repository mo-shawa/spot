from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=7)
    bio = models.TextField(max_length=250)
    # friends = models.ManyToManyField(Profile)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Dog(models.Model): 
    name = models.CharField(max_length=100)
    birthday = models.DateField('BirthDay')
    breed = models.CharField(max_length=100)
    hobbies = models.TextField(max_length=200)
    fav_snack = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=7)
    bio = models.TextField(max_length=250)
    
    age = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})

class Post(models.Model):
    creator = models.ForeignKey(Dog, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    image = models.CharField(max_length=200)
