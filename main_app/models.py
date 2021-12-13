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
    image = models.CharField(max_length=200, blank=True)

    # friends = models.ManyToManyField(Profile)
    def __str__(self):
        return self.user.get_full_name()
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'user_id': self.user.id})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# hello
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Dog(models.Model): 
    name = models.CharField(max_length=100)
    birthday = models.DateField('BirthDay')
    breed = models.CharField(max_length=100)
    hobbies = models.TextField(max_length=200)
    fav_snack = models.CharField(max_length=100)
    bio = models.TextField(max_length=250)
    image = models.CharField(max_length=200, blank=True)
    age = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})


class Post(models.Model):
    creator = models.ForeignKey(Dog, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    image = models.CharField(max_length=200, blank=True)


class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"