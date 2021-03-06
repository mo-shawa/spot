from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # ACCOUNT PATHS
    path('accounts/signup/', views.signup, name='signup'),    
    path('accounts/profile/<int:profile_id>', views.profile_detail, name='profile_detail'),
    path('accounts/profile/update/', views.profile_update, name='profile_update'),
    path('accounts/profile/profile-photo/', views.profile_photo, name="profile_photo"),
    # DOG PATHS
    path('dogs/create/',views.DogCreate.as_view(), name='dog_create'),
    path('dogs/<int:dog_id>',views.dog_detail, name='dog_detail'),
    path('dogs/<int:pk>/delete', views.DogDelete.as_view(),name='dog_delete'),
    path('dogs/<int:dog_id>/update', views.dog_update,name='dog_update'),
    # POST PATHS
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/create', views.post_create, name='post_create'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete', views.PostDelete.as_view() ,name='post_delete'),
    # COMMENT PATHS
    path('posts/<int:post_id>/comment',views.comment_create, name='comment_create')
]