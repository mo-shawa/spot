from django.forms import ModelForm
from .models import User, Dog, Profile

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password' ]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ 'bio', 'postal_code']