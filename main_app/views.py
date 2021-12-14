from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.forms import ProfileForm, UserForm
import boto3
import uuid
from main_app.models import Dog, Profile, Photo


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'hellofren'


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
       return redirect('profile_detail')

  else:
        error_message = 'Invalid Inputs'

  profile_form = ProfileForm()
  context= {"profile_form": profile_form, 'error_message': error_message}
  
  return render(request, 'main_app/profile_form.html', context)
  

# class ProfileView(DetailView):
#   model = Profile

def profile_detail(request):
  return render(request, 'profile.html')

class DogCreate(LoginRequiredMixin,CreateView):
  print('here')
  model = Dog
  fields = ['name','birthday','breed','hobbies','fav_snack','bio','age']
  success_url = '/accounts/profile/'

  def form_valid(self,form):
    profile = Profile.objects.get(user = self.request.user.id)
    form.instance.profile = profile
    return super().form_valid(form)

def profile_photo(request, user_id):
  photo_file = request.FILES.get("photo-file", None)
  print("photofunc")
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
            
            profile = Profile.objects.get(user=user_id)
            profile_id = profile.id
            profile.image = url
            profile.save()
            print(profile)
            
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, profile=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
  return redirect('profile_detail')