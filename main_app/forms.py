from django.forms import ModelForm
from .models import User, Dog

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password' ]