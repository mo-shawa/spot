from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/<int:user_id>/', views.ProfileCreate.as_view(), name="profile_create")
]