from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth.models import User
from django import forms 
from django.forms.widgets import PasswordInput, TextInput

#Register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
       
# Update LoginForm class
class LoginForm(AuthenticationForm):
    # No need for Meta class, directly define fields
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))