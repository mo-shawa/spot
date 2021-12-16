from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Comment, User, Dog, Profile

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2' ]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ 'bio', 'postal_code']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':2}),
        }
