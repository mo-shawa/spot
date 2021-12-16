from django.http import request
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.forms import ProfileForm, UserForm, CommentForm
import boto3
import uuid
from main_app.models import Comment, Dog, Profile, Photo, Post
from django.urls import reverse_lazy


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'hellofren'

class PostList(ListView):
  model = Post

# class PostDetail(LoginRequiredMixin, DetailView):
#   model = Post

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  comment_form = CommentForm
  return render(request,'main_app/post_detail.html',{'post':post, 'form': comment_form})


class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['image','text']

class PostDelete(LoginRequiredMixin,DeleteView):
  model = Post
  success_url = '/posts/'

@login_required
def comment_create(request,post_id):
  form = CommentForm(request.POST)
  if form.is_valid:
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.author_id = request.user.id
    new_comment.save()
  return redirect ('post_detail',post_id=post_id)


# class CommentCreate(LoginRequiredMixin,CreateView):
#   model = Comment


def home(request):
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    user_form = UserForm(request.POST)
    if user_form.is_valid():
      user = user_form.save()
      login(request, user)
      return redirect('profile_update')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserForm()
  context = {'user_form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = "__all__"

def profile_update(request):
  error_message = ''
  
  if request.method == 'POST':
     profile_form = ProfileForm(request.POST, instance=request.user.profile)
     if profile_form.is_valid():
       profile_form.save()
       profile_photo(request)
       return redirect('profile_detail', profile_id = request.user.profile.id)

  else:
        error_message = 'Invalid Inputs'

  profile_form = ProfileForm(instance=request.user.profile)
  context= {"profile_form": profile_form, 'error_message': error_message}
  
  return render(request, 'main_app/profile_form.html', context)
  

# class ProfileView(DetailView):
#   model = Profile

def profile_detail(request, profile_id):
  profile = Profile.objects.get(id = profile_id)
  return render(request, 'profile.html', {'profile':profile})

class DogCreate(LoginRequiredMixin,CreateView):
  model = Dog
  fields = ['name','birthday','breed','hobbies','fav_snack','bio','age']
  # success_url = '/accounts/profile/'

  def form_valid(self,form):
    profile = Profile.objects.get(user = self.request.user.id)
    form.instance.profile = profile
    return super().form_valid(form)

def dog_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  return render(request, 'dog_profile.html', {'profile':dog})

class DogDelete(LoginRequiredMixin,DeleteView):
  model = Dog
  
  def get_success_url(self):
      return reverse_lazy('profile_detail', kwargs={'profile_id': self.request.user.id})


def profile_photo(request):
  photo_file = request.FILES.get("photo-file", None)
  print("photofunc")
  # form.instance.user.profile = self.request.user.profile
  user = request.user.id
  print(user)
  if photo_file:
        print("photofile")
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            
            profile = Profile.objects.get(user=user)
            profile_id = profile.id
            profile.image = url
            profile.save()
            print(profile)
            
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, profile=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
  return redirect('profile_detail', profile_id= request.user.profile.id)

def post_photo(request):
  photo_file = request.FILES.get("photo-file", None)
  print("in post photo function: ",request.POST)
  # form.instance.user.profile = self.request.user.profile
  user = request.user.id
  print(user)
  if photo_file:
        print("photofile")
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"      
            
            
          
            return url
        except:
            print('An error occurred uploading file to S3')
  return redirect('profile_detail')

def post_create(request):
  print(request.POST)
  
  print("profile_id", )
  dog = Dog.objects.get(id=request.POST["creator"])
  print(dog)
  post = Post.objects.create(creator=dog, text=request.POST["text"])
  url = post_photo(request)
  post.image = url
  post.save()
  photo = Photo(url=url, dog=dog, post=post, profile=dog.profile)
  photo.save()
  

  return redirect('post_list')