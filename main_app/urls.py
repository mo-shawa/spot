from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/<int:user_id>/', views.ProfileCreate.as_view(), name="profile_create"),
    path('accounts/<int:user_id>', views.profile_detail, name='profile_detail'),
    # DOG PATHS
    path('dogs/create/',views.DogCreate.as_view(), name='dog_create'),
    path('accounts/<int:user_id>/update', views.profile_update, name='profile_update')
]