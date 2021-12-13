from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.forms import ProfileForm
from main_app.models import Dog, Profile

# Create your views here.

def home(request):
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    user_form = UserCreationForm(request.POST)
    if user_form.is_valid():
      user = user_form.save()
      login(request, user)
      return redirect('profile_update')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'user_form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = "__all__"

def profile_update(request):
  profile_form = ProfileForm() 
  context= {"profile_form": profile_form}
  return render(request, 'main_app/profile_form.html', context)


# class ProfileView(DetailView):
#   model = Profile

def profile_detail(request, user_id):
  return render(request, 'profile.html')

class DogCreate(LoginRequiredMixin,CreateView):
  model = Dog
  # fields = ['name','birthday','breed','hobbies','fav_snack','hobbies',]
  fields = '__all__'

  def form_valid(self,form):
    form.instance.user.profile = self.request.user.profile
    return super().form_valid(form)