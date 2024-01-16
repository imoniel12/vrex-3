from django.contrib.auth.forms import UserCreationForm

from django import forms 

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser
from .models import SchoolForm
from .models import Message


#--Register/ Create a user

class CreateUserForm(UserCreationForm):
    
    class Meta:

        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'sex', 'user_type', 'home_address', 'contact_number', 'email','username', 'password1', 'password2']

#--login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

#userform
class Createschoolform(forms.ModelForm):
    class Meta:
        model = SchoolForm  
        fields = ['first_name', 'middle_name', 'last_name', 'user_type', 'purpose', 'requestform','request_date', 'specialinstructions']
     


#calendar
class EventForm(forms.Form):
    title = forms.CharField(max_length=255)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


#chat
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']