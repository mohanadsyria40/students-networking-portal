from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Student



class StudentRegistrationForm(UserCreationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  studentId = forms.CharField(max_length=20, label='Student ID', widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
  first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  
  
  class Meta:
    model = User
    fields = ['username', 'studentId', 'email', 'first_name', 'last_name',  'password1', 'password2']

  # def clean_studentId(self):
  #   studentId = self.cleaned_data['studentId']
  #   if Student.objects.filter(studentId=studentId).exists():
  #       raise forms.ValidationError("Student ID already exists")
  #   return studentId

  # def clean_username(self):
  #   username = self.cleaned_data['username']
  #   if User.objects.filter(username=username).exists():
  #       raise forms.ValidationError("Username already exists")
  #   return username
  
  
class StudentLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  
  class Meta:
    fields = ['username', 'password']