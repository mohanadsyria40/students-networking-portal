from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


CustomUser = get_user_model()

class StudentRegistrationForm(UserCreationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  studentId = forms.CharField(max_length=20, label='Student ID', widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
  first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  
  
  class Meta:
    model = CustomUser
    fields = ['username', 'studentId', 'email', 'first_name', 'last_name',  'password1', 'password2']

  
class StudentLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  
  class Meta:
    model = CustomUser  
    fields = ['username', 'password']
    
    
    
class UserUpdateForm(forms.ModelForm):

    
  class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        

class ProfileUpdateForm(forms.ModelForm):

    
  class Meta:
        model = Profile
        fields = ['grade', 'description']