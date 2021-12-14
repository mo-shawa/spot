from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),    
    path('accounts/profile/', views.profile_detail, name='profile_detail'),
    # DOG PATHS
    path('dogs/create/',views.DogCreate.as_view(), name='dog_create'),
    path('accounts/profile/update/', views.profile_update, name='profile_update'),
    path('accounts/profile/profile-photo/', views.profile_photo, name="profile_photo"),
]